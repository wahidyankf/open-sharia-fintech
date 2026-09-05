---
title: "Vercel Deployment Convention"
description: "Rules for configuring vercel.json when Nx build targets must run before the framework build"
when_to_use: "Read this index to find the right Vercel Deployment Convention child document."
---

# Vercel Deployment Convention

- [Core Rule and Pattern](./core-rule-and-pattern.md) — The mandatory rule that vercel.json's buildCommand must mirror every dependsOn target in project.json's build target, and the canonical project.json/vercel.json pattern. Use when writing or auditing vercel.json's buildCommand for a Vercel-deployed app with Nx dependsOn prerequisites.
- [Standalone Output and Current State](./standalone-output-and-current-state.md) — How outputFileTracingIncludes must declare build-time generated directories for Next.js standalone output, the current vercel.json status of each Vercel app, and when to recheck vercel.json. Use when adding `output: "standalone"` to a Next.js app, or when auditing which Vercel-deployed apps have vercel.json build commands configured.
- [Common Pitfalls, Examples, and Validation](./common-pitfalls-examples-and-validation.md) — Common vercel.json misconfiguration pitfalls with fixes, PASS/FAIL examples of buildCommand alignment, and how the rules-checker agent validates this convention. Use when debugging a Vercel deployment that succeeded but has missing runtime files, or when verifying buildCommand matches dependsOn before merging.
