---
description: How outputFileTracingIncludes must declare build-time generated directories for Next.js standalone output, the current vercel.json status of each Vercel app, and when to recheck vercel.json.
when_to_use: 'Use when adding `output: "standalone"` to a Next.js app, or when auditing which Vercel-deployed apps have vercel.json build commands configured.'
---

# Standalone Output and Current State

## Next.js Standalone Output: `outputFileTracingIncludes`

For Next.js apps using `output: "standalone"`, generated files are only included in the Vercel
deployment bundle if they are declared in `outputFileTracingIncludes` inside `next.config.ts`.

Next.js standalone output traces file dependencies statically. Generated files (e.g., content
indexes, search data) created at build time are not automatically detected as runtime dependencies
unless explicitly listed.

**Pattern** (`next.config.ts`):

```typescript
const nextConfig: NextConfig = {
  output: "standalone",
  outputFileTracingIncludes: {
    "/**": ["./content/**/*", "./generated/**/*"],
  },
};
```

Include any directory that contains build-time generated files the runtime depends on.

## Current State of Vercel Apps

| App                | `vercel.json` location              | `buildCommand` status                       | Notes                                                    |
| ------------------ | ----------------------------------- | ------------------------------------------- | -------------------------------------------------------- |
| `ayokoding-www`    | `apps/ayokoding-www/vercel.json`    | Set (fixed after incident)                  | Runs `generate-indexes` and `generate-search-data` first |
| `organiclever-www` | `apps/organiclever-www/vercel.json` | Not set (no build-time targets at present)  | At risk if build-time targets are added                  |
| `ose-www`          | `apps/ose-www/vercel.json`          | Set (`generate-search-data` + `next build`) | Next.js build with search data generation                |

## When to Check

Check and update `vercel.json` whenever:

1. **Adding a new Nx target** to a Vercel-deployed app that feeds into `build` via `dependsOn`
2. **Reordering `dependsOn` targets** — order matters; `buildCommand` must match
3. **Adding a new Vercel-deployed app** to the monorepo — audit `project.json` for `dependsOn`
   before writing `vercel.json`
4. **Removing a `dependsOn` target** — remove the corresponding step from `buildCommand` to avoid
   running unnecessary work
