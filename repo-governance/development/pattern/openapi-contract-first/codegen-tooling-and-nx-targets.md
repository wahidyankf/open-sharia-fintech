---
title: "Codegen Tooling and Nx Targets"
description: "Which codegen tool runs for each app, and the Nx targets that invoke codegen and spec linting."
category: explanation
subcategory: development
tags:
  - openapi
  - contract-first
  - codegen
  - api
  - drift-enforcement
created: 2026-05-26
when_to_use: "Use when running codegen for an app or looking up which tool generates its client/server types."
---

# Codegen Tooling and Nx Targets

## Codegen Tooling

| Target                                                | Tool                  | Output Path                | Notes                                     |
| ----------------------------------------------------- | --------------------- | -------------------------- | ----------------------------------------- |
| TypeScript client (`organiclever-app-web`, `ose-www`) | `@hey-api/openapi-ts` | `src/generated-contracts/` | Emits typed fetch client + schema types   |
| F# server (`organiclever-be`)                         | `nswag` (F# target)   | `generated-contracts/`     | Emits Giraffe handler types + model types |
| F# server (`ose-be`)                                  | `nswag` (F# target)   | `generated-contracts/`     | Emits Giraffe handler types + model types |

Generated directories are committed to the repository. The CI drift check (see below) compares the freshly generated
output against the committed files and fails if they differ.

## Nx Targets

Each app that participates in contract-first development exposes these Nx targets in its `project.json`:

| Target    | App                      | Command                                                      |
| --------- | ------------------------ | ------------------------------------------------------------ |
| `codegen` | `organiclever-app-web`   | Runs `@hey-api/openapi-ts` against the contracts spec        |
| `codegen` | `organiclever-be`        | Runs `nswag` F# target                                       |
| `codegen` | `ose-www`                | Runs `@hey-api/openapi-ts` against the contracts spec        |
| `codegen` | `ose-be`                 | Runs `nswag` F# target                                       |
| `lint`    | `organiclever-contracts` | Validates and bundles the OpenAPI spec (Redocly or Spectral) |
| `docs`    | `organiclever-contracts` | Generates browsable API documentation                        |

Run codegen for a specific app:

```bash
nx run organiclever-app-web:codegen
nx run organiclever-be:codegen
nx run ose-www:codegen
nx run ose-be:codegen
```

Validate the spec itself:

```bash
nx run organiclever-contracts:lint
```
