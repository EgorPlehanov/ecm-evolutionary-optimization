"""Публичный API пакета для оптимизации параметров ECM.

Модуль переэкспортирует основные структуры данных, чтобы внешний код мог
импортировать их напрямую из `ecm_opt`, не зная внутреннюю структуру пакета.
"""

from .models import EvaluationResult, OptimizationConfig, OptimizationResult

__all__ = [
    "EvaluationResult",
    "OptimizationConfig",
    "OptimizationResult",
]
