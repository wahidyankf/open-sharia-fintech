---
title: "3. Check for Findings (Sequential)"
description: "Step 3: counts checker findings by mode threshold and decides whether to proceed to fixing or to a confirmation re-check."
when_to_use: "Use when implementing or debugging the findings-threshold decision step of the quality gate."
---

# 3. Check for Findings (Sequential)

Analyze audit report to determine if fixes are needed and track convergence progress.

**Condition Check**: Count findings based on mode level in `{step2.outputs.pdf-to-md-report-N}`

**Mode-based counting**:

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Reported in audit but don't block success.

**Decision**:

- If threshold-level findings > 0: Proceed to step 4 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the
  first zero); proceed to step 5 (Re-validate) for confirmation re-check (consecutive pass
  requirement)

**Depends on**: Step 2 completion
