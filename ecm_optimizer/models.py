from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Any

from ecm_optimizer.config import (
    DEFAULT_B1_RANGE,
    DEFAULT_B2_RANGE,
    DEFAULT_MAXITER,
    DEFAULT_MAX_CURVES_PER_N,
    DEFAULT_POPSIZE,
    DEFAULT_RATIO_MAX,
    DEFAULT_REPEATS_PER_N,
    DEFAULT_SEED,
    DEFAULT_WORKERS,
)


def resolve_workers(workers: int | None) -> int:
    """Нормализовать число процессов, запрошенное пользователем."""
    if workers is None or workers == 0:
        return 1
    if workers < 0:
        return os.cpu_count() or 1
    return workers


@dataclass(frozen=True)
class EvaluationResult:
    """Статистика repeated-run оценки ECM для одного числа `n`."""

    n: int
    success_runs: int
    runs: int
    total_curves: int
    total_seconds: float

    @property
    def success_rate(self) -> float:
        return self.success_runs / self.runs if self.runs > 0 else 0.0

    @property
    def avg_curves(self) -> float:
        return self.total_curves / self.runs if self.runs > 0 else 0.0

    @property
    def avg_time(self) -> float:
        return self.total_seconds / self.runs if self.runs > 0 else 0.0


@dataclass(frozen=True)
class OptimizationConfig:
    """Параметры запуска оптимизатора и измерений ECM."""

    b1_min: float = DEFAULT_B1_RANGE[0]
    b1_max: float = DEFAULT_B1_RANGE[1]
    b2_min: float = DEFAULT_B2_RANGE[0]
    b2_max: float = DEFAULT_B2_RANGE[1]
    ratio_max: float = DEFAULT_RATIO_MAX
    max_curves_per_n: int = DEFAULT_MAX_CURVES_PER_N
    repeats_per_n: int = DEFAULT_REPEATS_PER_N
    popsize: int = DEFAULT_POPSIZE
    maxiter: int = DEFAULT_MAXITER
    seed: int = DEFAULT_SEED
    curve_timeout_sec: float | None = None
    workers: int = DEFAULT_WORKERS
    verbose: bool = False
    method: str = "de"
    method_params: dict[str, dict[str, Any]] = field(default_factory=dict)


@dataclass(frozen=True)
class OptimizationResult:
    """Лучшее решение, найденное оптимизатором."""

    b1: int
    b2: int
    objective: float
    history: list[dict[str, Any]] = field(default_factory=list)
