---
title: "Step 6: Finalization"
description: Reports the final status (pass/partial/fail), iteration count, and final report.
when_to_use: Use when determining the workflow's terminal status after the iteration loop exits.
---

# Step 6: Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{lifecycle-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- **Success** (`pass`): Zero threshold-level findings on two consecutive validations
- **Partial** (`partial`): Findings remain after max-iterations, or fixer flagged
  out-of-scope findings requiring human resolution
- **Failure** (`fail`): Technical errors during check or fix

`final-status` describes harness compatibility only. Determine `lifecycle-status` independently:
`verified` for exact current evidence, `pending` for missing/stale evidence, and
`not-applicable` when no delegated predicate applies. Pending lifecycle evidence does not turn a
domain pass into a failure; the owning lifecycle surface still controls delivery.

**Depends on**: Reaching this step from step 2, 4, or 5
