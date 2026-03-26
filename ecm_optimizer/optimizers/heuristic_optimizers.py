from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Iterable

from ecm_optimizer.core.fitness import fitness_expected_time
from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.optimizers.base import Optimizer
from ecm_optimizer.utils.seed_utils import get_seed


def decode_candidate(x_log: tuple[float, float], config: OptimizationConfig) -> tuple[int, int]:
    """Преобразовать точку в логарифмическом пространстве в допустимые `(B1, B2)`."""
    b1 = int(10 ** x_log[0])
    b2 = int(10 ** x_log[1])
    b1 = min(max(b1, int(config.b1_min)), int(config.b1_max))
    b2 = max(b2, b1, int(config.b2_min))
    b2 = min(b2, int(config.b2_max), int(b1 * config.ratio_max))
    return b1, b2


def _candidate_from_rng(rng: random.Random, config: OptimizationConfig) -> tuple[float, float]:
    low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
    low2, high2 = math.log10(max(config.b2_min, config.b1_min)), math.log10(config.b2_max)
    return rng.uniform(low1, high1), rng.uniform(low2, high2)


@dataclass(frozen=True)
class _EvaluatedPoint:
    x: tuple[float, float]
    score: float


class _HeuristicBase(Optimizer):
    """База для эвристик с общим способом вычисления fitness."""

    def _evaluate(
        self,
        *,
        x_log: tuple[float, float],
        ecm_bin: str,
        numbers: list[int],
        config: OptimizationConfig,
    ) -> _EvaluatedPoint:
        b1, b2 = decode_candidate(x_log, config)
        score = fitness_expected_time(
            ecm_bin=ecm_bin,
            numbers=numbers,
            b1=b1,
            b2=b2,
            curves_per_n=config.curves_per_n,
            curve_timeout_sec=config.curve_timeout_sec,
            workers=config.workers,
        )
        return _EvaluatedPoint(x=x_log, score=score)

    @staticmethod
    def _to_result(point: _EvaluatedPoint, config: OptimizationConfig) -> OptimizationResult:
        b1, b2 = decode_candidate(point.x, config)
        return OptimizationResult(b1=b1, b2=b2, objective=point.score)


class ParticleSwarmOptimizer(_HeuristicBase):
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

        positions = [_candidate_from_rng(rng, config) for _ in range(swarm_size)]
        velocities = [
            (rng.uniform(-span1 * velocity_scale, span1 * velocity_scale), rng.uniform(-span2 * velocity_scale, span2 * velocity_scale))
            for _ in range(swarm_size)
        ]
        personal_best = [self._evaluate(x_log=pos, ecm_bin=ecm_bin, numbers=numbers, config=config) for pos in positions]
        global_best = min(personal_best, key=lambda p: p.score)

        for _ in range(iterations):
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
                current = self._evaluate(x_log=positions[i], ecm_bin=ecm_bin, numbers=numbers, config=config)
                if current.score < personal_best[i].score:
                    personal_best[i] = current
                    if current.score < global_best.score:
                        global_best = current

        return self._to_result(global_best, config)


class GeneticAlgorithmOptimizer(_HeuristicBase):
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

        def clip_gene(x: tuple[float, float]) -> tuple[float, float]:
            return min(max(x[0], low1), high1), min(max(x[1], low2), high2)

        def tournament(pop: list[_EvaluatedPoint]) -> _EvaluatedPoint:
            participants = rng.sample(pop, k=min(tournament_size, len(pop)))
            return min(participants, key=lambda p: p.score)

        population = [self._evaluate(x_log=_candidate_from_rng(rng, config), ecm_bin=ecm_bin, numbers=numbers, config=config) for _ in range(population_size)]
        best = min(population, key=lambda p: p.score)

        for _ in range(generations):
            ordered = sorted(population, key=lambda p: p.score)
            next_population: list[_EvaluatedPoint] = ordered[: max(1, min(elite_count, len(ordered)))]

            while len(next_population) < population_size:
                p_a = tournament(population).x
                p_b = tournament(population).x
                alpha = rng.random()
                child = (alpha * p_a[0] + (1 - alpha) * p_b[0], alpha * p_a[1] + (1 - alpha) * p_b[1])
                if rng.random() < mutation_prob:
                    child = (child[0] + rng.gauss(0, mutation_sigma), child[1] + rng.gauss(0, mutation_sigma))
                child = clip_gene(child)
                next_population.append(self._evaluate(x_log=child, ecm_bin=ecm_bin, numbers=numbers, config=config))

            population = next_population
            gen_best = min(population, key=lambda p: p.score)
            if gen_best.score < best.score:
                best = gen_best

        return self._to_result(best, config)


class BayesianOptimizationOptimizer(_HeuristicBase):
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
        evaluated: list[_EvaluatedPoint] = []

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
            x = _candidate_from_rng(rng, config)
            evaluated.append(self._evaluate(x_log=x, ecm_bin=ecm_bin, numbers=numbers, config=config))

        for _ in range(iterations):
            pool = [_candidate_from_rng(rng, config) for _ in range(candidate_pool)]
            candidate = min(pool, key=surrogate_lcb)
            evaluated.append(self._evaluate(x_log=candidate, ecm_bin=ecm_bin, numbers=numbers, config=config))

        best = min(evaluated, key=lambda p: p.score)
        return self._to_result(best, config)
