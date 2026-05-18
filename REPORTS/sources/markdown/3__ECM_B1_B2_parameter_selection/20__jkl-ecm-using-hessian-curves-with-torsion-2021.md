---
title: "JKL-ECM: an implementation of ECM using Hessian curves"
title_en: "JKL-ECM: an implementation of ECM using Hessian curves"
source_type: "article"
authors: ["Heer H.", "McGuire G.", "Robinson O."]
year: "2021"
source_link: "https://doi.org/10.1112/S1461157016000231"
doi: "10.1112/S1461157016000231"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "jkl-ecm-using-hessian-curves-with-torsion-2021.md"
---

# Content source: JKL-ECM: an implementation of ECM using Hessian curves

## Source type
Journal article (LMS Journal of Computation and Mathematics, 2021? Actually published 2016? The arXiv version is 2016, but the paper says "Published online by Cambridge University Press" — likely 2016–2021).

## Authors and affiliations
- Henriette Heer (Technical University of Kaiserslautern)
- Gary McGuire, Oisin Robinson (University College Dublin)

## Objective
Implement ECM using twisted Hessian curves from families discovered by Jeon, Kim and Lee (JKL, 2011) that have large torsion subgroups (ℤ/6ℤ⊕ℤ/6ℤ or ℤ/4ℤ⊕ℤ/8ℤ) over a quartic number field. Exploit torsion injection (guaranteeing small factors in group order) and "small parameter" speedup to compete with GMP-ECM and EECM-MPFQ. Generate thousands of curves with small parameters and base points.

## Key contribution

**Problem**: ECM over ℚ can only guarantee small torsion subgroups (max ℤ/12ℤ, ℤ/2ℤ⊕ℤ/8ℤ, etc.). Over quartic number fields, larger torsion (ℤ/6ℤ⊕ℤ/6ℤ) is possible via JKL families. When the quadratic irrationalities defining the field exist in 𝔽_p (i.e., the prime factor splits), the full torsion subgroup injects into E(𝔽_p), giving guaranteed small factors in the group order (36 divides #E(𝔽_p) in the ℤ/6ℤ⊕ℤ/6ℤ case).

**Solution**: Generate JKL curves with torsion ℤ/6ℤ⊕ℤ/6ℤ via rational parameter t. Convert to twisted Hessian form (aX³ + Y³ + Z³ = dXYZ). Find points of infinite order with small height. Use these curves in ECM with stage 2 FFT continuation (Montgomery 1992).

## JKL families (Section 2.3)

### Family 1: ℤ/6ℤ⊕ℤ/6ℤ (Theorem 2.1)

Given t ∈ ℚ \ {0, 1, -1/2}, define:
\[
\mu = \frac{2t^3 + 1}{3t^2}
\]
Elliptic curve in Weierstrass form:
\[
E_\mu: y^2 = x^3 - 27\mu(\mu^3 + 8)x + 54(\mu^6 - 20\mu^3 - 8)
\]
Over K = ℚ(√-3, √(8t³+1)), torsion ≅ ℤ/6ℤ⊕ℤ/6ℤ.

**Conversion to twisted Hessian**:
Hessian: X³ + Y³ + Z³ = 3μ XYZ.
Twisted Hessian: aX³ + Y³ + Z³ = dXYZ, where d/a = 3μ (a,d coprime integers).

**Affine point conversion**: Given affine point (u,v) on E_μ, compute affine (x,y) on twisted Hessian via formulas (Section 2.3.1).

### Family 2: ℤ/4ℤ⊕ℤ/8ℤ (Theorem 2.2)

Given t ∈ ℚ \ {0, ±1}, define ν = (t⁴ - 6t² + 1) / (4(t²+1)²).
Elliptic curve: y² + xy - (ν² - 1/16)y = x³ - (ν² - 1/16)x².
Over K = ℚ(√-1, √(t⁴ - 6t² + 1)), torsion ≅ ℤ/4ℤ⊕ℤ/8ℤ.
Over ℚ, torsion ≅ ℤ/2ℤ⊕ℤ/8ℤ (Theorem 4.2) with a point of order 4 → convertible to twisted Edwards form (Section 3).

**Bernstein et al.'s 25 high-performance ℤ/2ℤ⊕ℤ/8ℤ curves are all recovered** from this family, plus hundreds more.

## Torsion analysis (Section 4)

### ℤ/4ℤ⊕ℤ/8ℤ family over ℚ (Theorem 4.2)
- E_ν(ℚ)_tors = ℤ/2ℤ⊕ℤ/8ℤ.
- Proof via 4th division polynomial (Lemma 4.1) yields 4 points of order 4 with rational coordinates.
- One point of order 8 exists (explicit formula given), no point of order 16 (Mazur).

### ℤ/6ℤ⊕ℤ/6ℤ family over ℚ (Theorem 4.6)
- E_μ(ℚ)_tors = ℤ/6ℤ.
- Exactly one point of order 2 (Lemma 4.3), two points of order 3 (Lemma 4.4), two points of order 6 (Lemma 4.5).
- Not isomorphic to Edwards curve over ℚ (since no point of order 4).

### Hessian curve torsion classification (Corollary 4.12)
For Hessian curve H: x³ + y³ + z³ = d x y z:

| Condition | Torsion over ℚ |
|-----------|----------------|
| H is a JKL curve (d = (2t³+1)/3t²) | ℤ/6ℤ |
| Not JKL, but has point of order 2 (d of form?) — not in JKL? | ? Actually Corollary 4.12: If not JKL, then ℤ/3ℤ. |
| Generic | ℤ/3ℤ |

## Small parameter generation (Section 3, Table 1)

| Implementation | #Curves | Type | Torsion | Time | Resources |
|----------------|---------|------|---------|------|------------|
| EECM-MPFQ | 25 | Edwards | ℤ/2ℤ⊕ℤ/8ℤ | 1 week | Several computers |
| EECM-MPFQ | 78 | Edwards | ℤ/12ℤ | 1 week | Several computers |
| This work | 700 | Edwards | ℤ/4ℤ⊕ℤ/8ℤ | 2 weeks | One desktop |
| This work | 4,840 | Hessian | ℤ/6ℤ⊕ℤ/6ℤ | 2 weeks | One desktop |

**Observation**: JKL families generate thousands of curves with small parameters and base points in a short time (2 weeks on one desktop), compared to EECM-MPFQ's exhaustive search (1 week on multiple computers, only 78+25 curves).

## Curve arithmetic speedup (Section 3.1)

### Twisted Hessian addition (projective coordinates, fixed point P₁ with small coordinates)

Given (X₁:Y₁:Z₁) fixed (small), (X₂:Y₂:Z₂) variable:
```
A = X₁·Z₂,    B = Z₁·Z₂,    C = Y₁·X₂,
D = Y₁·Y₂,    E = Z₁·Y₂,    F = a·X₁·X₂,
X₃ = A·B - C·D,
Y₃ = D·E - F·A,
Z₃ = F·C - B·E.
```
Since X₁, Y₁, Z₁, a are small, multiplications by them cost O(n) instead of O(n²). Effective cost per addition: **6 multiplications O(n²) + 6 multiplications O(n)**.

### Twisted Hessian doubling (projective):
\[
2P = (y(z³ - x³) : x(y³ - z³) : z(x³ - y³))
\]
Cost: 7M + 1S + 1d (multiply by curve constant) + additions.

### Comparison with twisted Edwards (EECM-MPFQ)

| Operation | Twisted Edwards (Hisil) | Twisted Hessian (this work) |
|-----------|------------------------|-----------------------------|
| Doubling | 3M + 4S + 1a | 7M + 1S + 1d |
| Addition | 9M + 1a + 1d | 12M + 1a + 3add (general) → 6M + 6m + 1a + 3add (fixed point) |
| Double-and-add | (3M+4S+1a) + (9M+1a+1d) | (7M+1S+1d) + (6M+6m+1a) |

Note: "m" denotes multiplication by small constant (≈ cost of O(n) bit operations). For large n (e.g., 200+ digits), the O(n) operations are negligible compared to O(n²) multiplications. Thus effective cost is similar.

## Stage 2 implementation (Section 5.1)

- **FFT continuation** (Montgomery 1992): uses baby-step giant-step + polynomial multiplication via FFT.
- GMP automatically uses FFT multiplication for large integers (threshold calibrated), so no custom FFT implementation needed.
- Memory requirement: O(B₂ log B₂) for product trees.
- A technicality: For twisted Hessian curves in stage 2, use rational map ψ(X:Y:Z) = X²/(YZ) to get Edwards-like x-coordinate for comparisons.

## Torsion injection for ECM (Section 5.2)

For ℤ/6ℤ⊕ℤ/6ℤ family: over K = ℚ(√-3, √(8t³+1)).
- If both √-3 and √(8t³+1) exist in 𝔽_p (i.e., p splits completely in K), then torsion subgroup injects → 36 | #E(𝔽_p).
- If only √-3 exists, then torsion ≅ ℤ/3ℤ⊕ℤ/6ℤ → 18 | #E(𝔽_p).
- We can force √-3 to exist by choosing to factor numbers of the form N = x² + 3y² (since then √-3 ≡ x/y mod p).

For ℤ/4ℤ⊕ℤ/8ℤ family: similar with √-1.

## Largest factor found (Section 5.3)

- **57-digit prime factor** of a 248-digit number:
```
675047857067159607640250455245491501526526277140638512677
```
- Curve: twisted Hessian with d = 26511, a = 231136413353.
- Group order factorization: 2·3²·58211·73757·824039·13582747·17027609·74341063·99190781·6215336273.
- Stage 1 bound: 110,000,000.
- Effective stage 2 bound: ~1.15×10¹².
- Curves tried: only 1,152 (vs 17,899 recommended for 55-digit factors in standard ECM).

Several other 56-digit and 50+ digit factors found.

## Performance comparison (Tables A.1–A.3, Section 5.4)

Timings on Fionn cluster for B₁ = 1e6, 3e6, 11e6, 43e6, 110e6, and digits 50, 100, 150, 200, 250, 300, 350, 400.

**Example: B₁ = 11e6, 200-digit number**

| Implementation | Time (ms) |
|----------------|-----------|
| JKL-ECM (twisted Edwards) | 22,800 |
| JKL-ECM (twisted Hessian) | 22,190 |
| GMP-ECM 6.4.4 | 13,848 |

**Observation**: GMP-ECM is still faster (assembly optimized). JKL-ECM written in C++ using GMP mpz_t functions (no assembly). Significant potential for optimization (SSE/AVX, etc.).

## Effectiveness (success probability, Section 5.5, Figures A.1–A.2)

For 30-bit primes ≡ 1 mod 3:
- JKL curve (ℤ/6ℤ⊕ℤ/6ℤ) with (d,a)=(123,125) has significantly higher success probability than GMP-ECM Suyama curve (σ=4007218240) for B₁ up to ~16,000.
- Example at B₁=5,000: JKL success ~8%, GMP-ECM ~5%.

For 40-bit primes (Figure A.2): similar advantage.

## Strengths

1. **Large torsion injection** (36 divides group order) gives higher probability of smoothness.
2. **Thousands of curves** with small parameters generated quickly from rational parameter t.
3. **Recovers Bernstein et al.'s 25 high-performance curves** automatically from JKL ℤ/4ℤ⊕ℤ/8ℤ family.
4. **Twisted Hessian arithmetic** with fixed-point optimization yields competitive performance.
5. **Stage 2 FFT continuation** implemented using GMP's FFT multiplication.
6. **Open source** (presumably).

## Limitations (explicit)

1. **No assembly optimization** — performance lags behind GMP-ECM (up to 2× slower for some parameters).
2. **Torsion injection requires special input numbers** (e.g., N = x² + 3y²) to force √-3 to exist in 𝔽_p.
3. **Limited to families with torsion over quartic fields** — not all primes split completely.
4. **Stage 2 FFT continuation memory** grows as O(B₂ log B₂) — limits B₂ in practice.
5. **Only 4,840 ℤ/6ℤ⊕ℤ/6ℤ curves** — many more exist but not generated.
6. **Not as widely tested** as GMP-ECM (fewer users, less battle-hardened).

## Relation to other work

- Builds on Jeon, Kim & Lee (Math. Comp. 2011) — families of curves with prescribed torsion.
- EECM-MPFQ (Bernstein et al. 2013) — twisted Edwards curves for ECM; JKL-ECM recovers their curves.
- Twisted Hessian curves: Bernstein et al. (2015) — EFD database.
- Stage 2 FFT continuation: Montgomery (1992 PhD thesis), implemented in GMP-ECM.
- Torsion injection for ECM: Brier & Clavier (ANTS 2010) — similar idea for Cunningham numbers.
- GMP-ECM (Zimmermann et al.) — baseline.
