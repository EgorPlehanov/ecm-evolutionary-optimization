---
title: "A Survey of Integer Factorization Algorithms"
title_en: "A Survey of Integer Factorization Algorithms"
source_type: "technical_report"
authors: ["Montgomery P. L."]
year: "1994"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "survey-of-integer-factorization-algorithms-1994.md"
---

# Content source: A Survey of Integer Factorization Algorithms

## Source type
Technical report / survey article (appears to be an internal CWI document or unpublished manuscript from 1994, possibly later incorporated into a published work).

## Author affiliation
Peter L. Montgomery — CWI (Centrum voor Wiskunde en Informatica), Amsterdam.

## Objective
Provide a comprehensive survey of integer factorization algorithms, from elementary methods to state‑of‑the‑art (as of 1994) algorithms including Pollard Rho, P±1, ECM, Quadratic Sieve (MPQS), and the Number Field Sieve (NFS), with examples, complexity analyses, and records achieved at CWI.

## Core content summary

### 1. Fundamental concepts (Sections 2–5)
- **Modular arithmetic**, Chinese Remainder Theorem (CRT)
- **Smooth numbers**: integer n is B-smooth if all prime factors ≤ B.
  Density ≈ x·u⁻ᵘ where u = ln x / ln B.
- **Prime Number Theorem**: π(x) ~ x / ln x
- **RSA cryptosystem**: security depends on difficulty of factoring large integers.

### 2. Small‑factor methods (Section 6)

#### Pollard Rho (1975, Pollard)
- Iterates polynomial f(X) = X² + 1 modulo N.
- Sequence modulo prime p eventually periodic.
- Detects cycles via gcd(x₂ₙ − xₙ, N).
- **Complexity**: O(√p) iterations → O(N¹⸍⁴ (log N)²) bit operations.
- **Brent's variation**: tests gcd when n is a power of 2; ~24% faster.
- **Example**: Factor 563 from N = 1098413 after 5 iterations (Figure 6.2).

#### Pollard P−1 (1974, Pollard)
- Finds prime p if p−1 is B-smooth.
- Compute M = lcm of prime powers ≤ B, then aᴹ mod N.
- **Step 2** (Montgomery, Brent, etc.): allows one large prime q > B.
- **Example**: Finds 1951 (1951−1 = 2·3·5²·13) from N = 1098413 with B = 30.

#### Williams P+1 (1982)
- Works in GF(p²) using Lucas sequences.
- Succeeds if p+1 is smooth.
- Need P²−4 to be quadratic non‑residue (probabilistic; 87.5% success with 3 tries).
- **Example factor**: 37‑digit factor of 45¹²³ + 1 found with B = 30 million.

#### Elliptic Curve Method (ECM, Lenstra 1985)
- Generalizes P±1 by using group of points on elliptic curve over GF(p).
- Group order varies randomly between p+1−2√p and p+1+2√p (Hasse).
- By changing curve, different group orders are obtained.
- If order is B-smooth (or B₁-smooth with one extra prime ≤ B₂), ECM finds p.
- **Advantage**: Success probability independent of p±1 structure.
- **Example**: Factors 843rd Fibonacci number (12‑, 13‑, 15‑, 16‑digit factors missed by P−1/P+1).
- **Record (1993)**: 43‑digit factor of partition number p(19997) by F.‑D. Berger.
- **CWI record**: 40‑digit factor of 26¹²⁶ + 1 using 128 curves on Cray C90.

### 3. Congruence of squares methods (Section 7)

General approach: find X² ≡ Y² (mod N) with gcd(XY,N)=1 → gcd(X−Y,N) factors N with probability 1−2¹⁻ᵏ for k distinct odd primes.

#### Continued Fraction Method (CFRAC, Morrison–Brillhart 1975)
- Uses convergents P/Q to √N → P² − NQ² = O(√N).
- Small residues more likely smooth.
- **Record**: Factored 7th Fermat number (2¹²⁸+1, 39 digits) in 1970.

#### Sieving (general technique)
- For polynomial f, values f(x) divisible by p lie in arithmetic progressions.
- Sieve by subtracting log p from array entries; survivors are smooth.

#### Quadratic Sieve (QS, Pomerance 1985)
- Uses f(X) = X² − N, sieving x near √N.
- Residual size O(M√N) for sieve interval length M.
- **Multiple Polynomial QS (MPQS, Montgomery)**:
  - Uses many quadratic polynomials g(X) = a²X² + bX + c with b² − 4a²c = kN.
  - Each polynomial sieved over short interval → residual O(M₀√N) independent of total range.
  - Easily parallelized.

#### Large prime variations
- Allow smoothness up to one or two large primes beyond factor base.
- When same large prime appears in two relations, combine them.
- **PPMPQS**: two large primes.

#### Linear algebra over GF(2)
- Build matrix of exponent vectors (mod 2) of prime factorizations.
- Find nullspace vector → subset with even exponents → square.
- For large sparse matrices, iterative methods (Lanczos, Wiedemann) used.

### 4. Number Field Sieve (NFS, Pollard 1988, Lenstra et al. 1990/1993)

**Four phases**:

1. **Polynomial selection**:
   - Choose two irreducible polynomials f, g ∈ ℤ[X] with small coefficients.
   - Find integer m such that f(m) ≡ g(m) ≡ 0 (mod N).
   - For numbers of special form (e.g., Fermat numbers), one polynomial can be linear.

2. **Sieving**:
   - Find coprime integer pairs (a,b) such that both bᵈᵉᵍ⁽ᶠ⁾·f(a/b) and bᵈᵉᵍ⁽ᵍ⁾·g(a/b) are smooth.
   - These are norms of algebraic numbers a − bα and a − bβ.

3. **Linear algebra**:
   - Factor prime ideals in number fields Q(α) and Q(β).
   - Find set S where products of (a−bα) and (a−bβ) are squares of ideals.

4. **Square root**:
   - Compute square roots in number fields (Couveignes for odd degree, Montgomery for any degree).
   - Map back to integers via homomorphism α → m, β → m.

**Advantages**:
- Numbers tested for smoothness have size ~ exp((log N)²⸍³) — much smaller than √N.
- Asymptotic complexity L[1/3, (64/9)¹⸍³] — faster than QS for large N.

### 5. Records (as of 1994)

| Record | Method | Digits | Year | Notes |
|--------|--------|--------|------|-------|
| F₇ | CFRAC | 39 | 1970 | 2¹²⁸+1 |
| RSA‑129 | MPQS (PPMPQS) | 129 | 1994 | 5000 MIPS‑years, worldwide effort |
| N₁₆₂ (Cunningham) | NFS | 162 | 1993–1994 | p₄₄·p₁₁₉, sieved at OSU, linear algebra at CWI |
| N₁₀₅ (3³⁶⁷−1 cofactor) | NFS | 105 | 1994 | First NFS on number without special form |
| Partition number p(11887) cofactor | NFS (5th degree) | 116 | 1994 | Record broken month after N₁₀₅ |

**Matrix sizes** (N₁₆₂):
- 828077 × 833017, 32.3 nonzeros per column.
- Solved in 7.5 hours on Cray C90 using Block Lanczos.

## Key algorithms summary table

| Algorithm | Type | Complexity | Best for |
|-----------|------|------------|----------|
| Trial division | deterministic | O(√N) | very small N |
| Pollard Rho | probabilistic | O(√p) | small factors |
| P−1 | special‑purpose | O(B log N) | p−1 smooth |
| P+1 | special‑purpose | O(B log N) | p+1 smooth |
| ECM | special‑purpose | L_p[1/2, √2] | medium factors (10–50 digits) |
| CFRAC | general | L[1/2, √2] | historical |
| QS / MPQS | general | L[1/2, 1] | 80–120 digits (1994) |
| NFS | general | L[1/3, (64/9)¹⸍³] | >120 digits (1994) |

## Notable factorization examples

### RSA‑129 (1994)
```
RSA-129 = 1143816257578888676692357799761466120102182967212423625625618429
          35706935245733897830597123563958705058989075147599290026879543541
= p₆₄ · p₆₅
p₆₄ = 3490529510847650949147849619903898133417764638493387843990820577
p₆₅ = 32769132993266709549961988190834461413177642967992942539798288533
```

### N₁₆₂ (Cunningham number)
- First large NFS factorization with two nonlinear polynomials.
- Sieved on 30 workstations over 8 weeks, 8.98M relations.
- Linear algebra completed at CWI.

## Limitations (explicit from source / context)
- ECM effectiveness depends on smoothness of random group order near p; no deterministic guarantee.
- NFS polynomial selection for general numbers is not fully automated; still an art.
- Large matrices require specialized iterative methods and high‑performance computing.
- Records cited are as of 1994; subsequent progress (especially in NFS) has vastly extended feasible sizes.

## Practical workflow (as of 1994)
1. Remove small factors by trial division up to some bound.
2. Apply Pollard Rho, P−1, P+1, ECM to find small to medium factors.
3. When cofactor is "sufficiently small" (<100–120 digits), apply MPQS.
4. For larger cofactors or numbers of special form, apply NFS.
5. Use parallelization: multiple polynomials in MPQS, multiple curves in ECM, multiple workstations in sieving.

## References cited (selected)
- Pollard (1974, 1975) — P−1, Rho
- Williams (1982) — P+1
- Lenstra (1987) — ECM
- Morrison & Brillhart (1975) — CFRAC, factorization of F₇
- Pomerance (1982, 1985) — QS
- Montgomery — MPQS, Block Lanczos, NFS square root
- Lenstra & Lenstra (1993) — Development of NFS
- Couveignes (1993) — NFS square root
