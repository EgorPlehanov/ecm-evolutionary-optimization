from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import math
from typing import Iterable

from .fitness import evaluate_pair_for_n


@dataclass(frozen=True)
class ValidationSummary:
    optimized_mean: float
    baseline_mean: float
    relative_improvement_pct: float


def _evaluate_expected_time_task(args: tuple[str, int, int, int, int, float | None]) -> float:
    ecm_bin, n, b1, b2, curves_per_n, curve_timeout_sec = args
    return evaluate_pair_for_n(
        ecm_bin=ecm_bin,
        n=n,
        b1=b1,
        b2=b2,
        curves_per_n=curves_per_n,
        curve_timeout_sec=curve_timeout_sec,
    ).expected_time


def _evaluate_many(tasks: list[tuple[str, int, int, int, int, float | None]], workers: int) -> list[float]:
    if workers == 1:
        return [_evaluate_expected_time_task(task) for task in tasks]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_evaluate_expected_time_task, tasks))


def validate_on_control(
    ecm_bin: str,
    numbers: Iterable[int],
    optimized: tuple[int, int],
    baseline: tuple[int, int],
    curves_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
) -> ValidationSummary:
    numbers = list(numbers)

    opt_tasks = [
        (ecm_bin, n, optimized[0], optimized[1], curves_per_n, curve_timeout_sec)
        for n in numbers
    ]
    base_tasks = [
        (ecm_bin, n, baseline[0], baseline[1], curves_per_n, curve_timeout_sec)
        for n in numbers
    ]

    opt_scores = _evaluate_many(opt_tasks, workers)
    base_scores = _evaluate_many(base_tasks, workers)

    optimized_mean = sum(opt_scores) / len(opt_scores)
    baseline_mean = sum(base_scores) / len(base_scores)
    if baseline_mean == 0 or not math.isfinite(baseline_mean) or not math.isfinite(optimized_mean):
        relative = 0.0
    else:
        relative = (baseline_mean - optimized_mean) / baseline_mean * 100
    return ValidationSummary(
        optimized_mean=optimized_mean,
        baseline_mean=baseline_mean,
        relative_improvement_pct=relative,
    )
