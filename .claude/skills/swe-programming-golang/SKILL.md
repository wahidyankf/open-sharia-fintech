---
name: swe-programming-golang
description: Go coding standards quick reference for agents authoring Go code (primarily for downstream ose-primer; ose-public itself has no active Go apps)
---

# Go Coding Standards

## Purpose

Progressive disclosure of Go coding standards for agents writing Go code.

> **Scope note**: `ose-public` no longer ships a Go style-guide tree under
> `docs/explanation/software-engineering/programming-languages/golang/` (Go was removed from active
> apps 2026-05-23; CLIs are now Rust). This skill is retained because `swe-golang-dev` authors Go
> for the downstream [`ose-primer`](https://github.com/wahidyankf/ose-primer) template, which is
> the authoritative source for OSE Go conventions. Use the AyoKoding educational content below for
> universal Go idioms.

**Educational Resource**: [AyoKoding Go Learning Path](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/)

**Usage**: Auto-loaded for agents when writing Go code. Provides quick reference to idioms, best practices, and antipatterns.

## Prerequisite Knowledge

**IMPORTANT**: This skill provides **OSE Platform-specific style guides**, not educational tutorials.

**You MUST understand Go fundamentals before using these standards.** Complete the AyoKoding Go learning path first:

1. **[Go Learning Path](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/)** — Initial setup, language overview, quick start guide
2. **[Go By Example](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/by-example/)** — 75+ heavily annotated code examples (beginner to advanced patterns)
3. **[Go In the Field](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/in-the-field/)** — Production implementation guides (standard library first, framework integration)
4. **[Go Release Highlights](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/release-highlights/)** — Go 1.18+ features (generics, fuzzing, PGO, iterators, Green Tea GC)

**What this skill covers**: OSE Platform naming conventions, framework choices, repository-specific patterns, how to apply Go knowledge in THIS codebase (and in ose-primer).

**What this skill does NOT cover**: Go syntax, language fundamentals, generic patterns (those are in ayokoding-web).

**See**: [Programming Language Documentation Separation](../../../repo-governance/conventions/structure/programming-language-docs-separation.md) for content separation rules.

## Quick Standards Reference

- [Naming and Modern Features](./reference/naming-and-modern-features.md) — naming conventions, generics, error wrapping/comparison, sum types, doc comments, struct embedding
- [Error Handling, Concurrency, Testing, Security](./reference/error-handling-concurrency-testing-security.md) — error returns/custom types, goroutines/channels/context, table-driven tests, input validation

## Comprehensive Documentation

**OSE Platform Go standards** now live in the downstream
[`ose-primer`](https://github.com/wahidyankf/ose-primer) template (authoritative for Go conventions
in OSE-derived projects). `ose-public` itself has no active Go apps.

**AyoKoding educational content** (universal Go idioms — use for fundamentals and patterns):

- [Go Learning Path](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/)
- [Go By Example](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/by-example/)
- [Go In the Field](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/in-the-field/)
- [Go Release Highlights](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/release-highlights/)

## Test-Driven Development

TDD is required for all Go code changes. Write the failing test first using Go `testing` (or a
Godog step definition consuming a Gherkin scenario from `specs/apps/<app-name>/`), confirm it fails
for the right reason, implement the minimum code to pass, then refactor. For Go CLI projects the
primary levels are unit (Go `testing` + Godog, mocked I/O via package-level function vars) and
integration (Godog `//go:build integration` + real `/tmp` filesystem). Property-based testing via
gopter covers invariants over generated inputs.

**Canonical reference**:
[Test-Driven Development Convention](../../../repo-governance/development/workflow/test-driven-development.md)

## Related Skills

- repo-practicing-trunk-based-development
- docs-applying-content-quality

## References

- [AyoKoding Go Overview](../../../apps/ayokoding-www/content/en/learn/software-engineering/programming-languages/golang/)
- [Functional Programming](../../../repo-governance/development/pattern/functional-programming.md)
- [Programming Language Docs Separation](../../../repo-governance/conventions/structure/programming-language-docs-separation.md)
