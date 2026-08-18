---
title: "Naming Rules"
description: The naming rules governing dev/start/test:* target names and the colon-versus-hyphen separator convention.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when deciding what to call a new or renamed Nx target.
---

# Naming Rules

- Use `dev` for the development server — never `serve`, never `start:dev`
- Use `start` for the production server — never `serve`
- Use `test:quick` for the sequential 5-step quality gate (typecheck → lint → test:unit → test:coverage → test:specs; 4 steps on `rhino-cli`, where coverage runs on CI instead); `test:unit` for isolated unit tests with mocked dependencies (Rust CLI apps consume Gherkin specs at this level; `echo` where N/A); `test:integration` for tests with real infrastructure (demo-be: PostgreSQL via docker-compose) or in-process mocking (MSW, Godog) — `echo` where N/A; `test:e2e` for Playwright E2E tests on `*-e2e` projects (CRON-only; `echo` on non-e2e projects); `test:coverage` for the native per-project coverage gate (≥ 90% line; `echo` where `test:unit` is `echo`); `test:specs` for the aggregate of all `specs:*` validators (runs inside `test:quick`); `specs:behavior:coverage` for Gherkin behavior-level coverage validation; `specs:domain:coverage` for domain-area coverage gated by `repo-config.yml`
- Separate target variants with a colon (`build:web`, `test:e2e:ui`), not a hyphen or underscore
- All target names use lowercase with hyphens for multi-word names (`run-pre-commit`)
