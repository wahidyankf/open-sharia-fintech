---
title: "Worktree Specification — Executor Lifecycle and Example"
description: Defines the executor's enter/sync/cleanup lifecycle for a plan's worktree and shows a worked `## Worktree` block.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when implementing or auditing worktree entry, sync, and cleanup behavior.
---

# Worktree Specification — Executor Lifecycle and Example

Continues [Worktree Specification](./worktree-specification.md).

**Executor lifecycle** (enforced by the plan-execution workflow):

1. **Enter or provision**: execution always happens inside the declared worktree. The executor navigates to it if it exists, or provisions it from the latest `origin/main` (`git fetch origin && git worktree add -b <plan-identifier> worktrees/<plan-identifier> origin/main`) if it does not. When the plan produces more than one delivery unit in this repo, the SAME worktree is reused for every one of them (see [Worktree Cap](./worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule) below) — never provision a second worktree for a repo the plan already has one open in.
2. **Freshness sync**: before any implementation, the worktree is synced with the latest `origin/main` (ff-merge, or rebase when the worktree carries local commits). Dirty state or rebase conflicts stop execution for an explicit user decision. Starting a new delivery unit inside an already-provisioned worktree runs this same sync before branching off it.
3. **Prompted cleanup**: when the plan completes (`pass`), is archived, and all work is pushed to `origin main`, the executor verifies nothing is uncommitted or unpushed and then PROMPTS the user before deleting the worktree and its local branch(es). Worktrees are never deleted without explicit confirmation, and never deleted on `partial`/`fail`. For a multi-unit plan, this means the shared worktree is removed once — after every delivery unit's PR that used it has landed — not after the first one.

**This requirement applies to ALL plans regardless of size** — pure-docs, single-file, and trivial plans included. No exceptions.

See [Worktree Path Convention](../worktree-path.md) for the full routing and directory structure specification.

**Example `## Worktree` block** (delivery.md or README.md):

````markdown
## Worktree

Worktree path: `worktrees/auth-rewrite/`

Provisioned before this plan was written (run from repo root):

```bash
claude --worktree auth-rewrite
```

The plan-execution Step 0 gate enters this worktree by default: it auto-provisions from the latest `origin/main` when missing, syncs with `origin/main` before implementing, and prompts before deleting the worktree after the plan is archived and pushed.
````
