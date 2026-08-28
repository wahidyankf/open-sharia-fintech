---
title: "PRs Open at Delivery Boundaries — Rules 5-7 and *-to-pr Scope"
description: Gives the remaining three PR-boundary rules (independent nodes deliver separately, no deferred batching, an opened PR is never held) and states which delivery modes this rule binds.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding whether independent work may share a PR, or whether an already-open PR may wait for a later merge.
---

# PRs Open at Delivery Boundaries — Rules 5-7 and \*-to-pr Scope

Continues [PRs Open at Delivery Boundaries, Not Every Phase (HARD RULE)](./prs-open-at-delivery-boundaries-rules.md).

1. **Independent parallel DAG nodes still deliver separately.** Grouping phases into one delivery
   unit is permitted only along a dependency chain. Merging two independent nodes into one PR to
   reduce PR count is forbidden — it re-serialises work the DAG declared independent. This clause
   protects the parallelization rationale behind the `worktree-to-pr` default.
2. **A shippable increment may not be deferred merely to batch it.** If the work standing at phase N
   already satisfies the boundary test below, phase N is a boundary — a plan does not get to carry
   it forward to make a bigger PR.
3. **An opened PR is never held.** It is opened and merged when its boundary is reached; PRs never
   queue for a plan-end merge train. Grouping dependent phases into one delivery unit is not
   batching — holding independent, already-open PRs is exactly what this prohibition targets. Nor
   does this bar a **GitHub merge queue**, which serialises already-approved merges for CI
   correctness and holds nothing back: the prohibition is on a plan deferring its own merges, not on
   the platform ordering them.
4. **Parity PRs merge on each repository's own opportunity.** Once one repository's parity PR meets
   that repository's hardened merge prerequisites and a merge opportunity exists, merge it; never
   hold a ready PR solely to synchronize its merge with a sibling repository. Record any unfinished
   counterpart as a named sibling obligation until the repositories converge. A shared parity
   identity makes deliveries traceable; it does not create a synchronized-merge gate.

**Enforcement disposition for rule 4 — unenforced by decision.** Cross-repository readiness and a
merge opportunity require authenticated operational evidence that a repository-local deterministic
check cannot observe. The merge record plus explicit sibling obligation make the decision auditable.

This rule governs **PRs**, so it binds the `*-to-pr` delivery modes only. Under
`worktree-to-origin-main` or `main-to-origin-main` a plan opens no PR at all, and a **per-phase
commit-and-push checkpoint cadence there is correct and unaffected** — commits are not PRs, and
nothing in this section asks a direct-push plan to batch them.

See [PRs Open at Delivery Boundaries — Boundary Test and Rationale](./prs-open-at-delivery-boundaries-boundary-test.md) for the four-part boundary test that determines whether a given phase is a delivery boundary.
