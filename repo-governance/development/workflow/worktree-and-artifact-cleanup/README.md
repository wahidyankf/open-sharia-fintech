---
title: "Worktree and Artifact Cleanup Convention"
description: "Mandatory plan-end gate requiring a plan to remove the worktrees, branches, and build artifacts it created — self-scoped, verified idle, and never touching shared caches other sessions depend on"
when_to_use: "Read this index to find the right Worktree and Artifact Cleanup Convention child document."
---

# Worktree and Artifact Cleanup Convention

- [Principles and Conventions Implemented](./principles-and-conventions-implemented.md) — The principles and companion conventions the worktree and artifact cleanup gate implements and respects. Use when tracing why the worktree and artifact cleanup gate exists back to the principles and conventions it respects.
- [Why This Is a Gate](./why-this-is-a-gate.md) — Why uncleaned worktree artifacts harm a shared machine — disk, ref namespace, and stale-state ambiguity. Use when justifying why cleanup is mandatory rather than optional on a shared machine.
- [The Three Artifact Classes](./the-three-artifact-classes.md) — The three artifact classes a complete cleanup covers — worktrees, eligible branches, and plan-local regenerable build output. Use when checking that cleanup covers all three without deleting retained evidence or shared state.
- [Hard Safety Rules](./hard-safety-rules.md) — The rules bounding every action the cleanup gate takes — self-created only, verify before deleting, never touch shared caches. Use when deciding whether a specific cleanup action is in-scope for a plan to perform.
- [Mandatory Pre-Removal Checks](./mandatory-pre-removal-checks.md) — The six checks required before any git worktree remove, each grounded in an observed incident. Use immediately before running git worktree remove, to confirm identity, branch delivery, dirty diff, unpushed commits, and idleness.
- [Branch Cleanup](./branch-cleanup.md) — How to safely delete local and remote plan-created branches, including the bare-repository ordering exception. Use when ordering branch and worktree removal after delivery proof passes.
- [Build-Artifact Cleanup](./build-artifact-cleanup.md) — Scope and exclusions for purging plan-local regenerable output while preserving diagnostics and shared caches. Use when deciding what build output to purge or retain during cleanup.
