---
title: "FFT extension for algebraic-group factorization algorithms"
title_en: "FFT extension for algebraic-group factorization algorithms"
source_type: "book_chapter"
authors: ["Brent R. P.", "Kruppa A.", "Zimmermann P."]
year: "2017"
source_link: "https://hal.inria.fr/hal-01630907"
doi: "none (HAL preprint)"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "fft-extension-algebraic-group-factorization-2017.md"
---

# Content source: FFT extension for algebraic-group factorization algorithms

## Source type
Book chapter in "Topics in Computational Number Theory Inspired by Peter L. Montgomery" (Cambridge University Press, 2017, pp. 189–205).

## Authors affiliation
- Richard P. Brent — Australian National University (formerly)
- Alexander Kruppa — INRIA, France
- Paul Zimmermann — INRIA, France

## Objective
Describe Montgomery's FFT extension for stage two of algebraic-group factorization algorithms (ECM, p−1, p+1), which uses fast polynomial arithmetic (product trees, remainder trees, polynomial GCD) to reduce complexity from Θ(B₂/log B₂) to Õ(√B₂) operations.

## Core methodology (ECM stage two)

### Problem reduction
- Stage two: for primes π ∈ (B₁, B₂], compute πQ and check if gcd(z_π, n) > 1.
- Let S = {i·d} (d ≈ √B₂), T = {j: 0<j<d, gcd(j,d)=1}.
- Then all primes in (B₁, B₂] can be written as π = σ + τ (σ∈S, τ∈T).
- Condition σQ + τQ = O_E mod p ⇔ x_σ = x_τ mod p.
- Goal: compute h = ∏_{σ∈S} ∏_{τ∈T} (x_σ − x_τ) mod n.

### Fast polynomial arithmetic (POLYEVAL variant)

**Product tree** (Algorithm 1):
- Build F(X) = ∏_{τ∈T} (X − x_τ) and G(X) = ∏_{σ∈S} (X − x_σ)
- Complexity: O(M(d) log d) where M(d) = cost of multiplying degree-d polynomials.

**Remainder tree** (Algorithm 2, POLYEVAL):
- Evaluate F(x_σ) for all σ∈S via recursive modular reduction.
- Use RECIP algorithm to compute polynomial reciprocals (Barrett reduction for polynomials).
- Newton iteration: RECIP(G) = ⌊X^{2d}/G(X)⌋.
- Quotient: H(X) = ⌊⌊F(X)/X^d⌋·RECIP(G)/X^d⌋.
- Remainder: F(X) mod G(X) = F(X) − G(X)·H(X).
- Complexity: O(M(d) log d).

**Memory**: O(d log d) coefficients (can be reduced via external storage).

### POLYGCD variant (resultant as polynomial GCD)
- h = resultant(F, G) = Res(F, G).
- Compute via subquadratic polynomial GCD (HGCD) using quotient sequence.
- If Euclidean algorithm encounters non-invertible coefficient → yields factor of n.
- Complexity: O(M(d) log d), memory O(d) (smaller constant than POLYEVAL, but larger proportionality).

### Choice of points of evaluation
- Use x-coordinate only: x_σ and x_τ.
- Since x(P) = x(−P), match occurs if σQ = ±τQ ⇒ (σ ± τ)Q = O_E.
- If o = ord(Q) prime, then σ ≡ ±τ (mod o).
- Set T = {j: 0<j<d/2, gcd(j,d)=1} (half size) — primes expressed as σ−τ or σ+τ.

### Brent–Suyama extension (powers and Dickson polynomials)

**Using powers**:
- Compute σᵏQ, τᵏQ instead of σQ, τQ.
- Factor found if σᵏ ≡ ±τᵏ (mod o).
- X^{2k}−1 factors into ν(2k) cyclotomic polynomials.
- Clustering effect: primes with gcd(o−1,2k) large overrepresented.

**Dickson polynomials** (degree k, parameter a):
- D_{k,a}(X) has property: D_{k,a}(X) − D_{k,a}(Y) factors like X^{k} − Y^{k}.
- Average roots: (gcd(o−1,k) + gcd(o+1,k))/2 — avoids clustering.
- Implemented in GMP-ECM with Dickson polynomials of degree 30.

**Effectiveness (60-digit factor, B₁=2.6·10⁸, B₂≈3.18·10¹²)**:

| Polynomial | Expected curves |
|------------|-----------------|
| X¹ | 54,038 |
| X³⁰ | 48,508 |
| D₃₀(X) | 47,888 |

### Numerical example: factorization of 2¹¹⁶³−1
- Found by Bos, Kleinjung, Lenstra, Montgomery (2010).
- 73-digit factor p₇₃ using ECM with B₁=3·10⁹, B₂=10¹⁴, σ=3000085158.
- Group order: g = 2²·3²·5·23·1429·28229·1391133·249677·389749·15487861·47501591·111707179·g₂·g₁.
- Largest prime factors: g₁ = 13,007,798,103,359, g₂ = 431,421,191.
- g₁ / B₁ ≈ 4336.

## FFT extension for p−1 and p+1 methods

### Key differences from ECM
- Multiplicative group (p−1) or quadratic extension (p+1) — geometric progression.
- S = {kP: k∈ℕ, B₁ ≤ kP ≤ B₂} for highly composite P.
- T factored into sum of arithmetic progressions of prime length (using Chinese remainder theorem).

### Constructing F(X) for p−1
- Use reciprocal Laurent polynomials (RLPs): f(X) = Σ_{i=0}^{d} f_i (X + X⁻¹)ⁱ.
- Recursive construction via scaling and multiplication:
  - For set of cardinality 2: F₁(X) = X + X⁻¹ − V_{35}(R)
  - For odd cardinality: scale existing RLP by Q^{±k} and multiply.
  - Complexity: O(M(d)) — faster than generic product tree by factor log d.

### Evaluation via chirp-z transform (Bluestein's algorithm)
- Evaluate F(Q^{kP}) for k=0,...,s−1 via cyclic convolution:
  - F(Q^{kP}) = Q^{k²P/2} · Σ_i (f_i Q^{i²P/2}) · Q^{-(i−k)²P/2}
  - Single convolution of length ℓ = s + t (t = deg F).
- Complexity: O(M(t)) — faster than generic multi-point evaluation by factor log t.

### Practical results (p±1)
- 55-digit factor of 81901⁴¹−1 found by A. Reich (March 2015) using p−1.
- 60-digit factor of Lucas number L₂₃₆₆ found by Montgomery & Kruppa (Oct 2007) using p+1.

## Key contributions (historical context)
- Montgomery (1992) first to apply FFT to ECM stage two (PhD dissertation).
- Montgomery & Silverman (1990) FFT extension for p−1.
- Brent–Suyama extension (using higher powers) improves probability.
- Dickson polynomials (Montgomery 1992) avoid clustering bias of powers.
- Kruppa & Montgomery (2008) improved p±1 stage two via RLPs and chirp-z transform.

## Implementation notes
- Implemented in GMP-ECM (open source).
- Product tree can be stored on external storage to reduce memory.
- Fast polynomial multiplication via FFT modulo small primes + CRT, or Kronecker–Schönhage trick.

## Limitations (implicit)
- Assumes d = 2^k (power of two) for efficient product/remainder trees (can handle non-powers with adjustments).
- POLYEVAL requires O(d log d) memory; POLYGCD uses O(d) but larger constant.
- For p+1, Q not explicitly known → arithmetic in quadratic extension (higher cost).
- Dickson polynomials of high degree increase computation cost.

## Practical relevance
- Standard technique in modern ECM implementations (GMP-ECM).
- Enables finding 60+ digit factors with reasonable computational effort.
- Used in record factorizations (e.g., 2¹¹⁶³−1, RSA-240 cofactorization).
