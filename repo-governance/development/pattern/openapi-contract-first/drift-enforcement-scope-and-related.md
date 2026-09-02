---
title: "Drift Enforcement, Scope, and Related"
description: "How CI fails the build on spec/codegen drift, which BE-client pairs participate in contract-first development, and related pattern documentation."
category: explanation
subcategory: development
tags:
  - openapi
  - contract-first
  - codegen
  - api
  - drift-enforcement
created: 2026-05-26
when_to_use: "Use when a CI drift check fails, or checking whether a given app participates in contract-first codegen."
---

# Drift Enforcement, Scope, and Related

## Drift Enforcement

CI enforces that committed generated files match the spec. After running `codegen`, any non-empty `git diff` in the
generated output directory fails the build.

The CI step for each app follows this pattern:

```bash
# 1. Run codegen from the committed spec
nx run <app>:codegen

# 2. Fail if generated output differs from committed files
git diff --exit-code src/generated-contracts/
# (Rust apps use generated-contracts/ without the src/ prefix)
```

A non-zero exit code from `git diff --exit-code` means the spec was updated but codegen was not re-run before commit,
or vice versa. The fix is always to re-run `nx run <app>:codegen` and commit the updated generated files together with
the spec change.

## Scope

Contract-first development covers these BE↔client pairs:

| Backend           | Client                 | Spec                                                |
| ----------------- | ---------------------- | --------------------------------------------------- |
| `organiclever-be` | `organiclever-app-web` | `specs/apps/organiclever/be/contracts/openapi.yaml` |
| `ose-be`          | `ose-www`              | `specs/apps/ose/be/contracts/openapi.yaml`          |

Apps outside this table (CLI tools, content-only web apps such as `ayokoding-www` and `ose-www`) do not participate
in contract-first codegen.

## Related

- **[Hexagonal Architecture + DDD — Backend Apps](../hexagonal-architecture-be.md)** — Where generated types land in
  the layer structure (`api/http/` boundary); domain types are never generated
- **[Functional Core / Imperative Shell — Web Apps](../functional-core-imperative-shell-web.md)** — Where generated
  TypeScript client types land in the web app structure (`features/<name>/shell/`, the imperative shell)
