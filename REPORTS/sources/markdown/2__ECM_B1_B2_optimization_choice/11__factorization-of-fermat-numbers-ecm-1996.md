---
title: "Factorization of the Tenth and Eleventh Fermat Numbers"
title_en: "Factorization of the Tenth and Eleventh Fermat Numbers"
source_type: "tech_report"
authors: ["Brent R. P."]
year: "1996"
source_link: "https://doi.org/10.1016/S0012-365X(96)00140-1"
doi: "10.1016/S0012-365X(96)00140-1"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "factorization-of-fermat-numbers-ecm-1996.md"
---

# Content source: Factorization of the Tenth and Eleventh Fermat Numbers

## Source type
ANU Computer Sciences Laboratory Technical Report (TR-CS-96-02). Also published in Mathematics of Computation (1999).

## Author
Richard P. Brent (Australian National University)

## Objective
Report the complete factorization of the tenth and eleventh Fermat numbers using the Elliptic Curve Method (ECM). Provide historical context, implementation details of multiple ECM variants (vector, parallel, special-purpose hardware), and analysis of computational effort.

## Historical context (Table 1)

| n | Factorization | Method | Year | Discoverer |
|---|---------------|--------|------|------------|
| 5 | p3·p7 | Trial division | 1732 | Euler |
| 6 | p6·p14 | — | 1880 | Landry |
| 7 | p17·p22 | CFRAC | 1970 | Morrison & Brillhart |
| 8 | p16·p62 | Brent–Pollard rho | 1980 | Brent & Pollard |
| 9 | p7·p49·p99 | SNFS | 1990 | Lenstra et al. |
| **10** | **p8·p10·p40·p252** | **ECM** | **1995** | **Brent** |
| 11 | p6·p6·p21·p22·p564 | ECM | 1988 | Brent |

## Complete factorizations

### F₁₀
\[
F_{10} = 2^{1024} + 1 = 45592577 \cdot 6487031809 \cdot p_{40} \cdot p_{252}
\]
where:
- p₈ = 45592577 (Selfridge, 1953 — trial division)
- p₁₀ = 6487031809 (Brillhart, 1962 — trial division)
- **p₄₀ = 4659775785220018543264560743076778192897** (Brent, Oct 20, 1995 — ECM)
- p₂₅₂ = 13043…24577 (proved prime via Selfridge's Cube Root Theorem)

### F₁₁
\[
F_{11} = 2^{2048} + 1 = 319489 \cdot 974849 \cdot p_{21} \cdot p_{22} \cdot p_{564}
\]
where:
- p₆ = 319489, p₆ = 974849 (Cunningham, 1899 — trial division)
- p₂₁ = 167988556341760475137 (Brent, May 1988 — ECM)
- p₂₂ = 3560841906445833920513 (Brent, May 1988 — ECM)
- p₅₆₄ = 17346…34177 (proved prime by Morain via ECPP)

## ECM implementations (Section 5)

### Program A (1985)
- Pascal + assembler, Montgomery form, phase 2 birthday paradox.
- K₁ = 10/log 2, K₂ = 1/2.

### Program C (1988, MVFAC) — used for F₁₁
- Fortran, vectorized (Fujitsu VP100/VP2200).
- Multiple curves in parallel in phase 1 (vectorization), single curve phase 2.
- Montgomery form throughout, K₁ = 11/log 2, K₂ = 1.
- Multiplication: base 2²⁶, double-precision floating-point.

**F₁₁ timing**: 20 curves with B₁ = 16,000 → <1 hour on VP100.

### Program D (Sparc)
- Same as program C but scalar (non-vector). Used for F₁₀.
- 60 MHz SuperSparc: ~5.7×10⁻⁶·B₁ hours per curve.

### Program E (AP1000 parallel)
- 128 processors, each working independently. Found p₄₁ factor of 55¹²⁶+1.

### Program F (Dubner Cruncher, 1994–1995)
- Special-purpose hardware: LSI Logic L64240 MFIR DSP chip.
- 512-bit multiplication in 6.4 μs (peak), but communication overhead reduces effective performance for <1000 bits.
- 256 KB on-board memory.
- Memory-limited: cannot handle F₁₅ (requires ~4 KB, fine) but F₁₄ requires more.
- Phase 1 B₁ = 100,000: F₁₃ → 137 minutes/curve; F₁₄ → 391 minutes/curve.

**Found**: p₂₇ factor of F₁₃ = 319546020820551643220672513 (June 16, 1995) after 493 curves, 47 days.

### Program G (Cruncher, improved)
- Montgomery form throughout, improved standard continuation for phase 2.
- K₁ = 12/log 2, K₂ = 3 (no extended GCD computations).
- ~35% faster than program F.

## Computational effort for F₁₀ (Section 6)

| B₁ | Curves | E (efficiency) | Machine | Period |
|----|--------|----------------|---------|--------|
| 60,000 | 2,000 | 0.14 | VP100 | Mar 1988 – Nov 1990 |
| 200,000 | 17,360 | 0.42 | VP2200 | Aug 1991 – Aug 1995 |
| 500,000 | 700 | 0.69 | Sparc ×2 | Sep 1994 – Jul 1995 |
| 1,000,000 | 6,400 | 0.87 | Sparc ×8 | Jul 1995 – Aug 1995 |
| 2,000,000 | 900 | 0.98 | Sparc ×8 | Aug 1995 – Oct 1995 |
| 2.9×10⁵ (mean) | 21,440 | 0.63 | — | — |

**Successful curve**: σ = 14152267, B₁ = 2,000,000 → 10 curves in ~114 CPU hours on SuperSparc.

**Total multiplications mod c₂₉₁**: 1.4×10¹¹ (~240 Mips-years, ~140 Mflop-years).

## Group orders

### F₁₀ factor p₄₀
\[
g = p_{40} + 1 - 3674872259129499038
  = 2^{2}\cdot 3^{2}\cdot 5\cdot 149\cdot 163\cdot 197\cdot 7187\cdot 18311\cdot 123677\cdot 226133\cdot 314263\cdot 4677853
\]

### F₁₁ factor p₂₁
\[
p_{21} - 1 = 2^{14}\cdot 3\cdot 373\cdot 67003\cdot 136752547
\]

### F₁₁ factor p₂₂
\[
p_{22} - 1 = 2^{13}\cdot 7\cdot 677\cdot p_{14}
\]

### F₁₃ factor p₂₇
\[
p_{27} - 1 = 2^{19}\cdot 51309697\cdot 11878566851267
\]

## Theoretical analysis (Section 4)

### Dickman function and smoothness probabilities
- ρ(α): probability random integer's largest prime factor ≤ N¹ᐟᵅ.
- μ(α,β): probability second-largest ≤ N¹ᐟᵅ and largest ≤ Nᵝᐟᵅ.
- Functional equation: αρ'(α) + ρ(α−1) = 0.
- μ(α,β) = ρ(α) + ∫_{α−β}^{α−1} ρ(t)/(α−t) dt.

### Asymptotic optimal parameters for phase 1
Let α = log p / log B₁. Then:
- log B₁ ∼ α log α
- log(expected curves) ∼ α log α
- log(expected multiplications) ∼ √(2 log p log log p)
- τ(p) = (log W_opt)² / (log p log log p) → 2 as p→∞.

### Table 2 (expected work)

| Digits | log₁₀ W_opt | τ(p) |
|--------|-------------|------|
| 20 | 7.35 | 1.677 |
| 30 | 9.57 | 1.695 |
| 40 | 11.49 | 1.707 |
| 50 | 13.22 | 1.716 |
| 60 | 14.80 | 1.723 |

## Primality proofs (Section 9)

- p₄₀: primitive root 5, p₄₀−1 fully factored.
- p₂₅₂: Selfridge's Cube Root Theorem (p₂₅₂−1 = F·c₁₅₈ with F > 2×10⁹³, p₂₅₂ < 2F³+2F).
- p₅₆₄: Atkin–Morain ECPP (Morain, 1988) — 28 hours on 60 MHz SuperSparc.

## Prospects for F₁₂ (Section 10)

Known factors of F₁₂ (as of 1996):
\[
F_{12} = 114689\cdot 26017793\cdot 63766529\cdot 190274191361\cdot 1256132134125569\cdot c_{1187}
\]

- Sixth-smallest prime factor likely ≥ 10³⁰ (probability >0.9 given 500 curves with B₁=10⁶).
- Table 5: second-largest prime factor distribution (ρ₂) for F₇…F₁₁ shows F₁₁ unusually small (0.06).
- Complete factorization may require quantum computer (Shor 1994).

## Limitations (explicit)

1. ECM implementations assume heuristics about smoothness of group orders (not proved).
2. Probability estimates use asymptotic approximations; correction terms not included.
3. Special-purpose hardware (Cruncher) limited by memory and communication bandwidth; not a general-purpose accelerator.
4. Projection to F₁₂ based on limited data (500 curves with B₁=10⁶); actual sixth factor could be smaller.
5. No side-channel or fault attack considerations.
