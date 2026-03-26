"""Алгоритмы оптимизации параметров ECM."""

from .base import Optimizer
from .differential_evolution import DifferentialEvolutionOptimizer, optimize_parameters
from .heuristic_optimizers import BayesianOptimizationOptimizer, GeneticAlgorithmOptimizer, ParticleSwarmOptimizer
from .random_search import RandomSearchOptimizer

OPTIMIZER_ALIASES: dict[str, str] = {
    "de": "de",
    "differential-evolution": "de",
    "random-search": "rs",
    "rs": "rs",
    "pso": "pso",
    "particle-swarm-optimization": "pso",
    "bayesian-optimization": "bo",
    "bo": "bo",
    "ga": "ga",
    "genetic-algorithm": "ga",
}


def normalize_optimizer_method(method: str) -> str:
    """Нормализовать пользовательское имя метода оптимизации."""
    return OPTIMIZER_ALIASES.get(method.lower(), method.lower())


def create_optimizer(method: str) -> Optimizer:
    """Создать инстанс оптимизатора по имени метода."""
    normalized = normalize_optimizer_method(method)
    if normalized == "de":
        return DifferentialEvolutionOptimizer()
    if normalized == "rs":
        return RandomSearchOptimizer()
    if normalized == "pso":
        return ParticleSwarmOptimizer()
    if normalized == "bo":
        return BayesianOptimizationOptimizer()
    if normalized == "ga":
        return GeneticAlgorithmOptimizer()
    raise NotImplementedError(
        f"Optimization method '{method}' is planned but not implemented yet. "
        "Available methods now: de, rs, pso, bo, ga."
    )


__all__ = [
    "BayesianOptimizationOptimizer",
    "DifferentialEvolutionOptimizer",
    "GeneticAlgorithmOptimizer",
    "Optimizer",
    "ParticleSwarmOptimizer",
    "RandomSearchOptimizer",
    "create_optimizer",
    "normalize_optimizer_method",
    "optimize_parameters",
]
