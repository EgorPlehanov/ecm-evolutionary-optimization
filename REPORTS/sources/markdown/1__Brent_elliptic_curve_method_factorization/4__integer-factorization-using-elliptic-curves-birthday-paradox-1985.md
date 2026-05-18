---
title: "Some integer factorization algorithms using elliptic curves"
title_en: "Some integer factorization algorithms using elliptic curves"
source_type: "article"
authors: ["Brent R. P."]
year: "1985"
source_link: "https://doi.org/10.1016/S0167-5060(08)71909-3"
doi: "10.1016/S0167-5060(08)71909-3"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "integer-factorization-using-elliptic-curves-birthday-paradox-1985.md"
---

# Content source: Some integer factorization algorithms using elliptic curves

## Source type
Conference paper (Australian Computer Science Communications, 1986). Originally presented 24 September 1985, revised 10 December 1985.

## Author
Richard P. Brent (Australian National University)

## Historical significance
This is the **first published paper to propose a second phase (stage 2) for the Elliptic Curve Method**, introducing the "birthday paradox continuation" which speeds up ECM by a factor of ~4 for 20-digit factors. The paper predates Montgomery's "Speeding the Pollard and elliptic curve methods of factorization" (1987) and Montgomery's FFT continuation (1992). It also introduces the use of fast polynomial evaluation for stage 2 (anticipating Montgomery's FFT continuation).

## Objective
Improve Lenstra's original one-phase ECM (1985) by adding a second phase (stage 2) that searches for primes where the group order is smooth except for one large prime factor, using a birthday-paradox collision search. Analyze expected performance using Dickman's function ρ(α) and the two-prime smoothness function μ(α,β).

## Lenstra's original one-phase ECM (Section 5)

**Algorithm**: For a trial with bound \(B_1 = p^{1/\alpha}\):
- Choose random elliptic curve \(y^2 = x^3 + ax + b\) (mod N) and random point P.
- Compute \(Q = kP\) where \(k = \prod_{p \le B_1} p^{\lfloor \log B_1 / \log p \rfloor}\).
- If the group order \(g = |G|\) is \(B_1\)-smooth, then \(Q = I\) (point at infinity) modulo p, and \(\gcd(z_Q, N)\) reveals p.

**Success probability per trial**: ≈ ρ(α) (Dickman's function, probability a random integer near p has largest prime factor ≤ p^{1/α}).

**Expected work**:
\[
W_1(\alpha) = \frac{K_1 B_1}{\rho(\alpha)} \quad \text{with} \quad K_1 \approx 11/\log 2 \approx 15.87
\]
Minimization gives asymptotically:
\[
\log W_1 \sim \sqrt{2 \log p \log \log p}
\]

**Optimal α** for given p satisfies \(\log p = \alpha \rho(\alpha-1)/\rho(\alpha) \sim \alpha^2 \log \alpha\).

## Birthday paradox two-phase algorithm (Section 6)

**Key idea**: After stage 1 computes Q = kP, suppose the group order g has second-largest prime factor n₂ ≤ B₁ and largest prime factor n₁ in (B₁, B₂] with B₂ = B₁^β. Then Q ≠ I but order of Q is n₁.

**Stage 2 algorithm**:
- Generate r pseudo-random multiples Qᵢ = aᵢ·Q (using linear functions aᵢ = bᵢ for efficiency).
- Compute product:
\[
d = \prod_{1 \le i < j \le r} (y_i - y_j) \pmod{N}
\]
- If any Qᵢ = Qⱼ in G (mod p), then p divides (y_i - y_j) and thus p divides d.
- By birthday paradox, probability of collision ≈ 1 - exp(-r²/(2n₁)).

**Effect of folding by inverse**: Use x-coordinates instead:
\[
D = \prod_{1 \le i < j \le r} (x_i - x_j) \pmod{N}
\]
Since (x, y) and (x, -y) are inverses, this effectively folds the group → effective group size n₁/2. Probability ≈ 1 - exp(-r²/n₁).

**Parameter relation**: Choose r such that r² = n₁ ln 2 ≈ mᵝ ln 2, where m = B₁ = p^{1/α}. Then:
\[
\beta = \frac{2\ln r - \ln\ln 2}{\ln m}
\]

**Success probability per trial**: μ(α,β) (probability that n₁ ≤ mᵝ and n₂ ≤ m), given by:
\[
\mu(\alpha,\beta) = \rho(\alpha) + \int_{\alpha-\beta}^{\alpha-1} \frac{\rho(t)}{\alpha-t} dt
\]

## Fast polynomial evaluation for stage 2 (Section 7)

Instead of computing all O(r²) pairs directly, construct polynomial:
\[
P(x) = \prod_{j=1}^{r} (x - x_j) = \sum_{j=0}^{r-1} a_j x^j
\]
Then \(P'(x_j) = \prod_{i \neq j} (x_j - x_i)\), and:
\[
D^2 = \prod_{j=1}^{r} P'(x_j)
\]

**Complexity**: Using Karatsuba (M(r) = O(r^{log₂ 3}) ≈ O(r^{1.585})), D² can be evaluated in O(M(r)) time, reducing stage 2 cost from O(r²) to O(r^{1+ε}) for ε = log₂ 3 - 1 ≈ 0.585.

**Asymptotic speedup**: For fixed ε, β = 2/(1+ε) gives balanced phases, and:
\[
\frac{\rho(\alpha)}{\mu(\alpha,\beta)} = O\left(\frac{\ln\ln p}{(\ln p \ln\ln p)^{1/(1+\varepsilon)}}\right)
\]
With optimal ε→0 (Toom-Cook), speedup ≈ O(ln p).

## Optimal parameter selection (Section 8, Table 1)

Expected work W (in modular multiplications) for finding p-digit factor (log₁₀ W):

| log₁₀ p | Alg 1 (rho) | Alg 2 (Lenstra, 1-phase) | Alg 3 (2-phase, ε=1) | Alg 4 (2-phase, ε=0.585) |
|---------|-------------|--------------------------|----------------------|--------------------------|
| 6 | 3.49 | 4.67 | 4.09 | 4.26 |
| 8 | 4.49 | 5.38 | 4.76 | 4.91 |
| 10 | 5.49 | 6.03 | 5.39 | 5.53 |
| 12 | 6.49 | 6.62 | 5.97 | 6.07 |
| 14 | 7.49 | 7.18 | 6.53 | 6.60 |
| 16 | 8.49 | 7.71 | 7.05 | 7.12 |
| 18 | 9.49 | 8.21 | 7.56 | 7.59 |
| 20 | 10.49 | 8.69 | 8.04 | 8.05 |
| 30 | 15.49 | 10.85 | 10.22 | 10.14 |
| 40 | 20.49 | 12.74 | 12.11 | 11.97 |
| 50 | 25.49 | 14.44 | 13.82 | 13.62 |

**Observations**:
- Algorithm 3 (2-phase, ε=1) is 4–4.5× faster than Algorithm 2 (1-phase Lenstra).
- Algorithm 3 is faster than Pollard rho (Algorithm 1) for p ≥ 10¹⁰.
- Algorithm 4 (fast polynomial evaluation) is slightly better than Algorithm 3 for p ≥ 10²².

**Example**: With work budget 10¹⁰ multiplications, maximum factor size:
- Alg 1 (rho): ≈ 10¹⁹ digits (actually 19 decimal digits)
- Alg 2 (Lenstra): ≈ 10²⁶ digits
- Alg 3 (2-phase): ≈ 10²⁹ digits

## Optimal parameters for Algorithm 3 (Table 2, p=10²⁰)

| log₁₀ p | α | β | m = p^{1/α} | r | Expected trials T | m/T | w₂₁ (phase2/phase1 work) | Speedup S |
|---------|---|---|--------------|----|-------------------|-----|---------------------------|-----------|
| 10 | 3.72 | 1.56 | 484 | 1041 | 2.1 | 0.64 | 404 | 4.37 |
| 20 | 4.65 | 1.35 | 19970 | 66914 | 7.5 | 0.47 | 1354 | 4.46 |

**Observation**: m/T ≈ 135 for p ≈ 10²⁰ — useful heuristic for adaptive parameter selection.

## Experimental verification (Table 3)

Tests on numbers with p ≈ 10¹² showed observed work close to expected, with algorithms performing slightly better than predicted.

## Further refinements (Section 9)

1. **Better choice of random points** (exponent e > 1): Use aᵢ = bᵢᵉ with linear bᵢ. Number of solutions of xᵉ = 1 mod n₁ is gcd(e, n₁-1). Using e=6 gave speedup ~6.6 over 1-phase for p≈10²⁰.
2. **Other second phases**: Conventional P-1 stage 2 adapted to ECM gives speedup O(log log p) — asymptotically weaker than birthday paradox's O(log p).
3. **Better random elliptic curves** (Suyama): Ensures group order divisible by 12 → effectively reduces p to p/12 → significant practical speedup.
4. **Faster group operations** (Montgomery form): Use by² = x³ + ax² + x (mod N), dispense with y-coordinate. Saves ~43% over Weierstrass form.

## Legacy and relation to later work

- **Montgomery (1987)**: Improved the birthday paradox continuation with a baby-step giant-step approach (the "improved standard continuation") and introduced Montgomery curves.
- **Montgomery (1992)**: FFT continuation using fast polynomial arithmetic — this paper anticipated that idea (Section 7).
- **GMP-ECM**: Implements the birthday paradox continuation for small B₂ and FFT continuation for large B₂.
- **This paper's stage 2** is still used in some ECM implementations when B₂ is modest.

## Limitations (explicit)

1. **Heuristic assumptions**: Group order g is treated as random integer near p; distribution of prime factors in "short" interval is assumed uniform (still unproven).
2. **Birthday paradox stage 2** requires O(√n₁) steps and O(r²) multiplications — FFT continuation (Montgomery 1992) is asymptotically better.
3. **Experimental verification** only for p ≈ 10¹² (much smaller than modern ECM records).
4. **No hardware implementation** — purely algorithmic and theoretical.
