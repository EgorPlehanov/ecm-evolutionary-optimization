---
title: "An Evaluation of Sequential Model-Based Optimization for Expensive Blackbox Functions"
title_en: "An Evaluation of Sequential Model-Based Optimization for Expensive Blackbox Functions"
source_type: "conference"
authors: ["Hutter F.", "Hoos H. H.", "Leyton-Brown K."]
year: "2013"
source_link: "unknown (provided PDF: 65__2464576.2501592.pdf)"
doi: "10.1145/2464576.2501592"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "smac-bbob-evaluation-expensive-blackbox-2013.md"
---

# Content source: An Evaluation of Sequential Model-Based Optimization for Expensive Blackbox Functions

## Source type
Peer-reviewed conference paper (GECCO 2013 Companion — Genetic and Evolutionary Computation Conference, Amsterdam).

## Authors affiliation
- Frank Hutter — Freiburg University, Germany
- Holger Hoos, Kevin Leyton-Brown — University of British Columbia, Canada

## Objective
Evaluate SMAC-BBOB — a variant of the sequential model-based algorithm configuration procedure SMAC adapted for continuous blackbox optimization — on the BBOB (Blackbox Optimization Benchmarking) set of functions, comparing against CMA-ES (state-of-the-art) and best BBOB-2009 results, with budgets of 10×D and 100×D evaluations.

## Core methodology

### SMAC-BBOB adaptations for continuous optimization
- **Model**: Gaussian process (GP) instead of random forest (RF) — RF performed poorly on continuous problems (poor extrapolation, uncertainty estimates)
- **Kernel**: Isotropic Matérn kernel (noise-free) — less smooth than squared exponential; yields better results for BBOB functions
- **Initial design**: None (EGO uses 10×D initial evaluations; SMAC-BBOB skips this)
- **Acquisition function**: Expected Improvement (EI) — E[I(θ)] = E[max(0, f_min − f(θ))]
- **EI optimization**: Multi-start local search + one run of DIRECT (10×D evaluations of EI) + 10 runs of CMA-ES (100×D evaluations of EI) — all on cheap model evaluations, not expensive function

### Key differences from EGO
| Feature | EGO | SMAC-BBOB |
|---------|-----|-----------|
| Kernel | ARD squared exponential (different length scales per dimension) | Isotropic Matérn (single length scale) |
| Initial design | 10×D evaluations | None |
| Hyperparameter optimization | Maximum likelihood | (implied via kernel choice) |

## Key results

### Comparison: SMAC-BBOB vs CMA-ES (budget 10×D evaluations)

| Finding | Detail |
|---------|--------|
| SMAC-BBOB better | 13/24 functions for at least one dimension (5, 10, 20, 40) |
| Notable improvements | Functions 5 (linear slope), 6 (attractive sector), 7 (step-ellipsoid), 11 (discuss), 13 (sharp ridge) |
| Scaling | ERTs scale similarly with dimension for both methods |
| Performance pattern | SMAC-BBOB excels on separable, multimodal, weakly-structured functions |

### Budget increase to 100×D
- CMA-ES catches up and overtakes SMAC-BBOB in several cases
- SMAC-BBOB better on 7/24 functions, CMA-ES better on 8/24

### Comparison to best BBOB-2009 results (10×D budget)

| Dimension | SMAC-BBOB competitive on |
|-----------|--------------------------|
| D=5 | 2 functions, 3 target values |
| D=20 | 7 functions, 11 target values |

- Particularly strong on multimodal function f22 in D=20 (performance improves as target becomes more demanding)

### Computational requirements

| Budget | D=2 | D=20 |
|--------|-----|------|
| 10×D evaluations | tens of seconds | ~20 minutes |
| 100×D evaluations | ~5 minutes | 15–120 hours |

- GP fitting complexity O(N³) — grows cubically with number of evaluations
- SMAC-BBOB primarily targets very expensive functions where evaluation cost dominates modeling cost

## Key insights

1. **RF models suboptimal for continuous optimization**: Poor extrapolation, uncertainty estimates; performed badly even on simple linear function f5 (1/15 runs reached 10⁻⁸ vs 15/15 for GP)
2. **Noisy kernel detrimental**: Adding observation noise to GP produced overly smooth surfaces; noise-free Matérn kernel better
3. **No initial design beneficial**: For budgets ≤10×D, initial design wastes evaluations that could be used for exploration
4. **Isotropic vs ARD**: Simple isotropic Matérn kernel outperformed ARD squared exponential in high dimensions for small budgets

## Limitations (explicit)
- Not designed for budgets >100×D (CMA-ES overtakes)
- Computational cost grows cubically with evaluations (O(N³) GP fitting)
- SMAC-BBOB's performance depends on effective subsidiary optimizers (CMA-ES, DIRECT)
- BBOB functions are deterministic, continuous — does not test SMAC's strengths (categorical parameters, conditional spaces, censored data, noise)

## Practical recommendations
1. Use SMAC-BBOB for **very expensive** functions with budget ≤10×D
2. Use CMA-ES for budgets ≥100×D
3. For continuous optimization, prefer GP over RF models
4. Use noise-free Matérn kernel (not squared exponential with observation noise)
5. Skip initial design when budget is very tight

## Conclusions
- SMAC-BBOB outperforms CMA-ES for 10×D budget on many BBOB functions (13/24)
- Particularly effective for separable, multimodal, weakly-structured functions
- Competitive with best BBOB-2009 results for low budgets
- Not competitive for larger budgets (100×D) due to computational overhead and CMA-ES catching up
