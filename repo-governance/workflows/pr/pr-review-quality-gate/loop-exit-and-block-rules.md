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
  what a fixer commit wrote about the loop's own cycles.
  The test is authorship, not path. The rule and both its carve-outs (a plans-only PR, and any security-sensitive hunk, which stays reviewable
  every cycle) are stated once in
  [Correction-Record Freeze](../../../../.claude/skills/pr-review-scout-classification/reference/correction-record-freeze.md);
  this layer does not restate them, because a second copy drifts. **The PR body is NOT frozen** —
  it is the human reviewer's entry point, and a description nobody has checked since cycle 1 costs
  more than re-reading it does.

  Why: a loop whose scope contains its own correction record reviews the claims it wrote last cycle,
  so the surface grows about as fast as it is cleaned — on PR #239 the shipping files stopped
  changing at cycle 14 while the loop ran to 19. A factual defect in a **shipping artifact** is
  never suppressed by this rule.

- **Non-convergence learning**: at cycles six and seven **the orchestrator** appends sanitized evidence explaining why
  convergence has not occurred to the active plan's `learnings.md` — or, for ad-hoc work with no
  owning plan, to the PR itself as a comment — and create or update a deduplicated `plans/ideas`
  entry for a systemic improvement. Never place a secret, access token,
  or copied vulnerable value in either record.
- **Ceiling block**: when the configured ceiling (seven by default) is reached with an unresolved
  code-related MEDIUM/HIGH/CRITICAL finding, status is `blocked`, not `done`; do not merge and do not
  extend the cycle count as a substitute for resolving the finding. Extending it on the evidence of
  a [convergence checkpoint](./convergence-measurement.md) is a different act, recorded on the PR.
- **Repeated rejection block**: a reasoned reject is not an automatic resolution of a code-related
  MEDIUM/HIGH/CRITICAL finding. The next cycle must independently verify it. If it remains, the PR
  stays in the normal loop and ultimately blocks at the ceiling unless resolved with evidence.
- **CI wait discipline**: investigate code failures and fix their root cause. For queued or stalled
  jobs, first inspect runner contention across the OSE repositories, then continue patient two-minute
  polling. Do not cancel the active goal or classify a runner wait as a code defect.
