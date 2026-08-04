---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Use these five drills after working through the examples. Each `before/` source contains one
focused bug or unsafe design; make the smallest change needed, then compare your answer with
`after/`.

## Recall Q&A

1. Why is the null-forgiving operator not a substitute for handling a missing value?
   <details><summary>Answer</summary>It only suppresses a compiler warning. The runtime value can
   still be absent, so the program needs an explicit fallback or failure boundary.</details>
2. What does a record `with` expression preserve?
   <details><summary>Answer</summary>It creates a new value with selected changes, leaving the
   source value available for callers that still need it.</details>
3. When should an asynchronous exception be observed?
   <details><summary>Answer</summary>At the `await` boundary, where the caller can translate it into
   a useful result or diagnostic.</details>

## Applied problems

1. A repository returns no matching record. Keep the absence in the type and provide a caller-level
   fallback instead of dereferencing with `!`.
2. A LINQ query observes a collection that later changes. Materialize the query at the boundary where
   a stable snapshot is required.
3. A service consumer creates file storage directly. Introduce an interface so a test can use a
   deterministic substitute and the consumer keeps one responsibility.

## Code katas

1. Nullable lookup: replace a null-forgiving dereference with a safe fallback.
2. Record transition: replace mutation with a non-destructive `with` copy.
3. Deferred query: snapshot a LINQ query before a changing collection alters its output.
4. Interface seam: depend on an interface rather than construct storage in the consumer.
5. Awaited failure: await a task and catch its expected exception at the await boundary.

Run a fixed drill with `dotnet run --project after/Drill.csproj`. Its expected output is in the
fixed source.

## Self-check checklist

- [ ] I can represent an absent result without suppressing nullable analysis.
- [ ] I can explain why a record copy is safer than a shared mutable update.
- [ ] I can choose when a deferred query needs materializing.
- [ ] I can introduce an interface at the storage boundary without leaking implementation details.
- [ ] I can handle an expected asynchronous failure at the awaited operation.

## Elaborative interrogation and self-explanation

1. Why does making absence explicit improve both runtime safety and test design?
2. Why does a non-destructive record transition make state changes easier to reason about?
3. Why is the `await` expression the right place to decide how a failure appears to a caller?
