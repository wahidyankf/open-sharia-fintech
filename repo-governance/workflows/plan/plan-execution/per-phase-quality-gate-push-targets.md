---
title: "Per-Phase Quality Gate — Push Targets"
description: Defines the push target per delivery mode and the direct-push vs. *-to-pr branch/PR mechanics.
when_to_use: Use when deciding where a phase's changes should push to under the plan's resolved delivery mode.
---

# Per-Phase Quality Gate — Push Targets

**Continues** [Per-Phase Quality Gate — Gates](./per-phase-quality-gate-gates.md).

1. **Fix ALL failures** — including preexisting ones (Iron Rule 3)
2. Re-run failing checks to confirm resolution
3. Commit thematically (Iron Rule 7) — separate plan work from preexisting fixes
4. Push to the resolved delivery mode's target (Iron Rule 5), only after ALL local quality gates pass. The push target depends on the delivery mode resolved in Step 0:
   - **`worktree-to-origin-main` / `main-to-origin-main`** (direct-push modes): push directly to `origin main`.
   - **`worktree-to-pr`**: push the delivery unit's branch from the plan's one provisioned
     worktree. When moving to another independent unit, branch from fresh `origin/main` in that
     same worktree; do not provision another (see
     [Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule)).
   - **`main-to-pr`**: push the delivery unit's branch from the synced primary checkout. Never
     create or enter a worktree for this mode.
   - For either `*-to-pr` mode, each independent node gets one branch and one PR — strict
     **one branch → one PR → one delivery unit** mapping (see
     [Planning Granularity](../plan-planning/planning-granularity-and-one-branch-rule.md)). Open the
     PR only at the unit's declared delivery boundary. Its body is the reader's entry point and
     applies [Bounding PR Size](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-pr-size.md):
     at most 500 handwritten code/program-type additions, independently at most 1,000 handwritten
     other/document-type additions, and at most 20 hand-authored files. Claim the plan-document LOC
     exemption only for a qualifying initial establishment or backlog/in-progress pure move. At an
     intermediate phase, push for durability but open no PR, run no PR review, merge nothing, and
     skip Step 2c. Dependent phases share a delivery unit; independent nodes never do. Monitor CI
     on the PR, not `main`.
