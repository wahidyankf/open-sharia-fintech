module OrganicleverBe.Tests.Integration.Steps.EnvTierSteps

open System
open System.IO
open TickSpec
open Xunit
open OrganicleverBe.Contexts.Env.Infrastructure

let mutable private tempDir = ""
let mutable private previousCwd = ""
let mutable private previousAppEnv: string = null
let mutable private selectedTier = ""
let mutable private touchedKeys: string list = []
let mutable private previousValues: Map<string, string> = Map.empty
let mutable private startupError: exn option = None

let private beginScenario () =
    tempDir <- Path.Combine(Path.GetTempPath(), $"organiclever-be-env-integration-{Guid.NewGuid():N}")
    Directory.CreateDirectory(tempDir) |> ignore
    previousCwd <- Directory.GetCurrentDirectory()
    previousAppEnv <- Environment.GetEnvironmentVariable("APP_ENV")
    Directory.SetCurrentDirectory(tempDir)
    touchedKeys <- []
    previousValues <- Map.empty
    startupError <- None

let private finishScenario () =
    Directory.SetCurrentDirectory(previousCwd)
    Environment.SetEnvironmentVariable("APP_ENV", previousAppEnv)

    for key in touchedKeys do
        Environment.SetEnvironmentVariable(key, previousValues |> Map.tryFind key |> Option.toObj)

    if Directory.Exists tempDir then
        Directory.Delete(tempDir, true)

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () =
    beginScenario ()

    for tier in [ "local"; "test"; "stag"; "prod" ] do
        let key = $"ORGANICLEVER_BE_ENV_{tier.ToUpperInvariant()}"
        previousValues <- previousValues.Add(key, Environment.GetEnvironmentVariable key)
        File.WriteAllText(Path.Combine(tempDir, $".env.{tier}"), $"{key}=from-{tier}\n")
        touchedKeys <- key :: touchedKeys

[<When>]
let ``the process starts with APP_ENV set to "([^"]+)"`` (tier: string) =
    selectedTier <- tier
    Environment.SetEnvironmentVariable("APP_ENV", tier)
    loadEnvTier ()

[<Then>]
let ``configuration values are read from "\.env\.([^"]+)"`` (tier: string) =
    Assert.Equal(tier, selectedTier)
    Assert.Equal($"from-{tier}", Environment.GetEnvironmentVariable($"ORGANICLEVER_BE_ENV_{tier.ToUpperInvariant()}"))

[<Then>]
let ``no value is read from any other env file`` () =
    for tier in [ "local"; "test"; "stag"; "prod" ] |> List.filter ((<>) selectedTier) do
        Assert.Null(Environment.GetEnvironmentVariable($"ORGANICLEVER_BE_ENV_{tier.ToUpperInvariant()}"))


[<Given>]
let ``a tier file at the app's composition root sets a variable to a file value`` () =
    beginScenario ()
    File.WriteAllText(Path.Combine(tempDir, ".env.local"), "ORGANICLEVER_BE_PRECEDENCE=file-value\n")
    touchedKeys <- [ "ORGANICLEVER_BE_PRECEDENCE" ]

    previousValues <-
        previousValues.Add(
            "ORGANICLEVER_BE_PRECEDENCE",
            Environment.GetEnvironmentVariable "ORGANICLEVER_BE_PRECEDENCE"
        )

[<When>]
let ``the process starts with that variable already set in the process environment`` () =
    Environment.SetEnvironmentVariable("APP_ENV", "local")
    Environment.SetEnvironmentVariable("ORGANICLEVER_BE_PRECEDENCE", "process-value")
    loadEnvTier ()

[<Then>]
let ``the process environment value is used`` () =
    Assert.Equal("process-value", Environment.GetEnvironmentVariable("ORGANICLEVER_BE_PRECEDENCE"))

[<Then>]
let ``the tier file value is not applied over it`` () =
    Assert.Equal("process-value", Environment.GetEnvironmentVariable("ORGANICLEVER_BE_PRECEDENCE"))

[<Given>]
let ``no tier file exists at the app's composition root for the selected tier`` () =
    beginScenario ()
    Environment.SetEnvironmentVariable("ORGANICLEVER_BE_EXISTING", "preserved")
    touchedKeys <- [ "ORGANICLEVER_BE_EXISTING" ]

    previousValues <-
        previousValues.Add("ORGANICLEVER_BE_EXISTING", Environment.GetEnvironmentVariable "ORGANICLEVER_BE_EXISTING")

[<When>]
let ``the process starts with APP_ENV set to that tier`` () =
    Environment.SetEnvironmentVariable("APP_ENV", "test")

    startupError <-
        try
            loadEnvTier ()
            None
        with ex ->
            Some ex

[<Then>]
let ``startup does not throw`` () = Assert.True(startupError.IsNone)

[<Then>]
let ``configuration proceeds using whatever the process environment already supplies`` () =
    Assert.Equal("preserved", Environment.GetEnvironmentVariable("ORGANICLEVER_BE_EXISTING"))

[<AfterScenario>]
let ``restore the process environment and working directory`` () = finishScenario ()
