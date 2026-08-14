---
title: "Nx Cache Inputs Requirement"
description: "Declaring specs/ as an Nx cache input."
category: explanation
subcategory: development
tags:
  - testing
  - unit-tests
  - integration-tests
  - e2e-tests
  - bdd
  - gherkin
created: 2026-03-13
when_to_use: "Use when configuring a test target's cache inputs."
---

# Nx Cache Inputs Requirement

For Nx to invalidate cached test results when relevant files change, all `test:unit` and
`test:quick` targets must declare explicit `inputs` in `project.json` that include:

1. **Source files** — language-specific glob patterns (e.g., `{projectRoot}/src/**/*.rs`)
2. **Generated contracts** — `{projectRoot}/generated-contracts/**/*`
3. **Gherkin specs** — `{workspaceRoot}/specs/apps/<app-name>/**/*.feature` (for backends with BDD)

Without these explicit inputs, Nx may serve a cached result after a Gherkin spec is updated or
after the OpenAPI contract spec triggers a `codegen` run — causing stale test results.

Frontend apps include generated contracts in `inputs` but may use a separate spec directory path
(e.g., `specs/apps/<domain>/fe/gherkin/`).

See [Nx Target Standards](../infra/nx-targets.md) for the full canonical inputs table per language.

**Spec-coverage enforcement**: `specs:coverage` is compulsory for all apps and E2E runners.
`rhino-cli specs coverage` runs as the dedicated `specs:coverage` Nx target and is enforced
by the pre-push hook and all scheduled Test CI workflows. Projects with genuine step gaps have the
target deferred temporarily until step implementations are complete. See [Nx Target
Standards](../infra/nx-targets.md) for the full project-by-project status and command flags.
