# Ubiquitous Language — config

**Bounded context**: `config`
**Maintainer**: ose-be team
**Last reviewed**: 2026-08-12

## Responsibility

Loads exactly one `.env.<APP_ENV>` tier file for `ose-be`, before any other
configuration is read. `APP_ENV` defaults to `local` when unset. A variable
already present in the process environment is never overridden by a file
value — this is what lets CI run with no `.env.*` file on disk while still
respecting its real environment variables. A missing tier file is not an
error; only a required-but-absent variable (e.g. `DATABASE_URL`) fails fast,
and that check is unchanged by this context.

## Term index

| Term        | Code identifier(s)                | Used in features         |
| ----------- | --------------------------------- | ------------------------ |
| tier        | `resolveTier`                     | env-tier-loading.feature |
| tier file   | `loadEnvTierFrom`, `applyEnvFile` | env-tier-loading.feature |
| tier loader | `loadEnvTier`                     | env-tier-loading.feature |

## Out of scope

- Validating that a loaded value is well-formed (belongs to the consuming
  bounded context, e.g. `DATABASE_URL` parsing in `Database.fs`)
- The contents of `.env.stag` / `.env.prod` — agent-restricted, never read by
  an AI agent
- Secret storage / rotation — this context only reads a plaintext file if
  present
