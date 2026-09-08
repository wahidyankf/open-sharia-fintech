---
description: "Runs independent work in parallel within the agent cap while HIPPO controls compute admission."
when_to_use: "Read this index to find the right Parallel-by-Default Practice child document."
---

# Parallel-by-Default Practice

- [Parallel-by-Default — Purpose and Scope](./purpose-and-scope.md) — The two failure modes parallel-by-default eliminates, its ordinary scope, and its relationship to resource admission. Use when deciding whether a specific piece of work falls under this practice's scope.
- [Parallel-by-Default — Standards 1-2: Parallel Unless Dependent, and the N+1 Model](./standards-1-to-2.md) — The default execution model, capacity-controlled compute, and the adjustable N+1 agent model. Use when deciding whether to run work serially or in parallel, and how many concurrent units are allowed.
- [Parallel-by-Default — Standards 3-4: Background-Slot Preference and DAG-First Ordering](./standards-3-to-4.md) — Preferring background slots, declaring the dependency DAG, and recording workload classes plus surviving serialization edges. Use when deciding how to schedule a task list or delivery checklist.
- [Parallel-by-Default — Anti-Patterns and References](./anti-patterns-and-references.md) — Four common failure patterns (serial reads, serial searches, self-promoting the cap, parallelizing dependent work) plus links to related principles, practices, and agents Use when reviewing your own execution pattern for one of these four failure modes, or to find related documentation.
