---
title: "Rules Workflows"
description: Orchestrated workflows for propagating and validating repository rules
when_to_use: Use when routing to a workflow that propagates or validates repository rules.
category: explanation
subcategory: workflows
tags: []
created: 2026-05-12
---

# Rules Workflows

Use these workflows when a change creates, updates, supersedes, or validates repository rules.

## Purpose

These workflows define **WHEN and HOW to place and validate repository rules**, orchestrating
`rules-maker` and `rules-checker` without replacing their atomic
responsibilities.

## Scope

**✅ Workflows Here:**

- Propagating a newly-decided rule onto the correct surface
- Repository-wide consistency validation
- Cross-layer governance checking
- Agent standards enforcement
- Iterative check-fix-verify cycles

**❌ Not Included:**

- Content quality validation (that's docs/)
- ayokoding-web content validation (that's ayokoding-web/)
- Plan validation (that's plan/)

## Workflows

- [rules-quality-gate](./rules-quality-gate.md) — Read-only governance gate producing one semantic
  verdict on a proposed or effective rule state, in `PROPOSAL` or `EFFECTIVE` mode. It never writes:
  every finding hands off to rules-propagation, the sole writer. Use when explicitly named, or when
  rules-grooming reaches its Step 8.
- [rules-grooming](./rules-grooming.md) — Recurring corpus-wide sweep that removes volume
  carrying no obligation — fragmentation overhead, cross-surface duplication, non-normative
  scaffolding, dead rules — and hands every reduction to rules-propagation to write. Never writes,
  never rewords a rule. Use when a recurrence trigger fires, not to fix one file's word budget.
- [rules-propagation](./rules-propagation.md) — Places newly-stated rules on the correct surface — instruction surface first, governance layers below — de-conflicting, deduplicating, and arming enforcement. Use when a decided rule must be written into the repository, or an existing rule superseded.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Core Principles](../../principles/README.md) - Layer 1 governance
