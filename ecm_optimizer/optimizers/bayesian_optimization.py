from __future__ import annotations

import math
import random
from typing import Iterable

from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.optimizers.base import Optimizer
from ecm_optimizer.optimizers.heuristic_common import ProgressTracker, candidate_from_rng, evaluate_candidate, evaluated_point_to_result
from ecm_optimizer.utils.seed_utils import get_seed


class BayesianOptimizationOptimizer(Optimizer):
    """
    Лёгкий surrogate-based поиск:
    - случайный initial design;
    - k-NN surrogate по уже измеренным точкам;
    - выбор следующей точки по минимальному LCB.
    """

    def optimize(self, *, ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
        bo_params = config.method_params.get("bo", {})
        initial_samples = int(bo_params.get("initial_samples", max(6, config.popsize)))
        iterations = int(bo_params.get("iterations", max(1, config.maxiter)))
        candidate_pool = int(bo_params.get("candidate_pool", 64))
        k_neighbors = int(bo_params.get("k_neighbors", 5))
        exploration = float(bo_params.get("exploration", 1.2))

        rng = random.Random(get_seed(config.seed, "bayesian-optimization"))
        numbers = list(numbers)
        evaluated = []
        progress = ProgressTracker(method="bo")
        progress.log_step(
            config=config,
            message=(
                f"numbers={len(numbers)} max_curves_per_n={config.max_curves_per_n} repeats_per_n={config.repeats_per_n} "
                f"initial_samples={initial_samples} iterations={iterations} candidate_pool={candidate_pool} workers={config.workers}"
            ),
        )

        def surrogate_lcb(x: tuple[float, float]) -> float:
            if not evaluated:
                return 0.0
            distances = []
            for point in evaluated:
                dist = math.dist(x, point.x)
                distances.append((dist, point.score))
            distances.sort(key=lambda item: item[0])
            nearest = distances[: max(1, min(k_neighbors, len(distances)))]
            weights = [1.0 / (d + 1e-9) for d, _ in nearest]
            weight_sum = sum(weights)
            mean = sum(w * s for w, (_, s) in zip(weights, nearest)) / weight_sum
            variance = sum(w * (s - mean) ** 2 for w, (_, s) in zip(weights, nearest)) / weight_sum
            return mean - exploration * math.sqrt(max(variance, 0.0))

        for _ in range(initial_samples):
            x = candidate_from_rng(rng, config)
            point = evaluate_candidate(x_log=x, ecm_bin=ecm_bin, numbers=numbers, config=config, progress=progress)
            evaluated.append(point)
            progress.on_new_best(config=config, x_log=point.x, score=point.score, eval_id=point.eval_id)

        progress.log_step(config=config, message=f"initial_design_completed points={len(evaluated)}")
        for iteration in range(1, iterations + 1):
            pool = [candidate_from_rng(rng, config) for _ in range(candidate_pool)]
            candidate = min(pool, key=surrogate_lcb)
            point = evaluate_candidate(x_log=candidate, ecm_bin=ecm_bin, numbers=numbers, config=config, progress=progress)
            evaluated.append(point)
            progress.on_new_best(config=config, x_log=point.x, score=point.score, eval_id=point.eval_id)
            best_score = min(evaluated, key=lambda p: p.score).score
            progress.log_step(config=config, message=f"iteration={iteration}/{iterations} best_fitness={best_score}")

        best = min(evaluated, key=lambda p: p.score)
        return evaluated_point_to_result(best, config, history=progress.events)
