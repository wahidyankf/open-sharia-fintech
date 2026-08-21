namespace FsharpEnvLoader

open System
open System.IO

/// Shared tiered `.env.<APP_ENV>` env-file loader for this repo's F# backends
/// (`ose-be`, `organiclever-be`) — see the
/// `restrict-env-access-to-prod-and-stag` plan's `tech-docs.md` "The APP_ENV
/// loader contract" for the full rationale. Agent-restricted tiers
/// (`.env.stag`, `.env.prod`) never need to be opened by an AI agent, while
/// process environment variables set by CI always take precedence over any
/// file value. Mirrors the sibling TypeScript loader at
/// `libs/ts-env-loader/src/index.ts` (same four rules, same
/// process-env-wins / missing-file-is-not-an-error semantics), adapted for
/// F#.
///
/// Each consuming app calls `loadEnvTierFrom` itself, explicitly, as the
/// first statement of its own composition root (`Program.fs`'s `main`) —
/// this module never calls itself on load, so it never silently competes
/// with an app's own loader.
module EnvTier =

    /// Rule 1 of the loader contract — the tier selector: reads APP_ENV
    /// (default "local").
    let resolveTier () : string =
        match Environment.GetEnvironmentVariable("APP_ENV") with
        | null
        | "" -> "local"
        | value -> value

    /// Parses a single ".env" line into a KEY, VALUE pair. Blank lines and
    /// lines starting with "#" (comments) yield None, as do lines with no
    /// "=". A value may itself contain "=" — only the first "=" splits the
    /// line, matching the six TS loaders' `dotenv` parsing.
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

    /// Rule 3 of the loader contract — process env always wins: applies a
    /// tier file's KEY=VALUE lines to the process environment, leaving a
    /// variable that is already set (present at all — null-check only, so
    /// an explicit empty string still counts as set) untouched, so CI's real
    /// environment variables are never overridden. Matches the six TS
    /// loaders' `dotenv({ override: false })` presence semantics (they test
    /// via `hasOwnProperty`, which doesn't care whether an existing value is
    /// empty).
    let private applyEnvFile (path: string) : unit =
        path
        |> File.ReadLines
        |> Seq.choose parseLine
        |> Seq.iter (fun (key, value) ->
            match Environment.GetEnvironmentVariable(key) with
            | null -> Environment.SetEnvironmentVariable(key, value)
            | _ -> ())

    /// Rules 2 and 4 of the loader contract — one file, and a missing file
    /// is not an error: loads `.env.<APP_ENV>`, searching `searchDirs` in
    /// order for the first tier file that exists and applying it; does
    /// nothing if none of them do (the normal case in CI, where real env
    /// vars are set with no file on disk).
    let loadEnvTierFrom (searchDirs: string list) : unit =
        let fileName = $".env.%s{resolveTier ()}"

        searchDirs
        |> List.map (fun dir -> Path.Combine(dir, fileName))
        |> List.tryFind File.Exists
        |> Option.iter applyEnvFile
