---
title: "Per-Phase Quality Gate — Worktree Cleanup and Boundary Assertion"
description: Defines when a repo's shared worktree may be removed, and the per-phase assertion that every declared delivery boundary actually opened a PR.
when_to_use: Use when deciding whether a repo's worktree is safe to remove, or verifying a boundary phase actually opened its PR.
---

# Per-Phase Quality Gate — Worktree Cleanup and Boundary Assertion

**Continues** [Per-Phase Quality Gate — Phase 0 Exemption and Delivery-Boundary Merging](./per-phase-quality-gate-phase0-and-boundary-merging.md).

**The worktree is the unit of cleanup, at repo granularity, and cleanup is immediate**: because a repo's worktree is shared across every delivery unit landed in it, it is removed only once **all** of them have their PRs merged — never when the first one does — but the moment that last merge is confirmed, remove it **directly**, in the same working session, rather than deferring to plan end or a later batch pass. Cleanup is the terminal node of the DAG and depends on every delivery node, so it can never remove a worktree an in-flight node still needs, but nothing about that dependency licenses leaving an already-idle worktree in place "for later." On a multi-repo plan, each repo's worktree is torn down independently, as soon as that repo's own units land — not held open waiting for other repos still in flight. See [Worktree and Artifact Cleanup](../../../development/workflow/worktree-and-artifact-cleanup.md).

1. **Assert the boundary-PR invariant, immediately after this phase's push.** If the phase just completed is a delivery unit's boundary per the plan's `### Delivery Boundaries` table, confirm a PR now exists for that unit (`gh pr list --head <branch>`) before moving on to the next phase's work. A boundary phase whose content reached the push target without ever going through `gh pr create` — for example a direct branch push under a `*-to-pr` mode — is a **plan violation** discovered here, not at archival: stop, do not start the next phase, and open the missing PR (or escalate to the user if the unit's content has already advanced past the point where opening one is straightforward). This closes the same gap `plan-execution-checker`'s archival-time check ("PRs match the declared delivery boundaries," under its Delivery Mode and PR-Review Cycle Verification step: "every declared delivery unit has a PR that merged") exists to catch, moved from plan-end to phase-boundary so a missing PR is caught in hours, not after every downstream phase has already built on top of it.

**Output**: All quality gates passing, changes pushed

**On failure**: Fix failures and retry. Do NOT proceed to next phase with failures.
