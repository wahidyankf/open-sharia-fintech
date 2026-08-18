---
title: "Step 5: Iteration Control"
description: The consecutive_zero_count logic that decides whether the workflow loops back to fix, loops back to re-validate, or terminates with success/partial.
when_to_use: Use when implementing or debugging the loop-continuation decision after a re-validation check.
---

# Step 5: Iteration Control (Sequential)

Determine whether to continue fixing or terminate.

**Logic**:

- Count findings based on mode level in `{audit-report-N+1}` (same as step 2)
- Track `consecutive_zero_count` across iterations (resets to 0 when threshold-level
  findings > 0, increments when = 0)
- If `consecutive_zero_count >= 2` AND `iterations >= min-iterations` (or min not provided):
  Proceed to step 6 (Success — double-zero confirmed)
- If `consecutive_zero_count >= 2` AND `iterations < min-iterations`: Loop back to step 4
  (re-validate)
- If `consecutive_zero_count < 2` AND threshold-level findings = 0: Loop back to step 4
  (confirmation check — no fix needed, just re-verify)
- If threshold-level findings > 0 AND `max-iterations` provided AND
  `iterations >= max-iterations`: Proceed to step 6 (Partial)
- If threshold-level findings > 0 AND (`max-iterations` not provided OR
  `iterations < max-iterations`): Loop back to step 3
- At iteration 5: emit escalation warning if not converging

**Below-threshold findings**: Continue to be reported in audit but do not affect iteration
logic.

**Depends on**: Step 4 completion
