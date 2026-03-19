"""Публичный API пакета для оптимизации параметров ECM."""

from .config import PACKAGE_VERSION
from .models import EvaluationResult, OptimizationConfig, OptimizationResult

__all__ = [
    "EvaluationResult",
    "OptimizationConfig",
    "OptimizationResult",
    "PACKAGE_VERSION",
]
