---
title: "Per-Phase Quality Gate — Worktree Cleanup and Boundary Assertion"
description: Defines when a repo's shared worktree may be removed, and the per-phase assertion that every declared delivery boundary actually opened a PR.
when_to_use: Use when deciding whether a repo's worktree is safe to remove, or verifying a boundary phase actually opened its PR.
---

# Per-Phase Quality Gate — Worktree Cleanup and Boundary Assertion

**Continues** [Per-Phase Quality Gate — Phase 0 Exemption and Delivery-Boundary Merging](./per-phase-quality-gate-phase0-and-boundary-merging.md).

**The worktree is the repo-granular terminal cleanup unit**: because one worktree is shared across a
repository's delivery units, never remove it after an intermediate merge. After the repository's
last delivery is confirmed, first require replacement exact-head proof where applicable, record a
passing workflow-owned terminal audit in `{final-report}`, assign `pass`, and complete every safety
check. Then remove eligible worktree, branch, and plan-local build-output classes in the same
session. A terminal-audit gap retains the worktree and reopens execution. On a multi-repository
plan, each repository reaches this terminal gate independently; it need not wait for a sibling still
in flight. See [Worktree and Artifact Cleanup](../../../development/workflow/worktree-and-artifact-cleanup.md).

1. **Assert the boundary-PR invariant, immediately after this phase's push.** If the phase just completed is a delivery unit's boundary per the plan's `### Delivery Boundaries` table, confirm a PR now exists for that unit (`gh pr list --head <branch>`) before moving on to the next phase's work. A boundary phase whose content reached the push target without ever going through `gh pr create` — for example a direct branch push under a `*-to-pr` mode — is a **plan violation** discovered here, not at archival: stop, do not start the next phase, and open the missing PR (or escalate to the user if the unit's content has already advanced past the point where opening one is straightforward). This closes the same gap `plan-execution-checker`'s archival-time check ("PRs match the declared delivery boundaries," under its Delivery Mode and PR-Review Cycle Verification step: "every declared delivery unit has a PR that merged") exists to catch, moved from plan-end to phase-boundary so a missing PR is caught in hours, not after every downstream phase has already built on top of it.

**Output**: All quality gates passing, changes pushed

**On failure**: Fix failures and retry. Do NOT proceed to next phase with failures.
