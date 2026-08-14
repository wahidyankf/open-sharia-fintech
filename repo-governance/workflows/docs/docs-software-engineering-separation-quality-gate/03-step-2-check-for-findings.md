---
title: "2. Check for Findings (Sequential)"
description: "Step 2: counts all findings in the audit report and decides whether to proceed to fixing or a confirmation re-check."
when_to_use: "Use when implementing or debugging the findings-threshold decision step."
---

# 2. Check for Findings (Sequential)

Analyze audit report to determine if fixes are needed.

**Condition Check**: Count ALL findings (CRITICAL, HIGH, MEDIUM) in `{step1.outputs.audit-report-1}`

- If findings > 0: Proceed to step 3 (reset `consecutive_zero_count` to 0)
- If findings = 0: Initialize `consecutive_zero_count` to 1 (this check is the first zero),
  proceed to step 4 for confirmation re-check (consecutive pass requirement)

**Depends on**: Step 1 completion

**Notes**:

- Validates NO DUPLICATION between docs/explanation and AyoKoding
- Checks prerequisite statements exist and reference AyoKoding correctly
- Validates style guide focus on repository-specific conventions only
