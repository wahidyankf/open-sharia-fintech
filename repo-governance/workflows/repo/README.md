---
title: "Repository Workflows"
description: "Orchestrated repository-level governance workflows — rules consistency, harness compatibility (parity + external drift), ose-primer content synchronization, and dependency bump planning."
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

- [Repository Rules Validation](./repo-rules-quality-gate.md) - Validate repository consistency across all layers (principles, conventions, development, agents) and apply fixes iteratively until ZERO findings. Supports four strictness modes (lax, normal, strict, ocd)
- [Harness Compatibility Quality Gate](./repo-harness-compatibility-quality-gate.md) - Validates five deterministic cross-vendor parity invariants (Phase 0) then verifies the platform-binding catalog and committed binding files still match each supported harness's current upstream conventions (Phase 1); fixes drift iteratively to double-zero.
- [Dependency Bump Planning](./repo-dependency-bump-planning.md) - Surveys every dependency manifest across the whole monorepo (`apps/`, `libs/`, workspace-root pins, `.opencode/`, `infra/` containers, and the CI toolchain pins under `.github/`), classifies each candidate bump per the Dependency Bump Stability & Safety Policy (three-path tree + Rule 5a/5b), and produces a validated **backlog** plan (via `plan-planning` with `target-stage=backlog`) that will perform the bumps. Deliverable is the plan, not the dependency edits.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model these workflows enforce
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Core Principles](../../principles/README.md) - Layer 1 governance
