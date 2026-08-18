---
title: "2. Aggregate Findings (Sequential)"
description: "Step 2: counts findings across all three reports by mode threshold and decides whether to proceed to fixing or a confirmation re-check."
when_to_use: "Use when implementing or debugging the findings-aggregation and threshold decision step."
---

# 2. Aggregate Findings (Sequential)

Analyze all audit reports to determine if fixes are needed.

**Condition Check**: Count findings based on mode level across all three reports

**Mode-Based Counting**:

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH (default)
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Reported but don't block success

- **lax**: HIGH/MEDIUM/LOW reported, not counted
- **normal**: MEDIUM/LOW reported, not counted
- **strict**: LOW reported, not counted
- **ocd**: All findings counted

**Decision**:

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the
  first zero), proceed to step 1 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

**Notes**:

- Combines findings from all three validation dimensions
- Fix scope determined by mode level
- Below-threshold findings remain visible in audit reports
- Enables progressive quality improvement
