---
title: "Specs:Behavior:Coverage Projects"
description: The specs:behavior:coverage command-flag reference and per-project coverage-status table for Gherkin behavior-level validation.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when adding or debugging a project's specs:behavior:coverage target.
---

# Specs:Behavior:Coverage Projects

`specs:behavior:coverage` is compulsory for ALL apps and E2E runners (renamed from `specs:coverage`).
It validates Gherkin feature/scenario coverage at the behavior level — every scenario must be
exercised at the correct test level. It is enforced by the pre-push hook alongside `typecheck`,
`lint`, and `test:quick`, as well as in all scheduled Test CI workflows.

**Command flags used across project types**:

| Flag                         | Purpose                                                                                                                                                                                                                                                                                                               |
| ---------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--shared-steps`             | Validates steps across ALL source files rather than requiring 1:1 file-to-feature matching; used by all projects. `@wip`-tagged scenarios are fully exempt from step-gap reporting in this mode (same rule as the `@covers`-marker coverage model) — a step definition is never required for a scenario tagged `@wip` |
| `--exclude-dir test-support` | Excludes E2E-only `test-support` API spec files from non-E2E projects; used by demo-be backends and demo-fe frontends                                                                                                                                                                                                 |
| `--exclude-source-dir <dir>` | Excludes a directory name from the **app-tree source walk only** (never the `.feature`-file walk); for a directory name legitimate in both trees but that must not be scanned as source, e.g. ayokoding-www's Next.js `content/` directory colliding with a Gherkin `content/` spec folder                            |

**Project coverage status**:

| Project group                                                   | Status   | Notes                                                                                                                   |
| --------------------------------------------------------------- | -------- | ----------------------------------------------------------------------------------------------------------------------- |
| Rust CLI apps (`rhino-cli`)                                     | Enforced | `--shared-steps` only; no `--exclude-dir` needed (no test-support specs)                                                |
| API backends (`organiclever-be`)                                | Enforced | `--shared-steps --exclude-dir test-support`                                                                             |
| E2E runners (`organiclever-be-e2e`, `organiclever-app-web-e2e`) | Enforced | `--shared-steps` only; test-support steps are implemented here                                                          |
| Content platforms (`ose-www`)                                   | Enforced | `--shared-steps`                                                                                                        |
| Content platforms (`ayokoding-www`)                             | Enforced | `--shared-steps --exclude-source-dir content` (excludes the Next.js `content/` directory from the app-tree source walk) |
| Web UI apps (`organiclever-app-web`)                            | Enforced | `--shared-steps`                                                                                                        |
| Libraries (`web-ui`, `web-ui-token`)                            | Enforced | `--shared-steps`                                                                                                        |
| Projects with genuine step gaps                                 | Deferred | `specs:behavior:coverage` target exists but validation deferred until step implementation is complete                   |

All apps and E2E runners are required to have a `specs:behavior:coverage` target. Projects with
genuine step gaps have the target deferred temporarily until step implementations are complete.

**Nx inputs for `specs:behavior:coverage`**: The target must declare the project's feature files and
source files as inputs so the cache invalidates when specs or step definitions change:

```json
"specs:behavior:coverage": {
  "executor": "nx:run-commands",
  "cache": true,
  "inputs": [
    "{workspaceRoot}/specs/apps/organiclever-be/**/*.feature",
    "{projectRoot}/src/**/*.rs"
  ],
  "options": {
    "command": "rhino-cli specs behavior-coverage validate specs/apps/organiclever-be --shared-steps --exclude-dir test-support apps/organiclever-be/src"
  }
}
```

The exact source directory arguments vary by language. The feature files argument always points to
`{workspaceRoot}/specs/.../**/*.feature` for the project's spec directory.
