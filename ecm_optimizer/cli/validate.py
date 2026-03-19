from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import DEFAULT_CURVE_TIMEOUT_SEC, DEFAULT_SEED, DEFAULT_VALIDATION_CURVES_PER_N, DEFAULT_WORKERS, ECM_PATH, EXPERIMENTS_DIR
from ecm_optimizer.core.baseline import choose_baseline
from ecm_optimizer.core.problem import load_numbers, read_dataset_metadata
from ecm_optimizer.core.validation import validate_on_control
from ecm_optimizer.models import resolve_workers
from ecm_optimizer.utils.io_utils import ensure_dir, read_json, write_json_with_meta


def _parse_target_digits(dataset_path: Path, fallback: int | None = None) -> int | None:
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("target_digits")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


@click.command("validate")
@click.option("--dataset", required=True, type=click.Path(exists=True, path_type=Path), help="Path to the control dataset file with composite numbers.")
@click.option("--ecm-bin", default=ECM_PATH, show_default=True, type=str, help="Path to the GMP-ECM executable.")
@click.option("--opt-result-file", type=click.Path(exists=True, path_type=Path), help="Path to a saved optimization result JSON file.")
@click.option("--opt-b1", type=int, help="Optimized B1 value to use when no result file is provided.")
@click.option("--opt-b2", type=int, help="Optimized B2 value to use when no result file is provided.")
@click.option("--base-b1", type=int, help="Manual baseline B1 value; overrides automatic baseline selection.")
@click.option("--base-b2", type=int, help="Manual baseline B2 value; overrides automatic baseline selection.")
@click.option("--curves-per-n", default=DEFAULT_VALIDATION_CURVES_PER_N, show_default=True, type=int, help="Number of ECM curves to run per number during validation.")
@click.option("--curve-timeout-sec", default=DEFAULT_CURVE_TIMEOUT_SEC, type=float, help="Optional timeout in seconds for a single ECM curve run.")
@click.option("--workers", default=DEFAULT_WORKERS, show_default=True, type=int, help="Number of worker processes; use -1 to use all CPUs.")
@click.option("--results-dir", default=str(EXPERIMENTS_DIR), show_default=True, type=click.Path(path_type=Path), help="Directory where validation result JSON files will be saved.")
@click.option("--seed", default=DEFAULT_SEED, show_default=True, type=int, help="Seed recorded in validation metadata for reproducibility bookkeeping.")
def validate_command(
    dataset: Path,
    ecm_bin: str,
    opt_result_file: Path | None,
    opt_b1: int | None,
    opt_b2: int | None,
    base_b1: int | None,
    base_b2: int | None,
    curves_per_n: int,
    curve_timeout_sec: float | None,
    workers: int,
    results_dir: Path,
    seed: int,
) -> None:
    """Сравнить оптимизированные параметры с baseline на control-датасете."""
    numbers = load_numbers(dataset)

    if opt_result_file:
        opt_data = read_json(opt_result_file)
        opt_pair = (int(opt_data["optimized"]["b1"]), int(opt_data["optimized"]["b2"]))
        detected_digits = opt_data.get("dataset_target_digits")
    else:
        if opt_b1 is None or opt_b2 is None:
            raise click.UsageError("Provide --opt-result-file or both --opt-b1 and --opt-b2")
        opt_pair = (opt_b1, opt_b2)
        detected_digits = None

    if base_b1 is not None and base_b2 is not None:
        base_pair = (base_b1, base_b2)
        base_source = "manual"
        base_target_digits = _parse_target_digits(dataset, detected_digits)
    else:
        td = _parse_target_digits(dataset, detected_digits)
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
        curves_per_n=curves_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
    )

    click.echo(f"optimized_mean={summary.optimized_mean:.6f}")
    click.echo(f"baseline_mean={summary.baseline_mean:.6f}")
    click.echo(f"relative_improvement_pct={summary.relative_improvement_pct:.2f}")
    click.echo(f"used_opt_b1={opt_pair[0]}")
    click.echo(f"used_opt_b2={opt_pair[1]}")
    click.echo(f"used_base_b1={base_pair[0]}")
    click.echo(f"used_base_b2={base_pair[1]}")

    out_dir = ensure_dir(results_dir)
    out_file = out_dir / f"validate_{dataset.stem}_{seed}.json"
    payload = {
        "dataset": str(dataset),
        "ecm_bin": ecm_bin,
        "curves_per_n": curves_per_n,
        "curve_timeout_sec": curve_timeout_sec,
        "workers": workers,
        "seed": seed,
        "optimized": {"b1": opt_pair[0], "b2": opt_pair[1], "source_file": str(opt_result_file) if opt_result_file else None},
        "baseline": {
            "b1": base_pair[0],
            "b2": base_pair[1],
            "source": base_source,
            "table_target_digits": base_target_digits,
        },
        "metrics": {
            "optimized_mean": summary.optimized_mean,
            "baseline_mean": summary.baseline_mean,
            "relative_improvement_pct": summary.relative_improvement_pct,
        },
    }
    write_json_with_meta(out_file, payload, command="validate")
    click.echo(f"result_file={out_file}")
