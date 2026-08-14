---
title: "Target Anti-Patterns"
description: The catalog of Nx target anti-patterns to avoid -- non-standard names, omitted mandatory targets, heavy test:quick, and more.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when reviewing a project.json for target-definition mistakes before merging.
---

# Target Anti-Patterns

- **Non-standard target names**: `serve` instead of `dev`/`start`, `unit-test` instead of `test:unit`, `integration-test` instead of `test:integration`, `check` instead of `lint` or `typecheck`, bare `test` or `test:full` instead of a specific `test:*` variant
- **Omitting mandatory-six targets**: Every project must declare all six mandatory targets (`test:unit`, `test:integration`, `test:e2e`, `test:quick`, `lint`, `typecheck`); omitting any one silently breaks `nx affected -t <target>` workspace-wide — use echo placeholders instead
- **Missing `test:quick`**: Omitting the pre-push gate target silently excludes the project from `nx affected -t test:quick` — this breaks the workspace-wide hook
- **Missing `lint`**: Projects without `lint` cannot participate in workspace-wide lint runs or the pre-push hook lint gate
- **Heavy `test:quick`**: Including slow integration tests or E2E in `test:quick` defeats its purpose — `test:quick` composes `typecheck` → `lint` → `test:unit` → `test:coverage` → `test:specs`, all of which must stay fast; `test:integration` and `test:e2e` are CRON-only
- **Mixing concerns in `test:unit`**: `test:unit` must not spin up databases, external APIs, or network services — those belong in `test:integration`
- **Using a real database in unit tests**: Unit tests must use mocked repositories or in-memory implementations — never a real database. Real databases belong in integration tests (API backends via docker-compose) or E2E tests
- **Using HTTP dispatch in integration tests**: Integration tests for API backends must call service/repository functions directly — not through HTTP dispatch mechanisms. HTTP contract verification belongs in E2E tests. See [Three-Level Testing Standard](../../quality/three-level-testing-standard.md) for the full level boundaries
- **Enabling cache on `test:integration` with Docker**: Integration tests that use real PostgreSQL via docker-compose must have `cache: false` — stale results when database state matters. Only in-process-mocking integration tests (MSW, Godog) may enable caching
- **`build` on interpreted-language projects**: Adding a no-op `build` to plain Node.js scripts just to appear consistent — if there is no compile step, there is no `build` target
- **`typecheck` on compile-enforced languages without additional analysis**: Rust enforces types through `build`; a separate `typecheck` that only re-runs the compiler may be redundant for simple projects
- **Undeclared outputs**: Omitting `outputs` on `build` disables caching and forces full rebuilds on every run
- **Apps-only targets on libs**: Libs do not expose `dev` or `start`; those are app-specific concepts
- **Creating a `test:full` wrapper**: Adding a `test:full` that just chains other targets adds indirection without value — `test:integration` and `test:e2e` run directly in scheduled CI matrix steps, not through a wrapper
