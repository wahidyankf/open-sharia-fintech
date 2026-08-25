---
title: "Quality Gates: CRITICAL-Reproduction and Cycle Cap"
description: "Requiring reproduction for CRITICAL, and the bounded five-cycle cap."
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

# Quality-Gate Enhancements: CRITICAL-Requires-Reproduction and Bounded Cycle Cap

## CRITICAL-Requires-Reproduction

A CRITICAL-severity finding (per the [Criticality Levels Convention](.././criticality-levels.md))
must never rest on agreement-counting alone — multiple reviewers concluding the same thing is not
evidence that the thing is true. Any CRITICAL finding must carry a concrete **reproduction**:
specific inputs or state that produce the wrong output or crash, not a description of what a
reviewer believes would happen. A CRITICAL finding without a reproduction is not yet a CRITICAL
finding — it is held at a lower severity, or held for further verification under the
[Selective Adversarial Verification](./quality-gate-enhancements-selective-adversarial-verification.md) rule above when the
diff is also high-risk, until a reproduction is attached.

## Five-Cycle Maximum

For an eligible PR, the [PR Review Quality Gate
workflow](../../workflows/pr/pr-review-quality-gate.md) runs sequential CI-gated cycles only until
the target is resolution in cycles 1–3. Cycles 4–5 may use a changed focused probe only when the
remaining defect family is named. This is a convergence policy, not a target count.

If a blocking finding remains after cycle 5, stop before cycle 6, capture sanitized learning, and
ask for human direction. The ceiling is never extended automatically. LOW findings retain evidence
but are non-blocking.
