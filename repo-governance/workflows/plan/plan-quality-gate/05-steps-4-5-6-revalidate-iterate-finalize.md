---
title: "Steps 4-6 — Re-validate, Iteration Control, Finalization"
description: Describes the re-validation checker pass, the loop-continuation logic keyed on consecutive_zero_count and max-iterations, and how final status is determined.
when_to_use: Use when tracing the check-fix loop's re-validation, iteration-control, or final-status logic.
---

# Steps 4-6 — Re-validate, Iteration Control, Finalization

## 4. Re-validate (Sequential)

Run checker again to verify fixes resolved issues and no new issues introduced.

**Agent**: `plan-checker`

- **Args**: `scope: {input.scope}, uuid-chain: {previous-uuid-chain}, fix-report: {step3.outputs.fix-report}`
- **Output**: `{audit-report-N}` - Verification audit report
- **Depends on**: Step 3 completion

**Re-validation mode**: The UUID chain signals re-validation mode to the checker. The fix report provides the changed files list for scoped re-validation. The checker validates only changed plan files and reuses iteration 1's codebase inspection scope.

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.

## 5. Iteration Control (Sequential)

Determine whether to continue fixing or terminate.

**Logic**:

- Count findings based on mode level in `{step4.outputs.audit-report-N}` (same as Step 2):
  - **lax**: Count CRITICAL only
  - **normal**: Count CRITICAL + HIGH
  - **strict**: Count CRITICAL + HIGH + MEDIUM
  - **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)
- Track `consecutive_zero_count` across iterations (resets to 0 when threshold-level findings > 0, increments when = 0)
- If consecutive_zero_count >= 2 AND iterations >= min-iterations (or min not provided): Proceed to step 6 (Success — double-zero confirmed)
- If consecutive_zero_count >= 2 AND iterations < min-iterations: Loop back to step 4 (re-validate)
- If consecutive_zero_count < 2 AND threshold-level findings = 0: Loop back to step 4 (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND max-iterations provided AND iterations >= max-iterations: Proceed to step 6 (Partial)
- If threshold-level findings > 0 AND (max-iterations not provided OR iterations < max-iterations): Loop back to step 3

**Depends on**: Step 4 completion

**Notes**:

- **Default behavior**: Runs up to 7 iterations (default max-iterations). Override with higher value for more attempts
- **Consecutive pass requirement**: Zero findings must be confirmed by a second independent check before declaring success
- **Convergence target**: Workflow should stabilize in 3-5 iterations with convergence safeguards (scoped re-validation, cached verification, false positive tracking)
- **Escalation threshold**: If findings count is not monotonically decreasing after iteration 5, log a warning: "Convergence not achieved — likely non-deterministic findings or scope expansion"
- **Optional min-iterations**: Prevents premature termination before sufficient iterations
- Each iteration uses the latest audit report
- Tracks iteration count for observability

## 6. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- **Success** (`pass`): Zero findings after validation
- **Partial** (`partial`): Findings remain after max-iterations
- **Failure** (`fail`): Technical errors during check or fix

**Depends on**: Reaching this step from step 2, 4, or 5
