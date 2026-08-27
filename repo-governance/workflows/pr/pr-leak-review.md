---
name: pr-leak-review
title: "pr-leak-review"
description: "Run the mandatory focused leak review once for an exact current PR head."
when_to_use: "Use for every open pull request before merge and again whenever its head changes."
goal: "Detect real sensitive values, protected environment properties, and machine-specific absolute paths without broad semantic review"
termination: "Return pass/findings after one authenticated current-head review, or stale/failed without retrying inside the run"
inputs:
  - name: pr
    type: string
    description: Open PR number or URL
    required: true
outputs:
  - name: final-status
    type: enum
    values: [pass, findings, stale, failed]
    description: Focused leak-review result for the pinned head
  - name: reviewed-head
    type: string
    description: Exact PR head SHA reviewed
  - name: review-id
    type: string
    description: Authenticated GitHub review ID, or null before posting
  - name: finding-counts
    type: string
    description: Sanitized counts by leak category
  - name: evidence
    type: string
    description: Authenticated ose-pr-leak-review:v1 current-head evidence
---

# Focused PR Leak Review Workflow

Run one mandatory, narrow review for every PR's exact current head. It detects only real
secrets/private values, protected production or staging properties that belong outside git, and
real machine-specific absolute paths. It performs no broad security or semantic review, fixer
pass, CI wait, retry, or consecutive-clean confirmation.

Run [`pr-review-security-maker`](../../../.claude/agents/pr-review/pr-review-security-maker.md) in
**exact leak-only mode**. Its ordinary security charter is disabled for this invocation.

## Contents

- [Scope and Exclusions](./pr-leak-review/scope-and-exclusions.md) — Defines the three leak
  categories, exclusions, and canonical rule sources. Use when deciding whether a candidate is a
  real leak.
- [Execution](./pr-leak-review/execution.md) — Defines the pinned-head inspection and sanitized
  review phases. Use when running or implementing the focused review.
- [Evidence and Outcomes](./pr-leak-review/evidence-and-outcomes.md) — Defines authenticated
  current-head evidence and terminal states. Use when posting, authenticating, or consuming a leak
  result.
- [Success Criteria](./pr-leak-review/success-criteria.md) — Defines clean, finding, and stale
  scenarios. Use when validating the workflow's observable behavior.

Merge verification requires one authenticated `ose-pr-leak-review:v1` `pass` whose repository,
base, and head equal the PR's exact current coordinates. A changed head needs one new pass, never a
clean streak.

## Example Usage

```text
Run pr-leak-review for the exact current head of PR 412.
```

## Related Workflows

- [`pr-review`](./pr-review.md) — optional broad pass that delegates these exact predicates.
- [`pr-review-cycle`](./pr-review-cycle.md) — optional iterative workflow that consumes the same
  evidence without duplicating the scan.
