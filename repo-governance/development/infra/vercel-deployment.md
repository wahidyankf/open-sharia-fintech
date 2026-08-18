---
title: "Vercel Deployment Convention"
description: Rules for configuring vercel.json when Nx build targets must run before the framework build
category: explanation
subcategory: development
tags:
  - vercel
  - deployment
  - nx
  - build
  - monorepo
created: 2026-03-26
when_to_use: Use when configuring `vercel.json` for a Vercel-deployed app whose Nx `build` target has `dependsOn` prerequisites.
---

# Vercel Deployment Convention

Rules for configuring `vercel.json` when an app has Nx build-time targets that must run before the
framework build command. Vercel bypasses Nx entirely, so any `dependsOn` prerequisite must be
replicated explicitly in `buildCommand` or the deployed app silently loses generated files at
runtime. Covered below across three files: the core rule and pattern, standalone-output tracing
and the current per-app state, and common pitfalls with validation.

## Documents

- [Core Rule and Pattern](./vercel-deployment/core-rule-and-pattern.md) — The mandatory rule that vercel.json's buildCommand must mirror every dependsOn target in project.json's build target, and the canonical project.json/vercel.json pattern. Use when writing or auditing vercel.json's buildCommand for a Vercel-deployed app with Nx dependsOn prerequisites.
- [Standalone Output and Current State](./vercel-deployment/standalone-output-and-current-state.md) — How outputFileTracingIncludes must declare build-time generated directories for Next.js standalone output, the current vercel.json status of each Vercel app, and when to recheck vercel.json. Use when adding `output: "standalone"` to a Next.js app, or when auditing which Vercel-deployed apps have vercel.json build commands configured.
- [Common Pitfalls, Examples, and Validation](./vercel-deployment/common-pitfalls-examples-and-validation.md) — Common vercel.json misconfiguration pitfalls with fixes, PASS/FAIL examples of buildCommand alignment, and how the repo-rules-checker agent validates this convention. Use when debugging a Vercel deployment that succeeded but has missing runtime files, or when verifying buildCommand matches dependsOn before merging.
