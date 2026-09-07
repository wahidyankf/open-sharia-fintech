---
description: "Step 3: invokes docs-fixer to fix factual errors, outdated information, technical inaccuracies, and contradictions by mode."
when_to_use: "Use when implementing or debugging the factual-fix application step."
---

# 3. Apply Factual Fixes (Sequential, Conditional)

Fix factual errors, outdated information, technical inaccuracies, and contradictions.

**Agent**: `docs-fixer`

- **Args**: `report: {step1.outputs.docs-report-N}, approved: all, mode: {input.mode},
delegated-gate-ids: {step0.outputs.delegated-gate-ids},
lifecycle-evidence: {step0.outputs.lifecycle-evidence}`
- **Output**: `{factual-fixes-applied}`, `{updated-lifecycle-evidence}` after intersecting changed
  files with delegated scopes
- **Condition**: Factual findings exist from step 2
- **Depends on**: Step 2 completion

**Success criteria**: Fixer successfully applies factual fixes without errors.

**On failure**: Log errors, continue to step 4.

**Notes**:

- Re-validates findings before applying (prevents false positives)
- Uses web verification for technical claims
- **Fix scope based on mode**:
  - **lax**: Fix CRITICAL only (skip HIGH/MEDIUM/LOW)
  - **normal**: Fix CRITICAL + HIGH (skip MEDIUM/LOW)
  - **strict**: Fix CRITICAL + HIGH + MEDIUM (skip LOW)
  - **ocd**: Fix all levels (CRITICAL, HIGH, MEDIUM, LOW)
- Below-threshold findings remain untouched
- Preserves documentation intent while ensuring accuracy
