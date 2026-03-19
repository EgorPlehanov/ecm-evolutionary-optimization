from __future__ import annotations

from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import math
from typing import Iterable

from .fitness import evaluate_pair_for_n


@dataclass(frozen=True)
class ValidationSummary:
    """Сводка сравнения оптимизированных и базовых параметров на control-наборе."""

    optimized_mean: float
    baseline_mean: float
    relative_improvement_pct: float


def _evaluate_expected_time_task(args: tuple[str, int, int, int, int, float | None]) -> float:
    """Вычислить ожидаемое время факторизации для одной задачи валидации.

    Args:
        args: Кортеж с бинарником ECM, числом `n`, парой `(B1, B2)` и настройками запуска.

    Returns:
        Ожидаемое время факторизации для одного числа.
    """
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
    """Запустить пакет задач последовательно или параллельно и вернуть их оценки.

    Args:
        tasks: Список задач оценки ожидаемого времени.
        workers: Число worker-процессов.

    Returns:
        Список оценок, по одной на каждую задачу.
    """
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
    """Сравнить оптимизированные и базовые параметры на контрольной выборке.

    Args:
        ecm_bin: Путь к бинарнику `ecm`.
        numbers: Контрольный набор составных чисел.
        optimized: Оптимизированная пара `(B1, B2)`.
        baseline: Базовая пара `(B1, B2)` для сравнения.
        curves_per_n: Количество кривых на одно число.
        curve_timeout_sec: Таймаут для одного запуска кривой.
        workers: Число worker-процессов.

    Returns:
        Сводка со средними значениями и относительным улучшением.
    """
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
