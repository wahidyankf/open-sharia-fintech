---
title: "Steps"
description: The six sequential steps of the UI quality gate's check-fix-recheck loop, from initial validation through finalization.
when_to_use: Use when executing or auditing the UI quality gate's step-by-step logic.
---

# Steps

## Step 1: Initial Validation

**Agent**: `swe-ui-checker`

**Action**: Run full validation against all seven check dimensions (token compliance, accessibility, color contrast, component patterns, dark mode, responsive, anti-patterns).

**Output**: Audit report in `generated-reports/swe-ui__{uuid}__{timestamp}__audit.md`

## Step 2: Check for Findings

**Action**: Count all findings from Step 1 report.

**Routing**:

- Zero findings → Go to Step 5 (Confirmation Check)
- Findings exist → Go to Step 3

## Step 3: Apply Fixes

**Agent**: `swe-ui-fixer`

**Action**: Process audit report, re-validate each finding, apply fixes where confidence is HIGH.

**Rules**:

- Re-read each file before fixing (may have changed)
- Skip FALSE_POSITIVE findings
- Skip MEDIUM confidence findings (flag for manual review)
- Apply fixes in priority order: P0 first, then P1, P2, P3, P4

## Step 4: Re-validate

**Agent**: `swe-ui-checker`

**Action**: Re-run validation scoped to files changed by Step 3.

**Routing**:

- Zero findings → Go to Step 5 (Confirmation Check)
- Findings remain → Check iteration count
  - Below max-iterations → Go to Step 3
  - At max-iterations → Go to Step 6 (Finalization) with status "partial"

## Step 5: Confirmation Check

**Action**: Run one more validation to confirm zero findings (double-zero confirmation).

**Routing**:

- Still zero → Go to Step 6 with status "pass"
- Findings appeared → Go to Step 3

## Step 6: Finalization

**Action**: Report final status.

| Status  | Meaning                                           |
| ------- | ------------------------------------------------- |
| pass    | Zero findings confirmed on two consecutive checks |
| partial | Some findings remain after max-iterations         |
| fail    | Critical errors that could not be resolved        |
