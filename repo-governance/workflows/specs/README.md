---
title: "Specs Workflows"
description: Workflows for checking that specifications remain coherent, complete, and actionable
category: explanation
subcategory: workflows
tags: []
created: 2026-05-12
---

# Specs Workflows

Use these workflows when specifications need an independent quality pass. They check whether a spec remains coherent for people who need to understand the product as well as systems that need to validate it.

## Purpose

These workflows define **WHEN and HOW to validate specifications**, orchestrating specs-checker and specs-fixer agents to ensure structural completeness, content accuracy, internal consistency, and cross-folder coherence.

## Scope

**Workflows Here:**

- Specification structural and content validation
- Cross-spec consistency checking (shared domains, actors, terminology)
- C4 diagram accessibility and coherence
- Iterative check-fix-verify cycles with mode-based filtering

**Not Included:**

- Implementation code validation (that's per-language developer agents and CI)
- Test step definitions (that's `rhino-cli specs coverage`)
- Repository governance (that's repository/)
- Documentation quality (that's docs/)

## Workflows

- [Specs Validation](./specs-quality-gate.md) - Validate explicitly listed specs/ folders for structural completeness, content accuracy, cross-spec consistency, and C4 diagram correctness. Supports four strictness modes (lax, normal, strict, ocd)

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Three-Level Testing Standard](../../development/quality/three-level-testing-standard.md) - Testing standard that specs support
- [BDD Spec-Test Mapping](../../development/infra/bdd-spec-test-mapping.md) - How specs map to test implementations
