from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.config import DEFAULT_B1_RANGE, DEFAULT_B2_RANGE, DEFAULT_CURVE_TIMEOUT_SEC, DEFAULT_CURVES_PER_N, DEFAULT_MAXITER, DEFAULT_POPSIZE, DEFAULT_RATIO_MAX, DEFAULT_SEED, DEFAULT_WORKERS, ECM_PATH, EXPERIMENTS_DIR, NUMBERS_DIR
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


def _resolve_dataset_path(dataset_ref: str, *, expected_file: str) -> Path:
    """Resolve dataset reference.

    Supports:
    1) full path to a dataset file;
    2) full/relative path to a dataset directory;
    3) only generated folder name under data/numbers.
    """
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


@click.command("optimize")
@click.option("--dataset", required=True, type=str, help="Dataset file path OR generated dataset folder name under data/numbers.")
@click.option("--ecm-bin", default=ECM_PATH, show_default=True, type=str, help="Path to the GMP-ECM executable.")
@click.option("--curves-per-n", default=DEFAULT_CURVES_PER_N, show_default=True, type=int, help="Number of ECM curves to run per number when evaluating fitness.")
@click.option("--popsize", default=DEFAULT_POPSIZE, show_default=True, type=int, help="Population size multiplier for differential evolution.")
@click.option("--maxiter", default=DEFAULT_MAXITER, show_default=True, type=int, help="Maximum number of differential evolution iterations.")
@click.option("--seed", default=DEFAULT_SEED, show_default=True, type=int, help="Base random seed for the optimizer.")
@click.option("--b1-min", default=DEFAULT_B1_RANGE[0], show_default=True, type=float, help="Lower bound for the B1 search range.")
@click.option("--b1-max", default=DEFAULT_B1_RANGE[1], show_default=True, type=float, help="Upper bound for the B1 search range.")
@click.option("--b2-min", default=DEFAULT_B2_RANGE[0], show_default=True, type=float, help="Lower bound for the B2 search range.")
@click.option("--b2-max", default=DEFAULT_B2_RANGE[1], show_default=True, type=float, help="Upper bound for the B2 search range.")
@click.option("--ratio-max", default=DEFAULT_RATIO_MAX, show_default=True, type=float, help="Maximum allowed ratio B2 / B1 for candidate solutions.")
@click.option("--curve-timeout-sec", default=DEFAULT_CURVE_TIMEOUT_SEC, type=float, help="Optional timeout in seconds for a single ECM curve run.")
@click.option("--workers", default=DEFAULT_WORKERS, show_default=True, type=int, help="Number of worker processes; use -1 to use all CPUs.")
@click.option("--results-dir", default=str(EXPERIMENTS_DIR), show_default=True, type=click.Path(path_type=Path), help="Directory where optimization result JSON files will be saved.")
@click.option("--verbose", is_flag=True, help="Print verbose optimization progress during the run.")
def optimize_command(
    dataset: str,
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
    dataset_path = _resolve_dataset_path(dataset, expected_file="train.json")
    numbers = load_numbers(dataset_path)
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

    target_digits = _parse_target_digits(dataset_path)
    baseline = choose_baseline(target_digits)

    out_dir = ensure_dir(results_dir)
    out_file = out_dir / f"optimize_{dataset_path.stem}_{seed}.json"
    payload = {
        "dataset": str(dataset_path),
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
    click.echo(f"result_file: {out_file}")
