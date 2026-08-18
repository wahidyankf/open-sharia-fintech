---
title: "Steps 5-7: Iteration Control, Final Validation, and Finalization"
description: Documents the loop-continuation logic, the final confirmation check, and the finalization step that reports status for the general quality gate.
when_to_use: Use when determining whether a run should continue iterating, running the final confirmation check, or reporting final status.
---

# Steps 5-7: Iteration Control, Final Validation, and Finalization

## 5. Iteration Control (Sequential)

Determine whether to continue fixing or move to finalization.

**Logic**:

- Re-run all checkers (step 1) to get fresh reports
- Count ALL findings (CRITICAL, HIGH, MEDIUM, LOW) across all new reports
- Track `consecutive_zero_count` across iterations (resets to 0 when findings > 0, increments when findings = 0)
- If consecutive_zero_count >= 2 AND iterations >= min-iterations (or min not provided): Proceed to step 6 (Final Validation — double-zero confirmed)
- If consecutive_zero_count >= 2 AND iterations < min-iterations: Loop back to step 1 (re-validate)
- If consecutive_zero_count < 2 AND findings = 0: Loop back to step 1 (confirmation check — no fix needed, just re-verify)
- If findings > 0 AND max-iterations provided AND iterations >= max-iterations: Proceed to step 6 with status `partial`
- If findings > 0 AND (max-iterations not provided OR iterations < max-iterations): Loop back to step 3

**Depends on**: Step 4 completion

**Notes**:

- **Default behavior**: Runs up to 7 iterations (default max-iterations). Override with higher value for more attempts
- **Consecutive pass requirement**: Zero findings must be confirmed by a second independent check before declaring success
- **Optional min-iterations**: Prevents premature termination before sufficient iterations
- Each iteration gets fresh validation reports across all four validators
- Tracks iteration count and finding trends

## 6. Final Validation (Sequential)

Run all checkers one final time to confirm zero issues remain.

**Agents**: All checkers in parallel

- apps-ayokoding-www-general-checker
- apps-ayokoding-www-facts-checker
- apps-ayokoding-www-link-checker

**Args**: `scope: {input.scope}, expect: zero-issues`

**Output**: Final audit reports for all dimensions

**Success criteria**: All checkers report zero issues of ANY confidence level.

**On failure**: Set status to `partial`.

**Depends on**: Step 5 completion

## 7. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{iterations-completed}`, all final reports

**Status determination**:

- **Success** (`pass`): Zero findings after final validation
- **Partial** (`partial`): Findings remain after max-iterations OR final validation failed
- **Failure** (`fail`): Technical errors during check, fix, or finalization

**Depends on**: Step 6 completion
