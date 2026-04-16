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

from ecm_optimizer.utils.io_utils import ensure_dir, read_json, write_json_with_meta

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
    max_series_per_plot: int
    group_by: tuple[str, ...]
    auto_grouping: bool


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
    warnings: list[str]


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
            baseline_mean = metrics.get("baseline_mean")
            optimized_mean = metrics.get("optimized_mean")
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

    success_count = 0
    for run in runs:
        if run.first_fitness is not None:
            improvement = run.first_fitness - run.final_objective
            if run.evaluation_count > 0:
                imp_eval.append(improvement / run.evaluation_count)
            if run.total_runtime_sec > 0:
                imp_sec.append(improvement / run.total_runtime_sec)

        if any(best <= threshold for _, best in run.best_so_far_by_eval):
            success_count += 1

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
        success_share=(success_count / len(runs)) if runs else 0.0,
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


def _split_plot_groups(
    *,
    labels: list[str],
    objective_groups: list[list[float]],
    gain_groups: list[list[float]],
    max_series_per_plot: int,
) -> tuple[list[str], list[list[float]], list[list[float]], str | None]:
    if max_series_per_plot <= 0 or len(labels) <= max_series_per_plot:
        return labels, objective_groups, gain_groups, None

    keep_count = max(max_series_per_plot - 1, 1)
    kept_labels = labels[:keep_count]
    kept_objectives = objective_groups[:keep_count]
    kept_gains = gain_groups[:keep_count]

    others_objectives: list[float] = []
    others_gains: list[float] = []
    for idx in range(keep_count, len(labels)):
        others_objectives.extend(objective_groups[idx])
        others_gains.extend(gain_groups[idx])

    limited_labels = [*kept_labels, "others"]
    limited_objectives = [*kept_objectives, others_objectives]
    limited_gains = [*kept_gains, others_gains]

    warning = (
        f"Серии для графика ограничены до {max_series_per_plot}: "
        f"показано {keep_count} + агрегат others ({len(labels) - keep_count} скрытых групп)."
    )
    return limited_labels, limited_objectives, limited_gains, warning


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


def _build_node_artifacts(
    *,
    node: GroupNode,
    node_dir: Path,
    breadcrumb: list[tuple[str, Path]],
    threshold: float,
    next_dimension: str | None,
    plt: Any,
    max_series_per_plot: int,
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

    comparisons_table: Path | None = None
    comparison_rows: list[dict[str, Any]] = []
    if next_dimension:
        partitions: dict[str, list[RunRecord]] = {}
        for run in node.runs:
            label = _dimension_value(run, next_dimension)
            partitions.setdefault(label, []).append(run)

        for label, subset in sorted(partitions.items()):
            subset_stats = _stats_for_runs(subset, threshold)
            comparison_rows.append(
                {
                    "group": label,
                    "run_count": subset_stats.run_count,
                    "median_objective": subset_stats.median_objective,
                    "iqr_objective": subset_stats.iqr_objective,
                    "success_share": subset_stats.success_share,
                    "median_runtime_sec": subset_stats.median_time_sec,
                    "median_validation_gain_pct": subset_stats.median_validation_gain_pct,
                }
            )

        comparisons_table = tables_dir / f"compare_by_{next_dimension}.csv"
        _write_csv(
            comparisons_table,
            comparison_rows,
            [
                "group",
                "run_count",
                "median_objective",
                "iqr_objective",
                "success_share",
                "median_runtime_sec",
                "median_validation_gain_pct",
            ],
        )

    plots: dict[str, Path] = {}
    warnings: list[str] = []
    if plt is not None and comparison_rows:
        labels = [row["group"] for row in comparison_rows]
        grouped_values_all = [
            [run.final_objective for run in node.runs if _dimension_value(run, next_dimension or "") == label]
            for label in labels
        ]
        grouped_gains_all = [
            [
                run.validation_relative_improvement_pct
                for run in node.runs
                if _dimension_value(run, next_dimension or "") == label and run.validation_relative_improvement_pct is not None
            ]
            for label in labels
        ]

        labels, grouped_values, grouped_gains, plot_warning = _split_plot_groups(
            labels=labels,
            objective_groups=grouped_values_all,
            gain_groups=grouped_gains_all,
            max_series_per_plot=max_series_per_plot,
        )
        if plot_warning is not None:
            warnings.append(plot_warning)

        objective_plot = plots_dir / f"final_objective_by_{next_dimension}.png"
        _plot_boxplot(plt, labels, grouped_values, f"Final objective by {next_dimension}", objective_plot)
        plots[f"final_objective_by_{next_dimension}"] = objective_plot

        if any(values for values in grouped_gains):
            gain_plot = plots_dir / f"validation_gain_by_{next_dimension}.png"
            _plot_validation_gain(plt, labels, grouped_gains, f"Validation gain by {next_dimension}", gain_plot)
            plots[f"validation_gain_by_{next_dimension}"] = gain_plot

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
            report_lines.append(f"  - [{child.key}={child.value}](groups/{child_slug}/report.md)")
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
            "## Графики",
        ]
    )

    if plots:
        for _, path in plots.items():
            rel_path = path.relative_to(node_dir)
            file_name = path.name
            alt_name = path.stem
            report_lines.append(f"- [{file_name}]({rel_path})")
            report_lines.append(f"![{alt_name}]({rel_path})")
    else:
        report_lines.append("- Нет доступных графиков для текущей области.")
    if warnings:
        report_lines.extend(["", "## Предупреждения"])
        for warning in warnings:
            report_lines.append(f"- {warning}")

    report_lines.extend(
        [
            "",
            "## Таблицы",
            "",
        ]
    )

    table_configs = [
        {"file": f"tables/{runs_table.name}"},
        {"file": f"tables/{summary_table.name}"},
    ]
    if comparisons_table:
        table_configs.append({"file": f"tables/{comparisons_table.name}"})
    data_tables = json.dumps(table_configs, ensure_ascii=False)
    loader_src = _tables_loader_src(node_dir)

    report_lines.extend(
        [
            f"<div id=\"tables-container\" data-tables='{data_tables}'></div>",
            "",
            f"<script src=\"{loader_src}\"></script>",
        ]
    )

    report_file.write_text("\n".join(report_lines) + "\n", encoding="utf-8")

    tables = {"runs": runs_table, "summary": summary_table}
    if comparisons_table:
        tables[f"compare_by_{next_dimension}"] = comparisons_table
    return NodeArtifacts(report_file=report_file, tables=tables, plots=plots, warnings=warnings)


def _render_node_tree(
    *,
    node: GroupNode,
    node_dir: Path,
    breadcrumb: list[tuple[str, Path]],
    group_by: tuple[str, ...],
    threshold: float,
    plt: Any,
    max_series_per_plot: int,
    manifest_entries: list[dict[str, Any]],
) -> None:
    level_index = max(0, node.level - 1)
    next_dimension = group_by[level_index] if level_index < len(group_by) else None

    artifacts = _build_node_artifacts(
        node=node,
        node_dir=node_dir,
        breadcrumb=breadcrumb,
        threshold=threshold,
        next_dimension=next_dimension,
        plt=plt,
        max_series_per_plot=max_series_per_plot,
    )

    manifest_entries.append(
        {
            "analysis_level": _node_heading(node),
            "level": node.level,
            "status": "complete",
            "runs": len(node.runs),
            "report": str(artifacts.report_file),
            "tables": {name: str(path) for name, path in artifacts.tables.items()},
            "plots": {name: str(path) for name, path in artifacts.plots.items()},
            "warnings": artifacts.warnings,
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
            max_series_per_plot=max_series_per_plot,
            manifest_entries=manifest_entries,
        )


def run_analysis(
    *,
    input_entries: list[str],
    experiments_root: Path,
    output_dir: Path,
    options: AnalysisOptions,
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
        max_series_per_plot=options.max_series_per_plot,
        manifest_entries=manifest_entries,
    )

    manifest_nodes: list[dict[str, Any]] = []
    for node in manifest_entries:
        manifest_nodes.append(
            {
                "analysis_level": node["analysis_level"],
                "level": node["level"],
                "status": node.get("status", "complete"),
                "runs": node["runs"],
                "report": str(Path(node["report"]).resolve().relative_to(output_dir.resolve())),
                "tables": {
                    name: str(Path(path).resolve().relative_to(output_dir.resolve()))
                    for name, path in node["tables"].items()
                },
                "plots": {
                    name: str(Path(path).resolve().relative_to(output_dir.resolve()))
                    for name, path in node["plots"].items()
                },
                "warnings": node.get("warnings", []),
            }
        )

    manifest = {
        "schema_version": "1.0.0",
        "analysis_timestamp": str(output_dir.name).replace("analyze_", ""),
        "git_commit": os.getenv("GIT_COMMIT", "unknown"),
        "analysis_config": {
            "group_by": list(group_by),
            "auto_grouping": options.auto_grouping,
            "success_threshold": threshold,
            "max_eval_points": options.max_eval_points,
            "max_time_points": options.max_time_points,
            "max_series_per_plot": options.max_series_per_plot,
        },
        "coverage_summary": {
            "total_runs": len(runs),
            "group_nodes": len(manifest_nodes),
        },
        "groups_tree": manifest_nodes,
    }
    manifest_file = output_dir / "manifest.json"
    write_json_with_meta(manifest_file, manifest, command="analyze")

    summary = {
        "group_by": list(group_by),
        "total_runs": len(runs),
        "total_groups": len(manifest_entries),
        "threshold": threshold,
        "analysis_run": {
            "input_entries": input_entries,
            "include_paths": [str(path) for path in effective_input_paths],
            "exclude_rules": exclude_entries,
            "experiments_root": str(experiments_root),
            "auto_grouping": options.auto_grouping,
            "resolved_group_by": list(group_by),
            "success_threshold": options.success_threshold,
            "max_eval_points": options.max_eval_points,
            "max_time_points": options.max_time_points,
            "max_series_per_plot": options.max_series_per_plot,
            "discovered_run_files_before_exclusions": [str(path) for path in discovered_files],
            "discovered_run_files": [str(path) for path in run_files],
            "output_dir": str(output_dir),
        },
        "nodes": manifest_entries,
        "manifest_file": str(manifest_file),
    }

    summary_file = output_dir / "analysis_summary.json"
    write_json_with_meta(summary_file, summary, command="analyze")

    return AnalysisArtifacts(
        output_dir=output_dir,
        overview_report=overview_dir / "report.md",
        summary_file=summary_file,
        total_runs=len(runs),
        group_by=list(group_by),
    )
