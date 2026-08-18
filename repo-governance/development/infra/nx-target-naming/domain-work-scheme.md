---
title: "Scheme 2 — `{domain}:{work}` for Governance and Validation Targets"
description: Derivation rule and the canonical target table for the `{domain}:{work}` naming scheme used by governance, validation, lint, and format Nx targets.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - naming
  - conventions
created: 2026-06-13
when_to_use: Use when naming a new governance, validation, lint, or format Nx target, or checking an existing `{domain}:{work}` target name against the canonical list.
---

# Scheme 2 — `{domain}:{work}` for Governance and Validation Targets

Governance, validation, lint, and format targets use `{domain}:{work}` where:

- **domain**: lowercase noun naming the subject or scope of the check (e.g., `specs`,
  `links`, `mermaid`, `env`, `naming`, `governance`, `cross-vendor`, `harness`,
  `format`, `msrv`).
- **work**: lowercase verb phrase naming the operation. Pure checks end in `-validation`.
  Bare operations use a single verb (`check`).

**Rule**: do not invent `validate:{thing}` prefixes. The old `validate:*` naming scheme was
retired in P10 (2026-06-12); any `validate:` target in `project.json` or a caller script
is a bug.

## Canonical Governance and Validation Targets

All defined on `rhino-cli`. Other projects expose `specs:coverage` only.

| Target                                 | Subject                   | Operation                                                     |
| -------------------------------------- | ------------------------- | ------------------------------------------------------------- |
| `specs:coverage`                       | Gherkin specs             | Validate every step has a step definition                     |
| `specs:tree-validation`                | Specs directory tree      | Validate structure matches app registrations                  |
| `specs:counts-validation`              | Spec scenario/step counts | Validate counts meet thresholds                               |
| `specs:adoption-validation`            | App registrations         | Validate every app has a spec directory                       |
| `specs:gherkin-cardinality-validation` | Gherkin keyword usage     | Validate keyword cardinality within bounds                    |
| `links:validation`                     | All `.md` files           | Validate internal + anchor links                              |
| `mermaid:validation`                   | Mermaid diagrams          | Validate width, label length, syntax (flowchart + state)      |
| `headings:hierarchy-validation`        | Prose `.md` files         | Validate heading nesting on allowlist paths                   |
| `env:validation`                       | `.env.example` files      | Validate against `env-contract:` section in `repo-config.yml` |
| `naming:harness-validation`            | Agent definition files    | Validate names match naming convention                        |
| `naming:workflows-validation`          | Workflow files            | Validate names match naming convention                        |
| `governance:vendor-audit-validation`   | `repo-governance/` docs   | Validate no vendor-specific content leakage                   |
| `cross-vendor:parity-validation`       | All binding trees         | Validate cross-vendor behavioral parity                       |
| `harness:bindings-validation`          | Binding artifacts         | Validate `.claude/` ↔ `.opencode/` ↔ `.amazonq/` parity       |
| `format:check`                         | Rust source               | `rustfmt --check`                                             |
| `compat:min-version`                   | Rust toolchain            | Minimum Supported Rust Version compatibility                  |
