---
title: "Smooth numbers and the quadratic sieve"
title_en: "Smooth numbers and the quadratic sieve"
source_type: "book_chapter"
authors: ["Pomerance C."]
year: "2008"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "smooth-numbers-and-quadratic-sieve-2008.md"
---

# Content source: Smooth numbers and the quadratic sieve

## Source type
Book chapter in "Surveys in Algorithmic Number Theory" (MSRI Publications, Vol. 44, Cambridge University Press, 2008), pp. 69–81.

## Author affiliation
Carl Pomerance — Department of Mathematics, Dartmouth College (previously at Bell Laboratories).

## Objective
Provide a gentle, self‑contained introduction to the quadratic sieve factoring algorithm, emphasizing the central role of smooth numbers, the heuristic complexity analysis, and practical considerations.

## Core content summary

### 1. Motivation and basic concepts

**Trial division**:
- Works by testing divisibility by consecutive primes up to √n.
- Feasible only for very small n or for removing tiny prime factors.
- For RSA moduli (n = p·q with p,q of equal magnitude), trial division would take ~n¹⸍² steps → impossible even for 30‑digit numbers.

**Difference of squares** (Fermat’s method):
- For n odd composite, find x,y such that n = x² − y² = (x−y)(x+y).
- Example: 8051 = 90² − 7² = 83·97.
- Works quickly if factors are close; fails otherwise.

**Key insight from n = 1649**:
- Sequence: 41² − 1649 = 32, 42² − 1649 = 115, 43² − 1649 = 200.
- No single value is a square, but 32·200 = 6400 = 80².
- Then (41·43)² ≡ 80² (mod 1649) → congruence of squares.
- gcd(114 − 80, 1649) = 17 → factor.

### 2. Congruence of squares method

If a² ≡ b² (mod n) and a ≠ ± b (mod n), then:
- n | (a−b)(a+b), but n divides neither factor.
- Hence gcd(a−b, n) and gcd(a+b, n) are nontrivial factors.
- For n with ≥ 2 distinct odd primes, at least half of the solutions with gcd(ab,n)=1 satisfy a ≠ ± b (mod n).

### 3. Smooth numbers and the lemma

**Definition**: m is B‑smooth if all prime factors of m are ≤ B.
**Lemma**: If m₁,…,mₖ are positive B‑smooth integers and k > π(B), then some non‑empty subsequence has product a square.

**Proof via exponent vectors**:
- Write m = ∏_{i=1}^{π(B)} p_i^{v_i} where p_i is the i‑th prime.
- Exponents (v₁,…,v_{π(B)}) form a vector.
- Reducing exponents modulo 2 gives a vector in 𝔽₂^{π(B)}.
- With k > π(B) vectors, linear dependency exists → sum of a subset ≡ 0 (mod 2) → product is a square.

### 4. Proto‑algorithm for factoring

**Input**: composite n, no small prime factors, not a perfect power.

1. Choose bound B.
2. For x = ⌈√n⌉, ⌈√n⌉+1, …, compute x² − n; sieve to find B‑smooth values.
3. When > π(B) smooth values found, form exponent vectors modulo 2, use linear algebra to find subset whose product is a square A².
4. Let b ≡ ∏ x_i (mod n) and a ≡ A (mod n).
5. If a ≠ ± b (mod n), compute gcd(a − b, n). Otherwise, continue searching.

### 5. Recognizing smooth numbers via sieving

**Sieve of Eratosthenes** for integers up to X:
- Initialize array with the numbers.
- For each prime p ≤ B and its powers, divide the numbers in arithmetic progressions (multiples of p).
- Locations that become 1 correspond to B‑smooth numbers.
- Time: O(X log log B) operations.

**Quadratic sieve**: same idea applied to polynomial values x² − n:
- For each prime p (and its powers), solve x² ≡ n (mod p) → 0, 1, or 2 residue classes.
- For each residue class, step through x values in arithmetic progression, dividing out p.
- Total work per polynomial value ≈ log log B (amortized).

### 6. Heuristic complexity analysis

Let X be an upper bound on |x² − n|. For x near √n, X ≈ n¹⸍²⁺ᵒ⁽¹⁾.

**Probability that a random number ≤ X is B‑smooth**:
- ψ(X,B) = count of B‑smooth numbers ≤ X.
- For fixed u with B = X¹⸍ᵘ, ψ(X,B)/X ∼ ρ(u) (Dickman–de Bruijn function), where ρ(u) decays roughly like u⁻ᵘ.

**Expected number of trials to find a B‑smooth value**: X/ψ(X,B) ≈ uᵘ.

**Number of smooth values needed**: ≈ π(B) ≈ B/log B ≈ X¹⸍ᵘ / log X.

**Sieving cost per candidate**: ≈ log log B ≈ log log X.

**Total work**: W ≈ π(B) · (log log B) · X/ψ(X,B) ≈ X¹⸍ᵘ · uᵘ (ignoring logs).

**Optimization**: choose u to minimize (1/u) log X + u log u.
- Derivative zero when u²(log u + 1) = log X.
- This gives u ∼ (2 log X / log log X)¹⸍².
- Then B = X¹⸍ᵘ = exp((1/√2 + o(1)) (log X log log X)¹⸍²).
- The running time T = exp((1 + o(1)) (log X log log X)¹⸍²).

Since X ≈ n¹⸍²⁺ᵒ⁽¹⁾:
- B = exp((1/2 + o(1)) (log n log log n)¹⸍²)
- T = exp((1 + o(1)) (log n log log n)¹⸍²)

This is the heuristic complexity of the quadratic sieve.

### 7. Linear algebra considerations

- Naïve Gaussian elimination on a π(B) × π(B) matrix takes O(π(B)³) operations.
- With π(B) ≈ B ≈ exp((1/2)(log n log log n)¹⸍²), this would dominate (exponent 3/2).
- **Practical solutions**:
  - Use iterative methods (Wiedemann, Lanczos) → O(π(B)²⁺ᵒ⁽¹⁾).
  - Exploit sparsity: matrix starts very sparse (few non‑zeros per row).
  - Use binary arithmetic with 32‑bit word packing.
  - In practice, choose B slightly smaller than optimal to reduce matrix size.

### 8. Theoretical background on ψ(X,B) (smooth number count)

**For fixed u with B = X¹⸍ᵘ**:
- For 1 ≤ u ≤ 2: ψ(X,X¹⸍ᵘ)/X ∼ 1 − log u (simple inclusion‑exclusion).
- For u > 2: ψ(X,X¹⸍ᵘ)/X ∼ ρ(u), where ρ is the Dickman–de Bruijn function.
- ρ(u) = 1 for 0 ≤ u ≤ 1; uρ′(u) = −ρ(u−1) for u > 1.
- Asymptotically, ρ(u) = u⁻⁽¹⁺ᵒ⁽¹⁾⁾ᵘ.

**Theorem of Canfield–Erdős–Pomerance**: For X → ∞, u → ∞ with X¹⸍ᵘ ≥ (log X)¹⁺ᵋ, ψ(X,X¹⸍ᵘ)/X = u⁻⁽¹⁺ᵒ⁽¹⁾⁾ᵘ.

### 9. Practical observations

- Quadratic sieve is the algorithm of choice for “hard” composites with 20–120 digits.
- For larger numbers, Number Field Sieve (NFS) becomes faster (see [Stevenhagen 2008]).
- Multiple Polynomial Quadratic Sieve (MPQS) – due to Davis and Montgomery – greatly improves speed (but not asymptotic complexity).

### 10. Rigorous vs. heuristic algorithms

- Most practical factoring algorithms are heuristic.
- ECM is “almost” rigorous.
- Fastest rigorous probabilistic factoring: Lenstra–Pomerance, complexity exp((1+o(1))√(log n log log n)) – same as QS but with larger o(1).
- Fastest rigorous deterministic: Pollard–Strassen, O(n¹⸍⁴⁺ᵒ⁽¹⁾).

## Key takeaways on smooth numbers (author’s emphasis)

> “Smooth numbers are not an artifact, they were forced upon us once we decided to combine auxiliary numbers to make a square.”

Three properties that make smooth numbers indispensable:
1. **Simple multiplicative structure** – easy to represent and manipulate.
2. **Easy to recognize** – via sieving in nearly linear time.
3. **Surprisingly numerous** – e.g., about 30% of numbers have no prime factor > √X.

## Limitations (explicit from source)

- Complexity analysis is heuristic, assuming values x² − n behave like random numbers of the same magnitude.
- Matrix step (linear algebra) can become the bottleneck; not as easily parallelized as sieving.
- For very small or very large n, other methods (ECM, NFS) are superior.

## References cited in chapter
- Crandall & Pomerance (2005) – Prime Numbers (textbook)
- Granville (2008) – Smooth numbers (this volume)
- Schoof (2008) – Primality testing (this volume)
- Stevenhagen (2008) – Number field sieve (this volume)
- Pomerance (1996) – “A tale of two sieves” (Notices AMS)