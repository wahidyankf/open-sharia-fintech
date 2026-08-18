---
title: "Purpose, Scope, and When to Use"
description: Explains why the plan-multi-repo-parity-planning-and-execution composite exists and when to use it versus its standalone constituents.
when_to_use: Use when deciding whether this end-to-end composite (vs. running planning and execution separately) fits the task at hand.
---

# Purpose, Scope, and When to Use

**Purpose**: Run the full parity lifecycle end-to-end: first orchestrate
[plan-multi-repo-parity-planning](../plan-multi-repo-parity-planning.md) to survey the parity set,
grill every cross-repo gap to a recorded decision, and author one gated plan per repo — then
continue WITHOUT a separate invocation into [plan-execution](../plan-execution.md) for each
resulting plan, executing every delivery checklist to zero findings and archiving each plan to its
repo's `plans/done/`. The composite exists so "plan it across the repos AND do it" is a single
orchestrated request instead of four manual hand-offs.

This workflow composes its two constituents **by reference**: every rule of
plan-multi-repo-parity-planning governs the planning phase, and every rule of plan-execution
(worktree gate, Iron Rules, Atomic Sync Ritual, CI verification, archival, prompted worktree
cleanup) governs the execution phase. This document defines only the glue: the phase gate between
them, the third (pre-execution) grill, the composite Task list contract, and cross-repo
finalization.

**When to use**:

- When the same structural improvement is needed across sibling repos and the invoker wants it
  planned AND delivered in one orchestrated run
- When the cross-repo decision surface needs the parity grilling discipline, and the resulting
  plans should not sit unexecuted
- When you want one continuous observability surface (a single live Task list) covering planning
  and execution across all repos

**When NOT to use**:

- Plans should be reviewed via PR before execution → run
  [plan-multi-repo-parity-planning](../plan-multi-repo-parity-planning.md) alone with
  `mode: worktree-to-pr`, then run [plan-execution](../plan-execution.md) per repo after merge
- Single-repo work → [plan-planning](../plan-planning.md) followed by
  [plan-execution](../plan-execution.md)
