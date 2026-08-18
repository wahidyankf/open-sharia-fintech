---
title: "Principles and Conventions"
description: "The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, immutability, and OpenAPI contract-first."
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - ddd
  - fsharp
  - backend
created: 2026-05-26
when_to_use: "Use when you need to trace a backend hexagonal/DDD rule back to the principle or convention it implements."
---

# Principles and Conventions

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Bounded context
  boundaries are directory boundaries. Inter-context dependencies cross through application interfaces only —
  never through shared domain types.

- **[Pure Functions Over Side Effects](../../../principles/software-engineering/pure-functions.md)**: Domain layers
  contain pure business rules. Infrastructure layers contain all I/O. Error mapping (domain error → HTTP response)
  happens at the `api/http/` boundary, not inside the domain.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Each bounded context is
  independently deployable in principle. Keeping contexts isolated prevents a change in one domain from cascading
  through the entire codebase.

- **[Immutability Over Mutability](../../../principles/software-engineering/immutability.md)**: Domain entities are
  immutable value types. Infrastructure adapters translate mutable external representations at the boundary.

## Conventions Implemented/Respected

- **[Functional Programming Practices](../functional-programming.md)**: Domain and application layers use pure
  functions and immutable data.
- **[OpenAPI Contract-First Development](../openapi-contract-first.md)**: The `api/http/` inbound adapter layer
  implements handlers generated from or validated against the OpenAPI spec.
