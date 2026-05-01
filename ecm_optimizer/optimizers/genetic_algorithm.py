from __future__ import annotations

import math
import random
from typing import Iterable

from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.optimizers.base import Optimizer
from ecm_optimizer.optimizers.heuristic_common import EvaluatedPoint, ProgressTracker, candidate_from_rng, evaluate_candidate, evaluated_point_to_result
from ecm_optimizer.utils.seed_utils import get_seed


class GeneticAlgorithmOptimizer(Optimizer):
    """Генетический алгоритм с tournament-selection и гауссовой мутацией."""

    def optimize(self, *, ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
        ga_params = config.method_params.get("ga", {})
        population_size = int(ga_params.get("population_size", max(8, config.popsize * 2)))
        generations = int(ga_params.get("generations", max(1, config.maxiter)))
        mutation_prob = float(ga_params.get("mutation_prob", 0.2))
        mutation_sigma = float(ga_params.get("mutation_sigma", 0.15))
        tournament_size = int(ga_params.get("tournament_size", 3))
        elite_count = int(ga_params.get("elite_count", 1))

        rng = random.Random(get_seed(config.seed, "genetic-algorithm"))
        numbers = list(numbers)
        low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
        low2, high2 = math.log10(max(config.b2_min, config.b1_min)), math.log10(config.b2_max)
        progress = ProgressTracker(method="ga")
        progress.log_step(
            config=config,
            message=(
                f"numbers={len(numbers)} max_curves_per_n={config.max_curves_per_n} repeats_per_n={config.repeats_per_n} "
                f"population_size={population_size} generations={generations} mutation_prob={mutation_prob} workers={config.workers}"
            ),
        )

        def clip_gene(x: tuple[float, float]) -> tuple[float, float]:
            return min(max(x[0], low1), high1), min(max(x[1], low2), high2)

        def tournament(pop: list[EvaluatedPoint]) -> EvaluatedPoint:
            participants = rng.sample(pop, k=min(tournament_size, len(pop)))
            return min(participants, key=lambda p: p.score)

        population = [
            evaluate_candidate(x_log=candidate_from_rng(rng, config), ecm_bin=ecm_bin, numbers=numbers, config=config, progress=progress)
            for _ in range(population_size)
        ]
        best = min(population, key=lambda p: p.score)
        progress.on_new_best(config=config, x_log=best.x, score=best.score, eval_id=best.eval_id)
        progress.log_step(config=config, message=f"init_best fitness={best.score}")

        for generation in range(1, generations + 1):
            ordered = sorted(population, key=lambda p: p.score)
            next_population: list[EvaluatedPoint] = ordered[: max(1, min(elite_count, len(ordered)))]

            while len(next_population) < population_size:
                p_a = tournament(population).x
                p_b = tournament(population).x
                alpha = rng.random()
                child = (alpha * p_a[0] + (1 - alpha) * p_b[0], alpha * p_a[1] + (1 - alpha) * p_b[1])
                if rng.random() < mutation_prob:
                    child = (child[0] + rng.gauss(0, mutation_sigma), child[1] + rng.gauss(0, mutation_sigma))
                child = clip_gene(child)
                next_population.append(evaluate_candidate(x_log=child, ecm_bin=ecm_bin, numbers=numbers, config=config, progress=progress))

            population = next_population
            gen_best = min(population, key=lambda p: p.score)
            if gen_best.score < best.score:
                best = gen_best
                progress.on_new_best(config=config, x_log=best.x, score=best.score, eval_id=best.eval_id)
            progress.log_step(config=config, message=f"generation={generation}/{generations} best_fitness={best.score}")

        return evaluated_point_to_result(best, config, history=progress.events)
