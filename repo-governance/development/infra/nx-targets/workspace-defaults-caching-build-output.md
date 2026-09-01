---
title: "Workspace Defaults, Caching, and Build Output"
description: The nx.json targetDefaults block, the per-target caching-rules table, and the build output directory conventions.
category: explanation
subcategory: development
tags:
  - nx
  - targets
  - project-json
  - build
  - scripts
created: 2026-02-23
when_to_use: Use when deciding whether a target should be cached, or where a project's build output directory should live.
---

# Workspace Defaults, Caching, and Build Output

## Workspace-Level Defaults

`nx.json` `targetDefaults` provide inherited behaviour for standard targets. Individual `project.json` files override these when the project differs.

```json
{
  "targetDefaults": {
    "build": {
      "dependsOn": ["^build"],
      "outputs": ["{projectRoot}/dist"],
      "cache": true
    },
    "typecheck": {
      "cache": true
    },
    "lint": {
      "cache": true
    },
    "test:quick": {
      "cache": true
    },
    "test:unit": {
      "cache": true
    },
    "test:coverage": {
      "cache": true
    },
    "specs:behavior:coverage": {
      "cache": true
    },
    "test:specs": {
      "cache": true
    },
    "test:integration": {
      "cache": false
    },
    "test:e2e": {
      "cache": false
    }
  }
}
```

### Caching Rules

| Target                    | Cached | Notes                                                                                                                                                                                                                                      |
| ------------------------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `build`                   | Yes    | Declare `outputs` in `project.json` for cache restoration                                                                                                                                                                                  |
| `typecheck`               | Yes    | Pure analysis; safe to cache against source changes                                                                                                                                                                                        |
| `lint`                    | Yes    | Pure static analysis; safe to cache                                                                                                                                                                                                        |
| `test:quick`              | Yes    | Cache hit skips redundant pre-push runs                                                                                                                                                                                                    |
| `test:unit`               | Yes    | Deterministic; safe to cache against source changes                                                                                                                                                                                        |
| `test:coverage`           | Yes    | Deterministic native coverage gate; safe to cache against source changes                                                                                                                                                                   |
| `specs:behavior:coverage` | Yes    | Pure behavior-level Gherkin coverage analysis; deterministic against source and spec changes                                                                                                                                               |
| `test:specs`              | Yes    | Pure specs validation; deterministic against source, spec, and `repo-config.yml` changes; caches the aggregate of all `specs:*` validators                                                                                                 |
| `test:integration`        | No     | Demo-be backends use real PostgreSQL via docker-compose (non-deterministic external state). Default `cache: false` in `nx.json`. Projects using in-process mocking only (MSW, Godog) may override to `cache: true` in their `project.json` |
| `dev`                     | No     | Long-running process                                                                                                                                                                                                                       |
| `start`                   | No     | Long-running process                                                                                                                                                                                                                       |
| `run`                     | No     | Side-effectful execution                                                                                                                                                                                                                   |
| `test:e2e`                | No     | Requires live app state; run via scheduled cron, not pre-push                                                                                                                                                                              |
| `test:e2e:ui`             | No     | Interactive process                                                                                                                                                                                                                        |
| `test:e2e:report`         | No     | Reads filesystem state at invocation time                                                                                                                                                                                                  |
| `install`                 | No     | Must always run to ensure dep state                                                                                                                                                                                                        |
| `clean`                   | No     | Destructive operation                                                                                                                                                                                                                      |

## Build Output Conventions

Declare the output directory in `project.json` `outputs` to enable Nx cache restoration.

| Project Type | Output Directory        |
| ------------ | ----------------------- |
| Rust CLI     | `{projectRoot}/dist/`   |
| Next.js      | `{projectRoot}/.next/`  |
| Spring Boot  | `{projectRoot}/target/` |

Example override for a Next.js app with custom output:

```json
{
  "targets": {
    "build": {
      "executor": "nx:run-commands",
      "outputs": ["{projectRoot}/.next"],
      "options": { "command": "next build" }
    }
  }
}
```
