namespace FsharpEnvLoader

open System
open System.Globalization

/// The repo-wide runtime port contract for this repo's F# backends (`ose-be`,
/// `organiclever-be`). Mirrors the sibling TypeScript resolver at
/// `libs/ts-env-loader/src/port-resolver.ts` (`resolvePort`), so a TypeScript
/// service and an F# service accept and reject exactly the same port values.
///
/// Mirrored: the three-tier precedence below, the grammar of a valid port
/// (plain decimal digits, 1-65535), blank-falls-through, and
/// fail-loudly-on-malformed. Not mirrored: the exact error wording.
///
/// Precedence, highest first:
///   1. CLI flag  — an explicit `--port` passed at start time, in either
///                  `--port 4000` or `--port=4000` form.
///   2. Env var   — the app's own prefixed variable (e.g. `OSE_BE_PORT`),
///                  never a bare `PORT`. A prefixed name is what lets one
///                  shell hold every app's port at once; see
///                  `repo-governance/conventions/security/secrets-and-env-standards/environment-variable-naming-standard.md`.
///   3. Fallback  — the app's compiled-in default, which is also the value
///                  documented in `docs/reference/web-sites.md`.
///
/// An empty or whitespace-only value at a tier is treated as absent and falls
/// through to the next tier, matching `EnvTier`'s treatment of an empty
/// `APP_ENV`. A PRESENT but malformed value is a hard error rather than a
/// silent fall-through: a typo'd `--port 80800` must not quietly boot the
/// service on its default port, because the operator asked for something
/// specific and did not get it.
///
/// The environment is read through a caller-supplied `readEnvironment`
/// function rather than `Environment.GetEnvironmentVariable` directly, so the
/// unit suite can drive every scenario without touching the real process
/// environment.
module PortResolver =

    /// Lowest legal TCP port. Port 0 means "let the OS choose", which is never
    /// what an operator naming a port intends, so it is rejected.
    let private minPort: int = 1

    /// Highest legal TCP port (16-bit unsigned ceiling).
    let private maxPort: int = 65535

    /// Treats absent, empty, and whitespace-only alike as "not supplied", so a
    /// blank tier falls through instead of erroring.
    let private presentValue (value: string) : string option =
        match value with
        | null -> None
        | text ->
            let trimmed = text.Trim()
            if trimmed = "" then None else Some trimmed

    /// Parses one tier's value, naming that tier in the error so the message
    /// says which knob was wrong.
    ///
    /// `NumberStyles.None` is deliberate: it admits only plain digits, so
    /// `-1`, `31.5`, and `3100abc` are all rejected outright rather than
    /// partially parsed. That matches the TypeScript twin's use of `Number()`
    /// over `parseInt()`, which would silently accept `parseInt("3100abc")` as
    /// 3100.
    let private parsePort (text: string) (source: string) : Result<int, string> =
        match Int32.TryParse(text, NumberStyles.None, CultureInfo.InvariantCulture) with
        | true, parsed when parsed >= minPort && parsed <= maxPort -> Ok parsed
        | _ ->
            Error
                $"env-loader: %s{source} supplied an invalid port \"%s{text}\". A port must be an integer between %d{minPort} and %d{maxPort}."

    /// Finds an explicit `--port` in `argv`, accepting both the space-separated
    /// (`--port 4000`) and the joined (`--port=4000`) spellings. A trailing
    /// bare `--port` with no following value yields None, so it falls through
    /// to the env var rather than erroring on an empty string.
    let private flagValue (argv: string[]) : string option =
        let rec scan (index: int) : string option =
            if index >= argv.Length then
                None
            else
                let current = argv.[index]

                if current.StartsWith("--port=", StringComparison.Ordinal) then
                    Some(current.Substring("--port=".Length))
                elif current = "--port" && index + 1 < argv.Length then
                    Some argv.[index + 1]
                else
                    scan (index + 1)

        scan 0

    /// Resolves a listener port by the flag > env var > fallback precedence
    /// documented above. Returns Error when a tier is present but does not
    /// hold a valid port, or when the app's own compiled-in fallback is itself
    /// out of range (a programming error, caught at startup rather than
    /// shipped).
    let resolvePort
        (argv: string[])
        (readEnvironment: string -> string)
        (envVar: string)
        (fallback: int)
        : Result<int, string> =
        match flagValue argv |> Option.bind presentValue with
        | Some value -> parsePort value "--port"
        | None ->
            match presentValue (readEnvironment envVar) with
            | Some value -> parsePort value envVar
            | None ->
                if fallback >= minPort && fallback <= maxPort then
                    Ok fallback
                else
                    Error
                        $"env-loader: the compiled-in fallback for %s{envVar} is an invalid port %d{fallback}. A port must be an integer between %d{minPort} and %d{maxPort}."

    /// Shapes the ASP.NET listener URL for a resolved port.
    ///
    /// Loopback (`localhost`) on a developer machine, wildcard (`+`) only inside a container. The
    /// distinction is load-bearing in both directions: binding wildcard on a laptop exposes a
    /// development service to the local network, while binding loopback inside a container makes
    /// the service unreachable from outside it — the published port would connect to nothing.
    ///
    /// `DOTNET_RUNNING_IN_CONTAINER` is the signal this guard reads, and the official
    /// `mcr.microsoft.com/dotnet/aspnet` images set it to "true" themselves.
    let listenUrl (readEnvironment: string -> string) (port: int) : string =
        let host =
            match readEnvironment "DOTNET_RUNNING_IN_CONTAINER" with
            | "true" -> "+"
            | _ -> "localhost"

        $"http://%s{host}:%d{port}"
