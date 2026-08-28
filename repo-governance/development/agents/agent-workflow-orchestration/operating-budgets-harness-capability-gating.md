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

> Where the harness supports background or parallel subagents, execute the DAG's independent nodes concurrently, each on its own branch (never its own worktree — a repo's worktree is capped at one per plan and reused, branch-switched, across every node landing in that repo). Different repos may each use their one worktree, but resource-heavy provisioning, toolchain setup, builds, and validation run one repo at a time by default; concurrent cross-repo heavy work requires a recorded operational need and confirmed capacity/risk controls. Respect the harness's own documented concurrency ceiling if one exists. Where the harness does NOT support background/parallel subagents, execute the same DAG **serially**, node by node, in dependency order — one branch at a time is fine (serial execution has no concurrent-edit collision to isolate against). In both modes, the delivery-safety rules (no destructive git operations, worktree cleanup on completion, no direct pushes to protected branches) apply **identically** regardless of concurrency mode.

The DAG itself is the portable artifact: the same dependency graph drives a wide fan-out on a background-capable harness and a serial walk on a single-threaded one. Concurrency changes the schedule, never the ordering or the safety rules.
