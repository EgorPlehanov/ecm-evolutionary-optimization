from __future__ import annotations

import math
from typing import Iterable

from scipy.optimize import differential_evolution

from ecm_optimizer.core.fitness import fitness_with_stats
from ecm_optimizer.models import OptimizationConfig, OptimizationResult
from ecm_optimizer.optimizers.base import Optimizer
from ecm_optimizer.optimizers.heuristic_common import ProgressTracker, decode_candidate
from ecm_optimizer.utils.seed_utils import get_seed


class DifferentialEvolutionOptimizer(Optimizer):
    """Оптимизатор на основе `scipy.optimize.differential_evolution`."""

    def optimize(self, *, ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
        de_params = config.method_params.get("de", {})
        popsize = int(de_params.get("popsize", config.popsize))
        maxiter = int(de_params.get("maxiter", config.maxiter))
        low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
        low2, high2 = math.log10(max(config.b2_min, config.b1_min)), math.log10(config.b2_max)

        numbers = list(numbers)
        objective_calls = 0
        progress = ProgressTracker(method="de")
        progress.log_step(
            config=config,
            message=(
                f"numbers={len(numbers)} max_curves_per_n={config.max_curves_per_n} repeats_per_n={config.repeats_per_n} "
                f"popsize={popsize} maxiter={maxiter} workers={config.workers}"
            ),
        )

        if config.verbose:
            print(
                f"[optimize:de] numbers={len(numbers)} max_curves_per_n={config.max_curves_per_n} "
                f"repeats_per_n={config.repeats_per_n} popsize={popsize} maxiter={maxiter} workers={config.workers}",
                flush=True,
            )

        def objective(x: tuple[float, float]) -> float:
            nonlocal objective_calls
            objective_calls += 1
            b1, b2 = decode_candidate((x[0], x[1]), config=config)
            value, metrics = fitness_with_stats(
                ecm_bin=ecm_bin,
                numbers=numbers,
                b1=b1,
                b2=b2,
                max_curves_per_n=config.max_curves_per_n,
                repeats_per_n=config.repeats_per_n,
                curve_timeout_sec=config.curve_timeout_sec,
                workers=config.workers,
            )
            progress.eval_count = objective_calls - 1
            progress.on_evaluation(config=config, x_log=(x[0], x[1]), score=value, metrics=metrics)
            progress.on_new_best(config=config, x_log=(x[0], x[1]), score=value, eval_id=progress.eval_count)
            return value

        generation = 0

        def on_iteration(*args: object, **kwargs: object) -> bool:
            nonlocal generation
            generation += 1
            best_fitness = progress.best_score if progress.best_score is not None else float("nan")
            progress.log_step(
                config=config,
                message=f"generation={generation}/{maxiter} best_fitness={best_fitness}",
            )
            return False

        result = differential_evolution(
            objective,
            bounds=[(low1, high1), (low2, high2)],
            strategy="best1bin",
            popsize=popsize,
            maxiter=maxiter,
            mutation=(0.5, 0.9),
            recombination=0.8,
            seed=get_seed(config.seed, "differential-evolution"),
            callback=on_iteration,
            polish=False,
            disp=config.verbose,
        )

        b1, b2 = decode_candidate((result.x[0], result.x[1]), config=config)
        return OptimizationResult(b1=b1, b2=b2, objective=float(result.fun), history=progress.events)


def optimize_parameters(ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
    """Совместимая обертка для запуска DE-оптимизации."""
    return DifferentialEvolutionOptimizer().optimize(ecm_bin=ecm_bin, numbers=numbers, config=config)
