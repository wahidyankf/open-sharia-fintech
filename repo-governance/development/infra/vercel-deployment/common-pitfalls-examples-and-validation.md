---
title: "Common Pitfalls, Examples, and Validation"
description: Common vercel.json misconfiguration pitfalls with fixes, PASS/FAIL examples of buildCommand alignment, and how the rules-checker agent validates this convention.
category: explanation
subcategory: development
tags:
  - vercel
  - deployment
  - nx
  - build
  - monorepo
created: 2026-03-26
when_to_use: Use when debugging a Vercel deployment that succeeded but has missing runtime files, or when verifying buildCommand matches dependsOn before merging.
---

# Common Pitfalls, Examples, and Validation

## Common Pitfalls

### Pitfall 1: Adding a `dependsOn` target without updating `vercel.json`

**Scenario**: A developer adds a new code generation step to the `build` target's `dependsOn` in
`project.json`. Local builds work. The Vercel deployment succeeds but the generated files are
absent at runtime.

**Fix**: Immediately add the new step to `buildCommand` in `vercel.json` in the same commit.

### Pitfall 2: Assuming Nx orchestration applies to Vercel builds

**Scenario**: A developer runs `nx build ayokoding-www` and confirms the full pipeline works, then
assumes Vercel will do the same.

**Fix**: `nx build` and Vercel's build are independent pipelines. `vercel.json`'s `buildCommand`
is the only mechanism for controlling what Vercel runs.

### Pitfall 3: Generated files absent from standalone bundle

**Scenario**: A Next.js app with `output: "standalone"` generates files at build time and reads
them at runtime. The Vercel deployment includes the generated files, but the deployed function
cannot find them because they were not traced as dependencies.

**Fix**: Declare the generated directories in `outputFileTracingIncludes` in `next.config.ts`.

### Pitfall 4: Wrong working directory in `buildCommand`

**Scenario**: A `buildCommand` script path is written as if the working directory is the
repository root, but Vercel runs `buildCommand` from the app's directory (as configured in the
Vercel project settings).

**Fix**: Confirm the Vercel project's root directory setting. Scripts in `buildCommand` run
relative to that directory. In this monorepo, `buildCommand` runs from the app directory (e.g.,
`apps/ayokoding-www/`).

## Examples

### PASS: `ayokoding-www` — `buildCommand` mirrors `dependsOn`

`apps/ayokoding-www/project.json`:

```json
"build": {
  "dependsOn": ["generate-indexes", "generate-search-data"]
}
```

`apps/ayokoding-www/vercel.json`:

```json
{
  "buildCommand": "npx tsx src/scripts/generate-indexes.ts && npx tsx src/scripts/generate-search-data.ts && next build"
}
```

Both entries are present and in the same order.

### FAIL: `dependsOn` target added but `vercel.json` not updated

`apps/ayokoding-www/project.json`:

```json
"build": {
  "dependsOn": ["generate-indexes", "generate-search-data", "generate-sitemaps"]
}
```

`apps/ayokoding-www/vercel.json`:

```json
{
  "buildCommand": "npx tsx src/scripts/generate-indexes.ts && npx tsx src/scripts/generate-search-data.ts && next build"
}
```

`generate-sitemaps` runs locally via Nx but is absent from `buildCommand`. Vercel deployments
produce an app without the generated sitemaps.

## Validation

The `rules-checker` agent validates that:

- Any `build` target with a non-empty `dependsOn` list in `project.json` has a `buildCommand` in
  `vercel.json` that includes equivalent steps
- Next.js apps using `output: "standalone"` with a `generated/` directory declare it in
  `outputFileTracingIncludes`

## References

**Related Development Standards:**

- [Nx Target Standards](../nx-targets.md) - Canonical target names and `dependsOn` patterns
- [GitHub Actions Workflow Naming Convention](../github-actions-workflow-naming.md) - Related CI/CD
  naming convention

**Agents:**

- `rules-checker` - Validates `vercel.json` build command alignment
- `repo-workflow-fixer` - Corrects misaligned `buildCommand` entries
