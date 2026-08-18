---
title: "Delivery Checklists Express a DAG — Delivery Units and Planning Granularity"
description: Explains how each independent DAG node that produces changes maps to its own delivery unit, branch, and PR, and points to the full planning-granularity rules.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when mapping a plan's DAG nodes onto delivery units, branches, and PRs.
---

# Delivery Checklists Express a DAG — Delivery Units and Planning Granularity

Continues [Delivery Checklists Express a DAG (HARD RULE)](./delivery-checklists-express-a-dag.md).

**Each independent DAG node that produces changes lands as its own delivery unit and PR** — one
branch → one PR → one delivery unit, opened and merged when that unit's delivery boundary is
reached rather than held for a batch merge at plan end. The **worktree** is a coarser unit than the
branch: a plan provisions **at most one worktree per repository**, reused — branch-switched — across
every delivery unit the plan produces in that repo, rather than a fresh worktree per unit. See
[Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule). Partial work
reaches `main` merged-but-dark behind a feature flag; dependent nodes that cannot be separated stay a
single delivery unit. Exactly how a plan's phases map onto delivery units and PRs — including which
phase inside a unit is the boundary that actually opens one — is stated in
[PRs Open at Delivery Boundaries, Not Every Phase](./prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule).
The remaining planning-granularity rules — the strict 1-PR↔1-branch mapping, the worktree cap,
the feature-flag default with its unflagged escape and named removal step, and how the
`worktree-to-pr` default binds as a design obligation at authoring time — are stated in the
[plan-planning workflow §Planning Granularity](../../../workflows/plan/plan-planning/planning-granularity-and-one-branch-rule.md).
