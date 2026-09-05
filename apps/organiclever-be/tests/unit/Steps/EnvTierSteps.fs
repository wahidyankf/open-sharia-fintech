module OrganicleverBe.Tests.Unit.Steps.EnvTierSteps

open System.Collections.Generic
open TickSpec
open Xunit
open FsharpEnvLoader.EnvTier
open OrganicleverBe.Contexts.Env.Infrastructure

let private files = Dictionary<string, string list>()
let private environment = Dictionary<string, string>()
let private reads = ResizeArray<string>()
let mutable private startupError: exn option = None

let private normalize (path: string) = path.Replace('\\', '/')

let private readEnvironment key =
    match environment.TryGetValue key with
    | true, value -> value
    | false, _ -> null

let private ports: EnvTierPorts =
    { GetEnvironmentVariable = readEnvironment
      SetEnvironmentVariable = fun key value -> environment[key] <- value
      FileExists = fun path -> files.ContainsKey(normalize path)
      ReadLines =
        fun path ->
            let normalized = normalize path
            reads.Add normalized
            files[normalized]
      CombinePath = fun directory fileName -> $"{normalize directory}/{fileName}" }

let private reset () =
    files.Clear()
    environment.Clear()
    reads.Clear()
    startupError <- None

let private run () =
    try
        loadEnvTierWith ports
    with ex ->
        startupError <- Some ex

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () =
    reset ()

    for tier in [ "local"; "test"; "stag"; "prod" ] do
        files[$"apps/organiclever-be/.env.{tier}"] <- [ $"CONFIG_SOURCE=.env.{tier}" ]

[<When>]
let ``the process starts with APP_ENV set to "([^"]+)"`` (tier: string) =
    environment["APP_ENV"] <- tier
    run ()

[<Then>]
let ``configuration values are read from "\.env\.([^"]+)"`` (tier: string) =
    Assert.Equal($".env.{tier}", readEnvironment "CONFIG_SOURCE")
    Assert.Contains($"apps/organiclever-be/.env.{tier}", reads)

[<Then>]
let ``no value is read from any other env file`` () = Assert.Single(reads) |> ignore

[<Given>]
let ``a tier file at the app's composition root sets a variable to a file value`` () =
    reset ()
    files["apps/organiclever-be/.env.local"] <- [ "VALUE=file-value" ]

[<When>]
let ``the process starts with that variable already set in the process environment`` () =
    environment["APP_ENV"] <- "local"
    environment["VALUE"] <- "process-value"
    run ()

[<Then>]
let ``the process environment value is used`` () =
    Assert.Equal("process-value", readEnvironment "VALUE")

[<Then>]
let ``the tier file value is not applied over it`` () =
    Assert.Equal("process-value", readEnvironment "VALUE")
    Assert.Single(reads) |> ignore

[<Given>]
let ``no tier file exists at the app's composition root for the selected tier`` () =
    reset ()
    environment["EXISTING"] <- "preserved"

[<When>]
let ``the process starts with APP_ENV set to that tier`` () =
    environment["APP_ENV"] <- "test"
    run ()

[<Then>]
let ``startup does not throw`` () =
    Assert.True(startupError.IsNone, "missing tier files must not fail startup")

[<Then>]
let ``configuration proceeds using whatever the process environment already supplies`` () =
    Assert.Equal("preserved", readEnvironment "EXISTING")
    Assert.Empty(reads)
