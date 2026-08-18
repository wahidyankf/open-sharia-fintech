---
title: "Core Rule and Pattern"
description: The mandatory rule that vercel.json's buildCommand must mirror every dependsOn target in project.json's build target, and the canonical project.json/vercel.json pattern.
category: explanation
subcategory: development
tags:
  - vercel
  - deployment
  - nx
  - build
  - monorepo
created: 2026-03-26
when_to_use: Use when writing or auditing vercel.json's buildCommand for a Vercel-deployed app with Nx dependsOn prerequisites.
---

# Core Rule and Pattern

## Principles Implemented/Respected

This convention implements/respects the following core principles:

- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**:
  Build-time prerequisites must be declared explicitly in `vercel.json`. Relying on Nx
  orchestration to handle them during a Vercel deployment is implicit and will fail silently at
  runtime.

- **[Reproducibility First](../../../principles/software-engineering/reproducibility.md)**:
  The build on Vercel must produce the same outputs as a local `nx build`. All steps that `nx
build` depends on must also run during the Vercel build.

## Conventions Implemented/Respected

This practice respects the following conventions:

- **[Nx Target Standards](../nx-targets.md)**: The `build` target in `project.json` remains the
  source of truth for what must run. `vercel.json` replicates the `dependsOn` chain — it does not
  replace it.

## The Core Rule

**If the `build` target in `project.json` has a `dependsOn` list, every target in that list MUST
also be replicated in `vercel.json`'s `buildCommand`.**

Vercel runs the framework's default build command directly (e.g., `next build`). It does NOT
invoke `nx build` and does NOT resolve Nx `dependsOn` chains. Any target declared in `dependsOn`
is invisible to Vercel unless it is explicitly added to `buildCommand`.

## Why This Matters

Nx `dependsOn` is an orchestration instruction for the Nx task runner. When you run `nx build
ayokoding-www` locally, Nx resolves the dependency graph and runs `generate-indexes` and
`generate-search-data` first, then `next build`.

Vercel bypasses Nx entirely. It calls `next build` (or the configured `buildCommand`) in the app
directory. No Nx, no dependency graph, no `dependsOn` resolution.

If a build-time step is missing, the app still deploys — but runtime behavior is broken. The
generated files that `next build` expected to find are absent, and the runtime fallback (if any)
runs in a constrained serverless environment where it may exceed function timeout limits.

## The Pattern

### `project.json` (source of truth)

```json
"build": {
  "executor": "nx:run-commands",
  "options": {
    "command": "next build",
    "cwd": "{projectRoot}"
  },
  "dependsOn": ["generate-indexes", "generate-search-data"]
}
```

### `vercel.json` (must mirror the `dependsOn` chain)

```json
{
  "buildCommand": "npx tsx src/scripts/generate-indexes.ts && npx tsx src/scripts/generate-search-data.ts && next build"
}
```

The `buildCommand` must execute all `dependsOn` targets (in dependency order) followed by the
framework build command.
