---
title: "Mandatory Targets — Summary Matrix"
description: The per-project-type summary matrix of which mandatory targets are real versus echo, plus backend typecheck examples and CI schedules.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when checking at a glance which targets a given project type (API backend, Web UI, CLI, library, E2E runner) must declare.
---

# Mandatory Targets — Summary Matrix

## Summary Matrix

Per the mandatory-six rule, every project declares all six targets (`test:unit`, `test:integration`,
`test:e2e`, `test:quick`, `lint`, `typecheck`). In this matrix, **"echo"** means the target is
declared as a no-op echo placeholder — it is present but does no real work. `specs:behavior:coverage`
is compulsory for all apps and E2E runners.

| Project Type | `test:unit` | `test:integration` | `test:e2e` | `test:quick` | `specs:behavior:coverage` | `lint` | `build` | `typecheck`  |
| ------------ | ----------- | ------------------ | ---------- | ------------ | ------------------------- | ------ | ------- | ------------ |
| API Backend  | Yes         | Yes (PG)           | echo (†)   | Yes          | Yes                       | Yes    | Yes     | Yes (all 11) |
| Web UI App   | Yes         | Yes (MSW)          | echo (†)   | Yes          | Yes                       | Yes    | Yes     | If typed     |
| Demo-fe FE   | Yes         | echo               | echo (†)   | Yes          | Yes                       | Yes    | Yes     | If typed     |
| Fullstack    | Yes         | Yes                | echo (†)   | Yes          | Yes                       | Yes    | Yes     | If typed     |
| CLI App      | Yes         | Yes                | echo       | Yes          | Yes                       | Yes    | Yes     | If typed     |
| Library      | Yes         | Optional / echo    | echo       | Yes          | Yes                       | Yes    | —       | If typed     |
| E2E Runner   | echo        | echo               | Yes        | Yes          | Yes                       | Yes    | —       | If typed     |

† E2E tests live in dedicated `*-e2e` runner projects; non-e2e projects declare `test:e2e: echo "no e2e tests"`.

**Product backend `typecheck` examples** (all statically typed backends use `typecheck` with `dependsOn: ["codegen"]` where codegen applies):

| Backend           | `typecheck` command                                                   |
| ----------------- | --------------------------------------------------------------------- |
| `organiclever-be` | `dotnet build apps/organiclever-be/organiclever-be.fsproj -c Release` |

**CI schedules**: Per-service "Test" workflows run 2× daily (WIB 06, 18) combining `test:integration` and `test:e2e` for each service. `typecheck`, `lint`, and `test:quick` run on every PR event and on every push to `main` through `pr-quality-gate.yml`; its CI matrix is derived from the gate registry. Heavy integration and E2E tiers remain scheduled-only and are never gate-surface entries.
