---
title: "Principles and Conventions"
description: "The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, and immutability."
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - ports-and-adapters
  - dependency-rule
created: 2026-05-26
when_to_use: "Use when you need to trace a hexagonal-architecture rule back to the principle or convention it implements."
---

# Principles and Conventions

## Principles Implemented/Respected

This practice implements/respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Ports are named
  interfaces. Every dependency between layers crosses a well-defined boundary, making coupling explicit and auditable.

- **[Pure Functions Over Side Effects](../../../principles/software-engineering/pure-functions.md)**: The domain layer
  contains pure business logic. Side effects (database access, HTTP calls, file I/O) are pushed outward to adapter
  implementations.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: The dependency rule
  eliminates entire classes of coupling bugs. A layer that cannot import its neighbour cannot accidentally couple to it.

- **[Immutability Over Mutability](../../../principles/software-engineering/immutability.md)**: Domain models express
  business invariants as immutable value types. Adapters translate mutable external representations to and from
  immutable domain types at the boundary.

## Conventions Implemented/Respected

- **[Functional Programming Practices](../functional-programming.md)**: Domain logic uses pure functions and immutable
  data structures, consistent with the functional-core/imperative-shell pattern.
