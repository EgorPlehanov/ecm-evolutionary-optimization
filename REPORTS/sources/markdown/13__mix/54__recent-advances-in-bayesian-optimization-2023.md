---
title: "Recent Advances in Bayesian Optimization"
title_en: "Recent Advances in Bayesian Optimization"
source_type: "article"
authors: ["Wang X.", "Jin Y.", "Schmitt S.", "Olhofer M."]
year: "2023"
source_link: "https://doi.org/10.1145/3582078"
doi: "10.1145/3582078"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "recent-advances-in-bayesian-optimization-2023.md"
---

# Content source: Recent Advances in Bayesian Optimization

## Source type
Peer-reviewed survey article (ACM Computing Surveys, Vol. 55, No. 13s, Article 287).

## Authors affiliation
- Xilu Wang, Yaochu Jin — Bielefeld University, Germany
- Sebastian Schmitt, Markus Olhofer — Honda Research Institute Europe GmbH, Germany

## Objective
Provide a comprehensive and updated survey of recent advances in Bayesian optimization (BO) based on Gaussian processes, covering nine main research directions, and identify open challenges and future research directions including heterogeneity, privacy preservation, and fairness in distributed and federated optimization.

## Core methodology (BO fundamentals)

### Gaussian Process surrogate
- Characterized by prior mean μ(·) and covariance/kernel function κ(·,·).
- Kernel examples: squared exponential (SE), Matérn.
- Hyperparameters (length scale ℓ, signal variance σ_f, noise variance σ_ε) inferred by maximizing log marginal likelihood.

### Acquisition Functions (AFs)
| AF | Formula | Key property |
|----|---------|---------------|
| Probability of Improvement (PI) | PI(x) = Φ((μ(x)−f*)/σ(x)) | Earliest AF (Kushner 1964) |
| Expected Improvement (EI) | EI(x) = (μ−f*)Φ((μ−f*)/σ) + σ·φ((μ−f*)/σ) | Most popular (Mockus 1975) |
| Upper Confidence Bound (UCB) | UCB(x) = μ(x) + β·σ(x) | Bandit-inspired |
| Knowledge Gradient (KG) | KG(x) = E_n[max μ_{n+1} − max μ_n] | Maximizes expected incremental value |
| Entropy Search (ES) / PES | Mutual information I((x,y); x* | D_n) | Information-theoretic |
| Max-Value Entropy Search (MES) | I((x,y); y* | D_n) | Computationally simpler |

## Nine categories of BO advances

### 1. High-Dimensional Optimization
- **Challenge**: GP-based BO performs poorly beyond 10–20 dimensions.
- **Approaches**:
  - Variable selection (ARD length scales, sensitivity analysis)
  - Linear/non-linear embedding (REMBO, VAE-based, geometry-aware BO)
  - Additive structure (Add-GP-UCB, MCMC for structure learning)
  - Local modeling (TuRBO, ensemble BO)
- **Open issues**: Learning latent space effectively; combinatorial high-dimensional BO; high-dimensional multi-output BO.

### 2. Combinatorial Optimization
- **Challenge**: Discrete, categorical, graph-structured inputs incompatible with standard GP kernels.
- **Approaches**:
  - Inherently discrete models (random forests, tree-structured Parzen estimators, BOCS)
  - Kernels with discrete distance measures (Hamming distance, graph kernels, COMBO)
  - Mixed search spaces (product kernels, heterogeneous kernels)
- **Open issues**: Combinatorial explosion; scalability; constraint satisfaction.

### 3. Noisy and Robust Optimization
- **Output noise**: Augmented EI, expected quantile improvement (EQI), approximate KG, PES, TS.
- **Outliers**: Robust GPs with Student-t likelihood.
- **Input noise/corruption**: Noisy-input GP (NIGP) via Taylor expansion; unscented EI; probabilistic vs worst-case robust optimization.
- **Open issues**: Adversarial corruptions; robustness in batch/bandit settings.

### 4. Expensive Constrained Optimization (ECOP)
- **Probability of feasibility**: Constrained EI (cEI) = EI × Pr(constraints satisfied).
- **Expected volume reduction**: Stepwise uncertainty reduction (SUR), PES for constrained problems, MES with constraints.
- **Multi-step look-ahead**: Rollout, 2-OPT-C.
- **Surrogate-assisted constraint handling**: MOEAs optimizing objectives + constraints simultaneously.
- **Open issues**: Highly constrained problems with few feasible samples; user preferences as constraints.

### 5. Multi-Objective Optimization (MOP)
- **BO + MOEA**:
  - EBO: BO framework, AF optimized by MOEA (ParEGO, MOEA/D-EGO)
  - BEO: MOEA framework, AF as infill criterion (K-RVEA, Multi-EGO)
- **Performance indicator-based AFs**:
  - Expected Hypervolume Improvement (EHVI) — most popular; computationally intensive.
  - Expected Euclidean distance improvement (EEuI), maximin distance improvement.
- **Information-theoretic AFs**: PESMO, MESMO.
- **Open issues**: High-dimensional MOPs/MaOPs; balancing exploration/exploitation for PF.

### 6. Multi-Task Optimization (MTO)
- **Goal**: Optimize multiple related tasks simultaneously via knowledge transfer.
- **Multi-task GP**: Linear Model of Coregionalization (LMC), intrinsic coregionalization model, Kronecker product kernel.
- **AFs**: Cost-aware ES, TS for tasks and actions.
- **Open issues**: Computational complexity (O(K³n³)); effective surrogate models; simultaneous optimization of all tasks.

### 7. Multi-Fidelity Optimization (MFO)
- **Goal**: Use cheaper low-fidelity evaluations to accelerate high-fidelity optimization.
- **Multi-fidelity models**: Co-Kriging (autoregressive: y_H = ρ·y_L + δ), recursive Co-Kriging, deep GP, convolved GP.
- **AFs**: Augmented EI, MF-GP-UCB, MES-MFO.
- **Open issues**: Linear correlation assumption; different search spaces across fidelities; continuous fidelity setting; MOPs and robust optimization.

### 8. Transfer/Meta Learning
- **Goal**: Leverage knowledge from source tasks to avoid "cold start" in target task.
- **Approaches**:
  - Hierarchical models (ranking surrogates, per-dataset normalization)
  - Multi-task GP with modified positive semi-definite matrix
  - Weighted combination of GPs (product of GP experts, transfer AF)
- **Open issues**: Negative transfer; heterogeneous search spaces; data privacy.

### 9. Parallel/Batch BO
- **Goal**: Select multiple query points per iteration for parallel computing.
- **Extensions of AFs**:
  - q-EI (Kriging believer, constant liar)
  - Parallel GP-UCB, parallel PES, parallel KG
  - Thompson sampling (inherently parallel via multiple function draws)
- **Problem reformulation**: Weighted k-means clustering, local penalization, multi-start optimization, MOEA-based batch selection.
- **Open issues**: Avoiding redundancy; scalability to batch size; asynchronous settings.

## Challenges and future directions (detailed)

| Direction | Key issues |
|-----------|------------|
| Distributed BO | Tradeoff convergence rate vs communication cost; asynchronous settings; complex networks |
| Federated BO | GP approximation (random Fourier features); privacy (differential privacy); TS performance |
| Dynamic optimization | Time-varying objective functions; resetting vs weighted GP; transfer learning from previous runs |
| Heterogeneous evaluations | Cost-aware BO (EI per second); interleaving schemes; domain adaptation for objectives with different costs |
| Algorithmic fairness | FairBO (constrained BO); fair regret; measuring and mitigating bias |
| Non-stationary optimization | Non-stationary kernels; deep GPs; input warping |
| Negative transfer | Defining and detecting negative transfer; similarity criteria; adaptive transfer |

## Key quantitative results (empirical comparisons)

- **High-D BO**: REMBO and variants successfully optimize problems with D~1000 using low-dimensional embeddings (d~10).
- **EHVI computation**: Number of interval boxes scales exponentially with number of Pareto solutions and objectives — computationally intensive for >3 objectives.
- **Multi-task GP complexity**: O(K³n³) — Kronecker structure can reduce to O(K³ + n³) in special cases.
- **Batch BO**: q-EI with Kriging believer achieves near-linear speedup in batch size for synthetic functions.

## Limitations (explicit from source)
- No systematic empirical comparison of all nine categories — conceptual/qualitative comparison only.
- Survey focuses on GP-based BO; alternatives (BNN, random forests) mentioned but not deeply covered.
- Theoretical convergence proofs often require modifications (e.g., Gaussian mutation) not present in standard BO.
- Many advanced BO methods (especially federated, fairness, dynamic) are in early stages with few existing algorithms.

## Practical conclusions
1. For high-D problems, start with REMBO (random embedding) or additive models before trying complex non-linear embeddings.
2. For constrained optimization, cEI (probability of feasibility × EI) is the simplest and often effective baseline.
3. For multi-objective optimization with <3 objectives, EHVI is recommended despite computational cost; for >3 objectives, consider ParEGO or MESMO.
4. For multi-fidelity, Co-Kriging with augmented EI is a mature, widely used approach.
5. Parallel BO with q-EI and Kriging believer is a practical choice for batch sizes ≤10.
6. Negative transfer risk increases when source-target task similarity is low — use similarity metrics before transfer.
