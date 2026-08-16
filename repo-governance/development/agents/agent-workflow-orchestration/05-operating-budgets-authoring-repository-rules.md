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
when_to_use: Use when a rule change needs to be authored and propagated across the repository.
---

# Operating Budgets — Authoring and Propagating Repository Rules

These budgets bound how agents spend two scarce resources — external API rate limits and token burn — and how repository rules themselves are created and kept in sync. They apply to every agent and to the main conversation, across the OSE repositories — `ose-private` and `ose-public`.

## Authoring and Propagating Repository Rules

Repository rules and conventions are authored, maintained, and propagated using the `repo-rules-maker` agent. `repo-rules-maker` is the canonical maker for `repo-governance/` content; `repo-rules-checker` validates it and `repo-rules-fixer` applies validated fixes.

A rule that should hold everywhere is created with `repo-rules-maker` in one repo and then carried across the OSE repositories — via the [plan-multi-repo-parity-planning workflow](../../../workflows/plan/plan-multi-repo-parity-planning.md) when the change is planned, or an equivalent per-repo session otherwise — so the same rule text lands elsewhere rather than being retyped by hand per repo. `ose-private` receives it in real time; no other repository is a propagation target. See [Related Repositories §Sync cadence](../../../../docs/reference/related-repositories.md#sync-cadence) for the full policy and rationale.
