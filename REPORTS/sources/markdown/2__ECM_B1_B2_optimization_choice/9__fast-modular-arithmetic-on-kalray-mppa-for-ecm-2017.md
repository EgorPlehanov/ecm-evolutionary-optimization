---
title: "Fast Modular Arithmetic on the Kalray MPPA-256 Processor for an Energy-Efficient Implementation of ECM"
title_en: "Fast Modular Arithmetic on the Kalray MPPA-256 Processor for an Energy-Efficient Implementation of ECM"
source_type: "article"
authors: ["Ishii M.", "Detrey J.", "Gaudry P.", "Inomata A.", "Fujikawa K."]
year: "2017"
source_link: "https://doi.org/10.1109/TC.2017.2704082"
doi: "10.1109/TC.2017.2704082"
language: "en"
converted_on: "2026-05-14"
suggested_filename: "fast-modular-arithmetic-on-kalray-mppa-for-ecm-2017.md"
---

# Content source: Fast Modular Arithmetic on the Kalray MPPA-256 Processor for an Energy-Efficient Implementation of ECM

## Source type
Journal article (IEEE Transactions on Computers, Vol. 66, No. 12, 2017).

## Authors and affiliations
- Masahiro Ishii (Tokyo Institute of Technology)
- Jérémie Detrey, Pierrick Gaudry (INRIA Nancy, CARAMBA team)
- Atsuo Inomata (Tokyo Denki University)
- Kazutoshi Fujikawa (Nara Institute of Science and Technology)

## Objective
Implement an energy-efficient implementation of the Elliptic Curve Method (ECM) for integer factorization on the Kalray MPPA-256 manycore processor, targeting parameters relevant to the Number Field Sieve (NFS) — moduli of 192–512 bits, smoothness bounds B₁ up to 32768, B₂ up to ~360·2¹⁴. Compare performance (curves/sec) and energy efficiency (curves/joule) with GPU and CPU implementations.

## The Kalray MPPA-256 processor (Section 2)

**Architecture overview**:
- 28nm CMOS chip, 400 MHz.
- 4×4 array of compute clusters (CCs) = 16 clusters total.
- Each cluster: 16 processing engines (PEs) + 1 resource manager (RM) + 2 MB shared memory.
- 4 I/O subsystems (PCIe, Ethernet) for host communication.
- Total cores: 256 (16×16).
- Power consumption (measured during benchmarks): 16 W.

### Core microarchitecture (K1)
- 32-bit VLIW (Very Long Instruction Word), in-order, fully pipelined.
- 5 execution units: ALU0, ALU1 (arithmetic logic), MAU (multiply-accumulate, also FPU), LSU (load/store), BCU (branch/control).
- 64×32-bit general-purpose registers.
- L1 instruction/data caches: 8 KB each.
- **VLIW bundling**: instructions from different units can be issued in same clock cycle.

## Multiprecision modular arithmetic library (Section 3)

### Representation
- Radix 2³² (full word size), arrays of 32-bit words.
- n_w fixed at compile time (range 2–16, i.e., 64–512 bits).
- Carry-aware instructions (addc) available → no need for redundant representation.

### Integer addition (optimized to 3 cycles per 64-bit word)
- Uses 64-bit loads/stores (LSU) and 64-bit add-with-carry (two ALUs combined).
- Software pipelining: interleave load of next double-word with addition of previous pair.
- **Achieved**: 3 cycles per 64-bit limb (optimal, limited by LSU: 2 loads + 1 store per 2 limbs).

### Integer multiplication (parallel-serial, quadratic)
Algorithm:
\[
R \leftarrow 0;\ \text{for } i=0 \text{ to } n_W-1:\ R \leftarrow R + X \cdot y_i \cdot 2^{32i}
\]
- Split \(X = X_0 + X_1\cdot 2^{32}\) (even/odd words) to process contiguous 64-bit chunks.
- MAU: 32×32→64-bit multiply, 2-cycle latency, 1-cycle inverse throughput.
- Schedule (for n_W=8 shown in paper): each partial product computed and accumulated in n_W+1 cycles; overlapping consecutive iterations gives **n_W(n_W+1) + O(1)** cycles total.
- Example: n_W=8 (256 bits) → 72 cycles (vs 64 word products → near optimal).

### Montgomery reduction (REDC)
- Computes \(T \leftarrow X \cdot R^{-1} \bmod N\) with \(R = 2^{32n_W}\).
- Precomputed constant \(n' = (-N)^{-1} \bmod 2^{32}\).
- Similar parallel-serial structure as multiplication.
- **Achieved**: \(n_W(n_W+3) + O(1)\) cycles average.
- Example: n_W=8 → 95–102 cycles.

### Montgomery multiplication = multiplication + REDC
- Total: \(2n_W(n_W+2) + O(1)\) cycles.
- Example: n_W=8 → 178–185 cycles.

### Benchmark results (Table 1, partial)

| Function | 192 bits (n_W=6) | 256 bits (n_W=8) | 384 bits (n_W=12) | 512 bits (n_W=16) |
|----------|------------------|------------------|-------------------|-------------------|
| Integer addition | 16 | 19 | 25 | 31 |
| Integer multiplication | 51 | 81 | 172 | 287 |
| Montgomery reduction | 68–74 | 95–102 | 191–200 | 314–325 |
| Montgomery multiplication | 121–127 | 178–185 | 364–373 | 603–614 |

## ECM implementation (Section 4)

### Curve arithmetic
- Twisted Edwards curves with \(a = -1\), extended coordinates (Hisil et al. 2008).
- Point addition (A): 8 multiplications + 10 additions.
- Point doubling (D): 4 multiplications + 4 squarings + 6 additions.
- Projective coordinates (no y) reduce cost by 1 multiplication (A′, D′).

### Stage 1 — addition chains (Bos & Kleinjung 2012, modified)
- Goal: compute \(K = \prod_{p \le B_1} p^{e_p}\) with minimal elliptic curve operations.
- Greedy search using metric \(\kappa(s_i) = \log_2(s_i) / (\mathrm{dbl}(s_i) + (8/7)\mathrm{add}(s_i) - \log_2(s_i))\).
- Results for B₁ up to 32768 (Table 2).

Example: B₁ = 256 → 361 D′ + 38 A + 12 m = 2843 modular multiplications.

### Stage 2 — baby-step giant-step (Miele et al. 2014, modified)
- Write primes \(B_1 < p \le B_2\) as \(p = vw \pm u\) with \(u \in U\) (ϕ(w)/2 residues), \(v \in V\).
- Choose w as a smooth multiple of 210 (e.g., 210, 420, 630, 1050, 2310, 4620, 6930).
- For B₂ = 2¹⁴ = 16384, w = 420 gives lower cost (2538 multiplications) than w = 210 (2690).

### Throughput benchmarks (full chip, 256 cores, 16 W)

| B₁ | B₂ (≈) | 192 bits | 256 bits | 384 bits |
|----|--------|----------|----------|----------|
| 256 | 2¹⁴ | 105 k/s | 76.6 k/s | — |
| 512 | 3·2¹⁴ | 52.9 k/s | 38.1 k/s | — |
| 1024 | 7·2¹⁴ | 27.6 k/s | 19.9 k/s | — |
| 8192 | 80·2¹⁴ | 3.49 k/s | 2.47 k/s | — |
| 32768 | 360·2¹⁴ | 795 /s | 572 /s | — |

Throughput per joule: 49.7 curves/J (256 bits, B₁=32768) up to 6.56 k/J (192 bits, B₁=256).

## Comparison with other platforms (Table 5)

### Versus NVIDIA GTX580 GPU (Bos & Kleinjung 2012, Miele et al. 2014)

| Context | GTX580 (curves/s) | Ratio (GPU/MPPA) | MPPA curves/joule | Ratio (MPPA/GPU) |
|---------|-------------------|------------------|-------------------|------------------|
| Stage 1 only (B₁=960, 192 bits) | 171 k/s | 2.96× | 702 /J | 5.0× (inverse) |
| Stage 1+2 (B₁=256, B₂=2¹⁴, 192 bits) | 309 k/s | 2.94× | 1.27 k/J | 5.2× |
| Stage 1+2 (B₁=256, B₂=2¹⁴, 256 bits) | 180 k/s | 2.35× | 738 /J | 4.9× |
| Stage 1+2 (B₁=8192, B₂≈80·2¹⁴, 192 bits) | — | — | 8.2 /J | — |

**Conclusion**: GPU is 2–3× faster in throughput, but MPPA-256 is 5–7× more energy-efficient (curves per joule).

### Versus dual Intel Xeon E5-2650 (EECM-MPFQ)

- CPUs: 16 cores (32 threads), TDP 95 W each (190 W total, overestimated).
- MPPA-256 outperforms CPUs in both throughput (2–3×) and energy efficiency (20–30×).

## Optimizations specific to MPPA-256

- **VLIW bundling**: parallel execution of load, ALU, and branch in same cycle.
- **Software pipelining**: interleaved loads and adds to hide latency.
- **No squaring routine** (acknowledged shortcoming): would save ~25% on multiplications in stage 1 (≈10% total speedup).
- **Stage 2 memory constraints**: for large B₂, cache misses increase latency (~10% overhead).

## Limitations (explicit)

1. **No dedicated squaring implementation** (Section 3.5). Acknowledged as shortcoming; would save ~10% in stage 1.
2. **Quadratic multiplication only**; Karatsuba not beneficial for n_W ≤ 16 (crossover point higher).
3. **Stage 2 memory-bound** for large B₂; cache misses visible in benchmarks (e.g., B₁=8192, 10% overhead).
4. **Power measurement for CPUs/GPUs based on TDP (overestimate)**; MPPA measurements are actual.
5. **Moduli sizes fixed at compile time**; cannot handle arbitrary sizes without recompilation.
6. **Not optimized for side-channel resistance**.

## Relation to other work

- ECM implementation follows Bos & Kleinjung (ASIACRYPT 2012) and Miele et al. (CHES 2014) GPU implementations.
- Twisted Edwards curves with a=−1 from Hisil et al. (ASIACRYPT 2008).
- Montgomery multiplication references: Tenca & Koç (2003), Dusse & Kaliski (1990).
- NFS context from Lenstra & Lenstra (1993), Coppersmith (1993), Bernstein & Lange (2014).
