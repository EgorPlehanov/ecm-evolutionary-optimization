---
title: "A heterogeneous computing environment to solve the 768-bit RSA challenge"
title_en: "A heterogeneous computing environment to solve the 768-bit RSA challenge"
source_type: "article"
authors: ["Kleinjung T.", "Bos J. W.", "Lenstra A. K.", "Osvik D. A.", "Aoki K.", "Contini S.", "Franke J.", "Thomé E.", "Jermini P.", "Thiemard M.", "Leyland P.", "Montgomery P. L.", "Timofeev A.", "Stockinger H."]
year: "2010"
source_link: "https://doi.org/10.1007/s10623-010-9455-7"
doi: "10.1007/s10623-010-9455-7"
language: "en"
converted_on: "2026-05-15"
suggested_filename: "heterogeneous-computing-rsa-768-factorization-2010.md"
---

# Content source: A heterogeneous computing environment to solve the 768-bit RSA challenge

## Source type
Peer-reviewed journal article (Designs, Codes and Cryptography, 2010). Springer.

## Authors affiliation
Multiple institutions: EPFL (Switzerland), NTT (Japan), Macquarie University (Australia), University of Bonn (Germany), INRIA (France), CWI (Netherlands), Microsoft Research, British Institute of Technology, etc.

## Objective
Describe the heterogeneous computing infrastructure (multiple clusters, Grid environments, desktop grids, and individual machines) used to factor RSA‑768 (768‑bit, 232‑digit composite number) using the Number Field Sieve (NFS), and present the resulting factorization and its implications for RSA key size recommendations.

## Core content summary

### 1. Cryptographic motivation

- RSA security depends on hardness of factoring large integers (1024‑bit and 2048‑bit are common key sizes).
- NIST recommended phasing out 1024‑bit RSA by end of 2010, adopting 2048‑bit RSA.
- Factoring RSA‑768 (768 bits) was a benchmark to assess feasibility of factoring 1024‑bit RSA.
- **Conclusion**: factoring 1024‑bit RSA within 5 years (2010–2015) would require a breakthrough; gradual transition to 2048‑bit RSA is safe.

### 2. Number Field Sieve (NFS) steps for RSA‑768

**Overall workflow** (Table 2):

| Step | Description | Approx. cost | Timeline |
|------|-------------|--------------|----------|
| Polynomial selection | Find degree‑6 polynomial f and linear polynomial g = x − m with f(m) ≡ 0 (mod N). | ~20 core‑years | 2005 |
| Sieving (relation collection) | Find ~64B relations (48B unique) with special‑q from 1e8 to 1.11e10. | ~1500 core‑years | 2007:06 – 2009:06 |
| Filtering | Remove duplicates, useless relations, build matrix (193M rows, 28B non‑zero entries). | <12 core‑years | 2009:08 |
| Linear algebra (matrix) | Block Wiedemann (k=512, 8 chunks). | 119 days elapsed | – |
| Square root | Compute final factors from dependency. | ~1 core‑day | – |

**Parameters for RSA‑768**:
- Sieving bound: 2⁴⁰ (primes up to ~1.1×10¹⁰)
- Special‑q range: 10⁸ to 1.11×10¹⁰
- a,b ranges: |a| < 6.3×10¹¹, 0 < b < 1.4×10⁷
- ~10¹⁹ coprime (a,b) pairs tested
- Relations per task: drops from ~1600 to ~100 as special‑q increases
- Compressed data: 5 TB; transferred at ~10 GB/day to EPFL

### 3. Heterogeneous computing infrastructure (Section 4)

**Contributors and resources** (Table 1):

| Site | q‑range (millions) | RAM | Relations found | % of total | Management method |
|------|--------------------|-----|----------------|-------------|-------------------|
| EPFL (Callisto/Greedy/Lacal) | various | 1–2 GB | ~40% | ~40% | cabalc/cabald, Condor, PBS |
| INRIA (Grid5000) | 2400–11000 | 1–2 GB | ~38% | ~45% | OAR + watchdog (best‑effort) |
| NTT | 450–1100, 7000–7900 | 1–2 GB | ~15% | ~16% | ds2c/ds2 |
| CWI | 400–444, 2700–2800, 11000–11100 | 0.5–2 GB | ~3.5% | ~3.3% | factord (crontab + NFS) |
| Bonn | 1500–2000, 4760–4800 | 2 GB | ~7.7% | ~5% | manual queue submission |
| AC3 (Australia) | 2035–2100 | 1.7 GB | ~0.43% | ~0.35% | PBS + manual scripts |
| EGEE (Grid) | 1200–1500 | 1–2 GB | ~14.5% | ~3% | gLite + task server |
| Leyland (personal) | 9500–9600 | 1 GB | ~2.7% | ~0.9% | cabalc/cabald + manual |

**Sieving management tools**:

- **cabalc/cabald** (Leyland, also used at EPFL): client‑server with range allocation, manual error recovery.
- **factord** (CWI): crontab script on workstations, checkpoint/resume, auto‑reassignment of stalled jobs.
- **OAR + watchdog** (INRIA Grid5000): best‑effort jobs, atomic range allocation via file moves, watchdog reclaims partial ranges.
- **gLite + task server** (EGEE): BOINC‑like system on Grid middleware; ranges of length 1000; incomplete ranges reassigned after timeout.
- **ds2c/ds2** (NTT): client‑server with automatic reassignment if no report within 8 hours.
- **PBS + manual scripts** (AC3, Bonn): manual job submission, range tracking, error recovery.

**Matrix step (block Wiedemann)**:

- Matrix: 193 million rows, 28 billion non‑zero entries.
- k = 512 (8 chunks × 64 bit‑vectors).
- First stage: ~565,000 matrix‑vector multiplications per chunk.
- RAM required per chunk: 180 GB.
- Clusters used: EPFL Lacal (304 nodes, 2.93 GHz Opteron, 16 GB/node), 56‑node Lacal672 (896 GB total), others.
- Multiplication time per chunk: ~4.5 sec on 12 nodes (144 cores) with InfiniBand.
- Central stage: ~17 hours on 56 nodes (224 cores, 896 GB RAM).
- Total elapsed: 119 days.

**Polynomial selection**:
- Degree 6 polynomial (f) and linear polynomial g = x − m.
- Searched >2×10¹⁸ pairs at 1.6 billion pairs/core/second.
- Best polynomial found in 2005 after 3 months on 80 AMD Opteron cores in Bonn.
- 2007 search at EPFL did not find better.

### 4. RSA‑768 factorization result

**Composite** (232 decimal digits, 768 bits):
```
123018668453011775513049495838496272077285356959533479219732245215172640050726365751874520219978646938995647494277406384592519255732630345373154826850791702612214291346167042914311602212240479274737794080665351419597459856902143413
```

**Prime factors** (both 384 bits, 116 decimal digits each):

p = 33478071698956898786044169848212690817704794983713768568912431388982883793878002287614711652531743087737814467999489  
q = 36746043666799590428244633799627952632279158164343087642676032283815739666511279233373417143396810270092798736308917

### 5. Key insights and conclusions

- **Total computational effort**: >1700 core‑years (≈1500 core‑years sieving + 20 polynomial selection + 160 matrix + other).
- **Heterogeneity**: different clusters, Grids, OSes, memory sizes, scheduling systems all successfully integrated.
- **Feasibility of 1024‑bit factoring** (as of 2010):
  - Estimated ~500,000 core‑years, 4 billion row matrix.
  - Within reach of state‑level attacker but not academic teams without funding.
  - NIST's recommendation to phase out 1024‑bit RSA by end of 2010 was justified.
- **Lessons learned**:
  - Storage failures (disks, casings) were the most stressful issue.
  - Sieving tolerates errors and sloppiness; matrix step does not.
  - Automated range management (watchdog) essential for best‑effort Grid jobs.
  - Flexible block Wiedemann (variable chunk sizes) allowed heterogeneous clusters to contribute without idle time.

## Key tables

**Table 1**: Sieving contribution by site (q‑range, RAM, relations, tasks, management method).

**Table 3** (in Appendix, not fully extracted): Block Wiedemann timing details per cluster.

## Limitations (explicit from source / context)

- Polynomial selection for RSA‑768 took 3 months in 2005; no significantly better polynomial found later.
- Storage failures were the biggest practical problem; multiple backups needed.
- Some clusters (e.g., AC3) stopped contributing early due to personnel changes.
- 1024‑bit RSA factoring not attempted; estimates are extrapolations.
- No quantum computing considered (Shor’s algorithm would break RSA‑768 in polynomial time, but not feasible in 2010).

## References (selected)
- Aoki et al. (2007) — Kilo‑bit SNFS factorization
- Coppersmith (1993, 1994) — Block Lanczos, block Wiedemann
- Lenstra & Lenstra (1993) — Development of NFS
- Kleinjung et al. (2010) — RSA‑768 factorization (Crypto 2010 paper)
- NFS@home (BOINC project)
- Shor (1994) — Quantum factoring
