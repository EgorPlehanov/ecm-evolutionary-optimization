---
title: "Factoring Estimates for a 1024-Bit RSA Modulus"
title_en: "Factoring Estimates for a 1024-Bit RSA Modulus"
source_type: "conference_paper"
authors: ["Lenstra A.", "Tromer E.", "Shamir A.", "Kortsmit W.", "Dodson B.", "Hughes J.", "Leyland P."]
year: "2003"
source_link: "https://doi.org/10.1007/978-3-540-45146-2_1"
doi: "10.1007/978-3-540-45146-2_1"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "factoring-estimates-1024-bit-rsa-2003.md"
---

# Content source: Factoring Estimates for a 1024-Bit RSA Modulus

## Source type
Conference paper (Asiacrypt 2003? Published in LNCS).

## Authors and affiliations
- Arjen Lenstra (Citibank & TU Eindhoven)
- Eran Tromer, Adi Shamir (Weizmann Institute)
- Wil Kortsmit (TU Eindhoven)
- Bruce Dodson (Lehigh University)
- James Hughes (Storage Technology Corporation)
- Paul Leyland (Microsoft Research)

## Objective
Evaluate the feasibility and cost estimates of factoring a 1024-bit RSA modulus using the Number Field Sieve (NFS), specifically examining the parameter choices proposed in the preliminary TWIRL hardware design (Shamir & Tromer 2003). Provide improved parameter recommendations incorporated into the final TWIRL design.

## Core methodology

### NFS parameter estimation framework
- Use ρ (Dickman) and σ₁ (semi-smoothness) functions to estimate relation yield.
- Correction factor t: measures polynomial quality via E_f(2³⁰) / E(2³⁰).
- For given smoothness bounds (y_r, y_a) and large prime bounds (z_r, z_a), integrate probabilities over sieving region of size S = 2AB.
- Account for coprimality of (a,b) via factor 6/π² ≈ 0.608.

### Validation approach
- Perform actual smoothness tests (trial division up to 2³⁰ + ECM) on >100 billion (a,b) pairs for degrees 6 and 7.
- Compare actual semi-smooth counts with ρ+σ₁ estimates (Tables 4–6).
- Estimates consistently slightly higher than actual (attributed to asymptotic corrections and boundary effects).

### Polynomial generation
- Degrees d = 5,6,7,8,9 with m, skewness s, polynomial f, correction factor t (Appendix A).
- For final TWIRL parameters (Appendix B): degree 5 polynomial from Franke/Kleinjung program (20 CPU-days on Pentium 1.7GHz).

## Key results — original TWIRL parameters (from [17])

Proposed parameters for 1024-bit RSA (from preliminary TWIRL draft):

| Parameter | Value |
|-----------|-------|
| y_r = y_a | 2.5×10⁸ (<2²⁸) |
| Sieving region S | 6×10²³ (A≈5.5×10¹³, B≈5.5×10⁹) |
| Estimated cost | 1 year on US$10M device |

### Estimated yield (Table 1, d=6, S=6×10²³)

| y_r=y_a | ff | fp₁₂ | pf₁₂ | pp₁₂ |
|---------|----|-------|-------|-------|
| 2²⁸ | 2.6×10² | 2.2×10³ | 4.9×10⁴ | 1.1×10⁴ |
| 2³⁴ | 5.7×10⁷ | 7.2×10⁸ | 2.8×10⁸ | 3.5×10⁹ |

**Conclusion**: With y_r=y_a=2²⁸, yield is far too low (only ~260 full relations). With y_r=y_a=2³⁴ and no partial relations, insufficient. Partial relations required but matching behavior poorly understood.

### Optimal smoothness bounds for d=6, c=32 (T/32 full relations)

| Parameter | Value |
|-----------|-------|
| Optimal i_r, i_a | 47, 48 |
| Minimal effort | 9.2×10²⁰ |
| Effort at i=28 | 1.5×10³⁶ (factor ~10¹⁵ worse) |

→ Low smoothness bounds lie on steep region of runtime curve; extrapolation from 512-bit is dangerously optimistic.

## Revised TWIRL parameters (from [18], Appendix B)

### Polynomial (degree 5, Franke/Kleinjung)
- m = 2626... (≈1024-bit)
- s = 1,991,935.4
- t = exp(6.33) (much better than Appendix A polynomials)

### Parameter set (130nm technology)

| Parameter | Value |
|-----------|-------|
| y_r | 3.5×10⁹ |
| y_a | 2.6×10¹⁰ |
| z_r | 4.0×10¹¹ |
| z_a | 6.0×10¹¹ |
| S | 3.0×10²³ (A = s·B, B = 2.7×10⁸) |
| T(y_r,y_a) | ~1.3×10⁹ |

### Estimated yield (Table 10)

| Relation type | Count |
|---------------|-------|
| ff | 5.6×10⁷ |
| fp (1 large) | 3.0×10⁸ |
| pf (1 large) | 3.1×10⁸ |
| pp (1+1) | 1.7×10⁹ |
| fp₂ (2 large) | 6.7×10⁸ |
| pf₂ | 6.6×10⁸ |
| pp₂ | 7.9×10⁹ |
| **Total** | **1.9×10¹⁰** |

### Intermediate candidate counts (for filtering cost estimation)

| Stage | Count |
|-------|-------|
| Pass rational sieve (PRS) | 1.1×10²⁰ |
| Pass both sieves (PBS) | 5.0×10¹² |
| Pass primality test (PPT) | 6.2×10¹⁰ |
| Rational cofactor factorizations (RCF) | 4.9×10¹⁰ |
| Rational semi-smooth (RSS) | 3.4×10¹⁰ |
| Algebraic cofactor factorizations (ACF) | 2.7×10¹⁰ |

### Filtering cost estimate
- #RCF + #ACF ≈ 7.7×10¹⁰ factorizations of numbers ≤ max(z_r,z_a)² ≈ 3.6×10²³.
- Each factorization ~30ms on modern CPU.
- Total: 1 year on ~74 bare-bones PCs (parallel to TWIRL operation) — negligible compared to TWIRL cost.

## Technology scaling projections (90nm process)

Compared to 130nm: area ×½, speed ×2 → cost ×¼.

### Parameter set for 90nm (same cost as 130nm design)

| Parameter | Value |
|-----------|-------|
| y_r | 1.2×10¹⁰ |
| y_a | 5.5×10¹⁰ |
| z_r | 8.0×10¹¹ |
| z_a | 1.0×10¹² |
| S | 8.0×10²² |
| Total relations | 3.4×10¹⁰ |
| T(y_r,y_a)/ff | 2.9×10⁹ / 3.6 → ample safety margin |

### Parameter set for 768-bit RSA (for comparison)

| Parameter | Value |
|-----------|-------|
| y_r | 1.0×10⁸ |
| y_a | 1.0×10⁹ |
| z_r | 2.0×10¹⁰ |
| z_a | 3.0×10¹⁰ |
| S | 3.0×10²⁰ |
| Total relations | 2.1×10⁹ |

## Key limitations (explicit from paper)

1. **Large prime matching behavior** — "not yet well understood". Number of relations needed for T(y_r,y_a) independent cycles is uncertain. This is "the main reason that it is currently impossible to give reliable estimates".

2. **Asymptotic nature of ρ and σ₁ estimates** — systematically overestimate actual smoothness (Tables 4–6 show estimates ~10–20% higher). Correction terms exist but not applied.

3. **Polynomial quality** — Appendix A polynomials are "somewhat worse" than what an actual factoring attempt would use; estimates thus pessimistic. But Table 8 shows even t³ correction only improves yield by factor ~3, not enough to salvage original TWIRL parameters.

4. **Multi-polynomial variant** (Coppersmith) — performance highly dependent on constant E (ECM vs sieving cost). For current implementations E too large; unclear for dedicated hardware.

5. **Sieving region shape** — rectangular region assumed; non-rectangular may give same yield with smaller S, but "hardly a concern" for yield computations.

## Practical conclusions

| Question | Answer |
|----------|--------|
| Can original TWIRL parameters (y=2.5×10⁸) factor RSA-1024? | **No** — yield far too low (Table 1). |
| Can y=1.5×10¹⁰ without partial relations work? | **No** — would require S~13000× larger. |
| Revised TWIRL parameters (y_r=3.5×10⁹, y_a=2.6×10¹⁰) plausible? | **Yes** — yield 1.9×10¹⁰ relations, filtering cost manageable. |
| Cost estimate (US$10M × year) realistic? | **Yes** for 130nm; 90nm reduces to ~US$1.1M×year. |
| Does Moore's law help? | **Yes** — TWIRL cost decreases faster than linearly due to wafer-scale integration. |

## Relation to other sources

- Builds on TWIRL preliminary draft (Shamir & Tromer 2003).
- Uses Dickman function and semi-smoothness probabilities from Canfield–Erdős–Pomerance (1983) and Bach–Peralta (1992).
- Polynomial selection improvements from Montgomery–Murphy (1999) and Murphy's PhD thesis (1999).
- Final parameters adopted in published TWIRL design (Crypto 2003).
