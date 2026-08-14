---
title: "Programming Language Docs Separation: Scope for All Languages and Alignment with SE Principles"
description: Confirms this convention applies to every current and future repository language, and how docs/explanation/ style guides must align with the five software engineering principles
when_to_use: Read this when adding a new programming language's style guide, or verifying a style guide aligns with the repository's software engineering principles.
category: explanation
subcategory: conventions
tags:
  - documentation
  - programming-languages
  - style-guides
  - content-separation
  - dry-principle
created: 2026-02-04
---

# Scope for All Programming Languages, and Alignment with Software Engineering Principles

## Scope for All Programming Languages

This convention applies to **ALL** programming languages in the repository:

**Current languages**:

- Java (JVM) - `docs/explanation/.../java/`, `apps/ayokoding-www/.../java/`
- Kotlin (JVM) - `docs/explanation/.../kotlin/`, `apps/ayokoding-www/.../kotlin/`
- Python - `docs/explanation/.../python/`, `apps/ayokoding-www/.../python/`
- TypeScript (Node.js) - `docs/explanation/.../typescript/`, `apps/ayokoding-www/.../typescript/`
- Elixir (BEAM) - `docs/explanation/.../elixir/`, `apps/ayokoding-www/.../elixir/`
- Dart (Flutter) - `docs/explanation/.../dart/`, `apps/ayokoding-www/.../dart/`
- Rust - `docs/explanation/.../rust/`, `apps/ayokoding-www/.../rust/`
- Clojure (JVM) - `docs/explanation/.../clojure/`, `apps/ayokoding-www/.../clojure/`
- F# (.NET) - `docs/explanation/.../f-sharp/`, `apps/ayokoding-www/.../f-sharp/`
- C# (.NET) - `docs/explanation/.../c-sharp/`, `apps/ayokoding-www/.../c-sharp/`

**Future languages**: Apply same separation pattern when adding new languages.

## Alignment with Software Engineering Principles

Programming language style guides in `docs/explanation/` MUST align with the software engineering principles from [repo-governance/principles/software-engineering/](../../../principles/software-engineering/README.md):

### 1. Automation Over Manual

Style guides document automated tooling:

- Linters (golangci-lint for Go, Ruff for Python)
- Formatters (gofmt for Go, Black for Python)
- Code generators (protoc for gRPC)
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

- Dependency version pinning (go.mod, requirements.txt)
- Lockfiles (go.sum, poetry.lock)
- Docker build reproducibility

**Example alignment** (Golang):

```markdown
## Software Engineering Principles

Go development in OSE Platform follows the software engineering principles:

1. **[Automation Over Manual](../../principles/software-engineering/automation-over-manual.md)** - Go automates through golangci-lint, gofmt, go test, code generation
2. **[Explicit Over Implicit](../../principles/software-engineering/explicit-over-implicit.md)** - Go enforces through explicit error handling, no hidden control flow
3. **[Immutability Over Mutability](../../principles/software-engineering/immutability.md)** - Go encourages through value receivers, const correctness
4. **[Pure Functions Over Side Effects](../../principles/software-engineering/pure-functions.md)** - Go supports through functional core architecture
5. **[Reproducibility First](../../principles/software-engineering/reproducibility.md)** - Go enables through go.mod, go.sum, reproducible builds

See [Golang README](./README.md#purpose) for detailed examples.
```
