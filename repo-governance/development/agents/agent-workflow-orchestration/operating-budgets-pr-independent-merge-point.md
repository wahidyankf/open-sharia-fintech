---
title: "Operating Budgets — The PR Is the Independent Merge Point"
description: "Explains why worktree-to-pr isolates edits and why every DAG leaf that produces changes gets its own branch and PR."
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

Concretely: **every DAG leaf that produces changes gets its own branch and its own PR** — a strict one-node ↔ one-branch ↔ one-PR mapping. The **worktree**, unlike the branch, is capped at **one per repository per plan** and reused — branch-switched — across every leaf that lands in that repo; see [Plans Organization Convention §Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule). What sits on the PR side of the branch/PR mapping is a **delivery unit** — the contiguous run of phases ending at a **delivery boundary** — not necessarily a single phase: a PR opens at the natural delivery point, which may be once at the end of the unit or several times across a plan (see [§PRs Open at Delivery Boundaries](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule)). The corollary matters as much as the rule: nodes that are genuinely _dependent_ stay in one PR. The DAG governs. Never force-split an inseparable chain just to produce more PRs, and never batch independent nodes into one PR just to produce fewer.
