---
title: "Specs Quality Gate — Steps: Initial Validation and Fixes"
description: "Documents steps 1-3 of the specs-quality-gate loop: initial specs-checker validation, the findings threshold decision, and applying specs-fixer fixes by mode."
when_to_use: "Use when tracing exactly what happens in the first half of a specs-quality-gate check-fix cycle, before re-validation."
---

# Steps — Initial Validation and Fixes

## 0. Lifecycle Validation Filter

Apply [Lifecycle Validation Ownership](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md)
before composing checker prompts. Pass Step 0's `delegated-gate-ids` and `lifecycle-evidence` to
checker and fixer invocations; delegated predicates cannot become findings or enter the fix loop.
Retain narrative, domain, cross-folder, diagram-semantic, and implementation-alignment judgment.

## 1. Initial Validation (Sequential)

Run specs-wide consistency check to identify all issues.

**Agent**: `specs-checker`

- **Args**: `folders: {input.folders}, EXECUTION_SCOPE: specs,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{audit-report-1}` — Initial audit report in `local-tmp/specs/`
  (4-part format: `specs__{uuid-chain}__{timestamp}__audit.md`)

**UUID Chain Tracking**: Checker generates 6-char UUID and writes to
`local-tmp/.execution-chain-specs` before validation.
See [Temporary Files Convention](../../../development/infra/temporary-files/uuid-chain-generation.md#uuid-generation).

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.

## 2. Check for Findings (Sequential)

Analyze audit report to determine if fixes are needed.

**Condition Check**: Count findings based on mode level in `{step1.outputs.audit-report-1}`

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Report but don't block success

- **lax**: HIGH/MEDIUM/LOW reported, not counted
- **normal**: MEDIUM/LOW reported, not counted
- **strict**: LOW reported, not counted
- **ocd**: All findings counted

**Decision**:

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the
  first zero), proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

## 3. Apply Fixes (Sequential, Conditional)

Apply validated fixes from the audit report based on mode level.

**Agent**: `specs-fixer`

- **Args**: `report: {step1.outputs.audit-report-1}, folders: {input.folders}, approved: all,
mode: {input.mode}, EXECUTION_SCOPE: specs,
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{fixes-applied}`, `{updated-lifecycle-evidence}` after intersecting changed files
  with delegated scopes
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
- A skipped fixer carries Step 0 lifecycle evidence forward unchanged
