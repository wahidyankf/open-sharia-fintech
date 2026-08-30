---
title: "Step 3: Apply Fixes"
description: Invokes repo-rules-fixer with mode-scoped fix levels, and notes that below-threshold findings remain untouched.
when_to_use: Use when applying validated fixes from an audit report during a repo-rules quality-gate iteration.
---

# Step 3: Apply Fixes (Sequential, Conditional)

Apply validated fixes from the audit report based on mode level.

**Agent**: `repo-rules-fixer`

- **Args**: `report: {step1.outputs.audit-report-1}, approved: all, mode: {input.mode},
EXECUTION_SCOPE: repo-rules,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {current-lifecycle-evidence}`
- **Output**: `{fixes-applied}` plus `{updated-lifecycle-evidence}` with only predicates affected
  by changed files invalidated
- **Condition**: Threshold-level findings exist from step 2
- **Depends on**: Step 2 completion

**Success criteria**: Fixer successfully applies all threshold-level fixes without errors.

**On failure**: Log errors, proceed to step 4 for verification.

**Notes**:

- Fixer re-validates findings before applying (prevents false positives)
- **Fix scope based on mode**:
  - **lax**: Fix CRITICAL only (skip HIGH/MEDIUM/LOW)
  - **normal**: Fix CRITICAL + HIGH (skip MEDIUM/LOW)
  - **strict**: Fix CRITICAL + HIGH + MEDIUM (skip LOW)
  - **ocd**: Fix all levels (CRITICAL, HIGH, MEDIUM, LOW)
- Below-threshold findings remain untouched
- Delegated lifecycle predicates are never fixer work in this invocation
- Applied fixes invalidate affected evidence; the fixer never reruns a delegated check to restore it
- A word-budget finding permits progressive disclosure or an indexed split only. Before accepting
  the fix, diff the original and surviving semantic fields: obligation, named audience, strength,
  scope, boundaries, exceptions, pass/violation conditions, and enforcement disposition. Any
  weakening, generalization, deletion, or new ambiguity is a failed fix and a HIGH domain finding.
