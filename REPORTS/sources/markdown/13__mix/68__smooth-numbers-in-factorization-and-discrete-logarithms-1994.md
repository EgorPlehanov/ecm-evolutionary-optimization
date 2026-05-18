---
title: "Smooth Numbers in Factorization and Discrete Logarithms"
title_en: "Smooth Numbers in Factorization and Discrete Logarithms"
source_type: "conference"
authors: ["Pomerance C."]
year: "1994"
source_link: "unknown (provided PDF: 68__icm1994.1.0411.0422.ocr.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "smooth-numbers-in-factorization-and-discrete-logarithms-1994.md"
---

# Content source: Smooth Numbers in Factorization and Discrete Logarithms

## Source type
Invited survey paper (Proceedings of the International Congress of Mathematicians, Zurich, 1994, pp. 411–422).

## Author affiliation
Carl Pomerance — University of Georgia, Athens, GA, USA.

## Objective
Survey the central role of smooth numbers (integers with only small prime factors) in modern computational number theory, including integer factorization algorithms (random squares, quadratic sieve, number field sieve, elliptic curve method), discrete logarithm algorithms, and primality testing.

## Core concepts

### Smooth number definition
- A positive integer is y-smooth if it has no prime factor exceeding y.
- ψ(x,y) = number of y-smooth integers ≤ x.
- Key estimate: ψ(x, L(x)ᵃ) = x·L(x)^{-1/(2a)+o(1)} where L(x) = exp(√(ln x ln ln x)).

### Fundamental lemma (Lemma 2.1)
- Let ε > 0. If we choose L(x)^{√2+ε} integers uniformly from [1,x], probability → 1 that some nonempty subset product is a square.
- If we choose L(x)^{√2-ε} integers, probability → 0.
- Proof uses smooth numbers: need > π(y) smooth numbers; optimal y ≈ L(x)^{√2/2}; expected trials ≈ L(x)^{√2}.

## Factorization algorithms

### Random squares method (Dixon)
- Choose random A, compute Q ≡ A² mod n (least positive residue).
- Keep Q if y-smooth (y ≈ L(n)^{√2/2}).
- Find π(y)+1 smooth Qs, build exponent vectors over F₂, find dependency → square.
- Complexity: L(n)^{√2+o(1)} (rigorous).

### Continued fraction method (CFRAC)
- Use convergents of √n to get Q_i with |Q_i| < 2√n (smaller than n).
- Complexity: L(n)^{1+o(1)}.

### Quadratic sieve (QS) — Pomerance 1982
- Polynomial Q(t) = t² − n. For |t−√n| < n^ε, |Q(t)| < 3n^{1/2+ε}.
- Sieve with primes ≤ y to identify smooth Q(t) values.
- Complexity: L(n)^{1+o(1)} (heuristic).

### Number field sieve (NFS)
- Use two polynomials f, g with f(m) ≡ g(m) ≡ 0 mod n (e.g., base-m expansion of n).
- Work in number fields Q(α), Q(β) with f(α)=0, g(β)=0.
- Smoothness defined via norm to Z.
- Sieve over (a,b) pairs with small coprime integers.
- Complexity: L(n)^{(64/9)^{1/3} + o(1)} ≈ L(n)^{1.923 + o(1)} (heuristic).
- Later improved to L(n)^{(32/9)^{1/3} + o(1)} ≈ L(n)^{1.526 + o(1)}.

### Elliptic curve method (ECM) — Lenstra 1987
- Choose random elliptic curve E mod n and point P.
- Let M = lcm of all y-smooth numbers ≤ y.
- Compute MP mod n. If addition fails → factor found.
- Works when order of P in E(p) is y-smooth, but not in E(q).
- Worst-case complexity: L(p)^{1+o(1)} for smallest prime factor p.
- Best when p is small; faster than QS/NFS for finding small factors.

## Discrete logarithm algorithms

### Index calculus in F_p^*
- Collect relations: g^m ≡ smooth number (product of primes ≤ y) mod p.
- Solve linear system over Z/(p−1) for logs of small primes.
- Individual log: find m s.t. g^m·h smooth → log h = −m + Σ a_i log q_i.
- Complexity: L(p)^{√2+o(1)} for precomputation, L(p)^{√2/2+o(1)} for individual.

### Smooth polynomials in F_q
- For F_{p^k} with k large, represent as F_p[x]/(f), define smooth via low-degree irreducible factors.
- Analogous distribution theory exists.

### Elliptic curve discrete logarithms
- No known notion of smoothness in elliptic curve groups → basis for cryptographic security.

## Primality testing and smooth numbers

### Carmichael numbers
- Composite n with aⁿ ≡ a mod n for all a.
- Proved infinite in 1992 (Alford, Granville, Pomerance).
- Construction requires primes p where p−1 is y-smooth (Erdős method).

### Primality proving (APR-CL test)
- Uses auxiliary primes p with p−1 y-smooth.
- Complexity: (ln n)^{c ln ln ln n} (almost polynomial).

### Deterministic polynomial-time primality test
- Open problem; algorithm exists assuming GRH (Miller–Rabin with bases ≤ 2 ln² n).

## Key estimates

| Quantity | Approximate value |
|----------|-------------------|
| L(x) | exp(√(ln x ln ln x)) |
| Optimal y for smooth number collection | L(x)^{√2/2} |
| Expected trials to find π(y)+1 smooth numbers | L(x)^{√2} |
| QS complexity (heuristic) | L(n)^{1+o(1)} |
| NFS complexity (heuristic) | L(n)^{1.526+o(1)} |
| ECM worst-case complexity | L(p)^{1+o(1)} for smallest factor p |

## Practical notes (circa 1994)
- QS: numbers up to ~100 digits.
- NFS: factored 119-digit number (Contini, Dodson, A. Lenstra, Montgomery) — record at time.
- ECM: used as first-stage method before QS/NFS.

## Historical context
- Pomerance introduced quadratic sieve in 1982.
- Lenstra invented ECM in 1987.
- NFS developed by Pollard, Lenstra, Lenstra, Manasse, et al. (1988–1993).
- CFRAC (Morrison & Brillhart, 1975) factored F₇.
- Smooth numbers lemma (Lemma 2.1) derived from Canfield–Erdős–Pomerance (1983) estimates.

## References cited
- Canfield, Erdős, Pomerance (1983) — ψ(x,y) estimate.
- Buhler, Lenstra, Pomerance (1993) — NFS overview.
- Lenstra, Pila, Pomerance — hyperelliptic curve smoothness test.
- Alford, Granville, Pomerance (1992/1994) — infinitely many Carmichael numbers.
- Adleman, Pomerance, Rumely (1983) — APR primality test.
- Morrison & Brillhart (1975) — CFRAC factorization of F₇.
- Montgomery (1995) — block Lanczos for sparse linear algebra.
