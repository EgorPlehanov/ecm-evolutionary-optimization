---
title: "Theorems on factorization and primality testing"
title_en: "Theorems on factorization and primality testing"
source_type: "article"
authors: ["Pollard J. M."]
year: "1974"
source_link: "https://doi.org/10.1017/S0305004100049252"
doi: "10.1017/S0305004100049252"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "pollard-p-minus-1-and-rho-1974.md"
---

# Content source: Theorems on factorization and primality testing

## Source type
Peer-reviewed journal article (Mathematical Proceedings of the Cambridge Philosophical Society, Vol. 76, No. 3, Nov. 1974, pp. 521–528).

## Author affiliation
J. M. Pollard — Mathematics Department, Plessey Telecommunications Research, Taplow Court, Taplow, Maidenhead, Berkshire, UK.

## Objective
Prove theoretical upper bounds for the number of arithmetic operations required to factor an integer or test it for primality, using the fast Fourier transform (FFT) and a device from Shanks' class group method. Present a practical factoring algorithm (now known as Pollard's p−1 method) with an illustrative example.

## Core content summary

### 1. Theoretical results (Theorems 1–2)

**Theorem 1** (Factor finding):
For any \(0 < \alpha < 1\) and \(\delta > 0\), there exists a multi‑tape Turing machine that can determine whether \(n\) has a prime factor \(\leq n^\alpha\) (and find such a factor) in \(O(n^{\alpha/2 + \delta})\) operations.

**Corollary**: Complete factorization of \(n\) in \(O(n^{1/2 + \delta})\) operations (take \(\alpha = 1/2\)).

**Theorem 2** (Primality testing):
For any \(\delta > 0\), there exists a machine that can test \(n\) for primality in \(O(n^{1/2 + \delta})\) operations.

**Method**: Uses FFT (Schönhage‑Strassen) for polynomial multiplication (Lemma 1) and an algorithm to test whether \(\gcd(a^m - 1, n) > 1\) for some \(m \leq M\) (Lemma 2). The primality test in Theorem 2 is more complicated and relies on Lemma 4 (not covered in detail here).

### 2. Practical factoring algorithm (Section 4)

This is the **Pollard p−1 method** (though not named as such in the paper).

**Idea**:
- For a prime factor \(p\) of \(n\), Fermat's theorem gives \(a^{p-1} \equiv 1 \pmod{p}\).
- If all prime factors of \(p-1\) are \(\leq L\) (smooth), and we compute \(a^P \bmod n\) where \(P\) is a multiple of \(p-1\), then \(p \mid \gcd(a^P - 1, n)\).

**Two‑stage algorithm**:

**Step 1**:
- Choose small integer \(a > 1\) (e.g., \(a=2\)).
- Let \(P\) be the product of all primes \(\leq L\), each raised to a suitable power (e.g., \(p^{\lfloor \log_p L \rfloor}\)).
- Compute \(b \equiv a^P \pmod{n}\) (using binary exponentiation).
- Compute \(d = \gcd(b - 1, n)\).
- If \(1 < d < n\) → factor found.
- If \(d = n\) → try smaller \(L\).
- If \(d = 1\) → proceed to Step 2.

**Step 2** (allows one larger prime factor of \(p-1\) between \(L\) and \(M\)):
- Compute \(F_m \equiv b^m - 1 \pmod{n}\) for primes \(m\) with \(L < m \leq M\).
- Compute products of \(F_m\) and take gcd at intervals.
- If \(\gcd(F_m, n) > 1\) for some \(m\), factor found.

**Optimizations**:
- Precompute powers \(b^2, b^4, \dots, b^{2D}\) up to the largest gap between consecutive primes.
- Accumulate product of \(F_m\) to reduce gcd operations.

### 3. Numerical example (from the paper)

A difficult factorization from Brillhart and Selfridge (1967):

\[
2^{107} + 2^{54} + 1 = 843589 \cdot 8174912477117 \cdot 23528569104401
\]

For the largest factor \(p_3 = 23528569104401\):
\[
p_3 - 1 = 2^4 \cdot 5^2 \cdot 67 \cdot 107 \cdot 199 \cdot 41231
\]
Thus if we take \(L \geq 199\) and \(M \geq 41231\), Step 1 finds the factor (since all prime factors of \(p_3-1\) except 41231 are \(\leq L\), and Step 2 catches the large prime 41231).

Another favorable case: \(2^{150} + 2^{75} + 1\) requires only Step 1 with \(L \geq 61\).

### 4. Key lemmas

**Lemma 1** (FFT polynomial multiplication):
Given sequences \(a_i, b_i\) of length \(N\) and \(|a_i|,|b_i| < M\), can compute all convolution sums \(c_k = \sum_{i+j=k} a_i b_j\) in \(O(N^{1+\epsilon} M^{\epsilon})\) operations for any \(\epsilon > 0\).

**Lemma 2** (Finding \(m\) with \(\gcd(a^m-1,n) > 1\)):
For given \(a, n, M\), can determine the least \(m \leq M\) with \(\gcd(a^m-1,n) > 1\) (if any) in \(O(M^{1/2+\epsilon} n^{\epsilon})\) operations.

**Method**: Write \(m = -u + vL\) with \(L = \lfloor \sqrt{M} \rfloor\), compute polynomial \(f(x) = \prod_{u=0}^{L-1} (x - a^u)\) modulo \(n\), then evaluate \(f(a^{vL})\) for \(v=1,\dots,L\) using FFT.

**Lemma 3** (Bound on least \(k\)‑th power non‑residue):
For any \(\delta > 0\), there exists \(k \geq 2\) such that the least \(k\)‑th power non‑residue of a prime \(p\) is \(O(p^{\delta})\).

This is used in the primality test (Lemma 4) to handle composite numbers that might otherwise escape detection.

### 5. Comparison of theoretical and practical approaches

| Aspect | Theoretical (Theorems 1–2) | Practical (Section 4) |
|--------|---------------------------|----------------------|
| Goal | Prove existence of algorithm with given complexity | Provide usable method for factoring |
| Key tool | FFT (Schönhage‑Strassen) | Binary exponentiation, gcd |
| Complexity | \(O(n^{1/2+\delta})\) | Not analyzed, but depends on smoothness of \(p-1\) |
| Use case | Theoretical bound | Searching for medium factors of huge numbers |
| Limitations | Impractical constants, huge overhead | Fails if \(p-1\) has large prime factor |

### 6. Practical significance of Section 4

The algorithm described in Section 4 is now known as **Pollard's p−1 method**. Its key features:

- **Finds prime factor \(p\) when \(p-1\) is smooth**.
- **Two‑stage version** allows one larger prime factor between bounds.
- **Works well for numbers of special forms** (e.g., Cunningham numbers \(b^n \pm 1\)) where \(p-1\) often has many small factors.
- **Computationally inexpensive** per curve (unlike ECM, which came later).

**Example of when p−1 succeeds**: \(p = 23528569104401\) from \(2^{107}+2^{54}+1\), since \(p-1 = 2^4\cdot5^2\cdot67\cdot107\cdot199\cdot41231\) is smooth except for the prime 41231, which is caught in Stage 2.

## Key limitations (explicit from source)

- The theoretical algorithm (Theorems 1–2) has huge constant factors and is not practical.
- The practical p−1 method fails if \(p-1\) has a large prime factor (e.g., safe primes \(p = 2q+1\) with \(q\) prime).
- Step 2 requires storing tables of differences; memory may be an issue for large \(M\).
- No rigorous bound given for the practical method; it is heuristic.

## Impact and legacy

- Introduced **Pollard's p−1 factorization method** (Section 4), which remains in use today (e.g., in GMP‑ECM).
- Introduced **Pollard's Rho method**? Not in this paper; that appeared in Pollard (1975, BIT). This paper is the p−1 method.
- Used FFT for polynomial multiplication, later applied in the Number Field Sieve.
- Theorem 1 and Lemma 2 anticipate the use of smooth numbers and convolution techniques later used in QS and NFS.

## References (selected)
- Cooley & Tukey (1965) — FFT
- Schönhage & Strassen (1971) — Fast multiplication
- Lehman (1974) — \(O(n^{1/4+\epsilon})\) factoring (to appear)
- Shanks (1970) — Class number method
- Brillhart & Selfridge (1967) — Factorization of \(2^n \pm 1\)
