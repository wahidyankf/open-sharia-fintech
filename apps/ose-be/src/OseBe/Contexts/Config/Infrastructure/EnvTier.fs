namespace OseBe.Contexts.Config

open System.IO
open System.Diagnostics.CodeAnalysis

/// Infrastructure layer for the config bounded context: thin wrapper around the
/// shared `libs/fsharp-env-loader` tiered `.env.<APP_ENV>` loader so that
/// agent-restricted tiers (.env.stag, .env.prod) never need to be opened by an AI agent. The
/// loader rules themselves (tier resolution, process-env-wins, missing-file
/// tolerance) live in `FsharpEnvLoader.EnvTier`.
module Infrastructure =

    let private searchDirectories = [ Path.Combine("apps", "ose-be"); "." ]

    /// Loads this app's fixed composition-root search order through injected
    /// environment/filesystem ports for deterministic Unit proof.
    let loadEnvTierWith (ports: FsharpEnvLoader.EnvTier.EnvTierPorts) : unit =
        FsharpEnvLoader.EnvTier.loadEnvTierFromWith ports searchDirectories

    /// Composition-root entry point. `dotnet run --project apps/ose-be/src/OseBe/OseBe.fsproj`
    /// (the Nx `run`/`dev` targets) runs with the repo root as the working
    /// directory, so "apps/ose-be" is checked; running `dotnet run` directly
    /// from inside apps/ose-be/ makes that directory the working directory
    /// itself, so "." is checked too — either way, the tier file resolves
    /// correctly.
    [<ExcludeFromCodeCoverage(Justification = "Real filesystem/environment adapter; covered by Integration tests")>]
    let loadEnvTier () : unit =
        FsharpEnvLoader.EnvTier.loadEnvTierFrom searchDirectories
