---
title: "PR-Review Quality Gate — Loop-Exit and Block Rules"
description: "The six rules governing when the loop exits done, when it captures non-convergence learning, and when it blocks at the ceiling — including the correction-record freeze, the repeated-rejection rule, and the CI-wait rule."
when_to_use: "Use when determining whether the loop should exit, keep iterating, or block, or when writing a non-convergence learning entry."
---

# Loop-Exit and Block Rules

- **Clean exit**: after every eligible cycle's CI-green gate, evaluate unresolved
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

- **Paired-repository handoff**: when a reviewed public rule has a private counterpart, the public
  PR publishes one terminal handoff before private review. The private artifact records
  satisfaction, reasoned deviation, or one bounded correction request; a second reversal freezes
  the pair for human judgment.

- **Non-convergence learning**: at the configured ceiling, **the orchestrator** appends sanitized evidence explaining why
  convergence has not occurred to the active plan's `learnings.md` — or, for ad-hoc work with no
  owning plan, to the PR itself as a comment — and create or update a deduplicated `plans/ideas`
  entry for a systemic improvement. Never place a secret, access token,
  or copied vulnerable value in either record.
- **Ceiling block**: reaching the configured ceiling (five by default) without the
  [exit condition](./probe-variation-and-exit.md) holding is `blocked`, not `done` — whether or not a
  finding is outstanding. Never
  extend the cycle count as a substitute for resolving a finding. Extending it on the evidence of
  a [convergence checkpoint](./convergence-measurement.md) is a different act, recorded on the PR.
- **Disposition carry-forward**: `dismisses-finding` stays settled. Only `stale-cycle-only` carries
  its claim to fresh-head evaluation; an unresolved finding blocks at the ceiling.
- **CI wait discipline**: diagnose failures at root cause; a queued job is not a code defect.
