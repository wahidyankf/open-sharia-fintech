---
title: "Specs Quality Gate — Steps: Re-validate Through Termination"
description: "Documents steps 4-6 of the specs-quality-gate loop (re-validation, iteration control, finalization) and the mode-specific termination criteria for pass/partial/fail."
when_to_use: "Use when tracing how the specs-quality-gate loop decides to iterate again or terminate, or when checking the pass/partial/fail definitions per mode."
---

# Steps — Re-validate Through Termination

## 4. Re-validate (Sequential)

Run checker again to verify fixes resolved issues and no new issues introduced.

**Agent**: `specs-checker`

- **Args**: `folders: {input.folders}, delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step3.outputs.updated-lifecycle-evidence}`
- **Output**: `{audit-report-N}` — Verification audit report
- **Depends on**: Step 3 completion

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.

## 5. Iteration Control (Sequential)

Determine whether to continue fixing or terminate.

**Logic**:

- Count findings based on mode level in `{step4.outputs.audit-report-N}` (same as Step 2):
  - **lax**: Count CRITICAL only
  - **normal**: Count CRITICAL + HIGH
  - **strict**: Count CRITICAL + HIGH + MEDIUM
  - **ocd**: Count all levels
- Track `consecutive_zero_count` across iterations (resets to 0 when threshold-level findings > 0, increments when = 0)
- If consecutive_zero_count >= 2 AND iterations >= min-iterations (or min not provided):
  Proceed to step 6 (Success — double-zero confirmed)
- If consecutive_zero_count >= 2 AND iterations < min-iterations:
  Loop back to step 4 (re-validate)
- If consecutive_zero_count < 2 AND threshold-level findings = 0:
  Loop back to step 4 (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND max-iterations provided AND iterations >= max-iterations:
  Proceed to step 6 (Partial)
- If threshold-level findings > 0 AND (max-iterations not provided OR iterations < max-iterations):
  Loop back to step 3

**Below-threshold findings**: Continue to be reported in audit but don't affect iteration logic

**Depends on**: Step 4 completion

## 6. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{lifecycle-status}`, `{iterations-completed}`, `{final-report}`

Derive `lifecycle-status` separately from the latest lifecycle evidence (`verified`, `pending`, or
`not-applicable`). It never changes domain `final-status`.

**Status determination**:

- **Success** (`pass`): Zero threshold-level findings after validation
- **Partial** (`partial`): Findings remain after max-iterations
- **Failure** (`fail`): Technical errors during check or fix

**Depends on**: Reaching this step from step 2, 4, or 5

## Termination Criteria

**Success** (`pass`):

- **lax**: Zero CRITICAL findings on 2 consecutive checks (HIGH/MEDIUM/LOW may exist)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations safety limit

**Failure** (`fail`):

- Technical errors during check or fix

**Note**: Below-threshold findings are reported in final audit but don't prevent success status. Success requires two consecutive zero-finding validations (consecutive pass requirement).
