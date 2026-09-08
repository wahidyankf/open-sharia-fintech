---
description: Counts findings against the mode threshold and decides whether to fix or move to confirmation re-check.
when_to_use: Use when determining, from an audit report, whether the workflow proceeds to fixing or to a confirmation re-check.
---

# Step 2: Check for Findings (Sequential)

Analyze the audit report to determine if fixes are needed.

**Condition Check**: Count findings based on mode level in `{audit-report-1}`:

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Report in audit but do not block success.

**Decision**:

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is
  the first zero), proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion
