---
description: Confirms this convention applies to every current and future repository language, and how docs/explanation/ style guides must align with the five software engineering principles
when_to_use: Read this when adding a new programming language's style guide, or verifying a style guide aligns with the repository's software engineering principles.
---

# Scope for All Programming Languages, and Alignment with Software Engineering Principles

## Scope for All Programming Languages

This convention applies to **every** language that carries a `docs/explanation/` style guide. A
style guide exists only while this repository builds something in that language, so the set is
small and moves — read the
[`programming-languages/README.md`](../../../../docs/explanation/software-engineering/programming-languages/README.md)
index rather than a list restated here. Today it is TypeScript, Rust, and F#.

AyoKoding teaches many more languages than that. Educational content for a language with **no**
style guide has nothing to separate from — the no-duplication and prerequisite rules bind only
where both sides exist.

**Future languages**: apply the same separation pattern the moment a new language earns a style
guide.

## Alignment with Software Engineering Principles

Programming language style guides in `docs/explanation/` MUST align with the software engineering principles from [repo-governance/principles/software-engineering/](../../../principles/software-engineering/README.md):

### 1. Automation Over Manual

Style guides document automated tooling:

- Linters (Clippy for Rust, ESLint for TypeScript)
- Formatters (`cargo fmt`, Prettier, `dotnet format`)
- Code generators (OpenAPI contract codegen)
- CI/CD pipelines enforcing standards

### 2. Explicit Over Implicit

Style guides enforce explicitness:

- Explicit error handling (no silent failures)
- Explicit configuration (no hidden magic)
- Explicit imports (no wildcards)
- Explicit types where beneficial

### 3. Immutability Over Mutability

Style guides encourage immutable patterns:

- Value objects and immutable data structures
- Functional approaches where applicable
- Const correctness and readonly semantics

### 4. Pure Functions Over Side Effects

Style guides promote pure functions:

- Functional core, imperative shell architecture
- Pure domain logic, isolated side effects
- Testable business logic without mocks

### 5. Reproducibility First

Style guides enable reproducible builds:

- Dependency version pinning (`Cargo.toml`, `package.json`, `*.fsproj`)
- Lockfiles (`Cargo.lock`, `package-lock.json`)
- Docker build reproducibility

**Example alignment** (Rust):

```markdown
## Software Engineering Principles

Rust development in OSE Platform follows the software engineering principles:

1. **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)** - Rust automates through Clippy, `cargo fmt`, `cargo test`, `cargo-llvm-cov`
2. **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)** - Rust enforces through `Result`-typed error handling and no implicit conversions
3. **[Immutability Over Mutability](../../principles/software-engineering/immutability.md)** - Rust encourages through bindings immutable by default and `mut` opted into
4. **[Pure Functions Over Side Effects](../../principles/software-engineering/pure-functions.md)** - Rust supports through a functional core with IO pushed to the shell
5. **[Reproducibility First](../../principles/software-engineering/reproducibility.md)** - Rust enables through `Cargo.lock` and a pinned toolchain

See [Rust README](./README.md#purpose) for detailed examples.
```
