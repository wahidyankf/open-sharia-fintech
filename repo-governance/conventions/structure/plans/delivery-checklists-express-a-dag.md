---
title: "Delivery Checklists Express a DAG (HARD RULE)"
description: Requires a Parallelization Model naming concurrent vs. serial delivery nodes.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing a plan's Parallelization Model.
---

# Delivery Checklists Express a DAG (HARD RULE)

`delivery.md` expresses its phases and steps as a **dependency DAG**, not merely as a top-to-bottom
list. Nodes are phases and checklist items; edges are `blocks` / `blockedBy`. Independent nodes may
run in parallel; dependent nodes serialize.

Every non-trivial plan carries a **`## Parallelization Model`** section, placed before the first
phase, stating:

- **Which nodes are concurrent and which are serial**, and why — a serial spine exists because each
  phase builds the source of truth the next one needs, not because the list happens to be ordered.
- **The plan's chosen N** (see the [Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration.md)
  for the N+1 model), and any reason it differs from the default.
- **Cleanup as the terminal node**, depending on every delivery node — so the cleanup gate can never
  remove a worktree, branch, or artifact that an in-flight node still needs.

The distinction that makes this worth writing down: **sequence is not dependency**. A checklist is
necessarily written in some order, but only some of that order is load-bearing. Stating the DAG
separates the two, so an executor knows which items may fan out and which must wait — rather than
inferring it from list position and serializing work that never needed to be serial, or parallelizing
work that did.

Two nodes are independent only when neither reads what the other writes. A shared output file, a
shared branch, or an ordering constraint makes them dependent however separable they look.

**Enforcement**: `plan-checker` flags a non-trivial plan lacking a `## Parallelization Model` section
as **MEDIUM**, and flags a declared-parallel node set with a genuine write conflict as **HIGH**.

See [Delivery Checklists Express a DAG — Delivery Units and Planning Granularity](./delivery-checklists-express-a-dag-continued.md) for how DAG nodes map to delivery units, PRs, and the worktree cap.
