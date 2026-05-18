---
title: "GMP-ECM: yet another implementation of the Elliptic Curve Method (or how to find a 40-digit prime factor within 2·10^11 modular multiplications)"
title_en: "GMP-ECM: yet another implementation of the Elliptic Curve Method (or how to find a 40-digit prime factor within 2·10^11 modular multiplications)"
source_type: "conference_talk"
authors: ["Zimmermann P."]
year: "2000"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "gmpecm-implementation-talk-2000.md"
---

# Content source: GMP-ECM: yet another implementation of the Elliptic Curve Method

## Source type
Conference talk / extended abstract (likely from a workshop or seminar). The document appears to be slide handouts or an abstract with figures and tables, circa 1999–2000.

## Author affiliation
Paul Zimmermann — Inria Lorraine, Nancy, France.

## Objective
Present the design and performance of GMP‑ECM, an implementation of the Elliptic Curve Method (ECM) for integer factorization, focusing on the combination of Brent‑Suyama's improvement, fast polynomial multipoint evaluation, and the improved standard continuation (Montgomery 1987). Provide estimates of success probability and comparisons with other software (Magma, Pari/GP).

## Core content summary

### 1. ECM overview (slides 1–4)

**Stage 1**:
- Uses Montgomery's form with group order divisible by 12:
  \[
  b y^2 z = x^3 + a x^2 z + x z^2
  \]
- Starting point from parameter σ (Brent, Crandall, Woltman).
- Homogeneous coordinates with Montgomery's PRAC algorithm.
- Cost: \(K_1 \cdot B_1 / \log 2\) modular multiplications, with \(K_1 \approx 9.0\)–9.1 in practice.

**Stage 2**:
- Improved standard continuation (Montgomery 1987): checks all primes up to B₂.
- Baby‑step giant‑step with parameter d₁.
- Affine coordinates (after stage 1) using an idea by Gerhard Niklasch.
- Brent‑Suyama's improvement: use \( (s^e - t^e)Q \) instead of \( (s - t)Q \) → more divisors.
- Fast polynomial multipoint evaluation (product tree + remainder tree).

### 2. Brent‑Suyama improvement (slide 5)

- Instead of checking primes ℓ = i d₁ ± j, check divisors of \( (i d₁)^e \pm j^e \).
- Conjectured success probability multiplier: d(2e) = number of divisors of 2e.
- Table:

| e | 1 | 2 | 3 | 6 | 12 | 18 | 24 | 30 | 60 | 90 | 120 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| d(2e) | 2 | 3 | 4 | 6 | 9 | 10 | 12 | 16 | 18 | 20 | 20 |

- Used only in birthday‑paradox continuation so far (but GMP‑ECM uses it in standard continuation).

### 3. GMP‑ECM stage 2 algorithm (slides 6–8)

**Parameters**: choose m, K, D such that m·K·D > B₂, K = 2ᵏ, D = 6d, φ(D) < 2K.

**Steps**:

1. Compute S = { iᵉ·Q : 0 < i < D, i ≡ 1 mod 6, gcd(i,D)=1 } (baby steps).
2. Compute polynomial F(x) = ∏_{a∈S} (x − a) using product tree.
3. Compute R(x) = Quo(x^{2K−2}, F(x)) using Montgomery's reciprocal algorithm.
4. [m times] Compute Tₗ = { [ (lK+j)D ]ᵉ Q : 0 ≤ j < K } (giant steps).
5. [m times] Compute Gₗ(x) = ∏_{b∈Tₗ} (x − b).
6. [m−1 times] Compute Gₗ(x) = Gₗ₋₁(x)·Gₗ(x) mod F(x) using R(x).

**Cost analysis (Karatsuba multiplication M(n))**:
- Steps B and E (product trees): O(M(K)).
- Step C (reciprocal): 3/2 M(K).
- Step F (modular reduction of product of polynomials): 3M(K) per multiplication.
- Total: ≈ (4m − 1/2) M(K) modular multiplications.

### 4. Performance for 40‑digit factor (slide 9)

| B₁ | B₂ | e | hits | mul/curve | curves | total mul | speedup vs (e=1) |
|----|----|----|------|-----------|--------|----------|------------------|
| 3e6 | 3e8 | 1 | 870+ | 5.29e7 | 5366 | 2.84e11 | 1.00 |
| 3e6 | 8.0e8 | 12 | 1089+ | 5.44e7 | 3526 | 1.92e11 | 1.48 |
| 3e6 | 8.0e8 | 18 | 1089+ | 5.54e7 | 3486 | 1.93e11 | 1.47 |
| 3e6 | 8.0e8 | 30 | 1089+ | 5.74e7 | 3354 | 1.93e11 | 1.47 |

- Using e=12,18,30 increases number of primes found (hits) compared to e=1.
- For e=30, 3354 curves suffice vs 5366 for e=1 → speedup ≈1.48.

### 5. Modular multiplication counts (slide 10)

| B₁ | B₂ (m·K·D) | e | Stage 1 (K₁) | Stage 2 (K₂) |
|----|------------|----|--------------|--------------|
| 1e6 | 2.3e8 | 12 | 1.3e7 (9.0) | 6.3e6 (0.52) |
| 3e6 | 8.0e8 | 30 | 3.9e7 (9.0) | 1.8e7 (0.47) |
| 11e6 | 3.9e9 | 60 | 1.4e8 (9.1) | 6.9e7 (0.39) |
| 36e6 | 1.6e10 | 120 | 4.7e8 (9.1) | 2.3e8 (0.35) |

- K₁ ≈ 9.0–9.1 (modular multiplications per bit of B₁).
- Stage 2 cost grows more slowly than stage 1 as B₁ increases.

### 6. Timings on different hardware (slide 11)

For 155‑digit number, B₁=3e6, B₂=8e8, e=30 (3.9e7 stage1 M, 1.8e7 stage2 M):

| Machine | Stage1 time | Stage2 time | Total |
|---------|-------------|-------------|-------|
| 366 MHz PC/Linux | 601 s | 383 s | 984 s |
| 195 MHz SGI R10000 | 484 s | 389 s | 873 s |
| 500 MHz Alpha 21264 | 117 s | 101 s | 218 s |

- Alpha is ~4.5× faster than PC for this workload.

### 7. Comparison with other software (slide 14)

**Machine**: 500 MHz Alpha 21264, 155 digits, B₁=3,000,000.

| Variant | B₂ | Time |
|---------|-----|------|
| Magma V2.4‑6 | BP? | 614 s |
| Pari/GP 2.0.14 | SC 3.3e8 | 1411 s (extrapolated) |
| GMP‑ECM 4a | SC + Kara, 8e8, e=30 | 218 s |

**Remark**: Pari/GP extrapolated from B₁=43,000 (64 curves at a time).

**Additional comparison** (slide 15):

- 195 MHz R10000, 120 digits, B₁=8,000,000:
  - GMP‑ECM: B₂=2.6e9, e=60 → 1020 s.
  - ecmfft (Montgomery's FFT extension): B₂=2.7e10 → 1824 s.
- 450 MHz PC, 2⁷²⁷−1 (219 digits), B₁=3,000,000:
  - GMP‑ECM: B₂=8e8, e=30 → 208 s.
  - mprime: B₂=3e8 → 208 s (similar).

### 8. Factors found (slide 12)

List of factors discovered with GMP‑ECM (as of 2000):
- p49 by M. Quercia
- p48 by S. Wagstaff
- p45 by P. Leyland
- p37 by T. Granlund
- p37 (second) by T. Charron
- p36 by P. Zimmermann

### 9. Underlying arithmetic (slide 11 details)

- Uses GMP (GNU Multi‑Precision) library for modular multiplication.
- Modular multiplication (mul) and modular reduction (mod) times are reported.
- Example (155 digits, 500 MHz Alpha): mul 45 ns, mod 52 ns per operation.

## Key performance figures

| B₁ | Stage1 M | Stage2 M | Total M | Approx. time (500 MHz Alpha) |
|----|----------|----------|---------|------------------------------|
| 1e6 | 1.3e7 | 6.3e6 | 1.93e7 | ~1.1 s? (not given) |
| 3e6 | 3.9e7 | 1.8e7 | 5.7e7 | 218 s (for 155‑digit n) |
| 11e6 | 1.4e8 | 6.9e7 | 2.09e8 | ~ |
| 36e6 | 4.7e8 | 2.3e8 | 7.0e8 | ~ |

## Limitations (explicit from source / talk format)

- The document is an extended abstract or talk slides; lacks full algorithmic details, proofs, and completeness.
- Brent‑Suyama improvement's success probability is "conjectured" (no rigorous proof).
- Timings are from 1999–2000 hardware; not comparable to modern systems.
- Comparison with Magma and Pari/GP uses different B₂ values and may not be apples‑to‑apples.
- No discussion of memory usage or parallelization.

## Legacy and impact

- GMP‑ECM became the de facto standard ECM implementation.
- Used extensively in number theory research and factoring efforts (Cunningham project, RSA challenges).
- Brent‑Suyama improvement with Dickson polynomials (e>1) is a standard feature in modern ECM implementations.
- Fast polynomial arithmetic (product tree, remainder tree) for stage 2 became a standard technique.

## References (as listed in slide 16)
- Bosma, Lenstra (1995) — Implementation of ECM (Magma)
- Brent (1999) — Factorization of the tenth Fermat number
- Montgomery (1992) — Evaluating Recurrences… (Lucas chains)
- Montgomery (1992) — An FFT Extension of ECM (PhD thesis)
