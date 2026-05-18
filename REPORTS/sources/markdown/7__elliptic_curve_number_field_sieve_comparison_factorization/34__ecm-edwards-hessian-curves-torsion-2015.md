---
title: "A New Implementation of the Elliptic Curve Method of Integer Factorization using Edwards and Hessian Curves"
title_en: "A New Implementation of the Elliptic Curve Method of Integer Factorization using Edwards and Hessian Curves"
source_type: "thesis"
authors: ["Robinson O. M."]
year: "2015"
source_link: "http://hdl.handle.net/10197/8540"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "ecm-edwards-hessian-curves-torsion-2015.md"
---

# Content source: A New Implementation of the Elliptic Curve Method of Integer Factorization using Edwards and Hessian Curves

## Source type
Master's thesis (Research Masters in Mathematical Science), University College Dublin, School of Mathematics and Statistics, August 2015.

## Author and affiliation
- Oisin Matthew Robinson
- Supervisor: Professor Gary McGuire
- UCD School of Mathematical Science

## Objective
Develop a new implementation of the Elliptic Curve Method (ECM) using three main ideas:
1. Use of Edwards/Hessian curves for all curve arithmetic (including stage 2)
2. Use of elliptic curves with larger torsion subgroups over quartic number fields, specifically **Z/4Z ⊕ Z/8Z** for Edwards curves and **Z/6Z ⊕ Z/6Z** for Hessian curves (Jeon–Kim–Lee families)
3. Generation of hundreds (700) / thousands (4840) of such curves with small parameters and a point of infinite order with small projective coordinates, leading to improved efficiency in scalar multiplication

## Core methodology

### 1. Stage 1 implementation
- **Curve forms**: Twisted Edwards curves (aX² + Y² = 1 + dX²Y²) and twisted Hessian curves (aX³ + Y³ + Z³ = dXYZ)
- **Projective coordinates**: Used throughout to avoid inversions modulo N
- **Scalar multiplication**: Double‑and‑add algorithm with product tree for the LCM of integers up to B₁
- **Small parameters advantage**: For twisted Hessian addition, when one point has small coordinates, many multiplications effectively cost O(N) instead of O(N²); windowing not required → lower memory footprint

### 2. Stage 2 implementation (FFT continuation)
- Based on Montgomery's FFT continuation method
- Polynomial product tree for constructing G(x) = ∏ (x − ψ([j]Q))
- Bernstein's scaled remainder tree for multipoint evaluation
- Polynomial multiplication via Kronecker–Schönhage (FFT) using GMP
- **Stage 2 blocks**: To reduce memory requirements (degree of F ~ 40,000 for B₂ ~ 10¹⁴, memory ~ 2.7 GB)

### 3. Curve generation (SAGE scripts)
- **Z/4Z ⊕ Z/8Z family** (Edwards): parameter t ∈ Q, μ = (t⁴ − 6t² + 1)/(4(t² + 1)²). 700 curves generated with positive rank.
- **Z/6Z ⊕ Z/6Z family** (Hessian): parameter t ∈ Q, μ = (2t³ + 1)/(3t²). 4840 curves generated after removing isogenous/isomorphic curves.
- **Key discovery**: EECM‑MPFQ's "good curves" (torsion Z/2Z ⊕ Z/8Z) are a subset of the Z/4Z ⊕ Z/8Z family → much larger supply of curves.
- **Cantor diagonal traversal** of rationals to search dense regions first.

### 4. Isogeny problem
- Tate's isogeny theorem: isogenous curves have same #E(F_p) → redundant work.
- For Z/6Z ⊕ Z/6Z family, many Q‑isogenous curves identified by comparing group orders modulo a large prime; initial list of 8400 reduced to 4840.

### 5. Large integer arithmetic
- GNU‑MP (GMP) used for multi‑precision arithmetic (FFT multiplication for large integers, crucial for stage 2)
- No assembly language optimizations (but noted as future improvement)

## Key results

### Largest factor found
**57‑digit prime** factor of (5²²⁸ + 3·197¹¹⁰) / 227812: