from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import DEFAULT_B1_RANGE, DEFAULT_B2_RANGE, DEFAULT_CURVE_TIMEOUT_SEC, DEFAULT_CURVES_PER_N, DEFAULT_MAXITER, DEFAULT_POPSIZE, DEFAULT_RATIO_MAX, DEFAULT_SEED, DEFAULT_WORKERS, ECM_PATH, EXPERIMENTS_DIR
from ecm_optimizer.core.baseline import choose_baseline
from ecm_optimizer.core.problem import load_numbers, read_dataset_metadata
from ecm_optimizer.models import OptimizationConfig, resolve_workers
from ecm_optimizer.optimizers.differential_evolution import optimize_parameters
from ecm_optimizer.utils.io_utils import ensure_dir, write_json_with_meta


def _parse_target_digits(dataset_path: Path, fallback: int | None = None) -> int | None:
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("target_digits")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


@click.command("optimize")
@click.option("--dataset", required=True, type=click.Path(exists=True, path_type=Path))
@click.option("--ecm-bin", default=ECM_PATH, show_default=True, type=str)
@click.option("--curves-per-n", default=DEFAULT_CURVES_PER_N, show_default=True, type=int)
@click.option("--popsize", default=DEFAULT_POPSIZE, show_default=True, type=int)
@click.option("--maxiter", default=DEFAULT_MAXITER, show_default=True, type=int)
@click.option("--seed", default=DEFAULT_SEED, show_default=True, type=int)
@click.option("--b1-min", default=DEFAULT_B1_RANGE[0], show_default=True, type=float)
@click.option("--b1-max", default=DEFAULT_B1_RANGE[1], show_default=True, type=float)
@click.option("--b2-min", default=DEFAULT_B2_RANGE[0], show_default=True, type=float)
@click.option("--b2-max", default=DEFAULT_B2_RANGE[1], show_default=True, type=float)
@click.option("--ratio-max", default=DEFAULT_RATIO_MAX, show_default=True, type=float)
@click.option("--curve-timeout-sec", default=DEFAULT_CURVE_TIMEOUT_SEC, type=float)
@click.option("--workers", default=DEFAULT_WORKERS, show_default=True, type=int)
@click.option("--results-dir", default=str(EXPERIMENTS_DIR), show_default=True, type=click.Path(path_type=Path))
@click.option("--verbose", is_flag=True)
def optimize_command(
    dataset: Path,
    ecm_bin: str,
    curves_per_n: int,
    popsize: int,
    maxiter: int,
    seed: int,
    b1_min: float,
    b1_max: float,
    b2_min: float,
    b2_max: float,
    ratio_max: float,
    curve_timeout_sec: float | None,
    workers: int,
    results_dir: Path,
    verbose: bool,
) -> None:
    """Запустить оптимизацию параметров `(B1, B2)` на train-датасете."""
    numbers = load_numbers(dataset)
    workers = resolve_workers(workers)
    config = OptimizationConfig(
        b1_min=b1_min,
        b1_max=b1_max,
        b2_min=b2_min,
        b2_max=b2_max,
        ratio_max=ratio_max,
        curves_per_n=curves_per_n,
        popsize=popsize,
        maxiter=maxiter,
        seed=seed,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
        verbose=verbose,
    )
    result = optimize_parameters(ecm_bin=ecm_bin, numbers=numbers, config=config)

    click.echo(f"best_b1={result.b1}")
    click.echo(f"best_b2={result.b2}")
    click.echo(f"objective={result.objective:.6f}")

    target_digits = _parse_target_digits(dataset)
    baseline = choose_baseline(target_digits)

    out_dir = ensure_dir(results_dir)
    out_file = out_dir / f"optimize_{dataset.stem}_{seed}.json"
    payload = {
        "dataset": str(dataset),
        "dataset_target_digits": target_digits,
        "ecm_bin": ecm_bin,
        "config": {
            "b1_min": b1_min,
            "b1_max": b1_max,
            "b2_min": b2_min,
            "b2_max": b2_max,
            "ratio_max": ratio_max,
            "curves_per_n": curves_per_n,
            "popsize": popsize,
            "maxiter": maxiter,
            "seed": seed,
            "curve_timeout_sec": curve_timeout_sec,
            "workers": workers,
        },
        "optimized": {"b1": result.b1, "b2": result.b2, "objective": result.objective},
        "suggested_baseline": {
            "b1": baseline.b1,
            "b2": baseline.b2,
            "table_target_digits": baseline.target_digits,
            "source": baseline.source,
        },
    }
    write_json_with_meta(out_file, payload, command="optimize")
    click.echo(f"result_file={out_file}")
