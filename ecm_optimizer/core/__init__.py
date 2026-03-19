"""Ядро вычислительной логики ECM optimizer."""

from .baseline import BASELINE_TABLE, BaselineChoice, choose_baseline
from .fitness import evaluate_pair_for_n, fitness_expected_time
from .problem import GeneratedSample, generate_semiprime_samples, load_numbers, read_dataset_metadata
from .validation import ValidationSummary, validate_on_control

__all__ = [
    "BASELINE_TABLE",
    "BaselineChoice",
    "GeneratedSample",
    "ValidationSummary",
    "choose_baseline",
    "evaluate_pair_for_n",
    "fitness_expected_time",
    "generate_semiprime_samples",
    "load_numbers",
    "read_dataset_metadata",
    "validate_on_control",
]
