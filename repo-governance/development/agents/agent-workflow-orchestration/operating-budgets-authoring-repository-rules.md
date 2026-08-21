---
title: "Operating Budgets — Authoring and Propagating Repository Rules"
description: "Covers the operating-budget rule for authoring and propagating repository-wide rule changes."
category: explanation
subcategory: development
tags:
  - ai-agents
  - conventions
  - development
  - workflow
  - orchestration
created: 2025-11-23
when_to_use: Use when a rule change needs to be authored and propagated across the repository, or to find the workflow that rule work enters through.
---

# Operating Budgets — Authoring and Propagating Repository Rules

These budgets bound how agents spend two scarce resources — external API rate limits and token burn — and how repository rules themselves are created and kept in sync. They apply to every agent and to the main conversation, across the OSE repositories — `ose-private` and `ose-public`.

## Authoring and Propagating Repository Rules

Rule work runs through the [repo-rules-propagation workflow](../../../workflows/repo/repo-rules-propagation.md), which is entered automatically the moment a request implies a rule is being created, updated, superseded, or deleted — however that request is phrased, and including any edit to a repo-rules surface. The workflow composes the agents rather than replacing them: `repo-rules-maker` remains the canonical maker for `repo-governance/` content, `repo-rules-checker` validates, and `repo-rules-fixer` applies validated fixes. Invoking the maker directly skips the normalization, conflict scan, placement, and enforcement-disposition steps, which is the failure this routing exists to prevent.

**Enforcement disposition — unenforced by decision.** Two mechanisms make an ad-hoc rule edit
unlikely: an agent skill that fires on rule-shaped phrasing, and a pre-write reminder that fires on
any write to a repo-rules surface. Neither _fails_. The reminder is warn-only by deliberate choice,
so that it can never deadlock the propagation workflow's own writes — and a check that cannot fail
is not coverage. A blocking variant was considered and declined; enforcement is review-time.

A rule that should hold everywhere is created with `repo-rules-maker` in one repo and then carried across the OSE repositories — via the [plan-multi-repo-parity-planning workflow](../../../workflows/plan/plan-multi-repo-parity-planning.md) when the change is planned, or an equivalent per-repo session otherwise — so the same rule text lands elsewhere rather than being retyped by hand per repo. `ose-private` receives it in real time; no other repository is a propagation target. See [Related Repositories §Sync cadence](../../../../docs/reference/related-repositories.md#sync-cadence) for the full policy and rationale.
