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

**Provisioning command** (run from repo root, before the plan is written):

```bash
claude --worktree <plan-identifier>
```

## Worktree Identity Record

Record this immutable block in the plan's `## Worktree` section when that section is authored.
It is the cleanup authority; the file-touch ledger records files only.

```markdown
### Provisioned Worktree Identity

- Exact path: `/absolute/repo/worktrees/<plan-identifier>`
- Initial branch: `<plan-identifier>-base`
- Created by: `<executor identity or session>`
- Created at: `<ISO-8601 UTC timestamp>`
```

Record actual `git worktree add` values and never rewrite them; a missing/conflicting identity blocks
removal. The initial branch proves provisioning, not the final checkout.

### Delivery Branch Inventory

Keep an append-only inventory beside the identity; add initial and plan-created branches before use:

```markdown
| Branch              | Mode             | Lifecycle state | Proof                                                |
| ------------------- | ---------------- | --------------- | ---------------------------------------------------- |
| `<initial-branch>`  | `provisioned`    | `active`        | `git worktree add` at `<UTC timestamp>`              |
| `<delivery-branch>` | `worktree-to-pr` | `delivered`     | PR #`<number>` merged; reviewed head `<40-char SHA>` |
```

The initial entry is `provisioned`/`active`, proven by creation command and timestamp. Before removal,
classify every entry as delivered, unused, or retained/escalated; active/unrecorded branches block
cleanup. `*-to-pr` records merged PR + reviewed-head SHA; direct push records verified `origin/main`
commit. Include `git -C <exact-path> branch --show-current`; the inventory, not file-touch ledger,
controls branch cleanup.

**Provision the worktree BEFORE defining the plan, and author inside it.** Later moves split its
history and defeat the pre-execution check. The [Step 0 gate](../../../workflows/plan/plan-execution/enter-worktree-preconditions-and-work-branch.md#0-enter-the-designated-worktree-sequential-hard-gate) enters or auto-provisions only as a backstop.

**One worktree per plan, reused across every PR the plan opens.** A plan that splits its delivery into several sequential PRs (see [PRs Open at Delivery Boundaries](./prs-open-at-delivery-boundaries-rules.md)) does NOT provision a worktree per PR. Land one slice, fast-forward the same worktree from `origin/main`, then open the next slice from it.

See [Worktree Specification — Executor Lifecycle and Example](./worktree-specification-continued.md) for how the executor enters, syncs, and cleans up the worktree, plus a worked `## Worktree` block.
