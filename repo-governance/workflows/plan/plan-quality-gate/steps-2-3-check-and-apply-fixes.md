---
title: "Steps 2-3 — Check for Findings and Apply Fixes"
description: Describes the finding-count condition check and the conditional plan-fixer invocation, including its decision-envelope loop.
when_to_use: Use when determining whether threshold-level findings require a plan-fixer pass, or when resolving a plan-fixer decision envelope.
---

# Steps 2-3 — Check for Findings and Apply Fixes

## 2. Check for Findings (Sequential)

Analyze audit report to determine if fixes are needed.

**Condition Check**: Count findings based on mode level in `{step1.outputs.audit-report-1}`

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Report but don't block success

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the first zero),
  proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

**Notes**:

- Fix scope determined by mode level
- Below-threshold findings remain visible in audit reports
- Enables progressive quality improvement

## 3. Apply Fixes (Sequential, Conditional)

Apply all validated fixes from the audit report.

**Agent**: `plan-fixer`

- **Args**: `report: {step1.outputs.audit-report-1}, approved: all`
- **Output**: `{fixes-applied}`
- **Condition**: Findings exist from step 2
- **Depends on**: Step 2 completion

**Success criteria**: Fixer successfully applies all fixes without errors.

**Decision-envelope loop (HARD GATE)**: If `plan-fixer` returns `## User Decisions Required`, the
root validates it against the
[canonical envelope schema](../../../development/workflow/grilling-with-options/user-decisions-required-envelope.md#user-decisions-required-envelope),
invokes `grill-me` through its native UI when available (or emits the convention's markdown fallback
to its caller), records answers by stable decision ID, and resumes or reinvokes `plan-fixer`. Repeat
until the fixer returns completed fixes without an envelope. After rendering, the root MUST
construct the canonical [Resolved User Decisions Envelope](../../../development/workflow/grilling-with-options/resolved-user-decisions-envelope.md#resolved-user-decisions-envelope)
from the original IDs and pass that payload verbatim; `plan-fixer` validates it before dependent
work. An envelope is not a failure, skipped fix, or iteration; do not advance to Step 4 while it
remains unresolved.

**On failure**: For a technical error, log it and proceed to Step 4 for verification. Never classify
a `## User Decisions Required` envelope as failure.

**Notes**:

- Fixer re-validates findings before applying (prevents false positives)
- Fixes ALL criticality levels: CRITICAL (blocking), HIGH (objective), MEDIUM (structural), LOW (style/formatting)
- Achieves perfect plan quality with zero findings
