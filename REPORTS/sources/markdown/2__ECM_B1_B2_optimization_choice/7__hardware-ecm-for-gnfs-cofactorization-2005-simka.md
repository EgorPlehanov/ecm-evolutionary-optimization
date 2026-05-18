---
title: "Hardware Factorization Based on Elliptic Curve Method"
title_en: "Hardware Factorization Based on Elliptic Curve Method"
source_type: "conference_paper"
authors: ["Šimka M.", "Pelzl J.", "Kleinjung T.", "Franke J.", "Priplata C.", "Stahlke C.", "Drutarovský M.", "Fischer V.", "Paar C."]
year: "2005"
source_link: "https://doi.org/10.1109/FCCM.2005.3"
doi: "10.1109/FCCM.2005.3"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "hardware-ecm-for-gnfs-cofactorization-2005-simka.md"
---

# Content source: Hardware Factorization Based on Elliptic Curve Method

## Source type
Conference paper (FCCM 2005 — IEEE Symposium on Field-Programmable Custom Computing Machines).

## Authors and affiliations
- Martin Šimka, Miloš Drutarovský (Technical University of Košice, Slovakia)
- Jan Pelzl, Christof Paar (Horst Görtz Institute, Ruhr University Bochum, Germany)
- Thorsten Kleinjung, Jens Franke (University of Bonn, Germany)
- Christine Priplata, Colin Stahlke (EDIZONE GmbH, Bonn, Germany)
- Viktor Fischer (Université Jean Monnet, Saint-Étienne, France)

## Objective
Present the first hardware implementation of the Elliptic Curve Method (ECM) for integer factorization. Target: numbers up to 200 bits (factors up to ~40 bits), B₁=960, B₂=57,000, D=30. Proof-of-concept: software-hardware co-design on FPGA (Xilinx Virtex2000E-6) with ARM7TDMI microcontroller. Estimate cost/performance for massive parallel ECM in GNFS cofactorization.

## ECM algorithm parameters (Section 3.1)

| Parameter | Value | Notes |
|-----------|-------|-------|
| B₁ | 960 | Smoothness bound phase 1 |
| B₂ | 57,000 | Smoothness bound phase 2 |
| D | 30 | Step size for stage 2 (φ(30)=8) |
| k (scalar) | 1375 bits | Product of prime powers ≤ B₁ |
| Curves per factor | ≈20 | For >90% success probability |

**Phase 1 cost** (binary method, z_P=1):
- 1374 point additions + 1374 point duplications
- Each addition: 5 multiplications (since z_{P−Q}=1)
- Each duplication: 5 multiplications
- Total: 13740 modular multiplications

**Phase 2 cost** (D=30):
- 1881 point additions (general case, z_{P−Q}≠1) → 6 multiplications each
- 10 point duplications → 5 multiplications each
- 13590 multiplications for product accumulation
- Total: 24926 modular multiplications

## Montgomery form (x:z only) — Section 2.2

Equation: \(B y^2 z = x^3 + A x^2 z + x z^2\).

**Point addition** (requires P, Q, and P−Q):
- x_{P+Q} = z_{P−Q}[(x_P − z_P)(x_Q + z_Q) + (x_P + z_P)(x_Q − z_Q)]²
- z_{P+Q} = x_{P−Q}[(x_P − z_P)(x_Q + z_Q) − (x_P + z_P)(x_Q − z_Q)]²
- Cost: 6 multiplications (5 when z_{P−Q}=1).

**Point duplication**:
- 4x_P z_P = (x_P + z_P)² − (x_P − z_P)²
- x_{2P} = (x_P + z_P)² (x_P − z_P)²
- z_{2P} = 4x_P z_P[(x_P − z_P)² + A_{24}·4x_P z_P], with A_{24} = (A+2)/4
- Cost: 5 multiplications.

**Scalar multiplication (phase 1, binary method)**:
- z_{P₀}=1 → z_{P−Q}=1 throughout
- 11 multiplications per step (reduced to 10 with z=1)
- 1374 steps → 13740 multiplications.

## Montgomery multiplier (Tenca & Koç 2003) — Section 3.3.1

**Algorithm 1** (Multiple Word Radix-2 Montgomery Multiplication):
```
S = 0
for i = 0 to n-1:
    q_i = x_i·Y₀ + S₀  (mod 2)
    if q_i = 1:
        for j = 0 to e:
            (C_a, S(j)) = C_a + x_i·Y(j) + M(j)
            (C_b, S(j)) = C_b + S(j)
            S(j-1) = (S₀(j), S_{w-1}(j-1))
    else:
        for j = 0 to e:
            (C_a, S(j)) = C_a + x_i·Y(j)
            (C_b, S(j)) = C_b + S(j)
            S(j-1) = (S₀(j), S_{w-1}(j-1))
    S(e) = 0
```

**Parameters**:
- n = bit-length of modulus (198 bits)
- w = word width (32 bits)
- e = number of words = ⌈(n+1)/w⌉ = 7
- p = pipelining depth (2)

**Condition to omit final reduction**: 4M < 2ⁿ (Walter 2002).

**Clock cycles per multiplication** (Eq. 7):
\[
T_{mul} = \lceil n/p \rceil·(e+1) + 2p = \lceil 198/2 \rceil·8 + 4 = 99·8 + 4 = 796 \text{ cycles}.
\]

## Architecture design (Section 3.2)

### ECM unit (Figure 1)
- ALU (modular +,−,×)
- Memory (21 registers × n bits)
- Internal control logic

### Central control logic
- Single control unit drives multiple ECM units via control bus.
- Commands (16 bits): start, operation (add/sub/mul/square), input registers (2), output register.
- All units execute same instructions in parallel (SIMD style).

### Memory (Figure 2)
- Each register: e words of w=32 bits.
- Word-wise access.

### Addition/subtraction (Algorithm 2/3)
- Modular addition: compute X+Y, if >2M subtract 2M.
- T_add = 3(e+1) = 24 cycles (worst case).
- Modular subtraction: compute X−Y, if negative add 2M.
- T_sub = 2(e+1) = 16 cycles.

## Parallel ECM (Section 3.4)

- All units share same control (identical phase 1 and phase 2 flow).
- Only initial parameters (modulus N, curve A, starting point) differ.
- Units run in lockstep; results read out sequentially.

## FPGA implementation results (Section 4)

**Platform**:
- FPGA: Xilinx Virtex2000E-6 (2M gates)
- Microcontroller: ARM7TDMI (25 MHz)
- Clock: 25 MHz (both ARM and FPGA)

**Resource usage (single ECM unit, w=32, e=7, p=2)**:
- LUTs: 1754 (≈6% of logic)
- Flip-flops: 506
- Block RAMs: 44 (27% of memory)

**Timings at 25 MHz** (Table 1):

| Operation | Time | Cycles (approx) |
|-----------|------|-----------------|
| Modular addition | 2.00 μs | 50 |
| Modular subtraction | 1.68 μs | 42 |
| Modular multiplication | 64.5 μs | 1612 |
| Modular squaring | 64.5 μs | 1612 |
| Point addition (phase 1, z=1) | 333 μs | 8325 |
| Point addition (phase 2) | 397 μs | 9925 |
| Point doubling | 330 μs | 8250 |
| **Phase 1** | **912 ms** | **22.8×10⁶** |
| **Phase 2** | **1879 ms** | **47.0×10⁶** |

**Max clock frequency**: 38.13 MHz (post-place-and-route).

## Theoretical cycle estimates vs measured (Section 4.3)

| Operation | Estimated cycles | Measured cycles (approx) |
|-----------|-----------------|--------------------------|
| Modular multiplication (n=198, w=32, p=2) | 796 | 1612 (factor ~2× slower) |
| Phase 1 | 11.07×10⁶ | 22.8×10⁶ |
| Phase 2 | 20.28×10⁶ | 47.0×10⁶ |

**Discrepancy attributed to**:
- Control logic overhead
- Communication between ARM and FPGA
- Not yet optimized instruction sequencing

## GNFS case study (SHARK design, Franke et al. 2005)

- SHARK requires testing ~1.7×10¹⁴ cofactors (≤125 bits) per year.
- At 20 curves/cofactor → 3.4×10¹⁵ ECM curves/year.
- With ASIC implementation (500 MHz), single unit: ~55 ms/curve → 18 curves/s per unit.
- Required units: 3.4×10¹⁵ / (365·86400·18) ≈ 6×10⁶ units.
- Area estimate per unit: ≈55,600 transistors → 6×10⁶ units ≈ 3.3×10¹¹ transistors.
- With 0.13 μm CMOS (Pentium4-sized: 55M transistors) → ~6,000 chips.
- Cost: <$45,000 (negligible compared to $200M for SHARK).

## Key contributions claimed

1. **First published hardware implementation of ECM** (proof-of-concept).
2. Demonstration that ECM is suitable for hardware acceleration (low memory, regular operations, high parallelism).
3. Integration with ARM microcontroller for control (software-hardware co-design).
4. Estimates for ASIC implementation show ECM can accelerate GNFS at negligible cost.

## Limitations (explicit)

1. **Phase 2 not fully implemented** at time of publication (timings are estimates, Table 1 shows "Phase 2 1879 ms" but derived from estimates, not actual measurements).
2. **Control overhead** from ARM-FPGA communication significant (measured cycles ~2× theoretical estimates).
3. **Binary method** for phase 1 (not optimal addition chains; PRAC would reduce multiplications to ~9.3/log2·k).
4. **FPGA clock frequency** limited to 38 MHz (ASIC estimated at 500 MHz but not implemented).
5. **Memory**: 44 BlockRAMs per unit (27% of Virtex2000E) — limits number of units per FPGA.
6. **No dynamic scheduling** — all units run in lockstep, even if some finish earlier.

## Relation to other work

- Builds on ECM algorithm (Lenstra 1987)
- Montgomery form (Montgomery 1987)
- Montgomery multiplier (Tenca & Koç 2003)
- GNFS hardware design SHARK (Franke et al. 2005)
- This is the first hardware ECM; later improved by Gaj et al. (CHES 2006, TC 2009) and Zimmermann et al. (FPL 2010).
