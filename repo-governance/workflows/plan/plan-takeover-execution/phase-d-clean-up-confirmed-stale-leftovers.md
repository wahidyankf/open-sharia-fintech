---
title: "Phase D — Clean Up Confirmed-Stale Leftovers"
description: Describes the post-classification cleanup pass — the five-check pre-removal sequence, branch deletion, build-artifact scoping, and the never-remove-on-default-to-delete rule.
when_to_use: Use when removing a worktree, branch, or build artifact Phase A found that was not the Bucket-3 target Phase C adopted.
---

# Phase D — Clean Up Confirmed-Stale Leftovers (Sequential, After Every Repo Is Classified)

This phase runs only **after** Phase B has classified every candidate repo — cleaning up before
reconciliation completes risks removing evidence Phase B still needs. Bucket-4 anomalies are excluded
from this phase entirely; an anomaly is resolved with the user first and never auto-cleaned.

For every worktree/branch Phase A found that is **not** the Bucket-3 target Phase C adopted:

1. Run the full [Worktree and Artifact Cleanup Convention](../../../development/workflow/worktree-and-artifact-cleanup/mandatory-pre-removal-checks.md#mandatory-pre-removal-checks)
   five-check pre-removal sequence per candidate, without shortcuts: merge-state via
   `gh pr list --head <branch> --state all --json number,state,mergedAt` (never ancestry — squash
   merges make ancestry report false negatives), a read of the worktree's own dirty diff, an
   unpushed-commit check (`git log origin/<branch>..<branch>`), confirmation this workflow — not
   another live actor — has grounds to call it idle, and only then a non-force `git worktree remove`.
2. Branch deletion follows the same convention's [Branch
   Cleanup](../../../development/workflow/worktree-and-artifact-cleanup.md#branch-cleanup) section —
   `git branch -d` (never `-D`) locally, `git push origin --delete` remotely, and only once the check
   above confirms `MERGED` or the user has explicitly signed off on abandoning it.
3. Build-artifact cleanup is scoped to output produced **inside the removed worktree only**
   (`target/`, `dist/`, `.next/`) — never a shared cache. See the same convention's
   [Build-Artifact Cleanup](../../../development/workflow/worktree-and-artifact-cleanup/build-artifact-cleanup.md#build-artifact-cleanup)
   section and the [Build-Artifact Sweeper Convention](../../../development/infra/build-artifact-sweeper.md)
   for what the environment already reclaims on its own schedule — do not rebuild output solely to
   delete it if it is already gone.
4. `TaskCreate`/`TaskUpdate` one task per candidate, per the granularity rule stated above.
5. Log every removal (or explicit skip, with a stated reason) to the takeover-report.

A candidate this phase cannot positively confirm idle — the Cleanup Convention's fifth check, "no
positive evidence, only absence of evidence of activity" — is left in place and reported to the user,
never removed on a default-to-delete basis.
