---
description: "Step 6: reports the final status (pass/partial/fail), iteration count, and summary across all three validation dimensions."
when_to_use: "Use when implementing or debugging the workflow's final reporting step."
---

# 6. Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{lifecycle-status}`, `{iterations-completed}`, `{final-report}`

Derive `lifecycle-status` separately from the latest lifecycle evidence (`verified`, `pending`, or
`not-applicable`). It never changes domain `final-status`.

**Status determination**:

- **Success** (`pass`): Zero threshold-level findings across all validators
- **Partial** (`partial`): Findings remain after max-iterations OR broken links exist
- **Failure** (`fail`): Technical errors during check or fix

**Depends on**: Reaching this step from step 2, 4, or 5

**Notes**:

- Below-threshold findings are reported in final audit but don't prevent success status
- **Broken links always result in `partial` status** (manual intervention required)
- Generates comprehensive summary across all three validation dimensions
