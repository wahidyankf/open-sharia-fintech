---
description: "Prefer immutable data structures over mutable state for safer, more predictable code"
when_to_use: "Read this index to find the right Immutability Over Mutability child document."
---

# Immutability Over Mutability

- [Vision Supported](./vision-supported.md) — Explains how immutability serves the Open Sharia Enterprise Vision by making concurrent Islamic finance systems safer and easier to audit. Use when explaining why immutability matters for Shariah-compliant, globally collaborative systems, not just as a coding style preference.
- [What](./what.md) — Defines immutability and mutability and contrasts their core characteristics. Use when clarifying the precise meaning of "immutable" versus "mutable" before applying the principle.
- [Why](./why.md) — Lists the benefits of immutability, the problems mutability causes, and when immutability should and should not be used. Use when justifying a choice to use (or avoid) immutable data structures in a design discussion or code review.
- [How It Applies](./how-it-applies.md) — Shows immutable versus mutable patterns for variables and array operations in TypeScript. Use when implementing immutable variable declarations or array updates and needing a concrete before/after example.
- [How It Applies — Immer and Frozen Objects](./how-it-applies-immer-and-frozen-objects.md) — Shows immutable object updates plus Immer and Object.freeze techniques for complex or runtime-enforced immutability. Use when updating deeply nested objects immutably or when runtime enforcement of immutability is required.
- [Anti-Patterns](./anti-patterns.md) — Catalogs common mutability anti-patterns — mutating function arguments, shared mutable state, and hidden mutations in methods — with fixes. Use when reviewing code for accidental mutation bugs or refactoring a mutable design toward immutability.
- [PASS: Best Practices](./pass-best-practices.md) — Summarizes six concrete best practices for writing immutable code, from const-by-default to typed readonly enforcement. Use as a quick checklist when writing or reviewing TypeScript code for immutability compliance.
- [Islamic Finance Example](./islamic-finance-example.md) — Walks through a Murabaha profit-distribution contract implemented with mutable versus immutable state to show the audit-trail difference. Use when implementing or reviewing Islamic finance calculation logic that must produce an auditable, Shariah-compliant history of state changes.
- [Relationship to Other Principles](./relationship-to-other-principles.md) — Links immutability to the pure functions, explicit-over-implicit, and simplicity-over-complexity principles it supports. Use when tracing how immutability connects to other repository-wide software engineering principles.
- [Related Conventions](./related-conventions.md) — Links to the functional programming, code quality, and implementation workflow conventions that operationalize immutability. Use when looking for the concrete conventions that enforce or implement immutability in this repository.
- [References](./references.md) — Lists external references on functional programming, immutability in practice, and Islamic finance transparency standards. Use when seeking further reading on immutability theory or Shariah audit and transparency requirements.
