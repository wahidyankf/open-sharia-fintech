---
title: "Cache and Inputs Convention — Canonical Inputs"
description: Why explicit inputs are required for correct cache invalidation, with canonical Rust/Go input examples for CLI apps and API backends.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when declaring or auditing the inputs array on a project's test:unit or test:quick target.
---

# Cache and Inputs Convention — Canonical Inputs

Declaring explicit `inputs` in `project.json` ensures Nx invalidates the cache when any relevant
file changes. Without explicit inputs, Nx uses a broad default (all project files) and misses
cross-project dependencies like shared Gherkin specs or generated contracts.

## Canonical Inputs per Language

API backends with contract codegen must include Gherkin specs and generated contracts in `test:unit`
and `test:quick` inputs. The Gherkin specs path always points to
`{workspaceRoot}/specs/apps/<app-name>/**/*.feature`. The generated-contracts path varies by
language:

| Language | Source files                                               | Generated contracts                      | Gherkin specs                                        |
| -------- | ---------------------------------------------------------- | ---------------------------------------- | ---------------------------------------------------- |
| Rust     | `{projectRoot}/src/**/*.rs`, `{projectRoot}/tests/**/*.rs` | `{projectRoot}/generated-contracts/**/*` | `{workspaceRoot}/specs/apps/<app-name>/**/*.feature` |

**Rust CLI app** (`rhino-cli`) also consumes Gherkin specs in `test:unit`. Its `test:unit` and `test:quick` inputs must include the CLI's own spec files:

| CLI App     | Gherkin specs input                             |
| ----------- | ----------------------------------------------- |
| `rhino-cli` | `{workspaceRoot}/specs/apps/rhino/**/*.feature` |

Example for `rhino-cli` `test:unit` inputs:

```json
"inputs": [
  "{projectRoot}/src/**/*.rs",
  "{projectRoot}/tests/**/*.rs",
  "{projectRoot}/Cargo.toml",
  "{projectRoot}/Cargo.lock",
  "{workspaceRoot}/specs/apps/rhino/**/*.feature"
]
```

**Rust CLI apps** also consume Gherkin specs in `test:unit`. Their `test:unit` and `test:quick` inputs must include the CLI's own spec files:

| CLI App     | Gherkin specs input                             |
| ----------- | ----------------------------------------------- |
| `rhino-cli` | `{workspaceRoot}/specs/apps/rhino/**/*.feature` |

Example for `rhino-cli` `test:unit` inputs:

```json
"inputs": [
  "{projectRoot}/src/**/*.rs",
  "{projectRoot}/tests/**/*.rs",
  "{projectRoot}/Cargo.toml",
  "{projectRoot}/Cargo.lock",
  "{workspaceRoot}/specs/apps/rhino/**/*.feature"
]
```

**Why specs and contracts in inputs**: If a Gherkin feature file changes or the OpenAPI contract
spec changes (triggering `codegen`), `test:unit` and `test:quick` must re-run even if application
source files are unchanged. Without these paths in `inputs`, Nx incorrectly serves cached results.

**Note on specs:behavior:coverage enforcement**: `specs:behavior:coverage` is compulsory for all
apps and E2E runners (renamed from `specs:coverage`). `rhino-cli specs behavior-coverage validate`
runs as the `specs:behavior:coverage` Nx target, enforced by the pre-push hook alongside
`typecheck`, `lint`, and `test:quick`, and in all scheduled Test CI workflows. Projects with
genuine step gaps have the target deferred temporarily until step implementations are complete. See
the "Specs:Behavior:Coverage Projects" section for flags and project-by-project status.
