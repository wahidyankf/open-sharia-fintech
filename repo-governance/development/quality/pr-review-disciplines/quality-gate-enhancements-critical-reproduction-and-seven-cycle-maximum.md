---
title: "Quality Gates: CRITICAL-Reproduction and Cycle Cap"
description: "Requiring reproduction for CRITICAL, and the seven-cycle cap."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - boundary-rules
created: 2026-07-23
when_to_use: "Use when a CRITICAL finding lacks reproduction steps."
---

# Quality-Gate Enhancements: CRITICAL-Requires-Reproduction and Seven-Cycle Maximum With Early Clean Exit

## CRITICAL-Requires-Reproduction

A CRITICAL-severity finding (per the [Criticality Levels Convention](.././criticality-levels.md))
must never rest on agreement-counting alone — multiple reviewers concluding the same thing is not
evidence that the thing is true. Any CRITICAL finding must carry a concrete **reproduction**:
specific inputs or state that produce the wrong output or crash, not a description of what a
reviewer believes would happen. A CRITICAL finding without a reproduction is not yet a CRITICAL
finding — it is held at a lower severity, or held for further verification under the
[Selective Adversarial Verification](./quality-gate-enhancements-selective-adversarial-verification.md) rule above when the
diff is also high-risk, until a reproduction is attached.

## Seven-Cycle Maximum With Early Clean Exit

For an eligible PR, the [PR Review Quality Gate
workflow](../../workflows/pr/pr-review-quality-gate.md) runs sequential CI-gated cycles only until
two consecutive clean cycles under previously-unused probe classes, with seven cycles as the default
maximum. This is a convergence policy, not a target count: one clean cycle is evidence about one
question, and cycles beyond the second add cost without improving the merge decision.

If code-related MEDIUM/HIGH/CRITICAL findings remain at cycle six or seven, the execution captures
sanitized learning and a deduplicated improvement idea. At the ceiling, the PR is blocked rather
than merged or extended automatically. LOW findings retain full evidence but are non-blocking and
do not prevent the early clean exit.
