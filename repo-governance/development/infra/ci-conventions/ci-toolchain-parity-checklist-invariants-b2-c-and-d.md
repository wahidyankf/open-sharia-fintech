---
title: "Parity Checklist — Invariants B2, C, and D"
description: No-heavy-tests, hexagonal layout, and command-surface rules.
category: explanation
subcategory: development
tags: [ci-cd, testing]
created: 2026-03-31
when_to_use: Use when checking a test target's gate or rhino-cli's layers.
---

# Parity Checklist — Invariants B2, C, and D

## Invariant B2 — No Heavy Tests in Fast Gates

`test:integration` and `test:e2e` are heavy (docker-compose, Playwright, real services). They run
**only** in the scheduled tiered pipelines and must never appear on the fast feedback path. See
tech-docs §"Fast-gate test policy" for the rationale and the current compliance state.

| Surface                           | Runs                                                                                                                                   | `test:integration` / `test:e2e`? |
| --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------- |
| `.husky/pre-commit`               | Registry-declared `pre-commit`-surface gates via `gate run` (no test target — formatters/linters)                                      | **never**                        |
| `.husky/pre-push`                 | Registry-declared `pre-push`-surface gates via `gate run`, including `test:quick` (no `specs:behavior:coverage` — lifted out per DD-7) | **never**                        |
| `pr-quality-gate` (PR gate)       | `typecheck`, `lint`, `test:quick`, `specs:behavior:coverage` + lint jobs                                                               | **never**                        |
| `*-test-local-*` (CRON scheduled) | `test:integration` + `test:e2e` via docker-compose                                                                                     | **yes**                          |
| `*-test-stag-*` (CRON scheduled)  | `test:e2e` against deployed staging                                                                                                    | **yes**                          |

Any workflow that wires `test:integration` or `test:e2e` into a `pull_request` or `push` trigger
(rather than a `schedule` trigger) violates this invariant and must be corrected or removed before
merging. The deletion of `test-crane-cli-integration.yml` (which ran `crane-cli:test:integration`
on `pull_request`) was the remediation action that eliminated the last known violation.

## Invariant C — rhino-cli Hexagonal Architecture

Source tree layout:

| Layer                     | Path                  | Constraint                                      |
| ------------------------- | --------------------- | ----------------------------------------------- |
| Domain (pure)             | `src/domain/`         | No I/O; no `std::fs`, no HTTP, no env reads     |
| Application (use cases)   | `src/application/`    | Calls domain; injects infrastructure via trait  |
| Infrastructure (adapters) | `src/infrastructure/` | All I/O lives here (filesystem, network, env)   |
| CLI (inbound adapter)     | `src/commands/`       | Parses CLI args; delegates to application layer |

No file in `src/domain/` may import from `src/infrastructure/`. Violations fail `clippy`.

## Invariant D — rhino-cli Command Surface (Union Superset)

All callers (pre-push hook, CI workflows, `package.json` scripts) must use the canonical command
form `rhino {group} {verb} [{noun}]`. The `validate:*` prefix used before P10 is abolished.

Deprecated prefix→canonical mapping reference:

| Old (abolished)                            | Canonical                            |
| ------------------------------------------ | ------------------------------------ |
| `validate:env`                             | `env:validation`                     |
| `validate:links`                           | `links:validation`                   |
| `validate:mermaid`                         | `mermaid:validation`                 |
| `validate:heading-hierarchy`               | `headings:hierarchy-validation`      |
| `validate:specs-tree`                      | `specs:tree-validation`              |
| `validate:specs-counts`                    | `specs:counts-validation`            |
| `validate:specs-adoption`                  | `specs:adoption-validation`          |
| `validate:naming-agents`                   | `naming:harness-validation`          |
| `validate:naming-workflows`                | `naming:workflows-validation`        |
| `validate:repo-governance-vendor-audit`    | `governance:vendor-audit-validation` |
| `validate:cross-vendor-parity`             | `cross-vendor:parity-validation`     |
| `validate:harness-bindings` (package.json) | `harness:bindings-validation`        |
