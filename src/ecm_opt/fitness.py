from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from statistics import mean
from typing import Iterable

from .ecm_runner import run_single_curve
from .models import EvaluationResult


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


def evaluate_pair_for_n(
    ecm_bin: str,
    n: int,
    b1: int,
    b2: int,
    curves_per_n: int,
    curve_timeout_sec: float | None = None,
) -> EvaluationResult:
    successes = 0
    total_seconds = 0.0
    for _ in range(curves_per_n):
        run = run_single_curve(ecm_bin=ecm_bin, n=n, b1=b1, b2=b2, timeout_sec=curve_timeout_sec)
        total_seconds += run.seconds
        if run.success:
            successes += 1
    return EvaluationResult(n=n, successes=successes, curves=curves_per_n, total_seconds=total_seconds)


def fitness_expected_time(
    ecm_bin: str,
    numbers: Iterable[int],
    b1: int,
    b2: int,
    curves_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
) -> float:
    numbers = list(numbers)
    tasks = [(ecm_bin, n, b1, b2, curves_per_n, curve_timeout_sec) for n in numbers]

    if workers == 1:
        scores = [_evaluate_expected_time_task(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            scores = list(executor.map(_evaluate_expected_time_task, tasks))

    return mean(scores)
