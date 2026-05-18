---
title: "The irace package: Iterated racing for automatic algorithm configuration"
title_en: "The irace package: Iterated racing for automatic algorithm configuration"
source_type: "article"
authors: ["López-Ibáñez M.", "Dubois-Lacoste J.", "Pérez Cáceres L.", "Birattari M.", "Stützle T."]
year: "2016"
source_link: "unknown (provided PDF: 61__1-s2.0-S2214716015300270-main.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "irace-iterated-racing-algorithm-configuration-2016.md"
---

# Content source: The irace package: Iterated racing for automatic algorithm configuration

## Source type
Peer-reviewed journal article (Operations Research Perspectives, Elsevier, 2016). Open access (CC BY).

## Authors affiliation
- University of Manchester, UK
- IRIDIA, Université Libre de Bruxelles (ULB), Belgium

## Objective
Present the irace package (implemented in R), which implements iterated racing procedures for automatic algorithm configuration, including the Iterated F-Race (I/F-Race) algorithm and several extensions: soft-restart mechanism, elitist racing, parallel evaluation, forbidden configurations, and truncated sampling distributions.

## Core methodology: Iterated racing

### Overview (three steps, repeated until budget exhausted)
1. **Sampling** new configurations according to a sampling distribution (updated each iteration).
2. **Selection** of best configurations via racing (sequential statistical testing).
3. **Update** sampling distribution to bias toward best configurations.

### Sampling distributions (parameter types)
- **Numerical (real/integer)**: Truncated normal distribution N(θ_z, (σ_j)²) within [X̲, X̄].
  - Mean = value from parent elite configuration θ_z
  - σ_j decreases each iteration: σ_j = σ_{j-1} · (1/N_new)^{1/N_param}
- **Categorical**: Discrete probability distribution, updated each iteration:
  - P^{j,z}(X_d = x_i) = P^{j-1,z}(X_d = x_i)·(1 - (j-1)/N_iter) + ΔP
  - ΔP = (j-1)/N_iter if x_i equals parent value, else 0
  - Maximum probability capped at 0.2^{1/N_param} (elitist variant) to maintain exploration.
- **Ordinal**: Treated as numerical (integers).

### Racing procedure
- Start with set of candidate configurations Θ.
- Evaluate configurations sequentially on instances (instance + random seed pairs).
- After T_first instances (default 5), perform statistical test (Friedman test by default, paired t-test alternative).
- Discard configurations statistically worse than at least one other.
- Repeat tests every T_each instances (default 1) until:
  - Budget exhausted
  - ≤ N_min configurations remain
  - T_max (default 2) consecutive tests without discarding (elitist variant after T_new + e instances)

### Soft-restart mechanism (avoid premature convergence)
- Detects when distance between two configurations = 0 (all parameters same after rounding).
- Partially reinitializes sampling distributions for affected elite configurations:
  - Categorical: p' = 0.9·p + 0.1·max(P), then normalize.
  - Numerical: σ brought back two iterations.
- Discards zero-distance configurations and resamples.

### Elitist iterated racing (preserves best configurations)
- Elite configurations from previous iterations are not discarded unless:
  - New configurations evaluated on at least e + T_new instances (e = instances seen by elite).
- Randomizes order of previously seen instances and prepends T_new new instances (default 1).
- Prevents loss of high-quality configurations due to partial information (see Fig. 8 example).

### Parallel evaluation
- Supports parallel execution across multiple cores (via R parallel) or computers (via MPI).
- Can submit each run as a job in cluster environments (SGE, PBS).

## Key results

### Comparison of irace vs elitist irace (three scenarios)

| Scenario | Homogeneity (Kendall W) | Statistical test | Observation |
|----------|------------------------|------------------|-------------|
| ACOTSP (TSP, ACO) | 0.98 (high) | Friedman | No significant difference |
| MOACO (multi-objective) | 0.99 (high) | Friedman | No significant difference |
| SPEAR (SAT solver) | 0.16 (low/heterogeneous) | t-test | No significant difference on average; elitist avoids worst runs |

**Key finding for heterogeneous scenarios**: Non-elitist irace lost winning configurations in 8 of 30 SPEAR runs (example in Fig. 8). Elitist variant prevents this loss.

### Effect of T_new (elitist) and T_first (non-elitist) on SPEAR (heterogeneous)

| T_new / T_first | Mean runtime on test set | Configurations sampled |
|----------------|-------------------------|------------------------|
| Default (1/5) | ~1000s | ~200 |
| Optimal (40-50) | ~200s | ~80-100 |
| Too large | ~300s+ | ↓ |

- Increasing T_new or T_first improves performance on heterogeneous scenarios by evaluating configurations on more instances before discarding.
- Too large reduces number of configurations sampled, worsening results.

### ACOTSP tuning results (11 parameters, 5000 runs budget)
- irace configurations significantly outperform ACOTSP default (Fig. 5).
- Elitist and non-elitist variants produce similar quality.

## Package features (irace)

### Input components
1. **Parameter space**: Table format (name, label, type, domain, condition). Types: integer, real, ordinal, categorical. Supports conditional parameters (dependency graph).
2. **Training instances**: File/directory of instance paths; randomized order; instance + random seed pairs for variance reduction.
3. **Configuration scenario**: Options (budget, targetRunner, statistical test, etc.)

### Output
- Best configurations printed as table and command-line parameters.
- Saves R dataset (irace.Rdata) with:
  - scenario, parameters, seeds matrix, allConfigurations, experiments matrix.
  - Can resume interrupted runs.

### Example applications (survey of irace usage)

| Application area | Examples |
|------------------|----------|
| Algorithm configuration | TSP with time windows, flow shop, graph coloring, bin packing, course timetabling, continuous optimization (CEC benchmarks) |
| Multi-objective optimization | MOACO framework, TP+PLS, multi-objective evolutionary algorithms |
| Anytime algorithms | SCIP MIP solver, ACO parameter variation strategies |
| Automatic design from grammar | Bin packing, permutation flowshop, hybrid local search |
| Machine learning | SVM tuning, survival data analysis, mlr package (vs random/grid search) |
| Robotics | AutoMoDe: automatic design of swarm robot controllers (outperforms human designer) |

## Parameter guidelines

| irace parameter | Description | Default |
|----------------|-------------|---------|
| maxExperiments (B) | Tuning budget (number of runs) | User-specified |
| mu | Instances before first test | 5 (T_first) |
| minNbSurvival (N_min) | Stop when ≤N_min configurations remain | 1 |
| firstTest (T_first) | Instances before first statistical test | 5 |
| eachTest (T_each) | Instances between subsequent tests | 1 |
| testType | Friedman (ranks) or t-test (means) | "friedman" |

### Practical recommendations
- **Homogeneous scenarios** (W close to 1): Use default settings; focus on sampling new configurations.
- **Heterogeneous scenarios** (W low): Increase T_new (elitist) or T_first (non-elitist) to 40-50.
- **Small tuning budget**: Default irace may not outperform random.
- **Conditional parameters**: Define dependency graph; irace handles automatically.

## Limitations (explicit)
- Primarily designed for minimizing computational cost as primary objective (unlike ParamILS/SMAC which dynamically cap runtimes).
- Default parameters assume sufficient budget for multiple iterations and candidate configurations.
- Computationally expensive runs (hours/days) difficult; alternatives: tuning on easier instances (Styles & Hoos) or scaling parameters (Mascia et al.)
- No automatic handling of parameter interactions beyond conditional dependencies.

## Comparison to related methods

| Method | Key features | Parameter types | Statistical test |
|--------|--------------|-----------------|------------------|
| ParamILS [41] | Iterated local search, adaptive capping | Categorical (discretized numerical) | Pairwise comparison |
| SMAC [43] | Model-based (random forests), surrogate | Mixed (categorical + numerical) | — |
| irace | Iterated racing, truncated sampling | Mixed (categorical, numerical, ordinal, conditional) | Friedman / t-test |
| CALIBRA [2] | Fractional factorial + local search | Numerical, ≤5 parameters | — |
| SPOT [12] | Surrogate (DACE/Kriging) | Numerical | — |

## Conclusions
- irace implements iterated racing for automatic algorithm configuration with support for mixed parameter types, conditional parameters, and parallel execution.
- Soft-restart prevents premature convergence; elitist variant preserves best configurations (critical for heterogeneous scenarios).
- Used successfully across many domains (optimization, machine learning, robotics).
- Open source (R package); no prior R knowledge required; available with user guide.
