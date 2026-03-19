from __future__ import annotations

import math
from typing import Iterable

from scipy.optimize import differential_evolution

from .fitness import fitness_expected_time
from .models import OptimizationConfig, OptimizationResult


def _decode_candidate(x_log: tuple[float, float], ratio_max: float) -> tuple[int, int]:
    """Преобразовать точку в логарифмическом пространстве в целые `(B1, B2)`.

    Args:
        x_log: Пара значений в логарифмическом пространстве поиска.
        ratio_max: Максимально допустимое отношение `B2 / B1`.

    Returns:
        Нормализованная пара целочисленных границ ECM.
    """
    b1 = int(10 ** x_log[0])
    b2 = int(10 ** x_log[1])

    b2 = max(b2, b1)
    b2 = min(b2, int(b1 * ratio_max))
    return b1, b2


def optimize_parameters(ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
    """Подобрать параметры `(B1, B2)` с помощью дифференциальной эволюции.

    Args:
        ecm_bin: Путь к бинарнику `ecm`.
        numbers: Набор чисел, по которому оптимизируются параметры.
        config: Конфигурация границ поиска и параметров оптимизатора.

    Returns:
        Лучший найденный набор параметров и значение целевой функции.
    """
    low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
    low2, high2 = low1, math.log10(config.b1_max * config.ratio_max)

    numbers = list(numbers)
    objective_calls = 0

    if config.verbose:
        print(
            f"[optimize] numbers={len(numbers)} curves_per_n={config.curves_per_n} "
            f"popsize={config.popsize} maxiter={config.maxiter} workers={config.workers}",
            flush=True,
        )

    def objective(x: tuple[float, float]) -> float:
        """Обернуть fitness-функцию в интерфейс, ожидаемый SciPy.

        Args:
            x: Текущая точка оптимизации в логарифмическом пространстве.

        Returns:
            Значение fitness для кандидата.
        """
        nonlocal objective_calls
        objective_calls += 1
        b1, b2 = _decode_candidate((x[0], x[1]), ratio_max=config.ratio_max)
        value = fitness_expected_time(
            ecm_bin=ecm_bin,
            numbers=numbers,
            b1=b1,
            b2=b2,
            curves_per_n=config.curves_per_n,
            curve_timeout_sec=config.curve_timeout_sec,
            workers=config.workers,
        )

        if config.verbose and objective_calls % 5 == 0:
            print(f"[optimize] eval={objective_calls} b1={b1} b2={b2} fitness={value}", flush=True)
        return value

    result = differential_evolution(
        objective,
        bounds=[(low1, high1), (low2, high2)],
        strategy="best1bin",
        popsize=config.popsize,
        maxiter=config.maxiter,
        mutation=(0.5, 0.9),
        recombination=0.8,
        seed=config.seed,
        polish=False,
        disp=config.verbose,
    )

    b1, b2 = _decode_candidate((result.x[0], result.x[1]), ratio_max=config.ratio_max)
    return OptimizationResult(b1=b1, b2=b2, objective=float(result.fun))
