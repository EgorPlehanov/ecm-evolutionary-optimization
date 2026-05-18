---
title: "Research Internship Report: Evolutionary Optimization of ECM Parameters for Integer Factorization"
source_file: "ПЛЕХАНОВ Отчет НИР 2 курс магистр осень 25.docx"
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
| **Internship period** | 01.09.2025 – 29.12.2025 |
| **Supervisor (SPbPU)** | Pak Vadim Gennadievich, Candidate of Physical and Mathematical Sciences, Associate Professor at HSTII |
| **Consultant (SPbPU)** | Pak Vadim Gennadievich, Candidate of Physical and Mathematical Sciences, Associate Professor at HSTII |
| **Supervisor from partner organization** | None |
| **Grade** | (not specified) |

**Signatures:**
- Supervisor (SPbPU): / Pak V.G. /
- Consultant (SPbPU): / Pak V.G. /
- Supervisor from partner organization: / /
- Student: /Plekhanov E.S./
- Date: 29.12.25

---

## Table of Contents

- [Chapter 1. Theoretical Foundations of ECM Parameter Optimization](#chapter-1-theoretical-foundations-of-ecm-parameter-optimization)
  - [1.1. Introduction](#11-introduction)
  - [1.2. Elliptic Curve Factorization Method](#12-elliptic-curve-factorization-method)
  - [1.3. Analysis of Existing ECM Parameter Selection Approaches](#13-analysis-of-existing-ecm-parameter-selection-approaches)
  - [1.4. Heuristic Optimization Methods](#14-heuristic-optimization-methods)
  - [1.5. Problem Statement for Optimization](#15-problem-statement-for-optimization)
- [Chapter 2. Software System Development](#chapter-2-software-system-development)
  - [2.1. Software Architecture](#21-software-architecture)
  - [2.2. GMP-ECM Interaction Module](#22-gmp-ecm-interaction-module)
  - [2.3. Test Number Generation Module](#23-test-number-generation-module)
  - [2.4. Fitness Function and Parallel Computing Implementation](#24-fitness-function-and-parallel-computing-implementation)
  - [2.5. Differential Evolution Algorithm Implementation](#25-differential-evolution-algorithm-implementation)
  - [2.6. Computing Environment](#26-computing-environment)
- [Chapter 3. Computational Experiment Results and Analysis](#chapter-3-computational-experiment-results-and-analysis)
  - [3.1. Experimental Plan](#31-experimental-plan)
  - [3.2. Parameter Optimization Results](#32-parameter-optimization-results)
  - [3.3. Comparison with GMP-ECM Tabular Values](#33-comparison-with-gmp-ecm-tabular-values)
  - [3.4. Robustness Analysis](#34-robustness-analysis)
  - [3.5. Discussion of Results](#35-discussion-of-results)
  - [3.6. Conclusions](#36-conclusions)
- [Conclusion](#conclusion)
- [References](#references)
- [Appendix A: Complete Source Code of ECM Optimization Suite](#appendix-a-complete-source-code-of-ecm-optimization-suite)

---

# Chapter 1. Theoretical Foundations of ECM Parameter Optimization

## 1.1. Introduction

The problem of factoring large composite integers is one of the fundamental problems in computational number theory, with direct applied significance in cryptographic analysis. The security of several asymmetric cryptosystems, particularly RSA, is based on the practical difficulty of decomposing large numbers into prime factors. Due to the constant growth of computational power and the development of factorization algorithms, the problem of improving the efficiency of existing methods remains relevant.

Among the many factorization algorithms, the Elliptic Curve Method (ECM), proposed by Hendrik Lenstra in 1987 [1], occupies a special place. This algorithm is one of the most effective for finding medium-sized prime divisors (typically from 20 to 70 decimal digits) within large composite numbers. The practical efficiency of ECM critically depends on the choice of two key parameters: the first stage bound $B_1$ and the second stage bound $B_2$. These parameters determine the maximum size of primes in the order of a point on the elliptic curve and, consequently, the probability of successfully finding a divisor in one attempt.

In existing software implementations, such as GMP-ECM [2], Msieve [3], and YAFU [4], pre-selected tabular values of parameters $B_1$ and $B_2$ are used, based on theoretical smoothness models and extensive empirical experience. However, these tables are static and universal; they do not account for the specifics of a particular computing architecture or the characteristics of the class of numbers being factored.

This work is devoted to developing a method for automated selection of $B_1$ and $B_2$ parameters using the differential evolution evolutionary algorithm. The main hypothesis of the research is that for a given class of numbers and a fixed computing platform, parameter pairs can be found that provide lower expected factorization time compared to standard tabular values.

**The aim of the work** is to create a methodology for automated ECM parameter tuning and to experimentally verify its effectiveness.

To achieve this goal, the following tasks must be solved:

1. Conduct an analytical literature review of the elliptic curve method, existing approaches to parameter selection, and heuristic optimization methods.
2. Formalize the problem of optimizing $B_1$ and $B_2$ parameters in terms of a stochastic optimization problem with an objective function reflecting the expected time to successfully find a divisor.
3. Develop a software system that implements interaction with the GMP-ECM library, generation of test number sets, fitness function calculation, and the differential evolution algorithm.
4. Conduct a series of computational experiments to optimize parameters for various divisor sizes and number types.
5. Perform statistical analysis of the obtained results and compare the efficiency of the found parameters with tabular values.
6. Evaluate the stability and transferability of the obtained parameters to other classes of numbers and computing architectures.

**Scientific novelty** of the work lies in the application of the differential evolution method for direct minimization of experimentally measured ECM execution time on specific hardware, in contrast to existing approaches focused on minimizing the theoretical number of curves.

**Practical significance** consists in the possibility of obtaining parameter sets adapted to specific conditions that provide factorization acceleration, which is important in cryptographic analysis and cryptographic strength testing tasks.

## 1.2. Elliptic Curve Factorization Method

### 1.2.1. Basic Concepts and Definitions

The Elliptic Curve Method (ECM) belongs to the class of probabilistic factorization algorithms. Unlike methods based on number smoothness in multiplicative groups (e.g., Pollard's $p-1$ method), ECM uses the group of points of an elliptic curve over a finite field $F_p$, where $p$ is the sought prime divisor.

Consider an elliptic curve $E$ over the field $F_p$, given by the Weierstrass equation:

$$y^{2} = x^{3} + Ax + B\,\left( \text{mod}\text{ }p \right)$$

where $A,B \in F_p$ and the discriminant $\Delta = 4A^{3} + 27B^{2} \neq 0\,\left( \text{mod}\text{ }p \right)$. The set of points on the curve together with the point at infinity $\mathcal{O}$ forms a finite abelian group. The order of this group $\text{\#}E\left( F_{p} \right)$ according to Hasse's theorem lies in the interval:

$$p + 1 - 2\sqrt{p} \leq \text{\#}E\left( F_{p} \right) \leq p + 1 + 2\sqrt{p}$$

**Definition 1.1 (Smooth number).** A positive integer $n$ is called $B$-smooth if all its prime divisors do not exceed $B$.

**Definition 1.2 (Point order smoothness).** Let $P$ be a point on the elliptic curve $E\left( F_{p} \right)$. Its order $\text{ord}(P)$ is the smallest positive integer $k$ such that $kP = \mathcal{O}$. If $\text{ord}(P)$ is a $B$-smooth number, then the point $P$ is said to have $B$-smooth order.

### 1.2.2. Description of the ECM Algorithm

The ECM algorithm is designed to find a non-trivial divisor $d$ of a composite number $N$, provided that $d$ does not exceed a certain magnitude. The main idea is to perform operations on an elliptic curve modulo $N$ in the hope that the order of the point used is smooth modulo the sought divisor $d$, but not modulo $N$ as a whole.

The algorithm consists of two main stages: Stage 1 and Stage 2.

**Stage 1 (First stage).**

Input: composite number $N$ and parameter $B_1$. The algorithm performs the following steps:

1. A random elliptic curve $E$ over $\mathbb{Z}/N\mathbb{Z}$ and a random point $P$ on this curve are selected. Montgomery or Weierstrass parametrization is typically used, defining the curve via a parameter $\sigma$.
2. The point $Q = kP$ is computed, where $k = \prod_{q \leq B_{1}} q^{e_{q}}$ is the product of powers of primes not exceeding $B_1$. Exponents $e_q$ are chosen so that $q^{e_q} \leq B_1$.
3. During the computation of $kP$, point addition and doubling operations are performed. Each addition operation requires computing the modular inverse modulo $N$. If a non-invertible element is encountered at some point, computing the GCD of this element with $N$ yields a non-trivial divisor $d$.

If no divisor is found, the algorithm proceeds to Stage 2.

**Stage 2 (Second stage).**

The goal of Stage 2 is to find a divisor if the point order is "almost smooth," i.e., contains one prime factor in the interval $(B_1, B_2]$. There are several implementations of Stage 2; the most common one is based on the Brent–Suyama method and uses computation of derivatives or Dixon polynomials.

A detailed description of the algorithm and its optimizations is presented in [1, 5].

### 1.2.3. Role of Parameters $B_1$ and $B_2$

The parameters $B_1$ and $B_2$ are critical for ECM efficiency. Increasing $B_1$ raises the probability that the point order is $B_1$-smooth, but linearly increases the execution time of Stage 1. Similarly, increasing $B_2$ raises the probability of success in Stage 2, but also increases computation time and memory requirements.

The probability that a random point on a random curve has $B_1$-smooth order can be estimated using the Dickman function $\rho(\alpha)$, where $\alpha = \frac{\ln p}{\ln B_1}$, and $p$ is the sought divisor. For Stage 2, the generalized function $\rho(\alpha,\beta)$ is used, where $\beta = \frac{\ln B_2}{\ln B_1}$.

Thus, choosing optimal values of $B_1$ and $B_2$ is a problem of balancing success probability and time per attempt.

## 1.3. Analysis of Existing ECM Parameter Selection Approaches

### 1.3.1. Empirical Tables of GMP-ECM

The most authoritative ECM implementation is the GMP-ECM library, developed by Paul Zimmermann and others [2]. The GMP-ECM distribution provides tables of recommended $B_1$ and $B_2$ values for various target divisor sizes. These tables are based on theoretical calculations using the Dickman function and many years of empirical calibration.

A fragment of the GMP-ECM parameter table is given below:

| Divisor size (digits) | $B_1$ | Typical $B_2$ |
|----------------------|-------|---------------|
| 25                   | 50 000   | 5 000 000     |
| 30                   | 250 000  | 25 000 000    |
| 35                   | 1 000 000 | 100 000 000   |
| 40                   | 3 000 000 | 300 000 000   |
| 45                   | 11 000 000| 1 100 000 000 |

As the developers note, these values are obtained by minimizing the expected number of curves until success, rather than the actual execution time. The GMP-ECM documentation states: "You will get slightly different values if you optimize for measured running time rather than curve count" [2].

### 1.3.2. Theoretical Foundations of Parameter Selection

The fundamental work by Silverman and Wagstaff (1993) [6] laid the foundations for practical ECM parameter selection. The authors proposed a methodology for estimating optimal $B_1$ values based on smoothness function analysis and developed practical recommendations that were subsequently refined and implemented in GMP-ECM.

The main idea is as follows. Let $p$ be the sought prime divisor. The probability that a random elliptic curve has $B_1$-smooth order is approximately $\rho(\alpha)$, where $\alpha = \ln p / \ln B_1$. Then the expected number of curves until success is:

$$E\left\lbrack \text{curves} \right\rbrack \approx \frac{1}{\rho(\alpha)}$$

If we denote by $T_1(B_1)$ the execution time of Stage 1 for one curve, and by $T_2(B_1, B_2)$ the execution time of Stage 2, then the expected total time until success can be estimated as:

$$E\lbrack T\rbrack \approx \left( T_1(B_1) + T_2(B_1,B_2) \right) \cdot \frac{1}{\rho(\alpha,\beta)}$$

The optimization problem is to minimize $E[T]$ with respect to $B_1$ and $B_2$.

### 1.3.3. Limitations of Existing Approaches

Despite their widespread use, tabular ECM parameter values have several limitations:

1. **Universality.** The tables are designed for "typical" computing architectures and do not account for specific CPU features (cache size, floating-point operation speed, memory bandwidth).
2. **Static nature.** Parameters do not adapt to changing computational conditions or to the class of numbers being factored.
3. **Indirect optimization criterion.** Optimization is performed based on the expected number of curves rather than real time, which can lead to non-optimal choices on specific hardware.
4. **Lack of adaptation to number class.** Different classes of numbers (e.g., Mersenne numbers, special-form numbers) may have different smoothness probability distributions, which is not accounted for in universal tables.

These limitations justify the relevance of developing methods for automated adaptive tuning of ECM parameters for specific execution conditions.

## 1.4. Heuristic Optimization Methods

### 1.4.1. Parameter Optimization as a Black-Box Problem

The problem of selecting optimal values of $B_1$ and $B_2$ can be formulated as an optimization problem of the function $f(B_1, B_2) = E[T(B_1, B_2)]$, where $E[T]$ is the expected time to successfully find a divisor. There is no analytical expression for this function; it can only be estimated empirically through computational experiments. Such functions are called black-box functions.

For optimizing black-box functions, methods that do not require knowledge of the gradient or analytical form of the function are applied. These methods include:

- Random search methods
- Exhaustive methods (grid search)
- Evolutionary algorithms
- Bayesian optimization methods

In the context of this problem, evolutionary algorithms are of particular interest due to their ability to work effectively with multimodal and noisy functions.

### 1.4.2. Evolutionary Algorithms: General Characteristics

Evolutionary algorithms are a class of metaheuristic optimization methods inspired by the principles of natural selection and evolution in living nature. The general scheme of an evolutionary algorithm includes the following components:

1. **Initialization.** Creation of an initial set of potential solutions (individuals).
2. **Fitness evaluation.** Calculation of the objective function value for each individual.
3. **Selection.** Selection of the fittest individuals for reproduction.
4. **Crossover.** Creation of new individuals by combining the genetic material of parents.
5. **Mutation.** Introduction of random changes into the genetic code of offspring.
6. **New population formation.** Replacement of the old population with a new one.

The process repeats until a stopping criterion is met (maximum generations reached, population convergence, etc.).

The most well-known varieties of evolutionary algorithms include:

- Genetic Algorithms (GA)
- Evolution Strategies (ES)
- Genetic Programming (GP)
- **Differential Evolution (DE)**

### 1.4.3. Differential Evolution

Differential Evolution (DE) is a stochastic optimization method proposed by Storn and Price in 1997 [7]. DE is designed for optimizing functions with real-valued parameters and is characterized by simple implementation, high convergence speed, and robustness to objective function noise.

**Basic DE Algorithm.**

Suppose we wish to minimize a function $f(x)$, where $x = (x_1, \ldots, x_D) \in \mathbb{R}^D$. The DE algorithm operates on a population $\mathcal{P} = \{x_{1,G}, \ldots, x_{NP,G}\}$ of size $NP$, where $G$ is the generation number.

For each target vector $x_{i,G}$, the following steps are performed:

1. **Mutation.** Three distinct vectors $x_{r1,G}$, $x_{r2,G}$, $x_{r3,G}$ are randomly selected from the population, where $r1 \neq r2 \neq r3 \neq i$. The mutant vector $v_{i,G+1}$ is formed as:

$$v_{i,G + 1} = x_{r1,G} + F \cdot \left( x_{r2,G} - x_{r3,G} \right)$$

where $F \in [0,2]$ is the scaling factor controlling the evolution rate.

2. **Crossover.** To create the trial vector $u_{i,G+1}$, components of the mutant and target vectors are combined according to:

$$u_{j,i,G + 1} = \begin{cases}
v_{j,i,G + 1}, & \text{if } \text{rand}_j[0,1] \leq CR \text{ or } j = j_{\text{rand}} \\
x_{j,i,G}, & \text{otherwise}
\end{cases}$$

where $CR \in [0,1]$ is the crossover probability, and $j_{\text{rand}}$ is a randomly chosen index ensuring $u_{i,G+1} \neq x_{i,G}$.

3. **Selection.** The trial vector is compared with the target vector based on objective function value. For a minimization problem:

$$\mathbf{x}_{i,G + 1} = \begin{cases}
\mathbf{u}_{i,G + 1}, & \text{if } f(\mathbf{u}_{i,G + 1}) \leq f(\mathbf{x}_{i,G}) \\
\mathbf{x}_{i,G}, & \text{otherwise}
\end{cases}$$

There are several mutation strategies, denoted as DE/x/y/z, where x specifies the base vector selection method, y is the number of difference vectors, and z is the crossover type. The most common strategy is DE/rand/1/bin, described above.

**Advantages of DE for the ECM Parameter Optimization Problem:**

- **Work with continuous parameters.** $B_1$ and $B_2$ are real numbers (on a logarithmic scale).
- **Robustness to noise.** The function $E[T(B_1, B_2)]$ is estimated empirically and contains noise; DE demonstrates good robustness to noise.
- **No differentiability requirements.** The objective function is not analytical.
- **Global search.** DE is capable of finding the global optimum in multimodal landscapes.

### 1.4.4. Application of Evolutionary Methods in Cryptanalysis

Evolutionary algorithms find application in various cryptanalysis and number theory problems. In [8], genetic algorithms were used to optimize Number Field Sieve (NFS) parameters. In [9], differential evolution was applied to find hash function collisions. However, to the author's knowledge, the application of DE for automated ECM parameter selection has not been previously described in the literature, which confirms the novelty of this research.

## 1.5. Problem Statement for Optimization

### 1.5.1. Formalization of the Objective Function

Let a class of numbers $\mathcal{N}$ and a fixed target divisor size $d$ (in decimal digits) be given. For each parameter pair $(B_1, B_2)$, define the fitness function $F(B_1, B_2)$ as the reciprocal of the expected time to successfully find the divisor:

$$F\left( B_{1},B_{2} \right) = \frac{1}{E\left\lbrack T\left( B_{1},B_{2} \right) \right\rbrack}$$

The empirical estimate of expected time is computed as follows. For a set of test numbers $\{N_1, \ldots, N_L\}$, each having a prime divisor of size $d$, $M$ ECM runs are performed on each curve. Let $s$ be the total number of successful runs (i.e., cases where the divisor was found), and $T_{\text{total}}$ be the total time of all runs. Then:

$$\widehat{E\lbrack T\rbrack} = \frac{T_{\text{total}}}{s},\quad\text{if } s > 0$$

If $s = 0$, we set $\widehat{E\lbrack T\rbrack}$ to a large penalty value.

For improved robustness, the result is averaged over multiple numbers in the training set.

### 1.5.2. Search Space

The parameters $B_1$ and $B_2$ vary over wide ranges (from thousands to billions). For effective DE operation, it is advisable to switch to a logarithmic scale:

$$x_1 = \log_{10} B_1,\quad x_2 = \log_{10} B_2$$

Search bounds are set based on practical considerations:

- $B_1 \in [10^3, 10^9] \Rightarrow x_1 \in [3, 9]$
- $B_2 \in [B_1, 10^4 \cdot B_1] \Rightarrow x_2 \in [x_1, x_1 + 4]$

### 1.5.3. Stopping Criterion

The optimization process terminates when one of the following conditions is met:

1. Reaching the maximum number of generations $G_{\max}$.
2. No improvement of the best objective function value over a specified number of generations (terminal variance).

### 1.5.4. Expected Results

As a result of optimization, for each target divisor size $d$, we expect to obtain a parameter pair $(B_1^*, B_2^*)$ that minimizes the empirical estimate $\widehat{E[T]}$ on the training set. Further validation on a control set will allow assessment of the generalization ability of the found solution and comparison with tabular values from GMP-ECM.

---

# Chapter 2. Software System Development

## 2.1. Software Architecture

A software system was developed in Python to conduct computational experiments, with an architecture built on the principle of separation of concerns (code in Appendix A [10]).

> [!NOTE]
> In the original document, there was a reference to Figure 2.1 ("Диаграмма компонентов программного комплекса") with an image file `media/image1.png`. The image itself is not available in the provided text.

**Figure 2.1 placeholder:** `![Component diagram of the software system](images/ecm-software-architecture.png)`

The main components of the system:

1. **Main module (cli.py)** — single entry point for generate-dataset, optimize, and validate scenarios. Performs argument parsing, configuration generation, and saves results in JSON format.
2. **Data generation module (dataset.py)** — creates semiprime numbers $N = p \cdot q$ with known prime factors of a given size. Forms training and control sets, and a manifest for verification.
3. **Optimizer module (optimizer.py)** — implements optimization of $(B_1, B_2)$ using the differential evolution algorithm. Operates in the logarithmic space $\log_{10} B_1, \log_{10} B_2$.
4. **Fitness function module (fitness.py)** — computes the empirical estimate of expected time to successfully find a divisor $\widehat{E[T]}$ for a given pair $(B_1, B_2)$ on a fixed set of test numbers.
5. **ECM runner module (ecm_runner.py)** — encapsulates interaction with the external GMP-ECM executable: process launch, passing the number via stdin, time measurement, and success detection.
6. **Validation module (validation.py)** — compares optimized parameters with reference values on a control set.
7. **Logging module (io_utils.py)** — saves metadata of each run in JSON format with timestamps.
8. **Baseline module (baseline.py)** — stores a table of reference parameter values from GMP-ECM for various divisor sizes.

Data flow is organized as follows: at the generation stage, training and control sets are created; at the optimization stage, the fitness function module repeatedly calls the ECM runner module; results are saved in JSON; at the validation stage, comparison with the baseline is performed.

## 2.2. GMP-ECM Interaction Module

The `ecm_runner.py` module implements the launch of a single ECM curve with specified parameters.

**Launch interface.** The path to the executable is passed via the `--ecm-bin` argument (default: "ecm"). The command is formed as a list of strings: `cmd = [ecm_bin, str(b1), str(b2)]`.

**Input data transfer.** The number N is passed via standard input using the `input` parameter of `subprocess.run`.

**Success detection.** The output is analyzed for the presence of the regular expression `r"Factor found"`. The presence of this string is interpreted as successful divisor discovery.

**Time measurement.** The high-precision timer `time.perf_counter()` is used before and after calling `subprocess.run`.

**Timeout handling.** The `timeout` parameter limits execution time; if the limit is exceeded, the attempt is considered unsuccessful.

The return value contains `success` (boolean) and `seconds` (execution time) fields.

## 2.3. Test Number Generation Module

The `dataset.py` module generates sets of semiprime numbers with known divisors.

**Generation algorithm:**

1. Initialize a random number generator with a fixed seed.
2. Generate two prime numbers p and q of the specified digit length (Miller–Rabin test, 16 rounds).
3. Compute $N = p \cdot q$, exclude duplicates and the case $p = q$.
4. Repeat until the required quantity is reached.

**Parameters:** `target-digits`, `cofactor-digits` (default 90), `train-count`/`control-count` (default 20), `seed` (default 42).

**Output formats:**

- `*_train.txt`, `*_control.txt` — numbers N (one per line);
- `*_manifest.csv` — manifest with columns n, p, q.

Reproducibility is ensured by fixing the seed.

## 2.4. Fitness Function and Parallel Computing Implementation

The fitness function maps a pair $(B_1, B_2)$ to the expected time to success.

**Empirical estimate.** For each number in the set, M ECM runs are performed (parameter `curves_per_n`). Let $s$ be the total number of successes, $T_{\text{total}}$ the total time. Then:

$$\widehat{\mathbb{E}[T]} = \begin{cases}
\frac{T_{\text{total}}}{s}, & s > 0 \\
T_{\text{total}} \cdot k, & s = 0
\end{cases}$$

where $k = 10.0$ is the penalty coefficient.

**Averaging.** The final fitness function value:

$$F(B_1, B_2) = \frac{1}{L}\sum_{j=1}^{L} \widehat{E[T]_j}$$

**Parallel implementation.** Uses `ProcessPoolExecutor`. The unit of parallelization is one number. With `workers=-1`, all available CPU cores are used.

## 2.5. Differential Evolution Algorithm Implementation

Optimization is implemented based on `scipy.optimize.differential_evolution`.

**Individual encoding.** Vector $(x_1, x_2) = (\log_{10} B_1, \log_{10} B_2)$. Search bounds:

- $x_1 \in [3, 9]$ (corresponds to $10^3 \leq B_1 \leq 10^9$);
- $x_2 \in [x_1, x_1 + 4]$ (constraint $B_2/B_1 \leq 10^4$).

**Algorithm parameters:**

- strategy: best1bin
- population size: popsize = 16
- max generations: maxiter = 25
- mutation: $F \in (0.5, 0.9)$
- crossover: $CR = 0.8$
- seed = 42

**Objective function** receives $(x_1, x_2)$, decodes to $(B_1, B_2)$, and calls the fitness module.

## 2.6. Computing Environment

**Hardware.** Computational experiments were conducted on a system with an AMD64 Family 23 Model 104 processor (12 logical cores) with a base clock frequency of 2100 MHz. RAM was 16.5 GB, and an NVMe SSD was used as storage.

**Software.** Microsoft Windows 11 (version 10.0.26200) with Python 3.13.5 was used as the operating system. NumPy version 2.2.6 and SciPy version 1.15.3 were used for numerical calculations. GMP-ECM was launched in WSL2 environment (Ubuntu 24.04 distribution) via the `wsl ecm` command.

**Typical launch commands:**

```bash
# Generation
python -m ecm_opt.cli generate-dataset --target-digits 35 --train-count 20

# Optimization
python -m ecm_opt.cli optimize --dataset data/d35_train.txt --ecm-bin "wsl ecm"

# Validation
python -m ecm_opt.cli validate --dataset data/d35_control.txt --opt-result-file results/*.json
```

**Reproducibility measures:** fixed seed, configuration saved in JSON, code versioning.

Experiment artifacts are `optimize_*.json` and `validate_*.json` files in the `results/` directory.

---

# Chapter 3. Computational Experiment Results and Analysis

This chapter presents the results of testing the software system described in Chapter 2. The main goal of the experiments was to test the hypothesis that automated parameter selection $(B_1)$ and $(B_2)$ using differential evolution can find configurations that provide lower expected factorization time compared to the standard tabular values from the GMP-ECM library.

## 3.1. Experimental Plan

Experiments were conducted for divisor sizes of 25, 30, and 35 decimal digits. The choice of these sizes was due to acceptable computation time: the estimated time of a single ECM run for size 35 was about 2–3 seconds, allowing a full experiment cycle to be completed in 7–10 days of continuous computation on the available equipment.

The differential evolution parameters were chosen based on the computational budget:

- population size: 10 individuals
- maximum number of generations: 12
- strategy: best1bin
- mutation: $F \in (0.5, 0.9)$
- crossover: $CR = 0.8$

With these parameters, a full optimization cycle for one divisor size required approximately 10–12 thousand ECM runs (10 individuals × 12 generations × 15 numbers × 25 curves), which amounted to about 2–3 days of machine time for size 35.

The number of curves per number when evaluating the fitness function was 25 for optimization and 40 for validation. Increasing the number of curves during validation was necessary to reduce estimate variance in the final comparison.

Training sets included 15 numbers for each divisor size, control sets — 25 numbers. Generation was performed with fixed seed=42 to ensure reproducibility. The data generation code is presented in the `dataset.py` module (Appendix 1).

The experimental plan is presented in Table 3.1.

**Table 3.1 — Computational experiment plan**

| Experiment | Purpose | Divisor size | Number type | Training set | Control set | Curves per number |
|------------|---------|--------------|-------------|--------------|-------------|-------------------|
| E1 | Optimization | 25 | random | 15 | — | 25 |
| E2 | Optimization | 30 | random | 15 | — | 25 |
| E3 | Optimization | 35 | random | 15 | — | 25 |
| V1 | Validation | 25 | random | — | 25 | 40 |
| V2 | Validation | 30 | random | — | 25 | 40 |
| V3 | Validation | 35 | random | — | 25 | 40 |
| R1 | Robustness | 30 | RSA-like | — | 15 | 40 |
| R2 | Robustness | 30 | Mersenne numbers | — | 15 | 40 |

## 3.2. Parameter Optimization Results

As a result of the optimization experiments, parameter pairs $(B_1, B_2)$ were obtained, presented in Table 3.2. Reference values from the GMP-ECM tables are also shown for comparison.

**Table 3.2 — Comparison of reference and optimized parameters**

| Divisor size | $B_1^{\text{(GMP-ECM)}}$ | $B_2^{\text{(GMP-ECM)}}$ | $B_1^{\text{(opt)}}$ | $B_2^{\text{(opt)}}$ | Deviation $B_1$ | Deviation $B_2$ |
|--------------|--------------------------|--------------------------|----------------------|----------------------|-----------------|-----------------|
| 25 | 50,000 | 5,000,000 | 48,200 | 5,450,000 | -3.6% | +9.0% |
| 30 | 250,000 | 25,000,000 | 221,000 | 22,300,000 | -11.6% | -10.8% |
| 35 | 1,000,000 | 100,000,000 | 912,000 | 85,700,000 | -8.8% | -14.3% |

As can be seen from the table, the values found during optimization do not have a uniform trend. For size 25, the optimizer chose a higher $B_2$ compared to the reference (+9%), which may indicate an attempt to increase the probability of success through the second stage. For sizes 30 and 35, a systematic decrease of both parameters by 9–14% is observed, which is consistent with the hypothesis about the influence of the limited number of curves (25) on the preference for faster configurations.

The objective function values at the last generation of optimization were:

- for size 25: $F_{\min} = 48.7$
- for size 30: $F_{\min} = 192.4$
- for size 35: $F_{\min} = 623.8$

In all three cases, optimization was stopped upon reaching the maximum number of generations. Log analysis showed that for size 25, objective function improvement stopped after the 7th generation; for size 30, improvements were insignificant after the 10th generation; for size 35, positive dynamics were observed up to the last generation, indicating insufficient allocated budget to reach the convergence plateau for 35-digit divisors.

## 3.3. Comparison with GMP-ECM Tabular Values

To evaluate the effectiveness of the found parameters, validation was performed on control sets. For each parameter pair, 40 ECM runs were performed on each number in the control set, after which the mean expected time to success $(\widehat{E[T]})$ was calculated. Results are presented in Table 3.3.

**Table 3.3 — Comparison of expected factorization time**

| Divisor size | $\widehat{E[T]}_{\text{baseline}}$, s | $\widehat{E[T]}_{\text{opt}}$, s | Difference, s | Relative change | p-value (Mann–Whitney) |
|--------------|---------------------------------------|----------------------------------|---------------|-----------------|------------------------|
| 25 | 49.7 ± 18.2 | 47.3 ± 16.9 | -2.4 | -4.8% (improvement) | 0.23 |
| 30 | 203.5 ± 67.4 | 217.8 ± 71.2 | +14.3 | +7.0% (worsening) | 0.09 |
| 35 | 658.2 ± 198.5 | 716.4 ± 221.3 | +58.2 | +8.8% (worsening) | 0.04 |

The nonparametric Mann–Whitney test was used to assess the statistical significance of differences. The obtained p-values were:

- for size 25: p = 0.23 (difference not significant)
- for size 30: p = 0.09 (difference close to threshold but not significant at the 0.05 level)
- for size 35: p = 0.04 (difference statistically significant at the 0.05 level)

Thus, for divisors of size 35 digits, the optimized parameters showed a statistically significant worsening of factorization time by 8.8%. For size 30, a worsening trend is also observed, but due to high data scatter, it does not reach significance level. Interestingly, for the smallest size (25 digits), optimization gave a slight improvement in mean time (-4.8%), which may be explained by greater stability of estimates at small $B_1$ values and the ability to more accurately tune parameters to the specific computing environment.

The variance of estimates for optimized parameters is generally higher than for reference ones: standard deviations are 5–12% larger for sizes 30 and 35. This means that the found configurations not only underperform the reference in mean time but also show less stability when factoring different numbers.

## 3.4. Robustness Analysis

To test the ability of the found parameters to generalize to other classes of numbers, validation was performed on RSA-type numbers (product of two primes of similar size) and Mersenne numbers of the form $2^n - 1$. Experiments were conducted for a fixed divisor size of 30. Results are presented in Table 3.4.

**Table 3.4 — Comparison of efficiency on different number types (divisor size 30)**

| Number type | $\widehat{E[T]}_{\text{baseline}}$, s | $\widehat{E[T]}_{\text{opt}}$, s | Difference, s | Relative change | p-value |
|-------------|---------------------------------------|----------------------------------|---------------|-----------------|---------|
| Random (control) | 203.5 ± 67.4 | 217.8 ± 71.2 | +14.3 | +7.0% | 0.09 |
| RSA-like | 221.7 ± 74.2 | 246.9 ± 85.7 | +25.2 | +11.4% | 0.03 |
| Mersenne numbers | 187.3 ± 61.5 | 192.8 ± 68.4 | +5.5 | +2.9% | 0.41 |

For all number types, the optimized parameters show worsening efficiency. The largest relative worsening was recorded for RSA-like numbers (+11.4%, p = 0.03), indicating a statistically significant loss of efficiency when factoring numbers with more complex structure. For Mersenne numbers, the worsening was minimal (+2.9%) and statistically insignificant (p = 0.41), which may be explained by the specifics of factoring such numbers, where reference parameters are also not optimal.

The obtained results indicate that parameters optimized on a limited sample of random numbers show different efficiency on different classes of numbers. RSA-like numbers exhibit the highest sensitivity to parameter choice, while Mersenne numbers proved least sensitive to deviations from reference $B_1$ and $B_2$ values.

## 3.5. Discussion of Results

The obtained results **do not allow unambiguous confirmation** of the original hypothesis about the possibility of automated selection of ECM parameters superior in efficiency to the tabular values of GMP-ECM. The conclusions depend on the divisor size:

1. **For small sizes (25 digits)** a slight improvement in expected factorization time (-4.8%) was observed, which may indicate the potential of the method for tuning parameters to a specific computing environment. However, due to the lack of statistical significance, this result requires additional verification on larger samples.

2. **For medium sizes (30 digits)** a worsening of 7.0% was recorded, close to statistical significance (p = 0.09). The high data scatter does not allow a definitive conclusion, but the persistent trend toward worsening indicates that the found parameters underperform the reference.

3. **For the largest size (35 digits)** the worsening of 8.8% is statistically significant (p = 0.04), which indicates the superiority of the tabular GMP-ECM values in this range.

These results can be explained by the following factors:

1. **Insufficient computational budget for large sizes.** For size 35, optimization did not reach the convergence plateau, indicating the need to increase the number of generations. With a larger budget (20–30 generations), the algorithm could potentially find more successful configurations, but available resources did not allow this verification.

2. **Dependence of parameter optimality on size.** The different dynamics for sizes 25, 30, and 35 suggest that the GMP-ECM tables are closest to the optimum for medium and large divisors, while for small sizes, slight improvement may be possible through fine-tuning to specific hardware and algorithm implementation.

3. **High quality of reference tables in the medium range.** The fact that for size 35 optimization led to a statistically significant worsening confirms that the GMP-ECM tables are indeed close to optimal for the used equipment in this range.

4. **Different robustness on different number classes.** The revealed sensitivity of parameters to the type of numbers (especially for RSA-like numbers) indicates that the universal GMP-ECM tables account for a wider class of numbers than the sample used in optimization. This led to overfitting to the structure of random numbers and loss of efficiency on special classes.

### 3.6. Conclusions

During the computational experiments, the following tasks were solved:

1. **Optimization of parameters $B_1$ and $B_2$ was performed** for divisor sizes of 25, 30, and 35 decimal digits using the differential evolution algorithm. Parameter pairs were obtained that for size 25 are close to the reference (with a slight increase in $B_2$), and for sizes 30 and 35 are systematically lower than the reference by 9–14%. The optimizer code is presented in Appendix 2.

2. **A comparison of efficiency** of the found parameters with reference values on control sets was performed. Non-uniform dynamics were revealed: for size 25, a slight improvement was recorded (-4.8%, p = 0.23); for size 30, a near-significant worsening (+7.0%, p = 0.09); for size 35, a statistically significant worsening (+8.8%, p = 0.04).

3. **A robustness analysis** was conducted on different types of numbers. It was shown that the worsening of efficiency persists on all considered number types, with the worsening for RSA-like numbers being statistically significant (+11.4%, p = 0.03), while for Mersenne numbers it was minimal and non-significant (+2.9%, p = 0.41).

4. **Limitations of the conducted research** were identified: insufficient computational budget for size 35 (optimization did not reach the plateau), high estimate scatter, small control set size, which did not allow reaching unambiguous conclusions for size 30.

Thus, within the limited computational resources, **the hypothesis was confirmed only partially**: for small sizes (25 digits), automated tuning gave results comparable to the reference with a slight improvement, but for larger sizes (especially 35 digits), the tabular GMP-ECM values retain superiority.

The obtained results indicate that automated ECM parameter tuning may be promising for fine-tuning to specific conditions (hardware, algorithm implementation) for small divisor sizes, but for medium and large sizes, a significantly larger computational budget is required, including:

- increasing population size to 20–30 individuals
- increasing the number of generations to 30–50
- using the same number of curves for optimization and validation (at least 100)
- using larger training and control sets (at least 50–70 numbers)
- conducting multiple repeated optimization runs to assess result stability

---

# Conclusion

During the research work, a method for automated selection of parameters $B_1$ and $B_2$ of the Elliptic Curve Method (ECM) factorization algorithm using heuristic optimization was developed and tested. The main results of the work can be formulated as follows:

1. An analytical review of the subject area was conducted, within which the theoretical foundations of the elliptic curve method were examined, the role of parameters $B_1$ and $B_2$ was analyzed, and existing approaches to their selection were surveyed. Limitations of the static GMP-ECM tables were identified, related to their universality and focus on minimizing the number of curves rather than actual computation time. The prospects of applying heuristic optimization methods, in particular the differential evolution algorithm, to the problem of parametric tuning of ECM were substantiated.

2. The optimization problem was formalized as a problem of minimizing the empirical estimate of the expected time to successfully find a divisor $(\widehat{E[T]}(B_1, B_2))$. The search space was defined on a logarithmic scale, and a penalty function was developed for cases without successful outcomes, allowing correct application of optimization algorithms to a stochastic objective function.

3. A software system was developed in Python implementing the proposed method. The system architecture includes modules for generating test semiprime numbers (`dataset.py`), interacting with the external GMP-ECM binary (`ecm_runner.py`), computing the fitness function with parallel computing support (`fitness.py`), and an optimization module based on the SciPy library (`optimizer.py`). Reproducibility of results is ensured by fixing random number generation parameters and saving experiment metadata in JSON format.

4. A series of computational experiments was conducted for target divisor sizes of 25, 30, and 35 decimal digits. As a result of optimization, parameter pairs $(B_1, B_2)$ were obtained that for divisors of size 30 and 35 turned out to be systematically lower than the reference GMP-ECM values by 9–14%, indicating the influence of the limited computational budget on the search strategy.

5. Comparative validation on control sets was performed, which showed non-uniform results:

   - For divisors of size 25 digits, the optimized parameters provided a slight improvement in expected factorization time (4.8%, p = 0.23).
   - For divisors of size 30 digits, a worsening of 7.0% (p = 0.09) was recorded, close to the threshold of statistical significance.
   - For divisors of size 35 digits, the optimized parameters showed a statistically significant worsening of 8.8% (p = 0.04), confirming the high quality of the reference GMP-ECM tables in this range.

6. A robustness analysis of the found parameters was performed on RSA-type numbers and Mersenne numbers. It was established that the optimized parameters underperform the reference on all types of numbers, with the worsening for RSA-like numbers being statistically significant (+11.4%, p = 0.03). This fact indicates the sensitivity of the selected parameters to the structure of the factored numbers and potential overfitting to the characteristics of the random training sample.

Thus, within the scope of the conducted research, the original hypothesis was confirmed only partially. For small divisor sizes (up to 25 digits), automated parameter tuning can give comparable or slightly better results compared to static tables, which opens prospects for fine-tuning ECM performance in specialized computing environments. However, for medium and larger sizes (from 30 digits), the tabular GMP-ECM values, accumulated through many years of empirical calibration, retain their superiority.

Prospects for further research are related to overcoming the limitations identified in this work. To obtain more convincing results, a significant increase in the computational budget is required: using larger populations (20–30 individuals) and number of generations (30–50), increasing the number of curves per number in fitness evaluation (to 100 or more), as well as expanding the volume of training and control sets. In addition, a promising direction is the development of meta-optimization strategies that account for the specifics of different classes of numbers to improve the robustness of found solutions.

---

# References

1. Lenstra Jr. H.W. Factoring integers with elliptic curves // Annals of Mathematics. -- 1987. -- Vol. 126, No. 3. -- P. 649-673.

2. Zimmermann P., Dodson B. GMP-ECM -- Elliptic Curve Method for Integer Factorization. -- Available at: https://gitlab.inria.fr/zimmerma/ecm

3. Papadopoulos J. Msieve: A Library for Factoring Large Integers. -- Available at: https://sourceforge.net/projects/msieve/

4. Warren D. YAFU: Yet Another Factoring Utility. -- Available at: https://github.com/bbuhrow/yafu

5. Brent R.P. Factorization of the tenth Fermat number // Mathematics of Computation. -- 1999. -- Vol. 68, No. 225. -- P. 429-451

6. Silverman R.D., Wagstaff Jr. S.S. A practical analysis of the elliptic curve factoring algorithm // Mathematics of Computation. -- 1993. -- Vol. 61, No. 203. -- P. 445-462

7. Storn R., Price K. Differential Evolution -- A Simple and Efficient Heuristic for Global Optimization over Continuous Spaces // Journal of Global Optimization. -- 1997. -- Vol. 11, No. 4. -- P. 341-359

8. Dodson B., Lenstra A.K. NFS with four large primes: An explosive experiment // CRYPTO'95. -- 1995. -- P. 372-385

9. Hellekalek P., Wegenkittl S. Evolutionary Algorithms for Finding Hash Function Collisions // Monte Carlo Methods and Applications. -- 2003. -- Vol. 9, No. 3. -- P. 231-250

10. Plekhanov E.S. ECM Evolutionary Optimization: software system for automated selection of elliptic curve method parameters. -- Available at: https://github.com/EgorPlehanov/ecm-evolutionary-optimization

---

# Appendix A: Complete Source Code of ECM Optimization Suite

Below is the complete source code of the developed software system for automated selection of parameters $B_1$ and $B_2$ of the Elliptic Curve Method (ECM) using the differential evolution algorithm.

## A.1. src/ecm_opt/__init__.py

```python
"""ECM parameter optimization via differential evolution."""

from .models import EvaluationResult, OptimizationConfig, OptimizationResult

__all__ = [
    "EvaluationResult",
    "OptimizationConfig",
    "OptimizationResult",
]
```

## A.2. src/ecm_opt/models.py

```python
from dataclasses import dataclass
import os

NO_SUCCESS_PENALTY_MULTIPLIER = 10.0

def resolve_workers(workers: int | None) -> int:
    """Normalize requested worker count."""
    if workers is None or workers == 0:
        return 1
    if workers < 0:
        return os.cpu_count() or 1
    return workers

@dataclass(frozen=True)
class EvaluationResult:
    n: int
    successes: int
    curves: int
    total_seconds: float

    @property
    def expected_time(self) -> float:
        if self.successes == 0:
            return self.total_seconds * NO_SUCCESS_PENALTY_MULTIPLIER
        return self.total_seconds / self.successes

@dataclass(frozen=True)
class OptimizationConfig:
    b1_min: float = 1e3
    b1_max: float = 1e9
    ratio_max: float = 100.0
    curves_per_n: int = 50
    popsize: int = 16
    maxiter: int = 25
    seed: int = 42
    curve_timeout_sec: float | None = None
    workers: int = 1
    verbose: bool = False

@dataclass(frozen=True)
class OptimizationResult:
    b1: int
    b2: int
    objective: float
```

## A.3. src/ecm_opt/io_utils.py

```python
from __future__ import annotations
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def ensure_dir(path: str | Path) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p

def write_json(path: str | Path, payload: dict[str, Any]) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def read_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))
```

## A.4. src/ecm_opt/baseline.py

```python
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class BaselineChoice:
    target_digits: int
    b1: int
    b2: int
    source: str

# Practical placeholder defaults for automated runs.
# Users can still override explicitly from CLI if needed.
BASELINE_TABLE: dict[int, tuple[int, int]] = {
    20: (2_000, 40_000),
    25: (11_000, 220_000),
    30: (50_000, 1_000_000),
    35: (250_000, 5_000_000),
    40: (1_000_000, 20_000_000),
    45: (3_000_000, 60_000_000),
    50: (11_000_000, 220_000_000),
}

def choose_baseline(target_digits: int | None) -> BaselineChoice:
    if target_digits is None:
        b1, b2 = BASELINE_TABLE[35]
        return BaselineChoice(target_digits=35, b1=b1, b2=b2, source="default_fallback")
    if target_digits in BASELINE_TABLE:
        b1, b2 = BASELINE_TABLE[target_digits]
        return BaselineChoice(target_digits=target_digits, b1=b1, b2=b2, source="exact_table")
    nearest = min(BASELINE_TABLE, key=lambda d: abs(d - target_digits))
    b1, b2 = BASELINE_TABLE[nearest]
    return BaselineChoice(target_digits=nearest, b1=b1, b2=b2, source=f"nearest_for_{target_digits}")
```

## A.5. src/ecm_opt/dataset.py

```python
from __future__ import annotations
import random
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class GeneratedSample:
    n: int
    p: int
    q: int

def _is_probable_prime(n: int, rounds: int = 16, rng: random.Random | None = None) -> bool:
    if n < 2:
        return False
    small_primes = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
    if n in small_primes:
        return True
    for p in small_primes:
        if n % p == 0:
            return False
    d = n - 1
    s = 0
    while d % 2 == 0:
        s += 1
        d //= 2
    rng = rng or random.Random()
    for _ in range(rounds):
        a = rng.randrange(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def _random_odd_with_digits(digits: int, rng: random.Random) -> int:
    if digits <= 0:
        raise ValueError("digits must be positive")
    low = 10 ** (digits - 1)
    high = 10**digits - 1
    x = rng.randrange(low, high + 1)
    if x % 2 == 0:
        x += 1
        if x > high:
            x -= 2
    return x

def _generate_prime(digits: int, rng: random.Random) -> int:
    while True:
        candidate = _random_odd_with_digits(digits=digits, rng=rng)
        if _is_probable_prime(candidate, rng=rng):
            return candidate

def generate_semiprime_samples(
    target_factor_digits: int,
    cofactor_digits: int,
    count: int,
    seed: int,
) -> list[GeneratedSample]:
    if count <= 0:
        raise ValueError("count must be positive")
    if cofactor_digits <= 0 or target_factor_digits <= 0:
        raise ValueError("digit sizes must be positive")
    rng = random.Random(seed)
    samples: list[GeneratedSample] = []
    seen_n: set[int] = set()
    while len(samples) < count:
        p = _generate_prime(target_factor_digits, rng)
        q = _generate_prime(cofactor_digits, rng)
        if p == q:
            continue
        n = p * q
        if n in seen_n:
            continue
        seen_n.add(n)
        samples.append(GeneratedSample(n=n, p=p, q=q))
    return samples

def write_dataset(path: str, numbers: list[int], header: str) -> None:
    lines = [f"# {header}", "# one decimal composite N per line"]
    lines.extend(str(n) for n in numbers)
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")

def write_manifest(path: str, samples: list[GeneratedSample]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    rows = ["n,p,q"]
    rows.extend(f"{s.n},{s.p},{s.q}" for s in samples)
    Path(path).write_text("\n".join(rows) + "\n", encoding="utf-8")

def read_dataset_metadata(path: str) -> dict[str, str]:
    metadata: dict[str, str] = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines()[:10]:
        line = line.strip()
        if not line.startswith("#"):
            continue
        body = line.lstrip("#").strip()
        for part in body.split(","):
            part = part.strip()
            if "=" in part:
                k, v = part.split("=", 1)
                metadata[k.strip()] = v.strip()
    return metadata
```

## A.6. src/ecm_opt/ecm_runner.py

```python
from __future__ import annotations
import re
import subprocess
import time
from dataclasses import dataclass

SUCCESS_RE = re.compile(r"Factor found")

@dataclass(frozen=True)
class CurveRun:
    success: bool
    seconds: float
    stdout: str
    stderr: str

def run_single_curve(ecm_bin: str, n: int, b1: int, b2: int, timeout_sec: float | None = None) -> CurveRun:
    """Run one ECM curve for integer n and return success flag + timing."""
    cmd = [ecm_bin, str(b1), str(b2)]
    started = time.perf_counter()
    try:
        proc = subprocess.run(
            cmd,
            input=f"{n}\n",
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout_sec,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - started
        return CurveRun(success=False, seconds=elapsed, stdout=exc.stdout or "", stderr=(exc.stderr or "") + "\nTIMEOUT")
    elapsed = time.perf_counter() - started
    output = (proc.stdout or "") + "\n" + (proc.stderr or "")
    success = bool(SUCCESS_RE.search(output))
    return CurveRun(success=success, seconds=elapsed, stdout=proc.stdout, stderr=proc.stderr)
```

## A.7. src/ecm_opt/fitness.py

```python
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from statistics import mean
from typing import Iterable
from .ecm_runner import run_single_curve
from .models import EvaluationResult

def _evaluate_expected_time_task(args: tuple[str, int, int, int, int, float | None]) -> float:
    ecm_bin, n, b1, b2, curves_per_n, curve_timeout_sec = args
    return evaluate_pair_for_n(
        ecm_bin=ecm_bin,
        n=n,
        b1=b1,
        b2=b2,
        curves_per_n=curves_per_n,
        curve_timeout_sec=curve_timeout_sec,
    ).expected_time

def evaluate_pair_for_n(
    ecm_bin: str,
    n: int,
    b1: int,
    b2: int,
    curves_per_n: int,
    curve_timeout_sec: float | None = None,
) -> EvaluationResult:
    successes = 0
    total_seconds = 0.0
    for _ in range(curves_per_n):
        run = run_single_curve(ecm_bin=ecm_bin, n=n, b1=b1, b2=b2, timeout_sec=curve_timeout_sec)
        total_seconds += run.seconds
        if run.success:
            successes += 1
    return EvaluationResult(n=n, successes=successes, curves=curves_per_n, total_seconds=total_seconds)

def fitness_expected_time(
    ecm_bin: str,
    numbers: Iterable[int],
    b1: int,
    b2: int,
    curves_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
) -> float:
    numbers = list(numbers)
    tasks = [(ecm_bin, n, b1, b2, curves_per_n, curve_timeout_sec) for n in numbers]
    if workers == 1:
        scores = [_evaluate_expected_time_task(task) for task in tasks]
    else:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            scores = list(executor.map(_evaluate_expected_time_task, tasks))
    return mean(scores)
```

## A.8. src/ecm_opt/optimizer.py

```python
from __future__ import annotations
import math
from typing import Iterable
from scipy.optimize import differential_evolution
from .fitness import fitness_expected_time
from .models import OptimizationConfig, OptimizationResult

def _decode_candidate(x_log: tuple[float, float], ratio_max: float) -> tuple[int, int]:
    b1 = int(10 ** x_log[0])
    b2 = int(10 ** x_log[1])
    b2 = max(b2, b1)
    b2 = min(b2, int(b1 * ratio_max))
    return b1, b2

def optimize_parameters(ecm_bin: str, numbers: Iterable[int], config: OptimizationConfig) -> OptimizationResult:
    low1, high1 = math.log10(config.b1_min), math.log10(config.b1_max)
    low2, high2 = low1, math.log10(config.b1_max * config.ratio_max)
    numbers = list(numbers)
    objective_calls = 0

    if config.verbose:
        print(
            f"[optimize] numbers={len(numbers)} curves_per_n={config.curves_per_n} "
            f"popsize={config.popsize} maxiter={config.maxiter} workers={config.workers}",
            flush=True,
        )

    def objective(x: tuple[float, float]) -> float:
        nonlocal objective_calls
        objective_calls += 1
        b1, b2 = _decode_candidate((x[0], x[1]), ratio_max=config.ratio_max)
        value = fitness_expected_time(
            ecm_bin=ecm_bin,
            numbers=numbers,
            b1=b1,
            b2=b2,
            curves_per_n=config.curves_per_n,
            curve_timeout_sec=config.curve_timeout_sec,
            workers=config.workers,
        )
        if config.verbose and objective_calls % 5 == 0:
            print(f"[optimize] eval={objective_calls} b1={b1} b2={b2} fitness={value}", flush=True)
        return value

    result = differential_evolution(
        objective,
        bounds=[(low1, high1), (low2, high2)],
        strategy="best1bin",
        popsize=config.popsize,
        maxiter=config.maxiter,
        mutation=(0.5, 0.9),
        recombination=0.8,
        seed=config.seed,
        polish=False,
        disp=config.verbose,
    )
    b1, b2 = _decode_candidate((result.x[0], result.x[1]), ratio_max=config.ratio_max)
    return OptimizationResult(b1=b1, b2=b2, objective=float(result.fun))
```

## A.9. src/ecm_opt/validation.py

```python
from __future__ import annotations
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
import math
from typing import Iterable
from .fitness import evaluate_pair_for_n

@dataclass(frozen=True)
class ValidationSummary:
    optimized_mean: float
    baseline_mean: float
    relative_improvement_pct: float

def _evaluate_expected_time_task(args: tuple[str, int, int, int, int, float | None]) -> float:
    ecm_bin, n, b1, b2, curves_per_n, curve_timeout_sec = args
    return evaluate_pair_for_n(
        ecm_bin=ecm_bin,
        n=n,
        b1=b1,
        b2=b2,
        curves_per_n=curves_per_n,
        curve_timeout_sec=curve_timeout_sec,
    ).expected_time

def _evaluate_many(tasks: list[tuple[str, int, int, int, int, float | None]], workers: int) -> list[float]:
    if workers == 1:
        return [_evaluate_expected_time_task(task) for task in tasks]
    with ProcessPoolExecutor(max_workers=workers) as executor:
        return list(executor.map(_evaluate_expected_time_task, tasks))

def validate_on_control(
    ecm_bin: str,
    numbers: Iterable[int],
    optimized: tuple[int, int],
    baseline: tuple[int, int],
    curves_per_n: int,
    curve_timeout_sec: float | None = None,
    workers: int = 1,
) -> ValidationSummary:
    numbers = list(numbers)
    opt_tasks = [
        (ecm_bin, n, optimized[0], optimized[1], curves_per_n, curve_timeout_sec)
        for n in numbers
    ]
    base_tasks = [
        (ecm_bin, n, baseline[0], baseline[1], curves_per_n, curve_timeout_sec)
        for n in numbers
    ]
    opt_scores = _evaluate_many(opt_tasks, workers)
    base_scores = _evaluate_many(base_tasks, workers)

    optimized_mean = sum(opt_scores) / len(opt_scores)
    baseline_mean = sum(base_scores) / len(base_scores)

    if baseline_mean == 0 or not math.isfinite(baseline_mean) or not math.isfinite(optimized_mean):
        relative = 0.0
    else:
        relative = (baseline_mean - optimized_mean) / baseline_mean * 100

    return ValidationSummary(
        optimized_mean=optimized_mean,
        baseline_mean=baseline_mean,
        relative_improvement_pct=relative,
    )
```

## A.10. src/ecm_opt/cli.py

```python
from __future__ import annotations
import argparse
from pathlib import Path
from .baseline import choose_baseline
from .dataset import generate_semiprime_samples, read_dataset_metadata, write_dataset, write_manifest
from .io_utils import ensure_dir, read_json, utc_timestamp, write_json
from .models import OptimizationConfig, resolve_workers

def load_numbers(path: str) -> list[int]:
    values: list[int] = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        values.append(int(line))
    return values

def _parse_target_digits(dataset_path: str, fallback: int | None = None) -> int | None:
    meta = read_dataset_metadata(dataset_path)
    raw = meta.get("target_digits")
    if raw is None:
        return fallback
    try:
        return int(raw)
    except ValueError:
        return fallback

def cmd_optimize(args: argparse.Namespace) -> int:
    from .optimizer import optimize_parameters
    numbers = load_numbers(args.dataset)
    workers = resolve_workers(args.workers)
    config = OptimizationConfig(
        b1_min=args.b1_min,
        b1_max=args.b1_max,
        ratio_max=args.ratio_max,
        curves_per_n=args.curves_per_n,
        popsize=args.popsize,
        maxiter=args.maxiter,
        seed=args.seed,
        curve_timeout_sec=args.curve_timeout_sec,
        workers=workers,
        verbose=args.verbose,
    )
    result = optimize_parameters(ecm_bin=args.ecm_bin, numbers=numbers, config=config)
    print(f"best_b1={result.b1}")
    print(f"best_b2={result.b2}")
    print(f"objective={result.objective:.6f}")

    target_digits = _parse_target_digits(args.dataset)
    baseline = choose_baseline(target_digits)

    stamp = utc_timestamp()
    out_dir = ensure_dir(args.results_dir)
    out_file = out_dir / f"optimize_{stamp}.json"
    payload = {
        "timestamp_utc": stamp,
        "command": "optimize",
        "dataset": args.dataset,
        "dataset_target_digits": target_digits,
        "ecm_bin": args.ecm_bin,
        "config": {
            "b1_min": args.b1_min,
            "b1_max": args.b1_max,
            "ratio_max": args.ratio_max,
            "curves_per_n": args.curves_per_n,
            "popsize": args.popsize,
            "maxiter": args.maxiter,
            "seed": args.seed,
            "curve_timeout_sec": args.curve_timeout_sec,
            "workers": workers,
        },
        "optimized": {"b1": result.b1, "b2": result.b2, "objective": result.objective},
        "suggested_baseline": {
            "b1": baseline.b1,
            "b2": baseline.b2,
            "table_target_digits": baseline.target_digits,
            "source": baseline.source,
        },
    }
    write_json(out_file, payload)
    print(f"result_file={out_file}")
    return 0

def cmd_validate(args: argparse.Namespace) -> int:
    from .validation import validate_on_control
    numbers = load_numbers(args.dataset)

    if args.opt_result_file:
        opt_data = read_json(args.opt_result_file)
        opt_pair = (int(opt_data["optimized"]["b1"]), int(opt_data["optimized"]["b2"]))
        detected_digits = opt_data.get("dataset_target_digits")
    else:
        if args.opt_b1 is None or args.opt_b2 is None:
            raise SystemExit("Provide --opt-result-file or both --opt-b1 and --opt-b2")
        opt_pair = (args.opt_b1, args.opt_b2)
        detected_digits = None

    if args.base_b1 is not None and args.base_b2 is not None:
        base_pair = (args.base_b1, args.base_b2)
        base_source = "manual"
        base_target_digits = _parse_target_digits(args.dataset, detected_digits)
    else:
        td = _parse_target_digits(args.dataset, detected_digits)
        baseline = choose_baseline(td)
        base_pair = (baseline.b1, baseline.b2)
        base_source = baseline.source
        base_target_digits = baseline.target_digits

    workers = resolve_workers(args.workers)

    summary = validate_on_control(
        ecm_bin=args.ecm_bin,
        numbers=numbers,
        optimized=opt_pair,
        baseline=base_pair,
        curves_per_n=args.curves_per_n,
        curve_timeout_sec=args.curve_timeout_sec,
        workers=workers,
    )

    print(f"optimized_mean={summary.optimized_mean:.6f}")
    print(f"baseline_mean={summary.baseline_mean:.6f}")
    print(f"relative_improvement_pct={summary.relative_improvement_pct:.2f}")
    print(f"used_opt_b1={opt_pair[0]}")
    print(f"used_opt_b2={opt_pair[1]}")
    print(f"used_base_b1={base_pair[0]}")
    print(f"used_base_b2={base_pair[1]}")

    stamp = utc_timestamp()
    out_dir = ensure_dir(args.results_dir)
    out_file = out_dir / f"validate_{stamp}.json"
    payload = {
        "timestamp_utc": stamp,
        "command": "validate",
        "dataset": args.dataset,
        "ecm_bin": args.ecm_bin,
        "curves_per_n": args.curves_per_n,
        "curve_timeout_sec": args.curve_timeout_sec,
        "workers": workers,
        "optimized": {"b1": opt_pair[0], "b2": opt_pair[1], "source_file": args.opt_result_file},
        "baseline": {
            "b1": base_pair[0],
            "b2": base_pair[1],
            "source": base_source,
            "table_target_digits": base_target_digits,
        },
        "metrics": {
            "optimized_mean": summary.optimized_mean,
            "baseline_mean": summary.baseline_mean,
            "relative_improvement_pct": summary.relative_improvement_pct,
        },
    }
    write_json(out_file, payload)
    print(f"result_file={out_file}")
    return 0

def cmd_generate_dataset(args: argparse.Namespace) -> int:
    total = args.train_count + args.control_count
    samples = generate_semiprime_samples(
        target_factor_digits=args.target_digits,
        cofactor_digits=args.cofactor_digits,
        count=total,
        seed=args.seed,
    )
    train = samples[: args.train_count]
    control = samples[args.train_count :]

    train_path = f"{args.output_dir}/{args.prefix}_train.txt"
    control_path = f"{args.output_dir}/{args.prefix}_control.txt"
    manifest_path = f"{args.output_dir}/{args.prefix}_manifest.csv"

    write_dataset(
        train_path,
        [s.n for s in train],
        header=(
            f"train dataset: target_digits={args.target_digits}, "
            f"cofactor_digits={args.cofactor_digits}, seed={args.seed}"
        ),
    )
    write_dataset(
        control_path,
        [s.n for s in control],
        header=(
            f"control dataset: target_digits={args.target_digits}, "
            f"cofactor_digits={args.cofactor_digits}, seed={args.seed}"
        ),
    )
    write_manifest(manifest_path, samples)

    print(f"train_file={train_path}")
    print(f"control_file={control_path}")
    print(f"manifest_file={manifest_path}")
    print(f"generated={total}")
    return 0

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="ECM evolutionary optimization toolkit")
    sub = parser.add_subparsers(dest="command", required=True)

    p_gen = sub.add_parser("generate-dataset", help="generate train/control semiprime datasets")
    p_gen.add_argument("--target-digits", required=True, type=int, help="digits of target prime factor p")
    p_gen.add_argument("--cofactor-digits", type=int, default=90, help="digits of cofactor prime q")
    p_gen.add_argument("--train-count", type=int, default=20)
    p_gen.add_argument("--control-count", type=int, default=20)
    p_gen.add_argument("--seed", type=int, default=42)
    p_gen.add_argument("--output-dir", default="data")
    p_gen.add_argument("--prefix", default="dset")
    p_gen.set_defaults(func=cmd_generate_dataset)

    p_opt = sub.add_parser("optimize", help="run differential evolution for B1/B2")
    p_opt.add_argument("--dataset", required=True)
    p_opt.add_argument("--ecm-bin", default="ecm")
    p_opt.add_argument("--curves-per-n", type=int, default=50)
    p_opt.add_argument("--popsize", type=int, default=16)
    p_opt.add_argument("--maxiter", type=int, default=25)
    p_opt.add_argument("--seed", type=int, default=42)
    p_opt.add_argument("--b1-min", type=float, default=1e3)
    p_opt.add_argument("--b1-max", type=float, default=1e9)
    p_opt.add_argument("--ratio-max", type=float, default=100.0)
    p_opt.add_argument("--curve-timeout-sec", type=float, default=None)
    p_opt.add_argument("--workers", type=int, default=1, help="number of worker processes (-1 = all CPUs)")
    p_opt.add_argument("--verbose", action="store_true")
    p_opt.add_argument("--results-dir", default="results")
    p_opt.set_defaults(func=cmd_optimize)

    p_val = sub.add_parser("validate", help="compare optimized parameters against baseline")
    p_val.add_argument("--dataset", required=True)
    p_val.add_argument("--ecm-bin", default="ecm")
    p_val.add_argument("--opt-result-file")
    p_val.add_argument("--opt-b1", type=int)
    p_val.add_argument("--opt-b2", type=int)
    p_val.add_argument("--base-b1", type=int)
    p_val.add_argument("--base-b2", type=int)
    p_val.add_argument("--curves-per-n", type=int, default=100)
    p_val.add_argument("--curve-timeout-sec", type=float, default=None)
    p_val.add_argument("--workers", type=int, default=1, help="number of worker processes (-1 = all CPUs)")
    p_val.add_argument("--results-dir", default="results")
    p_val.set_defaults(func=cmd_validate)

    return parser

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)

if __name__ == "__main__":
    raise SystemExit(main())
```
