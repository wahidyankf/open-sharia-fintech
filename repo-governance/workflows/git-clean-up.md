---
description: "The ordered teardown pass for one repository — pre-removal checks, worktree, branches, build output, then the local main reconcile"
when_to_use: "Use when a plan or task has finished with a repository's worktree and its Git artifacts must come down."
---

# Git Clean-Up

Teardown, in order, for one repository. Every rule this workflow applies is stated elsewhere; this
is the sequence, and the point at which it stops.

## Goal and Termination

**Goal**: Remove exactly the Git artifacts this work created, and leave the primary checkout's
`main` level with `origin/main`.

**Termination**: PASS when the worktree, both copies of every branch, and the plan's regenerable
output are gone and the divergence count reads `0 0`. RETAIN when any required proof is missing —
retention is a valid terminal state, not a failure to finish.

## Scope

The worktree this plan provisioned, the branches it opened, the regenerable build output it
produced, and the primary checkout's `main` ref. Nothing else. An artifact another actor created
stays out of scope even when it looks abandoned — see
[Hard Safety Rules](../development/workflow/worktree-and-artifact-cleanup/hard-safety-rules.md).

## Steps

1. **Confirm the terminal gate.** Every delivery unit that used the worktree is delivered, or the
   work is deliberately abandoned. Not between units: one worktree is reused for all of them under
   the [Worktree Cap](../conventions/structure/plans/worktree-cap.md).
2. **Run the pre-removal checks** — all six, before any removal:
   [Mandatory Pre-Removal Checks](../development/workflow/worktree-and-artifact-cleanup/mandatory-pre-removal-checks.md).
3. **Remove the worktree**, then `git worktree prune`.
4. **Delete the branches**, local and remote, under the proof gate:
   [Branch Cleanup](../development/workflow/worktree-and-artifact-cleanup/branch-cleanup.md), or
   [Patch-Equivalent Branch Cleanup](../development/workflow/worktree-and-artifact-cleanup/patch-equivalent-branch-cleanup.md)
   where the branch carries no change `main` lacks.
5. **Purge plan-local build output**, preserving diagnostics and shared caches:
   [Build-Artifact Cleanup](../development/workflow/worktree-and-artifact-cleanup/build-artifact-cleanup.md).
6. **Reconcile local `main`.** Choose the command by repository topology —
   [Terminal Reconcile](../development/workflow/bare-repo-landing-method/terminal-reconcile.md) —
   then prove `git rev-list --left-right --count HEAD...origin/main` reads `0 0`.

## Why the Reconcile Is Step 6

It is documented as step 8 of the
[bare-repo landing method](../development/workflow/bare-repo-landing-method.md), keyed to that
method rather than to teardown. Cleanup is where it is actually reached, and it is the step most
often missing in practice: it runs in a checkout the merge never touched, so Git reports no error
and that checkout is simply behind until somebody notices.

Naming it here does not move the rule. The command and its topology reasoning stay canonical where
they are.

## Verification

`git worktree list` no longer names the path; `git branch -a` no longer lists the branch either
locally or on `origin`; the divergence count reads `0 0`.

## Retain Rather Than Delete

An artifact belonging to an active, `partial`, or `fail` run is retained and escalated, and the
reason is stated rather than left implied. A missing proof retains the artifact; it never authorizes
a forced deletion.

## Related

- [Worktree and Artifact Cleanup](../development/workflow/worktree-and-artifact-cleanup.md) — the convention this workflow sequences.
- [Worktree Toolchain Initialization](../development/workflow/worktree-setup.md) — the provisioning half of the same lifecycle.
- [No Destructive Git Operations](../development/workflow/no-destructive-git-operations.md) — the forbidden-operation set this stays within.
