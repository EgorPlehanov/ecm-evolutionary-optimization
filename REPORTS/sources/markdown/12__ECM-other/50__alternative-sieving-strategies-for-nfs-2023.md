---
title: "We are on the same side. Alternative sieving strategies for the number field sieve"
title_en: "We are on the same side. Alternative sieving strategies for the number field sieve"
source_type: "conference"
authors: ["Bouillaguet C.", "Fleury A.", "Fouque P.-A.", "Kirchner P."]
year: "2023"
source_link: "https://doi.org/10.1007/978-981-99-8730-6_5"
doi: "10.1007/978-981-99-8730-6_5"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "alternative-sieving-strategies-for-nfs-2023.md"
---

# Content source: We are on the same side. Alternative sieving strategies for the number field sieve

## Source type
Peer-reviewed conference paper (ASIACRYPT 2023, Guangzhou, China, December 2023, pp. 138–166). Springer.

## Authors affiliation
- Bouillaguet — Sorbonne Université, CNRS, LIP6, Paris, France.
- Fleury — Université Paris‑Saclay, CEA, List, Palaiseau, France.
- Fouque, Kirchner — Univ Rennes, CNRS, IRISA, France.

## Objective
Investigate alternative sieving strategies for the Number Field Sieve (NFS) to speed up relation collection – the most time‑consuming step (≈90% of total time for RSA‑250). Specifically, combine sieving (for medium/large primes) with Bernstein's batch smooth part algorithm (for extra‑small primes) on the same side, instead of sieving all primes up to the factor base bound. Evaluate experimentally using relations collected during the RSA‑250 factorization.

## Core content summary

### 1. Motivation and context

**NFS steps**:
- Polynomial selection, sieving (relation collection), filtering, linear algebra, square root.
- For RSA‑250 (250 digits, 829 bits), sieving required **2450 core‑years** (≈90% of total).

**Sieving in Cado‑NFS** (state‑of‑the‑art implementation):
- Uses lattice sieving (special‑q) with sieve area A = 2³³.
- Primes divided into ranges with different algorithms (Table 1):
  - **[2, 2^I]**: small sieve (two passes: approximate log, then exact for survivors).
  - **[2^I, bkthresh1]**: 1‑level bucket sieve.
  - **[bkthresh1, lim]**: 2‑level bucket sieve.
- Parameters for RSA‑250 (Table 3):
  - lim₀ = lim₁ = 2³¹
  - 1pb₀ = 36, 1pb₁ = 37 (large prime bounds)
  - mfb₀ = 72 (small special‑q) or 74 (large), mfb₁ = 111

**Relation collection process** (Section 4.1):
1. Sieve norms on algebraic side → survivors.
2. Trial division on survivors (algebraic side) → filter.
3. **Batch factor survivors on rational side** (product tree).
4. Filter → cofactorization.

### 2. Bernstein's batch smooth part algorithm (Section 2)

**Idea**: Given factor base P of primes and set of integers N = {n₁,…,nₖ}, compute smooth part of each n_i (product of primes in P dividing n_i) in O(b log²⁺ᵒ⁽¹⁾ b) where b = total bits.

**Steps**:
1. Compute z = ∏_{p∈P} p (product tree).
2. Compute r_i = z mod n_i (remainder tree).
3. For each i: s_i = gcd(r_i, n_i); if s_i>1, extract factors, divide n_i, repeat.

**Implementation in Cado‑NFS**: uses scaled remainder trees (Bernstein 2004) for better performance.

**Performance (Fig. 2)**: For prime product of size n bits, processing n/2 bits of integers takes ~0.001×n²? (log scale). Example: 3.1 Gbit product (primes <2³¹), batch of 5M 300‑bit numbers takes 271 s.

### 3. Statistical analysis of RSA‑250 relations (Section 5)

**Dataset**: 8.4G relations, 786 GB gzipped (1.5 TB uncompressed). Parsed with multithreaded C programs (370 MB/s, 3.8M relations/s on 32 cores).

**Basic statistics (Table 2)**:

| Range | special‑q | # relations | Rational norm (bits) | Algebraic norm (bits) |
|-------|-----------|-------------|----------------------|------------------------|
| Small | 1G–4G | 3.9G | 151.8 ± 2.0 | 283 ± 8.6 |
| Large | 4G–12G | 4.5G | 152.6 ± 2.0 | 288 ± 8.4 |

**Probability of prime occurrence** (Fig. 5, Section 5.1):
- Not 1/p as in random integers.
- For B‑smooth numbers, probability ≈ 1/p^α with α < 1.
- From Hildebrand‑Tenenbaum (1986): Ψ(x/p, y) / Ψ(x, y) ≈ 1/p^α, where α solves Σ_{p≤y} (log p)/(p^α − 1) = log x.
- α ≈ (log(1+y/log x))/log y.
- Sieved primes appear more frequently; special‑q's have boost.

**Yield per special‑q** (Fig. 6, Section 5.2):
- Density of relations: small special‑q ≈ 1.3, large ≈ 0.56.
- Model: R(q) ∝ (1/log q)·ρ((208 + α log₂ q)/37), where ρ is Dickman function.
- α ≈ 2.42 for small q, ≈ 2.54 for large q (empirical fit).
- For large q range, model predicts actual relations with 0.027% error.
- **Implication**: If alternative procedure finds fraction f of relations, must sieve special‑q up to q_max where ∫ f(q) dq = target. e.g., f=0.85 → need ≈26% more special‑q.

### 4. Combining sieving and batch smooth part on same side (Section 6)

**Two potential strategies**:

#### Strategy A: Sieve only extra‑small primes (Section 6.1)
- Sieve primes up to 2^B (small), discard rest.
- Use batch algorithm for remaining primes.
- **Conclusion**: Not practical with large sieve area (2³³). To avoid overwhelming batch algorithm, survival rate must be <0.1746% → discards too many real relations.

#### Strategy B: Sieve only medium/large primes (skip extra‑small) (Section 6.2)
- Do **not** sieve primes below 2^B.
- Sieve primes in [2^B, lim].
- After sieving, use batch algorithm to find missing small factors.
- **Advantage**: Sieving large primes is more efficient (fewer hits), batch algorithm can handle many survivors because missing small factors are… small.

**Parameter tuning** (Fig. 8, Table 5):
- For B = 17 (disable small sieve entirely), find mfb₀, mfb₁ to preserve target fraction (e.g., 85%, 90%) while minimizing survivors.
- Example for 85% relations: mfb₀ = 114, mfb₁ = 136, survival rate ≈ 10⁻².⁹⁵ ≈ 0.112%.

### 5. Implementation and results (Section 7)

**Modified Cado‑NFS**:
- Removed primes <2^B from factor base.
- Precomputed product of extra‑small primes.
- After sieving, applied batch algorithm to survivors to recover small factors.
- Experimental validation using Grid'5000 testbed.

**Results for small special‑q range [2.5G, 2.5G+500] (Table 7, B=17)**:

| mfb₀ | mfb₁ | #relations (×original) | Time (×original) | Local speedup |
|------|------|------------------------|------------------|---------------|
| 151 | 90 | 0.77 | 0.76 | 1.02 |
| 156 | 85 | 0.83 | 0.78 | 1.06 |
| 167 | 86 | 0.90 | 0.82 | 1.10 |
| 254 | 19 | 0.96 | 1.01 | 0.88 |

**For large special‑q range [8.2047G, 8.2047G+68] (Table 6, B=17)**:

| mfb₀ | mfb₁ | #relations (×original) | Time (×original) | Local speedup |
|------|------|------------------------|------------------|---------------|
| 152 | 59 | 0.77 | 0.78 | 1.08 |
| 158 | 51 | 0.85 | 0.81 | 1.10 |
| 167 | 37 | 0.90 | 0.94 | 1.01 |

**Best observed**: ~90% relations in ~82% time → local speedup ≈1.10.

### 6. Projected overall speedup for full factorization (Section 5.2, Conclusion)

- If new procedure finds 90% relations in 80% time, must sieve 16% more special‑q to compensate.
- Overall expected speedup ≈ (0.80 × 1.16)⁻¹? Wait: more special‑q means more work. Original: 1 unit time. New: 0.80 time per special‑q × 1.16 special‑q = 0.928 time → **≈7–8% speedup** (authors claim ~5%).
- Tables 6–7 show speedups up to 1.10 locally; after compensating for lost relations, net speedup ≈5%.

## Key parameters (RSA‑250)

| Parameter | Value | Meaning |
|-----------|-------|---------|
| lim₀, lim₁ | 2³¹ | Largest sieved prime (both sides) |
| 1pb₀, 1pb₁ | 36, 37 | Large prime bound (bits) |
| mfb₀ | 72 (small q), 74 (large) | Cofactor bound (bits) |
| mfb₁ | 111 | Cofactor bound (bits) |
| Sieve area A | 2³³ | # (a,b) pairs per special‑q |
| special‑q range | 1G – 12G | ~10¹⁰ to 1.2×10¹⁰ |
| Total relations | 8.4G | 3.9G small q, 4.5G large q |

## Limitations (explicit from source)

- **Only tested on RSA‑250 data**; parameters may not generalize to other numbers.
- **Batch algorithm invoked twice per sieve region** (once per side); often not enough survivors to fill batch efficiently.
- **Implementation not fully optimized** (prototype modifications to Cado‑NFS).
- **Speedup modest** (~5% overall projected); not a breakthrough in asymptotic complexity.
- **Requires access to original relations for parameter tuning** (not generalizable without such data).

## Practical conclusions

1. **Sieving large primes is more efficient per hit** than sieving small primes. Small primes can be handled by batch algorithm after sieving.
2. **Disabling the small sieve entirely** (B=17) is viable; the optimal balance is to let batch algorithm find small factors.
3. **For 90% relation retention**, new strategy achieves ~1.10 local speedup; after compensating for extra special‑q, net speedup ≈5% over full factorization.
4. **Further improvements** possible by:
   - Tuning B differently per side.
   - Decoupling batch processing from sieve region boundaries.
   - Exploring more aggressive parameter settings (e.g., 85% retention).

## References (selected)
- Aoki & Ueda (2004) — Bucket sieving
- Bernstein (2002, 2004) — Smooth parts, scaled remainder trees
- Boudot et al. (2020) — RSA‑250 factorization (CRYPTO 2020)
- Bouillaguet & Zimmermann (2021) — Parallel structured Gaussian elimination
- Hildebrand & Tenenbaum (1986) — Smooth number distribution
- Joux (2009) — Algorithmic cryptanalysis textbook
- Kleinjung et al. (2010) — RSA‑768 factorization
- Lenstra et al. (1993) — Development of NFS
- Pollard (1993) — Lattice sieve
- Vallée & Vera (2010) — LLL algorithm analysis
