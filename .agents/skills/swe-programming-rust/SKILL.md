---
name: swe-programming-rust
description: Rust coding standards from authoritative docs/explanation/software-engineering/programming-languages/rust/ documentation
---

# Rust Coding Standards

## Purpose

Progressive disclosure of Rust coding standards for agents writing Rust code.

**Usage**: Auto-loaded for agents when writing Rust code. Provides quick reference to idioms, best practices, and antipatterns.

**Authoritative Source**: [docs/explanation/software-engineering/programming-languages/rust/README.md](../../../docs/explanation/software-engineering/programming-languages/rust/README.md)

## Prerequisite Knowledge

**IMPORTANT**: This skill provides **OSE Platform-specific style guides**, not educational tutorials.

Complete the AyoKoding Rust learning path first:

1. **[Rust Learning Path](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/rust/)** - 0-95% language coverage
2. **[Rust By Example](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/rust/by-example/)** - 75+ annotated examples

**See**: [Programming Language Documentation Separation](../../../repo-governance/conventions/structure/programming-language-docs-separation.md)

## Quick Standards Reference

- [Naming, Errors, Ownership, Iterators, Newtype, Async](./reference/naming-errors-ownership-async.md) — naming conventions, thiserror/Result patterns, borrowing, iterator combinators, newtype IDs, Axum handlers
- [Unsafe Policy, Cargo.toml, Clippy/rustfmt](./reference/unsafe-policy-cargo-lints.md) — `forbid(unsafe_code)` in lib.rs+main.rs, required Cargo.toml structure, `[lints.clippy]` config, pre-commit commands

## Comprehensive Documentation

**Authoritative Index**: [docs/explanation/software-engineering/programming-languages/rust/README.md](../../../docs/explanation/software-engineering/programming-languages/rust/README.md)

### Mandatory Standards

1. **[Coding Standards](../../../docs/explanation/software-engineering/programming-languages/rust/coding-standards.md)**
2. **[Testing Standards](../../../docs/explanation/software-engineering/programming-languages/rust/testing-standards.md)**
3. **[Code Quality Standards](../../../docs/explanation/software-engineering/programming-languages/rust/code-quality-standards.md)**
4. **[Build Configuration](../../../docs/explanation/software-engineering/programming-languages/rust/build-configuration.md)**

### Context-Specific Standards

1. **[Error Handling](../../../docs/explanation/software-engineering/programming-languages/rust/error-handling-standards.md)**
2. **[Concurrency](../../../docs/explanation/software-engineering/programming-languages/rust/concurrency-standards.md)**
3. **[Memory Management](../../../docs/explanation/software-engineering/programming-languages/rust/memory-management-standards.md)**
4. **[Type Safety](../../../docs/explanation/software-engineering/programming-languages/rust/type-safety-standards.md)**
5. **[Performance](../../../docs/explanation/software-engineering/programming-languages/rust/performance-standards.md)**
6. **[Security](../../../docs/explanation/software-engineering/programming-languages/rust/security-standards.md)**
7. **[API Standards](../../../docs/explanation/software-engineering/programming-languages/rust/api-standards.md)**
8. **[DDD Standards](../../../docs/explanation/software-engineering/programming-languages/rust/ddd-standards.md)**

## Related Skills

- docs-applying-content-quality
- repo-practicing-trunk-based-development

## References

- [Rust README](../../../docs/explanation/software-engineering/programming-languages/rust/README.md)
- [Functional Programming](../../../repo-governance/development/pattern/functional-programming.md)
