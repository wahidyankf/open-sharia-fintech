---
name: swe-programming-fsharp
description: F# coding standards from authoritative docs/explanation/software-engineering/programming-languages/f-sharp/ documentation
---

# F# Coding Standards

## Purpose

Progressive disclosure of F# coding standards for agents writing F# code.

**Authoritative Source**: [docs/explanation/software-engineering/programming-languages/f-sharp/README.md](../../../docs/explanation/software-engineering/programming-languages/f-sharp/README.md)

**Usage**: Auto-loaded for agents when writing F# code. Provides quick reference to idioms, best practices, and antipatterns.

## Prerequisite Knowledge

**IMPORTANT**: This skill provides **OSE Platform-specific style guides**, not educational tutorials.

**You MUST understand F# fundamentals before using these standards.** Complete the AyoKoding F# learning path first:

1. **[F# Learning Path](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/f-sharp/)** - Initial setup, language overview, quick start guide (0-95% language coverage)
2. **[F# By Example](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/f-sharp/by-example/)** - 75+ annotated code examples (beginner to advanced patterns)

**What this skill covers**: OSE Platform naming conventions, framework choices, repository-specific patterns, how to apply F# knowledge in THIS codebase.

**What this skill does NOT cover**: F# syntax, language fundamentals, generic patterns (those are in ayokoding-web).

**See**: [Programming Language Documentation Separation](../../../repo-governance/conventions/structure/programming-language-docs-separation.md) for content separation rules.

## Quick Standards Reference

- [Naming, DUs, Railway, Pipeline](./reference/qs-naming-and-railway.md) — naming conventions, discriminated unions, railway-oriented programming, pipeline operator
- [Records, Async, Formatting, Testing](./reference/qs-records-async-testing.md) — immutable records, async workflows, Fantomas formatting, Expecto/FsCheck testing

## Comprehensive Documentation

**Authoritative Index**: [docs/explanation/software-engineering/programming-languages/f-sharp/README.md](../../../docs/explanation/software-engineering/programming-languages/f-sharp/README.md)

### Mandatory Standards (All F# Code MUST Follow)

1. **[Coding Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/coding-standards.md)** - F# naming conventions, module organization, pipeline idioms
2. **[Testing Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/testing-standards.md)** - Expecto, FsCheck property-based testing, AltCover coverage
3. **[Code Quality Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/code-quality-standards.md)** - Fantomas, FSharpLint, exhaustive pattern matching
4. **[Build Configuration](../../../docs/explanation/software-engineering/programming-languages/f-sharp/build-configuration.md)** - .fsproj file order, dotnet CLI, Nx integration

### Context-Specific Standards (Apply When Relevant)

1. **[Error Handling Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/error-handling-standards.md)** - Result type, railway-oriented programming, computation expressions
2. **[Concurrency Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/concurrency-standards.md)** - Async workflows, MailboxProcessor, Task interop
3. **[Functional Programming Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/functional-programming-standards.md)** - Computation expressions, monads, applicatives
4. **[Type Safety Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/type-safety-standards.md)** - DUs, units of measure, phantom types
5. **[Performance Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/performance-standards.md)** - Tail recursion, sequences, lazy evaluation
6. **[Security Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/security-standards.md)** - Type-driven validation, Giraffe authentication
7. **[API Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/api-standards.md)** - Giraffe HttpHandler composition, Saturn routing
8. **[DDD Standards](../../../docs/explanation/software-engineering/programming-languages/f-sharp/ddd-standards.md)** - DU-based domain modeling, making illegal states unrepresentable

## Related Skills

- docs-applying-content-quality
- repo-practicing-trunk-based-development

## References

- [F# README](../../../docs/explanation/software-engineering/programming-languages/f-sharp/README.md)
- [Functional Programming](../../../repo-governance/development/pattern/functional-programming.md)
