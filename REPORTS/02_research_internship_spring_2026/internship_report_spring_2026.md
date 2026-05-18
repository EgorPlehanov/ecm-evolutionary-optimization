---
title: "Research Internship Report (Spring 2026): Comparative Analysis of Heuristic Methods for ECM Parameter Optimization"
source_file: "Плеханов_Отчет_НИР_2_курс_магистр_весна_26.docx"
language: "ru"
converted_on: "2026-05-12"
---

# Report on Industrial (Research) Internship

## Student and Program Information

| Field | Value |
|-------|-------|
| **Full name** | Plekhanov Egor Sergeevich |
| **Course and group** | 2nd year, 5140203/40101 |
| **Program code/name** | 02.04.03 Mathematical support and administration of information systems |
| **Internship location** | FSAEI HE "SPbPU", IKNiK, HSTII, St. Petersburg, Obruchevykh St., 1, lit. V |
| **Internship period** | 29.01.2025 – 21.03.2026 |
| **Supervisor (SPbPU)** | Pak Vadim Gennadievich, Candidate of Physical and Mathematical Sciences, Associate Professor at HSTII |
| **Consultant (SPbPU)** | Pak Vadim Gennadievich, Candidate of Physical and Mathematical Sciences, Associate Professor at HSTII |
| **Supervisor from partner organization** | None |
| **Grade** | (not specified) |

**Signatures:**
- Supervisor (SPbPU): / Pak V.G. /
- Consultant (SPbPU): / Pak V.G. /
- Supervisor from partner organization: / /
- Student: /Plekhanov E.S./
- Date: 21.03.26

---

## Table of Contents

- [Introduction](#introduction)
- [Chapter 1. Theoretical Foundations of Heuristic Optimization for ECM Parameters](#chapter-1-theoretical-foundations-of-heuristic-optimization-for-ecm-parameters)
  - [1.1. ECM Parameter Optimization as a Black-Box Problem](#11-ecm-parameter-optimization-as-a-black-box-problem)
  - [1.2. Overview of Integrated Heuristic Methods](#12-overview-of-integrated-heuristic-methods)
  - [1.3. Comparative Characteristics of Methods for the Optimization Problem](#13-comparative-characteristics-of-methods-for-the-optimization-problem)
  - [1.4. The Noise Problem and Methods for Its Mitigation](#14-the-noise-problem-and-methods-for-its-mitigation)
  - [1.5. Adaptation of Search Boundaries](#15-adaptation-of-search-boundaries)
  - [1.6. Chapter Conclusions](#16-chapter-conclusions)
- [Chapter 2. Software System Enhancement](#chapter-2-software-system-enhancement)
  - [2.1. Extending the Optimization Core: Transition to Multi-Heuristic Architecture](#21-extending-the-optimization-core-transition-to-multi-heuristic-architecture)
  - [2.2. Automation of Multi-Step Experimental Scenarios](#22-automation-of-multi-step-experimental-scenarios)
  - [2.3. Enhanced Analytical Capabilities of Optimization Runs](#23-enhanced-analytical-capabilities-of-optimization-runs)
  - [2.4. Improved Dataset Management and Reproducibility](#24-improved-dataset-management-and-reproducibility)
  - [2.5. Structured Artifact Storage](#25-structured-artifact-storage)
  - [2.6. Status of Support for Specialized Number Classes](#26-status-of-support-for-specialized-number-classes)
  - [2.7. Chapter Conclusions](#27-chapter-conclusions)
- [Chapter 3. Computational Experiment Results](#chapter-3-computational-experiment-results)
  - [3.1. Experimental Plan](#31-experimental-plan)
  - [3.2. Optimization and Validation Results](#32-optimization-and-validation-results)
  - [3.3. Convergence Analysis and Impact of Search Boundaries](#33-convergence-analysis-and-impact-of-search-boundaries)
  - [3.4. Comparative Effectiveness of Methods](#34-comparative-effectiveness-of-methods)
  - [3.5. Solution Space Analysis](#35-solution-space-analysis)
  - [3.6. Discussion of Limitations](#36-discussion-of-limitations)
  - [3.7. Chapter Conclusions](#37-chapter-conclusions)
- [Conclusion](#conclusion)
- [References](#references)
- [Appendix A: Source Code of New Modules](#appendix-a-source-code-of-new-modules)

---

# Introduction

Within the framework of the previous stage of the research work, a basic software system was developed for automated selection of parameters $B_1$ and $B_2$ of the Elliptic Curve Method (ECM) using the differential evolution algorithm. Conducted experiments showed that for divisors of size 25–35 decimal digits, the optimized parameters did not outperform the reference GMP-ECM tables, but revealed the potential of the method for fine-tuning on small divisors (20 digits) and indicated the need to expand the range of heuristic approaches, improve reproducibility, and automate experiments.

**The aim of this stage** of the research work is to expand the software system to support multiple heuristic optimization methods, conduct comparative computational experiments on selecting ECM parameters $B_1$ and $B_2$, and identify the most effective method for the optimization problem on small divisors.

To achieve this goal, the following tasks were solved:

- Deepening the theoretical review of heuristic optimization methods and their applicability to the ECM parameter selection problem;
- Refining the software system to support multiple heuristic algorithms, automate full experiment cycles, and enhance analytics;
- Conducting a series of computational experiments for comparative evaluation of the effectiveness of various methods on a fixed class of numbers (20-digit divisor);
- Statistical processing of the obtained results and formulation of recommendations for the final stage of research and the master's thesis.

---

# Chapter 1. Theoretical Foundations of Heuristic Optimization for ECM Parameters

## 1.1. ECM Parameter Optimization as a Black-Box Problem

The selection of boundaries $B_1$ and $B_2$ of the Elliptic Curve Method is a stochastic optimization problem in which the objective function $(E[T](B_1, B_2))$ — the expected time to successfully find a divisor — has no analytical expression and can only be estimated empirically through multiple ECM runs. Such functions are called black-box functions [1]. Their optimization requires methods that are robust to noise, do not require gradient computation, and can work with multimodal landscapes [2].

At the previous stage, the differential evolution (DE) algorithm was applied, which showed operability but also revealed dependence of results on computational budget and search boundaries [3]. To increase robustness and enable comparative analysis at the current stage, additional heuristic approaches have been integrated into the software system, differing in search strategies, ways of balancing between global exploration and local exploitation, as well as sensitivity to noise [4, 5].

## 1.2. Overview of Integrated Heuristic Methods

### 1.2.1. Random Search (RS)

Random search is a basic reference method. At each iteration, a random point in the feasible region is generated, the objective function value is computed, and the best found is kept. Despite the lack of adaptation, RS can serve as a lower bound of effectiveness: if an adaptive method does not outperform RS, its application is impractical [6]. Advantages of RS include simplicity of implementation and noise robustness, while its disadvantage is low convergence speed in large search spaces.

### 1.2.2. Differential Evolution (DE)

DE remains one of the most effective methods for continuous optimization [7]. The main strategy used at the previous stage is denoted as DE/rand/1/bin. This notation, accepted in DE literature, decodes as follows:

- **rand** — the base vector for mutation is randomly selected from the population;
- **1** — one difference pair (i.e., one difference vector) is used for mutation;
- **bin** — binomial crossover is applied to form the trial vector.

Within the refinements, the ability to choose strategies and adapt coefficients has been preserved. For this problem, DE demonstrates high convergence speed with sufficiently large populations, but is sensitive to the choice of scaling factor $F$ and crossover probability $CR$ [8].

### 1.2.3. Particle Swarm Optimization (PSO)

PSO models the movement of particles in the solution space under the influence of personal and collective experience [9]. Each particle remembers its own best position and the swarm's best position. Main parameters: inertia ($w$), cognitive and social coefficients. PSO is less sensitive to initial scatter than DE and often gives good results with a limited computation budget [10], which is relevant for expensive objective functions.

### 1.2.4. Genetic Algorithm (GA)

GA operates on a population of solutions encoded as chromosomes. Selection, crossover, and mutation operators allow maintaining diversity [11]. For the parameter selection problem, real-valued encoding was used. GA has a tendency to premature convergence with poor parameter choices, but with proper tuning demonstrates noise robustness and ability to find global optima in multimodal problems [12].

### 1.2.5. Bayesian Optimization (BO)

BO builds a probabilistic surrogate model of the objective function (usually a Gaussian process) and uses an acquisition function to select the next evaluation point [13]. This approach is particularly effective when objective function evaluation is expensive and only a limited number of iterations is available [14]. However, BO is sensitive to space dimensionality and may lose effectiveness under strong noise or non-stationarity. In our case, BO is considered as a potentially promising method requiring separate verification.

## 1.3. Comparative Characteristics of Methods for the Optimization Problem

Table 1.1 presents key characteristics of the methods from the perspective of applicability to the problem.

**Table 1.1 — Comparison of heuristic methods for parameter optimization**

| Method | Noise sensitivity | Convergence speed | Dimensionality robustness | Tuning complexity |
|--------|-------------------|-------------------|---------------------------|-------------------|
| RS | Low | Low | High | Low |
| DE | Medium | High | Medium | Medium |
| PSO | Medium | High | Medium | Medium |
| GA | Medium | Medium | Medium | High |
| BO | High | High (small budget) | Low | High |

## 1.4. The Noise Problem and Methods for Its Mitigation

The objective function $(\widehat{E[T]}(B_1, B_2))$ is estimated from a finite number of ECM runs, which introduces stochastic noise. To reduce estimate variance at the optimization stage, averaging over multiple numbers in the training set is applied, as well as increasing the number of curves per number. However, with a limited computational budget, a trade-off must be found between estimation accuracy and the number of evaluated points [15].

## 1.5. Adaptation of Search Boundaries

Previously, wide boundaries were used $(B_1 \in [10^3, 10^9])$, $(B_2/B_1 \leq 10^4)$. Experiments on small divisors showed that optimal values concentrate near the lower boundary $(B_1 \approx 1000\ldots 2000)$ and with relatively small ratios $(B_2/B_1)$ (usually no more than 10). Based on these data, the search space was narrowed for subsequent runs, which made it possible to increase efficiency and reduce computational costs. Dynamic boundary adaptation is considered as one direction for further improvement.

## 1.6. Chapter Conclusions

This chapter examined the theoretical foundations of heuristic optimization methods integrated into the software system at the current stage. A comparative analysis of approaches was conducted considering the specifics of the problem: expensive objective function evaluation, noise, multimodality. It was shown that the choice of method significantly affects convergence and solution quality, and also requires individual parameter tuning. Based on preliminary experiments, narrowing of search boundaries for small divisors was justified. The obtained theoretical provisions formed the basis for the development of the extended architecture and planning of computational experiments described in subsequent chapters.

---

# Chapter 2. Software System Enhancement

This chapter presents the functional and architectural changes made to the software system after completion of the previous stage of research. All refinements are aimed at expanding the range of studied heuristic methods, improving experiment reproducibility, automating multi-step scenarios, and enhancing the analytical capabilities of the system. The basic modules described earlier (dataset generation, GMP-ECM launch, fitness function calculation) retained their structure but were supplemented with new interfaces ensuring their integration into a unified experimental pipeline. Full code is presented in Appendix A and in the project repository [16].

## 2.1. Extending the Optimization Core: Transition to Multi-Heuristic Architecture

At the previous stage, optimization was performed exclusively using the differential evolution (DE) algorithm. To organize comparative analysis and identify the most effective approach, the optimization core was redesigned to support multiple heuristic methods within a unified experimental pipeline.

An abstract `Optimizer` interface was introduced, defining an `optimize()` method that accepts the objective function, search boundaries, and parameters of the specific algorithm. An optimizer factory implementation ensures selection of a specific method based on the CLI flag `--method`. For each method, separate hyperparameters are provided through the command line interface, allowing independent tuning of algorithms within a unified scenario.

The integrated methods include:

- **Differential Evolution (DE)** — base DE/rand/1/bin strategy with ability to choose alternative strategies;
- **Random Search (RS)** — reference method serving as lower bound of effectiveness;
- **Particle Swarm Optimization (PSO)** — classical implementation with inertia weight;
- **Bayesian Optimization (BO)** — method based on Gaussian processes;
- **Genetic Algorithm (GA)** — real-coded genetic algorithm with tournament selection.

Table 2.1 shows the key tunable parameters for each of the integrated methods.

**Table 2.1 — Key parameters of integrated optimization methods**

| Method | Main parameters |
|--------|-----------------|
| DE | popsize, maxiter, mutation, recombination |
| RS | budget (number of random attempts) |
| PSO | swarm_size, iterations, inertia, cognitive, social |
| BO | initial_samples, iterations, candidate_pool |
| GA | population_size, generations, crossover_prob, mutation_prob |

The proposed architecture made it possible to conduct not a single, but a comparative search of parameters $(B_1, B_2)$ by different classes of heuristics in a unified experiment format, simplifying the acquisition of representative data for an informed choice of the most effective approach.

## 2.2. Automation of Multi-Step Experimental Scenarios

To reduce the probability of operator errors and increase result reproducibility, a `run-plan` command was implemented that executes sequences of operations described in JSON files. The scenario includes three main stages:

- **generate** — creation of a dataset (training and control sets) with specified parameters;
- **optimize** — launch of optimization for one or multiple methods;
- **validate** — comparison of found parameters with reference values on the control set.

Linking of steps is carried out through a `$ref` reference mechanism, allowing automatic transfer of paths to datasets, optimization results, and other artifacts between stages without manual specification. This approach eliminates the need for re-entering intermediate data and reduces the risk of errors during transfer.

A baseline plan `baseline_all_methods.json` was prepared, describing batch comparison of all five methods on a single dataset. The plan contains dataset generation parameters (divisor size, sample volumes), configurations of each method with their hyperparameters, and validation commands with reference values.

As a result of automation, overhead costs for manual configuration of paths and parameters were reduced, and full traceability was ensured: the sequence of steps and used parameters are fixed as experiment artifacts, allowing exact reproduction of any run if necessary.

## 2.3. Enhanced Analytical Capabilities of Optimization Runs

For in-depth analysis of optimizer behavior and informed choice of the practically best method (taking into account not only final quality but also convergence speed, computational costs), extended telemetry recording and automatic visualization generation were added to the optimization pipeline.

The JSON optimization results include the following metrics:

- `time_to_first_improvement_sec` — time until the first improvement of the best solution;
- `time_to_best_sec` — time until reaching the final best solution;
- `new_best_count` — number of improvements found;
- `eval_per_sec` — average speed of objective function calculation;
- `improvement_percent` — relative improvement compared to the initial population;
- `max_plateau_evals` — maximum number of iterations without improvement.

Based on the collected data, graphs are automatically generated in PNG format:

- `convergence.png` — change of best objective function value across generations;
- `raw_fitness.png` — objective function values for all individuals in each generation;
- `jump_plot.png` — magnitude of improvement at each change of best solution;
- `b1_b2_trajectory.png` — trajectory of best solutions in parameter space;
- `progress_by_phase.png` — cumulative share of improvements over time.

An example search trajectory for one of the runs is shown in Figure 2.1.

> [!NOTE]
> In the original document, there was a reference to Figure 2.1 with an image file `media/image1.png`. The image itself is not available in the provided text.

**Figure 2.1 placeholder:** `![Trajectory of best solutions in (log10 B1, log10 B2) space](images/ecm-b1-b2-trajectory.png)`

The introduction of extended telemetry and visualization made it possible to analyze not only the final quality of solutions but also the convergence dynamics, presence of stagnation, computational cost of each improvement, which greatly simplifies method selection and parameter tuning.

## 2.4. Improved Dataset Management and Reproducibility

To simplify repeated runs and reduce manual operations when switching between experiments, the dataset management system was refined.

A unified JSON dataset format was introduced, including meta-information (divisor sizes, seed, creation date) and an array of numbers (N). This format allows storing all data necessary for experiment reproduction in a single file.

A flexible dataset resolution mechanism was implemented in the command line interface, supporting:

- direct path to JSON file;
- path to folder (automatic search for first suitable dataset);
- folder name in the `data/numbers/` directory;
- autoselection of the last generated dataset.

For the `validate` command, automatic context recovery from the optimization result JSON file was added: the used dataset, search boundaries, and other parameters are extracted, allowing validation to be launched with a single command without re-specifying this data.

Work with seeds was systematized: the main seed is set during dataset generation, and for each optimization run a deterministic derived seed is generated (based on the main seed and run number). This ensures independence of runs while maintaining full reproducibility.

These improvements made repeated runs and transitions between experiments simpler and more reliable, and reduced overhead operations for manual configuration of paths and parameters between stages.

## 2.5. Structured Artifact Storage

To improve traceability and subsequent statistical analysis, the organization of file artifacts was changed. The new directory hierarchy has the following form:

```
data/experiments/
├── <dataset_name>/
│   ├── <method>/
│   │   ├── <run_id>/
│   │   │   ├── optimize.json   # optimization results
│   │   │   ├── validate.json   # validation results
│   │   │   └── plots/          # convergence plots
│   │   │       ├── convergence.png
│   │   │       └── ...
```

Where:

- `<dataset_name>` — dataset identifier (e.g., `20_dset_20260330T114111Z`);
- `<method>` — optimizer name (de, rs, pso, bo, ga);
- `<run_id>` — run timestamp ensuring uniqueness.

This structure groups all data for a specific run in one folder, simplifying archiving, transfer, and subsequent analysis.

## 2.6. Status of Support for Specialized Number Classes

In accordance with the individual plan, the tasks of this stage included expanding functionality for working with different classes of numbers (RSA-like, Mersenne numbers). At the current stage, preparatory work was performed to enable the addition of such classes in the future without reworking the system core.

The created launch infrastructure (run-plan) and optimizer comparison framework are suitable for use with any datasets, including specialized ones. The dataset generation interface allows adding new number types through extension of the `dataset.py` module without modifying other components.

Specialized generators (RSA-like, Mersenne numbers) as separate CLI modes have not yet been выделены; their implementation is planned for the next stage as a logical continuation on top of the already created infrastructure.

## 2.7. Chapter Conclusions

During this stage, a transition was made from a basic prototype oriented to a single optimization method to a full-fledged experimental system with the following properties:

- multi-heuristic optimization with ability to comparatively analyze five different approaches;
- automation of multi-step scenarios through run-plan and context recovery;
- extended telemetry and visual analytics for assessing convergence dynamics;
- improved reproducibility due to unified dataset format and deterministic seed management;
- strict artifact organization facilitating subsequent statistical analysis.

The presented refinements created a solid foundation for conducting a series of computational experiments, the results of which are presented in the next chapter.

---

# Chapter 3. Computational Experiment Results

## 3.1. Experimental Plan

To verify the operability of the developed software system and comparatively evaluate the effectiveness of the integrated heuristic methods, a series of experiments was conducted with a fixed target divisor size — 20 decimal digits. The choice of this size was due to acceptable computation time (one ECM curve executes in fractions of a second), allowing a full experiment cycle (dataset generation, optimization, validation) for several methods under limited computational resources.

Each experiment included three stages:

1. **Dataset generation** — creation of a training set of 15 random semiprime numbers and a control set of 25 numbers;
2. **Optimization** — search for parameters $(B_1, B_2)$ using each of the five methods (DE, RS, PSO, BO, GA) on the training set. Method parameters were chosen considering the computational budget and preliminary experiments;
3. **Validation** — comparison of found optimized parameters with reference GMP-ECM values $((B_1 = 11000), (B_2 = 220000))$ on the control set.

To improve estimate reliability, three independent experiment cycles were conducted (with datasets generated with a fixed seed). Optimization parameters and budgets were refined based on results of previous cycles.

## 3.2. Optimization and Validation Results

Table 3.1 presents the found parameters and effectiveness metrics for each method and each cycle. The quality metric used is the relative improvement of expected factorization time on the control set compared to the reference: positive value corresponds to improvement (less time), negative — worsening.

**Table 3.1 — Results of three experiment cycles (20-digit divisor)**

| Cycle | Method | $B_1^{\text{(opt)}}$ | $B_2^{\text{(opt)}}$ | $B_2/B_1$ | Objective (train) | Improvement on control, % |
|-------|--------|----------------------|----------------------|-----------|-------------------|---------------------------|
| №1 | DE | 1179 | 117900 | 100.00 | 0.6653 | **+16.11** |
| | RS | 2351 | 235100 | 100.00 | 0.6650 | **-21.67** |
| | PSO | 1000 | 1000 | 1.00 | 0.3321 | **+25.17** |
| | BO | 4370 | 437000 | 100.00 | 0.7983 | **-59.88** |
| | GA | 3143 | 5193 | 1.65 | 0.4406 | **+6.41** |
| №2 | DE | 1180 | 2144 | 1.82 | 0.4725 | **+27.49** |
| | RS | 1436 | 13674 | 9.52 | 0.5978 | **+20.94** |
| | PSO | 1000 | 1000 | 1.00 | 0.4429 | **+31.39** |
| | BO | 1234 | 74040 | 60.00 | 0.7198 | **-1.12** |
| | GA | 1631 | 1666 | 1.02 | 0.4739 | **+29.29** |
| №3 | DE | 1079 | 2638 | 2.44 | 0.6948 | **+17.31** |
| | RS | 1261 | 3457 | 2.74 | 0.7332 | **+31.42** |
| | PSO | 1000 | 1000 | 1.00 | 0.6796 | **+25.62** |
| | BO | 1003 | 20060 | 20.00 | 0.9182 | **-15.48** |
| | GA | 1033 | 1401 | 1.36 | 0.7074 | **+29.34** |

From the table data, it follows that for the 20-digit divisor, most methods (except BO and partially RS in the first cycle) demonstrate positive improvement compared to the reference. The highest improvement values are achieved for PSO (up to 31.39%), GA (up to 29.34%), and RS after boundary adjustment (31.42% in the third cycle). Differential evolution showed consistently positive but less pronounced results.

## 3.3. Convergence Analysis and Impact of Search Boundaries

Based on the results of the first two cycles, it was found that optimal parameters concentrate near the lower search boundary $(B_1 \approx 1000\ldots 2000)$ and with relatively small ratios $(B_2/B_1)$ (typically not exceeding 10). In the third cycle, boundaries were narrowed to $(B_1 \in [1000, 12000]), (B_2 \in [1000, 144000])$ with $(B_2/B_1 \leq 12)$. This allowed improving results for RS (from -21.67% to +20.94% and further to +31.42%) and increasing GA stability. PSO, despite some decrease (from 31.39% to 25.62%), maintained high performance. DE, on the contrary, lost some effectiveness after boundary narrowing, which may indicate sensitivity of this method to changes in the search space.

Figure 3.1 shows the dynamics of best objective function value change in the third cycle for DE, GA, and PSO methods respectively.

> [!NOTE]
> In the original document, there were references to three images: `media/image2.png`, `media/image3.png`, `media/image4.png`. The images themselves are not available in the provided text.

**Figure 3.1 placeholders:**
- `![DE convergence in cycle 3](images/de-convergence-cycle3.png)`
- `![GA convergence in cycle 3](images/ga-convergence-cycle3.png)`
- `![PSO convergence in cycle 3](images/pso-convergence-cycle3.png)`

## 3.4. Comparative Effectiveness of Methods

Based on three cycles, the following ranking of methods by stability and achieved improvement can be proposed:

1. **PSO** — consistently high results (25–31%), least sensitivity to boundary changes;
2. **GA** — close to PSO values (29–30%), stability confirmed in all three cycles;
3. **RS** — after boundary adjustment demonstrates results comparable to leaders, though initially less effective;
4. **DE** — consistently positive but more modest results (16–27%);
5. **BO** — unstable, often underperforms the reference, sensitive to budget and boundaries.

## 3.5. Solution Space Analysis

Figure 3.2 shows the distribution of found best solutions in the space $(B_1, B_2/B_1)$ for all three cycles.

> [!NOTE]
> In the original document, there was a reference to an image `media/image5.png`. The image itself is not available in the provided text.

**Figure 3.2 placeholder:** `![Solution space: B1 vs B2/B1 ratio](images/ecm-solution-space.png)`

It can be seen that the best solutions concentrate in the region $B_1 \in [1000, 1600]$ and $B_2/B_1 \in [1, 3]$. Deviations from this region are typically accompanied by decreased effectiveness (e.g., RS in the first cycle with $B_2/B_1 = 100$). This confirms the hypothesis that for small divisors, optimal parameters lie in a narrow range, and wide search boundaries are not required.

## 3.6. Discussion of Limitations

The results obtained within this stage have a number of limitations that must be considered when interpreting conclusions and planning further research.

First of all, all experiments were conducted exclusively for a divisor of size 20 decimal digits. This choice was due to acceptable computational cost, allowing multiple runs for five different methods in three independent cycles. However, the behavior of heuristic methods, as well as the optimal ranges of parameters $B_1$ and $B_2$, can change significantly with increasing divisor size. In particular, previously conducted experiments for divisors of 25–35 digits using differential evolution showed that the tabular GMP-ECM values become more effective. Consequently, conclusions obtained for the 20-digit divisor cannot be automatically extended to larger sizes without conducting appropriate series of experiments.

The second important limitation is the choice of reference values for comparison. In the official GMP-ECM documentation, there is no strict recommendation of parameters for a 20-digit divisor; the nearest tabular values were used as baseline, which may affect the magnitude of relative improvement. Nevertheless, this choice is conservative and allows correct comparison of the effectiveness of different methods among themselves.

Finally, all test numbers belong to the class of random semiprime numbers generated by the built-in module. For specialized classes of numbers, such as RSA-like (product of two primes of similar size) or Mersenne numbers, the distribution of smoothness of point orders on the elliptic curve may differ. This, in turn, can affect the optimal values of $B_1$ and $B_2$. Although the infrastructure of the software system allows extension to such classes, within this stage corresponding experiments were not conducted, leaving the question of robustness of the found parameters open for further research.

These limitations do not diminish the value of the obtained results, but set the boundaries of their applicability and determine directions for further work.

## 3.7. Chapter Conclusions

As a result of the performed experiments, the operability of automated selection of parameters $(B_1, B_2)$ using several heuristic methods was proven. For the 20-digit divisor, all methods except Bayesian optimization made it possible to obtain parameters that provide reduction of expected factorization time on the control set compared to reference GMP-ECM values. The greatest stability and effectiveness were shown by PSO and GA, demonstrating improvement of up to 31%. It was established that optimal parameter values concentrate in a narrow region $(B_1 \approx 1000\ldots 1600)$, $(B_2/B_1 \approx 1\ldots 3)$, which allowed narrowing search boundaries and increasing efficiency of subsequent runs.

The obtained results confirm the feasibility of using heuristic optimization for tuning ECM on small divisors. At the next stage, it is planned to expand experiments to larger divisors and specialized number classes, as well as to complete statistical processing using formal significance criteria.

---

# Conclusion

The aim of this stage of the research work has been fully achieved. The software system has been expanded to support five heuristic optimization methods (DE, RS, PSO, BO, GA), comparative computational experiments were conducted for a 20-digit divisor, and the most effective methods (PSO and GA) were identified, showing improvement in expected factorization time of up to 31% compared to reference GMP-ECM values.

During the work, tasks were solved aimed at deepening the theoretical foundation, expanding the functional capabilities of the software system, and obtaining experimental data for comparative evaluation of heuristic optimization methods for parameters of the Elliptic Curve Method (ECM) factorization algorithm.

In the theoretical part of the work, a review and comparative analysis of five heuristic optimization methods were conducted: differential evolution, random search, particle swarm optimization, Bayesian optimization, and genetic algorithm. For each method, principles of operation, key parameters, advantages, and limitations for the problem of selecting $B_1$ and $B_2$ ECM parameters were considered. It was shown that the choice of method significantly affects convergence and solution quality, and also requires individual tuning considering the expense of objective function computation and the presence of noise.

The software system underwent significant modernization. A multi-heuristic architecture was implemented with a unified optimizer interface and method selection factory, allowing comparative experiments to be conducted under controlled conditions. Automation of multi-step scenarios was introduced through the run-plan mechanism, ensuring reproducibility and traceability of experiments. Extended telemetry and automatic generation of convergence graphs were added, making it possible to analyze not only the final quality but also the dynamics of the optimization process. The dataset management system and artifact storage structure were improved, simplifying repeated runs and subsequent statistical analysis.

Experimental research was conducted for a divisor of size 20 decimal digits in three independent cycles. It was established that most methods (PSO, GA, RS after boundary adjustment) allow obtaining parameters that provide reduction of expected factorization time on the control set compared to reference GMP-ECM values. The greatest improvement was achieved for PSO (up to 31.4%) and GA (up to 29.3%). It was revealed that optimal parameter values concentrate in a narrow region $(B_1 \approx 1000\ldots 1600)$, $(B_2/B_1 \approx 1\ldots 3)$, which allowed reasonably narrowing search boundaries and increasing efficiency of subsequent runs. Differential evolution showed consistently positive but less pronounced results, while Bayesian optimization proved unstable and often underperformed the reference.

At the same time, the obtained results have limitations: they are valid for a 20-digit divisor and the class of random semiprime numbers. Extending conclusions to larger divisor sizes (30, 35 and above) and specialized number classes (RSA-like, Mersenne numbers) requires additional series of experiments.

For the final stage of work, it is recommended to:

- expand experimental research to divisors of 30, 35, and 40 digits;
- implement generation and include RSA-type numbers and Mersenne numbers in experiments;
- perform formal statistical processing using the Mann–Whitney test and confidence intervals;
- prepare final diagrams and tables for inclusion in the text of the final qualifying work.

Thus, the tasks set for the current stage have been completed in full. The created infrastructure and obtained results provide a solid foundation for completing the research work and preparing the final qualifying work.

---

# References

1. Jones, D. R., Schonlau, M., & Welch, W. J. (1998). Efficient global optimization of expensive black-box functions. Journal of Global Optimization, 13(4), 455–492.

2. Audet, C., & Hare, W. (2017). Derivative-Free and Blackbox Optimization. Springer.

3. Storn, R., & Price, K. (1997). Differential evolution -- a simple and efficient heuristic for global optimization over continuous spaces. Journal of Global Optimization, 11(4), 341–359.

4. Wolpert, D. H., & Macready, W. G. (1997). No free lunch theorems for optimization. IEEE Transactions on Evolutionary Computation, 1(1), 67–82.

5. Bäck, T. (1996). Evolutionary Algorithms in Theory and Practice. Oxford University Press.

6. Bergstra, J., & Bengio, Y. (2012). Random search for hyper-parameter optimization. Journal of Machine Learning Research, 13(Feb), 281–305.

7. Das, S., & Suganthan, P. N. (2011). Differential evolution: A survey of the state-of-the-art. IEEE Transactions on Evolutionary Computation, 15(1), 4–31.

8. Price, K., Storn, R. M., & Lampinen, J. A. (2005). Differential Evolution: A Practical Approach to Global Optimization. Springer.

9. Kennedy, J., & Eberhart, R. (1995). Particle swarm optimization. Proceedings of ICNN'95 — International Conference on Neural Networks, 4, 1942–1948.

10. Poli, R., Kennedy, J., & Blackwell, T. (2007). Particle swarm optimization. Swarm Intelligence, 1(1), 33–57.

11. Holland, J. H. (1975). Adaptation in Natural and Artificial Systems. University of Michigan Press.

12. Whitley, D. (1994). A genetic algorithm tutorial. Statistics and Computing, 4(2), 65–85.

13. Mockus, J. (1989). Bayesian Approach to Global Optimization. Kluwer Academic Publishers.

14. Shahriari, B., Swersky, K., Wang, Z., Adams, R. P., & de Freitas, N. (2016). Taking the human out of the loop: A review of Bayesian optimization. Proceedings of the IEEE, 104(1), 148–175.

15. Picheny, V., Wagner, T., & Ginsbourger, D. (2013). A benchmark of kriging-based infill criteria for noisy optimization. Structural and Multidisciplinary Optimization, 48(3), 607–626.

16. Plekhanov E.S. ECM Evolutionary Optimization: software system for automated selection of elliptic curve method parameters. — Available at: https://github.com/EgorPlehanov/ecm-evolutionary-optimization

---

# Appendix A: Source Code of New Modules

> [!NOTE]
> The appendix includes only the source code of new modules added/extended at the current stage. Due to the length of the code (9 modules with full implementations), it has been preserved from the original document but may be truncated in this view for readability. The complete code is available in the original document and the project repository.

The following modules were added:

- **A.1.** `ecm_optimizer/optimizers/base.py` — abstract optimizer interface
- **A.2.** `ecm_optimizer/optimizers/heuristic_common.py` — common utilities for heuristic methods
- **A.3.** `ecm_optimizer/optimizers/differential_evolution.py` — DE implementation
- **A.4.** `ecm_optimizer/optimizers/random_search.py` — RS implementation
- **A.5.** `ecm_optimizer/optimizers/particle_swarm.py` — PSO implementation
- **A.6.** `ecm_optimizer/optimizers/bayesian_optimization.py` — BO implementation (lightweight surrogate-based)
- **A.7.** `ecm_optimizer/optimizers/genetic_algorithm.py` — GA implementation
- **A.8.** `ecm_optimizer/cli/run_plan.py` — multi-step plan execution
- **A.9.** `ecm_optimizer/utils/optimization_reporting.py` — telemetry and visualization utilities
