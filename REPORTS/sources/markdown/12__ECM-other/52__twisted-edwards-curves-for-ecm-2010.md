---
title: "Twisted Edwards Curves for the Elliptic Curve Method of Factorization"
title_en: "Twisted Edwards Curves for the Elliptic Curve Method of Factorization"
source_type: "article"
authors: ["Bernstein D. J.", "Birkner P.", "Lange T."]
year: "2010"
source_link: "unknown (provided PDF: 2010-367.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "twisted-edwards-curves-for-ecm-2010.md"
---

# Content source: Twisted Edwards Curves for the Elliptic Curve Method of Factorization

## Source type
Academic paper (preprint/IACR archive, 2010).

## Authors affiliation
1. University of Illinois at Chicago, USA
2. Université de Versailles Saint-Quentin-en-Yvelines, France
3. Technische Universiteit Eindhoven, Netherlands

## Objective
Improve the price-performance ratio of ECM (Elliptic Curve Method) by constructing a = −1 twisted Edwards curves with high torsion (Z/2×Z/4, Z/8, Z/6) and positive rank, and comparing their effectiveness against traditional Montgomery/Suyama curves and Z/12 Edwards curves.

## Core methodology
- **Curve construction**: Parametrize twisted Edwards curves with a = −1 and torsion groups Z/2×Z/4, Z/8, Z/6 using rational parameters.
- **Search for small coefficients**: Enumerate small integer parameters to find curves with small d and non-torsion points of small height.
- **Infinite families**: Derive elliptic curves whose rational points generate infinite families of ECM curves with desired torsion and rank ≥1.
- **Effectiveness measurement**: For each b-bit prime (b = 15…26), test 1000 curves per torsion type using standard EECM parameters (B₁, d₁) from [4], counting primes found.
- **Cost metric**: Total multiplications + squarings in stage 1+2 divided by number of primes found.

## Key theoretical results

### Torsion group Z/2×Z/4 (a = −1)
- Condition: d = −e⁴ for some rational e.
- Parameterization via elliptic curve: V² = U³ − 11664U/25.
- Best curve found: −x² + y² = 1 − (77/36)⁴·x²y², non-torsion point (12/343, 1404/1421).

### Torsion group Z/8 (a = −1)
- Parameterization: u ∈ Q\{0}, x₈ = (2u²−1)/(2u), y₈ = (2u²+1)/(2u), d = 16u⁴/(4u⁴−1)².
- Infinite family from elliptic curve: S² = R³ + 48R, point (4,−16) generates rank.
- Only 3 small-coefficient curves found after extensive search.

### Torsion group Z/6 (a = −1)
- Suyama curves translated to a = −1 twisted Edwards form.
- Parameterization: u ∈ Q\{0,±1}, x₃ = (u²−1)/(2u), y₃ = (u−1)²/(2u), d = −16u³(u²−u+1)/((u−1)⁶(u+1)²).
- Infinite family from curve: V² = U³ − U²/2304 − 5U/221184 + 1/28311552, point (1/192, 1/4608) generates rank 1.

## Effectiveness results (22-bit primes as reference)

| Curve type | Best curve primes found | Median primes found | Cost speedup vs prior |
|------------|------------------------|---------------------|----------------------|
| Z/2×Z/4 (a=−1) | 46,150 | ~45,700 | −0.4% vs Z/12 prior |
| Z/8 (a=−1) | ~46,600 | ~46,200 | — |
| Z/6 (a=−1) | ~48,000 | 47,687 | +4% primes, +4% speed |
| Z/12 (a=1) | ~47,900 | 47,521 | baseline |
| Z/2×Z/8 (a=1) | ~46,800 | 46,501 | worse |

### Overall winner for 22-bit primes (price-performance)
Curve: −x² + y² = 1 − (6517/196608)·x²y²
- Torsion: Z/6, non-torsion point (336/527, 80/67)
- Finds 4% more primes than the Z/12 curve from [4] and runs 4% faster (a=−1 speedup) → ~8% overall improvement.

Runner-up: −x² + y² = 1 − (13312/18225)·x²y², non-torsion point (825/2752, 1521/1504).

## Cost ratio plots (Figures 7.1–7.4)
For b = 15…26, the cost (multiplications per prime found) varies significantly across curves. Z/6 (a=−1) consistently shows the lowest cost ratio (best price-performance), followed by Z/12 (a=1), then Z/2×Z/8 (a=1), then Z/8 (a=−1), and worst Z/2×Z/4 (a=−1).

## Comparison with prior work
- Prior ECM implementations used Montgomery curves (Suyama) or Weierstrass curves.
- [4] introduced Edwards curves with a=1 and Z/12 or Z/2×Z/8 torsion.
- This paper shows a=−1 curves can be competitive despite smaller torsion, due to 8M addition (vs 9M for a=1) and unexpectedly higher effectiveness (especially Z/6).

## Limitations (explicit from source)
- Computations only for b ≤ 26 (15–26 bit primes); ECM is not useful for b=15 (Pollard's rho better).
- Effectiveness improvements may decrease slowly with larger b; authors plan to extend computations.
- EECM parameters (B₁,d₁) fixed from prior work; different parameters may change rankings.
- Small-coefficient speedups (faster additions) ignored in cost counts.
- Greedy selection of curves may not be optimal for sequences after p−1 failures.

## Conclusions
- a = −1 twisted Edwards curves with Z/6 torsion achieve better price-performance than previously known Z/12 curves.
- The speed advantage (8M vs 9M per addition) outweighs the loss in torsion size.
- Some a = −1 curves are surprisingly more effective at finding primes than higher-torsion curves.
- Authors plan to maintain a web page with best curves for each b and explore optimal ECM sequences.

## Practical value
- Directly applicable to ECM implementations (e.g., EECM-MPFQ) as a patch.
- Improves GNFS cofactorization step.
- Provides concrete curve parameters for different prime sizes.
