---
title: "Phase A — Load Plans and Build the Dependency DAG (Scope and Nodes)"
description: Covers A1-A3 — resolving plan scope, gating unvetted plans, and parsing delivery checklists into DAG nodes.
when_to_use: Use when resolving plan scope, gating on plan-quality-gate, or building DAG nodes from a delivery.md.
---

# Phase A — Load Plans and Build the Dependency DAG (Scope and Nodes)

Continued in
[Phase A — Edges, Report, and Diagram](./phase-a-edges-report-and-diagram.md).

**A1. Resolve the caller's scope to a concrete, frozen plan set.** The `plans` input is either an
explicit list or a set-selector; both resolve once into one enumerated set.

- **Explicit list** — for each named plan, resolve its folder (in `plans/in-progress/` or, if named
  there, `plans/backlog/`). Fail fast with a clear error if a named plan does not exist.
- **Set-selector** — enumerate the named bucket's folders: `all-in-progress` → every folder directly
  under `plans/in-progress/`; `all-backlog` → every folder directly under `plans/backlog/`; `all` →
  both. Skip non-plan entries (`README.md`, the `ideas/` folder, `.gitkeep`).
- **Exclusion (`except …`)** — subtract every named plan from the resolved set. Each excluded name
  MUST match a plan actually in the set; a no-op exclusion (name not in scope) is a caller error —
  report it rather than silently ignoring, so a typo'd exclusion never fails open into executing a
  plan the caller meant to hold back.
- **Echo and persist the frozen set.** Print the fully enumerated list and selector/exclusions for
  caller confirmation. An empty set terminates `fail`. Before any promotion, apply
  [Frozen Scope Recovery](./phase-a-frozen-scope-recovery.md): store every member and promotion
  state in one durable run record, then reload that record rather than re-enumerating on resume.
- **Promote every resolved `plans/backlog/` entry before scheduling.** For each plan in the frozen
  set, resolve that plan's delivery mode and apply the canonical
  [Starting Work procedure](../../../conventions/structure/plans/starting-and-completing-work.md#starting-work).
  Complete and merge the pure-move worktree PR for a `*-to-pr` or direct-push-unavailable route;
  use direct push only for a selected direct-push mode that the repository permits. Schedule no
  node until the promotion exists on `origin/main`, the plan resolves under
  `plans/in-progress/`, and the durable run record reflects that verified state.

**A2. Refuse unvetted plans.** For each plan, confirm it passed `plan-quality-gate` (a clean strict
double-zero — check for the plan's audit trail or re-run the gate). A plan that has not been vetted
is **not scheduled**; report it and continue with the rest. This prevents executing a half-baked
plan concurrently with good ones.

**A3. Parse each plan's delivery checklist into nodes.** Read every plan's `delivery.md`
top-to-bottom (disk is truth). Each `- [ ]` checkbox — **including every nested sub-bullet** —
becomes one **node**. A node carries: `plan-id`, `phase`, the checkbox prose, its `[AI]`/`[HUMAN]`
tag, and a computed **resource-set** (A5).
