---
title: "Optimized Implementation of the Elliptic Curve Factorization Method on a Highly Parallelized Hardware Cluster"
title_en: "Optimized Implementation of the Elliptic Curve Factorization Method on a Highly Parallelized Hardware Cluster"
source_type: "diploma_thesis"
authors: ["Zimmermann R."]
year: "2009"
source_link: "http://doi.org/..."
doi: "none"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "optimized-ecm-on-fpga-cluster-copacobana-2009.md"
---

# Content source: Optimized Implementation of the Elliptic Curve Factorization Method on a Highly Parallelized Hardware Cluster

## Source type
Diploma Thesis, Ruhr University Bochum & TU Braunschweig. November 2009. Supervisors: Prof. Dr. Dietmar Wätjen (TU Braunschweig), Prof. Dr.-Ing. Christof Paar (Ruhr University Bochum). Advisor: Dr.-Ing. Tim Güneysu.

## Author
Ralf Zimmermann

## Objective
Implement an optimized hardware architecture for the Elliptic Curve Method (ECM) on Xilinx Virtex-4 SX35 FPGAs using the COPACOBANA cluster (32 FPGAs × 24 cores per FPGA = 768 parallel ECM units). Target: numbers up to 151 bits (scalable to 66–236 bits) with B₁=960, B₂=57000, D=210. Complete implementation of both Phase 1 and Phase 2 using DSP48 cores for modular arithmetic.

## Key contributions

1. **Sequential modular multiplier** using only 3 DSP48 cores per ALU (vs 10 DSPs in previous parallel implementation), achieving 200 MHz clock frequency.
2. **Complete Phase 2 implementation** with addition chain precomputation (instead of generic algorithm) and improved product accumulation (saving ~388 multiplications vs Gaj et al. 2006).
3. **Instruction ROM design** using dual-port BlockRAM (36+18 bits = 54 bits per instruction) storing all 326 instructions for 14 modes, eliminating long routing paths.
4. **24 parallel ECM cores per FPGA** running at 200 MHz arithmetic clock.
5. **Comparison with prior FPGA designs and GPU** (Bernstein et al. 2009): FPGA more power-efficient despite lower absolute throughput.

## COPACOBANA cluster (Chapter 2.3)

- 32 Virtex-4 SX35 FPGAs (speed grade 10) arranged in 4 modules × 8 FPGAs.
- Host PC communicates via Ethernet → integrated μATX → USB to cluster.
- Maximum power consumption: ~10W per FPGA (author's estimate, actual <4W).
- 25 MHz bus clock (BUSCLK) multiplied to 100 MHz system clock (SYSCLK) then to 200 MHz arithmetic clock (ALUCLK).

## ECM parameters

| Parameter | Value | Notes |
|-----------|-------|-------|
| B₁ | 960 | Smoothness bound phase 1 |
| B₂ | 57,000 | Smoothness bound phase 2 |
| D | 210 | Step size for baby-step giant-step (φ(D)=48 → 24 baby steps) |
| k (scalar) | 1323 bits | Product of prime powers ≤ B₁ |
| Max bits | 151 bits (scalable) | With b=10 blocks of 17 bits each |

## Architecture (Chapter 6)

### System-level view (Figure 6.1–6.4)

- Host generates parameters (k, primetable, curve data) per FPGA.
- Each FPGA: Data Request Scheduler + 24 ECM cores + system bus (24 bits, converted from 32-bit host bus).
- Each ECM core: Control Unit (SYSCLK) + ALU (ALUCLK) + synchronization memory (asynchronous BRAM).

### Instruction ROM (Section 6.3.2)

- 326 instructions × 54 bits per core (stored locally in 1 BRAM per core).
- Dual-port BRAM: one port 36 bits, other port 18 bits, concatenated to 54 bits.
- Includes: 7 workspace memory control modes, 2 multiplier control, MADSUB control, sync control.
- Instruction format (Table 6.2): 54 bits covering duration, finish flag, zero state, and control signals for all ALU components.

### Workspace memory (Section 6.3.1)

- One BRAM per core, 1024×18 bits.
- Partitioned into 32 storage blocks × 2 cells (x and z coordinates of points).
- Memory map: blocks 0–23: precomputed jQ₀ points; block 24–27: current R and temporary; blocks 28–31: temporary.

### Arithmetic Logic Unit (ALU) — Figure 6.6

Components per core:
- 1 MADDSUB (modular addition/subtraction) — 2 DSP48s (with custom OPMODE to avoid shared C port conflict)
- 2 MMUL (modular multiplication) — each 3 DSP48s
- Workspace memory (1 BRAM)
- Multiplication modulus memory (1 BRAM, shared between MMULs)
- 5 BRAMs total per core.

## Modular multiplication unit (Section 6.3.3)

### Algorithm: Montgomery multiplication with quotient pipelining (Orup 1995, Algorithm 7)

Input: modulus M (odd), radix R = 2^{k·n} with k=17, n=10 blocks (170-bit), M < 2^{k·(n-1)-2}.
Precomputed: M̃ = (M′ mod 2^k)·M, where (-M·M′) mod 2^k = 1.
Inputs A,B in Montgomery form (0 ≤ A,B < 2M̃).

**Loop (i=0 to n)**:
    q_i = S_i mod 2^k
    S_{i+1} = (S_i / 2^k) + q_i·M̃ + b_i·A

**DSP configuration (Figure 6.11)**:
- DSP1: S(i,j) + q_i·M̃_j
- DSP2: + b_i·A_j (via internal data path)
- DSP3: shift and carry handling.

**Timing (Figure 6.12)**:
- After reset, first iteration takes n+1 cycles.
- Total cycles: T_mul = n·(n+2) + 6.
- For n=10: T_mul = 10·12 + 6 = 126 cycles (vs 66 cycles for parallel implementation in Röpke 2008).

**Resource comparison (Table 7.1)**:

| Metric | Röpke (parallel) | This work (sequential) | Improvement |
|--------|------------------|------------------------|-------------|
| DSP48s | 10 | 3 | -70% |
| Flip-flops | 270 | 132 | -51% |
| Slices | 432 | 73 | -83% |
| LUTs | 651 | 105 | -84% |
| Cycles/mul | 66 | 126 | +91% (cost) |
| Clock freq | 305 MHz | 420 MHz | +38% |

## Modular addition/subtraction unit (Section 6.3.3)

**Original (Röpke)**:
- 2 DSP48s, output buffer BRAM, 2n+3 cycles.

**This work**:
- Two variants: (a) small design (0 BRAM, 106 LUTs), (b) larger design (143 LUTs) to avoid shared C port conflict on Virtex-4.
- Timing: 2b+3 cycles = 23 cycles for b=10 (10 blocks × 2 + 3).
- Frequency: 421 MHz (variant a).

## Phase 1 (Section 6.4.1)

- Montgomery ladder (Algorithm 5) with P₀ as initial point.
- ALU mode 7: computes one ladder step (concurrent point addition + doubling) with P−Q = P₀.
- Since z_{P₀}=1, saves 1 multiplication per step.
- 1323-bit scalar k → 1322 ladder steps.
- Cycles per step: 688 (b=10) → Phase 1 cycles = 1322·688 ≈ 909,536 (actual 945,746 with overhead).

## Phase 2 (Section 6.4.2)

### Precomputation (Algorithm 9)

**On host**:
- Compute M_min = ⌊B₁/D + 0.5⌋, M_max = ⌊B₂/D − 0.5⌋.
- J_S(D) = {j ≤ D/2 : gcd(j,D)=1} for D=210 → 24 values.
- primetable[M][j] = 1 if (mD ± j) prime, else 0.

**On FPGA (addition chain instead of generic, Table 6.5)**:
- Compute all j·Q₀ (24 points) using precomputed chain of 30 point additions + 7 doubles.
- Compute D·Q₀, M_min·D·Q₀, and (M_min−1)·D·Q₀ (for difference).

### Main computation (Algorithm 10 — improved over Gaj et al. 2006)

**Optimizations**:
- Instead of Table 6.6 (initial delay per round), parse primetable row to find two 1-bits before computing.
- Accumulate d = ∏ (R_x·z_j − x_j·R_z) using two multipliers in parallel.
- For b=10: 3·b²+6b+32 = 3·100+60+32 = 392 cycles for two points, 2·b²+4b+22 = 200+40+22 = 262 cycles for one point.
- **Savings**: 388 multiplications vs Gaj et al. (265 from initial delay + 123 from single-point handling).

**Total Phase 2 cycles**: 1,024,029 (b=10).

## Results (Chapter 7)

### Single FPGA (Virtex-4 SX35, speed grade 10)

| Metric | Value |
|--------|-------|
| ECM cores per FPGA | 24 |
| Arithmetic clock | 200 MHz |
| System clock | 100 MHz |
| Bus clock | 25 MHz |
| Phase 1 time | 4.73 ms (945,746 cycles) |
| Phase 2 time | 5.12 ms (1,024,029 cycles) |
| Total per curve | 9.85 ms (1,969,775 cycles) |
| Throughput (Phase 1 only) | 5,064 curves/s |
| Throughput (Phase 1+2) | 2,424 curves/s |

### Resource utilization (1 core)

| Resource | Used / Total | Utilization |
|----------|--------------|-------------|
| Flip-flops | 885 / 30,720 | 2% |
| LUTs | 1,007 / 30,720 | 3% |
| Slices | 766 / 15,360 | 4% |
| BRAMs | 7 / 192 | 3% |
| DSP48s | 8 / 192 | 4% |

→ 24 cores fit comfortably.

### Scalability (Table 7.6)

| b | Max bits | Phase 1 time (ms) | Phase 2 time (ms) | Curves/s |
|---|----------|-------------------|-------------------|----------|
| 9 | 134 | 3.99 | 4.31 | 6,000 |
| 10 | 151 | 4.73 | 5.12 | 5,064 |
| 11 | 168 | 5.54 | 6.00 | 4,320 |
| 12 | 185 | 6.42 | 6.96 | 3,720 |
| 13 | 202 | 7.37 | 8.00 | 3,240 |
| 14 | 219 | 8.39 | 9.10 | 2,856 |
| 15 | 236 | 9.47 | 10.29 | 2,520 |

## Comparison with prior work (Section 7.3)

### vs. Gaj et al. 2006 (Table 7.8)

| Metric | Gaj (Spartan-3 5000) | Gaj (Virtex-4 LX200) | This work (SX35) |
|--------|----------------------|----------------------|------------------|
| Max bits | 198 | 198 | 202 (b=13) |
| Cores | 13 | 24 | 24 |
| Freq | 80 MHz | 104 MHz | 200 MHz |
| Phase 1 time | 21 ms | 16 ms | 7.37 ms |
| Phase 1/s | 624 | 1,448 | 3,240 |
| Phase 1/s per $100 | 577 | 19 | 692 |

### vs. de Meulenaer et al. 2007 (Table 7.9) — Phase 1 only

| Metric | de Meulenaer (Virtex-4 SX25) | This work (SX35) |
|--------|------------------------------|------------------|
| Max bits | 135 | 134 (b=9) |
| Cores | 12 | 24 |
| Freq | 220 MHz | 200 MHz |
| Phase 1 time | 63 μs | 3.99 ms |
| Phase 1/s | 16,000 | 6,000 |

Note: de Meulenaer's design is fully pipelined, unrolled, Phase 1 only; Phase 2 not implemented. This work includes Phase 2.

### vs. GPU (Bernstein et al. 2009, GTX 295) — B₁=8192 (Table 7.10)

| Metric | GPU (GTX 295) | FPGA (XC4VSX35) |
|--------|--------------|-----------------|
| Max bits | 210 | 219 (b=14) |
| Freq | 1,242 MHz | 200 MHz |
| Phase 1/s | 4,928 | 312 |
| Power | 316.5 W | 10 W (max) |
| Phase 1/s per W | 15.6 | 31.2 |

→ FPGA is 2× more energy-efficient (per Watt) despite 16× slower absolute throughput.

## Full COPACOBANA scaling potential

- 32 FPGAs × 24 cores = 768 parallel ECM units.
- Throughput (Phase 1+2): 768 × 2,424 curves/s ≈ 1.86 million curves/s.
- For GNFS cofactorization: 20 curves per cofactor → 93,000 cofactors/s.

## Limitations (explicit)

1. **Manual placement required** for >19 cores due to DSP tile sharing (shared C input on Virtex-4). Variant (b) of MADDSUB needed to avoid conflict.
2. **Scalar k stored in BRAM** per core; not dynamically adjustable without recompilation.
3. **No dynamic power management** (DSP cores not disabled when idle).
4. **Comparison with GPU uses Phase 1 only** (GPU implementation lacks Phase 2).
5. **Addition chain precomputation** fixed for B₁=960; changing B₁ requires new chain.
6. **Host communication overhead** limits scaling beyond 128 FPGAs.
