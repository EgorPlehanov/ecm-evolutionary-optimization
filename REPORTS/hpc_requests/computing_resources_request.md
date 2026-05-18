---
title: "HPC Center Computing Resources Request – ECM Parameter Optimization"
source_file: "Plehanov-scc_resource.docx"
language: "ru"
converted_on: "2026-05-12"
---

# Computing Resources Request

| № | Parameter | Value |
|---|-----------|-------|
| 1 | **Project name** | Optimization of Elliptic Curve Method (ECM) parameters using heuristic methods |
| 1.1 | **Project classification** | Initiative |
| 1.2 | **Project registration number at SPbPU** | — |
| 1.3 | **Project goal** | Development and experimental verification of a method for automated selection of parameters B₁ and B₂ of the Elliptic Curve Method (ECM) factorization algorithm using heuristic optimization methods to reduce the expected factorization time on supercomputer systems |
| 1.4 | **Project supervisor** | Pak Vadim Gennadievich, Associate Professor at HSTII, Candidate of Physical and Mathematical Sciences |
| 2 | **Mathematical characteristics of tasks** | Numerical modeling of probabilistic factorization algorithms, statistical processing of results, parameter optimization using heuristic methods (evolutionary algorithms) |
| 3 | **Task type** | Data processing |
| 4 | **For third-party applications used "as is" – manufacturer, name, version** | GMP-ECM (factorization library), LGPL license; Python 3.10+, NumPy, SciPy (all Open Source) |
| 5 | **Program organization model** | Sequential (launching multiple independent tasks through queue system) |
| 6 | **List of required development tools: compilers, debuggers, libraries** | GCC compilers (for building GMP-ECM), Python 3.10+, libraries: GMP, MPFR, NumPy, SciPy |
| 7 | **Computing system whose resources are intended to be used** | "Polytechnik - RSK Tornado" |
| 8 | **Number of required compute nodes (virtual machines, VMs)** | Minimum: 1, Maximum: 4 |
| 9 | **RAM volume (per 1 core, per node, per VM)** | Per core: 2–4 GB, per node: 64 GB |
| 11 | **Estimated intensity of resource usage (hours per month)** | Maximum: 1000 |
| 12 | **Special data security requirements** | — |

| Role | Signature | Date |
|------|-----------|------|
| **Group supervisor** | _______________ | _______________ |
