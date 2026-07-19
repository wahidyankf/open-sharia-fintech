# 83 · Modern System Programming (By Example, Rust †)

**prd row**: Pass 4 · Concurrency & Systems · By Example · Rust † · Learn 183 / Drill 283 · Nvim-ready Yes · VSCode-ready Yes. ([prd canonical table](../prd.md#the-94-topics--canonical-table-spiral-order-identical-in-both-tracks))

**Scope note**: systems programming without the footguns — ownership as a compile-time memory-safety
strategy, fearless concurrency, zero-cost abstractions, and FFI across the C boundary. This is the modern
counterpart to the C systems topic ([`81-system-programming`](./81-system-programming.md)): the same
low-level control, but with the classes of bug that dominate C — use-after-free, data races, buffer
overruns — moved from runtime crashes to compile errors. The usable language slice is the prerequisite
[`82-just-enough-rust`](./82-just-enough-rust.md). `†`: Rust, driving `cargo` and building native binaries.

## Why this exists · the big idea

- **The problem before the solution**: systems languages gave you full control over memory and hardware and
  charged for it in the worst currency — use-after-free, double-free, buffer overflows, and data races that
  compile cleanly, ship, and then corrupt memory or open security holes in production. Decades of C/C++ CVEs
  are overwhelmingly this one category.
- **Keep-this-if-you-forget-everything**: Rust's borrow checker enforces, at compile time, that memory has
  exactly one owner and that shared access is either many-readers or one-writer but never both — so the
  bugs that plague manual memory management become programs that simply do not compile. Safety is a property
  the compiler proves, not a discipline you hope you maintained.
- **Big ideas touched**: `taming-state` (ownership and borrowing are a static discipline for mutable shared
  state — aliasing and mutation cannot coexist, which is exactly what makes data races unrepresentable),
  `mechanism-vs-policy` (zero-cost abstractions and the `unsafe` boundary separate the safe machinery you
  build on from the small, audited places where you take manual control of the mechanism).

## Prerequisites

- **Prior topics**: [topic 82 Just Enough Rust](./82-just-enough-rust.md) (ownership/borrowing intuition,
  the type system, `Result`/`Option`, traits, pattern matching) and [topic 80 Windows OS](./80-windows-os.md)
  (the OS-level view of memory, threads, and system calls that systems code sits on).
- **Tools & environment**: a macOS/Linux/Windows terminal; the **Rust toolchain** (`cargo`, `rustc`) pinned
  to a current stable; a C compiler/toolchain available for the FFI examples; Neovim/VSCode with the Rust
  LSP (rust-analyzer, DD-17).
- **Assumed knowledge**: ownership/borrowing and lifetimes at intuition level, traits, and `Result`/`Option`
  (topic 82); processes/threads and system calls (topics 79/80); the memory hierarchy and stack-vs-heap
  (topic 20).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: the core model is stable and correctly left version-unpinned — ownership,
  borrowing, lifetimes, `Send`/`Sync` and the "fearless concurrency" guarantees, zero-cost abstractions, and
  `unsafe`/FFI across the C ABI are settled Rust semantics, not fast-moving surface. Keep the toolchain at
  "a current stable" in shipped text.
- 2026-07-12 — verified (GAP for plan owner): async runtimes and specific crates (an async executor, an FFI
  helper crate) are referenced by role, not pinned — re-verify exact crate names/versions once the worked
  examples are drafted, and keep the standard-library-first framing (threads/channels before an async
  runtime).

### DD-35 primary-source citations (fetched-and-read)

> Anti-hallucination (DD-35): every crate/version/edition fact below traces to a primary source a
> `web-researcher` fetched and read on 2026-07-12. Unverifiable claims are marked `[Needs Verification]`.

- **Core model unpinned** — ownership/borrowing/lifetimes, `Send`/`Sync`, threads/channels/`Arc`/`Mutex`,
  zero-cost iterators/traits/generics, `Result`/`?`, `unsafe`, and FFI across the C ABI are settled Rust
  semantics; shipped prose keeps "a current stable" toolchain, not a pinned number. Verified against The
  Rust Programming Language book (doc.rust-lang.org/book) + the Rustonomicon.
- **`unsafe` chapter moved** — in the current book, `unsafe` is **chapter 20** (formerly ch19), and there is
  **no standalone FFI chapter** — FFI is folded into the unsafe material and the Rustonomicon. Cite ch20 /
  nomicon, never a "chapter 19" or a dedicated FFI chapter.
- **2024-edition FFI spelling** — exposing a Rust symbol to C uses `#[unsafe(no_mangle)]` (the 2024-edition
  attribute spelling), paired with `extern "C"`.
- **`env::set_var` is now `unsafe`** — `std::env::set_var`/`remove_var` became `unsafe` as of **Rust 1.85** —
  a real example of the safety surface expanding over time.
- **Crate versions (verified live, re-pin at authoring)** — the worked examples reference, by role:
  **tokio 1.52.3** (async runtime), **libc 0.2.186** (raw C bindings for FFI), **thiserror 2.0.18** (derive
  for library error enums), **anyhow 1.0.103** (application-level errors). Standard-library-first framing
  holds: threads/channels before an async runtime. Re-verify versions at authoring time.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (By-Example subject). Each example below cites the co-NN it exercises. -->

- **co-01 · ownership-memory** — ownership is a compile-time memory-safety strategy: each value has one owner freed when it drops.
- **co-02 · move-semantics** — assigning or passing a non-`Copy` value moves it, invalidating the source.
- **co-03 · borrow-shared** — `&T` is a shared, read-only borrow that does not move the value.
- **co-04 · borrow-mut** — `&mut T` is an exclusive borrow permitting mutation.
- **co-05 · borrow-rules** — aliasing and mutation cannot coexist; the borrow checker rejects `&mut` alongside any other borrow.
- **co-06 · lifetimes** — lifetimes make "a reference may not outlive its referent" explicit; elision covers common cases.
- **co-07 · drop** — RAII: a value's `Drop` runs deterministically at scope end, releasing its resources.
- **co-08 · box** — `Box<T>` moves a value to the heap and enables recursive types.
- **co-09 · rc-refcell** — `Rc<T>` shares ownership single-threaded; `RefCell` adds runtime-checked interior mutability.
- **co-10 · threads** — `std::thread::spawn`/`join` (and scoped threads) run work on OS threads.
- **co-11 · channels** — `mpsc` channels pass ownership of messages between threads.
- **co-12 · arc** — `Arc<T>` is the atomically-reference-counted shared owner for cross-thread sharing.
- **co-13 · mutex** — `Mutex<T>` (and atomics) guard shared mutable state against concurrent access.
- **co-14 · send-sync** — the `Send`/`Sync` marker traits decide what may cross or be shared between threads.
- **co-15 · data-race-compile-error** — because aliasing-plus-mutation is unrepresentable, data races are compile errors, not runtime lotteries.
- **co-16 · zero-cost-iterators** — iterator adapters, traits, and generics monomorphize to the same code you'd write by hand.
- **co-17 · traits-generics** — trait-bounded generics give static dispatch via monomorphization (zero-cost).
- **co-18 · trait-objects** — `dyn Trait` trades a vtable indirection for runtime polymorphism.
- **co-19 · result-error** — systems-level errors are values (`Result`), not exceptions, with explicit failure paths.
- **co-20 · question-mark** — `?` propagates an `Err` early, auto-converting via `From`.
- **co-21 · custom-errors** — library error types are enums, often derived with `thiserror`.
- **co-22 · anyhow** — `anyhow` gives ergonomic, context-carrying application-level errors.
- **co-23 · unsafe-block** — `unsafe {}` permits a small set of extra operations the compiler cannot check.
- **co-24 · raw-pointers** — `*const T`/`*mut T` are unchecked raw pointers, dereferenceable only in `unsafe`.
- **co-25 · unsafe-contract** — every `unsafe` block is a manual proof obligation; keep it small and behind a safe API.
- **co-26 · ffi-extern** — `extern "C"` declares the C ABI for calling across the language boundary.
- **co-27 · ffi-call-c** — calling a C function from Rust goes through an `unsafe extern "C"` declaration.
- **co-28 · ffi-expose-rust** — exposing a Rust function to C uses `#[unsafe(no_mangle)] extern "C"`.
- **co-29 · ffi-ownership** — ownership must be tracked by hand across the FFI boundary (who allocates, who frees).
- **co-30 · async-runtime** — `async`/`await` needs a runtime (e.g. tokio) to drive futures to completion.

## Tensions & trade-offs — when NOT to reach for this

- **The borrow checker is a learning tax**: patterns that are trivial in a GC'd or manually-managed
  language (self-referential structures, shared mutable graphs, some callback designs) fight the borrow
  checker and require rethinking. For a team without the time to climb that curve, a memory-safe GC language
  may ship the same feature faster.
- **`unsafe` is not a safety escape valve to reach for casually**: dropping into `unsafe` to silence the
  compiler reintroduces exactly the bugs Rust exists to prevent — now in code the compiler no longer checks.
  Every `unsafe` block is a manual proof obligation; if you find yourself writing many, the design is
  usually wrong.
- **When the ecosystem or hard-real-time constraints say otherwise**: an existing C/C++ codebase, a platform
  with only a C toolchain, or a hard-real-time context where you cannot tolerate any allocation may make Rust
  the wrong or premature choice. Rust wins the safety argument, not every argument.

## Lineage — why it beat the alternative

- Systems programming lived on C and C++ for decades: unmatched control and performance, paid for with a
  standing epidemic of memory-safety bugs that industry data repeatedly ties to the majority of critical
  CVEs. The alternatives each gave something up — garbage-collected languages removed the bug class but added
  a runtime and unpredictable pauses unacceptable for kernels, drivers, and hot paths. Rust's bet was that
  an ownership type system could prove memory and thread safety at compile time with no runtime cost,
  keeping C-level control while deleting the bug class — a bet now validated by its adoption in operating
  systems, browsers, and infrastructure. The safe-systems instincts, concurrency model, and FFI boundary
  built here are the toolkit you carry into any low-level work, and they contrast directly with the
  manual-discipline model of [`81-system-programming`](./81-system-programming.md).

## Worked examples

Colocated under `modern-system-programming/learning/code/`; each runnable via `cargo` (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · move-basic** — a move on assignment — verify the source is invalidated. (co-02)
- **ex-02 · move-compile-error** — a use-after-move is a compile error — verify the diagnostic. (co-02)
- **ex-03 · borrow-shared** — a `&T` read — verify no move. (co-03)
- **ex-04 · borrow-mut** — a `&mut T` mutation — verify the change. (co-04)
- **ex-05 · borrow-conflict** — a `&mut` alongside a `&` is rejected — verify the error. (co-05)
- **ex-06 · two-mut-borrows** — two `&mut` at once are rejected — verify the error. (co-05)
- **ex-07 · borrow-checker-fix** — a rejected program and its fix — verify it compiles after. (co-05)
- **ex-08 · lifetime-elision** — lifetime elision in a function — verify it compiles. (co-06)
- **ex-09 · lifetime-explicit** — an explicit lifetime annotation — verify it compiles. (co-06)
- **ex-10 · dangling-rejected** — a would-be dangling reference is rejected — verify the error. (co-06)
- **ex-11 · drop-order** — `Drop` runs at scope end — verify the drop fires. (co-07)
- **ex-12 · box-heap** — `Box<T>` heap allocation — verify the deref. (co-08)
- **ex-13 · box-recursive** — a recursive type via `Box` — verify it compiles. (co-08)
- **ex-14 · clone-vs-move** — `clone` to keep both — verify both are usable. (co-02)
- **ex-15 · ownership-in-fn** — pass ownership into a function — verify the transfer. (co-01)
- **ex-16 · borrow-in-fn** — pass a reference — verify no move. (co-03)
- **ex-17 · return-owned** — return an owned value — verify the transfer. (co-01)
- **ex-18 · slice-borrow** — a slice borrow of a `Vec` — verify the view. (co-03)
- **ex-19 · string-vs-str** — `String` vs `&str` — verify the borrow. (co-03)
- **ex-20 · vec-ownership** — a `Vec` owning its elements — verify drop-all. (co-01, co-07)
- **ex-21 · iterator-map-loop** — iterator `map` — verify it matches a hand-written loop. (co-16)
- **ex-22 · iterator-filter** — iterator `filter` — verify the selection. (co-16)
- **ex-23 · iterator-sum** — iterator `sum`/`fold` — verify the accumulation. (co-16)
- **ex-24 · result-basic** — a function returning `Result` — verify `Ok`/`Err`. (co-19)
- **ex-25 · question-mark** — `?` propagation — verify the short-circuit. (co-20, co-19)
- **ex-26 · result-match** — `match` on a `Result` — verify the arms. (co-19)

### Intermediate

- **ex-27 · thread-spawn** — spawn a thread and `join` — verify it runs. (co-10)
- **ex-28 · thread-move-closure** — move into a thread closure — verify the capture. (co-10, co-02)
- **ex-29 · channel-send-recv** — an `mpsc` channel send/recv — verify a message. (co-11)
- **ex-30 · channel-multiple** — multiple producers over a channel — verify all received. (co-11)
- **ex-31 · worker-pipeline** — worker threads over a channel pipeline — verify throughput. (co-10, co-11)
- **ex-32 · arc-shared** — `Arc<T>` shared across threads — verify a shared read. (co-12)
- **ex-33 · arc-mutex** — `Arc<Mutex<T>>` shared mutable state — verify safe mutation. (co-12, co-13)
- **ex-34 · mutex-lock** — `Mutex` lock/unlock — verify exclusion. (co-13)
- **ex-35 · data-race-rejected** — a data race rejected by the compiler — verify the error. (co-15, co-14)
- **ex-36 · send-sync-bound** — a `Send` bound on a thread — verify enforcement. (co-14)
- **ex-37 · rc-single-thread** — `Rc<T>` single-thread sharing — verify the count. (co-09)
- **ex-38 · refcell-interior** — `RefCell` interior mutability — verify the runtime borrow check. (co-09)
- **ex-39 · rc-not-send** — an `Rc` across threads is rejected — verify the error. (co-09, co-14)
- **ex-40 · trait-bound-generic** — a trait-bounded generic — verify monomorphization. (co-17)
- **ex-41 · trait-static-dispatch** — static dispatch via generics — verify the inlining. (co-17)
- **ex-42 · trait-object-dyn** — `dyn Trait` dynamic dispatch — verify polymorphism. (co-18)
- **ex-43 · iterator-chain-zero-cost** — a chained iterator pipeline — verify it's zero-cost. (co-16)
- **ex-44 · custom-error-enum** — a custom error enum — verify the variants. (co-21)
- **ex-45 · thiserror-derive** — a `thiserror` derive for an error type — verify `Display`. (co-21)
- **ex-46 · error-propagate-chain** — `?` across a call chain with a custom error — verify propagation. (co-20, co-21)
- **ex-47 · anyhow-context** — `anyhow` with `.context(...)` — verify the error message. (co-22)
- **ex-48 · result-from-conversion** — `From`/`Into` error conversion for `?` — verify the auto-convert. (co-20, co-21)
- **ex-49 · scoped-threads** — `std::thread::scope` borrowing stack data — verify a safe borrow. (co-10)
- **ex-50 · atomic-counter** — an atomic counter across threads — verify no race. (co-13)
- **ex-51 · channel-shutdown** — a channel close/drop as a shutdown signal — verify a graceful stop. (co-11)
- **ex-52 · producer-consumer** — a producer/consumer over `Arc<Mutex>` + channel — verify correctness. (co-11, co-12, co-13)

### Advanced

- **ex-53 · unsafe-block** — an `unsafe` block dereferencing a raw pointer — verify controlled access. (co-23, co-24)
- **ex-54 · raw-pointer-cast** — `&T` to `*const T` — verify the cast. (co-24)
- **ex-55 · unsafe-deref** — dereference a raw pointer in `unsafe` — verify the value. (co-23, co-24)
- **ex-56 · unsafe-wrapped-safe** — a small `unsafe` block behind a safe API — verify the safe surface. (co-25)
- **ex-57 · env-set-var-unsafe** — `env::set_var` (unsafe since 1.85) — verify the `unsafe` requirement. (co-25, co-23)
- **ex-58 · extern-c-declare** — an `extern "C"` declaration of a C function — verify it links. (co-26)
- **ex-59 · ffi-call-libc** — call a `libc` function via the `libc` crate — verify the result. (co-27, co-26)
- **ex-60 · ffi-call-c-fn** — call a hand-written C function from Rust — verify the return value. (co-27)
- **ex-61 · ffi-pass-primitive** — pass a primitive across FFI — verify the round-trip. (co-27, co-29)
- **ex-62 · ffi-pass-pointer** — pass a pointer/buffer across FFI — verify ownership handling. (co-29, co-24)
- **ex-63 · ffi-expose-rust** — expose a Rust fn to C via `#[unsafe(no_mangle)] extern "C"` — verify the symbol. (co-28)
- **ex-64 · ffi-string-boundary** — pass a C string (`CStr`/`CString`) across FFI — verify the conversion. (co-29)
- **ex-65 · ffi-ownership-free** — who frees what across the boundary — verify no double-free. (co-29)
- **ex-66 · async-await-basic** — an `async fn` awaited under tokio — verify it completes. (co-30)
- **ex-67 · tokio-runtime** — a `#[tokio::main]` runtime — verify a task runs. (co-30)
- **ex-68 · async-concurrent-tasks** — concurrent async tasks with `join!` — verify the overlap. (co-30)
- **ex-69 · async-channel** — an async channel (tokio `mpsc`) — verify a message. (co-30, co-11)
- **ex-70 · threads-vs-async** — threads vs async for the same task — verify the trade-off. (co-10, co-30)
- **ex-71 · zero-cost-verify** — inspect that an iterator compiles like a loop — verify the equivalence. (co-16)
- **ex-72 · safe-wrapper-over-unsafe** — a safe module wrapping unsafe FFI — verify the invariant holds. (co-25, co-29)
- **ex-73 · concurrent-race-free-run** — a concurrent program run repeatedly — verify no race. (co-15)
- **ex-74 · error-path-systems** — systems-level error paths with `Result` — verify clean failure. (co-19)
- **ex-75 · cargo-test-suite** — a `cargo test` suite for the tool — verify it passes. (co-19)
- **ex-76 · full-safety-slice** — ownership core + concurrency + zero-cost abstraction + FFI in one program — verify the whole. (co-01, co-12, co-16, co-27)
- **ex-77 · integration-borrow-clean** — the whole program borrow-checker-clean + race-free + FFI-correct — verify it. (co-05, co-15, co-29)
- **ex-78 · capstone-systems-tool** — a systems tool: an ownership-correct core, a race-free concurrent component (threads+channels or `Arc<Mutex>`), a zero-cost abstraction, and one FFI call whose single `unsafe` block sits behind a safe API — verify the core is borrow-checker-clean, the concurrent component is race-free, the abstraction is zero-cost, and the FFI works with ownership handled and `unsafe` confined. (co-01, co-12, co-16, co-27, co-25)

## Capstone spec — intra-topic (subject → full runnable)

- **Goal**: build one small systems tool in Rust that exercises the safety story end to end — an ownership-
  correct core, a concurrent component the compiler proves race-free, a zero-cost abstraction over its data,
  and an FFI call across the C boundary whose single `unsafe` block is contained behind a safe API.
- **Concepts exercised**: [ ] ownership/borrowing/lifetimes correct by construction (co-01, co-05, co-06)
  [ ] threads + channels or `Arc<Mutex<_>>` with `Send`/`Sync` (co-10, co-11, co-12, co-13, co-14) [ ] a
  zero-cost iterator/trait abstraction (co-16, co-17) [ ] `Result`/`?` error handling (co-19, co-20) [ ] one
  FFI call across the C ABI (co-26, co-27, co-29) [ ] a small audited `unsafe` block behind a safe wrapper
  (co-23, co-25).
- **Ordered steps**:
  1. `.../learning/capstone/code/core/` — the ownership-correct core logic with `Result`-based error paths.
     Verify `cargo build` compiles with no borrow-checker warnings and `cargo test` passes.
  2. `.../learning/capstone/code/concurrent/` — add a concurrent component (threads + channels or shared
     state behind `Arc<Mutex<_>>`). Verify it compiles (the type system proving `Send`/`Sync`) and runs
     without a data race under repeated execution.
  3. `.../learning/capstone/code/abstract/` — express the data handling through a zero-cost
     iterator/trait abstraction. Verify behavior is unchanged and the tests still pass.
  4. `.../learning/capstone/code/ffi/` — call a C function across the boundary, handling ownership, with the
     `unsafe` block small and wrapped in a safe API. Verify the FFI call returns the expected result and the
     `unsafe` surface is minimal and documented.
- **Acceptance criteria**: the core is borrow-checker-clean; the concurrent component is provably race-free
  and runs repeatably; the abstraction is zero-cost with unchanged behavior; the FFI call works with
  ownership handled and `unsafe` confined behind a safe wrapper.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **Rust for Rustaceans** — Jon Gjengset (2021). The canonical intermediate/advanced Rust book for
  engineers moving from language basics into idiomatic systems code, traits, and unsafe boundaries.
- **Rust Atomics and Locks** — Mara Bos (2023). Authoritative treatment of low-level concurrency primitives
  in Rust, written by the former Rust library team lead; free online. <https://marabos.nl/atomics/>

**Papers & articles**

- **Writing an OS in Rust** — Philipp Oppermann. Widely-used, free blog series building a minimal x86-64
  kernel in Rust from bare metal up. <https://os.phil-opp.com/>
- **The Rustonomicon** — The Rust Project. Official reference for unsafe Rust internals, required reading
  for systems-level Rust work. <https://doc.rust-lang.org/nomicon/>

---

← Previous: [82 · Just Enough Rust](./82-just-enough-rust.md) · Next: [84 · Just Enough Java](./84-just-enough-java.md) →
