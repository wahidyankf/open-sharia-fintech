---
description: The five sequential steps of the CI quality gate's check-fix-recheck loop, from initial check through finalization.
when_to_use: Use when executing or auditing the CI quality gate's step-by-step logic.
---

# Steps

## 0. Lifecycle Ownership Filter (Sequential)

Apply the
[lifecycle validation ownership policy](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Record exact `delegated-gate-ids` and their evidence ledger. This gate continues to audit CI/CD
declarations and standards; it must not execute or imitate predicates delegated to hooks or PR CI.

## 1. Initial Check (Sequential)

Run `ci-checker` to validate non-delegated CI standards.

**Agent**: `ci-checker`

- **Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: Audit report in `local-tmp/ci/`

**Success criteria**: Checker completes and generates audit report.

**On failure**: Terminate workflow with status `fail`.

## 2. Analyze Findings (Sequential)

Count findings by criticality level.

**Condition Check**: Count ALL findings in audit report.

- If findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If findings = 0: Initialize `consecutive_zero_count` to 1 (first zero),
  proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

## 3. Apply Fixes (Sequential)

Run `ci-fixer` to address findings from the latest audit report.

**Agent**: `ci-fixer`

- **Args**: `report: {step1.outputs.audit-report}, approved: all, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: Fixed files, updated configurations
- **Condition**: Findings exist from step 2
- **Depends on**: Step 2 completion

**Success criteria**: Fixer successfully applies fixes without errors.

After edits, invalidate only lifecycle evidence whose registered scope intersects changed files and
output `{updated-lifecycle-evidence}`.

**On failure**: Log errors, proceed to step 4 for verification.

## 4. Re-check and Iterate (Sequential)

Run `ci-checker` again to verify fixes and check for new issues.

**Agent**: `ci-checker`

- **Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step3.outputs.updated-lifecycle-evidence if step3 ran; otherwise step0.outputs.lifecycle-evidence}`
- **Output**: Verification audit report
- **Depends on**: Step 2 completion and, when invoked, Step 3 completion

**Logic**:

- Count ALL findings in verification report
- Track `consecutive_zero_count` across iterations (resets to 0 when findings > 0, increments when findings = 0)
- If consecutive_zero_count >= 2: Proceed to step 5 (Success — double-zero confirmed)
- If consecutive_zero_count < 2 AND findings = 0: Loop back to step 4 (confirmation check)
- If findings > 0 AND iterations < max-iterations: Loop back to step 3
- If findings > 0 AND iterations >= max-iterations: Proceed to step 5 (Partial)
- **Escalation**: If findings count is not decreasing after iteration 5, log a warning: "Convergence not achieved — likely non-deterministic findings or scope expansion"

## 5. Finalization (Sequential)

Report final status.

- **pass**: Zero findings confirmed on two consecutive validations
- **partial**: Findings remain after max-iterations
- **fail**: Technical errors during checking or fixing

Also report `lifecycle-status` (`verified`, `pending`, or `not-applicable`) from the preserved
evidence ledger. Missing or stale evidence remains pending without a local rerun; its owner still
enforces it at the appropriate lifecycle point.
