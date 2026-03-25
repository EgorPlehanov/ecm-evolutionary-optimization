from __future__ import annotations

from pathlib import Path

import click

from ecm_optimizer.cli.dataset_utils import dataset_generation_seed, resolve_dataset_path, resolve_opt_result_file
from ecm_optimizer.config import DEFAULT_CURVE_TIMEOUT_SEC, DEFAULT_SEED, DEFAULT_VALIDATION_CURVES_PER_N, DEFAULT_WORKERS, ECM_PATH, EXPERIMENTS_DIR
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
    "--curves-per-n",
    type=int,
    help=(
        "Number of ECM curves to run per number during validation. "
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
    curves_per_n: int | None,
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
        curves_per_n = curves_per_n if curves_per_n is not None else DEFAULT_VALIDATION_CURVES_PER_N
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
        curves_per_n = int(opt_config.get("curves_per_n", DEFAULT_VALIDATION_CURVES_PER_N)) if curves_per_n is None else curves_per_n
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
        curves_per_n=curves_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
        verbose=verbose,
    )

    click.echo(f"optimized_mean={summary.optimized_mean:.6f}")
    click.echo(f"baseline_mean={summary.baseline_mean:.6f}")
    click.echo(f"relative_improvement_pct={summary.relative_improvement_pct:.2f}")
    click.echo(f"used_opt_b1={opt_pair[0]}")
    click.echo(f"used_opt_b2={opt_pair[1]}")
    click.echo(f"used_opt_method={opt_method}")
    click.echo(f"used_base_b1={base_pair[0]}")
    click.echo(f"used_base_b2={base_pair[1]}")

    dataset_name = dataset_path.parent.name
    out_dir = ensure_dir(results_dir / dataset_name)
    out_file = out_dir / f"validate_{opt_method}_{utc_timestamp()}.json"
    payload = {
        "dataset": str(dataset_path),
        "ecm_bin": ecm_bin,
        "curves_per_n": curves_per_n,
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
            "optimized_mean": summary.optimized_mean,
            "baseline_mean": summary.baseline_mean,
            "relative_improvement_pct": summary.relative_improvement_pct,
        },
    }
    write_json_with_meta(out_file, payload, command="validate")
    click.echo(f"result_file: {out_file}")
