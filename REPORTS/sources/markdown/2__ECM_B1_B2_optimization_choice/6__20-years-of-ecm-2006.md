---
title: "20 years of ECM"
title_en: "20 years of ECM"
source_type: "inria_report"
authors: ["Zimmermann P.", "Dodson B."]
year: "2006"
source_link: "https://inria.hal.science/inria-00070192"
doi: "none"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "20-years-of-ecm-2006.md"
---

# Content source: 20 years of ECM

## Source type
INRIA Research Report (RR-5834). Also presented at ANTS VII (2006).

## Authors and affiliations
- Paul Zimmermann (INRIA Lorraine, project SPACES)
- Bruce Dodson (Lehigh University)

## Objective
Survey the state-of-the-art of the Elliptic Curve Method (ECM) for integer factorization after 20 years (1985–2005), with emphasis on the algorithms implemented in the GMP-ECM software. Present historical development, algorithmic improvements, implementation techniques, and record factors.

## Historical context

ECM was invented by H. W. Lenstra, Jr. in 1985 [13]. Key early contributions:
- **1985–1986**: Brent and Montgomery develop stage 2, Brent-Suyama extension, fast polynomial evaluation ideas (though FFT continuation not yet realized).
- **1987**: Montgomery's unified description of P-1, P+1, ECM; PRAC algorithm for Lucas chains.
- **1988**: Brent finds 21- and 22-digit factors of F₁₁.
- **1992**: Montgomery's PhD thesis introduces FFT continuation.
- **1998**: Conrad Curry finds 53-digit factor of 2⁶⁷⁷−1 with Woltman's prime95.
- **2005**: 66-digit ECM record (Dodson).

**Extrapolation (Figure 1)**:
- Brent's formula: √D = (Y − 1932.3)/9.3 (D = digits, Y = year)
- Projects 100-digit ECM factor around 2025.

## Notation and ECM overview

Let n be the number to factor, p an unknown prime divisor, π a prime.

Stage 1: Compute Q = ∏_{π ≤ B₁} π^{⌊log B₁ / log π⌋} · P₀ on elliptic curve E over ℤ/nℤ.
Stage 2: Search for prime π in [B₁, B₂] such that π·Q = O (mod p).

ECM finds p when the group order #E(𝔽_p) is (B₁,B₂)-smooth (largest prime factor ≤ B₂, second largest ≤ B₁).

**Asymptotic complexity**:
\[
O(L(p)^{\sqrt{2}+o(1)} \cdot M(\log n)), \quad L(p) = e^{\sqrt{\log p \log \log p}}
\]
where M(log n) = multiplication cost modulo n.

## Stage 1 implementation (Section 2)

### Montgomery's PRAC algorithm (1987)
- Lucas chains: addition chain where |i−j| also appears in the chain (required for Montgomery's addition formula).
- PRAC uses heuristics with ratio α ≈ φ = (1+√5)/2 to reduce (d,e) pairs.
- **Optimization**: Try 10 different α values (continued fraction approximations), keep lowest cost.
- Gain vs. φ-only: 3.72% for B₁=10⁶, 3.74% for B₁=10⁸.

### Point arithmetic in projective coordinates (x:z)

**Addition** (requires P−Q):
\[
x_{P+Q} = 4z_{P-Q}(x_P x_Q - z_P z_Q)^2, \quad z_{P+Q} = 4x_{P-Q}(x_P z_Q - z_P x_Q)^2
\]
Cost: 6 multiplications (2 squares).

**Doubling** (with d = (a+2)/4):
\[
x_{2P} = (x_P^2 - z_P^2)^2, \quad z_{2P} = (4x_P z_P)[(x_P - z_P)^2 + d(4x_P z_P)]
\]
Cost: 5 multiplications (2 squares).

### Modular arithmetic optimizations

**Montgomery representation**: Represent a as a′ = β^{ℓ}·a mod n (ℓ words in base β). REDC computes ab·β^{−ℓ} mod n.

**GMP-ECM implementation** (Kevin Ryde trick):
- Store carry words from mpn_addmul_1 in low ℓ words of c (set to zero by REDC).
- Replaces ℓ expensive carry propagations by one mpn_add_n call.

**Special numbers** (β^k ± 1): Use ad-hoc modular reduction via c ≡ c₀ + c₁ (mod n) when n divides β^k−1. Used for Cunningham numbers.

**Subquadratic arithmetic**: Barrett reduction with wrap-around trick for 1.5M(n) cost.

## Stage 2 implementation (Section 3)

### Standard continuation (baby-step giant-step)

Write primes π = i·d + j with:
- S = {i·d : 0 ≤ i·d < B₂} (giant steps)
- T = {j : 0 < j < d, gcd(j,d)=1} (baby steps)

Choose d ≈ √B₂ → O(√B₂) operations.

**Key observation**: jQ and −jQ share same x-coordinate → restrict to j ≤ d/2 (or j ≡ 1 mod 6 if d multiple of 6).

### FFT continuation (Montgomery 1992)

Instead of checking each prime individually, compute:
\[
h = \prod_{\sigma \in S} \prod_{\tau \in T} (x_\sigma - x_\tau) \bmod n
\]
If any gcd(x_σ−x_τ,n) > 1, then gcd(h,n) > 1.

**Two variants**:
1. **POLYGCD**: Compute h = Res(F,G) via polynomial gcd — O(M(d) log d).
2. **POLYEVAL**: h = ±∏_{τ∈T} G(x_τ) via remainder tree — faster constant, but uses O(d log d) memory (vs O(d) for POLYGCD).

**Kronecker–Schönhage trick for polynomial multiplication**:
- Pack polynomials into big integers: P = p(β^ℓ), Q = q(β^ℓ) with β^ℓ > d·n².
- Multiply integers (FFT), then unpack coefficients.
- Advantage: reuses fast integer multiplication, no need for polynomial FFT over ℤ/nℤ.

### Block splitting (k blocks)

Split stage 2 into k blocks: B₂ = k·b₂. Let d ≈ √b₂.
- S₁,…,Sₖ cover multiples of d up to B₂.
- Compute H = G₁·G₂·…·Gₖ mod F.
- Cost: ≈ ((k+1)p + r)/√k · M(d) log d, where p = product tree cost, r = remainder tree cost.
- With r/p ≈ 2 (Bernstein's scaled remainder trees), optimal k = 3, cost ≈ 3.46p M(d) log d (vs 4p for k=1).

### Brent–Suyama extension (1986)

Replace σ,τ by f(σ), f(τ) for polynomial f. If π = σ ± τ, then π divides f(σ) ± f(τ).

**Dickson polynomials** (parameter α = −1):
- D₁(x) = x
- D₂(x) = x² + 2
- D_{e+2}(x) = x·D_{e+1}(x) + D_e(x)
Examples: D₃(x)=x³+3x, D₄(x)=x⁴+4x²+2, D₆(x)=x⁶+6x⁴+9x²+2, D₁₂(x), D₃₀(x).

**Table of differences**: Precompute small multiples and use addition chains; then each new xᵉQ costs e point additions.

### Montgomery's d₁·d₂ improvement

Sieve primes as π = i·d₁ + j·d₂ (instead of i·d + j):
- T = {j·d₂ : 0 ≤ j < d₁, gcd(j,d₁)=1}
- S = {i·d₁ : −d₁·d₂ < i·d₁ ≤ B₂, gcd(i,d₂)=1}
- Condition gcd(i,d₂)=1 reduces |S| by factor 1/d₂.
- Allows enlarging block size b₂ by factor 1/d₂ for free.

## Default parameters in GMP-ECM 6.0.1 (table)

| Digits | B₁        | B₂′            | B₂′/B₁ | k   | d₁      | d₂ | degree | poly   | curves |
|--------|-----------|----------------|--------|-----|---------|----|--------|--------|--------|
| 40     | 3·10⁶     | 4.59·10¹¹      | 153,000| 2   | 150150  | 17 | 14400  | D₆     | 2440   |
| 45     | 11·10⁶    | 3.01·10¹¹      | 27,374 | 2   | 237128  | 11 | 36864  | D₁₂    | 4590   |
| 50     | 43·10⁶    | 1.986·10¹²     | 46,200 | 2   | 210210  | 20 | 199,216| D₁₂    | 7771   |
| 55     | 110·10⁶   | 7.294·10¹¹     | 6,632  | 2   | 1,891,890| 17 | 181,440| D₃₀    | 17,899 |
| 60     | 260·10⁶   | 2.433·10¹²     | 9,358  | 2   | 2,357,357| 19 | 322,560| D₃₀    | 43,670 |
| 65     | 850·10⁶   | 1.571·10¹²     | 1,848  | 2   | 8,978,970| 17 | 1,782,368| D₃₀ | 69,351 |

Note: Effective B₂′ is larger than requested B₂ due to d₁d₂ block structure.

## Record factors (as of January 2006)

### Largest ECM factor (66 digits) — Bruce Dodson, April 6, 2005
n = factor of 3⁴⁶⁶+1
p66 = 709601635082267320966424084955776787970864725643996885415676682297
Group order: 2²·3·11243·336181·844957·1866679·6062029·7600843·8046121·8154571·13153633·249436823
B₁ = 110·10⁶, σ = 1875377824
Largest group order factor ≈ 2.3·B₁ (much smaller than default B₂′).

### Largest P−1 factor (58 digits) — Zimmermann, Sep 28, 2005
n = 2²⁰⁹⁸+1
p58 = 137209840691013934741147397829773702964959583843164650153
B₁ = 10¹⁰, B₂ ≈ 1.38·10¹³

### Largest P+1 factor (48 digits) — Alexander Kruppa, Mar 29, 2003
n = Lucas number L(1849)
p48 = 884764954216571039925595816362554326397028807829
B₁ = 10⁸, B₂ ≈ 5.23·10¹⁰

### Largest group order factor (≈ 8.13·10¹³) — Dodson, Dec 27, 2005
n = 5⁴³⁰+1, 47-digit factor
Group order factor 81325590104999 ≈ 33.4·B₂ — success of Brent–Suyama extension.

## Performance observation (Figure 3)

Histogram of log(g₁/B₁) for 594 Cunningham factors found by ECM:
- Many factors have largest group order factor much larger than B₁.
- Standard ECM with B₂=100B₁ (log 100 ≈ 4.6) misses about half the factors that could be found with FFT continuation.

## Save/resume interface

- Stage 1 can be run in George Woltman's prime95 (faster on x86, but no FFT continuation).
- Stage 2 then run in GMP-ECM.
- Also allows splitting stage 2 across multiple computers (range [l,h] per machine).

## Open questions (Section 4.0.7)

1. **Stage 2 for very large n** (e.g., Fermat numbers): FFT continuation may be too expensive; may need to revert to classical continuation or PAIR algorithm (Kruppa 2005).
2. **Stage 1 bottleneck**: Can we break sequentiality of stage 1? Any o(B₁) cost algorithm would be a breakthrough.
3. **Saving one multiply per duplicate**: Forcing b small in curve equation y² = x³ + ax + b — possible for Suyama parametrization? Requires solving polynomial equation in σ mod n.
4. **Stage 3**: Hit two large primes in stage 2 — how much would it increase success probability?

## Acknowledgements

- H. W. Lenstra, Jr. — invention of ECM
- Peter Montgomery, Richard Brent — major improvements
- Alexander Kruppa, Jim Fougeron, Laurent Fousse, Dave Newman — GMP-ECM developers
- Torbjorn Granlund — GMP library
- George Woltman — save/resume interface
- Users who found factors (including anonymous ones who didn't find any)
