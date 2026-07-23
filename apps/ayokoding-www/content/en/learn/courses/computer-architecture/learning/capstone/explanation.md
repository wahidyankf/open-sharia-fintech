---
title: "Capstone: Sensor-Averaging Kernel"
date: 2026-07-17T00:00:00+07:00
draft: false
weight: 1
---

## The capstone: prove layout, not cleverness, drives the win

This capstone takes one small, realistic numeric kernel -- averaging a `reading` field across
millions of sensor records -- and makes it measurably faster by changing **only how it touches
memory**, never the arithmetic. Along the way it demonstrates the representation and endianness
hazards that hide inside exactly this kind of kernel if you don't understand what's underneath it.
Every number below is a genuine, captured transcript from this Apple Silicon dev machine (Apple
clang 17.0.0, arm64, macOS/Darwin 24.5.0, 128 B cache line, 64 KiB L1d, 4 MiB L2, 12 logical CPUs,
`-O2` unless stated) -- never a fabricated one, per this topic's DD-20 discipline.

- **Step 1 -- [`repr.c`](./code/repr.c)**: an int/float representation toolkit exercising the exact
  hazard classes that hide inside the averaging kernel this capstone builds -- two's-complement
  int bytes and IEEE-754 float bytes (co-11, co-13), an integer-overflow allocation bug caught by
  `__builtin_mul_overflow` (co-12), a `double` non-equal-compare on the same kind of arithmetic the
  kernel performs (co-13, co-14), and a sensor-ID round-tripped through network byte order (co-15).
- **Step 2 -- [`cache.c`](./code/cache.c)**: the averaging kernel over an array-of-structs
  (`SensorRecord`) dataset -- the cache-**hostile** baseline, timed.
- **Step 3 -- [`cache_soa.c`](./code/cache_soa.c)**: the identical kernel and dataset restructured
  to struct-of-arrays -- the cache-**friendly** version, re-measured with the same methodology.
- Concepts exercised: co-01, co-02, co-03, co-05, co-11, co-12, co-13, co-14, co-15, co-17, co-25.

---

## Step 1: representation and endianness hazards (`repr.c`)

**Compile**: `clang -O2 -Wall -std=c11 -fwrapv repr.c -o repr -lm`
**Run**: `./repr`

**Output** (actual, captured on this machine):

```text
=== Part A: raw representation ===
int32_t -1                   value=-1           bits=0xffffffff bytes(low->high)=ff ff ff ff
int32_t 42                   value=42           bits=0x0000002a bytes(low->high)=2a 00 00 00
float 1.0f                   value=1              bits=0x3f800000 sign=0 exponent=127(biased) mantissa=0x000000
float -0.5f                  value=-0.5           bits=0xbf000000 sign=1 exponent=126(biased) mantissa=0x000000

=== Part B: integer-overflow allocation hazard ===
hostile_n=100000000 record_size=32
  true 64-bit product   = 3200000000 bytes (3200.00 MB)
  naive int32 product   = -1094967296 bytes  <-- WRONG, this is what malloc(n*size) would request
  checked_records_bytes: REJECTED (overflow detected, allocation refused)
PASS: __builtin_mul_overflow caught the hazard naive multiplication silently missed

=== Part C: float comparison hazard ===
a=0.10000000000000001 b=0.20000000000000001 a+b=0.30000000000000004 target=0.29999999999999999
  strict (a+b == 0.3)    : false
  epsilon (|diff|<1e-9)  : true
PASS: strict equality fails on this exact arithmetic shape; epsilon compare is the correct tool

=== Part D: endianness round-trip ===
sensor_id_host = 0x0a2b3c4d  bytes = 4d 3c 2b 0a
sensor_id_wire = 0x4d3c2b0a  bytes = 0a 2b 3c 4d  (network/big-endian order)
roundtrip      = 0x0a2b3c4d
PASS: ntohl(htonl(x)) == x (host bytes differ from wire bytes on this little-endian machine)

CAPSTONE STEP 1 PASS: representation, overflow, float, and endianness hazards all demonstrated
```

**Why these four hazards, specifically**: every one of them is a bug class that can hide silently
inside the exact averaging kernel Steps 2-3 build. A `sensor_count * record_size` allocation-size
computation (Part B) is precisely how a real telemetry ingest pipeline would size its buffer before
building the array Step 2 averages over -- get it wrong and the kernel reads past a too-small
allocation. A naive `==` on averaged readings (Part C) is precisely how a monitoring threshold
check ("is the average exactly 50.0?") would silently misfire. And if these sensor IDs were ever
serialized to a network protocol (Part D), forgetting the byte-order conversion would corrupt every
ID on a big-endian receiver -- worth knowing even though this averaging kernel itself never crosses
the wire.

**One correction made while authoring this capstone**: the classic "`0.1 + 0.2 != 0.3`" anomaly
does NOT reproduce at 32-bit `float` precision on this toolchain -- `0.1f + 0.2f == 0.3f` evaluates
`true` here, because binary32 rounding happens to land both sides on the same bit pattern. The
anomaly is real but precision-dependent; `repr.c` correctly uses `double` (binary64, the same
precision the averaging kernel's own accumulator uses), where it reproduces exactly as shown above.
This is stated here rather than silently fixed, per this topic's DD-20 rule against ever presenting
invented output as real.

---

## Step 2: the cache-hostile baseline (`cache.c`)

`SensorRecord` packs one **hot** field (`reading`, the only field the averaging loop touches) next
to three **cold** fields (`sensor_id`, a 112-byte `location` buffer, `timestamp`) that the loop
never reads -- `static_assert(sizeof(SensorRecord) == 128, ...)` pins the struct to exactly this
machine's 128 B cache line at compile time, so every line the kernel fetches carries exactly one
record's worth of mostly-wasted bytes.

**Compile**: `clang -O2 -Wall -std=c11 cache.c -o cache -lm`
**Run**: `./cache`

**Output** (actual, captured on this machine):

```text
dataset: N=2000000 records, sizeof(SensorRecord)=128 bytes (256.0 MB total AoS)
AoS (cache-hostile) average_reading: best of 5 = 0.0067 s, result=50.001636
```

## Step 3: the cache-friendly restructuring, re-measured (`cache_soa.c`)

The identical dataset (same seed, same generation sequence) and the identical arithmetic, held as
struct-of-arrays instead: `float reading[N]` is now a dense array on its own, so every 128 B cache
line holds 32 real, useful readings instead of one useful reading buried in 124 bytes of cold
padding.

**Compile**: `clang -O2 -Wall -std=c11 cache_soa.c -o cache_soa -lm`
**Run**: `./cache_soa`

**Output** (actual, captured on this machine):

```text
dataset: N=2000000 records, SoA total = 256.0 MB (same 4 fields as cache.c, held as 4 dense arrays)
SoA (cache-friendly) average_reading: best of 5 = 0.0018 s, result=50.001636
```

**Identical results, measured speedup**: `50.001636 == 50.001636` -- the layout change did not
change the answer, only how fast the machine reached it. `0.0067 s / 0.0018 s ≈ 3.7x`. Re-running
both binaries repeatedly on this machine reproduces the same story every time (a representative
spread across five separate repeated runs: AoS 0.0055-0.0070 s, SoA 0.0017-0.0019 s -- always a
~3-4x gap, never overlapping), which is exactly the "reproducible" bar the syllabus's capstone
acceptance criteria set.

---

## Tying the numbers to the memory hierarchy (co-01, co-25)

Both kernels do the **same 2,000,000 additions and one division** -- the arithmetic cost is
identical. The entire 3.7x gap is memory-hierarchy cost, not compute cost:

- **AoS**: each iteration loads a full 128 B cache line (one complete `SensorRecord`) to use only
  the 4-byte `reading` field inside it. Streaming through 2M records touches 256 MB of memory
  traffic to deliver 8 MB of data the loop actually needs -- 32x more bytes moved than necessary.
  At 256 MB total and no reuse (each record is touched exactly once, so there's no help from
  temporal locality, co-04), this is a bandwidth-bound streaming workload through DRAM once the
  working set exceeds this machine's 4 MiB L2.
- **SoA**: each 128 B cache line now holds 32 consecutive `reading` values, all of them useful.
  The same 2M-element sum now moves roughly 8 MB of real memory traffic instead of 256 MB --
  a 32x reduction in bytes fetched from memory for the identical arithmetic, which is why the
  measured 3.7x wall-clock speedup (not the full theoretical 32x -- allocation, the accumulator's
  `double` division, and this machine's own memory-level parallelism all narrow the gap between
  the "bytes moved" ratio and the "wall clock" ratio) is entirely explained by co-02
  (cache-lines-and-blocks): AoS wastes 124 of every 128 fetched bytes; SoA wastes none.
- This is the same mechanism `ex-30` (AoS-vs-SoA-hot-loop) and `ex-58` (optimize-kernel-end-to-end)
  demonstrate elsewhere in this topic, at capstone scale on a purpose-built sensor-telemetry
  dataset rather than a synthetic one -- proof the lesson generalizes past a single canned example.

**Acceptance criteria met**: representation and endianness hazards demonstrated (Step 1);
the layout change (AoS to SoA) produces a measured, reproducible speedup with unchanged results
(Steps 2-3); this explanation grounds every number in the memory-hierarchy mechanism that produced
it, per the syllabus's capstone spec.

---

← Previous: [Advanced Examples](../advanced.md) &middot; Next: [Drilling](../../drilling/overview.md)
→
