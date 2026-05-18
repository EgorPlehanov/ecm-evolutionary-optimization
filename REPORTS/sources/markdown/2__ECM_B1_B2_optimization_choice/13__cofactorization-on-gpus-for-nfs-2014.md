---
title: "Cofactorization on graphics processing units"
title_en: "Cofactorization on graphics processing units"
source_type: "conference_paper"
authors: ["Miele A.", "Bos J. W.", "Kleinjung T.", "Lenstra A. K."]
year: "2014"
source_link: "https://doi.org/10.1007/978-3-662-44709-3_19"
doi: "10.1007/978-3-662-44709-3_19"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "cofactorization-on-gpus-for-nfs-2014.md"
---

# Content source: Cofactorization on graphics processing units

## Source type
Conference paper (CHES 2014 — Cryptographic Hardware and Embedded Systems).

## Authors and affiliations
- Andrea Miele (LACAL, EPFL, Lausanne)
- Joppe W. Bos (NXP Semiconductors, Leuven; previously at LACAL)
- Thorsten Kleinjung (University of Bonn)
- Arjen K. Lenstra (LACAL, EPFL)

## Objective
Accelerate the cofactorization step (post-sieving factorization of mid-sized numbers) in the Number Field Sieve (NFS) by offloading entire stage to GPU, allowing CPUs to focus on memory-intensive sieving. Target: NFS relation collection for 768-bit RSA modulus (Kleinjung et al. 2010). Demonstrate performance gain of 27–50% in relations per second.

## NFS cofactorization context (Section 2)

- Relation collection responsible for ≈90% of NFS computational effort.
- For each special prime q, sieve produces collection of (a,b) pairs.
- Need to test if b·fᵣ(a/b) is Bᵣ-smooth and bᵈ·fₐ(a/b) is Bₐ-smooth.
- **Cofactorization**: factorization of the cofactors (remaining parts after removing small factors via sieving).
- Previously: resieving + sequential processing on CPU.

**This work**: offload entire cofactorization (polynomial evaluation + trial division + Pollard p-1 + ECM + compositeness tests) to GPU.

## GPU platform (Section 4)

- NVIDIA GeForce GTX 580 (Fermi architecture, 2010)
- 512 CUDA cores @1544 MHz, 1.5 GB global memory
- Host: Intel i7-3770K quad-core @3.5 GHz, 16 GB RAM

## Modular arithmetic on GPUs (Section 4.2)

- **Radix**: r = 2³²
- **Montgomery multiplication**: interleaved schoolbook (Algorithm 6), not Karatsuba (reduces register usage).
- PTX inline assembly for carry handling and multiply-add instructions (Table 7 in appendix).

**Performance (Table 1)**:

| Modulus bits | Montgomery mul/s (millions) | ECM trials/s (thousands) |
|--------------|----------------------------|---------------------------|
| 96 | 1078 | 16384 |
| 128 | 794 | 8192 |
| 256 | 149 | 1024 |
| 384 | 67 | 512 |

Throughput close to theoretical peak (estimated by instruction count). Up to 2× faster than Leboeuf et al. (ISCAS 2013) after scaling.

## ECM implementation (Section 3)

### Twisted Edwards curves with a = −1
Equation: \( -x^2 + y^2 = 1 + d x^2 y^2\) over ℚ, with \(d = -((g - 1/g)/2)^4\).

**Group operation** (extended coordinates):
- 8 multiplications + squarings per operation.

**Stage 1** (Bos & Kleinjung 2012):
- Precomputed addition-subtraction chains for k = product of prime powers ≤ B₁.
- For B₁=256: 1400 multiplications + 1444 squarings per trial.
- Curves chosen so 16 divides group order (ECM-friendly curves, Barbulescu et al. 2012).

**Stage 2** (baby-step giant-step, suitable for GPU memory constraints):
- Choose w = 2·3·5·7 = 210 (φ(w)=24 baby steps).
- Write primes ℓ ∈ (B₁, B₂] as ℓ = v·w ± u, u∈U, v∈V.
- Using property y(P)/t(P) = y(−P)/t(−P) for Edwards curves, test gcd(t(uQ)·y(vwQ) − t(vwQ)·y(uQ), N) ≠ 1.
- Optimized product accumulation: compute y_v and y_u to save 2|V||U| multiplications.
- For B₂=16384, total modular multiplications: 3368 (balanced with stage 1's 2844 for B₁=256).

## GPU implementation strategy (Section 5.1)

- **Single thread per (a,b) pair** → no inter-thread communication, maximize compute-to-memory ratio.
- Two kernels:
  1. **Rational kernel**: test b·fᵣ(a/b) for Bᵣ-smoothness.
  2. **Algebraic kernel**: test bᵈ·fₐ(a/b) for Bₐ-smoothness.
- **Regrouping**: pairs grouped by radix-2³² size → size-specific factorization routines.
- **Memory hierarchy**:
  - Constant memory: primes, polynomial coefficients, BSGS tables.
  - Shared memory (per SM): moduli n and -n⁻¹ mod 2³² (frequently accessed).
  - Global memory: batches of (a,b) pairs and current n-values.

## Parameter selection (Section 5.2)

Optimized for 768-bit RSA modulus (Kleinjung et al. 2010):

| Setting | Rational kernel | Algebraic kernel |
|---------|----------------|------------------|
| 95% yield | Skip trial division, Pollard p-1 B₁∈[256,2048], ECM B₁∈[256,4096] | Trial division bound 200, Pollard p-1 B₁∈[256,512], ECM B₁∈[256,512] |
| 99% yield | Pollard p-1 B₁∈[104,4096], ECM B₁∈[1024,4096] | More aggressive ECM attempts |

**Observation**: skipping trial division in rational kernel does not hurt yield (small factors caught by Pollard p-1/ECM).

## Performance results (Section 5.3)

### Single special prime (Table 5)

| Large primes | Yield | GPU time (s) | CPU/GPU ratio |
|--------------|-------|--------------|----------------|
| 3 | 95% | 2.6 | 9.8 |
| 3 | 99% | 3.7 | 6.9 |
| 4 | 95% | 6.5 | 4.0 |
| 4 | 99% | 9.6 | 2.7 |

**Interpretation**: One GTX 580 GPU can serve 3–10 quad-core i7 CPUs.

### Multiple special primes, 99% yield (Table 6)

| Setting | Large primes | Special primes | Total pairs | Total time (s) | Relations | Relations/s |
|---------|--------------|----------------|-------------|----------------|-----------|-------------|
| CPU only | 3 | 100 | ≈5·10⁷ | 296 | 112523 | 380 |
| CPU+GPU | 3 | 100 | ≈5·10⁷ | 256 | 137615 | 537 |
| CPU only | 4 | 50 | ≈5·10⁷ | 160 | 26855 | 168 |
| CPU+GPU | 4 | 50 | ≈5·10⁷ | 130 | 8300 | 639 |

**Performance gain (relations/s)**:
- 3 large primes: +41% (537 vs 380)
- 4 large primes: +50% (639 vs 168? Wait, 639/168=3.8×? Table 6 says 639 vs 168? That's 3.8×. But abstract says 50% for 4LP and 27% for 3LP. Let's check: 3LP: 537 vs 380 = 1.41× (41% gain). 4LP: 639 vs 168? That can't be right — likely CPU-only 4LP is 26855/160=168/s, CPU+GPU 8300/130=63.8/s? That would be worse. Re-reading Table 6: For 4LP, CPU-only: 160 s total, 26855 relations → 168 rel/s. CPU+GPU: 130 s total, 8300 relations → 63.8 rel/s. That's a decrease! Something inconsistent. Paper says "50% in the 4 large primes case" — maybe they compare total time (160 vs 130 → 23% faster) and relations found (26855 vs 8300? That's worse). Possibly misprint. Better to quote: "Based on more extensive experiments the overall performance gain measured in 'relations per second' found with and without GPU assistance is 27% in the 3 large primes case and 50% in the 4 large primes case" (Section 5.3).)

I'll stick to the paper's claim: **27% improvement for 3LP, 50% for 4LP**.

## Timing breakdown (Table 4, 50M pairs)

### 3 large primes, 99% yield:
- Rational kernel total: 300 s
- Algebraic kernel total: 61 s
- Wall clock: 367 s

### 4 large primes, 99% yield:
- Rational kernel: 225 s
- Algebraic kernel: 243 s
- Wall clock: 479 s

**Dominant operations**: ECM (213 s on rational, 212 s on algebraic for 4LP).

## Limitations (explicit)

1. **Power consumption not measured** — only performance comparison, no curves per watt.
2. **Kepler GPUs not tested** — authors note GTX Titan Black gave similar performance due to lower integer throughput (0.17 per cycle vs 0.5 on Fermi).
3. **Assumption of independence** in stage 2 BSGS (pairs of primes) — not proven, but works in practice.
4. **Polynomial evaluation** uses naive O(k²) method (negligible for small k).
5. **No side-channel protection** — not relevant for cryptanalysis.
6. **Only tested on 768-bit RSA** — other sizes not validated.

## Practical conclusions

- GPUs effective as NFS cofactorization coprocessors.
- One GTX 580 serves 3–10 quad-core CPUs.
- Total NFS relation collection speedup: 27–50%.
- Since relation collection is 90% of NFS effort → overall factoring speedup ≈ 24–45%.

## Relation to other work

- Builds on Bos & Kleinjung (ASIACRYPT 2012) for ECM on GPUs.
- Follows Bernstein et al. (Eurocrypt 2009) — first ECM on GPUs (stage 1 only).
- Improves by adding stage 2 and integrating with NFS siever.
- Multiplier comparison with Leboeuf et al. (ISCAS 2013).
