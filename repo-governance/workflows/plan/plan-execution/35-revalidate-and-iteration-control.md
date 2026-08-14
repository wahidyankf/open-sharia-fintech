---
title: "Re-validate"
description: Defines the re-validation step and the iteration-control logic that loops execution or proceeds to finalization.
when_to_use: Use when deciding whether to loop back into execution again or proceed to finalization, based on remaining findings and iteration count.
---

# 6. Re-validate (Sequential)

Run validation again to verify findings resolved and no new issues introduced.

**Agent**: `plan-execution-checker`

- **Args**: `plan: {input.plan-path}`
- **Output**: `{audit-report-N}` — Verification validation report
- **Depends on**: Step 5 completion

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- Verifies all findings from previous report are resolved
- Checks no new issues were introduced during fixes
- Generates fresh validation report with current status

## 7. Iteration Control (Sequential)

Determine whether to continue execution or terminate.

**Logic**:

- Count ALL findings in `{step6.outputs.audit-report-N}` (CRITICAL, HIGH, MEDIUM, LOW)
- If findings = 0: Proceed to step 8 (Finalization - Success)
- If findings > 0 AND iterations < max-iterations: Loop back to step 5 with new report
- If findings > 0 AND iterations >= max-iterations: Proceed to step 8 (Finalization - Partial)

**Depends on**: Step 6 completion

**Notes**:

- Prevents infinite loops with max-iterations limit
- Continues until ZERO findings of any criticality level
- Each iteration uses the latest validation report
- Tracks iteration count for observability
