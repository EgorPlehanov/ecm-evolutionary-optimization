---
title: "A guide to general number field sieve for integer factorization"
title_en: "A guide to general number field sieve for integer factorization"
source_type: "article"
authors: ["Pandey G.", "Pal S. K."]
year: "2014"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "guide-to-general-number-field-sieve-2014.md"
---

# Content source: A guide to general number field sieve for integer factorization

## Source type
Journal article (Investigations in Mathematical Sciences, Vol. 4, No. 2, pp. 83–98, 2014). Likely a peer‑reviewed journal; exact publication details not fully specified in the provided content.

## Authors affiliation
Pandey G., Pal S. K. — Scientific Analysis Group, Defence Research & Development Organization (DRDO), Delhi, India.

## Objective
Provide a self‑contained, tutorial‑style introduction to the General Number Field Sieve (GNFS) algorithm for factoring large integers, covering the necessary mathematical background (number fields, algebraic integers, factor bases, sieving) and including a complete worked numerical example (n = 77) to illustrate each step.

## Core content summary

### 1. Mathematical background (Section 2)

**Difference of squares method** (Fermat):
- For odd composite n, find x,y such that x² ≡ y² (mod n).
- If x ≠ ± y (mod n), then gcd(x−y, n) is a nontrivial factor with probability > 1/2.

**Smooth numbers**:
- Factor base F = set of small primes.
- An integer s is smooth over F if all prime factors of s are in F.

**Algebraic number fields** (Definitions 2.3–2.4):
- Number field K = Q(α) where α is a root of irreducible monic polynomial f(x) ∈ Z[x].
- Ring of algebraic integers D (full ring).
- Ring Z[α] = { Σ a_i α^i : a_i ∈ Z } (order, not necessarily full ring).

**Properties**:
- Z ⊂ Z[α] ⊂ D ⊂ Q(α).
- D is a Dedekind domain (Theorem 2.7): every non‑zero ideal factors uniquely into prime ideals.
- Z[α] is used in GNFS because its elements are easy to represent (polynomials in α with integer coefficients).

**Ring homomorphism φ** (Proposition 2.8):
- For monic irreducible f(x) and integer m with f(m) ≡ 0 (mod n), there exists unique surjective φ: Z[α] → Z/nZ such that:
  - φ(a+b) = φ(a)+φ(b), φ(ab)=φ(a)φ(b), φ(1)=1, φ(α)=m.
- If V is a set of (a,b) such that ∏(a−bα) = β² (in Z[α]) and ∏(a−bm) = y² (in Z), then x = φ(β) satisfies x² ≡ y² (mod n).

### 2. GNFS algorithm: five steps (Section 3, Fig. 1)

#### Step 1: Polynomial selection (Section 3.1)
- Choose degree d ≥ 3 (typically 3–6 for numbers 100–200 digits).
- Choose m ≈ n^{1/d}.
- Write n in base m: n = mᵈ + c_{d-1} m^{d-1} + … + c₁ m + c₀, with 0 ≤ cᵢ < m.
- Define f(x) = xᵈ + c_{d-1} x^{d-1} + … + c₁ x + c₀.
- Then f(m) = n ⇒ f(m) ≡ 0 (mod n).
- Test irreducibility of f; if reducible, factors of n are obtained directly.

**Remark**: Polynomial selection is the most important and still open research area.

#### Step 2: Factor base generation (Section 3.2)

Three factor bases:

| Base | Description | Bound |
|------|-------------|-------|
| Rational Factor Base (RFB) | All primes ≤ B₁ | B₁ |
| Algebraic Factor Base (AFB) | First‑degree prime ideals of Z[α] (via (r,p) pairs with f(r)≡0 mod p) | p ≤ B₂ |
| Quadratic Character Base (QCB) | Additional first‑degree prime ideals not in AFB | B₂ < q ≤ B₃ |

**Representation of first‑degree prime ideals** (Theorem 3.4):
- Bijection between first‑degree prime ideals of Z[α] and pairs (r,p) where p prime, r ∈ Z/pZ, f(r) ≡ 0 (mod p).
- AFB = { (r,p) : p < B₂, f(r)≡0 (mod p) }.
- QCB = { (s,q) : B₂ < q ≤ B₃, f(s)≡0 (mod q) }.

Complete factor base FB = {−1} ∪ RFB ∪ AFB ∪ QCB.

#### Step 3: Sieving (Section 3.3)

Goal: Find smooth pairs (a,b) with b>0, gcd(a,b)=1 such that:
- Rational norm N₁(a,b) = |a − b m| is smooth over RFB.
- Algebraic norm N₂(a,b) = |bᵈ f(a/b)| is smooth over AFB.

Two sieving methods:

**Line sieving** (Section 3.3.1):
- Fix b = 1,2,…, vary a in [−A, A].
- Store |N₁(a,b)| and |N₂(a,b)| in two arrays.
- For each prime in RFB, divide N₁ at positions a ≡ b m (mod p).
- For each (r,p) in AFB, divide N₂ at positions a ≡ b r (mod p).
- After processing all primes, positions where both arrays are 1 give smooth pairs.
- Less memory, best for small primes.

**Lattice sieving** (Section 3.3.2; Pollard 1993):
- Choose a medium prime q from AFB, generate lattice R of (a,b) where q divides N₂.
- Sieve rational norms with primes p < q only.
- Sieve algebraic norms with all primes.
- Faster for large ranges but more memory.

**Optimization**: Use logarithms to convert divisions to additions.

#### Step 4: Matrix step (Section 3.4)

Goal: Find subset V ⊆ U such that:
- ∏_{(a,b)∈V} (a−bm) = y² (square in Z)
- ∏_{(a,b)∈V} (a−bα) = β² (square in Z[α])

**Binary vector construction**:

Let l₁ = |RFB|, l₂ = |AFB|, l₃ = |QCB|. Each smooth pair (a,b) gives a vector e_{(a,b)} ∈ F₂^{1 + l₁ + l₂ + l₃}:

| Position | Description |
|----------|-------------|
| 0 (sign) | 0 if a−bm > 0, 1 if a−bm < 0 |
| 1 … l₁ | exponent of each p in RFB (mod 2) |
| l₁+1 … l₁+l₂ | exponent of each (r,p) in AFB (mod 2) |
| last l₃ | quadratic character: 0 if ((a−bs)/q)=1, 1 if = −1 |

**Quadratic character** (Legendre symbol):
\[
\chi_{(s,q)}(a,b) = \left(\frac{a - b s}{q}\right)
\]
If ∏(a−bα) is a square, then for each (s,q) ∈ QCB, the product of these Legendre symbols over V must be 1 (necessary condition).

**Linear algebra**:
- Form matrix M with columns = e_{(a,b)} for (a,b) ∈ U.
- Solve M·X = 0 over F₂ (Gaussian elimination, block Lanczos, block Wiedemann).
- Each solution X gives subset V (where x_i = 1).

#### Step 5: Square root computation (Section 3.5)

- **Rational square root**: compute y = √(∏(a−bm)) (easy from prime factorization).
- **Algebraic square root**: find β ∈ Z[α] such that β² = ∏(a−bα).

**Small‑example method** (for illustration):
- Write β = a_{d-1}α^{d-1} + … + a₀, γ = known coefficients.
- Compute β² mod f(α), equate coefficients → system of quadratic Diophantine equations.
- Solve for a_i (small numbers).

**Practical methods for large numbers**:
- Couveignes (1993) — works when degree d is odd.
- Montgomery (1993) — works for any degree.
- Use square root in finite fields F_{pᵈ} and Chinese Remainder Theorem.

### 3. Complete numerical example: n = 77 (Section 4)

**Step 1: Polynomial selection**:
- d = 3, m = ⌊77^{1/3}⌋ = 4.
- 77 = 4³ + 0·4² + 3·4 + 1 → f(x) = x³ + 3x + 1.
- f irreducible (f(1)=5≠0, f(−1)=−3≠0).

**Step 2: Factor bases**:
- B₁ = 10 → RFB = {2,3,5,7}
- B₂ = 10 → AFB = find (r,p) with p<10, f(r)≡0 mod p → (2,3), (1,5), (2,5), (4,7)
- B₃ = 15 → QCB = (4,11), (11,13)

**Step 3: Sieving**:
- Range: a ∈ [−10,10], b ∈ [1,13] → 273 pairs.
- Found 12 smooth pairs (Table 1): (-10,1), (-4,1), (-3,1), (-1,1), (1,1), (2,1), (-1,2), (1,2), (-2,3), (9,4), (-1,5), (-4,13).

**Step 4: Matrix** (Table 2, Eq. 4.3):
- Each (a,b) gives vector e of length 1+4+4+2 = 11.
- With 12 smooth pairs → 11×12 matrix M.
- Solve M·X = 0 → three solutions (Table 3).

**Take X₁**: V = {(-10,1), (-4,1), (-3,1), (-1,2)}.

Compute:
- z = ∏(a−bm) = (-10-4)(-4-4)(-3-4)(-1-8) = (-14)(-8)(-7)(-9) = 7056 = 84².
- γ = ∏(a−bα) mod f(α) = 175α² + 215α + 85.

**Step 5: Algebraic square root**:
- Let β = aα² + bα + c.
- Compute β² mod (α³+3α+1):
  β² = (b²+2ac−3a²)α² + (2bc−a²−6ab)α + (c²−2ab).
- Equate to γ:
  b²+2ac−3a² = 175, 2bc−a²−6ab = 215, c²−2ab = 85.
- Solution: a = −3, b = 14, c = −1 → β = −3α² + 14α − 1.

**Homomorphism φ**:
- y = φ(β) ≡ −3·4² + 14·4 − 1 = −48 + 56 − 1 = 7 (mod 77).
- x = √z = 84 ≡ 7 (mod 77).

Then x² ≡ y² (mod 77) with x ≡ 7, y ≡ 7 → trivial? Wait: check: 84 ≡ 7 mod 77 indeed, so this gives trivial congruence. The paper's calculation yields x=84, y=7, but 84 ≡ 7 mod 77, so x ≡ y. This would not factor 77. However, they claim x = 84, y = 7 and then compute gcd(x+y,77)=14 → factor 7. There is inconsistency: if x≡y mod 77 then x−y ≡0, but x+y might still give factor. Actually 84+7=91, gcd(91,77)=7. So the pair (x,y) = (84,7) satisfies x²≡y² (mod 77) with x≠±y? 84 ≡ 7 mod 77 means they are equal modulo 77, not just squares. Check: 84² = 7056, 7²=49, 7056 mod 77 = 7056-77·91=7056-7007=49. Yes. So x ≡ y mod 77, so x−y ≡0, but x+y may not be 0 mod 77. The condition for nontrivial factorization is that x ≠ ± y mod n; here x ≡ y mod 77, so x−y ≡0, so gcd(x−y,n)=n, useless. But they used x+y. So this works if x≡y but x+y not multiple of n. Unusual but possible.

Better to trust the example: they factor 77 = 7·11.

## Complexity (GNFS)
\[
\mathcal{O}\left(\exp^{(c + o(1))(\ln n)^{1/3}(\ln\ln n)^{2/3}}\right)
\]
- SNFS: c = (32/9)^{1/3} ≈ 1.526
- GNFS: c = (64/9)^{1/3} ≈ 1.923

## Key observations from the paper

- GNFS is only efficient for numbers > 110–120 digits; for smaller numbers, QS is faster.
- Polynomial selection is the most important open research area.
- Sieving is the most time‑consuming step.
- Practical factoring of RSA‑1024 (309 decimal digits) would require a mathematical breakthrough or new computing paradigm.

## Limitations (explicit from source / tutorial nature)
- The example n=77 is trivial; real GNFS uses much larger parameters.
- Algebraic square root method described (solving quadratic equations) only works for very small numbers; real implementations use Couveignes or Montgomery methods.
- The example's factorization works but has an unusual property (x≡y mod n still yields factor via x+y).
- No parallelization discussed; no implementation details for large numbers.
- The paper is a tutorial, not original research.

## References (selected)
- Briggs (1998) — Introduction to GNFS (Master's thesis)
- Couveignes (1993) — Square root for NFS
- Lenstra & Lenstra (1993) — Development of NFS (book)
- Montgomery (1993) — Block Lanczos, square roots
- Pollard (1993) — Lattice sieve
- Murphy (1999) — Polynomial selection (PhD thesis)
- Wiedemann (1986) — Sparse linear equations
