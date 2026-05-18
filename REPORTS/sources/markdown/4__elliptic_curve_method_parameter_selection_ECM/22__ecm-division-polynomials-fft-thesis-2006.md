---
title: "Elliptic Curve Factoring Method via FFTs with Division Polynomials"
title_en: "Elliptic Curve Factoring Method via FFTs with Division Polynomials"
source_type: "phd_thesis"
authors: ["Li Z."]
year: "2006"
source_link: "https://docs.lib.purdue.edu/dissertations/AAI3255695/"
doi: "none"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "ecm-division-polynomials-fft-thesis-2006.md"
---

# Content source: Elliptic Curve Factoring Method via FFTs with Division Polynomials (PhD Thesis)

## Source type
Doctoral dissertation, Purdue University, December 2006. Advisor: Prof. Samuel S. Wagstaff, Jr.

## Objective
Develop a practical implementation of Schnorr's 2001 proposal to use division polynomials in ECM, enabling simultaneous testing of many elliptic curves via FFT, and analyze its complexity, success probability, and memory optimization for numbers of the form \(s^n \pm 1\).

## Core innovation — implied univariate division polynomial

Standard ECM tests one curve at a time with a fixed point \(P\) and random \(a\). This method:

1. Fixes a rational point \(P = (x, y)\).
2. Parameterizes elliptic curves by \(a\): \(b = y^2 - x^3 - ax\).
3. Defines the **\(m\)-th implied univariate division polynomial** \(\bar{\psi}_m(a)\) via division polynomials \(\psi_m\).
4. Uses property (3.8): \(m \cdot P = \left( \frac{\phi_m}{\psi_m^2}, \frac{\omega_m}{\psi_m^3} \right)\). The denominator of the \(x\)-coordinate is \(\bar{\psi}_m(a)^2\).
5. If \(\bar{\psi}_m(a_i) \equiv 0 \pmod{p}\) but \(\not\equiv 0 \pmod{N}\), then \(\gcd(\bar{\psi}_m(a_i), N)\) reveals \(p\).
6. Evaluates \(\bar{\psi}_m\) at \(m^2/4\) points \(a = s^i\) simultaneously via FFT and cyclic convolutions.

## Key theoretical results

### Theorem 3.2.1 — Degree of implied division polynomial

\[
\deg(\bar{\psi}_m) = 
\begin{cases}
\frac{m^2}{4} - 1 & m \text{ even} \\[4pt]
\frac{m^2 - 1}{4} & m \text{ odd}
\end{cases}
\]

### Theorem 3.3.2 — Complexity of generating \(\bar{\psi}_m\)

Algorithm 3.3.1 (dynamic programming + FFT) computes \(\bar{\psi}_m\) using **\(O(m^2 \ln m)\)** arithmetic operations.

*Proof sketch*: \(m = 2^e\) loops; \(i\)-th loop degree \(O(2^{2i})\); FFT cost \(O(i \cdot 2^{2i})\); sum over \(i\) gives \(O(e \cdot 2^{2e}) = O(m^2 \ln m)\).

### Theorem 4.1.3 — Probability of success

For \(B = p^{1/t}\) (\(t = \ln p / \ln B\)), probability that a random curve in the interval \((p+1-2\sqrt{p}, p+1+2\sqrt{p})\) has \(B\)-smooth order is \(\varepsilon(t) \approx t^{-t} \cdot e^{(1-\ln\ln t)(t + t/\ln t)}\).

With \(m^2/4\) independent curves (geometric progression \(a = s^i\)):

\[
\text{Pr(success)} = 1 - (1 - \varepsilon(t))^{m^2/4}.
\]

### Corollary 4.1.1 — Lower bound

\[
\text{Pr(success)} \geq 1 - \exp\left( -\frac{m^2}{4} (t^{-t})^{1 + \frac{\ln\ln t}{\ln t} - \frac{1}{\ln^2 t}} \right).
\]

### Theorem 4.5.1 — Main algorithm complexity (Algorithm 4.1.1)

With geometric progression evaluation (Algorithm 4.4.1): **\(O(m^2 \ln m)\)** arithmetic operations.

### Corollary 4.5.1 — Random evaluation case

With random \(a\) values (Algorithm 4.4.2): **\(O(m^2 \ln^2 m)\)** operations.

## Optimization for numbers of the form \(s^n \pm 1\) (Mersenne, Fermat, etc.)

For \(N = s^n \pm 1\) (family \(\mathcal{F}_n\)), note \((s^i)^n \equiv \pm 1 \pmod{N}\). Work modulo \(x^n \pm 1\) in polynomial arithmetic.

### Algorithm 4.6.1 (full \(m^2/4\) curves distributed as \(m^2/(4n)\) loops)

Calls Algorithm 3.3.1 \(m^2/(4n)\) times; each call works with degree \(n\) polynomials.

### Theorem 4.6.1 — Complexity for \(\mathcal{F}_n\)

\[
O(m^2 \ln m \ln n) \quad \text{arithmetic operations}.
\]

### Algorithm 4.6.2 — Fixed number of curves \(k\) (practical version)

### Theorem 4.6.2

Complexity: \(O(k \ln m \ln n)\). Probability of success:

\[
\geq 1 - \exp\left( -k (t^{-t})^{1 + \frac{\ln\ln t}{\ln t} - \frac{1}{\ln^2 t}} \right).
\]

## Implementation details

- **Multiple-precision arithmetic**: radix \(2^{30}\), array-based representation (Silverman's package).
- **FFT**: Implemented over finite rings; \(D^* = 2^k \geq 2D\) with principal roots of unity.
- **Chinese Remainder Theorem**: Compute modulo several 30-bit primes \(p_i\) of form \(D^* \cdot (r+j)+1\) (guarantees \(D^*\)-th roots of unity exist), then reconstruct modulo \(N\).
- **Cyclic convolution** (4.7): \(x \otimes y = DFT^{-1}(DFT(x) \star DFT(y))\), used in polynomial evaluation.

## Experimental results

Hardware: 1.86GHz PC, 4GB DDR2 SDRAM at 533MHz.

| \(N\) | Digits of found factor | Time | Parameters (\(B, k\)) |
|-------|------------------------|------|----------------------|
| \(2^{139} - 1\) | 13 | Several minutes | \(B=146, k\approx 10^4\) |
| \(2^{149} - 1\) | 20 | 24 minutes | \(B=719, k\approx 10^5\) |
| \(5^{430} + 1\) | 47 | 1 week | \(B=166810, k\approx 10^9\) |
| \(2^{353} + 1\) | 37 | 20 hours | \(B=12915, k\approx 10^7\) |
| \(2^{373} + 1\) | 48 | 10 days | \(B=63096, k\approx 10^{10}\) |

> The first 48-digit ECM factor was found less than 10 years before this thesis, after tens of thousands of computer-hours. Current ECM record is 67 digits.

## Limitations and open problems (explicit from thesis)

1. **Independence assumption** (Conjecture 4.4.1): Probability distributions for different \(a = s^i\) are assumed independent — not proved.
2. **No second step**: After failure, the algorithm restarts with larger \(B\) rather than reusing information (unlike standard 2-step ECM).
3. **Point choice**: Does choice of \((x,y)\) matter? Open problem — needs rationalization.
4. **Choice of base \(s\) for random \(N\)**: For \(\mathcal{F}_n\), \(s\) equals the base. For random \(N\), no general rule — could use Shanks' baby-step-giant-step to estimate order.
5. **Memory**: Without optimization (Section 4.6), storing \(\bar{\psi}_m\) of degree \(O(m^2)\) limits feasible \(m\).

## Practical conclusions (from thesis)

- Algorithm 4.1.1 works but memory-bound for large \(m\).
- For \(N = s^n \pm 1\) (or divisors thereof), optimization in Section 4.6 removes memory restriction entirely, allowing very large \(m\).
- Implementation found competitive results (48-digit factor in 10 days) using a single PC, comparable to conventional ECM at the time.
- Goal: 60-digit primes; expectation of 70-digit primes.

## Relation to previous work

- Builds on Schnorr (2001) — solved memory issues.
- Uses Dickman's function analysis from Knuth & Trabb Pardo (1976), Canfield–Erdős–Pomerance (1983).
- Parameter selection guidelines from Silverman & Wagstaff (1993).
- FFT polynomial evaluation from Crandall & Pomerance (2001).