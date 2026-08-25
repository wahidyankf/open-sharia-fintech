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
   - **`worktree-to-pr` / `main-to-pr`** (`*-to-pr` modes): push to the **branch of the delivery unit being worked**. Each independent node gets its own branch and PR — a strict **one branch → one PR → one delivery unit** mapping — but shares the repo's single provisioned worktree with every other node in that repo (see [Worktree Cap](../../../conventions/structure/plans/worktree-cap.md#worktree-cap--one-worktree-per-repository-per-plan-hard-rule) and [plan-planning §Planning Granularity](../plan-planning/planning-granularity-and-one-branch-rule.md)). Moving to a new node in the same repo means branching off `origin/main` again inside the same worktree directory, not provisioning a new one. **Open the PR only when the phase just completed is the unit's delivery boundary**, as named in the plan's `### Delivery Boundaries` table (`gh pr create --base main --head <branch> --title "<plan-identifier>: <delivery unit>" --body "<summary>"`, draft or non-draft per plan/user preference). Every PR here is read by humans: write the body as a reader's entry point — what changed, why, where to start, which paths to skip — and apply [Bounding PR Size](../../../conventions/structure/plans/prs-open-at-delivery-boundaries-pr-size.md): count additions only; allow at most 500 handwritten code/program-type additions, independently allow at most 1,000 handwritten other/document-type additions, and keep at most 20 hand-authored files. Claim its narrow plan-document added-line exemption only when the entire hand-authored diff meets that convention's initial-establishment or backlog/in-progress pure-move test. For an **intermediate** phase — one inside the unit but not its boundary — push the branch for durability and stop there: open no PR, run no PR-Review Maker→Fixer Cycle, merge nothing, and skip Step 2c (no PR exists, so there is no PR CI to verify). Genuinely dependent phases share one delivery unit and therefore one PR; independent nodes never do. CI is monitored on the PR itself, not on `main` — see Step 2c.
