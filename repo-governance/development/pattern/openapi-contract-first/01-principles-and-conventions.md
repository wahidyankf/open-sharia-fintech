---
title: "Principles and Conventions"
description: "The core principles and conventions this pattern implements - explicitness, reproducibility, automation, simplicity, and the backend hexagonal-architecture layering."
category: explanation
subcategory: development
tags:
  - openapi
  - contract-first
  - codegen
  - api
  - drift-enforcement
created: 2026-05-26
when_to_use: "Use when you need to trace an OpenAPI contract-first rule back to the principle or convention it implements."
---

# Principles and Conventions

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Every endpoint,
  request body, response schema, and error type is declared explicitly in the YAML before it exists in any
  implementation. No undocumented behaviour can accumulate silently.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**: Codegen runs from a
  committed YAML file. The same spec always produces the same generated types. CI enforces that generated files match
  the spec — no drift is tolerated.

- **[Automation Over Manual](../../../principles/software-engineering/automation-over-manual.md)**: Type definitions,
  serialisers, and route skeletons are generated automatically. Manual synchronisation between spec and code is
  eliminated.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: A single YAML file is the
  authoritative interface description. Frontend, backend, and integration tests all read from the same source.

## Conventions Implemented/Respected

- **[Hexagonal Architecture + DDD — Backend Apps](../hexagonal-architecture-be.md)**: Generated types land in the
  `api/http/` inbound adapter layer. Domain types are hand-authored; generated request/response types stay at the
  boundary.
