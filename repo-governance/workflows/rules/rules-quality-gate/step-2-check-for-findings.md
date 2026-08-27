---
title: "Step 2: Check for Findings"
description: Counts retained deterministic and AI-only domain findings without mixing in delegated lifecycle evidence.
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

These thresholds apply to retained deterministic domain findings and AI-only findings. Delegated
lifecycle predicates never enter the domain finding count.

- **lax**: HIGH/MEDIUM/LOW reported, not counted
- **normal**: MEDIUM/LOW reported, not counted
- **strict**: LOW reported, not counted
- **ocd**: All findings counted

Layer-coherence and traceability preflight findings count because this workflow owns them.
Lifecycle evidence is reported in its separate ledger and status.

**Decision**:

- If threshold-level findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If threshold-level findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the
  first zero), proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

**Notes**:

- Fix scope determined by mode level
- Below-threshold findings remain visible in audit reports
- Enables progressive quality improvement
