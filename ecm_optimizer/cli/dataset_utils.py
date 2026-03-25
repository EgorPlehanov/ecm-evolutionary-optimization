from __future__ import annotations

import re
from pathlib import Path

import click

from ecm_optimizer.config import NUMBERS_DIR
from ecm_optimizer.core.problem import read_dataset_metadata


def resolve_dataset_path(dataset_ref: str | None, *, expected_file: str) -> Path:
    """Resolve dataset reference from file path, directory path, or latest generated dataset."""
    if dataset_ref is None:
        latest_dir = _latest_generated_dataset_dir(expected_file=expected_file)
        if latest_dir is None:
            raise click.UsageError(
                f"No generated datasets found in {NUMBERS_DIR}. Generate one first or pass --dataset explicitly."
            )
        return latest_dir / expected_file

    ref = Path(dataset_ref)

    if ref.exists() and ref.is_file():
        return ref

    if ref.exists() and ref.is_dir():
        candidate = ref / expected_file
        if candidate.exists() and candidate.is_file():
            return candidate
        raise click.UsageError(f"Expected dataset file '{expected_file}' inside directory: {ref}")

    if ref.suffix:
        raise click.UsageError(f"Dataset file not found: {ref}")

    candidate = NUMBERS_DIR / ref / expected_file
    if candidate.exists() and candidate.is_file():
        return candidate

    raise click.UsageError(
        f"Cannot resolve dataset '{dataset_ref}'. Pass full file path or generated folder name under {NUMBERS_DIR}."
    )


def dataset_generation_seed(dataset_path: Path, *, fallback: int) -> int:
    """Read generation seed from dataset metadata and return fallback on missing/invalid value."""
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("seed")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


def _latest_generated_dataset_dir(*, expected_file: str) -> Path | None:
    if not NUMBERS_DIR.exists():
        return None

    candidates = [
        d for d in NUMBERS_DIR.iterdir()
        if d.is_dir() and (d / expected_file).exists() and (d / 'generation.json').exists()
    ]
    if not candidates:
        return None

    candidates_with_ts = [(d, _trailing_timestamp(d.name)) for d in candidates]
    candidates_with_ts = [(d, ts) for d, ts in candidates_with_ts if ts is not None]
    if not candidates_with_ts:
        return None

    return max(candidates_with_ts, key=lambda item: item[1])[0]


def resolve_opt_result_file(
    opt_result_ref: str | None,
    *,
    dataset_path: Path,
    results_dir: Path,
) -> Path:
    """Resolve optimization result JSON by absolute/relative path, dataset-local file name, or latest file."""
    dataset_name = dataset_path.parent.name
    dataset_results_dir = results_dir / dataset_name

    if opt_result_ref is None:
        latest = _latest_opt_result_file(dataset_results_dir)
        if latest is None:
            raise click.UsageError(
                f"No optimization result files found in {dataset_results_dir}. "
                "Run optimize first, pass --opt-result-file, or provide --opt-b1 and --opt-b2."
            )
        return latest

    ref = Path(opt_result_ref)
    if ref.exists() and ref.is_file():
        return ref

    candidate = dataset_results_dir / ref.name
    if candidate.exists() and candidate.is_file():
        return candidate

    raise click.UsageError(
        f"Cannot resolve optimization result '{opt_result_ref}'. "
        "Pass a valid file path or file name inside the current dataset experiments folder."
    )


def _latest_opt_result_file(dataset_results_dir: Path) -> Path | None:
    if not dataset_results_dir.exists() or not dataset_results_dir.is_dir():
        return None

    candidates = [
        p for p in dataset_results_dir.iterdir()
        if p.is_file() and p.suffix.lower() == ".json" and p.name.startswith("optimize_")
    ]
    if not candidates:
        return None

    candidates_with_ts = [(p, _trailing_timestamp(p.stem)) for p in candidates]
    candidates_with_ts = [(p, ts) for p, ts in candidates_with_ts if ts is not None]
    if not candidates_with_ts:
        return None

    return max(candidates_with_ts, key=lambda item: item[1])[0]


TIMESTAMP_RE = re.compile(r"^\d{8}T\d{6}Z$")


def _trailing_timestamp(name: str) -> str | None:
    parts = name.rsplit("_", 1)
    if len(parts) != 2:
        return None
    ts = parts[1]
    if TIMESTAMP_RE.match(ts):
        return ts
    return None
