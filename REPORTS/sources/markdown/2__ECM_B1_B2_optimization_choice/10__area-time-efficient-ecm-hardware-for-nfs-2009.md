---
title: "Area-Time Efficient Implementation of the Elliptic Curve Method of Factoring in Reconfigurable Hardware for Application in the Number Field Sieve"
title_en: "Area-Time Efficient Implementation of the Elliptic Curve Method of Factoring in Reconfigurable Hardware for Application in the Number Field Sieve"
source_type: "article"
authors: ["Gaj K.", "Kwon S.", "Baier P.", "Kohlbrenner P.", "Le H.", "Khaleeluddin M.", "Bachimanchi R.", "Rogawski M."]
year: "2009"
source_link: "https://doi.org/10.1109/TC.2009.131"
doi: "10.1109/TC.2009.131"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "area-time-efficient-ecm-hardware-for-nfs-2009.md"
---

# Content source: Area-Time Efficient Implementation of the Elliptic Curve Method of Factoring in Reconfigurable Hardware for Application in the Number Field Sieve

## Source type
Journal article (IEEE Transactions on Computers, 2009).

## Authors and affiliations
- Kris Gaj, Paul Kohlbrenner, Marcin Rogawski (George Mason University)
- Soonhak Kwon (Sungkyunkwan University)
- Patrick Baier (Siemens PLM Software)
- Hoang Le (University of Southern California)
- Mohammed Khaleeluddin (Hughes Network Systems)
- Ramakrishna Bachimanchi (Jefferson Lab)

## Objective
Design an area-time efficient hardware architecture for the Elliptic Curve Method (ECM) of integer factorization, optimized for application in the Number Field Sieve (NFS). Target: factoring ~200-bit numbers (cofactors in NFS relation collection) with smoothness bounds B₁=960, B₂=57,000. Compare with previous hardware implementation (Pelzl, Simka et al. 2005) and state-of-the-art software (GMP-ECM).

## Key architectural improvements over Pelzl/Simka (2005)

| Feature | Pelzl/Simka | This work |
|---------|-------------|-----------|
| Control | External ARM microcontroller | On-chip optimized controller |
| Multipliers | 1 (iterative) | 2 (parallel) |
| Arithmetic units | Multiplier only | Multipliers + adder/subtractor working in parallel |
| Phase 1 point operation | Sequential | Interleaved: P+Q and 2P computed concurrently |
| Phase 1 cost (clocks) | 8200 | 1212 |
| Phase 1 time (Virtex2000E-6) | 213 μs | 23 μs |
| Memory per unit | 512×32 words (22 BRAMs) | 256×32 or 512×32 words (1–4 BRAMs) |
| Max ECM units per Virtex2000E | 3 | 7 |

## ECM algorithm parameters (for NFS context)

- **N** size: up to 198 bits (n = 198, corresponds to 2·n_W·32? Actually n=198 bits)
- **B₁** = 960 (smoothness bound for stage 1)
- **B₂** = 57,000 (smoothness bound for stage 2)
- **D** = 30 or 210 (step size for baby-step giant-step)
- **k** = product of prime powers ≤ B₁ → size ~1375 bits
- **Number of ECM curves per factor** ≈ 20 (for >80% success probability)

### Formulas for B₁, B₂ selection (from Silverman & Wagstaff 1993)
- For factor size ~40 bits: 4p ≈ 2⁴⁰ → p ≈ 2³⁸; e^{√(½ log p log log p)} ≈ 960 → B₁ ≈ 960.
- Ratio B₂/B₁ ≈ 59.

## Montgomery ladder (Algorithm 2) — x:z only

**Initialization**: z_{P₀}=1 → z_{P−Q}=1 throughout Phase 1 (saves one multiplication per step).

**Basic step** (Table I): concurrent P+Q and 2P using 2 multipliers + 1 adder/subtractor

| Cycle | Adder/Subtractor | Multiplier 1 | Multiplier 2 |
|-------|------------------|--------------|--------------|
| 0-1 | a₁ = x_P+z_P, s₁ = x_P−z_P, a₂ = x_Q+z_Q, s₂ = x_Q−z_Q | — | — |
| 1-2 | — | m₃ = s₁·a₂ | m₄ = s₂·a₁ |
| 2-3 | a₃ = m₃+m₄, s₄ = m₃−m₄ | — | — |
| 3-4 | — | x_{P+Q} = a₃² | m₈ = s₄² |
| 4-5 | — | — | x_{P+Q} = m₈·z_{P−Q} |
| ... | ... | ... | ... |

**Cost Phase 1 (point addition + doubling)**: 5 multiplications + 2 additions → **1212 clock cycles** (vs 8200 in prior work).

**Cost Phase 2 (general case, z_{P−Q}≠1)**: 6 multiplications + 2 additions → **1428 cycles**.

**Cost Phase 2 (addition only)**: 3 multiplications + 6 additions → **924 cycles**.

## Montgomery multiplication (Algorithm 8) — radix-2, carry-save adders

**Algorithm**:
```
S[0] ← 0; C[0] ← 0
for i = 0 to n-1:
    q_i ← (C[i]₀ + S[i]₀ + X_i·Y₀) mod 2
    (C[i+1], S[i+1]) ← CSA(C[i], S[i], X_i·Y, q_i·N) / 2
end for
Convert (C[n], S[n]) to regular integer (carry-propagate adder)
```

**Key optimizations**:
- Carry-save adders (CSAs) reduce critical path (single full adder delay)
- n = ⌈log₂ N⌉ + 2 (ensures output < 2N)
- **Latency**: n + 16 clock cycles
  - For n=200 → 216 cycles per Montgomery multiplication

**Hardware** (Fig. 8a):
- 2 CSAs in cascade → reduces 4-input sum to (C,S)
- Shift registers for X (input), N (modulus)
- Final addition (carry-propagate) over 8 cycles

## Phase 2 — Baby-step giant-step (Section II-D)

**Parameters**:
- D = 30 or 210 (step size)
- U = {j: 1 ≤ j ≤ D/2, gcd(j,D)=1} (baby steps)
- V = {m: m = ⌈(B₁-D/2)/D⌉ to ⌊(B₂+D/2)/D⌋} (giant steps)

**Prime representation**: π = m·D ± j for j∈U, m∈V.

**Precomputations**:
- Build table S = {j·Q₀ | j∈U} (24 points for D=210, 8 for D=30)
- Compute D·Q₀ and M_min·(D·Q₀)
- Generate prime table: check which (m,j) correspond to primes

**Main computation**:
- For each m, compute m·D·Q₀
- Accumulate product d = ∏ (x_{mD}·z_j − z_{mD}·x_j) mod N
- Final gcd(d,N) reveals factor

**Execution time breakdown (D=210, n=198)**:

| Operation | Cycles | % total |
|-----------|--------|---------|
| Precompute j·Q₀ | 49,056 | 2.56% |
| Compute D·Q₀ | 11,424 | 0.60% |
| Compute M_min·D·Q₀ | 4,284 | 0.22% |
| Compute m·D·Q₀ (m=M_min+1 to M_max) | 244,860 | 12.78% |
| Accumulate product d | 1,525,886 | 79.67% |
| **Total Phase 2** | **1,915,219** | 100% |

**Total ECM per curve (Phase 1+2)**: ~3.6 million cycles (D=210) → **35.5 ms** at 100 MHz.

## Implementation results on multiple FPGAs (Table IX)

| Device | #Units | Freq (MHz) | Time P1+P2 | ECM ops/s | Cost (2006) | Ops/s per $100 |
|--------|--------|------------|------------|-----------|-------------|----------------|
| Virtex XCV2000E-6 | 7 | 48 | 75.5 ms | 93 | $1,230 | 8 |
| Virtex II XC2V6000-6 | 13 | 120 | 30.2 ms | 430 | $2,700 | 16 |
| Spartan 3 XC3S5000-5 | 13 | 80 | 45.3 ms | 287 | $130 | 221 |
| Spartan 3E XC3S1600E-5 | 5 | 96 | 37.7 ms | 133 | $35 | 380 |
| Virtex 4 XC4VLX200-11 | 24 | 104 | 35.2 ms | 682 | $3,000 | 22 |

**Observation**: Low-cost Spartan 3E achieves **380 ECM ops/s per $100** — 17× better cost-effectiveness than high-end Virtex 4 (22 ops/s per $100).

## Comparison with GMP-ECM on Pentium 4 Xeon (2.8 GHz)

| | GMP-ECM (optimized) | Virtex II (13 units) | Spartan 3 (13 units) |
|---|---------------------|----------------------|----------------------|
| Phase 1 | 11.3 ms | — | — |
| Phase 2 | 13.5 ms | — | — |
| Total per curve | 24.8 ms | 30.2 ms (per unit) | 45.3 ms (per unit) |
| Throughput (curves/s) | 40 | 430 | 287 |
| Cost per chip (2006) | ~$300 | $2,700 | $130 |
| Throughput per $100 | 13 | 16 | 221 |

**Conclusion**: Spartan 3 achieves **17× better cost-performance** than Pentium 4 for ECM.

## Comparison with Pelzl/Simka et al. (2005) — both on Virtex2000E-6

| Metric | Pelzl/Simka | This work | Ratio (ours better) |
|--------|-------------|-----------|---------------------|
| Phase 1 time | 292.9 ms | 31.7 ms | 9.3× |
| Phase 2 time (D=30) | 527.2 ms | 72.1 ms | 7.3× |
| Phase 2 time (D=210) | — | 35.5 ms | — |
| CLB slices per unit | 3,102 | 8,411 | 0.37× (2.7× more area) |
| BRAMs per unit | 22 | 1–4 | 5.5–22× reduction |
| Max units per chip | 3 | 7 | 2.33× |

## Projection to 1024-bit RSA factoring (SHARK device, Franke et al. 2005)

- SHARK produces 1.7×10¹⁴ sieving reports per year.
- Each report requires ~20 ECM trials.
- Required ECM ops per year: 3.4×10¹⁵.
- With Spartan 3E (133 ops/s) → need 810,626 FPGAs → cost $29M.
- With ASIC (Kuon & Rose 2007: 100× area-time improvement) → cost ~$290k + $1M non-recurring.

## Limitations (explicit)

1. **Parameters fixed for ~40-bit factors** (B₁=960, B₂=57,000). Not general-purpose; would need re-tuning for larger factors.
2. **No embedded multipliers used** (by design, to keep portability). Modern FPGAs with DSP blocks could give further improvement (de Meulenaer et al. 2007).
3. **ASIC estimates based on generic library** (Synopsys 90nm) — not actual tape-out.
4. **Comparison with GMP-ECM uses different CPU generation** (Pentium 4 Xeon, 2006 era). Modern CPUs would be faster.
5. **Phase 2 memory-intensive** — D=210 requires 512×32-bit local memory per unit (4 BRAMs in Spartan 3).
6. **No side-channel or fault attack considerations**.
