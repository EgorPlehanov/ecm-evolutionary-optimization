---
title: "Technological (Project-Technological) Internship Report – Spring 2026: HPC Adaptation and Large-Scale ECM Parameter Optimization"
source_file: "Плеханов_Отчет_Техн_практ_2_курс_магистр_весна_26.docx"
language: "ru"
converted_on: "2026-05-12"
---

# Report on Industrial (Technological/Project-Technological) Internship

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
- [Chapter 1. Adaptation of the Software System for Operation in the HPC Environment](#chapter-1-adaptation-of-the-software-system-for-operation-in-the-hpc-environment)
  - [1.1. Requirements for Cluster Execution](#11-requirements-for-cluster-execution)
  - [1.2. JSON Plan as a Unified Experiment Scenario](#12-json-plan-as-a-unified-experiment-scenario)
  - [1.3. SLURM Scripts and DAG Orchestration for Parallel Execution](#13-slurm-scripts-and-dag-orchestration-for-parallel-execution)
  - [1.4. Environment Setup and Dependency Verification](#14-environment-setup-and-dependency-verification)
  - [1.5. Chapter Conclusion](#15-chapter-conclusion)
- [Chapter 2. Computational Experiment Methodology](#chapter-2-computational-experiment-methodology)
  - [2.1. Dataset Generation Parameters](#21-dataset-generation-parameters)
  - [2.2. Search Space and Objective Function](#22-search-space-and-objective-function)
  - [2.3. Budgets and Hyperparameters of Optimization Methods](#23-budgets-and-hyperparameters-of-optimization-methods)
  - [2.4. Evaluation and Validation Parameters](#24-evaluation-and-validation-parameters)
  - [2.5. Reference Values for Comparison](#25-reference-values-for-comparison)
  - [2.6. Computational Process Organization](#26-computational-process-organization)
  - [2.7. Metrics and Calculation Method](#27-metrics-and-calculation-method)
- [Chapter 3. Computational Experiment Results](#chapter-3-computational-experiment-results)
  - [3.1. Comparison of Found Parameters with Reference](#31-comparison-of-found-parameters-with-reference)
  - [3.2. Optimization Dynamics and Search Geometry](#32-optimization-dynamics-and-search-geometry)
  - [3.3. Comparative Effectiveness of Methods](#33-comparative-effectiveness-of-methods)
  - [3.4. Chapter Conclusions](#34-chapter-conclusions)
- [Conclusion](#conclusion)
- [References](#references)
- [Appendix A: JSON Experiment Plan](#appendix-a-json-experiment-plan)
- [Appendix B: SLURM Scripts for Cluster Execution](#appendix-b-slurm-scripts-for-cluster-execution)

---

# Introduction

This report describes the work performed during the technological internship and is devoted to the adaptation of the software system for automated parameter selection of the Elliptic Curve Method (ECM) factorization algorithm to the computing environment of the Supercomputer Center of Peter the Great St. Petersburg Polytechnic University, as well as conducting resource-intensive computational experiments on the "Polytechnik – RSK Tornado" cluster. The previous stage of research work made it possible to create a multi-heuristic optimization core that included five methods: Bayesian optimization (BO), differential evolution (DE), random search (RS), particle swarm optimization (PSO), and genetic algorithm (GA). However, until now all experiments were conducted in a local environment with limited computational budget.

**The aim of the technological internship** was to transfer the computational pipeline to supercomputer resources, conduct a full-scale comparative experiment for a 20-digit divisor, and subsequent analysis of the effectiveness of each of the five methods. The report describes the completed stages: preparation of SLURM scripts and environment setup, parameters of the high-budget experiment, obtained metrics, their interpretation, as well as recommendations for further use of the methods. All computational results were obtained using the resources of the Supercomputer Center of Peter the Great St. Petersburg Polytechnic University (www.spbstu.ru), for which the author expresses gratitude to the center's staff.

---

# Chapter 1. Adaptation of the Software System for Operation in the HPC Environment

## 1.1. Requirements for Cluster Execution

The primary task of the technological internship was to adapt the existing software system to work in the supercomputer batch environment. The "Polytechnik – RSK Tornado" cluster operates under the SLURM queue management system and provides users with access to compute nodes with two Intel Xeon E5-2697 v3 processors (total 28 cores per node) and 64 GB of RAM. For correct execution of the multi-step experiment, it was necessary to ensure environment reproducibility, automatic result copying between steps, and efficient use of allocated cores. The complete project code is available in the repository [1].

## 1.2. JSON Plan as a Unified Experiment Scenario

The foundation of the computational pipeline became the JSON plan `full_all_methods_single_run_20d_high_budget.json` (full text given in Appendix A), describing the sequence of operations: dataset generation, parameter optimization by each of the five methods, validation of found parameters on the control set, and collection of final metrics. This approach made it possible to abstract from the specific execution environment and use the same scenario both for local debugging and for cluster execution. Thus, the individual plan item regarding automation of build and result verification was fulfilled: a unified plan eliminates manual data transfer between stages and guarantees identical conditions for all methods.

## 1.3. SLURM Scripts and DAG Orchestration for Parallel Execution

Two SLURM scripts were prepared for plan execution. The first, `run_ecm_plan.slurm`, executes the entire plan within a single task with allocation of all 28 cores of one node. It was used only at the initial debugging stage to verify system operability in the HPC environment. The main high-budget experiment was conducted using the second script — `run_ecm_plan_multinode.slurm`. This script implements orchestration based on a directed acyclic graph (DAG), in which each materialized step of the plan (dataset generation, optimization for each method, validation, analysis) is launched as a separate SLURM task. Dependencies between steps (e.g., `optimize_*` from `generate`, `validate_*` from the corresponding `optimize_*`) are expressed through the `--dependency=afterok` mechanism, allowing automatic chaining and simultaneous execution of all independent branches (in this case, optimization for five methods). Results of intermediate steps are saved to a common state file `plan_state.json` using file locks, ensuring data transfer between tasks. Such DAG orchestration can potentially achieve parallelism equal to the number of independent branches (up to five), but at the time of the experiment, allocated computing resources were limited to four nodes of the tornado partition, so the actual level of parallelism did not exceed four simultaneously executing tasks. Nevertheless, the use of the multi-task script noticeably reduced the total wall-clock time of the experiment compared to sequential execution. Fragments of SLURM scripts are given in Appendix B.

## 1.4. Environment Setup and Dependency Verification

An important element of adaptation was path configuration and verification of command availability. In the SLURM script, before running the plan, loading of the Python module, activation of the project's virtual environment (if present), and addition of the directory with the self-compiled `ecm` binary (GMP-ECM) to the PATH are performed. A check for the presence of `ecm-optimizer` and `ecm` commands with diagnostic message output was also added. These measures ensured a deterministic environment and reduced the probability of failures due to missing dependencies. Thus, the individual plan item prescribing the preparation of SLURM scripts and optimization of parallel ECM execution was fully completed.

## 1.5. Chapter Conclusion

As a result of adaptation, the software system was successfully deployed on the cluster and ready for the high-budget experiment. All subsequent computational experiments were performed on nodes of the tornado partition using the described scripts. The tasks of the first stage of the internship, concerning adaptation to the HPC environment, have been completed in full.

---

# Chapter 2. Computational Experiment Methodology

In accordance with the individual plan of the technological internship, this stage required conducting computational experiments on the selection of parameters $B_1$ and $B_2$ of the Elliptic Curve Method (ECM) using five heuristic optimization methods: Bayesian optimization (BO), differential evolution (DE), random search (RS), particle swarm optimization (PSO), and genetic algorithm (GA). All experiments were performed on the supercomputer resources of SCC "Polytechnichesky" using the prepared SLURM scripts (Appendix B) and a unified JSON plan (Appendix A), which ensured reproducibility and automation of the full cycle "generation → optimization → validation → analysis".

## 2.1. Dataset Generation Parameters

To obtain representative results, a dataset was generated for a 20-digit divisor. The cofactor size (the second prime factor) was set to 30 decimal digits, which corresponds to common practice in modeling factorization tasks where the sought prime divisor is significantly smaller than the cofactor, but the sizes of both factors remain within limits that ensure acceptable computational complexity of generation and ECM runs. The training set contains 80 numbers, the control set also 80 numbers. Generation was performed with a fixed seed value of 42, which guarantees full reproducibility of the experiment. All generated numbers are semiprime, i.e., the product of two primes; the primality of each factor was verified by the Miller–Rabin test. The corresponding parameters are fixed in the JSON plan (Appendix A) in the `generate_args` block.

## 2.2. Search Space and Objective Function

Each of the five optimization methods searched for a pair of parameters $(B_1, B_2)$ within the following bounds: $B_1 \in [500, 50000]$, $B_2 \in [5000, 3000000]$ with a constraint on the maximum ratio $B_2/B_1 \leq 1000$. These bounds were chosen based on GMP-ECM tables for the 20-digit divisor [2] and expanded both towards smaller and larger values to test the possibility of going beyond recommended ranges.

Unlike the previous implementation, where the objective function was focused exclusively on minimizing the expected factorization time $\widehat{E[T]}(B_1, B_2)$, which led to the selection of fast but unreliable configurations with unacceptably low success probability, at this stage the quality metric was redesigned. The new fitness function is a composite of three components, taking into account the probability of successfully finding the divisor, the average execution time, and the average number of curves.

The calculation is performed as follows. For each test number $n$ from the training set, $R$ repetitions ($R = 8$) are performed. In each repetition, ECM curves are run sequentially until reaching the limit $C_{\max} = 260$ (such a boundary is significantly higher than the expected number and cuts off unsuccessful parameter combinations) or until the first successful divisor discovery (stop-on-success strategy). For each repetition, success, time spent, and number of curves are recorded. Then, for number $n$, the average values across repetitions are calculated: success rate $success\_rate_n$, average time $\text{time}_n$, and average number of curves $\text{curves}_n$. After that, arithmetic means are calculated across all numbers in the training set: $\text{mean\_success\_rate}$, $\text{mean\_time}$, $\text{mean\_curves}$.

The final fitness function value (to be minimized) is calculated by the formula:

$$\text{score} = \text{success\_shortfall} \times 200000 + \text{mean\_time} \times 10000 + \text{mean\_curves} \times 50$$

where $\text{success\_shortfall} = \max(0, 0.9 - \text{mean\_success\_rate})$. The introduced weight coefficients (200000, 10000, 50) were chosen empirically and reflect the following hierarchy of priorities. First place is ensuring reliability: if the average proportion of successful runs falls below the target threshold of 90%, a significant penalty is imposed, making such a candidate obviously unacceptable. Among configurations that achieve the required reliability, preference is given to faster ones (lower average time). For close times, preference is given to the option with a lower average number of curves, which additionally stimulates saving computational resources. Thus, the new fitness function ensures balanced search, not allowing the optimizer to sacrifice factorization quality for speed.

## 2.3. Budgets and Hyperparameters of Optimization Methods

To ensure comparability of results, each method was allocated a comparable computational budget, expressed in the number of objective function evaluations. Individual method settings were chosen empirically based on preliminary experiments, taking into account their specifics: for DE and GA, the key parameters are population size and number of generations; for PSO — swarm size and number of iterations; for BO — number of initial random points and number of surrogate optimization rounds; for RS — total number of random attempts.

Method parameters are given in Table 2.1.

**Table 2.1 — Budgets and hyperparameters of optimization methods**

| Method | Budget / Main parameters |
|--------|--------------------------|
| BO | 16 initial samples, 56 iterations, candidate pool size 2500 |
| DE | popsize = 10, maxiter = 28, standard mutation (0.5–0.9) and crossover (0.8) coefficients |
| RS | budget = 160 random attempts |
| PSO | swarm_size = 18, iterations = 32, standard inertia, cognitive and social coefficients |
| GA | population_size = 22, generations = 36, mutation_prob = 0.14, crossover_prob = 0.8 |

## 2.4. Evaluation and Validation Parameters

To reduce the influence of random noise inherent to the probabilistic ECM algorithm, repeated runs were used. The values of parameters `max_curves_per_n` (upper bound of curves per number) and `repeats_per_n` (number of repetitions) were chosen considering the trade-off between statistical accuracy and computational cost.

According to GMP-ECM documentation [2], for a 20-digit divisor with optimal parameters $B_1=11000$, $B_2=1900000$, the expected number of curves to success is 74. At the optimization stage, `max_curves_per_n = 260` (approximately 3.5 times higher than the table value) allows reliable rejection of obviously suboptimal configurations without wasting excessive time on unsuccessful candidates. The number of repetitions `repeats_per_n = 8` provides initial averaging of random fluctuations.

At the validation stage, increased values are used: `max_curves_per_n = 600` and `repeats_per_n = 80`. The upper bound of 600 exceeds the expected number of curves even for non-optimal parameters, guaranteeing that the upper bound practically does not distort the measured average number of curves, allowing plausible estimates. The number of repetitions 80 provides high statistical accuracy (standard error about 5.6%). Such separation of budgets allows quick iteration over candidates at the optimization stage and obtaining reliable results for final comparison at the validation stage.

## 2.5. Reference Values for Comparison

As a baseline, parameters $B_1=11000$, $B_2=1900000$ recommended by the official GMP-ECM documentation [11] for a 20-digit divisor were used (Table 2.2). These values are a generally accepted benchmark for evaluating ECM efficiency. For each optimized method, the following metrics were calculated on the control set: integral score, average factorization time (in seconds), average number of curves to success, and success rate. Comparison was performed by absolute values and relative change (in percent) relative to baseline.

## 2.6. Computational Process Organization

All stages of the experiment (dataset generation, optimization, validation, analysis) were combined into a single JSON plan (Appendix A), which was orchestrated on the cluster using the script `run_ecm_plan_multinode.slurm` (Appendix B). Thanks to DAG dependencies, optimization for different methods started in parallel after dataset generation, and validation of each method — after completion of its optimization. Allocated resources (four nodes of the tornado partition) allowed simultaneous execution of up to four tasks, which reduced the total experiment time. Results were saved in structured form in the folder `data/experiments/20_dset_20260505T214657Z_job7012254/`.

## 2.7. Metrics and Calculation Method

Upon completion of validation, four main metrics were calculated for each method. The integral score is calculated by the formula given in section 2.2 and is subject to minimization. Average factorization time (in seconds) and average number of curves to success characterize the practical efficiency of the configuration, and success rate (proportion of successful runs on the control set) reflects reliability. All metrics were compared with the baseline both in absolute values and in the form of relative change (in percent). Calculations were automated within the `analyze` command of the plan, which eliminated manual errors during processing.

---

# Chapter 3. Computational Experiment Results

This chapter presents the results of the high-budget computational experiment performed on the supercomputer resources of SCC "Polytechnichesky" for a 20-digit divisor. Five optimization methods were compared: Bayesian optimization (BO), differential evolution (DE), random search (RS), particle swarm optimization (PSO), and genetic algorithm (GA). For each method, parameters $(B_1, B_2)$ were found, their validation on the control set was performed, and comparison with reference GMP-ECM values was conducted.

## 3.1. Comparison of Found Parameters with Reference

Table 3.1 presents validation results for all five methods. For each method, found parameters $B_1$, $B_2$, integral score values for baseline and validation (in absolute values and percent), as well as average factorization time, average number of curves, and success rate on the control set are indicated.

**Table 3.1 — Summary experiment results**

| Method | Parameters $(B_1, B_2)$ | Score baseline | Score val | Δ score | Time val (sec) | Δ time | Curves val | Δ curves | Success rate |
|--------|------------------------|----------------|-----------|---------|----------------|--------|------------|----------|--------------|
| BO | B1=26729, B2=2126731 | 37325 | 27844 | -25.4% | 2.514 | -22.4% | 54.03 | -44.7% | 1.00 |
| DE | B1=38271, B2=2713793 | 36652 | 27670 | -24.5% | 2.554 | -19.7% | 42.53 | -55.8% | 1.00 |
| RS | B1=26901, B2=2959183 | 36443 | 28181 | -22.6% | 2.563 | -19.0% | 51.02 | -46.8% | 0.99 |
| PSO | B1=49999, B2=3000000 | 36731 | 27875 | -24.1% | 2.600 | -18.5% | 37.33 | -61.2% | 1.00 |
| GA | B1=37480, B2=2545245 | 36482 | 27203 | -25.4% | 2.508 | -20.8% | 42.31 | -55.7% | 1.00 |

As follows from the table, all five methods ensured almost complete factorization reliability: success rate reached 1.0000 for four methods and 0.9998 for RS. The average number of curves decreased by 44–61% relative to baseline, indicating a significant increase in divisor search efficiency.

For detailed analysis of metric distributions for each method, Figures 3.1–3.5 present 5 groups of graphs — one figure per method. Each figure contains four distribution graphs: in the top row — distribution of score and success rate, in the bottom row — distribution of execution time and number of curves. Methods are arranged in descending order of validation time efficiency: GA (Figure 3.1), DE (Figure 3.2), RS (Figure 3.3), PSO (Figure 3.4), BO (Figure 3.5).

> [!NOTE]
> The original document contains 20 images (`media/image1.png` through `media/image20.png`) showing distribution graphs and convergence plots for each method. These images are not available in the provided text. Placeholders are noted below.

**Figure 3.1 placeholder:** `![GA distributions: score, success rate, time, curves](images/ga-distributions.png)`
**Figure 3.2 placeholder:** `![DE distributions: score, success rate, time, curves](images/de-distributions.png)`
**Figure 3.3 placeholder:** `![RS distributions: score, success rate, time, curves](images/rs-distributions.png)`
**Figure 3.4 placeholder:** `![PSO distributions: score, success rate, time, curves](images/pso-distributions.png)`
**Figure 3.5 placeholder:** `![BO distributions: score, success rate, time, curves](images/bo-distributions.png)`

Analysis of distributions confirms the tabular data. For GA (Figure 3.1), the most compact time distribution and a strong left shift of the number of curves are observed. DE (Figure 3.2) shows a similar pattern, but with slightly larger time variance. RS (Figure 3.3) shows the smallest score decline, which agrees with the minimal relative change of this metric. PSO (Figure 3.4) stands out with the strongest shift in the number of curves distribution, but the time distribution is shifted right relative to GA, indicating a non-optimal balance. BO (Figure 3.5) shows the least pronounced improvement across all metrics.

Notable is the behavior of the PSO method. The parameters it found, $B_1=49999$ and $B_2=3000000$, are at the upper bounds of the specified search range. This indicates that PSO during optimization "hit" the boundaries and could not find an interior point where further parameter increase ceases to improve the objective function. As a result, PSO achieved the maximum reduction in the number of curves (–61.24%), since high values of $B_1$ and $B_2$ increase the probability of success, but at the cost of the highest validation time among all methods (2.6009 seconds). In other words, PSO minimized the number of curves but did not optimize execution time.

Unlike PSO, the DE, GA, and RS methods converged to close parameter values: $B_1$ in the range 26900–38271, $B_2$ in the range 2.1–2.7 million. This region appears to be the true optimum for the considered fitness function: it is here that the best balance between execution time and reliability is achieved. GA showed the best validation time (2.5088 seconds) with a reduction in the number of curves of 55.75% and the maximum reduction in score (–25.44%). DE and RS showed similar results, only slightly inferior to GA. Thus, the convergence of three independent methods (DE, GA, RS) to one region of parameters serves as indirect confirmation that this region is indeed optimal, while PSO, which ended up at the boundary, did not find a better solution due to the characteristics of its search trajectory.

The integral score decreased in all methods by 22–25%. The smallest decline was recorded for RS (–22.67%), the largest for GA (–25.44%). This means that, despite increased reliability and reduction in the number of curves, the overall efficiency of the configurations in terms of the composite metric turned out to be lower than the reference. The reason is that the new fitness function described in section 2.2 was redesigned to achieve balanced consideration of reliability, time, and number of curves. Unlike the previous implementation, which minimized only expected time, often leading to the choice of fast but unreliable parameters, the new metric imposes a significant penalty for success rate falling below the 90% threshold. Therefore, optimizers, seeking to minimize fitness, may choose configurations that are not optimal in terms of score in GMP-ECM terms, but provide high reliability and low number of curves. For most practical factorization tasks where the priority is guaranteed divisor discovery, such a compromise is quite acceptable.

## 3.2. Optimization Dynamics and Search Geometry

To understand optimizer behavior during the search process, Figures 3.6–3.11 present convergence graphs and trajectories in parameter space.

> [!NOTE]
> The original document contains additional images (`media/image21.png` through `media/image26.png`) showing convergence curves and parameter trajectories. These images are not available in the provided text.

**Figure 3.6 placeholder:** `![GA best objective dynamics by phase](images/ga-convergence-dynamics.png)`
**Figure 3.7 placeholder:** `![Improvement jump size and plateau length](images/improvement-jumps.png)`
**Figure 3.8 placeholder:** `![PSO parameter trajectory (B1, B2)](images/pso-trajectory.png)`
**Figure 3.9 placeholder:** `![PSO quality map (B1, B2/B1 ratio)](images/pso-quality-map.png)`
**Figure 3.10 placeholder:** `![GA parameter trajectory (B1, B2)](images/ga-trajectory.png)`
**Figure 3.11 placeholder:** `![GA quality map (B1, B2/B1 ratio)](images/ga-quality-map.png)`

Comparison of PSO and GA trajectories visually explains the difference in obtained results. PSO's particle motion trajectory (Figure 3.8) shows that the algorithm starts with a wide spread across the entire feasible region, then quickly shifts toward increasing parameters. By the middle of optimization, all particles concentrate near the upper bounds ($B_1 \approx 50000$, $B_2 \approx 3000000$). In the final iterations, the swarm practically does not move, having "hit" the boundary. The PSO quality heat map (Figure 3.9) confirms that the region of best values is at the edge of the explored zone, but not necessarily the global optimum.

In contrast to PSO, the GA trajectory (Figure 3.10) demonstrates fundamentally different behavior. The population also explores a wide range at the beginning, but then converges to a compact region in the center of the space: $B_1 \approx 35000–38000$, $B_2 \approx 2.5–2.6$ million. None of the individuals reach the upper bounds, and the final generation stabilizes inside the feasible region. The GA heat map (Figure 3.11) shows a clear local minimum with smooth quality deterioration when shifting toward boundaries. This indicates that GA indeed found an interior optimum point, rather than being stopped by search boundaries.

Comparison of Figures 3.8 and 3.10 clearly illustrates the PSO problem: the lack of a mechanism that returns particles inside the region upon reaching boundaries led to the swarm "getting stuck" at the edge of the feasible range. GA, thanks to crossover and mutation operators, maintains population diversity and is able to return from boundaries to interior regions, which ultimately allowed finding a more balanced solution.

Analysis of found parameters confirms these visual observations. Optimal $B_1$ values for GA, DE, and RS lie in the range from 26900 to 38271, which is noticeably higher than the table value of 11000, but still below the upper bound. $B_2$ values are in the range from 2.1 to 2.7 million. PSO reached $B_1=49999$ and $B_2=3000000$ — the maximum possible values. Such divergence indicates that PSO did not find the true optimum, but only demonstrated a tendency to extreme parameter increase, while more effective methods (GA, DE, RS) were able to find a balanced solution. The optimal balance achieved by GA, DE, and RS allows reducing the number of curves by 55–56% with validation time about 2.51–2.56 seconds, while PSO, having reduced the number of curves more strongly (61%), paid for this with higher time (2.60 seconds).

Thus, visualization of trajectories and heat maps not only confirms quantitative conclusions but also provides tools for diagnosing optimizer behavior: PSO is prone to premature convergence at boundaries, while GA more stably finds interior optima.

## 3.3. Comparative Effectiveness of Methods

Based on the obtained results, the following ranking of methods by aggregate indicators can be proposed.

**GA** showed the best average validation time (2.5088 seconds) with a significant reduction in the number of curves (–55.75%) and high reliability. The GA search trajectory (Figure 3.10) demonstrates convergence to an interior parameter region, indicating the algorithm's ability to find balanced solutions. This makes GA the main candidate for tasks where execution time is critical with guaranteed reliability.

**DE** demonstrated results close to GA (2.5544 seconds, –55.80% curves) and remains a reliable evolutionary method. Its convergence to a similar parameter region confirms the correctness of the chosen optimum.

**RS**, despite its simplicity, showed results comparable to DE (2.5631 seconds, –46.81% curves) and the smallest score decline (–22.67%). This makes it useful for quickly estimating the lower bound of effectiveness and for sanity-check, confirming that adaptive methods indeed outperform random search (in time and number of curves, RS is inferior to GA and DE).

**PSO**, although achieving the maximum reduction in the number of curves (–61.24%), showed the worst validation time (2.6009 seconds). As shown in Figure 3.8, PSO "hit" the upper search boundaries and did not find a balanced solution that other methods found. This suggests that PSO in this hyperparameter configuration is less suitable for the ECM parameter optimization problem, especially with constraints on search boundaries. For practical use of PSO, it is recommended to either narrow the search boundaries or modify the boundary handling mechanism (e.g., introduce reflection or speed reduction when exiting boundaries).

**BO** proved the least effective in terms of number of curves (–44.76%) and score decline (–25.40%), which may be explained by an insufficient initial sample size (16 points) or the difficulty of building an adequate surrogate model for a space with non-uniform metric sensitivity. For problems of such dimensionality (two parameters), Bayesian optimization did not show advantages over simpler evolutionary methods.

## 3.4. Chapter Conclusions

The high-budget experiment confirmed the operability of all five heuristic methods for automated ECM parameter selection. All methods achieved almost complete reliability (success rate ≥ 0.9998) and reduced the average number of curves by 44–61%.

The best validation time was shown by GA (2.5088 seconds), the maximum reduction in the number of curves by PSO (–61.24%). However, PSO hit the upper search boundaries and did not find a balanced solution, unlike GA, DE, and RS, which converged to similar parameters ($B_1$ 26900–38271, $B_2$ 2.1–2.7 million) providing better time. The convergence of three independent methods to one region serves as confirmation that this region is optimal for the chosen fitness function. The found parameters are stably shifted toward higher $B_1$ and $B_2$ values compared to GMP-ECM table recommendations ($B_1=11000$, $B_2=1900000$).

The obtained results confirm that the use of heuristic optimization methods makes it possible to find parameters that provide high reliability and reduction in the number of curves, even if the integral score metric slightly worsens compared to the reference. For practical factorization tasks where the priority is guaranteed divisor discovery with a limited curve budget, the proposed approach may be preferable to using standard tables. GA proved to be the most balanced method, while PSO is a specialized tool for minimizing the number of curves, requiring careful application with revision of search boundaries or modification of boundary handling strategy.

---

# Conclusion

During the internship, the tasks provided for by the individual plan were fully implemented.

**Adaptation of the software system for operation in the SCC "Polytechnichesky" environment.** SLURM scripts (`run_ecm_plan.slurm` and `run_ecm_plan_multinode.slurm`) were prepared, providing both monolithic and DAG-orchestrated launch of a multi-step JSON plan on the cluster. Automatic transfer of dependencies between steps (dataset generation → optimization by methods → validation → analysis) through the `--dependency=afterok` mechanism and a common state file was implemented. The environment was configured (Python modules, virtual environment, PATH for GMP-ECM) and command availability was verified. This allowed transferring the computational pipeline to the supercomputer and conducting resource-intensive experiments with parallel execution of independent branches.

**Conducting a high-budget computational experiment.** For a 20-digit divisor, a full cycle of "generation → optimization → validation → analysis" was performed using five heuristic methods: Bayesian optimization (BO), differential evolution (DE), random search (RS), particle swarm optimization (PSO), and genetic algorithm (GA). The training set size was 80 numbers, the control set — 80 numbers, budgets at the optimization stage — 260 curves per number with 8 repetitions, at the validation stage — 600 curves with 80 repetitions. All calculations were performed on nodes of the tornado partition of SPbPU SCC.

**Obtained results.** All methods achieved almost complete reliability (success rate ≥ 0.9998) and reduced the average number of curves by 44–61% relative to the reference GMP-ECM parameters ($B_1=11000$, $B_2=1900000$). The best validation time was shown by GA (2.5088 s), the maximum reduction in the number of curves by PSO (–61.24%). At the same time, PSO hit the upper search boundaries ($B_1=49999$, $B_2=3000000$) and did not find a balanced solution, unlike GA, DE, and RS, which converged to similar parameters ($B_1$ 26900–38271, $B_2$ 2.1–2.7 million) with better time. The convergence of three independent methods confirms that the found region is optimal for the chosen fitness function. The integral `score` metric decreased by 22–25% for all methods, which is explained by the reorientation of the objective function from minimizing only time to balanced consideration of reliability, time, and number of curves, which is a conscious compromise in favor of practical guarantee of divisor discovery.

**Conclusions for further work.** GA is recommended as the main method for factorization tasks requiring high reliability and minimal time. PSO can be used to minimize the number of curves, but requires revision of search boundaries or modification of boundary handling. DE and RS remain reliable backup options. The obtained parameter configurations $(B_1, B_2)$ can be used for tuning ECM in practical cryptanalytic tasks where the priority is guaranteed divisor discovery with a limited budget.

Thus, the goals of the technological internship have been achieved, the software system has been prepared for cluster execution, a full cycle of comparative experiment has been conducted, and the results have been analyzed and interpreted. The materials of the report can be used in the preparation of the final qualifying work.

---

# References

1. Plekhanov E.S. ECM Evolutionary Optimization: software system for automated selection of elliptic curve method parameters. — Available at: https://github.com/EgorPlehanov/ecm-evolutionary-optimization

2. Zimmermann P. GMP-ECM: Elliptic Curve Method for Integer Factorization. — URL: https://gitlab.inria.fr/zimmerma/ecm (accessed: 5.04.2026)

---

# Appendix A: JSON Experiment Plan

Below is a brief explanation of the plan structure and its full text.

## A.1 Plan Explanation

The plan `full_all_methods_single_run_20d_high_budget.json` is a full experiment scenario in `ecm_run_plan_v1` format. It is intended for a single run that sequentially performs: dataset generation for 20-digit divisors, parameter optimization $(B_1, B_2)$ for all five methods (DE, RS, PSO, BO, GA), validation of found parameters on the control set, and collection of final analytics.

The top level of the plan contains the `format` field (version format), `description` (human-readable description), `params` (common parameters reused in several steps), and `operations` (sequence of operations). The `params` block includes a fixed seed for reproducibility, search boundaries, method list, individual optimization parameters for each method, common optimization and validation parameters, and dataset generation parameters. The `operations` block consists of three large steps: dataset generation, then a loop over methods (optimization and validation for each), followed by analytics collection. This approach ensures full reproducibility of the experiment and allows its execution both in a local environment and on a supercomputer without changing the logic.

## A.2 Full Plan Text

```json
{
  "format": "ecm_run_plan_v1",
  "description": "Full run for all methods (de/rs/pso/bo/ga) for target-digits=20 under new composite logic: generate + repeat(method)->optimize+validate + common analyze. High-budget version: increased optimize/validate budgets, expanded dataset; B2-max set to 3000000 and max-curves-per-n oriented to ECM table for D=20 (N≈74).",
  "params": {
    "seed": 42,
    "search": {
      "b1-min": 500,
      "b1-max": 50000,
      "b2-min": 5000,
      "b2-max": 3000000,
      "ratio-max": 1000
    },
    "method_list": ["de", "rs", "pso", "bo", "ga"],
    "method_opt": {
      "de": { "de-popsize": 10, "de-maxiter": 28 },
      "rs": { "rs-budget": 160 },
      "pso": { "pso-swarm-size": 18, "pso-iterations": 32 },
      "bo": { "bo-initial-samples": 16, "bo-iterations": 56, "bo-candidate-pool": 2500 },
      "ga": { "ga-population-size": 22, "ga-generations": 36, "ga-mutation-prob": 0.14 }
    },
    "shared_opt_args": {
      "max-curves-per-n": 260,
      "repeats-per-n": 8
    },
    "shared_val_args": {
      "max-curves-per-n": 600,
      "repeats-per-n": 80
    },
    "generate_args": {
      "target-digits": 20,
      "cofactor-digits": 30,
      "train-count": 80,
      "control-count": 80
    },
    "analyze_group_by": ["divisor_size", "method"]
  },
  "operations": [
    {
      "type": "generate",
      "label": "dataset_20_single",
      "args": {
        "$spread_ref": "params.generate_args",
        "seed": "$ref:params.seed"
      }
    },
    {
      "repeat": {
        "as": "method_iter",
        "values": { "method": "$ref:params.method_list" }
      },
      "operations": [
        {
          "type": "optimize",
          "label": "opt_{{method_iter.method}}_single",
          "args": {
            "dataset": "$ref:dataset_20_single.dataset_dir",
            "method": "$ref:method_iter.method",
            "seed": "$ref:params.seed",
            "$spread_ref": [
              "params.shared_opt_args",
              "params.method_opt.{{method_iter.method}}",
              "params.search"
            ]
          }
        },
        {
          "type": "validate",
          "label": "val_{{method_iter.method}}_single",
          "args": {
            "dataset": "$ref:dataset_20_single.dataset_dir",
            "opt-result-file": "$ref:opt_{{method_iter.method}}_single.result_file",
            "seed": "$ref:params.seed",
            "$spread_ref": "params.shared_val_args"
          }
        }
      ]
    },
    {
      "type": "analyze",
      "label": "analysis_single_dataset_all_methods",
      "args": {
        "dataset": "$ref:dataset_20_single.dataset_dir",
        "group-by": "$ref:params.analyze_group_by"
      }
    }
  ]
}
```

In the above code, all key experiment parameters are fixed, ensuring strict reproducibility. The plan was used during the high-budget run `20_dset_20260505T214657Z_job7012254` on the supercomputer resources of SCC.

---

# Appendix B: SLURM Scripts for Cluster Execution

Below are two working scripts for launching the ECM plan on SCC supercomputer resources. The first script (`run_ecm_plan.slurm`) executes the entire plan within a single SLURM task and was used at the debugging stage. The second script (`run_ecm_plan_multinode.slurm`) implements DAG orchestration: each plan step is submitted as a separate task with explicit dependencies, allowing parallel execution of independent branches (e.g., optimization by different methods). For high-budget experiments, the second, multi-task script is recommended.

## B.1 run_ecm_plan.slurm — monolithic plan launch

```bash
#!/bin/bash
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=28
#SBATCH --partition=tornado
#SBATCH --time=3-00:00:00
#SBATCH --job-name=ecm_plan
#SBATCH --output=%x-%j.out
#SBATCH --error=%x-%j.err

set -euo pipefail

# Environment Modules initialization (as per SCC instructions)
if [ -f /etc/profile.d/modules-basis.sh ]; then
    source /etc/profile.d/modules-basis.sh
fi

module purge

# Load Python module (search for conda version)
PYTHON_MODULE=""
for mod in python/3.10_conda python/3.10 python/3.12; do
    if module load "$mod"; then
        PYTHON_MODULE="$mod"
        break
    fi
done

if [ -z "$PYTHON_MODULE" ]; then
    echo "ERROR: Could not load any Python module." >&2
    exit 1
fi

echo "Loaded Python module: ${PYTHON_MODULE}"

cd "${SLURM_SUBMIT_DIR}"

# Activate virtual environment if exists
if [ -d .venv ]; then
    source .venv/bin/activate
fi

export PATH="$HOME/.local/bin:$PATH"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

# Check required commands
command -v ecm-optimizer >/dev/null 2>&1 || { echo "ERROR: ecm-optimizer not found." >&2; exit 1; }
command -v ecm >/dev/null 2>&1 || { echo "ERROR: ecm binary not found." >&2; exit 1; }

PLAN_NAME="${PLAN_NAME:-full_all_methods_single_run_20d}"

srun ecm-optimizer run-plan --plan "${PLAN_NAME}"
```

## B.2 run_ecm_plan_multinode.slurm — DAG orchestration via separate tasks

```bash
#!/bin/bash
#SBATCH --job-name=ecm_plan_multi
#SBATCH --partition=tornado
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --cpus-per-task=2
#SBATCH --time=02:00:00
#SBATCH --output=/dev/null
#SBATCH --error=/dev/null

set -euo pipefail

SUBMIT_DIR="${SLURM_SUBMIT_DIR:-$PWD}"
RUN_ROOT="${SUBMIT_DIR}/data/slurm_runs/job_${SLURM_JOB_ID}"
mkdir -p "${RUN_ROOT}/steps" "${RUN_ROOT}/state"

exec >"${RUN_ROOT}/controller.out" 2>"${RUN_ROOT}/controller.err"

if [ -f /etc/profile.d/modules-basis.sh ]; then
    source /etc/profile.d/modules-basis.sh
fi

module purge

PYTHON_MODULE=""
for mod in python/3.10_conda python/3.10 python/3.12; do
    if module load "$mod"; then
        PYTHON_MODULE="$mod"
        break
    fi
done

if [ -z "$PYTHON_MODULE" ]; then
    echo "ERROR: Could not load Python module." >&2
    exit 1
fi

echo "Loaded Python module: ${PYTHON_MODULE}"

cd "${SUBMIT_DIR}"

if [ -d .venv ]; then
    source .venv/bin/activate
fi

export PATH="$HOME/.local/bin:$PATH"
export OMP_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export OPENBLAS_NUM_THREADS="${SLURM_CPUS_PER_TASK}"
export MKL_NUM_THREADS="${SLURM_CPUS_PER_TASK}"

command -v ecm-optimizer >/dev/null 2>&1 || { echo "ERROR: ecm-optimizer not found." >&2; exit 1; }
command -v ecm >/dev/null 2>&1 || { echo "ERROR: ecm binary not found." >&2; exit 1; }

PLAN_NAME="${PLAN_NAME:-full_all_methods_single_run_20d}"
STEP_PARTITION="${STEP_PARTITION:-tornado}"
STEP_CPUS_PER_TASK="${STEP_CPUS_PER_TASK:-28}"
STEP_TIME_LIMIT="${STEP_TIME_LIMIT:-12:00:00}"
STEP_LOG_DIR="${STEP_LOG_DIR:-${RUN_ROOT}/steps}"
STEP_STATE_FILE="${STEP_STATE_FILE:-${RUN_ROOT}/state/plan_state.json}"

echo "Checking plan (dry-run validation): ${PLAN_NAME}"
ecm-optimizer run-plan-slurm \
    --plan "${PLAN_NAME}" \
    --partition "${STEP_PARTITION}" \
    --cpus-per-task "${STEP_CPUS_PER_TASK}" \
    --time-limit "${STEP_TIME_LIMIT}" \
    --log-dir "${STEP_LOG_DIR}" \
    --state-file "${STEP_STATE_FILE}" \
    --dry-run >/dev/null

echo "Orchestrator: ${PLAN_NAME}"
echo "Controller node(s): ${SLURM_NNODES}, tasks: ${SLURM_NTASKS}, cpu/task: ${SLURM_CPUS_PER_TASK}"
echo "Step resources: partition=${STEP_PARTITION}, cpus-per-task=${STEP_CPUS_PER_TASK}, time=${STEP_TIME_LIMIT}"
echo "Step logs: ${STEP_LOG_DIR}, state: ${STEP_STATE_FILE}"

srun --ntasks=1 --nodes=1 ecm-optimizer run-plan-slurm \
    --plan "${PLAN_NAME}" \
    --partition "${STEP_PARTITION}" \
    --cpus-per-task "${STEP_CPUS_PER_TASK}" \
    --time-limit "${STEP_TIME_LIMIT}" \
    --log-dir "${STEP_LOG_DIR}" \
    --state-file "${STEP_STATE_FILE}"
```

Both scripts are operational and were used during the internship: the first for debugging, the second for the main high-budget experiment. The choice of script is determined by the required degree of parallelism.
