---
title: "Tiered Env Files — the `APP_ENV` Contract"
description: How an app selects its runtime tier via APP_ENV and loads exactly one .env.<tier> file, the fallback rule for a missing tier file, and the local/test/stag/prod agent-access table.
when_to_use: Use when you need to know which .env.<tier> file an app loads for a given APP_ENV value, or whether agents may access it.
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

# Tiered Env Files — the `APP_ENV` Contract

Every app selects its runtime tier via the `APP_ENV` process variable (unset means `local`) and loads
exactly one file for that tier — `.env.<tier>`. A variable already present in the process
environment is never replaced by a file value, which is what lets CI run with no file on disk at
all. A missing tier file is not an error — the app falls back to process-env values and
framework/library defaults.

| Tier    | `APP_ENV` value   | File loaded  | Storage    | Agent access | Role                      |
| ------- | ----------------- | ------------ | ---------- | ------------ | ------------------------- |
| `local` | `local` (default) | `.env.local` | gitignored | allow        | Developer machine         |
| `test`  | `test`            | `.env.test`  | gitignored | allow        | CI / e2e test runs        |
| `stag`  | `stag`            | `.env.stag`  | gitignored | **DENIED**   | Staging deploy secrets    |
| `prod`  | `prod`            | `.env.prod`  | gitignored | **DENIED**   | Production deploy secrets |

`.env.stag` is used rather than the more familiar `.env.staging` for symmetry with `.env.prod` — no
framework recognizes either name natively, so nativeness is not a tiebreaker and symmetry is.
