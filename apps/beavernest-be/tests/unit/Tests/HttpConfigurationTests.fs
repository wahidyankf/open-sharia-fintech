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
