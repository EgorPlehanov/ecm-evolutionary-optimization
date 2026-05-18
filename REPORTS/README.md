# ECM Optimization – Master's Research

## Project Overview

This repository contains all documents related to the master's research of **Egor Plekhanov** (group 5140203/40101) at the Institute of Computer Science and Cybersecurity, Peter the Great St. Petersburg Polytechnic University.

**Research topic:** Automation of parameter selection for the Elliptic Curve Method (ECM) factorization algorithm using heuristic optimization methods.

**Supervisor:** Pak Vadim Gennadievich, Candidate of Physical and Mathematical Sciences, Associate Professor at HSTII.

---

## Repository Structure

```
ecm-optimization-master-research/
│
├── 01_research_internship_fall_2025/
│   ├── individual_plan_fall_2025.md
│   └── internship_report_fall_2025.md
│
├── 02_research_internship_spring_2026/
│   ├── individual_plan_spring_2026.md
│   └── internship_report_spring_2026.md
│
├── 03_technological_internship_spring_2026/
│   ├── individual_plan_technological_spring_2026.md
│   └── internship_report_technological_spring_2026.md
│
├── 04_pre_graduation_internship_spring_2026/
│   ├── individual_plan_pre_graduation_spring_2026.md
│   └── internship_report_pre_graduation_spring_2026.md          # (pending)
│
├── 05_thesis/
│   ├── thesis_assignment.md
│   ├── thesis_structure_requirements.md
│   └── thesis_text.md                                           # (pending)
│
├── hpc_requests/
│   ├── user_registration_request.md
│   ├── group_registration_request.md
│   └── computing_resources_request.md
│
├── hpc_guide/
│   └── quick_user_guide_tornado_petastream.md
│
└── README.md
```

---

## Document Descriptions

### 01 Research Internship – Fall 2025 (Sep – Dec 2025)

| Document | Description |
|----------|-------------|
| `individual_plan_fall_2025.md` | Individual plan for research internship, focused on ECM parameter optimization using differential evolution |
| `internship_report_fall_2025.md` | Report containing theoretical foundations, software architecture, and experimental results for divisors of 25, 30, and 35 digits |

### 02 Research Internship – Spring 2026 (Jan – Mar 2026)

| Document | Description |
|----------|-------------|
| `individual_plan_spring_2026.md` | Plan for spring research internship – expanding to multiple heuristic methods |
| `internship_report_spring_2026.md` | Report on comparative analysis of 5 heuristic methods (DE, RS, PSO, BO, GA) for 20-digit divisors |

### 03 Technological Internship – Spring 2026 (Mar – Apr 2026)

| Document | Description |
|----------|-------------|
| `individual_plan_technological_spring_2026.md` | Plan for technological practice – HPC adaptation, large-scale experiments, ant colony algorithm |
| `internship_report_technological_spring_2026.md` | Report on cluster adaptation, DAG orchestration, and high-budget comparative experiment |

### 04 Pre-Graduation Internship – Spring 2026 (Apr – May 2026)

| Document | Description |
|----------|-------------|
| `individual_plan_pre_graduation_spring_2026.md` | Plan for pre-graduation practice – thesis structure refinement, literature review, comparison with related works |
| `internship_report_pre_graduation_spring_2026.md` | (Pending) |

### 05 Master's Thesis

| Document | Description |
|----------|-------------|
| `thesis_assignment.md` | Official master's thesis assignment (issued February 25, 2026) |
| `thesis_structure_requirements.md` | University requirements for thesis structure (title page, abstract, introduction, main part, conclusion, references, appendices) |
| `thesis_text.md` | (Pending – full thesis text) |

### HPC Center Documents

| Document | Description |
|----------|-------------|
| `user_registration_request.md` | SCC "Polytechnichesky" user registration request |
| `group_registration_request.md` | Research group registration request (supervisor: Pak V.G.) |
| `computing_resources_request.md` | Computing resources request for ECM optimization project |

### HPC Guide

| Document | Description |
|----------|-------------|
| `quick_user_guide_tornado_petastream.md` | Quick user guide for "Polytechnik – RSK Tornado" and "Polytechnik – RSK Petastream" clusters (SSH keys, modules, SLURM) |

---

## Chronological Order

| # | Folder | Period | Type |
|---|--------|--------|------|
| 01 | `research_internship_fall_2025` | Sep – Dec 2025 | Research internship |
| 02 | `research_internship_spring_2026` | Jan – Mar 2026 | Research internship |
| 03 | `technological_internship_spring_2026` | Mar – Apr 2026 | Technological internship |
| 04 | `pre_graduation_internship_spring_2026` | Apr – May 2026 | Pre-graduation internship |
| 05 | `thesis` | May – Jun 2026 | Master's thesis |

---

## Thesis Structure Requirements (from `thesis_structure_requirements.md`)

The thesis must contain the following sections:

1. **Title page** – по форме Приложения 2 и 3
2. **Assignment** – по форме Приложения 4 и 5
3. **Abstract (Реферат)** – на русском и английском языках (1000–1500 знаков)
4. **Table of Contents**
5. **Introduction** – актуальность, цель, задачи, объект, методы, значимость
6. **Main part** – ход и результаты исследования
7. **Conclusion** – выводы, предложения, рекомендации
8. **References**
9. **Appendices** (optional)

---

## Key Findings Summary

### Fall 2025 (25–35 digit divisors)
- Differential evolution showed limited improvement compared to GMP-ECM tables
- For 25-digit divisors: slight improvement (–4.8%, not statistically significant)
- For 30- and 35-digit divisors: optimized parameters underperformed reference tables
- **Conclusion:** Tabular GMP-ECM values remain optimal for medium/large divisors

### Spring 2026 Research (20-digit divisors)
- Five heuristic methods compared: DE, RS, PSO, BO, GA
- PSO and GA showed best results (improvement up to 31%)
- Bayesian optimization proved unstable
- Optimal parameters concentrate in narrow region: $B_1 \approx 1000–1600$, $B_2/B_1 \approx 1–3$
- **Conclusion:** Heuristic optimization is effective for small divisors

### Spring 2026 Technological Internship (HPC adaptation)
- Full DAG orchestration implemented for cluster execution
- New composite fitness function (reliability + time + curves)
- GA achieved best validation time (2.51 sec), PSO best curve reduction (–61%)
- Three methods (GA, DE, RS) converged to same optimal parameter region

---

## Software Resources

The software system developed during this research is available at:
[https://github.com/EgorPlehanov/ecm-evolutionary-optimization](https://github.com/EgorPlehanov/ecm-evolutionary-optimization)

**Technologies used:**
- Python 3.10+
- NumPy, SciPy (heuristic optimization)
- GMP-ECM (factorization library)
- SLURM (HPC job scheduling)

---

## Document Status

| Component | Status |
|-----------|--------|
| Research internship (Fall 2025) | ✅ Complete |
| Research internship (Spring 2026) | ✅ Complete |
| Technological internship (Spring 2026) | ✅ Complete |
| Pre-graduation internship (Spring 2026) | 🔄 Plan ready, report pending |
| Master's thesis – assignment | ✅ Complete |
| Master's thesis – structure requirements | ✅ Complete |
| Master's thesis – full text | 🔄 Pending |
| HPC registration | ✅ Submitted |

---

## Notes

- All documents have been converted from `.docx`/`.pdf` to Markdown format
- Original formatting (tables, lists, mathematical notation) preserved where possible
- Missing images are marked with `> [!NOTE]` placeholders
- Signatures and dates may be blank in the original documents
- Thesis structure requirements are based on official SPbPU standards

---

## Contact

**Student:** Egor Plekhanov – plehanov.es@edu.spbstu.ru  
**Supervisor:** Vadim G. Pak – pak_vg@spbstu.ru

---

*Last updated: 2026-05-12*
