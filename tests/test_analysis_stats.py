from ecm_optimizer.analysis.stats import (
    bootstrap_ci,
    cliffs_delta,
    coefficient_of_variation,
    pairwise_mannwhitney,
    success_rate,
)


def test_bootstrap_ci_contains_point_estimate() -> None:
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    ci = bootstrap_ci(values, confidence=0.95, n_resamples=1000, seed=7)
    assert ci["ci_low"] <= ci["point_estimate"] <= ci["ci_high"]


def test_cliffs_delta_sign_and_magnitude() -> None:
    result = cliffs_delta([1, 2, 3], [10, 11, 12])
    assert result["delta"] < 0
    assert result["magnitude"] in {"small", "medium", "large", "negligible"}


def test_coefficient_of_variation() -> None:
    cv = coefficient_of_variation([10, 12, 14, 16])
    assert cv is not None
    assert cv > 0


def test_success_rate() -> None:
    rate = success_rate([0.5, 0.7, 0.8, 0.3], threshold=0.7)
    assert rate == 0.75


def test_pairwise_mannwhitney_holm() -> None:
    groups = {
        "a": [1.0, 1.2, 1.3, 1.1],
        "b": [2.0, 2.1, 1.9, 2.2],
        "c": [1.4, 1.5, 1.6, 1.4],
    }
    rows = pairwise_mannwhitney(groups, correction="holm")
    assert len(rows) == 3
    assert all("p_value_adj" in row for row in rows)
