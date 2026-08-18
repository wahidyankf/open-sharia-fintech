---
title: "4. Apply Pedagogical Fixes (Sequential, Conditional)"
description: "Step 4: invokes docs-tutorial-fixer, sequenced after docs-fixer, to fix pedagogical/tutorial-structure issues."
when_to_use: "Use when implementing or debugging the pedagogical-fix application step."
---

# 4. Apply Pedagogical Fixes (Sequential, Conditional)

Fix pedagogical issues, tutorial structure problems, narrative flow issues, and visual completeness gaps.

**Agent**: `docs-tutorial-fixer`

- **Args**: `report: {step1.outputs.tutorial-report-N}, approved: all, mode: {input.mode}`
- **Output**: `{tutorial-fixes-applied}` - Fix report with same UUID chain as source audit
- **Condition**: Tutorial findings exist from step 2
- **Depends on**: Step 3 completion

**Success criteria**: Fixer successfully applies tutorial fixes without errors.

**On failure**: Log errors, proceed to step 5.

**Notes**:

- Runs AFTER docs-fixer (sequential to avoid conflicts)
- Handles subjective tutorial issues carefully
- Only fixes objective, verifiable pedagogical issues
- Respects mode parameter for fix scoping
- Preserves educational narrative and learning objectives
