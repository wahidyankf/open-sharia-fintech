---
title: "Steps"
description: The six sequential steps of the UI quality gate's check-fix-recheck loop, from initial validation through finalization.
when_to_use: Use when executing or auditing the UI quality gate's step-by-step logic.
---

# Steps

## Step 0: Lifecycle Ownership Filter

Apply the
[lifecycle validation ownership policy](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md)
before the first checker pass. Record exact `delegated-gate-ids` and their evidence ledger. Never
delegate the seven UI dimensions below unless the registry explicitly assigns the same predicate.

## Step 1: Initial Validation

**Agent**: `swe-ui-checker`

**Action**: Run validation against all seven check dimensions (token compliance, accessibility,
color contrast, component patterns, dark mode, responsive, anti-patterns), omitting only exact
delegated predicates.

**Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step0.outputs.lifecycle-evidence}`

**Output**: Audit report in `generated-reports/swe-ui__{uuid}__{timestamp}__audit.md`

## Step 2: Check for Findings

**Action**: Count all findings from Step 1 report.

**Routing**:

- Zero findings → Go to Step 5 (Confirmation Check)
- Findings exist → Go to Step 3

## Step 3: Apply Fixes

**Agent**: `swe-ui-fixer`

**Action**: Process audit report, re-validate each finding, apply fixes where confidence is HIGH.

**Args**: Preserve `delegated-gate-ids`; never fix or re-derive delegated predicates. After edits,
invalidate only evidence whose registered scope intersects the changed files.

**Output**: `{updated-lifecycle-evidence}` plus the ordinary fix report.

**Rules**:

- Re-read each file before fixing (may have changed)
- Skip FALSE_POSITIVE findings
- Skip MEDIUM confidence findings (flag for manual review)
- Apply fixes in priority order: P0 first, then P1, P2, P3, P4

## Step 4: Re-validate

**Agent**: `swe-ui-checker`

**Action**: Re-run validation scoped to files changed by Step 3, preserving the Step 0 delegation
set and using the selectively invalidated evidence ledger.

**Routing**:

- Zero findings → Go to Step 5 (Confirmation Check)
- Findings remain → Check iteration count
  - Below max-iterations → Go to Step 3
  - At max-iterations → Go to Step 6 (Finalization) with status "partial"

## Step 5: Confirmation Check

**Agent**: `swe-ui-checker`

**Action**: Run one more validation to confirm zero findings (double-zero confirmation), preserving
the Step 0 delegation set and latest selectively invalidated evidence ledger.

**Args**: `scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {latest.lifecycle-evidence}`

Missing or invalid evidence stays `pending`; the confirmation pass never reruns or re-derives its
predicate.

**Routing**:

- Still zero → Go to Step 6 with status "pass"
- Findings appeared → Go to Step 3

## Step 6: Finalization

**Action**: Carry the final evidence ledger forward. Report domain status and the separate
`lifecycle-status` (`verified`, `pending`, or `not-applicable`). Pending lifecycle evidence does not
manufacture a UI finding or trigger a local rerun; the owning lifecycle gate still blocks delivery.

| Status  | Meaning                                           |
| ------- | ------------------------------------------------- |
| pass    | Zero findings confirmed on two consecutive checks |
| partial | Some findings remain after max-iterations         |
| fail    | Critical errors that could not be resolved        |
