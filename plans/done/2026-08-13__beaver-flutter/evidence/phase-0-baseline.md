# Phase 0 Legacy and Backend Baseline

**Recorded**: 2026-08-13T00:20:00Z

All commands below ran from `worktrees/beaver-flutter/`. The initial dependency
state did not contain `node_modules`; `npm install` was therefore run as the
worktree setup step before recording the final legacy-client result. It made no
tracked source change.

## Command Results

| Timestamp (UTC)      | Command                                                    | Outcome         | Relevant stdout/stderr                                                                                                                                                                                                                                                              |
| -------------------- | ---------------------------------------------------------- | --------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-08-13T00:12:00Z | `npm exec nx show project beavernest-app-web`              | PASS            | Project resolves as the legacy Vite/TypeScript app. Its `test:quick` serially invokes typecheck, lint, unit, coverage, and specs.                                                                                                                                                   |
| 2026-08-13T00:13:00Z | `npm exec nx run beavernest-app-web:test:quick`            | FAIL, diagnosed | `npx @hey-api/openapi-ts` attempted an uncached latest `0.99.0` and failed with `TypeError: Cannot read properties of undefined (reading 'AnyKeyword')`. The tracked lock pins `@hey-api/openapi-ts` `0.94.2`, but no installed workspace dependency was present.                   |
| 2026-08-13T00:15:00Z | `npm install`                                              | PASS            | Installed the lockfile-pinned workspace dependencies; postinstall ran the repository doctor. This is worktree initialization, not a BeaverNest source failure.                                                                                                                      |
| 2026-08-13T00:15:00Z | `npm exec nx run beavernest-app-web:test:quick`            | PASS            | `beavernest-contracts:bundle`, legacy codegen, typecheck, lint, unit, coverage, and specs all completed successfully. The only emitted messages were non-failing `NO_COLOR`/`FORCE_COLOR` Node warnings.                                                                            |
| 2026-08-13T00:16:00Z | `npm exec nx run beavernest-app-web-e2e:test:quick`        | PASS            | Typecheck, lint, no-op unit/coverage targets, specs structure validation, and Playwright E2E coverage baseline all passed; coverage reported `0 new unbound scenario(s) beyond baseline`.                                                                                           |
| 2026-08-13T00:17:00Z | `npm exec nx run fsharp-env-loader:test:quick`             | PASS            | F# build/lint/analyzers passed. Unit tests: `Passed: 20`; coverage: `100%` line, `88.88%` branch, `100%` method. The test rewrote only its tracked absolute-path coverage fixture; that test artifact was restored before this evidence was written.                                |
| 2026-08-13T00:18:00Z | `APP_ENV=test npm exec nx run beavernest-be:test:quick`    | PASS            | Backend typecheck, lint, unit, coverage, and specs passed with the committed `APP_ENV=test` tier contract.                                                                                                                                                                          |
| 2026-08-13T00:18:00Z | `APP_ENV=test npm exec nx run beavernest-be-e2e:test:e2e`  | FAIL, diagnosed | Host `dotnet build` succeeds, but the combined-runtime image fails at `dotnet publish`: warning `MSB9008` says `../../../../libs/fsharp-env-loader/fsharp-env-loader.fsproj` is absent; error `FS0225` says generated `Health.fs` is absent. The command does not reach Playwright. |
| 2026-08-13T00:18:00Z | `bash infra/dev/beavernest-app/tests/clean-image-build.sh` | FAIL, diagnosed | The intended clean, source-only image reproduces the same two defects: the Dockerfile omits the `fsharp-env-loader` project/source and does not generate/copy `apps/beavernest-be/generated-contracts/OpenAPI/src/BeaverNestBe.Contracts/Health.fs` before backend publish.         |

## Backend and Container Baseline

The direct backend quick gate proves that `APP_ENV=test` is runnable in the
committed host-side composition and test contract. The current container E2E
does **not** forward that caller tier: `apps/beavernest-be/scripts/run-e2e.sh`
creates Compose with `--env-file /dev/null`, while both BeaverNest Compose files
contain no `APP_ENV` service environment mapping. Therefore its container uses
the loader's existing `local` default until Phase 2 deliberately forwards
`APP_ENV`; the image failure above prevents a runtime container assertion in
this baseline.

The source-only image failure is a pre-existing Phase 0 blocker. Its narrow
remediation must preserve the tier-loader contract while making Docker build
inputs complete: copy `libs/fsharp-env-loader/fsharp-env-loader.fsproj` before
restore and `libs/fsharp-env-loader/src/` before publish, and generate or make
the required F# contract source available before publishing. Re-run both failed
commands after that implementation change, rather than treating the existing
host-side quick gates as image evidence.

## Flutter Web Capability

**Recorded**: 2026-08-13T00:39:56Z

- `flutter doctor -v` reports Flutter stable `3.41.5`, framework revision
  `2c9eb20739`, engine revision `052f31d115`, and Dart `3.11.3`.
- `flutter devices` reports Chrome `151.0.7922.109` as an available Web device.
- `flutter test --help` completed successfully, confirming the required unit-test command is
  available.
- `fvm --version` reports `4.0.5`.
- The only doctor warnings concern an Android command-line component and Dart PATH ordering. Android
  is out of this Flutter Web-only plan; the selected pinned FVM toolchain is established in Phase 1.

## Existing Hosted-Client and Tier-Loader Behavior

**Recorded**: 2026-08-13T00:43:00Z

- `Program.main` calls `loadEnvTier ()` before `configuration ()`, database configuration, listener
  parsing, migrations, or Kestrel construction.
- `EnvTierLoader.loadEnvTier` delegates to the shared loader with only
  `apps/beavernest-be` and `.` as candidate roots, preserving process-environment precedence.
- `StaticContent.staticFileOptions` serves Vite `index.html` with `Cache-Control: no-cache` and
  `/assets/**` with immutable one-year caching. The SPA fallback is GET/HEAD-only, excludes API and
  assets, and serves only dotless paths when `index.html` exists.
- `run-e2e.sh` deliberately invokes Compose with `--env-file /dev/null` and does not map `APP_ENV`
  into container services; current hosted E2E therefore uses the loader's `local` default. P2 owns
  forwarding the caller tier.
- The legacy browser suite uses the same-origin combined runtime and the existing
  `beavernest-app-web` Gherkin identity; P2 replaces that identity atomically.
