---
title: "Worktree and Artifact Cleanup Convention"
description: Mandatory plan-end gate requiring a plan to remove the worktrees, branches, and build artifacts it created — self-scoped, verified idle, and never touching shared caches other sessions depend on
category: explanation
subcategory: development
tags:
  - git
  - workflow
  - worktree
  - cleanup
  - parallelism
created: 2026-07-20
when_to_use: Use when a plan that created worktrees, branches, or build output is finishing and needs to tear them down.
---

# Worktree and Artifact Cleanup Convention

A plan that creates worktrees, branches, and build output must remove them when it finishes. This is
the **teardown** half of the worktree lifecycle; provisioning and toolchain initialization are covered
separately.

Cleanup is a **mandatory gate**, not a courtesy. It is also the one gate most likely to cause harm if
executed carelessly, because every action it takes is a deletion. The whole convention exists to make
that combination safe: delete thoroughly, delete only what is yours, and verify before each removal.

**Cleanup is immediate, not deferred.** Remove a repo's worktree the moment this plan is done using
it — when every delivery unit this plan places in that repo is confirmed merged — right then, not
batched with unrelated later steps and not left in place "in case it's needed again." Under the
[Worktree Cap](../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule),
a single-repo plan's "done using it" coincides with plan-end; a multi-repo plan's does not — each
repo's worktree is torn down as soon as that repo's own units land, independently of whether the
plan's other repos are still in flight.

**No confirmation prompt is required for an exact, self-created plan worktree.** Once all mandatory
pre-removal checks pass, the AI executor removes the exact path recorded in the plan immediately.
This authority never extends to a repository root, a wildcard, a worktree absent from the plan's
file-touch ledger, or any worktree created by another actor; those remain out of scope.

## Contents

- [Principles and Conventions Implemented](./worktree-and-artifact-cleanup/principles-and-conventions-implemented.md) — Why this gate exists.
- [Why This Is a Gate](./worktree-and-artifact-cleanup/why-this-is-a-gate.md) — Disk, ref namespace, and stale-state risk on a shared machine.
- [The Three Artifact Classes](./worktree-and-artifact-cleanup/the-three-artifact-classes.md) — Worktrees, branches, build output.
- [Hard Safety Rules](./worktree-and-artifact-cleanup/hard-safety-rules.md) — Self-created only, verify before deleting, never touch shared caches.
- [Mandatory Pre-Removal Checks](./worktree-and-artifact-cleanup/mandatory-pre-removal-checks.md) — The five checks before any `git worktree remove`.
- [Branch Cleanup](./worktree-and-artifact-cleanup/branch-cleanup.md) — Deleting merged local and remote branches safely.
- [Build-Artifact Cleanup](./worktree-and-artifact-cleanup/build-artifact-cleanup.md) — Purging plan-local build output, never shared caches.

## Related Documentation

- [Worktree Toolchain Initialization](../workflow/worktree-setup.md) — the setup half of the same lifecycle.
- [Temporary Files Convention](../infra/temporary-files.md) — the build-artifact and temporary-file taxonomy.
- [No Destructive Git Operations Convention](../workflow/no-destructive-git-operations.md) — the forbidden-op set this gate stays within.
- [File-Touch Discipline](../practice/file-touch-discipline.md) — distinguishes a plan's own artifacts from another actor's.
- [Git Push Safety Convention](../workflow/git-push-safety.md) — the remote-side companion; branch deletion is gated here, not there.
- [Build-Artifact Sweeper Convention](../infra/build-artifact-sweeper.md) — the environment-side counterpart that runs on its own schedule.
- [Agent Workflow Orchestration Convention](../agents/agent-workflow-orchestration.md) — cleanup is the DAG's terminal node.
