---
title: "Derivative-Free Optimization of Expensive Functions with Computational Error Using Weighted Regression"
title_en: "Derivative-Free Optimization of Expensive Functions with Computational Error Using Weighted Regression"
source_type: "article"
authors: ["Custódio A. L.", "Scheinberg K.", "Vicente L. N."]
year: "2013"
source_link: "unknown (provided PDF: 66__Derivative-Free_Optimization_of_Expensive_Function.pdf)"
doi: "none (SIAM Journal on Optimization, likely DOI exists but not in file)"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "derivative-free-optimization-weighted-regression-2013.md"
---

# Content source: Derivative-Free Optimization of Expensive Functions with Computational Error Using Weighted Regression

## Source type
Peer-reviewed journal article (SIAM Journal on Optimization, circa 2013).

## Authors affiliation
- A. L. Custódio — (appears from reference [7])
- K. Scheinberg — Lehigh University? (not explicitly in provided pages)
- L. N. Vicente — University of Coimbra? (not explicitly in provided pages)

## Objective
Develop a derivative-free trust-region optimization algorithm that handles expensive functions with computational error (deterministic from discretization or stochastic from Monte Carlo) where error levels can vary. Extend CSV2 framework (Conn, Scheinberg, Vicente) to weighted regression to allow varying accuracy levels for different function evaluations.

## Core methodology

### Problem setting
- Function evaluations expensive (minutes to days), no derivatives available
- Function evaluations subject to computational error: f̄_i = f(yⁱ) + Eᵢ
- Error magnitude can be user-controlled (e.g., finer discretization, larger Monte Carlo sample)
- Goal: reduce number of function evaluations by performing more computation per iteration

### CSV2 trust-region framework (Conn, Scheinberg, Vicente)
- Quadratic model m_k approximates f on sample set Yᵏ
- Step sᵏ solves: min m_k(xᵏ + s) subject to ‖s‖ ≤ Δₖ
- Model improvement ensures m_k is κ-fully quadratic (error bounds proportional to Δ³, Δ², Δ)
- Algorithm converges to second-order stationary points under smoothness assumptions

### Weighted regression model construction
- Weighted least squares: minimize Σ wᵢ² (m(yⁱ) − f̄ᵢ)²
- Solution: α = (W M)⁺ W f̄, where M = matrix of basis functions φ(yⁱ)
- Basis φ: monomials {1, x₁, …, x_n, x₁²/2, x₁x₂, …, x_n²/2}
- Weights wᵢ positive; can account for varying error levels

### Weighted regression Lagrange polynomials
- ℓⱼ(x) = φ(x)ᵀ aⱼ, where aⱼ = (W M)⁺ W eⱼ
- Model m(x) = Σ f̄ᵢ ℓᵢ(x)

### Error analysis (Corollary 4.6)
For any x in convex set Ω containing Y, with f ∈ LC² (Lipschitz continuous Hessian):

|f(x) − m(x)| ≤ Σ (L/2 ‖yⁱ − x‖³ + |Eᵢ|) |ℓᵢ(x)|
‖∇f(x) − ∇m(x)‖ ≤ Σ (L/2 ‖yⁱ − x‖³ + |Eᵢ|) ‖∇ℓᵢ(x)‖
‖∇²f(x) − ∇²m(x)‖ ≤ Σ (L/2 ‖yⁱ − x‖³ + |Eᵢ|) ‖∇²ℓᵢ(x)‖

### Λ-poisedness definitions (weighted regression sense)
- Y is Λ-poised in B if max_{x∈B} max_i |ℓᵢ(x)| ≤ Λ
- Y is strongly Λ-poised in B if max_{x∈B} ‖ℓ(x)‖ ≤ (q₁/√p₁) Λ
- (q₁ = (n+1)(n+2)/2, dimension of quadratic polynomial space)

### Key theoretical result (Proposition 4.11)
If shifted/scaled set Ŷ is strongly Λ-poised in unweighted regression sense, then it is strongly cond(W)·θ·Λ-poised in weighted regression sense for constant θ independent of Ŷ, Λ, w.

→ Any model improvement algorithm for unweighted regression can be used for weighted regression if cond(W) bounded.

### Model improvement algorithm (MIA) for regression
1. Find Λ-poised subset via Gaussian elimination with threshold test (ξ_acc)
2. If subset found, keep it; otherwise add new point y_new within B(0; Δ̃) to create Λ-subpoised set
3. Remove points outside B(0; rΔ̃) where r ≥ 1 (scale factor)
4. Repeat until sample set is strongly Λ-poised

### Weighting scheme heuristic (Equation 6.2)
w_i ∝ 1 / √(C ‖yⁱ − y⁰‖⁶ + 1)

- Balances Taylor error (∝ ‖yⁱ − y⁰‖³) and computational error
- C = 100 used in experiments

## Key results

### Benchmark comparison (Moré & Wild test suite, 53 problems each)

**Smooth problems** (no noise):
- Weighted regression ≈ unweighted regression > interpolation
- NEWUOA (mature code) outperforms all; DFO similar to weighted regression

**Piecewise smooth (nondifferentiable) problems**:
- Weighted regression significantly better than interpolation and unweighted regression
- Weighted regression outperforms DFO and NEWUOA

**Deterministic noise problems**:
- Weighted regression slightly better than unweighted regression and interpolation
- Weighted regression outperforms DFO and NEWUOA

### Performance profiles (τ = 10⁻⁵ accuracy)

| Problem type | Weighted regression vs interpolation | Weighted regression vs DFO | Weighted regression vs NEWUOA |
|--------------|--------------------------------------|----------------------------|-------------------------------|
| Smooth | Slightly better | Similar | Worse (NEWUOA best) |
| Nondifferentiable | Significantly better | Better | Better |
| Noisy | Slightly better | Better | Better |

## Algorithm parameters
- Δ_max = 100, Δ₀ = 1
- η₀ = 10⁻⁶, η₁ = 0.5
- γ = 0.5, γ_inc = 2
- ε_c = 0.01, μ = 2, β = 0.5, ω = 0.5
- r = 3, ξ_acc = 10⁻⁴
- Weighted regression: C̄ = 100

## Limitations (explicit)
- Weighted regression requires O(n⁶) operations per iteration (interpolation can update models in O(n²) using Powell's methods)
- Not tested on stochastically noisy functions (would require multiple sampling, point removal strategies)
- Weighting scheme heuristic; better schemes possible with more rigorous analysis
- Assumes bounded condition number of weight matrix

## Conclusions
- Weighted regression can reduce function evaluations for expensive optimization with computational error
- Regression methods advantageous even without computational error because they keep more points close to trust region center
- Theory extends Λ-poisedness to weighted regression; any unweighted model improvement algorithm works if cond(W) bounded
- Weighted regression particularly beneficial for nondifferentiable and noisy problems
- Trade-off: more computation per iteration (O(n⁶)) for fewer function evaluations — worthwhile when function evaluations extremely expensive

## Practical recommendations
1. Use weighted regression when function evaluations have varying accuracy (e.g., adaptive discretization, Monte Carlo sample sizes)
2. Weighting scheme w_i ∝ 1/√(C‖yⁱ − y⁰‖⁶ + 1) with C ≈ 100 is a reasonable heuristic
3. For smooth problems without noise, NEWUOA remains state-of-the-art
4. For nondifferentiable or noisy problems, weighted regression outperforms interpolation and NEWUOA
