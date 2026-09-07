---
description: Where each app's env template lives, the no-duplication rule, the HUMAN-only rule for relocating real env files, and the library env-var declaration rule.
when_to_use: Use when adding an env template for a new app, or when a library reads process env vars directly and you need to know where to declare them.
---

# Layout Standard — One Template per App

Each app's env template lives in exactly one place: `apps/<app>/.env.example`.

- **Rust backends**: template lives at `apps/<app>/.env.example` (where `Cargo.toml` lives).
- **Next.js webs**: template lives at `apps/<app>/.env.example` (where `next.config.*` lives). Next.js
  auto-loads `.env.local` from this directory; the `.env.example` is a documentation file only —
  never auto-loaded by Next.js or Nx.
- **Duplication is forbidden**: no second template for the same app under `infra/dev/` or elsewhere.

Relocating real gitignored `.env*` files (`.env.local` etc.) is a **[HUMAN]** task — the
`guard-env-file-access` policy forbids agents from touching them directly.

## Library env-var rule

A `libs/` project never loads an env file itself — no `.env.example` template, no tier loader. If a
library reads the process environment directly (`GetEnvironmentVariable`, `process.env`, `env::var`),
each name it reads must be declared in the `.env.example` of every **tiered app** that consumes it
(the app is what crosses the local/test/stag/prod tier boundary; the library does not). A library
consumed only by out-of-scope CLI tooling (no `.env.example` by design — see §3's app-only scope) is
an explicit exception: there is no tiered-app consumer to declare the name in, so none is required.
Re-verify this exception whenever the library gains a new consumer — a name that was legitimately
undeclared while the only consumer was a CLI tool must be declared the moment a tiered app starts
consuming that library too.
