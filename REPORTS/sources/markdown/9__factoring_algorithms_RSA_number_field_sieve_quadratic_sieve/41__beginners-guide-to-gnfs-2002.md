---
title: "A Beginner's Guide To The General Number Field Sieve"
title_en: "A Beginner's Guide To The General Number Field Sieve"
source_type: "technical_report"
authors: ["Case M."]
year: "2002"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "beginners-guide-to-gnfs-2002.md"
---

# Content source: A Beginner's Guide To The General Number Field Sieve

## Source type
Technical report / student paper (Oregon State University, ECE 575). Likely a course project or tutorial.

## Author affiliation
Michael Case — Oregon State University.

## Objective
Provide an accessible, self-contained introduction to the General Number Field Sieve (GNFS) algorithm for factoring large composite numbers, explaining the underlying theory and including a complete worked numerical example.

## Core content summary

### 1. Motivation: RSA security
- RSA public key: (e, n), private key: d with ed ≡ 1 (mod (p−1)(q−1)).
- Factoring n = p·q breaks RSA → adversary can compute d.
- GNFS is the fastest known method for numbers > 100 digits (as of 2002).

### 2. Difference of squares factorization method (Section II‑A)

Given s² ≡ r² (mod n) with n = p·q:

- n | (s−r)(s+r)
- For each prime factor p of n, p divides (s−r) or (s+r) (or both).
- Table I enumerates 8 divisibility scenarios.
- **Probability of nontrivial factor**: 2/3 (if all scenarios equally likely).
- Example: if p|(s+r), q|(s−r), then gcd(n, s+r) = p, gcd(n, s−r) = q.

### 3. Free parameters: polynomial f and integer m

Given composite n:
- Choose m (e.g., m = ⌊n^{1/d}⌋ for some degree d).
- Write n in base m: n = a_d·m^d + a_{d-1}·m^{d-1} + ... + a_0.
- Define f(x) = a_d x^d + a_{d-1} x^{d-1} + ... + a_0.
- Then f(m) = n ⇒ f(m) ≡ 0 (mod n).

**Example (n = 45113)**: m = 31, d = 3
45113 = 31³ + 15·31² + 29·31 + 8 → f(x) = x³ + 15x² + 29x + 8.

### 4. The ring ℤ[θ]

- θ ∈ ℂ is a root of f (so f(θ) = 0).
- ℤ[θ] = { a_{d-1}θ^{d-1} + ... + a_0 | a_i ∈ ℤ }.
- Multiplication in ℤ[θ]: multiply polynomials, then reduce modulo f(θ).
- **Theorem 2.2 (Homomorphism φ)**: There exists a unique ring homomorphism φ: ℤ[θ] → ℤ/nℤ with φ(θ) ≡ m (mod n) and φ(1) ≡ 1.

### 5. Core GNFS strategy (Section II‑D)

Find a set U of integer pairs (a,b) such that:
1. ∏_{(a,b)∈U} (a + bm) = y² (square in ℤ)
2. ∏_{(a,b)∈U} (a + bθ) = β² (square in ℤ[θ])

Then with x = φ(β):
x² ≡ φ(β²) = φ(∏(a+bθ)) = ∏(a+bm) ≡ y² (mod n) → x² ≡ y² (mod n) → factor n with probability 2/3.

### 6. Finding squares via linear algebra over 𝔽₂ (Section II‑E)

**Key idea (numerical example)**:
- Numbers {455, 39270, 770, 429, 1616615, 3990, 106590, 187, 19019} all have prime factors ≤ 19.
- Represent each number by exponent vector modulo 2 (e.g., 455 = 2⁰·3⁰·5¹·7¹·11⁰·13¹·17⁰·19⁰ ↔ (0,0,1,1,0,1,0,0)).
- Find subset whose vectors sum to zero (mod 2) → product is a square.
- Solve linear system over 𝔽₂. Example: 455·39270·1616615·3990 = (339489150)².

### 7. Smoothness definitions

**Rational factor base ℛ**: finite set of small primes (e.g., all primes ≤ M).
- Integer l is smooth over ℛ if all prime divisors of l are in ℛ.

**Algebraic factor base 𝒜**: finite set of elements a+bθ ∈ ℤ[θ] that are "prime ideals".
- **Theorem 2.3**: There is a bijection between such elements and pairs (r,p) where p is prime and f(r) ≡ 0 (mod p).
- Element a+bθ is smooth over 𝒜 if it factors completely into such prime ideals.

**Quadratic character base 𝒬**: additional pairs (s,q) with q prime, f(s) ≡ 0 (mod q), used to verify squares in ℤ[θ] (Legendre symbol test).

### 8. Sieving to find smooth pairs (Section II‑E.2)

For fixed b, create arrays for a from −N to N:
- For each prime q in ℛ: a+bm ≡ 0 (mod q) ⇔ a ≡ −b·m (mod q). Mark positions.
- For each (r,p) in 𝒜: a+bθ divisible by (r,p) ⇔ a ≡ −b·r (mod p). Mark positions.
- After processing all primes, entries where a+bm and a+bθ are both fully factored are smooth pairs.

**Theorems used**:
- **Theorem 2.4**: (r,p) divides a+bθ ⇔ a ≡ −b·r (mod p).
- **Theorem 2.5**: Complete factorization of a+bθ occurs iff ∏ p_i = |(−b)^d·f(−a/b)|.
- **Theorem 2.6**: q | (a+bm) ⇔ a ≡ −b·m (mod q).

### 9. Quadratic characters for square testing (Section II‑E.3)

**Theorem 2.7**: If ∏(a+bθ) is a square in ℤ[θ], then every exponent in its prime ideal factorization is even.

**Theorem 2.8**: If ∏(a+bθ) is a square, then for any (s,q) ∈ 𝒬 (with (s,q) not dividing any a+bθ):
∏_{(a,b)∈U} ( (a+bs)/q ) = 1, where (·/·) is the Legendre symbol.

These are necessary conditions; if enough independent quadratic characters are satisfied, the product is "probably" a square.

### 10. Matrix construction and solving (Section II‑E.4)

For each smooth pair (a,b), construct row vector of length 1 + k + l + u:

| Sign (0/1) | Exponents mod 2 in ℛ (k bits) | Exponents mod 2 in 𝒜 (l bits) | Legendre results for 𝒬 (u bits) |

- Sign: 0 if a+bm > 0, 1 if negative (ensures product positive).
- ℛ exponents: exponents of primes in a+bm, reduced mod 2.
- 𝒜 exponents: exponents of (r_i,p_i) in factorization of a+bθ, reduced mod 2.
- 𝒬 entries: 0 if Legendre symbol = 1, 1 if = −1.

Let X be the y × (1+k+l+u) matrix of rows. Solve X^T·A ≡ 0 (mod 2).
If y > 1+k+l+u, nontrivial solution exists.
Set V = {(a,b) | A_i = 1}. Then:
- ∏_{(a,b)∈V} (a+bm) is a square in ℤ.
- ∏_{(a,b)∈V} (a+bθ) is a square in ℤ[θ].

### 11. Complete numerical example: n = 45113

| Parameter | Value |
|-----------|-------|
| m | 31 |
| f(x) | x³ + 15x² + 29x + 8 |
| ℛ | primes ≤ 29 (10 primes) |
| 𝒜 | pairs (r,p) with p < 90, f(r)≡0 mod p (20 entries) |
| 𝒬 | primes {97,101,103,107} (6 entries) |
| Required rows | > 1+10+20+6 = 37 |

Sieving: b = 1..41, a ∈ [−400,400] → found 38 smooth pairs (Table III).

Sample smooth pair (119,11):
- a+bm = 119 + 11·31 = 460 = 2²·5·23 → smooth over ℛ.
- a+bθ factorization: (19,41), (44,67), (62,89) in 𝒜. Check: 41·67·89 = (−11)³·f(−119/11).

Matrix solution yields subset V of 15 pairs. Computed:
- ∏(a+bm) = 45999712751795195582606376960000 = (2553045317222400)²
- ∏(a+bθ) = (108141021·θ² + 235698019·θ + 62585630)²

Apply φ:
φ(108141021·θ² + 235698019·θ + 62585630) ≡ 111292745400 (mod n)

Then:
111292745400² ≡ 2553045317222400² (mod 45113)

Compute gcd:
- gcd(45113, 111292745400 + 2553045317222400) = 197
- gcd(45113, 111292745400 − 2553045317222400) = 229

Thus n = 45113 = 197·229.

### 12. Practical note on performance (Section IV)

- GNFS has high setup overhead → slower than other methods for small numbers.
- For large composites (e.g., > 100 digits), GNFS is dramatically faster.
- **Record (as of 2002)**: 155‑digit (512‑bit) composite factored in 3.7 months by University of Bonn team.

## Key theoretical prerequisites summarized
- Modular arithmetic, Chinese Remainder Theorem (implicit).
- Ring theory (ℤ[θ], homomorphisms).
- Prime ideals in number fields (simplified via (r,p) pairs).
- Legendre symbol and quadratic residues.
- Linear algebra over GF(2) (solving sparse systems).

## Limitations (explicit from source / educational nature)
- Paper is a tutorial, not original research.
- Assumes certain algebraic number theory facts without proof (e.g., bijection between prime ideals and (r,p) pairs).
- Sieving described conceptually; actual implementation details (logarithms, early aborts) omitted.
- Example uses very small parameters (n=45113, m=31, a up to 400); real GNFS uses much larger ranges.
- Quadratic character test is probabilistic; increasing 𝒬 size increases confidence but not absolute certainty.

## Pedagogical value
- Excellent step‑by‑step illustration of GNFS with complete, checkable arithmetic.
- Clear separation of concepts: difference of squares, smoothness, factor bases, matrix construction, square root.
- Demystifies algebraic number theory by focusing on concrete representations (pairs (r,p)) rather than abstract ideals.
