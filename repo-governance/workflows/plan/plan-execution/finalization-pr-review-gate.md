---
title: "Finalization and Archival — PR-Review Maker→Fixer Cycle Gate"
description: Defines the mandatory PR-Review Maker→Fixer Cycle gate and its four-item done-definition for *-to-pr delivery modes.
when_to_use: Use when a *-to-pr plan approaches archival and must complete its PR review cycle before merge.
---

**PR-Review Maker→Fixer Cycle gate (mandatory for `*-to-pr` modes, before archival and before the
merge)**: When the delivery mode resolved in Step 0 is `worktree-to-pr` or `main-to-pr`,
archival additionally requires the
[PR-Review Maker→Fixer Cycle](../../pr/pr-review-quality-gate.md) workflow to run to completion
against the plan's PR before any archival step below. This gate does not apply to the direct-push
modes (`worktree-to-origin-main`, `main-to-origin-main`), which carry no PR and no review cycle.

- Run the workflow's strictly sequential N-cycle loop (default **N = 3**): each cycle,
  `pr-review-scout-maker` classifies and briefs the diff, nine discipline specialists fan out, and
  `pr-review-synthesis-maker` posts one consolidated set of
  line-anchored findings against the PR's current head commit via the GitHub Reviews API, a
  `pr-review-fixer` triages and resolves every unresolved thread, and CI on the PR must be GREEN
  before the next cycle starts. See the linked workflow for the full Loop Algorithm, posting
  mechanics, and escalation rules.
- **Done-definition for `*-to-pr` modes** (all four items required):
  1. **N review cycles complete** (default 3 — a **hard ceiling**, never extended past this count)
     **and the review loop did not exit `escalated`** — an escalated exit blocks the merge on its
     own, whatever the other preconditions say.
  2. **Every inline review comment is answered** — a fix applied and pushed, or a reasoned reject,
     on every thread.
  3. **All PR quality gates are GREEN** — both the local gates (Step 2b) and CI on the PR (Step 2c),
     as of the PR's current head commit.
  4. **Archival-in-PR is committed** — see below.
- **Archival-in-PR**: for `*-to-pr` modes, the `git mv plans/in-progress/... plans/done/...` move
  (and the accompanying README index updates) is committed **inside the delivering PR itself**, as a
  normal commit on the PR branch pushed before the merge — not as a separate commit landed
  on `main` after merge. This keeps the archival move inside the same review cycle as the rest of the
  plan's changes, so the merged PR already contains the finished, archived plan.
- The merge sits **outside** this AI done-boundary: once all four done-definition items
  are satisfied, the orchestrator holds a green, fully-reviewed, archival-included PR, and the merge
  follows — "done" is not the same as "merged" (see
  [Executor Tagging](../../../conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)).
  **`[AI]` merges by default** once the hardened preconditions hold; a `[HUMAN]` merge gate applies
  only where a plan's own step says so explicitly, and the preconditions are identical either way —
  only the actor differs. See
  [Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).
  Worktree cleanup for `*-to-pr` modes happens **after** the merge completes (see the
  archival Logic below) — in contrast to the direct-push modes, where cleanup already correctly
  happens right after the push is confirmed green, because those modes have no separate merge step.
