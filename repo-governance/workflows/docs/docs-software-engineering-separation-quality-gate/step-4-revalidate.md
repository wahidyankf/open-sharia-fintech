---
description: "Step 4: re-runs the checker to verify fixes resolved issues and no new issues were introduced."
when_to_use: "Use when implementing or debugging the re-validation step."
---

# 4. Re-validate (Sequential)

Run checker again to verify fixes resolved issues and no new issues introduced.

**Agent**: `docs-software-engineering-separation-checker`

- **Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step3.outputs.updated-lifecycle-evidence}`
- **Output**: `{audit-report-N}` - Verification audit report
- **Depends on**: Step 3 completion

**Success criteria**: Checker completes validation.

**On failure**: Terminate workflow with status `fail`.
