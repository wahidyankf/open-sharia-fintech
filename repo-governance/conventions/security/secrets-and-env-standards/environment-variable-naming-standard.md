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
| Framework-reserved         | Keep the framework's required name          | `NEXT_PUBLIC_*`, `NODE_ENV`                       |
| Shared service connection  | Unprefixed, conventional name               | `DATABASE_URL`                                    |
| Environment tier in a name | **Forbidden** (keys identical across tiers) | not `PROD_DATABASE_URL`                           |

The **per-app prefix** is the app's Nx project name upcased with `_` separators: `ose-be` →
`OSE_BE_`, `ose-www` → `OSE_WWW_`.

## Framework-reserved exempt names

| Name            | Why exempt                                                                    |
| --------------- | ----------------------------------------------------------------------------- |
| `NEXT_PUBLIC_*` | Framework-required (Next.js browser-exposure prefix)                          |
| `NODE_ENV`      | Node reserved                                                                 |
| `DATABASE_URL`  | Cross-ecosystem convention; prefixing breaks every tool that reads it by name |
| `HOSTNAME`      | Platform convention for Next.js dev server                                    |

## Runtime port contract

Every port-binding app in this repository — the six Next.js sites and the three F# backends alike —
resolves its listener port by one precedence rule:

1. An explicit **`--port` flag** passed at start time.
2. The app's **prefixed variable** (`OSE_WWW_PORT`, `AYOKODING_WWW_PORT`, `OSE_BE_PORT`,
   `BEAVERNEST_BE_HTTP_LISTEN_PORT`, …), formed by the per-app prefix rule above.
3. The app's **compiled-in default**, which is also the value recorded in
   [web-sites.md](../../../../docs/reference/web-sites.md).

A value that is present but malformed is a hard startup error, never a silent fall back to the
default: an operator who asked for a specific port must not get a different one quietly.

**A port variable takes the app prefix — including on the web tier**, reversing the older rule that
treated `PORT` as framework-reserved for webs. A single exported `PORT` used to retarget every app
at once; the prefixed name is what lets one shell hold all nine ports. The frameworks are bridged,
not fought: `scripts/next-with-port.mjs` resolves the port and then sets `process.env.PORT` itself
before starting Next, and `libs/fsharp-env-loader`'s `PortResolver` shapes the `UseUrls` value for
the F# backends. A bare `PORT` is **not** an override source for either. `HOSTNAME` is unaffected.

A valid port is plain decimal digits in 1-65535. The TypeScript and F# resolvers are deliberate
mirrors with scenarios paired one-for-one, so both accept and reject exactly the same values.
`beavernest-be` composes them differently — its own `HttpConfiguration` owns the variable and default
tiers under that same grammar and calls `PortResolver` for the flag tier alone, because its listener
address carries a loopback-versus-wildcard guard.
