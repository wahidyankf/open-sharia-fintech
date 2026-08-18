---
title: "Parity Checklist — Invariants E, F, and G"
description: Nx naming scheme, governance-currency checklist, Mermaid rules.
category: explanation
subcategory: development
tags: [ci-cd, nx]
created: 2026-03-31
when_to_use: Use when naming a target or writing a state diagram.
---

# Parity Checklist — Invariants E, F, and G

## Invariant E — Nx Target Naming (`{domain}:{work}`)

Governance, validation, lint, and format targets use the `{domain}:{work}` scheme.
`spec-coverage` is renamed `specs:coverage` repo-wide.

Rust-specific renames applied to all Rust `project.json` files:

| Old name     | New name             |
| ------------ | -------------------- |
| `fmt:check`  | `format:check`       |
| `check:msrv` | `compat:min-version` |
| `deny:check` | `deps:audit`         |

The full naming rationale and complete target catalog are documented in
[Nx Target Standards](../nx-targets.md).

## Invariant F — Governance Documentation Currency

All documentation in `repo-governance/` must reflect the converged toolchain. After any P10-class
rename or command-surface change, update:

1. `repo-governance/development/infra/ci-conventions.md` (this file) — pre-push section + checklist
2. `repo-governance/development/infra/nx-targets.md` — target name tables + `{domain}:{work}` naming section
3. `AGENTS.md` — Cross-Language Lint Gates section + rhino-cli command surface
4. `apps/rhino-cli/README.md` — command surface table + hexagonal layout diagram
5. Any index READMEs that reference renamed targets

Stale `validate:*` or `spec-coverage` references in any of the above are bugs caught by
`rhino-cli:links:validation` fragment checks and by the Parity Checklist gate in the plan delivery
process.

## Invariant G — Mermaid State Diagram Validation

`stateDiagram-v2` and `stateDiagram` (v1) diagrams are subject to the same width and label rules
as flowchart diagrams:

- **Width**: State node count contributes to the diagram width calculation. Diagrams exceeding
  the width limit must be split or redesigned.
- **Label length**: State display names and transition edge labels are limited to 30 characters.
  Use abbreviations or split composite states when labels exceed this limit.

Both rules are enforced by `rhino-cli:mermaid:validation`, which scans the entire repo (excluding
`plans/done/`, `apps/ayokoding-www/content/`, and the standard noise-skip set).
