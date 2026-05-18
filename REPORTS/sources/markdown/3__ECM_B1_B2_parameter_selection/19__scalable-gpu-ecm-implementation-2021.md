---
title: "A High-Performance and Scalable Implementation of the Elliptic Curve Method on Graphics Processing Units"
title_en: "A High-Performance and Scalable Implementation of the Elliptic Curve Method on Graphics Processing Units"
source_type: "conference_paper"
authors: ["Wloka J.", "Richter-Brockmann J.", "Güneysu T.", "Stahlke C.", "Priplata C.", "Kleinjung T."]
year: "2020/2021"
source_link: "https://doi.org/10.1007/978-3-030-65411-5_13"
doi: "10.1007/978-3-030-65411-5_13"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "scalable-gpu-ecm-implementation-2021.md"
---

# Content source: A High-Performance and Scalable Implementation of the Elliptic Curve Method on Graphics Processing Units

## Source type
Conference paper (CT-RSA 2021? Appears in LNCS).

## Authors and affiliations
- Jonas Wloka (DFKI GmbH, Bremen)
- Jan Richter-Brockmann, Tim Güneysu (Ruhr University Bochum, HGI)
- Colin Stahlke, Christine Priplata (CONET Solutions GmbH, Hennef)
- Thorsten Kleinjung (EPFL IC LACAL, Lausanne)

## Objective
Present a highly optimized, scalable GPU implementation of ECM (both stages) supporting arbitrary modulus sizes and ECM parameters (B₁, B₂), with state-of-the-art curve arithmetic (a=−1 twisted Edwards curves, extended coordinates). Achieve record throughput on modern GPUs (RTX 2080 Ti, Tesla V100). Support multi-GPU computation and scale to larger DLP parameters (e.g., B₁=50,000, B₂=5,000,000, 448-bit moduli).

## Key differences from prior GPU ECM implementations

Prior work (Bernstein et al. 2009, Bos & Kleinjung 2012, Miele et al. 2014):
- Fixed parameter sets (limited B₁, modulus size)
- Often only stage 1 on GPU, stage 2 on CPU
- Not scalable to larger DLP parameters

This work:
- **Full ECM (stage 1 + stage 2) on GPU**
- **Scalable to arbitrary B₁, B₂, modulus size** (parameters configurable at compile time)
- **Multi-GPU support** (linear scaling)
- **State-of-the-art modular multiplication** (FIOS, FIPS, CIOS) with PTX assembly
- **Available open source**: https://github.com/Chair-for-Security-Engineering/ecmongpu

## ECM parameters for DLP application (Section 2.2)

For individual discrete logarithm computation in 768- to 1024-bit prime fields:

| Factor size (bits) | B₁ (stage 1) | B₂ (stage 2) |
|-------------------|--------------|--------------|
| 44–80 | ≈7·exp(n/9) | ≈600·exp(0.113·n) |
| (≈ 768-bit DLP) | — | — |
| 1024-bit DLP | 50,000 | 5,000,000 |

## Curve arithmetic (a=−1 twisted Edwards, extended coordinates)

**Point addition (Algorithm 1)** — Hisil et al. 2008, Bernstein & Lange EFD:
- Cost: 9M + 1S + 1d (multiplication by curve constant)
- Input: two points in extended coordinates (X:Y:T:Z)

**Precomputed point format** (for w-NAF table):
- Normalize to Z=1 (cost: 1 inversion + 3 multiplications per point)
- Precompute: x̄ = y−x, ȳ = y+x, z̄ = 1, t̄ = 2d·t
- Addition with precomputed point: **7M** (instead of 9M+1S+1d)

**Doubling** (projective coordinates, no T coordinate):
- Cost: 3M + 4S

**Mixed representation** (Section 4.2, Table 2):
- When addition is followed by doubling, can omit T coordinate from result (saves 1M)
- For consecutive doublings (NAF zero digits), stay in projective coordinates
- Achieves: 3M+4S per doubling, 8M+9S per addition+double pair

## Scalar multiplication (stage 1) — w-NAF

- w = 4 (configurable)
- Scalar s = lcm(1,…,B₁) computed on host, converted to w-NAF
- Precomputed points: {P, 3P, 5P, 7P} (strided in global memory)
- For each digit:
  - If digit = 0: double only
  - If digit > 0: add precomputed point, then double
  - If digit < 0: add negative of precomputed point, then double

**Comparison with double-base chains (Bos & Kleinjung 2012, Table 1)**:

| B₁ | Method | M* | I | trials/s | Notes |
|----|--------|----|---|----------|-------|
| 8192 | Optimal chains (Bernstein 2017) | — | — | — | Too computation-intensive |
| 8192 | 4-NAF | 95,756 | 421 | 5,495 | Baseline |
| 8192 | Random batching | 163,751 | 90 | 3,830 | 30% slower |
| 8192 | Adapted from Bouvier 2018 | 138,565 | 50 | 4,266 | 22% slower |
| 50,000 | 4-NAF | 585,509 | 432 | 2,718 | — |
| 50,000 | Random batching | 225,718 | — | — | Too slow (kernel launches overhead) |

**Conclusion**: 4-NAF with optimized coordinates outperforms batching for large B₁ due to lower kernel launch overhead and better memory locality.

## Stage 2 optimization — baby-step giant-step (Section 3.2)

- Choose giant-step size g (e.g., 2310 for DLP parameters)
- U = {u: 1 ≤ u ≤ g/2, gcd(u,g)=1} (baby steps)
- V = {v: ⌈B₁/g − ½⌉ ≤ v ≤ ⌊B₂/g + ½⌋} (giant steps)
- Precompute points uQ (baby) and vgQ (giant)
- Normalize all points to same Z (batch inversion, 4(|V|+|U|) multiplications)
- Compute m = ∏_{v∈V}∏_{u∈U} (y_{vgQ} − y_{uQ}) with only |V||U| multiplications
- Batch processing if memory limited (GPU global memory)

## Modular multiplication strategies (Section 4.1, Figure 1)

Comparison of CIOS, FIOS, FIPS on different GPU architectures:

| GPU | Architecture | Best strategy | Note |
|-----|--------------|---------------|------|
| Tesla P100 | Pascal | CIOS | Slight advantage |
| Tesla V100 | Volta | FIPS | 2× faster than CIOS for large moduli |
| RTX 2080 Ti | Turing | FIPS | Up to 4× faster than CIOS for 448-bit |

**Throughput (million modular multiplications per second)**:

| Modulus | Tesla P100 (CIOS) | Tesla V100 (FIPS) | RTX 2080 Ti (FIPS) |
|---------|-------------------|-------------------|---------------------|
| 128-bit | 1,250? (table 5 gives scaled values) | ~2,900? | ~5,400? |
| 256-bit | ~700 | ~2,500 | ~4,500 |
| 384-bit | ~450 | ~1,600 | ~2,900 |

## ECM stage 1 throughput (B₁=8192, Table 3)

| Modulus (bits) | Tesla P100 | Tesla V100 | RTX 2080 Ti | 2×RTX 2080 Ti |
|----------------|------------|------------|-------------|---------------|
| 128 | 103.9 k/s | 228.9 k/s | 450.6 k/s | 542.6 k/s |
| 192 | 46.8 k/s | 149.1 k/s | 214.1 k/s | 377.1 k/s |
| 256 | 19.0 k/s | 117.6 k/s | 124.2 k/s | 232.9 k/s |
| 320 | 14.3 k/s | 73.4 k/s | 98.9 k/s | 191.4 k/s |
| 384 | 8.3 k/s | 35.4 k/s | 37.2 k/s | 73.0 k/s |
| 448 | 5.2 k/s | 24.7 k/s | 24.7 k/s | 48.2 k/s |

**Observation**: RTX 2080 Ti ≈ 1.4–2× faster than Tesla V100 for smaller moduli (<256 bits), but similar for larger moduli.

## Full ECM (stage 1+2) throughput (B₁=50,000, B₂=5,000,000, Table 4)

| Modulus (bits) | Tesla P100 | Tesla V100 | RTX 2080 Ti | 2×RTX 2080 Ti |
|----------------|------------|------------|-------------|---------------|
| 128 | 10.8 k/s | 46.9 k/s | 40.9 k/s | 80.5 k/s |
| 192 | 4.97 k/s | 22.85 k/s | 20.21 k/s | 39.42 k/s |
| 256 | 2.11 k/s | 13.58 k/s | 11.62 k/s | 22.51 k/s |
| 320 | 1.42 k/s | 7.99 k/s | 9.34 k/s | 17.91 k/s |
| 384 | 0.77 k/s | 4.60 k/s | 4.11 k/s | 7.89 k/s |
| 448 | 0.55 k/s | 2.78 k/s | 2.78 k/s | 5.39 k/s |

**For 448-bit moduli (1024-bit DLP individual log): 2,780–5,390 trials/s on RTX 2080 Ti**.

## Comparison with prior ECM implementations (Tables 5–6)

### Modular multiplication throughput (scaled per core·cycle, 10⁻³)

| Work | GPU | 128-bit | 256-bit | 384-bit |
|------|-----|---------|---------|---------|
| Leboeuf 2013 | GTX 580 | 3.54 | 1.53 | 0.76 |
| Miele 2014 | GTX 580 | 6.34 | 1.88 | 0.85 |
| Emmart 2016 | GTX 980 Ti | 19.03 | 1.33 | — |
| **This work (FIPS)** | **RTX 2080 Ti** | **>100** | **~45** | **~20** |

**Observation**: Modern GPUs with FIPS strategy achieve >30× higher throughput per core·cycle than 2014 implementations.

### ECM stage 1 throughput (B₁=960, 192-bit, scaled per core·cycle, 10⁻⁵)

| Work | GPU | Throughput | Ratio (vs our) |
|------|-----|------------|----------------|
| Bos & Kleinjung 2012 (no-storage) | GTX 580 | 2.17 | 4.4× slower |
| Bos & Kleinjung 2012 (windowing) | GTX 580 | 1.00 | 9.5× slower |
| **This work** | **RTX 2080 Ti** | **9.53** | **1.0×** |

### ECM stage 1 throughput (B₁=8192, 192-bit)

| Work | Throughput (scaled) | Factor |
|------|---------------------|--------|
| Bos & Kleinjung 2012 (no-storage) | 0.25 | 0.85× slower |
| Bos & Kleinjung 2012 (windowing) | 0.12 | 1.75× slower |
| **This work (RTX 2080 Ti)** | **0.29** | **1.0×** |

Note: For B₁=8192, our w=4 NAF with optimized coordinates is slightly faster than Bos & Kleinjung's no-storage chains (which required 40 core-years precomputation).

## Application: DLP individual logarithm acceleration (Section 2.2)

**Problem**: Individual discrete logarithm in 768-bit prime field took 2 core-days on 100 CPU cores. With GPUs, reduced to 2 minutes.

**Our contribution**: For 1024-bit DLP individual logs, 448-bit cofactors after trial division need ECM with B₁=50,000, B₂=5,000,000. Our GPU implementation processes 2,780 trials/s on RTX 2080 Ti, enabling significant speedup.

**Cost estimate for DLP database precomputation** (from paper):
- 768-bit: $10⁶ per year (CPUs)
- 1024-bit: $10⁹ per year (CPUs)
- 1536-bit: ≥$10¹⁴ per year (CPUs)

GPUs could substantially reduce these costs.

## Strengths

1. **First open-source, scalable GPU ECM** (both stages) with configurable parameters.
2. **State-of-the-art throughput**: 214k trials/s for B₁=8192, 192-bit moduli on RTX 2080 Ti.
3. **Multi-GPU support** with near-linear scaling.
4. **Modular multiplication** optimized for modern GPU architectures (FIPS best on Volta/Turing).
5. **Practical DLP acceleration** demonstrated (1024-bit individual logs from 1 hour to minutes with GPUs).

## Limitations (explicit)

1. **4-NAF is not optimal** for small B₁ (B₁<4096) — batching/addition chains would be better but not implemented.
2. **Stage 2 batch normalization** requires large memory; for B₂=5M, g=2310 → |U|=240 baby steps, |V|≈B₂/g≈2164 giant steps → total ~4800 points × 4 coordinates × 448 bits = ~10 MB per batch, fits in GPU memory but limits concurrency.
3. **Precomputed points for w-NAF** stored in global memory (not shared/registers) due to limited shared memory.
4. **Power consumption not measured** (only throughput).
5. **Comparison with prior work** uses scaled metrics (per core·cycle) due to different hardware, not wall-clock on same platform.
6. **No side-channel resistance** (not relevant for cryptanalysis).

## Relation to other work

- Builds on Bernstein et al. (EUROCRYPT 2009) — first ECM on GPUs (stage 1 only).
- Extends Miele et al. (CHES 2014) — full ECM on GPU with stage 2.
- Improves Bos & Kleinjung (ASIACRYPT 2012) — addition chains; replaces with w-NAF for scalability.
- Modular multiplication comparison: Koc et al. (IEEE Micro 1996), Neves & Araujo (ASAP 2011).
- Twisted Edwards curves: Bernstein et al. (AFRICACRYPT 2008), Hisil et al. (ASIACRYPT 2008).
- DLP records: Kleinjung et al. (EUROCRYPT 2017), Boudot et al. (2020).
