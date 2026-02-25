from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

from .fitness import evaluate_pair_for_n


@dataclass(frozen=True)
class ValidationSummary:
    optimized_mean: float
    baseline_mean: float
    relative_improvement_pct: float


def validate_on_control(
    ecm_bin: str,
    numbers: Iterable[int],
    optimized: tuple[int, int],
    baseline: tuple[int, int],
    curves_per_n: int,
) -> ValidationSummary:
    numbers = list(numbers)

    opt_scores = [
        evaluate_pair_for_n(ecm_bin=ecm_bin, n=n, b1=optimized[0], b2=optimized[1], curves_per_n=curves_per_n).expected_time
        for n in numbers
    ]
    base_scores = [
        evaluate_pair_for_n(ecm_bin=ecm_bin, n=n, b1=baseline[0], b2=baseline[1], curves_per_n=curves_per_n).expected_time
        for n in numbers
    ]

    optimized_mean = sum(opt_scores) / len(opt_scores)
    baseline_mean = sum(base_scores) / len(base_scores)
    relative = (baseline_mean - optimized_mean) / baseline_mean * 100 if baseline_mean != 0 else 0.0
    return ValidationSummary(
        optimized_mean=optimized_mean,
        baseline_mean=baseline_mean,
        relative_improvement_pct=relative,
    )
