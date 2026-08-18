---
title: "Operating Budgets — The PR Is the Independent Merge Point (Continued)"
description: "Continues the independent-merge-point rule: why the worktree is a per-repository unit rather than a per-PR unit."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when reasoning about worktree scope relative to a repository versus a single PR.
---

# Operating Budgets — The PR Is the Independent Merge Point (Continued)

The qualifier **"that produces changes"** is load-bearing, and a plan's **Phase 0** is where it bites: Environment Setup and Baseline produces no reviewable change, so it is not a DAG leaf and gets **no PR** under any delivery mode. The earliest phase that may open one is **Phase 1**. See [Plans Organization Convention §Phase 0 Opens No PR](../../../conventions/structure/plans/phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).

Because the worktree is now a per-repository unit rather than a per-PR one, it is cleaned up once — after every PR that used it has landed — not when the first one does. Cross-repo parallelism is unaffected: an N-repo plan still runs one worktree per repo, in parallel with the other repos' worktrees; the cap only forecloses opening a second worktree for a repo the plan already has one open in.
