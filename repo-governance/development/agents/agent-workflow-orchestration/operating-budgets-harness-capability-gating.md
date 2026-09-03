---
title: "Operating Budgets — Harness Capability Gating"
description: "Defines how orchestration behavior is gated by the current harness's capabilities."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when an orchestration behavior depends on whether the current harness supports it.
---

# Operating Budgets — Harness Capability Gating

Not every coding-agent harness can run background or parallel subagents. The model above is stated so that it degrades cleanly rather than becoming inapplicable:

> Where the harness supports background or parallel subagents, execute independent DAG nodes concurrently up to the declared cap. Under `*-to-pr`, each unit has its own branch; under permitted direct modes, each unit uses its declared checkpoint. Worktree modes reuse at most one worktree per repo per plan, while main modes use the primary checkout and provision none. Resource-heavy cross-repository work remains serial by default unless the plan records a concrete need and confirmed capacity/risk controls. Without background subagents, walk the same DAG serially. In every case, preserve dependency order, non-destructive Git, mode-specific integration safety, and cleanup.

The DAG itself is the portable artifact: the same dependency graph drives a wide fan-out on a background-capable harness and a serial walk on a single-threaded one. Concurrency changes the schedule, never the ordering or the safety rules.
