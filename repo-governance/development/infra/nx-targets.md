---
title: "Nx Target Standards"
description: Standardized Nx target definitions for apps and libs in the monorepo
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when defining, naming, or auditing Nx targets in a project's project.json.
---

# Nx Target Standards

Standard Nx targets for apps and libs, and the naming rules that keep them consistent.

## Execution, Naming, and Foundations

- [Execution Model](./nx-targets/01-execution-model.md) — Pre-push/PR gate flow and CRON tiers. Use to trace execution order.
- [Principles and Conventions Implemented/Respected](./nx-targets/02-principles-and-conventions.md) — Principles the scheme implements. Use to cite a rule's rationale.
- [Canonical Target Reference (Lifecycle Targets)](./nx-targets/03-target-naming-canonical-names.md) — build–test:e2e reference table. Use before adding a lifecycle target.
- [Canonical Target Reference (E2E and Utility Targets)](./nx-targets/04-target-naming-canonical-names-e2e-and-utility.md) — test:e2e:ui–clean reference table. Use before adding an E2E/utility target.
- [Naming Rules](./nx-targets/05-target-naming-rules.md) — dev/start/test:\* naming rules. Use when naming a target.
- [`{domain}:{work}` Naming for Governance and Validation Targets](./nx-targets/06-domain-work-naming-for-governance-targets.md) — Naming scheme for governance targets. Use when adding one.
- [Formatting and File-Type Linting (lint-staged, not Nx targets)](./nx-targets/07-formatting-and-file-type-linting.md) — Why these are lint-staged, not targets. Use when adding a file check.

## Tag Convention

- [Tag Convention — Four-Dimension Scheme](./nx-targets/08-tag-convention-four-dimension-scheme.md) — Four tag dimensions and special rules. Use when tagging a new project.
- [Tag Convention — Tags, Examples, and Anti-Patterns](./nx-targets/09-tag-convention-current-tags-and-examples.md) — Per-project tags, examples, anti-patterns. Use to copy an existing tag set.

## Mandatory Targets by Project Type

- [Mandatory Targets — Summary Matrix](./nx-targets/10-mandatory-targets-summary-matrix.md) — Real vs. echo targets, by type. Use for a quick per-type check.
- [Mandatory Targets — Mandatory-Six and Required-Where-Applicable Targets](./nx-targets/11-mandatory-targets-all-projects-six-and-required.md) — Always-required and conditional targets. Use when scaffolding project.json.
- [Mandatory Targets — test:quick Composition and Gate-Surface Rule](./nx-targets/12-mandatory-targets-all-projects-quick-and-gate.md) — The 5-step test:quick chain. Use when wiring test:quick.
- [Mandatory Targets — Type, Build, Server, and Unit-Test Requirements](./nx-targets/13-mandatory-targets-type-build-server-unit.md) — typecheck/build/dev/start/unit conditions. Use to check which apply.
- [Projects with Integration Tests](./nx-targets/14-mandatory-targets-integration-tests.md) — Docker+PostgreSQL vs. mocking patterns. Use when writing test:integration.
- [Mandatory Targets — CLI and E2E Test Projects](./nx-targets/15-mandatory-targets-cli-e2e.md) — run/install and E2E-runner requirements. For CLI or \*-e2e projects.
- [Specs:Behavior:Coverage Projects](./nx-targets/16-mandatory-targets-specs-behavior-coverage.md) — Command flags, per-project status. Use when debugging this target.
- [Accessibility Testing](./nx-targets/17-mandatory-targets-accessibility-testing.md) — Static a11y lint plus axe-core E2E. Use when adding a11y coverage.

## Caching, Build Output, and Codegen

- [Workspace Defaults, Caching, and Build Output](./nx-targets/18-workspace-defaults-caching-build-output.md) — targetDefaults, caching table, output dirs. Use when setting cache/output config.
- [Cache and Inputs Convention — Canonical Inputs](./nx-targets/19-cache-and-inputs-convention-canonical.md) — Why explicit inputs matter, per language. Use when declaring a target's inputs.
- [Cross-Repo rhino-cli Byte-Identity Standard](./nx-targets/20-cache-cross-repo-byte-identity.md) — Rules holding rhino-cli byte-identical cross-repo. Use when changing apps/rhino-cli.
- [Codegen Dependency Chain](./nx-targets/21-codegen-dependency-chain.md) — codegen → typecheck/build dependsOn chain. Use when wiring contract codegen.

## Anti-Patterns and Traceability

- [Anti-Patterns — Echo Placeholders](./nx-targets/22-anti-patterns-echo-placeholders.md) — Echo placeholders are required, not anti-patterns. Use when a project lacks real integration/E2E tests.
- [Target Anti-Patterns](./nx-targets/23-target-anti-patterns.md) — Catalog of target-definition mistakes. Use when reviewing a project.json.
- [Principles Traceability](./nx-targets/24-principles-traceability.md) — Maps decisions to principles. Use to cite a principle in a rationale.
