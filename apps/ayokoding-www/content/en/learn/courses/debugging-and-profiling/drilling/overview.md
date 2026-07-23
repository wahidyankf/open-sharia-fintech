---
title: "Overview"
date: 2026-07-15T00:00:00+07:00
draft: false
weight: 1
---

This page is the active-recall companion to the Debugging & Profiling learning track: four fixed
drills that force retrieval instead of passive re-reading. Work through them in order -- short-answer
recall first, then scenario judgment, then hands-on implementation, then a checklist to confirm real
automaticity. Every answer is hidden in a `<details>` block; try each item yourself, out loud or on
paper, before opening it. Every prompt below uses its own mocked, self-contained scenario -- different
function names, domains, and situations from anything in the learning track's 80 worked examples -- so
recognizing an answer isn't enough; you have to actually reconstruct the reasoning. Nothing on this
page requires `gdb`/`lldb`/`perf`/`py-spy`, a live process attach, or root access -- every scenario is
reasoned about on paper.

## Recall Q&A

Twenty-three short-answer questions, one per concept (`co-01` through `co-23`). Answer from memory,
then check.

**Q1 (co-01 -- interactive-breakpoints-and-stepping).** Name the three ways a paused debugger can
resume execution one unit at a time, and what distinguishes each.

<details>
<summary>Answer</summary>

Step-into (enters the next function call, if any, and pauses at its first line), step-over (runs the
next line to completion, including any function calls inside it, without pausing inside them), and
step-out (runs until the current function returns, pausing back in its caller). All three contrast
with "continue," which runs to completion or the next breakpoint instead of one unit at a time.

</details>

**Q2 (co-02 -- conditional-and-watch-breakpoints).** A loop runs 50,000 times, and a bug only shows up
on iteration 4,213. What debugger feature avoids manually resuming 4,212 times?

<details>
<summary>Answer</summary>

A conditional breakpoint -- one that only halts execution when a predicate evaluates true (e.g.
`i == 4213`), rather than on every single hit. The debugger still evaluates the condition on every
pass through the breakpoint's line, but only actually stops and hands control back once it's true.

</details>

**Q3 (co-03 -- call-stack-frame-and-variable-inspection).** At a paused breakpoint three functions deep,
what command family lets a developer read (and test a fix against) a variable that belongs to the
CALLER, not the current function?

<details>
<summary>Answer</summary>

Frame-navigation commands (`up`/`down` in `pdb`) move the debugger's current context to an enclosing
(or inner) frame without resuming execution -- once moved, ordinary variable-printing commands (`p`)
read locals from THAT frame, letting a developer inspect or test-evaluate an expression against the
caller's own state.

</details>

**Q4 (co-04 -- post-mortem-debugging).** A script crashes with an uncaught exception before a developer
attached any debugger. What lets them still inspect the exact failing frame's locals, without
re-running the script under a debugger from the start?

<details>
<summary>Answer</summary>

Post-mortem debugging -- `python -m pdb script.py` (which automatically drops into the debugger at the
crash site when an uncaught exception propagates to the top) or `pdb.pm()` (which inspects the most
recent traceback interactively, after the fact) -- both open a real debugger session rooted at the
frame where the exception actually occurred, with all its locals still intact.

</details>

**Q5 (co-05 -- print-and-logging-vs-interactive-debugging).** A background worker process runs
continuously in production and occasionally corrupts one field in a queue message. Why is `print`/
`logging` usually the right first tool here, over an interactive breakpoint?

<details>
<summary>Answer</summary>

An interactive breakpoint would pause the ENTIRE process, which is unacceptable for a live,
continuously-running service -- and a rare, occasional bug means the developer may not even be present
when the breakpoint would hit. Structured logging at the suspect point runs non-blocking, every time,
and accumulates evidence across many real occurrences without ever stopping the process.

</details>

**Q6 (co-06 -- remote-and-dap-debugging).** A process is already running inside a container with no
terminal attached. What lets a developer pause it at a real breakpoint anyway, from their own editor?

<details>
<summary>Answer</summary>

Remote/DAP debugging -- a debug adapter (e.g. `debugpy`) running inside the already-live process
listens for a connection over the Debug Adapter Protocol; an editor's DAP client connects to it
remotely, sets breakpoints, and receives `stopped`/`scopes`/`variables` events exactly as it would for
a locally-launched process, without ever needing a terminal inside the container itself.

</details>

**Q7 (co-07 -- scientific-method-debugging-loop).** A developer changes three things at once, re-runs a
failing test, and it passes. Why does this NOT actually tell them which change fixed the bug?

<details>
<summary>Answer</summary>

The scientific-method debugging loop requires ONE falsifiable hypothesis and ONE change per iteration,
observed before the next change -- changing three things at once confounds the result: any one of the
three (or some combination) could be responsible, and there is no way to isolate which, without
reverting two of the three and re-testing individually.

</details>

**Q8 (co-08 -- bisection-search-as-a-general-strategy).** A 100,000-line log file contains exactly one
line that triggers a downstream parser crash. Roughly how many candidate cuts does a bisection search
need to isolate it, compared to a linear scan?

<details>
<summary>Answer</summary>

Roughly log2(100,000), about 17 cuts, versus up to 100,000 individual checks for a linear scan --
bisection halves the remaining search space on every step, turning a linear-time search into a
logarithmic one, regardless of whether the search space is commits, lines, or a numeric range.

</details>

**Q9 (co-09 -- git-bisect-manual).** What are the exact three `git bisect` subcommands a developer
types by hand to start narrowing a regression to one commit, and what does each one tell git?

<details>
<summary>Answer</summary>

`git bisect start` begins the session; `git bisect bad <commit>` (often `HEAD`) names a commit known
to exhibit the bug; `git bisect good <commit>` names an earlier commit known to be free of it. Git then
checks out the midpoint commit and waits for the developer to manually test it and report `git bisect
good` or `git bisect bad` again, repeating until only one candidate commit remains.

</details>

**Q10 (co-10 -- git-bisect-automated).** What must a script return for `git bisect run <script>` to
correctly report "this commit is fine," and what special exit code means "skip this commit entirely"?

<details>
<summary>Answer</summary>

Exit code `0` means good (the bug is absent at this commit); any nonzero exit code except `125` means
bad; exit code `125` specifically tells `git bisect run` to SKIP this commit (e.g. because it doesn't
build, or the check is inapplicable at this point in history) without treating it as either good or
bad evidence.

</details>

**Q11 (co-11 -- delta-debugging-input-minimization).** A 500-line config file crashes a parser. What
property must EVERY remaining line have once delta-debugging (`ddmin`) finishes minimizing it?

<details>
<summary>Answer</summary>

1-minimality -- removing ANY single remaining line (or chunk, at the finest granularity the algorithm
reached) causes the failure to STOP reproducing. Every remaining piece is individually necessary to
trigger the exact same failure signature; nothing left in the minimized input is incidental.

</details>

**Q12 (co-12 -- sampling-vs-instrumenting-profilers).** Contrast the overhead and accuracy tradeoff
between a sampling profiler and an instrumenting profiler, in one sentence each.

<details>
<summary>Answer</summary>

A sampling profiler periodically snapshots the call stack from outside the running program (low
overhead, since it never intercepts every call/return, but statistical -- fast functions can be
under-sampled). An instrumenting profiler intercepts every single call and return event to record
exact counts and timings (precise, but the interception itself adds real overhead that can distort
timing, especially for functions with many cheap calls).

</details>

**Q13 (co-13 -- cpu-profiling-with-cprofile).** After running `cProfile.Profile()` around a function
call, what stdlib module turns the raw profile into a sorted, readable table, and what's the minimal
sequence of calls to print the top 10 rows by cumulative time?

<details>
<summary>Answer</summary>

`pstats`. The minimal sequence is `stats = pstats.Stats(profiler); stats.sort_stats(pstats.SortKey
.CUMULATIVE); stats.print_stats(10)` -- `pstats.Stats` wraps the raw `Profile` object, `sort_stats`
picks the ordering, and `print_stats(N)` prints only the top N rows.

</details>

**Q14 (co-14 -- cpu-profiling-with-py-spy).** What is `py-spy`'s single biggest advantage over
`cProfile` for diagnosing a slow process already running in production?

<details>
<summary>Answer</summary>

`py-spy` attaches to an ALREADY-RUNNING process by PID, with zero code changes and zero restart
required -- `cProfile` requires the profiled code to run INSIDE a `Profile()` context from the start,
which means either restarting the process or having instrumented it in advance. `py-spy`'s
attach-to-a-live-PID model is what makes it usable for "this process is slow right now" investigations.

</details>

**Q15 (co-15 -- wall-clock-vs-cpu-time).** A function takes 500ms of wall-clock time but only 40ms of
CPU time. What does that gap most likely indicate, and which Python stdlib call measures each?

<details>
<summary>Answer</summary>

The gap indicates the function spent most of its time WAITING (I/O, a lock, a network call, a sleep)
rather than actually computing -- it is I/O-bound, not CPU-bound. `time.perf_counter()` measures
elapsed wall-clock time; `time.process_time()` measures only CPU time actually consumed by the process,
excluding time spent waiting.

</details>

**Q16 (co-16 -- tottime-vs-cumtime).** A `pstats` table shows function `dispatch()` with a huge
`cumtime` but a tiny `tottime`. Should a developer optimize `dispatch()` itself? Why or why not?

<details>
<summary>Answer</summary>

No -- `cumtime` includes every function `dispatch()` calls, recursively, while `tottime` is
`dispatch()`'s OWN time, excluding all callees. A huge `cumtime` with a tiny `tottime` means
`dispatch()` itself does almost no work; nearly all the cumulative time belongs to whatever it calls.
The fix target is whichever CALLEE has the largest `tottime`, not the dispatcher/wrapper itself.

</details>

**Q17 (co-17 -- memory-profiling-with-tracemalloc).** Two `tracemalloc` snapshots, taken before and
after a burst of activity, show memory grew by 5MB. Why is a THIRD snapshot, after an equivalent
second burst, necessary to actually confirm a leak?

<details>
<summary>Answer</summary>

Two snapshots can only show growth happened once -- which is also consistent with a legitimate cache or
buffer warming up and then stabilizing. A third snapshot, after an equivalent second burst of the SAME
kind of activity, distinguishes the two cases: if the second burst also grows memory by roughly 5MB
(proportional, repeated growth), that's a genuine leak; if the second burst adds close to zero net
growth, the first snapshot's growth was one-time stabilization, not a leak.

</details>

**Q18 (co-18 -- line-level-profiling).** `cProfile` says a 40-line function has a high `tottime`, but
does not say WHICH of the 40 lines is expensive. What tool provides that finer resolution, and what
decorator does it require?

<details>
<summary>Answer</summary>

`line_profiler` (run via its `kernprof` CLI wrapper) attributes cost to individual SOURCE LINES inside
a function, one resolution finer than `cProfile`'s function-level granularity. It requires the target
function to be decorated with `@profile` (a name `kernprof` injects into the global namespace at run
time, not a normal import) before running `kernprof -l -v script.py`.

</details>

**Q19 (co-19 -- flame-graph-reading).** In a flame graph, what does WIDTH represent, and what does
HEIGHT represent -- and which one identifies the actual hot spot?

<details>
<summary>Answer</summary>

Width represents the total time (or sample count) attributed to a call subtree -- the wider a frame,
the more total time was spent inside it (and everything it calls). Height represents call-stack
DEPTH -- how many frames deep that sample was captured, not how expensive it was. The hot spot is
identified by finding the WIDEST frame, not the tallest stack; a very deep but narrow stack can be
cheap, while a shallow but wide frame is where the real time goes.

</details>

**Q20 (co-20 -- race-and-heisenbug-reproduction).** A concurrency bug reproduces roughly 1-in-50 runs
on CI but never locally. What is the general strategy for making it reproduce reliably enough to debug
interactively, and name two concrete mechanisms that strategy might use.

<details>
<summary>Answer</summary>

Force the specific interleaving or timing condition that triggers the bug, rather than hoping natural
scheduling jitter reproduces it. Concrete mechanisms include: a forced explicit yield point (e.g.
`asyncio.sleep(0)` inside a check-then-act sequence, widening the race window on purpose), a
`threading.Barrier` to force multiple threads to reach a critical point simultaneously, and pinning a
random seed that stands in for whichever nondeterministic choice actually drives the rare outcome.

</details>

**Q21 (co-21 -- load-representative-vs-toy-profiling).** A function is profiled against a 10-item test
list and shows no meaningful hot spot. In production it processes 500,000 items and is measurably
slow. What's the likely mistake in how it was profiled?

<details>
<summary>Answer</summary>

Profiling at toy scale instead of load-representative scale -- an O(n) versus O(n^2) difference (or
any superlinear cost) is invisible or negligible at n=10 but dominates at n=500,000. A profile's
answer about WHICH function is the hot spot can genuinely change with scale, so profiling must be done
at a size and concurrency level that resembles production, not a small convenience sample.

</details>

**Q22 (co-22 -- native-layer-costs-and-native-debugging).** `cProfile` shows a call into a C extension
as a single opaque line with no internal breakdown. What class of tool is needed to see costs INSIDE
that C code, and name one example.

<details>
<summary>Answer</summary>

A native-aware profiler or debugger -- one that instruments at the OS/native level rather than only
intercepting CPython's own interpreter call/return events. Examples include `perf record` (Linux,
kernel-level sampling with Python-aware symbol resolution via `-X perf`), `py-spy record --native`
(samples both Python and native frames in one flame graph), and `gdb`/`lldb` with a Python-aware
extension (`python-gdb.py`, `cpython_lldb`) for reading Python-level state from within a native
debugger session.

</details>

**Q23 (co-23 -- before-after-measurement-discipline).** A developer applies a performance fix, runs the
function once before and once after, and reports "3x faster." What's wrong with that measurement, and
what should replace it?

<details>
<summary>Answer</summary>

A single before-run and a single after-run are each vulnerable to one-off noise (a cold cache, a
background process, OS scheduling jitter) -- the "3x" could easily be measurement noise rather than a
real effect. The fix is a repeated, median-of-N measurement on BOTH sides (e.g. run each version 9
times, take the median), which is resistant to any one outlier run in either direction, producing a
number that actually reflects the fix's real, repeatable effect.

</details>

## Applied problems

Twelve scenarios spanning beginner through native-and-systems material. Each describes a realistic
engineering situation without naming the specific tool or technique -- decide what applies and why,
then check your reasoning against the worked solution. Every scenario below is invented for this drill
and does not reuse any function, fixture, or domain from the 80 worked examples.

**AP1.** A function `parse_manifest()` throws a `ValueError` on line 340 of a 2,000-line config file,
but the error message alone doesn't say WHY that specific line is malformed. What's the fastest way to
see every local variable at the exact moment the exception was raised, without adding a single print
statement or rerunning under a debugger from the very start?

<details>
<summary>Worked solution</summary>

Post-mortem debugging (co-04) -- run `python -m pdb parse_manifest_script.py` (or, if already inside a
REPL/notebook after the exception happened, call `pdb.pm()`). Either drops directly into the exact
failing frame with every local still intact, no rerun-from-scratch and no manual instrumentation
needed.

</details>

**AP2.** A teammate says "I just print()'d the variable at every step until I found the bug." For a
one-off bug in a short script they control completely, is this actually a bad approach? When WOULD
it become the wrong choice?

<details>
<summary>Worked solution</summary>

For a short, one-off, fully-controlled script, print debugging is often perfectly fine (co-05) --
low ceremony, and the developer can re-run cheaply as many times as needed. It becomes the wrong
choice for a long-lived or production process (where each print requires a restart/redeploy and print
statements risk being left in), for deep, hard-to-reach state (many print calls needed just to narrow
down where to look), or for a bug that needs interactive follow-up questions ("wait, what's THIS
value?") that a fixed set of print statements can't answer without another edit-and-rerun cycle.

</details>

**AP3.** A regression appeared somewhere in the last 40 commits, and each commit takes 3 minutes to
build and test manually. What is the single change that turns a potential 2-hour investigation into
roughly 6 tests total, and what must exist first for it to work unattended?

<details>
<summary>Worked solution</summary>

`git bisect run <script>` (co-10), which needs roughly log2(40) ≈ 6 candidate commits instead of a
linear 40, running fully unattended overnight if needed. It requires a SCRIPT (not a manual step) whose
exit code reliably encodes pass/fail (0 = good, nonzero-not-125 = bad) for the specific regression --
without that oracle script, only the manual `git bisect start/good/bad` (co-09) loop is available,
which still gets the log2(n) search-space reduction but needs a human to test and answer at every step.

</details>

**AP4.** A crash report from a user includes a 15,000-line CSV they were importing. The team needs to
attach a minimal reproducer to the bug ticket, not the whole file. What technique produces the
smallest input that still triggers the IDENTICAL crash, and what must be held constant while shrinking
it?

<details>
<summary>Worked solution</summary>

Delta-debugging / `ddmin` (co-11) -- an automated, chunk-removal search that repeatedly tries removing
pieces of the input and keeps only the removal if the failure STILL reproduces with the identical
signature. The thing held constant throughout is the failure's SIGNATURE (exception type + message, or
whatever oracle defines "same bug") -- a candidate reduction is only accepted if it still triggers that
exact same failure, not merely "some" failure.

</details>

**AP5.** A function is profiled with `cProfile`, and a wrapper function `run_pipeline()` shows the
largest number in the "cumulative time" column. A developer spends a day optimizing `run_pipeline()`
itself and sees no improvement. What did they misread?

<details>
<summary>Worked solution</summary>

They optimized based on `cumtime` (which includes every function `run_pipeline()` calls, recursively)
instead of `tottime` (co-16, the function's own self time, excluding callees). A wrapper or dispatcher
naturally has a huge `cumtime` simply because it contains everything beneath it -- the correct fix
target is whichever function has the largest `tottime` in the SAME table, which is very likely one of
`run_pipeline()`'s callees, not `run_pipeline()` itself.

</details>

**AP6.** A batch job processes 50 records per test run and looks fast in every profile. In production
it processes 2 million records nightly and is measurably the slowest job in the pipeline. What's the
mismatch, and what should the NEXT profiling run change?

<details>
<summary>Worked solution</summary>

Load-representative-vs-toy profiling (co-21) -- an algorithm's actual cost profile can change
qualitatively with scale (an O(n) cost is invisible at n=50 but dominant at n=2,000,000, and an O(n^2)
cost is even more dramatically hidden at small n). The next profiling run should use an input size (and
ideally concurrency level) that actually resembles the 2-million-record production workload, not the
50-record convenience sample used so far.

</details>

**AP7.** A service occasionally returns stale cached data to exactly ONE concurrent request out of
every few hundred, and the bug never reproduces when the developer steps through it alone in a
debugger. What class of bug is this, and what's the general fix strategy before attempting a code
change?

<details>
<summary>Worked solution</summary>

A race condition / heisenbug (co-20) -- stepping through alone in a debugger changes the timing enough
that the natural interleaving that triggers the bug never occurs. The general strategy is to FORCE the
suspected interleaving reliably first (an explicit yield point, a barrier synchronizing multiple
threads/coroutines to a critical instant, or pinning whatever randomness decides the outcome) so the
bug reproduces on every attempt, THEN debug and fix it against that now-reliable reproduction --
attempting a fix against an unreliable, rare reproduction risks "fixing" something that was never the
actual cause.

</details>

**AP8.** `tracemalloc` shows a service's memory grew by 40MB after processing 10,000 requests, and grew
by another 41MB after a second batch of 10,000 identical-shaped requests. Is this a leak? What's the
next diagnostic step if the growth pattern were instead 40MB then 2MB?

<details>
<summary>Worked solution</summary>

Yes -- proportional, repeated growth across equivalent bursts (co-17) is the signature of a genuine
leak (something is accumulating without bound, roughly 1:1 with request count). If the pattern were
instead 40MB then only 2MB, that would indicate the FIRST burst's growth was mostly one-time
stabilization (a cache warming up, a connection pool filling), not a leak -- the near-zero net growth
on the second, equivalent burst is what a genuinely bounded/healthy allocator looks like.

</details>

**AP9.** A `cProfile` run shows a hashing function's entire cost as one flat line:
`{built-in method _hashlib.openssl_sha256}`, with no further breakdown even though the team suspects
one specific OpenSSL code path is unusually slow on their hardware. What's the fundamental reason
`cProfile` can't help further here, and what category of tool could?

<details>
<summary>Worked solution</summary>

`cProfile` (and any instrumenting Python profiler) can only see events the CPython interpreter itself
generates -- Python function call/return boundaries. Once execution crosses into a C extension's own
compiled machine code, there is no further Python-level call/return event to intercept, so the whole
C call collapses to one flat, opaque line (co-22). Seeing costs INSIDE that C code requires a
native-aware tool -- `perf record` (Linux), `py-spy record --native`, or a native debugger (`gdb`/
`lldb`) attached at the process level, all of which instrument below the Python interpreter itself.

</details>

**AP10.** A team applies a caching fix and reports "startup got faster" based on one manual timing
before and one after, both run on a laptop with several other apps open. A skeptical reviewer asks for
better evidence before merging. What's the concrete fix to the measurement, not the code?

<details>
<summary>Worked solution</summary>

Before-after measurement discipline (co-23) -- replace the single-run-each comparison with a
repeated, median-of-N measurement on BOTH the before and after versions (e.g. `subprocess`-launch each
version 9 times, take the median of each), which is resistant to any one outlier run caused by
background load, a cold cache, or OS scheduling noise. The reviewer's real ask is for a number that
would hold up if re-measured, not a single anecdote.

</details>

**AP11.** A developer needs to debug a Python process that is ALREADY running inside a remote container
with no shell access beyond the app's own logs, and cannot restart it without losing the exact state
that triggers the bug. What debugging model applies here, distinct from launching a fresh process
under a debugger?

<details>
<summary>Worked solution</summary>

Remote/DAP debugging (co-06) -- if a debug adapter (`debugpy`) can be attached to the already-running
process (e.g. via a signal-triggered attach or a pre-configured listen socket), an editor's DAP client
can connect over the network, set breakpoints, and read live state without ever restarting the process
or needing a local shell inside the container. This is fundamentally different from `python -m pdb
script.py`, which only works for a process LAUNCHED under the debugger from the start.

</details>

**AP12.** A hot function's `cProfile` numbers look identical before and after a supposed fix, but a
`py-spy`-style sampling profile of the SAME workload shows the widest frame moved from one function to
another. Which measurement should the team trust, and what's the most likely explanation for the
disagreement?

<details>
<summary>Worked solution</summary>

Neither should be trusted alone without investigating the disagreement (co-12) -- an instrumenting
profiler's numbers can be distorted by its own overhead (especially for a function with MANY cheap
calls, where per-call interception cost adds up), while a sampling profiler's numbers are statistical
and can under-sample a fast-running function if the sampling interval is too coarse relative to the
function's own runtime. The most likely explanation is that one of the two measurements is being
skewed by its own methodology's blind spot; the reliable next step is to re-run BOTH profilers with
a load-representative workload (co-21) and cross-check whether they now agree, rather than trusting
whichever one matches the expected answer.

</details>

## Code katas

Seven self-contained exercises. Every kata uses in-memory data and stdlib-only dependencies (plus, for
Kata 6, whatever `pdb`/`cProfile`/`tracemalloc` the standard library already provides) -- no live
process attach, no `gdb`/`lldb`/`perf`, no root access required -- so every kata is runnable anywhere
this topic's pinned toolchain (Python 3.13.12) is installed, with nothing else to set up.

### Kata 1 -- Post-mortem a self-inflicted KeyError

Write a function `total_for(order: dict) -> float` that indexes `order["tax_rate"]` directly (no
`.get()`). Call it once with an order dict that has no `"tax_rate"` key, letting it crash. Debug the
crash with `python -m pdb your_script.py` (co-04), confirm you can print the full `order` dict from
the failing frame, then fix the function to default the missing rate to `0.0` and confirm no crash.

### Kata 2 -- Bisect a 10-commit toy repo by hand, then automate it

Build a 10-commit git repo (in a throwaway directory) where a one-line function's behavior changes at
commit 6. Run `git bisect start`/`good`/`bad` manually (co-09) to find commit 6, noting how many
commits you actually had to check. Then write a one-line pass/fail check script and re-run the SAME
search with `git bisect run` (co-10), confirming it lands on the identical commit unattended.

### Kata 3 -- Shrink a 200-character failing string by hand-rolled ddmin

Write a function that raises on any string containing the substring `"XX"`. Build a 200-character
string containing exactly one occurrence of `"XX"`, buried in the middle among random characters.
Implement (or reuse) a simple `ddmin`-style chunk-removal loop (co-11) that shrinks the string down to
the minimal reproducer while re-checking the SAME exception signature at every candidate.

### Kata 4 -- Cross-check cProfile against a hand-rolled sampler

Write a function with one obvious O(n^2) hot spot and one cheap O(n) function alongside it. Profile it
with `cProfile`, sorted by `tottime` (co-13). Separately, write a minimal sampling profiler using
`sys._current_frames()` from a background thread sampling every 1ms (co-12/co-14's underlying idea,
without needing `py-spy` itself) -- confirm both independently name the SAME function as the hot spot.

### Kata 5 -- Diff three tracemalloc snapshots against a real leak and a real non-leak

Write two versions of a cache: one that never evicts (a plain, ever-growing dict) and one that evicts
past a fixed size (an `OrderedDict`-based LRU). Take three `tracemalloc` snapshots (before, after burst
1, after burst 2) against EACH version (co-17) and confirm the leaking version shows proportional
growth on burst 2 while the bounded version shows near-zero net growth on burst 2.

### Kata 6 -- Force a reproducible race, then fix it

Write a function that increments a shared counter across 8 threads with no lock, inserting an explicit
`time.sleep(0)` between the read and the write to widen the race window (co-20). Run it 20 times and
confirm real, measurable lost updates on most or all runs. Add a `threading.Lock()` around the
critical section and confirm the SAME 20-run loop now produces the exact expected count every time.

### Kata 7 -- Read a real flame graph and name the widest frame without counting pixels

Take any `.svg` flame graph you've already generated in this topic's learning track (or generate a
fresh one from a two-hot-spot workload of your own design). Without opening a text editor on the
underlying data, visually identify the widest frame at any depth (co-19) -- then confirm your visual
answer against the underlying `.collapsed`/`.prof` data's own numbers.

## Self-check checklist

Confirm each item without checking the learning track first. If you hesitate, that concept needs
another pass.

- [ ] I can name the three ways a paused debugger resumes one unit at a time and what distinguishes
      each. (co-01)
- [ ] I can explain what a conditional breakpoint avoids compared to an unconditional one. (co-02)
- [ ] I can explain how to move a paused debugger's context to a caller's frame and read its locals.
      (co-03)
- [ ] I can name the two ways to enter a post-mortem debugging session after an uncaught exception.
      (co-04)
- [ ] I can state when print/logging beats an interactive breakpoint, and when it does not. (co-05)
- [ ] I can explain what remote/DAP debugging lets a developer do that launching a fresh process under
      a debugger cannot. (co-06)
- [ ] I can state the scientific-method debugging loop's core rule about how many things to change per
      iteration, and why. (co-07)
- [ ] I can explain why bisection search is logarithmic rather than linear in the size of the search
      space. (co-08)
- [ ] I can name the three `git bisect` subcommands used to drive a manual search by hand. (co-09)
- [ ] I can state which exit codes `git bisect run` treats as good, bad, and skip. (co-10)
- [ ] I can state the property every remaining piece of a delta-debugged, 1-minimal input must have.
      (co-11)
- [ ] I can contrast a sampling profiler's overhead/accuracy tradeoff against an instrumenting
      profiler's. (co-12)
- [ ] I can name the stdlib module that turns a raw `cProfile` run into a sorted, readable table, and
      the minimal call sequence to print the top N rows. (co-13)
- [ ] I can state `py-spy`'s single biggest advantage over `cProfile` for an already-running process.
      (co-14)
- [ ] I can explain what a large gap between wall-clock time and CPU time most likely indicates, and
      name the two stdlib calls that measure each. (co-15)
- [ ] I can explain why a wrapper function's huge cumtime with a tiny tottime means it is NOT the
      right optimization target. (co-16)
- [ ] I can explain why a third `tracemalloc` snapshot, not just two, is needed to confirm a genuine
      leak. (co-17)
- [ ] I can name the tool and required decorator for attributing profiling cost to individual source
      lines, one resolution finer than function-level. (co-18)
- [ ] I can state what width and height each represent in a flame graph, and which one identifies the
      hot spot. (co-19)
- [ ] I can name the general strategy for making a rare concurrency bug reproduce reliably, plus two
      concrete mechanisms. (co-20)
- [ ] I can explain why profiling at toy scale can give a qualitatively wrong answer about where the
      real hot spot is. (co-21)
- [ ] I can name at least two classes of native-aware tool that can see costs hidden from cProfile
      inside a C extension. (co-22)
- [ ] I can state what's wrong with a single before-run/single after-run performance comparison, and
      what should replace it. (co-23)

---

← Previous: [Capstone](../learning/capstone/overview.md)
