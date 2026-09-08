---
description: "Covers DAG-first orchestration and the preference for background slots over serial execution."
when_to_use: Use when sequencing dependent work or deciding whether to run a task in the background.
---

# Operating Budgets — DAG-First Orchestration and Background-Slot Preference

## DAG-First Orchestration

Every non-trivial task list **and** plan delivery checklist declares an explicit **dependency DAG**: nodes are tasks or checklist items, edges are `blocks` / `blockedBy`. **Independent** nodes run in parallel up to N; **dependent** nodes serialize. The DAG's **independent-node width** — not N — is what the orchestrator actually fans out to; N only caps it.

- **Task lists** express dependencies directly via `blocks` / `blockedBy`.
- **`delivery.md`** expresses phases and steps as a DAG, plus a `## Parallelization Model` section naming which items are concurrent and which are serial. **Cleanup is the terminal node**, depending on every delivery node — it runs last, once nothing else can still need the artifacts it removes.

Determine independence before fanning out, not after. Two nodes are independent only when neither reads what the other writes; a shared output file, a shared branch, or an ordering constraint makes them dependent regardless of how separable they look. The delivery-checklist expression of this rule is documented in the [Plans Organization Convention](../../../conventions/structure/plans.md).

For multi-repository plans, classify each compute-bearing node under
[Resource-Aware Development](../../practice/resource-aware-development.md). Compute cost alone does
not add a DAG edge: logically independent nodes enter HIPPO concurrently and run only when their
fixed CPU/memory reservations fit. Add serial edges only for dependency, shared-output,
byte-identity, transactional, or documented correctness constraints.

## Background-Slot Preference

Fill the **background** slots up to N and keep the **main thread vacant** and responsive — the main thread is the **orchestrator**, background agents are the **workers**. This is **bounded by the DAG**: fan out only genuinely independent nodes, and never split dependent work artificially to raise slot utilization.
