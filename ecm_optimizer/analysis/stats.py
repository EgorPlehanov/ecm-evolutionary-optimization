from __future__ import annotations

import math
import random
from statistics import NormalDist


def _clean(values: list[float]) -> list[float]:
    return [float(v) for v in values if v is not None and math.isfinite(float(v))]


def bootstrap_ci(
    values: list[float],
    confidence: float = 0.95,
    n_resamples: int = 10_000,
    seed: int = 42,
) -> dict[str, float]:
    """Percentile bootstrap CI for sample mean."""
    clean = _clean(values)
    if not clean:
        raise ValueError("bootstrap_ci requires at least one numeric value")

    rng = random.Random(seed)
    means: list[float] = []
    n = len(clean)
    for _ in range(n_resamples):
        sample = [clean[rng.randrange(n)] for _ in range(n)]
        means.append(sum(sample) / n)

    means.sort()
    alpha = (1.0 - confidence) / 2.0
    lo_idx = max(0, int(math.floor(alpha * (len(means) - 1))))
    hi_idx = min(len(means) - 1, int(math.ceil((1.0 - alpha) * (len(means) - 1))))

    return {
        "metric": "mean",
        "point_estimate": sum(clean) / n,
        "confidence": confidence,
        "ci_low": means[lo_idx],
        "ci_high": means[hi_idx],
        "n": float(n),
    }


def cliffs_delta(a: list[float], b: list[float]) -> dict[str, float | str]:
    """Cliff's delta effect size."""
    aa = _clean(a)
    bb = _clean(b)
    if not aa or not bb:
        raise ValueError("cliffs_delta requires both groups to be non-empty")

    gt = 0
    lt = 0
    for av in aa:
        for bv in bb:
            if av > bv:
                gt += 1
            elif av < bv:
                lt += 1

    delta = (gt - lt) / (len(aa) * len(bb))
    abs_delta = abs(delta)
    if abs_delta < 0.147:
        magnitude = "negligible"
    elif abs_delta < 0.33:
        magnitude = "small"
    elif abs_delta < 0.474:
        magnitude = "medium"
    else:
        magnitude = "large"

    return {
        "delta": delta,
        "abs_delta": abs_delta,
        "magnitude": magnitude,
        "n_a": float(len(aa)),
        "n_b": float(len(bb)),
    }


def coefficient_of_variation(values: list[float]) -> float | None:
    clean = _clean(values)
    if len(clean) < 2:
        return None
    mean = sum(clean) / len(clean)
    if mean == 0:
        return None
    variance = sum((x - mean) ** 2 for x in clean) / (len(clean) - 1)
    std = math.sqrt(variance)
    return std / mean


def success_rate(values: list[float], threshold: float) -> float:
    clean = _clean(values)
    if not clean:
        return 0.0
    return sum(1 for v in clean if v <= threshold) / len(clean)


def _rankdata(values: list[float]) -> list[float]:
    indexed = sorted(enumerate(values), key=lambda p: p[1])
    ranks = [0.0] * len(values)
    i = 0
    while i < len(indexed):
        j = i
        while j + 1 < len(indexed) and indexed[j + 1][1] == indexed[i][1]:
            j += 1
        rank = (i + j + 2) / 2.0
        for k in range(i, j + 1):
            ranks[indexed[k][0]] = rank
        i = j + 1
    return ranks


def _mannwhitney_u(a: list[float], b: list[float]) -> tuple[float, float]:
    x = _clean(a)
    y = _clean(b)
    if not x or not y:
        raise ValueError("Mann-Whitney requires two non-empty groups")

    n1 = len(x)
    n2 = len(y)
    merged = x + y
    ranks = _rankdata(merged)
    r1 = sum(ranks[:n1])

    u1 = r1 - (n1 * (n1 + 1)) / 2.0
    mu = (n1 * n2) / 2.0
    sigma = math.sqrt((n1 * n2 * (n1 + n2 + 1)) / 12.0)
    if sigma == 0:
        return u1, 1.0

    z = (u1 - mu) / sigma
    p_two_sided = 2.0 * (1.0 - NormalDist().cdf(abs(z)))
    return u1, max(min(p_two_sided, 1.0), 0.0)


def _holm_adjust(pairs: list[tuple[str, float]]) -> dict[str, float]:
    ordered = sorted(pairs, key=lambda p: p[1])
    m = len(ordered)
    adjusted: dict[str, float] = {}

    running_max = 0.0
    for idx, (name, pval) in enumerate(ordered):
        adj = min(1.0, (m - idx) * pval)
        running_max = max(running_max, adj)
        adjusted[name] = running_max
    return adjusted


def pairwise_mannwhitney(groups: dict[str, list[float]], correction: str = "holm") -> list[dict[str, float | str]]:
    labels = sorted(groups.keys())
    raw_results: list[dict[str, float | str]] = []
    p_index: list[tuple[str, float]] = []

    for i in range(len(labels)):
        for j in range(i + 1, len(labels)):
            a_label = labels[i]
            b_label = labels[j]
            key = f"{a_label}__vs__{b_label}"
            u, p = _mannwhitney_u(groups[a_label], groups[b_label])
            raw_results.append(
                {
                    "comparison": key,
                    "group_a": a_label,
                    "group_b": b_label,
                    "u_stat": u,
                    "p_value": p,
                }
            )
            p_index.append((key, p))

    adjusted_map: dict[str, float] = {}
    if correction == "holm":
        adjusted_map = _holm_adjust(p_index)
    else:
        adjusted_map = {key: pval for key, pval in p_index}

    for row in raw_results:
        row["p_value_adj"] = adjusted_map[str(row["comparison"])]

    return raw_results
