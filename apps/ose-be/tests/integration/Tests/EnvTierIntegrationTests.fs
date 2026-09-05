module OseBe.Tests.Integration.Tests.EnvTierIntegrationTests

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

// The loader's own rules (tier resolution, one-file, process-env-wins,
// missing-file tolerance, and parsing edge cases) are covered once, in
// libs/fsharp-env-loader/tests/unit/Tests/EnvTierTests.fs. This app's own
// test focuses on the thin wrapper: `loadEnvTier` must resolve this app's own
// composition-root search dirs (`apps/ose-be` then `.`) correctly.

[<Fact>]
let ``loadEnvTier defaults to the local tier when APP_ENV is unset, and resolves this app's own composition root`` () =
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

[<Fact>]
let ``loadEnvTier never overrides a variable already set in the process environment`` () =
    let tempDir = newTempDir ()
    let varName = $"OSE_BE_ENV_TIER_TEST_PRECEDENCE_{Guid.NewGuid():N}"
    let previousCwd = Directory.GetCurrentDirectory()
    let previousAppEnv = Environment.GetEnvironmentVariable("APP_ENV")

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varName}=from-file\n")
        Environment.SetEnvironmentVariable("APP_ENV", "test")
        Environment.SetEnvironmentVariable(varName, "from-process-env")
        Directory.SetCurrentDirectory(tempDir)

        loadEnvTier ()

        Assert.Equal("from-process-env", Environment.GetEnvironmentVariable(varName))
    finally
        Directory.SetCurrentDirectory(previousCwd)
        Environment.SetEnvironmentVariable("APP_ENV", previousAppEnv)
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTier does not throw when no tier file is present at either search dir`` () =
    let tempDir = newTempDir ()
    let previousCwd = Directory.GetCurrentDirectory()
    let previousAppEnv = Environment.GetEnvironmentVariable("APP_ENV")

    try
        // No .env.nonexistent-tier file is created — absence must not raise.
        Environment.SetEnvironmentVariable("APP_ENV", "nonexistent-tier")
        Directory.SetCurrentDirectory(tempDir)

        loadEnvTier ()
    finally
        Directory.SetCurrentDirectory(previousCwd)
        Environment.SetEnvironmentVariable("APP_ENV", previousAppEnv)
        Directory.Delete(tempDir, true)
