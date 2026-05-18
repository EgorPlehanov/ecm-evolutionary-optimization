---
title: "Recent Progress and Prospects for Integer Factorisation Algorithms"
title_en: "Recent Progress and Prospects for Integer Factorisation Algorithms"
source_type: "article"
authors: ["Brent R. P."]
year: "2000"
source_link: "https://doi.org/10.1007/3-540-44683-4_1"
doi: "10.1007/3-540-44683-4_1"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "recent-progress-and-prospects-for-integer-factorisation-2000.md"
---

# Content source: Recent Progress and Prospects for Integer Factorisation Algorithms

## Source type
Conference paper (Euro-Par 1999? Also published as Oxford University Computing Laboratory technical report, April 2000).

## Author
Richard P. Brent (Oxford University Computing Laboratory)

## Objective
Survey the state of integer factorization algorithms as of 2000, focusing on ECM (class B, run time depends on factor size), MPQS, SNFS, and GNFS (class A, run time depends on N). Discuss parallel implementations, historical records, and extrapolations to future capabilities (e.g., 1024-bit RSA). Address parallel linear algebra challenges (Lanczos, block Lanczos, distributed computation).

## Key factorization records as of April 2000

| Method | Number | Digits | Year | Notes |
|--------|--------|--------|------|-------|
| ECM | Factor of (6⁴³−1)⁴²+1 | 54 | 1999 | Largest ECM factor (Lygeros & Mizony) |
| MPQS | RSA129 | 129 | 1994 | Factored by Atkins et al. |
| SNFS | 10²¹¹−1 | 211 | 1999 | Factored by "The Cabal" |
| GNFS | RSA155 | 155 (512 bits) | 1999 | 8000 Mips-years, 8.7×10⁶ matrix rows |

## ECM: analysis and extrapolation (Section 3)

### ECM record growth (Figure 1)
- 1991: 40 digits
- 1995: 40–44 digits? (F₁₀ factor: 40 digits)
- 1999: 54 digits

**Extrapolation (Figure 2)**: √D = (Y − 1932.3)/9.3
- D = 60 digits predicted for Y = 2004
- D = 70 digits predicted for Y = 2010

**Group order divisibility**: Suyama's parametrization ensures group order divisible by 12 → effectively reduces p to p/12.

### Parallel ECM
Linear speedup (independent trials). Expected parallel time:
\[
T_P = T_1 / P + O(T_1^{1/2 + \varepsilon})
\]

## MPQS (Section 4)

### One large prime (P-MPQS) and two large primes (PP-MPQS)
- PP-MPQS gives significant performance improvement at cost of higher storage.
- Sieving stage ideally suited to parallelization (linear speedup).

### RSA129 (1994)
- 569,466 columns after relation collection
- Reduced to 188,614 dense matrix
- Solution on MasPar MP-1
- Estimated 5000 Mips-years (vs RSA130 GNFS: 1000 Mips-years)

## SNFS (Section 5)

### Example: F₉ = 2⁵¹² + 1
- Degree d=5, m=2¹⁰³
- Norms: |u⁵ − 8v⁵| ≈ N^{1/d}
- Factored June 1990: p₇·p₄₉·p₉₉

### Record (1999): 10²¹¹−1 (211 digits)

## GNFS (Section 6)

### Polynomial selection (Murphy 1999)
Base-m method: m = ⌊N^{1/(d+1)}⌋, N = Σ aⱼ mʲ, g(x) = Σ aⱼ xʲ, f(x) = x − m.
Improved selection (Montgomery–Murphy) reduces coefficients, increases yield.

### Optimal degree:
\[
d \sim \left( \frac{3\ln N}{\ln\ln N} \right)^{1/3}
\]

### RSA155 factorisation (August 1999)

**Polynomials** (degree 5):
f(x) = x − 3912307972116800077131449081
g(x) = +119377138320x⁵ − 80168937284997582x⁴ − 66269852234118574445x³ + 11816848430079521880356852x² + 7459661580071786443919743056x − 40679843542362159361913708405064

**Statistics** (Table 1):

| | RSA130 | RSA140 | RSA155 |
|---|--------|--------|--------|
| Digits | 130 | 140 | 155 |
| Total CPU (Mips-years) | 1000 | 2000 | 8000 |
| Matrix rows | 3.5×10⁶ | 4.7×10⁶ | 6.7×10⁶ |
| Nonzeros per row | 39 | 32 | 62 |
| Nonzeros total | 1.4×10⁸ | 1.5×10⁸ | 4.2×10⁸ |
| Matrix solution time (Cray C90/C916) | 68 h | 100 h | 224 h |

### Square root stage
Montgomery (1994) found method to compute square root of product of algebraic numbers.

## Parallel linear algebra (Section 7)

### Lanczos/block Lanczos (Montgomery 1995)
- Solves A x = b where A = RᵀR (normal equations)
- Main work: compute A w = Rᵀ(R w) ≈ ρ n operations per iteration
- Problem: communication overhead for distributed implementation

### Distributed sparse matrix-vector multiplication
- P = q² processors, matrix R distributed with scattered data distribution.
- Local storage: O(ρ n / q² + n / q)
- Communication: O(n) bits per iteration along rows/columns.
- Efficiency:
\[
E_P \approx \frac{\alpha \rho}{\alpha \rho + \beta P}
\]
where β/α is communication/computation ratio (50–500).

**For RSA155**: n = 6.7×10⁶, ρ ≈ 62, n² ≈ 4.5×10¹³. Communication dominates unless P < 600.

### Pre-elimination to reduce communication
Eliminate relations with large primes using single processor. Can reduce n (hence communication) at expense of increasing weight (storage).

**Example** (c₁₀₂, PP-MPQS): n reduced from 73,000 to 32,000 (56% reduction), weight increased 76%, communication reduced 81%.

## Historical factoring records (Section 8)

**General numbers** (Figure 3):
- 1964: 20 digits (trial division? CFRAC?)
- 1970: 22 digits? (F₇ factor)
- 1980: 50 digits? (F₈ factor)
- 1990: 100 digits? (F₉)
- 1999: 155 digits (RSA155)

**Extrapolation for 1024-bit RSA (309 digits)** (Figure 4):
\[
D^{1/3} = \frac{Y - 1928.6}{13.24} \quad \Rightarrow \quad Y \approx 13.24 \cdot D^{1/3} + 1928.6
\]
For D=309, D^{1/3}≈6.76 → Y≈1928.6+13.24·6.76≈1928.6+89.5≈**2018**.

> "1024-bit RSA keys should remain secure for at least fifteen years, barring the unexpected (but unpredictable) discovery of a completely new algorithm which is better than GNFS, or the development of a practical quantum computer."

## Conclusions (2000)

| System | Security status |
|--------|-----------------|
| 512-bit RSA | Already insecure |
| 1024-bit RSA | Secure until ≈2018 (barring breakthroughs) |
| ECC | Promising long-term alternative |

## Extrapolation vs actual (post-2000)

| Prediction (2000) | Actual |
|-------------------|--------|
| D=60 ECM factor by 2004 | 2005: 66-digit factor (F₁₀ cofactor) |
| D=70 ECM factor by 2010 | 2013: 73-digit factor? Actually 67-digit record stood until 2013? 2013: 73-digit (Suyama) |
| 1024-bit RSA by 2018 | Not factored as of 2026 (768-bit factored 2010) |

## Limitations (explicit in paper)

1. **Heuristic assumptions** for smoothness probabilities (Dickman function) — not rigorously proven.
2. **Moore's law extrapolation** assumes continuation of historical trends; may fail due to physical limits.
3. **Communication/computation ratio** β/α is highly implementation and hardware dependent.
4. **Pre-elimination strategy** can cause "explosion" (matrix becomes dense) if pushed too far.
5. **Quantum computer** threat acknowledged but considered speculative.
6. **No details on block Wiedemann** — only Lanczos discussed.

## Relation to other work

- Builds on Brent (1999) survey of parallel integer factorization.
- ECM records from Zimmermann's ECMNET.
- RSA challenge factorizations (RSA130/140/155) from CWI team (te Riele et al.).
- Block Lanczos for GF(2) from Montgomery (Eurocrypt 1995).
- Polynomial selection from Murphy's PhD thesis (1999).
