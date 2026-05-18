---
title: "Efficient Global Optimization of Expensive Black-Box Functions"
title_en: "Efficient Global Optimization of Expensive Black-Box Functions"
source_type: "article"
authors: ["Jones D. R.", "Schonlau M.", "Welch W. J."]
year: "1998"
source_link: "unknown (provided PDF: 56__jones98.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "efficient-global-optimization-expensive-functions-1998.md"
---

# Content source: Efficient Global Optimization of Expensive Black-Box Functions

## Source type
Peer-reviewed journal article (Journal of Global Optimization, Kluwer Academic Publishers, 1998).

## Authors affiliation
1. General Motors R&D Operations, Warren, MI, USA
2. National Institute of Statistical Sciences, Research Triangle Park, NC, USA
3. University of Waterloo, Ontario, Canada

## Objective
Introduce a response surface methodology (DACE — Design and Analysis of Computer Experiments) based on stochastic processes for modeling expensive black-box functions, and present an efficient global optimization algorithm (EGO) that balances local and global search using an expected improvement criterion with a credible stopping rule.

## Core methodology

### DACE stochastic process model
- Model: y(x⁽ⁱ⁾) = μ + ε(x⁽ⁱ⁾), where ε(x) is a Gaussian process with mean 0, variance σ², and correlation function:
  - Corr[ε(x⁽ⁱ⁾), ε(x⁽ʲ⁾)] = exp[-d(x⁽ⁱ⁾, x⁽ʲ⁾)]
  - d(x⁽ⁱ⁾, x⁽ʲ⁾) = Σₕ θₕ |xₕ⁽ⁱ⁾ - xₕ⁽ʲ⁾|^(pₕ), θₕ ≥ 0, pₕ ∈ [1,2]
- Parameters θₕ measure variable "activity" (importance); pₕ controls smoothness (2 = smooth, 1 = less smooth).
- Maximum likelihood estimation of μ, σ², θₕ, pₕ.

### Predictor (Best Linear Unbiased Predictor)
- ŷ(x*) = μ̂ + rᵀ R⁻¹ (y - 1μ̂)
- r = correlation vector between x* and sampled points.
- Predictor interpolates data (ŷ(x⁽ⁱ⁾) = y⁽ⁱ⁾).

### Prediction uncertainty (Mean Squared Error)
- s²(x*) = σ²[1 - rᵀR⁻¹r + (1 - 1ᵀR⁻¹r)² / (1ᵀR⁻¹1)]
- s(x*) = 0 at sampled points; increases away from data.

### Expected Improvement (EI) criterion
- Let f_min = current best function value. Model uncertainty at x as Y ~ N(ŷ(x), s²(x)).
- Improvement I = max(f_min - Y, 0)
- E[I(x)] = (f_min - ŷ)Φ((f_min - ŷ)/s) + s·φ((f_min - ŷ)/s)
- Properties: ∂E[I]/∂ŷ = -Φ(·) < 0, ∂E[I]/∂s = φ(·) > 0
- EI is larger when ŷ is lower (exploitation) and s is higher (exploration).

### EGO algorithm
1. Initial space-filling design (Latin hypercube, ≈10k points).
2. Fit DACE model, validate via cross-validation (standardized residuals in [-3,3]).
3. Apply log or inverse transformation if needed.
4. Maximize E[I(x)] using branch-and-bound (bounds on ŷ via nonconvex relaxation, on s² via convex relaxation).
5. If max E[I] < 1% of f_min, stop.
6. Else evaluate function at argmax E[I], update model, repeat.

## Key results (test functions)

| Test function | Dimensions | Initial points | Evaluations to stop (1% criterion) | Actual error at stop | Evaluations for 1% actual error |
|---------------|------------|----------------|-------------------------------------|----------------------|--------------------------------|
| Branin | 2 | 21 | 28 | 0.2% | 28 |
| Goldstein-Price | 2 | 21 | 32 | 0.1% | 32 |
| Hartman 3 | 3 | 33 | 34 | 1.7% | 35 |
| Hartman 6 | 6 | 65 | 84 | 1.9% | 121 |

### Computation times (Pentium II 266 MHz)
- Branin: 139 sec first iterate, subsequent faster
- Goldstein-Price: 6 sec first iterate
- Hartman 3: 40 sec first iterate
- Hartman 6: 135 sec first iterate, 262 sec last iterate

## Model validation diagnostics
- Cross-validation: leave out one point, predict based on remaining n-1 points.
- Standardized cross-validated residual = (y(x⁽ⁱ⁾) - ŷ₋ᵢ(x⁽ⁱ⁾)) / s₋ᵢ(x⁽ⁱ⁾)
- Should lie in [-3, +3] for valid model.
- Q-Q plot of standardized residuals vs normal quantiles.
- Goldstein-Price function required log transformation for valid model.

## Visualization techniques
- Variance decomposition into main effects and interactions (integrates out other variables).
- Main effect of variable x_h: a_h(x_h) = ∫ ... ∫ ŷ(x) dx_(≠h)
- Interaction effect: remainder after subtracting main effects.
- Total variance = Σ main effects + Σ interactions + higher-order terms.
- Enables identification of important variables (example: 36-variable IC problem → only 5 variables important).

## Key theoretical properties
- Predictor derived as value maximizing likelihood of augmented sample (pseudo-observation).
- Expected improvement monotonic in ŷ (decreasing) and s (increasing).
- Conjecture: EGO search points form dense subset of feasible region if θₕ > 0 and function continuous.

## Limitations (explicit)
- p_h fixed = 2 in implementation (bounding methods limited to this case).
- Ill-conditioning of correlation matrix R when points are close or function very smooth (mitigated via SVD).
- Branch-and-bound slows significantly for high dimensions (Hartman 6 required limited-memory version).
- Expected improvement criterion underestimates true potential gain (requires lower tolerance or multiple iterations).
- Noisy data extension not yet developed.
- Multi-fidelity extension mentioned as promising but not implemented.

## Practical recommendations
- Initial design: ~10k points (space-filling Latin hypercube).
- Use cross-validation to validate model before optimization.
- Transform response (log, inverse) if standardized residuals exceed ±3.
- Stop when max E[I] < 1% of current best value.
- For high dimensions (≥6), use limited-memory branch-and-bound.

## Conclusions
- DACE stochastic process models are highly effective for approximating expensive nonlinear, multimodal functions.
- Expected improvement criterion naturally balances exploration and exploitation.
- EGO provides a credible stopping rule based on statistical model.
- Response surface approach not only optimizes but also provides visualization and insight into input-output relationships.
