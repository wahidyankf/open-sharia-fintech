---
description: The run/install targets required on CLI applications and the install/test:e2e/test:e2e:ui/test:e2e:report targets required on *-e2e projects.
when_to_use: Use when scaffolding a new CLI application or a new *-e2e Playwright runner project.
---

# Mandatory Targets — CLI and E2E Test Projects

## CLI Applications

Executable CLIs and similar tools:

| Target    | Requirement                                           |
| --------- | ----------------------------------------------------- |
| `run`     | Execute the application through its project toolchain |
| `install` | Restore or sync project dependencies                  |

## E2E Test Projects

Playwright suites (`*-e2e`):

| Target            | Requirement                  |
| ----------------- | ---------------------------- |
| `install`         | Install npm dependencies     |
| `test:e2e`        | Run all tests headlessly     |
| `test:e2e:ui`     | Run tests with Playwright UI |
| `test:e2e:report` | Open the HTML test report    |

**Execution strategy**: `test:e2e` never runs through pre-commit, pre-push, PR/main gates,
`test:quick`, or a static coverage target. Developers run impacted scenarios manually; scheduled
full-quality workflows run complete Integration suites before complete unfiltered E2E suites.

**BDD suites**: When the E2E project uses playwright-bdd, `test:e2e` runs
`npx bddgen && npx playwright test`. The `bddgen` step regenerates `.features-gen/`
spec files from the Gherkin feature files before Playwright executes them.
See `apps/organiclever-be-e2e/project.json` for a canonical product-app example.

An E2E project also exposes `test:coverage:e2e` and `test:coverage:behaviour`. These validators
statically prove adapter completeness and exemption validity without running Playwright. The owning
corpus is an explicit Nx input of both coverage and runtime targets.
