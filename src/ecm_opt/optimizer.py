from __future__ import annotations

import math
from typing import Iterable

from scipy.optimize import differential_evolution

from .fitness import fitness_expected_time
from .models import OptimizationConfig, OptimizationResult


def _decode_candidate(x_log: tuple[float, float], ratio_max: float) -> tuple[int, int]:
    b1 = int(10 ** x_log[0])
    b2 = int(10 ** x_log[1])
    b2 = max(b2, b1)
    b2 = min(b2, int(b1 * ratio_max))
    return b1, b2


def optimize_parameters(ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
    low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
    low2, high2 = low1, math.log10(config.b1_max * config.ratio_max)

    numbers = list(numbers)

    def objective(x: tuple[float, float]) -> float:
        b1, b2 = _decode_candidate((x[0], x[1]), ratio_max=config.ratio_max)
        return fitness_expected_time(
            ecm_bin=ecm_bin,
            numbers=numbers,
            b1=b1,
            b2=b2,
            curves_per_n=config.curves_per_n,
        )

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
    )

    b1, b2 = _decode_candidate((result.x[0], result.x[1]), ratio_max=config.ratio_max)
    return OptimizationResult(b1=b1, b2=b2, objective=float(result.fun))
