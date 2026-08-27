---
title: "Step 6: Finalization"
description: Reports the final status (pass/partial/fail), iteration count, and final report.
when_to_use: Use when determining the workflow's terminal status after the iteration loop exits.
---

# Step 6: Finalization (Sequential)

Report final status and summary.

**Output**: `{final-status}`, `{lifecycle-status}`, `{iterations-completed}`, `{final-report}`

**Status determination**:

- **Success** (`pass`): Zero threshold-level domain findings on two consecutive validations
- **Partial** (`partial`): Threshold-level domain findings remain after max-iterations
- **Failure** (`fail`): Technical errors during check or fix

`final-status` covers retained rules-domain predicates only. `lifecycle-status` is `verified`
when every applicable delegated ID has exact current evidence, `pending` when evidence is
missing/stale, and `not-applicable` when none applies. Pending does not rewrite a domain pass;
lifecycle owners remain delivery-blocking at their normal surface.

**Depends on**: Reaching this step from step 2, 4, or 5
