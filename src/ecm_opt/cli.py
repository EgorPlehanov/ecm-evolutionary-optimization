from __future__ import annotations

import argparse
from pathlib import Path

from .baseline import choose_baseline
from .dataset import generate_semiprime_samples, read_dataset_metadata, write_dataset, write_manifest
from .io_utils import ensure_dir, read_json, utc_timestamp, write_json
from .models import OptimizationConfig, resolve_workers


def load_numbers(path: str) -> list[int]:
    """Прочитать текстовый датасет и извлечь из него числа `N`.

    Args:
        path: Путь к текстовому файлу с числами и необязательными строками-комментариями.

    Returns:
        Список составных чисел, прочитанных из файла.
    """
    values: list[int] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(int(line))
    return values


def _parse_target_digits(dataset_path: str, fallback: int | None = None) -> int | None:
    """Извлечь из заголовка датасета число цифр целевого множителя.

    Args:
        dataset_path: Путь к файлу датасета.
        fallback: Значение, которое нужно вернуть, если метаданные отсутствуют
            или не могут быть интерпретированы как целое число.

    Returns:
        Количество цифр целевого множителя либо `fallback`.
    """
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("target_digits")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback


def cmd_optimize(args: argparse.Namespace) -> int:
    """Обработчик команды CLI `optimize`.

    Args:
        args: Разобранные аргументы командной строки для запуска оптимизации.

    Returns:
        Код завершения процесса.
    """
    from .optimizer import optimize_parameters

    numbers = load_numbers(args.dataset)
    workers = resolve_workers(args.workers)
    config = OptimizationConfig(
        b1_min=args.b1_min,
        b1_max=args.b1_max,
        ratio_max=args.ratio_max,
        curves_per_n=args.curves_per_n,
        popsize=args.popsize,
        maxiter=args.maxiter,
        seed=args.seed,
        curve_timeout_sec=args.curve_timeout_sec,
        workers=workers,
        verbose=args.verbose,
    )
    result = optimize_parameters(ecm_bin=args.ecm_bin, numbers=numbers, config=config)

    print(f"best_b1={result.b1}")
    print(f"best_b2={result.b2}")
    print(f"objective={result.objective:.6f}")

    target_digits = _parse_target_digits(args.dataset)
    baseline = choose_baseline(target_digits)

    stamp = utc_timestamp()
    out_dir = ensure_dir(args.results_dir)
    out_file = out_dir / f"optimize_{stamp}.json"
    payload = {
        "timestamp_utc": stamp,
        "command": "optimize",
        "dataset": args.dataset,
        "dataset_target_digits": target_digits,
        "ecm_bin": args.ecm_bin,
        "config": {
            "b1_min": args.b1_min,
            "b1_max": args.b1_max,
            "ratio_max": args.ratio_max,
            "curves_per_n": args.curves_per_n,
            "popsize": args.popsize,
            "maxiter": args.maxiter,
            "seed": args.seed,
            "curve_timeout_sec": args.curve_timeout_sec,
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
    write_json(out_file, payload)
    print(f"result_file={out_file}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    """Обработчик команды CLI `validate`.

    Args:
        args: Разобранные аргументы командной строки для запуска валидации.

    Returns:
        Код завершения процесса.
    """
    from .validation import validate_on_control

    numbers = load_numbers(args.dataset)

    if args.opt_result_file:
        opt_data = read_json(args.opt_result_file)
        opt_pair = (int(opt_data["optimized"]["b1"]), int(opt_data["optimized"]["b2"]))
        detected_digits = opt_data.get("dataset_target_digits")
    else:
        if args.opt_b1 is None or args.opt_b2 is None:
            raise SystemExit("Provide --opt-result-file or both --opt-b1 and --opt-b2")
        opt_pair = (args.opt_b1, args.opt_b2)
        detected_digits = None

    if args.base_b1 is not None and args.base_b2 is not None:
        base_pair = (args.base_b1, args.base_b2)
        base_source = "manual"
        base_target_digits = _parse_target_digits(args.dataset, detected_digits)
    else:
        td = _parse_target_digits(args.dataset, detected_digits)
        baseline = choose_baseline(td)
        base_pair = (baseline.b1, baseline.b2)
        base_source = baseline.source
        base_target_digits = baseline.target_digits

    workers = resolve_workers(args.workers)

    summary = validate_on_control(
        ecm_bin=args.ecm_bin,
        numbers=numbers,
        optimized=opt_pair,
        baseline=base_pair,
        curves_per_n=args.curves_per_n,
        curve_timeout_sec=args.curve_timeout_sec,
        workers=workers,
    )
    print(f"optimized_mean={summary.optimized_mean:.6f}")
    print(f"baseline_mean={summary.baseline_mean:.6f}")
    print(f"relative_improvement_pct={summary.relative_improvement_pct:.2f}")
    print(f"used_opt_b1={opt_pair[0]}")
    print(f"used_opt_b2={opt_pair[1]}")
    print(f"used_base_b1={base_pair[0]}")
    print(f"used_base_b2={base_pair[1]}")

    stamp = utc_timestamp()
    out_dir = ensure_dir(args.results_dir)
    out_file = out_dir / f"validate_{stamp}.json"
    payload = {
        "timestamp_utc": stamp,
        "command": "validate",
        "dataset": args.dataset,
        "ecm_bin": args.ecm_bin,
        "curves_per_n": args.curves_per_n,
        "curve_timeout_sec": args.curve_timeout_sec,
        "workers": workers,
        "optimized": {"b1": opt_pair[0], "b2": opt_pair[1], "source_file": args.opt_result_file},
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
    write_json(out_file, payload)
    print(f"result_file={out_file}")
    return 0


def cmd_generate_dataset(args: argparse.Namespace) -> int:
    """Обработчик команды `generate-dataset`, создающий train/control-выборки.

    Args:
        args: Разобранные аргументы командной строки для генерации датасета.

    Returns:
        Код завершения процесса.
    """
    total = args.train_count + args.control_count
    samples = generate_semiprime_samples(
        target_factor_digits=args.target_digits,
        cofactor_digits=args.cofactor_digits,
        count=total,
        seed=args.seed,
    )

    train = samples[: args.train_count]
    control = samples[args.train_count :]

    train_path = f"{args.output_dir}/{args.prefix}_train.txt"
    control_path = f"{args.output_dir}/{args.prefix}_control.txt"
    manifest_path = f"{args.output_dir}/{args.prefix}_manifest.csv"

    write_dataset(
        train_path,
        [s.n for s in train],
        header=(
            f"train dataset: target_digits={args.target_digits}, "
            f"cofactor_digits={args.cofactor_digits}, seed={args.seed}"
        ),
    )
    write_dataset(
        control_path,
        [s.n for s in control],
        header=(
            f"control dataset: target_digits={args.target_digits}, "
            f"cofactor_digits={args.cofactor_digits}, seed={args.seed}"
        ),
    )
    write_manifest(manifest_path, samples)

    print(f"train_file={train_path}")
    print(f"control_file={control_path}")
    print(f"manifest_file={manifest_path}")
    print(f"generated={total}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    """Собрать дерево аргументов командной строки для всего приложения.

    Returns:
        Настроенный объект `ArgumentParser` со всеми подкомандами.
    """
    parser = argparse.ArgumentParser(description="ECM evolutionary optimization toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate-dataset", help="generate train/control semiprime datasets")
    p_gen.add_argument("--target-digits", required=True, type=int, help="digits of target prime factor p")
    p_gen.add_argument("--cofactor-digits", type=int, default=90, help="digits of cofactor prime q")
    p_gen.add_argument("--train-count", type=int, default=20)
    p_gen.add_argument("--control-count", type=int, default=20)
    p_gen.add_argument("--seed", type=int, default=42)
    p_gen.add_argument("--output-dir", default="data")
    p_gen.add_argument("--prefix", default="dset")
    p_gen.set_defaults(func=cmd_generate_dataset)

    p_opt = sub.add_parser("optimize", help="run differential evolution for B1/B2")
    p_opt.add_argument("--dataset", required=True)
    p_opt.add_argument("--ecm-bin", default="ecm")
    p_opt.add_argument("--curves-per-n", type=int, default=50)
    p_opt.add_argument("--popsize", type=int, default=16)
    p_opt.add_argument("--maxiter", type=int, default=25)
    p_opt.add_argument("--seed", type=int, default=42)
    p_opt.add_argument("--b1-min", type=float, default=1e3)
    p_opt.add_argument("--b1-max", type=float, default=1e9)
    p_opt.add_argument("--ratio-max", type=float, default=100.0)
    p_opt.add_argument("--curve-timeout-sec", type=float, default=None)
    p_opt.add_argument("--workers", type=int, default=1, help="number of worker processes (-1 = all CPUs)")
    p_opt.add_argument("--verbose", action="store_true")
    p_opt.add_argument("--results-dir", default="results")
    p_opt.set_defaults(func=cmd_optimize)

    p_val = sub.add_parser("validate", help="compare optimized parameters against baseline")
    p_val.add_argument("--dataset", required=True)
    p_val.add_argument("--ecm-bin", default="ecm")
    p_val.add_argument("--opt-result-file")
    p_val.add_argument("--opt-b1", type=int)
    p_val.add_argument("--opt-b2", type=int)
    p_val.add_argument("--base-b1", type=int)
    p_val.add_argument("--base-b2", type=int)
    p_val.add_argument("--curves-per-n", type=int, default=100)
    p_val.add_argument("--curve-timeout-sec", type=float, default=None)
    p_val.add_argument("--workers", type=int, default=1, help="number of worker processes (-1 = all CPUs)")
    p_val.add_argument("--results-dir", default="results")
    p_val.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    """Точка входа CLI-приложения.

    Returns:
        Код завершения, возвращаемый выбранной подкомандой.
    """
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
