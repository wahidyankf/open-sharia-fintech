---
title: "PR-Review Cycle — Loop-Exit and Block Rules"
description: "The seven rules governing clean exit, paired delivery, non-convergence learning, and ceiling blocking — including correction-record freeze, disposition carry-forward, and CI-wait discipline."
when_to_use: "Use when determining whether the loop should exit, keep iterating, or block, or when writing a non-convergence learning entry."
---

# Loop-Exit and Block Rules

- **Clean exit**: after every pass's CI-green gate, evaluate unresolved
  [**code-related**](./what-code-related-means.md) findings — a defect in an artifact this PR ships,
  governance prose included. Zero MEDIUM/HIGH/CRITICAL findings makes the cycle clean, and the loop
  exits `done` when [two consecutive cycles under unused probe classes](./probe-variation-and-exit.md)
  are both clean; never spend a cycle merely to reach a target count. Capture LOW findings as non-blocking improvement
  work.
- **Correction-record freeze (after cycle 1)**: from cycle 2 onward the review scope excludes
  what a fixer commit wrote about the loop's own cycles. The frozen delivery outcome still allows a
  correction that completes the same evidenced defect; unrelated improvements are not smuggled
  into the fix and instead receive a reasoned reject or a linked follow-up.
  The test is authorship, not path; the PR body remains reviewable. A shipping-artifact defect is
  never suppressed.

- **Paired-repository handoff**: private scouting starts only after the public PR is merged and its
  merge SHA is reachable from public `origin/main`. The public PR then holds exactly one
  authenticated terminal handoff pinned to its final reviewed head, merge SHA, and unique private
  successor repository/branch. Missing, duplicate, conflicting, or pre-merge evidence freezes the pair.

- **Non-convergence learning**: at the configured ceiling, keep the blocked reviewed head
  immutable. The orchestrator opens one bounded `worktree-to-pr` follow-up from current
  `origin/main`, limited to sanitized evidence in the owning plan's `learnings.md` (when present),
  one deduplicated `plans/ideas` entry, and required indexes. With no owning plan, the idea carries
  the evidence. An authenticated top-level record on the blocked PR pins its final cycle, ceiling,
  reviewed head, and follow-up PR. Never place a secret or copied vulnerable value in either record.
- **Ceiling block**: reaching the configured ceiling (five by default) without the
  [exit condition](./probe-variation-and-exit.md) holding is `blocked`, not `done` — whether or not a
  finding is outstanding. Never
  extend the cycle count as a substitute for resolving a finding. Extending it on the evidence of
  a [convergence checkpoint](./convergence-measurement.md) is a different act, recorded on the PR.
- **Disposition carry-forward**: `dismisses-finding` stays settled. Only `stale-cycle-only` carries
  its claim to fresh-head evaluation; an unresolved finding blocks at the ceiling.
- **CI wait discipline**: diagnose failures at root cause; a queued job is not a code defect.
