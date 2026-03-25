from __future__ import annotations

from dataclasses import dataclass, field
import os
from typing import Any

from ecm_optimizer.config import DEFAULT_B1_RANGE, DEFAULT_B2_RANGE, DEFAULT_CURVES_PER_N, DEFAULT_MAXITER, DEFAULT_POPSIZE, DEFAULT_RATIO_MAX, DEFAULT_SEED, DEFAULT_WORKERS


NO_SUCCESS_PENALTY_MULTIPLIER = 10.0


def resolve_workers(workers: int | None) -> int:
    """Нормализовать число процессов, запрошенное пользователем."""
    if workers is None or workers == 0:
        return 1
    if workers < 0:
        return os.cpu_count() or 1
    return workers


@dataclass(frozen=True)
class EvaluationResult:
    """Статистика многократного запуска ECM для одного числа `n`."""

    n: int
    successes: int
    curves: int
    total_seconds: float

    @property
    def expected_time(self) -> float:
        """Оценить ожидаемое время успеха для данного `n`."""
        if self.successes == 0:
            return self.total_seconds * NO_SUCCESS_PENALTY_MULTIPLIER
        return self.total_seconds / self.successes


@dataclass(frozen=True)
class OptimizationConfig:
    """Параметры запуска оптимизатора и измерений ECM."""

    b1_min: float = DEFAULT_B1_RANGE[0]
    b1_max: float = DEFAULT_B1_RANGE[1]
    b2_min: float = DEFAULT_B2_RANGE[0]
    b2_max: float = DEFAULT_B2_RANGE[1]
    ratio_max: float = DEFAULT_RATIO_MAX
    curves_per_n: int = DEFAULT_CURVES_PER_N
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
