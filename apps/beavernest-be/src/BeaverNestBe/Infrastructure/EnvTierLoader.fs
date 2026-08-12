module BeaverNestBe.Infrastructure.EnvTierLoader

open System
open System.IO

// Composition-root infrastructure: loads the tiered `.env.<APP_ENV>` file per
// the repo-wide `APP_ENV` loader contract (`restrict-env-access-to-prod-and-
// stag` plan, `tech-docs.md` §The APP_ENV loader contract) so that
// agent-restricted tiers (.env.stag, .env.prod) never need to be opened by an
// AI agent, while process environment variables set by CI always take
// precedence over any file value. Mirrors the sibling `ose-be` /
// `organiclever-be` F#/.NET loaders (same five rules, same shape) so the
// three backends stay consistent.

/// Rule 1 of the loader contract — the tier selector: reads APP_ENV (default
/// "local").
let private resolveTier () : string =
    match Environment.GetEnvironmentVariable("APP_ENV") with
    | null
    | "" -> "local"
    | value -> value

/// Parses a single ".env" line into a KEY, VALUE pair. Blank lines and lines
/// starting with "#" (comments) yield None, as do lines with no "=".
let private parseLine (line: string) : (string * string) option =
    let trimmed = line.Trim()

    if trimmed = "" || trimmed.StartsWith("#") then
        None
    else
        match trimmed.IndexOf('=') with
        | -1 -> None
        | index ->
            let key = trimmed.Substring(0, index).Trim()
            let value = trimmed.Substring(index + 1).Trim()
            if key = "" then None else Some(key, value)

/// Rule 3 of the loader contract — process env always wins: applies a tier
/// file's KEY=VALUE lines to the process environment, leaving a variable
/// that is already set (non-null, non-empty) untouched, so CI's real
/// environment variables are never overridden.
let private applyEnvFile (path: string) : unit =
    path
    |> File.ReadLines
    |> Seq.choose parseLine
    |> Seq.iter (fun (key, value) ->
        match Environment.GetEnvironmentVariable(key) with
        | null
        | "" -> Environment.SetEnvironmentVariable(key, value)
        | _ -> ())

/// Rules 2 and 4 of the loader contract — one file, and a missing file is not
/// an error: loads `.env.<APP_ENV>`, searching `searchDirs` in order for the
/// first tier file that exists and doing nothing if none of them do (the
/// normal case in CI, where real env vars are set with no file on disk).
let loadEnvTierFrom (searchDirs: string list) : unit =
    let fileName = $".env.%s{resolveTier ()}"

    searchDirs
    |> List.map (fun dir -> Path.Combine(dir, fileName))
    |> List.tryFind File.Exists
    |> Option.iter applyEnvFile

/// Composition-root entry point — call as the first statement in `main`,
/// before any config is read. Rule 5 (fail loudly on required-but-absent
/// config) is deliberately NOT this function's job: it stays exactly as-is
/// downstream in `DatabaseConfiguration.fromEnvironment` and
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
    loadEnvTierFrom [ Path.Combine("apps", "beavernest-be"); "." ]
