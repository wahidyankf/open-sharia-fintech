---
name: pr-review
title: "pr-review"
description: "Run one explicitly requested semantic PR-review pass and post one consolidated COMMENT review."
when_to_use: "Use only when a user explicitly requests one semantic review pass for an open pull request."
goal: "Review one pinned pull-request head through risk-routed specialists and publish one stale-safe consolidated review"
termination: "Return after one consolidated review post, or return stale/failed without retrying"
inputs:
  - name: pr
    type: string
    description: PR number or URL identifying the open pull request
    required: true
  - name: probe-class
    type: string
    description: Optional semantic angle supplied by an explicit caller or enclosing cycle
    required: false
    default: general
  - name: prior-review-state
    type: string
    description: Authenticated settled findings to deduplicate; empty for an independent pass
    required: false
    default: empty
  - name: delegated-gate-ids
    type: string
    description: Exact lifecycle-owned predicates supplied by a caller; empty suppresses nothing
    required: false
    default: empty
  - name: lifecycle-evidence
    type: string
    description: Caller-supplied lifecycle evidence carried unchanged; this workflow never waits for it
    required: false
    default: empty
  - name: leak-review-evidence
    type: string
    description: Authenticated current-head ose-pr-leak-review:v1 evidence, or pending
    required: false
    default: pending
outputs:
  - name: final-status
    type: enum
    values: [clean, findings, stale, failed]
    description: Terminal result of this single pass
  - name: reviewed-head
    type: string
    description: Pinned head SHA used by every reviewer and line anchor
  - name: review-id
    type: string
    description: GitHub review ID, or null when no review was posted
  - name: severity-counts
    type: string
    description: Counts for critical, high, medium, and low findings
  - name: pass-record
    type: string
    description: Authenticated ose-pr-review-pass:v1 record, or null when posting did not occur
---

# Single-Pass PR Review Workflow

Run one semantic review only when the user explicitly asks. It reviews every change type, including
prose, governance, and plans. It never classifies eligibility, fixes findings, waits for CI,
retries, or decides merge readiness.

[`pr-review-scout-maker`](../../../.claude/agents/pr-review/pr-review-scout-maker.md) pins base/head,
selects a risk route, and builds shared context. Selected specialists review concurrently;
[`pr-review-synthesis-maker`](../../../.claude/agents/pr-review/pr-review-synthesis-maker.md)
deduplicates and posts exactly one GitHub `COMMENT` review. A trivial route still gets a generalist
synthesis pass. `pr-review-fixer` never participates.

## Contents

- [Execution](./pr-review/execution.md) — Defines pinned-head routing, fan-out, synthesis, and
  posting. Use when running or implementing a single semantic pass.
- [Evidence and Outcomes](./pr-review/evidence-and-outcomes.md) — Defines pass authentication,
  terminal states, and no-retry rules. Use when posting or consuming a pass result.
- [Success Criteria](./pr-review/success-criteria.md) — Defines clean, findings, and stale scenarios.
  Use when validating the workflow's observable behavior.

`clean` describes this pass only. It is not approval or a merge gate.

## Example Usage

```text
Run one pr-review pass for PR 412.
```

## Related Workflows

- [`pr-review-cycle`](./pr-review-cycle.md) — optional iterative composition with a fixer and CI.
- [`pr-quality-gate.yml`](../../../.github/workflows/pr-quality-gate.yml) — independent default
  automated integration gate.
