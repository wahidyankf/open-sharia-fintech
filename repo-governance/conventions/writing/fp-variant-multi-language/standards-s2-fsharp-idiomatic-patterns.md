---
title: "FP-Variant Multi-Language Convention — Standards S2: F# Idiomatic Patterns"
description: The F# language patterns (discriminated unions, records, smart constructors, Result, async, units of measure, pipelines, pattern matching) required in the F# tab.
when_to_use: Use when writing or reviewing the F# tab of an FP-variant example, to confirm it uses native F# idioms rather than Clojure-influenced equivalents.
category: explanation
subcategory: conventions
tags:
  - fp
  - clojure
  - fsharp
  - by-example
  - ayokoding-www
  - tutorial
created: 2026-05-17
---

# Standards S2: F# Idiomatic Patterns

F# code in these tutorials MUST remain idiomatic to the F# community and runtime. The following patterns are expected to appear at the appropriate complexity level and MUST NOT be replaced by Clojure-influenced equivalents:

- **Discriminated unions (DUs)** — model domain variants as `type Result<'T, 'E> = Ok of 'T | Error of 'E`, sum types for state machines, and tagged union domain concepts.
- **Record types** — immutable named-field types with `{ FieldName: Type }` syntax and `with` update syntax.
- **Smart constructors** — private constructors plus a public `create` function returning `Result` to enforce invariants at the boundary.
- **`Result<'T, 'E>` and computation expressions** — `result { ... }` or `asyncResult { ... }` computation expressions for railway-oriented programming; `Result.bind`, `Result.map` combinators.
- **`Async<'T>` and async computation expressions** — `async { ... }` blocks for asynchronous workflows; `Async.RunSynchronously`, `Async.StartAsTask`.
- **Units of measure** — `[<Measure>]` type attributes and `float<kg>`, `decimal<USD>` annotations where numeric domain types have physical or monetary units.
- **`|>` pipelines and partial application** — left-to-right composition with the pipe operator; curried function application for dependency injection and workflow construction.
- **Module-level functions** — top-level `let` bindings rather than method-on-class patterns; modules as namespaces.
- **Pattern matching** — `match` expressions for case analysis, `function` keyword for single-argument match, active patterns for reusable decomposition.
- **Interfaces and object expressions** — when required by platform APIs, expressed as `{ new IInterface with member _.Method() = ... }` rather than class definitions.

F# code that introduces class hierarchies, mutable state, or imperative loops solely to mirror a Clojure pattern is non-compliant with this standard.
