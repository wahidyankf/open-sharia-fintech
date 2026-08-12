# Ubiquitous Language — be-env

**Bounded context**: `be-env`
**Maintainer**: organiclever-be team
**Last reviewed**: 2026-08-12

## Responsibility

Loads exactly one `.env.<tier>` file selected by `APP_ENV` at process startup, per this
repo's tiered env-file convention. A variable already present in the process environment is
never replaced by a file value, and a missing file is not an error — the normal case in CI,
which sets real env vars with no file on disk. This is what lets `.env.stag`/`.env.prod`
(agent-restricted, sensitive) files never need to be opened by an AI agent, while
`.env.local`/`.env.test` stay agent-readable.

## Term index

| Term                 | Code identifier(s)   | Used in features        |
| -------------------- | -------------------- | ----------------------- |
| tier                 | `currentTier`        | env-tier-loader.feature |
| tier file            | `loadEnvTierFromDir` | env-tier-loader.feature |
| composition root     | `candidateDirs`      | env-tier-loader.feature |
| tiered env-file load | `loadEnvTier`        | env-tier-loader.feature |

## Out of scope

- Secret management / vaulting — this loader only reads plaintext `.env.<tier>` files,
  never remote secret stores
- `.env.stag`/`.env.prod` content — those files are agent-restricted and are never read or
  written by an AI agent (see the repo-wide env-file convention)
- Multi-file overlay/merge — exactly one tier file is loaded, never a stack of files
