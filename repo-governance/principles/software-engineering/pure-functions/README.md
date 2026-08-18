---
title: "Pure Functions Over Side Effects"
description: "Prefer pure functions (deterministic, no side effects) for predictable, testable code"
when_to_use: "Read this index to find the right Pure Functions Over Side Effects child document."
---

# Pure Functions Over Side Effects

- [Vision Supported](./vision-supported.md) — Explains how pure functions make Shariah-compliant business logic verifiable, auditable, and trustworthy. Use when explaining why pure functions matter for auditable, transparent Islamic finance logic.
- [What](./what.md) — Defines pure and impure functions and contrasts their determinism, side-effect, and referential-transparency characteristics. Use when clarifying the precise meaning of "pure function" before applying the principle.
- [Why](./why.md) — Lists the benefits of pure functions, the problems side effects cause, and when each applies. Use when justifying a choice to isolate side effects and keep logic pure.
- [How It Applies](./how-it-applies.md) — Shows pure versus impure patterns for calculating Zakat and distributing Musharakah profit shares in TypeScript. Use when implementing a business-logic calculation and needing a concrete pure-versus-impure example.
- [How It Applies — Functional Core and Hidden Dependencies](./how-it-applies-functional-core-and-hidden-dependencies.md) — Shows the Functional Core, Imperative Shell pattern and how to avoid hidden global-config dependencies. Use when separating pure logic from I/O or removing a hidden dependency on global state.
- [Anti-Patterns](./anti-patterns.md) — Catalogs common purity anti-patterns — side-effecting functions, hidden randomness, reading current time, and global state dependencies — with fixes. Use when reviewing code for hidden non-determinism or side effects and refactoring toward pure functions.
- [PASS: Best Practices](./pass-best-practices.md) — Summarizes six concrete best practices for writing pure functions, from explicit dependencies to mock-free testing. Use as a quick checklist when writing or reviewing TypeScript code for purity compliance.
- [Islamic Finance Example](./islamic-finance-example.md) — Walks through a Mudharabah profit-distribution calculation implemented with impure versus pure functions to show the verifiability difference. Use when implementing Islamic finance profit-sharing logic that must be independently verifiable.
- [Relationship to Other Principles](./relationship-to-other-principles.md) — Links pure functions to the immutability, explicit-over-implicit, simplicity-over-complexity, and automation-over-manual principles they support. Use when tracing how pure functions connect to other repository-wide software engineering principles.
- [Related Conventions](./related-conventions.md) — Links to the functional programming, code quality, and implementation workflow conventions that operationalize pure functions. Use when looking for the concrete conventions that enforce or implement pure functions in this repository.
- [References](./references.md) — Lists external references on functional programming, testing pure functions, the Functional Core/Imperative Shell pattern, and Islamic finance standards. Use when seeking further reading on pure-function theory, testing practice, or Shariah transparency requirements.
