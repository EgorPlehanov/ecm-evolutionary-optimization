from __future__ import annotations

import math
import re
from fnmatch import fnmatch
from dataclasses import dataclass
from pathlib import Path
from statistics import median
from typing import Any

from ecm_optimizer.utils.io_utils import ensure_dir, read_json, write_json_with_meta

_METHODS = {"de", "rs", "pso", "bo", "ga"}
_DATASET_RE = re.compile(r"^(\d+)_dset_")


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
    dataset: str
    divisor_size: int | None
    method: str
    seed: int | None
    final_objective: float
    total_runtime_sec: float
    evaluation_count: int
    time_to_best_sec: float | None
    max_plateau_evals: int | None
    best_so_far_by_eval: list[tuple[int, float]]
    best_so_far_by_time: list[tuple[float, float]]
    first_fitness: float | None


@dataclass(frozen=True)
class AnalysisOptions:
    success_threshold: float | None
    max_eval_points: int
    max_time_points: int
    group_by: tuple[str, ...]


@dataclass(frozen=True)
class MultiRunArtifacts:
    summary_file: Path
    plots: dict[str, Path]
    total_runs: int
    group_labels: list[str]


def _extract_best_so_far(history: list[dict[str, Any]]) -> tuple[list[tuple[int, float]], list[tuple[float, float]], float | None]:
    evaluation_events = [event for event in history if event.get("kind") == "evaluation"]
    if not evaluation_events:
        return [], [], None

    best_so_far_eval: list[tuple[int, float]] = []
    best_so_far_time: list[tuple[float, float]] = []
    current_best: float | None = None
    first_fitness: float | None = None
    for event in evaluation_events:
        eval_id = int(event.get("eval", len(best_so_far_eval) + 1))
        fitness = float(event["fitness"])
        elapsed = float(event.get("elapsed_sec", 0.0))
        if first_fitness is None:
            first_fitness = fitness
        if current_best is None or fitness < current_best:
            current_best = fitness
        assert current_best is not None
        best_so_far_eval.append((eval_id, current_best))
        best_so_far_time.append((elapsed, current_best))
    return best_so_far_eval, best_so_far_time, first_fitness


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


def _matches_exclusion_rule(run_file: Path, rule: str) -> bool:
    candidate = Path(rule).expanduser()
    if candidate.exists():
        resolved_candidate = candidate.resolve()
        if resolved_candidate.is_file():
            return run_file == resolved_candidate
        return run_file.is_relative_to(resolved_candidate)

    run_path = str(run_file)
    return (
        fnmatch(run_path, rule)
        or fnmatch(run_file.name, rule)
        or (rule in run_path)
        or (rule in run_file.name)
    )


def _parse_divisor_size(dataset_name: str) -> int | None:
    match = _DATASET_RE.match(dataset_name)
    if match is None:
        return None
    return int(match.group(1))


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
    divisor_size = _parse_divisor_size(dataset)

    best_eval, best_time, first_fitness = _extract_best_so_far(history if isinstance(history, list) else [])

    return RunRecord(
        run_file=run_file,
        dataset=dataset,
        divisor_size=divisor_size,
        method=method,
        seed=payload.get("config", {}).get("seed"),
        final_objective=float(optimized["objective"]),
        total_runtime_sec=float(run_stats.get("total_runtime_sec", 0.0) or 0.0),
        evaluation_count=int(run_stats.get("evaluation_count", len(best_eval)) or len(best_eval)),
        time_to_best_sec=(
            float(run_stats["time_to_best_sec"]) if run_stats.get("time_to_best_sec") is not None else None
        ),
        max_plateau_evals=(
            int(run_stats["max_plateau_evals"]) if run_stats.get("max_plateau_evals") is not None else None
        ),
        best_so_far_by_eval=best_eval,
        best_so_far_by_time=best_time,
        first_fitness=first_fitness,
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
    if not values:
        return math.nan
    return _quantile(values, 0.75) - _quantile(values, 0.25)


def _stdev(values: list[float]) -> float:
    if len(values) < 2:
        return 0.0
    mean = sum(values) / len(values)
    variance = sum((v - mean) ** 2 for v in values) / (len(values) - 1)
    return math.sqrt(max(variance, 0.0))


def _group_label(run: RunRecord, group_by: tuple[str, ...]) -> str:
    parts: list[str] = []
    for key in group_by:
        if key == "method":
            parts.append(f"method={run.method}")
        elif key == "divisor_size":
            value = run.divisor_size if run.divisor_size is not None else "unknown"
            parts.append(f"divisor_size={value}")
        elif key == "dataset":
            parts.append(f"dataset={run.dataset}")
    return " | ".join(parts) if parts else run.method


def _median_curve_by_eval(runs: list[RunRecord], max_points: int) -> tuple[list[int], list[float]]:
    max_eval = max((points[-1][0] for points in (r.best_so_far_by_eval for r in runs) if points), default=0)
    if max_eval == 0:
        return [], []
    if max_eval <= max_points:
        grid = list(range(1, max_eval + 1))
    else:
        step = max(1, max_eval // max_points)
        grid = list(range(1, max_eval + 1, step))
        if grid[-1] != max_eval:
            grid.append(max_eval)

    medians: list[float] = []
    for eval_id in grid:
        values: list[float] = []
        for run in runs:
            if not run.best_so_far_by_eval:
                continue
            value = run.best_so_far_by_eval[-1][1]
            for run_eval, run_best in run.best_so_far_by_eval:
                if run_eval >= eval_id:
                    value = run_best
                    break
            values.append(value)
        medians.append(float(median(values)) if values else math.nan)
    return grid, medians


def _median_curve_by_time(runs: list[RunRecord], max_points: int) -> tuple[list[float], list[float]]:
    max_time = max((points[-1][0] for points in (r.best_so_far_by_time for r in runs) if points), default=0.0)
    if max_time <= 0:
        return [], []
    if max_points <= 1:
        grid = [max_time]
    else:
        grid = [max_time * idx / (max_points - 1) for idx in range(max_points)]

    medians: list[float] = []
    for t in grid:
        values: list[float] = []
        for run in runs:
            if not run.best_so_far_by_time:
                continue
            value = run.best_so_far_by_time[-1][1]
            for run_t, run_best in run.best_so_far_by_time:
                if run_t >= t:
                    value = run_best
                    break
            values.append(value)
        medians.append(float(median(values)) if values else math.nan)
    return grid, medians


def _plot_overlay_curves(plt: Any, grouped_runs: dict[str, list[RunRecord]], output_dir: Path, options: AnalysisOptions) -> Path:
    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 11), sharey=True)

    for label, runs in sorted(grouped_runs.items()):
        x_eval, y_eval = _median_curve_by_eval(runs, options.max_eval_points)
        if x_eval:
            axes[0].plot(x_eval, y_eval, linewidth=1.8, label=label)
        x_time, y_time = _median_curve_by_time(runs, options.max_time_points)
        if x_time:
            axes[1].plot(x_time, y_time, linewidth=1.8, label=label)

    axes[0].set_title("Overlay convergence (median best_so_far by eval)")
    axes[0].set_xlabel("Evaluation")
    axes[0].set_ylabel("Best objective so far")
    axes[0].grid(alpha=0.3)
    axes[0].legend(fontsize=8)

    axes[1].set_title("Overlay convergence (median best_so_far by time)")
    axes[1].set_xlabel("Elapsed seconds")
    axes[1].set_ylabel("Best objective so far")
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=8)

    out = output_dir / "overlay_convergence_combined.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def _plot_boxplot(plt: Any, grouped_runs: dict[str, list[RunRecord]], output_dir: Path) -> Path:
    labels = sorted(grouped_runs.keys())
    values = [[run.final_objective for run in grouped_runs[label]] for label in labels]
    plt.figure(figsize=(max(9, len(labels) * 1.3), 6))
    plt.boxplot(values, labels=labels, patch_artist=True)
    plt.xticks(rotation=30, ha="right")
    plt.title("Final objective by group")
    plt.ylabel("Final objective")
    plt.grid(axis="y", alpha=0.3)
    out = output_dir / "boxplot_final_objective.png"
    plt.tight_layout()
    plt.savefig(out, dpi=160)
    plt.close()
    return out


def _plot_time_to_best(plt: Any, grouped_runs: dict[str, list[RunRecord]], output_dir: Path) -> Path:
    labels = sorted(grouped_runs.keys())
    values = [[run.time_to_best_sec for run in grouped_runs[label] if run.time_to_best_sec is not None] for label in labels]
    plt.figure(figsize=(max(9, len(labels) * 1.3), 6))
    parts = plt.violinplot(values, showmeans=True, showmedians=True)
    for body in parts["bodies"]:
        body.set_alpha(0.4)
    plt.xticks(range(1, len(labels) + 1), labels, rotation=30, ha="right")
    plt.title("Time to best by group")
    plt.ylabel("Seconds")
    plt.grid(axis="y", alpha=0.3)
    out = output_dir / "violin_time_to_best.png"
    plt.tight_layout()
    plt.savefig(out, dpi=160)
    plt.close()
    return out


def _plot_pareto(plt: Any, grouped_runs: dict[str, list[RunRecord]], output_dir: Path) -> Path:
    plt.figure(figsize=(10, 6))
    for label, runs in sorted(grouped_runs.items()):
        x = [run.total_runtime_sec for run in runs]
        y = [run.final_objective for run in runs]
        plt.scatter(x, y, alpha=0.7, s=45, label=label)
    plt.title("Pareto chart: final objective vs elapsed time")
    plt.xlabel("Elapsed time (sec)")
    plt.ylabel("Final objective")
    plt.grid(alpha=0.3)
    plt.legend(fontsize=8)
    out = output_dir / "pareto_quality_vs_time.png"
    plt.tight_layout()
    plt.savefig(out, dpi=160)
    plt.close()
    return out


def _plot_success_profile(plt: Any, grouped_runs: dict[str, list[RunRecord]], output_dir: Path, threshold: float) -> Path:
    max_eval = max((run.evaluation_count for runs in grouped_runs.values() for run in runs), default=0)
    max_time = max((run.total_runtime_sec for runs in grouped_runs.values() for run in runs), default=0.0)
    eval_grid = list(range(1, max_eval + 1)) if max_eval > 0 else []
    time_points = 80
    time_grid = [max_time * idx / (time_points - 1) for idx in range(time_points)] if max_time > 0 else []

    fig, axes = plt.subplots(nrows=2, ncols=1, figsize=(11, 11))
    for label, runs in sorted(grouped_runs.items()):
        shares: list[float] = []
        for eval_id in eval_grid:
            success = 0
            for run in runs:
                reached = False
                for run_eval, run_best in run.best_so_far_by_eval:
                    if run_eval > eval_id:
                        break
                    if run_best <= threshold:
                        reached = True
                        break
                if reached:
                    success += 1
            shares.append(success / len(runs) if runs else 0.0)
        if eval_grid:
            axes[0].plot(eval_grid, shares, linewidth=1.8, label=label)
    axes[0].set_title(f"Success profile by eval (threshold <= {threshold:.6f})")
    axes[0].set_xlabel("Evaluation")
    axes[0].set_ylabel("Share of successful runs")
    axes[0].set_ylim(0, 1.05)
    axes[0].grid(alpha=0.3)
    axes[0].legend(fontsize=8)

    for label, runs in sorted(grouped_runs.items()):
        shares: list[float] = []
        for point in time_grid:
            success = 0
            for run in runs:
                reached = False
                for run_t, run_best in run.best_so_far_by_time:
                    if run_t > point:
                        break
                    if run_best <= threshold:
                        reached = True
                        break
                if reached:
                    success += 1
            shares.append(success / len(runs) if runs else 0.0)
        if time_grid:
            axes[1].plot(time_grid, shares, linewidth=1.8, label=label)
    axes[1].set_title(f"Success profile by time (threshold <= {threshold:.6f})")
    axes[1].set_xlabel("Elapsed seconds")
    axes[1].set_ylabel("Share of successful runs")
    axes[1].set_ylim(0, 1.05)
    axes[1].grid(alpha=0.3)
    axes[1].legend(fontsize=8)
    out = output_dir / "success_profile_combined.png"
    fig.tight_layout()
    fig.savefig(out, dpi=160)
    plt.close(fig)
    return out


def _build_summary(grouped_runs: dict[str, list[RunRecord]], *, threshold: float, group_by: tuple[str, ...], input_paths: list[Path]) -> dict[str, Any]:
    per_group: dict[str, Any] = {}
    for label, runs in sorted(grouped_runs.items()):
        finals = [run.final_objective for run in runs]
        runtimes = [run.total_runtime_sec for run in runs]
        eval_counts = [run.evaluation_count for run in runs]
        plateaus = [run.max_plateau_evals for run in runs if run.max_plateau_evals is not None]

        improvements_eval: list[float] = []
        improvements_sec: list[float] = []
        for run in runs:
            if run.first_fitness is None:
                continue
            improvement = run.first_fitness - run.final_objective
            if run.evaluation_count > 0:
                improvements_eval.append(improvement / run.evaluation_count)
            if run.total_runtime_sec > 0:
                improvements_sec.append(improvement / run.total_runtime_sec)

        successful = sum(1 for run in runs if any(best <= threshold for _, best in run.best_so_far_by_eval))
        per_group[label] = {
            "run_count": len(runs),
            "objective": {
                "min": min(finals),
                "q25": _quantile(finals, 0.25),
                "median": _quantile(finals, 0.5),
                "q75": _quantile(finals, 0.75),
                "max": max(finals),
                "std": _stdev(finals),
                "iqr": _iqr(finals),
            },
            "time": {
                "median_runtime_sec": _quantile(runtimes, 0.5),
                "median_time_to_best_sec": _quantile([run.time_to_best_sec for run in runs if run.time_to_best_sec is not None], 0.5)
                if any(run.time_to_best_sec is not None for run in runs)
                else None,
            },
            "budget": {
                "median_evaluation_count": _quantile(eval_counts, 0.5),
                "average_max_plateau_evals": (sum(plateaus) / len(plateaus)) if plateaus else None,
            },
            "efficiency": {
                "median_improvement_per_eval": _quantile(improvements_eval, 0.5) if improvements_eval else None,
                "median_improvement_per_sec": _quantile(improvements_sec, 0.5) if improvements_sec else None,
            },
            "success": {
                "threshold": threshold,
                "share": successful / len(runs) if runs else 0.0,
            },
            "methods": sorted({run.method for run in runs}),
            "divisor_sizes": sorted({run.divisor_size for run in runs if run.divisor_size is not None}),
            "datasets": sorted({run.dataset for run in runs}),
            "run_files": [str(run.run_file) for run in runs],
        }

    return {
        "group_by": list(group_by),
        "input_paths": [str(p) for p in input_paths],
        "total_groups": len(per_group),
        "total_runs": sum(group["run_count"] for group in per_group.values()),
        "threshold": threshold,
        "group_metrics": per_group,
    }


def generate_multi_run_artifacts(
    *,
    input_entries: list[str],
    experiments_root: Path,
    output_dir: Path,
    options: AnalysisOptions,
) -> MultiRunArtifacts:
    include_entries, exclude_entries = _split_include_exclude_inputs(input_entries)
    include_paths = [Path(entry) for entry in include_entries]
    effective_input_paths = include_paths or [experiments_root]

    discovered_files = _discover_run_files(effective_input_paths, experiments_root)
    run_files = [
        run_file for run_file in discovered_files if not any(_matches_exclusion_rule(run_file, rule) for rule in exclude_entries)
    ]
    run_records = [record for record in (_parse_run_file(path) for path in run_files) if record is not None]
    if not run_records:
        raise ValueError("No optimization run files found for analysis.")

    grouped_runs: dict[str, list[RunRecord]] = {}
    for run in run_records:
        label = _group_label(run, options.group_by)
        grouped_runs.setdefault(label, []).append(run)

    output_dir = ensure_dir(output_dir)
    threshold = options.success_threshold if options.success_threshold is not None else _quantile([r.final_objective for r in run_records], 0.25)

    summary = _build_summary(grouped_runs, threshold=threshold, group_by=options.group_by, input_paths=effective_input_paths)

    plots: dict[str, Path] = {}
    plt = _load_matplotlib_pyplot()
    if plt is not None:
        plots["overlay_convergence_combined"] = _plot_overlay_curves(plt, grouped_runs, output_dir, options)
        plots["boxplot_final_objective"] = _plot_boxplot(plt, grouped_runs, output_dir)
        plots["violin_time_to_best"] = _plot_time_to_best(plt, grouped_runs, output_dir)
        plots["pareto_quality_vs_time"] = _plot_pareto(plt, grouped_runs, output_dir)
        plots["success_profile_combined"] = _plot_success_profile(plt, grouped_runs, output_dir, threshold)

    summary["plots"] = {name: str(path) for name, path in plots.items()}
    summary["analysis_run"] = {
        "input_entries": list(input_entries),
        "include_paths": [str(path) for path in effective_input_paths],
        "exclude_rules": exclude_entries,
        "experiments_root": str(experiments_root),
        "group_by": list(options.group_by),
        "success_threshold": options.success_threshold,
        "max_eval_points": options.max_eval_points,
        "max_time_points": options.max_time_points,
        "discovered_run_files_before_exclusions": [str(path) for path in discovered_files],
        "discovered_run_files": [str(path) for path in run_files],
        "output_dir": str(output_dir),
    }
    summary_file = output_dir / "multi_run_summary.json"
    write_json_with_meta(summary_file, summary, command="analyze")

    return MultiRunArtifacts(
        summary_file=summary_file,
        plots=plots,
        total_runs=len(run_records),
        group_labels=sorted(grouped_runs.keys()),
    )
