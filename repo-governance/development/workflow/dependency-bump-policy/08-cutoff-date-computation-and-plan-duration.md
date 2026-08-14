---
title: "Cutoff Date Computation and Plan Duration"
description: How to state the Path B cutoff date in writing, and why a plan spanning more than 60 days must re-run the eligibility check.
category: explanation
subcategory: development
tags:
  - dependencies
  - security
  - versioning
  - reproducibility
  - workflow
created: 2026-05-15
when_to_use: Use when computing the 60-day cutoff for a bump, or when a plan with dependency bumps has been open longer than 60 days.
---

# Cutoff Date Computation and Plan Duration

## Cutoff Date Computation

For every bump, the policy author MUST state the cutoff date in writing:

```
Today: <YYYY-MM-DD>
Cutoff: today − 60 days = <YYYY-MM-DD>
Eligible (Path B): versions released on or before <cutoff>
```

This ensures auditability when CVE or release dates are revisited.

## When the Plan Spans Many Days

If a plan with dependency bumps takes more than 60 days to merge, the cutoff drifts forward. Re-run the eligibility check before the final merge to catch newly-eligible versions or newly-disclosed CVEs.
