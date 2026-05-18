---
title: "A Practical Analysis of the Elliptic Curve Factoring Algorithm"
title_en: "A Practical Analysis of the Elliptic Curve Factoring Algorithm"
source_type: "article"
authors: ["Silverman R. D.", "Wagstaff Jr. S. S."]
year: "1993"
source_link: "https://doi.org/10.1090/S0025-5718-1993-1122078-7"
doi: "10.1090/S0025-5718-1993-1122078-7"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "ecm-optimal-parameters-and-qs-comparison-1993.md"
---

# Content source: A Practical Analysis of the Elliptic Curve Factoring Algorithm

## Source type
Peer-reviewed journal article (Mathematics of Computation).

## Authors affiliation
- R. D. Silverman — The MITRE Corporation, Bedford, Massachusetts.
- S. S. Wagstaff Jr. — Purdue University, West Lafayette, Indiana.

## Objective
Provide practical guidance for parameter selection in the Elliptic Curve Method (ECM) of integer factorization, analyze its runtime as a function of factor size, and determine optimal switching strategy between ECM and the Quadratic Sieve (MPQS).

## Core methodology
- Theoretical basis: Dickman's function ρ(α) for largest prime factor distribution, and μ(α,β) for second largest factor distribution.
- Probability of ECM success: P(B₁,B₂) ≃ μ(α,β) where α = log p / log B₁, β = log B₂ / log B₁.
- Numerical integration of ρ(α) and μ(α,β) using Simpson's method.
- Bayesian re-estimation of unknown factor size after failed ECM trials.
- Comparative analysis of ECM vs MPQS using expected time minimization.

## Key results

### Optimal parameter selection (K = 100, step2/step1 speed ratio)

| Digits (p) | Optimal B₁ | Optimal B₂ | B₂/B₁ | Avg curves L | Cost per curve T (arb. units) |
|------------|------------|------------|-------|--------------|-------------------------------|
| 5 | 16 | 800 | 50.0 | 2.19 | 5 |
| 10 | 519 | 19407 | 37.4 | 14.1 | 488 |
| 15 | 3350 | 151000 | 45.1 | 376 | 5210 |
| 20 | 11000 | 440000 | 40.0 | 3.93e+4 | 1.39e+6 |
| 25 | 33000 | 1.33e+6 | 40.3 | 7.64e+5 | 3.51e+7 |
| 30 | 91000 | 4.05e+6 | 44.5 | 2.05e+7 | 9.55e+8 |
| 35 | 333000 | 1.61e+7 | 48.4 | 4.19e+8 | 1.61e+10 |
| 40 | 1.15e+6 | 5.65e+7 | 49.1 | 7.91e+9 | 2.24e+11 |

### Practical heuristics derived
- **B₂ ≈ 0.4·K·B₁** is a good general rule (response surface flat near optimum).
- **g = 1** (probability of success 1 - 1/e ≈ 0.632) is optimal for ECM-only usage.
- Incremental cost ratio for adding one digit to factor size ~ O(p^{1/5}) for 5–40 digit range.
- After ECM failure, the expected factor size increases by ~0.8–1.2 digits.

### Comparison with Quadratic Sieve (MPQS)
For a 100-digit N (after trial division to log²N), recommended ECM time fraction before switching to MPQS:

| log₁₀ N | ECM time fraction |
|---------|-------------------|
| 40 | 0.72 |
| 50 | 0.43 |
| 60 | 0.16 |
| 70 | 0.058 |
| 80 | 0.0080 |
| 90 | 0.0029 |
| 100 | 0.0016 |

### Actual runtime data (Montgomery's ECM on SUN-3/60, step1)

| B₁ | 50-digit N (sec) | 100-digit N (sec) | 200-digit N (sec) |
|----|------------------|-------------------|-------------------|
| 100 | 3 | 11 | 44 |
| 1000 | 12 | 46 | 184 |
| 10000 | 81 | 323 | 1293 |
| 100000 | 439 | 1754 | 7027 |
| 500000 | 1835 | 7338 | 29353 |

## Limitations (explicit from source)
- Asymptotic estimates rely on unproven extension of the Canfield–Erdős–Pomerance theorem.
- Tables assume elliptic curve coefficients chosen to make group order divisible by 12 (loses ~1 digit otherwise).
- Analysis of complete factorization (vs finding one factor) is "extremely difficult" — not performed.
- The o(1) terms in asymptotic formulas for B(p) and K(p) are not known analytically; only empirically estimated for 5–40 digit range.
- Step 2 speed ratio K varies by implementation and hardware (K=100 assumed, Montgomery's gave K≈170).

## Practical conclusions
1. For ECM only: use B₂ ≈ 0.4·K·B₁, and set expected curves L = 1/P(B₁,B₂) to achieve 63% success probability.
2. For hybrid ECM+MPQS strategy: run ECM for time = g·F(p)·M(N) where g is determined by (7.4), then switch to MPQS.
3. After each ECM failure, re-estimate expected factor size using Bayesian update (Table 7) and increase parameters accordingly.
4. For very small factors (<15 digits) consider P–1 algorithm instead of ECM.