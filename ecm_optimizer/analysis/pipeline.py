from __future__ import annotations

import csv
import json
import math
import os
import re
from urllib.parse import quote
from dataclasses import dataclass
from fnmatch import fnmatch
from pathlib import Path
from typing import Any

from ecm_optimizer.analysis.stats import (
    bootstrap_ci,
    cliffs_delta,
    coefficient_of_variation,
    effect_size_label,
    kruskal_wallis,
    levene_test,
    pairwise_mannwhitney,
    pairwise_win_rate,
    success_rate,
)
from ecm_optimizer.utils.io_utils import ensure_dir, read_json, utc_timestamp, write_json_with_meta

_DATASET_RE = re.compile(r"^(\d+)_dset_")
_METHODS = {"de", "rs", "pso", "bo", "ga"}
_DEFAULT_GROUP_PRIORITY = ("divisor_size", "dataset", "method", "seed")


def _load_matplotlib_pyplot():
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except ModuleNotFoundError:
        return None


@dataclass(frozen=True)
class RunRecord:
    run_file: Path
    validation_file: Path | None
    dataset: str
    dataset_file: Path | None
    divisor_size: int | None
    method: str
    seed: int | None
    final_objective: float
    evaluation_count: int
    total_runtime_sec: float
    time_to_best_sec: float | None
    first_fitness: float | None
    best_so_far_by_eval: list[tuple[int, float]]
    best_so_far_by_time: list[tuple[float, float]]
    validation_baseline_mean: float | None
    validation_optimized_mean: float | None
    validation_relative_improvement_pct: float | None


@dataclass(frozen=True)
class AnalysisOptions:
    success_threshold: float | None
    max_eval_points: int
    max_time_points: int
    group_by: tuple[str, ...]
    auto_grouping: bool
    max_series_per_plot: int
    bootstrap_iterations: int
    alpha: float


@dataclass(frozen=True)
class AnalysisArtifacts:
    output_dir: Path
    overview_report: Path
    summary_file: Path
    total_runs: int
    group_by: list[str]


@dataclass
class GroupNode:
    key: str
    value: str
    level: int
    runs: list[RunRecord]
    children: dict[str, "GroupNode"]


@dataclass(frozen=True)
class NodeArtifacts:
    report_file: Path
    tables: dict[str, Path]
    plots: dict[str, Path]
    decision_summary: dict[str, Any]


@dataclass(frozen=True)
class _SummaryStats:
    run_count: int
    median_objective: float
    iqr_objective: float
    median_time_sec: float
    median_time_to_best_sec: float | None
    median_eval_count: float
    success_share: float
    median_improvement_per_eval: float | None
    median_improvement_per_sec: float | None
    median_validation_gain_abs: float | None
    median_validation_gain_pct: float | None


def _tables_loader_src(report_dir: Path) -> str:
    repo_root = Path(__file__).resolve().parents[2]
    loader_path = repo_root / "ecm_optimizer" / "analysis" / "tables-loader.js"
    return os.path.relpath(loader_path, start=report_dir).replace(os.sep, "/")


def _split_include_exclude_inputs(input_entries: list[str]) -> tuple[list[str], list[str]]:
    include_entries: list[str] = []
    exclude_entries: list[str] = []
    for entry in input_entries:
        stripped = entry.strip()
        if not stripped:
            continue
        if stripped.startswith("!") and len(stripped) > 1:
            exclude_entries.append(stripped[1:])
        else:
            include_entries.append(stripped)
    return include_entries, exclude_entries


def _discover_run_files(inputs: list[Path], experiments_root: Path) -> list[Path]:
    start_points = inputs or [experiments_root]
    run_files: list[Path] = []

    for raw_path in start_points:
        path = raw_path.expanduser().resolve()
        if path.is_file():
            if path.name.endswith(".json") and "_optimize_" in path.name:
                run_files.append(path)
            continue

        if not path.is_dir():
            continue

        if path.name.startswith("optimize_"):
            run_files.extend(sorted(x for x in path.glob("*_optimize_*.json") if x.is_file()))
            continue

        run_files.extend(sorted(x for x in path.rglob("*_optimize_*.json") if x.is_file()))

    return sorted({p.resolve() for p in run_files})


def _matches_exclusion_rule(run_file: Path, rule: str) -> bool:
    candidate = Path(rule).expanduser()
    if candidate.exists():
        resolved_candidate = candidate.resolve()
        if resolved_candidate.is_file():
            return run_file == resolved_candidate
        return run_file.is_relative_to(resolved_candidate)

    run_path = str(run_file)
    return fnmatch(run_path, rule) or fnmatch(run_file.name, rule) or (rule in run_path) or (rule in run_file.name)


def _parse_divisor_size(dataset_name: str) -> int | None:
    match = _DATASET_RE.match(dataset_name)
    return int(match.group(1)) if match else None


def _extract_best_so_far(history: list[dict[str, Any]]) -> tuple[list[tuple[int, float]], list[tuple[float, float]], float | None]:
    evaluation_events = [event for event in history if event.get("kind") == "evaluation"]
    if not evaluation_events:
        return [], [], None

    by_eval: list[tuple[int, float]] = []
    by_time: list[tuple[float, float]] = []
    current_best: float | None = None
    first_fitness: float | None = None

    for event in evaluation_events:
        eval_id = int(event.get("eval", len(by_eval) + 1))
        fitness = float(event["fitness"])
        elapsed = float(event.get("elapsed_sec", 0.0))
        if first_fitness is None:
            first_fitness = fitness
        if current_best is None or fitness < current_best:
            current_best = fitness
        by_eval.append((eval_id, current_best))
        by_time.append((elapsed, current_best))

    return by_eval, by_time, first_fitness


def _find_validation_file(run_file: Path, method: str) -> Path | None:
    match = re.search(r"_optimize_(\d{8}T\d{6}Z)", run_file.name)
    if not match:
        return None
    ts = match.group(1)
    candidate = run_file.parent / f"{method}_validate_{ts}.json"
    if candidate.exists():
        return candidate

    fallback = sorted(run_file.parent.glob(f"{method}_validate_*.json"))
    return fallback[-1] if fallback else None


def _parse_run_file(run_file: Path) -> RunRecord | None:
    payload = read_json(run_file)
    optimized = payload.get("optimized", {})
    run_stats = payload.get("run_stats", {})
    history = payload.get("optimization_trace", [])

    if not isinstance(optimized, dict) or "objective" not in optimized:
        return None

    method = str(optimized.get("method", payload.get("config", {}).get("method", "unknown"))).lower()
    if method not in _METHODS:
        method = "unknown"

    dataset_path = Path(payload.get("dataset", "unknown"))
    dataset = dataset_path.parent.name if dataset_path.parent.name else str(dataset_path)
    dataset_file = dataset_path if str(dataset_path) != "unknown" else None
    divisor_size = _parse_divisor_size(dataset)

    best_eval, best_time, first_fitness = _extract_best_so_far(history if isinstance(history, list) else [])

    validation_file = _find_validation_file(run_file, method)
    validation_baseline_mean: float | None = None
    validation_optimized_mean: float | None = None
    validation_relative_improvement_pct: float | None = None

    if validation_file:
        validation_payload = read_json(validation_file)
        metrics = validation_payload.get("metrics", {})
        if isinstance(metrics, dict):
            baseline_mean = metrics.get("baseline_mean_score", metrics.get("baseline_mean"))
            optimized_mean = metrics.get("optimized_mean_score", metrics.get("optimized_mean"))
            relative = metrics.get("relative_improvement_pct")
            validation_baseline_mean = float(baseline_mean) if baseline_mean is not None else None
            validation_optimized_mean = float(optimized_mean) if optimized_mean is not None else None
            validation_relative_improvement_pct = float(relative) if relative is not None else None

    return RunRecord(
        run_file=run_file,
        validation_file=validation_file,
        dataset=dataset,
        dataset_file=dataset_file,
        divisor_size=divisor_size,
        method=method,
        seed=payload.get("config", {}).get("seed"),
        final_objective=float(optimized["objective"]),
        evaluation_count=int(run_stats.get("evaluation_count", len(best_eval)) or len(best_eval)),
        total_runtime_sec=float(run_stats.get("total_runtime_sec", 0.0) or 0.0),
        time_to_best_sec=float(run_stats["time_to_best_sec"]) if run_stats.get("time_to_best_sec") is not None else None,
        first_fitness=first_fitness,
        best_so_far_by_eval=best_eval,
        best_so_far_by_time=best_time,
        validation_baseline_mean=validation_baseline_mean,
        validation_optimized_mean=validation_optimized_mean,
        validation_relative_improvement_pct=validation_relative_improvement_pct,
    )


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return math.nan
    if len(ordered) == 1:
        return ordered[0]
    idx = (len(ordered) - 1) * q
    left = math.floor(idx)
    right = math.ceil(idx)
    if left == right:
        return ordered[left]
    frac = idx - left
    return ordered[left] * (1.0 - frac) + ordered[right] * frac


def _iqr(values: list[float]) -> float:
    return _quantile(values, 0.75) - _quantile(values, 0.25) if values else math.nan


def _safe_slug(value: str) -> str:
    text = value.strip().replace(" ", "_")
    return re.sub(r"[^0-9a-zA-Z_=.-]+", "_", text)


def _project_relative(path: Path) -> str:
    try:
        return str(path.resolve().relative_to(Path.cwd().resolve()))
    except ValueError:
        return str(path.resolve())


def _dimension_value(run: RunRecord, key: str) -> str:
    if key == "divisor_size":
        return str(run.divisor_size) if run.divisor_size is not None else "unknown"
    if key == "dataset":
        return run.dataset
    if key == "method":
        return run.method
    if key == "seed":
        return str(run.seed) if run.seed is not None else "unknown"
    raise ValueError(f"Unsupported group key: {key}")


def _auto_group_order(runs: list[RunRecord]) -> tuple[str, ...]:
    ordered: list[str] = []
    for key in _DEFAULT_GROUP_PRIORITY:
        unique_values = {_dimension_value(run, key) for run in runs}
        if len(unique_values) > 1:
            ordered.append(key)
    return tuple(ordered)


def _stats_for_runs(runs: list[RunRecord], threshold: float) -> _SummaryStats:
    finals = [run.final_objective for run in runs]
    runtimes = [run.total_runtime_sec for run in runs]
    eval_counts = [run.evaluation_count for run in runs]
    time_to_best = [run.time_to_best_sec for run in runs if run.time_to_best_sec is not None]

    imp_eval: list[float] = []
    imp_sec: list[float] = []
    validation_gain_abs: list[float] = []
    validation_gain_pct: list[float] = []

    success_values: list[float] = []
    for run in runs:
        if run.first_fitness is not None:
            improvement = run.first_fitness - run.final_objective
            if run.evaluation_count > 0:
                imp_eval.append(improvement / run.evaluation_count)
            if run.total_runtime_sec > 0:
                imp_sec.append(improvement / run.total_runtime_sec)

        run_best = min((best for _, best in run.best_so_far_by_eval), default=math.inf)
        success_values.append(run_best)

        if run.validation_baseline_mean is not None and run.validation_optimized_mean is not None:
            validation_gain_abs.append(run.validation_baseline_mean - run.validation_optimized_mean)
        if run.validation_relative_improvement_pct is not None:
            validation_gain_pct.append(run.validation_relative_improvement_pct)

    return _SummaryStats(
        run_count=len(runs),
        median_objective=_quantile(finals, 0.5),
        iqr_objective=_iqr(finals),
        median_time_sec=_quantile(runtimes, 0.5),
        median_time_to_best_sec=_quantile(time_to_best, 0.5) if time_to_best else None,
        median_eval_count=_quantile(eval_counts, 0.5),
        success_share=success_rate(success_values, threshold),
        median_improvement_per_eval=_quantile(imp_eval, 0.5) if imp_eval else None,
        median_improvement_per_sec=_quantile(imp_sec, 0.5) if imp_sec else None,
        median_validation_gain_abs=_quantile(validation_gain_abs, 0.5) if validation_gain_abs else None,
        median_validation_gain_pct=_quantile(validation_gain_pct, 0.5) if validation_gain_pct else None,
    )


def _build_group_tree(runs: list[RunRecord], group_by: tuple[str, ...]) -> GroupNode:
    root = GroupNode(key="root", value="all", level=0, runs=runs, children={})

    def attach(node: GroupNode, level: int, node_runs: list[RunRecord]) -> None:
        if level >= len(group_by):
            return
        dimension = group_by[level]
        bucket: dict[str, list[RunRecord]] = {}
        for run in node_runs:
            label = _dimension_value(run, dimension)
            bucket.setdefault(label, []).append(run)

        for value, subset in sorted(bucket.items()):
            child = GroupNode(key=dimension, value=value, level=level + 1, runs=subset, children={})
            node.children[value] = child
            attach(child, level + 1, subset)

    attach(root, 0, runs)
    return root


def _write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def _plot_boxplot(plt: Any, labels: list[str], values: list[list[float]], title: str, out_file: Path) -> None:
    plt.figure(figsize=(max(8, len(labels) * 1.2), 6))
    plt.boxplot(values, labels=labels, patch_artist=True)
    plt.xticks(rotation=25, ha="right")
    plt.title(title)
    plt.ylabel("Final objective")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _plot_validation_gain(plt: Any, labels: list[str], gains: list[list[float]], title: str, out_file: Path) -> None:
    plt.figure(figsize=(max(8, len(labels) * 1.1), 5.5))
    medians = [(_quantile(group, 0.5) if group else math.nan) for group in gains]
    plt.bar(labels, medians)
    plt.xticks(rotation=25, ha="right")
    plt.title(title)
    plt.ylabel("Validation relative improvement, %")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _plot_pareto_runtime_gain(plt: Any, labels: list[str], runtimes: list[float], gains: list[float], title: str, out_file: Path) -> None:
    plt.figure(figsize=(8, 6))
    plt.scatter(runtimes, gains, alpha=0.8)
    for idx, label in enumerate(labels):
        plt.annotate(label, (runtimes[idx], gains[idx]), fontsize=8, xytext=(4, 3), textcoords="offset points")
    plt.title(title)
    plt.xlabel("Median runtime, sec (lower is better)")
    plt.ylabel("Median validation gain, % (higher is better)")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _plot_risk_vs_gain(plt: Any, labels: list[str], risks: list[float], gains: list[float], title: str, out_file: Path) -> None:
    plt.figure(figsize=(8, 6))
    plt.scatter(risks, gains, alpha=0.8)
    for idx, label in enumerate(labels):
        plt.annotate(label, (risks[idx], gains[idx]), fontsize=8, xytext=(4, 3), textcoords="offset points")
    plt.title(title)
    plt.xlabel("Risk (CV objective, lower is better)")
    plt.ylabel("Median validation gain, %")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _plot_time_to_best(plt: Any, labels: list[str], values: list[list[float]], title: str, out_file: Path) -> None:
    plt.figure(figsize=(max(8, len(labels) * 1.2), 6))
    plt.boxplot(values, labels=labels, patch_artist=True)
    plt.xticks(rotation=25, ha="right")
    plt.title(title)
    plt.ylabel("Time to best, sec")
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _plot_convergence_ribbons(plt: Any, traces: dict[str, list[list[tuple[int, float]]]], title: str, out_file: Path) -> None:
    plt.figure(figsize=(9, 6))
    for label, runs in traces.items():
        if not runs:
            continue
        max_len = max(len(run) for run in runs)
        medians: list[float] = []
        p25: list[float] = []
        p75: list[float] = []
        xs = list(range(1, max_len + 1))
        for idx in range(max_len):
            vals = [run[idx][1] for run in runs if idx < len(run)]
            if not vals:
                continue
            medians.append(_quantile(vals, 0.5))
            p25.append(_quantile(vals, 0.25))
            p75.append(_quantile(vals, 0.75))
        xs = xs[: len(medians)]
        if not xs:
            continue
        plt.plot(xs, medians, label=label)
        plt.fill_between(xs, p25, p75, alpha=0.2)
    plt.title(title)
    plt.xlabel("Evaluation step")
    plt.ylabel("Best-so-far objective")
    plt.grid(alpha=0.3)
    plt.legend()
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _plot_run_objectives(plt: Any, values: list[float], title: str, out_file: Path) -> None:
    plt.figure(figsize=(8, 5))
    xs = list(range(1, len(values) + 1))
    plt.plot(xs, values, marker="o", linewidth=1.0)
    plt.title(title)
    plt.xlabel("Run index")
    plt.ylabel("Final objective")
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(out_file, dpi=160)
    plt.close()


def _method_objectives_by_subgroup(runs: list[RunRecord], subgroup_key: str) -> dict[str, dict[str, list[float]]]:
    result: dict[str, dict[str, list[float]]] = {}
    for run in runs:
        subgroup = _dimension_value(run, subgroup_key)
        methods = result.setdefault(subgroup, {})
        methods.setdefault(run.method, []).append(run.final_objective)
    return result


def _node_heading(node: GroupNode) -> str:
    if node.key == "root":
        return "overview"
    return f"{node.key}={node.value}"


def _breadcrumb_path(node_dir: Path, breadcrumb: list[tuple[str, Path]]) -> str:
    items: list[str] = []
    for index, (label, level_dir) in enumerate(breadcrumb):
        if index == len(breadcrumb) - 1:
            items.append(label)
            continue
        relative_report = os.path.relpath(level_dir / "report.md", node_dir)
        items.append(f"[{label}]({relative_report})")
    return "/" + "/".join(items)


def _with_display_name(path_value: str, display_name: str | None = None) -> str:
    if not display_name:
        return path_value
    separator = "&" if "?" in path_value else "?"
    return f"{path_value}{separator}display_name={quote(display_name)}"


def _partition_runs(node_runs: list[RunRecord], dimension: str) -> dict[str, list[RunRecord]]:
    partitions: dict[str, list[RunRecord]] = {}
    for run in node_runs:
        label = _dimension_value(run, dimension)
        partitions.setdefault(label, []).append(run)
    return partitions


def _comparison_rows_with_stats(
    partitions: dict[str, list[RunRecord]],
    *,
    threshold: float,
    bootstrap_iterations: int,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for label, subset in sorted(partitions.items()):
        subset_stats = _stats_for_runs(subset, threshold)
        objectives = [run.final_objective for run in subset]
        gains = [run.validation_relative_improvement_pct for run in subset if run.validation_relative_improvement_pct is not None]
        obj_ci_low, obj_ci_high = bootstrap_ci(objectives, n_boot=bootstrap_iterations)
        gain_ci_low, gain_ci_high = bootstrap_ci(gains, n_boot=bootstrap_iterations) if gains else (math.nan, math.nan)
        rows.append(
            {
                "group": label,
                "run_count": subset_stats.run_count,
                "median_objective": subset_stats.median_objective,
                "objective_ci_low": obj_ci_low,
                "objective_ci_high": obj_ci_high,
                "iqr_objective": subset_stats.iqr_objective,
                "cv_objective": coefficient_of_variation(objectives),
                "success_share": subset_stats.success_share,
                "median_runtime_sec": subset_stats.median_time_sec,
                "median_validation_gain_pct": subset_stats.median_validation_gain_pct,
                "validation_gain_ci_low": gain_ci_low,
                "validation_gain_ci_high": gain_ci_high,
            }
        )
    return rows


def _build_pairwise_table(partitions: dict[str, list[RunRecord]], *, alpha: float) -> list[dict[str, Any]]:
    groups = {label: [run.final_objective for run in subset] for label, subset in partitions.items() if len(subset) > 0}
    pairwise_rows = pairwise_mannwhitney(groups, correction="holm")
    enriched: list[dict[str, Any]] = []
    for row in pairwise_rows:
        group_a = str(row["group_a"])
        group_b = str(row["group_b"])
        delta = cliffs_delta(groups.get(group_a, []), groups.get(group_b, []))
        enriched.append(
            {
                "group_a": group_a,
                "group_b": group_b,
                "u_stat": row.get("u_stat"),
                "p_raw": row.get("p_raw"),
                "p_holm": row.get("p_adj"),
                "is_significant": bool(float(row.get("p_adj", 1.0)) < alpha),
                "cliffs_delta": delta,
                "effect_size": effect_size_label(delta),
            }
        )
    return enriched


def _coverage_matrix_rows(node_runs: list[RunRecord]) -> list[dict[str, Any]]:
    matrix: dict[tuple[str, str], dict[str, Any]] = {}
    for run in node_runs:
        key = (str(run.divisor_size), run.dataset)
        bucket = matrix.setdefault(
            key,
            {
                "divisor_size": run.divisor_size,
                "dataset": run.dataset,
                "methods": set(),
                "runs": 0,
                "with_validation": 0,
                "seeds": set(),
            },
        )
        bucket["methods"].add(run.method)
        bucket["seeds"].add(str(run.seed))
        bucket["runs"] += 1
        if run.validation_file:
            bucket["with_validation"] += 1

    rows: list[dict[str, Any]] = []
    for _, bucket in sorted(matrix.items()):
        rows.append(
            {
                "divisor_size": bucket["divisor_size"],
                "dataset": bucket["dataset"],
                "methods_count": len(bucket["methods"]),
                "runs": bucket["runs"],
                "validation_coverage_share": bucket["with_validation"] / bucket["runs"] if bucket["runs"] else 0.0,
                "seed_count": len(bucket["seeds"]),
            }
        )
    return rows


def _decision_summary(comparison_rows: list[dict[str, Any]], pairwise_rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not comparison_rows:
        return {
            "top_by_objective": None,
            "top_by_gain": None,
            "adopt": [],
            "watch": [],
            "deprioritize": [],
            "significant_pairs": 0,
        }

    by_objective = sorted(comparison_rows, key=lambda row: (row["median_objective"], -row["run_count"]))
    gain_candidates = [row for row in comparison_rows if not math.isnan(row["median_validation_gain_pct"])]
    by_gain = sorted(gain_candidates, key=lambda row: (row["median_validation_gain_pct"], row["run_count"]), reverse=True) if gain_candidates else []

    significant_groups: set[str] = set()
    for row in pairwise_rows:
        if row.get("is_significant"):
            significant_groups.add(str(row["group_a"]))
            significant_groups.add(str(row["group_b"]))

    adopt: list[str] = []
    watch: list[str] = []
    deprioritize: list[str] = []

    for row in comparison_rows:
        label = str(row["group"])
        gain = row.get("median_validation_gain_pct")
        cv_value = row.get("cv_objective")
        run_count = int(row.get("run_count", 0))
        has_signal = label in significant_groups

        if gain is not None and not math.isnan(gain) and gain >= 20 and run_count >= 3 and (has_signal or cv_value < 0.25):
            adopt.append(label)
        elif gain is not None and not math.isnan(gain) and gain < 0:
            deprioritize.append(label)
        else:
            watch.append(label)

    return {
        "top_by_objective": by_objective[0]["group"],
        "top_by_gain": by_gain[0]["group"] if by_gain else None,
        "adopt": adopt,
        "watch": watch,
        "deprioritize": deprioritize,
        "significant_pairs": sum(1 for row in pairwise_rows if row.get("is_significant")),
    }


def _profile_tables(
    *,
    node: GroupNode,
    next_dimension: str | None,
    threshold: float,
    bootstrap_iterations: int,
    alpha: float,
) -> tuple[dict[str, list[dict[str, Any]]], dict[str, list[str]], list[dict[str, Any]], list[dict[str, Any]], dict[str, list[RunRecord]]]:
    tables: dict[str, list[dict[str, Any]]] = {}
    fields: dict[str, list[str]] = {}

    partitions = _partition_runs(node.runs, next_dimension) if next_dimension else {}
    comparison_rows = _comparison_rows_with_stats(partitions, threshold=threshold, bootstrap_iterations=bootstrap_iterations) if partitions else []
    pairwise_rows = _build_pairwise_table(partitions, alpha=alpha) if partitions else []

    common_compare_fields = [
        "group",
        "run_count",
        "median_objective",
        "objective_ci_low",
        "objective_ci_high",
        "iqr_objective",
        "cv_objective",
        "success_share",
        "median_runtime_sec",
        "median_validation_gain_pct",
        "validation_gain_ci_low",
        "validation_gain_ci_high",
    ]

    if comparison_rows:
        table_name = f"compare_by_{next_dimension}"
        tables[table_name] = comparison_rows
        fields[table_name] = common_compare_fields

    if pairwise_rows:
        table_name = f"pairwise_significance_by_{next_dimension}"
        tables[table_name] = pairwise_rows
        fields[table_name] = [
            "group_a",
            "group_b",
            "u_stat",
            "p_raw",
            "p_holm",
            "is_significant",
            "cliffs_delta",
            "effect_size",
        ]
        win_rate_name = f"pairwise_win_rate_by_{next_dimension}"
        objective_groups = {label: [run.final_objective for run in subset] for label, subset in partitions.items()}
        win_rate_rows = pairwise_win_rate(objective_groups)
        if win_rate_rows:
            tables[win_rate_name] = win_rate_rows
            fields[win_rate_name] = ["group_a", "group_b", "win_rate_a", "win_rate_b"]

        kw = kruskal_wallis(objective_groups)
        lv = levene_test(objective_groups)
        omnibus_rows = [
            {
                "kruskal_h_stat": kw.get("h_stat"),
                "kruskal_p_value": kw.get("p_value"),
                "kruskal_df": kw.get("df"),
                "levene_w_stat": lv.get("w_stat"),
                "levene_p_value": lv.get("p_value"),
                "levene_df_between": lv.get("df_between"),
                "levene_df_within": lv.get("df_within"),
            }
        ]
        tables[f"omnibus_tests_by_{next_dimension}"] = omnibus_rows
        fields[f"omnibus_tests_by_{next_dimension}"] = [
            "kruskal_h_stat",
            "kruskal_p_value",
            "kruskal_df",
            "levene_w_stat",
            "levene_p_value",
            "levene_df_between",
            "levene_df_within",
        ]

    if node.key == "root":
        method_partitions = _partition_runs(node.runs, "method")
        method_rows = _comparison_rows_with_stats(method_partitions, threshold=threshold, bootstrap_iterations=bootstrap_iterations)
        tables["method_ranking"] = sorted(method_rows, key=lambda row: (row["median_objective"], -row["run_count"]))
        fields["method_ranking"] = common_compare_fields
        gain_rows = [row for row in method_rows if not math.isnan(row["median_validation_gain_pct"])]
        tables["validation_gain_ranking"] = sorted(gain_rows, key=lambda row: (row["median_validation_gain_pct"], row["run_count"]), reverse=True)
        fields["validation_gain_ranking"] = fields["method_ranking"]
        tables["coverage_matrix"] = _coverage_matrix_rows(node.runs)
        fields["coverage_matrix"] = [
            "divisor_size",
            "dataset",
            "methods_count",
            "runs",
            "validation_coverage_share",
            "seed_count",
        ]

    if node.key == "divisor_size":
        method_partitions = _partition_runs(node.runs, "method")
        method_rows = _comparison_rows_with_stats(method_partitions, threshold=threshold, bootstrap_iterations=bootstrap_iterations)
        tables["method_comparison"] = sorted(method_rows, key=lambda row: (row["median_objective"], -row["run_count"]))
        fields["method_comparison"] = common_compare_fields
        tables["stability_table"] = [
            {"method": row["group"], "run_count": row["run_count"], "cv_objective": row["cv_objective"], "iqr_objective": row["iqr_objective"]}
            for row in method_rows
        ]
        fields["stability_table"] = ["method", "run_count", "cv_objective", "iqr_objective"]
        tables["validation_gain_by_method"] = [
            {"method": row["group"], "median_validation_gain_pct": row["median_validation_gain_pct"], "validation_gain_ci_low": row["validation_gain_ci_low"], "validation_gain_ci_high": row["validation_gain_ci_high"]}
            for row in method_rows
        ]
        fields["validation_gain_by_method"] = ["method", "median_validation_gain_pct", "validation_gain_ci_low", "validation_gain_ci_high"]

    if node.key == "dataset":
        method_partitions = _partition_runs(node.runs, "method")
        method_rows = _comparison_rows_with_stats(method_partitions, threshold=threshold, bootstrap_iterations=bootstrap_iterations)
        tables["leaderboard"] = sorted(method_rows, key=lambda row: (row["median_objective"], -row["run_count"]))
        fields["leaderboard"] = common_compare_fields

        baseline_rows: list[dict[str, Any]] = []
        for method, subset in sorted(method_partitions.items()):
            baseline = [run.validation_baseline_mean for run in subset if run.validation_baseline_mean is not None]
            optimized = [run.validation_optimized_mean for run in subset if run.validation_optimized_mean is not None]
            baseline_rows.append(
                {
                    "method": method,
                    "baseline_mean_median": _quantile(baseline, 0.5) if baseline else math.nan,
                    "optimized_mean_median": _quantile(optimized, 0.5) if optimized else math.nan,
                    "delta_abs": (_quantile(baseline, 0.5) - _quantile(optimized, 0.5)) if baseline and optimized else math.nan,
                }
            )
        tables["baseline_vs_optimized"] = baseline_rows
        fields["baseline_vs_optimized"] = ["method", "baseline_mean_median", "optimized_mean_median", "delta_abs"]

        gain_ci_rows: list[dict[str, Any]] = []
        for method, subset in sorted(method_partitions.items()):
            gains = [run.validation_relative_improvement_pct for run in subset if run.validation_relative_improvement_pct is not None]
            low, high = bootstrap_ci(gains, n_boot=bootstrap_iterations) if gains else (math.nan, math.nan)
            gain_ci_rows.append({"method": method, "gain_ci_low": low, "gain_ci_high": high})
        tables["gain_ci"] = gain_ci_rows
        fields["gain_ci"] = ["method", "gain_ci_low", "gain_ci_high"]

    if node.key == "method":
        by_dataset = _partition_runs(node.runs, "dataset")
        dataset_rows = _comparison_rows_with_stats(by_dataset, threshold=threshold, bootstrap_iterations=bootstrap_iterations)
        tables["method_profile"] = sorted(dataset_rows, key=lambda row: row["median_objective"])
        fields["method_profile"] = common_compare_fields

        sensitivity_rows: list[dict[str, Any]] = []
        by_size = _partition_runs(node.runs, "divisor_size")
        for size, subset in sorted(by_size.items()):
            objectives = [run.final_objective for run in subset]
            gains = [run.validation_relative_improvement_pct for run in subset if run.validation_relative_improvement_pct is not None]
            sensitivity_rows.append(
                {
                    "divisor_size": size,
                    "run_count": len(subset),
                    "median_objective": _quantile(objectives, 0.5),
                    "cv_objective": coefficient_of_variation(objectives),
                    "median_gain_pct": _quantile(gains, 0.5) if gains else math.nan,
                }
            )
        tables["method_sensitivity"] = sensitivity_rows
        fields["method_sensitivity"] = ["divisor_size", "run_count", "median_objective", "cv_objective", "median_gain_pct"]

    decision = _decision_summary(comparison_rows, pairwise_rows)
    tables["adoption_candidates"] = [
        {"label": label, "decision": "adopt"} for label in decision["adopt"]
    ] + [{"label": label, "decision": "watch"} for label in decision["watch"]] + [
        {"label": label, "decision": "deprioritize"} for label in decision["deprioritize"]
    ]
    fields["adoption_candidates"] = ["label", "decision"]

    return tables, fields, comparison_rows, pairwise_rows, partitions


def _build_node_artifacts(
    *,
    node: GroupNode,
    node_dir: Path,
    breadcrumb: list[tuple[str, Path]],
    threshold: float,
    next_dimension: str | None,
    plt: Any,
    options: AnalysisOptions,
) -> NodeArtifacts:
    tables_dir = ensure_dir(node_dir / "tables")
    plots_dir = ensure_dir(node_dir / "plots")

    node_stats = _stats_for_runs(node.runs, threshold)
    run_rows: list[dict[str, Any]] = []
    for run in sorted(node.runs, key=lambda item: (item.dataset, item.method, str(item.seed))):
        run_report_file = run.run_file.with_name(f"{run.run_file.stem}_report.md")
        run_report_rel = _project_relative(run_report_file) if run_report_file.exists() else None
        dataset_rel = _project_relative(run.dataset_file) if run.dataset_file else None
        dataset_link = _with_display_name(str(dataset_rel), run.dataset) if dataset_rel else run.dataset
        run_rel = _project_relative(run.run_file)
        run_link = _with_display_name(str(run_rel), run.run_file.name)
        validation_link = ""
        if run.validation_file:
            validation_rel = _project_relative(run.validation_file)
            validation_link = _with_display_name(str(validation_rel), run.validation_file.name)
        run_rows.append(
            {
                "run_report": _with_display_name(str(run_report_rel), "📄") if run_report_rel else "",
                "dataset": dataset_link,
                "divisor_size": run.divisor_size,
                "method": run.method,
                "seed": run.seed,
                "final_objective": run.final_objective,
                "total_runtime_sec": run.total_runtime_sec,
                "evaluation_count": run.evaluation_count,
                "time_to_best_sec": run.time_to_best_sec,
                "validation_relative_improvement_pct": run.validation_relative_improvement_pct,
                "run_file": run_link,
                "validation_file": validation_link,
            }
        )

    runs_table = tables_dir / "runs.csv"
    _write_csv(
        runs_table,
        run_rows,
        [
            "run_report",
            "dataset",
            "divisor_size",
            "method",
            "seed",
            "final_objective",
            "total_runtime_sec",
            "evaluation_count",
            "time_to_best_sec",
            "validation_relative_improvement_pct",
            "run_file",
            "validation_file",
        ],
    )

    summary_table = tables_dir / "summary.csv"
    _write_csv(
        summary_table,
        [
            {
                "analysis_level": _node_heading(node),
                "run_count": node_stats.run_count,
                "median_objective": node_stats.median_objective,
                "iqr_objective": node_stats.iqr_objective,
                "median_runtime_sec": node_stats.median_time_sec,
                "median_time_to_best_sec": node_stats.median_time_to_best_sec,
                "median_evaluation_count": node_stats.median_eval_count,
                "success_share": node_stats.success_share,
                "median_improvement_per_eval": node_stats.median_improvement_per_eval,
                "median_improvement_per_sec": node_stats.median_improvement_per_sec,
                "median_validation_gain_abs": node_stats.median_validation_gain_abs,
                "median_validation_gain_pct": node_stats.median_validation_gain_pct,
            }
        ],
        [
            "analysis_level",
            "run_count",
            "median_objective",
            "iqr_objective",
            "median_runtime_sec",
            "median_time_to_best_sec",
            "median_evaluation_count",
            "success_share",
            "median_improvement_per_eval",
            "median_improvement_per_sec",
            "median_validation_gain_abs",
            "median_validation_gain_pct",
        ],
    )

    profile_tables, profile_fields, comparison_rows, pairwise_rows, partitions = _profile_tables(
        node=node,
        next_dimension=next_dimension,
        threshold=threshold,
        bootstrap_iterations=options.bootstrap_iterations,
        alpha=options.alpha,
    )

    tables: dict[str, Path] = {"runs": runs_table, "summary": summary_table}
    for table_name, rows in profile_tables.items():
        if not rows:
            continue
        table_file = tables_dir / f"{table_name}.csv"
        _write_csv(table_file, rows, profile_fields[table_name])
        tables[table_name] = table_file

    plots: dict[str, Path] = {}
    if plt is not None and comparison_rows and next_dimension:
        limited_rows = sorted(comparison_rows, key=lambda row: (-int(row["run_count"]), row["median_objective"]))[: options.max_series_per_plot]
        labels = [str(row["group"]) for row in limited_rows]
        grouped_values = [[run.final_objective for run in partitions[label]] for label in labels if label in partitions]
        if labels and grouped_values:
            objective_plot = plots_dir / f"final_objective_by_{next_dimension}.png"
            _plot_boxplot(plt, labels, grouped_values, f"Final objective by {next_dimension}", objective_plot)
            plots[f"final_objective_by_{next_dimension}"] = objective_plot

        grouped_gains = [
            [run.validation_relative_improvement_pct for run in partitions[label] if run.validation_relative_improvement_pct is not None]
            for label in labels
            if label in partitions
        ]
        if any(values for values in grouped_gains):
            gain_plot = plots_dir / f"validation_gain_by_{next_dimension}.png"
            _plot_validation_gain(plt, labels, grouped_gains, f"Validation gain by {next_dimension}", gain_plot)
            plots[f"validation_gain_by_{next_dimension}"] = gain_plot

        runtimes = [float(row["median_runtime_sec"]) for row in limited_rows]
        gains = [float(row["median_validation_gain_pct"]) if not math.isnan(float(row["median_validation_gain_pct"])) else 0.0 for row in limited_rows]
        risks = [float(row["cv_objective"]) if not math.isnan(float(row["cv_objective"])) else 0.0 for row in limited_rows]
        if labels:
            pareto_plot = plots_dir / f"pareto_runtime_gain_by_{next_dimension}.png"
            _plot_pareto_runtime_gain(plt, labels, runtimes, gains, f"Pareto runtime-vs-gain by {next_dimension}", pareto_plot)
            plots[f"pareto_runtime_gain_by_{next_dimension}"] = pareto_plot

            risk_plot = plots_dir / f"risk_vs_gain_by_{next_dimension}.png"
            _plot_risk_vs_gain(plt, labels, risks, gains, f"Risk-vs-gain by {next_dimension}", risk_plot)
            plots[f"risk_vs_gain_by_{next_dimension}"] = risk_plot

        grouped_time_to_best = [
            [run.time_to_best_sec for run in partitions[label] if run.time_to_best_sec is not None]
            for label in labels
            if label in partitions
        ]
        if any(values for values in grouped_time_to_best):
            ttb_plot = plots_dir / f"time_to_best_by_{next_dimension}.png"
            _plot_time_to_best(plt, labels, grouped_time_to_best, f"Time-to-best by {next_dimension}", ttb_plot)
            plots[f"time_to_best_by_{next_dimension}"] = ttb_plot

        if node.key == "divisor_size":
            top_three = labels[:3]
            convergence_traces = {label: [run.best_so_far_by_eval for run in partitions[label]] for label in top_three if label in partitions}
            if convergence_traces:
                ribbons_plot = plots_dir / "convergence_ribbons_top3_methods.png"
                _plot_convergence_ribbons(plt, convergence_traces, "Convergence ribbons (top-3)", ribbons_plot)
                plots["convergence_ribbons_top3_methods"] = ribbons_plot

    if plt is not None:
        # Method-level comparisons on every hierarchy level for better readability.
        method_partitions = _partition_runs(node.runs, "method")
        if len(method_partitions) > 1:
            method_labels = sorted(method_partitions)
            method_values = [[run.final_objective for run in method_partitions[label]] for label in method_labels]
            method_plot = plots_dir / "final_objective_by_method_overall.png"
            _plot_boxplot(plt, method_labels, method_values, "Final objective by method (overall)", method_plot)
            plots["final_objective_by_method_overall"] = method_plot

        if node.key == "root":
            subgroup_dim = "divisor_size"
        elif node.key == "divisor_size":
            subgroup_dim = "dataset"
        else:
            subgroup_dim = None

        if subgroup_dim:
            subgroup_map = _method_objectives_by_subgroup(node.runs, subgroup_dim)
            for subgroup, method_map in sorted(subgroup_map.items()):
                if len(method_map) <= 1:
                    continue
                labels = sorted(method_map)
                values = [method_map[label] for label in labels]
                split_plot = plots_dir / f"final_objective_by_method_{subgroup_dim}={_safe_slug(subgroup)}.png"
                _plot_boxplot(plt, labels, values, f"Method comparison ({subgroup_dim}={subgroup})", split_plot)
                plots[f"final_objective_by_method_{subgroup_dim}={subgroup}"] = split_plot

        if node.key in {"method", "seed"} and len(node.runs) > 1:
            sorted_runs = sorted(node.runs, key=lambda run: (run.dataset, str(run.seed), run.run_file.name))
            run_values = [run.final_objective for run in sorted_runs]
            runs_plot = plots_dir / "final_objective_by_run_index.png"
            _plot_run_objectives(plt, run_values, "Final objective by run index", runs_plot)
            plots["final_objective_by_run_index"] = runs_plot

    decision = _decision_summary(comparison_rows, pairwise_rows)

    report_file = node_dir / "report.md"
    report_lines = [
        f"# Отчёт анализа: `{_node_heading(node)}`",
        "",
        "## Навигация",
    ]
    report_lines.append(f"- Путь: {_breadcrumb_path(node_dir, breadcrumb)}")

    if node.children:
        report_lines.append("- Переход на нижний уровень:")
        for child in node.children.values():
            child_slug = _safe_slug(f"{child.key}={child.value}")
            report_lines.append(f"  - [{child.key}={child.value}](groups/{child_slug}/report.md) ({len(child.runs)} runs)")
    else:
        report_lines.append("- Нижних уровней группировки нет.")

    report_lines.extend(
        [
            "",
            "## Краткая сводка",
            f"- запусков в области: **{node_stats.run_count}**",
            f"- медиана final objective: **{node_stats.median_objective:.6f}**",
            f"- IQR objective: **{node_stats.iqr_objective:.6f}**",
            f"- доля успеха (`objective <= {threshold:.6f}`): **{node_stats.success_share:.2%}**",
            f"- медианное время выполнения: **{node_stats.median_time_sec:.3f} сек**",
        ]
    )

    if node_stats.median_validation_gain_pct is not None:
        report_lines.append(f"- медианный прирост по validation: **{node_stats.median_validation_gain_pct:.3f}%**")
    else:
        report_lines.append("- медианный прирост по validation: **N/A** (в области нет файлов валидации)")

    report_lines.extend(
        [
            "",
            "## Executive summary",
            f"- лучший сегмент по objective: **{decision['top_by_objective'] or 'N/A'}**",
            f"- лучший сегмент по validation gain: **{decision['top_by_gain'] or 'N/A'}**",
            f"- statistically significant пар: **{decision['significant_pairs']}**",
            f"- кандидаты на adoption: **{', '.join(decision['adopt']) if decision['adopt'] else 'нет'}**",
            f"- кандидаты под наблюдение: **{', '.join(decision['watch']) if decision['watch'] else 'нет'}**",
            f"- кандидаты на понижение приоритета: **{', '.join(decision['deprioritize']) if decision['deprioritize'] else 'нет'}**",
        ]
    )

    if comparison_rows and len(comparison_rows) > options.max_series_per_plot:
        report_lines.append(
            f"- графики ограничены top-{options.max_series_per_plot} группами по run_count для снижения визуального шума"
        )

    report_lines.extend([
        "",
        "## Графики",
    ])

    if plots:
        for _, path in plots.items():
            rel_path = path.relative_to(node_dir)
            file_name = path.name
            alt_name = path.stem
            report_lines.append(f"- [{file_name}]({rel_path})")
            report_lines.append(f"![{alt_name}]({rel_path})")
    else:
        report_lines.append("- Нет доступных графиков для текущей области.")

    report_lines.extend([
        "",
        "## Таблицы",
        "",
    ])

    table_configs = [{"file": f"tables/{path.name}"} for _, path in tables.items()]
    data_tables = json.dumps(table_configs, ensure_ascii=False)
    loader_src = _tables_loader_src(node_dir)

    report_lines.extend([
        f"<div id=\"tables-container\" data-tables='{data_tables}'></div>",
        "",
        f"<script src=\"{loader_src}\"></script>",
    ])

    report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8")
    return NodeArtifacts(report_file=report_file, tables=tables, plots=plots, decision_summary=decision)


def _render_node_tree(
    *,
    node: GroupNode,
    node_dir: Path,
    breadcrumb: list[tuple[str, Path]],
    group_by: tuple[str, ...],
    threshold: float,
    plt: Any,
    manifest_entries: list[dict[str, Any]],
    options: AnalysisOptions,
) -> None:
    level_index = node.level
    next_dimension = group_by[level_index] if level_index < len(group_by) else None

    artifacts = _build_node_artifacts(
        node=node,
        node_dir=node_dir,
        breadcrumb=breadcrumb,
        threshold=threshold,
        next_dimension=next_dimension,
        plt=plt,
        options=options,
    )

    manifest_entries.append(
        {
            "analysis_level": _node_heading(node),
            "group_key": node.key,
            "group_value": node.value,
            "parent_path": _project_relative(node_dir.parent) if node.level > 0 else None,
            "level": node.level,
            "runs": len(node.runs),
            "report": _project_relative(artifacts.report_file),
            "tables": {name: _project_relative(path) for name, path in artifacts.tables.items()},
            "plots": {name: _project_relative(path) for name, path in artifacts.plots.items()},
            "artifacts_by_type": {
                "reports": [_project_relative(artifacts.report_file)],
                "tables": [_project_relative(path) for path in artifacts.tables.values()],
                "plots": [_project_relative(path) for path in artifacts.plots.values()],
            },
            "decision_summary": artifacts.decision_summary,
        }
    )

    if not node.children:
        return

    groups_dir = ensure_dir(node_dir / "groups")
    for child in node.children.values():
        slug = _safe_slug(f"{child.key}={child.value}")
        child_dir = ensure_dir(groups_dir / slug)
        _render_node_tree(
            node=child,
            node_dir=child_dir,
            breadcrumb=[*breadcrumb, (f"{child.key}={child.value}", child_dir)],
            group_by=group_by,
            threshold=threshold,
            plt=plt,
            manifest_entries=manifest_entries,
            options=options,
        )


def run_analysis(
    *,
    input_entries: list[str],
    experiments_root: Path,
    output_dir: Path,
    options: AnalysisOptions,
    command_line: str | None = None,
) -> AnalysisArtifacts:
    include_entries, exclude_entries = _split_include_exclude_inputs(input_entries)
    include_paths = [Path(entry) for entry in include_entries]
    effective_input_paths = include_paths or [experiments_root]

    discovered_files = _discover_run_files(effective_input_paths, experiments_root)
    run_files = [
        path for path in discovered_files if not any(_matches_exclusion_rule(path, rule) for rule in exclude_entries)
    ]

    runs = [record for record in (_parse_run_file(path) for path in run_files) if record is not None]
    if not runs:
        raise ValueError("No optimization run files found for analysis.")

    group_by = _auto_group_order(runs) if options.auto_grouping else options.group_by
    if not group_by:
        group_by = ("method",)

    threshold = options.success_threshold
    if threshold is None:
        threshold = _quantile([run.final_objective for run in runs], 0.25)

    output_dir = ensure_dir(output_dir)
    overview_dir = ensure_dir(output_dir / "overview")

    tree = _build_group_tree(runs, group_by)
    plt = _load_matplotlib_pyplot()

    manifest_entries: list[dict[str, Any]] = []
    _render_node_tree(
        node=tree,
        node_dir=overview_dir,
        breadcrumb=[("overview", overview_dir)],
        group_by=group_by,
        threshold=threshold,
        plt=plt,
        manifest_entries=manifest_entries,
        options=options,
    )

    validation_runs = sum(1 for run in runs if run.validation_file is not None)

    summary = {
        "schema_version": "2.0",
        "group_by": list(group_by),
        "total_runs": len(runs),
        "total_groups": len(manifest_entries),
        "threshold": threshold,
        "generated_at_utc": utc_timestamp(),
        "coverage": {
            "datasets": len({run.dataset for run in runs}),
            "methods": len({run.method for run in runs}),
            "seeds": len({str(run.seed) for run in runs}),
            "validation_coverage_share": validation_runs / len(runs) if runs else 0.0,
            "nodes_with_plots_share": (sum(1 for node in manifest_entries if node.get("plots")) / len(manifest_entries)) if manifest_entries else 0.0,
        },
        "analysis_run": {
            "input_entries": input_entries,
            "include_paths": [_project_relative(path) for path in effective_input_paths],
            "exclude_rules": exclude_entries,
            "experiments_root": _project_relative(experiments_root),
            "auto_grouping": options.auto_grouping,
            "resolved_group_by": list(group_by),
            "success_threshold": options.success_threshold,
            "max_eval_points": options.max_eval_points,
            "max_time_points": options.max_time_points,
            "max_series_per_plot": options.max_series_per_plot,
            "bootstrap_iterations": options.bootstrap_iterations,
            "alpha": options.alpha,
            "discovered_run_files_before_exclusions": [_project_relative(path) for path in discovered_files],
            "discovered_run_files": [_project_relative(path) for path in run_files],
            "output_dir": _project_relative(output_dir),
        },
        "nodes": manifest_entries,
    }

    summary_file = output_dir / "analysis_summary.json"
    write_json_with_meta(summary_file, summary, command="analyze", command_line=command_line)

    return AnalysisArtifacts(
        output_dir=output_dir,
        overview_report=overview_dir / "report.md",
        summary_file=summary_file,
        total_runs=len(runs),
        group_by=list(group_by),
    )
