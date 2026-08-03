---
title: "Overview"
date: 2026-08-03T00:00:00+07:00
draft: false
weight: 1
---

Use these five drills after working through the examples. Each `before/` source contains one
focused bug or unsafe design; make the smallest change needed, then compare your answer with
`after/`.

1. Nullable lookup: replace a null-forgiving dereference with a safe fallback.
2. Record transition: replace mutation with a non-destructive `with` copy.
3. Deferred query: snapshot a LINQ query before a changing collection alters its output.
4. Interface seam: depend on an interface rather than construct storage in the consumer.
5. Awaited failure: await a task and catch its expected exception at the await boundary.

Run a fixed drill with `dotnet run --project after/Drill.csproj`. Its expected output is in the
fixed source.
