---
title: "3. Apply Fixes (Sequential, Conditional)"
description: "Step 3: invokes docs-software-engineering-separation-fixer to add missing prerequisite statements and remove duplicated educational content."
when_to_use: "Use when implementing or debugging the fix-application step."
---

# 3. Apply Fixes (Sequential, Conditional)

Apply all validated fixes from the audit report.

**Agent**: `docs-software-engineering-separation-fixer`

- **Args**: `report: {step1.outputs.audit-report-1}, approved: all`
- **Output**: `{fixes-applied}`
- **Condition**: Findings exist from step 2
- **Depends on**: Step 2 completion

**Success criteria**: Fixer successfully applies all fixes without errors.

**On failure**: Log errors, proceed to step 4 for verification.

**Notes**:

- Fixer re-validates findings before applying (prevents false positives)
- Adds missing prerequisite statements
- Removes duplicated educational content from style guides
- Ensures docs/explanation focuses on repository-specific conventions
