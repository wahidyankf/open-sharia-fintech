---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

This is a code-first on-ramp to Kotlin for a reader about to work on Android. Each example is a
complete program in its Markdown block. Save a standard-library block as `Example.kt`, then run
`kotlinc Example.kt -include-runtime -d example.jar && java -jar example.jar`. The coroutine blocks
link to a shared Gradle runner because coroutine builders are a library, not part of Kotlin's
standard library.

Kotlin's current releases change more quickly than a course should. The examples deliberately do
not pin a compiler version: use a current stable Kotlin compiler and JDK 17 toolchain, as recommended
by the [official Gradle setup guide](https://kotlinlang.org/docs/gradle-configure-project.html).

## Prerequisites

This track has no earlier library-course prerequisite. You need a terminal, a current Kotlin compiler,
a JDK, and enough command-line confidence to run a compiler. The course assumes no Android SDK: that
is intentionally deferred to Android App Development.

## Concept map

The examples are deliberately broad but shallow: exactly the Kotlin surface an Android newcomer
will meet immediately. Each item is named so you can return to its first worked example.

- **co-01 · Kotlin toolchain** — compile and run `fun main()` with `kotlinc` or Gradle.
- **co-02 · `val` and `var`** — bindings are read-only or reassignable; prefer `val`.
- **co-03 · type inference** — Kotlin infers types from initial values while preserving explicit annotations.
- **co-04 · basic types** — numeric, boolean, character, and string values have explicit conversions.
- **co-05 · string templates** — `$name` and `${expression}` compose readable output.
- **co-06 · null safety** — non-null is the default; `T?` records possible absence in the type.
- **co-07 · safe calls** — `?.` stops a member-access chain and returns `null` safely.
- **co-08 · Elvis** — `?:` supplies a fallback or makes an early return explicit.
- **co-09 · not-null assertions** — `!!` converts a nullable value at the cost of a possible NPE.
- **co-10 · safe `let`** — `?.let` enters a block only for a present value.
- **co-11 · functions** — `fun` declares reusable behaviour; an omitted return type is `Unit`.
- **co-12 · default and named arguments** — one signature replaces many overloads.
- **co-13 · single-expression functions** — concise functions infer their result type.
- **co-14 · lambdas** — function literals support trailing-lambda syntax and implicit `it`.
- **co-15 · higher-order functions** — functions can accept and return functions.
- **co-16 · collections** — read-only and mutable collection interfaces are intentionally distinct.
- **co-17 · collection operations** — `map`, `filter`, `fold`, and `forEach` build data pipelines.
- **co-18 · extension functions** — add a natural call syntax without changing the receiver type.
- **co-19 · classes and constructors** — constructor properties and `init` establish object state.
- **co-20 · data classes** — value records receive equality, `copy`, destructuring, and diagnostics.
- **co-21 · interfaces** — behaviour contracts permit polymorphism and useful defaults.
- **co-22 · objects and companions** — singleton state and class-level factories have explicit homes.
- **co-23 · `when` expressions** — branching can produce a value instead of merely selecting statements.
- **co-24 · `if` expressions** — value-producing conditionals must cover both outcomes.
- **co-25 · sealed classes** — a closed result hierarchy makes a `when` exhaustively checkable.
- **co-26 · coroutine preview** — `suspend`, `launch`, and structured lifetimes introduce non-blocking work.

## Learning route

- [Beginner examples](./beginner.md) establish syntax, nullability, and functions (Examples 1–26).
- [Intermediate examples](./intermediate.md) add lambdas, collections, and modelling (Examples 27–54).
- [Advanced examples](./advanced.md) use exhaustive state and a carefully scoped coroutine preview (Examples 55–78).
- [Capstone](./capstone/overview.md) consolidates the whole primer without becoming an Android project.

## Scope boundary

The course intentionally stops before Android views, Compose, lifecycle APIs, Flows, channels,
dependency injection, and architecture patterns. Those are platform concerns or deeper concurrency
topics. Finishing this primer means you can read Kotlin used by the Android course and make small,
safe changes; it does not claim comprehensive Kotlin mastery.
