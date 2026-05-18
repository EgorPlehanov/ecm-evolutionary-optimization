---
title: "Substantiation of correctness and advantages of Lenstra factorization method on Edwards curves"
title_en: "Substantiation of correctness and advantages of Lenstra factorization method on Edwards curves"
source_type: "article"
authors: ["Kovalchuk L.", "Bespalov O.", "Kuchynska N.", "Seliukh P.", "Zhylin A.", "Tsurkan V."]
year: "2018"
source_link: "https://doi.org/10.15587/1729-4061.2018.151090"
doi: "10.15587/1729-4061.2018.151090"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "lenstra-method-on-edwards-curves-factorization-2018.md"
---

# Content source: Substantiation of correctness and advantages of Lenstra factorization method on Edwards curves

## Source type
Journal article (Eastern-European Journal of Enterprise Technologies, Vol. 6, No. 4(96), 2018, pp. 2–9).

## Authors and affiliations
- L. Kovalchuk (Institute of Foreign Intelligence Service of Ukraine)
- O. Bespalov, P. Seliukh (National Technical University of Ukraine "Igor Sikorsky Kyiv Polytechnic Institute")
- N. Kuchynska (Institute of Foreign Intelligence Service of Ukraine)
- A. Zhylin (Department of Security of State Information Resources)
- V. Tsurkan (Department of Cybersecurity and Application of Automated Information Systems and Technologies)

## Objective
Develop a rigorous mathematical foundation for adapting Lenstra's Elliptic Curve Method (ECM) from Weierstrass curves to Edwards curves. Prove correctness, estimate speedup (≈1.5×), and derive lower bounds on success probability. Construct a detailed step-by-step algorithm for ECM on Edwards curves.

## Core mathematical contributions

### Theorem 2 — Existence of complementary points on Edwards curves
For any point \((x_1, y_1) \in E_p\) on the Edwards curve \(x^2 + y^2 = 1 + d x^2 y^2\) over \(\mathbb{F}_p\) with \(d \in Q_p\) (quadratic residue), there exists \((x_2, y_2) \in E_p\) such that:
\[
d \cdot x_1 x_2 y_1 y_2 \equiv 1 \pmod{p}
\]
Similarly, there exists a point satisfying \(\equiv -1 \pmod{p}\).

**Proof sketch**: Construct \(U = (x_1 + y_1)^2 / (d x_1^2 y_1^2)\), \(V = (x_1 - y_1)^2 / (d x_1^2 y_1^2)\). Since \(d\) is a quadratic residue, \(U, V\) are squares. Set \(A = \sqrt{U}\), \(B = \sqrt{V}\), then \(x_2 = (A+B)/2\), \(y_2 = (A-B)/2\) satisfy the condition.

**Consequence**: For composite \(n = p \cdot q\) with \(\left(\frac{d}{n}\right) = -1\), either \(d \bmod p\) or \(d \bmod q\) is a quadratic residue. Thus, there exist points \(P_1, P_2\) on \(E_n\) such that the denominator of \(P_1 + P_2\) is divisible by the corresponding prime factor — a new success condition not present in Weierstrass ECM.

### Theorem 3 — Chinese remainder theorem structure of Edwards curves over rings
For \(n = p \cdot q\), the mapping
\[
f: E_n \to (E_n \bmod p) \times (E_n \bmod q),\quad f(P) = (P \bmod p, P \bmod q)
\]
is a **bijection**. The proof uses the Chinese Remainder Theorem to reconstruct \((x, y) \bmod n\) from \((x_p, y_p)\) and \((x_q, y_q)\). This is essential for proving that a point is a neutral element modulo \(p\) but not modulo \(n\).

### Theorem 4 — Condition for non-trivial GCD
If for some \(k \in \mathbb{N}\) the order of \(P \bmod p\) divides \(k\), then the denominators of the coordinates of \(kP\) have a common divisor with \(n\) greater than 1. Equivalently, \(k(P \bmod p) = (0, 1)\) (neutral element in \(E_n \bmod p\)), so the \(x\)-coordinate of \(kP\) is divisible by \(p\).

## Edwards curve group law

For \(x^2 + y^2 = 1 + d x^2 y^2\) with \(e = 1\) (full Edwards curve), point addition is unified:
\[
(x_1, y_1) + (x_2, y_2) = \left( \frac{x_1 y_2 + x_2 y_1}{1 + d x_1 x_2 y_1 y_2}, \frac{y_1 y_2 - x_1 x_2}{1 - d x_1 x_2 y_1 y_2} \right)
\]
- Neutral element: \((0, 1)\)
- Group is cyclic
- Order divisible by 4
- Addition law is **complete** (no special cases for doubling or identity)

## Algorithm 3 — Lenstra method on Edwards curves

**Input**: Composite \(n\)

**Step 1**: Choose random \(x_0, y_0 \in [2, n-1]\).

**Step 2**: Compute \(D_1 = \gcd(x_0, n)\), \(D_2 = \gcd(y_0, n)\). If \(1 < D_i < n\), return \(D_i\).

**Step 3**: Compute \(t = x_0^2 + y_0^2 - 1\).

**Step 4**: Compute \(D_3 = \gcd(t, n)\). If \(1 < D_3 < n\), return \(D_3\).

**Step 5**: If Jacobi symbol \(\left(\frac{t}{n}\right) = 1\), go to Step 1 (different \(x_0, y_0\)).

**Step 6**: Compute \(d = t \cdot (x_0^2 y_0^2)^{-2} \bmod n\).

**Step 7**: Define Edwards curve \(\widetilde{E}_n: x^2 + y^2 = 1 + d x^2 y^2\) and point \(P = (x_0, y_0)\).

**Step 8**: Choose \(k = \prod_{p \le B_1} p^{\lfloor \log B_1 / \log p \rfloor}\) (product of prime powers up to bound \(B_1\)).

**Step 9**: Compute \(kP\) using Horner's scheme (repeated doubling and addition via unified Edwards addition law). At each addition of \(P_1\) and \(P_2\), compute:
\[
D_4 = \gcd(1 + d x_1 y_1 x_2 y_2, n),\quad D_5 = \gcd(1 - d x_1 y_1 x_2 y_2, n)
\]
\[
D_6 = \gcd(x_1 y_2 + x_2 y_1, n),\quad D_7 = \gcd(y_1 y_2 - x_1 x_2, n)
\]

**Step 10**: If any \(1 < D_i < n\), return \(D_i\).

**Step 11**: If no factor found, restart with new \(x_0, y_0\) or larger \(k\).

## Key advantages over Weierstrass ECM

| Feature | Weierstrass ECM | Edwards ECM | Speedup |
|---------|----------------|-------------|---------|
| Point addition cost | ~16 multiplications | ~10 multiplications | ~1.6× |
| Point doubling cost | ~10 multiplications | ~6 multiplications | ~1.67× |
| Unified addition | No (separate doubling) | Yes (same formula) | Side-channel resistance |
| Neutral element | Point at infinity (no coordinates) | (0, 1) (regular point) | Easier to detect |
| Extra success conditions | Only via smooth order | Also via quadratic residue property (Theorem 2) | Higher probability |

**Claimed speedup**: At least 1.5× compared to Weierstrass ECM.

## Probability of success (theoretical)

The classic Lenstra method success probability is approximately:
\[
P_{\text{Weierstrass}} \approx \rho(\alpha) \quad \text{where} \quad \alpha = \frac{\log p}{\log B_1}
\]

For Edwards curves, additional success conditions from Theorem 2 increase the probability. The paper states:

> "The probability of success of the constructed algorithm is higher than that of the classic Lenstra method."

Specifically, the algorithm succeeds when either:
1. The order of \(P \bmod p\) divides \(k\) (classic condition), or
2. The denominator of a point addition becomes zero modulo \(p\) due to the quadratic residue property (Theorem 2).

## Time complexity estimate

The number of point additions is \(O(\log k)\), same as Weierstrass ECM. However, each addition is ~1.5× faster. Therefore:

\[
T_{\text{Edwards}} \approx \frac{2}{3} T_{\text{Weierstrass}}
\]
or better (claimed "at least 1.5 times more efficient").

## Experimental results (on full vs twisted/quadratic Edwards curves)

The authors performed experiments on standard data types (not large RSA moduli) comparing full Edwards curves with twisted and quadratic Edwards curves:

| Curve type | Relative steps to success | Speedup vs full Edwards |
|------------|---------------------------|-------------------------|
| Full Edwards | 1.00 (baseline) | 1.0× |
| Twisted Edwards | 0.70–0.80 | 1.25–1.43× |
| Quadratic Edwards | 0.70–0.80 | 1.25–1.43× |

**Conclusion**: Twisted/quadratic Edwards curves reduce the average number of steps by 20–30%, further improving performance beyond the 1.5× gain over Weierstrass.

## Relationship to prior work

- Builds on Bernstein et al. (2012) "ECM using Edwards curves" — experimental results only.
- Extends by providing **rigorous proofs** of correctness and success conditions.
- Uses Bessalov (2017) results on Edwards curve isomorphism conditions.
- Theorem 1 from Bespalov & Kuchynska (2017) on Edwards curves over residue rings.

## Limitations (explicit)

1. **Analytical estimates for twisted/quadratic curves not yet obtained** — only experimental results presented.
2. **Experiments performed on "standard data types"** (not specified; likely small numbers), not large RSA moduli.
3. **No explicit numerical comparison** with GMP-ECM or other state-of-the-art implementations.
4. **No discussion of stage 2** (baby-step giant-step or FFT continuation) — only stage 1 considered.
5. **Proofs assume \(e = 1\) in Edwards equation** — generalization to arbitrary \(e\) not given.
6. **Jacobi symbol condition in Step 5** requires computing \(\left(\frac{t}{n}\right)\), which for composite \(n\) is the Jacobi symbol (not Legendre). The paper does not discuss the case when the Jacobi symbol is 0.
