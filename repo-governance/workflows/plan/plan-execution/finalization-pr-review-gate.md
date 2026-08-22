---
title: "Finalization and Archival — PR-Review Maker→Fixer Cycle Gate"
description: Defines the mandatory PR-Review Maker→Fixer Cycle gate and points at the workflow's route-specific done-definition for *-to-pr delivery modes.
when_to_use: Use when a *-to-pr plan approaches archival and must complete its PR review cycle before merge.
---

**PR-Review Maker→Fixer Cycle gate (mandatory for `*-to-pr` modes, before archival and before the
merge)**: When the delivery mode resolved in Step 0 is `worktree-to-pr` or `main-to-pr`,
archival additionally requires the
[PR-Review Maker→Fixer Cycle](../../pr/pr-review-quality-gate.md) workflow to run to completion
against the plan's PR before any archival step below. This gate does not apply to the direct-push
modes (`worktree-to-origin-main`, `main-to-origin-main`), which carry no PR and no review cycle.

- Run the workflow's strictly sequential loop, **ceiling N = 7**: each cycle,
  `pr-review-scout-maker` classifies and briefs the diff, the tier-selected discipline specialists
  fan out, and `pr-review-synthesis-maker` posts one consolidated set of
  line-anchored findings against the PR's current head commit via the GitHub Reviews API, a
  `pr-review-fixer` triages and resolves every unresolved thread, and CI on the PR must be GREEN
  before the next cycle starts. **N is a ceiling, not a floor**: the loop stops at the earliest
  completed cycle leaving zero code-related MEDIUM/HIGH/CRITICAL findings, and spending a further
  cycle merely to reach a target count is waste, not thoroughness. See the linked workflow for the
  full Loop Algorithm, posting mechanics, and loop-exit rules.
- **Done-definition for `*-to-pr` modes**: the workflow's own
  [Route-Specific Done-Definition](../../pr/pr-review-quality-gate/route-specific-done-definition.md)
  is normative and is not restated here — satisfy every item it lists, including archival-in-PR
  below. A loop that reaches the ceiling with a code-related MEDIUM/HIGH/CRITICAL finding
  outstanding exits `blocked`, and a `blocked` exit prevents the merge on its own, whatever the
  other preconditions say.
- **Archival-in-PR**: for `*-to-pr` modes, the `git mv plans/in-progress/... plans/done/...` move
  (and the accompanying README index updates) is committed **inside the delivering PR itself**, as a
  normal commit on the PR branch pushed before the merge — not as a separate commit landed
  on `main` after merge. This keeps the archival move inside the same review cycle as the rest of the
  plan's changes, so the merged PR already contains the finished, archived plan.
- The merge sits **outside** this AI done-boundary: once every done-definition item
  is satisfied, the orchestrator holds a green, fully-reviewed, archival-included PR, and the merge
  follows — "done" is not the same as "merged" (see
  [Executor Tagging](../../../conventions/structure/plans/executor-tagging-tags-and-bias.md#executor-tagging--ai-vs-human-hard-rule)).
  **`[AI]` merges by default** once the hardened preconditions hold; a `[HUMAN]` merge gate applies
  only where a plan's own step says so explicitly, and the preconditions are identical either way —
  only the actor differs. See
  [Delivery Mode](../../../conventions/structure/plans/delivery-mode-the-four-modes.md#delivery-mode).
  Worktree cleanup for `*-to-pr` modes happens **after** the merge completes (see the
  archival Logic below) — in contrast to the direct-push modes, where cleanup already correctly
  happens right after the push is confirmed green, because those modes have no separate merge step.
