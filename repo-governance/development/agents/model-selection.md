---
title: "AI Agent Model Selection Convention"
description: "Standards for selecting the appropriate model tier (planning-grade, execution-grade, fast) for AI agents based on task complexity"
category: explanation
subcategory: development
tags:
  - ai-agents
  - model-selection
  - standards
  - development
created: 2026-04-03
when_to_use: Use when deciding which model tier a new or existing agent should declare, or translating a tier to a concrete model ID.
---

# AI Agent Model Selection Convention

This document defines the standards for selecting the appropriate model tier when creating or updating AI agents. The governing principle is **match model capability to task complexity** -- use the most capable model only when the task demands it, and use lighter models for structured or mechanical work.

## Foundations

- [Principles Implemented/Respected](./model-selection/principles-implemented-respected.md) — principle list.
- [Conventions Implemented/Respected](./model-selection/conventions-implemented-respected.md) — sibling conventions.
- [Purpose](./model-selection/purpose.md) — why tiers exist.
- [Scope](./model-selection/scope.md) — what's covered.

## Model Tiers

- [Planning-Grade (Inherit / No Model Specified)](./model-selection/model-tiers-planning-grade.md) — budget-adaptive tier.
- [Execution-Grade](./model-selection/model-tiers-execution-grade.md) — sonnet tier.
- [Fast](./model-selection/model-tiers-fast.md) — haiku tier.
- [Model Selection Decision Tree](./model-selection/model-selection-decision-tree.md) — the decision tree.
- [Justification Requirement](./model-selection/justification-requirement.md) — the required block.

## Comparisons and Mistakes

- [Tier Comparison Summary](./model-selection/tier-comparison-summary.md) — side-by-side table.
- [Common Mistakes](./model-selection/common-mistakes.md) — mistakes to avoid.
- [Current Model Versions (April 2026)](./model-selection/current-model-versions.md) — version strings.

## Platform Bindings and Special Cases

- [Platform Binding Examples](./model-selection/platform-binding-examples.md) — `Claude Code`, `Cursor` mappings.
- [Special Considerations — Borderline Cases and Tier Assignments](./model-selection/special-considerations-borderline-and-tier-cases.md) — edge cases.
- [Special Considerations — Link Fixer as Fast-Tier](./model-selection/special-considerations-link-fixer.md) — link-fixer case.
- [Tools and Automation](./model-selection/tools-and-automation.md) — validation tools.
- [References](./model-selection/references.md) — further reading.
