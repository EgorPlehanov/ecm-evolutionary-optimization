---
title: "Differential Evolution - A Simple and Efficient Adaptive Scheme for Global Optimization over Continuous Spaces"
title_en: "Differential Evolution - A Simple and Efficient Adaptive Scheme for Global Optimization over Continuous Spaces"
source_type: "technical_report"
authors: ["Storn R."]
year: "1995"
source_link: "unknown (provided PDF: 69__Storn95-012.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-18"
suggested_filename: "differential-evolution-original-technical-report-1995.md"
---

# Content source: Differential Evolution - A Simple and Efficient Adaptive Scheme for Global Optimization over Continuous Spaces

## Source type
Technical report (ICSI, Berkeley, Report No. TR-95-012, 1995).

## Author affiliation
Rainer Storn — International Computer Science Institute, Berkeley, CA (on leave from Siemens AG, Munich).

## Objective
Introduce Differential Evolution (DE) — a new parallel direct search method for global optimization over continuous spaces — and demonstrate its superior performance compared to Adaptive Simulated Annealing (ASA) and Annealed Nelder-Mead (ANM) on a testbed of 9 challenging functions.

## Core methodology

### Problem formulation
- System properties g_m (objectives and constraints) dependent on D-dimensional parameter vector x.
- Combine into single objective function z(x) via weighted sum or max (Pareto formulation).
- Goal: minimize z(x) over x ∈ ℝᴰ.

### DE1 scheme (basic variant)
- Population: NP D-dimensional vectors x_i,G.
- For each target vector i, generate trial vector v:
  - v = x_{r1,G} + F·(x_{r2,G} − x_{r3,G})
  - r1, r2, r3 mutually different random indices, also ≠ i.
  - F > 0 (scale factor, typically 0.5–1.0).
- **Crossover** (exponential): parameters from v replace target vector parameters starting at random index n for length L (geometric distribution with crossover probability CR).
- **Selection**: trial vector u replaces target vector x_i,G if f(u) ≤ f(x_i,G).

### DE2 scheme
- Alternative: v = x_i,G + λ·(x_best,G − x_i,G) + F·(x_{r2,G} − x_{r3,G})
- Combines attraction toward best vector with difference perturbation.
- Uses binomial crossover.

## Test functions (9 functions)

| # | Name | Dim | Domain | Min | Characteristics |
|---|------|-----|--------|-----|-----------------|
| f₁ | Sphere | 3 | [-5.12, 5.12] | 0 | Simple, unimodal |
| f₂ | Rosenbrock | 2 | [-2.048, 2.048] | 0 | Narrow curved valley |
| f₃ | Step (De Jong) | 5 | [-5.12, 5.12] | 0 | Plateaus |
| f₄ | Quartic (noisy) | 30 | [-1.28, 1.28] | ≤15 | Uniform noise |
| f₅ | Shekel's Foxholes | 2 | [-65.536, 65.536] | ≈0.998 | Many local minima |
| f₆ | Corana's parabola | 4 | [-1000, 1000] | 0 | Holes increasing near origin |
| f₇ | Griewangk | 10 | [-400, 400] | 0 | Many local minima, product term |
| f₈ | Zimmermann's problem | 2 | [0,100] | 0 | Constrained, min at corner |
| f₉ | Chebyshev T₈ | 9 | [-100,100] | 0 | Large magnitude differences |
| f₁₀ | Chebyshev T₁₆ | 17 | [-1000,1000] | 0 | Same, higher degree |

## Key results (10 trials per function)

### Performance comparison — number of function evaluations (nfe) to reach global minimum

| Function | ANM | ASA | DE1 (F=0.5) | DE2 (F=1) |
|----------|-----|-----|-------------|-----------|
| f₁ (sphere) | n.a. | 397 | 566 | 392 |
| f₂ (Rosenbrock) | n.a. | 11,275 | 746 | 566 |
| f₃ (step) | 3,000 | 212 | 385 | 298 |
| f₄ (quartic) | — | 4,812 | 1,375 | 1,257 |
| f₅ (Shekel) | — | 3,581 | 3,520 | 1,125 |
| f₆ (Corana) | — | 12,752 | 2,804 | 1,257 |
| f₇ (Griewangk) | — | 11,864 | 1,559 | 769 |
| f₈ (Zimmermann) | — | — | 4,943 | 1,069 |
| f₉ (T₈) | — | (391,373) | 1,943 | 901 |
| f₁₀ (T₁₆) | — | — | 5,680 | 2,482 |

### Key findings
- **DE only method** that converged for all 10 functions.
- ASA failed on f₈ (Zimmermann) and f₁₀ (T₁₆); ANM failed on f₄–f₁₀.
- For functions where ASA or ANM converged, DE converged faster (often by factor 2–10×).
- DE2 consistently outperformed DE1 on all test functions.

## Parameter settings (from Table I)

| Method | Key parameters |
|--------|----------------|
| DE1 | NP=10–100 (varies), F=0.5–0.9, CR=0.2–0.5 |
| DE2 | NP=10–80, F=0.2–1.0, CR=0.2–0.9, λ=0.5–1.0 |
| ANM | T=1·10⁻⁵–1·10⁻⁷, TF=0.5–0.995, NV=50–100 |
| ASA | TRS=1·10⁻⁵–1·10⁻⁷, TAS=100–100,000 |

## Key insights

### Why DE works (author's hypotheses)
1. **Adaptive step sizes**: Difference vectors automatically adapt to the natural scaling of the problem (small in compact variables, large in dispersed variables).
2. **Contour matching**: The population's difference vectors reflect the local topography of the objective function.
3. **Inherent parallelism**: NP independent trial vector generations per generation.
4. **Robust crossover**: Exponential crossover balances exploration and exploitation.

### Advantages over competitors
- **Over ASA**: No cooling schedule tuning; faster convergence; finds minima ASA misses.
- **Over ANM**: Not just local search with annealing; population-based global search.
- **Simplicity**: 4–5 lines of code for main loop.

## Limitations (explicit)
- Parameter choice (NP, F, CR) still heuristic; no theoretical guidance.
- No convergence proof (unlike SA).
- DE2's λ parameter adds another degree of freedom.
- Computational cost per generation O(NP·D).

## Historical significance
- **First public description of DE** (precedes the 1996 ICEC contest and 1997 Journal of Global Optimization paper by Storn & Price).
- Introduces DE1 (DE/rand/1/bin) and DE2 (DE/current-to-best/1/bin).
- First systematic comparison against ASA and ANM on a diverse testbed.
- Establishes DE as a serious competitor to established global optimization methods.

## Practical recommendations (from author)
- DE2 (with attraction to best vector) generally outperforms DE1.
- F = 0.5–1.0 works for most problems.
- CR = 0.2–0.9 depending on problem separability.
- NP = 10–100 depending on dimensionality.
