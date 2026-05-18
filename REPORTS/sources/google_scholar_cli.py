from __future__ import annotations

import argparse
import json
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urljoin
from urllib.request import Request, urlopen


SCHOLAR_BASE_URL = "https://scholar.google.com"
SCHOLAR_SEARCH_URL = f"{SCHOLAR_BASE_URL}/scholar"
DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/124.0 Safari/537.36"
)


def slugify_filename(value: str, *, max_length: int = 120) -> str:
    slug = re.sub(r"[^\w\s.-]+", "", value, flags=re.UNICODE)
    slug = re.sub(r"\s+", "_", slug.strip(), flags=re.UNICODE)
    slug = slug.strip("._")
    if not slug:
        slug = "scholar_query"
    return slug[:max_length].rstrip("._") or "scholar_query"


def resolve_output_path(output: Path, query: str) -> Path:
    filename = f"{slugify_filename(query)}.json"
    if output.exists() and output.is_dir():
        return output / filename
    if output.suffix.lower() != ".json":
        return output / filename
    return output


@dataclass
class HtmlNode:
    tag: str
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["HtmlNode"] = field(default_factory=list)
    text_parts: list[str] = field(default_factory=list)


class TreeBuilder(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = HtmlNode("document")
        self.stack = [self.root]

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = HtmlNode(tag=tag, attrs={key: value or "" for key, value in attrs})
        self.stack[-1].children.append(node)
        self.stack.append(node)

    def handle_endtag(self, tag: str) -> None:
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == tag:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].text_parts.append(data)


def normalize_ws(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def text_content(node: HtmlNode | None) -> str | None:
    if node is None:
        return None
    parts: list[str] = []

    def visit(current: HtmlNode) -> None:
        parts.extend(current.text_parts)
        for child in current.children:
            visit(child)

    visit(node)
    return normalize_ws(" ".join(parts))


def classes(node: HtmlNode) -> set[str]:
    return set(node.attrs.get("class", "").split())


def has_classes(node: HtmlNode, *required: str) -> bool:
    node_classes = classes(node)
    return all(item in node_classes for item in required)


def walk(node: HtmlNode) -> list[HtmlNode]:
    nodes = [node]
    for child in node.children:
        nodes.extend(walk(child))
    return nodes


def first_descendant(node: HtmlNode | None, tag: str | None = None, *required_classes: str) -> HtmlNode | None:
    if node is None:
        return None
    for item in walk(node):
        if tag is not None and item.tag != tag:
            continue
        if required_classes and not has_classes(item, *required_classes):
            continue
        return item
    return None


def descendants(node: HtmlNode | None, tag: str | None = None, *required_classes: str) -> list[HtmlNode]:
    if node is None:
        return []
    items = []
    for item in walk(node):
        if tag is not None and item.tag != tag:
            continue
        if required_classes and not has_classes(item, *required_classes):
            continue
        items.append(item)
    return items


def absolutize(url: str | None) -> str | None:
    if not url:
        return None
    return urljoin(SCHOLAR_BASE_URL, url)


def extract_first_link(node: HtmlNode | None) -> tuple[str | None, str | None]:
    link = first_descendant(node, "a")
    if link is None:
        return None, None
    return text_content(link), absolutize(link.attrs.get("href"))


def parse_cited_by(text: str) -> int | None:
    match = re.search(r"Cited by\s+(\d+)", text, flags=re.IGNORECASE)
    return int(match.group(1)) if match else None


def parse_footer_links(result_node: HtmlNode) -> dict[str, Any]:
    footer = first_descendant(result_node, "div", "gs_fl")
    parsed: dict[str, Any] = {
        "cited_by_count": None,
        "cited_by_url": None,
        "related_url": None,
        "versions_count": None,
        "versions_url": None,
        "cached_url": None,
        "other_links": [],
    }

    for link in descendants(footer, "a"):
        label = text_content(link) or ""
        href = absolutize(link.attrs.get("href"))
        cited_by = parse_cited_by(label)
        versions = re.search(r"All\s+(\d+)\s+versions", label, flags=re.IGNORECASE)
        lower = label.lower()

        if cited_by is not None:
            parsed["cited_by_count"] = cited_by
            parsed["cited_by_url"] = href
        elif "related" in lower:
            parsed["related_url"] = href
        elif versions:
            parsed["versions_count"] = int(versions.group(1))
            parsed["versions_url"] = href
        elif "cached" in lower:
            parsed["cached_url"] = href
        else:
            parsed["other_links"].append({"label": label, "url": href})

    return parsed


def parse_result(result_node: HtmlNode, rank: int) -> dict[str, Any]:
    title_node = first_descendant(result_node, "h3", "gs_rt")
    title, url = extract_first_link(title_node)
    if title is None:
        title = text_content(title_node)

    pdf_title, pdf_url = extract_first_link(first_descendant(result_node, "div", "gs_or_ggsm"))
    return {
        "rank": rank,
        "title": title,
        "url": url,
        "publication_info": text_content(first_descendant(result_node, "div", "gs_a")),
        "snippet": text_content(first_descendant(result_node, "div", "gs_rs")),
        "pdf": {"label": pdf_title, "url": pdf_url} if pdf_url else None,
        **parse_footer_links(result_node),
    }


def parse_scholar_html(html: str, *, offset: int = 0) -> dict[str, Any]:
    parser = TreeBuilder()
    parser.feed(html)
    result_nodes = [
        node
        for node in walk(parser.root)
        if node.tag == "div" and has_classes(node, "gs_r") and has_classes(node, "gs_or")
    ]
    return {
        "records": [parse_result(node, offset + index + 1) for index, node in enumerate(result_nodes)],
        "diagnostics": {
            "result_nodes_found": len(result_nodes),
            "captcha_or_block_detected": "sorry/index" in html or "unusual traffic" in html.lower(),
        },
    }


def fetch_page(query: str, *, start: int, hl: str, timeout: float, user_agent: str) -> tuple[str, str]:
    url = f"{SCHOLAR_SEARCH_URL}?{urlencode({'q': query, 'hl': hl, 'start': start})}"
    request = Request(
        url,
        headers={
            "User-Agent": user_agent,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": f"{hl},en;q=0.8",
        },
    )
    with urlopen(request, timeout=timeout) as response:
        charset = response.headers.get_content_charset() or "utf-8"
        return response.read().decode(charset, errors="replace"), url


def scholar_search(query: str, *, limit: int, hl: str, timeout: float, delay: float, user_agent: str) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    pages: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []
    start = 0

    while len(records) < limit:
        try:
            html, url = fetch_page(query, start=start, hl=hl, timeout=timeout, user_agent=user_agent)
            parsed = parse_scholar_html(html, offset=start)
        except HTTPError as exc:
            errors.append({"type": "http_error", "status": exc.code, "reason": exc.reason, "start": start})
            break
        except URLError as exc:
            errors.append({"type": "url_error", "reason": str(exc.reason), "start": start})
            break
        except TimeoutError as exc:
            errors.append({"type": "timeout", "reason": str(exc), "start": start})
            break

        page_records = parsed["records"]
        pages.append({"start": start, "url": url, "records_found": len(page_records), "diagnostics": parsed["diagnostics"]})

        for record in page_records:
            if len(records) >= limit:
                break
            records.append(record)

        if parsed["diagnostics"]["captcha_or_block_detected"]:
            errors.append({"type": "captcha_or_block", "message": "Google Scholar returned a captcha/block page.", "start": start})
            break
        if not page_records:
            break

        start += 10
        if len(records) < limit and delay > 0:
            time.sleep(delay)

    return {
        "metadata": {
            "source": SCHOLAR_SEARCH_URL,
            "query": query,
            "requested_limit": limit,
            "saved_records": len(records),
            "hl": hl,
            "created_at_utc": datetime.now(timezone.utc).isoformat(),
        },
        "pages": pages,
        "records": records,
        "errors": errors,
    }


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def positive_int(value: str) -> int:
    parsed = int(value)
    if parsed <= 0:
        raise argparse.ArgumentTypeError("value must be positive")
    return parsed


def non_negative_float(value: str) -> float:
    parsed = float(value)
    if parsed < 0:
        raise argparse.ArgumentTypeError("value must be non-negative")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Fetch the first N Google Scholar records for a query and save a structured JSON file."
    )
    parser.add_argument("-q", "--query", required=True, help="Search query.")
    parser.add_argument("-n", "--limit", type=positive_int, default=10, help="Number of records to save.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        required=True,
        help="Output JSON file or output directory. If a directory/path without .json is given, <query>.json is used.",
    )
    parser.add_argument("--hl", default="en", help="Google Scholar interface language, for example en or ru.")
    parser.add_argument("--timeout", type=non_negative_float, default=20.0, help="HTTP request timeout in seconds.")
    parser.add_argument("--delay", type=non_negative_float, default=2.0, help="Delay between result pages in seconds.")
    parser.add_argument("--user-agent", default=DEFAULT_USER_AGENT, help="HTTP User-Agent header.")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    output_path = resolve_output_path(args.output, args.query)
    payload = scholar_search(
        args.query,
        limit=args.limit,
        hl=args.hl,
        timeout=args.timeout,
        delay=args.delay,
        user_agent=args.user_agent,
    )
    write_json(output_path, payload)

    if payload["errors"]:
        print(f"saved {payload['metadata']['saved_records']} records with warnings to {output_path}", file=sys.stderr)
        for error in payload["errors"]:
            print(f"warning: {error}", file=sys.stderr)
        return 2

    print(f"saved {payload['metadata']['saved_records']} records to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
