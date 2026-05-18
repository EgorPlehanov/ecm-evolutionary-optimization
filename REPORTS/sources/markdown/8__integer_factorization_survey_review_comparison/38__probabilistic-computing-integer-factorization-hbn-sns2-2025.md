---
title: "Highly durable and energy-efficient probabilistic bits based on h-BN/SnS2 interface for integer factorization"
title_en: "Highly durable and energy-efficient probabilistic bits based on h-BN/SnS2 interface for integer factorization"
source_type: "article"
authors: ["Han J.-K.", "Park J.-Y.", "Rehman S.", "Khan M. F.", "Kim M.-S.", "Kim S."]
year: "2025"
source_link: "https://doi.org/10.1002/inf2.70018"
doi: "10.1002/inf2.70018"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "probabilistic-computing-integer-factorization-hbn-sns2-2025.md"
---

# Content source: Highly durable and energy-efficient probabilistic bits based on h-BN/SnS₂ interface for integer factorization

## Source type
Peer-reviewed journal article (InfoMat, Vol. 7, Issue 7, e70018, 2025). Wiley.

## Authors affiliation
Multiple institutions: Seoul National University, Sejong University, Hanbat National University, Ewha Womans University (all Republic of Korea).

## Objective
Demonstrate a novel probabilistic bit (p‑bit) device using two‑dimensional materials (h‑BN/SnS₂ nanosheets) that achieves high durability (>10⁸ cycles), low energy consumption (3.36 pJ/bit for switching), improved noise immunity (pulse‑width control), and apply it to invertible logic gates and integer factorization as an example of solving combinatorial optimization problems.

## Core content summary

### 1. Motivation: probabilistic computing (p‑computing)

**Problem context**:
- Conventional digital computing faces energy efficiency challenges, especially for combinatorial optimization problems (traveling salesperson, integer factorization, Boolean satisfiability, knapsack).
- Quantum annealing (e.g., D‑Wave) is effective but requires cryogenic temperatures.
- **Probabilistic computing (p‑computing)** leverages intrinsic stochasticity of nanodevices as a feature, not a limitation, to perform probabilistic inference and solve optimization problems via energy minimization (Ising model).

**Energy function (Ising model)**:
\[
E = -\sum_{j\neq i} w_{ij} p_i p_j + \sum_i \theta_i p_i
\]
where \(w_{ij}\) = connection weight, \(p_i\) = p‑bit output (0 or 1), \(\theta_i\) = external bias.

**Input function**:
\[
I_i = -\frac{\partial E}{\partial p_i} = \sum_{j\neq i} w_{ij} p_j - \theta_i
\]

P‑bits are updated iteratively based on \(I_i\) to minimize \(E\), finding global minima even in the presence of local minima.

### 2. Device structure and operation (Sections 2.1–2.3)

**Materials**:
- Channel: tin disulfide (SnS₂) nanosheet (~26 nm thick).
- Gate insulator: hexagonal boron nitride (h‑BN) nanosheet (~23 nm thick).
- Stack: top gate / h‑BN / SnS₂ / Al₂O₃ / n⁺‑Si substrate.
- Two transistors M1 (p‑bit) and M2 (active switch) share source electrode.

**Interface trap mechanism**:
- Electron trapping/detrapping at h‑BN/SnS₂ interface modulates channel conductance (G).
- Positive VG pulse (+3 V) → electron trapping → G decreases.
- Negative VG pulse (−5 V) → electron detrapping → G increases.
- Low interface trap density (\(D_{it} \approx 10^8\)–\(10^9\) cm⁻² eV⁻¹) estimated from high field‑effect mobility (49.7 cm² V⁻¹ s⁻¹) and endurance tests.

**Stochasticity** (Section 2.2):
- Due to intrinsic randomness of trapping/detrapping, G values follow a Gaussian distribution.
- Mean (\(\mu_G\)) and standard deviation (\(\sigma_G\)) are tunable by pulse width (\(t_{pulse}\)).
- As \(t_{pulse}\) increases from 1 μs to 10 ms, both \(\mu_G\) and \(\sigma_G\) increase.

**P‑bit operation phases** (Section 2.3, Fig. 3B):
1. **Idle**: M2 off (−3 V) → no short‑circuit path → static power mitigated.
2. **Probabilistic switching**: M1 receives VG pulse (width \(t_{pulse}\)), M2 on (0 V), VD1 = VD2 = 0 V → minimal energy.
3. **Digitizing**: Both M1 and M2 on, VD1 = VD2 = VDD/2 (0.5 V), buffer amplifies small VS deviations → digital output Vout = 0 or VDD (1 V).

**Key result**: Output probability P(Vout = 1) follows sigmoid function of \(t_{pulse}\) (Fig. 3C). Control variable is \(t_{pulse}\) (10 μs to 10 ms) rather than voltage amplitude → much wider input margin → better noise immunity than prior p‑bits (<1 V margin).

### 3. Energy consumption (Section 2.4, Table 1)

| Component | Energy per bit | Notes |
|-----------|---------------|-------|
| P‑bit switching (M1) | ≤ 3.36 pJ/bit | Lowest among non‑MTJ p‑bits |
| Buffer (peripheral) | up to 1.095 nJ/bit | Dominant; needed for digitization |
| Total | ~1.1 nJ/bit | |

**Comparison with prior p‑bits**:
- Previous studies ignored peripheral circuit energy; this work includes it.
- Use of active switch (M2) instead of resistor reduces static power.
- Buffer uses fewer transistors than comparator → lower energy.

**Endurance**: >10⁸ cycles (Fig. 1D) — highest reported among p‑bits (Table 1).

### 4. Invertible Boolean logic gates (Section 2.5)

**Principle**:
- Each variable assigned a p‑bit.
- Energy function \(E = (\text{target} - \text{output})^2\).
- \(I_i\) derived from \(\partial E/\partial p_i\), mapped to \(t_{pulse}\) via sigmoid model.

**Results** (Supporting Information):
- AND, OR, NOT gates demonstrated in both forward and reverse directions.
- Reverse operation (estimating inputs from output) is unique to invertible logic; not possible in conventional deterministic gates.
- Example: For AND gate with output fixed at 1, p‑bit network outputs (1,1) with highest probability (Fig. S11B).

### 5. Integer factorization (Section 2.6, Fig. 4)

**2‑bit × 2‑bit multiplier**:
- Inputs: A = A₁A₀ (2 bits), B = B₁B₀ (2 bits).
- Output: N = N₃N₂N₁N₀ (4 bits).
- Total: 8 p‑bits.
- Energy function: \(E = (\text{AB} - \text{N})^2\).

**Factorization results**:
- For N = 6 (binary 0110), network outputs (A,B) = (10₂,11₂) or (11₂,10₂) with highest probability → factors 2 and 3 (or 3 and 2). (Fig. 4B)
- For N = 9 (binary 1001), network outputs (A,B) = (11₂,11₂) with highest probability → factor 3 and 3. (Fig. 4C)

**Scaling to RSA** (speculative):
- RSA‑2048 modulus: ~2048 bits, each prime ~1024 bits (~333 binary digits for product of two 1024‑bit primes; careful: the paper says "617‑digit modulus" and "333‑bit primes" — needs verification).
- Estimated p‑bit count for RSA‑2048: ~2716 p‑bits.
- Claim: achievable with current device integration; no cryogenic cooling needed → potential energy advantage over quantum computing.

### 6. Experimental methods (Section 4)

**Fabrication**:
- Mechanical exfoliation of SnS₂ and h‑BN.
- Dry transfer onto Al₂O₃/Si substrate.
- Electron‑beam lithography for source/drain/gate electrodes (Ti/Au deposition).

**Measurement**:
- Function generator for pulses (Keysight 33622a).
- Current waveform analyzer (Keysight CX3324a) for real‑time ID measurement.
- Room temperature, ambient air.

**P‑bit model** (Eq. 5–6):
\[
p_i = U[\sigma((t_{pulse}-t_0)/t_s) - r]
\]
where σ = sigmoid, U = unit step, r = random variable (Gaussian).  
Fitted parameters: \(t_0 = 291\ \mu s\), \(t_s = 1.62\ s\).

## Key innovations claimed

1. **First p‑bit using 2D materials** (h‑BN/SnS₂) and interface trap mechanism.
2. **Active switch** (M2) replaces series resistor → reduces static power.
3. **Pulse‑width control** (instead of voltage amplitude) → wider input margin (10 μs – 10 ms) → higher noise immunity.
4. **Highest reported endurance** (>10⁸ cycles) for p‑bits (Table 1).
5. **Lowest switching energy** (3.36 pJ/bit) among non‑MTJ p‑bits.
6. **First demonstration** of integer factorization using p‑bit network based on 2D material devices.

## Limitations (explicit from source / acknowledged)

- **Peripheral energy** (buffer) dominates (1.095 nJ/bit) — future work needed to optimize.
- **Material characterization** of interface traps is indirect (based on electrical behavior, not direct spectroscopy). Alternative 2D materials with lower Dit or wider bandgap may improve performance.
- **Device count** for RSA‑2048 (2716 p‑bits) is speculative; no actual hardware implementation.
- **Factorization demonstration** limited to 2‑bit × 2‑bit multiplier (N up to 9). Scaling to cryptographically relevant sizes (100+ digits) not experimentally shown.
- **Room‑temperature operation** is advantage over quantum, but comparison with classical factoring algorithms (GNFS, ECM) not provided.
- The work is primarily a **hardware/device** paper; factorization is a "demonstration of principle" application.

## Practical implications for factorization (as stated by authors)

- P‑bit networks can solve combinatorial optimization problems (including integer factorization) more efficiently than classical deterministic computing, using massively parallel probabilistic inference.
- Potential alternative to quantum annealing (no cryogenics, higher integrability with CMOS).
- For RSA‑2048, ~2716 p‑bits could theoretically factor the modulus (speculative).

## References cited (selected relevant to factorization)
- Borders et al. (2019) — Integer factorization using stochastic magnetic tunnel junctions (Nature).
- Camsari et al. (2017) — Stochastic p‑bits for invertible logic (Phys. Rev. X).
- Woo et al. (2022) — Probabilistic computing using CuTe/HfO₂/Pt diffusive memristors (Nat. Commun.).
- Numerous references on p‑computing, Ising machines, memristors, and 2D materials.
