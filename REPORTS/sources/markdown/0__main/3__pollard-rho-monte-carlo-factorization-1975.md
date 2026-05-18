---
title: "A Monte Carlo method for factorization"
title_en: "A Monte Carlo method for factorization"
source_type: "article"
authors: ["Pollard J. M."]
year: "1975"
source_link: "none"
doi: "10.1007/BF01933667"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "pollard-rho-monte-carlo-factorization-1975.md"
---

# Content source: A Monte Carlo method for factorization

## Source type
Peer-reviewed journal article (BIT Numerical Mathematics, Vol. 15, No. 3, 1975, pp. 331–334). This is the short note introducing the Pollard Rho algorithm.

## Author affiliation
J. M. Pollard — Mathematics Department, Plessey Telecommunications Research, Taplow Court, Taplow, Maidenhead, Berkshire, England.

## Objective
Present a simple, practical, probabilistic algorithm for integer factorization that finds a prime factor p in expected O(√p) arithmetic operations, using a pseudorandom sequence and Floyd's cycle‑detection method. This algorithm is now known as **Pollard's Rho method**.

## Core content summary

### 1. Algorithm description (Section 1)

**Setup**:
- Let n be the number to factor.
- Choose a polynomial of degree ≥ 2, e.g., \(f(x) = x^2 - 1\) (mod n), and a starting value, e.g., \(x_0 = 2\).
- Generate sequence: \(x_{i+1} \equiv f(x_i) \pmod{n}\).

**Main loop** (Floyd's cycle detection):
- Generate triples \((x_i, x_{2i}, Q_i)\) for i = 1, 2, …,
  where \(Q_i \equiv \prod_{j=1}^{i} (x_{2j} - x_j) \pmod{n}\).
- Each triple is obtained from the previous by:
  - Two applications of f to update x_{2i-2} → x_{2i-1} → x_{2i}
  - One application of f to update x_{i-1} → x_i
  - One multiplication to update Q_i.
- **Work per iteration**: about 4 modular multiplications.

**GCD check**:
- Every m iterations (e.g., m = 100), compute \(d_i = \gcd(Q_i, n)\).
- If \(1 < d_i < n\), then d_i is a (possibly composite) factor of n.

**Continuation**:
- Replace n by n/d_i and continue with the reduced modulus.
- Stop after a preset maximum number of steps S (e.g., S = 10,000).

### 2. Theory (Section 2)

**Why it works (mod a prime p)**:
- Consider the same recurrence modulo a prime divisor p of n.
- Since the sequence is defined on a finite set (p residues), it must eventually become periodic: there exist c ≥ 1 (length of cycle) and t ≥ 0 (length of tail) such that \(x_{c+t} \equiv x_t \pmod{p}\) and earlier terms are distinct.
- Let \(r = r(p)\) be the least positive integer such that \(x_r \equiv x_{2r} \pmod{p}\).
- Then after r(p) steps, \(Q_r \equiv 0 \pmod{p}\), so p divides Q_r, and thus p will be discovered at the next GCD check.

**Heuristic assumption**:
- The mapping \(x \mapsto x^2 - 1 \bmod p\) behaves like a random mapping on the set of residues modulo p.
- Under this assumption, the expected values are:
  - Expected tail length + cycle length: about \(2\sqrt{\pi p / 8} \approx 1.2533 \sqrt{p}\).
  - Expected r(p) (the first index where \(x_r \equiv x_{2r}\)): about \(\sqrt{\pi p / 8} \cdot \frac{\pi}{2\sqrt{2}}?\) – paper gives ≈ 1.0308√p.

**Empirical check** (100 largest primes below 10⁶):
- Average c/√p ≈ 0.6127, average t/√p ≈ 0.6821, average r/√p ≈ 1.0780.
- Estimates: \(r(p) < 0.5\sqrt{p}\) with probability ≈ 0.183; \(r(p) > 2\sqrt{p}\) with probability ≈ 0.065.

**Deterministic bound**:
- Define M(L) = maximum of r(p) over all primes p ≤ L.
- Computed values: M(10³) = 67, M(10⁴) = 292.
- If we run the algorithm with S ≥ M(L), we are guaranteed to find all prime factors ≤ L.

**Choice of polynomial**:
- All polynomials \(x^2 + b\) seem equally good, except \(x^2\) and \(x^2 - 2\) (for the latter, due to connections with Lucas–Lehmer test).
- If prime factors are known to satisfy p ≡ 1 (mod k) with k > 2, one may use \(x^k + b\); this heuristically reduces the expected r(p) by a factor of \(\sqrt{k-1}\), but increases work per iteration.

### 3. Examples (Section 3)

Complete factorizations found using the method (m = 100, S = 10⁴):

1. \(27^{7} - 3 = 1291 \cdot 99432527 \cdot 1177212722617\)
   - Factors found at i = 100 and i = 8200.

2. \(27^{9} - 3 = 5 \cdot 3414023 \cdot 146481287 \cdot 241741417\)
   - Factors found at i = 100, 800, and 5300 (in that order).

### 4. Practical role

- The Rho method is intended as a **pre‑processor** for finding smaller factors before applying heavier algorithms (e.g., the continued fraction method of Morrison & Brillhart [4]).
- Compared to trial division:
  - Rho: expected O(√p) operations
  - Trial division: O(p) operations (or O(p/log p) if only primes are used)
- Other methods for small factors: methods that search for p where p−1 or p+1 is smooth (Pollard's p−1 method was described in [2, Section 4]).

## Key formulae

**Floyd's cycle detection**:
- The condition \(x_r \equiv x_{2r}\) detects a cycle because if the sequence becomes periodic, the "tortoise" (x_i) and "hare" (x_2i) will meet within the cycle.

**Expected r(p) under random mapping assumption**:
\[
E[r(p)] \approx \sqrt{\frac{\pi p}{8}} \cdot \frac{\pi}{2\sqrt{2}} \approx 1.0308\sqrt{p}
\]

**Empirical constants** (from sample of 100 primes near 10⁶):
- c/√p ≈ 0.6127 (tail length)
- t/√p ≈ 0.6821 (cycle length)
- r/√p ≈ 1.0780

## Limitations (explicit from source)

- **Heuristic**: the analysis assumes that the recurrence behaves like a random mapping; this is not proven.
- **Not guaranteed**: the algorithm might fail to find a factor even if it exists (probabilistic).
- **Worst‑case**: in theory, r(p) could be as large as O(p), but such primes are extremely rare under the random mapping heuristic.
- **Memoryless**: only a few variables are stored, but the product Q_i can become large; reduction modulo n is used to keep it bounded.
- **GCDs are not computed every iteration**; they are batched (every m steps) to reduce cost, but this may delay detection.

## Legacy and impact

- The Pollard Rho method is one of the most widely used algorithms for finding small‑to‑medium prime factors (up to about 10–20 digits).
- It is a standard component in factoring software (e.g., GMP‑ECM, YAFU).
- Brent (1980) improved the algorithm by using a different cycle detection method, making it about 24% faster.
- The Rho method is still used today as a first step after trial division, before switching to ECM or QS/NFS.

## References (cited)
- Knuth (1969) – The Art of Computer Programming, Vol. 2 (random mappings, cycle detection)
- Pollard (1974) – Theorems on factorization and primality testing (p−1 method)
- Morrison & Brillhart (1975) – Continued fraction factorization (F₇)
- Wunderlich & Selfridge (1974) – Trial division optimization
