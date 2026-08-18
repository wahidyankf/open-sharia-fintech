---
title: "Principles and Conventions"
description: "The core principles and conventions this practice implements - immutability, pure functions, explicitness, and simplicity."
category: explanation
subcategory: development
tags:
  - development
  - functional-programming
  - immutability
  - pure-functions
  - typescript
created: 2025-12-28
when_to_use: "Use when you need to trace a functional-programming rule back to the principle or convention it implements."
---

# Principles and Conventions

## Principles Implemented/Respected

This practice respects the following core principles:

- **[Immutability Over Mutability](../../../principles/software-engineering/immutability.md)**: All data transformations create new values instead of modifying existing ones. Use `const`, spread operators, and immutable array methods to prevent state mutations.

- **[Pure Functions Over Side Effects](../../../principles/software-engineering/pure-functions.md)**: Business logic implemented as pure, deterministic functions. Side effects (I/O, logging, state changes) isolated at system boundaries using Functional Core, Imperative Shell pattern.

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: All function dependencies passed as explicit arguments. No hidden dependencies on global state or implicit context.

- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: Functional programming simplifies reasoning by eliminating mutable state and side effects. Prefer composition of simple pure functions over complex class hierarchies.

## Conventions Implemented/Respected

This practice implements/respects the following conventions:

- **[Code Quality Convention](../../quality/code.md)**: Prettier formats functional code consistently. ESLint can enforce functional patterns (prefer-const, no-mutation rules).

- **[Implementation Workflow](../../workflow/implementation.md)**: Functional patterns introduced in "Make it Right" stage after functionality works. Start simple, refactor to functional style, then optimize if needed.
