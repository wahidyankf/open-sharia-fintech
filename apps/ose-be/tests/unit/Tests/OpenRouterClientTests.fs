module OseBe.Tests.Unit.Tests.OpenRouterClientTests

open System
open Xunit
open OseBe.Infrastructure.OpenRouterClient
open OseBe.Infrastructure.OpenRouterConnect

/// Saves and restores the three OSE_BE_OPENROUTER_* variables around a test
/// body so this module's mutations of process-wide environment state never
/// leak into other tests.
let private withOpenRouterEnv
    (apiKey: string option)
    (model: string option)
    (baseUrl: string option)
    (body: unit -> unit)
    =
    let previousApiKey = Environment.GetEnvironmentVariable("OSE_BE_OPENROUTER_API_KEY")
    let previousModel = Environment.GetEnvironmentVariable("OSE_BE_OPENROUTER_MODEL")

    let previousBaseUrl =
        Environment.GetEnvironmentVariable("OSE_BE_OPENROUTER_BASE_URL")

    try
        Environment.SetEnvironmentVariable("OSE_BE_OPENROUTER_API_KEY", (defaultArg apiKey null))
        Environment.SetEnvironmentVariable("OSE_BE_OPENROUTER_MODEL", (defaultArg model null))
        Environment.SetEnvironmentVariable("OSE_BE_OPENROUTER_BASE_URL", (defaultArg baseUrl null))
        body ()
    finally
        Environment.SetEnvironmentVariable("OSE_BE_OPENROUTER_API_KEY", previousApiKey)
        Environment.SetEnvironmentVariable("OSE_BE_OPENROUTER_MODEL", previousModel)
        Environment.SetEnvironmentVariable("OSE_BE_OPENROUTER_BASE_URL", previousBaseUrl)

[<Fact>]
let ``loadConfig falls back to documented defaults when unset`` () =
    withOpenRouterEnv None None None (fun () ->
        let config = loadConfig ()
        Assert.Equal("", config.ApiKey)
        Assert.Equal(DefaultModel, config.Model)
        Assert.Equal(DefaultBaseUrl, config.BaseUrl))

[<Fact>]
let ``loadConfig returns the configured values when set`` () =
    withOpenRouterEnv
        (Some "sk-test-key")
        (Some "openrouter/custom-model")
        (Some "https://example.internal/v1")
        (fun () ->
            let config = loadConfig ()
            Assert.Equal("sk-test-key", config.ApiKey)
            Assert.Equal("openrouter/custom-model", config.Model)
            Assert.Equal("https://example.internal/v1", config.BaseUrl))

[<Fact>]
let ``isConfigured is false when the API key is blank`` () =
    Assert.False(
        isConfigured
            { ApiKey = ""
              Model = DefaultModel
              BaseUrl = DefaultBaseUrl }
    )

[<Fact>]
let ``isConfigured is true when the API key is set`` () =
    Assert.True(
        isConfigured
            { ApiKey = "sk-test-key"
              Model = DefaultModel
              BaseUrl = DefaultBaseUrl }
    )

// complete's live-HTTP branches require a real OpenRouter endpoint and are
// excluded from unit coverage (see OpenRouterConnect.fs); this test proves the
// documented not-configured short-circuit, with no network required.
[<Fact>]
let ``complete returns an error without calling the network when no API key is configured`` () =
    let result =
        complete
            { ApiKey = ""
              Model = DefaultModel
              BaseUrl = DefaultBaseUrl }
            "prompt"
        |> Async.AwaitTask
        |> Async.RunSynchronously

    match result with
    | Error message -> Assert.Contains("not configured", message)
    | Ok _ -> Assert.Fail("expected Error when no API key is configured")
