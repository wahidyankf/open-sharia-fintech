---
title: "Overview"
date: 2026-07-17T00:00:00+07:00
draft: false
weight: 1
---

This page is the spaced-repetition companion to the Computer Architecture topic: recall first, then
applied judgment, then hands-on katas, then a checklist to confirm real automaticity. Every answer
is hidden in a `<details>` block; try each item yourself before opening it.

Every kata below is self-contained and deterministic -- mocked/hand-constructed inputs only, no live
network, no external service, and no dependency on this topic's own worked-example code. Where a
kata touches timing (cache locality, branch prediction), it checks a **relative** comparison (e.g.
sequential faster than random) rather than asserting a specific number, since wall-clock numbers
vary run to run and machine to machine.

## Recall Q&A

Twenty-five short-answer questions, one per concept (`co-01` through `co-25`). Answer from memory,
then check.

**Q1 (co-01 -- memory hierarchy).** Why does the memory hierarchy trade capacity for latency at
every level, and roughly how many orders of magnitude separate an L1 cache hit from a DRAM access?

<details>
<summary>Answer</summary>

Faster storage technology is physically more expensive per byte (SRAM for caches vs. DRAM vs.
disk), so a machine can afford only a little of the fastest tier and progressively more of each
slower one -- capacity grows as latency grows. An L1 hit costs a handful of cycles; a DRAM access
costs on the order of a hundred-plus cycles -- roughly two orders of magnitude apart.

</details>

**Q2 (co-02 -- cache lines and blocks).** Why does touching a single byte pull an entire cache line
into cache instead of just that byte, and why does Apple Silicon's 128-byte line matter for code
tuned assuming the common 64-byte line?

<details>
<summary>Answer</summary>

Memory moves between cache levels in fixed-size blocks (cache lines) because fetching a whole line
amortizes the fixed per-transaction overhead of a memory access and exploits spatial locality --
neighboring bytes are usually needed soon. Code that hardcodes a 64 B line (common on x86) will
under-count how many elements share a line on a 128 B-line machine, misjudging both false-sharing
risk and prefetch/stride math -- line size must be detected or documented per target, never assumed
universal.

</details>

**Q3 (co-03 -- spatial locality).** What does spatial locality predict about accessing `array[i]`
right after `array[i-1]`, and why does row-major traversal of a 2-D array exploit it while
column-major traversal defeats it?

<details>
<summary>Answer</summary>

Spatial locality predicts that an address near a recently-accessed one is likely already cached,
because it shared that address's cache line. Row-major storage places `a[i][j]` and `a[i][j+1]`
adjacent in memory, so a row-major (inner loop over `j`) traversal walks each cache line fully
before moving on; column-major traversal jumps a full row's stride between consecutive accesses,
landing in a different, likely-uncached line almost every step.

</details>

**Q4 (co-04 -- temporal locality).** What does temporal locality predict about re-reading the same
address twice in quick succession, and why does a working set larger than L1 lose this benefit?

<details>
<summary>Answer</summary>

Temporal locality predicts that re-accessing a recently-touched address is fast because it's still
resident in a cache level. Once the working set exceeds a level's capacity, earlier entries get
evicted to make room for newer ones before they're re-read, so the "recently touched" data is no
longer there when it's needed again -- the benefit degrades to whatever the next (slower) level
provides.

</details>

**Q5 (co-05 -- cache-miss cost).** Why does a single cache miss that must fetch from DRAM often cost
more cycles than dozens of arithmetic instructions combined?

<details>
<summary>Answer</summary>

A modern core can retire multiple arithmetic instructions per cycle, but a DRAM fetch has a fixed,
much larger physical latency (on the order of a hundred-plus cycles) that arithmetic throughput
cannot hide unless there's independent work to overlap with it. A tight loop with one dependent miss
per iteration is bottlenecked by that miss latency, not by the handful of cycles its arithmetic
would otherwise cost.

</details>

**Q6 (co-06 -- cache associativity).** What problem does set-associative cache placement solve
that direct-mapped placement has, and why can a large power-of-two access stride trigger it even in
a mostly-empty cache?

<details>
<summary>Answer</summary>

Direct-mapped caches map each address to exactly one line slot, so two frequently-used addresses
that happen to map to the same slot will repeatedly evict each other (a conflict miss) even though
the cache overall has free capacity. Set-associative placement gives each address a small set of
candidate slots, absorbing some of these collisions. A power-of-two stride can make every accessed
address map to the same (or very few) sets, causing conflict misses regardless of overall cache
occupancy.

</details>

**Q7 (co-07 -- write policies).** What's the difference between write-through and write-back caching,
and what does "write-allocate" add to that choice?

<details>
<summary>Answer</summary>

Write-through propagates every store immediately to the next level (simpler, more memory traffic);
write-back holds the modified data in cache and only flushes it to the next level on eviction
(fewer transfers, but requires tracking "dirty" lines). Write-allocate governs what happens on a
write MISS specifically: whether the line is first fetched into cache before being modified (so a
subsequent read/write to the same line hits) or written directly to the next level without caching
it.

</details>

**Q8 (co-08 -- virtual memory and pages).** Why does each process see a private virtual address
space instead of raw physical addresses, and what translates one to the other?

<details>
<summary>Answer</summary>

A private virtual address space lets the OS isolate processes from each other (one process can't
read/corrupt another's physical memory by address alone), relocate physical memory freely, and
present a uniform address layout to every process regardless of what's physically resident. The
MMU (memory management unit), consulting per-process page tables, translates each virtual address to
its physical counterpart in fixed-size pages.

</details>

**Q9 (co-09 -- TLB).** What does the TLB cache, and why does randomly touching many pages run slower
than the same number of touches confined to a few pages?

<details>
<summary>Answer</summary>

The TLB (translation-lookaside buffer) caches recent virtual-to-physical page translations, so a hit
skips the full page-table walk. Randomly touching many distinct pages exhausts the TLB's limited
entry count, forcing frequent TLB misses (each requiring a multi-level page-table walk) -- whereas
confining accesses to a few pages keeps their translations resident in the TLB across repeated
touches.

</details>

**Q10 (co-10 -- page faults and swapping).** What's the difference between a minor and a major page
fault, and why is only one of them a real performance emergency?

<details>
<summary>Answer</summary>

Both trap to the OS because the accessed virtual page isn't currently mapped. A minor fault is
resolved cheaply in memory (e.g. the page is already resident elsewhere, or is a fresh
zero-fill/first-touch page) -- microseconds. A major fault requires reading the page's data from
disk/swap -- milliseconds, many orders of magnitude slower, and the real performance emergency when
a workload's resident set exceeds available RAM.

</details>

**Q11 (co-11 -- two's-complement integers).** Why do the SAME bits represent different values
depending on whether they're read as `int` or `unsigned int`, and which encoding does C's signed
integer type use?

<details>
<summary>Answer</summary>

A bit pattern has no inherent sign -- it's the TYPE of the read that decides the interpretation.
C's signed integers use two's-complement encoding, where the high bit contributes a negative
weight (`-2^(n-1)`) instead of a positive one; reinterpreting the exact same bits as unsigned makes
that same high bit contribute `+2^(n-1)`, so `-1` (all-ones bits) reads back as the unsigned type's
maximum value.

</details>

**Q12 (co-12 -- integer overflow and wraparound).** Why is unsigned overflow well-defined in C while
signed overflow is undefined behavior, and why does that asymmetry matter for security-sensitive
code?

<details>
<summary>Answer</summary>

The C standard defines unsigned arithmetic as modulo `2^n` (wraparound is guaranteed, specified
behavior), but leaves signed overflow explicitly undefined -- the compiler is allowed to assume it
never happens and optimize accordingly, which can silently eliminate an overflow check the
programmer intended, rather than just producing a "wrong but predictable" wrapped value. A size
computation like `n * record_size` that overflows can therefore under-allocate a buffer in a way
that's both a correctness bug and, in unsigned code, a reliably-wrapped (and thus exploitable)
value.

</details>

**Q13 (co-13 -- IEEE-754 in C).** What are the three fields of an IEEE-754 float's bit layout, and
why is `0.1 + 0.2 != 0.3` not a bug?

<details>
<summary>Answer</summary>

Sign (1 bit), biased exponent, and mantissa (fractional significand) together encode a
sign-magnitude-with-scaling representation. `0.1`, `0.2`, and `0.3` each already round to the
nearest representable binary value the moment the literal is parsed -- before any arithmetic runs --
so the sum of two already-rounded values doesn't have to land on the rounding of the third; this is
structural to finite binary floating point, not an implementation defect.

</details>

**Q14 (co-14 -- float comparison hazards).** Why is exact `==` on two floats unreliable, and what
should replace it?

<details>
<summary>Answer</summary>

Because floating-point arithmetic accumulates rounding error at nearly every operation, two
mathematically-equal expressions computed via different paths (or the same expression computed
twice with different compiler optimizations) can land on adjacent-but-different bit patterns. An
epsilon-tolerant comparison (`fabs(a - b) < epsilon`) should replace exact equality -- and the
epsilon itself needs care when comparing values of very different magnitudes, since a fixed
absolute epsilon can be too loose for tiny values and too tight for huge ones.

</details>

**Q15 (co-15 -- endianness).** What's the difference between little-endian and big-endian byte
order, and what do `htonl`/`ntohl` do about it?

<details>
<summary>Answer</summary>

Little-endian stores a multi-byte value's least-significant byte first; big-endian stores the
most-significant byte first. The same bytes read in the wrong order produce a different, still
plausible-looking number rather than an error. `htonl`/`ntohl` convert a 32-bit value between host
byte order and network byte order (which is defined as big-endian), so code that serializes across
machines/the wire doesn't silently assume its own host's order.

</details>

**Q16 (co-16 -- struct padding and alignment).** Why can `sizeof` a struct exceed the sum of its
fields' individual sizes, and why does field order change the total?

<details>
<summary>Answer</summary>

The compiler inserts padding bytes so each field starts at an address satisfying its own alignment
requirement (and so the whole struct's size is a multiple of its strictest member's alignment, for
correct behavior in arrays). Declaring a large-alignment field after a small one can force padding
between them that a largest-first field order would have avoided -- the same fields, reordered,
can produce a smaller `sizeof`.

</details>

**Q17 (co-17 -- data layout: AoS vs. SoA).** Why does struct-of-arrays often outperform
array-of-structs for a hot loop that only touches one field per element?

<details>
<summary>Answer</summary>

Array-of-structs interleaves every field of a record together, so a loop reading only one hot field
still pulls each record's ENTIRE cache line (including cold fields it never touches) into cache --
wasted memory bandwidth. Struct-of-arrays stores that one field as its own dense array, so every
fetched cache line is 100% useful data for that loop, cutting memory traffic roughly in proportion
to how much of the original record was cold.

</details>

**Q18 (co-18 -- instruction-set architecture).** What does an ISA specify, and what's the core
philosophical difference between RISC and CISC?

<details>
<summary>Answer</summary>

An ISA (x86, ARM, RISC-V, ...) is the hardware/software contract: the set of instructions, registers,
and encoding rules a compiler can target and a CPU implementation must execute correctly -- it's an
abstraction boundary, not an implementation. RISC (Reduced Instruction Set Computer) favors a small
set of simple, uniform, fixed-latency instructions (favoring pipelining and compiler-driven
optimization); CISC (Complex Instruction Set Computer) favors fewer, denser instructions that can
each do more work (e.g. a memory operand built into an arithmetic instruction), trading instruction
count for per-instruction complexity.

</details>

**Q19 (co-19 -- assembly basics).** What can reading a function's emitted assembly reveal that its C
source alone cannot?

<details>
<summary>Answer</summary>

The C source describes WHAT the computation should produce; the assembly reveals HOW the compiler
actually implemented it on the target ISA -- which values live in registers vs. spill to the stack,
whether a division became a shift, whether a loop got vectorized or unrolled, and exactly which ABI
argument registers hold the function's parameters -- all invisible in the source itself.

</details>

**Q20 (co-20 -- pipelining).** What does instruction pipelining overlap, and what's the difference
between a data hazard and a control hazard?

<details>
<summary>Answer</summary>

Pipelining overlaps the fetch/decode/execute/memory/writeback stages of consecutive instructions, so
a new instruction can enter the pipeline every cycle even though any single instruction still takes
several cycles to fully complete. A data hazard occurs when one instruction needs a result a prior,
still-in-flight instruction hasn't produced yet (forcing a stall or forwarding); a control hazard
occurs when a branch's outcome isn't known yet but the pipeline must decide what to fetch next.

</details>

**Q21 (co-21 -- branch prediction).** Why does a mispredicted branch cost tens of cycles, and why
does sorted/predictable data run faster through a branch-heavy loop than random data?

<details>
<summary>Answer</summary>

A pipelined, speculative CPU guesses a branch's outcome and starts executing down that path before
the branch actually resolves; if the guess is wrong, every speculatively-executed instruction must
be discarded and the correct path re-fetched from scratch -- a pipeline flush costing roughly the
pipeline's depth in cycles. Sorted/predictable data lets the branch predictor learn a stable,
repeating pattern (near-perfect prediction); random data defeats prediction, paying the mispredict
penalty on close to every branch.

</details>

**Q22 (co-22 -- superscalar and out-of-order execution).** How can a modern core execute more than
one instruction per cycle, and why might independent work run faster than an equivalent dependent
chain even at the same instruction count?

<details>
<summary>Answer</summary>

A superscalar core has multiple parallel execution units (ports) and can issue several independent
instructions in the same cycle; out-of-order execution additionally lets the core run a LATER
instruction ahead of an EARLIER one that's stalled waiting on an operand, as long as no dependency is
violated. A dependent chain (each result feeding the next) forces strictly sequential execution
regardless of how many ports are free; splitting the same total work into independent chains (e.g.
multiple accumulators) lets the core actually use its parallel execution capacity.

</details>

**Q23 (co-23 -- SIMD vectorization).** What does a SIMD instruction do differently from a scalar
one, and why does array-of-structs layout make auto-vectorization harder than struct-of-arrays?

<details>
<summary>Answer</summary>

A SIMD instruction applies one operation to several data lanes packed into a single wide register in
one instruction (e.g. adding 4 floats at once), instead of one value per instruction. Vectorizing a
loop requires loading several CONSECUTIVE, same-type values into one vector register; array-of-structs
interleaves different fields between the values a vectorized loop would want side by side, forcing
an expensive gather instead of a simple contiguous load, while struct-of-arrays already stores the
needed values contiguously.

</details>

**Q24 (co-24 -- memory ordering and atomics).** What does an atomic operation guarantee that a plain
read-modify-write on a shared variable doesn't, and what is false sharing?

<details>
<summary>Answer</summary>

An atomic operation guarantees the read-modify-write happens as one indivisible step from every
other core's point of view, so concurrent increments from multiple threads can't interleave and lose
an update; a plain (non-atomic) increment can be interrupted mid-sequence by another thread's
conflicting update, silently dropping increments (a data race). False sharing is a DIFFERENT problem
-- two threads updating logically-independent variables that happen to share one cache line still
serialize on that line's coherence traffic, even though there's no actual data race, because the
cache-coherence protocol treats the whole line as the unit of ownership.

</details>

**Q25 (co-25 -- mechanical sympathy and profiling).** Why is "measure, don't guess" the closing
principle of this topic, and what's the macOS equivalent of Linux's `perf`?

<details>
<summary>Answer</summary>

Modern out-of-order, superscalar, speculatively-executing CPUs are complex enough that
back-of-envelope cycle-counting intuition routinely gets the actual bottleneck wrong; a profiler is
the arbiter that turns a plausible-sounding performance story into a verified one. `perf
stat`/`perf record` are Linux-kernel-only; on macOS the equivalent tooling is Instruments (the "CPU
Counters"/"Time Profiler" templates) or `dtrace`.

</details>

## Applied problems

Twelve scenarios spanning representation through mechanical sympathy. Each describes a realistic
situation without naming the specific concept -- decide what applies and why, then check your
reasoning against the worked solution. Every scenario below is invented for this drill and does not
reuse any function, fixture, or dataset from this topic's 80 worked examples or its capstone.

**AP1.** A financial application computes `int total = n_shares * price_per_share_cents;` where
`n_shares` and `price_per_share_cents` are both `int`, and for one particular large trade the result
comes back negative. The developer assumes it's a business-logic bug. What's more likely going on,
and how should it be fixed?

<details>
<summary>Answer</summary>

This is signed integer overflow (co-12) -- the true product exceeds `INT_MAX` and wraps into
negative range, which is undefined behavior in C even though it "looks like" a predictable wrap on
most toolchains. The fix is to compute the multiplication in a wider type (`int64_t` or `long long`)
or use a checked-multiply builtin (`__builtin_mul_overflow`) that detects the overflow before it
happens, not to add a business-logic check for a negative result after the fact.

</details>

**AP2.** A game engine's particle system stores each particle as one struct with position,
velocity, color, and a dozen other fields, and a profiler shows the position-update loop (which only
touches position and velocity) is memory-bandwidth-bound despite doing very little arithmetic per
particle. What's the likely fix?

<details>
<summary>Answer</summary>

Restructure from array-of-structs to struct-of-arrays (co-17) -- store position and velocity as
their own dense arrays, separate from the rarely-touched cold fields. The update loop then streams
only the bytes it actually needs per cache line instead of dragging along a dozen unrelated fields
on every fetch, cutting memory traffic roughly in proportion to how much of the original struct was
cold for that loop.

</details>

**AP3.** Two threads each increment their OWN independent `int` counter in a tight loop with no
shared data between them logically, yet a benchmark shows this "obviously parallel" workload barely
scales past one thread. No data race is present (each thread only touches its own counter). What's
the likely cause?

<details>
<summary>Answer</summary>

False sharing (co-02, co-24) -- if the two counters happen to be allocated close enough together to
share one cache line, every increment from either thread invalidates the other core's cached copy
of that line via the cache-coherence protocol, even though there's no actual race on the DATA. The
fix is padding each counter onto its own separate cache line (or otherwise separating them in
memory).

</details>

**AP4.** A network client reads a 4-byte length-prefix field from an incoming TCP stream using a
raw `*(int*)buffer` cast on a little-endian x86 machine, and it works in local testing. In
production, talking to a big-endian embedded device, lengths come out wildly wrong. What's wrong,
and what's the general fix?

<details>
<summary>Answer</summary>

An endianness mismatch (co-15) -- the raw cast reads the 4 bytes in the LOCAL machine's byte order,
but the wire protocol's bytes are in the REMOTE device's (big-endian) order; the same bytes
reinterpreted in the wrong order produce a different, still-plausible-looking integer instead of an
obvious error. The fix is `ntohl()` (or an explicit byte-order-aware unpack) on every multi-byte
field crossing a network boundary, never a raw pointer cast.

</details>

**AP5.** A tight numerical loop compares a computed running average against a literal threshold
using `if (average == 100.0)` and the branch never fires even when the average is, by all
appearances, exactly 100. What's the likely cause, and what's the fix?

<details>
<summary>Answer</summary>

Floating-point comparison hazard (co-13, co-14) -- the accumulated rounding error from however
`average` was computed almost certainly left it a few ULPs away from the exact literal `100.0`, even
though it prints as "100" at typical `printf` precision. The fix is an epsilon-tolerant comparison
(`fabs(average - 100.0) < epsilon`), with the epsilon sized to the values' actual magnitude.

</details>

**AP6.** A code reviewer sees a struct reordered from `{char flag; double value; char kind;}` to
`{double value; char flag; char kind;}` in a pull request with no other change, and the author
claims it "shrinks memory usage with zero behavior change." Is that a plausible, safe claim?

<details>
<summary>Answer</summary>

Plausible and likely correct (co-16) -- placing the largest-alignment field (`double`, needing
8-byte alignment) first, followed by the two 1-byte `char` fields, minimizes the padding the
compiler must insert between fields (the original order likely pads after `flag` to align `value`,
and again at the end to align the struct's own size); reordering fields never changes the VALUES
stored, only their byte offsets, so it's a safe, pure layout optimization as long as nothing in the
codebase depends on the struct's specific byte offsets (e.g. hand-rolled serialization) without
recomputing them.

</details>

**AP7.** A sorting benchmark shows an algorithm that branches on `if (a[i] > pivot)` runs
noticeably faster on already-mostly-sorted input than on randomly shuffled input of the identical
size, even though both inputs require the exact same number of comparisons. What explains the gap?

<details>
<summary>Answer</summary>

Branch prediction (co-21) -- mostly-sorted data produces a branch outcome pattern the CPU's
predictor can learn and predict correctly almost every time, avoiding the tens-of-cycles pipeline-
flush cost of a misprediction; randomly shuffled data defeats the predictor, paying that cost on
close to every comparison, even though the total INSTRUCTION count (comparisons) is identical
between the two runs.

</details>

**AP8.** A build engineer notices that changing a hot loop's `x / 2` to `x >> 1` "for speed" made
no measurable difference in the compiled binary's performance, and a colleague says this is
expected. Why would the colleague be right?

<details>
<summary>Answer</summary>

The compiler already performs this exact strength-reduction optimization itself (co-19, co-25) --
at any optimization level above `-O0`, dividing a signed or unsigned integer by a compile-time-known
power of two is routinely lowered to a shift instruction automatically, because the compiler can
prove the two are equivalent for that specific divisor. The hand-written shift and the
compiler-optimized division compile to the same (or near-identical) assembly, so no measurable
difference is expected.

</details>

**AP9.** A service pre-allocates a large `mmap`'d buffer at startup and a monitoring dashboard
shows a burst of page faults immediately after the process begins actively writing into previously
untouched regions of that buffer, even though `mmap` itself returned instantly. Is this a bug?

<details>
<summary>Answer</summary>

Not a bug -- expected behavior (co-08, co-10). `mmap` reserves virtual address space essentially
instantly without necessarily backing every page with physical memory yet; the first WRITE to each
previously-untouched page traps as a (cheap) minor page fault, which the OS resolves by mapping in a
fresh physical page on demand. The burst is exactly this "first touch" cost being paid once per page
as the buffer is actually used, not a sign of memory pressure or swapping (which would instead show
up as MAJOR faults).

</details>

**AP10.** A hash-map benchmark comparing open addressing against separate chaining shows open
addressing winning even though both implementations perform the same asymptotic number of probes on
average for the same load factor. What's the likely explanation for the wall-clock gap?

<details>
<summary>Answer</summary>

Cache locality (co-01, co-03, co-17), not algorithmic complexity -- open addressing stores probe
candidates contiguously in one backing array, so consecutive probes during a lookup tend to land in
the same or an adjacent cache line; separate chaining follows a linked list of heap-allocated nodes,
where each node hop is very likely a fresh, uncached memory address (a pointer chase). Identical
average probe COUNTS can still produce very different wall-clock times because one access pattern is
cache-friendly and the other isn't.

</details>

**AP11.** A team wants to run `perf stat -e cache-misses ./their_app` to diagnose a suspected cache
problem, but their CI runners and developer laptops are all macOS. What should they actually use,
and is there a way to get a comparable signal without it?

<details>
<summary>Answer</summary>

`perf` is Linux-kernel-only (co-25); on macOS the direct equivalents are Instruments' "CPU Counters"
template (a GUI profiler) or `dtrace` (also privileged and not trivially scriptable in CI). For a
comparable, CI-friendly signal without either, a before/after wall-clock timing comparison around a
suspected layout fix (the same best-of-N `clock_gettime` methodology used throughout this topic) is
a legitimate proxy -- it doesn't report a raw miss COUNT, but it directly measures the thing the miss
count was a proxy for in the first place: elapsed time.

</details>

**AP12.** A benchmark claims a 32x memory-bandwidth reduction from an AoS-to-SoA refactor should
translate directly into a 32x wall-clock speedup, but the actual measured speedup comes back at
around 3-4x. Is the smaller number evidence the refactor "didn't really work"?

<details>
<summary>Answer</summary>

No (co-01, co-05, co-25) -- bytes-moved and wall-clock time are related but not identical
quantities. The original workload wasn't purely memory-bound at every stage (allocation,
accumulator arithmetic, and the machine's own memory-level parallelism/prefetching can already hide
some of the AoS version's cost), and a large but finite reduction in wasted bytes fetched doesn't
scale linearly into wall-clock time once other costs (that didn't change) become a larger share of
the remaining total. A real, reproducible, correctly-attributed 3-4x speedup with unchanged results
is a genuine win; the theoretical byte-count ratio is an upper bound on the win, not a prediction of
the measured one.

</details>

## Code katas

Eight self-contained exercises. Every kata compiles and runs on hand-constructed, in-memory data
using only the C11 standard library (plus POSIX headers already used throughout this topic, like
`<arpa/inet.h>` and `<pthread.h>`) -- no live network, no external service, and no dependency on
this topic's own worked-example or capstone files, so every kata is runnable anywhere a C11
toolchain is installed, with nothing else to set up.

### Kata 1 -- Two's-complement round-trip on three self-chosen values

Write `print_bits(int32_t n)` that prints a 32-character `0`/`1` string of `n`'s bits (most
significant first), using only bitwise operators (no `printf("%x")` shortcuts). Pick three values of
your own choosing -- one `0`, one positive value near `INT32_MAX`, and one negative value -- and
confirm by hand that your negative value's bit string, reinterpreted as unsigned, equals
`(uint32_t)(2^32 + your_negative_value)` (co-11).

### Kata 2 -- IEEE-754 bit inspector for two self-chosen floats

Using `memcpy` to reinterpret a `float`'s 4 bytes as a `uint32_t` (never a raw pointer cast, to
avoid strict-aliasing UB), write a function decoding sign/exponent/mantissa. Run it against `4.0f`
and `-4.0f` of your choosing, and confirm by hand that they differ ONLY in the sign bit, with
identical exponent and mantissa (co-13).

### Kata 3 -- Endianness round-trip on a value you choose

Pick a 4-byte unsigned integer with at least three distinct nonzero bytes (e.g. something like
`0xAABBCCDD`, but choose your own). Convert it with `htonl`, print both the host-order and
network-order byte sequences using `memcpy` into an `unsigned char[4]`, confirm the two sequences
are byte-reversed from each other on this little-endian machine, and confirm `ntohl(htonl(x)) == x`
(co-15).

### Kata 4 -- Shrink a struct by reordering fields

Define a struct with your own choice of at least four fields spanning at least three different
alignments (e.g. one `char`, one `short`, one `int`, one `double`), deliberately ordered smallest-
to-largest so padding is maximized. Print its `sizeof`, then define a second struct with the exact
same fields reordered largest-to-smallest, print ITS `sizeof`, and confirm the reordered version is
strictly smaller (co-16).

### Kata 5 -- Sequential vs. random sum, direction only

Allocate an `int` array of a size you choose (at least 10 million elements, to make the effect
measurable), fill it with values of your choosing, and time (with `clock_gettime(CLOCK_MONOTONIC,
...)`) a full sequential-order sum against a full sum over a pre-shuffled random index permutation of
the same array. Confirm ONLY that `sequential_time < random_time` -- do not assert or hardcode any
specific ratio, since wall-clock numbers vary by machine and by run (co-03, co-05).

### Kata 6 -- Branchless min of two values, verified against the branching version

Write `int branchy_min(int a, int b)` using an `if`, and `int branchless_min(int a, int b)` using
only arithmetic/bitwise operations (no `if`, no ternary, no comparison-to-boolean shortcuts the
compiler could trivially turn back into a branch). Test both against at least 20 self-chosen `(a,
b)` pairs of your own devising, including equal values and negative values, and confirm they always
agree (co-21).

### Kata 7 -- Atomic vs. non-atomic increment race, observed directly

Using `<pthread.h>` and `<stdatomic.h>`, spawn 4 threads that each increment a SHARED plain `int`
counter 1,000,000 times, and separately spawn 4 threads that each increment a shared `_Atomic int`
counter the same number of times. Compile at `-O0` specifically (verified: at `-O2` the compiler can
legally hoist each thread's whole loop into one local accumulate-then-write-back, which collapses
the race window almost to nothing and hides the bug for a data-race-containing program). At `-O0`,
confirm the non-atomic total comes back well below the expected 4,000,000 (a real, observed lost-
update race -- rerun a few times if one run happens not to show it, since the exact shortfall is
nondeterministic) while the atomic total is always exactly 4,000,000 (co-24).

### Kata 8 -- Cache-line-size-aware false-sharing check

Detect this machine's real cache line size via `sysctl -n hw.cachelinesize` (macOS) or
`sysconf(_SC_LEVEL1_DCACHE_LINESIZE)` (Linux) rather than hardcoding 64 or 128 -- print whichever
value your program actually detects. Then allocate two `int` counters guaranteed to share one cache
line (adjacent in a small array) and two counters padded onto separate lines using the DETECTED size
(not a hardcoded one), and time 4 threads incrementing each pair concurrently. Confirm ONLY that the
padded pair's wall-clock time is less than the unpadded pair's, using whatever line size this
specific machine actually reports (co-02, co-24).

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can order register/L1/L2/L3/DRAM/disk from fastest to slowest and state roughly how many
      orders of magnitude separate an L1 hit from a DRAM access. (co-01)
- [ ] I can explain why touching one byte pulls in its whole cache line, and why I can't assume
      64 B universally (Apple Silicon uses 128 B). (co-02)
- [ ] I can explain why row-major traversal of a 2-D array is faster than column-major, in terms of
      spatial locality. (co-03)
- [ ] I can explain why re-reading a small working set is fast and why that benefit disappears once
      the working set exceeds a cache level's capacity. (co-04)
- [ ] I can explain why a single cache miss can cost more cycles than dozens of arithmetic
      instructions combined. (co-05)
- [ ] I can explain what a conflict miss is and why a large power-of-two stride can trigger one.
      (co-06)
- [ ] I can state the difference between write-through and write-back, and what write-allocate
      adds. (co-07)
- [ ] I can explain why each process sees a private virtual address space and what the MMU does
      with it. (co-08)
- [ ] I can explain what the TLB caches and why randomly touching many pages is slower than touching
      few. (co-09)
- [ ] I can explain the difference between a minor and a major page fault and why only one is a
      performance emergency. (co-10)
- [ ] I can explain why the same bits read differently as `int` vs. `unsigned int`. (co-11)
- [ ] I can state why unsigned overflow is defined and signed overflow is undefined behavior in C,
      and why that distinction matters for a `n * size` allocation computation. (co-12)
- [ ] I can name the three fields of an IEEE-754 float and explain why `0.1 + 0.2 != 0.3` is
      structural, not a bug. (co-13)
- [ ] I can explain why exact `==` on floats is unreliable and what should replace it. (co-14)
- [ ] I can explain the difference between little-endian and big-endian and what `htonl`/`ntohl`
      do about it. (co-15)
- [ ] I can explain why `sizeof` a struct can exceed the sum of its fields, and why field order
      changes it. (co-16)
- [ ] I can explain why struct-of-arrays often beats array-of-structs for a hot loop touching one
      field. (co-17)
- [ ] I can state what an ISA specifies and the core RISC-vs-CISC philosophical difference. (co-18)
- [ ] I can explain what reading emitted assembly reveals that the C source alone cannot. (co-19)
- [ ] I can explain what pipelining overlaps and the difference between a data hazard and a control
      hazard. (co-20)
- [ ] I can explain why a mispredicted branch is expensive and why sorted data beats random data in
      a branch-heavy loop. (co-21)
- [ ] I can explain how a superscalar, out-of-order core executes more than one instruction per
      cycle, and why independent work can beat a dependent chain at equal instruction count. (co-22)
- [ ] I can explain what a SIMD instruction does differently from a scalar one and why AoS makes
      auto-vectorization harder than SoA. (co-23)
- [ ] I can explain what an atomic operation guarantees over a plain read-modify-write, and what
      false sharing is (and how it differs from a real data race). (co-24)
- [ ] I can state this topic's closing principle in one sentence and name the macOS equivalent of
      Linux's `perf`. (co-25)

---

← Previous: [Capstone](../learning/capstone/explanation.md)
