---
title: "infra/dev/<stack> Compose Env — No Duplicate Templates"
description: Why compose stacks must not introduce a second .env.example key list, and how they load a gitignored local .env with CI overrides instead.
when_to_use: Use when adding or renaming a docker-compose dev stack under infra/dev/ and wiring its environment variables.
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

# infra/dev/<stack> Compose Env — No Duplicate Templates

The layout standard forbids a second template per app. Compose stacks must not introduce their own `.env.example`
key list. They load a gitignored local `.env` (e.g. `infra/dev/organiclever-app/.env`, already
gitignored) and override with inline `environment:` in `docker-compose.ci.yml` for CI — never a
committed second template. Any value a CI job needs is set inline in the compose override or
sourced from the app's canonical `apps/<app>/.env.example` keys (placeholders only), so the drift
guard still sees one source of truth. New stacks (e.g. `infra/dev/organiclever-www/`) and stack
renames (e.g. `infra/dev/organiclever` → `infra/dev/organiclever-app`) follow this rule and keep
the gitignored `.env` in place.
