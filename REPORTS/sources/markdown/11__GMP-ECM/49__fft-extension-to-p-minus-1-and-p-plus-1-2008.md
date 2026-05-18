---
title: "FFT continuation of P-1 and P+1 factorization algorithms"
title_en: "FFT continuation of P-1 and P+1 factorization algorithms"
source_type: "article"
authors: ["Montgomery P. L.", "Kruppa A."]
year: "2008"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "fft-extension-to-p-minus-1-and-p-plus-1-2008.md"
---

# Content source: FFT continuation of P-1 and P+1 factorization algorithms

## Source type
Preprint / technical report (submitted to ANTS-VIII, 2008). HAL open archive.

## Authors affiliation
- Peter L. Montgomery — Microsoft Research, Redmond, WA, USA (also CWI, Amsterdam).
- Alexander Kruppa — LORIA, Nancy, France.

## Objective
Present a space‑efficient implementation of stage 2 of Pollard's P−1 and Williams's P+1 factorization algorithms using Fast Fourier Transforms (FFTs) and Number Theoretic Transforms (NTTs). Achieve convolution lengths up to 2²³ (~8 million) and stage 2 limits B₂ ≈ 10¹⁶ on modern PCs with 4–32 GB RAM. Report record factors, including a 60‑digit P+1 factor.

## Core content summary

### 1. Background: P−1 and P+1 methods (Sections 1–2)

**P−1** (Pollard 1974):
- Stage 1: compute b₁ = b₀ᵉ mod N where e = lcm(1,…,B₁). If p | N and (p−1) | e, then b₁ ≡ 1 (mod p) → p | gcd(b₁−1, N).
- Stage 2: if p−1 = n·q with n | e and B₁ < q ≤ B₂, then b₁^q ≡ 1 (mod p) → p | gcd(b₁^q−1, N).

**P+1** (Williams 1982):
- Replace multiplicative group F_p* with group of points on a quadratic twist: works when p+1 is smooth.
- Use Lucas sequences; stage 2 analogous to P−1.

**Traditional stage 2** (Montgomery 1987): O(π(B₂) − π(B₁)) operations.

**FFT continuation** (Montgomery & Silverman 1990): O(√B₂ log B₂) using polynomial evaluation along geometric progressions.

### 2. Algorithm overview (Section 3)

**Goal**: Find prime q ∈ [B₁, B₂] such that b₁^q ≡ 1 (mod p) for some unknown p | N.

**Covering sets S₁, S₂**:
- Choose integer P (product of small primes) with large ratio φ(P)/P.
- Choose S₁, S₂ such that every integer coprime to P can be written as q = P + 2k₁ + 2k₂ + 2mP for some k₁∈S₁, k₂∈S₂, integer m.
- Let s₁ = |S₁|, s₂ = |S₂|.
- Then for each k₂ ∈ S₂, evaluate polynomial f(X) at points X = b₁^{2k₂ + (2m+1)P} for m = m₁ … m₂−1 (geometric progression with ratio b₁^{2P}).

**Polynomial f**(X):
- Monic reciprocal Laurent polynomial (RLP) with roots b₁^{±2k₁} for k₁∈S₁.
- f(X) has degree s₁ (even). Represented with s₁/2 coefficients (plus leading 1).
- f(X) is symmetric: f(X) = f(1/X).

**Multipoint evaluation** (Section 8):
- Using convolution of length ℓ = ℓ_max (power of 2, ≥ s₁/2).
- Compute h(X) = ∑_{j} r^{-j²} f_j X^j where r = b₁^P.
- Compute g(X) = ∑_{i} x₀^{M−i} r^{(M−i)²} X^i where x₀ = b₁^{2k₂ + (2m₁+1)P}, M = ℓ−1−s₁/2.
- Then coefficient of X^{M−m} in g(X)h(X) (mod X^ℓ−1) is x₀^m r^{m²} f(x₀ r^{2m}).
- Compute by NTT convolution of length ℓ.

**Adaptation for P+1**:
- Work in quadratic extension ring (Z/NZ)[√Δ] where Δ = P₁²−4.
- Use basis {1, √Δ}. Each element uses 2× storage.
- Recurrence (12) to compute powers r^{n²} in extension ring (5 multiplications per step).
- Evaluate f using two convolutions (real and imaginary parts) via equation (13).

### 3. Building polynomial f (Section 7)

**Decomposition of S₁**:
- S₁ = T₁ + T₂ + … + T_m, each T_j arithmetic progression of prime length centered at 0.
- Example: T₁ = {−k, k} (length 2), T₂ length t₂, etc.

**Iterative construction**:
- Start with F₁(X) = X + X⁻¹ − (α₁^{2k} + α₁^{-2k}) = X + X⁻¹ − V_{2k}(P₁) (degree 2).
- For each T_{j+1}, form F_{j+1}(X) = ∏_{k₂∈T_{j+1}} F_j(α₁^{2k₂} X) using RLP multiplication.
- Use **weighted NTT** to multiply RLPs (Section 6.2, Figure 1).
- Final f = F_m, degree s₁.

**Reciprocal Laurent polynomial multiplication** (Section 6.2):
- Represent RLP by coefficients a₀,…,a_{d/2} for basis {1, X^j+X^{-j}}.
- To multiply two RLPs of degree ≤ 2d_q, 2d_r, set ℓ > d_q+d_r, choose w with w^ℓ = ±1.
- Perform weighted convolution: store q_j w^j and r_j w^j, compute product, extract s_j via solving 2×2 system for overlapping coefficients.

### 4. Memory management (Section 9, Table 1)

**Buffers** (for 230‑digit N, N≈12×64‑bit words = 12 quadwords):
- **MZNZ**: stores coefficients (s₁/2 elements).
- **MDFT**: stores NTT transforms (ℓ elements per NTT prime).
- **MHDFT**: stores DFT of h (ℓ/2+1 elements for P−1, ℓ+2 for P+1).

**NTT parameters**:
- Use 25 primes of 63–64 bits each, product > ℓ·N².
- For ℓ_max = 2²³ (~8.4 million), memory ~315 million quadwords (~2.5 GB).
- For ℓ_max = 2²⁶ (~67 million), memory ~2.5× larger (requires 32 GB).

**Parallelization** (Section 10):
- Distribute NTT primes across cores.
- On NUMA, allocate memory local to each core.
- Use recurrences to compute r^{−j²} and g_i for contiguous blocks.

### 5. Implementation and performance (Sections 11–12)

**Implementation**:
- Based on GMP‑ECM (Zimmermann & Dodson 2006).
- New stage 2 replaces previous product‑tree implementation (O(n (log n)²) cost).
- Uses GMP for arbitrary precision, Montgomery REDC, fast reduction mod 2ⁿ±1.

**Performance example** (230‑digit cofactor of 12²⁵⁴+1, 2.4 GHz Opteron):

| Method | B₂ | ℓ_max | s₁ | s₂ | Time (single core) | Time (8‑core) |
|--------|-----|-------|----|----|--------------------|---------------|
| P−1 (old) | 10¹⁵ | — | — | — | 34,080 s | — |
| P−1 (new) | 1.2·10¹⁵ | 2²⁴ | 7.4e6 | 3 | 1,738 s | 269 s (elapsed) |
| P+1 (new) | 1.2·10¹⁵ | 2²⁴ | 7.4e6 | 3 | 3,356 s | 642 s (elapsed) |
| P−1 (new) | 1.34·10¹⁶ | 2²⁶ | 3.32e7 | 2 | 5,483 s | 922 s (elapsed) |
| P+1 (new) | 1.34·10¹⁶ | 2²⁶ | 3.32e7 | 2 | 10,089 s | 2,192 s (elapsed) |

- Speedup over old stage 2: factor ~20 (P−1) and ~? (P+1 not compared).

### 6. New record factors (Section 12, Table 2)

| Number | Method | Factor (p) | Digits | Largest factor of p±1 |
|--------|--------|------------|--------|----------------------|
| 73¹⁰⁹−1 | P−1 | 760227...152299 | c191 | 462832247372839 (15 digits) |
| 24¹⁴²+1 | P−1 | 204890...24637 | c183 | 12750725834505143 (17 digits) |
| 47¹⁴⁶+1 | **P+1** | 798647...4001 | **52** | 1632221953 etc. |
| **L₂₃₆₆** | **P+1** | **725516...50523** | **60** | 483576618980159 (15 digits) |

- The 60‑digit factor of Lucas number L₂₃₆₆ is a record for P+1 (previous record 48 digits).
- The 17‑digit factor q = 12750725834505143 (for 24¹⁴²+1) is the largest prime reported in the group order for P−1/P+1/ECM at the time.

### 7. Technical innovations

1. **Reciprocal Laurent polynomials** reduce storage by factor ~2 (store only half the coefficients).
2. **Weighted NTT** for RLP multiplication (Section 6.2, Figure 1).
3. **Efficient multipoint evaluation** along geometric progression using one convolution of length ℓ.
4. **Extension ring arithmetic** for P+1 using two convolutions.
5. **Memory‑efficient** NTT with multiple small primes (explicit CRT) and in‑place transforms.
6. **Parallelization** across NTT primes and across blocks of indices.

## Key formulas

**Covering condition** (Section 5):
- q = P + 2k₁ + 2k₂ + 2mP.
- S₁ + S₂ ≡ (Z/PZ)* (mod P).
- Use Chinese Remainder Theorem to construct S₁, S₂ from prime power decompositions.

**Weighted RLP convolution** (Section 6.2):
- ℓ > d_q + d_r, choose w with w^ℓ = ±1.
- Compute convolution of w^j q_j and w^j r_j.
- Extract s_j from output using 2×2 system for overlapping coefficients.

**Multipoint evaluation** (Section 8):
- h_j = r^{-j²} f_j, g_i = x₀^{M−i} r^{(M−i)²}.
- Then coefficient of X^{M−m} in g·h ≡ x₀^m r^{m²} f(x₀ r^{2m}) (mod X^ℓ−1).

**Recurrence for r^{n²} in extension ring** (Equation 12):
- r1[i] = r²? (details in paper)
- Uses 5 base‑ring multiplications per step.

## Limitations (explicit from source)

- Does **not** apply to ECM (elliptic curve method) – only to P−1 and P+1.
- Requires large memory (≥4 GB for 2²³, ≥32 GB for 2²⁶).
- NTT implementation restricted to power‑of‑two lengths (and 3·2^k? supported but not detailed).
- P+1 stage 2 requires two convolutions (vs one for P−1), so ~2× slower.
- Polynomial construction for f uses degree up to s₁ ≈ ℓ_max/2; for very large B₂, this may dominate memory.
- No optimality proof for parameter choices (P, S₁, S₂).

## References (selected)
- Pollard (1974) — P−1 algorithm
- Williams (1982) — P+1 algorithm
- Montgomery (1985) — REDC modular multiplication
- Montgomery (1987) — Speeding Pollard and ECM
- Montgomery & Silverman (1990) — FFT extension to P−1 (Math. Comp.)
- Montgomery (1992) — PhD thesis (FFT extension to ECM)
- Zimmermann & Dodson (2006) — 20 years of ECM, GMP‑ECM
- Crandall & Fagin (1994) — Discrete weighted transforms
- Bernstein & Sorenson (2007) — Explicit CRT
