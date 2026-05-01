from __future__ import annotations

import math
import random
from typing import Iterable

from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.optimizers.base import Optimizer
from ecm_optimizer.optimizers.heuristic_common import ProgressTracker, candidate_from_rng, evaluate_candidate, evaluated_point_to_result
from ecm_optimizer.utils.seed_utils import get_seed


class ParticleSwarmOptimizer(Optimizer):
    """Простой PSO в логарифмическом пространстве `(log10(B1), log10(B2))`."""

    def optimize(self, *, ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
        pso_params = config.method_params.get("pso", {})
        swarm_size = int(pso_params.get("swarm_size", max(8, config.popsize * 2)))
        iterations = int(pso_params.get("iterations", max(1, config.maxiter)))
        inertia = float(pso_params.get("inertia", 0.7))
        cognitive = float(pso_params.get("cognitive", 1.4))
        social = float(pso_params.get("social", 1.4))
        velocity_scale = float(pso_params.get("velocity_scale", 0.2))

        rng = random.Random(get_seed(config.seed, "particle-swarm-optimization"))
        numbers = list(numbers)
        low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
        low2, high2 = math.log10(max(config.b2_min, config.b1_min)), math.log10(config.b2_max)
        span1, span2 = high1 - low1, high2 - low2
        progress = ProgressTracker(method="pso")

        progress.log_step(
            config=config,
            message=(
                f"numbers={len(numbers)} max_curves_per_n={config.max_curves_per_n} repeats_per_n={config.repeats_per_n} "
                f"swarm_size={swarm_size} iterations={iterations} workers={config.workers}"
            ),
        )

        positions = [candidate_from_rng(rng, config) for _ in range(swarm_size)]
        velocities = [
            (rng.uniform(-span1 * velocity_scale, span1 * velocity_scale), rng.uniform(-span2 * velocity_scale, span2 * velocity_scale))
            for _ in range(swarm_size)
        ]
        personal_best = [evaluate_candidate(x_log=pos, ecm_bin=ecm_bin, numbers=numbers, config=config, progress=progress) for pos in positions]
        global_best = min(personal_best, key=lambda p: p.score)
        progress.on_new_best(config=config, x_log=global_best.x, score=global_best.score, eval_id=global_best.eval_id)
        progress.log_step(config=config, message=f"init_best fitness={global_best.score}")

        for iteration in range(1, iterations + 1):
            for i in range(swarm_size):
                x1, x2 = positions[i]
                v1, v2 = velocities[i]
                p1, p2 = personal_best[i].x
                g1, g2 = global_best.x
                r1, r2 = rng.random(), rng.random()
                r3, r4 = rng.random(), rng.random()

                nv1 = inertia * v1 + cognitive * r1 * (p1 - x1) + social * r3 * (g1 - x1)
                nv2 = inertia * v2 + cognitive * r2 * (p2 - x2) + social * r4 * (g2 - x2)
                nx1 = min(max(x1 + nv1, low1), high1)
                nx2 = min(max(x2 + nv2, low2), high2)

                velocities[i] = (nv1, nv2)
                positions[i] = (nx1, nx2)
                current = evaluate_candidate(x_log=positions[i], ecm_bin=ecm_bin, numbers=numbers, config=config, progress=progress)
                if current.score < personal_best[i].score:
                    personal_best[i] = current
                    if current.score < global_best.score:
                        global_best = current
                        progress.on_new_best(config=config, x_log=global_best.x, score=global_best.score, eval_id=global_best.eval_id)
            progress.log_step(config=config, message=f"iteration={iteration}/{iterations} best_fitness={global_best.score}")

        return evaluated_point_to_result(global_best, config, history=progress.events)
