---
title: "The Differential Evolution Algorithm"
title_en: "The Differential Evolution Algorithm"
source_type: "book_chapter"
authors: ["Price K. V."]
year: "2005"
source_link: "unknown (provided PDF: 53__3-540-31306-0_2.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "differential-evolution-overview-and-analysis-2005.md"
---

# Content source: The Differential Evolution Algorithm

## Source type
Book chapter (likely from "Differential Evolution: A Practical Approach to Global Optimization" by Price, Storn, Lampinen).

## Author affiliation
Not specified in provided pages (assumed to be Price K. V.).

## Objective
Provide a comprehensive overview of the Differential Evolution (DE) algorithm, including its population structure, initialization, mutation, crossover, selection mechanisms, parameter control, termination criteria, and theoretical analysis of its behavior on various function classes.

## Core methodology described

### Population structure
- Current population P_x,g: Np vectors of D real-valued parameters (x_i,g).
- Mutant population P_v,g: created via differential mutation.
- Trial population P_u,g: created via crossover between target and mutant.

### Initialization
- Parameters initialized uniformly between bounds: x_j,i,0 = b_L + rand(0,1)·(b_U − b_L).
- Far initialization can shrink bounding box; may cause failure on highly multimodal functions.
- Halton point sets as alternative to random uniformity (more even distribution, similar performance).

### Mutation (DE/rand/1/bin — "classic DE")
- v_i,g = x_r0,g + F·(x_r1,g − x_r2,g)
- F ∈ (0,1+), typically <1.0.
- Indices r0,r1,r2 distinct from each other and from target index i.

### Crossover
- **Exponential crossover**: parameters inherited from mutant as long as rand_j(0,1) ≤ Cr; first failure switches to target for remaining parameters. Number of mutant parameters follows exponential distribution.
- **Binomial (uniform) crossover**: each parameter independently inherited from mutant with probability Cr, except one parameter forced from mutant. Number of mutant parameters follows binomial distribution.
- Cr ∈ [0,1] controls exploration vs exploitation.

### Selection
- One-to-one survivor selection: trial vector replaces target if f(u_i,g) ≤ f(x_i,g).
- Elitist (best-so-far retained).
- Lower selection pressure than (μ+λ) selection or large tournament sizes.

## Key theoretical results

### Zaharie's critical F analysis
- Without selection pressure, expected variance of mutant population: E(Var(P_v,g)) = (2F² + (Np−1)/Np)·Var(P_x,g).
- Critical F (variance constant): F_crit = √((1 − p_Cr/2)/(Np−1)/Np).
- For Np=50, p_Cr=0.2: F_crit ≈ 0.134. In practice F must be larger (≥0.3–0.4) to counteract selection pressure.

### Degenerate vector combinations (indices not mutually exclusive)

| Event | Process | Probability | Effect |
|-------|---------|-------------|--------|
| r1 = r2 | No mutation (uniform crossover only) | 1/Np | Duplicates base vector with probability Cr^(D−1) |
| r0 = r1 or r0 = r2 | Arithmetic recombination (line search) | 1/Np each | Two-vector linear combination |
| i = r0 | Mutation only | 1/Np | Target vector mutated, no crossover |
| i = r1 or i = r2 | None | 1/Np each | No reduction to conventional process |

- Allowing r1=r2 degrades performance (wastes evaluations).
- Allowing r0=r2 (contractive mapping) speeds convergence.
- Enforcing mutually exclusive indices (i≠r0≠r1≠r2) is recommended for reliability and speed.

### Rotation invariance
- Crossover (Cr<1) is **not** rotationally invariant — performance depends on coordinate system orientation.
- Only mutation-only (Cr=1) with constant F or dither is rotationally invariant.
- Jitter (per-parameter random F) breaks rotational invariance; small jitter (d≈0.001) mitigates penalty.

### Computational complexity
- Decomposable (separable) functions: low Cr (≈0) efficient; complexity O(D·ln D).
- Non-decomposable (parameter-dependent) functions: low Cr leads to complexity up to O(D^D) — prohibitive.
- Recommendation: use Cr close to 1 for general (epistatic) problems.

### Phase portraits (K-F plane)
- Decompose three-vector linear combination into recombination component K and mutation component F.
- Successful strategies cluster on mutation axis (F) or recombination axis (K), not off-axis.
- Either/Or algorithm: randomly choose between pure mutant (probability p_F) and pure recombinant (probability 1−p_F).

## Parameter guidelines

| Parameter | Recommended range | Notes |
|-----------|-------------------|-------|
| Np | 5×D to 10×D | Larger for multimodal; optimal for 10-D sphere ~9 |
| F | 0.5–0.9 | <0.4 risks premature convergence; >1 rarely needed |
| Cr | 0–0.2 (separable) or 0.9–1 (epistatic) | Bifurcation depending on function decomposability |
| dither (uniform) | d ≈ 0.9 | Can outperform constant F on some functions |
| jitter (uniform) | d ≤ 0.001 | Small jitter can prevent stagnation |

## Limitations (explicit from source)
- Classic DE (DE/rand/1/bin) may not be optimal for all problem classes.
- Phase portrait analysis limited to specific test functions.
- Jitter with normal distribution (σ=1) performed poorly on non-separable multimodal functions (Chebyshev: >6 million evaluations vs 35k for dither).
- Theoretical convergence proof requires Gaussian mutation (Zaharie) — not satisfied by classic DE with constant F.
- Far initialization (h≤0.01) causes DE to fail on Ackley, Rastrigin, Schwefel functions.

## Practical conclusions
1. For general optimization, use mutually exclusive indices (i≠r0≠r1≠r2).
2. Choose Cr based on problem structure: low for separable, high for epistatic.
3. F in [0.5, 0.9] works for most problems; avoid F<0.4.
4. Dither with uniform PDF (d≈0.9) can improve performance on some functions.
5. Very small jitter (d≈0.001) may help prevent stagnation without harming rotation invariance significantly.
6. Population size Np = 5×D to 10×D is a good starting point.
