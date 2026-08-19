module BeaverNestBe.Domain.HttpConfiguration

open System
open System.Globalization

type ListenerConfiguration = { Address: string; Port: int }

let private environmentValue (readEnvironment: string -> string) key =
    match readEnvironment key with
    | null
    | "" -> None
    | value -> Some value

let private validPort value = value > 0 && value <= 65535

/// Parses the only supported HTTP listener configuration. Host processes are
/// deliberately loopback-only; container publication must be explicit.
let parse (readEnvironment: string -> string) : Result<ListenerConfiguration, string> =
    let runningInContainer =
        environmentValue readEnvironment "DOTNET_RUNNING_IN_CONTAINER" = Some "true"

    let address =
        environmentValue readEnvironment "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS"
        |> Option.defaultValue "127.0.0.1"

    let port =
        environmentValue readEnvironment "BEAVERNEST_BE_HTTP_LISTEN_PORT"
        |> Option.defaultValue "19300"

    // NumberStyles.None matches FsharpEnvLoader.PortResolver.parsePort exactly: plain digits only,
    // so `+4000` and `0x1F4` are rejected here rather than passing this tier and then failing
    // applyPortFlag's stricter re-parse of the same raw string. One variable, one grammar.
    match Int32.TryParse(port, NumberStyles.None, CultureInfo.InvariantCulture) with
    | true, parsedPort when validPort parsedPort ->
        match address, runningInContainer with
        | "127.0.0.1", _ -> Ok { Address = address; Port = parsedPort }
        | "0.0.0.0", true -> Ok { Address = address; Port = parsedPort }
        | "0.0.0.0", false -> Error "wildcard HTTP listening is container-only"
        | _ -> Error "HTTP listener address must be loopback or explicit container wildcard"
    | _ -> Error "HTTP listener port must be an integer between 1 and 65535"

let url configuration =
    $"http://%s{configuration.Address}:%d{configuration.Port}"

/// True when argv carries nothing but a `--port` override, in either spelling — including a
/// trailing bare `--port` with no value, which the shared resolver treats as "no flag supplied"
/// and falls through to the env var rather than erroring.
///
/// `Program.commandMode` classifies argv as a subcommand (`backup`, `integrity`, `restore`) and
/// rejects anything it does not recognise. Without this predicate it treated `--port 4000` as an
/// unrecognised subcommand and refused to boot — the reason a port flag was previously impossible
/// for this service.
let isOnlyPortFlags (args: string[]) : bool =
    match args with
    | [||] -> true
    | [| "--port"; _ |] -> true
    | [| single |] -> single = "--port" || single.StartsWith("--port=", StringComparison.Ordinal)
    | _ -> false

/// Applies the repo-wide `--port` flag on top of an already-parsed listener.
///
/// `parse` has resolved the env-var and default tiers already, so passing its port through as the
/// fallback yields exactly the shared precedence — flag, then BEAVERNEST_BE_HTTP_LISTEN_PORT, then
/// the 19300 default — without changing `parse`'s signature or weakening its loopback/wildcard
/// guard, which still owns the address half of the decision.
let applyPortFlag
    (argv: string[])
    (readEnvironment: string -> string)
    (listener: ListenerConfiguration)
    : Result<ListenerConfiguration, string> =
    FsharpEnvLoader.PortResolver.resolvePort argv readEnvironment "BEAVERNEST_BE_HTTP_LISTEN_PORT" listener.Port
    |> Result.map (fun port -> { listener with Port = port })
