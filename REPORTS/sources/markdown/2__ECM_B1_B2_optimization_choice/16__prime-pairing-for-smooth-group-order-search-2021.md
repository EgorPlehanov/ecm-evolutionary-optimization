---
title: "Prime pairing in algorithms searching for smooth group order"
title_en: "Prime pairing in algorithms searching for smooth group order"
source_type: "article"
authors: ["Atnashev P.", "Woltman G."]
year: "2021"
source_link: "https://doi.org/..."
doi: "none"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "prime-pairing-for-smooth-group-order-search-2021.md"
---

# Content source: Prime pairing in algorithms searching for smooth group order

## Source type
Preprint/article (arXiv? Not specified). Dated September 20, 2021.

## Authors
- Pavel Atnashev (patnashev@gmail.com)
- George Woltman (woltman@alum.mit.edu) — author of prime95 (GIMPS software)

## Objective
Improve the "prime pairing" process in stage 2 of factorization algorithms (P−1, P+1, ECM) where primes are represented as \(p = iD \pm r\) and both \(iD + r\) and \(iD - r\) are tested simultaneously. Introduce new methods: relocatable primes, graph matching, irregular precomputation distances, second base, and pairing sharing. Aim to increase the percentage of primes in \([B_1, B_2]\) that can be paired, reducing the number of required group operations.

## Background: Stage 2 of P−1/P+1/ECM

After stage 1 computes \(X = X(B_1)\), stage 2 tests whether any prime \(p \in (B_1, B_2]\) satisfies \(p \cdot X \equiv 0 \pmod{\text{factor}}\).

**Montgomery's method (1987)**:
- Choose \(D\) (even, with many small prime factors → small \(\phi(D)\)).
- Write each prime \(p = iD - r\) with \(0 < r < D\), \(\gcd(r,D) = 1\).
- Precompute \(r \cdot X\) for all \(r\) in reduced residue system modulo \(D\) (baby steps).
- Iterate over \(i\) such that \(iD\) runs from \(B_1\) to \(B_2\) (giant steps).
- For each prime \(p\), test if \(iD \cdot X \equiv r \cdot X\) (mod factor). Because \(abs(-bX) = abs(bX)\) (inherent in P+1 and ECM, achievable in P−1), one test checks both \(iD + r\) and \(iD - r\).

**Problem**: Each residue class can pair only with one prime in the previous D-section and one in the next → limited pairing probability. Increasing precomputed set to \(\{r, r+D, r+2D, \dots, r+(L-1)D\}\) gives \(2L\) pairing opportunities per prime but increases memory.

**Montgomery's algorithm** (greedy) finds optimal pairing for fixed residue classes.

## Key innovations

### 1. Relocatable primes (Section 2.1)

If \(p \cdot X = 0\) (mod factor), then for any constant \(c\) with \(\gcd(c, D)=1\), \(cp \cdot X = c(p \cdot X) = 0\) as well. So one can test \(cp\) instead of \(p\) as long as \(cp \le B_2\).

Let \(c_0\) be the smallest constant coprime to \(D\) such that \(B_2 / c_0 > B_1\). Primes in \((B_1, B_2/c_0]\) are **relocatable** — they can be multiplied by \(c\) and moved to higher ranges.

**Multiple relocation options**: If \(B_2/B_1\) is large (e.g., 20), multiple constants \(c_0, c_1, c_2, \dots\) can satisfy \(B_2 / c_j > B_1\). Add all \(\{c_j\}p\) to the pairing algorithm. Only one of them needs to be paired; when a pair is found, that constant becomes fixed and the prime is relocated accordingly.

**Benefit**:
- Starting point \(iD\) moves from \(B_1\) to \(B_2/c_0\) → fewer D-sections to process.
- Greatly increases pairing density.

### 2. Graph matching (Section 2.2)

With relocatable primes, primes are not locked in residue classes. Greedy algorithm insufficient.

**Graph model**:
- Vertices: all primes in \((B_2/c_0, B_2)\) (non-relocatable) + relocation positions for primes in \((B_1, B_2/c_0)\) (each relocatable prime represented by at least one vertex \(c_0p\)).
- Edges: pairing opportunities between vertices (when \(iD \pm r = p\) and \(i'D \pm r' = q\) with \(iD\) common giant step).

**Matching algorithm**:
- Each relocatable prime is a **subgraph** (multiple possible relocation positions). Only one can be matched.
- Search for augmenting paths (standard bipartite matching extended to general graphs with subgraph vertices).
- Final relocation constant chosen only when match is found.

Complexity: O(|V|·|E|) in practice, but Micali–Vazirani (1980) gives O(√|V|·|E|) for maximum matching in general graphs.

### 3. Irregular precomputation distances (Section 2.3)

Montgomery's algorithm uses sequential distances: unit, D−unit, D+unit, 2D−unit, 2D+unit, etc.

**Proposed irregular distribution**: Use powers of 2:
\[
\text{distances} = \{u + (2^i - 1)D \mid u \in \text{unit}, i = 0,\dots,L-1\} \cup \{-u - (2^i - 1)D\}
\]

This provides \(L\) pairing opportunities at exponentially increasing scales, matching the decreasing density of primes from \(B_1\) to \(B_2\).

**Flexibility**: If memory limited, can precompute only part of the last unit (non-integer \(L\)).

### 4. Second base (Section 2.4)

Let \(A > 2\) be a prime divisor of \(D\). Represent prime in two ways:
\[
p = iD \pm r \quad \text{and} \quad p = iD + \frac{D}{A} \pm r
\]

The second representation doubles pairing opportunities and breaks residue class restrictions, dramatically boosting pairing.

**Memory cost**: Precomputed set size becomes \(\frac{1}{2} \phi(D/A) \cdot A \cdot L\). Example: D=210, A=7, L=2 → size grows from 48 to 56.

**Performance trade-off**: Doubles work for incrementing giant steps (both \(iD\) and \(iD + D/A\) need to be updated). For ECM with complex arithmetic, second base is rarely beneficial for D < 1000. For P+1 (cheaper group operations), may be beneficial.

### 5. Pairing sharing (Section 2.5)

Pairing depends only on parameters \(B_1, B_2, D, A, L\) and available memory — **not on the specific number being factored**.

- Pairings can be stored in a central repository.
- Hosts can download precomputed pairings or compute and upload for others.
- Pairings can be upgraded over time with new methods.

## Algorithm outline (Section 3)

### Precomputation

**Algorithm 1** (unit for residue r):
\[
\text{unit} = \{r \mid 1 \le r \le D/2,\ \gcd(D/A, r) = 1\}
\]

**Algorithm 2** (all distances, power-of-two distribution):
\[
\text{distribution} = \{2^i - 1 \mid i = 0,\dots,L-1\}
\]
\[
\text{distances} = \{u + d\cdot D \mid u \in \text{unit},\ d \in \text{distribution}\} \cup \{\text{negatives}\}
\]

**Algorithm 3** (residue distances per residue class):
For each residue \(0 \le i < D\) with \(\gcd(D/A, i)=1\), if \(i + d \equiv 0 \pmod{D}\) or \(i + d \equiv D/A \pmod{D}\), add distance \(2d\) to residue.distance(i).

### Graph construction

- Vertices \(V\): primes in \((B_1, B_2]\) (relocatable primes split into multiple vertices for each possible \(c\)).
- Edges: adjacency based on residue distances modulo \(D\).
- source(p) = original prime for relocation vertices, nil otherwise.

### Initialization (Algorithm 6)

Greedy initial matching (equivalent to Montgomery's algorithm). For each free vertex \(p\) (or its source if relocatable), try to match with the smallest available neighbor.

### BFS augmentation

- Standard BFS for augmenting paths in bipartite graphs, extended to handle subgraph vertices (relocatable primes).
- When entering a relocatable prime from its match, add all of its individual relocation vertices to the queue.
- Augment path using back-links (Algorithm 4).

## Results (Table 1)

| B₁ | B₂ | #primes | D | A | L | #{r} | Montgomery | Prefactor | Prime95 |
|----|----|---------|---|---|---|------|------------|-----------|---------|
| 9,500 | 1,000,000 | 77,269 | 210 | 1 | 8 | 192 | 32,121 (83.1%) | 38,370 (99.3%) | 38,206 (98.9%) |
| 10,000 | 1,000,000 | 77,269 | 714 | 3 | 5 | 720 | — | 38,577 (99.9%) | — |
| 700,000 | 23,100,000 | 1,397,601 | 84 | 1 | 10 | 120 | 535,912 (76.7%) | 677,422 (96.9%) | 664,321 (95.1%) |
| 700,000 | 23,100,000 | 1,397,601 | 210 | 1 | 15 | 120 | 465,585 (66.6%) | 537,185 (76.9%) | 536,248 (76.7%) |
| 700,000 | 23,100,000 | 1,397,601 | 210 | 7 | 5 | 140 | — | 657,563 (94.1%) | — |
| 700,000 | 23,100,000 | 1,397,601 | 210 | 11 | 10 | 240 | 566,578 (81.1%) | 680,178 (97.3%) | 671,159 (96.0%) |
| 700,000 | 23,100,000 | 1,397,601 | 510 | 3 | 6 | 576 | — | 689,404 (98.7%) | — |

**Observations**:
- Montgomery's greedy algorithm: 66–83% pairing.
- Prefactor (full graph matching + relocatable primes + irregular distances): up to **99.9%** pairing.
- Prime95 (windowed matching, one base only): 95–98% pairing.

## Implementations

- **Prefactor** (https://github.com/patnaheev/prefactor): full implementation of all methods.
- **Prime95** (https://www.mersenne.org/download/): uses "windowed mode" (augmenting paths only in small subsets to save time). Uses only one base (no second base). Targets Mersenne numbers with high B₁,B₂ where extra 1–2% pairing not worth setup time.

## Limitations (explicit)

1. **Graph matching complexity**: Micali–Vazirani algorithm (1980) is complex; practical implementations use "good enough" matching (sacrifice a few percent for speed).
2. **Second base rarely beneficial for ECM** with D < 1000 due to doubled increment cost.
3. **Optimal distance distribution unknown**; powers of two are heuristic, not proven optimal.
4. **Parameter dependence**: Optimal D, A, L depend on B₁,B₂ and memory constraints; no universal formula given.
5. **Pairing repository not yet implemented** (proposed for future).
6. **Analysis assumes large numbers** (millions of decimal digits); may not apply to smaller inputs.

## Relation to prior work

- Builds on Montgomery (1987) — standard continuation with baby-step giant-step.
- FFT continuation (Montgomery & Silverman 1990) is an alternative when memory available.
- GMP-ECM (Zimmermann & Dodson 2006) implements FFT continuation.
