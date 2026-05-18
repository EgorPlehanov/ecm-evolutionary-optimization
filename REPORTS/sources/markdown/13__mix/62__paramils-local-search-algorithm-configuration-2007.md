---
title: "Automatic Algorithm Configuration based on Local Search"
title_en: "Automatic Algorithm Configuration based on Local Search"
source_type: "conference"
authors: ["Hutter F.", "Hoos H. H.", "Stützle T."]
year: "2007"
source_link: "unknown (provided PDF: 62__AAAI07-183.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "paramils-local-search-algorithm-configuration-2007.md"
---

# Content source: Automatic Algorithm Configuration based on Local Search

## Source type
Peer-reviewed conference paper (AAAI 2007 — Association for the Advancement of Artificial Intelligence).

## Authors affiliation
- Frank Hutter, Holger H. Hoos — University of British Columbia, Canada
- Thomas Stützle — Université Libre de Bruxelles, Belgium

## Objective
Present ParamILS (Parameter Iterated Local Search), a local search approach for automatic algorithm configuration that handles arbitrary parameter types (categorical, ordinal, continuous via discretization) and conditional parameters, with convergence guarantees and empirical validation on SAT solvers and MPE algorithms.

## Core methodology

### Problem formulation
- Parameter configuration space Θ: cross-product of parameter domains (finite via discretization)
- Cost distribution CD(A, θ, D) induced by running A(θ) on instances from distribution D
- Goal: minimize statistic c(θ) (mean, median, etc.) of cost distribution
- Approximate via consistent estimator ĉ_N(θ) based on N samples

### BasicILS(N)
- Iterated local search in configuration space with one-exchange neighbourhood (change one parameter at a time)
- Initialization: default config + R random configs (keep best)
- IterativeFirstImprovement (greedy local search)
- Perturbation: s random moves
- Acceptance: always accept better/equal; restart with probability p_restart
- Handles conditional parameters: exclude irrelevant configs from neighbourhood
- Compares configurations using ĉ_N based on fixed N samples (N=100 in experiments)

### Over-confidence and over-tuning
**Problem**: ĉ_N(θ_train*) (best on training) underestimates c(θ_train*) (true cost). With exponential cost distributions, E[ĉ_1(θ_train*)] = (∑ λ_θ)⁻¹, which underestimates true mean by factor of number of configurations evaluated in expectation.

**Consequence**: Over-tuning — additional tuning actually impairs test performance (analogous to overfitting in ML).

**Lemma 1** (Bias for exponential distributions): If CD ∼ Exp(λ_θ), then ĉ_1(θ_train*) ∼ Exp(∑ λ_θ).

**Lemma 2** (No mistakes): For consistent estimators, lim_{N→∞} P(ĉ_N(θ₁) ≥ ĉ_N(θ₂)) = 0 when c(θ₁) < c(θ₂).

### FocusedILS (avoids over-confidence/over-tuning)
- Adaptively increases N(θ) (number of samples) for promising configurations
- **Domination**: θ₁ dominates θ₂ iff N(θ₁) ≥ N(θ₂) and ĉ_{N(θ₂)}(θ₁) < ĉ_{N(θ₂)}(θ₂)
- **Comparison**: repeatedly sample configuration with smaller N until one dominates
- **Bonus runs**: after improvement, sample B bonus runs for winner (B = #configurations evaluated since last improvement)

**Lemma 3** (Unbounded evaluations): lim_{J→∞} P(N(J,θ) ≥ K) = 1 for any θ, K (due to random restarts).

**Theorem 4** (Convergence): FocusedILS converges to true optimal parameter configuration θ* as iterations → ∞.

## Key results

### Configuration scenarios

| Scenario | Algorithm | Parameters | Configurations | Objective |
|----------|-----------|------------|----------------|-----------|
| SAT4J-SW | SAT4J (tree search) | 7 (categorical + conditional) | 567,000 | Minimize median runtime |
| SAPS-SW | SAPS (local search SAT) | 4 (continuous) | 2,401 | Minimize median runtime |
| SAPS-QWH | SAPS | 4 (continuous) | 2,401 | Minimize median run-length |
| GLS-GRID | GLS⁺ (MPE) | 5 | 1,680 | Maximize solution quality |

### Performance comparison (25 repetitions, N=100 for BasicILS/CALIBRA)

| Scenario | Default | CALIBRA(100) test | BasicILS(100) test | FocusedILS test | FocusedILS vs CALIBRA p-value |
|----------|---------|-------------------|---------------------|-----------------|-------------------------------|
| SAPS-SW | 9.7s | 6.6 ± 0.7s | 6.2 ± 0.2s | **6.0 ± 0.1s** | 0.003 |
| SAPS-QWH | 0.023s | 0.020 ± 0.002s | 0.018 ± 0.001s | **0.017 ± 0.001s** | 3·10⁻⁶ |
| GLS-GRID | 0.31 ε | 0.44 ± 0.01 ε | 0.46 ± 0.01 ε | **0.49 ± 0.01 ε** | 3·10⁻⁷ |

(ε < 1 means tuned finds better solutions in 10 seconds than default in 1 hour)

**SAT4J-SW** (CALIBRA not applicable due to >5 parameters):
- Default median runtime: ~50s
- BasicILS(100): ~20s
- FocusedILS: **~18s** (best test performance)

### Over-tuning demonstration (SAPS-QWH, BasicILS(1))
- Training performance (single run) suggests run-length ~0.01s
- Test performance (1000 runs) shows actual run-length ~0.03–0.1s — **3–10× worse**
- FocusedILS avoids divergence (training ≈ test)

### SAPS speedup on SW-GCP (tuned on easy subclass SW-GCP-saps, 1 hour)
- Default SAPS: median 33s, average 263s
- Tuned SAPS (α=1.189, ρ=0.666, P_smooth=0.066, wp=0.01): median 0.09s, average 0.43s
- **Speedup: 3–4 orders of magnitude** (up to 10,000×)

## Comparison to CALIBRA

| Feature | CALIBRA | ParamILS |
|---------|---------|----------|
| Max parameters | 5 (numerical only) | Unlimited (categorical, conditional) |
| Search method | Fractional factorial + local search | Iterated local search |
| Over-confidence | Yes (fixed N) | FocusedILS avoids |
| Convergence guarantee | No | Yes (FocusedILS) |

## Practical recommendations
1. **Use FocusedILS** for best test performance and to avoid over-tuning.
2. **Discretize numerical parameters** uniformly or logarithmically based on scale.
3. **Split instances** into independent training and test sets.
4. **Use consistent estimator**: sample N instances with single run each (minimizes variance for expected cost).
5. **Conditional parameters**: define dependency graph; ParamILS handles automatically.

## Limitations (explicit)
- Numerical parameters require discretization (no continuous optimization within ParamILS).
- BasicILS suffers from over-confidence/over-tuning for small N.
- Requires sufficient budget for meaningful results.
- Theoretical convergence assumes finite configuration space (via discretization).

## Practical impact
- Used to tune SAT4J, SAPS, GLS⁺
- Applied to protein structure prediction (Thachuk et al., 2007) — 50% improvement
- Used to boost verification tools (Hutter et al., 2007) — 50× speedup
- Open source code available at http://www.cs.ubc.ca/labs/beta/Projects/ParamILS

## Conclusions
- ParamILS is versatile, handles arbitrary parameter types and conditional parameters.
- FocusedILS provably converges to optimal configuration and avoids over-tuning.
- Outperforms CALIBRA and algorithm defaults (often by orders of magnitude).
- Open source implementation enables widespread adoption.
