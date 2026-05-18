---
title: "On the Analysis of Public-Key Cryptologic Algorithms"
title_en: "On the Analysis of Public-Key Cryptologic Algorithms"
source_type: "phd_thesis"
authors: ["Miele A."]
year: "2015"
source_link: "https://infoscience.epfl.ch/record/208187"
doi: "none"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "analysis-of-public-key-cryptologic-algorithms-thesis-2015.md"
---

# Content source: On the Analysis of Public-Key Cryptologic Algorithms (PhD Thesis)

## Source type
Doctoral dissertation, EPFL, May 2015. Advisor: Prof. Arjen K. Lenstra.

## Core contributions

This thesis addresses four main problems in public-key cryptanalysis and cryptography:

1. **GPU acceleration of NFS cofactorization** – speeding up the relation collection step of the Number Field Sieve using NVIDIA GPUs.
2. **Practical security analysis of elliptic and hyperelliptic curves** – evaluating Pollard rho with automorphism speedups for curves with m=2,6 (genus 1) and m=2,10 (genus 2).
3. **FPGA architecture for ECDLP** – many-core design for Pollard rho with negation map, targeting Certicom ECCp-131 challenge.
4. **Ephemeral ECC parameter generation** – real-time generation of unique, secure ECC parameters using CM method with class numbers ≤3.

---

## Chapter 3: Cofactorization on GPUs

### Objective
Accelerate the post-sieving (cofactorization) step of NFS — responsible for ~90% of factoring effort for 768-bit RSA — by offloading to GPUs.

### Method
- Process each (a,b) pair independently in a single CUDA thread (no inter-thread sync).
- Rational kernel: test b·f_t(a/b) for B_t-smoothness using trial division, Pollard p-1, ECM.
- Algebraic kernel: test b^d·f_a(a/b) for B_a-smoothness.
- ECM implementation: twisted Edwards curves (a=-1) with extended coordinates; stage 2 uses baby-step giant-step (BSGS) optimized for GPU memory constraints.

### GPU Implementation Highlights
- Radix r = 2³², Montgomery multiplication (Algorithm 14) using PTX inline assembly.
- Memory hierarchy: constants in constant memory, moduli in shared memory, pairs in global memory.
- No parallel integer arithmetic (one thread per pair) to maximize compute-to-memory ratio.
- ECM stage 2: BSGS with w = 2·3·5·7, 24 tabulated baby steps, B₂ up to 16384.

### Performance Results (NVIDIA GTX 580, 512 cores @1544 MHz)

| Modulus bits | Montgomery mul/s (millions) | ECM trials/s (thousands) |
|--------------|----------------------------|---------------------------|
| 96           | 1078                       | 16384                     |
| 128          | 794                        | 8192                      |
| 256          | 149                        | 1024                      |
| 384          | 67                         | 512                       |

### Integration with NFS
- Single GPU can serve multiple quad-core CPUs.
- For 4-large-prime setting: 50% performance gain in relations per second.
- For 3-large-prime setting: 27% gain.

### Limitations
- Independence of curves in ECM stage 2 assumed, not proven.
- Performance on Kepler GPUs (GTX Titan Black) similar to Fermi due to lower per-core integer throughput.
- Power consumption not measured.

---

## Chapter 4: Elliptic and Hyperelliptic Curves — Practical Security Analysis

### Objective
Quantify practical speedup of Pollard rho using automorphisms (negation map, higher-order automorphisms) for curves at ~128-bit security level.

### Target Curves

| Curve | Genus | #Aut (m) | Field size | Group order |
|-------|-------|----------|------------|-------------|
| NIST P-256 | 1 | 2 | 256-bit | 256-bit prime |
| BN254 | 1 | 6 | 254-bit | 254-bit prime |
| Generic1271 | 2 | 2 | 127-bit | 254-bit prime |
| 4GLV127-BK | 2 | 10 | ~127-bit | 254-bit prime |

### Methodology
- Affine coordinates with Montgomery simultaneous inversion (2048 concurrent walks).
- Cycle reduction: 2-cycle avoidance with second lookup table (probability ~1/(2r³)).
- Cycle detection: every α steps, check β=32 previous points; escape by doubling representative.
- Parameters: r=1024 for automorphism walks, r=32 for baseline.

### Results

| Curve | Cycles/step (baseline) | Cycles/step (aut) | Expected speedup | Actual speedup | Core-years for DLP | Security vs P-256 |
|-------|------------------------|-------------------|------------------|----------------|--------------------|-------------------|
| NIST P-256 | 1129 | 1185 | √2 ≈ 1.414 | 0.947√2 | 3.95·10²⁴ | baseline (128-bit) |
| BN254 | 1030 | 1296 | √6/0.857 ≈ 2.86 | 0.790√6 | 9.49·10²³ | ~127.6-bit |
| Generic1271 | 986 | 1043 | √2 | 0.940√2 | 1.74·10²⁴ | ~127.0-bit |
| 4GLV127-BK | 1398 | 1765 | √10·(120/150)⁻¹ ≈ 3.53 | 0.784√10 | 1.31·10²⁴ | ~126.5-bit |

### Key Findings
- Theoretical √m speedup not achieved in practice (overhead of representative computation, fruitless cycles).
- BN254 (m=6) achieves ~2.26× speedup vs baseline (not 2.45×).
- Larger automorphism groups give diminishing returns due to higher representative cost.
- All four curves provide 126.5–128 bits of practical security.

---

## Chapter 5: FPGA Architecture for ECDLP (ECCp-131)

### Objective
Design many-core FPGA architecture for parallel Pollard rho with negation map, estimate cost to solve Certicom ECCp-131 challenge (131-bit prime field).

### Architecture
- **SPMW core** (Single-Pipeline Multi-Walk): interleaves multiple walks in one pipeline.
- Operations: addition/subtraction (1 cycle), Montgomery multiplication (k cycles), inversion (2k cycles).
- **Pipeline unrolling**: replicate inversion and multiplication modules to reduce t_max from 2k to ⌈k/u⌉.
- Throughput: TP = 1/(⌈k/u⌉ + 1) points/cycle; N_cores = floor(A_max / A_SPMW).
- Lookup tables T-WALK and T-RED shared among t_max+1 cores via time-division.

### Target: Certicom ECCp-131
- Prime size: 131 bits (k=131).
- Operating frequency (Virtex-7 xc7v2000t): 192 MHz.
- Parameters: u=14 unrolling, N_s=78 stages, N_SPMW=11 cores, N_tables=2.

### Comparison with Prior Work

| Work | Device | Frequency | Points/cycle | Relative speedup |
|------|--------|-----------|--------------|------------------|
| Judge et al. (2012) | Virtex-5 vxs240t | 100 MHz | 1/114 | baseline |
| Our SPMWopt | Virtex-5 vxs240t | 125 MHz | 1/14 | **4.80×** |
| Güneysu et al. (2008) | Spartan-3 xc3s5000 | 40 MHz | 1/855 | baseline |
| Our SPMWopt | Spartan-3 xc3s5000 | 48 MHz | 1/41 | **3.93×** |

### Cost Estimate for ECCp-131
- Expected points needed: ~√(q·π/4) ≈ 2⁶⁵·⁵.
- On Virtex-7: 1.1·10⁹ points/sec → 1.3·10¹⁷ years for one FPGA.
- With 10⁶ FPGAs (cluster): ~130 years.

### Limitations
- Cycle detection/escape handled by host (not on FPGA).
- No SIMD or DSP48 use (pure logic).
- Assumes generic prime fields (no special-form optimizations).

---

## Chapter 6: Efficient Ephemeral ECC Parameter Generation

### Objective
Generate unique, unpredictable ECC parameters on-the-fly (50ms on smartphone) for one-time use, avoiding trust in fixed standards.

### Method: Complex Multiplication (CM) with small class numbers
- Use imaginary quadratic fields Q(√-d) with class number h₋d ≤ 3.
- Precomputed curves for d = 3,7,8,11,19,43,67,163 (h=1) and d = 91,115,187,235,403,427,51,123,267,35,243 (h=2–3).
- For given (u,v) with 4p = u² + d·v², curve order #E(F_p) = p + 1 ± s·u.
- Sieve over (u,v) pairs to quickly find prime p with #E(F_p) prime (or almost prime).

### Sieving Improvement vs. Lenstra (1999)
- Sieve with small primes ζ ∈ P to eliminate (u,v) where p or #E has small factors.
- 16 discriminants checked simultaneously using bitmask sieve.
- Montgomery-friendly primes (p ≡ -1 mod 2⁶⁴) supported.

### Performance Results (128-bit security)

| Platform | Generation type | Time (ms) | Parameters |
|----------|----------------|-----------|------------|
| x86 (2.7GHz i7) | not twist-secure | 7.8–8.8 | 1000 runs |
| x86 | twist-secure | 143–180 | 10000 runs |
| ARM (Samsung S4, 1.9GHz) | not twist-secure | 44–50 | 3000 runs |
| ARM | twist-secure | 1270–1430 | 3000 runs |

- Key reconstruction: ~0.3ms (x86), ~1.7ms (ARM).
- Twist-secure generation ~20× slower than non-twist-secure.

### Security Criteria (vs. SafeCurves)
| Criterion | Our method | SafeCurves requirement | Acceptable? |
|-----------|------------|------------------------|--------------|
| Pollard rho | 2k-bit prime subgroup | N/A | ✓ |
| Transfers (embedding degree) | avoided by construction | ✓ | ✓ |
| CM discriminant | small (≤163) | ≥2¹⁰⁰ | ✗ (but no known attack) |
| Rigidity | transparent, user-controlled | N/A | ✓ |
| Twist security | optional (costly) | recommended | optional |
| Completeness | via Edwards/Montgomery conversion | recommended | ✓ |

### Practical Conclusion
- Acceptable for Diffie-Hellman key agreement where parameters are used once.
- Does not meet SafeCurves discriminant requirement, but no known exploit.
- Extension to genus 2 hyperelliptic curves proposed as future work.

---

## Summary of Contributions

| Contribution | Platform | Key Result |
|--------------|----------|------------|
| NFS cofactorization | GPU (CUDA) | 50% speedup for 4LP setting |
| Pollard rho with automorphisms | x86-64 | √6 gives ~2.26×, not 2.45× |
| ECDLP hardware accelerator | FPGA (Virtex-7) | 4.8× faster than prior art |
| Ephemeral ECC parameters | ARM (Samsung S4) | 50ms for 128-bit security |

---

## Limitations (Explicit)

- **GPU work**: Power consumption not measured; Kepler GPUs show no improvement due to lower integer throughput.
- **Pollard rho**: Independence of walks for automorphism optimization is heuristic; cycle reduction probability analysis assumes uniform distribution.
- **FPGA**: Cycle detection/escape offloaded to host; no DSP48 usage; area estimates for Virtex-7 use 90% of slices (may affect routing).
- **ECC parameters**: Discriminant too small per SafeCurves; twist-secure generation 20× slower; not proven immune to Cheon's attack (q-1, q+1 factorization).
