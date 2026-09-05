namespace OrganicleverBe.Contexts.Env

open System.IO
open System.Diagnostics.CodeAnalysis

/// Infrastructure layer for the env bounded context: thin wrapper around the
/// shared `libs/fsharp-env-loader` tiered `.env.<APP_ENV>` loader, so
/// agent-restricted, sensitive `.env.stag`/`.env.prod` files never need to be
/// opened by an AI agent while `.env.local`/`.env.test` stay agent-readable.
/// The loader rules themselves (tier resolution, process-env-wins,
/// missing-file tolerance) live in `FsharpEnvLoader.EnvTier`, shared with the
/// sibling `ose-be` backend.
module Infrastructure =

    let private searchDirectories = [ Path.Combine("apps", "organiclever-be"); "." ]

    /// Loads this app's fixed composition-root search order through injected
    /// environment/filesystem ports for deterministic Unit proof.
    let loadEnvTierWith (ports: FsharpEnvLoader.EnvTier.EnvTierPorts) : unit =
        FsharpEnvLoader.EnvTier.loadEnvTierFromWith ports searchDirectories

    /// Loads `.env.<APP_ENV>` per the repo's tiered env-file convention.
    /// Call this as the first statement of `main`, before any required-config
    /// check (e.g. `requireDatabaseUrl`).
    ///
    /// `dotnet run`/`dotnet test` inherit the invoking shell's working
    /// directory rather than changing to the project directory, so this
    /// app's Nx targets always invoke `dotnet run`/`dotnet test` from the
    /// repo root with a full relative path, making the real-world
    /// composition root `<repo-root>/apps/organiclever-be`; a developer who
    /// has already `cd`'d into `apps/organiclever-be` gets CWD itself
    /// instead — both are searched, and only the first candidate whose file
    /// exists is loaded.
    [<ExcludeFromCodeCoverage(Justification = "Real filesystem/environment adapter; covered by Integration tests")>]
    let loadEnvTier () : unit =
        FsharpEnvLoader.EnvTier.loadEnvTierFrom searchDirectories
