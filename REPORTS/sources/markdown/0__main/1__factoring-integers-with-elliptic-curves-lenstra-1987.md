---
title: "Factoring integers with elliptic curves"
title_en: "Factoring integers with elliptic curves"
source_type: "article"
authors: ["Lenstra Jr. H. W."]
year: "1987"
source_link: "https://doi.org/10.2307/1971363"
doi: "10.2307/1971363"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "factoring-integers-with-elliptic-curves-lenstra-1987.md"
---

# Content source: Factoring integers with elliptic curves

## Source type
Peer-reviewed journal article (Annals of Mathematics, Second Series, Vol. 126, No. 3, Nov. 1987, pp. 649–673). Princeton University, Mathematics Department.

## Author affiliation
H. W. Lenstra Jr. — Universiteit van Amsterdam (at time of publication), also University of California, Berkeley.

## Objective
Present a new integer factorization algorithm based on elliptic curves (ECM), analyze its expected running time under a plausible conjecture about the distribution of smooth numbers in short intervals, and compare it with existing methods (Pollard's p−1, quadratic sieve, class group method).

## Core content summary

### 1. Relationship to Pollard's p−1 method

**Pollard's p−1 method** (1974):
- Works in multiplicative group (Z/pZ)* of order p−1.
- If p−1 is B‑smooth (all prime factors ≤ B), then for k = lcm(1,…,B), a^k ≡ 1 mod p → p | gcd(a^k−1, n).
- Fails if p−1 has a large prime factor.

**ECM**: replaces (Z/pZ)* with group of points on a random elliptic curve E over F_p.
- Order of E(F_p) = p + 1 − t_p with |t_p| ≤ 2√p (Hasse, 1934).
- If order is B‑smooth, algorithm succeeds.
- If one curve fails, try another random curve → different t_p → new independent chance.

### 2. Counting elliptic curves with given order (Section 1)

**Key result (Deuring, 1941)**:
- Weighted number of isomorphism classes of elliptic curves over F_p with #E(F_p) = p + 1 − t is H(t² − 4p), where H(Δ) is the Kronecker class number.

**Proposition 1.9**: For primes p > 3 and S a set of integers with |s−(p+1)| ≤ 2√p:
- Upper bound: weighted count ≤ c₄·|S|·√p·log p·(log log p)².
- Lower bound: for |s−(p+1)| ≤ √p: weighted count ≥ c₅·(|S|−2)·√p / log p.

**Proposition 1.14**: Probability (weighted) that #E(F_p) ≡ 0 mod l:
- If p ≢ 1 mod l: ≈ 1/(l−1).
- If p ≡ 1 mod l: ≈ l/(l²−1).

**Proposition 1.16**: Lower bounds for number of (a,x,y) triples giving curves with certain properties.

### 3. ECM algorithm (Section 2)

**Elliptic curves modulo composite n (Section 2.1)**:
- Work in projective plane over Z/nZ.
- Point P = (x:y:1), O = (0:1:0).
- Curve: y² = x³ + ax + b with 6(4a³+27b²) ∈ (Z/nZ)*.

**Addition algorithm (2.2)**:
- Computes P+Q or finds factor d of n when denominator not invertible mod n.
- Uses gcd to detect when denominator shares a factor with n.

**Multiplication (2.3)**:
- Repeated addition (binary method) to compute kP.
- If inversion fails at any step, factor found.

**Factoring with one curve (2.4)**:
- Choose bounds v (estimate for p) and w (smoothness bound).
- Define e(r) = max{m : rᵐ ≤ v + 2√v + 1}.
- Compute k = ∏_{r=2}^{w} r^{e(r)}.
- Compute kP; if inversion fails, factor found.

**Proposition 2.6 (Sufficient condition for success)**:
If there exist primes p, q dividing n such that:
(i) p ≤ v
(ii) 6(4a³+27b²) ≠ 0 mod p (non‑singular curve)
(iii) all primes dividing #E(F_p) are ≤ w
(iv) 6(4a³+27b²) ≠ 0 mod q
(v) #E(F_q) not divisible by the largest prime dividing the order of P_p
then algorithm succeeds.

**Proposition 2.7** (Probability of success for random (a,x,y)):
Under the conditions, the number N of successful triples satisfies:
N / n³ ≥ (c₁₁ / log p) · (u − 2) / (2⌊√p⌋+1),
where u = #{s : |s−(p+1)| < √p, all prime factors of s ≤ w}.

### 4. Conjectured complexity (Section 2.9–2.10)

**Smooth number conjecture**:
For a random integer s in (p+1−√p, p+1+√p), probability that all prime factors ≤ L(p)^α is L(p)^{-1/(2α)+o(1)}.
Here L(x) = exp(√(log x log log x)).

**Optimization**:
Choose w = L(p)^α. Then w / f(w) ≈ L(p)^{α + 1/(2α)}.
Minimum at α = 1/√2 (since α + 1/(2α) minimized at α = 1/√2 gives √2).
Thus:
- w = L(p)^{1/√2 + o(1)}
- Expected work per curve: O(w log v M(n))
- Number of curves needed: h ≈ (log v)/f(w) ≈ L(p)^{√2 + o(1)}
- Total expected time: ≈ L(p)^{√2 + o(1)} M(n)

**Conjecture 2.10**:
For n not a prime power and not divisible by 2 or 3, with probability ≥ 1 − e^{-g}, ECM finds a nontrivial divisor in time:
g·K(p)·M(n),
where K(x) = exp(√((2+o(1)) log x log log x)) and M(n) = O((log n)²) or O(log n (log log n)² log log log n).

**Worst‑case** (n product of two roughly equal primes):
- Expected time: L(n)^{1+o(1)} (same as quadratic sieve conjectured complexity).

### 5. Comparison with other methods (2.11–2.13)

| Algorithm | Conjectured complexity | Depends on | Storage |
|-----------|------------------------|------------|---------|
| QS / CFRAC / class group | L(n)^{1+o(1)} | n only | large |
| ECM | L(p)^{√2+o(1)} | smallest prime factor p | O(log n) |

**Advantages of ECM**:
- Much faster if n has a small prime factor.
- Very low storage requirement (O(log n)).
- Can be used as subroutine in other factoring algorithms to recognize numbers built up from small primes.
- Useful in primality testing (finding completely factored divisors of n−1, n+1, etc.).

**Practical modifications**:
- Use different curve models.
- Add second stage (allows one larger prime factor).
- See Montgomery (1987), Brent (1985) for practical improvements.

## Key mathematical results used

| Result | Source | Use in ECM |
|--------|--------|-------------|
| Hasse's theorem | Hasse (1934) | Order of E(F_p) in [p+1−2√p, p+1+2√p] |
| Deuring's formula | Deuring (1941) | Count curves with given order → H(t²−4p) |
| Weil's inequality | Weil | Bound points on modular curves X(l), X₁(l) |
| Kronecker class number | Classical | Upper/lower bounds via class number formula |
| Smooth number density | Canfield–Erdős–Pomerance (1983) | Conjectured behavior in short intervals |

## Limitations (explicit from source)

- **Heuristic assumption**: smooth number density in short intervals around p+1 behaves like density for random integers up to p. Not proven; needed for complexity bound.
- **Algorithm as described** is for exposition, not optimized for practice.
- **Excludes** numbers divisible by 2 or 3 (trivial to handle separately) and prime powers.
- **No second stage** in the analyzed version (allows one larger prime factor); practical implementations include it.
- **Constants** in complexity are not given explicitly; existence is proven but values not computed.
- **Assumes** ability to draw random triples (a,x,y) uniformly from (Z/nZ)³.

## Open problems (implicit)

- Prove the smooth number conjecture in short intervals (or find a rigorous version).
- Improve the bound d < N^{0.292} for small private exponent attacks (later work by Boneh–Durfee, 1999; Herrmann–May, 2010).
- Extend ECM to handle numbers with factors of arbitrary size more efficiently (but GNFS already does this).

## References (selected, many classical)
- Deuring (1941) — Typen der Multiplikatorenringe elliptischer Funktionenkörper
- Pollard (1974) — p−1 method
- Montgomery (1987) — Speeding Pollard and elliptic curve methods (same issue of Math. Comp.)
- Brent (1985) — ECM improvements
- Canfield, Erdős, Pomerance (1983) — smooth number density
- Schoof (1985) — elliptic curve point counting
- Silverman (1986) — Arithmetic of Elliptic Curves (textbook)
