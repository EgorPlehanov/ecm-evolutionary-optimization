---
title: "Particle Swarm Optimization"
title_en: "Particle Swarm Optimization"
source_type: "conference"
authors: ["Eberhart R. C.", "Kennedy J."]
year: "1995"
source_link: "unknown (provided PDF: 59__Particle_swarm_optimization.pdf)"
doi: "none"
language: "en"
converted_on: "2026-05-17"
suggested_filename: "particle-swarm-optimization-introduction-1995.md"
---

# Content source: Particle Swarm Optimization

## Source type
Peer-reviewed conference paper (IEEE International Conference on Neural Networks, 1995 — as per citation context).

## Authors affiliation
Purdue School of Engineering and Technology, Indianapolis, IN, USA.

## Objective
Introduce particle swarm optimization (PSO) — a new method for optimizing continuous nonlinear functions inspired by social behavior of bird flocks and fish schools — and demonstrate its effectiveness on benchmark functions and neural network training.

## Core methodology development

### Origins: Simulation of social behavior
- Inspired by Reynolds' bird flocking simulation and Heppner & Grenander's models.
- Key insight from Wilson (1975): social sharing of information among conspecifics offers evolutionary advantage — individuals can profit from discoveries of all other members of the group.

### Evolutionary stages of the algorithm

**Stage 1: Nearest neighbor velocity matching + "craziness"**
- Population of birds (agents) on torus pixel grid with X/Y velocities.
- Each agent adopts velocity of its nearest neighbor → synchrony, but flock quickly settles on unanimous unchanging direction.
- Craziness (stochastic velocity changes) added to maintain movement.

**Stage 2: Cornfield vector (pbest + gbest)**
- Goal point at (100,100) with evaluation = Manhattan distance to goal.
- Each agent remembers its own best position (pbest) and its value.
- Global best (gbest) = best position found by any agent, available to all.
- Velocities adjusted based on whether agent is to right/left or above/below pbest and gbest.
- Result: flock swirls and eventually "lands" on target.

**Stage 3: Elimination of ancillary variables**
- Craziness removed (unnecessary).
- Nearest neighbor velocity matching removed (optimization faster without it).

**Stage 4: Multidimensional search**
- Extended to D dimensions (e.g., 13-dimensional XOR neural network training).
- Each agent tracks position and velocity vectors in D-dimensional space.

**Stage 5: Acceleration by distance (not just sign)**
- Velocity adjustment based on difference (not just inequality test):
  - vx[i] = vx[i] + rand()·p_increment·(pbestx[i] − presentx[i])

**Stage 6: Current simplified version**
- p_increment and g_increment removed (stripped out).
- Stochastic factor multiplied by 2 (mean = 1) so agents overfly target ~50% of time.
- Final velocity update formula:
  - vx[i] = vx[i] + 2·rand()·(pbestx[i] − presentx[i]) + 2·rand()·(pbestx[gbest] − presentx[i])

### Algorithm description (current simplified version)
- Population: N particles moving in D-dimensional search space.
- Each particle has: position x[i][d], velocity v[i][d], personal best pbest[i][d], and its fitness.
- Global best gbest[d] = best position found by any particle.
- Velocity update: v[i][d] = v[i][d] + φ₁·rand()·(pbest[i][d] − x[i][d]) + φ₂·rand()·(gbest[d] − x[i][d])
  (φ₁ = φ₂ = 2 in this version)
- Position update: x[i][d] = x[i][d] + v[i][d]

## Key results

### XOR neural network (2-3-1 architecture, 13 parameters)
- Average iterations to error < 0.05: 30.7 iterations with 20 particles
- Performance comparable to backpropagation

### Fisher Iris data set classification
- Particle swarm trained weights as effectively as backpropagation
- Average: 284 epochs over 10 training sessions

### EEG spike waveform classification
- Backpropagation: 89% correct on test data
- Particle swarm: 92% correct on test data (better generalization)

### Schaffer f6 function (highly nonlinear, many local optima)
- Particle swarm found global optimum every run
- Performance comparable to elementary genetic algorithms

## Conceptual principles (Millonas, 1994)

| Principle | PSO implementation |
|-----------|---------------------|
| Proximity | n-D space calculations over time steps |
| Quality | Responds to pbest and gbest (quality factors) |
| Diverse response | Allocation of responses between pbest and gbest ensures diversity |
| Stability | Changes state only when gbest changes |
| Adaptability | Changes when gbest changes (worth computational price) |

## Relationship to other methods
- **Genetic algorithms**: Adjustment toward pbest and gbest is conceptually similar to crossover.
- **Evolutionary programming**: Highly dependent on stochastic processes.
- **Artificial life**: Mid-level form between evolutionary search (eons) and neural processing (milliseconds).
- **Unique aspect**: Flying potential solutions through hyperspace, accelerating toward "better" solutions; momentum causes overshooting/exploration.

## Limitations (explicit or implied)
- Optimal value of constant factor (currently 2) not known — may need problem-specific tuning or evolution.
- Version using weighted average of pbest and gbest (single term) tended to converge on that point whether optimum or not — stochastic "kicks" necessary.
- Removing velocity momentum (replacing instead of adding) proved ineffective for global optima.
- No theoretical convergence guarantees provided (empirical only).

## Practical conclusions
1. PSO is extremely simple (few lines of code) and computationally inexpensive.
2. Requires only primitive mathematical operators.
3. Effective for continuous nonlinear function optimization and neural network weight training.
4. May generalize better than gradient descent (EEG example: 92% vs 89%).
5. Adheres to five principles of swarm intelligence (Millonas).

## Legacy significance
- One of the first publications introducing PSO (1995).
- Established PSO as a major swarm intelligence algorithm alongside genetic algorithms and evolutionary programming.
- Laid groundwork for decades of subsequent PSO research (velocity clamping, inertia weight, constriction coefficient, etc.).
