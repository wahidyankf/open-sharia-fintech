module FsharpEnvLoader.Tests.Unit.Tests.EnvTierTests

open Xunit
open FsharpEnvLoader.EnvTier

[<Fact>]
let ``resolveTierWith defaults to local without APP_ENV`` () =
    Assert.Equal("local", resolveTierWith (fun _ -> null))

[<Fact>]
let ``resolveTierWith preserves a selected tier`` () =
    Assert.Equal("stag", resolveTierWith (fun key -> if key = "APP_ENV" then "stag" else null))

[<Fact>]
let ``loadEnvTierFromWith uses injected environment and filesystem ports`` () =
    let mutable environment = Map.ofList [ "APP_ENV", "test" ]
    let mutable reads: string list = []

    let ports =
        { GetEnvironmentVariable = fun key -> environment |> Map.tryFind key |> Option.defaultValue null
          SetEnvironmentVariable = fun key value -> environment <- environment.Add(key, value)
          FileExists = fun path -> path = "root/.env.test"
          ReadLines =
            fun path ->
                reads <- path :: reads
                seq { "VALUE=from-file" }
          CombinePath = fun directory fileName -> $"{directory}/{fileName}" }

    loadEnvTierFromWith ports [ "root" ]

    Assert.Equal("from-file", environment["VALUE"])
    Assert.Equal<string list>([ "root/.env.test" ], reads)

[<Fact>]
let ``loadEnvTierFromWith preserves an existing environment value`` () =
    let mutable environment = Map.ofList [ "APP_ENV", "test"; "VALUE", "from-process" ]

    let ports =
        { GetEnvironmentVariable = fun key -> environment |> Map.tryFind key |> Option.defaultValue null
          SetEnvironmentVariable = fun key value -> environment <- environment.Add(key, value)
          FileExists = fun _ -> true
          ReadLines = fun _ -> seq { "VALUE=from-file" }
          CombinePath = fun directory fileName -> $"{directory}/{fileName}" }

    loadEnvTierFromWith ports [ "root" ]

    Assert.Equal("from-process", environment["VALUE"])
