---
title: "6. Finalization (Sequential)"
description: "Step 6: reports the final status (pass/partial/fail), iteration count, and summary report."
when_to_use: "Use when implementing or debugging the workflow's final reporting step."
---

# 6. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{lifecycle-status}`, `{iterations-completed}`, `{final-report}`

Derive `lifecycle-status` separately from the latest lifecycle evidence (`verified`, `pending`, or
`not-applicable`). It never changes domain `final-status`.

**Status determination**:

- **Success** (`pass`): Zero findings after validation
- **Partial** (`partial`): Findings remain after max-iterations
- **Failure** (`fail`): Technical errors during check or fix

**Depends on**: Reaching this step from step 2, 4, or 5
