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

Every plan declares its worktree path before the executor reads the delivery checklist.

**Where to declare**:

- **Multi-file plans**: Add a top-level `## Worktree` section in `delivery.md`, placed before any phase heading.
- **Existing pre-contract single-file plans only**: Add a `## Worktree` section in `README.md`,
  placed before `## Delivery Checklist`. This compatibility path never authorizes creation of a new
  single-file formal plan.

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

Record actual `git worktree add` values immutably. Missing or conflicting identity blocks removal;
the initial branch proves provisioning, not final checkout.

For a declared multi-repository parity objective, also include the common objective slug, worktree
basename, and corresponding branch mapping defined by
[Cross-Repository Parity Identity](../../../development/workflow/cross-repository-parity-identity.md).
Every repository using a worktree records the same basename; every corresponding short-lived branch
records the same name. Modes without either identity record `not applicable` with a reason.

### Delivery Branch Inventory

Keep an append-only inventory beside the identity; add initial and plan-created branches before use:

```markdown
| Branch              | Mode             | Lifecycle state | Proof                                                |
| ------------------- | ---------------- | --------------- | ---------------------------------------------------- |
| `<initial-branch>`  | `provisioned`    | `active`        | `git worktree add` at `<UTC timestamp>`              |
| `<delivery-branch>` | `worktree-to-pr` | `delivered`     | PR #`<number>` merged; reviewed head `<40-char SHA>` |
```

Before removal, classify every entry as delivered, unused, or retained/escalated; active or
unrecorded branches block cleanup. `*-to-pr` records merged PR plus reviewed-head SHA; direct push
records verified `origin/main`. Include `git -C <exact-path> branch --show-current`. This inventory,
not the file ledger, controls branch cleanup.

**Provision the worktree BEFORE defining the plan, and author inside it by default.** Later moves
split its history and defeat the pre-execution check.

### Authoring-Worktree Exception

When the new plan artifact is itself a deliverable being authored inside another existing worktree
that the user explicitly required the session to keep using, the plan may declare its matching
execution worktree as pending. This exception exists for plan-authoring changes that depend on
unlanded work in the active worktree; convenience alone does not qualify.

The `## Worktree` section must still name `worktrees/<plan-identifier>/`, record `Provisioning status:
pending`, name the active authoring worktree and user constraint, and omit—not fabricate—the
Provisioned Worktree Identity and branch inventory. The
[Step 0 gate](../../../workflows/plan/plan-execution/enter-worktree-preconditions-and-work-branch.md#0-enter-the-designated-worktree-sequential-hard-gate)
must provision the declared matching worktree, initialize the immutable identity/inventory, and
sync it before any delivery packet begins. The exception ends at execution.

**At most one worktree per repository per plan, reused across its PRs.** For sequential PRs, land
one slice, fast-forward the same worktree from `origin/main`, then open the next. See
[PRs Open at Delivery Boundaries](./prs-open-at-delivery-boundaries-rules.md).

See [Worktree Specification — Executor Lifecycle and Example](./worktree-specification-continued.md) for how the executor enters, syncs, and cleans up the worktree, plus a worked `## Worktree` block.
