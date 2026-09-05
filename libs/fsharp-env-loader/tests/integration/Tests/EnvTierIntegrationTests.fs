module FsharpEnvLoader.Tests.Integration.Tests.EnvTierIntegrationTests

open System
open System.IO
open Xunit
open FsharpEnvLoader.EnvTier

/// Creates an empty temp directory and returns its path; caller is
/// responsible for deleting it.
let private newTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), $"fsharp-env-loader-test-{Guid.NewGuid()}")

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

// --- Rule 1: tier selector -------------------------------------------------

[<Fact>]
let ``resolveTier defaults to "local" when APP_ENV is unset`` () =
    let previous = Environment.GetEnvironmentVariable("APP_ENV")

    try
        Environment.SetEnvironmentVariable("APP_ENV", null)
        Assert.Equal("local", resolveTier ())
    finally
        Environment.SetEnvironmentVariable("APP_ENV", previous)

[<Fact>]
let ``resolveTier defaults to "local" when APP_ENV is the empty string`` () =
    let previous = Environment.GetEnvironmentVariable("APP_ENV")

    try
        Environment.SetEnvironmentVariable("APP_ENV", "")
        Assert.Equal("local", resolveTier ())
    finally
        Environment.SetEnvironmentVariable("APP_ENV", previous)

[<Fact>]
let ``resolveTier reads APP_ENV when set`` () =
    withAppEnv "stag" (fun () -> Assert.Equal("stag", resolveTier ()))

// --- Rule 2: one file --------------------------------------------------

[<Theory>]
[<InlineData("local")>]
[<InlineData("test")>]
[<InlineData("stag")>]
[<InlineData("prod")>]
let ``loadEnvTierFrom reads only the file matching APP_ENV`` (tier: string) =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_VALUE_{Guid.NewGuid():N}"

    try
        // Sibling tier files also exist — only the file matching APP_ENV must be read.
        File.WriteAllText(Path.Combine(tempDir, ".env.local"), $"{varName}=from-local\n")
        File.WriteAllText(Path.Combine(tempDir, ".env.stag"), $"{varName}=from-stag\n")
        File.WriteAllText(Path.Combine(tempDir, $".env.{tier}"), $"{varName}=from-{tier}\n")

        withAppEnv tier (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal($"from-{tier}", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom checks each search directory in order and stops at the first match`` () =
    let firstDir = newTempDir ()
    let secondDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_SEARCH_ORDER_{Guid.NewGuid():N}"

    try
        // Only the second directory carries the tier file — the loader must
        // fall through the first (non-matching) directory to find it.
        File.WriteAllText(Path.Combine(secondDir, ".env.test"), $"{varName}=from-second-dir\n")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ firstDir; secondDir ]
            Assert.Equal("from-second-dir", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(firstDir, true)
        Directory.Delete(secondDir, true)

[<Fact>]
let ``loadEnvTierFrom does not read from a non-matching search directory once the first match is found`` () =
    let firstDir = newTempDir ()
    let secondDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_FIRST_MATCH_WINS_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(firstDir, ".env.test"), $"{varName}=from-first-dir\n")
        File.WriteAllText(Path.Combine(secondDir, ".env.test"), $"{varName}=from-second-dir\n")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ firstDir; secondDir ]
            Assert.Equal("from-first-dir", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(firstDir, true)
        Directory.Delete(secondDir, true)

// --- Rule 3: process env wins ----------------------------------------------

[<Fact>]
let ``loadEnvTierFrom never overrides a variable already set in the process environment`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_PRECEDENCE_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varName}=from-file\n")
        Environment.SetEnvironmentVariable(varName, "from-process-env")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("from-process-env", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

/// The deliberate fix from the review cycle: "already set" is a null-check
/// only, so a variable explicitly set to the empty string still counts as
/// present and must not be overwritten by a file value. Matches the TS
/// loaders' `hasOwnProperty` presence semantics.
[<Fact>]
let ``loadEnvTierFrom treats a process env variable explicitly set to the empty string as already set`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_EMPTY_STRING_PRESENCE_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varName}=from-file\n")
        Environment.SetEnvironmentVariable(varName, "")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom applies a file value when the variable is not set in the process environment`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_UNSET_APPLIES_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varName}=from-file\n")
        Environment.SetEnvironmentVariable(varName, null)

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("from-file", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

// --- Rule 4: missing file is not an error -----------------------------------

[<Fact>]
let ``loadEnvTierFrom does nothing when the tier file is absent`` () =
    let tempDir = newTempDir ()

    try
        // No .env.nonexistent-tier file is created — absence must not raise.
        withAppEnv "nonexistent-tier" (fun () -> loadEnvTierFrom [ tempDir ])
    finally
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom does nothing when no search directory exists at all`` () =
    let nonexistentDir =
        Path.Combine(Path.GetTempPath(), $"fsharp-env-loader-nonexistent-{Guid.NewGuid()}")

    withAppEnv "test" (fun () -> loadEnvTierFrom [ nonexistentDir ])

// --- Parsing edge cases ------------------------------------------------

[<Fact>]
let ``loadEnvTierFrom is a no-op against an empty tier file`` () =
    let tempDir = newTempDir ()

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), "")

        withAppEnv "test" (fun () -> loadEnvTierFrom [ tempDir ])
    finally
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom keeps only the substring after the first "=" when a value itself contains "="`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_EQUALS_IN_VALUE_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varName}=key=value=with=equals\n")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("key=value=with=equals", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom parses CRLF-terminated lines the same as LF-terminated lines`` () =
    let tempDir = newTempDir ()
    let varA = $"FSHARP_ENV_LOADER_TEST_CRLF_A_{Guid.NewGuid():N}"
    let varB = $"FSHARP_ENV_LOADER_TEST_CRLF_B_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"{varA}=value-a\r\n{varB}=value-b\r\n")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("value-a", Environment.GetEnvironmentVariable(varA))
            Assert.Equal("value-b", Environment.GetEnvironmentVariable(varB)))
    finally
        Environment.SetEnvironmentVariable(varA, null)
        Environment.SetEnvironmentVariable(varB, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom skips blank lines and full-line "#" comments`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_COMMENTS_{Guid.NewGuid():N}"

    try
        File.WriteAllText(
            Path.Combine(tempDir, ".env.test"),
            $"# a leading comment\n\n   \n{varName}=actual-value\n# a trailing comment\n"
        )

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("actual-value", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom skips a line with no "=" without throwing`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_NO_EQUALS_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"this line has no equals sign\n{varName}=set\n")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("set", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)

[<Fact>]
let ``loadEnvTierFrom trims surrounding whitespace from both key and value`` () =
    let tempDir = newTempDir ()
    let varName = $"FSHARP_ENV_LOADER_TEST_WHITESPACE_{Guid.NewGuid():N}"

    try
        File.WriteAllText(Path.Combine(tempDir, ".env.test"), $"   {varName}   =   padded-value   \n")

        withAppEnv "test" (fun () ->
            loadEnvTierFrom [ tempDir ]
            Assert.Equal("padded-value", Environment.GetEnvironmentVariable(varName)))
    finally
        Environment.SetEnvironmentVariable(varName, null)
        Directory.Delete(tempDir, true)
