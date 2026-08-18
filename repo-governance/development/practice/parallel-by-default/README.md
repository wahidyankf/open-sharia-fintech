---
title: "Parallel-by-Default Practice"
description: "When doing work with independent sub-units (tool calls, file reads/edits, searches, or delegated agents), default to running them in parallel rather than serially, capped at three concurrent units of work"
when_to_use: "Read this index to find the right Parallel-by-Default Practice child document."
---

# Parallel-by-Default Practice

- [Parallel-by-Default — Purpose and Scope](./purpose-and-scope.md) — The two failure modes (unnecessary latency, wasted throughput) that parallel-by-default eliminates, and exactly what work this practice covers and does not cover Use when deciding whether a specific piece of work falls under this practice's scope.
- [Parallel-by-Default — Standards 1-2: Parallel Unless Dependent, and the N+1 Model](./standards-1-to-2.md) — The default execution model (parallel unless dependent) and the adjustable N+1 concurrency model, including why the default is 3 and the adjustment rule Use when deciding whether to run work serially or in parallel, and how many concurrent units are allowed.
- [Parallel-by-Default — Standards 3-4: Background-Slot Preference and DAG-First Ordering](./standards-3-to-4.md) — Preferring background slots to keep the main thread vacant, and declaring an explicit dependency DAG in every non-trivial task list or plan delivery checklist Use when deciding whether to run parallel work in the foreground or background, or when writing a task list's or delivery checklist's dependency structure.
- [Parallel-by-Default — Anti-Patterns and References](./anti-patterns-and-references.md) — Four common failure patterns (serial reads, serial searches, self-promoting the cap, parallelizing dependent work) plus links to related principles, practices, and agents Use when reviewing your own execution pattern for one of these four failure modes, or to find related documentation.
