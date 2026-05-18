---
title: "The State of the Art in Integer Factoring and Breaking Public-Key Cryptography"
title_en: "The State of the Art in Integer Factoring and Breaking Public-Key Cryptography"
source_type: "article"
authors: ["Boudot F.", "Gaudry P.", "Guillevic A.", "Heninger N.", "Thomé E.", "Zimmermann P."]
year: "2022"
source_link: "https://doi.org/10.1109/MSEC.2022.3141918"
doi: "10.1109/MSEC.2022.3141918"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "state-of-the-art-integer-factoring-2022.md"
---

# Content source: The State of the Art in Integer Factoring and Breaking Public-Key Cryptography

## Source type
Peer-reviewed journal article (IEEE Security and Privacy Magazine, Vol. 20, No. 2, March–April 2022, pp. 80–86).

## Authors affiliation
- Boudot — Université de Limoges, XLIM, France
- Gaudry, Guillevic, Thomé, Zimmermann — Université de Lorraine, CNRS, Inria, LORIA, Nancy, France
- Heninger — University of California, San Diego, USA

## Objective
Survey the current state of the art (as of 2022) in classical (non‑quantum) cryptanalysis of the three fundamental number‑theoretic problems underpinning public‑key cryptography: integer factorization (RSA), discrete logarithms in finite fields (Diffie‑Hellman, DSA), and discrete logarithms on elliptic curves (ECDH, ECDSA, Ed25519). Emphasis is placed on the General Number Field Sieve (GNFS) and its variants, recent records, and practical progress.

## Core content summary

### 1. Integer factorization and RSA (Section 1)

**General Number Field Sieve (GNFS) sketch**:
- Based on constructing a congruence of squares: find X, Y with X² ≡ Y² (mod N) and X ≠ ± Y (mod N) → gcd(X−Y, N) factors N.
- Two main phases:
  1. **Relation collection** (embarrassingly parallel): find many (a,b) pairs such that both rational side (a − bm) and algebraic side (norm of a − bα) are smooth over chosen factor bases.
  2. **Linear algebra** over F₂ (block Wiedemann): combine relations to obtain a square product.
- **Polynomial selection**: choose a monic irreducible polynomial f(x) and integer m with f(m) ≡ 0 (mod N). Degree d ≈ (log N / log log N)^{1/3}. Quality of polynomial critically affects runtime.

**Asymptotic complexity** (heuristic):
\[
\exp\left((64/9)^{1/3} (\log N)^{1/3} (\log \log N)^{2/3} (1+o(1))\right) \approx \exp\left(1.923 (\log N)^{1/3} (\log \log N)^{2/3}\right)
\]

**Practical progress (1990s–2020s)**:
- Despite unchanged asymptotic complexity, constant‑factor improvements have been significant:
  - Better polynomial selection (Kleinjung, 2017; “ideal” polynomials would halve sieving cost – open problem).
  - Improved relation collection algorithms and parameter tuning via simulations.
  - Block Wiedemann linear algebra effectively parallelized; memory no longer the bottleneck.
- **Records** (Fig. 2, Table in text):
  - RSA‑240 (795 bits, 240 decimal digits) factored in 2019.
  - **RSA‑250** (829 bits, 250 decimal digits) factored in **February 2020** – cost ≈ 2,700 core‑years.
- **1024‑bit RSA** (309 decimal digits) estimated ~500,000 core‑years, matrix ~4 billion rows/columns → feasible for state‑level attacker.

### 2. Finite field discrete logarithms (DLP) and Diffie‑Hellman (Section 2)

**Number Field Sieve for Discrete Logarithms (NFS‑DL)**:
- Similar structure to GNFS but linear algebra modulo prime group order (not F₂) → more expensive.
- Polynomial selection can be optimized for fields (not rings), giving up to 5× speedup.
- Precomputation (polynomial selection, sieving, linear algebra) depends only on the modulus p, not on the target logarithm → offline attack possible (Adrian et al., 2015).

**Records** (Fig. 2):
- 795‑bit DLP (240 decimal digits) in 2020: 3,100 core‑years, about 3× harder than factoring same size.
- Historically DLP records lag factoring by several years.

**Small characteristic case (GF(pⁿ) with small p)**:
- Breakthrough (Barbulescu–Gaudry–Joux–Thomé 2014, Kleinjung–Wesolowski 2021): **quasi‑polynomial** (n^{O(log n)}) time algorithms for GF(2ⁿ).
- Consequence: binary fields no longer secure for cryptography; supersingular elliptic curves over binary fields deprecated.

**Medium‑degree extension fields (pairing‑friendly curves)**:
- Tower NFS (TNFS) and variants; current record: 521‑bit computation in degree‑6 field (De Micheli–Gaudry–Pierrot, 2021).
- Ongoing progress makes security assessments challenging.

### 3. Elliptic curve discrete logarithms (ECDLP) (Section 3)

**Current best algorithms**: Pollard rho and parallel collision search.
- Expected runtime: O(√n) group operations where n is group order (exponential in key size).
- **Record**: 114 bits (as of 2022). Progress largely from Moore's law and faster implementations, not algorithmic breakthroughs.

**No index‑calculus (NFS‑like) improvement** for cryptographically relevant curves:
- Generic algorithms remain the best.
- Pairing‑friendly curves allow transfer of ECDLP to finite field DLP → must ensure field size is large enough.
- Binary fields of prime extension degree have not seen quasi‑polynomial breakthrough (unlike GF(2ⁿ) DLP).

### 4. Prospects for the future (Section 4)

**Quantum threat** (Shor's algorithm):
- Would break RSA, finite‑field DLP, and ECDLP in polynomial time on a sufficiently large quantum computer.
- Whether such a quantum computer can be built remains an open question (National Academies 2019).

**Post‑quantum cryptography**:
- Standardization underway; new algorithms based on lattices, codes, hashes, multivariate polynomials, etc.
- Classical cryptanalysis of these new algorithms will be a major research area.

**Transition**:
- Existing algorithms will remain in use for a long time (coexistence with post‑quantum algorithms).
- Mathematical breakthroughs could still yield faster classical attacks.

## Key recent records (factoring)

| Record | Bits | Digits | Year | Cost (core‑years) |
|--------|------|--------|------|-------------------|
| RSA‑240 | 795 | 240 | 2019 | ~? |
| **RSA‑250** | **829** | **250** | **Feb 2020** | **2,700** |
| RSA‑1024 (estimate) | 1024 | 309 | (feasible) | ~500,000 |

## Comparison of problem difficulties (as of 2022)

| Problem | Best algorithm | Asymptotic complexity | 2022 record size | Notes |
|---------|----------------|----------------------|------------------|-------|
| Factoring (RSA) | GNFS | L[1/3, 1.923] | 829 bits (RSA‑250) | 2,700 core‑years |
| DLP (prime field) | NFS‑DL | same as GNFS | 795 bits | ~3× harder than factoring |
| DLP (binary field) | quasi‑polynomial | n^{O(log n)} | >any | no longer secure |
| ECDLP | Pollard rho | O(√n) | 114 bits | exponential |

## Limitations (explicit from source / as of 2022)

- **Quantum computing** not discussed as a present threat; future uncertainty.
- **Small characteristic DLP** has quasi‑polynomial algorithm, but **does not** affect RSA or standard elliptic curves.
- **Polynomial selection** remains an art; “ideal” polynomials (Kleinjung) would halve sieving cost but no efficient construction known.
- **1024‑bit factoring** estimated but not publicly performed; academic teams lack resources.
- **Pairing‑friendly curve** security assessments are fragile due to ongoing NFS improvements.

## Practical takeaways

- **1024‑bit RSA** is now considered feasible for state‑level attackers (500k core‑years, 4B‑row matrix).
- **2048‑bit RSA** remains secure for now but migration to post‑quantum algorithms is recommended.
- **Diffie‑Hellman** with 1024‑bit primes is vulnerable to precomputation attacks (Logjam, Adrian et al. 2015).
- **Elliptic curve cryptography** (256‑bit curves) offers 128‑bit security with much shorter keys; no major cryptanalytic progress.
- **Post‑quantum standardization** is underway; classical cryptanalysis of new algorithms is a new frontier.

## References (selected, from the paper)
- Adrian et al. (2015) — Imperfect forward secrecy (Logjam)
- Barbulescu et al. (2014) — Quasi‑polynomial DLP in small characteristic
- Boudot et al. (2020) — 240‑digit factoring/DLP comparison
- De Micheli, Gaudry, Pierrot (2021) — 521‑bit TNFS record
- Kleinjung (2017) — Polynomial selection for NFS
- Kleinjung, Wesolowski (2021) — Quasi‑polynomial DLP in fixed characteristic (proved)
- Lenstra & Lenstra (1993) — Development of NFS
- National Academies (2019) — Quantum computing progress and prospects
- Stevens et al. (2009, 2017) — MD5 collisions, SHA‑1 collision
