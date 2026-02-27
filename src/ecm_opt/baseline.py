from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class BaselineChoice:
    target_digits: int
    b1: int
    b2: int
    source: str


# Practical placeholder defaults for automated runs.
# Users can still override explicitly from CLI if needed.
BASELINE_TABLE: dict[int, tuple[int, int]] = {
    20: (2_000, 40_000),
    25: (11_000, 220_000),
    30: (50_000, 1_000_000),
    35: (250_000, 5_000_000),
    40: (1_000_000, 20_000_000),
    45: (3_000_000, 60_000_000),
    50: (11_000_000, 220_000_000),
}


def choose_baseline(target_digits: int | None) -> BaselineChoice:
    if target_digits is None:
        b1, b2 = BASELINE_TABLE[35]
        return BaselineChoice(target_digits=35, b1=b1, b2=b2, source="default_fallback")

    if target_digits in BASELINE_TABLE:
        b1, b2 = BASELINE_TABLE[target_digits]
        return BaselineChoice(target_digits=target_digits, b1=b1, b2=b2, source="exact_table")

    nearest = min(BASELINE_TABLE, key=lambda d: abs(d - target_digits))
    b1, b2 = BASELINE_TABLE[nearest]
    return BaselineChoice(target_digits=nearest, b1=b1, b2=b2, source=f"nearest_for_{target_digits}")
