---
title: "Phase A — Load Plans and Build the Dependency DAG (Scope and Nodes)"
description: Covers A1-A3 — resolving plan scope, gating unvetted plans, and parsing delivery checklists into DAG nodes.
when_to_use: Use when resolving plan scope, gating on plan-quality-gate, or building DAG nodes from a delivery.md.
---

# Phase A — Load Plans and Build the Dependency DAG (Scope and Nodes)

Continued in
[Phase A — Edges, Report, and Diagram](./phase-a-edges-report-and-diagram.md).

**A1. Resolve the caller's scope to a concrete, frozen plan set.** The `plans` input is either an
explicit list or a set-selector; both resolve here into one enumerated set that is then **frozen for
the whole run** (never re-expanded later — a plan added to `plans/backlog/` mid-run is not pulled in).

- **Explicit list** — for each named plan, resolve its folder (in `plans/in-progress/` or, if named
  there, `plans/backlog/`). Fail fast with a clear error if a named plan does not exist.
- **Set-selector** — enumerate the named bucket's folders: `all-in-progress` → every folder directly
  under `plans/in-progress/`; `all-backlog` → every folder directly under `plans/backlog/`; `all` →
  both. Skip non-plan entries (`README.md`, the `ideas/` folder, `.gitkeep`).
- **Exclusion (`except …`)** — subtract every named plan from the resolved set. Each excluded name
  MUST match a plan actually in the set; a no-op exclusion (name not in scope) is a caller error —
  report it rather than silently ignoring, so a typo'd exclusion never fails open into executing a
  plan the caller meant to hold back.
- **Echo the frozen set.** Before scheduling, print the fully-enumerated resolved plan list (and, for
  a selector, the bucket + exclusions that produced it) so the caller can confirm scope. An empty
  resolved set (e.g., `all-in-progress` with nothing in-progress) terminates `fail` with a clear
  message — there is nothing to execute.
- **Promote every resolved `plans/backlog/` entry before scheduling.** For each plan in the frozen
  set that still resolves inside `plans/backlog/` (an explicit-list entry or any `all-backlog`/`all`
  member), run the promotion from
  [`plan-execution.md` Step 0](../plan-execution/enter-worktree-preconditions-and-work-branch.md) —
  `git mv plans/backlog/<slug>/ plans/in-progress/<slug>/`, commit, push to `origin main` — on the
  local `main` checkout, never inside a worktree, before that plan's first node is scheduled. Only
  after that push lands does the plan's path resolve to `plans/in-progress/` for the rest of this
  run. No plan in the frozen set is ever scheduled directly out of `plans/backlog/`.

**A2. Refuse unvetted plans.** For each plan, confirm it passed `plan-quality-gate` (a clean strict
double-zero — check for the plan's audit trail or re-run the gate). A plan that has not been vetted
is **not scheduled**; report it and continue with the rest. This prevents executing a half-baked
plan concurrently with good ones.

**A3. Parse each plan's delivery checklist into nodes.** Read every plan's `delivery.md`
top-to-bottom (disk is truth). Each `- [ ]` checkbox — **including every nested sub-bullet** —
becomes one **node**. A node carries: `plan-id`, `phase`, the checkbox prose, its `[AI]`/`[HUMAN]`
tag, and a computed **resource-set** (A5).
