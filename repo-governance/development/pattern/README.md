---
description: Reusable architecture and quality patterns for maintainable platform changes
when_to_use: "Use when a change needs a proven shape — an application boundary, an audit trail, or an independent review cycle."
---

# Development Patterns

Use these patterns when a change needs a proven shape, such as a clear application boundary, an audit trail, or an independent review cycle. They offer reusable choices, not permission to add complexity by default.

## Purpose

These patterns define **HOW to structure development workflows and code**, covering the Maker-Checker-Fixer quality workflow and functional programming practices. These are proven patterns that solve common development challenges.

## Scope

**✅ Belongs Here:**

- Reusable development patterns
- Workflow patterns (maker-checker-fixer)
- Programming paradigm practices (functional programming)
- Code organization patterns

**❌ Does NOT Belong:**

- Why we value patterns (that's a principle)
- Specific tool configuration (that's workflow/)
- Language-specific syntax (that's reference docs)

## Documents

- [Anti-Patterns in Development Patterns](./anti-patterns.md) — Common mistakes when applying the development patterns in this directory. Use when reviewing a change for a known anti-pattern.
- [Best Practices for Development Patterns](./best-practices.md) — Recommended techniques for applying the Maker-Checker-Fixer pattern and functional programming practices, with worked examples for each. Use when applying the Maker-Checker-Fixer pattern or functional programming practices and want a concrete good-example/bad-example pairing.
- [Database Audit Trail Pattern](./database-audit-trail.md) — Required 6-column audit trail for every database table in open-sharia-enterprise. Use when creating a database table or migration.
- [Functional Core / Imperative Shell — Web Apps](./functional-core-imperative-shell-web.md) — The architecture pattern for Next.js web apps — every feature module splits into a pure functional core and an effectful imperative shell under src/features/<name>/{core,shell}/. Use when structuring or reviewing a Next.js feature module, or deciding whether a file belongs in core/ or shell/.
- [Functional Programming Practices](./functional-programming.md) — Guidelines for applying functional programming principles in TypeScript/JavaScript. Use when writing or reviewing TypeScript/JavaScript business logic.
- [Hexagonal Architecture](./hexagonal-architecture.md) — Core hexagonal architecture pattern — ports, adapters, dependency rule, and app-type specializations. Use when structuring a backend or CLI app's layers, or deciding whether code belongs in domain, application, infrastructure, or an adapter.
- [Hexagonal Architecture + DDD — Backend Apps](./hexagonal-architecture-be.md) — Hexagonal architecture with DDD bounded contexts for backend apps — F#/Giraffe directory layouts, language-specific idioms, and inter-context isolation rules. Use when structuring a backend bounded context, wiring F# dependency injection, or mapping a domain error to an HTTP response.
- [Hexagonal Architecture — CLI Apps](./hexagonal-architecture-cli.md) — Hexagonal architecture specialization for CLI apps — commands as inbound adapters, layer responsibilities, and forbidden imports. Use when structuring a CLI app's commands/, domain/, application/, or infrastructure/ layer.
- [Maker-Checker-Fixer Pattern Convention](./maker-checker-fixer.md) — Three-stage content quality workflow used across multiple agent families. Use when designing or invoking a maker/checker/fixer agent trio.
- [OpenAPI Contract-First Development](./openapi-contract-first.md) — Spec-first API development — the OpenAPI YAML is the single source of truth; code is generated from it, not the reverse. Use when adding or changing an API endpoint, running codegen, or debugging a CI spec/codegen drift failure.

## Related Documentation

- [Development Index](../README.md) - All development practices
- [Pure Functions Over Side Effects Principle](../../principles/software-engineering/pure-functions.md) - Why functional programming matters
- [Immutability Over Mutability Principle](../../principles/software-engineering/immutability.md) - Why immutability matters
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model

## Principles Implemented/Respected

- **[Immutability Over Mutability](../../principles/software-engineering/immutability.md)**: Functional programming practices favor immutable data structures and pure functions, reducing side effects and improving code predictability.

- **[Pure Functions Over Side Effects](../../principles/software-engineering/pure-functions.md)**: Functional programming guidelines emphasize pure functions for deterministic, testable, and composable code.

## Conventions Implemented/Respected

- **[Content Quality Principles](../../conventions/writing/quality.md)**: Pattern documentation follows active voice, clear structure, and proper formatting standards.

- **[Criticality Levels Convention](../quality/criticality-levels.md)**: Maker-Checker-Fixer pattern integrates with criticality assessment to prioritize and validate fixes systematically.
