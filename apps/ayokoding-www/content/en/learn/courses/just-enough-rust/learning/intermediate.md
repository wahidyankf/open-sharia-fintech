---
title: "Intermediate Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 20
---

Examples 27–52 make Rust’s distinctive ownership model practical, then connect fallible functions
to traits, generic contracts, iterators, and closures. Each code file is independently runnable:
from `learning/code/`, use `cargo run --bin ex-NN`.

### Example 27: Ownership Move

_ex-27 · co-08, co-09_ — Assignment transfers a `String` to one new owner. Read the annotation in
`src/bin/ex-27.rs`, run it, and notice that the original name is intentionally not reused.

**Key takeaway**: non-`Copy` values move unless you borrow or clone them.

**Why it matters**: Ownership gives resource cleanup one accountable owner without a garbage
collector or a manually maintained free path.

### Example 28: Move on a Function Call

_ex-28 · co-09_ — Passing an owned `String` transfers it into the callee.

**Key takeaway**: a by-value parameter advertises ownership transfer.

**Why it matters**: Function signatures explain who may keep, mutate, or release a resource.

### Example 29: Clone Deliberately

_ex-29 · co-08_ — `clone` makes the second owned value explicit.

**Key takeaway**: duplicate owned data only when two owners are actually needed.

**Why it matters**: Explicit duplication keeps allocation and copying visible in performance-sensitive code.

### Example 30: Shared Borrow

_ex-30 · co-10_ — `&str` reads a `String` without moving it.

**Key takeaway**: shared borrows preserve the owner’s usability.

**Why it matters**: Read-only APIs can be efficient and clear without transferring ownership.

### Example 31: Mutable Borrow

_ex-31 · co-11_ — `&mut String` gives one function exclusive mutation access.

**Key takeaway**: mutation through a reference requires exclusivity.

**Why it matters**: The compiler prevents two writers from silently changing the same value.

### Example 32: Borrow Rules

_ex-32 · co-12_ — many shared borrows are valid; a conflicting mutable borrow is not.

**Key takeaway**: one mutable borrow xor many shared borrows.

**Why it matters**: This rule rules out whole classes of aliasing bugs before execution.

### Example 33: Borrow in a Function

_ex-33 · co-10_ — a predicate borrows only the path text it inspects.

**Key takeaway**: borrow the narrowest view needed by the operation.

**Why it matters**: Narrow contracts make composition possible without unnecessary moves or clones.

### Example 34: Reject a Dangling Reference

_ex-34 · co-13_ — returning owned `String` replaces an invalid reference to local data.

**Key takeaway**: references may never outlive their referent.

**Why it matters**: Lifetime checking prevents use-after-free without asking the programmer to track it manually.

### Example 35: Annotate a Lifetime

_ex-35 · co-13_ — `longest` states which input lifetime constrains its returned slice.

**Key takeaway**: lifetime annotations describe relationships; they do not extend data lifetime.

**Why it matters**: Rare explicit lifetimes make borrowed API boundaries honest.

### Example 36: Return Result

_ex-36 · co-19_ — parsing succeeds with `Ok` or returns a named `Err`.

**Key takeaway**: fallibility belongs in the return type.

**Why it matters**: Callers must confront recoverable failure instead of discovering a hidden null or panic.

### Example 37: Propagate with Question Mark

_ex-37 · co-19, co-20_ — `?` returns parse failure early.

**Key takeaway**: `?` keeps the success path readable while preserving errors.

**Why it matters**: Small fallible steps compose into honest higher-level operations.

### Example 38: Parse Result

_ex-38 · co-19_ — `str::parse` is fallible because arbitrary text is not a port number.

**Key takeaway**: parsing is an explicit validation boundary.

**Why it matters**: Systems programs receive strings from users, files, and networks, none guaranteed valid.

### Example 39: Map an Option

_ex-39 · co-18_ — `map` changes a present value while preserving absence.

**Key takeaway**: transform optional data without unwrapping it prematurely.

**Why it matters**: This keeps missing-data policy local and easy to review.

### Example 40: Supply an Option Default

_ex-40 · co-18_ — `unwrap_or` chooses a documented fallback.

**Key takeaway**: defaults should be deliberate at the consuming boundary.

**Why it matters**: A visible fallback makes operational behavior predictable when configuration is incomplete.

### Example 41: Match a Result

_ex-41 · co-16, co-19_ — a `match` makes success and failure handling explicit.

**Key takeaway**: pattern matching is ordinary error control flow.

**Why it matters**: Match arms can give each failure a different useful response.

### Example 42: Define a Trait

_ex-42 · co-21_ — `Describe` names behavior independent of one concrete struct.

**Key takeaway**: traits express capabilities, not inheritance trees.

**Why it matters**: Capability-based design keeps systems components composable.

### Example 43: Implement a Trait

_ex-43 · co-21_ — `Api` supplies the `Healthy` behavior.

**Key takeaway**: implementations connect types to contracts.

**Why it matters**: A caller can depend on behavior while the implementation stays replaceable.

### Example 44: Use a Trait Default Method

_ex-44 · co-21_ — a default method reuses behavior built from a required method.

**Key takeaway**: traits can provide small shared derivations.

**Why it matters**: Shared defaults reduce repeated code without forcing a class hierarchy.

### Example 45: Write a Generic Function

_ex-45 · co-23_ — `twice` works for distinct concrete `T` values.

**Key takeaway**: generics describe one algorithm over many types.

**Why it matters**: Rust specializes generic code while preserving a focused source contract.

### Example 46: Use a Generic Struct

_ex-46 · co-23_ — `Config<T>` carries a chosen field type.

**Key takeaway**: generic data models preserve type information rather than erasing it.

**Why it matters**: Typed configuration makes invalid mixes of values harder to express.

### Example 47: Constrain a Generic

_ex-47 · co-22, co-23_ — `Display` is the capability needed to format `T`.

**Key takeaway**: trait bounds state exactly what generic code can do.

**Why it matters**: Minimal bounds keep APIs flexible and compiler errors actionable.

### Example 48: Map an Iterator

_ex-48 · co-25_ — `map` lazily transforms each item before collection.

**Key takeaway**: iterator adapters express data flow as a pipeline.

**Why it matters**: Small transformations combine without manual index bookkeeping.

### Example 49: Filter an Iterator

_ex-49 · co-25_ — `filter` retains only ports meeting the predicate.

**Key takeaway**: predicates make selection rules local.

**Why it matters**: Clear selection code is easier to test and adjust than interleaved control flow.

### Example 50: Collect an Iterator

_ex-50 · co-24, co-25_ — the target `Vec<String>` determines the materialized collection.

**Key takeaway**: collection is the deliberate allocation boundary.

**Why it matters**: Knowing where laziness ends helps reason about ownership and allocation.

### Example 51: Capture in a Closure

_ex-51 · co-26_ — a closure reads the local prefix it captures.

**Key takeaway**: closures package behavior with required context.

**Why it matters**: Local transformations stay near the values that define them.

### Example 52: Pass a Closure

_ex-52 · co-26_ — `apply` accepts behavior through `Fn`.

**Key takeaway**: closures are typed values that can be passed safely.

**Why it matters**: Callback-style APIs can state the precise call behavior they accept.
