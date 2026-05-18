---
title: "Random Search for Hyper-Parameter Optimization"
title_en: "Random Search for Hyper-Parameter Optimization"
source_type: "article"
authors: ["Bergstra J.", "Bengio Y."]
year: "2012"
source_link: "unknown (provided PDF: 55__bergstra12a.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "random-search-for-hyperparameter-optimization-2012.md"
---

# Content source: Random Search for Hyper-Parameter Optimization

## Source type
Peer-reviewed journal article (Journal of Machine Learning Research, 2012).

## Authors affiliation
Département d'Informatique et de recherche opérationnelle, Université de Montréal, Canada.

## Objective
Demonstrate empirically and theoretically that random search is more efficient than grid search for hyper-parameter optimization of machine learning algorithms, and establish random search as a baseline against which adaptive (sequential) hyper-parameter optimization methods should be compared.

## Core methodology

### Problem formulation
- Learning algorithm A_λ with hyper-parameters λ ∈ Λ.
- Goal: minimize generalization error: λ* = argmin_λ E_{x~G_x}[L(x; A_λ(x_train))].
- In practice: minimize validation error Ψ(λ) = mean_{x∈X_valid} L(x; A_λ(X_train)).
- Hyper-parameter optimization ≈ minimization of response surface Ψ(λ) over Λ.

### Random search procedure
- Draw S independent trials λ^(1)...λ^(S) from a uniform distribution over Λ (or appropriate prior).
- Evaluate Ψ(λ) for each trial.
- Return λ^(i) with best validation performance.

### Key insight: Low effective dimensionality
- Ψ(λ) typically depends strongly on only a few hyper-parameters (low effective dimension).
- Different data sets have different important hyper-parameters.
- Grid search wastes exponential trials on unimportant dimensions; random search efficiently covers important subspaces.

### Performance estimation with model uncertainty
- Weighted average of test scores, weighted by probability that each trial is truly best given validation uncertainty.
- Weights w_s = P(Z^(s) < Z^(s') ∀ s'≠s) where Z^(i) ~ N(Ψ_valid(λ^(i)), Var_valid(λ^(i))).

## Key results

### Neural network experiments (7 hyper-parameters, no preprocessing)

| Data set | Grid search accuracy (avg 100 trials) | Random search accuracy (8 trials) |
|----------|---------------------------------------|-----------------------------------|
| mnist basic | ~2.5% test error | matched or better |
| mnist background images | ~45% | matched or better |
| mnist background random | ~40% | matched or better |
| mnist rotated | ~30% | matched or better |
| rectangles | ~1% test error | matched or better |
| rectangles images | ~25% | matched or better |
| convex | ~20% | matched or better |

- Random search with 8 trials matches or outperforms grid search with ~100 trials.
- With preprocessing considered (9 hyper-parameters), 64 random trials find better models than grid search.

### Deep Belief Network experiments (up to 32 hyper-parameters)
- Random search of 128 trials found:
  - Superior model on 1 data set (convex)
  - Statistically equal performance on 4 data sets
  - Inferior model on 3 data sets (compared to expert manual+grid search, avg 41 trials)
- 1-layer DBN random search found models at least as good as manual search in all cases.

### Gaussian process ARD analysis (neural networks, 7 hyper-parameters)
- Effective dimensionality varies by data set: 1–4 dimensions matter.
- Most important hyper-parameters vary across data sets:
  - Learning rate always important
  - Annealing rate important for rectangles images
  - L2 penalty important for convex, mnist rotated
  - Number of hidden units important for rectangles
- Correlation between low effective dimensionality and ease of optimization.

### Simulation: finding axis-aligned intervals (1% volume)

| Scenario | Grid best | Random expectation | Sobol |
|----------|-----------|--------------------|-------|
| 3D cube | competitive | good | slightly better |
| 3D rectangle (low effective dim) | poor | good | best |
| 5D cube | competitive | good | slightly better |
| 5D rectangle (low effective dim) | very poor | good | best |

- Latin hypercube sampling no better than random for search efficiency.
- Sobol sequence (low-discrepancy) offers small advantage (few %) for 100–300 trials.

## Practical recommendations

1. **Replace grid search with random search** for hyper-parameter optimization.
2. **Advantages of random search**:
   - Trials are i.i.d. — can be stopped anytime, added incrementally.
   - Asynchronous execution; failed trials can be ignored.
   - No need to pre-commit to grid resolution.
3. **For controlled experiments** (testing one hyper-parameter): randomize all others, reuse same set across conditions.
4. **Report uncertainty** in best model selection using weighted averaging (Equation 5).
5. **Baseline for future work**: random search should be compared against, not grid search.

## Limitations (explicit)
- Random search not as good as expert manual+grid search for DBNs (32 dimensions, small good regions).
- Sequential/adaptive optimization can overcome inefficiency where random search requires many trials.
- Low-discrepancy sequences (Sobol) not i.i.d. — harder to analyze, less practical.
- Requires careful choice of prior distribution over Λ (not discussed in depth).

## Conclusions
- Grid search is inefficient because hyper-parameter response surfaces have low effective dimensionality, but which dimensions matter varies by data set.
- Random search is more efficient, simpler to implement, and more practical than grid search.
- Should serve as baseline for evaluating adaptive hyper-parameter optimization algorithms.
