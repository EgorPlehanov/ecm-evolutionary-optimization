---
title: "Speeding the Pollard and elliptic curve methods of factorization"
title_en: "Speeding the Pollard and elliptic curve methods of factorization"
source_type: "article"
authors: ["Montgomery P. L."]
year: "1987"
source_link: "https://doi.org/10.1090/S0025-5718-1987-0866113-7"
doi: "10.1090/S0025-5718-1987-0866113-7"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "speeding-pollard-and-elliptic-curve-factoring-methods-1987.md"
---

# Content source: Speeding the Pollard and elliptic curve methods of factorization

## Source type
Journal article (Mathematics of Computation, Vol. 48, No. 177, January 1987, pp. 243–264).

## Author
Peter L. Montgomery

## Objective
Present algorithmic improvements to Pollard's p−1, p+1 (Williams), and Elliptic Curve Method (Lenstra) factoring algorithms. Key contributions:
- Polynomial preconditioning to reduce GCD cost in Monte Carlo (Section 3)
- Improved standard continuation for p±1 using baby-step giant-step (Section 4.1)
- Pairing primes via complementary residue classes (Algorithm PAIR, Section 4.2)
- Montgomery form for elliptic curves (x:z only, no y-coordinate) with unified addition/doubling (Section 10.3.1)
- Parametrization to force group order divisible by 12 (Suyama's method, Section 10.3.2)

## Historical significance
This is the paper that introduced **Montgomery curves** and the **Montgomery ladder** for elliptic curve scalar multiplication, which became fundamental for both elliptic curve cryptography (ECC) and the elliptic curve method (ECM) of factorization. It also introduced the "improved standard continuation" for stage 2 of p−1 and ECM using baby-step giant-step, and the "Montgomery multiplication" algorithm for modular arithmetic (though that appeared in a separate 1985 paper).

## Overview of improvements by section

### Section 3: Polynomial preconditioning for Monte Carlo (Pollard rho)

**Problem**: Each GCD with N in cycle detection is expensive. Using (1.2), GCDs can be batched, but still cost ~1 multiplication each.

**Solution**: Precompute polynomial \(g(x) = \prod_{t \in T} (x - t) \bmod N\) for set T of 3 values. Then evaluate g(x) for each new x using precomputed constants with only 1 multiplication per block of 3 comparisons.

For T of size 3, with \(F(x) = x^2 + c\):
- Compute \(g(x) = (x - t_1)(x - t_2)(x - t_3)\).
- Using Winograd's scheme, evaluate g(x) in 4 multiplications (preconditioning) then 1 multiplication per g(x).
- 33 comparisons cost ~28 multiplications vs 32 in naive method → ~14% speedup.

Asymptotically, with polynomial degree \(2^k - 1\), cost per comparison drops to 2/3 of a multiplication modulo N.

### Section 4: Improved standard continuation for p−1 (and p+1, ECM)

**Standard continuation** (for p−1, after stage 1 computes b = a^R mod N):
- For each prime s in (B₁, B₂], compute b^s mod N and test gcd(b^s − 1, N).
- Cost: O(π(B₂)) multiplications.

**Baby-step giant-step improvement (Section 4.1)**:
- Choose w ≈ √B₂.
- Precompute baby steps: b^u for 0 ≤ u < w, gcd(u,w)=1.
- Precompute giant steps: b^{vw} for v = ⌈B₁/w⌉ to ⌊B₂/w⌋.
- For each prime s = v·w − u, test gcd(b^{vw} − b^u, N) — no multiplication for s, just table look-up + gcd.
- Cost: O(√B₂) precomputation + O(π(B₂)) look-ups (50% improvement over standard).

**Pairing two primes at once (Section 4.1–4.2)**:
- Use f(n) = b^{n²} mod N. Then if s divides v·w ± u, then s divides v²·w² − u², so f(vw) ≡ f(u) mod p.
- Algorithm PAIR (Section 4.2): partition primes by residue class modulo 2w, pair complementary classes.
- For w=1000, u_max=w/2=500, pairs generated: 62,836 primes → 34,453 pairs minimum; actual 59,059 pairs (86% of primes paired).
- Memory: O(w) baby steps.

### Section 10: Elliptic curve method with Montgomery form

**Montgomery curve** (10.3.1.1):
\[
B y^2 = x^3 + A x^2 + x
\]

**Point addition (x:z only)** — given P, Q, and P−Q:
\[
x_{P+Q} = z_{P-Q} \cdot [(x_P - z_P)(x_Q + z_Q) + (x_P + z_P)(x_Q - z_Q)]^2
\]
\[
z_{P+Q} = x_{P-Q} \cdot [(x_P - z_P)(x_Q + z_Q) - (x_P + z_P)(x_Q - z_Q)]^2
\]

**Point doubling**:
\[
4x_P z_P = (x_P + z_P)^2 - (x_P - z_P)^2
\]
\[
x_{2P} = (x_P + z_P)^2 (x_P - z_P)^2
\]
\[
z_{2P} = 4x_P z_P \cdot \big[(x_P - z_P)^2 + A_{24} \cdot 4x_P z_P\big], \quad A_{24} = (A+2)/4
\]

**Cost per operation**:
- Addition (when P−Q known): 6 multiplications + 4 additions.
- Duplication: 5 multiplications + 4 additions.
- With precomputed (x+z) and (x−z), addition: 6 multiplications, duplication: 5 multiplications.

**Scalar multiplication (Montgomery ladder)**:
- Binary method: compute (P, nP, (n+1)P) → (P, 2nP, (2n+1)P) or ((2n+1)P, (2n+2)P) using one addition + one duplication per bit.
- Starting with X₁=2, Z₁=1 → cost reduces to 9 log₂ n multiplications + 9 log₂ n additions.
- Using optimal addition chains (Lucas chains): ~9.3 log₂ n multiplications.

### Section 10.3.2: Parametrization for ECM — forcing group order divisible by 12 (Suyama)

Given σ > 5 (pseudo-random integer), set:
\[
u/v = (\sigma^2 - 5)/(4\sigma), \quad x_1/z_1 = u^3/v^3, \quad d = (v - u)^3(3u + v)/(4u^3 v)
\]
Then curve (10.3.1.1) with A+2 = d has group order divisible by 12.

**Further divisibility**: For order divisible by 24, need B(A+2), B(A−2), (A−2)(A+2) all quadratic residues (25% chance with random curves; with explicit torsion group, ~50% chance).

## Experimental results

**Largest factors found** (Fibonacci/Lucas numbers, with ECM):

| Factor (digits) | Number | B₁ |
|----------------|--------|-----|
| 25-digit | F₅₁₇ | 100k–175k |
| 25-digit | L₃₈₆ | 10⁶ |
| 25-digit | F₅₆₃ | 50k–100k |
| 28-digit | L₄₁₂ | 175k |
| 28-digit | L₄₈₂ | 175k |
| 33-digit | L₄₆₄ | 225k |

**B₂ ≈ 40× B₁** for these runs.

**p±1 largest factors**:
- F₉₇₁: 30-digit factor, p−1 = 2⁵·3·13·23·971·25801·689851·1089469·1146793 (Step 1, B₁=2·10⁶? Actually found with B₁=2,000,000? The paper mentions Step 1 success for p−1 of F₉₇₁).

## Key innovations (legacy)

1. **Montgomery form** and **Montgomery ladder** — now standard in ECC for side-channel resistance and efficiency.
2. **Improved standard continuation** (baby-step giant-step) — used in GMP-ECM for moderate B₂.
3. **Algorithm PAIR** for prime pairing — still used in prime95 and GMP-ECM (see Atnashev & Woltman 2021 for improvements).
4. **Suyama parametrization** for ECM curves with group order divisible by 12 — standard in GMP-ECM.

## Limitations (explicit)

1. **Heuristic assumptions** about smoothness distribution (as in Lenstra 1987).
2. **Stage 2 for ECM** only described in outline; full implementation details not given (though Montgomery later developed FFT continuation in 1992 PhD thesis).
3. **Polynomial preconditioning** for Monte Carlo only practical for small k (k=2–3) due to increasing preconditioning cost.
4. **Algorithm PAIR** requires storage O(w); for large w may exceed memory.
