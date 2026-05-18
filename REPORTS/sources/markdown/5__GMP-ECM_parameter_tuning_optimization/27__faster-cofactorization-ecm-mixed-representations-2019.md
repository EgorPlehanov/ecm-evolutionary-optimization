---
title: "Faster Cofactorization with ECM Using Mixed Representations"
title_en: "Faster Cofactorization with ECM Using Mixed Representations"
source_type: "preprint"
authors: ["Bouvier C.", "Imbert L."]
year: "2019"
source_link: "https://hal.science/hal-01951942v1"
doi: "none"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "faster-cofactorization-ecm-mixed-representations-2019.md"
---

# Content source: Faster cofactorization with ECM using mixed representations

## Source type
Preprint (HAL open archive), submitted for peer review. LIRMM, CNRS, Univ. Montpellier, France.

## Objective
Improve the efficiency of the Elliptic Curve Method (ECM) specifically for medium‑size integers (≈100 bits) that arise in the cofactorization step of the Number Field Sieve (NFS), where only a few fixed smoothness bounds B₁ are used (e.g., 105, 601, 3517).

## Core methodology

### 1. Mixed curve representations
- Use **twisted Edwards curves** with a = −1 (fast addition, doubling, tripling).
- Use **Montgomery curves** in XZ coordinates (fast differential addition, doubling).
- Switch between them using a new operation **ADDₘ**:
  - Input: two points on twisted Edwards curve (extended coordinates).
  - Output: their sum on the equivalent Montgomery curve (XZ coordinates).
  - Cost: **4M** (cheaper than staying on Edwards).

### 2. Scalar multiplication for stage 1
Scalar k = lcm(2,3,…,B₁) = product of prime powers.

Three types of building blocks generated offline:

| Block type | Curve model | Key feature | Storage cost |
|------------|-------------|-------------|---------------|
| Double‑base expansions (≤4 terms) | Twisted Edwards | Uses doublings + triplings + additions | ≤4 extra points |
| Double‑base chains (divisibility condition) | Twisted Edwards | Horner‑style, no extra storage | 0 extra points |
| Lucas chains (PRAC rules) | Montgomery (XZ) | For powers of 2 and small primes | 3 extra XZ points |

### 3. Block generation (offline for fixed B₁)
- Generated >10¹⁹ candidates (expansions, chains, Lucas chains).
- Filtered for B₁‑powersmoothness (B₁ = 2¹³ = 8192 used in experiments).
- Kept only blocks with minimal cost per bit (acpb).
- Total precomputation: ~9000 CPU hours.

### 4. Combination algorithm (quasi‑exhaustive)
- Input: set of blocks B, multiset M_B₁ of prime factors to cover.
- Sort blocks by acpb.
- Enumerate subsets with bounded size using branch‑and‑bound.
- Upper bound C from Bos–Kleinjung or Ishii et al. algorithms.
- Pruning: acpb_max formula (Equation 14) limits next block cost.

## Key results

### Cost comparison for stage 1 (modular multiplications, 1S = 1M)

| Implementation | B₁=256 | B₁=512 | B₁=1024 | B₁=8192 |
|----------------|--------|--------|---------|---------|
| CADO‑NFS (Montgomery) | 3091 | 6410 | 12916 | 104428 |
| EECM‑MPFQ (Edwards) | 3074 | 6135 | 12036 | 93040 |
| ECM at Work (no storage) | 2844 | 5806 | 11508 | 91074 |
| ECM on Kalray (Ishii et al.) | 2843 | 5786 | 11468 | 90730 |
| ECM at Work (low storage) | 2831 | 5740 | 11375 | 89991 |
| **This work** | **2748** | **5667** | **11257** | **89572** |

Savings: 3–11% vs. previous best.

### Stage 2 cost comparison

| Implementation | B₁=256 | B₁=512 | B₁=1024 | B₁=8192 |
|----------------|--------|--------|---------|---------|
| CADO‑NFS | 23876 | 120132 | 641376 | 134761 |
| ECM on Kalray | 25385 | 81211 | 410911 | 22122 |
| **This work** | **22275** | **160127** | **102738** | **9866** |

(Note: values for large B₁ in this work are lower due to better ω parameter tuning.)

### Practical speedup in CADO‑NFS
- For RSA‑200 and RSA‑220 sieving phase: cofactorization time decreased by **5–10%**.
- Memory: similar to low‑storage setting of Bos–Kleinjung (≤4 extra points), much lower than EECM‑MPFQ.

### Best combination for B₁ = 256 (example block)
- 14 blocks (mix of double‑base chains and Lucas chains on Montgomery).
- Total cost: **2748 M**.
- Includes one ADDₘ switch (saves 4M vs. staying on Edwards).

## Limitations (explicit from source)
- Only optimized for **medium‑size integers** (≈100 bits) and **small, fixed B₁** values (≤8192).
- Large offline precomputation (9000 CPU hours) required for each B₁.
- Double‑base expansions limited to ≤4 terms to control storage; may miss longer low‑cost expansions.
- Does **not** address complete factorization of N, only finding one factor in cofactorization.
- The combination algorithm is quasi‑exhaustive but still heuristic (not proven optimal).
- Assumes 1S = 1M; actual ratio may differ by hardware.

## Practical conclusions
1. For NFS cofactorization with fixed B₁, precompute optimal blocks using mixed Edwards+Montgomery representations.
2. Use ADDₘ operation to switch from Edwards to Montgomery at optimal point (usually after processing most primes except powers of 2).
3. Double‑base chains with triplings (cost 12M) often beat NAF for primes >1000.
4. Adjust stage‑2 parameter ω (baby‑step giant‑step) dynamically based on B₁, B₂ for significant speedups (up to 5× for B₁=8192).
5. Implementation in CADO‑NFS reduces cofactorization time by 5–10% for RSA‑200 class numbers.
