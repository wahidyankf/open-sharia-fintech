# System Context — ts-env-loader

C4 Level 1 system context for `ts-env-loader`.

## Actors and consumers

- **`ayokoding-www`, `organiclever-app-web`, `organiclever-www`, `ose-app-web`,
  `ose-www`** — each app calls `loadTierEnv()` explicitly as the first statement of its own
  composition root (e.g. the first import of `next.config.ts`, before `./env.ts`).
- **`process.env`** (or an app-supplied `EnvRecord`) — the target record `loadTierEnv()` reads
  `APP_ENV` from and populates with tier-file values.
- **Filesystem `.env.<tier>` files** — the tier files an app's `appDir` holds on disk; the loader
  reads at most one of them per call.

`ts-env-loader` has no runtime dependency on any backend and never calls itself on import; it is a
pure, explicitly-invoked loader module. A library that auto-loaded its own tier file on import
would silently compete with the consuming app's own loader.

See [context.md](./context.md) for the C4 context diagram placeholder.
