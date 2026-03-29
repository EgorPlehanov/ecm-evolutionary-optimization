from __future__ import annotations

import math
import random
from dataclasses import dataclass

from ecm_optimizer.core.fitness import fitness_expected_time
from ecm_optimizer.models import OptimizationConfig, OptimizationResult


def decode_candidate(x_log: tuple[float, float], config: OptimizationConfig) -> tuple[int, int]:
    """Преобразовать точку в логарифмическом пространстве в допустимые `(B1, B2)`."""
    b1 = int(10 ** x_log[0])
    b2 = int(10 ** x_log[1])
    b1 = min(max(b1, int(config.b1_min)), int(config.b1_max))
    b2 = max(b2, b1, int(config.b2_min))
    b2 = min(b2, int(config.b2_max), int(b1 * config.ratio_max))
    return b1, b2


def candidate_from_rng(rng: random.Random, config: OptimizationConfig) -> tuple[float, float]:
    low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
    low2, high2 = math.log10(max(config.b2_min, config.b1_min)), math.log10(config.b2_max)
    return rng.uniform(low1, high1), rng.uniform(low2, high2)


@dataclass(frozen=True)
class EvaluatedPoint:
    x: tuple[float, float]
    score: float


def evaluate_candidate(
    *,
    x_log: tuple[float, float],
    ecm_bin: str,
    numbers: list[int],
    config: OptimizationConfig,
) -> EvaluatedPoint:
    """Вычислить fitness для кандидата в лог-пространстве."""
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
    if config.run_recorder is not None:
        config.run_recorder.record_evaluation(b1=b1, b2=b2, fitness=score)
    return EvaluatedPoint(x=x_log, score=score)


def evaluated_point_to_result(point: EvaluatedPoint, config: OptimizationConfig) -> OptimizationResult:
    """Преобразовать оцененную точку в стандартный OptimizationResult."""
    b1, b2 = decode_candidate(point.x, config)
    return OptimizationResult(b1=b1, b2=b2, objective=point.score)
