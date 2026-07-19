# 65 · CSP-Style Concurrency (By Example, Go †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · Go † · Learn 165 / Drill 265 ·
Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: the CSP (communicating-sequential-processes) concurrency model in Go — goroutines,
channels, `select`, `sync`, `context`/cancellation, pipelines, worker pools, and the race detector. Sets
up the deliberate contrast with the actor model in
[`67-actor-model-concurrency`](./67-actor-model-concurrency.md). Deepens the concepts from
[`24-concurrency-and-parallelism`](./24-concurrency-and-parallelism.md).

## Why this exists · the big idea

- **The problem before the solution**: shared mutable state across threads breeds races and deadlocks that
  are nearly impossible to reproduce or reason about — CSP answers with a discipline where goroutines never
  share memory; they hand values across channels.
- **Keep-this-if-you-forget-everything**: "don't communicate by sharing memory; share memory by
  communicating" — make the channel the synchronization point and whole classes of races disappear.
- **Big ideas touched**: `taming-state` — channels contain state by transferring ownership across a
  boundary instead of sharing it; `determinism-vs-emergence` — pipelines and worker pools compose into
  predictable dataflow, yet scheduling and cancellation add emergent timing you must design for (hence the
  race detector).

## Prerequisites

- **Prior topics**: [topic 64 Just Enough Go](./64-just-enough-go.md) (the language + a channel preview) and
  [topic 24 Concurrency & Parallelism](./24-concurrency-and-parallelism.md) (races, deadlocks, the shared-
  state hazards CSP avoids).
- **Tools & environment**: a macOS/Linux terminal; the **Go toolchain** with the **race detector**
  (`go test -race`); Neovim/VSCode with Go LSP (DD-17).
- **Assumed knowledge**: Go syntax + goroutines/channels at a preview level (topic 64); what a race
  condition and a deadlock are (topic 24).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: channels, `select`, `sync` (Mutex/WaitGroup/Once), `context` cancellation,
  `go test -race`, and fan-in/fan-out + worker-pool patterns are long-stable Go concurrency primitives —
  nothing in Go 1.26 changes this surface. No corrections.

### DD-35 primary-source citations (fetched-and-read)

> Every claim below traces to an official go.dev / pkg.go.dev page the pre-authoring `web-researcher` sweep
> fetched and read. `[Needs Verification]` marks items corroborated only by secondary consensus at fetch
> time (single-page-spec truncation), never contradicted.

- **`go` statement** — the Go Language Specification (go.dev/ref/spec): "A go statement starts the execution
  of a function call as an independent concurrent thread of control, or goroutine, within the same address
  space ... program execution does not wait for the invoked function to complete." Effective Go adds
  goroutines are "lightweight, costing little more than the allocation of stack space" and "multiplexed onto
  multiple OS threads." `[Verified]`
- **`GOMAXPROCS`** — pkg.go.dev/runtime#GOMAXPROCS: "sets the maximum number of CPUs that can be executing
  simultaneously." **Version-drift**: Go 1.25 made the default container-aware (honours the cgroup CPU
  bandwidth limit on Linux and periodically re-reads it); teaching "defaults to `runtime.NumCPU()`" flat is
  now incomplete for containerised processes. `[Verified]`
- **Channels** — spec: unbuffered ("communication succeeds only when both a sender and receiver are ready"),
  buffered ("succeeds without blocking if the buffer is not full/empty"), directional `chan<-`/`<-chan`,
  "value of an uninitialized channel is `nil`", "a `nil` channel is never ready for communication", FIFO,
  `x, ok := <-c` on close. **Panics** (spec): "Sending on a closed channel causes a run-time panic. Closing
  the nil channel also causes a run-time panic." The "closing an already-closed channel panics" sub-case is
  correct and universally corroborated but its exact spec sentence was not retrievable this pass:
  `[Needs Verification]` on wording only. `[Verified]` otherwise.
- **`select`** — spec: "If multiple cases can proceed, a uniform pseudo-random choice is made"; a `default`
  case "executes if no other case is ready". `[Verified]`
- **`time.After` in `select`** — pkg.go.dev/time#After: `func After(d Duration) <-chan Time`. **Version
  note (favourable)**: "As of Go 1.23, the garbage collector can recover unreferenced, unstopped timers.
  There is no reason to prefer NewTimer when After will do." The old "`time.After` in a loop leaks" warning
  is now scoped to pre-1.23. `[Verified]`
- **`sync`** — pkg.go.dev/sync: `WaitGroup` (Add/Done/Wait; "If the counter goes negative, Add panics";
  "A WaitGroup must not be copied after first use"); **`WaitGroup.Go(f func())` added in Go 1.25** —
  "creating and counting goroutines more convenient" (the modern idiom taught alongside classic Add/Done);
  `Mutex` ("zero value ... is an unlocked mutex"; "run-time error if m is not locked on entry to Unlock");
  `RWMutex` ("held by an arbitrary number of readers or a single writer"); `Once.Do` ("if and only if Do
  is being called for the first time"); `sync.Map` ("safe for concurrent use ... without additional
  locking"). `[Verified]`
- **`context`** — pkg.go.dev/context: the four-method `Context` interface; `Err()` "returns
  DeadlineExceeded if the context's deadline passed, or Canceled if ... canceled for some other reason";
  `Background`/`TODO`/`WithCancel`/`WithDeadline`/`WithTimeout`/`WithValue`; `WithTimeout` = "WithDeadline
  (parent, time.Now().Add(timeout))"; sentinels `context.Canceled` / `context.DeadlineExceeded`. The doc's
  own `select { case <-ctx.Done(): return ctx.Err() ... }` example links to go.dev/blog/pipelines.
  `[Verified]`
- **Go Memory Model** — go.dev/ref/mem: "A send on a channel is synchronized before the completion of the
  corresponding receive"; "A receive from an unbuffered channel is synchronized before the completion of
  the corresponding send"; "The closing of a channel is synchronized before a receive that returns a zero
  value because the channel is closed"; the k / k+C buffered rule. `[Verified]`
- **"Share memory by communicating"** — go.dev/blog/codelab-share + Effective Go, verbatim: **"Do not
  communicate by sharing memory; instead, share memory by communicating."** Effective Go: Go's concurrency
  "originates in Hoare's Communicating Sequential Processes (CSP)". `[Verified]`
- **Pipelines & fan-in/fan-out** — go.dev/blog/pipelines: "a pipeline is a series of stages connected by
  channels, where each stage is a group of goroutines running the same function"; fan-out = "Multiple
  functions can read from the same channel until that channel is closed"; fan-in = multiplexing several
  inputs onto one channel closed when all inputs are; "stages close their outbound channels when all the
  send operations are done"; goroutine-leak remedy = buffering or a `done`-channel `select`. `[Verified]`
- **Race detector** — go.dev/doc/articles/race_detector: "A data race occurs when two goroutines access the
  same variable concurrently and at least one of the accesses is a write"; enabled via `go test -race`
  (also run/build/install); cost "memory usage may increase by 5-10x and execution time by 2-20x"; "only
  finds races that happen at runtime". go.dev/blog/race-detector: "The race detector will not issue false
  positives." `[Verified]`
- **Deadlock** — the runtime message `fatal error: all goroutines are asleep - deadlock!` is a stable
  `runtime` string, universally corroborated but not documented in go.dev prose (source-level literal):
  `[Needs Verification]` on a fetched primary source; safe to quote (accurate + version-stable).
- **CSP vs actor contrast** — framed against Elixir/BEAM in
  [`67-actor-model-concurrency`](./67-actor-model-concurrency.md): CSP = synchronous rendezvous over
  channels (the channel is the sync point, processes are anonymous); actor = shared-nothing processes with
  async mailboxes addressed by identity. The conceptual distinction is standard; any sharper claim is
  flagged `[Needs Verification]`.

## Concepts

<!-- co-NN · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · csp-model** — communicating sequential processes: goroutines never share memory, they hand
  values across channels; "don't communicate by sharing memory; share memory by communicating."
- **co-02 · goroutines** — the `go` keyword starts a function as an independent concurrent goroutine in
  the same address space; lightweight (little more than stack allocation), multiplexed onto OS threads.
- **co-03 · scheduler-gomaxprocs** — the runtime multiplexes goroutines onto `GOMAXPROCS` OS threads; the
  default is CPU-count (and, since Go 1.25, container/cgroup-aware) — concurrency ≠ parallelism.
- **co-04 · unbuffered-channels** — a zero-capacity channel is a synchronous rendezvous: the send blocks
  until a receiver is ready, making the channel itself the synchronisation point.
- **co-05 · buffered-channels** — a capacity-N channel lets N sends proceed without a waiting receiver;
  sends block only when full, receives only when empty (a natural bounded queue / semaphore).
- **co-06 · channel-directions** — `chan<- T` (send-only) and `<-chan T` (receive-only) types encode a
  goroutine's role in the type system, so misuse is a compile error.
- **co-07 · channel-close** — `close(c)` signals no-more-values; `for v := range c` drains until close,
  `v, ok := <-c` detects it; sending on / closing a closed (or nil) channel panics.
- **co-08 · nil-channel** — a nil channel is never ready; assigning a case's channel to nil disables that
  `select` case, a real idiom for dynamically turning arms off.
- **co-09 · select** — `select` waits on multiple channel operations and, if several are ready, makes a
  uniform pseudo-random choice; a `default` case makes the whole select non-blocking.
- **co-10 · select-timeout** — a `time.After` (or `ctx.Done()`) case inside `select` bounds how long a
  receive waits — the canonical timeout pattern.
- **co-11 · mutex** — `sync.Mutex` gives mutual exclusion over shared state for the cases where a channel
  is the wrong tool; the zero value is unlocked and it must not be copied after use.
- **co-12 · rwmutex** — `sync.RWMutex` lets many readers OR one writer hold the lock, cheaper than a full
  mutex on read-heavy shared state.
- **co-13 · waitgroup** — `sync.WaitGroup` (Add/Done/Wait) waits for a set of goroutines to finish;
  `wg.Go` (Go 1.25) packages the launch+count; the value must not be copied after first use.
- **co-14 · once** — `sync.Once` runs an initialiser exactly once across all goroutines, the concurrency-
  safe lazy-init primitive.
- **co-15 · atomic-and-syncmap** — `sync/atomic` and `sync.Map` provide lock-free/lock-internal concurrent
  access for counters and concurrent maps without a hand-rolled mutex.
- **co-16 · context-cancellation** — `context.Context` propagates cancellation + deadlines across call
  boundaries; `WithCancel`/`WithTimeout`/`WithDeadline`, `ctx.Done()`, and `ctx.Err()` (Canceled /
  DeadlineExceeded) are the standard shutdown signal.
- **co-17 · pipeline** — a pipeline is a series of stages connected by channels, each stage a group of
  goroutines running the same function; stages close their outbound channel when their sends are done.
- **co-18 · fan-out** — multiple goroutines reading the same inbound channel distribute work to parallelise
  CPU/IO — the read side of a worker set.
- **co-19 · fan-in** — multiplexing several inbound channels onto one outbound channel (closed when all
  inputs are) merges parallel results back into a single stream.
- **co-20 · worker-pool** — a bounded set of worker goroutines draining a jobs channel and writing a
  results channel caps parallelism and back-pressures the producer.
- **co-21 · done-channel-cancellation** — a shared `done` channel (closed via `defer close(done)`) checked
  in every stage's `select` unblocks upstream senders so no goroutine leaks on early exit.
- **co-22 · memory-model** — the Go memory model's happens-before rules: a channel send is synchronised
  before the corresponding receive, and a close before a zero-value receive — the guarantee that makes
  channel hand-off safe without extra locks.
- **co-23 · race-detector** — `go test -race` instruments memory accesses to catch data races (concurrent
  access with ≥1 write); it has no false positives, costs 5–10× memory / 2–20× time, and only sees
  executed paths.
- **co-24 · goroutine-leak** — goroutines are not garbage-collected; one blocked forever on a send/receive
  leaks resources — every goroutine must have a guaranteed exit (via close, cancellation, or draining).
- **co-25 · deadlock** — a cycle where every goroutine waits on another (`fatal error: all goroutines are
asleep - deadlock!`); unbuffered self-sends and circular channel waits are the classic causes.
- **co-26 · csp-vs-actor** — CSP (Go channels: anonymous processes, synchronous rendezvous, the channel is
  the address) contrasts with the actor model (BEAM processes: identity-addressed, async mailboxes) —
  set up for [`67-actor-model-concurrency`](./67-actor-model-concurrency.md).

## Worked examples

Colocated under `csp-style-concurrency/learning/code/`; each runnable + race-checked (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · goroutine-basic** — launch one goroutine with `go` and wait for it — verify it ran. (co-02)
- **ex-02 · goroutine-waitgroup** — launch N goroutines coordinated by a `WaitGroup` — verify all ran
  before `Wait` returned. (co-02, co-13)
- **ex-03 · share-by-communicating** — pass ownership of a value across a channel instead of a shared var
  — verify only the receiver mutates it (race-clean). (co-01)
- **ex-04 · unbuffered-rendezvous** — send/receive on an unbuffered channel — verify the send unblocks
  only when the receive happens. (co-04)
- **ex-05 · unbuffered-blocks** — a send with no receiver under a timeout — verify it blocks. (co-04)
- **ex-06 · buffered-capacity** — a `make(chan int, 3)` — verify three sends proceed without a receiver. (co-05)
- **ex-07 · buffered-nonblock** — send into buffer space — verify no block until full. (co-05)
- **ex-08 · buffered-full-blocks** — a fourth send into a size-3 buffer — verify it blocks. (co-05)
- **ex-09 · send-only-channel** — pass a `chan<- int` to a producer — verify a receive on it fails to
  compile. (co-06)
- **ex-10 · receive-only-channel** — pass a `<-chan int` to a consumer — verify a send on it fails to
  compile. (co-06)
- **ex-11 · close-channel** — `close(c)` then receive — verify a post-close receive returns the zero
  value. (co-07)
- **ex-12 · range-over-channel** — `for v := range c` — verify the loop ends when the channel closes. (co-07)
- **ex-13 · comma-ok-closed** — `v, ok := <-c` on a closed channel — verify ok is false. (co-07)
- **ex-14 · send-on-closed-panics** — send on a closed channel under `recover` — verify it panics. (co-07)
- **ex-15 · close-closed-panics** — close an already-closed channel under `recover` — verify it panics. (co-07)
- **ex-16 · nil-channel-blocks** — receive on a nil channel under a timeout — verify it never becomes
  ready. (co-08)
- **ex-17 · nil-disables-select-case** — set a case's channel to nil in a loop — verify that case is
  skipped. (co-08)
- **ex-18 · select-two-ready** — a `select` over two ready receives — verify exactly one case runs. (co-09)
- **ex-19 · select-pseudo-random** — a `select` over many ready cases run in a loop — verify the choice
  is roughly uniform. (co-09)
- **ex-20 · select-default-nonblock** — a `select` with `default` on an empty channel — verify default
  runs immediately. (co-09)
- **ex-21 · select-timeout-after** — a `select` with a `time.After` case — verify the timeout fires when
  no value arrives. (co-10)
- **ex-22 · mutex-guard-counter** — increment a shared counter under `sync.Mutex` — verify no lost
  updates under `-race`. (co-11)
- **ex-23 · mutex-no-copy** — demonstrate why a `Mutex` must not be copied — verify `go vet` flags a copy. (co-11)
- **ex-24 · rwmutex-readers** — many concurrent readers + one writer under `RWMutex` — verify readers run
  concurrently and the writer is exclusive. (co-12)
- **ex-25 · waitgroup-add-done-wait** — classic `Add`/`Done`/`Wait` — verify `Wait` blocks until the
  counter hits zero. (co-13)
- **ex-26 · waitgroup-go** — the Go 1.25 `wg.Go(f)` idiom — verify it launches+counts equivalently to the
  classic pattern. (co-13)

### Intermediate

- **ex-27 · once-init** — `sync.Once` around an initialiser called from many goroutines — verify it runs
  exactly once. (co-14)
- **ex-28 · sync-map** — concurrent `Store`/`Load` on `sync.Map` — verify race-clean under `-race`. (co-15)
- **ex-29 · atomic-counter** — `atomic.AddInt64` from many goroutines — verify the final total is exact. (co-15)
- **ex-30 · context-withcancel** — `context.WithCancel`; cancel and observe `ctx.Done()` — verify the
  goroutine returns. (co-16)
- **ex-31 · context-cancel-propagation** — a parent cancel cascading to child contexts — verify all
  children see Done. (co-16)
- **ex-32 · context-withtimeout** — `WithTimeout`; let it elapse — verify `ctx.Err()` is
  `DeadlineExceeded`. (co-16)
- **ex-33 · context-withdeadline** — `WithDeadline` at a fixed time — verify it fires at the deadline. (co-16)
- **ex-34 · context-err-canceled** — cancel explicitly — verify `ctx.Err()` is `context.Canceled`. (co-16)
- **ex-35 · context-done-in-select** — `select { case <-ctx.Done(): ... case v := <-in: ... }` — verify
  cancellation wins over a slow input. (co-16)
- **ex-36 · pipeline-two-stage** — generator → squarer over channels — verify the output sequence. (co-17)
- **ex-37 · pipeline-three-stage** — add a filter stage — verify each stage closes its outbound channel. (co-17)
- **ex-38 · pipeline-generator** — a reusable `gen(nums...)` source stage — verify it emits then closes. (co-17)
- **ex-39 · fan-out-workers** — N goroutines reading one inbound channel — verify work is distributed
  across them. (co-18)
- **ex-40 · fan-out-parallel-speedup** — fan-out a CPU task — verify it uses multiple workers (counts per
  worker > 0). (co-18)
- **ex-41 · fan-in-merge** — merge several worker outputs into one channel — verify all values arrive. (co-19)
- **ex-42 · fan-in-waitgroup-close** — close the merged channel when all inputs finish (WaitGroup) — verify
  the consumer's range ends. (co-19)
- **ex-43 · worker-pool-bounded** — a fixed pool draining a jobs channel — verify at most N run at once. (co-20)
- **ex-44 · worker-pool-results** — collect results on a results channel — verify every job produced one
  result. (co-20)
- **ex-45 · worker-pool-jobs-channel** — producer closes the jobs channel to signal done — verify workers
  exit on close. (co-20)
- **ex-46 · done-channel-cancel** — a shared `done` channel closed to stop a pipeline — verify all stages
  return. (co-21)
- **ex-47 · done-channel-defer-close** — `defer close(done)` on early return — verify upstream senders
  unblock. (co-21)
- **ex-48 · pipeline-cancel-early** — consumer stops reading mid-stream — verify no stage blocks forever. (co-21)
- **ex-49 · select-send-or-done** — `select { case out <- v: case <-done: return }` in each stage — verify
  a stage exits on cancel. (co-21)
- **ex-50 · context-vs-done** — reimplement the done-channel pipeline with `context` — verify equivalent
  cancellation. (co-16, co-21)
- **ex-51 · timeout-per-job** — a per-job `context.WithTimeout` inside a worker — verify a slow job is
  abandoned. (co-10, co-16)
- **ex-52 · graceful-shutdown** — signal a worker pool to drain then stop — verify in-flight jobs finish
  and no new ones start. (co-20, co-16)
- **ex-53 · rate-limit-ticker** — a `time.Ticker` gating a `select` loop — verify the emit rate is
  bounded. (co-09)
- **ex-54 · semaphore-buffered-channel** — a buffered channel as a counting semaphore — verify concurrency
  is capped at the buffer size. (co-05, co-20)

### Advanced

- **ex-55 · happens-before-channel** — a value written before a send, read after the receive — verify the
  read sees the write (memory-model guarantee). (co-22)
- **ex-56 · memory-visibility-unsync** — the same read WITHOUT the channel sync — verify `-race` flags it. (co-22)
- **ex-57 · race-on-shared-var** — two goroutines writing one variable — verify `go test -race` reports a
  data race. (co-23)
- **ex-58 · race-detector-output** — read the `-race` report — verify it names the conflicting accesses. (co-23)
- **ex-59 · race-fixed-mutex** — fix ex-57 with a mutex — verify `-race` is clean. (co-23, co-11)
- **ex-60 · race-fixed-channel** — fix ex-57 by moving the state onto a channel — verify `-race` is clean. (co-23, co-01)
- **ex-61 · race-cost-note** — measure `-race` overhead on a benchmark — verify it runs slower (documents
  the 2–20× cost). (co-23)
- **ex-62 · goroutine-leak-blocked-send** — a goroutine blocked on a send nobody receives — verify it
  leaks (goroutine count stays up). (co-24)
- **ex-63 · goroutine-leak-fix-done** — fix the leak with a `done`/`ctx` guard — verify the goroutine
  count returns to baseline. (co-24, co-21)
- **ex-64 · goroutine-leak-detect** — count goroutines before/after with `runtime.NumGoroutine` — verify
  the leak is observable. (co-24)
- **ex-65 · deadlock-all-asleep** — an unbuffered send with no receiver in `main` — verify `fatal error:
all goroutines are asleep - deadlock!`. (co-25)
- **ex-66 · deadlock-unbuffered-selfsend** — a goroutine sending to itself on an unbuffered channel —
  verify the deadlock. (co-25)
- **ex-67 · deadlock-fix** — fix the deadlock with a buffer or a second goroutine — verify it completes. (co-25)
- **ex-68 · deadlock-circular-wait** — two goroutines each waiting on the other's channel — verify the
  circular deadlock. (co-25)
- **ex-69 · pipeline-error-propagation** — carry an error alongside the value through a pipeline — verify
  the first error stops the run. (co-17)
- **ex-70 · bounded-parallelism** — cap concurrent work with a semaphore/pool over a large job set — verify
  the in-flight count never exceeds the bound. (co-20)
- **ex-71 · context-value-request-scoped** — thread a request id through `context.WithValue` — verify a
  worker reads it (and note values are request-scoped, not params). (co-16)
- **ex-72 · select-fairness** — a hot and a cold channel in a `select` loop — verify neither starves over
  many iterations. (co-09)
- **ex-73 · mutex-vs-channel-choice** — solve one problem both with a mutex and with a channel — verify
  both are correct and note when each fits. (co-11, co-01)
- **ex-74 · csp-vs-actor-contrast** — a table/diagram contrasting Go channels with the actor model — verify
  it names synchronous-rendezvous vs async-mailbox. (co-26)
- **ex-75 · csp-synchronous-handoff** — demonstrate the unbuffered synchronous hand-off that an actor
  mailbox does NOT provide — verify the sender waits for the receiver. (co-26)
- **ex-76 · mini-worker-pool** — a small end-to-end pool (producer → fan-out workers → fan-in collector) —
  verify counts reconcile. (co-20, co-18, co-19)
- **ex-77 · clean-shutdown-race-clean** — the mini pool with `context` cancellation, run under `-race` —
  verify clean shutdown and zero races. (co-23, co-16)
- **ex-78 · concurrency-not-parallelism** — show the same concurrent design at `GOMAXPROCS=1` and `>1` —
  verify correctness is independent of parallelism. (co-01, co-03)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build a concurrent work processor in Go — a bounded worker pool draining a channel pipeline
  (fan-out / fan-in), coordinated with `select` + `context` cancellation and `sync` primitives, that
  shuts down cleanly and passes `go test -race` with no data races — a demonstrably correct CSP design.
- **Concepts exercised**: [ ] goroutines + channels (co-02, co-04, co-07) [ ] a fan-out/fan-in pipeline
  (co-17, co-18, co-19) [ ] a bounded worker pool (co-20) [ ] `select` + `context` cancellation (co-09,
  co-16, co-21) [ ] `sync` coordination (co-11, co-13) [ ] a race-clean `go test -race` (co-23, co-24).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a channel pipeline (producer → workers → collector). Verify all items
     flow through and the counts reconcile.
  2. Bound it with a worker pool + `select` + `context` cancellation. Verify a cancel signal stops all
     workers promptly with no goroutine leak.
  3. `go test -race`. Verify the suite passes with **no** race-detector warnings.
- **Acceptance criteria**: the pipeline processes every item; cancellation shuts workers down cleanly with
  no leak; `go test -race` reports zero data races.
- **Done bar**: runnable end-to-end + race-clean + web-verified.

## Read more

**Books**

- **The Go Programming Language** — Alan A. A. Donovan & Brian W. Kernighan (2015). The definitive Go reference book, with a canonical treatment of goroutines, channels, and `select`.
- **Communicating Sequential Processes** — C. A. R. Hoare (1985). Hoare's own book-length formalization of CSP, freely distributed by the author's estate/collaborators. <http://www.usingcsp.com/cspbook.pdf>

**Papers & articles**

- **Communicating Sequential Processes** — C. A. R. Hoare, _Communications of the ACM_ 21(8) (1978). The original paper that introduced CSP, the formal model underlying Go's concurrency primitives. <https://www.cs.cmu.edu/~crary/819-f09/Hoare78.pdf>
- **Share Memory By Communicating** — Andrew Gerrand, The Go Blog (2010). The Go team's canonical articulation of "don't communicate by sharing memory; share memory by communicating." <https://go.dev/blog/codelab-share>
- **Concurrency Is Not Parallelism** — Rob Pike (2012). Foundational talk by a Go co-creator distinguishing concurrent design from parallel execution. <https://go.dev/talks/2012/waza.slide>
- **Effective Go** — The Go Authors (official documentation). Canonical guidance on idiomatic goroutine and channel usage. <https://go.dev/doc/effective_go>

---

← Previous: [64 · Just Enough Go](./64-just-enough-go.md) · Next: [66 · Just Enough Elixir](./66-just-enough-elixir.md) →
