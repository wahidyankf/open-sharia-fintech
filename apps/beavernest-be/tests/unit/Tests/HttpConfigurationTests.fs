module BeaverNestBe.Tests.Unit.Tests.HttpConfigurationTests

open Xunit
open BeaverNestBe.Domain.HttpConfiguration

let private environment entries key =
    entries |> Map.tryFind key |> Option.toObj

[<Fact>]
let ``listener configuration accepts only documented addresses and ports`` () =
    let cases =
        [ Map.empty, Ok { Address = "127.0.0.1"; Port = 19300 }
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS", "" ], Ok { Address = "127.0.0.1"; Port = 19300 }
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "" ], Ok { Address = "127.0.0.1"; Port = 19300 }
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "19320" ], Ok { Address = "127.0.0.1"; Port = 19320 }
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS", "0.0.0.0" ],
          Error "wildcard HTTP listening is container-only"
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS", "localhost" ],
          Error "HTTP listener address must be loopback or explicit container wildcard"
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "invalid" ],
          Error "HTTP listener port must be an integer between 1 and 65535"
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "0" ],
          Error "HTTP listener port must be an integer between 1 and 65535"
          Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "65536" ],
          Error "HTTP listener port must be an integer between 1 and 65535" ]

    cases
    |> List.iter (fun (entries, expected) -> Assert.Equal(expected, parse (environment entries)))

[<Fact>]
let ``listener accepts the Nx development loopback override`` () =
    let result =
        parse (environment (Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "19320" ]))

    Assert.Equal(Ok { Address = "127.0.0.1"; Port = 19320 }, result)

[<Fact>]
let ``wildcard listener requires an explicit container runtime`` () =
    let hostResult =
        parse (environment (Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS", "0.0.0.0" ]))

    let containerResult =
        parse (
            environment (
                Map.ofList
                    [ "BEAVERNEST_BE_HTTP_LISTEN_ADDRESS", "0.0.0.0"
                      "DOTNET_RUNNING_IN_CONTAINER", "true" ]
            )
        )

    Assert.True(Result.isError hostResult)
    Assert.Equal(Ok { Address = "0.0.0.0"; Port = 19300 }, containerResult)

[<Fact>]
let ``listener URL is constructed only from validated configuration`` () =
    let configuration =
        parse (environment (Map.ofList [ "BEAVERNEST_BE_HTTP_LISTEN_PORT", "19320" ]))
        |> Result.defaultWith failwith

    Assert.Equal("http://127.0.0.1:19320", url configuration)

// --- Runtime port override -------------------------------------------------

let private envWith (pairs: (string * string) list) : string -> string =
    fun key ->
        pairs
        |> List.tryFind (fun (name, _) -> name = key)
        |> Option.map snd
        |> Option.defaultValue null

let private noEnvironment: string -> string = envWith []

[<Theory>]
[<InlineData(true, "--port", "4000")>]
[<InlineData(true, "--port=4000", null)>]
[<InlineData(false, "backup", "--name")>]
[<InlineData(false, "integrity", null)>]
[<InlineData(false, "--verbose", null)>]
let ``isOnlyPortFlags recognises a bare port override and nothing else``
    (expected: bool)
    (first: string)
    (second: string)
    =
    let args = if isNull second then [| first |] else [| first; second |]
    Assert.Equal(expected, isOnlyPortFlags args)

[<Fact>]
let ``isOnlyPortFlags treats empty argv as a plain server start`` () = Assert.True(isOnlyPortFlags [||])

[<Fact>]
let ``applyPortFlag lets an explicit --port outrank the parsed listener`` () =
    let listener = { Address = "127.0.0.1"; Port = 19300 }

    Assert.Equal(Ok { Address = "127.0.0.1"; Port = 4000 }, applyPortFlag [| "--port"; "4000" |] noEnvironment listener)

[<Fact>]
let ``applyPortFlag keeps the parsed listener when no flag is given`` () =
    let listener = { Address = "127.0.0.1"; Port = 19320 }
    Assert.Equal(Ok listener, applyPortFlag [||] noEnvironment listener)

[<Fact>]
let ``applyPortFlag preserves the address half of the listener`` () =
    // The loopback/wildcard guard belongs to parse; the port flag must not disturb it.
    let listener = { Address = "0.0.0.0"; Port = 19300 }

    Assert.Equal(Ok { Address = "0.0.0.0"; Port = 4000 }, applyPortFlag [| "--port=4000" |] noEnvironment listener)

[<Fact>]
let ``applyPortFlag rejects a malformed --port instead of falling back`` () =
    let listener = { Address = "127.0.0.1"; Port = 19300 }

    match applyPortFlag [| "--port"; "99999" |] noEnvironment listener with
    | Ok configuration -> Assert.Fail($"expected an error, but resolved to %d{configuration.Port}")
    | Error message -> Assert.Contains("--port", message)
