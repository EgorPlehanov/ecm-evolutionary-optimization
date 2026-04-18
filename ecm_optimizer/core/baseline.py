from __future__ import annotations

from dataclasses import dataclass

from ecm_optimizer.config import DEFAULT_BASELINE_B1, DEFAULT_BASELINE_B2, DEFAULT_BASELINE_TARGET_DIGITS


@dataclass(frozen=True)
class BaselineChoice:
    """Описание базовых параметров ECM для сравнения с оптимизированным решением."""

    target_digits: int
    b1: int
    b2: int
    source: str


BASELINE_TABLE: dict[int, tuple[int, int]] = {
    20: (11_000, 220_000),
    25: (50_000, 1_000_000),
    30: (250_000, 5_000_000),
    35: (1_000_000, 20_000_000),
    40: (3_000_000, 60_000_000),
    45: (11_000_000, 220_000_000),
    50: (43_000_000, 860_000_000),
}


def choose_baseline(target_digits: int | None) -> BaselineChoice:
    """Подобрать базовые параметры ECM по размеру искомого множителя."""
    if target_digits is None:
        return BaselineChoice(
            target_digits=DEFAULT_BASELINE_TARGET_DIGITS,
            b1=DEFAULT_BASELINE_B1,
            b2=DEFAULT_BASELINE_B2,
            source="default_fallback",
        )

    if target_digits in BASELINE_TABLE:
        b1, b2 = BASELINE_TABLE[target_digits]
        return BaselineChoice(target_digits=target_digits, b1=b1, b2=b2, source="exact_table")

    nearest = min(BASELINE_TABLE, key=lambda d: abs(d - target_digits))
    b1, b2 = BASELINE_TABLE[nearest]
    return BaselineChoice(target_digits=nearest, b1=b1, b2=b2, source=f"nearest_for_{target_digits}")
