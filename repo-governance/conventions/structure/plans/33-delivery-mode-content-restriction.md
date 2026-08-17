---
title: "Delivery Mode — main-to-origin-main Content Restriction"
description: States the two-condition test (.md-only changes or explicit standing go-ahead) that must hold before main-to-origin-main is a valid selection.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when deciding whether a plan may select main-to-origin-main as its delivery mode.
---

# Delivery Mode — main-to-origin-main Content Restriction

Continues [Delivery Mode](./32-delivery-mode-the-four-modes.md).

**`main-to-origin-main` carries a further content restriction, on top of Standard 2's
selection-signal test in the
[Git Push Default Convention](../../../development/workflow/git-push-default/04-standard-2-direct-push-modes-are-explicit-selections-not-inferred-and-are-repo-restricted.md#standard-2-direct-push-modes-are-explicit-selections-not-inferred--and-are-repo-restricted).**
An explicit selection signal (invocation argument or plan field) is necessary but not sufficient:
choosing `main-to-origin-main` is additionally valid only when **one** of two conditions holds —

1. the change set is **`.md` files only** (no source, config, spec, or generated-mirror files), or
2. the user has given **explicit, standing go-ahead** for that specific change.

Absent one of these two, use `worktree-to-pr` even if a direct-push mode would otherwise be
convenient. This restriction targets `main-to-origin-main` specifically — working directly in the
primary checkout skips both PR review and worktree isolation, so it is held to a narrower bar than
`worktree-to-origin-main`, which still isolates work from the primary checkout even though it also
skips review. The [Plan-Docs-Only Carve-Out](../../../workflows/plan/plan-planning/07-plan-docs-only-carve-out.md#the-plan-docs-only-carve-out-superseded--retired-in-ose-public)
is the plan-authoring-time instance of condition 1 above — see that section for how the two
reconcile when a plan folder's push includes non-markdown evidence files.

**This two-condition test is the general historical rule. It is now narrowed per repository by**
[Per-Repository Delivery Mode Restrictions](./35-per-repository-delivery-mode-restrictions.md#per-repository-delivery-mode-restrictions-hard-rule)
**below, which is the current binding rule** — read that subsection before relying on either
condition above.

The `*-to-pr` modes additionally run the
PR-Review Maker→Fixer Cycle (`repo-governance/workflows/pr/pr-review-quality-gate.md`) before
the PR is considered done. Selecting a `*-to-pr` mode authorizes PR steps at the plan's
**delivery boundaries** only — never at every phase, per
[PRs Open at Delivery Boundaries](./25-prs-open-at-delivery-boundaries-rules.md#prs-open-at-delivery-boundaries-not-every-phase-hard-rule), and
never at Phase 0 under any mode, per
[Phase 0 Opens No PR](./23-phase-0-opens-no-pr.md#phase-0-opens-no-pr--the-earliest-pr-is-phase-1-hard-rule).
