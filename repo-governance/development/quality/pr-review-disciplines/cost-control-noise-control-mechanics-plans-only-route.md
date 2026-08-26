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
when_to_use: "Use when the current PR cycle may contain only qualifying hand-authored plan artifacts."
---

# Cost/Noise Control: Plans-Only Review Route

## Route Test

Recompute this route from the current diff every cycle. It applies only when the entire
hand-authored diff consists of `plans/**` documents, their required indexes, and required
non-executable assets referenced by those documents: binary mockups, exported images, or editable
diagram/design sources under plan-local `assets/`. Executable source or scripts,
runtime/build/tool configuration or manifests, tests or fixtures, runnable prototypes,
unreferenced assets, and unrelated files force the standard route even inside a plan directory.
Use the binding ownership registry by file and region: only wholly generated files and generated
regions are ignored; vendored files and hand-authored regions participate in the test.

Record the ordinary trivial/lite/full risk tier. For `lite` and `full`, select these five
specialists plus `pr-review-synthesis-maker` as coordinator:

- `pr-review-security-maker`
- `pr-review-architecture-maker`
- `pr-review-logic-maker`
- `pr-review-docs-maker`
- `pr-review-governance-maker`

For `trivial`, select no specialists. The coordinator performs one generalist pass which runs the
primary security probe first, then covers architecture/design, domain intent and Gherkin,
documentation quality, and governance conformance. This preserves all five concerns without a
six-pass trivial review.

Record the plans-only verdict and every selected or skipped specialist in the human-readable
review-route record.

## Review Focus

Security runs the **primary mandatory probe**: whether the diff exposes real secrets, credentials,
or other values that grant access under the canonical
[system-secret boundary](../../../conventions/security/secrets-and-env-standards/hard-iron-rule-no-secrets-in-committed-files.md).
Architecture reviews architecture and design decisions made by the plan. Logic reviews domain
intent and Gherkin acceptance-criteria completeness. Documentation reviews the plan as the shipping
artifact for substantive quality and completeness. Governance reviews mechanical conformance.

Suppress findings that merely complain that eventual implementation artifacts are absent from the
plans-only PR. Later implementation correctness belongs to the PR that ships that implementation;
the plan's own architecture, domain criteria, contradictions, omissions, and rule violations remain
in scope.

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
