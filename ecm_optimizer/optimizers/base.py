from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Iterable

from ecm_optimizer.models import OptimizationConfig, OptimizationResult


class Optimizer(ABC):
    """Абстрактный интерфейс оптимизатора пары `(B1, B2)`."""

    @abstractmethod
    def optimize(self, *, ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
        """Подобрать лучшие параметры для заданного набора чисел."""
