---
title: "Worktree Cap — One Worktree Per Repository Per Plan (HARD RULE)"
description: Caps a plan to at most one worktree per repository, reused across every delivery unit landed there, and states the cleanup timing.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when a plan produces more than one delivery unit in the same repository and needs to know whether a second worktree is allowed.
---

# Worktree Cap — One Worktree Per Repository Per Plan (HARD RULE)

A plan provisions **at most one worktree per repository**, regardless of how many independent DAG
leaves or delivery units that plan produces in that repo. The worktree is reused — branch-switched —
across every delivery unit the plan lands in that repository; provisioning a second `git worktree add`
for the same repo within one plan is a defect. A plan touching **N** repositories therefore provisions
**at most N worktrees total**, one per repo, never more than one concurrently open per repo.

This caps a genuinely scarce shared resource: each worktree is a full checkout plus a converged
polyglot toolchain (`npm install && npm run doctor -- --fix`), and on the same-machine assumption
(other agents, engineers, and CI runners sharing this disk concurrently — see the
[Agent Workflow Orchestration Convention](../../../development/agents/agent-workflow-orchestration/operating-budgets-parallelism-budget.md))
that setup cost is worth paying once per repo, not once per delivery unit.

**What stays one-per-delivery-unit**: the **branch** and the **PR** — unchanged from
[One Branch, One PR, One Delivery Unit](../../../workflows/plan/plan-planning/planning-granularity-and-one-branch-rule.md#one-branch-one-pr-one-delivery-unit-hard-rule).
Only the **worktree** moves from a per-delivery-unit unit to a per-repository one.

**Sequencing consequence**: because at most one worktree exists per repo, delivery units that share a
repo execute their file edits **serially** within that shared worktree — finish and push unit A's
branch, open its PR, then `git fetch origin && git checkout -b <unit-B-branch> origin/main` in the
same worktree directory for unit B. Repositories remain separate DAG nodes, but their
resource-heavy worktree provisioning, toolchain setup, builds, and validation run **one repository
at a time by default** on the shared machine. Concurrent cross-repository heavy work requires the
plan's recorded operational need plus confirmed capacity and risk controls; lightweight independent
work may still fan out. See
[Delivery Checklists Express a DAG](./delivery-checklists-express-a-dag.md).

**Cleanup timing**: a repo's shared worktree is removed only once **every** delivery unit's PR that
used it has landed — never when the first one does. See the
[Worktree and Artifact Cleanup Convention](../../../development/workflow/worktree-and-artifact-cleanup.md).

**Enforcement**: `plan-checker` flags a plan whose `## Parallelization Model` or `### Delivery
Boundaries` table names more than one worktree path for the same repository as **HIGH**.
`plan-execution-checker` flags an execution history showing more than one `git worktree add` for the
same repo within one plan as **HIGH**.
