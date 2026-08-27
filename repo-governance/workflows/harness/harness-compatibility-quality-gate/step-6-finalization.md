---
title: "Step 6: Finalization"
description: Reports the final status (pass/partial/fail), iteration count, and final report.
when_to_use: Use when determining the workflow's terminal status after the iteration loop exits.
---

# Step 6: Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- **Success** (`pass`): Zero threshold-level findings on two consecutive validations
- **Partial** (`partial`): Findings remain after max-iterations, or fixer flagged
  out-of-scope findings requiring human resolution
- **Failure** (`fail`): Technical errors during check or fix

**Depends on**: Reaching this step from step 2, 4, or 5
