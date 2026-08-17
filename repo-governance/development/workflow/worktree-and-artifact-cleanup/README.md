---
title: "Worktree and Artifact Cleanup Convention"
description: "Mandatory plan-end gate requiring a plan to remove the worktrees, branches, and build artifacts it created — self-scoped, verified idle, and never touching shared caches other sessions depend on"
when_to_use: "Read this index to find the right Worktree and Artifact Cleanup Convention child document."
---

# Worktree and Artifact Cleanup Convention

- [Principles and Conventions Implemented](./01-principles-and-conventions-implemented.md) — The principles and companion conventions the worktree and artifact cleanup gate implements and respects. Use when tracing why the worktree and artifact cleanup gate exists back to the principles and conventions it respects.
- [Why This Is a Gate](./02-why-this-is-a-gate.md) — Why uncleaned worktree artifacts harm a shared machine — disk, ref namespace, and stale-state ambiguity. Use when justifying why cleanup is mandatory rather than optional on a shared machine.
- [The Three Artifact Classes](./03-the-three-artifact-classes.md) — The three artifact classes a complete cleanup covers — worktrees, branches, and build output. Use when checking that a cleanup covers all three artifact classes, not just the first.
- [Hard Safety Rules](./04-hard-safety-rules.md) — The rules bounding every action the cleanup gate takes — self-created only, verify before deleting, never touch shared caches. Use when deciding whether a specific cleanup action is in-scope for a plan to perform.
- [Mandatory Pre-Removal Checks](./05-mandatory-pre-removal-checks.md) — The five checks required before any git worktree remove, each grounded in an observed incident. Use immediately before running git worktree remove, to confirm merge state, dirty diff, unpushed commits, and idleness.
- [Branch Cleanup](./06-branch-cleanup.md) — How to safely delete local and remote branches a plan created, after their PR is confirmed merged. Use when deleting local or remote branches after removing a repo's worktree.
- [Build-Artifact Cleanup](./07-build-artifact-cleanup.md) — Scope and exclusions for purging build output produced inside a plan's own worktrees. Use when deciding what build output to purge, and what to leave alone, during plan-end cleanup.
