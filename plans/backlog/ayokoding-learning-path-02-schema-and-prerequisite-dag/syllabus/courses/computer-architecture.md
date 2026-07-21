# Computer Architecture (By Example, C)

**Course ID**: `computer-architecture` · **Format**: By Example · **Language**: C.

**Short summary**: CPU, memory, caches, instruction execution

**Scope note**: how the machine actually runs your code, in the CS:APP "program in the machine's
terms" model — the memory hierarchy and caches, the cost of a cache miss, virtual memory,
integer/float representation, endianness, the instruction-set contract and a little assembly, how
pipelining / branch prediction / superscalar out-of-order execution shape a hot loop, SIMD
vectorization, multi-core memory ordering and atomics, and why data layout dominates performance.
`†`: examples in C (with a little assembly to read), where memory layout and representation are
visible rather than hidden. Builds on [`19-computer-science-foundations`](./computer-science-foundations.md).

## Why this exists · the big idea

- **The problem before the solution**: reasoning about a flat, uniform memory and a CPU that runs one
  instruction at a time stopped predicting performance once caches, pipelines, and virtual memory
  arrived — the same big-O algorithm now runs an order of magnitude apart depending on how it touches
  memory.
- **Keep-this-if-you-forget-everything**: memory is a hierarchy and the CPU is fast only when it hits
  cache — sequential, cache-friendly access to compact data beats a "clever" algorithm that chases
  pointers, because a cache miss costs hundreds of cycles.
- **Big ideas touched**: `layering-and-leaks` (this is the layer just under your language — its cache,
  page, and word-size behavior leaks upward as performance you must explain), `abstraction-and-its-cost`
  (the "flat memory, one instruction at a time" abstraction is convenient and wrong; the cost it hides
  is exactly the 100× gap between cache hit and miss).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md) and
  [topic 19 Computer Science Foundations](./computer-science-foundations.md).
- **Tools & environment**: a macOS/Linux terminal; a C toolchain (a recent stable `clang`/`gcc`); a
  profiler/`perf`-style tool to measure cache and cycle behavior; optionally a disassembler to read
  emitted assembly; Neovim/VSCode with the C LSP (DD-17).
- **Assumed knowledge**: reading and running a small program (topic 04); binary/number
  representation and complexity intuition (topic 19); reading a typed script to drive experiments
  (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the model taught here (memory hierarchy, cache lines, virtual memory,
  two's-complement integers, IEEE-754 floats, endianness, data-layout effects) is long-settled and
  correctly left version-unpinned. CS:APP remains the canonical programmer's-eye reference.
- 2026-07-12 — verified: exact cache sizes, line sizes, and miss penalties are microarchitecture- and
  vendor-specific — the file describes them as order-of-magnitude and hardware-dependent rather than
  asserting one CPU's numbers. Note the common 64-byte cache line is **not universal**: Apple Silicon
  (M-series) uses a 128-byte line — `ex-22` must detect the line size at runtime rather than hardcode
  64 B. (apple.com developer docs / llvm target notes)
- 2026-07-12 — verified: `perf stat`/`perf record` are **Linux-only**. On macOS the equivalent
  cache-miss/cycle profiling uses Instruments (the "CPU Counters"/"Time Profiler" templates) or
  `dtrace`; `ex-56`/`ex-57` name the profiler per platform rather than assuming `perf`. (Apple
  Instruments docs / perf.wiki.kernel.org)
- 2026-07-16 — re-verified (Phase 23 dispatch `V` step): all three findings above re-confirmed
  still accurate, nothing changed since 2026-07-12. CS:APP remains at its 3rd edition
  (csapp.cs.cmu.edu, no 4th edition published) — the model taught here is still correctly
  version-unpinned. Apple Silicon's 128 B cache line is unchanged through the current M-series
  lineup (confirmed against this dev machine's own `sysctl -n hw.cachelinesize` → `128`, consistent
  with published Apple Silicon reporting; no generation is documented to have moved off 128 B).
  `perf` remains Linux-kernel-only (en.wikipedia.org/wiki/Perf\_(Linux)); Instruments/`dtrace` remain
  the macOS equivalents (`/usr/sbin/dtrace`, `/usr/bin/xctrace` both present on this dev machine).
  No unresolved "to verify" line remains in this file.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject). Each example below cites the co-NN it exercises. -->

- **co-01 · memory-hierarchy** — registers → L1/L2/L3 cache → DRAM → disk, each level trading capacity
  for a latency gap of roughly an order of magnitude.
- **co-02 · cache-lines-and-blocks** — memory moves between levels in fixed-size lines (typically 64 B;
  128 B on Apple Silicon), so touching one byte pulls in its neighbors.
- **co-03 · spatial-locality** — accessing memory addresses near recently-used ones is fast because they
  already share a cached line.
- **co-04 · temporal-locality** — re-accessing the same address soon is fast because it is still resident
  in a cache level.
- **co-05 · cache-miss-cost** — a miss that must fetch from a lower level costs tens-to-hundreds of
  cycles, dwarfing the arithmetic it feeds.
- **co-06 · cache-associativity** — direct-mapped / set-associative / fully-associative placement decides
  which lines evict each other; power-of-two strides cause conflict misses.
- **co-07 · write-policies** — write-through vs write-back and write-allocate govern when a store reaches
  the next level and what a write costs.
- **co-08 · virtual-memory-and-pages** — each process sees a private virtual address space mapped to
  physical RAM in fixed-size pages by the MMU.
- **co-09 · tlb** — the translation-lookaside buffer caches recent virtual→physical page translations; a
  TLB miss adds a page-table walk.
- **co-10 · page-faults-and-swapping** — touching an unmapped/paged-out page traps to the OS, which maps
  or swaps it in — a minor fault is cheap, a major (disk) fault is not.
- **co-11 · twos-complement-integers** — signed integers in C use two's complement; the same bits read
  as signed or unsigned give different values.
- **co-12 · integer-overflow-and-wraparound** — unsigned overflow wraps modulo 2ⁿ (defined); signed
  overflow is undefined behavior in C — a real correctness/security hazard.
- **co-13 · ieee-754-in-c** — `float`/`double` are sign/exponent/mantissa bit layouts; rounding error is
  structural, not a bug.
- **co-14 · float-comparison-hazards** — exact `==` on floats is unreliable; compare within an epsilon and
  beware precision loss when magnitudes differ.
- **co-15 · endianness** — byte order (little- vs big-endian) differs across machines and the wire;
  `htonl`/`ntohl` convert for portable serialization.
- **co-16 · struct-padding-and-alignment** — the compiler pads struct fields to their alignment, so field
  order changes `sizeof` and misaligned access is slow or faulting.
- **co-17 · data-layout-aos-vs-soa** — array-of-structs vs struct-of-arrays decides how a hot loop strides
  memory; layout beats micro-tuning.
- **co-18 · instruction-set-architecture** — the ISA (x86 / ARM / RISC-V) is the hardware/software
  contract; RISC vs CISC is a design-philosophy split.
- **co-19 · assembly-basics** — registers, load/store, and reading emitted assembly reveal what the CPU
  actually does with your C.
- **co-20 · pipelining** — the CPU overlaps fetch/decode/execute/memory/writeback stages; data and
  control hazards force stalls.
- **co-21 · branch-prediction** — the CPU guesses branch outcomes; a mispredict flushes the pipeline
  (tens of cycles), so predictable or branchless code wins.
- **co-22 · superscalar-and-out-of-order** — modern cores issue several instructions per cycle and
  execute out of order (speculatively), exploiting instruction-level parallelism.
- **co-23 · simd-vectorization** — SIMD units (SSE/AVX/NEON) apply one operation to a vector of values,
  the data-parallel path to throughput.
- **co-24 · memory-ordering-and-atomics** — cache coherence, atomic operations, and memory barriers make
  multi-core shared memory correct; false sharing silently kills scaling.
- **co-25 · mechanical-sympathy-and-profiling** — measure, don't guess: a profiler (perf on Linux,
  Instruments/`dtrace` on macOS) is the arbiter of every performance claim.

## Tensions & trade-offs — when NOT to reach for this

- **Cache-tuning is premature for most code**: data-layout tuning pays off in hot loops and tight
  kernels, but rewriting readable code for cache lines before a profile proves it's the bottleneck
  trades clarity for imagined speed.
- **The model is itself an abstraction**: modern out-of-order, superscalar CPUs with speculative
  execution defeat back-of-envelope reasoning — mechanical-sympathy intuition must be _checked_ against
  a profiler (topic 16), not trusted blind.
- **Portability vs exploiting the machine**: endianness, word size, and alignment assumptions bake in
  hardware details; code that depends on them is fast on one target and broken on another. Reach for
  the machine's specifics only where the win is measured and the target is fixed.

## Lineage — why it beat the alternative

- Programmers once reasoned about a flat, uniform memory and a CPU that executed one instruction at a
  time — a model that stopped predicting performance once caches, pipelines, and virtual memory arrived
  and the "memory wall" (CPU speed outpacing DRAM latency) opened. The CS:APP "program in the machine's
  terms" view won because it explains the gaps the flat model can't: why the same algorithm runs an
  order of magnitude faster with a cache-friendly layout, and why a float comparison can lie. This
  mechanical-sympathy foundation feeds the systems-programming topics — [`82-just-enough-rust`](./just-enough-rust.md)
  lists it as a prerequisite — and gives [`16-debugging-and-profiling`](./debugging-and-profiling.md)
  the vocabulary to read a profile instead of guessing.

## Worked examples

Colocated under `computer-architecture/learning/code/`; each is a small C program you compile, run,
and measure to make an invisible cost visible (DD-20/DD-30). Every example cites the `co-NN` concept(s)
it exercises. Contiguous `ex-01..ex-80`.

### Beginner

- **ex-01 · print-int-bytes** — cast an `int*` to `unsigned char*` and print its bytes — verify the byte
  sequence matches the value's two's-complement encoding. (co-11, co-15)
- **ex-02 · hex-dump-value** — hex-dump a 4-byte `int` — verify the nibbles match `printf("%x")`. (co-11)
- **ex-03 · signed-vs-unsigned-print** — print `-1` as `%u` — verify it shows `4294967295`. (co-11, co-12)
- **ex-04 · signed-overflow-wrap** — compute `INT_MAX + 1` compiled with `-fwrapv` — verify it wraps to
  `INT_MIN` (and note it is UB without the flag). (co-12)
- **ex-05 · unsigned-wraparound** — compute `0u - 1u` — verify it yields `UINT_MAX`. (co-12)
- **ex-06 · unsigned-underflow-loop-bug** — a `for (size_t i = n-1; i >= 0; i--)` infinite-loop bug —
  verify the fix (signed index or `!= SIZE_MAX` guard) terminates. (co-12)
- **ex-07 · float-bits-inspect** — union an `int` and a `float`, print IEEE-754 bits of `1.0` — verify
  sign/exponent/mantissa fields. (co-13)
- **ex-08 · float-not-equal** — show `0.1 + 0.2 != 0.3` in C — verify the strict `==` is false. (co-13, co-14)
- **ex-09 · float-epsilon-compare** — compare with `fabs(a-b) < 1e-9` — verify the epsilon test passes
  where `==` failed. (co-14)
- **ex-10 · float-precision-loss** — add a large and a tiny `float` — verify the tiny addend is lost.
  (co-13, co-14)
- **ex-11 · endianness-detect** — inspect the first byte of a multibyte int at runtime — verify
  little-endian on x86/ARM. (co-15)
- **ex-12 · htonl-roundtrip** — round-trip a value through `htonl`/`ntohl` — verify identity. (co-15)
- **ex-13 · manual-byteswap** — hand-swap the bytes of a `uint32_t` — verify it matches `htonl` on a
  little-endian host. (co-15)
- **ex-14 · struct-sizeof-padding** — `sizeof` a `{char; int; char}` struct — verify it exceeds the field
  sum due to padding. (co-16)
- **ex-15 · struct-reorder-shrink** — reorder the same fields largest-first — verify a smaller `sizeof`.
  (co-16)
- **ex-16 · packed-struct** — apply `__attribute__((packed))` — verify `sizeof` equals the field sum.
  (co-16)
- **ex-17 · alignof-types** — print `_Alignof` for `char`/`int`/`double` — verify increasing alignment.
  (co-16)
- **ex-18 · misaligned-access-cost** — time aligned vs deliberately misaligned loads — verify the
  misaligned path is slower (or faults on strict targets). (co-16)
- **ex-19 · pointer-arithmetic-stride** — increment a typed pointer — verify the address advances by
  `sizeof(T)`. (co-17)
- **ex-20 · array-row-major-layout** — compute a 2-D array element address by hand — verify it matches
  `&a[i][j]`. (co-17)
- **ex-21 · latency-hierarchy-table** — print approximate cycle costs per memory level — verify the
  strictly increasing ordering. (co-01)
- **ex-22 · cache-line-size-probe** — sweep access stride and find the timing jump — verify it lands at
  ~64 B (128 B on Apple Silicon). (co-02)
- **ex-23 · sequential-vs-random-sum** — sum an array in order vs by random index — verify sequential is
  much faster. (co-03, co-05)
- **ex-24 · temporal-locality-working-set** — repeatedly touch a small vs large working set — verify the
  small set stays cache-resident and fast. (co-04)
- **ex-25 · read-disassembly** — compile a function with `-S` and read its assembly — verify load/store
  and arithmetic instructions appear. (co-19)
- **ex-26 · registers-in-asm** — identify register operands in emitted assembly — verify arguments land in
  the ABI's argument registers. (co-19)
- **ex-27 · isa-compare-riscv-x86** — compile the same C to x86 and RISC-V assembly — verify the
  instruction counts/mnemonics differ. (co-18)

### Intermediate

- **ex-28 · cache-miss-stride-sweep** — sweep strides 1…1024 timing a fixed number of accesses — verify a
  performance cliff appears at the cache-line stride. (co-02, co-05)
- **ex-29 · matrix-traversal-ij-vs-ji** — sum a row-major matrix `[i][j]` vs `[j][i]` — verify `[i][j]` is
  faster. (co-03, co-17)
- **ex-30 · aos-vs-soa-hot-loop** — sum one field across array-of-structs vs struct-of-arrays — verify SoA
  is faster. (co-17)
- **ex-31 · working-set-cache-cliffs** — grow a random-access working set past L1/L2/L3 — verify a timing
  cliff at each level's capacity. (co-01, co-05)
- **ex-32 · cache-blocking-matmul** — naive vs tiled matrix multiply — verify the tiled version is faster
  for large matrices. (co-03, co-25)
- **ex-33 · false-sharing-demo** — two threads increment adjacent words in one cache line — verify a large
  slowdown vs independent lines. (co-02, co-24)
- **ex-34 · padding-fixes-false-sharing** — pad the two counters onto separate lines — verify the slowdown
  disappears. (co-02, co-24)
- **ex-35 · prefetch-hint** — add `__builtin_prefetch` to a pointer walk — verify a measurable
  improvement. (co-03)
- **ex-36 · branch-predictable-vs-random** — sum-if-positive over sorted vs shuffled data — verify sorted
  runs faster. (co-21)
- **ex-37 · branchless-max** — replace a conditional with arithmetic/`cmov` — verify identical output and
  a speedup on random data. (co-21)
- **ex-38 · pipeline-dependency-chain** — time a dependent add chain vs independent adds — verify the
  independent version is faster. (co-20, co-22)
- **ex-39 · loop-unrolling** — unroll a reduction loop — verify higher throughput than the rolled loop.
  (co-20, co-22)
- **ex-40 · ilp-multiple-accumulators** — sum with 4 accumulators vs 1 — verify the 4-accumulator version
  is faster (breaks the dependency). (co-22)
- **ex-41 · tlb-pressure-random-pages** — random-access across many pages — verify TLB misses dominate vs
  a compact footprint. (co-09, co-08)
- **ex-42 · page-fault-mmap** — `mmap` a file and touch pages — verify minor faults occur on first touch.
  (co-08, co-10)
- **ex-43 · virtual-address-print** — print a pointer and note it is a virtual address — verify two
  processes reuse the "same" address independently. (co-08)
- **ex-44 · swapping-slowdown** — allocate and touch more than free RAM — verify major-fault swapping
  slows access sharply. (co-10)
- **ex-45 · write-heavy-cost** — time a write-heavy vs read-heavy loop over the same data — verify the
  store traffic cost. (co-07)
- **ex-46 · associativity-conflict-stride** — access with a large power-of-two stride — verify conflict
  misses spike at the critical stride. (co-06)
- **ex-47 · simd-auto-vectorize** — compile a sum loop at `-O3` — verify vector registers in the asm and a
  speedup over `-O0`. (co-23)
- **ex-48 · simd-intrinsics-add** — hand-write an SSE/NEON vector add — verify it matches the scalar result
  and is faster. (co-23)
- **ex-49 · simd-dot-product** — vectorize a dot product with a horizontal reduction — verify correctness
  and speedup. (co-23)
- **ex-50 · aligned-alloc-for-simd** — use `aligned_alloc` for SIMD loads — verify aligned loads avoid
  faults and run faster. (co-16, co-23)
- **ex-51 · atomic-increment** — increment a shared `_Atomic` counter from N threads — verify no updates
  are lost. (co-24)
- **ex-52 · non-atomic-race** — increment a plain shared counter from N threads — verify the total
  undercounts (a race). (co-24)
- **ex-53 · memory-barrier-ordering** — demonstrate reordered stores/loads needing a barrier — verify the
  barrier restores the expected order. (co-24)
- **ex-54 · div-vs-shift-asm** — compare `/2` and `>>1` in emitted asm — verify the compiler lowers the
  division to a shift. (co-19, co-25)
- **ex-55 · hot-cold-struct-split** — split rarely-used cold fields out of a hot struct — verify a
  hot-loop speedup. (co-17, co-04)
- **ex-56 · perf-cache-miss-count** — measure cache misses with `perf stat` / Instruments before and after
  a layout fix — verify the miss count drops. (co-25, co-05)
- **ex-57 · cpi-ipc-measure** — measure cycles-per-instruction for two loops — verify they differ and
  explain why. (co-25, co-22)

### Advanced

- **ex-58 · optimize-kernel-end-to-end** — profile a slow kernel, fix its layout, re-measure — verify a
  documented, reproducible speedup with identical output. (co-25, co-17)
- **ex-59 · blocked-transpose** — naive vs cache-blocked matrix transpose — verify the blocked version is
  faster and correct. (co-03)
- **ex-60 · particle-sim-soa-simd** — update a particle system as AoS vs SoA+SIMD — verify SoA+SIMD is
  fastest. (co-17, co-23)
- **ex-61 · parallel-histogram-scaling** — parallel histogram with shared vs per-thread bins — verify
  per-thread bins scale while shared bins suffer false sharing. (co-24, co-02)
- **ex-62 · mispredict-cost-measure** — measure branch-mispredict penalty in cycles — verify it lands near
  the microarchitecture's known depth. (co-21)
- **ex-63 · branch-to-lookup-table** — replace a data-dependent branch with a table lookup — verify it is
  faster on random input. (co-21)
- **ex-64 · numa-local-allocation** — allocate memory local to a thread (Linux `numactl`/`first-touch`) —
  verify lower latency than remote-node memory. (co-01)
- **ex-65 · hugepages-tlb** — walk a large region with 4 KB vs huge pages — verify hugepages cut TLB
  misses. (co-09)
- **ex-66 · integer-overflow-security-bug** — an `n * size` allocation that overflows to under-allocate —
  verify the overflow, then fix with a checked multiply. (co-12)
- **ex-67 · kahan-summation** — sum many floats naively vs with Kahan compensation — verify Kahan is more
  accurate. (co-13, co-14)
- **ex-68 · fast-inverse-sqrt-bits** — the bit-hack reciprocal-sqrt reading float bits — verify it
  approximates `1/sqrt(x)` within tolerance. (co-13)
- **ex-69 · portable-serialization** — serialize/deserialize a struct across endianness with explicit byte
  order — verify a round-trip on both orders. (co-15, co-16)
- **ex-70 · soa-enables-vectorization** — show AoS blocks auto-vectorization that SoA enables — verify
  vector registers appear only for SoA. (co-17, co-23)
- **ex-71 · loop-interchange** — swap nested-loop order for locality — verify the interchanged loop is
  faster. (co-03, co-17)
- **ex-72 · roofline-bandwidth-vs-compute** — measure a bandwidth-bound and a compute-bound kernel —
  verify each sits where the roofline predicts. (co-25, co-01)
- **ex-73 · prefetch-distance-tuning** — sweep the prefetch distance — verify an optimal distance exists.
  (co-03)
- **ex-74 · pipeline-hazard-diagram** — a Mermaid 5-stage pipeline showing a load-use stall — verify the
  diagram's stall matches the measured latency. (co-20)
- **ex-75 · superscalar-port-contention** — two ops contending for one execution port — verify throughput
  caps below the independent-op rate. (co-22)
- **ex-76 · atomic-vs-mutex-throughput** — a CAS-atomic counter vs a mutex counter — verify the atomic is
  faster under low contention. (co-24)
- **ex-77 · cache-friendly-hashmap** — open-addressing vs chaining lookup — verify open-addressing is
  faster from better locality. (co-03, co-17)
- **ex-78 · vectorized-byte-search** — a SIMD `memchr`-style search — verify it beats a scalar byte loop.
  (co-23)
- **ex-79 · profile-guided-layout-record** — a decision record choosing a layout — verify every claim
  cites a measured profiler number. (co-25)
- **ex-80 · mechanical-sympathy-recap** — a benchmark harness asserting cache-friendly beats cache-hostile
  across N kernels — verify all N assertions hold. (co-25, co-03, co-05)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take one small numeric/data-processing kernel and make it measurably faster by changing
  only how it touches memory — proving that data layout, not cleverness, drove the win — while
  demonstrating representation and endianness hazards along the way.
- **Concepts exercised**: [ ] integer/float representation + an overflow/rounding hazard (co-11, co-12,
  co-13, co-14) [ ] endianness inspection (co-15) [ ] a measured cache-miss cost (co-02, co-05) [ ] a
  data-layout transformation (AoS→SoA or blocking) (co-17) [ ] a before/after profile (co-25) [ ] a
  written explanation tying the speedup to the memory hierarchy (co-01, co-03).
- **Ordered steps**:
  1. `.../learning/capstone/code/repr.c` — print bytes of int/float values, force an overflow, and
     show a non-equal float compare. Verify the output matches the documented representation.
  2. `.../cache.c` — the kernel with a cache-hostile layout, timed. Verify the miss cost is
     reproducible across runs.
  3. Restructure to a cache-friendly layout and re-measure with a profiler. Verify a documented
     speedup attributable to cache behavior, with identical results.
  4. `.../explanation.md` — tie the numbers to the memory hierarchy. Verify the explanation matches the
     measured profile.
- **Acceptance criteria**: representation/endianness hazards are demonstrated; the layout change
  produces a measured, reproducible speedup with unchanged results; the explanation is grounded in the
  profile.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Computer Organization and Design: The Hardware/Software Interface (RISC-V ed.)** — Patterson,
  Hennessy (2nd RISC-V ed., 2020). Standard bridge from digital logic to ISAs, pipelining, and the
  memory hierarchy.
- **Computer Systems: A Programmer's Perspective (CS:APP)** — Bryant, O'Hallaron (3rd ed., 2015).
  Canonical programmer's-eye view of machine representation, linking, and the memory hierarchy.
  <https://csapp.cs.cmu.edu/>
- **Computer Architecture: A Quantitative Approach** — Hennessy, Patterson (6th ed., 2017).
  Graduate-level, data-driven reference for ILP, pipelining, and memory-system trade-offs.

**Papers & articles**

- **"The Case for the Reduced Instruction Set Computer"** — Patterson, Ditzel (1980, ACM SIGARCH).
  Landmark paper founding the RISC design philosophy. <https://dl.acm.org/doi/10.1145/641914.641917>
- **What Every Programmer Should Know About Memory** — Ulrich Drepper (2007). Detailed explanation of
  cache hierarchies and NUMA on real hardware.
  <https://people.freebsd.org/~lstewart/articles/cpumemory.pdf>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · CS fundamentals, DS&A & algorithms — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 1 · CS theory & foundations (the university core, taught first).

> _Content originated in the now-closed FS-SE plan (topic 20); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
