---
title: "Cost/Noise Control: Plans-Only Review Route"
description: "Defines the freshly recomputed specialist route and mandatory probes for plans-only PRs."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
  - plans
created: 2026-08-25
when_to_use: "Use when the current PR cycle may contain only hand-authored plan documents and indexes."
---

# Cost/Noise Control: Plans-Only Review Route

## Route Test

Recompute this route from the current diff every cycle. It applies only when the entire
hand-authored diff consists of `plans/**` documents and their required plan indexes. Generated
mirrors do not affect the test.

Record the ordinary trivial/lite/full risk tier, but select these three specialists plus
`pr-review-synthesis-maker` as coordinator regardless of that tier:

- `pr-review-security-maker`
- `pr-review-docs-maker`
- `pr-review-governance-maker`

Record the plans-only verdict and every selected or skipped specialist in the human-readable
review-route record.

## Review Focus

Security runs the **primary mandatory probe**: whether the diff exposes real secrets, credentials,
or sensitive operational values. Documentation reviews the plan as the shipping artifact for
substantive quality and completeness. Governance reviews its mechanical conformance to repository
rules.

Suppress findings that merely complain that eventual implementation artifacts are absent from the
plans-only PR. Later implementation correctness belongs to the PR that ships that implementation;
the plan's own contradictions, omissions, and rule violations remain in scope.

For every non-plans-only PR, security-sensitive paths still force `full` regardless of size. The
standard full-tier Content-Type Applicability Filter also remains unchanged.

## Enforcement

**Enforcement disposition — covered.** The PR-Review Quality Gate invokes a fresh
`pr-review-scout-maker` every cycle. Its review-route record exposes the ordinary tier, plans-only
verdict, primary probe, and every selected or skipped specialist.

## Related

- [Risk-Tier Fan-Out](./cost-control-noise-control-mechanics-risk-tier-fan-out.md) — standard tier
  calculation and specialist selection.
- [What Code-Related Means](../../../workflows/pr/pr-review-quality-gate/what-code-related-means.md)
  — why the plan remains a blocking shipping artifact.
