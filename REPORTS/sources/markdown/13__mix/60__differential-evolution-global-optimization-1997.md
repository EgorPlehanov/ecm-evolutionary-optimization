---
title: "Differential Evolution - A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces"
title_en: "Differential Evolution - A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces"
source_type: "article"
authors: ["Storn R.", "Price K."]
year: "1997"
source_link: "unknown (provided PDF: 60__storn_price_de.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "differential-evolution-global-optimization-1997.md"
---

# Content source: Differential Evolution - A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces

## Source type
Peer-reviewed journal article (Journal of Global Optimization, Kluwer Academic Publishers, 1997).

## Authors affiliation
- Rainer Storn — Siemens AG, Munich, Germany
- Kenneth Price — Vacaville, CA, USA

## Objective
Introduce Differential Evolution (DE) — a novel, simple, and efficient heuristic for global optimization over continuous spaces — and demonstrate its superior performance compared to annealing methods, evolutionary algorithms, and stochastic differential equations on extensive testbeds.

## Core methodology

### Algorithm overview
DE is a parallel direct search method using NP D-dimensional parameter vectors x_{i,G} as a population for each generation G.

**Mutation** (DE/rand/1/bin — the basic strategy):
- For each target vector x_{i,G}, generate mutant vector:
  - v_{i,G+1} = x_{r1,G} + F·(x_{r2,G} − x_{r3,G})
- r1, r2, r3 ∈ {1,…,NP}, mutually different and ≠ i
- F ∈ [0,2] — amplification factor for differential variation

**Crossover** (binomial):
- Trial vector u_{i,G+1} inherits parameters:
  - from v_{i,G+1} if randb(j) ≤ CR or j = rnbr(i)
  - from x_{i,G} otherwise
- CR ∈ [0,1] — crossover constant
- rnbr(i) ensures at least one parameter from mutant

**Selection** (greedy):
- If cost(u_{i,G+1}) ≤ cost(x_{i,G}), then x_{i,G+1} = u_{i,G+1}
- Otherwise retain x_{i,G}

### Notation for DE variants
- DE/x/y/z
  - x: vector to be mutated (rand, best)
  - y: number of difference vectors (1, 2)
  - z: crossover scheme (bin, exp)

Examples:
- DE/rand/1/bin — basic strategy (this paper)
- DE/best/2/bin — uses best vector + 2 differences

## Key results

### Testbed #1 (9 functions, vs ANM and ASA)

| Function | ANM nfe | ASA nfe | DE/rand/1/bin nfe | DE found minimum? |
|----------|---------|---------|-------------------|-------------------|
| f₁ (sphere) | n.a. | n.a. | 397 | Yes |
| f₂ (Rosenbrock) | n.a. | 11,275 | 967 | Yes |
| f₃ (step) | 3000 | 212 | 494 | Yes |
| f₄ (quartic) | — | 4,812 | 1,379 | Yes |
| f₅ (Shekel) | — | 3,581 | 2,116 | Yes |
| f₆ (Corana) | — | 12,752 | 2,112 | Yes |
| f₇ (Griewangk) | — | 11,864 | 1,912 | Yes |
| f₈ (Zimmermann) | — | — | 2,959 | Yes |
| f₉ (T₈ polynomial) | — | (391,373) | 2,116 | Yes (DE only) |
| f₁₀ (T₁₆ polynomial) | — | — | 3,650 | Yes (DE only) |

**Key finding**: DE was the only strategy that found all global minima.

### Testbed #2 (5 functions, vs BGA and EASY)

| Function | D | BGA nfe | EASY nfe | DE/rand/1/bin nfe |
|----------|---|---------|----------|-------------------|
| f₁₁ (hyper-ellipsoid) | 30 | NA | 27,111 | 16,907 |
| f₁₁ | 100 | NA | 104,520 | 56,145 |
| f₁₂ (Katsuura) | 10 | NA | 9,626 | 4,269 |
| f₁₂ | 30 | NA | 39,333 | 12,859 |
| f₁₃ (Rastrigin) | 20 | 3,608 | 6,098 | 12,971 |
| f₁₄ (Griewangk) | 20 | 66,000 | 26,700 | 8,691 |
| f₁₄ | 100 | 361,722 | 77,250 | 31,796 |
| f₁₅ (Ackley) | 30 | 19,420 | 13,997 | 12,481 |
| f₁₅ | 100 | 53,860 | 57,628 | 36,801 |

DE required fewest evaluations in 8 of 10 cases.

### Testbed #3 (15 functions, vs SDE)

| Function | SDE nfe (best reported) | DE/rand/1/bin nfe | DE success rate |
|----------|------------------------|-------------------|-----------------|
| f₁₆ (Goldstein) | 163,184 | 503 | 100% |
| f₁₇ (Shubert 1D) | 726,893 | 499 | 100% |
| f₁₈ (Shubert 2D) | 241,215 | 3,137 | 100% |
| f₂₀ (6-hump camel) | 5,393 | 927 | 100% |
| f₂₅ (1D quartic) | 6,751 | 273 | 100% |
| f₃₀ (likelihood) | 48,802 | 1,266 | 100% |

DE outperformed SDE in all cases with 100% success rate.

## Parameter guidelines (from extensive experimentation)

| Parameter | Recommended range | Notes |
|-----------|-------------------|-------|
| NP | 5×D to 10×D | Must be ≥4 |
| F | 0.5 (initial) | Increase if premature convergence; <0.4 or >1 rarely effective |
| CR | 0.1 (initial) or 0.9/1.0 for speed | Large CR often speeds convergence |
| IPR | Cover suspected global optimum | Not mandatory but helpful |

## Properties and advantages

1. **Handles non-differentiable, nonlinear, multimodal cost functions** — direct search method.
2. **Parallelizable** — vector population perturbations independent.
3. **Easy to use** — few robust control variables.
4. **Good convergence** — consistent convergence across independent trials.

**Self-organization**: DE borrows from Nelder-Mead the idea of using information from within the population to alter search space. Difference vector of two randomly chosen vectors perturbs an existing vector — in contrast to ESs which use predetermined probability distributions.

**Divergence property**: When objective function surface is flat, vector distances increase, preventing slow progress. Near minimum, distances decrease due to selection.

## Test functions summary

**Testbed #1** (9 functions, D=1–30): Sphere, Rosenbrock, Step, Quartic, Shekel's Foxholes, Corana's parabola, Griewangk, Zimmermann's problem, Chebyshev polynomial fitting (T₈, T₁₆).

**Testbed #2** (5 functions, D=10–100): Hyper-ellipsoid, Katsuura, Rastrigin, Griewangk, Ackley.

**Testbed #3** (15 functions, D=1–5): Goldstein, Shubert family, 6-hump camel, penalized trigonometric functions, likelihood function.

## Limitations (explicit)

- No mathematical convergence proof (unlike Simulated Annealing).
- Scaling behavior for very large problems (>100 parameters) unknown.
- Most complex real-world applications solved: 60-parameter FIR filter, 30-parameter communications control.
- Combination with other optimization approaches not yet studied.

## Conclusions
- DE is extremely simple (main engine <30 lines of C code), robust, and effective.
- Outperformed ASA, ANM, BGA, EASY, and SDE on extensive testbeds.
- Self-organizing nature is remarkable and deserves deeper theoretical analysis.
- Practical rules of thumb for control variables make DE easy to use.
