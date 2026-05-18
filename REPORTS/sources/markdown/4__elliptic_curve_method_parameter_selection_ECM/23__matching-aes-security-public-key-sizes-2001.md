---
title: "Unbelievable Security: Matching AES security using public key systems"
title_en: "Unbelievable Security: Matching AES security using public key systems"
source_type: "article"
authors: ["Lenstra A. K."]
year: "2001"
source_link: "https://doi.org/10.1007/3-540-45682-1_5"
doi: "10.1007/3-540-45682-1_5"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "matching-aes-security-public-key-sizes-2001.md"
---

# Content source: Unbelievable Security: Matching AES security using public key systems

## Source type
Conference paper (Asiacrypt 2001? Published in LNCS).

## Author affiliation
Citibank, N.A. and Technische Universiteit Eindhoven.

## Objective
Determine public key sizes (RSA, RSA-MP, finite field DH, LUC, XTR, ECC) that provide security equivalent to symmetric cryptosystems: DES (56-bit), 2K3DES (95-bit), 3K3DES (112-bit), AES-128, AES-192, AES-256. Considers both **computational equivalence** and **cost equivalence** with projections to years 2010, 2020, 2030.

## Core methodology

### Symmetric security assumptions
- DES: 56-bit security
- 2K3DES: 95-bit security (cost-equivalent estimate, memory prices decreased)
- 3K3DES: 112-bit security (computational; realistic attack gives ~116 bits)
- AES-ℓ: ℓ-bit security (ℓ = 128, 192, 256)

### Public key security models
Two distinct equivalence measures (from Lenstra & Verheul 2000):

| Model | Definition | Gap for non-ECC systems |
|-------|------------|--------------------------|
| **Computational equivalence** | Same average computational effort to break | RSA: larger sizes |
| **Cost equivalence** | Same hardware cost to break in same time | RSA: smaller sizes (accounts for special-purpose hardware) |

For ECC, computational and cost equivalence coincide (parallelized Pollard rho storage requirements do not depend on subgroup order).

### RSA security function

Asymptotic growth rate for NFS factoring:
\[
L[n] = e^{1.923 (\log n)^{1/3} (\log \log n)^{2/3}}
\]
where \(n\) is the RSA modulus.

### RSA-MP (multiprime) security

For modulus with \(m\) equal-sized factors, smallest factor \(p\) must resist ECM:
\[
E[n,p] = (\log_2 n)^2 e^{\sqrt{2 \log p \log \log p}}
\]

Condition: \(E[n,p] \geq 80 \cdot 2^{d-56} \cdot E[2^{768}, 2^{167}]\).

### Finite field security

**Prime fields (\(k=1\))**: field size \(p\) from Table 1 (same as RSA).

**LUC (degree 2, trace representation)**: \([\log_2 p]\) from Table 4.

**XTR (degree 6, trace over \(\mathbb{F}_{p^2}\))**: \([\log_2 p]\) from Table 5.

**Small characteristic fields (e.g., \(\mathbb{F}_{2^k}\))**:
\[
L'[p^k] = e^{1.526 (\log p^k)^{1/3} (\log \log p^k)^{2/3}}
\]
(smaller constant 1.526 vs 1.923 for NFS). Calibrated against \(\mathbb{F}_{2^{607}}\) (25× easier than DES).

### Future projections
Moore-type law: progress factor \(2^{2(y-2001)/3}\) for year \(y\). For cost equivalence, divide by \(26 \cdot P\) where \(P=100\) (processor vs memory cost ratio).

## Key results — RSA modulus sizes (bits)

| Year | DES | 2K3DES | 3K3DES | AES-128 | AES-192 | AES-256 |
|------|-----|--------|--------|---------|---------|---------|
| 2001 | 416 / 620 | 1333 / 1723 | 1941 / 2426 | 2048 | 3072 | 4096 |
| 2010 | 518 / 747 | 1532 / 1955 | 2189 / 2709 | 2780 | 4170 | 5560 |
| 2020 | 647 / 906 | 1773 / 2233 | 2487 / 3046 | 3420 | 5130 | 6840 |
| 2030 | 793 / 1084 | 2035 / 2534 | 2807 / 3408 | 4200 | 6300 | 8400 |

*Lower = cost equivalent, higher = computationally equivalent.*

Example: AES-192 until 2020 → RSA modulus **7000–9000 bits**. Using 3000–4000 bits would undermine desired security (weaker than AES-128).

## RSA-MP: number of factors and factor sizes

Example for AES-128 (2010, cost equiv → 2780-bit modulus):
- 3 factors of ~927 bits each
- 4 factors of ~695 bits each (computationally equivalent)

| Year | DES | 2K3DES | 3K3DES | AES-128 | AES-192 | AES-256 |
|------|-----|--------|--------|---------|---------|---------|
| 2001 | 2:217 / 2:310 | 2:667 / 3:575 | 2:971 / 3:809 | 3:882 / 3:1075 | 4:1725 / 4:1980 | 4:3460 / 5:3078 |
| 2010 | 2:259 / 3:249 | 3:511 / 4:489 | 3:730 / 4:678 | 3:981 / 4:890 | 4:1857 / 5:1699 | 5:2929 / 5:3250 |

## Finite field sizes

### Prime fields (bits) — from Table 1 (same as RSA)

### LUC (degree 2 trace, \(\log_2 p\) bits)

| Year | AES-128 | AES-192 | AES-256 |
|------|---------|---------|---------|
| 2001 | 1322 / 1612 | 3449 / 3959 | 6920 / 7694 |
| 2010 | 1471 / 1780 | 3713 / 4247 | 7323 / 8123 |

### XTR (degree 6 trace over \(\mathbb{F}_{p^2}\), \(\log_2 p\) bits)

| Year | AES-128 | AES-192 | AES-256 |
|------|---------|---------|---------|
| 2001 | 441 / 538 | 1150 / 1320 | 2307 / 2565 |
| 2010 | 491 / 594 | 1238 / 1416 | 2441 / 2708 |

Note: XTR \(p\) is much smaller because representation uses \(\mathbb{F}_{p^2}\) with \(p^2\) field size, and trace reduces public key size.

### Small characteristic fields (\(\log_2 p^k\) bits, e.g., \(\mathbb{F}_{2^k}\))

| Year | AES-128 | AES-192 | AES-256 |
|------|---------|---------|---------|
| 2001 | 3781 / 4695 | 10637 / 12318 | 22210 / 24823 |
| 2010 | 3249 / 4225 | 11508 / 13269 | 23570 / 26277 |

Very large sizes → questionable practicality despite computational advantages.

## Public key sizes (bits, year 2010, AES-128, regular PKI)

| System | Public key size |
|--------|-----------------|
| RSA (cost eq) | 2800 |
| RSA (comp eq) | 4200 |
| RSA-MP (cost, 3 factors) | ~2800 |
| Prime field DH | 3100–3900 |
| LUC | 1700–2100 |
| XTR | 960–1200 |
| ECC | 860–1000 |

ID-based and shared environments reduce overhead significantly (see Table 7–8).

## Relative performance (year 2010, AES-128, regular arithmetic, unit = 1 mul mod 1024-bit)

### Encryption (cost equivalent)

| System | Time |
|--------|------|
| RSA (e=2^16+1) | ~3× faster than ECC? |
| XTR | ~5× slower than ECC |
| Prime field DH | ~10× slower than ECC |

### Decryption (cost equivalent)

- RSA (sequential) extremely slow (~7900 units)
- RSA-MP (parallel, 3 processors) ~1200 units
- XTR ~410 units
- ECC ~150 units

### Signature generation

- ECC fastest (~130 units)
- XTR ~460 units
- RSA-MP (parallel) ~1200 units

## Performance with Karatsuba multiplication (L^log2 3 scaling)

Relative rankings change:
- RSA encryption becomes faster than ECC (~960 vs ~1500 units for AES-128)
- RSA decryption remains very slow even with Karatsuba

## Practical conclusions (author's summary)

1. **AES-192/256 with RSA** requires moduli of ~7000–9000 bits → questionable practicality.
2. **RSA-MP** fares better but still requires significant parallelism.
3. **Prime field subgroups** outperformed by LUC and XTR; not competitive.
4. **XTR** is best non-ECC choice: easy parameter selection, can reuse RSA hardware, public keys ~1200 bits for AES-128.
5. **ECC** suffers smallest performance degradation at high security levels; choice is "obvious" if parameter generation is not a concern.
6. For current higher security levels (≈2048-bit RSA equivalent), RSA/RSA-MP with hardware accelerators remain practical. For very high levels (AES-192/256), only ECC and possibly XTR remain viable.

## Limitations (explicit from paper)

- Assumes Moore-type factoring progress until 2030 — may not hold.
- Estimates for 2K3DES/3K3DES security are approximate, especially cost equivalence.
- No guarantee that AES will not be broken; assumes no dramatic cryptanalytic progress.
- Small characteristic field discrete logarithms have oscillating constant (1.526–1.588); uses conservative lower bound.
- Remark 5.4 (replacing fields with extension fields) not reflected in public key size tables → could reduce sizes further for LUC/XTR.
- "Unbelievable security" — even perfect implementations may not achieve theoretical bounds.

## Relation to other sources

- Builds on Lenstra & Verheul (2000) cryptographic key size selection framework.
- RSA security based on NFS; ECM analysis for RSA-MP from Silverman & Wagstaff (1993) and personal communication with Zimmermann (1999) and Silverman (2000).
- XTR from Lenstra & Verheul (2000).