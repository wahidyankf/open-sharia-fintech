---
title: "Repository Workflows"
description: "Orchestrated repository-level governance workflows — rules consistency, harness compatibility (parity + external drift), and dependency bump planning."
when_to_use: Use when routing to a workflow that validates repository-level rules, harness compatibility, or dependency posture.
category: explanation
subcategory: workflows
tags: []
created: 2026-05-12
---

# Repository Workflows

Use these workflows when a change affects the repository as a system: its rules, generated bindings, public-template relationship, or dependency posture.

## Purpose

These workflows define **WHEN and HOW to validate and synchronize repository artifacts**, orchestrating agents for two concerns: repository rules consistency (repo-rules-checker, repo-rules-fixer) and harness compatibility including cross-vendor parity and external drift (repo-harness-compatibility-checker, repo-harness-compatibility-fixer).

## Scope

**✅ Workflows Here:**

- Repository-wide consistency validation
- Cross-layer governance checking
- Agent standards enforcement
- Iterative check-fix-verify cycles

**❌ Not Included:**

- Content quality validation (that's docs/)
- ayokoding-web content validation (that's ayokoding-web/)
- Plan validation (that's plan/)

## Workflows

- [repo-rules-quality-gate](./repo-rules-quality-gate.md) — Orchestrated quality gate that runs repo-rules-checker iteratively until zero findings, then applies fixes and re-validates. Use after changing conventions/principles/development practices, before major releases, periodically for repo health, or after adding/modifying agents.
- [repo-harness-compatibility-quality-gate](./repo-harness-compatibility-quality-gate.md) — Validates internal cross-vendor parity and external harness-conformance drift, then fixes iteratively until zero findings. Use after modifying agents, governance prose, or binding-sync logic; after a harness breaking change; or as a scheduled hygiene audit.
- [repo-dependency-bump-planning](./repo-dependency-bump-planning.md) — Surveys monorepo dependency manifests, classifies bumps per the Dependency Bump Policy, and produces a validated backlog plan — never edits a manifest itself. Use for a dependency-hygiene sweep, a pre-release bump snapshot, or an LTS-line upgrade.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Core Principles](../../principles/README.md) - Layer 1 governance
