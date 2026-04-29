from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
import math
from statistics import mean
from typing import Iterable

# Коэффициенты baseline-независимой fitness-модели.
# Успех остаётся обязательным: при низком success включается сильный штраф.
TARGET_SUCCESS_RATE = 0.80
SUCCESS_DEFICIT_PENALTY_WEIGHT = 25.0
SUCCESS_WEIGHT = 1.2
TIME_WEIGHT = 1.0
CURVE_WEIGHT = 0.15

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

    Актуальная логика:
    - baseline не участвует в score;
    - baseline не участвует в score;
    - успех факторизации обязателен: действует сильный штраф за недобор `success_rate` до целевого порога;
    - среди кандидатов с приемлемым success минимизируются время и число кривых.
    """
    numbers = list(numbers)
    evaluations = _evaluate_many(
        ecm_bin=ecm_bin,
        numbers=numbers,
        b1=b1,
        b2=b2,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
    )

    mean_success_rate, mean_curves, mean_time = _mean_metrics(evaluations)
    success_penalty = 1.0 - mean_success_rate
    success_deficit = max(0.0, TARGET_SUCCESS_RATE - mean_success_rate)
    success_deficit_penalty = SUCCESS_DEFICIT_PENALTY_WEIGHT * (success_deficit**2)
    time_term = math.log1p(mean_time)
    curves_term = math.log1p(mean_curves)
    score = (
        success_deficit_penalty
        + (SUCCESS_WEIGHT * success_penalty)
        + (TIME_WEIGHT * time_term)
        + (CURVE_WEIGHT * curves_term)
    )
    stats: dict[str, float | int] = {
        "success_runs": sum(item.success_runs for item in evaluations),
        "total_runs": sum(item.runs for item in evaluations),
        "mean_success_rate": mean_success_rate,
        "mean_curves_to_outcome": mean_curves,
        "mean_time_to_outcome_sec": mean_time,
        "target_success_rate": TARGET_SUCCESS_RATE,
        "success_penalty": success_penalty,
        "success_deficit": success_deficit,
        "success_deficit_penalty": success_deficit_penalty,
        "time_term": time_term,
        "curves_term": curves_term,
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


def _evaluate_many(
    ecm_bin: str,
    numbers: list[int],
    b1: int,
    b2: int,
    max_curves_per_n: int,
    repeats_per_n: int,
    curve_timeout_sec: float | None,
    workers: int,
) -> list[EvaluationResult]:
    tasks = [(ecm_bin, n, b1, b2, max_curves_per_n, repeats_per_n, curve_timeout_sec) for n in numbers]
    if workers == 1:
        return [_evaluate_pair_task(task) for task in tasks]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_evaluate_pair_task, tasks))


def _mean_metrics(evaluations: list[EvaluationResult]) -> tuple[float, float, float]:
    return (
        mean(item.success_rate for item in evaluations),
        mean(item.avg_curves for item in evaluations),
        mean(item.avg_time for item in evaluations),
    )
