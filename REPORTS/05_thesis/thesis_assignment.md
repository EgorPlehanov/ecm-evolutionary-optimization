---
title: "Master's Thesis Assignment: Automation of ECM Parameter Selection Using Heuristic Optimization Methods"
source_file: "Плеханов_Задание_на_ВКР.docx"
language: "ru"
converted_on: "2026-05-12"
---

# Master's Thesis Assignment

## Ministry of Science and Higher Education of the Russian Federation
### Peter the Great St. Petersburg Polytechnic University
#### Institute of Computer Science and Cybersecurity
##### Higher School of Artificial Intelligence Technologies

---

| | |
|---|---|
| **APPROVED BY** | |
| **Program Director** | |
| **V.G. Pak** | |
| "___" ___________ 2026 | |

---

## ASSIGNMENT
### for the Completion of the Final Qualifying Work (Master's Thesis)

| Field | Value |
|-------|-------|
| **Student** | Plekhanov Egor Sergeevich, group 5140203/40101 |

---

### 1. Thesis Title

> **"Automation of Parameter Selection for the Elliptic Curve Factorization Algorithm Using Heuristic Optimization Methods."**

---

### 2. Submission Deadline

> **May 2026**

---

### 3. Initial Data for the Work

- Scientific publications on the Elliptic Curve Method (ECM), including works by Lenstra H.W., Zimmermann P., Silverman R.D., Brent R.P.;
- Documentation and source code of the GMP-ECM library;
- Descriptions of heuristic optimization methods (differential evolution, genetic algorithms).

---

### 4. Content of the Work (List of Topics to Be Developed)

- Conducting an analytical review of elliptic curve factorization methods and existing approaches to selecting parameters $B_1$ and $B_2$;
- Review of heuristic optimization methods, justification for selecting the class of algorithms (evolutionary methods) for solving the problem;
- Formalization of the parameter optimization problem as a "black box" problem and development of efficiency criteria;
- Mathematical formulation of the optimization problem: selection of the objective function (expected factorization time), construction of the constraint system, and justification of the applicability of heuristic methods;
- Architectural design and development of a software system in Python for automated ECM parameter selection using heuristic methods;
- Conducting computational experiments on parameter optimization for divisors of various sizes;
- Statistical analysis and comparison of the obtained results with reference GMP-ECM tables;
- Robustness analysis of the found parameters on various classes of numbers (RSA-like, Mersenne numbers);
- Formulation of conclusions and recommendations for application of the proposed method.

---

### 5. List of Graphic Materials (Indicating Mandatory Drawings)

- ECM algorithm flowchart;
- Component diagram of the developed software system;
- Comparison tables of optimized and reference parameters;
- Histograms of expected factorization time distribution;
- Diagrams comparing efficiency on different number types.

---

### 6. List of Information Technologies Used, Including Software, Cloud Services, Databases, and Other Cross-cutting Digital Technologies (if applicable)

- Python 3.10+ programming language;
- NumPy, SciPy libraries (implementation of heuristic optimization algorithms);
- External GMP-ECM library (factorization);
- Development environment: Visual Studio Code / Jupyter Notebook;
- Git version control system.

---

### 7. Consultants for the Work

> Not applicable.

---

### 8. Date of Assignment Issue

> **February 25, 2026**

---

## Signatures

| Role | Signature | Name |
|------|-----------|------|
| **Thesis Supervisor** | _________ | Pak V.G. |
| **Student (Assignment Accepted)** | _________ | Plekhanov E.S. |

**Date of acceptance:** February 25, 2026

---

## Potential issues

- **Missing approval date:** The approval date line for the Program Director is left blank in the original document (shown as "\_\_\_").
- **No signatures:** The signature lines are empty in the source document.
- **Minor formatting:** Underlined text in the original (e.g., student name, title) has been converted to standard Markdown formatting using blockquotes and proper headers.
- **Graphic materials:** No actual images/figures are present in the document; only a list of required graphic materials is provided.

**Converted successfully**