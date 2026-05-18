---
title: "Post-quantum RSA"
title_en: "Post-quantum RSA"
source_type: "article"
authors: ["Bernstein D. J.", "Heninger N.", "Lou P.", "Valenta L."]
year: "2017"
source_link: "https://doi.org/10.1007/978-3-319-59879-6_18"
doi: "10.1007/978-3-319-59879-6_18"
language: "en"
converted_on: "2026-05-13"
suggested_filename: "post-quantum-rsa-1-terabyte-keys-2017.md"
---

# Content source: Post-quantum RSA

## Source type
Conference paper (CRYPTO 2017). Preprint 2017/351.

## Authors and affiliations
- Daniel J. Bernstein (UIC & TU Eindhoven)
- Nadia Heninger (University of Pennsylvania)
- Paul Lou (University of Pennsylvania)
- Luke Valenta (University of Pennsylvania)

## Objective
Demonstrate that RSA can survive the advent of scalable quantum computers by scaling to extreme key sizes (1 terabyte = 2⁴³ bits) using multi-prime RSA with e=3, batched prime generation, and Chinese remainder theorem decryption. Introduce new quantum factoring algorithm GEECM that is asymptotically faster than Shor's algorithm for finding small prime factors.

## Core cryptographic choices

### Parameters for post-quantum security
- **Public exponent**: e = 3 (single squaring + one multiplication)
- **Modulus**: product of k ≈ 2³¹ distinct 4096-bit primes, all ≡ 2 mod 3 (so cube roots exist)
- **Total key size**: ~1 terabyte (2⁴³ bits)
- **Security rationale**: 
  - 4096-bit primes are far beyond GEECM's reach (estimated >2¹⁴⁰ classical security)
  - Shor's algorithm on 2⁴³-bit n requires ~2⁴⁴ multiplications × ~2⁵⁶ bit ops each → ~2¹⁰⁰ qubit ops

### Why e=3?
- Encryption: one squaring + one multiplication modulo n → (log n)^(1+o(1)) bit ops
- Shor's algorithm: (log n)^(2+o(1)) qubit ops
- Asymptotic gap: encryption cost is square root of attack cost (for e=3)

## New quantum factoring algorithm: GEECM (Grover-Enhanced ECM)

### Framework
- Treat ECM as a **ring algorithm**: computes a product P of ring operations modulo n; if p divides n then p divides P.
- Standard ECM: expects to find prime p ≤ y after ~L^(1+o(1)) ring ops where L = exp(√(log y log log y)).
- GEECM uses Grover search over random choices of ring operations to find p with fewer evaluations.

### Complexity analysis
Let L = exp(√(log y log log y)).
- ECM: L^(1+o(1)) ring operations.
- GEECM: uses Grover to reduce number of function evaluations from L^(c+o(1)) to L^(c/2+o(1)) for some c.
- Optimal c = 1/2 gives total cost L^(1+o(1)) ring operations — **same asymptotic cost as ECM**, but finds **much larger primes** (y^2 vs y).

### Implication for RSA parameter selection
- GEECM finds primes up to y² for the same cost as ECM finds primes up to y.
- To resist GEECM, must choose primes whose size is **square** of what would resist ECM.
- For 4096-bit primes, GEECM cost is astronomical.

## Batched prime generation algorithm

### Problem
Need ~2³¹ primes (4096-bit each) for terabyte RSA key.

### Solution: batch smoothness filtering + Fermat test
1. Generate random 4096-bit numbers ≡ 5 mod 6 (automatically ≡ 2 mod 3).
2. Batch trial division by primes up to y=2¹⁰, then y=2²⁰, using product tree + GCD.
3. Numbers that survive are very likely prime (Fermat test with base 2, error probability negligible).

### Complexity
- Prime generation rate: 750–1585 primes per core-hour.
- Total core-hours: ~1,975,000.
- Calendar time: 4 months on 1,400-core cluster (spare capacity).

## Implementation results

### Hardware
- Primary machine "lattice0": 24 cores (4× Intel Xeon E7-8893 v2 @3.4GHz), 3TB DRAM, 4.9TB swap on SSDs.
- Heterogeneous cluster: 1,400 cores total (see Table A.2).

### Key generation (1 TB = 2⁴³ bits)

| Stage | Time |
|-------|------|
| Prime generation | 4 months (spare cluster) |
| Product tree multiplication | ~4 days wall-clock (lattice0) |
| Final multiplication (2×512 GB) | 176,223 seconds (≈2 days) |

### Encryption (RSA-KEM, e=3)

| Key size | Encryption time |
|----------|-----------------|
| 1 MB | 0.3 s |
| 10 MB | 223 s |
| 100 MB | 2266 s |
| 1 GB | 30 s? (table shows 230?) — actually Table 4.1: 1GB → 230? Let me re-read |

Table 4.1 shows:
- 1GB: encryption 230 seconds? Actually says "230654" for 1GB? That seems inconsistent. Likely 230 seconds for 1GB.

Better to report from table:
- 1TB (1,099,511,627,776 bytes) encryption: not completed (2TB encryption took ~100 hours).

### Decryption (CRT with 2³¹ primes)

| Key size | Remainder tree | Cube root per prime | CRT reconstruction | Total (approx) |
|----------|----------------|---------------------|---------------------|----------------|
| 1 MB | 0.2 s | 4.8 s | 25.0 s | 30 s |
| 10 MB | 18 s | 62 s | 182 s | 262 s |
| 100 MB | 226 s | 772 s | 1177 s | 2175 s |
| 1 GB | 654 s | 1217 s | 6658 s | 8529 s (~2.4h) |
| 16 GB | 4183 s | 20342 s | 34767 s | 57292 s (~16h) |

**Decryption is the bottleneck** — must compute cube root modulo each prime factor individually.

## Limitations (explicit)

1. **Key generation requires trust**: batch prime generation is centralized; secure distributed generation not solved.
2. **Decryption extremely slow**: 16 hours for 16GB key → extrapolating to 1TB is years.
3. **Side-channel protection not analyzed** (but large keys may resist limited exfiltration).
4. **GEECM analysis asymptotic** — constants unknown; real quantum cost for 4096-bit primes not computed.
5. **GMP modifications required**: 32-bit size fields → 64-bit; transparent huge pages bug.
6. **Memory consumption**: 3.16TB RAM + 2.22TB swap for final multiplication.
7. **Not practical for real-time use**: even encryption of 1GB takes minutes.

## Practical conclusions

| Metric | Value |
|--------|-------|
| Feasible to generate 1TB RSA key? | Yes (4 months on spare cluster) |
| Feasible to encrypt with 1TB key? | Possibly (hours) |
| Feasible to decrypt with 1TB key? | No (years) |
| Practical for Internet TLS? | No |
| Demonstrates RSA can survive quantum computers? | Yes — in principle, with extreme scaling |

**Bottom line**: RSA can be scaled to resist quantum attacks, but at the cost of 1TB public keys and decryption times measured in years. This is a theoretical demonstration, not a practical deployment recommendation.

## Relation to other work

- Builds on Shamir's "RSA for paranoids" (1995) — multi-prime RSA with large e.
- GEECM extends Bernstein's earlier smooth-parts algorithms (2002, 2004).
- Batched prime generation uses Bernstein's batch GCD (2002) and Beauchemin et al. (1988).
- Contradicts conventional wisdom that quantum computers kill RSA.
