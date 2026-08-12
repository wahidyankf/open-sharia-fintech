namespace OseBe.Contexts.Config

open System
open System.IO

/// Infrastructure layer for the config bounded context: loads the tiered
/// `.env.<APP_ENV>` file (see specs/apps/ose/ddd/ubiquitous-language/config.md)
/// so that agent-restricted tiers (.env.stag, .env.prod) never need to be
/// opened by an AI agent, while process environment variables set by CI
/// always take precedence over any file value.
module Infrastructure =

    /// Reads APP_ENV (default "local") — the tier selector for the repo's
    /// tiered env-file convention: exactly one .env.<APP_ENV> file is loaded
    /// per process.
    let private resolveTier () : string =
        match Environment.GetEnvironmentVariable("APP_ENV") with
        | null
        | "" -> "local"
        | value -> value

    /// Parses a single ".env" line into a KEY, VALUE pair. Blank lines and
    /// lines starting with "#" (comments) yield None, as do lines with no "=".
    let private parseLine (line: string) : (string * string) option =
        let trimmed = line.Trim()

        if trimmed = "" || trimmed.StartsWith("#", StringComparison.Ordinal) then
            None
        else
            match trimmed.IndexOf('=') with
            | -1 -> None
            | idx ->
                let key = trimmed.Substring(0, idx).Trim()
                let value = trimmed.Substring(idx + 1).Trim()
                if key = "" then None else Some(key, value)

    /// Applies a tier file's KEY=VALUE lines to the process environment.
    /// Process env always wins: a variable already set (present at all —
    /// null-check only, so an explicit empty string still counts as set) is
    /// left untouched, so CI's real environment variables are never
    /// overridden. Matches the six TS loaders' `dotenv({ override: false })`
    /// presence semantics (they test via `hasOwnProperty`, which doesn't care
    /// whether an existing value is empty).
    let private applyEnvFile (path: string) : unit =
        path
        |> File.ReadLines
        |> Seq.choose parseLine
        |> Seq.iter (fun (key, value) ->
            match Environment.GetEnvironmentVariable(key) with
            | null -> Environment.SetEnvironmentVariable(key, value)
            | _ -> ())

    /// Loads .env.<APP_ENV> per the repo's tiered env-file convention: process
    /// env always wins over file values, and a missing file is not an error
    /// (the normal case in CI, where real env vars are set with no file on
    /// disk). Searches `searchDirs` in order for the first ".env.<tier>" file
    /// that exists; does nothing if none of them do.
    let loadEnvTierFrom (searchDirs: string list) : unit =
        let fileName = $".env.%s{resolveTier ()}"

        searchDirs
        |> List.map (fun dir -> Path.Combine(dir, fileName))
        |> List.tryFind File.Exists
        |> Option.iter applyEnvFile

    /// Composition-root entry point. `dotnet run --project apps/ose-be/src/OseBe/OseBe.fsproj`
    /// (the Nx `run`/`dev` targets) runs with the repo root as the working
    /// directory, so "apps/ose-be" is checked; running `dotnet run` directly
    /// from inside apps/ose-be/ makes that directory the working directory
    /// itself, so "." is checked too — either way, the tier file resolves
    /// correctly.
    let loadEnvTier () : unit =
        loadEnvTierFrom [ Path.Combine("apps", "ose-be"); "." ]
