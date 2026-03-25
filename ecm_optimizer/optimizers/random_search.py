from __future__ import annotations

import math
import random
from typing import Iterable

from ecm_optimizer.core.fitness import fitness_expected_time
from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.optimizers.base import Optimizer
from ecm_optimizer.utils.seed_utils import get_seed


class RandomSearchOptimizer(Optimizer):
    """Простая baseline-эвристика случайного поиска по логарифмической сетке."""

    def optimize(self, *, ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
        rng = random.Random(get_seed(config.seed, "random-search"))
        numbers = list(numbers)
        best: OptimizationResult | None = None

        rs_params = config.method_params.get("rs", {})
        budget = int(rs_params.get("budget", max(4, config.popsize * max(1, config.maxiter))))
        for _ in range(budget):
            b1 = int(10 ** rng.uniform(math.log10(config.b1_min), math.log10(config.b1_max)))
            b2 = int(10 ** rng.uniform(math.log10(max(config.b2_min, b1)), math.log10(config.b2_max)))
            b2 = min(max(b2, b1), int(b1 * config.ratio_max), int(config.b2_max))
            score = fitness_expected_time(
                ecm_bin=ecm_bin,
                numbers=numbers,
                b1=b1,
                b2=b2,
                curves_per_n=config.curves_per_n,
                curve_timeout_sec=config.curve_timeout_sec,
                workers=config.workers,
            )
            candidate = OptimizationResult(b1=b1, b2=b2, objective=score)
            if best is None or candidate.objective < best.objective:
                best = candidate

        assert best is not None
        return best
