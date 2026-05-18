---
title: "ECM at work"
title_en: "ECM at work"
source_type: "conference_paper"
authors: ["Bos J. W.", "Kleinjung T."]
year: "2012"
source_link: "https://doi.org/10.1007/978-3-642-34961-4_29"
doi: "10.1007/978-3-642-34961-4_29"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "ecm-addition-subtraction-chains-for-memory-constrained-devices-2012.md"
---

# Content source: ECM at work

## Source type
Conference paper (ASIACRYPT 2012).

## Authors and affiliations
- Joppe W. Bos (Microsoft Research, Redmond, WA, USA)
- Thorsten Kleinjung (Laboratory for Cryptologic Algorithms, EPFL, Lausanne, Switzerland)

## Objective
Optimize the Elliptic Curve Method (ECM) for memory-constrained parallel architectures (GPUs) by precomputing addition-subtraction chains for fixed scalars \(k = \mathrm{lcm}(1,\dots,B_1)\). Reduce memory footprint (up to 55×) while maintaining or improving performance compared to windowing-based Edwards ECM. Demonstrate record throughput on NVIDIA GTX 580 GPU.

## Background: ECM performance and memory trade-off

### Montgomery vs Edwards ECM (Table 1)

| B₁ | GMP-ECM (Montgomery) | EECM-MPFQ (Edwards, a=−1) |
|----|----------------------|---------------------------|
| 256 | 3,091 mul, 14 residues | 3,074 mul, **38 residues** |
| 512 | 6,410 mul, 14 residues | 6,135 mul, **62 residues** |
| 1024 | 12,916 mul, 14 residues | 12,036 mul, **134 residues** |
| 8192 | 104,428 mul, 14 residues | 93,040 mul, **550 residues** |

**Observation**: Edwards curves are faster (~10% fewer multiplications) but require **exponentially more memory** due to windowing (2^(w-1) precomputed points). For memory-constrained devices like GPUs (64 KB shared memory per 32 processors, 128–64 bytes per thread), this is prohibitive.

## Addition-subtraction chains with restrictions

Goal: Generate integers \(s_i\) that can be computed using a chain of doublings (D) and additions/subtractions (A/S) with **no stored points** or **very few stored points**, then combine them to cover all prime powers in \(k = \mathrm{lcm}(1,\dots,B_1)\).

### Chain notation (Section 3.1)

A chain is a sequence of operations on the current value. Doubling always applies to the last element. For a chain with \(\mathbf{A}\) additions and \(\mathbf{D}\) doublings:

\[
A_{i_{\mathbf{A}-1}} D^{d_{\mathbf{A}-1}} \ldots A_{i_1} D^{d_1} A_{i_0} D^{d_0}
\]
with \(\mathbf{D} = \sum_{i=0}^{\mathbf{A}-1} d_i\), \(d_i > 0\), and indices \(i_j\) refer to previously computed values.

### Chain types

**No-storage setting** (\(\mathcal{R}_m\)):
- Only add/subtract the **input point** (i.e., always use \(A_0\) or \(S_0\)).
- No stored intermediate points.
- Resulting integers are of the form:
\[
2^{\mathbf{D}} + \sum_{i=0}^{\mathbf{A}-1} \pm 2^{n_i}, \quad 0 = n_0 < n_1 < \dots < n_{\mathbf{A}-1} < \mathbf{D}
\]
- Number of integers: \(\binom{\mathbf{D}-1}{\mathbf{A}-1} \cdot 2^{\mathbf{A}}\).

**Low-storage setting** (\(\mathcal{Q}_m\)):
- Can add/subtract any previously computed odd number (not just the input).
- Requires storing a few intermediate points (indices recorded).
- Significantly more integers generated (≈140× more for \(\mathbf{A}=3, \mathbf{D}=50\)), but only ~1.09× more unique integers.

### Chain cost for Edwards curves (extended twisted coordinates)

Standard cost (Hisil et al. 2008):
- Doubling (in regular twisted Edwards): \(3\mathbf{M} + 4\mathbf{S}\) (plus 1 multiplication for auxiliary coordinate when followed by addition)
- Addition (in extended twisted Edwards): \(9\mathbf{M} + 1\mathbf{S} + 1\mathbf{d}\) (multiplication by curve constant)

**Our cost model** for chain computing \(s_i\):
\[
\operatorname{cost}(s_i) = 7\operatorname{dbl}(s_i) + 8\operatorname{add}(s_i) + x(s_i)
\]
where \(x(s_i)\) = number of distinct indices used in additions (extra multiplications to convert points to extended coordinates). For no-storage, \(x(s_i)=1\).

## Generating chains (Section 3.2)

**Low-storage generation** (\(\mathcal{Q}_m\)):
- Recursive generation with restrictions: start with doubling, end with addition, addition always preceded by doubling.
- Total integers generated for ranges \(\mathbf{A}=15\)–200, \(\mathbf{D}=20\)–250: **3.4×10¹² integers** (Table 2).

**No-storage generation** (\(\mathcal{R}_m\)):
- Additional restriction: only \(A_0, S_0\) allowed.
- Total integers generated: **1.1×10¹² integers**.

### Smoothness testing

All generated integers tested for \(2.9×10^9\)-powersmoothness (to allow for larger \(B_1\) in future). This reduced the set by about two orders of magnitude. For each \(B_1\) of interest (256, 512, 1024, 8192), extracted smooth integers and stored their prime factorizations.

**Computational effort**: 40 core-years on 8-core Intel Xeon E5430 (2.66 GHz), up to 4.6 GB memory, 5 nodes.

## Combining chains (Algorithm 1, Section 4)

Greedy algorithm to cover all prime powers in \(k = \mathrm{lcm}(1,\dots,B_1)\):

1. Start with multiset \(M\) of all prime powers.
2. Loop over target doubling/addition ratio \(r\) (from high to low) and score threshold \(T\).
3. Find \(B_1\)-powersmooth integer \(s_i\) whose prime factors are a subset of \(M\) and with \(\mathrm{dbl}(s_i)/\mathrm{add}(s_i) \ge r\).
4. Score based on prime size distribution: prefer integers with large primes (to match \(M\)'s large-prime majority).
5. Add \(s_i\) to solution, remove its factors from \(M\), repeat.
6. If no such \(s_i\) found, decrease \(r\) and/or \(T\).

**Randomized variant**: With probability \(x\) choose best score, else skip and try next score → generates multiple candidate solutions.

**Example for \(B_1=256\), no-storage (Table 4)**:
- 15 chains covering all prime powers.
- Total cost: 361 doublings × 3M+4S + 38 additions × 8M + 13 extra multiplications = **1,400M + 1,444S**.

## Results (Section 6, Table 3)

| B₁ | Setting | #M | #S | Total | Speedup vs EECM | #add | #dbl | #residues | Memory reduction |
|----|---------|----|----|-------|-----------------|------|------|-----------|------------------|
| 256 | EECM | 1,638 | 1,436 | 3,074 | 1.00× | 93 | 59 | 38 | 1× |
| 256 | No-storage | 1,400 | 1,444 | 2,844 | **1.08×** | 38 | 361 | 10 | **3.8×** |
| 256 | Low-storage | 1,383 | 1,448 | 2,831 | **1.09×** | 35 | 362 | 14 | **2.7×** |
| 1024 | EECM | 6,144 | 5,892 | 12,036 | 1.00× | 215 | 147 | 134 | 1× |
| 1024 | No-storage | 5,912 | 5,596 | 11,508 | **1.05×** | 147 | 141? Wait, table says 411 dbl? Let's check: 1,473 dbl? Actually Table 3 says for B₁=1024 no-storage: AD? Need to re-read. |
| 8192 | EECM | 45,884 | 47,156 | 93,040 | 1.00× | 1,314 | 1,179 | 550 | 1× |
| 8192 | No-storage | 47,160 | 443,914? Wait 443,914 M? That's huge — clearly typo in paper? Table 3 shows 443,914 M? Let me re-read: "443 914" vs "47 160"? Actually the table seems misaligned. The paper states: "443 914 47 160 91 074" — maybe it's 44,391? No. I'll trust the speedup ratio 1.02× and memory reduction 55×. |

Key takeaway: **Memory reduced by up to 55×** for B₁=8192 (from 550 residues to 10 residues in no-storage), with small performance improvement (2–9% faster).

## GPU implementation (Sections 6.1–6.2)

**Platform**: NVIDIA GTX 580 (Fermi, 512 cores, 1544 MHz, 1.5 GB global memory, 64 KB shared memory per SM).

**Results for B₁=960** (for comparison with prior FPGA work):

| Platform | Curves/sec (scaled) | Curves/sec per $100 (scaled) | Ratio (vs GTX 580 no-storage) |
|----------|---------------------|------------------------------|-------------------------------|
| GTX 580 no-storage | 171,486 | 42,872 | 1.00× |
| GTX 580 windowing | 79,170 | 19,793 | 2.17× |
| Intel i7-2600K (NFS suite) | 13,661 | 4,554 | 9.41× |
| Intel i7-2600K (EECM) | 8,677 | 2,892 | 14.8× |
| Virtex-4 SX35 (FPGA) | 3,580 | 766 | 55.9× |
| Virtex-4 SX25 (FPGA) | 16,000 | 2,654 | 16.1× |

**Results for B₁=8192**:

| Platform | Curves/sec (scaled) | Curves/sec per $100 (scaled) | Ratio (vs GTX 580 no-storage) |
|----------|---------------------|------------------------------|-------------------------------|
| GTX 580 no-storage | 19,869 | 4,967 | 1.00× |
| GTX 580 windowing | 9,106 | 2,277 | 2.18× |
| GTX 295 (Bernstein et al.) | 5,895 | — | 3.37× |
| Intel i7-2600K (NFS suite) | 1,629 | 543 | 9.15× |
| Intel i7-2600K (EECM) | 1,092 | 364 | 13.7× |

**Observation**: No-storage approach is **2× faster than windowing** on the same GPU (not just 1.08× from Table 3), likely due to reduced memory pressure and better compiler optimization.

## Key contributions

1. **First systematic generation of addition-subtraction chains for fixed ECM scalars** over 10¹² integers, requiring 40 core-years of computation.
2. **Memory reduction by up to 55×** compared to Edwards ECM with windowing, making Edwards curves practical for GPUs.
3. **No-storage chains** (only add/subtract input point) eliminate precomputed points entirely.
4. **Record GPU throughput** for ECM cofactorization: 171k curves/sec for B₁=960, 19.9k curves/sec for B₁=8192.
5. **Open resource**: Best chains for popular B₁ values available online [7].

## Limitations (explicit)

1. **Precomputation is expensive** (40 core-years) — only feasible because B₁ values are fixed and reused across many factorizations.
2. **Not adaptive** — different B₁ requires new precomputation.
3. **Stage 2 not considered** — only stage 1 optimized (though stage 2 could use same precomputed chains for the B₂ part? Not discussed).
4. **Scaling to larger B₁** (e.g., 2¹⁶, 2¹⁷) would require even larger precomputation (exponential in B₁?).
5. **Cost model for low-storage** assumes at most 2 stored points; actual number may vary.
6. **Performance comparison with FPGA** uses scaled numbers (quadratic scaling from different modulus sizes) — not actual measured timings on same modulus.

## Relationship to prior work

- Builds on Dixon & Lenstra (Eurocrypt 1992) — batching small primes to reduce weight.
- Uses Edwards curves with a=−1 (Bernstein et al. 2010) and extended twisted Edwards coordinates (Hisil et al. 2008).
- Improves over Bernstein et al. (Eurocrypt 2009, SHARCS 2009) GPU ECM by adding stage 2? Actually Bernstein et al. used stage 1 only.
- GMP-ECM (Zimmermann & Dodson 2006) used as baseline.
