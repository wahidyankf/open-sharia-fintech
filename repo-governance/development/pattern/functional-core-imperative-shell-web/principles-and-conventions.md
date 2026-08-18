---
title: "Principles and Conventions"
description: "The core principles and conventions this pattern implements - pure functions, simplicity, immutability, explicitness, and functional programming practices."
category: explanation
subcategory: development
tags:
  - architecture
  - functional-core-imperative-shell
  - nextjs
  - functional-programming
  - web
created: 2026-06-17
when_to_use: "Use when you need to trace the core/shell split back to the principles and conventions it implements."
---

# Principles and Conventions

## Principles Implemented/Respected

- **[Pure Functions Over Side Effects](../../../principles/software-engineering/pure-functions.md)**: The functional core
  is pure — every decision, transformation, validation, and derivation lives in functions with no IO and no side
  effects. Effects are pushed to the imperative shell at the edge.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Two zones, not four
  layers. No port interfaces or dependency-injection wiring are introduced for their own sake; the shell imports the
  core directly.

- **[Immutability Over Mutability](../../../principles/software-engineering/immutability.md)**: Core data is immutable;
  shell state uses immutable update patterns (spread, `produce`).

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The directory a file
  lives in declares its nature. A file under `core/` is provably pure; a file under `shell/` is where effects are
  allowed. No ambient inference required.

## Conventions Implemented/Respected

- **[Functional Programming Practices](../functional-programming.md)**: The core uses pure functions and immutable data
  structures throughout.
