---
title: "Revisiting ECM on GPUs"
title_en: "Revisiting ECM on GPUs"
source_type: "conference"
authors: ["Wloka J.", "Richter-Brockmann J.", "Stahlke C.", "Priplata C.", "Kleinjung T.", "Güneysu T."]
year: "2020"
source_link: "unknown (provided PDF: 2020-1265.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "ecm-on-gpus-high-throughput-implementation-2020.md"
---

# Content source: Revisiting ECM on GPUs

## Source type
Conference paper (appears to be from IACR/CHES or similar, 2020).

## Authors affiliation
1. DFKI GmbH, Cyber-Physical Systems, Bremen, Germany
2. Ruhr University Bochum, Horst Görtz Institute, Germany
3. CONET Solutions GmbH, Hennef, Germany
4. EPFL IC LACAL, Lausanne, Switzerland

## Objective
Present a highly optimized, scalable GPU implementation of the entire Elliptic Curve Method (ECM) for integer factorization, supporting arbitrary parameter sizes and multiple GPUs, with applications to cofactorization in GNFS and discrete logarithm problem solving.

## Core methodology
- **Curve arithmetic**: Twisted Edwards curves with a = −1 using extended projective coordinates (fastest known ops).
- **Scalar multiplication (stage 1)**: w-NAF representation (w=4) — outperforms addition chains/batching for larger B₁ due to uninterrupted program flow.
- **Stage 2 optimization**: Baby-step giant-step approach with normalization of y-coordinates to reduce multiplications; batch processing for large B₂ when memory insufficient.
- **Integer arithmetic**: Montgomery multiplication with FIOS/FIPS/CIOS strategies; FIPS performs best on Volta/Turing architectures.
- **Multi-precision**: 32-bit limbs, strided memory layout for coalesced access, PTX assembly for carry flags.
- **Multiple GPU support**: Designed for multi-device computation (first implementation to support this).

## Key results

### Throughput (ECM trials/second)

**Stage 1 only (B₁ = 8192):**

| Modulus (bits) | Tesla P100 | Tesla V100 | RTX 2080 Ti | 2×RTX 2080 Ti |
|----------------|------------|------------|-------------|---------------|
| 192 | 46,800 | 149,100 | 214,100 | 377,100 |
| 320 | 9,900 | 61,900 | 77,100 | 150,200 |
| 448 | 5,200 | 24,700 | 24,700 | 48,200 |

**Stage 1+2 (B₁ = 50,000, B₂ = 500,000):**

| Modulus (bits) | Tesla P100 | Tesla V100 | RTX 2080 Ti | 2×RTX 2080 Ti |
|----------------|------------|------------|-------------|---------------|
| 192 | 4,970 | 22,850 | 20,210 | 39,420 |
| 320 | 1,420 | 7,990 | 9,340 | 17,910 |
| 448 | 550 | 2,780 | 2,780 | 5,390 |

### Montgomery multiplication performance (million multiplications/sec)

| Architecture | 192-bit | 320-bit | 448-bit |
|--------------|---------|---------|---------|
| RTX 2080 Ti (FIPS) | 32,800 | 7,575 | 5,125 |
| Tesla V100 (FIPS) | 29,340 | 5,018 | 3,914 |
| Tesla P100 (CIOS) | 5,536 | 1,945 | 937 |

### Comparison with prior work (trials/core/cycle ×10⁻⁵, 192-bit)

| B₁ | Bos et al. (GTX 580) | This work (RTX 2080 Ti) |
|----|----------------------|--------------------------|
| 960 | 2.169 | 0.493 |
| 8192 | 0.251 | 0.294 |
| 50000 | N/A | 0.052 |

### Practical DLP application
- For 768-bit DLP individual logarithm: reduced latency from 3 minutes to 2 minutes on 25 CPUs + 2 GPUs.
- For 1024-bit individual logarithms: upper bound ~1 hour on 100 CPU cores (without final database).
- ECM parameters for n-bit factor (n=44–80): B₁ ≈ 7·exp(n/9), B₂ ≈ 600·exp(0.113·n).

## Implementation highlights
1. **PTX-level abstraction** — GPU-generation independent.
2. **Open source** — https://github.com/Chair-for-Security-Engineering/ecmongpu
3. **Scalable** — Supports arbitrary B₁, B₂, and modulus sizes (not fixed small parameters).
4. **Multiple devices** — Near-linear throughput scaling with 2 GPUs.

## Limitations (explicit or implied)
- Stage 2 memory-bound: for B₂ > 1e6, batch processing required (Tesla V100's 16GB vs RTX 2080 Ti's 11GB matters).
- w-NAF approach chosen over addition chains despite higher op count due to implementation practicality (GPU divergence, precomputed point storage costs).
- Comparison with prior work difficult due to different hardware generations.
- Yield (actual factor discovery rate) not evaluated — only throughput benchmarks.

## Conclusions from source
- w-NAF with w=4 is most promising for stage 1 on GPUs despite more operations.
- FIPS Montgomery multiplication outperforms CIOS/FIOS on recent NVIDIA architectures (Volta, Turing).
- Scalability to arbitrary parameters and multiple GPUs achieved.
- Implementation freely available to support future factorization/DLP records.

## Practical value
- Can accelerate GNFS cofactorization step.
- Reduces latency of individual discrete logarithm computation in DLP records.
- Allows reassessment of security of RSA and Diffie-Hellman parameters.
