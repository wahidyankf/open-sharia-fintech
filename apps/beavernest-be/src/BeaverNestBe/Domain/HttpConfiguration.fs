module BeaverNestBe.Domain.HttpConfiguration

open System

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

    match Int32.TryParse port with
    | true, parsedPort when validPort parsedPort ->
        match address, runningInContainer with
        | "127.0.0.1", _ -> Ok { Address = address; Port = parsedPort }
        | "0.0.0.0", true -> Ok { Address = address; Port = parsedPort }
        | "0.0.0.0", false -> Error "wildcard HTTP listening is container-only"
        | _ -> Error "HTTP listener address must be loopback or explicit container wildcard"
    | _ -> Error "HTTP listener port must be an integer between 1 and 65535"

let url configuration =
    $"http://%s{configuration.Address}:%d{configuration.Port}"
