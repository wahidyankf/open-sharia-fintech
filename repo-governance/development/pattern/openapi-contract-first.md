---
description: Spec-first API development — the OpenAPI YAML is the single source of truth; code is generated from it, not the reverse
when_to_use: "Use when adding or changing an API endpoint, running codegen, or debugging a CI spec/codegen drift failure."
---

# OpenAPI Contract-First Development

Contract-first development means the OpenAPI YAML specification is written before any implementation code.
The spec is the single source of truth for every API contract. Generated code follows from the spec; the
spec never follows from the code.

## Contents

- [Principles and Conventions](./openapi-contract-first/principles-and-conventions.md) — The core principles and conventions this pattern implements - explicitness, reproducibility, automation, simplicity, and the backend hexagonal-architecture layering. Use when you need to trace an OpenAPI contract-first rule back to the principle or convention it implements.
- [Codegen Tooling and Nx Targets](./openapi-contract-first/codegen-tooling-and-nx-targets.md) — Which codegen tool runs for each app, and the Nx targets that invoke codegen and spec linting. Use when running codegen for an app or looking up which tool generates its client/server types.
- [Drift Prevention, Scope, and Related](./openapi-contract-first/drift-prevention-scope-and-related.md) — Why uncommitted generated output makes spec/codegen drift unrepresentable, which BE-client pairs participate in contract-first development, and related pattern documentation. Use when generated contract output is missing or stale, or checking whether a given app participates in contract-first codegen.

## Overview and Spec Location

### Overview

Each BE↔client pair maintains an OpenAPI 3.1 YAML spec. Codegen tooling reads that spec and emits typed client code
(TypeScript) and server scaffolding (Rust). CI runs codegen on every push and fails the build if the generated
output differs from the committed output. This makes spec drift a hard CI failure rather than a silent runtime
divergence.

### Spec Location

Specs live under the `specs/` tree, organised by app and container:

```
specs/
└── apps/
    └── <app-name>/
        └── containers/
            └── contracts/
                └── openapi.yaml
```

| BE App            | Spec Path                                           |
| ----------------- | --------------------------------------------------- |
| `organiclever-be` | `specs/apps/organiclever/be/contracts/openapi.yaml` |
| `ose-be`          | `specs/apps/ose/be/contracts/openapi.yaml`          |

The spec file is the only artefact that humans edit. Generated files are never edited by hand.
