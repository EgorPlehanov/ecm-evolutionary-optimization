from __future__ import annotations

from dataclasses import dataclass
from statistics import median

from scipy.stats import mannwhitneyu


@dataclass(frozen=True)
class MannWhitneyResult:
    u_statistic: float
    p_value: float
    alternative: str


def safe_median(values: list[float]) -> float:
    if not values:
        return 0.0
    return float(median(values))


def mann_whitney_optimized_faster(optimized_scores: list[float], baseline_scores: list[float]) -> MannWhitneyResult:
    """One-sided Mann-Whitney test for H1: optimized_scores < baseline_scores."""
    if not optimized_scores or not baseline_scores:
        return MannWhitneyResult(u_statistic=0.0, p_value=1.0, alternative="less")

    result = mannwhitneyu(optimized_scores, baseline_scores, alternative="less", method="auto")
    return MannWhitneyResult(
        u_statistic=float(result.statistic),
        p_value=float(result.pvalue),
        alternative="less",
    )

