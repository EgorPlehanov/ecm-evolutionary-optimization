from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from statistics import mean
from typing import Iterable

from ecm_optimizer.config import DEFAULT_BASELINE_B1, DEFAULT_BASELINE_B2

EPSILON = 1e-9

# Допуски и коэффициенты новой fitness-модели.
SUCCESS_TOLERANCE = 0.01  # 1 п.п.
TIME_TOLERANCE = 0.0  # время не должно деградировать
SUCCESS_PENALTY_WEIGHT = 50.0
TIME_PENALTY_WEIGHT = 20.0
TIME_DELTA_WEIGHT = 1.0
CURVE_DELTA_WEIGHT = 0.35

from ecm_optimizer.core.ecm_runner import run_single_curve
from ecm_optimizer.models import EvaluationResult

_BASELINE_METRICS_CACHE: dict[tuple[str, tuple[int, ...], int, int, float | None], tuple[float, float, float]] = {}


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
    - нормализация времени/кривых относительно baseline (`DEFAULT_BASELINE_B1/B2`);
    - штраф за падение success_rate относительно baseline (с небольшим допуском);
    - штраф за деградацию времени относительно baseline;
    - линейный вклад дельт времени и кривых (время важнее кривых).
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
    baseline_success_rate, baseline_curves, baseline_time = _baseline_metrics(
        ecm_bin=ecm_bin,
        numbers=numbers,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
    )

    delta_success = baseline_success_rate - mean_success_rate
    delta_curves = (mean_curves - baseline_curves) / (baseline_curves + EPSILON)
    delta_time = (mean_time - baseline_time) / (baseline_time + EPSILON)

    success_penalty = SUCCESS_PENALTY_WEIGHT * max(0.0, delta_success - SUCCESS_TOLERANCE) ** 2
    time_penalty = TIME_PENALTY_WEIGHT * max(0.0, delta_time - TIME_TOLERANCE) ** 2
    score = success_penalty + time_penalty + (TIME_DELTA_WEIGHT * delta_time) + (CURVE_DELTA_WEIGHT * delta_curves)
    stats: dict[str, float | int] = {
        "success_runs": sum(item.success_runs for item in evaluations),
        "total_runs": sum(item.runs for item in evaluations),
        "mean_success_rate": mean_success_rate,
        "mean_curves_to_outcome": mean_curves,
        "mean_time_to_outcome_sec": mean_time,
        "baseline_success_rate": baseline_success_rate,
        "baseline_curves_to_outcome": baseline_curves,
        "baseline_time_to_outcome_sec": baseline_time,
        "delta_success_vs_baseline": delta_success,
        "delta_curves_vs_baseline": delta_curves,
        "delta_time_vs_baseline": delta_time,
        "success_penalty": success_penalty,
        "time_penalty": time_penalty,
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


def _baseline_metrics(
    ecm_bin: str,
    numbers: list[int],
    max_curves_per_n: int,
    repeats_per_n: int,
    curve_timeout_sec: float | None,
    workers: int,
) -> tuple[float, float, float]:
    key = (ecm_bin, tuple(numbers), max_curves_per_n, repeats_per_n, curve_timeout_sec)
    cached = _BASELINE_METRICS_CACHE.get(key)
    if cached is not None:
        return cached

    baseline_evaluations = _evaluate_many(
        ecm_bin=ecm_bin,
        numbers=numbers,
        b1=DEFAULT_BASELINE_B1,
        b2=DEFAULT_BASELINE_B2,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=workers,
    )
    baseline_metrics = _mean_metrics(baseline_evaluations)
    _BASELINE_METRICS_CACHE[key] = baseline_metrics
    return baseline_metrics
