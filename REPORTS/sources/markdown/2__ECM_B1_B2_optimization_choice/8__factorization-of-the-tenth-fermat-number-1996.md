---
title: "Factorization of the tenth Fermat number"
title_en: "Factorization of the tenth Fermat number"
source_type: "article"
authors: ["Brent R. P."]
year: "1996"
source_link: "https://doi.org/10.1090/S0025-5718-96-00710-8"
doi: "10.1090/S0025-5718-96-00710-8"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "factorization-of-the-tenth-fermat-number-1996.md"
---

# Content source: Factorization of the tenth Fermat number

## Source type
Journal article (Mathematics of Computation, 1996). Also INRIA Research Report RR-5834.

## Author and affiliation
- Richard P. Brent (Oxford University Computing Laboratory)

## Historical context

Fermat numbers: \(F_n = 2^{2^n} + 1\).

Known: \(F_0, F_1, F_2, F_3, F_4\) prime (Fermat primes). \(F_5, \ldots, F_{23}\) composite. No larger Fermat primes known.

### Prior factorizations (Table 1)

| n | Factorization | Method | Year | Discoverer |
|---|---------------|--------|------|------------|
| 5 | p3·p7 | Trial division | 1732 | Euler |
| 6 | p6·p14 | — | 1880 | Landry |
| 7 | p17·p22 | CFRAC | 1970 | Morrison & Brillhart |
| 8 | p16·p62 | B–P rho | 1980 | Brent & Pollard |
| 9 | p7·p49·p99 | SNFS | 1990 | Lenstra et al. |
| 10 | p8·p10·p40·p252 | ECM | 1995 | Brent (p40, p252) |
| 11 | p6·p6·p21·p22·p564 | ECM | 1988 | Brent (p21, p22, p564) |

## Complete factorization of \(F_{10}\)

Before this work: \(F_{10} = 45592577 \cdot 6487031809 \cdot c_{291}\) (c291 = 291-digit composite). Small factors found by Selfridge (1953) and Brillhart (1962).

**New 40-digit factor found October 20, 1995**:
\[
p_{40} = 4659775785220018543264560743076778192897
\]
Cofactor \(c_{291}/p_{40}\) proved prime (\(p_{252}\)).

Thus:
\[
F_{10} = 45592577 \cdot 6487031809 \cdot p_{40} \cdot p_{252}
\]

### Successful ECM parameters
- Curve: Montgomery form (5) with \(\sigma = 14152267\)
- \(B_1 = 2{,}000{,}000\)
- \(B_2\) chosen such that phase 2 time ≈ phase 1/2
- Birthday paradox continuation, \(e = 6\)
- Machine: 60 MHz SuperSparc, 10 curves in ~114 CPU hours

### Group order of successful curve
\[
g = p_{40} + 1 - 3674872259129499038
\]
\[
= 2^2 \cdot 3^2 \cdot 5 \cdot 149 \cdot 163 \cdot 197 \cdot 7187 \cdot 18311 \cdot 123677 \cdot 226133 \cdot 314263 \cdot 4677853
\]
Largest prime factor \(g_1 = 4677853\), second-largest \(g_2 = 314263\). Note \(B_1 = 2 \times 10^6\) but curve would succeed with \(B_1\) as low as 314263.

### Computational effort
- Total multiplications mod c291: ~\(1.4 \times 10^{11}\)
- ~240 Mips-years (SuperSparc) or ~140 Mflop-years (VP2200)
- Predicted optimal effort (Table 2): \(3.3 \times 10^{11}\) multiplications

## Factorization of \(F_{11}\) (1988)

\(F_{11} = 319489 \cdot 974849 \cdot p_{21} \cdot p_{22} \cdot p_{564}\)

Factors found by ECM:
- May 13, 1988: \(p_{22} = 3560841906445833920513\) (first, surprising — larger found before smaller)
- May 17, 1988: \(p_{21} = 167988556341760475137\)

Parameters: \(B_1 = 16{,}000\), 20 curves per run on VP100.

## ECM implementation details (Program C/D)

### Montgomery form (projective x:z only)
Equation: \(b y^2 z = x^3 + a x^2 z + x z^2\)

Addition (requires \(P_m\) and \(P_n\) with known \(P_{|m-n|}\)):
\[
\frac{x_{m+n}}{z_{m+n}} = \frac{z_{|m-n|}(x_m x_n - z_m z_n)^2}{x_{|m-n|}(x_m z_n - z_m x_n)^2}
\]
Cost: 11 multiplications (mod N).

Duplication:
\[
\frac{x_{2n}}{z_{2n}} = \frac{(x_n^2 - z_n^2)^2}{4x_n z_n (x_n^2 + a x_n z_n + z_n^2)}
\]
Cost: 5 multiplications.

### Phase 1
Compute \(P_r\) where \(r = \prod_{p \le B_1} p^{\lfloor \log B_1 / \log p \rfloor}\) using binary method. Cost \(K_1 B_1\) multiplications, \(K_1 = 11 / \log 2 \approx 15.87\).

Check success: \(\gcd(z_r, N) > 1\).

### Phase 2 (improved standard continuation)
Idea: precompute \(2dQ\) for \(0 < d \le D\) (baby steps). Compute \(mQ\) for \(m = 1, 2D+1, 4D+1, \ldots\) (giant steps).

If prime \(s = m + n\) with \(0 < n \le 2D\), test if \(\gcd(x_m z_n - x_n z_m, N) > 1\). Product over many (m,n) reduces GCD frequency.

Cost per prime: \(K_2\) multiplications, \(K_2 \approx 1\).

Total phase 2 cost \(\approx K_2 B_3\) where \(B_3 = \pi(B_2) - \pi(B_1) \approx B_2 / \log B_2\).

### Birthday paradox continuation (used for \(F_{10}\))
- Choose polynomial \(f(x) = x^e\) (or Dickson polynomial \(D_e\)).
- Build set \(S = \{f(i) Q \mid i = 1,\ldots,M\}\).
- Build set \(T = \{f(j) Q \mid j = 1,\ldots,M\}\).
- If prime \(s\) divides \(f(i) \pm f(j)\) for some i,j, then \(s\) may be found.
- \(e = 6\) used for \(F_{10}\); success probability increased but analysis more complex.

## Theoretical analysis of ECM performance

### Smoothness probabilities (Dickman–Vershik)
Let \(n_1(N) \ge n_2(N) \ge \cdots\) be prime factors of random integer N.

\(\rho(\alpha) = \Phi_1(1/\alpha)\) = probability \(n_1^\alpha \le N\).

\(\mu(\alpha, \beta) = \Phi_2(\beta/\alpha, 1/\alpha)\) = probability \(n_2^\alpha \le N\) and \(n_1^\alpha \le N^\beta\).

Functional equations:
\[
\alpha \rho'(\alpha) + \rho(\alpha-1) = 0 \quad (\alpha \ge 1)
\]
\[
\mu(\alpha, \beta) = \rho(\alpha) + \int_{\alpha-\beta}^{\alpha-1} \frac{\rho(t)}{\alpha-t} dt \quad (1 \le \beta \le \alpha)
\]

### Optimal parameters for phase 1
Let \(\alpha = \log p / \log B_1\). Probability one curve succeeds ≈ \(\rho(\alpha)\). Expected curves \(C_1 = 1/\rho(\alpha)\).

Work per curve ≈ \(K_1 B_1\). Expected work \(W(\alpha) = K_1 p^{1/\alpha} / \rho(\alpha)\).

Minimising \(W(\alpha)\) yields asymptotically:
\[
\log B_1 \sim \alpha \log \alpha,\quad \log C_1 \sim \alpha \log \alpha,\quad \log W \sim \sqrt{2 \log p \log \log p}
\]

### Phase 2 speedup
Expected work with (B₁,B₂): \(W = (K_1 B_1 + K_2 B_3) / \mu(\alpha,\beta)\) where \(\beta = \log B_2 / \log B_1\), \(B_3 \approx B_2 / \log B_2\).

Speedup factor from phase 2 (with standard continuation) ≈ \(\log \log p\).

### Table 2: Expected work (log₁₀ W_opt)

| Digits D | log₁₀ W_opt | τ(p) |
|----------|-------------|------|
| 20 | 7.35 | 1.677 |
| 30 | 9.57 | 1.695 |
| 40 | 11.49 | 1.707 |
| 50 | 13.22 | 1.716 |
| 60 | 14.80 | 1.723 |

τ(p) = \((\log W_{opt})^2 / (\log p \log \log p) \to 2\) as \(p \to \infty\) (slow convergence).

## ECM vs SNFS for Fermat numbers

For \(F_9\) (1990): SNFS took ~340 Mips-years. Brent shows \(p_{49}\) of \(F_9\) could have been found by ECM (rediscovered 1997 with ~73,000 curves, \(B_1=10^7\)).

For \(F_{12}\): five known small factors; sixth factor likely > \(10^{30}\). Probability from Vershik's theorem suggests ~6% chance that second-largest factor < \(10^{40}\). ECM continues but complete factorization may require quantum computer (Shor 1994).

## Primality proofs

- \(p_{40}\) prime via Lucas–Lehmer method: \(p_{40}-1\) fully factored, primitive root 5.
- \(p_{252}\) prime via Selfridge's Cube Root Theorem (since \(p_{252}-1 = F \cdot c_{158}\) with \(F > 2 \times 10^{93}\) and \(p_{252} < 2F^3 + 2F\)).
- \(p_{564}\) prime via Atkin–Morain ECPP (Morain 1988, 28 hours on SuperSparc).

## Open questions (from paper)

1. Can ECM find factors of \(F_{12}\)? Probability low but no alternative.
2. Complete factorization of \(F_{12}\) may require quantum computers.
3. Could the FFT continuation be implemented more efficiently?
4. When to switch from ECM to SNFS? Vershik's theorem gives heuristic.
