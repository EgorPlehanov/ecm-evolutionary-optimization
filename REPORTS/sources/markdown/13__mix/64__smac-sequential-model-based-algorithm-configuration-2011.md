---
title: "Sequential Model-based Optimization for General Algorithm Configuration"
title_en: "Sequential Model-based Optimization for General Algorithm Configuration"
source_type: "conference_slides"
authors: ["Hutter F.", "Hoos H. H.", "Leyton-Brown K."]
year: "2011"
source_link: "unknown (provided PDF: 64__11-LION5-SMAC-slides.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "smac-sequential-model-based-algorithm-configuration-2011.md"
---

# Content source: Sequential Model-based Optimization for General Algorithm Configuration

## Source type
Conference presentation slides (LION 5 — Learning and Intelligent Optimization, Rome, January 18, 2011).

## Authors affiliation
University of British Columbia, Canada.

## Objective
Present two new methods for general algorithm configuration: (1) ROAR (Random Online Aggressive Racing) — a simple baseline, and (2) SMAC (Sequential Model-based Algorithm Configuration) — using random forests to predict algorithm performance and guide configuration search.

## Core methodology

### Problem context
- Algorithm parameters: categorical (e.g., preprocessing, branching strategies), many parameters (CPLEX: 76 parameters)
- Goal: optimize performance on a set of problem instances
- Challenge: expensive evaluations (each run may take hours)

### ROAR (Random Online Aggressive Racing)
- Simple method: select configuration θ uniformly at random
- Compare θ to current incumbent θ* using aggressive racing
- Racing: few runs for poor θ, many runs for good θ
- Once confident enough: update θ* ← θ
- Aggressively rejects poor configurations (often after a single run)

### SMAC (Sequential Model-based Algorithm Configuration)

**Core idea**: Construct model to predict algorithm performance, use model to select promising configurations.

**Random Forest model**:
- Ensemble of regression trees
- Training: subsample data T times (with replacement), fit regression tree to each subsample
- Each internal node stores split criterion (parameter value threshold or categorical choice)
- Each leaf stores mean runtime of training examples reaching that leaf
- Prediction: aggregate across T trees → empirical mean and variance

**Extension to instance features**:
- Model g: Θ × ℝᵐ → ℝ (configuration + instance features → predicted runtime)
- Features characterize problem instances (e.g., graph properties for SAT)
- Allows predicting runtime for unseen (θ, instance) pairs

**Configuration selection**:
- Use model to predict performance across instances (e.g., average predicted runtime row)
- Select promising configuration θ
- Compare to incumbent using aggressive racing (same as ROAR)
- Update model with new data

## Key results

### Experimental setup
- 17 small configuration scenarios
- Algorithms: SAPS (local search SAT), SPEAR (tree search SAT), CPLEX (commercial MIP solver)
- 25 configuration runs per configurator per scenario, 5-hour budget each
- Evaluate final configuration on independent test set
- Total: over 1 year of CPU time

### Comparison results

| Configurator | Improvement over FocusedILS | Improvement over GGA |
|--------------|----------------------------|---------------------|
| SMAC | 0.93× – 2.25× (11/17 scenarios significantly better) | 1.01× – 2.76× (13/17 significantly better) |
| ROAR | Surprisingly effective baseline | — |

- SMAC never significantly worse than competitors.
- Performance depends on availability of instance features.

## Key insights

1. **Model-based configuration** (SMAC) outperforms iterated local search (FocusedILS) and genetic algorithms (GGA) on most scenarios.
2. **Simple random search with aggressive racing** (ROAR) is surprisingly effective baseline.
3. **Instance features** crucial for SMAC's performance — without them, model cannot generalize across instances.
4. **Aggressive racing** (early rejection of poor configs) is key component for both ROAR and SMAC.

## Comparison to other methods

| Method | Search strategy | Model | Parameter types | Instance features |
|--------|----------------|-------|-----------------|-------------------|
| F-Race | Racing | None (statistical testing) | Categorical (limited) | No |
| ParamILS (FocusedILS) | Iterated local search | None (direct comparison) | Categorical (discretized) | No |
| GGA | Genetic algorithm | None | Categorical | No |
| SPO | Sequential parameter opt | Gaussian process (kriging) | Numerical | No |
| **SMAC** | Model-based + racing | Random forest | Categorical, numerical | **Yes** |

## Practical recommendations
- Use ROAR as simple baseline (easy to implement, surprisingly effective).
- Use SMAC for better performance when instance features are available.
- Aggressive racing is effective for rejecting poor configurations early.
- Random forests handle categorical parameters naturally (no discretization needed).

## Limitations (explicit or implied)
- SMAC performance depends critically on availability of informative instance features.
- Random forest predictions may be less accurate than GPs for smooth numerical functions.
- Slides format lacks detailed algorithm pseudocode and theoretical analysis.
- No comparison to Bayesian optimization methods (GP-based) on same tasks.

## Future work directions (from slides)
1. Cut off poor runs early (adaptive capping, like ParamILS)
2. Handle censored data (timeouts) in models
3. Combine model-free (ROAR) and model-based (SMAC) methods
4. Use SMAC's models for scientific insight: parameter importance, parameter-instance interactions
5. Per-instance algorithm configuration (compute instance features, pick best configuration for each instance)

## Conclusions
- SMAC is a state-of-the-art configuration procedure, improving over FocusedILS and GGA.
- ROAR is a simple yet surprisingly effective baseline.
- Both methods use aggressive racing to efficiently compare configurations.
- Instance features are crucial for SMAC's performance.

## Relationship to other papers
- This is the conference presentation (slides) for the SMAC paper. The full paper likely appears in LION 5 proceedings or later as a journal article.
- SMAC was later extended and became part of the AutoML/AClib framework.
