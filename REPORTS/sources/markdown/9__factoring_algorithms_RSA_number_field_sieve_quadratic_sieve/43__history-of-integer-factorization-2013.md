---
title: "History of integer factorization"
title_en: "History of integer factorization"
source_type: "book_chapter"
authors: ["Wagstaff Jr. S. S."]
year: "2013"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "history-of-integer-factorization-2013.md"
---

# Content source: History of integer factorization

## Source type
Book chapter (from "The Joy of Factoring", Student Mathematical Library Vol. 68, American Mathematical Society, 2013, pp. 1–42). This appears to be a draft or preprint version of Chapter 1.

## Author affiliation
Samuel S. Wagstaff Jr. — Department of Computer Sciences, Purdue University (as of original ECM work); also affiliated with Center for Education and Research in Information Assurance and Security (CERIAS).

## Objective
Provide a comprehensive historical overview of integer factorization algorithms from ancient times to the early 2010s, covering trial division, Fermat's method, Pollard's methods, CFRAC, QS, ECM, NFS, and their impact on RSA cryptography, with predictions for the future.

## Core content summary

### 1. The Dark Ages: Before RSA (Section 1.1)

**Trial Division (ancient)**:
- Test divisibility by primes up to √n.
- Wheel method: skip composites by adding 2,4 (skips multiples of 2,3) or extended to mod 30.
- Quadratic residues can restrict possible prime divisors (Legendre symbol).

**Fermat's Difference of Squares (1643)**:
- Write n = x² − y² = (x−y)(x+y).
- Algorithm: x = ⌈√n⌉, r = x²−n, increment x until r is a square.
- Works quickly when factors are close; reason RSA primes should not be too close.

**Pollard's Rho (1975)**:
- Iterate f(x) = x² + b mod n.
- By birthday paradox, sequence mod p repeats after O(√p) steps.
- If u ≡ v (mod p) but u ≠ v (mod n), then gcd(u−v, n) = p.
- Complexity: O(√p). Finds small factors quickly.
- **Success**: Brent & Pollard factored F₈ (1980).

**Pollard's p−1 (1974)**:
- Based on Fermat: a^{p−1} ≡ 1 (mod p).
- Choose L = product of primes ≤ B (with powers).
- Compute a^L mod n; if p−1 divides L, then p divides gcd(a^L−1, n).
- **Example**: Baillie found 16‑digit factor of F₁₂ with B = 30,000,000.
- **Second stage** (B₂ > B): allows one large prime factor of p−1.

**Primality testing**:
- Early: trial division; "prime by failure to factor".
- Lehmer's theorem (c. 1914): m prime iff ∃ a with a^{m−1}≡1 mod m and a^{(m−1)/q}≠1 for every prime q|m−1 (requires factoring m−1).
- **Probable prime test** (Fermat): a^{m−1} ≡ 1 mod m.
- **Strong probable prime test** (Miller–Rabin): write m−1 = 2ᵉ·f, check a^f ≡ 1 or a^{f·2ᶜ} ≡ −1 for some c<e.
- **Baillie–PSW test** (1980): strong probable prime to base 2 + Lucas test; no known counterexample; $620 reward for counterexample.
- **AKS (2002)**: first deterministic polynomial‑time primality test; O((log m)¹²) originally, improved to ~O((log m)⁶).

### 2. The Enlightenment: RSA (Section 1.2)

**Diffie–Hellman (1976)**:
- One‑way functions, public key exchange.
- Man‑in‑the‑middle attack; digital signatures.

**RSA (Rivest, Shamir, Adleman, 1977)**:
- n = p·q, φ(n) = (p−1)(q−1).
- Choose e with gcd(e,φ(n))=1, compute d ≡ e⁻¹ mod φ(n).
- Encryption: C = Mᵉ mod n; Decryption: M = Cᵈ mod n.
- Security relies on difficulty of factoring n.
- **RSA‑129 challenge** (1977): 129‑digit product; Rivest estimated 40 quadrillion years; factored in 1994 (8 months, 1600 computers, 5000 MIPS‑years) using MPQS.

### 3. The Renaissance: Continued Fractions (CFRAC) (Section 1.3)

**Continued fraction of √n**:
- Convergents Aᵢ/Bᵢ satisfy Aᵢ² − nBᵢ² = (−1)ⁱQᵢ with |Qᵢ| < 2√n.
- Thus Aᵢ² ≡ (−1)ⁱQᵢ (mod n), and Qᵢ are small → more likely to be smooth.

**Morrison–Brillhart (1975)**:
- Factor base of primes where n is quadratic residue.
- Collect relations, use linear algebra over GF(2) to find subset whose product of Qᵢ is a square.
- **Large prime variation**: when cofactor after trial division is prime, match with another relation having same large prime.
- **Hardware implementation**: Smith & Wagstaff built EPOC machine with 16 parallel remaindering units.
- **Complexity** (Pomerance, heuristic): L(n)^{√2} where L(x)=exp(√(ln x ln ln x)).

### 4. The Reformation: Quadratic Sieve (QS) (Section 1.4)

**Key innovation**: replace trial division of Qᵢ by sieving.

**Sieve of Eratosthenes** for polynomial f(x) = x² − n:
- For each prime p in factor base, find roots of x² ≡ n (mod p) (0,1,2 solutions).
- For each root, step through arithmetic progression, divide out p.
- Time per value ≈ log log B (amortized), far faster than trial division.

**Multiple Polynomial Quadratic Sieve (MPQS)**: use many polynomials to keep values small.

**Large prime variation** (two large primes) used in RSA‑129 factorization.

**Records**: 
- 100‑digit number factored by Lenstra & Manasse (1988, front page NY Times).
- RSA‑129 (1994) by Atkins, Graff, Lenstra, Leyland.

### 5. The Revolution: Number Field Sieve (NFS) (Section 1.5)

**Special NFS (SNFS)** (Pollard 1988, Lenstra et al. 1990):
- For numbers of special form n = rᵉ − s with small r,|s|.
- Choose degree d, let k = ⌈e/d⌉, m = rᵏ, f(x) = xᵈ − s·r^{kd−e}.
- Then f(m) ≡ 0 (mod n).
- **Example**: F₉ = 2⁵¹² + 1 factored with f(x)=x⁵+8, m=2¹⁰³.

**General NFS (GNFS)** (Buhler, Lenstra, Pomerance 1993):
- Choose m ≈ n^{1/d}, write n in base m → coefficients cᵢ.
- f(x) = c_d x^d + ... + c₀.
- Work in algebraic number field Q(α) where α is root of f.
- Sieve two sides: rational side (a − bm) and algebraic side (norm of a − bα).
- Combine using linear algebra over GF(2) plus quadratic characters to ensure square in number field.

**Complexity**:
- SNFS: L_n[1/3, (32/9)^{1/3}] ≈ exp(1.526 (log n)^{1/3} (log log n)^{2/3})
- GNFS: L_n[1/3, (64/9)^{1/3}] ≈ exp(1.923 (log n)^{1/3} (log log n)^{2/3})

**Hardware proposals**: TWINKLE (Shamir, 1999) – optoelectronic sieving device.

### 6. An Exquisite Diversion: Elliptic Curve Method (ECM) (Section 1.6)

**Background** (Weierstrass form y² = x³ + ax + b over finite field):
- Points form an abelian group with point at infinity ∞.
- Addition formula: slope s = (y₂−y₁)/(x₂−x₁) if P≠Q; s = (3x₁²+a)/(2y₁) if P=Q.
- Then x₃ = s² − x₁ − x₂, y₃ = s(x₁−x₃) − y₁.
- **Fast point multiplication**: O(log i) group operations.

**Hasse's theorem**: |#E(F_p) − p − 1| ≤ 2√p.

**Lenstra's ECM (1985)**:
- Replace multiplicative group in Pollard p−1 with elliptic curve group over F_p.
- Order M = #E(F_p) is in Hasse interval.
- Choose random curve (by picking a and point P, setting b = y₁² − x₁³ − a x₁).
- Compute L = product of primes ≤ B (with powers), compute L·P mod n.
- If p divides L in the group (i.e., L·P = ∞ over F_p), then slope computation will attempt division by non‑invertible element → factor n.
- If one curve fails, try another random curve → independent chance.

**Complexity**: Expected work to find p is L(p)^{√2} point additions.

**Second stage** (B₂ > B) allows one larger prime factor of M.

**Modern ECM capabilities** (c. 2013):
- Factors up to 20 digits in seconds.
- Factors up to 40 digits in hours.
- Factors >60 digits require luck.
- **Record (2005)**: 66‑digit factor by Dodson.

**ECM in other contexts**:
- Elliptic curve cryptography (Miller, Koblitz 1987): smaller keys than RSA.
- Pairing‑based cryptography (Menezes–Okamoto–Vanstone, 1993).

### 7. Theoretical and Practical Aspects (Section 1.7)

**Rigorous factoring algorithms**:
- Trial division: O(√n).
- Pollard–Strassen: O(n^{1/4+ε}) (deterministic).
- Shanks' class group method: O(n^{1/5+ε}) assuming ERH.
- **Dixon's random squares** (1981): first rigorous subexponential algorithm, complexity L(n)^{3√2}.

**Attacks on RSA when parameters are poorly chosen**:
- If φ(n) or d is known, n can be factored (Theorem 1.15, 1.16, May 2004).
- Small d: Wiener (d < n^{1/4}/3) → continued fraction attack.
- Boneh–Durfee (d < n^{0.292}) → lattice attack (LLL).
- Sharing primes across keys (Lenstra et al. 2012) → GCD attack.

**Factoring with partial information** (Coppersmith, LLL):
- Given high or low bits of p, can factor n (Theorem 1.21: |p − \bar{p}| < n^{5/28}/2).
- Given small d, can factor n (Boneh–Durfee).

**The future of factoring** (author's predictions, 2013):
- Quantum computers (Shor 1994): polynomial time, but require millions of entangled qbits → not yet practical.
- Suggest new algorithms: combine NFS with lattices (Schnorr), find t = 1/4 algorithm, simulate Shor classically with nonlinear optimization.
- Prediction: slow increase in factoring capability over next century; no polynomial‑time classical algorithm likely.

**Factoring records** (Fermat numbers):

| m | NFac | Year | Method | Who |
|---|------|------|--------|-----|
| 5 | 2 | 1732 | Trial division | Euler |
| 6 | 2 | 1855 | Trial division + p≡1 mod 2ᵐ⁺² | Clausen & Landry |
| 7 | 2 | 1970 | CFRAC | Morrison & Brillhart |
| 8 | 2 | 1980 | Pollard Rho | Brent & Pollard |
| 9 | 3 | 1990 | SNFS | Lenstra, Manasse, et al. |
| 10 | 4 | 1995 | ECM | Brent |
| 11 | 5 | 1988 | ECM | Brent |

**New factoring algorithms invented every ~5 years (1970–1995)**:
- 1970 CFRAC (Morrison–Brillhart)
- 1975 Pollard p−1 and Rho (Pollard)
- 1980 Quadratic Sieve (Pomerance)
- 1985 ECM (H. W. Lenstra Jr.)
- 1990 SNFS (Pollard, Lenstra)
- 1995 GNFS (Pollard, Lenstra)

Author's question: "Why have we found no new faster factoring algorithms since 1995?" → suggests need for new approach.

## Key theoretical results

**Theorem 1.7**: For n with ≥2 distinct odd prime factors, random x,y with x²≡y² (mod n) yield nontrivial factor with probability ≥ 1/2.

**Theorem 1.11 (Hasse)**: p+1−2√p ≤ #E(F_p) ≤ p+1+2√p.

**Theorem 1.13 (Dixon)**: Average time of Dixon's random squares algorithm is L(n)^{3√2} (rigorous).

**Theorem 1.20 (May)**: Computing RSA secret key d is deterministic polynomial time equivalent to factoring n when ed ≤ n².

## Practical recommendations (for RSA key generation)

- Primes should not be too close (avoid Fermat factorization).
- p−1 and q−1 should have a large prime factor (avoid Pollard p−1).
- Private exponent d should not be too small (avoid Wiener, Boneh–Durfee attacks).
- Use strong probable prime test (Miller–Rabin) plus Lucas test (Baillie–PSW) for primality.
- Key length: 1024‑bit considered borderline by 2013; 2048‑bit recommended for long‑term security.

## Limitations (explicit from source)

- The chapter is historical; no new algorithms are presented.
- Complexity analyses are heuristic for QS, NFS, ECM (except Dixon's method).
- The Baillie–PSW primality test is conjectured but not proven correct.
- Quantum factoring (Shor) not yet practical.
- Predictions are speculative.

## References (selected, many historical)
- Agrawal, Kayal, Saxena (2004) – AKS primality test
- Boneh, Durfee (2000) – small d attack
- Buhler, Lenstra, Pomerance (1993) – GNFS origins
- Coppersmith (1996) – small root methods
- Crandall, Pomerance (2005) – Prime Numbers textbook
- Dixon (1981) – rigorous subexponential factoring
- Lenstra, Lenstra (1993) – NFS development
- Lenstra, Lenstra, Lovász (1982) – LLL algorithm
- Lenstra (1987) – ECM
- Morrison, Brillhart (1975) – CFRAC
- Pollard (1974, 1975) – p−1, Rho
- Pomerance (1982, 1985) – QS
- Rivest, Shamir, Adleman (1978) – RSA
- Shor (1994) – quantum factoring
- Silverman, Wagstaff (1993) – practical ECM analysis
- Wiener (1990) – small d attack
- Zimmermann, Dodson (2006) – 20 years of ECM
