---
title: "Operating Budgets — The PR Is the Independent Merge Point"
description: "Explains why worktree-to-pr isolates edits and gives every change-producing DAG leaf its own branch and PR under that mode."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when deciding whether two pieces of concurrent work need separate worktrees and PRs.
---

# Operating Budgets — The PR Is the Independent Merge Point

`worktree-to-pr` is the default delivery mode (see [Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode)), and the reason is a parallelism reason, not a review-process one.

A worktree isolates **edits** — two agents writing to the same file in the same checkout would collide, and separate working trees prevent that. But isolated edits still have to land, and if N parallel units all funnel into one shared branch or one shared PR, they re-serialize at exactly the moment that matters. The **PR** is what makes them genuinely independent: N parallel units become **N PRs that review, gate, and merge independently**, none blocking any other. A slow review on one unit does not hold the other N-1 hostage.

Concretely, under `worktree-to-pr`, **every change-producing DAG leaf gets its own branch and PR** — a strict one-node ↔ one-branch ↔ one-PR mapping. The worktree is capped at **one per repository per plan** and reused across leaves; see [Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule). What sits on the PR side is a **delivery unit** — the contiguous run of phases ending at a natural **delivery boundary**, not necessarily one phase. Dependent nodes stay together; independent nodes do not batch. Other delivery modes preserve those natural units but use their resolved work location and integration mechanism.
