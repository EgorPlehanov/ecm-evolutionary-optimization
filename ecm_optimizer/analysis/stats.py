from __future__ import annotations

import math
import random
from itertools import combinations
from typing import Callable


def _normal_cdf(x: float) -> float:
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _median(values: list[float]) -> float:
    ordered = sorted(values)
    n = len(ordered)
    mid = n // 2
    if n % 2 == 1:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2.0


def _quantile(values: list[float], q: float) -> float:
    ordered = sorted(values)
    if not ordered:
        return math.nan
    if len(ordered) == 1:
        return ordered[0]
    idx = (len(ordered) - 1) * q
    left = math.floor(idx)
    right = math.ceil(idx)
    if left == right:
        return ordered[left]
    frac = idx - left
    return ordered[left] * (1.0 - frac) + ordered[right] * frac


def bootstrap_ci(
    values: list[float],
    *,
    confidence: float = 0.95,
    n_boot: int = 2000,
    rng_seed: int = 42,
    stat_fn: Callable[[list[float]], float] | None = None,
) -> tuple[float, float]:
    if not values:
        return math.nan, math.nan
    if len(values) == 1:
        return values[0], values[0]

    fn = stat_fn or _median
    rng = random.Random(rng_seed)
    n = len(values)
    boot_stats: list[float] = []

    for _ in range(max(100, n_boot)):
        sample = [values[rng.randrange(n)] for _ in range(n)]
        boot_stats.append(fn(sample))

    alpha = 1.0 - confidence
    low = _quantile(boot_stats, alpha / 2.0)
    high = _quantile(boot_stats, 1.0 - alpha / 2.0)
    return low, high


def _mann_whitney_u(x: list[float], y: list[float]) -> tuple[float, float]:
    n1, n2 = len(x), len(y)
    if n1 == 0 or n2 == 0:
        return math.nan, math.nan

    merged = [(value, 0) for value in x] + [(value, 1) for value in y]
    merged.sort(key=lambda item: item[0])

    ranks = [0.0] * len(merged)
    i = 0
    tie_counts: list[int] = []
    while i < len(merged):
        j = i + 1
        while j < len(merged) and merged[j][0] == merged[i][0]:
            j += 1
        avg_rank = (i + 1 + j) / 2.0
        for k in range(i, j):
            ranks[k] = avg_rank
        tie_counts.append(j - i)
        i = j

    rank_sum_x = sum(rank for rank, (_, group) in zip(ranks, merged) if group == 0)
    u1 = rank_sum_x - n1 * (n1 + 1) / 2.0
    u2 = n1 * n2 - u1
    u = min(u1, u2)

    mean_u = n1 * n2 / 2.0
    tie_term = sum(t * t * t - t for t in tie_counts)
    denom = (n1 + n2) * (n1 + n2 - 1)
    tie_correction = 1.0 - (tie_term / denom) if denom > 0 else 1.0
    var_u = n1 * n2 * (n1 + n2 + 1) / 12.0
    var_u *= max(0.0, tie_correction)

    if var_u <= 0.0:
        return u, 1.0

    z = (u - mean_u) / math.sqrt(var_u)
    p_two_sided = 2.0 * (1.0 - _normal_cdf(abs(z)))
    return u, max(0.0, min(1.0, p_two_sided))


def _holm_correction(p_values: list[float]) -> list[float]:
    indexed = sorted(enumerate(p_values), key=lambda item: item[1])
    m = len(p_values)
    adjusted = [1.0] * m
    running_max = 0.0

    for rank, (orig_idx, p_value) in enumerate(indexed, start=1):
        adj = (m - rank + 1) * p_value
        running_max = max(running_max, adj)
        adjusted[orig_idx] = min(1.0, running_max)
    return adjusted


def pairwise_mannwhitney(groups: dict[str, list[float]], *, correction: str = "holm") -> list[dict[str, float | str]]:
    group_names = sorted(groups)
    rows: list[dict[str, float | str]] = []
    raw_p_values: list[float] = []

    for a, b in combinations(group_names, 2):
        u_stat, p_value = _mann_whitney_u(groups[a], groups[b])
        rows.append(
            {
                "group_a": a,
                "group_b": b,
                "u_stat": u_stat,
                "p_raw": p_value,
            }
        )
        raw_p_values.append(p_value)

    if not rows:
        return rows

    if correction == "holm":
        adjusted = _holm_correction(raw_p_values)
    else:
        adjusted = raw_p_values

    for row, p_adj in zip(rows, adjusted):
        row["p_adj"] = p_adj
    return rows


def cliffs_delta(x: list[float], y: list[float]) -> float:
    if not x or not y:
        return math.nan
    gt = 0
    lt = 0
    for a in x:
        for b in y:
            if a > b:
                gt += 1
            elif a < b:
                lt += 1
    total = len(x) * len(y)
    return (gt - lt) / total if total else math.nan


def coefficient_of_variation(values: list[float]) -> float:
    if len(values) < 2:
        return math.nan
    mean_value = _mean(values)
    if mean_value == 0:
        return math.nan
    variance = sum((value - mean_value) ** 2 for value in values) / (len(values) - 1)
    std = math.sqrt(max(0.0, variance))
    return std / abs(mean_value)


def success_rate(values: list[float], threshold: float) -> float:
    if not values:
        return 0.0
    successes = sum(1 for value in values if value <= threshold)
    return successes / len(values)


def effect_size_label(delta: float) -> str:
    if math.isnan(delta):
        return "unknown"
    absolute = abs(delta)
    if absolute < 0.147:
        return "negligible"
    if absolute < 0.33:
        return "small"
    if absolute < 0.474:
        return "medium"
    return "large"
