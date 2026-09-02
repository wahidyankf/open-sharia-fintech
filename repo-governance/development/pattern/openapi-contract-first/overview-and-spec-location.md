---
title: "Overview and Spec Location"
description: "How contract-first codegen works end to end, and where each backend app's OpenAPI spec file lives."
category: explanation
subcategory: development
tags:
  - openapi
  - contract-first
  - codegen
  - api
  - drift-enforcement
created: 2026-05-26
when_to_use: "Use when locating the OpenAPI spec file for a given backend app, or explaining the contract-first workflow."
---

# Overview and Spec Location

## Overview

Each BE↔client pair maintains an OpenAPI 3.1 YAML spec. Codegen tooling reads that spec and emits typed client code
(TypeScript) and server scaffolding (Rust). CI runs codegen on every push and fails the build if the generated
output differs from the committed output. This makes spec drift a hard CI failure rather than a silent runtime
divergence.

## Spec Location

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
| `ose-be`          | `specs/apps/ose/containers/contracts/openapi.yaml`  |

The spec file is the only artefact that humans edit. Generated files are never edited by hand.
