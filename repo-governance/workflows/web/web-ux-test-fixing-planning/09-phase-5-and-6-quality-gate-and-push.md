---
title: "Web UX Test-Fixing Planning — Phases 5 and 6: Plan Quality Gate and Push & Hand-back"
description: "The nested plan-quality-gate call that hardens the authored plan, and the final push-and-summary step that lands the plan and reports findings counts."
when_to_use: "Use when checking the plan-quality-gate args/output for this workflow, or exactly what the final push step stages and reports."
---

# Phase 5 and Phase 6 — Plan Quality Gate and Push & Hand-back

## Phase 5 — Plan Quality Gate (Nested Workflow)

**Workflow**: `plan/plan-quality-gate`

- **Args**: `scope: {plan-path}, mode: {input.mode}`
- **Output**: `{final-status}`

Iterates `plan-checker` → `plan-fixer` to double-zero at the requested mode, confirming the plan's
requirements completeness, technical clarity, and delivery-checklist executability (including the
TDD shape and specs-coverage steps).

**Success criteria**: `plan-quality-gate` returns `pass`.
**On failure**: If it returns `partial` after max-iterations, surface the residual findings to the
user before pushing.

## Phase 6 — Push & Hand-back (Sequential)

- Stage the explicit plan paths and the workflow/governance edits only (never `git add -A`; sibling
  repos carry unrelated WIP). Commit with a Conventional Commit message and push to `push-target`.
- Emit a user-visible summary: `plan-path`, `exploratory-findings-count`, `usability-findings-count`,
  `design-findings-count`, `final-status`, and a reminder that the plan is a **snapshot of the site as
  tested** — re-run all three testers if the site changes materially before the plan is executed.

**Output**: `plan-path`, `final-status`, pushed commit.
