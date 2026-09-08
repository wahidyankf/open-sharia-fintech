---
description: Extends plan-execution.md's granular 1:1 Task-list mapping to the discovery, anomaly, and cleanup phases this workflow adds before the delivery checklist loads.
when_to_use: Use when materializing Tasks for a takeover-execution run, to confirm the granularity each phase requires.
---

# Task List Discipline for This Workflow

The same granular, 1:1 Task-list mapping `plan-execution.md` requires for delivery-checklist items
(see its [Iron Rule 1](../plan-execution/iron-rules-1-5.md#iron-rules-non-negotiable)) extends to the phases this
workflow adds before that checklist even loads:

- **One Task per (repo × artifact-class) discovery probe** in Phase A — never one coarse "discover
  state" task. Six artifact classes × N repos is 6N tasks, not one.
- **One Task per Bucket-4 anomaly** raised in Phase B, closed only once the user's resolution is
  recorded (see Phase C step 5) — an anomaly is never silently dropped from the live list.
- **One Task per cleanup candidate** in Phase D — never a single "cleanup" task covering several
  worktrees or branches.
- **Every checkbox Phase C step 5 ticks from discovered evidence gets its own Task too.** If no Task
  yet exists for that checkbox (the common case — discovery runs before any delivery-checklist Task
  list has been materialized), create one, then immediately complete it in the same breath as the
  `delivery.md` edit — the identical pairing `plan-execution.md`'s Atomic Sync Ritual requires mid-execution, applied here at takeover time instead.
- **Phase E rebuilds and resumes `plan-execution.md`'s own per-checkbox Task list per its Step 1**,
  unchanged — this workflow's own discovery/cleanup/reconciliation tasks close out as Phase E's
  handoff begins, not before, and never get silently merged into the delivery-checklist tasks Phase E
  creates next.

**This is harness-agnostic.** Per the [multi-harness binding
model](../../../conventions/structure/multi-harness-binding.md), this document is vendor-neutral: "Task
list" here means whatever live task/todo-tracking primitive the executing session's harness exposes
(`TaskCreate`/`TaskUpdate`, or an equivalent primitive under another platform binding). Only the
concrete tool name varies by harness — the 1:1-mapping and immediate-sync requirements above bind
identically regardless of which one is in use.

Sync every task to completion immediately, matching the cadence `plan-execution.md` itself enforces
— no batching several probes', anomalies', or reconciled checkboxes' worth of task closes into one
update.
