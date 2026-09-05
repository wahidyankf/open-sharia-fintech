module OseBe.Tests.Unit.Tests.EnvTierTests

open System.Collections.Generic
open Xunit
open FsharpEnvLoader.EnvTier
open OseBe.Contexts.Config.Infrastructure

[<Fact>]
let ``loadEnvTierWith probes the ose-be composition root before cwd`` () =
    let probes = ResizeArray<string>()
    let environment = Dictionary<string, string>()
    environment["APP_ENV"] <- "test"

    let ports: EnvTierPorts =
        { GetEnvironmentVariable =
            fun key ->
                if environment.ContainsKey key then
                    environment[key]
                else
                    null
          SetEnvironmentVariable = fun key value -> environment[key] <- value
          FileExists =
            fun path ->
                probes.Add(path.Replace('\\', '/'))
                false
          ReadLines = fun _ -> Seq.empty
          CombinePath = fun directory fileName -> $"{directory.Replace('\\', '/')}/{fileName}" }

    loadEnvTierWith ports

    Assert.Equal<string list>([ "apps/ose-be/.env.test"; "./.env.test" ], List.ofSeq probes)

[<Fact>]
let ``loadEnvTierWith applies the first matching composition-root file`` () =
    let environment = Dictionary<string, string>()
    environment["APP_ENV"] <- "local"

    let ports: EnvTierPorts =
        { GetEnvironmentVariable =
            fun key ->
                if environment.ContainsKey key then
                    environment[key]
                else
                    null
          SetEnvironmentVariable = fun key value -> environment[key] <- value
          FileExists = fun path -> path.Replace('\\', '/') = "apps/ose-be/.env.local"
          ReadLines = fun _ -> seq { "SOURCE=ose-be" }
          CombinePath = fun directory fileName -> $"{directory.Replace('\\', '/')}/{fileName}" }

    loadEnvTierWith ports

    Assert.Equal("ose-be", environment["SOURCE"])
