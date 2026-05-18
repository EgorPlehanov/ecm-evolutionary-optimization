---
title: "RSA Cryptanalysis: An Elitist Genetic Algorithm for Integer Factorization"
title_en: "RSA Cryptanalysis: An Elitist Genetic Algorithm for Integer Factorization"
source_type: "conference"
authors: ["Kumari A.", "Garain U.", "Bandyopadhyay S.", "Mishra G.", "Pal S. K.", "Bhattacharyya M."]
year: "2024"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "elitist-genetic-algorithm-for-integer-factorization-2024.md"
---

# Content source: RSA Cryptanalysis: An Elitist Genetic Algorithm for Integer Factorization

## Source type
Conference paper (appears to be from a proceedings; year ~2024 based on references and content).

## Authors affiliation
- Kumari, Bandyopadhyay, Bhattacharyya — Indian Statistical Institute (CAIML/MIU).
- Garain — CVPRU, Indian Statistical Institute.
- Mishra, Pal — Scientific Analysis Group, DRDO (Defence Research and Development Organisation), India.

## Objective
Improve upon existing genetic algorithm (GA) approaches for integer factorization by incorporating **elitism**, removing redundancy (duplicate individuals and parents), and reducing the effect of exploitation (lowering crossover rate), achieving factorization of semi‑primes up to **22 decimal digits (~70 bits)** on a standard desktop, surpassing previous metaheuristic records (19 digits).

## Core content summary

### 1. Problem context
- RSA security relies on difficulty of factoring large semi‑primes (n = p·q).
- Classical methods: GNFS (asymptotically fastest) but not scalable for moderate sizes, complex implementation, overhead for small numbers.
- Metaheuristics (GAs, firefly, particle swarm, simulated annealing) offer alternative population‑based approaches that can be parallelized.

### 2. Related work (Section II)

| Authors | Method | Best result | Notes |
|---------|--------|-------------|-------|
| Yampolskiy (2010) | GA | 12 decimal digits | >6 hours, many local minima |
| Mishra et al. (2014) | Chaotic firefly | 14 digits | >80% success rate |
| Mishra et al. (2016) | Molecular geometry optimization | 14 digits | 69% success rate |
| Rutkowski & Houghton (2020) | GA (2‑point crossover, tournament selection) | **19 digits** | Prime form p = 6m ± 1 in binary |

**Limitations of prior work**: No elitism, duplicates in population, parents could be identical (redundancy), exploitation‑heavy.

### 3. Proposed method (Section III, Fig. 1)

**Key modifications to Rutkowski et al. (2020) GA**:

1. **Elitism**: Best individuals survive to next generation unchanged (retaining elite samples).
2. **Redundancy removal**:
   - No duplicates in initial population (size 2000).
   - Two parents selected for crossover are always different.
3. **Reduced exploitation**: Lowered crossover rate (default 90% after sensitivity analysis); mutation rate kept at 100%.

**Rationale**: Integer factorization is primarily an **exploration** problem, not exploitation. Crossover may not contribute significantly; lowering it improves runtime.

**Other parameters** (unchanged from Rutkowski et al.):
- Population size: 2000
- Generations: 2000
- Selection: Tournament (roulette wheel tested but slower)
- Chromosome: represents m in p = 6m ± 1 (binary form)
- Fitness: based on similarity of product to target N

### 4. Results (Section IV, Tables I–III, Figs. 2–3)

**Performance comparison** (Table I – factorization ability by digit length):

| # digits | Yampolskiy (2010) | Mishra et al. (2014/2016) | Rutkowski (2020) | **Proposed** |
|----------|-------------------|---------------------------|------------------|--------------|
| 11–12 | Yes | Yes | Yes | **Yes** |
| 14 | No | Yes | Yes | **Yes** |
| 15–18 | No | No | Yes | **Yes** |
| 19 | No | No | Yes | **Yes** |
| **20** | No | No | No | **Yes** |
| **21** | No | No | No | **No** |
| **22** | No | No | Yes | **Yes** |
| 22* | No | No | No | **No** |

*22‑digit number 45000005145200123902792 — not factored by proposed method.

**Success rate** (Table II – 30 runs per number):
- 11‑12 digits: 28–30/30 (93–100%)
- 14‑15 digits: 24–30/30 (80–100%)
- 16–19 digits: 1–15/30 (3–50%)
- 20 digits: 1/30 (3%) — first metaheuristic success at 20 digits
- 22 digits: 1/30 (3%) — first metaheuristic success at 22 digits

**Average generations to solution** (Table III):
- 11–12 digits: 121–2165 generations
- 14–15 digits: 415–5486 generations
- 16–18 digits: 569–14405 generations
- 19 digits: 12769 generations
- 20 digits: 399 generations (N = 31625125947164338313)
- 22 digits: 2514 generations (N = 3381755902745713031047)

**Runtime**: For 22‑digit number, <1 hour on standard desktop (2000 generations, 30 runs). Previous best (Rutkowski 2020) took 6 hours for 19 digits.

**Fitness plots** (Figs. 2–3):
- For 20‑digit N, perfect fitness (0) reached at generation 399.
- For 22‑digit N, perfect fitness reached at generation 457.

**Sensitivity analysis**: Crossover rate 90% gave best results; lower rates reduced efficiency for larger digit lengths.

### 5. Discussion (Section V)

**Advantages over GNFS**:
- GNFS not scalable for larger integers; complexity exponential; polynomial selection challenging.
- GNFS inefficient for smaller integers (overhead).
- Proposed GA is population‑based, operations independent → easily parallelizable on multiple clusters.
- Works well for both small and moderate‑sized integers with quick convergence.

**Claim**: Best metaheuristic factorization result to date (22 decimal digits) — breaking bottleneck of previous approaches.

### 6. Limitations (explicit from source / observed)

- **Maximum factored**: 22 decimal digits (~70 bits). For cryptographically relevant RSA sizes (1024–2048 bits = 308–617 digits), this is minuscule.
- **Success rate** drops sharply with digit length (3% at 22 digits).
- **Not all 22‑digit numbers** factored (e.g., 45000005145200123902792 failed).
- **No comparison** with classical factoring algorithms (GNFS, ECM, QS) on same hardware — cannot claim practical superiority.
- **Population size (2000) and generations (2000)** are fixed; scaling to larger numbers would require enormous increases.
- **Theoretical insight** that IF is "exploration‑only" is asserted but not proven.
- **No parallelization** actually implemented; only claimed as potential.

## Key claims vs. classical factoring (authors' perspective)

| Aspect | GNFS (classical) | Proposed GA |
|--------|------------------|-------------|
| Asymptotic complexity | L_n[1/3, 1.923] | Not analyzed |
| Scalability | Not scalable for moderate sizes | Claimed scalable (population‑based) |
| Implementation | Complex (polynomial selection) | Simpler (GA parameters) |
| Parallelization | Possible (sieving) | Claimed easily parallelizable |
| Performance on 22 digits | Trivial (milliseconds) | <1 hour, 3% success rate |

## Conclusions (Section VI)

- Proposed GA (elitism + no duplicates + 90% crossover) achieves best metaheuristic factorization results to date: **22 decimal digits**, <1 hour.
- Better success rate and fewer generations than prior GA‑based methods.
- Roulette wheel selection performed worse (slower, worse convergence).
- Future work: incorporate recent theoretical results [21], formulate as multi‑objective optimization [22,23].

## References (selected)
- Yampolskiy (2010) — Bio‑inspired algorithm for IF.
- Rutkowski & Houghton (2020) — GA for RSA cryptanalysis (19 digits).
- Mishra et al. (2014, 2016) — Firefly and molecular optimization.
- Mishra et al. (2015) — Limitations of evolutionary computation for IF.
- Pandey & Pal (2014) — Guide to GNFS.
