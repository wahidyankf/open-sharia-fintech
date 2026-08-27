---
title: "Steps"
description: The bounded UI quality gate steps, from discovery through optional fixing, scoped verification, and finalization.
when_to_use: Use when executing or auditing the UI quality gate's step-by-step logic.
---

# Steps

## Step 0: Lifecycle Ownership Filter

Apply the
[lifecycle validation ownership policy](../../meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Record exact `delegated-gate-ids` and evidence. Delegate a UI dimension only when the registry
assigns the same predicate.

## Step 1: Discovery

**Agent**: `swe-ui-checker`

**Action**: Validate all seven dimensions (tokens, accessibility, contrast, component patterns,
dark mode, responsive design, anti-patterns), omitting exact delegated predicates.

**Args**: `quality-gate-phase: discovery, scope: {input.scope}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step0.outputs.lifecycle-evidence}`

**Output**: Audit report in `generated-reports/swe-ui__{uuid}__{timestamp}__audit.md`

Technical checker or report-generation errors go directly to Step 5 with `final-status: fail`.

## Step 2: Triage Findings

**Action**: Apply the `mode` threshold. Preserve below-threshold findings without fixing them.

**Routing**:

- Zero in-threshold findings → Go to Step 5 with `final-status: pass`
- In-threshold findings exist → Go to Step 3

## Step 3: Apply Fixes

**Agent**: `swe-ui-fixer`

**Action**: Run once. Revalidate in-threshold findings and fix those with HIGH confidence.

**Args**: Preserve `delegated-gate-ids`; never fix or re-derive delegated predicates. After edits,
invalidate only evidence whose registered scope intersects the changed files.

**Output**: `{updated-lifecycle-evidence}` plus the ordinary fix report.

**Rules**:

- Re-read each file before fixing
- Skip FALSE_POSITIVE findings
- Skip MEDIUM confidence findings (flag for manual review)
- Apply fixes from P0 through P4
- Do not invoke the fixer again during this run

If the fixer cannot complete because of a technical error, go to Step 5 with `final-status: fail`.

## Step 4: Scoped Verification

**Agent**: `swe-ui-checker`

**Action**: Run once to reproduce original in-threshold findings and smoke-test affected components
and interactions. Preserve delegation and selectively invalidated evidence. Do not repeat discovery
or expand to unrelated components.

**Args**: `quality-gate-phase: verification, original-finding-ids: {step2.outputs.in-threshold-finding-ids}, affected-components: {step3.outputs.affected-components}, delegated-gate-ids: {step0.outputs.delegated-gate-ids}, lifecycle-evidence: {step3.outputs.updated-lifecycle-evidence}`

**Routing**:

- Every original in-threshold finding resolves and smoke checks pass → Go to Step 5 with `pass`
- Any original finding remains or a smoke check exposes a regression → Go to Step 5 with `partial`
- The checker cannot complete → Go to Step 5 with `fail`

The workflow never starts another fixer or verification pass.

## Step 5: Finalization

**Action**: Carry evidence forward. Report domain status and `lifecycle-status` (`verified`,
`pending`, or `not-applicable`). Pending evidence creates no UI finding or rerun; its owner still
blocks delivery. Merge readiness requires `pass` plus `verified` or `not-applicable` lifecycle.

| Status  | Meaning                                                                  |
| ------- | ------------------------------------------------------------------------ |
| pass    | Discovery is clean, or scoped verification resolves originals cleanly    |
| partial | An original finding remains or affected-component smoke finds regression |
| fail    | A checker, fixer, or report-generation step cannot complete              |
