---
description: Preferring background slots to keep the main thread vacant, and declaring an explicit dependency DAG in every non-trivial task list or plan delivery checklist
when_to_use: Use when deciding whether to run parallel work in the foreground or background, or when writing a task list's or delivery checklist's dependency structure.
---

# Standards 3-4: Background-Slot Preference and DAG-First Ordering

## Standard 3 — Background-Slot Preference (Keep the Main Thread Vacant)

Prefer to fill the **background** slots up to N and keep the **main thread vacant** and responsive. The main thread is the **orchestrator**; background agents are the **workers**. A user who asks a question mid-batch should not wait behind the main thread's own long-running work.

This preference is **bounded by the DAG** (Standard 4): fan out only genuinely independent nodes. "Maximize background utilization" never justifies artificially splitting dependent work to fill idle slots — a dependent chain running one node at a time is correct, not a failure to parallelize. Independence governs the fan-out; N only caps it.

## Standard 4 — DAG-First Ordering

Every non-trivial task list **and** plan delivery checklist declares an explicit **dependency DAG**: nodes are tasks or checklist items, edges are `blocks` / `blockedBy`. Independent nodes run in parallel up to N; dependent nodes serialize.

The DAG's **independent-node width** is what the orchestrator fans out to — N only caps that width, it never creates it. Establish the DAG _before_ dispatching, not after: two nodes are independent only when neither reads what the other writes, so a shared output file, a shared branch, or an ordering constraint makes them dependent however separable they appear. **Cleanup is the terminal node**, depending on every other node, so it can never remove an artifact something still in flight needs.

Task lists express this via `blocks` / `blockedBy`; `delivery.md` expresses it as phases/steps plus a `## Parallelization Model` section — see the [Plans Organization Convention](../../../conventions/structure/plans.md) and the [Agent Workflow Orchestration Convention](../../agents/agent-workflow-orchestration.md).

For a plan spanning repositories, the `## Parallelization Model` also classifies each compute node
under [Resource-Aware Development](../resource-aware-development.md) and records any dependency,
shared-output, byte-identity, transactional, or correctness edge that forces serialization.
Logically independent compute nodes may overlap only when HIPPO admits their complete reservations;
the plan never invents its own live-capacity exception.
