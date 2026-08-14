---
title: "PR-Review Quality Gate — Loop-Exit and Block Rules"
description: "The five rules governing when the loop exits done, when it captures non-convergence learning, and when it blocks at the ceiling — including the repeated-rejection and CI-wait rules."
when_to_use: "Use when determining whether the loop should exit, keep iterating, or block, or when writing a non-convergence learning entry."
---

# Loop-Exit and Block Rules

- **Earliest clean exit**: after every eligible cycle's CI-green gate, evaluate unresolved
  **code-related** findings. Zero MEDIUM/HIGH/CRITICAL findings means status `done`; do not spend an
  additional cycle merely to reach a target count. Capture LOW findings as non-blocking improvement
  work.
- **Non-convergence learning**: at cycles six and seven, append sanitized evidence explaining why
  convergence has not occurred to the active plan's `learnings.md`, and create or update a
  deduplicated `plans/ideas` entry for a systemic improvement. Never place a secret, access token,
  or copied vulnerable value in either record.
- **Ceiling block**: when the configured ceiling (seven by default) is reached with an unresolved
  code-related MEDIUM/HIGH/CRITICAL finding, status is `blocked`, not `done`; do not merge and do not
  extend the cycle count as a substitute for resolving the finding.
- **Repeated rejection block**: a reasoned reject is not an automatic resolution of a code-related
  MEDIUM/HIGH/CRITICAL finding. The next cycle must independently verify it. If it remains, the PR
  stays in the normal loop and ultimately blocks at the ceiling unless resolved with evidence.
- **CI wait discipline**: investigate code failures and fix their root cause. For queued or stalled
  jobs, first inspect runner contention across the OSE repositories, then continue patient two-minute
  polling. Do not cancel the active goal or classify a runner wait as a code defect.
