# Ubiquitous Language — env-loader

**Bounded context**: `env-loader`
**Maintainer**: organiclever-app-web team
**Last reviewed**: 2026-08-12
**Audience:** Engineers, Technical Product/Project Managers

## One-line summary

Tiered `.env.<APP_ENV>` loader for `organiclever-app-web`, wired as the first import in
`next.config.ts`. Loads exactly one `.env.<tier>` file at startup; process env values always win over
file values, a missing file is not an error, and a stray auto-loaded `.env`/`.env.production` beside
the tier file fails loudly at any non-local tier.

## Term index

| Term          | Code identifier(s)            | Used in features       |
| ------------- | ----------------------------- | ---------------------- |
| `Tier`        | `resolveTier`, `DEFAULT_TIER` | `env-loader/*.feature` |
| `Tier file`   | `tierEnvFilePath`             | `env-loader/*.feature` |
| `Stray guard` | `assertNoStrayEnvFile`        | `env-loader/*.feature` |
| `Loader`      | `loadTierEnv`                 | `env-loader/*.feature` |

## Terms in detail

### Term: `Tier`

The deployment environment selector read from the `APP_ENV` process variable, defaulting to `"local"`
when unset. One of `local`, `test`, `stag`, `prod`.

### Term: `Tier file`

The single `.env.<tier>` file the loader reads for the resolved tier — no other tier's file is ever
read in the same process.

### Term: `Stray guard`

A startup check that throws, at any non-local tier, if a bare `.env` or `.env.production` file exists
beside the tier file — both of which Next.js's own `@next/env` would otherwise auto-load in addition to
the explicit tier file, silently violating the "exactly one file" rule.

### Term: `Loader`

The `loadTierEnv()` entry point, self-invoked on module import from `next.config.ts`, before
`@t3-oss/env-nextjs`'s `createEnv()` in `env.ts` validates anything.
