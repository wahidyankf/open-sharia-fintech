---
description: Workflows for checking that repository CI setup follows its documented standards
when_to_use: Use when routing to a workflow that validates or fixes CI/CD standards compliance.
---

# CI Workflows

Use these workflows when CI configuration needs a repository-wide quality pass. They distinguish the rules from the process for checking that projects follow them.

## Purpose

These workflows define **WHEN and HOW to validate CI/CD standards**, orchestrating ci-checker and ci-fixer agents to ensure all projects conform to documented CI conventions, workflow structure, and infrastructure requirements.

## Scope

**Workflows Here:**

- CI/CD standards compliance validation
- Project-level CI configuration checking
- Iterative check-fix-verify cycles with bounded iterations

**Not Included:**

- CI/CD convention definitions (that's development/infra/)
- Repository governance validation (that's repository/)
- Content quality validation (that's docs/)

## Workflows

- [ci-quality-gate](./ci-quality-gate.md) — Validates all projects conform to CI/CD standards and iteratively fixes non-compliance until zero findings are confirmed twice. Use after adding a new app, modifying CI/CD infrastructure, as a periodic compliance check, or before major releases.

## Related Documentation

- [Workflows Index](../README.md) - All orchestrated workflows
- [CI/CD Conventions](../../development/infra/ci-conventions.md) - The standards these workflows validate
- [Maker-Checker-Fixer Pattern](../../development/pattern/maker-checker-fixer.md) - Core workflow pattern
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model
