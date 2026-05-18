---
title: "Factoring Integers with the Number Field Sieve"
title_en: "Factoring Integers with the Number Field Sieve"
source_type: "book_chapter"
authors: ["Buhler J. P.", "Lenstra Jr. H. W.", "Pomerance C."]
year: "1993"
source_link: "https://doi.org/10.1007/3-540-57055-4_2"
doi: "10.1007/3-540-57055-4_2"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "number-field-sieve-general-integers-1993.md"
---

# Content source: Factoring Integers with the Number Field Sieve

## Source type
Book chapter in "The Development of the Number Field Sieve" (Lecture Notes in Mathematics 1554, Springer 1993). Extended abstract published in STOC 1990.

## Authors affiliation
- J. P. Buhler — Reed College, Portland.
- H. W. Lenstra Jr. — University of California, Berkeley.
- C. Pomerance — University of Georgia, Athens.

## Objective
Extend the Number Field Sieve (NFS), previously applicable only to numbers of special form (e.g., \(b^c \pm 1\)), to **arbitrary integers** with heuristic complexity \(L_n[1/3, (64/9)^{1/3} + o(1)]\), where \(L_n[u,v] = \exp(v (\log n)^u (\log \log n)^{1-u})\).

## Core methodology

### Overall structure (congruence of squares)
Find a non‑empty set \(S\) of coprime integer pairs \((a,b)\) with \(|a| \le u\), \(0 < b \le u\) such that:

1. \(\prod_{(a,b)\in S} (a + b m)\) is a square in \(\mathbb{Z}\).
2. \(\prod_{(a,b)\in S} (a + b \alpha)\) is a square in \(\mathbb{Z}[\alpha]\), where \(\alpha\) is a root of monic irreducible \(f \in \mathbb{Z}[X]\) with \(f(m) \equiv 0 \bmod n\).

Then \(\phi(\sum b_i \alpha^i) = \sum b_i m^i \bmod n\) gives \(x^2 \equiv y^2 \pmod n\), and \(\gcd(x-y,n)\) may factor \(n\).

### Step 1: Polynomial selection (base‑\(m\) method)
- Choose degree \(d > 1\) with \(n > 2^{d^2}\).
- Set \(m = \lfloor n^{1/d} \rfloor\), write \(n = \sum_{i=0}^d c_i m^i\) with \(0 \le c_i < m\).
- \(f(X) = X^d + c_{d-1} X^{d-1} + \cdots + c_0\).
- Then \(f(m) = n\), leading coefficient \(c_d = 1\), and \(c_{d-1} \le d\).

**Discriminant bound**: \(|\Delta_f| < d^{2d} n^{2-3/d}\) (Lemma 3.3).

### Step 2: Sieving (rational and algebraic sides)
- **Rational side**: \(a + b m\) – sieve over primes \(p \le y\).
- **Algebraic side**: Norm \(N(a + b\alpha) = a^d - c_{d-1}a^{d-1}b + \cdots + (-1)^d c_0 b^d\).
- Sieve over primes \(p \le y\) and roots \(r \in R(p) = \{r \bmod p : f(r) \equiv 0 \bmod p\}\).
- Smoothness bound \(y\) to be optimized.

### Step 3: Linear algebra over \(\mathbb{F}_2\)
Build matrix rows = \((a,b) \in T = T_1 \cap T_2\) with columns for:
- Sign of \(a+bm\) (1 bit).
- Exponents mod 2 of primes \(p \le y\) in \(a+bm\).
- Exponents mod 2 of first‑degree primes \(\mathfrak{p}\) (pairs \(p,r\)) in \(N(a+b\alpha)\).
- **Quadratic characters** (Adleman’s idea): Legendre symbols \(\left(\frac{a+bs}{q}\right)\) for \(B'' \approx 3\log_2 n\) primes \(q > y\) with \(r \in R(q)\).

If \(\#T > 1 + \pi(y) + B' + B''\), linear dependence exists → subset \(S\) with even parity in all columns.

### Step 4: Square root in \(\mathbb{Z}[\alpha]\)
- Compute \(\gamma = f'(\alpha)^2 \prod_{(a,b)\in S} (a + b\alpha)\).
- Use Newton iteration modulo powers of a prime \(q\) for which \(f \bmod q\) is irreducible.
- Recover \(\beta \in \mathbb{Z}[\alpha]\) with \(\beta^2 = \gamma\).

### Step 5: Final GCD
- Compute \(x = \sqrt{f'(m)^2 \prod (a+bm)}\).
- Compute \(y = \phi(\beta) \bmod n\).
- \(\gcd(x-y, n)\) yields a factor.

## Key results

### Asymptotic complexity (heuristic, Conjecture 11.2)

| Parameter | Optimal asymptotic value |
|-----------|--------------------------|
| Degree \(d\) | \((3^{1/3} + o(1)) (\log n / \log \log n)^{1/3}\) |
| Smoothness bound \(y = u\) | \(L_n[1/3, (8/9)^{1/3} + o(1)]\) |
| Heuristic runtime | \(L_n[1/3, (64/9)^{1/3} + o(1)] \approx L_n[1/3, 1.923 + o(1)]\) |

**Comparison with other methods**:
- Quadratic sieve (QS): \(L_n[1/2, 1 + o(1)]\)
- Special NFS (SNFS, for \(b^c \pm 1\)): \(L_n[1/3, (32/9)^{1/3} + o(1)] \approx L_n[1/3, 1.526]\)
- Elliptic Curve Method (ECM): \(L_p[1/2, \sqrt{2} + o(1)]\) for factor \(p\)

### Crossover estimate (circa 1993)
- General NFS vs. QS crossover ≈ **125 decimal digits**.
- At 130 digits, predicted operations within factor ~3.

### Obstructions to squaring in \(\mathbb{Z}[\alpha]\) and their handling

| Obstruction | Description | Handling method |
|-------------|-------------|----------------|
| (6.2) | \(\mathbb{Z}[\alpha] \neq \mathcal{O}\) (order vs. full ring of integers) | Quadratic characters (Adleman) |
| (6.3) | Class group not trivial | Quadratic characters |
| (6.4) | Units not squares | Quadratic characters |
| (6.5) | Square root not in \(\mathbb{Z}[\alpha]\) | Multiply by \(f'(\alpha)^2\) (Eq. 6.6) |

**Theorem 6.7**: \(\dim_{\mathbb{F}_2} V / K^{*2} < \log_2 n\), where \(V = \{\beta \in K^* : l_{\mathfrak{p}}(\beta) \equiv 0 \bmod 2 \ \forall \mathfrak{p}\}\).  
Thus the obstruction group is small – \(B'' \approx 3\log_2 n\) quadratic characters suffice.

### Homogeneous polynomial variant (Section 12)
- Replace \(f(X)\) by homogeneous \(f(X,Y) = \sum_{i=0}^d c_i X^i Y^{d-i}\).
- Find \(m_1, m_2\) with \(f(m_1, m_2) \equiv 0 \bmod n\) and \(|c_i|, |m_i| \approx n^{1/(d+1)}\) (vs. \(n^{1/d}\) in base‑\(m\)).
- Improves practical performance; asymptotically same complexity.

**Proposition 12.11** (lower bound for coefficients):  
If every integer in \([1,N]\) has a multiple of the form \(f(m_1,m_2)\) with \(|c_i|\le C\), \(|m_i|\le M\), then \(CM \ge \frac{1}{8} N^{(2-\epsilon)/(d+2)}\).

### Square root algorithm (Section 9)
- Choose prime \(q\) where \(f \bmod q\) irreducible (density \(1/d\) by Čebotarev; Lemma 9.2 proves at least \(\#G/d\) fixed‑point‑free elements).
- Newton iteration: \(\delta_{j} \equiv \frac{\delta_{j-1}(3 - \delta_{j-1}^2 \gamma)}{2} \bmod q^{2^j}\).
- Complexity: \(y^{1+o(1)}\) with fast multiplication, \(y^{2+o(1)}\) with naive arithmetic.

## Limitations (explicit from source)
- **Heuristic assumptions**:
  - Smoothness probability of \(a+bm\) and \(N(a+b\alpha)\) equals that of random integers of same size.
  - Quadratic characters \( \chi_{\mathfrak{q}}\) behave like random homomorphisms on \(V/K^{*2}\).
- **No rigorous proof**: Effective Čebotarev would be needed; even GRH insufficient without additional heuristics.
- **Square root** may involve numbers of size \(\exp(y^{1+o(1)})\) — potentially dominating runtime without FFT multiplication.
- **Special numbers** (e.g., \(n = m^4+1\)) may lack a prime \(q\) with \(f \bmod q\) irreducible; requires alternative method.
- **Expected crossover** (125 digits) was speculative in 1993; today NFS dominates for much smaller numbers.

## Practical conclusions (as of 1993)
1. For arbitrary integers >125 digits, NFS is asymptotically faster than QS.
2. Polynomial selection via base‑\(m\) is simple but not optimal; homogeneous variant reduces coefficient size.
3. Adleman’s quadratic characters elegantly handle all obstructions (class group, units, non‑maximal order) with linear algebra over \(\mathbb{F}_2\) only.
4. Large prime variation and lattice sieve (Pollard) improve practical performance.
5. Square root remains the most delicate step; Couveignes (odd degree) and Bernstein have proposed more practical algorithms.

## Open problems noted
- Rigorous complexity analysis (still open as of 1993).
- Practical polynomial selection beyond base‑\(m\) and homogeneous methods.
- Efficient square root for even degree fields.

## Key technical lemmas

**Lemma 10.12 & Theorem 10.1 (analytic number theory)**:  
For \(x,y \to \infty\), the smoothness counting function \(\psi(x,y)\) satisfies that minimizing \(x g(y) / \psi(x,y)\) (with \(g(y) = y^{1+o(1)}\)) gives \(y = L_x[1/2, \sqrt{2}/2 + o(1)]\) and minimal value \(L_x[1/2, \sqrt{2} + o(1)]\).  
Used to derive NFS parameters.

**Proposition 7.1 (Jordan‑Hölder for orders)**:  
For any order \(A\) in a number field \(K\), there exist homomorphisms \(l_{\mathfrak{p}}: K^* \to \mathbb{Z}\) satisfying \(l_{\mathfrak{p}}(x) \ge 0\) for \(x\in A\setminus\{0\}\), \(l_{\mathfrak{p}}(x) >0 \iff x\in\mathfrak{p}\), and \(\prod \mathfrak{N}\mathfrak{p}^{l_{\mathfrak{p}}(x)} = |N(x)|\).  
Generalizes prime ideal factorization to non‑maximal orders.