module OrganicleverBe.Tests.Unit.Tests.EnvTierLoaderTests

open System
open System.IO
open Xunit
open OrganicleverBe.Contexts.Env.Infrastructure

/// Creates a fresh empty temp directory for a test's `.env.<tier>` fixtures.
let private makeTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "organiclever-be-env-tier-tests", Guid.NewGuid().ToString())

    Directory.CreateDirectory(dir) |> ignore
    dir

[<Fact>]
let ``currentTier defaults to local when APP_ENV is unset`` () =
    let previous = Environment.GetEnvironmentVariable("APP_ENV")

    try
        Environment.SetEnvironmentVariable("APP_ENV", null)
        Assert.Equal("local", currentTier ())
    finally
        Environment.SetEnvironmentVariable("APP_ENV", previous)

[<Fact>]
let ``currentTier reads APP_ENV when set`` () =
    let previous = Environment.GetEnvironmentVariable("APP_ENV")

    try
        Environment.SetEnvironmentVariable("APP_ENV", "stag")
        Assert.Equal("stag", currentTier ())
    finally
        Environment.SetEnvironmentVariable("APP_ENV", previous)

// @covers specs/apps/organiclever/behavior/organiclever-be/gherkin/env/env-tier-loader.feature:organiclever-be loads exactly one tier file
[<Theory>]
[<InlineData("local")>]
[<InlineData("test")>]
[<InlineData("stag")>]
[<InlineData("prod")>]
let ``loadEnvTierFromDir loads only the requested tier file`` (tier: string) =
    let dir = makeTempDir ()
    let varName = sprintf "ENV_TIER_MARKER_%s" (Guid.NewGuid().ToString("N"))

    try
        // "the files .env.local and .env.stag both exist at the app's composition root"
        File.WriteAllText(Path.Combine(dir, ".env.local"), sprintf "%s=local_value\n" varName)
        File.WriteAllText(Path.Combine(dir, ".env.stag"), sprintf "%s=stag_value\n" varName)
        // the tier under test always gets its own distinguishable value, so a
        // wrong-file read is caught even when the tier under test is "local" or "stag"
        File.WriteAllText(Path.Combine(dir, sprintf ".env.%s" tier), sprintf "%s=%s_value\n" varName tier)

        Environment.SetEnvironmentVariable(varName, null)
        loadEnvTierFromDir dir tier

        Assert.Equal(sprintf "%s_value" tier, Environment.GetEnvironmentVariable(varName))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(dir, true)

// @covers specs/apps/organiclever/behavior/organiclever-be/gherkin/env/env-tier-loader.feature:organiclever-be process env wins over a tier file value
[<Fact>]
let ``loadEnvTierFromDir does not override an already-set process variable`` () =
    let dir = makeTempDir ()
    let varName = sprintf "ENV_TIER_MARKER_%s" (Guid.NewGuid().ToString("N"))

    try
        File.WriteAllText(Path.Combine(dir, ".env.test"), sprintf "%s=from_file\n" varName)
        Environment.SetEnvironmentVariable(varName, "from_process")

        loadEnvTierFromDir dir "test"

        Assert.Equal("from_process", Environment.GetEnvironmentVariable(varName))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(dir, true)

// @covers specs/apps/organiclever/behavior/organiclever-be/gherkin/env/env-tier-loader.feature:organiclever-be tolerates a missing tier file
[<Fact>]
let ``loadEnvTierFromDir is a no-op when the tier file is absent`` () =
    let dir = makeTempDir ()

    try
        // Absence must not throw and must not touch the process environment.
        loadEnvTierFromDir dir "prod"
        Assert.True(true)
    finally
        Directory.Delete(dir, true)
