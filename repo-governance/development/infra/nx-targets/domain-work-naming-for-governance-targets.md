---
title: "`{domain}:{work}` Naming for Governance and Validation Targets"
description: Defines the {domain}:{work} naming scheme for governance, validation, lint, and format targets, with the canonical target list.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when adding a new governance or validation Nx target and deciding its key name.
---

# `{domain}:{work}` Naming for Governance and Validation Targets

Governance, validation, lint, and format targets use the `{domain}:{work}` scheme rather than the
`validate:*` prefix. The domain names the scope or subject of the check; the work names the
operation. This distinguishes governance targets from language-level lifecycle targets
(`test:quick`, `build`, etc.) and makes the Nx target list self-describing.

**Canonical governance and validation targets** (defined on `rhino-cli`):

| Target                                 | What it validates                                                                          |
| -------------------------------------- | ------------------------------------------------------------------------------------------ |
| `specs:behavior:coverage`              | Gherkin feature/scenario coverage at the behavior level (renamed from `specs:coverage`)    |
| `specs:domain:coverage`                | Domain-area coverage gated by the `specs.domain-areas` allowlist in `repo-config.yml`      |
| `specs:structure-validation`           | Adoption + tree shape + counts validated together (merged from three removed leaf targets) |
| `specs:gherkin-cardinality-validation` | Each Gherkin keyword used within cardinality bounds                                        |
| `links:validation`                     | Internal links in all non-excluded `.md` files                                             |
| `mermaid:validation`                   | Mermaid diagram width, label, and syntax rules (flowchart + state)                         |
| `headings:hierarchy-validation`        | Heading nesting in prose allowlist paths                                                   |
| `env:validation`                       | `.env.example` surfaces match the `env-contract:` section in `repo-config.yml`             |
| `governance:vendor-audit-validation`   | `repo-governance/` docs contain no vendor-specific content                                 |
| `cross-vendor:parity-validation`       | Cross-vendor behavioral parity (Phase 0 deterministic invariants)                          |
| `governance-word-budget:validation`    | Word budget on auto-loaded instruction files (`AGENTS.md`, `CLAUDE.md`, harness surfaces)  |
| `governance-readme-index:validation`   | README index audit (`docs/`, `repo-governance/`, `specs/`, `.claude/`)                     |
| `harness:bindings-validation`          | `.claude/` ↔ `.opencode/` ↔ `.amazonq/` binding parity                                     |
| `compat:min-version`                   | Minimum Supported Rust Version compatibility                                               |

**Rule**: governance/validation target keys are `{domain}:{work}` where both parts are lowercase
kebab-case. The domain must be a recognizable noun (the scope); the work must be a verb phrase
ending in `-validation` (for pure checks) or a bare verb (`check`). Do not invent `validate:*`
prefixes — use the canonical list above or follow the `{domain}:{work}` pattern.

See [nx-target-naming.md](../nx-target-naming.md) for the full derivation rule and examples.
