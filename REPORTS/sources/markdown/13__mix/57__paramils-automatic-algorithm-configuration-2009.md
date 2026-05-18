---
title: "ParamILS: An Automatic Algorithm Configuration Framework"
title_en: "ParamILS: An Automatic Algorithm Configuration Framework"
source_type: "article"
authors: ["Hutter F.", "Hoos H. H.", "Leyton-Brown K.", "Stützle T."]
year: "2009"
source_link: "unknown (provided PDF: 57__live-2861-4703-jair.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "paramils-automatic-algorithm-configuration-2009.md"
---

# Content source: ParamILS: An Automatic Algorithm Configuration Framework

## Source type
Peer-reviewed journal article (Journal of Artificial Intelligence Research, JAIR, 2009).

## Authors affiliation
- Frank Hutter, Holger H. Hoos, Kevin Leyton-Brown — University of British Columbia, Canada
- Thomas Stützle — Université Libre de Bruxelles, Belgium

## Objective
Present ParamILS (Parameter Iterated Local Search), an automatic algorithm configuration framework for optimizing performance of parameterized algorithms (including categorical, ordinal, and numerical parameters) on given instance distributions, with adaptive capping techniques to accelerate evaluation.

## Core methodology

### Problem formulation (Algorithm Configuration Problem)
- Input: ⟨A, Θ, D, κ_max, o, m⟩
  - A: parameterized algorithm
  - Θ: parameter configuration space (finite, categorical parameters, conditional dependencies)
  - D: distribution over problem instances Π
  - κ_max: cutoff time (runs terminated after this)
  - o: observed cost function (runtime, solution quality)
  - m: statistical population parameter (expectation, median, variance)
- Goal: minimize c(θ) = m(O_θ) over θ ∈ Θ

### ParamILS framework (Iterated Local Search in configuration space)
- Neighbourhood: one-exchange (change one parameter at a time)
- Procedure:
  1. Initialize: r random configurations, keep best as θ_0
  2. IterativeFirstImprovement from θ_0 (local optimum)
  3. Perturbation: s random moves
  4. Local search from perturbed configuration
  5. Acceptance: accept if better, restart with probability p_restart
- Handles conditional parameters: exclude irrelevant configurations from neighbourhood

### BasicILS(N)
- Evaluates each configuration on fixed N training instances (same instances/seeds for fair comparison)
- Uses Procedure better_N: compare cost estimates ĉ_N based on N runs
- Simple, but N must be chosen (tradeoff: speed vs generalization)

### FocusedILS
- Adaptively varies number of runs per configuration
- Domination: θ₁ dominates θ₂ iff N(θ₁) ≥ N(θ₂) and ĉ_{N(θ₂)}(θ₁) ≤ ĉ_{N(θ₂)}(θ₂)
- Comparison: repeatedly add runs to the configuration with fewer runs until one dominates
- Bonus runs: after improvement, perform B bonus runs for winner (B = #configurations evaluated since last improvement)
- Theoretical guarantee: converges to true optimum in limit (for consistent estimators)

### Adaptive capping (trajectory-preserving and aggressive)
- Lower bound on mean runtime after i runs: (sum of runtimes) / N
- If bound exceeds current best, terminate evaluation early
- Trajectory-preserving (TP): bound based on best config in current ILS iteration
- Aggressive (Aggr): bound = min(∞, bm·ĉ_N(θ_inc)) with bound multiplier bm (default 2)
- Procedure objective implements capping with re-use of cached runs

## Key results

### BROAD configuration scenarios (5-second cutoff, 5 CPU hours configuration)

| Scenario | Default runtime | BasicILS(100) (mean ± std) | FocusedILS (mean ± std) | Best training run (Basic / Focused) |
|----------|----------------|----------------------------|-------------------------|--------------------------------------|
| SAPS-SWGCP | 20.4 | 0.32 ± 0.06 | 0.32 ± 0.05 | 0.26 / 0.26 |
| SPEAR-SWGCP | 9.74 | 8.05 ± 0.9 | 8.3 ± 1.1 | 6.8 / 6.6 |
| SAPS-QCP | 12.97 | 4.86 ± 0.56 | 4.70 ± 0.39 | 4.85 / 4.29 |
| SPEAR-QCP | 2.65 | 1.39 ± 0.33 | 1.29 ± 0.21 | 1.16 / 1.21 |
| CPLEX-REGIONS100 | 1.61 | 0.5 ± 0.3 | 0.35 ± 0.04 | 0.35 / 0.32 |

**Speedups** (with larger cutoff, 1 hour):
- SAPS-SWGCP: default 531s → optimized 0.15s (factor 3540)
- SAPS-QCP: default 72s → optimized 0.17s (factor 424)
- SPEAR-QCP: default 9.6s → optimized 0.85s (factor 11.3)

### Comparison: BasicILS vs RandomSearch(100) (no capping)
- BasicILS better in all 5 scenarios; significant in 3 (SAPS-SWGCP, SAPS-QCP, SPEAR-QCP)
- Both substantially outperform defaults

### Comparison: FocusedILS vs BasicILS(100) (no capping)
- FocusedILS significantly better on SAPS-SWGCP, SAPS-QCP, CPLEX-REGIONS100
- No significant difference on SPEAR scenarios

### Adaptive capping speedups (BasicILS(100))

| Scenario | No capping | TP capping | p-value | # ILS iterations (no/TP) |
|----------|------------|------------|---------|--------------------------|
| SAPS-SWGCP | 0.38 ± 0.19 | 0.24 ± 0.05 | 6.1·10⁻⁵ | 3 / 12 |
| SAPS-QCP | 3.19 ± 1.19 | 2.96 ± 1.13 | 9.8·10⁻⁴ | 6 / 10 |
| CPLEX-REGIONS100 | 0.67 ± 0.35 | 0.47 ± 0.26 | 7.3·10⁻⁴ | 1 / 1 |

TP capping enabled up to 4× more ILS iterations. Aggressive capping further improved SAPS-SWGCP (12→219 iterations).

### CPLEX case study (300s cutoff, 2 days configuration)

| Scenario | Default | BasicILS(100) best training | FocusedILS best training | Speedup factor |
|----------|---------|----------------------------|--------------------------|----------------|
| CPLEX-REGIONS200 | 72s | 10.5s | 10.5s | ~7× |
| CPLEX-CONIC.SCH | 5.37s | 2.39s | 2.39s | ~2.2× |
| CPLEX-CLS | 309s | 21.5s | 21.5s | ~14× |
| CPLEX-MIK | 28s | 1.2s | 1.2s | ~23× |
| CPLEX-QP | 296s | 234s | (timeout issue) | —

## Key insights
- Most parameters can be categorical — ParamILS handles arbitrary parameter types.
- Conditional parameters reduce effective configuration space size (e.g., SPEAR: 3.7·10¹⁸ → 8.34·10¹⁷).
- Adaptive capping dramatically speeds up configuration without (TP) or with minimal (Aggr) search trajectory change.
- Multiple parallel configuration runs with best training performance selection yields robust test performance.
- Mean runtime optimization produces robust configurations (vs median which can overfit).

## Theoretical guarantees
- Lemma 6: FocusedILS evaluates each configuration unboundedly often (due to random restarts).
- Lemma 8: For consistent estimators, probability of comparing two configurations incorrectly → 0 as N → ∞.
- Theorem 9: FocusedILS converges to true optimal configuration in limit.

## Limitations (explicit)
- FocusedILS struggles with highly heterogeneous instance distributions (extrapolates from few runs).
- Numerical parameters must be discretized by user (no continuous optimization within ParamILS).
- Choosing cutoff time κ_max critical: too small may not generalize to longer runs (CPLEX-QP failure mode).
- Overhead of Ruby implementation significant for very fast target algorithms (millisecond runs).

## Practical recommendations
1. Use homogeneous instance distributions when possible.
2. Split instances into disjoint training/test sets to avoid overfitting.
3. Use mean (not median) runtime with penalized timeouts (10× cutoff) for robust optimization.
4. Run multiple independent configuration runs (e.g., 10–25) in parallel; select best training performance.
5. Use aggressive capping with bm=2 (default) for best speed.
6. For highly heterogeneous instances, consider BasicILS over FocusedILS.

## Applications beyond paper
- Configuring SPEAR for industrial verification (500× speedup on SWV)
- SATenstein: automatic construction of SAT solvers from components (41 parameters, outperformed 11 state-of-the-art solvers)
- Protein folding (Thachuk et al., 2007)
- Course timetabling (Fawcett et al., 2009, 3rd in ITC2007)

## Conclusions
- ParamILS is a versatile, effective framework for automatic algorithm configuration.
- Substantial improvements over manually tuned defaults (up to 3 orders of magnitude).
- Adaptive capping provides order-of-magnitude speedups.
- Open source implementation available at http://www.cs.ubc.ca/labs/beta/Projects/ParamILS/
