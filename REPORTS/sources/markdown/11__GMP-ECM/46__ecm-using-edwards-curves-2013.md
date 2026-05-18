---
title: "ECM using Edwards curves"
title_en: "ECM using Edwards curves"
source_type: "article"
authors: ["Bernstein D. J.", "Birkner P.", "Lange T.", "Peters C."]
year: "2013"
source_link: "https://doi.org/10.1090/S0025-5718-2012-02654-X"
doi: "10.1090/S0025-5718-2012-02654-X"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "ecm-using-edwards-curves-2013.md"
---

# Content source: ECM using Edwards curves

## Source type
Peer-reviewed journal article (Mathematics of Computation, Vol. 82, No. 282, pp. 1139–1179, April 2013). American Mathematical Society.

## Authors affiliation
- Bernstein — Department of Mathematics, University of Illinois at Chicago (and Technische Universiteit Eindhoven).
- Birkner — Technische Universiteit Eindhoven.
- Lange — Department of Mathematics and Computer Science, Technische Universiteit Eindhoven.
- Peters — Department of Mathematics, Technical University of Denmark.

## Objective
Present EECM‑MPFQ, a new implementation of the Elliptic Curve Method (ECM) using Edwards curves (and twisted Edwards curves) with extended coordinates, batch prime processing, signed‑sliding‑window addition‑subtraction chains, and curves with small parameters and large torsion (Z/12Z, Z/2Z×Z/8Z). Compare performance with GMP‑ECM in terms of modular multiplications, CPU cycles, and success probability.

## Core content summary

### 1. Edwards and twisted Edwards curves (Section 2)

**Twisted Edwards curve** (a,d distinct nonzero in field k, char≠2):
\[
a x^2 + y^2 = 1 + d x^2 y^2
\]

- **Edwards curve**: a = 1.
- **Neutral element**: (0,1); negative of (x,y) is (−x,y).
- **Addition law** (strongly unified):
  \[
  (x_1,y_1)+(x_2,y_2) = \left(\frac{x_1 y_2 + y_1 x_2}{1 + d x_1 x_2 y_1 y_2},\; \frac{y_1 y_2 - a x_1 x_2}{1 - d x_1 x_2 y_1 y_2}\right)
  \]

**Coordinate systems**:
- **Projective** (X:Y:Z): addition 10M+1S, doubling 3M+4S.
- **Inverted** (X:Y:Z with (x,y)=(Z/X,Z/Y)): addition 9M+1S, doubling 3M+4S+1D.
- **Extended** (X:Y:Z:T with T=XY/Z): addition 9M (for a=1), doubling 3M+4S.
- **Completed** ((X:Z),(Y:T)): intermediate representation.

**EECM‑MPFQ uses**:
- Extended Edwards coordinates for additions (9M).
- Projective coordinates for accumulator (doubling 3M+4S).
- Mixed coordinates: double in projective, add using precomputed points in extended.

### 2. Stage 1 improvements (Section 4)

**Montgomery coordinates (GMP‑ECM)**: differential addition chains, ≈9 multiplications per bit of s.

**EECM‑MPFQ improvements**:
- **Edwards curves** with extended coordinates → fewer multiplications.
- **Batch primes**: compute entire s = lcm(1,…,B₁) once, then single scalar multiplication [s]P.
- **Signed‑sliding‑window addition‑subtraction chains** (Cm(s) from [15]): average additions per bit → 0 as chain length grows.
- **Result**: Stage 1 cost (multiplications per bit of s):

| B₁ | bits of s | #DBL | #ADD | #M | #S | M/bit |
|----|-----------|------|------|----|----|-------|
| 64 | 67 | 66 | 32 | 683 | 533 | 8.84 |
| 512 | 176 | 175 | 109 | 1753 | 1867 | 8.42 |
| 16384 | 466 | 465 | 372 | 4677 | 5966 | 7.91 |
| 1048576 | 1527 | 1526 | 1323 | 15263 | 22407 | 7.61 |

**Comparison with GMP‑ECM** (240‑bit n, B₁=1024, 1000 curves):
- EECM‑MPFQ: 2.8 million cycles/curve (MPFQ arithmetic).
- GMP‑ECM: 3.8 million cycles/curve (GMP arithmetic).

For B₁=65536:
- EECM‑MPFQ: 162 million cycles (735618 M).
- GMP‑ECM: 243 million cycles (842998 M).

### 3. Stage 2 improvements (Section 5)

**Standard baby‑step‑giant‑step** with parameter d₁.
- Baby steps: [j s]P, giant steps: [i d₁ s]P.
- Prime ℓ = i d₁ ± j divides (i d₁)ᵉ ± jᵉ when using Dickson polynomials Dₑ.

**EECM‑MPFQ features**:
- Use only ϕ(d₁)/2 values of j with gcd(j,d₁)=1 (vs d₁/6 in GMP‑ECM).
- Batch inversions: compute all desired y‑coordinates at once, cost 1I + (4(#i+#j)−3)M.
- **Bos‑Coster multi‑scalar multiplication** for computing multiples [n₁ s]P, [n₂ s]P, …
- **Fast polynomial arithmetic** (product tree, scaled remainder tree) for large parameters.

**Performance** (240‑bit n, B₁=1024, d₁=630, #i=#j=72, e=1):
- EECM‑MPFQ: 4.7 million cycles/curve.
- GMP‑ECM (B₂=41526): 10.8 million cycles/curve.

### 4. Curves with large torsion (Section 6)

**Mazur's theorem**: possible Q‑torsion groups of elliptic curves.
Edwards curves have a point (1,0) of order 4 → torsion is one of:
Z/4Z, Z/8Z, Z/12Z, Z/2Z×Z/4Z, Z/2Z×Z/8Z.

**Z/12Z family** (Theorem 6.2–6.4):
- Parameter u ∈ Q\{0,±1}.
- Point of order 3: (x₃,y₃) = ((u²−1)/(u²+1), −(u−1)²/(u²+1)).
- Curve parameter d = (u²+1)³(u²−4u+1) / ((u−1)⁶(u+1)²).

**Z/2Z×Z/8Z family** (Theorem 6.6–6.9):
- Parameter u ∈ Q\{0,−1,−2}.
- Point of order 8: (x₈,x₈) with x₈ = (u²+2u+2)/(u²−2).
- d = (2x₈²−1)/x₈⁴ (must be a square; automatically satisfied).

**Impossibility results** (Theorems 6.11–6.14):
- No twisted Edwards curve with torsion Z/2Z×Z/6Z or Z/10Z over Q.
- For a = −1, no torsion Z/12Z or Z/2Z×Z/8Z.

### 5. Curves with small parameters (Section 8)

**Goal**: find Edwards curves with:
- Torsion Z/12Z or Z/2Z×Z/8Z,
- Small curve parameters d,
- Small‑height non‑torsion point (X₁:Y₁:Z₁).

**Method**: parameter search via weighted‑homogeneous Diophantine equations.

**Results**:
- **Z/12Z**: 78 distinct j‑invariants found. Example: d = −11·13³/5², base point (5/23, −1/7).
- **Z/2Z×Z/8Z**: 25 distinct j‑invariants found. Example: d = 161²/17⁴, base point (17/19, 17/33).

Complete lists at http://eecm.cr.yp.to/goodcurves.html.

### 6. Effectiveness measurements (Sections 9–10)

**For 20‑bit primes** (38635 primes):
| Torsion | Primes found (B₁=256) | Fraction |
|---------|----------------------|----------|
| Z/12Z | 12467 | 32.27% |
| Z/2Z×Z/8Z | 12686 | 32.84% |
| Z/2Z×Z/4Z | 10616 | 27.49% |
| Z/4Z | 9056 | 23.47% |

**For 30‑bit primes** (sample of 65536 primes, B₁=1024):
| Torsion | Fraction found |
|---------|----------------|
| Z/12Z | 12.16% |
| Z/2Z×Z/8Z | 11.98% |
| Z/2Z×Z/4Z | 9.85% |
| Z/4Z | 9.01% |
| GMP‑ECM (Suyama) | 11.68% |
| Pollard p−1 | 6.35% |

**Key observation**: Larger torsion improves success probability by a factor ~1.3–1.4.

### 7. Optimal parameter tables (Section 10)

Table 10.1 reports optimal (B₁, d₁, e) for finding b‑bit primes, with cost in modular multiplications per prime found.  
Example: for 30‑bit primes, optimal choice gives ~2351 M per prime found.

## Key tables

**Table 4.1**: Stage 1 costs for various B₁.

**Table 5.1**: Stage 2 Bos‑Coster chain costs for various (d₁, e).

**Table 10.1**: Optimal parameters for b = 15…50 bits (multiplications per prime found).

## Limitations (explicit from source)

- EECM‑MPFQ's fast polynomial arithmetic for stage 2 (NTL) is not fully integrated with MPFQ; moving data between libraries is costly.
- For very large B₂, GMP‑ECM's FFT‑based polynomial arithmetic is faster; EECM‑MPFQ lags.
- The small‑parameter curves were found by exhaustive search (≈1 week on multiple computers); not a closed‑form infinite family (unlike Atkin‑Morain or Montgomery constructions).
- Effectiveness measurements are for primes only; composite factors may behave differently.
- The paper does not provide a full complexity analysis; it is empirical.

## References (selected)
- Lenstra (1987) — ECM original paper
- Montgomery (1987) — Speeding ECM, Montgomery curves
- Brent (1986) — ECM improvements
- Silverman & Wagstaff (1993) — Practical ECM analysis
- Bernstein & Lange (2007) — Edwards curves, addition formulas
- Hisil et al. (2008) — Twisted Edwards curves revisited, extended coordinates
- Atkin & Morain (1993) — Finding suitable curves for ECM
- Suyama (1985) — Suyama curves
- Zimmermann & Dodson (2006) — 20 years of ECM, GMP‑ECM
