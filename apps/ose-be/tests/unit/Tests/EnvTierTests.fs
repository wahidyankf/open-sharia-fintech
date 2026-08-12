module OseBe.Tests.Unit.Tests.EnvTierTests

open System
open System.IO
open Xunit
open OseBe.Contexts.Config.Infrastructure

/// Creates an empty temp directory and returns its path; caller is
/// responsible for deleting it.
let private newTempDir () : string =
    let dir = Path.Combine(Path.GetTempPath(), $"ose-be-env-tier-test-{Guid.NewGuid()}")
    Directory.CreateDirectory(dir) |> ignore
    dir

/// Runs `body` with APP_ENV set to `tier`, restoring the prior value afterwards.
let private withAppEnv (tier: string) (body: unit -> unit) : unit =
    let previous = Environment.GetEnvironmentVariable("APP_ENV")

    try
        Environment.SetEnvironmentVariable("APP_ENV", tier)
        body ()
    finally
        Environment.SetEnvironmentVariable("APP_ENV", previous)

// @covers specs/apps/ose/behavior/be/gherkin/config/env-tier-loading.feature:ose-be loads exactly one tier file
[<Theory>]
[<InlineData("local")>]
[<InlineData("test")>]
[<InlineData("stag")>]
[<InlineData("prod")>]
let ``loadEnvTierFrom reads only the file matching APP_ENV`` (tier: string) =
    let tempDir = newTempDir ()
    let varName = $"OSE_BE_ENV_TIER_TEST_VALUE_{Guid.NewGuid():N}"

    try
        // A sibling tier file also exists — only the file matching APP_ENV must be read.
        File.WriteAllText(Path.Combine(tempDir, $".env.{tier}"), $"{varName}=from-{tier}\n")
        File.WriteAllText(Path.Combine(tempDir, ".env.other-tier"), $"{varName}=from-other-tier\n")

        withAppEnv tier (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal($"from-{tier}", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

// @covers specs/apps/ose/behavior/be/gherkin/config/env-tier-loading.feature:ose-be process env wins over a tier file value
[<Fact>]
let ``loadEnvTierFrom never overrides a variable already set in the process environment`` () =
    let tempDir = newTempDir ()
    let varName = $"OSE_BE_ENV_TIER_TEST_PRECEDENCE_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varName}=from-file\n")
        Environment.SetEnvironmentVariable(varName, "from-process-env")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("from-process-env", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

// @covers specs/apps/ose/behavior/be/gherkin/config/env-tier-loading.feature:ose-be tolerates a missing tier file
[<Fact>]
let ``loadEnvTierFrom does nothing when the tier file is absent`` () =
    let tempDir = newTempDir ()

    try
        // No .env.nonexistent-tier file is created — absence must not raise.
        withAppEnv "nonexistent-tier" (fun () -> loadEnvTierFrom [ tempDir ])
    finally
        Directory.Delete(tempDir, true)

// @covers specs/apps/ose/behavior/be/gherkin/config/env-tier-loading.feature:ose-be loads exactly one tier file
[<Fact>]
let ``loadEnvTier defaults to the local tier when APP_ENV is unset`` () =
    let tempDir = newTempDir ()
    let varName = $"OSE_BE_ENV_TIER_TEST_DEFAULT_{Guid.NewGuid():N}"
    let previousCwd = Directory.GetCurrentDirectory()
    let previousAppEnv = Environment.GetEnvironmentVariable("APP_ENV")

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.local"), $"{varName}=from-local\n")
        Environment.SetEnvironmentVariable("APP_ENV", null)
        Directory.SetCurrentDirectory(tempDir)

        loadEnvTier ()

        Assert.Equal("from-local", Environment.GetEnvironmentVariable(varName))
    finally
        Directory.SetCurrentDirectory(previousCwd)
        Environment.SetEnvironmentVariable("APP_ENV", previousAppEnv)
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)
