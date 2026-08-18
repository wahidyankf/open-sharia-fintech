---
title: "Scope"
description: "The boundary of this convention, including the plans/ exception and its Two Paths cross-reference."
category: explanation
subcategory: development
tags:
  - feature-completeness
  - specs
  - contracts
  - testing
  - documentation
  - quality
created: 2026-04-04
when_to_use: "Use when checking whether this convention's scope covers a specific directory or artifact."
---

# Scope

This convention applies to:

- All directories under `apps/`
- All directories under `libs/`
- All related artifacts in `specs/`, `docs/`, and `repo-governance/`

It does not apply to:

- `plans/` -- plan documents are intentions, not implementation artifacts, so this convention does not treat the plan files themselves as artifacts to keep in sync. **However**, per the [Two Paths](./two-paths-with-a-plan-and-without-a-plan.md) section, a plan whose scope touches `apps/`, `libs/`, or `specs/` MUST plan the companion specs/Gherkin work in its delivery checklist; a plan that omits those steps is incomplete (enforced by `plan-maker` and `plan-checker`).
- `generated-contracts/` -- auto-generated; update the source spec instead
- Governance documents that are not tied to specific features
