---
title: "Development Patterns"
description: Reusable architecture and quality patterns for maintainable platform changes
category: explanation
subcategory: development
tags: []
created: 2026-05-12
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

- [Database Audit Trail Pattern](./database-audit-trail.md) - Required 6-column audit trail (created_at/by, updated_at/by, deleted_at/by) for every database table. Covers language-agnostic migration requirements, F#/DbUp patterns (versioned SQL scripts, EF Core entity mapping), and soft-delete discipline
- [Functional Core / Imperative Shell — Web Apps](./functional-core-imperative-shell-web.md) - Next.js pattern: every `features/<name>/` module splits into a pure `core/` and an effectful `shell/` (React/IO/wiring); deliberately not hexagonal/DDD
- [Functional Programming Practices](./functional-programming.md) - Guidelines for applying functional programming principles in TypeScript/JavaScript (immutability patterns, pure functions, function composition)
- [Hexagonal Architecture](./hexagonal-architecture.md) - Core ports-and-adapters pattern: dependency rule, layer definitions (domain, application, infrastructure, inbound adapters), and links to app-type specializations
- [Hexagonal Architecture — CLI Apps](./hexagonal-architecture-cli.md) - CLI specialization: `commands/` as inbound adapter, canonical directory layouts for rhino-cli/crane-cli/ose-cli/ayokoding-cli, layer responsibilities, and forbidden imports
- [Hexagonal Architecture + DDD — Backend Apps](./hexagonal-architecture-be.md) - Backend specialization with DDD bounded contexts: F#/Giraffe directory layouts, error mapping at the API boundary, and inter-context isolation rules
- [Maker-Checker-Fixer Pattern](./maker-checker-fixer.md) - Three-stage quality workflow for content creation and validation with user review gates and confidence level integration
- [OpenAPI Contract-First Development](./openapi-contract-first.md) - Spec-first API development: OpenAPI YAML as single source of truth, codegen tooling per language, Nx targets, and CI drift enforcement

## Companion Documents

- [Anti-Patterns](./anti-patterns.md) - Common pattern mistakes to avoid (with examples and corrections)
- [Best Practices](./best-practices.md) - Recommended pattern techniques and guidelines

## Related Documentation

- [Development Index](../README.md) - All development practices
- [Pure Functions Over Side Effects Principle](../../principles/software-engineering/pure-functions.md) - Why functional programming matters
- [Immutability Over Mutability Principle](../../principles/software-engineering/immutability.md) - Why immutability matters
- [Repository Architecture](../../repository-governance-architecture.md) - Six-layer governance model

## Principles Implemented/Respected

This set of development practices implements/respects the following core principles:

- **[Immutability Over Mutability](../../principles/software-engineering/immutability.md)**: Functional programming practices favor immutable data structures and pure functions, reducing side effects and improving code predictability.

- **[Pure Functions Over Side Effects](../../principles/software-engineering/pure-functions.md)**: Functional programming guidelines emphasize pure functions for deterministic, testable, and composable code.

## Conventions Implemented/Respected

This set of development practices respects the following conventions:

- **[Content Quality Principles](../../conventions/writing/quality.md)**: Pattern documentation follows active voice, clear structure, and proper formatting standards.

- **[Criticality Levels Convention](../quality/criticality-levels.md)**: Maker-Checker-Fixer pattern integrates with criticality assessment to prioritize and validate fixes systematically.
