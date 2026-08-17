---
title: "Mandatory Targets — test:quick Composition and Gate-Surface Rule"
description: The canonical five-step test:quick composition with a worked rhino-cli example, and the gate-surface / scheduled-tier rule.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when wiring or auditing a project's test:quick target definition.
---

# Mandatory Targets — test:quick Composition and Gate-Surface Rule

## Canonical `test:quick` Composition

`test:quick` is a **sequential** `nx:run-commands` with `"parallel": false` running in this **exact order**:

1. `nx run <project>:typecheck`
2. `nx run <project>:lint`
3. `nx run <project>:test:unit` (plain/fast smoke)
4. `nx run <project>:test:coverage` (same suite under coverage, ≥ 90% line)
5. `nx run <project>:test:specs` (all `specs:*` validators)

It reuses each sibling target's definition and Nx cache. Order is guaranteed by `parallel: false`.
It stops at the first failing step. Because `test:quick` composes `test:unit` + `test:coverage` +
`test:specs`, **all three must be present on every project** (echo where N/A).

Canonical example for a Rust CLI project (`rhino-cli`):

```json
{
  "test:quick": {
    "executor": "nx:run-commands",
    "cache": true,
    "inputs": [
      "{projectRoot}/src/**/*.rs",
      "{projectRoot}/tests/**/*.rs",
      "{projectRoot}/Cargo.toml",
      "{projectRoot}/Cargo.lock",
      "{workspaceRoot}/specs/apps/rhino/**/*.feature"
    ],
    "options": {
      "commands": [
        "nx run rhino-cli:typecheck",
        "nx run rhino-cli:lint",
        "nx run rhino-cli:test:unit",
        "nx run rhino-cli:test:coverage",
        "nx run rhino-cli:test:specs"
      ],
      "parallel": false
    }
  }
}
```

## Gate-Surface and Scheduled-Tier Rule

**Gate rule**: `(pre-commit ∪ pre-push) == PR gate`; the registry defines the check set and the
CI matrix derives matrix-wired entries from it.

| Gate       | What runs                                                                               | When                               |
| ---------- | --------------------------------------------------------------------------------------- | ---------------------------------- |
| Pre-commit | Formatting only (lint-staged: prettier, rustfmt, fantomas, gofmt, …)                    | Every commit                       |
| Pre-push   | `typecheck`, `lint`, `test:quick` (includes `test:unit`, `test:coverage`, `test:specs`) | Every push                         |
| PR gate    | Identical to pre-push                                                                   | Every PR open / update             |
| CRON-only  | `test:integration`, `test:e2e`                                                          | Scheduled CI (2× daily, WIB 06/18) |

`test:integration` and `test:e2e` are **CRON-only** — they run in scheduled CI workflows (2× daily at
WIB 06:00 and 18:00), never in the pre-push hook or PR gate. This keeps the pre-push gate fast while
ensuring continuous coverage.
