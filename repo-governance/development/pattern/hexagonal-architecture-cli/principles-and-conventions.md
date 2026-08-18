---
title: "Principles and Conventions"
description: "The core principles and conventions this pattern implements - explicitness, pure functions, simplicity, and functional programming."
category: explanation
subcategory: development
tags:
  - architecture
  - hexagonal
  - cli
  - rust
  - fsharp
created: 2026-05-26
when_to_use: "Use when you need to trace a CLI hexagonal-architecture rule back to the principle or convention it implements."
---

# Principles and Conventions

## Principles Implemented/Respected

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: Command handlers
  receive parsed, typed arguments. The application layer is invoked with named domain concepts, not raw `&[String]`
  slices or `os.Args`.

- **[Pure Functions Over Side Effects](../../../principles/software-engineering/pure-functions.md)**: Domain logic runs as
  pure functions. File I/O, HTTP requests, and standard-output writes are outbound adapter concerns confined to
  `infrastructure/`.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Separating argument
  parsing from business logic keeps each layer testable in isolation. Domain tests need no CLI harness.

## Conventions Implemented/Respected

- **[Functional Programming Practices](../functional-programming.md)**: Domain functions are pure and stateless.
