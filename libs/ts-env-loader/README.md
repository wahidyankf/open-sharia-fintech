# ts-env-loader

Shared `.env.<APP_ENV>` tiered env-file loader for the open-sharia-enterprise monorepo's Next.js
and Vite apps.

## What's Shared

The pure loader logic behind the repo-wide `APP_ENV` tier convention — tier resolution
(`resolveTier`), tier-file-path resolution (`tierEnvFilePath`), the stray-auto-loaded-file guard,
and `loadTierEnv`, which applies a tier file's values to a process-env-like record with
process-env-always-wins semantics.

Every TS app that consumes this package still calls `loadTierEnv()` itself, explicitly, from its
own composition root (e.g. the first line of `next.config.ts`) — this package never calls it on
import. A library that auto-loaded its own tier file on import would silently compete with the
app's own loader; see this repo's `restrict-env-access-to-prod-and-stag` plan's `tech-docs.md` for
the full rationale.

## Usage

```ts
// next.config.ts, first import
import { loadTierEnv } from "@open-sharia-enterprise/ts-env-loader";

loadTierEnv();
```

## Consumers

`ayokoding-www`, `organiclever-app-web`, `organiclever-www`, `ose-app-web`, `ose-www`.
