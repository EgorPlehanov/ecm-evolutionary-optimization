---
title: "Differential Evolution: A Survey of the State-of-the-Art"
title_en: "Differential Evolution: A Survey of the State-of-the-Art"
source_type: "article"
authors: ["Das S.", "Suganthan P. N."]
year: "2011"
source_link: "unknown (provided PDF: 63__Das2011.pdf)"
doi: "10.1109/TEVC.2010.2059031"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "differential-evolution-state-of-the-art-survey-2011.md"
---

# Content source: Differential Evolution: A Survey of the State-of-the-Art

## Source type
Peer-reviewed journal article (IEEE Transactions on Evolutionary Computation, Vol. 15, No. 1, February 2011).

## Authors affiliation
- Swagatam Das — Jadavpur University, Kolkata, India
- Ponnuthurai Nagaratnam Suganthan — Nanyang Technological University, Singapore

## Objective
Provide a comprehensive survey of Differential Evolution (DE) — its basic concepts, major variants, applications to multiobjective, constrained, large-scale, and uncertain optimization, theoretical studies, and engineering applications — covering developments from 1995 to 2010.

## Core methodology (classical DE/rand/1/bin)

### Algorithm stages
1. **Initialization**: NP D-dimensional vectors uniformly random within bounds.
2. **Mutation** (DE/rand/1): V_i,G = X_r1,G + F·(X_r2,G − X_r3,G), F ∈ (0,2), typically [0.4,1].
3. **Crossover** (binomial): u_j,i,G = v_j,i,G if rand(0,1) ≤ CR or j = j_rand, else x_j,i,G.
4. **Selection**: X_i,G+1 = U_i,G if f(U_i,G) ≤ f(X_i,G), else X_i,G.

### DE family notation: DE/x/y/z
- x: base vector (rand, best, target-to-best)
- y: number of difference vectors (1, 2)
- z: crossover type (bin: binomial, exp: exponential)

**Five mutation schemes**:
- DE/rand/1: V = X_r1 + F·(X_r2 − X_r3)
- DE/best/1: V = X_best + F·(X_r1 − X_r2)
- DE/target-to-best/1: V = X_i + F·(X_best − X_i) + F·(X_r1 − X_r2)
- DE/best/2: V = X_best + F·(X_r1 − X_r2) + F·(X_r3 − X_r4)
- DE/rand/2: V = X_r1 + F·(X_r2 − X_r3) + F·(X_r4 − X_r5)

## Key variants covered

| Variant | Key feature | Reference |
|---------|-------------|-----------|
| Trigonometric mutation (TDE) | Uses fitness-weighted three-vector combination | Fan & Lampinen (2003) |
| Opposition-based DE (ODE) | Opposite points for initialization, generation jumping | Rahnamayan et al. (2008) |
| DEGL | Neighborhood-based mutation (local + global) | Das et al. (2009) |
| SaDE | Strategy adaptation (4 strategies, learning period) | Qin et al. (2009) |
| JADE | DE/current-to-pbest mutation, optional external archive | Zhang & Sanderson (2009) |
| jDE | Self-adaptive F and Cr encoded in individuals | Brest et al. (2006) |
| DESAP | Self-adaptive population size | Teo (2006) |
| CDE | Crowding DE for multimodal optimization | Thomsen (2004) |
| DynDE | Multi-population for dynamic environments | Mendes & Mohais (2005) |

## Parameter adaptation and control

### Zaharie's critical F analysis (2002)
- Without selection: E(Var(P_u)) = (2F²·p_Cr − 2p_Cr/NP + p_Cr²/NP + 1)·Var(P_x)
- Critical F_crit = √((1 − p_Cr/2)/NP)
- If F < F_crit, variance decreases even without selection pressure.

### Self-adaptation schemes
- **jDE**: F_i,G+1 = F_l + rand·(F_u − F_l) with probability τ₁ (default τ₁=0.1); CR similarly.
- **SaDE**: F ~ N(0.5, 0.3); CR ~ N(CR_m, 0.1); strategy probabilities updated every LP generations.
- **JADE**: Adaptive F based on Cauchy distribution, CR based on normal distribution.

### Rotation invariance
- DE with binomial crossover (Cr < 1) is **not** rotationally invariant.
- Only Cr = 1 (mutation-only) with constant F is rotationally invariant.
- DE/current-to-rand/1 with arithmetic recombination is rotationally invariant.

## Applications overview (Tables I-II)

| Domain | Example applications |
|--------|---------------------|
| Electrical Power Systems | Economic dispatch, optimal power flow, capacitor placement |
| Electromagnetics | Antenna array design, inverse scattering, waveguide design |
| Control Systems | System identification, PID tuning, aircraft control |
| Bioinformatics | Gene regulatory networks, microarray analysis, protein folding |
| Chemical Engineering | Process synthesis, phase equilibrium, parameter estimation |
| Pattern Recognition | Data clustering, image segmentation, feature extraction |
| Signal Processing | Digital filter design, IIR/FIR optimization |
| Neural Networks | Training feedforward, wavelet, B-spline networks |

## Theoretical studies summary

1. **Population variance** (Zaharie, 2001-2008): DE's expected variance greater than ES.
2. **Crossover analysis** (Zaharie, 2009): Binomial vs exponential — difference mainly in distribution of mutated components; exponential more sensitive to problem size.
3. **Population dynamics** (Dasgupta et al., 2008-2009): 1-D model reveals gradient-descent type behavior; convergence rate depends on Cr.
4. **Runtime complexity**: O(NP·D·G_max) for fixed generations.
5. **Multiobjective convergence** (Xue et al., 2005): Under Gaussian initialization, MODE population mean converges to center of Pareto set.

## Comparison with other EAs

| Feature | DE | GA | ES | EP |
|---------|----|----|----|----|
| Mutation | Scaled difference of population vectors | Bit flips (binary) / Gaussian (real) | Gaussian with self-adaptation | Gaussian |
| Crossover | Binomial/exponential | One/two-point, uniform | Discrete/arithmetic | None |
| Selection | One-to-one (parent vs offspring) | Fitness-proportional + generational | (μ+λ) or (μ,λ) | Tournament |
| Parent selection | Random | Fitness-biased | Random | Random |
| Rotation invariance | Only at Cr=1 | No | Yes (with full covariance) | No |

## Drawbacks of DE (explicitly noted)
1. Poor performance on non-linearly separable functions compared to CMA-ES.
2. Weak selection pressure (unbiased parent selection) may cause inefficient exploitation.
3. Rotationally variant unless Cr=1.
4. Stagnation possible (population remains diverse but no progress).
5. No comprehensive convergence proof for general case.

## Future research directions (Section IX)
1. Rotation-based mutation (opposition-based DE already uses 180° rotation; generalize to arbitrary angles).
2. Ensemble of mutation strategies and parameter values (beyond SaDE).
3. Integration of opposition-based learning with self-adaptive DE variants.
4. Theoretical analysis (probabilistic convergence, drift analysis, Lyapunov functions).
5. Rank-based parent selection to increase selective pressure.
6. Investigation of different neighborhood topologies in DEGL.

## Conclusions
- DE is simple (4-5 lines of code), robust, and effective.
- Self-adaptive variants (jDE, SaDE, JADE) reduce parameter sensitivity.
- DE secured top ranks in multiple CEC competitions (2006 constrained, 2007 MO, 2008 large-scale, 2009 dynamic/unconstrained MO).
- Widely applied across engineering domains (3964 SCI-indexed papers 2007-2009).
- Theoretical understanding remains incomplete; many open problems.
