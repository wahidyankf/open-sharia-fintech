module BeaverNestBe.Infrastructure.EnvTierLoader

open System.IO

// Composition-root infrastructure: thin wrapper around the shared
// `libs/fsharp-env-loader` tiered `.env.<APP_ENV>` loader per the repo-wide
// `APP_ENV` loader contract (`restrict-env-access-to-prod-and-stag` plan,
// `tech-docs.md` §The APP_ENV loader contract) so that agent-restricted
// tiers (.env.stag, .env.prod) never need to be opened by an AI agent. The
// loader rules themselves (tier resolution, process-env-wins, missing-file
// tolerance) live in `FsharpEnvLoader.EnvTier`, shared with the sibling
// `ose-be` / `organiclever-be` backends.

/// Composition-root entry point — call as the first statement in `main`,
/// before any config is read. Fail-loudly-on-required-but-absent-config stays
/// exactly as-is downstream in `DatabaseConfiguration.fromEnvironment` and
/// `HttpConfiguration.parse`, which already fail when a required variable is
/// absent once this loader has run.
///
/// `dotnet run --project apps/beavernest-be/src/BeaverNestBe/BeaverNestBe.fsproj`
/// (the Nx `run`/`dev` targets) runs with the repo root as the working
/// directory — empirically verified 2026-08-12 — so "apps/beavernest-be" is
/// checked; running `dotnet run` directly from inside apps/beavernest-be/
/// makes that directory the working directory itself, so "." is checked too
/// — either way, the tier file resolves correctly.
let loadEnvTier () : unit =
    FsharpEnvLoader.EnvTier.loadEnvTierFrom [ Path.Combine("apps", "beavernest-be"); "." ]
