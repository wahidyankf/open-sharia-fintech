---
title: "Step 2: Check for Findings"
description: Counts AI-only findings against the mode threshold, and how deterministic preflight findings are reported but excluded from the threshold count.
when_to_use: Use when determining, from an audit report, whether the workflow proceeds to fixing or to a confirmation re-check.
---

# Step 2: Check for Findings (Sequential)

Analyze audit report to determine if fixes are needed.

**Condition Check**: Count findings based on mode level in `{step1.outputs.audit-report-1}`

- **lax**: Count CRITICAL only
- **normal**: Count CRITICAL + HIGH
- **strict**: Count CRITICAL + HIGH + MEDIUM
- **ocd**: Count all levels (CRITICAL, HIGH, MEDIUM, LOW)

**Below-threshold findings**: Report but don't block success

These below-threshold rules apply to AI-only findings; deterministic findings from preflight follow the separate visibility-only rule defined above in the Step 2 Condition Check (deterministic findings are reported in the `## Deterministic Findings (rhino-cli preflight)` section of the audit but NEVER count toward the mode threshold regardless of their criticality).

- **lax**: HIGH/MEDIUM/LOW reported, not counted
- **normal**: MEDIUM/LOW reported, not counted
- **strict**: LOW reported, not counted
- **ocd**: All findings counted

Deterministic findings (those from the rhino-cli preflight) are reported in the audit but do NOT count toward the mode threshold. They are managed via the `generated-reports/.known-false-positives.md` skip-list outside the iteration loop. Only AI-only findings count toward the mode threshold.

**Decision**:

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the
  first zero), proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

**Notes**:

- Fix scope determined by mode level
- Below-threshold findings remain visible in audit reports
- Enables progressive quality improvement
