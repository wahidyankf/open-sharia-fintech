---
title: "The Rule"
description: "The rule: every feature change lands with all related specs, contracts, tests, and docs updated."
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
when_to_use: "Use when you need the exact wording of the feature-change-completeness rule."
---

# The Rule

**When creating, updating, or deleting features in projects, apps, or libs, you MUST also update all related artifacts in the same commit or pull request.**

The related artifacts are:

1. **Specs** -- Gherkin feature files in `specs/`
2. **Contracts** -- OpenAPI specs in `specs/apps/*/contracts/`
3. **Tests** -- Unit, integration, E2E, and accessibility tests
4. **Documentation** -- READMEs, docs/, repo-governance/, and inline documentation

A feature change is not complete until all four categories are addressed.
