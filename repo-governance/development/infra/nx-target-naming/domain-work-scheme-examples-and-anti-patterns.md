---
description: Worked derivation examples and forbidden-vs-correct anti-pattern pairs for the `{domain}:{work}` governance and validation Nx target naming scheme.
when_to_use: Use when deriving a new `{domain}:{work}` target name from a subject and operation, or checking a proposed name against known anti-patterns.
---

# Derivation Examples and Anti-Patterns for the `{domain}:{work}` Scheme

## Derivation Examples

| Subject scope              | Operation      | Derived target                       |
| -------------------------- | -------------- | ------------------------------------ |
| `specs` (Gherkin)          | check adoption | `specs:adoption-validation`          |
| `links` (markdown)         | validate       | `links:validation`                   |
| `mermaid` (diagrams)       | validate       | `mermaid:validation`                 |
| `governance` (vendor docs) | audit          | `governance:vendor-audit-validation` |
| `format` (Rust fmt)        | check          | `format:check`                       |

## Anti-Patterns

| Forbidden                 | Correct                     | Reason                                 |
| ------------------------- | --------------------------- | -------------------------------------- |
| `validate:mermaid`        | `mermaid:validation`        | `validate:*` prefix abolished          |
| `validate:links`          | `links:validation`          | same                                   |
| `validate:specs-adoption` | `specs:adoption-validation` | same                                   |
| `spec-coverage`           | `test:coverage:behaviour`   | Hyphen dropped; domain clarified       |
| `fmt:check`               | `format:check`              | Domain must be the noun (`format`)     |
| `check:msrv`              | `compat:min-version`        | Verb follows domain: `{domain}:{verb}` |
