from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import math
from typing import Iterable

from ecm_optimizer.core.fitness import fitness_with_stats


@dataclass(frozen=True)
class ValidationSummary:
    """Сводка сравнения optimized/baseline по новой composite-метрике."""

    optimized_mean_score: float
    baseline_mean_score: float
    relative_improvement_pct: float
    optimized_mean_time_sec: float
    baseline_mean_time_sec: float
    time_improvement_pct: float
    optimized_mean_curves: float
    baseline_mean_curves: float
    curves_improvement_pct: float
    optimized_mean_success_rate: float
    baseline_mean_success_rate: float
    success_rate_delta_pp: float
    trace_by_number: tuple[dict[str, float | int], ...]


def _evaluate_single_number_task(args: tuple[str, int, int, int, int, int, float | None]) -> dict[str, float | int]:
    """Вычислить score+метрики для одного числа `n`."""
    ecm_bin, n, b1, b2, max_curves_per_n, repeats_per_n, curve_timeout_sec = args
    score, stats = fitness_with_stats(
        ecm_bin=ecm_bin,
        numbers=[n],
        b1=b1,
        b2=b2,
        max_curves_per_n=max_curves_per_n,
        repeats_per_n=repeats_per_n,
        curve_timeout_sec=curve_timeout_sec,
        workers=1,
    )
    return {
        "n": n,
        "score": score,
        "success_runs": int(stats["success_runs"]),
        "total_runs": int(stats["total_runs"]),
        "mean_success_rate": float(stats["mean_success_rate"]),
        "mean_curves_to_outcome": float(stats["mean_curves_to_outcome"]),
        "mean_time_to_outcome_sec": float(stats["mean_time_to_outcome_sec"]),
    }


def _evaluate_many(
    tasks: list[tuple[str, int, int, int, int, int, float | None]],
    workers: int,
    *,
    verbose: bool = False,
    label: str = "",
    log_prefix: str = "[validate]",
) -> list[dict[str, float | int]]:
    """Запустить пакет задач последовательно или параллельно и вернуть score+метрики."""
    if workers == 1:
        values: list[dict[str, float | int]] = []
        for idx, task in enumerate(tasks, start=1):
            values.append(_evaluate_single_number_task(task))
            if verbose:
                print(f"{log_prefix} {label} {idx}/{len(tasks)}", flush=True)
        return values

    with ProcessPoolExecutor(max_workers=workers) as executor:
        values: list[dict[str, float | int]] = []
        for idx, value in enumerate(executor.map(_evaluate_single_number_task, tasks), start=1):
            values.append(value)
            if verbose:
                print(f"{log_prefix} {label} {idx}/{len(tasks)}", flush=True)
        return values


def validate_on_control(
    ecm_bin: str,
    numbers: Iterable[int],
    optimized: tuple[int, int],
    baseline: tuple[int, int],
    max_curves_per_n: int,
    repeats_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
    verbose: bool = False,
    method: str | None = None,
) -> ValidationSummary:
    """Сравнить оптимизированные и базовые параметры на контрольной выборке."""
    numbers = list(numbers)
    opt_tasks = [
        (ecm_bin, n, optimized[0], optimized[1], max_curves_per_n, repeats_per_n, curve_timeout_sec)
        for n in numbers
    ]
    base_tasks = [
        (ecm_bin, n, baseline[0], baseline[1], max_curves_per_n, repeats_per_n, curve_timeout_sec)
        for n in numbers
    ]

    method_suffix = f":{method}" if method else ""
    log_prefix = f"[validate{method_suffix}]"

    if verbose:
        print(
            f"{log_prefix} numbers={len(numbers)} max_curves_per_n={max_curves_per_n} repeats_per_n={repeats_per_n} workers={workers}",
            flush=True,
        )

    opt_scores = _evaluate_many(opt_tasks, workers, verbose=verbose, label="optimized", log_prefix=log_prefix)
    base_scores = _evaluate_many(base_tasks, workers, verbose=verbose, label="baseline", log_prefix=log_prefix)

    trace_by_number: list[dict[str, float | int]] = []
    for n, opt_point, base_point in zip(numbers, opt_scores, base_scores):
        optimized_score = float(opt_point["score"])
        baseline_score = float(base_point["score"])
        delta_abs = baseline_score - optimized_score
        delta_pct = (
            (delta_abs / baseline_score * 100.0)
            if baseline_score != 0 and math.isfinite(baseline_score) and math.isfinite(optimized_score)
            else 0.0
        )
        trace_by_number.append(
            {
                "n": n,
                "optimized_score": optimized_score,
                "baseline_score": baseline_score,
                "delta_abs": delta_abs,
                "delta_pct": delta_pct,
                "optimized_success_rate": float(opt_point["mean_success_rate"]),
                "baseline_success_rate": float(base_point["mean_success_rate"]),
                "optimized_mean_curves": float(opt_point["mean_curves_to_outcome"]),
                "baseline_mean_curves": float(base_point["mean_curves_to_outcome"]),
                "optimized_mean_time_sec": float(opt_point["mean_time_to_outcome_sec"]),
                "baseline_mean_time_sec": float(base_point["mean_time_to_outcome_sec"]),
                "delta_pct_time": (
                    (
                        (float(base_point["mean_time_to_outcome_sec"]) - float(opt_point["mean_time_to_outcome_sec"]))
                        / float(base_point["mean_time_to_outcome_sec"])
                        * 100.0
                    )
                    if float(base_point["mean_time_to_outcome_sec"]) != 0
                    else 0.0
                ),
                "delta_pct_curves": (
                    (
                        (float(base_point["mean_curves_to_outcome"]) - float(opt_point["mean_curves_to_outcome"]))
                        / float(base_point["mean_curves_to_outcome"])
                        * 100.0
                    )
                    if float(base_point["mean_curves_to_outcome"]) != 0
                    else 0.0
                ),
            }
        )

    optimized_mean = sum(float(point["score"]) for point in opt_scores) / len(opt_scores)
    baseline_mean = sum(float(point["score"]) for point in base_scores) / len(base_scores)
    if baseline_mean == 0 or not math.isfinite(baseline_mean) or not math.isfinite(optimized_mean):
        relative = 0.0
    else:
        relative = (baseline_mean - optimized_mean) / baseline_mean * 100.0

    optimized_mean_time = sum(float(point["mean_time_to_outcome_sec"]) for point in opt_scores) / len(opt_scores)
    baseline_mean_time = sum(float(point["mean_time_to_outcome_sec"]) for point in base_scores) / len(base_scores)
    if baseline_mean_time == 0 or not math.isfinite(baseline_mean_time) or not math.isfinite(optimized_mean_time):
        time_improvement_pct = 0.0
    else:
        time_improvement_pct = (baseline_mean_time - optimized_mean_time) / baseline_mean_time * 100.0

    optimized_mean_curves = sum(float(point["mean_curves_to_outcome"]) for point in opt_scores) / len(opt_scores)
    baseline_mean_curves = sum(float(point["mean_curves_to_outcome"]) for point in base_scores) / len(base_scores)
    if baseline_mean_curves == 0 or not math.isfinite(baseline_mean_curves) or not math.isfinite(optimized_mean_curves):
        curves_improvement_pct = 0.0
    else:
        curves_improvement_pct = (baseline_mean_curves - optimized_mean_curves) / baseline_mean_curves * 100.0

    optimized_mean_success_rate = sum(float(point["mean_success_rate"]) for point in opt_scores) / len(opt_scores)
    baseline_mean_success_rate = sum(float(point["mean_success_rate"]) for point in base_scores) / len(base_scores)
    success_rate_delta_pp = (optimized_mean_success_rate - baseline_mean_success_rate) * 100.0

    return ValidationSummary(
        optimized_mean_score=optimized_mean,
        baseline_mean_score=baseline_mean,
        relative_improvement_pct=relative,
        optimized_mean_time_sec=optimized_mean_time,
        baseline_mean_time_sec=baseline_mean_time,
        time_improvement_pct=time_improvement_pct,
        optimized_mean_curves=optimized_mean_curves,
        baseline_mean_curves=baseline_mean_curves,
        curves_improvement_pct=curves_improvement_pct,
        optimized_mean_success_rate=optimized_mean_success_rate,
        baseline_mean_success_rate=baseline_mean_success_rate,
        success_rate_delta_pp=success_rate_delta_pp,
        trace_by_number=tuple(trace_by_number),
    )
