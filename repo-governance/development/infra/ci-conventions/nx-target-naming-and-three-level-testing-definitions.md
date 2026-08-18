---
title: "Nx Target Naming and Three-Level Testing Definitions"
description: Key Nx target names and the three test-level isolation rules.
category: explanation
subcategory: development
tags: [ci-cd, nx, testing]
created: 2026-03-31
when_to_use: Use when checking which target or isolation rule applies.
---

# Nx Target Naming and Three-Level Testing Definitions

## Nx Target Naming and Caching Rules

This document uses the canonical target names defined in [Nx Target Standards](../nx-targets.md).
Refer to that document for:

- The full required target set per project type
- Caching rules per target (`cache: true` / `cache: false`)
- Input declarations required for correct cache invalidation
- The four-dimension tag scheme for `project.json`

Key targets referenced throughout this document:

| Target             | Summary                                                         |
| ------------------ | --------------------------------------------------------------- |
| `test:quick`       | Fast pre-push gate: `test:unit` + coverage validation           |
| `test:unit`        | Isolated unit tests, all dependencies mocked, coverage measured |
| `test:integration` | Real infrastructure, no HTTP layer, not cacheable               |
| `test:e2e`         | Full stack via Playwright, not cacheable                        |
| `lint`             | Static analysis                                                 |
| `typecheck`        | Type verification without producing artifacts                   |

## Three-Level Testing Definitions

The three levels apply universally across all project types. The isolation boundary at each level
is fixed — only the step implementation details change per language and framework.

| Level                                | Dependencies                | HTTP Layer                     | Coverage      | Nx Cache       |
| ------------------------------------ | --------------------------- | ------------------------------ | ------------- | -------------- |
| **Unit** (`test:unit`)               | All mocked                  | None — call functions directly | Measured here | `cache: true`  |
| **Integration** (`test:integration`) | Real infra (DB, filesystem) | None — no HTTP dispatch        | Not measured  | `cache: false` |
| **E2E** (`test:e2e`)                 | All real                    | Real HTTP via Playwright       | Not measured  | `cache: false` |

For the full definition including architecture diagrams, Docker infrastructure requirements, and
per-backend implementation patterns, see the
[Three-Level Testing Standard](../../quality/three-level-testing-standard.md).
