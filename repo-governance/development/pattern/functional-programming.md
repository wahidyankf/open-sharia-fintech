---
title: Functional Programming Practices
description: Guidelines for applying functional programming principles in TypeScript/JavaScript
category: explanation
subcategory: development
tags:
  - development
  - functional-programming
  - immutability
  - pure-functions
  - typescript
created: 2025-12-28
when_to_use: "Use when writing or reviewing TypeScript/JavaScript business logic."
---

# Functional Programming Practices

Guidelines for applying functional programming principles in TypeScript/JavaScript — how to write
immutable, pure, and testable code, one topic per child page below.

## Contents

- [Principles and Conventions](./functional-programming/principles-and-conventions.md) — The core principles and conventions this practice implements - immutability, pure functions, explicitness, and simplicity. Use when you need to trace a functional-programming rule back to the principle or convention it implements.
- [Overview](./functional-programming/overview.md) — A summary of the four functional-programming emphases this practice covers: immutable data, pure functions, composition, and functional core/imperative shell. Use when orienting to what this functional-programming practice covers before reading a specific section.
- [Immutability Patterns — Primitives, Objects, and Arrays](./functional-programming/immutability-patterns-primitives-objects-and-arrays.md) — How to prefer const, use the spread operator for object updates, and use immutable array methods instead of mutation. Use when updating a primitive, object, or array value and need the immutable equivalent of a mutating operation.
- [Immutability Patterns — Immer and Object.freeze](./functional-programming/immutability-patterns-immer-and-object-freeze.md) — How to use Immer for deep nested updates and Object.freeze for runtime immutability enforcement. Use when a nested object update is too deep for spread syntax, or you need to enforce immutability at runtime.
- [Pure Function Patterns](./functional-programming/pure-function-patterns.md) — Examples of basic pure functions, pure data transformations, and the functional core/imperative shell split. Use when writing a function and want a worked example of keeping it pure versus isolating its side effects.
- [Function Composition](./functional-programming/function-composition.md) — The pipe pattern, compose pattern, and higher-order functions for building complex behaviour from simple functions. Use when you need to combine several small functions into a single pipeline or transformation.
- [Avoiding Common Pitfalls](./functional-programming/avoiding-common-pitfalls.md) — Common functional-programming mistakes - mutating function arguments, class-based mutable state, and mixing validation with I/O. Use when reviewing code for accidental mutation, mutable class state, or side effects mixed into pure logic.
- [TypeScript-Specific Patterns](./functional-programming/typescript-specific-patterns.md) — TypeScript-specific functional patterns - readonly types, branded types, and discriminated unions for state modeling. Use when you need a TypeScript-specific technique for enforcing immutability or modeling state explicitly.
- [Islamic Finance Example](./functional-programming/islamic-finance-example.md) — A worked Mudharabah profit-distribution example showing functional core/imperative shell applied to Shariah-compliant business logic. Use when you need a complete worked example of applying functional core/imperative shell to financial business logic.
- [When to Use Classes, Testing, Libraries, and Migration Strategy](./functional-programming/when-to-use-classes-testing-libraries-and-migration-strategy.md) — When classes are acceptable, how pure functions simplify testing, recommended functional libraries, and how to migrate an existing codebase incrementally. Use when deciding whether a class is appropriate, or planning an incremental migration to functional patterns.
- [Related Documentation and References](./functional-programming/related-documentation-and-references.md) — Links to related principles and conventions, plus external books and articles on functional programming. Use when you need a link to the underlying principle, or a book/article reference on functional programming.
