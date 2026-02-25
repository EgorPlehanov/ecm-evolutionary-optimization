from __future__ import annotations

import argparse
from pathlib import Path

from .models import OptimizationConfig
from .optimizer import optimize_parameters
from .validation import validate_on_control


def load_numbers(path: str) -> list[int]:
    values: list[int] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(int(line))
    return values


def cmd_optimize(args: argparse.Namespace) -> int:
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


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ECM evolutionary optimization toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

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
