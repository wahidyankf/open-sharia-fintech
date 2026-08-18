---
title: "Precondition Summary and When Gates Fail"
description: The status summary an agent presents before merging, and the fix-then-re-evaluate procedure to follow when a quality gate fails.
category: explanation
subcategory: development
tags:
  - pull-request
  - merge
  - quality-gates
  - workflow
  - merge-preconditions
created: 2026-04-04
when_to_use: Use when writing the merge status summary, or when a quality gate has failed and the merge is on hold.
---

# Precondition Summary and When Gates Fail

## The Precondition Summary

When all preconditions hold, the agent presents a clear summary, then merges:

```
PR #42: feat(auth): add email validation

Quality gates:
  typecheck:     PASSED
  lint:          PASSED
  test:quick:    PASSED
  specs:coverage: PASSED
  CI workflows:  PASSED

Preconditions:
  (a) review route:      eligible, clean at cycle 2 of 7
  (b) C/H/M:             0 / 0 / 0 outstanding
  (c) branch vs main:    up to date (fast-forwarded, no rewrite)
  (d) quality gates:     all green (above)
  (e) tester gates:      run, findings resolved

Merging PR #42.
```

## When Gates Fail

If any quality gate fails, the agent must:

1. Report which gate failed and the error details.
2. Investigate the root cause.
3. Fix the issue (not bypass the gate).
4. Re-run the gates.
5. Only then re-evaluate the merge preconditions.

```
PR #42: feat(auth): add email validation

Quality gates:
  typecheck:     PASSED
  lint:          FAILED (3 errors in auth-validator.ts)
  test:quick:    PASSED
  specs:coverage: PASSED

I will investigate and fix the lint errors before merging.
```
