---
title: "Framework for Evaluation and Comparison of Integer Factorization Algorithms"
title_en: "Framework for Evaluation and Comparison of Integer Factorization Algorithms"
source_type: "conference"
authors: ["Duta C.-L.", "Gheorghe L.", "Tapus N."]
year: "2016"
source_link: "none"
doi: "none"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "factorization-algorithms-framework-comparison-2016.md"
---

# Content source: Framework for Evaluation and Comparison of Integer Factorization Algorithms

## Source type
Conference paper (University Politehnica of Bucharest, Romania). Appears to be from a proceedings volume; exact conference name not specified in the provided content.

## Authors affiliation
Department of Computer Science and Engineering, University Politehnica of Bucharest, Romania.

## Objective
Implement, evaluate, and compare 14 integer factorization algorithms (both special-purpose and general-purpose) for input numbers of various sizes (2 to 50 digits), and determine which algorithm is best suited for real-world applications based on experimental runtime measurements.

## Categories of factorization methods

### Special-purpose algorithms (runtime depends on properties of the number or its factors)
| Algorithm | Key characteristic | Complexity |
|-----------|-------------------|------------|
| Trial division | Divide by all primes up to √N | O(√N) bit ops |
| Fermat's method | Difference of squares: N = x² − y² | O(√N) steps (worst case) |
| Euler's method | Represent N as sum of two squares in two ways | — |
| Pollard's p−1 | Works when p−1 is B-smooth | O(B·log N / log B) |
| Pollard's Rho | Iterates polynomial modulo N | O(√p) (p = smallest factor) |
| Williams's p+1 | Uses Lucas sequences over quadratic field | — |
| Elliptic Curve Method (ECM) | Group of points on random elliptic curve | L_p[1/2, 1] (heuristic) |

### General-purpose algorithms (speed independent of factor properties)
| Algorithm | Key idea | Complexity |
|-----------|----------|------------|
| Dixon's method | Congruence of squares with factor base | O(exp(2√2·√(log n log log n))) |
| CFRAC | Uses convergents of continued fraction of √N | O(exp(√(2 log n log log n))) |
| Quadratic Sieve (QS) | Sieving quadratic residues | L_n[1/2, 1] |
| Number Field Sieve (NFS) | Uses algebraic number fields | L_n[1/3, (64/9)^{1/3}] |
| Special NFS (SNFS) | For numbers of form rᵉ ± s (r,s small) | Faster than GNFS |
| General NFS (GNFS) | For arbitrary numbers | L_n[1/3, (64/9)^{1/3}] |
| Shanks's SQUFOF | Square forms, improvement of Fermat | O(N^{1/4}) |

## Framework architecture

### Design
- Thick client application under Microsoft Windows (.NET 4 Framework)
- MVP (Model-View-Presenter) design pattern
- GUI with two groups of algorithms (special-purpose and general-purpose)
- Input options: manual entry or file upload with multiple numbers
- Output: prime factors displayed in GUI and written to text files

### Use case steps
1. Initialization: enter composite number or load file
2. Apply integer factorization methods: select specific algorithms or run all

## Experimental setup

### Hardware
- Intel Core i5-5250U, CPU 1.6 GHz
- 16 GB RAM
- Windows 8 32-bit
- Integrated video card

### Input numbers
Composite numbers from 2 to 50 digits, including:
- **Generic numbers**: randomly selected composites (e.g., 2608837, 128094161, etc.)
- **Special form numbers**: Fermat numbers, Mersenne numbers

See Table 1 in original for complete list (9 to 50 digits).

## Key results

### Special-purpose algorithms (Table 2, Figure 4)

| # digits | Trial div. | Fermat | Euler | Pollard p−1 | Pollard Rho | Williams p+1 | ECM |
|----------|------------|--------|-------|-------------|-------------|--------------|-----|
| 13 | 2.118 | 0.104 | 0.096 | 3.082 | 0.009 | 0.000? | 0.014 |
| 14 | 2.714 | 0.645 | 0.589 | 1.487 | 0.014 | 0.000? | 0.010? |
| 15 | 4.688 | 4.312 | 4.168 | 0.000 | 0.577 | 0.000? | 0.010? |
| 17 | 7.274 | 7.183 | 7.169 | 0.000 | 1.941 | 0.000? | 0.010? |
| 19 | 14.53 | 12.51 | 11.18 | 0.368 | 0.329 | 0.000? | 3.234 |
| 20 | 25.34 | 22.156 | 20.882 | 0.872 | 0.193 | 0.726 | 7.164 |
| 25 | 106.05 | 197.22 | 199.46 | 1.253 | 0.246 | 1.016 | 24.87 |
| 30 | 693.7 | 14638.0 | 4611.09 | 5722.55 | 0.519 | 678.23 | 1202.7 |
| 39 | 2543.1 | 812289.3 | 711184.2 | 0 | 11.61 | 967.92 | 456.5 |
| 40 | 2799.3 | 302461.9 | 0 | 31243.0 | 52.825 | 1020.1 | 15498.6 |
| 50 | 3609.6 | 196.64 | 0 | 53289.4 | 76864.9 | 19 | — |

**Observations:**
- **Pollard's Rho** is the fastest special-purpose algorithm for numbers up to 30–40 digits (as low as 0.009–0.5 seconds).
- **Trial division** and **Fermat's method** become infeasible above 20–25 digits.
- **ECM** performance improves with larger numbers (inverse relationship with input size). For small numbers (<40 digits), ECM is slower than Pollard Rho.
- **Pollard p−1** runtime fluctuates due to probabilistic nature (e.g., 0 seconds at 15 digits, 5722 seconds at 30 digits).

### General-purpose algorithms (Table 3, Figure 5)

| # digits | Dixon | CFRAC | QS | NFS | SNFS | GNFS | SQUFOF |
|----------|-------|-------|----|----|----|----|-------|
| 20 | 7.210 | 0.019 | 0.000? | 0.000? | 0.000? | 0.000? | 0.000? |
| 25 | 14.228 | 0.096 | 0.045 | 0.010 | 0.008 | 0.019 | 0.041 |
| 30 | 19.384 | 0.589 | 0.066 | 0.042 | 0.038 | 0.031 | 0.053 |
| 39 | 49.205 | 1.332 | 0.089 | 0.068 | 0.062 | 0.045 | 0.078 |
| 40 | 50.663 | 1.486 | 0.126 | 0.092 | 0.083 | 0.045 | 0.085 |
| 50 | 111.29 | 23.345 | 1.534 | 0.588 | 0.512 | 0.267 | 1.022 |

**Observations:**
- **Dixon's method** is the slowest (111 seconds for 50 digits).
- **CFRAC** is ~100× faster than Dixon but still much slower than QS/NFS.
- **QS, NFS, SNFS, GNFS, SQUFOF** all factor 50-digit numbers in <1.6 seconds.
- **GNFS** is the fastest general-purpose algorithm overall (0.267 seconds for 50 digits).
- Differences between QS, NFS variants, and SQUFOF are very small at this scale; GNFS shows slight advantage.

## Main conclusions

1. **Fastest special-purpose algorithm**: Pollard's Rho (for numbers <40 digits). ECM becomes competitive for larger inputs (>65 digits).
2. **Fastest general-purpose algorithm**: GNFS (overall best performance for numbers with >50 digits).
3. **General-purpose algorithms** have better performance and are best suited for practical applications such as factoring RSA numbers.
4. **Trial division** is infeasible for numbers >30 digits.
5. **Fermat's and Euler's methods** are historically interesting but not practical for large numbers.
6. **ECM performance is inverse proportional to input size** – poor for small numbers, excellent for large numbers (>65 digits).

## Limitations (explicit from source/observed)

- Maximum input size tested: **50 decimal digits**. Results for larger numbers are extrapolated or not provided.
- Hardware is modest (1.6 GHz, 32-bit Windows). Absolute times may not generalize to modern systems, but relative comparisons are informative.
- Some algorithms (e.g., Williams p+1, QS for small inputs) show "0" seconds – likely due to timer resolution or truncation.
- Pollard p−1 results show extreme fluctuations (0 seconds to 5722 seconds) due to probabilistic nature; single-run times are not statistically robust.
- Framework runs algorithms sequentially on a single core – no parallelization used.
- ECM performance claim (inverse relationship with input size) lacks theoretical justification in the paper and may be misinterpreted (ECM complexity depends on factor size, not input size).

## Practical recommendations (based on results)

| Input size | Recommended algorithm(s) |
|------------|--------------------------|
| <30 digits | Pollard's Rho, trial division (very small) |
| 30–50 digits | Pollard's Rho (special), GNFS (general) |
| 50–65 digits | ECM (becomes competitive), GNFS |
| >65 digits | GNFS, ECM (for finding small factors) |

## Related software mentioned

| Software | Algorithms included | Max digits |
|----------|---------------------|------------|
| MIRACL | Pollard Rho, p−1, p+1, ECM, MPQS | 80 |
| LiDIA | Trial division, ECM, MPQS | — |
| CALC | Pollard p−1, ECM, MPQS | 55 |
| Schulenger & Assoc. | Trial division, Pollard Rho, MPQS | 200 (rho), 100 (MPQS) |