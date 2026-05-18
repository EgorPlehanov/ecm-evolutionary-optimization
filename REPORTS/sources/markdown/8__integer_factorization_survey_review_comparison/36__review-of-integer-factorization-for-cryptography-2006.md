---
title: "Review of Methods for Integer Factorization Applied to Cryptography"
title_en: "Review of Methods for Integer Factorization Applied to Cryptography"
source_type: "article"
authors: ["Rabah K."]
year: "2006"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "review-of-integer-factorization-for-cryptography-2006.md"
---

# Content source: Review of Methods for Integer Factorization Applied to Cryptography

## Source type
Peer-reviewed journal article (Journal of Applied Sciences, Vol. 6, No. 2, pp. 458–481, 2006). Asian Network for Scientific Information.

## Author affiliation
Kefa Rabah — Department of Physics, Eastern Mediterranean University, Gazimagusa, North Cyprus, via Mersin 10, Turkey.

## Objective
Provide a comprehensive review of integer factorization algorithms with emphasis on their application to cryptanalysis of the RSA public-key cryptosystem, including practical examples, complexity analysis, and historical records.

## Core content summary

### 1. RSA cryptosystem and factorization
- RSA security relies on the difficulty of factoring n = p·q.
- Public key (e, n), private key d with ed ≡ 1 (mod (p−1)(q−1)).
- If n can be factored, the private key is compromised.
- Key length recommendations (Fig. 1): 1024‑bit for near‑term security, 2048‑bit for long‑term.

**Historical factoring milestones (as of 2006):**

| Year | Number | Digits | Method | Notes |
|------|--------|--------|--------|-------|
| 1970 | 20 digits | 20 | trial division | state of the art |
| 1980 | 70 digits | 70 | CFRAC | Morrison–Brillhart |
| 1990 | 116 digits | 116 | QS | record |
| 1994 | RSA‑129 | 129 | MPQS (distributed) | 5000 MIPS‑years |
| 1999 | RSA‑155 | 155 (512‑bit) | NFS | CWI, factor of 512‑bit RSA key |
| 2005 | RSA‑200 | 200 | GNFS | Bahr et al. |
| 2005 | Cunningham | 248 | SNFS | Aoki et al. (CRYPTREC) |

### 2. Classification of factoring methods

| Category | Algorithms | Complexity depends on |
|----------|------------|----------------------|
| Special‑purpose (find small factors) | Trial division, Pollard Rho, P−1, P+1, ECM | size of smallest factor p |
| General‑purpose (factor any number) | CFRAC, QS, MPQS, NFS (SNFS/GNFS) | size of N itself |

### 3. Pollard's P−1 method (Section "Pollard's (p−1)-method")
- Based on Fermat's little theorem: a^(p−1) ≡ 1 (mod p).
- If p−1 is B‑powersmooth, then a^M ≡ 1 (mod p) where M = lcm(1,…,B).
- Compute d = gcd(a^M − 1, N). If 1 < d < N, factor found.
- **Example**: N = 172189 = 421·409. p−1 = 2³·3·5·7, q−1 = 2³·3·17. B = 7…16 works.
- **Large prime variant**: allows one extra prime factor between B and B'.
- **Limitation**: fails if both p−1 and q−1 have large prime factors.

### 4. Elliptic Curve Method (ECM)
- Invented by H. W. Lenstra Jr. (1985, published 1987).
- Generalizes P−1 by replacing multiplicative group (order p−1) with group of points on a random elliptic curve over F_p (order p+1−t, |t| ≤ 2√p).
- By varying the curve, different group orders are obtained → higher chance of smoothness.
- **Hasse's theorem**: |#E(F_p) − p − 1| < 2√p.

**Example** (from paper):
- N = 963 = 9·107.
- Curve: y² = x³ + ax + 9 with point Q = (8,23).
- B = 3, m = 2⁶·3⁴.
- During computation of λ, denominator 315 shares factor 9 with N → factor found.

**Improvements noted**:
- Brent (1986): birthday‑paradox second phase.
- Montgomery (1987): homogeneous coordinates (XZ), 6M per addition, 5M per doubling; group order divisible by 12 or 16.
- ECM used to factor F₁₀, F₁₁ (Brent, 1988).

**Record (as of 2005)**: 66‑digit factor by Dodson (April 2005).  
Brent's extrapolation: 70 digits by 2010, 85 by 2018, 100 by 2025.

### 5. Pollard's Rho method
- Iterates polynomial f(x) = x² + 1 (mod N).
- Sequence modulo prime p eventually periodic.
- Floyd's cycle detection: test gcd(x_{2n} − x_n, N).
- Complexity: O(√p) iterations → O(N^{1/4}(log N)²) bit operations.
- **Brent's variant**: ~24% faster.
- **Example**: N = 5561 = 67·83 found via gcd(5080−3171, N).

### 6. Quadratic Sieve (QS) and Multiple Polynomial QS (MPQS)

**Basic QS** (Pomerance, 1985):
- Sieve values Q(x) = x² − N for x near ⌊√N⌋.
- Find x such that Q(x) is smooth over factor base of primes where (N/p) = 1.
- Build exponent vectors, solve linear system over GF(2) → square on both sides.
- Complexity: L[1/2, 1] = exp((1+o(1))√(log N log log N)).

**Example** (N = 45313 = 113·401):
- Factor base = {2,3,7,11,17,19,23,37,41}.
- Sieve range x = 200…225.
- Combine Q(214), Q(220), Q(223) → X = 31537, Y = 35831.
- gcd(31537−35831, 45313) = 113, gcd(31537+35831, 45313) = 401.

**MPQS** (Montgomery, Davis & Holdridge):
- Uses multiple quadratic polynomials g(x) = a²x² + 2bx + c with b² − 4a²c = N.
- Each polynomial sieved over short interval → residues ≈ aM² − N/a (much smaller than QS).
- Easily parallelized: assign different polynomials to different processors.
- Used in RSA‑129 factorization (1994): 524,339 primes in factor base, 5000 MIPS‑years, 2 GB data.

### 7. Index Calculus method
- Choose factor base of small primes.
- Find relations a_i² ≡ ∏ p_j^{α_{ij}} (mod N).
- Solve linear system over GF(2) to get squares on both sides.
- Complexity: O(exp(√(n log n))) for n‑bit N.
- Historical importance: led to NFS.

### 8. Number Field Sieve (NFS)

**General NFS (GNFS)**:
- Uses two monic irreducible polynomials f, g with small coefficients and common root m (mod N).
- Work in number fields Q(α) and Q(β) where α root of f, β root of g.
- Sieve over (a,b) pairs: F(a,b) = b^{deg f} f(a/b) and G(a,b) = b^{deg g} g(a/b) both smooth.
- Linear algebra over prime ideals in the two fields.
- Square root step (Couveignes for odd degree, Montgomery for any degree).

**Special NFS (SNFS)**: for numbers of special form (e.g., r^e ± s with r,s small). Faster constant factor.

**Complexity**:
- GNFS: L[1/3, (64/9)^{1/3}] ≈ exp(1.923 (log N)^{1/3} (log log N)^{2/3})
- SNFS: L[1/3, (32/9)^{1/3}] ≈ exp(1.526 (log N)^{1/3} (log log N)^{2/3})
- Coppersmith variant (many polynomials): c = (92+26√13)^{1/3}/3 ≈ 1.902

**Estimated MIPS‑years for GNFS (Table in paper):**

| Bits | MIPS‑years |
|------|------------|
| 512  | 30,000 |
| 768  | 2×10⁶ |
| 1024 | 3×10¹¹ |
| 1280 | 1×10⁴ |
| 1536 | 3×10⁶ |
| 2048 | 3×10²⁰ |

**Special‑purpose hardware proposals**:
- TWINKLE (Shamir)
- TWIRL (Shamir & Tromer, 2003): estimate $10M machine could factor 1024‑bit RSA modulus in <1 year.

### 9. Quantum factoring (Shor 1994, 1997)
- Polynomial‑time quantum algorithm for integer factorization and discrete logarithms.
- Would break RSA if large‑scale quantum computer built.
- Not yet practical; long‑term concern.

## Key practical recommendations (as of 2006)
1. For numbers with smallest prime factor ≤ 30 digits → use ECM.
2. For numbers with smallest factor > 30 digits and size ≤ 90 digits → use MPQS.
3. For numbers > 100 digits → use GNFS.
4. RSA key length recommendation: at least 1024 bits; 2048 bits for long‑term security.

## Limitations (explicit from source / context)
- Survey as of 2006; records and recommendations are dated.
- Some complexity expressions use n as integer (not bit length) inconsistently.
- Example factorizations use very small numbers; real‑world parameters are much larger.
- The paper is a review; original contributions are limited to exposition and examples.
- ECM complexity is heuristic (assumes random group orders behave like random integers near p).

## References cited (selected)
- Lenstra (1987) — ECM
- Montgomery (1987) — Speeding ECM
- Brent (1986) — ECM improvements
- Pomerance (1985) — QS
- Montgomery — MPQS
- Lenstra & Lenstra (1993) — NFS
- Pollard (1974, 1975) — P−1, Rho
- Shor (1994, 1997) — quantum factoring
- Cowie et al. (1996) — RSA‑155 factorization
- Morrison & Brillhart (1975) — CFRAC, F₇