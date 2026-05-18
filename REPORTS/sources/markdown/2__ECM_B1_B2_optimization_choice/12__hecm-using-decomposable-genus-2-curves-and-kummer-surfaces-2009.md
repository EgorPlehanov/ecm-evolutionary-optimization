---
title: "HECM: Hyperelliptic Curve Method using decomposable genus 2 curves and Kummer surfaces"
title_en: "HECM: Hyperelliptic Curve Method using decomposable genus 2 curves and Kummer surfaces"
source_type: "article"
authors: ["Cosset R."]
year: "2009"
source_link: "https://arxiv.org/abs/0905.2325"
doi: "none"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "hecm-using-decomposable-genus-2-curves-and-kummer-surfaces-2009.md"
---

# Content source: HECM: Hyperelliptic Curve Method using decomposable genus 2 curves and Kummer surfaces

## Source type
Journal article (preprint). 2000 Mathematics Subject Classification: 11Y05, 11Y16, 11Y40.

## Author
Romain Cosset (contact information not provided in file)

## Objective
Implement the Hyperelliptic Curve Method (HECM) for integer factorization using decomposable genus 2 curves whose Jacobians are isogenous to the product of two elliptic curves, combined with Kummer surface arithmetic. Achieve performance comparable to or better than ECM for large numbers, effectively running two ECM trials in parallel.

## Core idea: Why hyperelliptic curves could be faster?

**Problem**: Jacobian of genus 2 curve over 𝔽_p has size ≈ p², much larger than elliptic curve group (≈ p). Larger group → lower probability of smoothness → more curves needed.

**Solution**: Use **decomposable** (also called (2,2)-decomposable) genus 2 curves whose Jacobian is isogenous to the product of two elliptic curves E₁ × E₂. One HECM run = two simultaneous ECM runs on two independent elliptic curves.

**Result**: Probability of success comparable to two ECM trials, but arithmetic overhead can be shared.

## Kummer surface arithmetic (Gaudry 2007)

The Kummer surface κ_(α:β:γ:δ) is obtained by identifying opposite points on the Jacobian: Jac(C)/{±1}. It is a quartic surface in ℙ³ with equation (2):

\[
4E'^2 \alpha \beta \gamma \delta XYZT = \big((X^2+Y^2+Z^2+T^2) - F(XT+YZ) - G(XZ+YT) - H(XY+ZT)\big)^2
\]

where E',F,G,H are constants derived from the theta constants (α,β,γ,δ).

**Advantage**: Arithmetic on the Kummer surface uses only X:Y:Z:T coordinates (no y-coordinate). Two operations:

1. **Doubling** (Algorithm 1): [2]P — 8 squarings + 8 multiplications by constants (8S+8d).
2. **Pseudo-addition** (Algorithm 2): Given P, Q, and R = P−Q, compute P+Q — cost: 14M+4S+4d (if divisions replaced by multiplications) or 4I+4M+4S+4d (if inversions used).

**Scalar multiplication** (Algorithm 3): Binary method with P−Q always equal to initial point. Cost per bit: 12M+4S+16d. With optimizations (two coordinates equal/opposite): 12M+10S+? — ~5% faster.

### Parameter α=δ (special choice from parametrization)
When α=δ, two coordinates of (1/α:1/β:1/γ:1/δ) become equal, saving 2 multiplications per bit.

## Parametrization of decomposable curves (Section 2)

### Rosenhain form for genus 2 curve
\[
\mathcal{C}: \chi y^2 = x(x-1)(x-\lambda)(x-\mu)(x-\nu), \quad \chi \neq 0
\]

### Condition for (2,2)-decomposability with rational underlying elliptic curves and rational Kummer surface (Lemma 2.1)

\[
\lambda = \mu \frac{1-\nu}{1-\mu}, \quad \mu(\mu-\nu) = \square, \quad \lambda\mu\nu = \square
\]
where □ denotes a rational square.

### Parametric family (Theorem 2.3)

Set:
\[
\mu = 1 - \frac{\nu(1-\nu)}{s^2}, \quad \nu = \frac{s^2 - u^2}{1-u^2}, \quad s,u \in \mathbb{Q}
\]

Then (u,v) lies on the elliptic curve:
\[
1 + \left(-\frac{3}{s^2} + \frac{1}{s^4}\right)u^2 + \frac{u^4}{s^2} = v^2
\]

A non-torsion point is (1, 1−1/s²). To avoid genericity issues (denominators zero), use a multiple, e.g., its double (2, 1+2/s²).

### Restrictions on parameters (Condition 2.4–2.5)

- s ≠ 0, ±1, ±u, ±u²
- u ≠ 0, ±1
- v ≠ 0
- All λ, μ, ν distinct and not in {0,1,∞}

## Theta constants (α:β:γ:δ) from (s,u)

From the construction, α = δ (a key simplification). In projective coordinates, we can scale to α = δ = 1.

Then:
\[
(\frac{1}{\alpha}:\frac{1}{\beta}:\frac{1}{\gamma}:\frac{1}{\delta}) = \left(s^4 v^2 : s^5 v^2 : s (u^2 - s^2)(u^2 - 1) : s^4 v^2\right)
\]

**Observation**: 1/α = 1/δ, so two constants are equal → saves multiplications.

## Small parameters (Section 3.3)

The constants 1/α, 1/β, 1/γ, 1/δ, and the curve parameters A,B,C,D in the Kummer surface equation are rational functions in s,u of small degree.

By fixing s and u as small integers (fitting into a signed long), all constants become small integers modulo n. Then multiplication by these constants is essentially free (cost negligible compared to full-length modular multiplications).

**Number of useful curves** (for 64-bit processor): ~185,399 — sufficient for finding factors >65 digits.

## Performance analysis

### Cost per bit for scalar multiplication

| Operation | ECM (Montgomery, PRAC) | HECM (Kummer, binary) | Two ECM runs |
|-----------|------------------------|----------------------|--------------|
| Multiplications per bit | ≈6M+3S | 12M+4S+16d | 12M+6S |
| With S≈0.8M | ≈8.4M | ≈17.2M (but d cheap) | ≈16.8M |
| With small constants (d negligible) | — | 12M+4S ≈ 15.2M | 16.8M |

**Theoretical advantage**: HECM ~10% faster than two independent ECM runs when constants are small.

### Table 3: Fraction of time spent on operations (GMP-HECM, B₁=10⁷)

| size of n | M | S | d (small const mul) | additions |
|-----------|----|----|---------------------|-----------|
| 10¹⁰⁰ | 0.143 | 0.428 | 0.163 | 0.237 |
| 10²⁵⁰ | 0.216 | 0.597 | 0.081 | 0.109 |
| 10¹⁰⁰⁰ | 0.234 | 0.700 | 0.051 | 0.017 |

**Note**: Squaring takes same time as multiplication (GMP-ECM has assembly for multiplication but not dedicated squaring). For large n, additions become negligible.

### Table 4: Speedup of GMP-HECM vs two runs of GMP-ECM (B₁=10⁷)

| size of n | Ratio (HECM / 2×ECM) |
|-----------|----------------------|
| 10¹⁰⁰ | 1.15 (slower) |
| 10²⁵⁰ | 1.00 (equal) |
| 10⁵⁰⁰ | 0.93 |
| 10¹⁰⁰⁰ | 0.89 |

→ For n ≥ 10²⁵⁰, HECM is faster (up to 11% speedup for very large n).

### Table 2: Optimal B₁ and expected curves (GMP-ECM vs GMP-HECM)

| Factor digits | ECM B₁ | ECM curves | HECM B₁ | HECM B₂ | HECM curves |
|---------------|--------|------------|---------|---------|-------------|
| 20 | 11k | 74 | 14k | 2.1·10⁶ | 75 |
| 25 | 50k | 214 | 60k | 16·10⁶ | 214 |
| 30 | 250k | 430 | 260k | 130·10⁶ | 491 |
| 35 | 1·10⁶ | 904 | 1·10⁶ | 900·10⁶ | 1,116 |
| 40 | 3·10⁶ | 2,350 | 3·10⁶ | 4·10⁹ | 2,871 |
| 45 | 11·10⁶ | 4,480 | 11·10⁶ | 28·10⁹ | 5,425 |
| 50 | 43·10⁶ | 7,553 | 43·10⁶ | 200·10⁹ | 9,003 |
| 55 | 110·10⁶ | 17,769 | 110·10⁶ | 750·10⁹ | 21,183 |
| 60 | 260·10⁶ | 42,017 | 260·10⁶ | 2·10¹² | 49,534 |
| 65 | 850·10⁶ | 69,408 | 850·10⁶ | 14·10¹² | 81,387 |

**Observation**: For factors ≥35 digits, HECM uses the same B₁ as ECM, but the expected number of curves is only slightly higher (about 1.2× at 40 digits).

## Torsion properties (Section 3.2)

The underlying elliptic curves have at least (ℤ/2ℤ)² torsion. Probability of 4-torsion depends on Legendre symbols of (s²−u²), (s²−1), (u²−1) (Table 1).

Experimental: The order of the curves is as likely to be smooth as a random integer about 1/7.75 of its value (compared to 1/23.7 for Suyama curves in ECM). For p≡3 mod 4, average 2-adic valuation ≈3.48 (vs 3.5 expected); for p≡1 mod 4, ≈3.15 (vs 3 expected).

## Implementation and comparison with GMP-ECM

**Stage 1**: Custom implementation on Kummer surface with small parameters (s,u small integers). After computing [k]P on Kummer surface, recover the two underlying elliptic curves and their points.

**Stage 2**: Call GMP-ECM's stage 2 on each underlying elliptic curve (can be done in parallel).

**Speedup observed**: For very large n (≥10²⁵⁰ digits), GMP-HECM is 7–11% faster than two independent runs of GMP-ECM.

**Limitations**:
- Initialization cost higher (morphisms from Kummer surface to elliptic curves require square roots; handled but adds overhead).
- Not competitive for small n (<10²⁵⁰) or small factors (<30 digits).
- Kummer surface arithmetic uses more squarings than multiplications; GMP's lack of optimized squaring hurts HECM more than ECM.
- Only stage 1 is optimized; stage 2 still uses GMP-ECM (not parallelized).

## Relation to other work

- ECM using Montgomery form (Montgomery 1987)
- Kummer surface arithmetic (Gaudry 2007)
- Edwards curves for ECM (Bernstein et al. 2008, "EECM")
- GMP-ECM (Zimmermann & Dodson 2006)
- This work extends ECM to genus 2 decomposable curves with Kummer surfaces, achieving the first practical HECM implementation faster than ECM for large inputs.
