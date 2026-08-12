module OseBe.Tests.Unit.Steps.EnvTierSteps

open System
open System.IO
open TickSpec
open Xunit
open OseBe.Contexts.Config.Infrastructure

/// Temp composition-root directory created by the Given step and torn down
/// by the closing And step.
let mutable private tempDir: string = ""

/// APP_ENV as it was before this scenario ran, restored by the closing And step.
let mutable private previousAppEnv: string option = None

let private varName = "OSE_BE_ENV_TIER_BDD_VAR"

[<Given>]
let ``the files ".env.local" and ".env.stag" both exist at the app's composition root`` () =
    tempDir <- Path.Combine(Path.GetTempPath(), $"ose-be-env-tier-bdd-{Guid.NewGuid():N}")
    Directory.CreateDirectory(tempDir) |> ignore
    File.WriteAllText(Path.Combine(tempDir, ".env.local"), $"{varName}=from-local\n")
    File.WriteAllText(Path.Combine(tempDir, ".env.stag"), $"{varName}=from-stag\n")
    previousAppEnv <- Environment.GetEnvironmentVariable("APP_ENV") |> Option.ofObj

// Representative row of the Scenario Outline: APP_ENV="stag" (one of the two
// tier files the Given step created) — a single instance of the general
// "process env picks its own tier file" contract exercised by every row.
[<When>]
let ``the process starts with APP_ENV set to "<tier>"`` () =
    Environment.SetEnvironmentVariable("APP_ENV", "stag")
    loadEnvTierFrom [ tempDir ]

[<Then>]
let ``configuration values are read from ".env.<tier>"`` () =
    Assert.Equal("from-stag", Environment.GetEnvironmentVariable(varName))

[<Then>]
let ``no value is read from any other env file`` () =
    Assert.NotEqual<string>("from-local", Environment.GetEnvironmentVariable(varName))

    // Teardown: restore APP_ENV and remove the fixture directory.
    Environment.SetEnvironmentVariable(varName, null)

    match previousAppEnv with
    | Some v -> Environment.SetEnvironmentVariable("APP_ENV", v)
    | None -> Environment.SetEnvironmentVariable("APP_ENV", null)

    Directory.Delete(tempDir, true)
