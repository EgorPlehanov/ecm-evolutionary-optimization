---
title: "High-Performance Integer Factoring with Reconfigurable Devices"
title_en: "High-Performance Integer Factoring with Reconfigurable Devices"
source_type: "conference"
authors: ["Zimmermann R.", "Güneysu T.", "Paar C."]
year: "2010"
source_link: "unknown (provided PDF: 45__High_Performance_Integer_Factoring_with.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "fpga-ecm-implementation-virtex4-2010.md"
---

# Content source: High-Performance Integer Factoring with Reconfigurable Devices

## Source type
Peer-reviewed conference paper (FPL 2010 — International Conference on Field Programmable Logic and Applications).

## Authors affiliation
Horst Görtz Institute for IT-Security, Ruhr-University Bochum, Germany.

## Objective
Present a high-performance FPGA implementation of the Elliptic Curve Method (ECM) for factoring medium-sized composite integers (66–236 bits), targeting the COPACOBANA cluster platform, with both phase 1 and phase 2 implemented in hardware.

## Core methodology
- **Target platform**: COPACOBANA (Cost-Optimized Parallel Code Breaker) with 128 Xilinx Virtex-4 FPGAs.
- **Parallelism**: 24 ECM cores per FPGA running at 200 MHz (arithmetic clock).
- **Curve form**: Montgomery curves (allows computation using only x,z-coordinates; highly regular patterns).
- **Arithmetic units**: DSP-based modular multiplication (Orup's quotient pipelining variant, k=17 bits, n=10 blocks → 170-bit intermediate precision for 151-bit moduli) and modular addition/subtraction.
- **Phase 2 optimization**: Improved continuation method with D=210 parameter, addition chain for fixed multiples, reduced initial multiplications per round (Algorithm 2).
- **Clock domains**: Control unit at 100 MHz, ECP at 200 MHz, dual-ported memory buffer for crossing.

## Key results (B₁=960, B₂=57,000, D=210, scalar e=1,323 bits, 151-bit integers)

| Metric | Value |
|--------|-------|
| FPGA | Xilinx Virtex-4 SX35 |
| Number of ECM cores | 24 |
| Arithmetic clock | 200 MHz |
| Cycles phase 1 | 945,746 |
| Cycles phase 2 | 1,024,029 |
| Cycles total | 1,969,775 |
| Time phase 1 | 4.73 ms |
| Time phase 2 | 5.12 ms |
| **Phase 1 throughput** | **5,064 factorizations/sec** |
| **Phase 1+2 throughput** | **2,424 factorizations/sec** |

### Scalability
- Supports composite integers from 66 to 236 bits with minor generic changes.
- On fully equipped COPACOBANA (128 FPGAs): theoretical peak **310,272 factorizations/sec** (both phases).

## Comparison with prior work (Virtex-4, 202-bit integers)

| Design | Device | Cost | Phase 1+2 per sec | Per 100$ | Factor vs Gaj |
|--------|--------|------|-------------------|----------|---------------|
| Gaj et al. (2006/2009) | V4LX200 | $7,564 | 696 | 9.2 | 1× |
| **This work** | V4SX35 | $468 | 1,560 | 333 | **37× better** |
| de Meulenaer et al. (2007)* | V4SX25 | $298 | (phase1 only) ~16,000 | 5,369* | N/A |

> *de Meulenaer's design implements only phase 1 (reduced success probability), not directly comparable.

## Implementation details

### Modular multiplication (Orup's quotient pipelining, d=0)
- Word size k=17 bits, n=10 blocks → 170-bit intermediate precision.
- Three cascaded DSP cores in fixed pipeline.
- Total latency: n(n+2)+6 = 10×12+6 = 126 cycles per multiplication.
- No additional configurable logic resources needed.

### Modular addition/subtraction
- Two cascaded DSP cores.
- Supports both addition and subtraction with reduction.
- Latency: 2n+3 = 23 cycles for n=10.

### Phase 2 improvement (Algorithm 2)
- Delayed computation of r−s to next iteration → only one initial multiplication per run (vs initial delay every round in Gaj's method).
- Addition chain for D=210: 30 additions + 7 doublings vs 52 additions + 1 doubling (Gaj).
- 24 fixed multiples of Q₀ stored.

## Limitations (explicit or implied)
- Parameters B₁=960, B₂=57,000 fixed for reported results (not scalable for larger factors without re-synthesis).
- COPACOBANA platform-specific; not a standalone solution.
- Phase 2 improvement assumes D=210 fixed; changing D requires recomputing addition chain.
- Host PC required for pre/post-processing (gcd, curve generation).

## Conclusions
- First ECM implementation on Virtex-4 using DSP blocks for both phases.
- 37× better cost-performance ratio than previous work on same platform.
- Scales from 66 to 236 bits with minimal changes.
- Suitable for NFS cofactorization step.

## Practical value
- Direct application in COPACOBANA cluster for attacking RSA via NFS.
- Provides 2,424 factorizations/sec per FPGA for 151-bit composites.
- Open design principles (but code not explicitly released).
