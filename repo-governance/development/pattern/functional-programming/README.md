---
title: "Functional Programming Practices"
description: "Guidelines for applying functional programming principles in TypeScript/JavaScript"
when_to_use: "Read this index to find the right Functional Programming Practices child document."
---

# Functional Programming Practices

- [Principles and Conventions](./01-principles-and-conventions.md) — The core principles and conventions this practice implements - immutability, pure functions, explicitness, and simplicity. Use when you need to trace a functional-programming rule back to the principle or convention it implements.
- [Overview](./02-overview.md) — A summary of the four functional-programming emphases this practice covers: immutable data, pure functions, composition, and functional core/imperative shell. Use when orienting to what this functional-programming practice covers before reading a specific section.
- [Immutability Patterns — Primitives, Objects, and Arrays](./03-immutability-patterns-primitives-objects-and-arrays.md) — How to prefer const, use the spread operator for object updates, and use immutable array methods instead of mutation. Use when updating a primitive, object, or array value and need the immutable equivalent of a mutating operation.
- [Immutability Patterns — Immer and Object.freeze](./04-immutability-patterns-immer-and-object-freeze.md) — How to use Immer for deep nested updates and Object.freeze for runtime immutability enforcement. Use when a nested object update is too deep for spread syntax, or you need to enforce immutability at runtime.
- [Pure Function Patterns](./05-pure-function-patterns.md) — Examples of basic pure functions, pure data transformations, and the functional core/imperative shell split. Use when writing a function and want a worked example of keeping it pure versus isolating its side effects.
- [Function Composition](./06-function-composition.md) — The pipe pattern, compose pattern, and higher-order functions for building complex behavior from simple functions. Use when you need to combine several small functions into a single pipeline or transformation.
- [Avoiding Common Pitfalls](./07-avoiding-common-pitfalls.md) — Common functional-programming mistakes - mutating function arguments, class-based mutable state, and mixing validation with I/O. Use when reviewing code for accidental mutation, mutable class state, or side effects mixed into pure logic.
- [TypeScript-Specific Patterns](./08-typescript-specific-patterns.md) — TypeScript-specific functional patterns - readonly types, branded types, and discriminated unions for state modeling. Use when you need a TypeScript-specific technique for enforcing immutability or modeling state explicitly.
- [Islamic Finance Example](./09-islamic-finance-example.md) — A worked Mudharabah profit-distribution example showing functional core/imperative shell applied to Shariah-compliant business logic. Use when you need a complete worked example of applying functional core/imperative shell to financial business logic.
- [When to Use Classes, Testing, Libraries, and Migration Strategy](./10-when-to-use-classes-testing-libraries-and-migration-strategy.md) — When classes are acceptable, how pure functions simplify testing, recommended functional libraries, and how to migrate an existing codebase incrementally. Use when deciding whether a class is appropriate, or planning an incremental migration to functional patterns.
- [Related Documentation and References](./11-related-documentation-and-references.md) — Links to related principles and conventions, plus external books and articles on functional programming. Use when you need a link to the underlying principle, or a book/article reference on functional programming.
