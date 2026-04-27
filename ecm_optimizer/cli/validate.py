from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import click

from ecm_optimizer.cli.dataset_utils import dataset_generation_seed, resolve_dataset_path, resolve_opt_result_file
from ecm_optimizer.config import (
    DEFAULT_CURVE_TIMEOUT_SEC,
    DEFAULT_SEED,
    DEFAULT_VALIDATION_MAX_CURVES_PER_N,
    DEFAULT_VALIDATION_REPEATS_PER_N,
    DEFAULT_WORKERS,
    ECM_PATH,
    EXPERIMENTS_DIR,
)
from ecm_optimizer.core.baseline import choose_baseline
from ecm_optimizer.core.problem import load_numbers, read_dataset_metadata
from ecm_optimizer.core.validation import validate_on_control
from ecm_optimizer.models import resolve_workers
from ecm_optimizer.utils.io_utils import ensure_dir, read_json, utc_timestamp, write_json_with_meta


def _parse_target_digits(dataset_path: Path, fallback: int | None = None) -> int | None:
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("target_digits")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


def _load_matplotlib_pyplot() -> Any | None:
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        return plt
    except ModuleNotFoundError:
        return None


def _extract_run_timestamp(file_stem: str) -> str:
    match = re.search(r"(\d{8}T\d{6}Z)$", file_stem)
    if match:
        return match.group(1)
    return utc_timestamp()


def _build_validation_trace_plots(out_file: Path, trace_points: list[dict[str, Any]]) -> dict[str, Path]:
    plt = _load_matplotlib_pyplot()
    if plt is None or not trace_points:
        return {}

    from matplotlib import ticker

    plots_dir = ensure_dir(out_file.parent / "plots")
    x_idx = list(range(1, len(trace_points) + 1))
    plots: dict[str, Path] = {}

    chart_specs = [
        {
            "name": "score",
            "title": "Validation trace: composite score (baseline vs optimized)",
            "left_label": "Composite score",
            "baseline_key": "baseline_score",
            "optimized_key": "optimized_score",
            "delta_key": "delta_pct",
        },
        {
            "name": "time",
            "title": "Validation trace: mean time to outcome (baseline vs optimized)",
            "left_label": "Mean time to outcome, sec",
            "baseline_key": "baseline_mean_time_sec",
            "optimized_key": "optimized_mean_time_sec",
            "delta_key": "delta_pct_time",
        },
        {
            "name": "curves",
            "title": "Validation trace: mean curves to outcome (baseline vs optimized)",
            "left_label": "Mean curves to outcome",
            "baseline_key": "baseline_mean_curves",
            "optimized_key": "optimized_mean_curves",
            "delta_key": "delta_pct_curves",
        },
    ]

    for spec in chart_specs:
        baseline = [float(point.get(spec["baseline_key"], 0.0)) for point in trace_points]
        optimized = [float(point.get(spec["optimized_key"], 0.0)) for point in trace_points]
        delta_pct = [float(point.get(spec["delta_key"], 0.0)) for point in trace_points]

        fig, ax_left = plt.subplots(figsize=(12, 6))

        ax_right = ax_left.twinx()
        bar_colors = ["tab:green" if value >= 0 else "tab:red" for value in delta_pct]
        bars = ax_right.bar(
            x_idx,
            delta_pct,
            width=0.72,
            color=bar_colors,
            alpha=0.25,
            edgecolor="none",
            label=str(spec["delta_key"]),
            zorder=1,
        )
        ax_right.axhline(0.0, color="tab:orange", linewidth=1.0, alpha=0.85, zorder=2)

        ax_left.vlines(x_idx, baseline, optimized, color="0.55", linewidth=1.2, alpha=0.85, zorder=3)
        ax_left.scatter(
            x_idx,
            baseline,
            color="tab:blue",
            s=34,
            marker="o",
            label=str(spec["baseline_key"]),
            zorder=4,
        )
        ax_left.scatter(
            x_idx,
            optimized,
            color="tab:green",
            s=34,
            marker="o",
            label=str(spec["optimized_key"]),
            zorder=4,
        )

        ax_left.set_xlabel("Validation run index")
        ax_left.set_ylabel(str(spec["left_label"]))
        ax_right.set_ylabel("Delta, %")
        ax_left.set_title(f"{spec['title']} — lollipop + delta bars")

        ax_left.set_xlim(0.35, len(x_idx) + 0.65)
        ax_left.xaxis.set_major_locator(ticker.FixedLocator(x_idx))
        ax_left.xaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

        ax_left.grid(axis="y", alpha=0.28)
        ax_left.grid(axis="x", alpha=0.10)

        handles_left, labels_left = ax_left.get_legend_handles_labels()
        handles_right, labels_right = ax_right.get_legend_handles_labels()
        if bars:
            handles_right = [bars]
            labels_right = [str(spec["delta_key"])]
        ax_left.legend(handles_left + handles_right, labels_left + labels_right, loc="best")

        trace_plot_file = plots_dir / f"{out_file.stem}_{spec['name']}_trace.png"
        fig.tight_layout()
        fig.savefig(trace_plot_file, dpi=140)
        plt.close(fig)
        plots[f"{spec['name']}_trace_plot"] = trace_plot_file

        # Distribution overview: violin + box + swarm-like jittered points.
        fig_dist, ax_dist = plt.subplots(figsize=(8, 5))
        groups = [baseline, optimized]
        positions = [1, 2]

        violin = ax_dist.violinplot(
            groups,
            positions=positions,
            widths=0.7,
            showmeans=False,
            showmedians=False,
            showextrema=False,
        )
        for body, color in zip(violin["bodies"], ["tab:blue", "tab:green"]):
            body.set_facecolor(color)
            body.set_edgecolor(color)
            body.set_alpha(0.18)

        ax_dist.boxplot(
            groups,
            positions=positions,
            widths=0.22,
            patch_artist=True,
            boxprops={"facecolor": "white", "edgecolor": "0.35", "linewidth": 1.0},
            medianprops={"color": "0.15", "linewidth": 1.1},
            whiskerprops={"color": "0.35", "linewidth": 1.0},
            capprops={"color": "0.35", "linewidth": 1.0},
        )

        jitter_width = 0.08
        for pos, values, color in zip(positions, groups, ["tab:blue", "tab:green"]):
            for i, value in enumerate(values):
                jitter = (((i % 9) - 4) / 4.0) * jitter_width
                ax_dist.scatter(pos + jitter, value, s=18, color=color, alpha=0.65, edgecolors="none", zorder=3)

        ax_dist.set_xticks(positions)
        ax_dist.set_xticklabels(["baseline", "optimized"])
        ax_dist.set_ylabel(str(spec["left_label"]))
        ax_dist.set_title(f"Validation distribution: {spec['name']} (violin + box + swarm)")
        ax_dist.grid(axis="y", alpha=0.28)

        dist_plot_file = plots_dir / f"{out_file.stem}_{spec['name']}_distribution.png"
        fig_dist.tight_layout()
        fig_dist.savefig(dist_plot_file, dpi=140)
        plt.close(fig_dist)
        plots[f"{spec['name']}_distribution_plot"] = dist_plot_file

    return plots


def _append_validation_section(
    report_file: Path,
    *,
    out_file: Path,
    payload: dict[str, Any],
    trace_plot_files: dict[str, Path],
) -> None:
    report_file.parent.mkdir(parents=True, exist_ok=True)
    has_validation_section = False
    if report_file.exists():
        current = report_file.read_text(encoding="utf-8")
        has_validation_section = "\n## Validation runs\n" in current or current.startswith("## Validation runs\n")
        lines: list[str] = [current.rstrip(), ""]
    else:
        lines = [f"# Validation report: {report_file.stem}", ""]

    report_dir = report_file.parent
    rel_validate = out_file.relative_to(report_dir)
    validate_link = f"[`{rel_validate.name}`]({rel_validate.as_posix()})"

    metrics = payload.get("metrics", {})
    optimized_meta = payload.get("optimized", {})
    baseline_meta = payload.get("baseline", {})
    run_ts = _extract_run_timestamp(out_file.stem)

    section_prefix = ["## Validation runs", ""] if not has_validation_section else []

    lines.extend(
        section_prefix
        + [
            f"### Validation run `{run_ts}`",
            f"- validation file: {validate_link}",
            f"- dataset: `{payload.get('dataset')}`",
            f"- method: `{optimized_meta.get('method')}`",
            f"- optimized params: `(B1, B2)=({optimized_meta.get('b1')}, {optimized_meta.get('b2')})`",
            f"- baseline params: `(B1, B2)=({baseline_meta.get('b1')}, {baseline_meta.get('b2')})`",
            f"- max_curves_per_n: `{payload.get('max_curves_per_n')}`",
            f"- repeats_per_n: `{payload.get('repeats_per_n')}`",
            f"- curve_timeout_sec: `{payload.get('curve_timeout_sec')}`",
            f"- workers: `{payload.get('workers')}`",
            f"- seed: `{payload.get('seed')}`",
            f"- optimized_mean_score: `{metrics.get('optimized_mean_score')}`",
            f"- baseline_mean_score: `{metrics.get('baseline_mean_score')}`",
            f"- relative_improvement_pct: `{metrics.get('relative_improvement_pct')}`",
            f"- optimized_mean_time_sec: `{metrics.get('optimized_mean_time_sec')}`",
            f"- baseline_mean_time_sec: `{metrics.get('baseline_mean_time_sec')}`",
            f"- time_improvement_pct: `{metrics.get('time_improvement_pct')}`",
            f"- optimized_mean_curves: `{metrics.get('optimized_mean_curves')}`",
            f"- baseline_mean_curves: `{metrics.get('baseline_mean_curves')}`",
            f"- curves_improvement_pct: `{metrics.get('curves_improvement_pct')}`",
            f"- optimized_mean_success_rate: `{metrics.get('optimized_mean_success_rate')}`",
            f"- baseline_mean_success_rate: `{metrics.get('baseline_mean_success_rate')}`",
            f"- success_rate_delta_pp: `{metrics.get('success_rate_delta_pp')}`",
        ]
    )

    if trace_plot_files:
        lines.append("- trace plots:")
        for plot_name, plot_path in sorted(trace_plot_files.items()):
            rel_plot = plot_path.relative_to(report_dir)
            lines.append(f"  - {plot_name}: [`{rel_plot.name}`]({rel_plot.as_posix()})")
            lines.append(f"![{plot_name}]({rel_plot.as_posix()})")

    lines.extend(["", "---", ""])
    report_file.write_text("\n".join(lines), encoding="utf-8")



@click.command("validate")
@click.option("--dataset", type=str, help="Dataset file path OR generated dataset folder name under data/numbers. Defaults to the latest generated dataset.")
@click.option("--ecm-bin", default=ECM_PATH, show_default=True, type=str, help="Path to the GMP-ECM executable.")
@click.option(
    "--opt-result-file",
    type=str,
    help=(
        "Optimization result JSON reference. "
        "Supports file path or file name inside current dataset experiments folder. "
        "Defaults to latest optimize result (for selected dataset, or globally if dataset is omitted)."
    ),
)
@click.option("--opt-b1", type=int, help="Manual optimized B1 value. If set, both --opt-b1 and --opt-b2 are required.")
@click.option("--opt-b2", type=int, help="Manual optimized B2 value. If set, both --opt-b1 and --opt-b2 are required.")
@click.option("--base-b1", type=int, help="Manual baseline B1 value; overrides automatic baseline selection.")
@click.option("--base-b2", type=int, help="Manual baseline B2 value; overrides automatic baseline selection.")
@click.option(
    "--max-curves-per-n",
    type=int,
    help=(
        "Maximum number of ECM curves per repeated run during validation. "
        "Defaults to value from optimization result when available."
    ),
)
@click.option(
    "--repeats-per-n",
    type=int,
    help=(
        "Repeated stop-on-success runs per number during validation. "
        "Defaults to value from optimization result when available."
    ),
)
@click.option(
    "--curve-timeout-sec",
    type=float,
    help=(
        "Optional timeout in seconds for a single ECM curve run. "
        "Defaults to value from optimization result when available."
    ),
)
@click.option("--workers", default=DEFAULT_WORKERS, show_default=True, type=int, help="Number of worker processes; use -1 to use all CPUs.")
@click.option("--results-dir", default=str(EXPERIMENTS_DIR), show_default=True, type=click.Path(path_type=Path), help="Directory where validation result JSON files will be saved.")
@click.option("--verbose/--no-verbose", default=True, show_default=True, help="Print validation progress during the run.")
@click.option("--seed", type=int, help="Seed recorded in validation metadata. Defaults to dataset generation seed.")
def validate_command(
    dataset: str | None,
    ecm_bin: str,
    opt_result_file: str | None,
    opt_b1: int | None,
    opt_b2: int | None,
    base_b1: int | None,
    base_b2: int | None,
    max_curves_per_n: int | None,
    repeats_per_n: int | None,
    curve_timeout_sec: float | None,
    workers: int,
    results_dir: Path,
    seed: int | None,
    verbose: bool,
) -> None:
    """Сравнить оптимизированные параметры с baseline на control-датасете."""
    dataset_path: Path | None = resolve_dataset_path(dataset, expected_file="control.json") if dataset else None
    if opt_b1 is not None or opt_b2 is not None:
        if opt_b1 is None or opt_b2 is None:
            raise click.UsageError("When using manual optimized params, provide both --opt-b1 and --opt-b2")
        opt_pair = (opt_b1, opt_b2)
        opt_method = "manual"
        detected_digits = None
        resolved_opt_result_file: Path | None = None
        if dataset_path is None:
            dataset_path = resolve_dataset_path(None, expected_file="control.json")
        max_curves_per_n = max_curves_per_n if max_curves_per_n is not None else DEFAULT_VALIDATION_MAX_CURVES_PER_N
        repeats_per_n = repeats_per_n if repeats_per_n is not None else DEFAULT_VALIDATION_REPEATS_PER_N
        curve_timeout_sec = curve_timeout_sec if curve_timeout_sec is not None else DEFAULT_CURVE_TIMEOUT_SEC
    else:
        resolved_opt_result_file = resolve_opt_result_file(
            opt_result_file,
            dataset_path=dataset_path,
            results_dir=results_dir,
        )
        opt_data = read_json(resolved_opt_result_file)
        if dataset_path is None:
            dataset_from_opt = opt_data.get("dataset")
            if not isinstance(dataset_from_opt, str):
                raise click.UsageError("Optimization result does not contain a valid 'dataset' field.")
            dataset_from_opt_path = Path(dataset_from_opt)
            dataset_path = dataset_from_opt_path.parent / "control.json"
            if not dataset_path.exists():
                raise click.UsageError(
                    f"Cannot resolve control dataset from optimization result: {dataset_path}"
                )
        opt_pair = (int(opt_data["optimized"]["b1"]), int(opt_data["optimized"]["b2"]))
        opt_method = str(
            opt_data.get("optimized", {}).get(
                "method",
                opt_data.get("config", {}).get("method", "unknown"),
            )
        )
        detected_digits = opt_data.get("dataset_target_digits")
        opt_config = opt_data.get("config", {})
        if not isinstance(opt_config, dict):
            opt_config = {}
        max_curves_per_n = int(opt_config.get("max_curves_per_n", DEFAULT_VALIDATION_MAX_CURVES_PER_N)) if max_curves_per_n is None else max_curves_per_n
        repeats_per_n = int(opt_config.get("repeats_per_n", DEFAULT_VALIDATION_REPEATS_PER_N)) if repeats_per_n is None else repeats_per_n
        curve_timeout_sec = opt_config.get("curve_timeout_sec", DEFAULT_CURVE_TIMEOUT_SEC) if curve_timeout_sec is None else curve_timeout_sec

    if dataset_path is None:
        raise click.UsageError("Cannot resolve dataset for validation.")

    numbers = load_numbers(dataset_path)
    if seed is None:
        seed = dataset_generation_seed(dataset_path, fallback=DEFAULT_SEED)

    if base_b1 is not None and base_b2 is not None:
        base_pair = (base_b1, base_b2)
        base_source = "manual"
        base_target_digits = _parse_target_digits(dataset_path, detected_digits)
    else:
        td = _parse_target_digits(dataset_path, detected_digits)
        baseline = choose_baseline(td)
        base_pair = (baseline.b1, baseline.b2)
        base_source = baseline.source
        base_target_digits = baseline.target_digits

    workers = resolve_workers(workers)
    summary = validate_on_control(
        ecm_bin=ecm_bin,
        numbers=numbers,
        optimized=opt_pair,
        baseline=base_pair,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
        verbose=verbose,
        method=opt_method if opt_method and opt_method != "unknown" else None,
    )

    click.echo(f"optimized_mean_score={summary.optimized_mean_score:.6f}")
    click.echo(f"baseline_mean_score={summary.baseline_mean_score:.6f}")
    click.echo(f"relative_improvement_pct={summary.relative_improvement_pct:.2f}")
    click.echo(f"optimized_mean_time_sec={summary.optimized_mean_time_sec:.6f}")
    click.echo(f"baseline_mean_time_sec={summary.baseline_mean_time_sec:.6f}")
    click.echo(f"time_improvement_pct={summary.time_improvement_pct:.2f}")
    click.echo(f"optimized_mean_curves={summary.optimized_mean_curves:.6f}")
    click.echo(f"baseline_mean_curves={summary.baseline_mean_curves:.6f}")
    click.echo(f"curves_improvement_pct={summary.curves_improvement_pct:.2f}")
    click.echo(f"optimized_mean_success_rate={summary.optimized_mean_success_rate:.6f}")
    click.echo(f"baseline_mean_success_rate={summary.baseline_mean_success_rate:.6f}")
    click.echo(f"success_rate_delta_pp={summary.success_rate_delta_pp:.4f}")
    click.echo(f"used_opt_b1={opt_pair[0]}")
    click.echo(f"used_opt_b2={opt_pair[1]}")
    click.echo(f"used_opt_method={opt_method}")
    click.echo(f"used_base_b1={base_pair[0]}")
    click.echo(f"used_base_b2={base_pair[1]}")

    if resolved_opt_result_file is not None:
        out_dir = ensure_dir(resolved_opt_result_file.parent)
    else:
        dataset_name = dataset_path.parent.name
        out_dir = ensure_dir(results_dir / dataset_name)
    out_file = out_dir / f"{opt_method}_validate_{utc_timestamp()}.json"
    payload = {
        "dataset": str(dataset_path),
        "ecm_bin": ecm_bin,
        "max_curves_per_n": max_curves_per_n,
        "repeats_per_n": repeats_per_n,
        "curve_timeout_sec": curve_timeout_sec,
        "workers": workers,
        "seed": seed,
        "optimized": {
            "method": opt_method,
            "b1": opt_pair[0],
            "b2": opt_pair[1],
            "source_file": str(resolved_opt_result_file) if resolved_opt_result_file else None,
        },
        "baseline": {
            "b1": base_pair[0],
            "b2": base_pair[1],
            "source": base_source,
            "table_target_digits": base_target_digits,
        },
        "metrics": {
            "optimized_mean_score": summary.optimized_mean_score,
            "baseline_mean_score": summary.baseline_mean_score,
            "relative_improvement_pct": summary.relative_improvement_pct,
            "optimized_mean_time_sec": summary.optimized_mean_time_sec,
            "baseline_mean_time_sec": summary.baseline_mean_time_sec,
            "time_improvement_pct": summary.time_improvement_pct,
            "optimized_mean_curves": summary.optimized_mean_curves,
            "baseline_mean_curves": summary.baseline_mean_curves,
            "curves_improvement_pct": summary.curves_improvement_pct,
            "optimized_mean_success_rate": summary.optimized_mean_success_rate,
            "baseline_mean_success_rate": summary.baseline_mean_success_rate,
            "success_rate_delta_pp": summary.success_rate_delta_pp,
        },
        "trace": {
            "by_number": list(summary.trace_by_number),
        },
    }
    write_json_with_meta(out_file, payload, command="validate")

    trace_plot_files = _build_validation_trace_plots(out_file, payload["trace"]["by_number"])
    if trace_plot_files:
        payload["plots"] = {name: str(path) for name, path in trace_plot_files.items()}
        write_json_with_meta(out_file, payload, command="validate")
    if resolved_opt_result_file is not None:
        report_file = resolved_opt_result_file.with_name(f"{resolved_opt_result_file.stem}_report.md")
    else:
        report_file = out_file.with_name(f"validate_{_extract_run_timestamp(out_file.stem)}_report.md")
    _append_validation_section(
        report_file,
        out_file=out_file,
        payload=payload,
        trace_plot_files=trace_plot_files,
    )

    click.echo(f"result_file: {out_file}")
    click.echo(f"report_file: {report_file}")
