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
`repo-rules-maker`, `repo-rules-checker`, and `repo-rules-fixer` without replacing their atomic
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

- [rules-quality-gate](./rules-quality-gate.md) — Orchestrated quality gate that runs repo-rules-checker iteratively until zero findings, then applies fixes and re-validates. Use after changing conventions/principles/development practices, before major releases, periodically for repo health, or after adding/modifying agents.
- [rules-propagation](./rules-propagation.md) — Places newly-stated rules on the correct surface — instruction surface first, governance layers below — de-conflicting, deduplicating, and arming enforcement. Use when a decided rule must be written into the repository, or an existing rule superseded.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Core Principles](../../principles/README.md) - Layer 1 governance
