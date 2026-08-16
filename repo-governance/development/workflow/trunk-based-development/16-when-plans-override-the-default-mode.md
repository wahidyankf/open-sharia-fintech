---
title: "When Plans Override the Default Mode"
description: The three reasons a plan may declare a non-default Delivery Mode, and a worked ose-private infrastructure-as-code example.
category: explanation
subcategory: development
tags:
  - trunk-based-development
  - git
  - workflow
  - development
  - continuous-integration
created: 2025-11-26
when_to_use: Use when deciding whether a plan's change justifies overriding the worktree-to-pr default.
---

# When Plans Override the Default Mode

Specify a non-default `## Delivery Mode` field in a plan if:

- **Trivial, well-understood change**: A single-line fix or mechanical rename that does not warrant a
  review pass -- use `worktree-to-origin-main` or `main-to-origin-main`.
  **Also subject to the branch-protection axis, independent of the trivial-change rationale**:
  neither direct-push mode has an executable path in `ose-public`; both direct-push
  modes remain available only for `ose-private` infrastructure-as-code plans. See
  [Plans Organization Convention §Per-Repository Delivery Mode Restrictions](../../../conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule).
- **External integration**: Working with a third party that requires a specific branch/PR shape.
- **Compliance**: A regulatory requirement changes the review process beyond the standard PR-review
  cycle.

**Example plan overriding the default** -- recast here as an `ose-private` infrastructure-as-code
plan, the case this repo's convention treats as the only one where a direct-push mode is genuinely
sanctioned today (see the branch-protection callout above; a `worktree-to-origin-main`/
`main-to-origin-main` example targeting `ose-public` would fail this
repo's own `plan-checker` gate on sight, because neither mode has an executable path there):

```markdown
## Delivery Mode

`main-to-origin-main`

**Justification**: This `ose-private` infrastructure-as-code plan updates a single Terraform
resource tag and needs the primary checkout's local secrets/state access. The change is trivial and
well-understood; a full PR-review cycle is unnecessary overhead. Not executable in `ose-public`
-- see
[Plans Organization Convention §Per-Repository Delivery Mode Restrictions](../../../conventions/structure/plans/35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule).
```
