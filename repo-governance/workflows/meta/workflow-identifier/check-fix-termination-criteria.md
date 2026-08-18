---
title: "*-check-fix Workflow Pattern — Termination Criteria (Mandatory)"
description: The mandatory success/partial/failure termination criteria every *-check-fix workflow must use, by mode level.
category: explanation
subcategory: workflows
tags:
  - workflows
  - agents
  - orchestration
  - patterns
created: 2025-12-23
when_to_use: Use when writing the Termination Criteria section of a new *-check-fix workflow.
---

# \*-check-fix Workflow Pattern — Termination Criteria (Mandatory)

All \*-check-fix workflows MUST use termination criteria based on mode level:

**Success** (`pass`):

- Requires **two consecutive** zero-finding validations at the mode's threshold level (consecutive pass requirement)
- **normal**: Zero CRITICAL/HIGH findings on 2 consecutive checks (MEDIUM/LOW may exist)
- **strict**: Zero CRITICAL/HIGH/MEDIUM findings on 2 consecutive checks (LOW may exist)
- **ocd**: Zero findings at all levels on 2 consecutive checks

**Partial** (`partial`):

- Threshold-level findings remain after max-iterations safety limit

**Failure** (`fail`):

- Technical errors during check or fix

**Note**: Below-threshold findings are reported in final audit but don't prevent success status.
