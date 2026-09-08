---
description: Hexagonal architecture with DDD bounded contexts for backend apps — F#/Giraffe directory layouts, language-specific idioms, and inter-context isolation rules
when_to_use: "Use when structuring a backend bounded context, wiring F# dependency injection, or mapping a domain error to an HTTP response."
---

# Hexagonal Architecture + DDD — Backend Apps

Backend apps combine hexagonal architecture with Domain-Driven Design (DDD) bounded contexts. Each bounded
context lives under `contexts/<name>/` and owns its hexagonal layers independently. DDD applies **only** to
backend apps (`organiclever-be`, `ose-be`). Next.js web apps do not use hexagonal/DDD at all — see
[Functional Core / Imperative Shell — Web Apps](../pattern/functional-core-imperative-shell-web.md).

## Contents

- [Overview and Directory Layout](./hexagonal-architecture-be/overview-and-directory-layout.md) — How bounded contexts and the api/ transport directory relate, plus the canonical F#/Giraffe directory layout. Use when scaffolding a new bounded context and need the canonical directory layout.
- [F#-Specific](./hexagonal-architecture-be/fsharp-specific.md) — F#-specific idioms for outbound ports, dependency injection, and mapping domain errors to HTTP responses at the API boundary. Use when implementing an F# outbound port interface, wiring DI in Program.fs, or mapping a domain error to an HTTP response.
- [DDD Integration, Forbidden Imports, and Related](./hexagonal-architecture-be/ddd-integration-forbidden-imports-and-related.md) — Bounded-context isolation rules, shared infrastructure placement, anti-corruption layers, the forbidden-imports table, and related pattern documentation. Use when two bounded contexts need to communicate, or checking whether a layer imports something it should not.

## Principles and Conventions

### Principles Implemented/Respected

- **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)**: Bounded context
  boundaries are directory boundaries. Inter-context dependencies cross through application interfaces only —
  never through shared domain types.

- **[Pure Functions Over Side Effects](../../principles/software-engineering/pure-functions.md)**: Domain layers
  contain pure business rules. Infrastructure layers contain all I/O. Error mapping (domain error → HTTP response)
  happens at the `api/http/` boundary, not inside the domain.

- **[Simplicity Over Complexity](../../principles/general/simplicity-over-complexity.md)**: Each bounded context is
  independently deployable in principle. Keeping contexts isolated prevents a change in one domain from cascading
  through the entire codebase.

- **[Immutability Over Mutability](../../principles/software-engineering/immutability.md)**: Domain entities are
  immutable value types. Infrastructure adapters translate mutable external representations at the boundary.

### Conventions Implemented/Respected

- **[Functional Programming Practices](./functional-programming.md)**: Domain and application layers use pure
  functions and immutable data.
- **[OpenAPI Contract-First Development](./openapi-contract-first.md)**: The `api/http/` inbound adapter layer
  implements handlers generated from or validated against the OpenAPI spec.
