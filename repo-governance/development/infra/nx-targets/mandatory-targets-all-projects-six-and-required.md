---
title: "Mandatory Targets — Mandatory-Six and Required-Where-Applicable Targets"
description: The mandatory-six targets every registered project must declare, and the required-where-applicable targets declared only when a condition applies.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when scaffolding a new project's project.json to confirm every mandatory target is present, even as an echo placeholder.
---

# Mandatory Targets — Mandatory-Six and Required-Where-Applicable Targets

## Mandatory-Six Targets

Every direct child of `apps/` or `libs/` registered with Nx (i.e. has a `project.json`) **must declare
all six targets below**, even when the body is a no-op `echo` placeholder. This ensures
`nx affected -t <target>` covers every project uniformly with no special-casing.

| Target             | Requirement                                                                                                                                                                                      |
| ------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `test:unit`        | Isolated unit tests with mocked dependencies; must consume Gherkin specs. `echo "no unit tests"` where no real unit tests exist                                                                  |
| `test:integration` | Service-level or in-process integration tests; real PostgreSQL (BE) or MSW/PGlite (FE). `echo "no integration tests"` where no real integration tests exist                                      |
| `test:e2e`         | Playwright E2E tests over HTTP/UI — real only on `*-e2e` projects; CRON-only (never pre-push/PR). `echo "no e2e tests"` on all non-e2e projects                                                  |
| `test:quick`       | Sequential 5-step gate (4 on `rhino-cli`) — see canonical composition below; enforced at pre-push, PR merge gate, and main merge gate                                                            |
| `lint`             | Static analysis and code-style checks; exit non-zero on violations; UI projects add `oxlint --jsx-a11y-plugin`. `echo` is not acceptable here — every project must have a real linter            |
| `typecheck`        | Type-correctness check without emitting artifacts (`tsc --noEmit`, `dotnet build`, `cargo check`). `echo "no typecheck"` for dynamically typed projects where compilation already enforces types |

**Echo-placeholder rule**: Declaring `test:unit: echo "no unit tests"` (or `test:integration`, `test:e2e`)
as a mandatory placeholder is **required** for projects where the real implementation does not apply — it
is **not** an anti-pattern. Omitting the target entirely is the anti-pattern. Echo placeholders enable
`nx affected -t test:unit` (and similar) to run workspace-wide without special-casing.

## Required-Where-Applicable Targets

Not part of the mandatory-six; declared only when the condition applies:

| Target                    | Condition                                                                                                                                                                                   |
| ------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `build`                   | Compiled and bundled projects only (Rust, .NET, Next.js); not required for interpreted-language projects without a compile step                                                             |
| `test:coverage`           | Wherever `test:unit` is real: native coverage gate (≥ 90% line) via `vitest --coverage`, `cargo llvm-cov`, or `dotnet test` coverage gate. `echo "no coverage"` where `test:unit` is `echo` |
| `specs:behavior:coverage` | All apps and E2E runners; validates Gherkin feature/scenario coverage at the behavior level                                                                                                 |
| `test:specs`              | All projects (echo where no specs); aggregate of `specs:structure-validation` and `specs:behavior:coverage` — runs inside `test:quick`                                                      |
