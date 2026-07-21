# Just Enough Rust (Primer, Rust)

**Course ID**: `just-enough-rust` · **Format**: Primer · **Language**: Rust.

**Short summary**: Rust syntax, ownership, borrowing, type system

**Scope note**: **just enough Rust** to be productive in modern systems programming
([`83-modern-system-programming`](./modern-system-programming.md)). `cargo`, an intuition for
ownership/borrowing/lifetimes, the type system, `Result`/`Option`, traits, and pattern matching. `†`:
Rust, run and built with the `cargo` toolchain.

## Why this exists · the big idea

- **The problem before the solution**: Rust's ownership model is the one genuinely new idea most engineers
  meet here, and trying to learn it while also wrestling concurrency, FFI, and `unsafe` at once is how people
  bounce off the language — so the primer isolates the language core first.
- **Keep-this-if-you-forget-everything**: in Rust every value has exactly one owner, and the borrow checker
  enforces that at compile time — fighting the borrow checker early is normal, and the moment its rules click
  is the moment Rust starts feeling productive rather than obstructive.
- **Big ideas touched**: `taming-state` (ownership and borrowing are a compile-time discipline for who may
  read and who may mutate — the language's whole approach to shared mutable state), `abstraction-and-its-cost`
  (traits and `Result`/`Option` give expressive, zero-cost abstractions — the cost is paid up front in
  explicitness the compiler demands).

## Prerequisites

- **Prior topics**: [topic 8 Object-Oriented Programming Essentials](./object-oriented-programming-essentials.md)
  (interfaces map onto traits, and composition-over-inheritance is Rust's default) and
  [topic 20 Computer Architecture](./computer-architecture.md) (stack vs heap and the memory model that
  ownership is really about).
- **Tools & environment**: a macOS/Linux/Windows terminal; the **Rust toolchain** (`cargo`, `rustc`) pinned
  to a current stable; Neovim/VSCode with the Rust LSP (rust-analyzer, DD-17).
- **Assumed knowledge**: interfaces and composition (topic 08); stack-vs-heap and the memory hierarchy
  (topic 20); running a CLI build tool (topic 05).

## Accuracy notes (web-verified)

> Verified in the pre-authoring `web-researcher` sweep (#48, DD-28).

- 2026-07-12 — verified: keep the Rust toolchain at "a current stable" in shipped text — `cargo`
  (`new`/`run`/`build`/`test`), ownership/borrowing/lifetimes, `Result`/`Option`, traits, generics, and
  pattern matching are stable, settled language surface. Rust ships on a six-week cadence, so a pinned
  version number would go stale fast; the language core here does not.
- 2026-07-12 — verified: the primer stays on the standard library and language core, so no third-party
  crate version is claimed — nothing to re-pull beyond the toolchain itself.

### DD-35 primary-source citations (fetched-and-read)

> Anti-hallucination (DD-35): every version/feature below traces to a primary source a
> `web-researcher` fetched and read on 2026-07-12. Unverifiable claims are marked `[Needs Verification]`.

- **Rust toolchain** — current stable is **Rust 1.97.0** on a six-week release cadence; shipped prose
  keeps the wording "a current stable" (not a pinned number) because a pinned version goes stale fast.
  The **2024 edition** is the default for new `cargo new` projects. Verified against doc.rust-lang.org /
  the Rust release channel.
- **Language core** — `cargo` (`new`/`run`/`build`/`test`/add-a-dependency), ownership/borrowing
  (`&`/`&mut`, one-`&mut`-xor-many-`&`), lifetimes, `struct`/`enum`, `match`/`if let`, `Option`/`Result`
  - `?`, traits + trait bounds, generics, `Vec`/`String`/`HashMap`, iterators, and closures are stable,
    settled surface — verified against The Rust Programming Language book (doc.rust-lang.org/book).
- **No crate versions** — the primer stays on the standard library and language core, so no third-party
  crate version is claimed; nothing to re-pull beyond the toolchain.

## Concepts

<!-- co-01 · concept enumeration (DD-34): every concept this topic teaches, 1:1-mirrored to a delivery.md checkbox. Floor ≥ 10 (Primer, subject band). Each example below cites the co-NN it exercises. -->

- **co-01 · cargo-new** — `cargo new` scaffolds a project with `Cargo.toml` and `src/main.rs`.
- **co-02 · cargo-run** — `cargo run` compiles and runs the binary in one step.
- **co-03 · cargo-build** — `cargo build` compiles to `target/` without running.
- **co-04 · cargo-test** — `cargo test` runs `#[test]` functions.
- **co-05 · cargo-add-dep** — a dependency is declared in `Cargo.toml` (or via `cargo add`) and resolved by cargo.
- **co-06 · variables-mut** — bindings are immutable by default; `let mut` opts into mutation; `let` can shadow.
- **co-07 · scalar-types** — `i32`/`f64`/`bool`/`char` plus tuples and functions with typed params/returns.
- **co-08 · ownership** — every value has exactly one owner; when the owner drops, the value is freed.
- **co-09 · move-semantics** — assigning or passing a non-`Copy` value moves it, invalidating the source.
- **co-10 · borrowing-shared** — `&T` is a shared, read-only borrow that does not move the value.
- **co-11 · borrowing-mut** — `&mut T` is an exclusive borrow permitting mutation through the reference.
- **co-12 · borrow-rules** — at any time either one `&mut` or many `&`, never both — enforced by the borrow checker.
- **co-13 · lifetimes** — references may not outlive their referent; lifetimes make that constraint explicit.
- **co-14 · structs** — `struct`s aggregate named fields and carry methods via `impl`.
- **co-15 · enums** — `enum`s are sum types whose variants may carry data.
- **co-16 · pattern-match** — `match` destructures values and must be exhaustive over an enum's variants.
- **co-17 · if-let** — `if let`/`while let` match a single pattern without a full `match`.
- **co-18 · option** — `Option<T>` (`Some`/`None`) models an optional value with no null.
- **co-19 · result** — `Result<T, E>` (`Ok`/`Err`) models a fallible computation.
- **co-20 · question-mark** — `?` propagates an `Err`/`None` early, returning it from the enclosing function.
- **co-21 · traits** — a `trait` defines shared behavior; types `impl` it (Rust's interface mechanism).
- **co-22 · trait-bounds** — generics are constrained by trait bounds (`T: Trait`) so the compiler knows the contract.
- **co-23 · generics** — generic functions and structs are monomorphized per concrete type (zero-cost).
- **co-24 · collections** — `Vec<T>`, `String`, and `HashMap<K, V>` are the core owned collections.
- **co-25 · iterators** — iterator adapters (`map`/`filter`/`collect`/`fold`) compose lazy pipelines.
- **co-26 · closures** — closures capture their environment and can be passed as arguments.

## Worked examples

Colocated under `just-enough-rust/learning/code/`; each runnable via `cargo` (DD-20/DD-30).
Contiguous `ex-01..ex-78`. Every example cites the `co-NN` it exercises. Concepts come before examples.

### Beginner

- **ex-01 · cargo-new** — `cargo new` a project — verify the `Cargo.toml` + `src/main.rs` structure. (co-01)
- **ex-02 · cargo-run-hello** — `cargo run` a hello-world — verify the output. (co-02)
- **ex-03 · cargo-build** — `cargo build` — verify a binary lands in `target/`. (co-03)
- **ex-04 · let-binding** — `let` a variable — verify its value. (co-06)
- **ex-05 · mutability** — `let mut` then reassign — verify the change. (co-06)
- **ex-06 · immutable-error** — reassigning an immutable binding is a compile error — verify the error. (co-06)
- **ex-07 · scalar-int** — `i32` arithmetic — verify the result. (co-07)
- **ex-08 · scalar-float** — `f64` arithmetic — verify the result. (co-07)
- **ex-09 · bool-char** — a `bool` and a `char` — verify the values. (co-07)
- **ex-10 · function-def** — a function with typed params and return — verify the result. (co-07)
- **ex-11 · struct-def** — define a struct — verify field access. (co-14)
- **ex-12 · struct-methods** — an `impl` method on a struct — verify the call. (co-14)
- **ex-13 · enum-basic** — an enum — verify a variant. (co-15)
- **ex-14 · enum-data** — an enum variant carrying data — verify the payload. (co-15)
- **ex-15 · match-enum** — `match` exhaustively over an enum — verify each arm. (co-16)
- **ex-16 · match-guard** — a `match` guard — verify the conditional arm. (co-16)
- **ex-17 · match-binding** — bind a value in a `match` arm — verify the capture. (co-16)
- **ex-18 · if-let** — `if let` on an `Option` — verify the `Some` path. (co-17, co-18)
- **ex-19 · while-let** — `while let` popping a `Vec` — verify the loop. (co-17)
- **ex-20 · option-some-none** — `Option` `Some`/`None` — verify both. (co-18)
- **ex-21 · vec-basic** — a `Vec` push and index — verify the elements. (co-24)
- **ex-22 · string-basic** — a `String` `push_str` — verify the content. (co-24)
- **ex-23 · vec-iterate** — iterate a `Vec` with `for` — verify the traversal. (co-24)
- **ex-24 · tuple** — a tuple and destructure — verify the parts. (co-07)
- **ex-25 · array-slice** — an array and a slice — verify the slicing. (co-24)
- **ex-26 · shadowing** — variable shadowing — verify the rebinding. (co-06)

### Intermediate

- **ex-27 · ownership-move** — a move on assignment — verify the source is invalidated. (co-08, co-09)
- **ex-28 · move-on-call** — a move into a function — verify a later use is a compile error. (co-09)
- **ex-29 · clone** — `clone` to keep both — verify both are usable. (co-08)
- **ex-30 · borrow-shared** — a `&T` shared borrow — verify a read without moving. (co-10)
- **ex-31 · borrow-mut** — a `&mut T` mutation through a reference — verify the change. (co-11)
- **ex-32 · borrow-rules** — one `&mut` xor many `&` — verify the conflict is rejected. (co-12)
- **ex-33 · borrow-in-function** — pass by reference to a function — verify no move. (co-10)
- **ex-34 · dangling-ref-error** — a would-be dangling reference is a compile error — verify the rejection. (co-13)
- **ex-35 · lifetime-annotation** — a function with an explicit lifetime — verify it compiles. (co-13)
- **ex-36 · result-ok-err** — a function returning `Result` — verify `Ok` and `Err`. (co-19)
- **ex-37 · question-mark-propagate** — propagate an error with `?` — verify the short-circuit. (co-20, co-19)
- **ex-38 · parse-result** — `str::parse` returning `Result` — verify success and failure. (co-19)
- **ex-39 · option-map** — `Option::map` — verify the transform. (co-18)
- **ex-40 · option-unwrap-or** — `unwrap_or` a default — verify the fallback. (co-18)
- **ex-41 · result-match** — `match` on a `Result` — verify both arms. (co-19, co-16)
- **ex-42 · trait-define** — define a trait — verify the contract. (co-21)
- **ex-43 · trait-impl** — `impl` a trait for a type — verify dispatch. (co-21)
- **ex-44 · trait-default-method** — a trait default method — verify inherited behavior. (co-21)
- **ex-45 · generic-function** — a generic function — verify it works for two types. (co-23)
- **ex-46 · generic-struct** — a generic struct — verify it holds different types. (co-23)
- **ex-47 · trait-bound** — a generic constrained by a trait bound — verify the bound is enforced. (co-22, co-23)
- **ex-48 · iterator-map** — iterator `map` — verify the transformed collection. (co-25)
- **ex-49 · iterator-filter** — iterator `filter` — verify the selection. (co-25)
- **ex-50 · iterator-collect** — `collect` into a `Vec` — verify materialization. (co-25, co-24)
- **ex-51 · closure-basic** — a closure capturing a variable — verify the capture. (co-26)
- **ex-52 · closure-as-arg** — pass a closure to a function — verify the invocation. (co-26)

### Advanced

- **ex-53 · hashmap** — a `HashMap` insert/get — verify the lookup. (co-24)
- **ex-54 · hashmap-entry** — the `entry` API — verify insert-or-update. (co-24)
- **ex-55 · iterator-chain** — chained `map`+`filter`+`collect` — verify the pipeline. (co-25)
- **ex-56 · iterator-fold** — `fold`/reduce — verify the accumulation. (co-25)
- **ex-57 · enum-with-methods** — an enum with `impl` methods — verify the behavior. (co-15, co-14)
- **ex-58 · option-in-struct** — a struct field of `Option` — verify present/absent. (co-18, co-14)
- **ex-59 · result-custom-error** — a custom error enum returned in `Result` — verify the variants. (co-19, co-15)
- **ex-60 · question-mark-chain** — chained `?` across calls — verify propagation. (co-20)
- **ex-61 · trait-object** — a `dyn Trait` object — verify dynamic dispatch. (co-21)
- **ex-62 · generic-trait-bound-multi** — multiple trait bounds — verify the combined constraints. (co-22)
- **ex-63 · derive-debug** — `#[derive(Debug)]` + `{:?}` print — verify the formatting. (co-14)
- **ex-64 · derive-clone-eq** — derive `Clone` + `PartialEq` — verify equality. (co-14)
- **ex-65 · struct-borrow-method** — a method taking `&self` vs `&mut self` — verify the distinction. (co-10, co-11)
- **ex-66 · vec-of-structs** — a `Vec` of structs iterated — verify the traversal. (co-24, co-14)
- **ex-67 · match-option-result** — `match` nesting `Option`/`Result` — verify each case. (co-16, co-18, co-19)
- **ex-68 · ownership-return** — return ownership from a function — verify the transfer. (co-08)
- **ex-69 · borrow-then-return** — borrow, compute, return owned — verify the borrow doesn't escape. (co-10)
- **ex-70 · generic-with-result** — a generic function returning `Result` — verify success/failure. (co-23, co-19)
- **ex-71 · cargo-test-unit** — a `#[test]` unit test — verify `cargo test` passes. (co-04)
- **ex-72 · cargo-test-assert** — `assert_eq!` in a test — verify the assertion. (co-04)
- **ex-73 · cargo-add-dependency** — add a dependency in `Cargo.toml` and use it — verify it builds. (co-05)
- **ex-74 · borrow-checker-fix** — a borrow-checker error then its fix — verify it compiles after. (co-12)
- **ex-75 · move-vs-borrow** — moving vs borrowing at a call site — verify the difference. (co-09, co-10)
- **ex-76 · full-primer-slice** — structs+enums+trait+generic+`Result`/`Option`+`match` in one program — verify the whole. (co-14, co-21, co-23, co-19)
- **ex-77 · integration-cargo-test** — the whole program with a passing `cargo test`, borrow-checker-clean — verify it. (co-04)
- **ex-78 · capstone-rust-primer** — a Rust program: structs/enums, a trait impl, a generic constrained by the trait, `Result`/`Option` with `?`, exhaustive `match`, `cargo run` + `cargo test` — verify structs/enums+match work, the trait+generic dispatch, `Result`/`Option`+`?` handle success/failure, borrow-checker-clean, and `cargo test` passes. (co-14, co-21, co-23, co-19, co-04)

## Capstone spec — intra-topic (primer → light consolidation)

- **Goal**: build a small Rust program that exercises the primer's surface — structs/enums, a trait, a
  generic, `Result`/`Option` with `?`, and exhaustive pattern matching — runnable via `cargo run` plus a
  `cargo test`, with the borrow checker satisfied, proving readiness for modern systems programming.
- **Concepts exercised**: [ ] structs + enums (co-14, co-15) [ ] a trait implemented for a type (co-21) [ ] a
  generic function or struct (co-23) [ ] `Result`/`Option` + `?` (co-19, co-18, co-20) [ ] exhaustive `match`
  (co-16) [ ] a `cargo test` (co-04).
- **Ordered steps**:
  1. `.../learning/capstone/code/` — a program modeling data with structs and enums and a `match` over the
     enum. Verify `cargo run` produces the expected output with an exhaustive match.
  2. Add a trait and implement it for a type, and a fallible function returning `Result` propagated with
     `?`. Verify the trait dispatches and the error path returns an `Err` cleanly.
  3. Add a generic constrained by the trait and a `cargo test`. Verify borrow-checker-clean compilation and
     that the test passes.
- **Acceptance criteria**: structs/enums and exhaustive matching work; the trait and generic compile and
  dispatch; `Result`/`Option` + `?` handle success and failure; the code is borrow-checker-clean and
  `cargo test` passes.
- **Done bar**: runnable end-to-end + web-verified.

## Read more

**Books**

- **The Rust Programming Language**, 2nd ed. — Steve Klabnik, Carol Nichols, with the Rust community. The
  official book and canonical entry point to Rust, including ownership and borrowing; maintained by the Rust
  project itself. <https://doc.rust-lang.org/book/>
- **Programming Rust**, 2nd ed. — Jim Blandy, Jason Orendorff, Leonora F. S. Tindall (2021). The deep,
  systems-oriented O'Reilly treatment of Rust's ownership and type system.

**Papers & articles**

- **Rust By Example** — The Rust Project. Official companion of runnable examples reinforcing
  ownership/borrowing and core syntax. <https://doc.rust-lang.org/rust-by-example/>

## In which paths

- `interview-ready/software-engineer` — Go deeper · Theory & low-level systems — optional deepening tail, not in the required spine.
- `immediately-effective/software-engineer` — Deepening band · Concurrency & language breadth — deepening band, deferred out of the early spine.
- `fundamentally-strong/software-engineer` — Stage 3 · Concurrency & language breadth.

> _Content originated in the now-closed FS-SE plan (topic 82); it now lives here in
> full — this course block is self-contained._

---

← Back to the [course library catalog](./README.md)
