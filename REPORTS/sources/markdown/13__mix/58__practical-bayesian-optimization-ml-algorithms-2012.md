---
title: "Practical Bayesian Optimization of Machine Learning Algorithms"
title_en: "Practical Bayesian Optimization of Machine Learning Algorithms"
source_type: "conference"
authors: ["Snoek J.", "Larochelle H.", "Adams R. P."]
year: "2012"
source_link: "unknown (provided PDF: 58__NIPS-2012-practical-bayesian-optimization-of-machine-learning-algorithms-Paper.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "practical-bayesian-optimization-ml-algorithms-2012.md"
---

# Content source: Practical Bayesian Optimization of Machine Learning Algorithms

## Source type
Peer-reviewed conference paper (NIPS 2012 — Neural Information Processing Systems).

## Authors affiliation
- Jasper Snoek — University of Toronto, Canada
- Hugo Larochelle — University of Sherbrooke, Canada
- Ryan P. Adams — Harvard University, USA

## Objective
Present practical Bayesian optimization methods for hyperparameter tuning of machine learning algorithms, addressing three key limitations: (1) appropriate covariance function and hyperparameter treatment, (2) variable evaluation time/cost, and (3) parallel experimentation on multi-core systems.

## Core methodology

### Gaussian Process surrogate
- **Covariance function**: ARD Matérn 5/2 kernel (not squared exponential)
  - K_M52(x,x') = θ₀ (1 + √(5r²) + (5/3)r²) exp(-√(5r²))
  - r²(x,x') = Σ_d (x_d − x'_d)² / θ_d²
  - **Rationale**: Squared exponential assumes unrealistic smoothness; Matérn 5/2 gives twice-differentiable functions (compatible with quasi-Newton assumptions).

### Fully Bayesian treatment of GP hyperparameters
- Instead of point estimate via marginal likelihood maximization, integrate over hyperparameters:
  - â(x; {x_n,y_n}) = ∫ a(x; {x_n,y_n}, θ) p(θ | {x_n,y_n}) dθ
- Monte Carlo estimate using slice sampling (Murray & Adams, 2010)
- **Rationale**: Accounts for uncertainty in length scales, covariance amplitude, noise.

### Acquisition function: Expected Improvement (EI)
- a_EI(x) = σ(x)(γ(x)Φ(γ(x)) + φ(γ(x)))
- γ(x) = (f(x_best) − μ(x)) / σ(x)
- **Why EI over PI or UCB?**: No tuning parameter; better-behaved than PI.

### Cost-aware optimization: Expected Improvement per Second
- Model log cost c(x) with independent GP
- a_EI_per_sec(x) = a_EI(x) / E[exp(μ_c(x) + σ_c²(x)/2)]
- **Rationale**: Optimizes wall-clock time, not just number of evaluations.

### Parallel Bayesian optimization via Monte Carlo acquisition
- J pending evaluations at {xⱼ}
- Compute expected acquisition under all possible outcomes:
  - â(x) = ∫ a(x; {x_n,y_n}, θ, {xⱼ,yⱼ}) p({yⱼ} | {xⱼ}, {x_n,y_n}) dy₁...dyⱼ
- Sample from J-dimensional Gaussian distribution (mean and covariance from GP)
- **Rationale**: Allows sequential decision-making while experiments run in parallel.

## Key results

### Branin-Hoo (2D benchmark)
- GP EI MCMC (marginalized hyperparameters) finds minimum in ~15 evaluations
- GP EI Opt (point estimate) requires ~30 evaluations
- Tree Parzen Algorithm (TPA) requires ~40 evaluations

### Logistic regression on MNIST (4 hyperparameters)
| Method | Evaluations to optimum | Wall-clock time |
|--------|------------------------|-----------------|
| GP EI MCMC | ~20 | slower in time |
| GP EI per second | ~35 | faster in wall time |
| Random search | ~60 | — |

### Online LDA (3 hyperparameters, 5-10 hours per eval)
- Grid search: 288 evaluations (60-120 processor days)
- GP EI MCMC finds optimum in ~15 evaluations
- 3× parallel GP EI MCMC: finds optimum faster in wall time
- **Key result**: Found better perplexity than grid search optimum (Figure 4c)

### Protein motif finding with M³E (structured SVM, 3 hyperparameters)
- Grid search: 1,400 evaluations
- GP EI MCMC: ~40 evaluations
- GP EI per second: finds better parameters faster by learning to use loose tolerance early
- **Covariance comparison**: Matérn 5/2 significantly outperforms squared exponential

### Convolutional neural networks on CIFAR-10 (9 hyperparameters)
- Expert-tuned result: ~18% test error (state of the art at time)
- GP EI MCMC result: **14.98% test error** (3% better than expert)
- With data augmentation: 9.5% test error (vs 11% state of the art)
- **First time Bayesian optimization surpassed human expert on competitive deep learning benchmark**

## Implementation details
- Gradient-based search with multiple restarts for optimizing acquisition function
- Code made publicly available at http://www.cs.toronto.edu/~jasper/software.html
- Slice sampling for GP hyperparameter posterior

## Limitations (explicit or implied)
- Independence assumption between objective and cost functions (could be improved with multi-task learning)
- Cubic complexity O(N³) in number of observations
- Parallel acquisition via Monte Carlo requires sampling from J-dimensional Gaussian (J = number of pending evaluations)
- Cost modeling requires specifying cost function (runtime, money, etc.)

## Practical recommendations
1. **Use Matérn 5/2 kernel** (not squared exponential) for hyperparameter optimization
2. **Marginalize over GP hyperparameters** via MCMC (slice sampling) rather than point estimation
3. **Use expected improvement per second** when evaluation times vary significantly
4. **Use Monte Carlo acquisition for parallelism** when multiple cores/machines available
5. **Focus on EI** over PI or UCB (no tuning parameters)

## Comparison to prior work
- Bergstra et al. (2011): Tree Parzen Algorithm — GP EI MCMC outperforms on Branin-Hoo and logistic regression
- Hutter et al. (2011): SMAC (random forests) — different problem class (discrete/config)
- Jones et al. (1998): EGO — point estimate of GP hyperparameters, no cost or parallelization

## Conclusions
- Fully Bayesian treatment of GP hyperparameters improves optimization efficiency
- Cost-aware acquisition optimizes wall-clock time
- Monte Carlo parallelization enables multi-core Bayesian optimization
- Surpasses human expert on CIFAR-10 convolutional network tuning
