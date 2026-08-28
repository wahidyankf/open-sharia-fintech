---
title: "Parallel-by-Default Practice"
description: "Runs independent work in parallel within the declared cap, except cross-repository heavy work serializes by default on the shared machine."
when_to_use: "Read this index to find the right Parallel-by-Default Practice child document."
---

# Parallel-by-Default Practice

- [Parallel-by-Default — Purpose and Scope](./purpose-and-scope.md) — The two failure modes parallel-by-default eliminates, its ordinary scope, and the narrow cross-repository heavy-work exception. Use when deciding whether a specific piece of work falls under this practice's scope.
- [Parallel-by-Default — Standards 1-2: Parallel Unless Dependent, and the N+1 Model](./standards-1-to-2.md) — The default execution model, the shared-machine heavy-work exception, and the adjustable N+1 concurrency model. Use when deciding whether to run work serially or in parallel, and how many concurrent units are allowed.
- [Parallel-by-Default — Standards 3-4: Background-Slot Preference and DAG-First Ordering](./standards-3-to-4.md) — Preferring background slots, declaring the dependency DAG, and recording a multi-repository resource schedule. Use when deciding how to schedule a task list or delivery checklist.
- [Parallel-by-Default — Anti-Patterns and References](./anti-patterns-and-references.md) — Four common failure patterns (serial reads, serial searches, self-promoting the cap, parallelizing dependent work) plus links to related principles, practices, and agents Use when reviewing your own execution pattern for one of these four failure modes, or to find related documentation.
