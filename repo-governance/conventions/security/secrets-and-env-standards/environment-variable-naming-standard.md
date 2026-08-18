---
title: "Environment Variable Naming Standard"
description: The variable-class naming rules (app-defined, framework-reserved, shared-service, tier-forbidden) and the list of framework-reserved exempt names.
when_to_use: Use when naming a new environment variable and deciding whether it needs an app prefix.
category: explanation
subcategory: conventions
tags:
  - security
  - secrets
  - env-files
  - guard-env-file-access
  - naming
  - reproducibility
created: 2026-06-10
---

# Environment Variable Naming Standard

## Variable classes

| Class                      | Rule                                        | Example                                           |
| -------------------------- | ------------------------------------------- | ------------------------------------------------- |
| App-defined value          | `SCREAMING_SNAKE`, per-app prefix           | `ORGANICLEVER_BE_PORT`, `OSE_BE_OPENROUTER_MODEL` |
| Framework-reserved         | Keep the framework's required name          | `NEXT_PUBLIC_*`, Next.js `PORT`                   |
| Shared service connection  | Unprefixed, conventional name               | `DATABASE_URL`                                    |
| Environment tier in a name | **Forbidden** (keys identical across tiers) | not `PROD_DATABASE_URL`                           |

The **per-app prefix** is the app's Nx project name upcased with `_` separators: `ose-be` →
`OSE_BE_`, `ose-www` → `OSE_WWW_`.

## Framework-reserved exempt names

| Name            | Why exempt                                                                    |
| --------------- | ----------------------------------------------------------------------------- |
| `NEXT_PUBLIC_*` | Framework-required (Next.js browser-exposure prefix)                          |
| `PORT`          | Platform convention (host/PaaS injects it) — **webs only**                    |
| `NODE_ENV`      | Node reserved                                                                 |
| `DATABASE_URL`  | Cross-ecosystem convention; prefixing breaks every tool that reads it by name |
| `HOSTNAME`      | Platform convention for Next.js dev server                                    |

**Critical asymmetry**: The **Next.js dev server** reads `PORT` natively — renaming it to
`OSE_WWW_PORT` would break `nx dev ose-www`. Rust **backend** ports are app-defined code, so they
**do** take the prefix (`ORGANICLEVER_BE_PORT`, `OSE_BE_PORT`). This is the single most
error-prone point of the naming standard.
