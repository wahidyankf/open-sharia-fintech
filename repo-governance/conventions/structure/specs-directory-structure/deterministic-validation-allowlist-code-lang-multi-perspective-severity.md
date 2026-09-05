---
title: "Deterministic Validation: Allowlist-Driven App Selection"
description: The rhino-cli specs validation commands and their default app selection
when_to_use: Read this when running or configuring rhino-cli specs validate-* commands.
category: explanation
subcategory: conventions
tags:
  - conventions
  - specs
  - gherkin
  - directory-structure
  - organization
  - c4-diagrams
  - openapi
  - c4
created: 2026-04-02
---

# Deterministic Validation (rhino-cli)

The following `rhino-cli specs` commands validate the directory structure mechanically:

| Command                                    | What it checks                                                             |
| ------------------------------------------ | -------------------------------------------------------------------------- |
| `rhino-cli specs validate-tree <app>`      | Top-level folders match the canonical five — no flat-root artifacts remain |
| `rhino-cli specs validate-counts <folder>` | README count claims match actual `.feature` file counts                    |
| `rhino-cli specs validate-links <folder>`  | Markdown link integrity within the spec tree                               |
| `rhino-cli specs validate-adoption <app>`  | BDD/Contracts adoption gaps per surface profile                            |

These commands run as part of the `specs-quality-gate` workflow deterministic-offload pass. See [Deterministic Offload](./pre-push-ci-llm-validation-deterministic-offload-and-related-documentation.md#deterministic-offload) in the next section.

## Allowlist-driven default app selection

`validate-adoption`, `validate-tree`, `validate-counts`, and `validate-links` all accept the same three calling shapes:

- Positional `<folder>` or `<app>` — single-target legacy behaviour preserved.
- `--apps <csv>` — multi-app validation across an explicit list.
- No positional, no flag — validates nothing; `specs structure validate` is the wired entry point and discovers every directory under `specs/apps/`.

Pre-push and CI surfaces invoke `specs structure validate` without arguments, so a new app is picked up by folder discovery alone.
