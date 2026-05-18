---
title: "Experimental comparison of integer factoring algorithms for medium-sized composites"
title_en: "Experimental comparison of integer factoring algorithms for medium-sized composites"
source_type: "technical_report"
authors: ["Milan J."]
year: "2010"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-16"
suggested_filename: "experimental-comparison-factoring-algorithms-2010.md"
---

# Content source: Experimental comparison of integer factoring algorithms for medium-sized composites

## Source type
Technical report / preprint (HAL open archive). Likely from a research project (possibly part of a thesis or software package TIFA).

## Author affiliation
Jérôme Milan — Laboratoire d'Informatique de l'École Polytechnique (LIX), Palaiseau, France.

## Objective
Implement and experimentally compare several integer factoring algorithms for small to medium‑sized composites (45–200 bits) that arise in sieving methods (e.g., Number Field Sieve, discrete logarithms, class group computations). Algorithms tested: SQUFOF (with fast return), McKee's Fermat speedup, ECM, CFRAC (with batch smoothness detection), and SIQS. Provide detailed timing measurements and practical recommendations.

## Core content summary

### 1. Implemented algorithms (Section 2)

| Algorithm | Type | Complexity | Key feature |
|-----------|------|------------|-------------|
| **SQUFOF** (Shanks) | deterministic | O(N^{1/4}) | Uses quadratic forms; works with numbers ≤2 machine words (single‑precision) |
| **McKee's Fermat** | probabilistic | O(N^{1/4}) (heuristic) | Improves Fermat's difference‑of‑squares |
| **ECM** (Lenstra) | probabilistic | L_p[1/2,√2] | Standard continuation; Suyama curves; Montgomery ladder |
| **CFRAC** (Morrison–Brillhart) | subexponential | L_N[1/2,√2] | Generates residues <2√N; single large prime variation |
| **SIQS** (Contini) | subexponential | L_N[1/2,1] | Self‑initializing quadratic sieve; uses batches for relation selection |

**Batch smoothness detection** (Bernstein 2004):
- Precompute product of factor base primes z.
- Compute product X = ∏ x_i via product tree.
- Compute z mod x_i via remainder tree.
- Compute y_i = z^{2^e} mod x_i (with 2^{2^e} ≥ x_i).
- Smooth part = gcd(x_i, y_i).
- Used in CFRAC to avoid trial division per residue.

### 2. Implementation details (Section 3)

**Hardware**:
- 64‑bit AMD Opteron 250, 2GB RAM, GNU/Linux.
- GMP 4.2 with assembly optimizations for Opteron.
- gcc 4.1, -march=opteron -O3.

**Composites tested**: product of two random primes of similar size (45–200 bits). 20–1000 composites per data point.

**Linear algebra**: Gaussian elimination over GF(2) (small matrices; not dominant).

**SQUFOF**:
- Follows Gower–Wagstaff (2007) description.
- Multiplier list {1, 15 multipliers} (as in [9]).
- **Fast return** (large step) adapted from Williams–Wunderlich (1987).
- Fast return threshold n_FR = 4096 (determined experimentally).
- Limited to numbers fitting in 2 machine words (≤128 bits).

**McKee's Fermat**:
- "Greedy" variant as described in [13].
- Multipliers {1,3} and {1,3,5,7,11}.
- Limited to double‑precision integers.

**ECM**:
- Montgomery point representation, Suyama curves.
- Stage 1: Montgomery ladder.
- Stage 2: improved standard continuation with precomputed points (like [12]).
- B₁, B₂ optimized for composites with equal‑sized factors.

**CFRAC**:
- Multiplier k<100 to make kN≡1 mod 8 and maximize quadratic residues.
- Single large prime variation.
- Relation selection: trial division (with/without early abort) vs. batch smoothness detection.
- Batch size: 128 residues.
- Early abort bound: experimental c = 4/7 (vs. Pomerance's asymptotic 1/7).

**SIQS**:
- Factor base as in CFRAC.
- Polynomial selection: Carrier–Wagstaff method [1].
- Sieve interval M determined experimentally.
- **Unusual approach**: use batch smoothness detection (instead of traditional trial division) to relax sieve threshold τ, reducing sieving time.
- τ determined empirically (Table 2): e.g., 60‑bit → τ=10, 200‑bit → τ=87.

### 3. Results (Section 3.2–3.7)

**SQUFOF (Fig. 1,2)**:
- Timings from 45 to 80 bits (1000 composites per size).
- Fast return benefit negligible below 60 bits.
- Comparison with PARI and YAFU: similar performance for 45–80 bits.
- PARI and YAFU limited to single‑precision; our version works up to 128 bits.

**McKee's Fermat (Fig. 3)**:
- Consistently slower than SQUFOF (by factor ~2–5).
- Disagrees with McKee's original claim (attributed to poor SQUFOF implementation in Maple).

**ECM (Fig. 4)**:
- Timings for 2‑prime (2P) and 3‑prime (3P) composites, 45–100 bits.
- Failure rate: 0.5–2%.
- For composites with two equal‑sized factors (RSA‑like), ECM is slower than SQUFOF below ~60 bits.
- For three‑factor composites, ECM is faster because factors are smaller.

**CFRAC (Fig. 5,6, Table 1)**:
- Factor base size grows with N: e.g., 80 bits → 128 primes, 200 bits → 512 primes.
- Batch smoothness detection dramatically speeds up relation selection (Fig. 5).
- For 80 bits: tdiv+ea ≈ 40 s, batch ≈ 8 s.
- For 200 bits: tdiv+ea ≈ 2000 s, batch ≈ 450 s.
- Dominant step remains relation selection (60–80% of total time, even with batches).

**SIQS (Fig. 7–9, Table 2)**:
- Factor base sizes: 60 bits → 60 primes, 200 bits → 4600 primes.
- Sieve interval M: 60 bits → 1000, 200 bits → 65536.
- Sieve filling + polynomial initialization = 50–80% of relation collection time.
- Comparison with PARI and YAFU (Fig. 9):
  - At 100 bits: our SIQS ≈ 0.6 s, PARI ≈ 1.8 s, YAFU ≈ 0.8 s.
  - At 200 bits: our SIQS ≈ 160 s, YAFU ≈ 130 s (YAFU ~20% faster).
- SIQS scales down to 50 bits (competitors revert to QS/MPQS and are slower).

**Overall comparison (Fig. 10, 45–200 bits)**:

| Size (bits) | Fastest algorithm | Approx. time |
|-------------|-------------------|--------------|
| 45–60 | SQUFOF | <0.1 s |
| 60–80 | SQUFOF / ECM (depending on factor size) | 0.1–1 s |
| 80–120 | SIQS | 1–20 s |
| 120–200 | SIQS | 20–160 s |

- CFRAC is slower than SIQS across the whole range (factor 2–5).
- McKee's Fermat is not competitive.

### 4. Key findings and recommendations

1. **SQUFOF**: Still viable for tiny composites (≤60 bits). Fast return is negligible for small sizes.
2. **McKee's Fermat**: Poor performance; not a viable alternative to SQUFOF.
3. **ECM**: More effective than SQUFOF when composites have more than two factors (smaller factors). For RSA‑like numbers (two equal factors), ECM becomes competitive only above ~70 bits.
4. **CFRAC**: Even with batch smoothness detection, it is not competitive compared to sieving methods (SIQS) for any tested size.
5. **SIQS**: The best general‑purpose algorithm for composites from ~70 bits to at least 200 bits. Can be tuned to work well even for numbers as small as 60 bits (using relaxed sieve thresholds and batch detection).
6. **Batch smoothness detection** (Bernstein) is highly effective for CFRAC but not needed for SIQS (though it can be used to relax sieve thresholds).

### 5. Practical implementation notes

- All implementations are part of the **TIFA software package** (http://www.lix.polytechnique.fr/Labo/Jerome.Milan/tifa/tifa.html).
- Multi‑precision arithmetic via GMP (with assembly optimizations for Opteron).
- Linear algebra (Gaussian elimination) is negligible for the tested sizes.
- For SIQS, polynomial selection follows Carrier–Wagstaff [1]; leading coefficients within a few percent of ideal target.

## Key tables

**Table 1** (CFRAC factor base sizes):
- Trial division: 80 bits → 128, 160 bits → 256, 200 bits → 512.
- Batches: 80 bits → 128, 125 bits → 192, 200 bits → 512.

**Table 2** (SIQS parameters):
| Bits | Base size | Sieve interval M | τ |
|------|-----------|------------------|----|
| 60 | 60 | 10,000 | 30 |
| 80 | 140 | 14,000 | 31 |
| 100 | 200 | 30,000 | 36 |
| 120 | 400 | 30,000 | 43 |
| 140 | 700 | 49,000 | 52 |
| 160 | 1300 | 65,536 | 56 |
| 180 | 2100 | 65,536 | 62 |
| 200 | 4600 | 196,608 | 87 |

## Limitations (explicit from source / context)

- Tested only up to 200 bits; for larger numbers, NFS would be faster.
- SQUFOF limited to 2‑machine‑word numbers (≤128 bits).
- ECM failure rate non‑zero (0.5–2%); but in practice multiple curves are used.
- Timings are for single‑threaded C implementations on 2009–2010 hardware.
- SIQS parameter tuning (τ, M) is empirical; may not generalize to other hardware or number distributions.
- No comparison with modern NFS implementations (not relevant for <200 bits).

## References (selected)
- Bernstein (2004) — How to find smooth parts of integers (batch method)
- Contini (1997) — SIQS (thesis)
- Gower & Wagstaff (2007) — SQUFOF (Mathematics of Computation)
- Lenstra (1987) — ECM
- Morrison & Brillhart (1975) — CFRAC, F₇ factorization
- McKee (1999) — Speeding Fermat's factoring method
- Montgomery (1987) — ECM improvements
- Silverman (1987) — MPQS
- Williams & Wunderlich (1987) — Parallel CFRAC (large steps)