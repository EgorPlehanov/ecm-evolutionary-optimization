---
title: "A Study on the Limitations of Evolutionary Computation and other Bio-inspired Approaches for Integer Factorization"
title_en: "A Study on the Limitations of Evolutionary Computation and other Bio-inspired Approaches for Integer Factorization"
source_type: "conference"
authors: ["Mishra M.", "Gupta V.", "Chaturvedi U.", "Shukla K. K.", "Yampolskiy R. V."]
year: "2015"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "limitations-of-evolutionary-computation-for-factorization-2015.md"
---

# Content source: A Study on the Limitations of Evolutionary Computation and other Bio-inspired Approaches for Integer Factorization

## Source type
Conference paper (2015 International Conference on Soft Computing and Software Engineering, SCSE 2015). Published in Procedia Computer Science, Vol. 62, pp. 603–610, Elsevier B.V.

## Authors affiliation
- Mishra, Gupta, Chaturvedi, Shukla — Dept. of Computer Science and Engineering, Indian Institute of Technology (BHU) Varanasi, India.
- Yampolskiy — Dept. of Computer Engineering and Computer Science, University of Louisville, KY, USA.

## Objective
Critically analyze evolutionary computation and other bio‑inspired approaches (genetic algorithms, swarm intelligence, neural networks) applied to the integer factorization problem, identify fundamental limitations, and explain why these methods fail to scale to cryptographically relevant semi‑primes.

## Core content summary

### 1. Problem context
- Integer factorization (especially semi‑primes N = p·q with p,q ≈ √N) is a one‑way function: easy to compute N from p,q, hard to invert.
- No polynomial‑time classical algorithm exists; best known is GNFS with complexity O(exp((64/9)^{1/3} (log N)^{1/3} (log log N)^{2/3})).
- RSA‑768 (232 digits) factored by Lenstra et al. (2010) using GNFS with hundreds of machines over 2 years.

### 2. Classification of factoring approaches
1. **Special form** — exploits structure of N or its factors.
2. **General form** — runtime depends only on size of N (QS, NFS).
3. **Alternative form** — genetic algorithms, neural networks, meta‑heuristics, swarm intelligence, oracles.

This paper focuses on category 3.

### 3. Genetic algorithm approach (Yampolskiy 2010 and authors' variant)

**Chromosome representation**: concatenation of candidate factors p and q (equal digit length assumed, worst‑case semi‑primes).

**Fitness function (Yampolskiy)**: similarity of digits between N and p·q.

**Authors' modification**: weight digits by position (less significant digits weighted more). Crossover between fittest and weakest; mutation on fittest members (rate > crossover rate).

**Critical flaw identified**:
- Example: N = 437 = 19·23.
- Candidate (p,q) = (06,73) gives 06·73 = 438 → fitness very high (product close to N in digits).
- Candidate (18,22) gives 396 → lower fitness.
- But (06,73) is far from actual factors (19,23); (18,22) is much closer.
- Fitness function rewards digit‑wise similarity, not proximity to true factors.
- High mutation rate reduces to random search.
- **Conclusion**: Missing selection pressure; method does not converge reliably.

### 4. Objective functions for discrete optimization

#### Function 1: Congruence of squares
\[
\text{minimize } f(x,y) = (x^2 - y^2) \bmod N,\quad x,y \in [2,N-1],\quad (x \pm y) \bmod N \neq 0
\]

**Observations** (Figs. 1–2, N=35):
- Multiple solutions exist.
- Surface is chaotic with sharp drops and steep slopes → many local minima.
- Mean standard deviation ≈ mean function evaluation → no reliable direction.

**Used successfully by Mishra et al. (2014) with Molecular Geometry Optimization, but still highly dependent on chance.**

#### Function 2: Modular remainder
\[
\text{minimize } f(x) = N \bmod x,\quad x \in [2,\sqrt{N}]
\]

**Properties** (Figs. 3–4, N=4757):
- Exactly one global minimum at x = p (or q).
- Search space reduced to \(\sqrt{N}\) (≈ \(10^{n/2}\) for n‑digit N).
- Still suffers from sharp edges, steep slopes, many local minima.
- No reliable gradient information.

#### Function 3: Logarithmic difference (proposed by authors)
\[
\text{minimize } f(x,y) = |\log N - \log x - \log y|,\quad x \in [2,\sqrt{N}],\; y \in [\sqrt{N},N]
\]

**Properties** (Fig. 5, N=41·19 and 131·263):
- Smooth contour, fewer sharp edges.
- Provides selection pressure.
- Search space: x ~ \(10^{n/2}\), y ~ \(10^{n/2}\) (combined ~\(10^n\) combinations).
- Domain size for log x is O(n) if log x treated as variable → potential for gradient‑based methods.
- Accuracy still a concern.

### 5. Error function formulation (Section 5)

Given approximate factors p,q with errors x,y (P = p + x, Q = q + y, N = PQ):

\[
qx + py + xy = N - pq
\]

**Unconstrained formulation**:
\[
\text{minimize } |qx + py + xy + pq - N|
\]

**Constraints**:
- p + x ≤ √N, q + y ≥ √N.
- If approximations are close, domain for x,y is small.

But "closeness" requires a measure → circular dependency.

### 6. Reducing search space by multiple equations (Section 6)
- Multiply N by small primes S: NS = P·Q·S.
- Evolve P simultaneously across multiple equations → more constraints → narrower search space.
- Still requires good fitness function; GA flaw persists.

### 7. Information‑theoretic critique (Section 7, based on Dembski & Marks 2009)

**Definitions**:
- Endogenous information \(I_{\text{in}} = -\log(\text{probability by blind search})\).
- Exogenous information \(I_s = -\log(\text{probability given problem‑specific structure})\).
- Active information \(I_+ = I_s - I_{\text{in}}\) (information injected by heuristic).

**Case 1**: Random search for both factors (blind):
\[
p = \frac{1}{N} \cdot \frac{1}{N} = \frac{1}{N^2},\quad I_{\text{in}} = 2\log N
\]

**Case 2**: Search for one factor using f(x) = N mod x (domain [2,√N]):
\[
q = \frac{1}{\sqrt{N}},\quad I_s = \frac{1}{2}\log N,\quad I_+ = -\frac{3}{2}\log N \text{ (actually }0.5\log N\text{ by their calculation)}
\]
(Correction in paper: \(I_+ = 0.5\log N\) for Eq. (10).)

**Case 3**: Congruence of squares with m solutions:
\[
q \approx \frac{8m}{(N-1)(N-3)},\quad I_s \approx 2\log N - \log(8m),\quad I_+ = \log(8m)
\]
m unknown → active information unknown.

**Conclusion**: The effectiveness of bio‑inspired methods depends entirely on how much problem‑specific structure (active information) they exploit. For integer factorization, existing heuristics provide very little active information relative to blind search.

### 8. Main conclusions

1. **All‑or‑nothing nature**: Either a candidate divides N or it does not. No partial credit heuristic can reliably guide search.
2. **No gradient / selection pressure**: Fitness functions based on digit similarity or modular remainder produce chaotic landscapes with many local maxima/minima.
3. **Scaling impossible**: Even for N ~ \(10^{14}\), evolutionary methods struggle; cryptographically relevant N ~ \(10^{300}\) are astronomically out of reach.
4. **Active information deficit**: The amount of heuristic information injected by existing bio‑inspired methods is negligible compared to blind search.
5. **Future breakthroughs** would require new number‑theoretic heuristics, not just better optimization algorithms.

## Key observations from experimental data

| N | Factors | Method | Observation |
|---|---------|--------|-------------|
| 437 | 19·23 | GA (digit similarity) | (06,73) → 438 (high fitness) but far from solution. |
| 4757 | 67·71 | f(x)=N mod x | Many local minima; sharp edges. |
| 41·19, 131·263 | various | f(x,y)=|log N−log x−log y| | Smoother contours, potential for gradient. |

## Limitations of bio‑inspired approaches (explicit from paper)

- Cannot guarantee convergence to global optimum.
- Mean standard deviation ≈ mean function evaluation → no consistent improvement over random search.
- High mutation rate degrades to random search.
- Digit‑similarity fitness is deceptive (rewards digit‑wise matches, not factor proximity).
- Modular remainder function has O(√N) local minima.
- Even "smooth" logarithmic function requires high precision to distinguish close candidates.

## Theoretical implications

The paper applies **Dembski–Marks conservation of information** (2009) to argue:
- Any search algorithm's performance is bounded by the active information available.
- For factorization, known heuristics provide at most O(log N) active information vs. O(N²) blind search.
- Thus bio‑inspired methods cannot bridge the exponential gap to polynomial‑time factoring.

## Practical recommendations (implicit)

- For factoring cryptographically sized semi‑primes, stick to GNFS/ECM.
- Evolutionary methods may be useful for toy problems (N < \(10^{15}\)) but not for real RSA moduli.
- Future work should focus on number‑theoretic heuristics, not generic meta‑heuristics.
