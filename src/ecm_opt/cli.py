from __future__ import annotations

import argparse
from pathlib import Path

from .dataset import generate_semiprime_samples, write_dataset, write_manifest
from .models import OptimizationConfig


def load_numbers(path: str) -> list[int]:
    values: list[int] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(int(line))
    return values


def cmd_optimize(args: argparse.Namespace) -> int:
    from .optimizer import optimize_parameters

    numbers = load_numbers(args.dataset)
    config = OptimizationConfig(
        curves_per_n=args.curves_per_n,
        popsize=args.popsize,
        maxiter=args.maxiter,
        seed=args.seed,
    )
    result = optimize_parameters(ecm_bin=args.ecm_bin, numbers=numbers, config=config)
    print(f"best_b1={result.b1}")
    print(f"best_b2={result.b2}")
    print(f"objective={result.objective:.6f}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    from .validation import validate_on_control

    numbers = load_numbers(args.dataset)
    summary = validate_on_control(
        ecm_bin=args.ecm_bin,
        numbers=numbers,
        optimized=(args.opt_b1, args.opt_b2),
        baseline=(args.base_b1, args.base_b2),
        curves_per_n=args.curves_per_n,
    )
    print(f"optimized_mean={summary.optimized_mean:.6f}")
    print(f"baseline_mean={summary.baseline_mean:.6f}")
    print(f"relative_improvement_pct={summary.relative_improvement_pct:.2f}")
    return 0


def cmd_generate_dataset(args: argparse.Namespace) -> int:
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
    p_opt.set_defaults(func=cmd_optimize)

    p_val = sub.add_parser("validate", help="compare optimized parameters against baseline")
    p_val.add_argument("--dataset", required=True)
    p_val.add_argument("--ecm-bin", default="ecm")
    p_val.add_argument("--opt-b1", required=True, type=int)
    p_val.add_argument("--opt-b2", required=True, type=int)
    p_val.add_argument("--base-b1", required=True, type=int)
    p_val.add_argument("--base-b2", required=True, type=int)
    p_val.add_argument("--curves-per-n", type=int, default=100)
    p_val.set_defaults(func=cmd_validate)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
