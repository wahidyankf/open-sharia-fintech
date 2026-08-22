---
title: "PR-Review Quality Gate — Loop-Exit and Block Rules"
description: "The six rules governing when the loop exits done, when it captures non-convergence learning, and when it blocks at the ceiling — including the correction-record freeze, the repeated-rejection rule, and the CI-wait rule."
when_to_use: "Use when determining whether the loop should exit, keep iterating, or block, or when writing a non-convergence learning entry."
---

# Loop-Exit and Block Rules

- **Earliest clean exit**: after every eligible cycle's CI-green gate, evaluate unresolved
  **code-related** findings. Zero MEDIUM/HIGH/CRITICAL findings means status `done`; do not spend an
  additional cycle merely to reach a target count. Capture LOW findings as non-blocking improvement
  work.
- **Correction-record freeze (after cycle 1)**: from cycle 2 onward the review scope EXCLUDES the
  prose the loop itself authors: `plans/**`, including `delivery.md` and `learnings.md`. On a
  plans-only PR the plan **is** the shipping surface and stays in scope every cycle. **The PR
  body is NOT frozen** — it stays in scope every cycle, because it is the human reviewer's entry
  point and a description nobody has checked since cycle 1 costs more than re-reading it does. A loop whose scope contains its own correction record
  reviews new falsifiable claims it wrote last cycle, so the surface grows about as fast as it is
  cleaned and a zero-finding cycle becomes unreachable: on PR #239 the shipping files stopped
  changing at cycle 14 while the loop ran to 19, and every finding from `C-72` onward was the record
  making a claim about itself and getting it wrong. Cycle 1 still reviews the record, so a plan
  document that misstates the change is caught once. A **factual defect in a shipping artifact**
  discovered later is never suppressed by this rule — the freeze covers the correction record, not
  the code, specs, or governance text under review.
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
