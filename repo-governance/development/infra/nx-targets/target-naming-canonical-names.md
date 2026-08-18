---
title: "Target Naming Standards — Canonical Target Reference (Lifecycle Targets)"
description: The canonical target-name reference table for the core lifecycle and quality-gate targets (build through test:e2e), with purpose and when-required columns.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when checking whether a lifecycle or quality-gate target name already exists in the canonical vocabulary before adding a new one to project.json.
---

# Target Naming Standards — Canonical Target Reference (Lifecycle Targets)

Use these canonical names. Aliases (`serve`, `start:dev`, `unit-test`) are anti-patterns. See
[Canonical Target Reference (E2E and Utility Targets)](./target-naming-canonical-names-e2e-and-utility.md)
for the remaining targets.

| Target                    | Purpose                                                                                                                                                                                                                                                                                                      | When Required                      |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | ---------------------------------- |
| `build`                   | Produce deployable or runnable artifacts                                                                                                                                                                                                                                                                     | Compiled and bundled projects      |
| `typecheck`               | Verify type correctness without producing artifacts                                                                                                                                                                                                                                                          | Statically typed languages         |
| `lint`                    | Static analysis, code style checks, and static a11y checks (oxlint jsx-a11y for TS UI projects)                                                                                                                                                                                                              | All projects                       |
| `test:quick`              | Sequential 5-step quality gate (`typecheck` → `lint` → `test:unit` → `test:coverage` → `test:specs`); runs with `parallel: false`; enforced at pre-push, PR, and main merge. **`rhino-cli` only**: 4 steps — `test:coverage` runs in the CI Rust quality-gate job instead                                    | All projects                       |
| `specs:behavior:coverage` | Validate Gherkin feature/scenario coverage at the behavior level; every scenario exercised at the correct test level (renamed from `specs:coverage`)                                                                                                                                                         | All apps and E2E runners           |
| `specs:domain:coverage`   | Validate domain-area coverage gated by the explicit `specs.domain-areas` allowlist in `repo-config.yml` (not folder-presence)                                                                                                                                                                                | All apps                           |
| `test:specs`              | Aggregate of every `specs:*` validator for the project (`specs:structure-validation`, `specs:behavior:coverage`, `specs:domain:coverage` where in the `specs.domain-areas` allowlist; `echo` elsewhere); present on all projects; runs inside `test:quick` — replaces the separate specs-structural gate job | All projects (echo where no specs) |
| `test:unit`               | Isolated unit tests with mocked dependencies; must consume Gherkin specs; `echo` placeholder where no real unit tests exist                                                                                                                                                                                  | All projects (echo where N/A)      |
| `test:coverage`           | Native coverage gate (≥ 90% line coverage) per project via native test runner; `echo` where `test:unit` is `echo`                                                                                                                                                                                            | All projects (echo where N/A)      |
| `test:integration`        | Demo-be: real PostgreSQL via docker-compose, direct code calls (no HTTP); others: in-process mocking (MSW, Godog); `echo` placeholder where no real integration tests exist                                                                                                                                  | All projects (echo where N/A)      |
| `test:e2e`                | Real Playwright tests driving the running app over HTTP/UI — **only** on `*-e2e` projects; `echo` on all non-e2e projects; runs on scheduled CRON only (never pre-push/PR)                                                                                                                                   | All projects (echo on non-e2e)     |
