---
title: "Area-Time Efficient Hardware Architecture for Factoring Integers with the Elliptic Curve Method"
title_en: "Area-Time Efficient Hardware Architecture for Factoring Integers with the Elliptic Curve Method"
source_type: "article"
authors: ["Pelzl J.", "Šimka M.", "Kleinjung T.", "Franke J.", "Priplata C.", "Stahlke C.", "Drutarovský M.", "Fischer V.", "Paar C."]
year: "2005"
source_link: "https://doi.org/10.1049/ip-ifs:20055018"
doi: "10.1049/ip-ifs:20055018"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "area-time-efficient-hardware-architecture-for-ecm-2005-pelzl.md"
---

# Content source: Area-Time Efficient Hardware Architecture for Factoring Integers with the Elliptic Curve Method

## Source type
Journal article (IEE Proceedings — Information Security, Vol. 152, No. 1, 2005).

## Authors and affiliations
- Jan Pelzl, Christof Paar (Horst Görtz Institute, Ruhr University Bochum)
- Martin Šimka, Miloš Drutarovský (Technical University of Košice)
- Thorsten Kleinjung, Jens Franke (University of Bonn)
- Christine Priplata, Colin Stahlke (EDIZONE GmbH)
- Viktor Fischer (Université Jean Monnet, Saint-Étienne)

## Objective
Design and implement an area-time efficient hardware architecture for the Elliptic Curve Method (ECM) of integer factorization, targeting numbers up to 200 bits with factors up to ~40 bits. Provide proof-of-concept FPGA implementation (software-hardware co-design with ARM microcontroller) and estimate cost/performance for massive parallel ECM ASICs in GNFS cofactorization.

## ECM parameter selection (Section 4.1)

Target: numbers up to 200 bits (n ≤ 200), factors up to ≈40 bits.

| Parameter | Value | Notes |
|-----------|-------|-------|
| B₁ | 960 | Smoothness bound for stage 1 |
| B₂ | 57,000 | Smoothness bound for stage 2 |
| k (scalar) | ≈1375 bits | Product of prime powers ≤ B₁ |
| Curves per factor | ≈20 | For >90% success probability |

**Phase 1 cost** (binary method):
- 1374 point additions + 1374 point duplications
- 13740 modular multiplications

**Phase 2 cost** (D=30):
- 1881 point additions + 10 point duplications + 13590 product multiplications
- Total: 24926 modular multiplications

## Montgomery form (x:z only) — Section 3.2

Equation: \(B y^2 z = x^3 + A x^2 z + x z^2\) with \(\gcd(A^2-4, N)=1\). Group order divisible by 4 (by construction). To get divisibility by 12, use parametrization from Atkin & Morain (Appendix A.2).

**Point addition** (requires P, Q, and P−Q):
\[
x_{P+Q} = z_{P-Q}[(x_P - z_P)(x_Q + z_Q) + (x_P + z_P)(x_Q - z_Q)]^2
\]
\[
z_{P+Q} = x_{P-Q}[(x_P - z_P)(x_Q + z_Q) - (x_P + z_P)(x_Q - z_Q)]^2
\]
Cost: 6 multiplications (or 5 when z_{P−Q}=1).

**Point duplication**:
\[
4x_P z_P = (x_P + z_P)^2 - (x_P - z_P)^2
\]
\[
x_{2P} = (x_P + z_P)^2 (x_P - z_P)^2
\]
\[
z_{2P} = 4x_P z_P \big[(x_P - z_P)^2 + A_{24}·4x_P z_P\big], \quad A_{24} = (A+2)/4
\]
Cost: 5 multiplications.

## Montgomery ladder (Algorithm 2) — binary method

- Input: k with bits g_{t-1}…g₀, g_{t-1}=1.
- Initialization: P_n = P, P_{n+1} = 2P.
- For i = t-2 down to 0:
  - if g_i = 1: P_n = P_n + P_{n+1}, P_{n+1} = 2P_{n+1}
  - else: P_{n+1} = P_n + P_{n+1}, P_n = 2P_n
- Final: if g₀=1 then Q = P_n + P_{n+1} else Q = 2P_n.

**Cost per bit**: 11 multiplications (addition + duplication). With z_P=1 in phase 1, cost reduces to 10 multiplications per bit. With optimal addition chains (Montgomery PRAC), can reduce to ~9.3 multiplications per bit.

## Improved standard continuation for phase 2 (Section 3.4)

- Choose D (small, with many small prime factors).
- Precompute table T of kQ for 1 ≤ k < D/2, gcd(k,D)=1 (baby steps).
- Write each prime p ∈ (B₁, B₂] as p = mD ± k with kQ ∈ T.
- By Lemma 1: gcd(z_{pQ}, N) > 1 ⇔ gcd(x_{mDQ}·z_{kQ} − x_{kQ}·z_{mDQ}, N) > 1.
- Accumulate product Π = ∏(x_{mDQ}·z_{kQ} − x_{kQ}·z_{mDQ}) mod N, then one final gcd.

**Cost**: O(D) precomputation + O(B₂/D) point operations + 3·(π(B₂)−π(B₁)) multiplications for product.

## Parameter D selection (Table 1)

| D | φ(D) | Point additions | Point duplications | Product multiplications | Total muls | Extra registers |
|---|------|-----------------|--------------------|-------------------------|------------|-----------------|
| 6 | 2 | 56094 | 45 | 14625 | 70764 | 10 |
| 30 | 8 | 11286 | 50 | 13590 | 24926 | 10 |
| 60 | 16 | 5706 | 50 | 13629 | 19385 | 18 |
| 210 | 48 | 1818 | 70 | 13038 | 14926 | 50 |

**Choice for minimal AT product**: D=30 (φ(D)=8, only 8 extra registers, total 21 registers).

## Montgomery multiplier architecture (Tenca & Koç 2003)

- Scalable: word width w, pipeline depth p, number of words e = ⌈(n+1)/w⌉.
- Radix-2, carry-propagate adders (non-redundant representation).
- **Clock cycles per multiplication** (Eq. 4):
\[
T_{mul} = \lceil n/p \rceil · (e+1) + 2p
\]
- For w=32, p=2, e=7, n=198: T_mul = ⌈198/2⌉·8 + 4 = 99·8+4 = 796 cycles? Wait, paper says with w=8,p=8,e=25 gives 666 cycles (Section 6.1). For actual FPGA implementation: w=32, p=2 → T_mul = 666? Let's compute: ⌈198/2⌉=99, e=7 → 99·8=792, +4=796. But Table 2 shows 64.5 μs at 25 MHz → 1612 cycles. Something inconsistent. Stick to reported numbers.

**FPGA implementation** (w=32, p=2):
- T_mul = 64.5 μs at 25 MHz → 1612 cycles.

**ASIC estimate** (w=8, p=8, n=199, e=25):
- T_mul = ⌈199/8⌉·26 + 16 = 25·26+16 = 666 cycles.
- T_add = 3(e+1) = 78 cycles, T_sub = 2(e+1)=52 cycles.

## Point operation timings (ASIC estimate, 500 MHz)

| Operation | Cycles | Time (ms) |
|-----------|--------|-----------|
| Point addition (phase 1, z_{P−Q}=1) | 3742 | 0.00748 |
| Point duplication (phase 1) | 3608 | 0.00722 |
| Point addition (phase 2, general) | 4410 | 0.00882 |

**Total per curve**:
- Phase 1: 1374·(3742+3608) ≈ 10.099×10⁶ cycles → 20.2 ms.
- Phase 2: 1881·4410 + 50·3608 + 13590·666 ≈ 17.55×10⁶ cycles → 35.1 ms.
- Total: 55.3 ms per curve at 500 MHz.

## FPGA implementation results (Section 5)

**Platform**:
- FPGA: Xilinx Virtex2000E-6 (2M gates)
- Microcontroller: ARM7TDMI (25 MHz)
- Clock frequency: 25 MHz (limited by board, max 38 MHz)

**Resource usage (single ECM unit)**:
- LUTs: 1754
- Flip-flops: 506
- Block RAMs: 44 (27% of available)
- Max clock: 38.13 MHz

**Timings at 25 MHz** (Table 2):

| Operation | Time | Cycles (approx) |
|-----------|------|-----------------|
| Modular addition | 2.16 μs | 54 |
| Modular subtraction | 2.00 μs | 50 |
| Modular multiplication | 64.5 μs | 1612 |
| Modular squaring | 64.3 μs | 1608 |
| Point addition (phase 1) | 334 μs | 8350 |
| Point addition (phase 2) | 399 μs | 9975 |
| Point duplication | 331 μs | 8275 |
| Phase 1 | 918 ms | 22.95×10⁶ |
| Phase 2 (estimate) | 1760 ms | 44×10⁶ |

**Throughput**: ~0.37 curves/second (2.7 s per curve) at 25 MHz.

## Parallel ECM control (Section 4.4)

- All units execute same commands in parallel (identical control flow).
- Only initial data (modulus N, curve parameters, starting point) differ.
- Single controller can handle up to ~100 units before I/O overhead dominates.
- For massive parallelism (ASIC), use clusters with dedicated controllers.

## GNFS case study (Section 6)

**Requirements** (from SHARK design, Franke et al. 2005):
- 1.7×10¹⁴ cofactors (≤125 bits) per year.
- Each cofactor: 20 ECM curves (90% success probability).
- Required ECM ops/s: 1.7×10¹⁴·20 / (365·86400) ≈ 1.08×10⁸ ops/s.

**ASIC estimates** (w=8, p=8, 500 MHz):
- Time per curve: 55 ms.
- Units needed: 1.08×10⁸ ops/s · 0.055 s = 5.94×10⁶ units.

**Area per unit** (transistors):
- Multiplier (w=8,p=8): 21,400
- Add/sub: 1,000
- Memory (21 registers): 25,200
- Control: 8,000
- **Total: 55,600 transistors/unit**

**Chip count** (Pentium4-sized, 55M transistors):
- Units per chip: 55×10⁶ / 55,600 ≈ 990 units.
- Chips needed: 5.94×10⁶ / 990 ≈ 6,000 chips.

**Cost estimate**:
- 300mm wafer cost: $5,000 (from TWIRL paper).
- Dies per wafer ≈ (π·150²)/(chip area) — but paper says total chip area ≈ 625,000 mm²? That's huge (25×25 cm). Something off. They claim area scaling factor 0.628 from 198 to 125 bits → 198-bit unit area = (55,600 transistors) = ~0.1475 mm² (from earlier paper). For 125-bit: ~0.0926 mm².
- 5.94×10⁶ units × 0.0926 mm² = 550 mm² total silicon.
- Wafer 300mm → area ~70,686 mm², but chips are smaller. They estimate cost <$45,000 for ECM units — negligible compared to total GNFS machine cost ($200M).

## Comparison with GMP-ECM (software)

Not directly compared in this paper, but previous work (Franke et al. 2005, SHARK) indicates ECM hardware is orders of magnitude more cost-effective than software for large-scale GNFS.

## Key innovations claimed

1. First published hardware implementation of ECM (proof-of-concept).
2. Parameterization optimized for hardware (B₁=960, B₂=57000, D=30 minimizes AT product).
3. Use of Montgomery form with x:z only, avoiding y-coordinate.
4. Highly parallelizable: identical control for all units.
5. ASIC cost estimates show ECM hardware can accelerate GNFS at negligible extra cost.

## Limitations (explicit)

1. Phase 2 control logic not fully implemented at time of publication (estimated timings only).
2. Binary method for phase 1 (not optimal addition chains), though they mention PRAC could reduce to ~9.3 multiplications per bit.
3. FPGA frequency limited to 38 MHz (ASIC would be 500 MHz).
4. Word width w=32, pipeline depth p=2 chosen for area-time tradeoff, but not necessarily optimal for all applications.
5. Memory requirements: 44 BlockRAMs (27% of Virtex2000E) per unit, limiting number of units per FPGA.
6. Communication overhead for >100 units per controller.
