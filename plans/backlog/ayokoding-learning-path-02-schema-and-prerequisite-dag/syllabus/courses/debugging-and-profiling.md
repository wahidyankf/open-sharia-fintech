# Debugging and Profiling (By Example, Python + native)

**Course ID**: `debugging-and-profiling` · **Format**: By Example · **Language**: Python + native.

**Short summary**: Systematic debugging and performance profiling

**Scope note**: finding and fixing what the tests didn't catch — interactive debuggers (breakpoints,
watches, stepping), sampling versus instrumenting profilers, flame graphs, and a systematic bisection
method. `†`: fully type-annotated Python examples (DD-39) plus a native-profiler pass to see costs the
interpreter hides. Builds directly on [`15-software-testing`](./software-testing.md) — tests tell
you _that_ something is wrong; this topic is _where_ and _why_.

## Why this exists · the big idea

- **The problem before the solution**: a failing test tells you something is wrong but not where or
  why; `print`-driven guessing scales poorly, and optimizing by hunch tunes the wrong 90% while the
  real bottleneck sits untouched.
- **Keep-this-if-you-forget-everything**: debugging is a search — form a hypothesis, change one thing,
  observe, halve the space; performance work is measure-first, because the hot spot is almost never
  where you would have guessed.
- **Big ideas touched**: `layering-and-leaks` (a bug or a hot spot usually lives at a seam — your code,
  the runtime, the OS, the CPU cache — and a profiler is how you see through the layer),
  `determinism-vs-emergence` (the hardest bugs are emergent — races, heisenbugs, load-dependent
  slowdowns — reproducible only by controlling the interaction, not the line).

## Prerequisites

- **Prior topics**: [topic 4 Just Enough Python](./just-enough-python.md),
  [topic 5 Just Enough Bash](./just-enough-bash.md), and
  [topic 15 Software Testing](./software-testing.md).
- **Tools & environment**: a macOS/Linux terminal; an interactive debugger (`pdb`/`debugpy` for
  Python, `gdb`/`lldb` for native); a sampling profiler and an instrumenting one (`cProfile`-style); a
  flame-graph renderer; Neovim/VSCode with DAP debugger integration (DD-17).
- **Assumed knowledge**: reading a stack trace and writing a failing test (topic 15); driving CLI
  tools (topic 05); reading a typed Python module (topic 04).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the concepts (breakpoint/watch/step debugging, sampling vs instrumenting
  profilers, flame graphs, bisection) are tool-independent and stable; tool names are left generic and
  version-unpinned on purpose. Python's `pdb`/`cProfile` are standard-library and current; native
  `perf`/`gdb`/`lldb` behavior is stable across recent releases.
- 2026-07-12 — verified: flame graphs (Brendan Gregg's visualization) remain the standard way to read
  a profile; there is no version to pin. `py-spy` emits `--format speedscope` natively (viewable in
  speedscope) and `inferno` is a drop-in Rust reimplementation of the collapse+render pipeline.
- 2026-07-12 — verified (enrichment): `pdb` gained real remote-attach in 3.14 (`python -m pdb -p <pid>`,
  `await pdb.set_trace_async()`, a `sys.monitoring`/PEP-669 trace backend); Python 3.12+ ships built-in
  `perf`-map support (`python -X perf` / `PYTHONPERFSUPPORT=1`) so Python frames show real names in
  `perf report`. Native-debugger asymmetry to note: `gdb` bundles Python-awareness (`py-bt`/`py-locals`
  via `python-gdb.py`), but `lldb` needs the third-party `cpython_lldb` package + `~/.lldbinit` on macOS.
  Delta-debugging has no canonical package — implement a small `ddmin` directly (per debuggingbook.org).

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (subject By-Example). Each example below cites the co-NN it exercises. -->

- **co-01 · interactive-breakpoints-and-stepping** — pausing execution at a chosen line and driving it
  forward with step-into / step-over / step-out, versus letting it run to completion.
- **co-02 · conditional-and-watch-breakpoints** — halting only when a predicate holds (`i == 47`,
  `id(obj)==…`) or a value changes, instead of stopping on every hit.
- **co-03 · call-stack-frame-and-variable-inspection** — reading the stack, moving between frames, and
  printing or mutating locals at a paused point to test a hypothesis.
- **co-04 · post-mortem-debugging** — entering a debugger on an already-thrown, uncaught exception
  (`pdb.pm()`, `python -m pdb`) to inspect the failing frame without a rerun.
- **co-05 · print-and-logging-vs-interactive-debugging** — when `print`/`logging` beats a breakpoint
  (long-lived processes, production, timing) and when it does not (one-off, deep state).
- **co-06 · remote-and-dap-debugging** — attaching a debugger to an already-running process over the
  Debug Adapter Protocol (`debugpy`, editor DAP) or `pdb -p <pid>`.
- **co-07 · scientific-method-debugging-loop** — expected-vs-actual, one falsifiable hypothesis, one
  change, observe, repeat — debugging as controlled experiment, not guessing.
- **co-08 · bisection-search-as-a-general-strategy** — halving the search space (commits, input, code
  region) to localize a fault in logarithmic rather than linear steps.
- **co-09 · git-bisect-manual** — driving `git bisect start/good/bad` by hand to name the commit that
  introduced a regression.
- **co-10 · git-bisect-automated** — `git bisect run <script>` with a pass/fail (or 125-skip) exit code
  so the whole search runs unattended.
- **co-11 · delta-debugging-input-minimization** — shrinking a failing input to a 1-minimal reproducer
  (hand-rolled `ddmin`, Hypothesis shrinking) so every remaining piece is necessary.
- **co-12 · sampling-vs-instrumenting-profilers** — periodic stack sampling (low overhead, statistical)
  versus per-call instrumentation (exact counts, high overhead), and when each is right.
- **co-13 · cpu-profiling-with-cprofile** — the stdlib instrumenting profiler: running it from the CLI
  or programmatically and reading its `pstats` table.
- **co-14 · cpu-profiling-with-py-spy** — a sampling profiler that attaches to a live PID with no code
  changes (`top`, `record`, `dump`, `--native`).
- **co-15 · wall-clock-vs-cpu-time** — distinguishing elapsed time (`perf_counter`) from on-CPU time
  (`process_time`); I/O-bound vs CPU-bound diagnosis.
- **co-16 · tottime-vs-cumtime** — a function's own time versus time including callees, and which one to
  optimize (many-cheap leaf vs one-expensive parent).
- **co-17 · memory-profiling-with-tracemalloc** — snapshotting allocations, diffing two snapshots to
  find a leak, and widening the traceback (`nframe`) to split allocation sites.
- **co-18 · line-level-profiling** — attributing cost to individual source lines (`line_profiler`
  `@profile` + `kernprof`), one resolution finer than function-level.
- **co-19 · flame-graph-reading** — width = total time in a call subtree, height = stack depth; finding
  the widest frame (hot spot), not the tallest stack.
- **co-20 · race-and-heisenbug-reproduction** — forcing nondeterministic concurrency bugs to reproduce
  reliably (forced yields, seeds, barriers) before attempting a fix.
- **co-21 · load-representative-vs-toy-profiling** — profiling at realistic scale and concurrency,
  because the hot spot at 100 items or single-call differs from production.
- **co-22 · native-layer-costs-and-native-debugging** — seeing costs the interpreter hides: `gdb`/`lldb`
  Python-aware backtraces, `perf` with Python perf-maps, `py-spy --native`, core dumps.
- **co-23 · before-after-measurement-discipline** — proving a fix with a repeated (median-of-N)
  before/after measurement rather than a single lucky run or a hunch.

## Worked examples

Colocated under `debugging-and-profiling/learning/code/`; each is a seeded bug or slow function you
diagnose from the CLI, fully type-annotated Python (DD-20/DD-30/DD-34/DD-39) with one native pass. Contiguous
`ex-01..ex-80`; every example cites the `co-NN` it exercises.

- **ex-01 · first-breakpoint-with-breakpoint** — insert `breakpoint()` in a running-total function and step with `n` — verify the reader names the exact line the total first goes wrong. (co-01)
- **ex-02 · step-into-vs-step-over** — at a breakpoint before a helper call, use `s` then `n` — verify the transcript shows `s` entering the helper and `n` skipping past the call. (co-01)
- **ex-03 · step-out-of-a-deep-call** — breakpoint three calls deep, `r` to pop to the caller — verify pdb prints the function's actual return value on return. (co-01)
- **ex-04 · reading-the-call-stack-with-w** — breakpoint three frames deep, `w` — verify the reader names the frame that owns the bad variable. (co-03)
- **ex-05 · navigating-frames-with-up-down** — `u`/`d` and print the same name at two frames — verify two different values are captured. (co-03)
- **ex-06 · inspecting-locals-with-p-and-pp** — `p`/`pp` in a dict-building function — verify the reader identifies the reused/shadowed key. (co-03)
- **ex-07 · mutating-a-variable-to-confirm-hypothesis** — reassign a wrong var to the expected value and continue — verify post-mutation output matches expected. (co-03, co-07)
- **ex-08 · conditional-breakpoint-in-a-loop** — `break lineno, i == 47` in a 100-iteration loop — verify pdb halts exactly once, at i==47. (co-02)
- **ex-09 · condition-command-on-existing-breakpoint** — `condition 1 x < 0` — verify positive-x hits continue and only negative x stops. (co-02)
- **ex-10 · watching-a-variable-with-display** — `display total` across iterations — verify the transcript shows `[old → new]` only when total changes. (co-02)
- **ex-11 · display-in-place-mutation-caveat** — `display lst` then mutate the list in place — verify the reader explains the silence and fixes it with `display lst[:]`. (co-02)
- **ex-12 · print-debugging-a-one-off-script** — diagnose with only `print()`, then remove them — verify the same bug is found and the rerun-per-hypothesis cost is noted. (co-05)
- **ex-13 · logging-vs-print-in-long-lived-process** — replace prints with `logging` levels — verify the bug is found from log output with no pause. (co-05)
- **ex-14 · breakpoint-builtin-and-pythonbreakpoint** — compare `pdb.set_trace()` and `breakpoint()`; `PYTHONBREAKPOINT=0` disables — verify unset stops, `0` skips. (co-01)
- **ex-15 · first-post-mortem-with-pdb** — an uncaught raise run under `python -m pdb script.py` — verify the debugger lands on the raising frame with the offending var visible. (co-04)
- **ex-16 · pdb-pm-in-a-repl-session** — raise in a REPL, then `pdb.pm()` with no restart — verify it reaches the same frame/state a live breakpoint would. (co-04)
- **ex-17 · first-cprofile-run-command-line** — `python -m cProfile -s cumulative script.py` — verify the reader names the top-cumulative-time function. (co-13)
- **ex-18 · cprofile-programmatic-with-pstats** — `cProfile.Profile()`, top 5 by `SortKey.TIME` — verify the top-1 by tottime differs from the top-1 by cumtime, and the reader explains why. (co-13, co-16)
- **ex-19 · wall-time-vs-cpu-time** — time an I/O-sleep function with `perf_counter()` and `process_time()` — verify wall ≫ CPU for the sleep and wall ≈ CPU for a busy loop. (co-15)
- **ex-20 · first-tracemalloc-snapshot** — `tracemalloc.start()`, allocate a big list, top-5 `statistics('lineno')` — verify the top line matches the list-building line. (co-17)
- **ex-21 · reading-a-pregenerated-flame-graph** — given an SVG, identify the widest frame and the deepest stack — verify the reader names the widest frame as the hot spot, distinct from the tallest stack. (co-19)
- **ex-22 · git-bisect-by-hand** — a 5-commit repo with a seeded regression, `git bisect start/good/bad` — verify git names the exact bad commit. (co-09, co-08)
- **ex-23 · rubber-duck-hypothesis-writing** — write expected-vs-actual plus one falsifiable hypothesis, then verify it with one breakpoint — verify it is confirmed or refuted in exactly one stop. (co-07)
- **ex-24 · minimizing-a-failing-input-by-hand** — manually halve a 200-char failing string — verify the failing region is under 50 chars in ≤4 steps. (co-08, co-11)
- **ex-25 · sticky-mode-and-list-command** — `l`/`ll` at a breakpoint — verify the reader spots a nearby line that also needs the fix. (co-01, co-03)
- **ex-26 · tbreak-one-shot-breakpoint** — `tbreak` to stop only on the first call — verify it stops once and runs on afterward. (co-01)
- **ex-27 · before-after-timing-a-one-line-fix** — median of 5 `perf_counter()` runs before and after — verify "after" is consistently faster, not a one-off. (co-23)
- **ex-28 · profiling-two-ways-sampling-and-instrumenting** — the same function via `cProfile` and `py-spy record` — verify both agree on the top function, or the discrepancy is explained. (co-12, co-13, co-14)
- **ex-29 · py-spy-top-live-view** — `py-spy top --pid` on a running script — verify the predicted hot function tops the live view. (co-14, co-12)
- **ex-30 · py-spy-record-flamegraph-svg** — `py-spy record -o profile.svg` — verify the widest SVG frame matches cProfile's top function. (co-14, co-19)
- **ex-31 · py-spy-record-speedscope** — `--format speedscope` loaded in speedscope — verify the "left heavy" view surfaces the same hot function. (co-14, co-19)
- **ex-32 · py-spy-dump-on-a-hung-process** — `py-spy dump --pid` on an infinite loop — verify the dumped stack shows the stuck line. (co-14, co-03)
- **ex-33 · sorting-pstats-tottime-vs-cumtime** — one `.prof`, sort by TIME and by CUMULATIVE — verify both rankings are labelled (many-cheap-leaf vs one-expensive-parent). (co-16, co-13)
- **ex-34 · line-profiler-kernprof** — `@profile` + `kernprof -l -v` — verify the reported hot line matches a seeded redundant re-sort. (co-18)
- **ex-35 · line-profiler-vs-function-level** — cProfile attributes to one function, line_profiler to one line — verify the reader states the exact hot line. (co-18, co-13)
- **ex-36 · tracemalloc-snapshot-diff-for-a-leak** — two snapshots around N iterations of an unbounded cache, `compare_to()` — verify the top diff line is the append line and grows with N. (co-17)
- **ex-37 · tracemalloc-nframe-traceback** — `nframe=5` vs `nframe=1` to split two paths identical at one frame — verify only one path is the real leak. (co-17)
- **ex-38 · conditional-breakpoint-on-object-identity** — `break lineno, id(obj)==some_id` — verify it stops only on that instance. (co-02)
- **ex-39 · commands-attached-to-a-breakpoint** — pdb `commands` auto-running `p x; c` — verify it runs unattended through uninteresting hits. (co-01, co-02)
- **ex-40 · debugpy-attach-to-a-running-server** — `python -m debugpy --listen 5678`, attach a DAP client, breakpoint on the next request — verify the client stops and a local var is inspectable. (co-06)
- **ex-41 · debugpy-wait-for-client-vs-attach-later** — `--wait-for-client` vs attaching later — verify only wait-for-client catches an import-time bug. (co-06)
- **ex-42 · pdb-remote-attach-by-pid** — `python -m pdb -p <pid>` with no prior instrumentation (3.14+) — verify the session shows the live stack without a restart. (co-06, co-04)
- **ex-43 · git-bisect-run-automated** — a script running a failing pytest, `git bisect run ./check.sh` — verify it names the same commit unattended. (co-10, co-08)
- **ex-44 · git-bisect-run-skip-125** — seed an unbuildable commit whose script exits 125 — verify the final result still names the true culprit. (co-10)
- **ex-45 · delta-debugging-a-json-payload** — `ddmin` against a 500-key crashing JSON — verify the minimized payload still crashes and is under 5 keys. (co-11)
- **ex-46 · delta-debugging-a-long-string** — `ddmin` to a 1-minimal substring — verify removing any remaining char clears the bug. (co-11)
- **ex-47 · hypothesis-shrinking-as-delta-debugging** — Hypothesis auto-shrink vs the hand-rolled `ddmin` — verify the shrunk example is comparably minimal. (co-11)
- **ex-48 · profiling-toy-vs-realistic-input** — profile at 100 vs 1,000,000 items — verify the toy-scale hot spot differs from the realistic-scale one. (co-21)
- **ex-49 · profiling-under-concurrent-load** — a handler single-call vs several threads — verify lock-contention/wait shows up only under load. (co-21)
- **ex-50 · pdb-interact-mode** — `interact` at a breakpoint for a frame-scoped REPL — verify the experiment's corrected value is copied into the real fix. (co-03, co-07)
- **ex-51 · pdb-exceptions-command-chained** — `raise … from …`, pdb `exceptions` in post-mortem — verify the reader identifies the root-cause exception. (co-04, co-03)
- **ex-52 · logging-config-multi-module-bug** — per-module `getLogger(__name__)` + `dictConfig` — verify the cause is found from correlated log lines with no breakpoints. (co-05)
- **ex-53 · cprofile-to-flame-graph** — convert a `.prof` via `gprof2dot`/`snakeviz` and compare to py-spy's — verify both point at the same widest frame. (co-19, co-13)
- **ex-54 · neovim-dap-breakpoint** — a breakpoint via `nvim-dap-python`, inspect a var in the scopes view — verify the DAP UI stops at the same line/value as CLI pdb. (co-06, co-01)
- **ex-55 · before-after-with-cprofile** — re-profile a fixed hot spot and confirm its `tottime` share dropped — verify the percent-of-total drop is measurable. (co-23, co-13)
- **ex-56 · reproducing-a-threading-race** — a plain-int increment across threads with no lock, 100× — verify at least one run shows a final count below expected. (co-20)
- **ex-57 · fixing-the-race-with-a-lock** — add a `threading.Lock` and rerun the loop — verify 100+ runs are all exact. (co-20, co-23)
- **ex-58 · asyncio-interleaving-bug** — check-then-act on a shared dict across two coroutines, forcing a yield with `asyncio.sleep(0)` — verify a reliable failure under the forced yield. (co-20)
- **ex-59 · pdb-set-trace-async** — `await pdb.set_trace_async()` at an await, inspect `$_asynctask` — verify it identifies the paused coroutine's Task. (co-01, co-06)
- **ex-60 · multiprocessing-vs-threading-profiling** — a CPU-bound job via threading vs multiprocessing, watched with py-spy — verify threaded wall ≈ single-thread CPU (GIL) while mp wall drops toward CPU/cores. (co-14, co-15, co-21)
- **ex-61 · git-bisect-run-perf-regression** — a check script that fails when a benchmark exceeds a threshold — verify the parent/child benchmark confirms the crossing at the named commit. (co-10)
- **ex-62 · delta-debugging-10000-line-crash** — automated `ddmin` on a large crashing input down to under 10 lines — verify the reduced input triggers the identical exception. (co-11)
- **ex-63 · gdb-attach-to-cpython** — `gdb -p <pid>` with `python-gdb.py`, `py-bt` — verify the frame names match a py-spy dump. (co-22)
- **ex-64 · gdb-py-locals-py-print** — `py-locals`/`py-print` reading a Python local from process memory — verify the value matches logging. (co-22, co-03)
- **ex-65 · lldb-with-cpython-lldb** — macOS `pip install cpython_lldb`, `lldb -p <pid>`, `py-bt` — verify py-bt shows the Python stack, matching gdb. (co-22)
- **ex-66 · lldb-core-dump-postmortem** — a core dump from a crashed native extension, `lldb <bin> -c <core>` — verify the backtrace shows the seeded fault's function. (co-22, co-04)
- **ex-67 · perf-record-with-python-perf-support** — `python -X perf` + `perf record -F 99 -g` — verify `perf report` shows readable Python names, not opaque symbols. (co-22)
- **ex-68 · perf-script-to-flamegraph-pl** — `stackcollapse-perf.pl` + `flamegraph.pl` — verify the SVG's widest frame is a Python name. (co-19, co-22)
- **ex-69 · perf-script-to-inferno** — regenerate with `inferno-collapse-perf` + `inferno-flamegraph` — verify the same widest frame, tool-independent. (co-19)
- **ex-70 · native-cost-hidden-from-cprofile** — profile a C-extension call with cProfile (one line) then perf/py-spy `--native` — verify native profiling reveals the internal C hot functions. (co-22, co-13)
- **ex-71 · py-spy-native-flag-mixed-stacks** — `py-spy record --native` — verify the mixed Python+native flame graph shows native frames under the Python caller. (co-14, co-19, co-22)
- **ex-72 · correctness-and-performance-bug** — one repo with a seeded correctness bug and a seeded perf regression; bisect+fix+test first, profile+fix+measure second — verify the bisect is correct, the regression test goes red→green, and the profiled fix is measured with no regressions. (co-09, co-10, co-04, co-13, co-23)
- **ex-73 · recursive-tottime-vs-cumtime-trap** — a recursive function whose wrapper's cumtime looks alarming but tottime is tiny — verify the fix targets the leaf pstats names by tottime. (co-16, co-13)
- **ex-74 · cache-that-never-evicts-leak** — an unbounded dict cache found via tracemalloc diffing, fixed with eviction — verify a third snapshot shows near-zero net growth. (co-17, co-23)
- **ex-75 · import-time-startup-profiling** — `python -X importtime` + cProfile around imports — verify deferring the named module reduces startup wall time. (co-13, co-23, co-22)
- **ex-76 · lock-contention-under-load** — profile a coarse-lock function single vs many concurrent callers with `py-spy top` — verify threads visibly wait (a wall-vs-CPU gap) only under load. (co-21, co-20, co-15)
- **ex-77 · flame-graph-diff-before-after** — two flame graphs before/after a hot-path fix — verify the wide frame shrinks proportionally and nothing else grew. (co-19, co-23)
- **ex-78 · deterministic-seeding-for-a-flaky-bug** — pin the seed, add a scheduling barrier, freeze the clock — verify a ~1-in-20 CI failure now reproduces on every local run. (co-20, co-07)
- **ex-79 · bisecting-with-a-flaky-test-guard** — retry a borderline check N times and report bad on the majority — verify the guarded runs converge on the same correct commit. (co-10, co-20)
- **ex-80 · sys-monitoring-low-overhead-tracer** — a minimal line tracer via `sys.monitoring` (PEP 669) vs `sys.settrace` — verify the `sys.monitoring` overhead is measurably lower. (co-22, co-23)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: take a repo with one seeded correctness bug and one seeded performance bug and resolve both
  by method — bisect and minimize the failing case, fix it with a regression test; profile and fix the
  hot path with a before/after measurement.
- **Concepts exercised**: [ ] a debugger session — breakpoints/watch/step (co-01, co-02, co-03)
  [ ] `git bisect` to the offending commit (co-09, co-10) [ ] delta-debugging to a minimal input
  (co-11) [ ] a sampling + instrumenting profile (co-12, co-13, co-14) [ ] a flame-graph read (co-19)
  [ ] a documented before/after speedup (co-23).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — reproduce the correctness bug; `git bisect` to the introducing
     commit and minimize the failing input. Verify the minimal case still fails.
  2. Fix the bug with a debugger-guided change plus a regression test. Verify the test fails before the
     fix and passes after.
  3. Profile the slow path (sampling then instrumenting), render a flame graph, and identify the hot
     spot. Verify both profilers agree on the hot spot.
  4. Fix the hot spot and re-measure. Verify a documented before/after improvement with no test
     regressions.
- **Acceptance criteria**: the regression is bisected and covered by a failing→passing test; the hot
  spot is identified from a profile (not a guess) and measurably improved.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Why Programs Fail: A Guide to Systematic Debugging** — Andreas Zeller (2005). First comprehensive
  treatment of debugging as a systematic, teachable discipline.
- **Debugging: The 9 Indispensable Rules** — David J. Agans (2002). Concise, tool-agnostic heuristics
  for isolating faults.
- **Systems Performance** — Brendan Gregg (2nd ed., 2020). Standard reference for methodical
  performance analysis and profiling on Linux and in the cloud.

**Papers & articles**

- **What Every Programmer Should Know About Memory** — Ulrich Drepper (2007). Canonical explanation of
  cache and memory-hierarchy behavior for making sense of profiler output.
  <https://people.freebsd.org/~lstewart/articles/cpumemory.pdf>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Ops, platform, quality & product — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Quality, product, delivery & leadership — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 14 · Quality, product, delivery & leadership.

> _Content originated in the now-closed FS-SE plan (topic 16); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
