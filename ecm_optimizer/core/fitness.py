from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from statistics import mean
from typing import Iterable

SUCCESS_RATE_WEIGHT = 1_000_000.0
CURVE_WEIGHT = 1_000.0
TIME_WEIGHT = 1.0

from ecm_optimizer.core.ecm_runner import run_single_curve
from ecm_optimizer.models import EvaluationResult


def _evaluate_pair_task(args: tuple[str, int, int, int, int, int, float | None]) -> EvaluationResult:
    """Подготовить и выполнить одну задачу оценки для конкретного числа `n`."""
    ecm_bin, n, b1, b2, max_curves_per_n, repeats_per_n, curve_timeout_sec = args
    return evaluate_pair_for_n(
        ecm_bin=ecm_bin,
        n=n,
        b1=b1,
        b2=b2,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
    )


def evaluate_pair_for_n(
    ecm_bin: str,
    n: int,
    b1: int,
    b2: int,
    max_curves_per_n: int,
    repeats_per_n: int,
    curve_timeout_sec: float | None = None,
) -> EvaluationResult:
    """Оценить пару `(B1, B2)` на одном числе `n` по логике stop-on-success."""
    success_runs = 0
    total_curves = 0
    total_seconds = 0.0

    for _ in range(repeats_per_n):
        run_success = False
        for curve_idx in range(1, max_curves_per_n + 1):
            run = run_single_curve(ecm_bin=ecm_bin, n=n, b1=b1, b2=b2, timeout_sec=curve_timeout_sec)
            total_seconds += run.seconds
            total_curves += 1
            if run.success:
                run_success = True
                break
        if run_success:
            success_runs += 1

    return EvaluationResult(
        n=n,
        success_runs=success_runs,
        runs=repeats_per_n,
        total_curves=total_curves,
        total_seconds=total_seconds,
    )


def fitness_with_stats(
    ecm_bin: str,
    numbers: Iterable[int],
    b1: int,
    b2: int,
    max_curves_per_n: int,
    repeats_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
) -> tuple[float, dict[str, float | int]]:
    """Вычислить composite fitness по набору чисел.

    Fitness минимизируется:
    - максимизирует success_rate (через штраф 1-success_rate);
    - минимизирует среднее число кривых до исхода (успех или лимит);
    - минимизирует среднее время до исхода.
    """
    numbers = list(numbers)
    tasks = [(ecm_bin, n, b1, b2, max_curves_per_n, repeats_per_n, curve_timeout_sec) for n in numbers]

    if workers == 1:
        evaluations = [_evaluate_pair_task(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            evaluations = list(executor.map(_evaluate_pair_task, tasks))

    mean_success_rate = mean(item.success_rate for item in evaluations)
    mean_curves = mean(item.avg_curves for item in evaluations)
    mean_time = mean(item.avg_time for item in evaluations)
    score = ((1.0 - mean_success_rate) * SUCCESS_RATE_WEIGHT) + (mean_curves * CURVE_WEIGHT) + (mean_time * TIME_WEIGHT)
    stats: dict[str, float | int] = {
        "success_runs": sum(item.success_runs for item in evaluations),
        "total_runs": sum(item.runs for item in evaluations),
        "mean_success_rate": mean_success_rate,
        "mean_curves_to_outcome": mean_curves,
        "mean_time_to_outcome_sec": mean_time,
    }
    return score, stats


def fitness_composite(
    ecm_bin: str,
    numbers: Iterable[int],
    b1: int,
    b2: int,
    max_curves_per_n: int,
    repeats_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
) -> float:
    """Вычислить целевую composite fitness-метрику."""
    score, _ = fitness_with_stats(
        ecm_bin=ecm_bin,
        numbers=numbers,
        b1=b1,
        b2=b2,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
    )
    return score
