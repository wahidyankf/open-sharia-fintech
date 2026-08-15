---
title: "Advanced Examples"
date: 2026-08-15T00:00:00+07:00
draft: false
weight: 30
---

Examples 53–78 compose the Primer surface into small, inspectable programs. They remain language
examples—not concurrency, `unsafe`, FFI, or platform programming—because that applied depth belongs
to Modern System Programming. Run each from `learning/code/` with `cargo run --bin ex-NN`.

### Example 53: Use a HashMap

_ex-53 · co-24_ — Insert a service port, then handle lookup as `Option`.

**Key takeaway**: map lookup can legitimately be absent.

**Why it matters**: Keyed configuration and registries must state what happens for missing keys.

### Example 54: Use the Entry API

_ex-54 · co-24_ — `entry(...).or_insert(...)` combines lookup and initialization.

**Key takeaway**: the entry API makes insert-or-update one explicit operation.

**Why it matters**: One access path avoids accidental duplicated lookup logic.

### Example 55: Chain Iterators

_ex-55 · co-25_ — Filter, map, and collect one port pipeline.

**Key takeaway**: iterator chains compose one transformation per step.

**Why it matters**: Data pipelines stay readable without temporary mutable collections.

### Example 56: Fold an Iterator

_ex-56 · co-25_ — Fold ports into one numeric accumulator.

**Key takeaway**: a fold defines both its initial state and combination rule.

**Why it matters**: Explicit accumulation prevents hidden mutable state.

### Example 57: Add Methods to an Enum

_ex-57 · co-14, co-15_ — An enum method uses exhaustive `match` internally.

**Key takeaway**: behavior can live beside a sum type.

**Why it matters**: The compiler reminds the method author when a new state needs handling.

### Example 58: Put Option in a Struct

_ex-58 · co-14, co-18_ — A configuration field explicitly may be absent.

**Key takeaway**: optionality belongs in the data model.

**Why it matters**: A consumer cannot mistake a possibly missing field for a guaranteed value.

### Example 59: Return a Custom Error

_ex-59 · co-15, co-19_ — A small error enum names missing and invalid configuration separately.

**Key takeaway**: error variants document recoverable categories.

**Why it matters**: Callers can later assign a different response to each failure class.

### Example 60: Chain Question Mark

_ex-60 · co-20_ — Two parse steps propagate the first `Err` with `?`.

**Key takeaway**: `?` composes a fallible path without obscuring the happy path.

**Why it matters**: Systems code commonly validates several independent inputs in sequence.

### Example 61: Use a Trait Object

_ex-61 · co-21_ — `&dyn Render` performs dynamic dispatch through a trait.

**Key takeaway**: trait objects trade static specialization for a uniform runtime interface.

**Why it matters**: This is a small contrast with generic dispatch, not a recommendation to erase types by default.

### Example 62: Use Multiple Trait Bounds

_ex-62 · co-22_ — A generic needs both `Clone` and `Display`.

**Key takeaway**: each bound corresponds to a real operation in the body.

**Why it matters**: Honest bounds make generic APIs easier to call and maintain.

### Example 63: Derive Debug

_ex-63 · co-14_ — `#[derive(Debug)]` enables diagnostic output.

**Key takeaway**: derives add routine trait implementations declaratively.

**Why it matters**: Debuggable values make early experiments and test failures easier to inspect.

### Example 64: Derive Clone and Equality

_ex-64 · co-14_ — Derived `Clone` and `PartialEq` support a small value comparison.

**Key takeaway**: derive common behavior when it matches the data model.

**Why it matters**: Explicit derives show which operations a type promises to support.

### Example 65: Compare Self Borrow Modes

_ex-65 · co-10, co-11_ — One method reads `&self`; another changes `&mut self`.

**Key takeaway**: a method’s receiver communicates its access requirement.

**Why it matters**: Receiver choice makes state change visible at every method call.

### Example 66: Store Structs in a Vec

_ex-66 · co-14, co-24_ — Iterate borrowed service structs.

**Key takeaway**: collections own values while loops can borrow each one.

**Why it matters**: This is the everyday foundation for inspecting structured program state.

### Example 67: Match Option and Result

_ex-67 · co-16, co-18, co-19_ — Distinguish missing input from invalid input.

**Key takeaway**: nested fallibility can preserve meaningful outcomes.

**Why it matters**: Operational diagnostics are clearer when absence and invalid data are not collapsed.

### Example 68: Return Ownership

_ex-68 · co-08_ — Returning `String` transfers ownership to the caller.

**Key takeaway**: return types say who owns produced data next.

**Why it matters**: Ownership transfer turns lifetime responsibility into an API-level decision.

### Example 69: Borrow Then Return Owned Data

_ex-69 · co-10_ — Borrow input, compute a new owned label, and return it.

**Key takeaway**: an owned result need not carry a borrow relationship.

**Why it matters**: This pattern keeps APIs simple when callers need a result beyond input lifetime.

### Example 70: Combine Generic and Result

_ex-70 · co-19, co-23_ — A generic required-value helper returns `Result<String, String>`.

**Key takeaway**: generic code can be fallible without losing type constraints.

**Why it matters**: Reusable validation helpers should retain both useful input types and failure signals.

### Example 71: Write a Cargo Unit Test

_ex-71 · co-04_ — Run `cargo test --bin ex-71` to execute `#[test]`.

**Key takeaway**: tests live beside the behavior they verify.

**Why it matters**: A focused unit test guards the smallest reusable rule against regression.

### Example 72: Assert Equality

_ex-72 · co-04_ — `assert_eq!` compares expected and actual behavior.

**Key takeaway**: a precise assertion makes a failure informative.

**Why it matters**: Tests become executable documentation when their expectation is specific.

### Example 73: Declare a Cargo Dependency

_ex-73 · co-05_ — The source explains `cargo add <crate>` and keeping resolved intent in `Cargo.toml`.

**Key takeaway**: Cargo manifests make dependencies visible and reproducible.

**Why it matters**: This Primer uses only the standard library; add crates later only for a stated need.

### Example 74: Repair a Borrow-Checker Conflict

_ex-74 · co-12_ — Finish a shared read before asking for mutable access.

**Key takeaway**: shorten the borrow’s useful scope instead of working around the rule.

**Why it matters**: Clear access phases are easier for both the compiler and a human to reason about.

### Example 75: Compare Move and Borrow Calls

_ex-75 · co-09, co-10_ — One function borrows; another consumes the same value.

**Key takeaway**: call syntax follows the ownership contract in the signature.

**Why it matters**: Choosing borrow versus move deliberately avoids surprise clones and invalid names.

### Example 76: Combine the Primer Slice

_ex-76 · co-14, co-15, co-16, co-19, co-21, co-23_ — One short program joins structs, enums,
trait-bound generic code, `Result`, and exhaustive matching.

**Key takeaway**: the language pieces fit through explicit contracts.

**Why it matters**: This is the immediate bridge to the light capstone, not a replacement for systems practice.

### Example 77: Test a Fallible Function

_ex-77 · co-04, co-19_ — Run `cargo test --bin ex-77` to cover success and error paths.

**Key takeaway**: tests should cover the error contract as well as success.

**Why it matters**: Fallible APIs are only reliable when consumers can count on both outcomes.

### Example 78: Capstone Preview

_ex-78 · co-04, co-14–co-16, co-18–co-23_ — This final runnable binary previews the capstone’s
struct, enum, exhaustive match, trait-bound generic, `Option`, and `Result` surface.

**Key takeaway**: each feature has a small, purposeful role in one program.

**Why it matters**: Run the dedicated capstone next to prove the same surface with `cargo run` and `cargo test`.
