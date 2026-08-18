---
title: "Worktree Specification"
description: Defines where a plan declares its worktree path and the executor lifecycle for entering, syncing, and cleanup.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing a plan's Worktree section or resolving worktree entry/cleanup.
---

# Worktree Specification

Every plan MUST declare the worktree path in its content so the executor can verify the execution environment before reading the delivery checklist.

**Where to declare**:

- **Multi-file plans**: Add a top-level `## Worktree` section in `delivery.md`, placed before any phase heading.
- **Single-file plans**: Add a `## Worktree` section in `README.md`, placed before the `## Delivery Checklist` section.

**Worktree path format**: `worktrees/<plan-identifier>/` where `<plan-identifier>` is the slug portion of the folder name (strip the `YYYY-MM-DD__` prefix when present).

- `backlog/auth-rewrite/` → worktree path `worktrees/auth-rewrite/` (no prefix to strip)
- `in-progress/auth-rewrite/` → worktree path `worktrees/auth-rewrite/` (no prefix to strip)
- `done/2026-03-01__add-user-search/` → worktree path `worktrees/add-user-search/` (strip the completion-date prefix)

**Provisioning command** (optional manual pre-provisioning, run from repo root):

```bash
claude --worktree <plan-identifier>
```

Manual pre-provisioning is OPTIONAL: the [plan-execution workflow Step 0 gate](../../../workflows/plan/plan-execution/enter-worktree-preconditions-and-work-branch.md#0-enter-the-designated-worktree-sequential-hard-gate) enters the declared worktree by default — navigating to it when it already exists, and auto-provisioning it from the latest `origin/main` when it does not.

See [Worktree Specification — Executor Lifecycle and Example](./worktree-specification-continued.md) for how the executor enters, syncs, and cleans up the worktree, plus a worked `## Worktree` block.
