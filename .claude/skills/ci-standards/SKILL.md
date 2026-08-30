---
name: ci-standards
description: CI/CD standards knowledge for validating project compliance with CI conventions
context: inline
---

# CI Standards

Inline skill providing CI/CD standards knowledge from the governance documentation. Used by `ci-checker` and `ci-fixer` agents to validate compliance.

## Reference Documents

- [CI/CD Conventions](../../../repo-governance/development/infra/ci-conventions.md) — Central CI conventions reference
- [Three-Level Testing Standard](../../../repo-governance/development/quality/three-level-testing-standard.md) — Test level definitions
- [Nx Target Standards](../../../repo-governance/development/infra/nx-targets.md) — Mandatory targets per project type
- [Specs Directory Structure Convention](../../../repo-governance/conventions/structure/specs-directory-structure.md) — Canonical path patterns for specs/ directory

## Mandatory Nx Targets Per App Type

| App Type         | Required Targets                                                                                  |
| ---------------- | ------------------------------------------------------------------------------------------------- |
| Demo-be backend  | codegen, typecheck, lint, build, test:unit, test:quick, test:integration, specs:behavior:coverage |
| Demo-fe frontend | codegen, typecheck, lint, build, test:unit, test:quick, specs:behavior:coverage                   |
| Fullstack app    | codegen, typecheck, lint, build, test:unit, test:quick, test:integration, specs:behavior:coverage |
| CLI app (F#)     | typecheck, lint, build, test:unit, test:quick, test:integration, specs:behavior:coverage          |
| Content platform | typecheck, lint, build, test:unit, test:quick, test:integration, specs:behavior:coverage          |
| Library          | lint, build, test:unit, test:quick                                                                |
| E2E runner       | lint, test:e2e, test:e2e:ui, specs:behavior:coverage                                              |

Required-target lists name Nx targets that must exist, not necessarily distinct test scopes: for
`rhino-cli`, `test:unit` and `test:integration` both exist as required, but
`test:integration` — a single-scenario F# suite (`Steps/PreCommitHookSteps.fs`) — is not wired
into any CI job for this app, so it never runs outside a local
`nx run rhino-cli:test:integration` invocation. See [Per-Backend and CLI App Implementation
Patterns](../../../repo-governance/development/quality/three-level-testing-standard/per-backend-and-cli-app-implementation-patterns.md).

## Coverage Thresholds

| Threshold | Projects                                   |
| --------- | ------------------------------------------ |
| 90%       | organiclever-be, CLI apps                  |
| 80%       | Content platforms (ayokoding-www, ose-www) |
| 70%       | organiclever-app-web                       |

## Docker Setup Requirements

Every app with a `dev` or `test:integration` target must have:

- `infra/dev/{app}/docker-compose.yml` — Dev environment
- `infra/dev/{app}/docker-compose.ci.yml` — CI overlay (backends only)
- `infra/dev/{app}/.env.example` — Environment variable template
- `apps/{app}/docker-compose.integration.yml` — Integration tests (backends only)

## E2E Pairing Rules

| Variant Type | Pairs With                      |
| ------------ | ------------------------------- |
| Backend      | Corresponding frontend via E2E  |
| Frontend     | Corresponding backend via E2E   |
| Fullstack    | Self-contained (own API routes) |

## Gherkin Consumption Mandate

All testable projects must consume Gherkin specs at ALL test levels. Unit tests are a superset of Gherkin — they MUST implement ALL Gherkin scenarios plus additional non-Gherkin tests.

## Workflow Requirements

Each demo backend/frontend must have a per-variant test workflow (`test-{app-name}.yml`) calling reusable workflows with CRON schedule (2x daily at WIB 06:00 and 18:00).

## Quality-Gate Lifecycle Handoff

When the CI quality gate provides `delegated-gate-ids` and an evidence ledger, audit the standards
and declarations but omit exact registry-owned predicates or those connected through `verifies`.
Preserve pending state; never execute, imitate, revalidate, or fix delegated work. See the
[lifecycle ownership policy](../../../repo-governance/workflows/meta/workflow-identifier/check-fix-lifecycle-validation-ownership.md).
Fixers invalidate evidence whose registered scope intersects their changed files.
