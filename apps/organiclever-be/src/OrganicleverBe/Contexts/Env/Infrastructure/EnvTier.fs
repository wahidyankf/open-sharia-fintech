namespace OrganicleverBe.Contexts.Env

open System
open System.IO

/// Infrastructure layer for the env bounded context: the tiered
/// `.env.<APP_ENV>` loader every app in this repo implements identically, so
/// agent-restricted, sensitive `.env.stag`/`.env.prod` files never need to be
/// opened by an AI agent while `.env.local`/`.env.test` stay agent-readable.
module Infrastructure =

    /// Reads APP_ENV, defaulting to "local" when unset or empty — rule 1 of
    /// the repo's tiered env-file convention (every app loads exactly one
    /// `.env.<tier>` file selected by APP_ENV).
    let currentTier () : string =
        match Environment.GetEnvironmentVariable("APP_ENV") with
        | null
        | "" -> "local"
        | value -> value

    /// Parses `KEY=VALUE` lines from raw `.env` file content. Minimal by
    /// design — no quoting, escaping, or `export` syntax, matching this app's
    /// `.env.example` format. Blank lines and full-line `#` comments are
    /// skipped.
    let parseEnvLines (content: string) : (string * string) list =
        content.Split('\n')
        |> Array.map (fun line -> line.TrimEnd('\r').Trim())
        |> Array.filter (fun line -> line <> "" && not (line.StartsWith("#", StringComparison.Ordinal)))
        |> Array.choose (fun line ->
            match line.IndexOf('=') with
            | -1 -> None
            | idx -> Some(line.Substring(0, idx).Trim(), line.Substring(idx + 1).Trim()))
        |> Array.toList

    /// Applies parsed `KEY=VALUE` pairs to the process environment, but only
    /// for keys not already set — rule 3: process env always wins over file
    /// values. This is what lets CI work with no `.env.<tier>` file on disk:
    /// CI sets real env vars, and those are never replaced by a file value.
    let private applyIfUnset (pairs: (string * string) list) : unit =
        for key, value in pairs do
            let current = Environment.GetEnvironmentVariable(key)

            if String.IsNullOrEmpty(current) then
                Environment.SetEnvironmentVariable(key, value)

    /// Loads `<dir>/.env.<tier>` into the process environment
    /// (process-env-wins, see `applyIfUnset`). A missing file is not an error
    /// — rule 4, the normal case in CI. This is the primitive the unit tests
    /// exercise directly against a temp directory; `loadEnvTier` below is the
    /// composition-root wrapper used at real startup.
    let loadEnvTierFromDir (dir: string) (tier: string) : unit =
        let path = Path.Combine(dir, sprintf ".env.%s" tier)

        if File.Exists path then
            File.ReadAllText path |> parseEnvLines |> applyIfUnset

    /// Candidate composition-root directories, relative to the process's
    /// current working directory, searched in order for `.env.<tier>`.
    ///
    /// `dotnet run`/`dotnet test` do NOT change the working directory to the
    /// project directory — they inherit the invoking shell's CWD (verified
    /// empirically: `dotnet run --project sub/proj/proj.fsproj` run from a
    /// parent directory leaves `Environment.CurrentDirectory` at that parent,
    /// not `sub/proj`). This repo's Nx targets always invoke `dotnet
    /// run`/`dotnet test` from the repo root with a full relative path (e.g.
    /// `dotnet run --project
    /// apps/organiclever-be/src/OrganicleverBe/OrganicleverBe.fsproj`), so
    /// the real-world composition root is `<repo-root>/apps/organiclever-be`.
    /// A developer who has already `cd`'d into `apps/organiclever-be` before
    /// invoking dotnet directly gets CWD itself instead — both are searched,
    /// and only the first candidate whose file exists is loaded (rule 2: one
    /// file).
    let private candidateDirs () : string list = [ "."; "apps/organiclever-be" ]

    /// Loads `.env.<APP_ENV>` per the repo's tiered env-file convention:
    /// reads APP_ENV (default "local"), searches this app's composition
    /// root, and applies file values only where the process environment
    /// doesn't already have them. Missing file is not an error. Call this as
    /// the first statement of `main`, before any required-config check (e.g.
    /// `requireDatabaseUrl`).
    let loadEnvTier () : unit =
        let tier = currentTier ()

        candidateDirs ()
        |> List.tryFind (fun dir -> File.Exists(Path.Combine(dir, sprintf ".env.%s" tier)))
        |> Option.iter (fun dir -> loadEnvTierFromDir dir tier)
