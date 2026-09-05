---
title: "5. Re-validate (Sequential)"
description: "Step 5: re-runs pdf-to-md-checker after fixes to confirm resolution, including scoped re-validation and the carry-forward audit for zero-applied-fix iterations."
when_to_use: "Use when implementing or debugging the re-validation step, especially the scoped-scan and carry-forward-audit behaviour."
---

# 5. Re-validate (Sequential)

Run the checker again to verify fixes resolved issues and no new issues were introduced.

**Agent**: `pdf-to-md-checker`

- **Args**: `pdf-file: {input.pdf-file}, md-file: {input.md-file}, EXECUTION_SCOPE: pdf-to-md,
uuid-chain: {previous-uuid-chain}, delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step4.outputs.updated-lifecycle-evidence if step4 ran; otherwise
step0.outputs.lifecycle-evidence}`. Add
  `fix-report: {step4.outputs.pdf-to-md-fix-report-N}` only when Step 4 ran.
- **Output**: `{pdf-to-md-report-N}` — re-validation audit report
- **Depends on**: Step 3 completion (when confirming a first-zero pass) or Step 4 completion
  (when verifying fixes were applied correctly)

**Re-validation mode**: The UUID chain signals re-validation mode to the checker. When called
after Step 4, the fix report provides the changed sections list — checker validates only changed
sections and reuses the iteration 1 full-document scan scope for unchanged sections. When called
directly from Step 3 (zero-findings confirmation path), no fix report is provided and the checker
re-validates the full document.

**Empty `changed_sections` case**: When the preceding fixer ran with `Applied (HIGH_CONFIDENCE): 0`,
the fix report's `Changed Sections` list is empty. The checker writes a thin **carry-forward audit**
that references the prior audit by UUID and reproduces its findings verbatim — no re-scan. This
satisfies the per-iteration audit requirement at zero scan cost when the fixer's outcome is
deterministically a no-op.

**Success criteria**: Checker completes and generates re-validation audit report.

**On failure**: Terminate workflow with status `fail`.

**Notes**:

- Loads `local-tmp/.known-false-positives.md` skip list before validating
- Scoped re-validation (changed sections only) on iterations where fixes were applied
- Full re-validation when confirming a zero-findings pass with no preceding fix step
- Carry-forward audit (no re-scan) when `changed_sections` is empty after a zero-applied fixer iteration
