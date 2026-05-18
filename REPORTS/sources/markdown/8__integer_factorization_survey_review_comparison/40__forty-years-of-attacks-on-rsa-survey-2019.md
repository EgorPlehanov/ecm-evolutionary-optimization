---
title: "Forty years of attacks on the RSA cryptosystem: A brief survey"
title_en: "Forty years of attacks on the RSA cryptosystem: A brief survey"
source_type: "article"
authors: ["Mumtaz M.", "Ping L."]
year: "2019"
source_link: "https://doi.org/10.1080/09720529.2018.1564201"
doi: "10.1080/09720529.2018.1564201"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "forty-years-of-attacks-on-rsa-survey-2019.md"
---

# Content source: Forty years of attacks on the RSA cryptosystem: A brief survey

## Source type
Peer-reviewed journal article (Journal of Discrete Mathematical Sciences and Cryptography, Vol. 22, No. 1, pp. 9–29, 2019). Taylor & Francis.

## Authors affiliation
Majid Mumtaz, Luo Ping — State Key Laboratory of Information Security, Institute of Software Systems and Engineering, School of Software, Tsinghua University, Beijing, China.

## Objective
Provide a comprehensive survey of attacks on the RSA cryptosystem over its first forty years (1977–2017), covering integer factorization attacks, elementary attacks, weak public/private exponent attacks (especially lattice‑based methods using Coppersmith's technique), and open challenges.

## Core content summary

### 1. RSA preliminaries
- \(N = p \cdot q\) (product of two large distinct primes of equal bit‑size)
- \(\phi(N) = (p-1)(q-1)\)
- Public key \((e, N)\), private key \(d\) with \(e \cdot d \equiv 1 \pmod{\phi(N)}\)
- Encryption: \(c = m^e \bmod N\), Decryption: \(m = c^d \bmod N\)
- RSA key equation: \(ed - 1 = k \cdot \phi(N)\) for some integer \(k\)

### 2. Integer Factorization Problem (IFP) – Section 2

**Classical factoring algorithms**:
- Quadratic Sieve (QS, 1984) – Pomerance
- Elliptic Curve Method (ECM, 1987) – Lenstra
- General Number Field Sieve (GNFS, 1990) – Lenstra, Lenstra, Manasse, Pollard

**GNFS complexity**:
- General case: \(L_n[1/3, (64/9)^{1/3}] \approx \exp(1.923 (\log N)^{1/3} (\log \log N)^{2/3})\)
- Special case (SNFS): \(L_n[1/3, (32/9)^{1/3}] \approx \exp(1.526 (\log N)^{1/3} (\log \log N)^{2/3})\)

**Record (as of 2010)**: RSA‑768 (232 decimal digits / 768 bits) factored by Kleinjung et al. (2010) using GNFS with hundreds of machines.

### 3. Elementary attacks – Section 3

**Common modulus attack**:
- If same message M encrypted with same modulus N but different exponents \(e_1, e_2\):
- Adversary knows \(C_1 = M^{e_1} \bmod N\), \(C_2 = M^{e_2} \bmod N\)
- Finds \(a, b\) such that \(a e_1 + b e_2 = 1\) (extended Euclidean)
- Then \(C_1^a C_2^b \equiv M \pmod{N}\)

**Blind signature attack** (Chaum, 1984):
- Attacker can disguise message before signing, then extract valid signature.
- Randomized padding schemes (e.g., PKCS#1) prevent this.

### 4. Weak public exponent attacks – Section 4

**Håstad's broadcast attack** (1988):
- Same message \(m\) encrypted with \(e\) different moduli \(N_1, \ldots, N_e\), pairwise coprime.
- If \(m < \min N_i\), adversary can recover \(m\) by Chinese Remainder Theorem.

**Franklin‑Reiter related message attack** (1996):
- For \(e = 3\), if two messages satisfy \(m_2 = m_1 + b\) with known \(b\), the attacker can recover both messages.

**Coppersmith's short pad attack** (1996–97):
- For \(e = 3\), if \(m_2 = m_1 + b\) with \(|b| < N^{1/9}\), attacker recovers \(m_1, m_2\) in polynomial time.
- **Lesson**: Low public exponent (\(e=3\)) requires strong random padding.

**Coppersmith's univariate modular root finding (Theorem 3)**:
- Finds all integer solutions \(x_0\) of \(p(x_0) \equiv 0 \pmod{N}\) with \(|x_0| < N^{1/k}\) in polynomial time (where \(k = \deg p\)).
- Basis for many lattice attacks.

### 5. Weak private exponent attacks – Section 5

#### Wiener's continued fraction attack (1990)
- If \(d < \frac{1}{3} N^{1/4}\), then \(k/d\) is a convergent of \(e/N\).
- Once \(k, d\) known, \(\phi(N) = (ed-1)/k\) is exposed → factor \(N\).
- **Countermeasure**: Use larger \(d\) or \(e > N^{3/2}\).

**Variants** (Table 2):
- Verheul & van Tilborg (1997): \(d \le r N^{0.25}\), \(r \approx 1/4\)
- Dujella (2004): \(d < 4.04 \sqrt{N}\)
- Aono (2009): \(d \le N^{0.292}\)
- Nitaj (2011): \(d \le N^{3/4-\varepsilon}\)

#### Boneh‑Durfee lattice attack (1998–1999) – Section 5.1.3
- **Key result** (Theorem 4): If \(d < N^{0.292}\), then \(N\) can be factored in polynomial time.
- Method: Use Coppersmith's method (Howgrave‑Graham reformulation) to find small roots of bivariate polynomial:
  \[
  f(x, y) = x(N + y) + 1,\quad x = -k,\; y = -(p+q)
  \]
- Improves Wiener's bound \(N^{0.25} \to N^{0.292}\).
- **Open problem**: Improve bound beyond \(0.292\) (theoretical limit conjectured \(0.5\) but unproven).

**Coron's simplified approach (2004)** – Section 5.1.4:
- Full rank lattice with triangular basis.
- If high‑order \((1/4 + \epsilon)\log_2 N\) bits of \(p\) known, factor \(N\) in polynomial time.

### 6. Large private exponent attack – Section 6

**Special case \(d > e\)** (Luo et al., 2009):
- If \(e < d\) and \(d < N^{0.5}\) (under algebraic independence assumption), \(N\) can be factored.

### 7. Challenges and advancements – Section 7

**Bound optimization**:
- Univariate case: maximize root bound \(x_0\).
- Multivariate case: complex, depends on Newton polytope geometry.
- Example: For \(g(x,y) = xy - N\), Coppersmith gives \(XY \le N^{1-\epsilon}\).

**Multivariate polynomial solution (rigorous vs. heuristic)**:
- Bivariate: resultant method works reliably.
- Trivariate: results are heuristic; depends on algebraic independence assumption.
- Bauer & Joux (2007): iterative LLL + Gröbner basis for special polynomial shapes.

**Limitations of Coppersmith's method**:
- Enabling condition \(|\Lambda| \le e^{m(n-1)} (n2^n)^{(1-n)/2}\) restricts applicability.
- Long discarded vectors may contain useful information (Miller, Narayanan, Venkatesan 2017).

### 8. Conclusion (Section 8)

- RSA remains secure after 40 years when properly implemented.
- All known attacks exploit improper parameter selection or implementation flaws, not the core RSA problem.
- Recommendations:
  - Avoid common modulus.
  - Use large public exponent (e.g., \(e = 65537\)) — speeds up encryption.
  - Use CRT‑RSA for resource‑constrained devices.
  - Use randomized padding (PKCS#1, OAEP) to prevent deterministic attacks.
- A well‑implemented RSA is widely trusted.

## Key theorems summarized

| Theorem | Description | Bound |
|---------|-------------|-------|
| Wiener (1990) | \(d < N^{1/4}\) → factor N | \(N^{0.25}\) |
| Boneh‑Durfee (1998–99) | \(d < N^{0.292}\) → factor N (lattice) | \(N^{0.292}\) |
| Coppersmith (1996) | Univariate modular root | \(|x_0| < N^{1/k}\) |
| Coron (2004) | High bits of p known (\(1/4 + \varepsilon\)) | Factor N |

## Attacks classification

| Category | Examples |
|----------|----------|
| Integer factorization | GNFS, ECM, QS |
| Elementary | Common modulus, blind signature |
| Weak public exponent | Håstad, Franklin‑Reiter, Coppersmith short pad |
| Weak private exponent | Wiener (continued fraction), Boneh‑Durfee (lattice), Coron |
| Implementation | Timing, power analysis, fault injection (not covered in detail) |

## Limitations (explicit from source)

- Survey is brief; many attacks only summarized, not fully explained.
- Implementation attacks (side‑channel, fault injection) mentioned but not elaborated.
- Quantum attacks (Shor's algorithm) not discussed (focus on classical).
- Some bounds (e.g., \(d < N^{0.292}\)) are heuristic; no rigorous proof that larger \(d\) is safe.
- Multivariate Coppersmith results are heuristic; no general rigorous method.

## References (selected)
- Rivest, Shamir, Adleman (1978) – RSA
- Wiener (1990) – short secret exponent attack
- Boneh & Durfee (1998–99) – lattice attack on \(d < N^{0.292}\)
- Coppersmith (1996–97) – small root methods
- Lenstra et al. (1990) – NFS
- Kleinjung et al. (2010) – RSA‑768 factorization
- Howgrave‑Graham (1997) – reformulation of Coppersmith
- Coron (2004) – simplified bivariate Coppersmith
- Jochemsz & May (2006) – multivariate strategy
- Herrmann & May (2010) – unravelled linearization
