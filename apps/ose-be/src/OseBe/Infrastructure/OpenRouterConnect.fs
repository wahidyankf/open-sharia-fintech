module OseBe.Infrastructure.OpenRouterConnect

open System
open System.Diagnostics.CodeAnalysis
open System.Net.Http
open System.Net.Http.Headers
open System.Text
open System.Text.Json
open System.Threading.Tasks
open OseBe.Infrastructure.OpenRouterClient

/// Requests a chat completion from OpenRouter for the given prompt.
///
/// Returns Ok with the model's text response, or Error with a diagnostic
/// message. When no API key is configured the call short-circuits with an
/// Error rather than issuing an unauthenticated request — that guard clause is
/// unit-tested directly in Tests/OpenRouterClientTests.fs, with no network
/// required. The live-HTTP branches beyond it require a real OpenRouter
/// endpoint and are not yet exercised by any E2E spec. Kept in its own file
/// (rather than alongside the pure,
/// fully unit-tested `loadConfig`/`isConfigured` in OpenRouterClient.fs) so
/// the project-level coverage `/p:ExcludeByFile` can exclude exactly this
/// live-network surface.
[<ExcludeFromCodeCoverage(Justification = "Requires a live OpenRouter API endpoint — see module doc comment above")>]
let complete (config: OpenRouterConfig) (prompt: string) : Task<Result<string, string>> =
    task {
        if not (isConfigured config) then
            return Error "OpenRouter API key is not configured"
        else
            try
                use client = new HttpClient()
                client.BaseAddress <- Uri(config.BaseUrl.TrimEnd('/') + "/")
                client.DefaultRequestHeaders.Authorization <- AuthenticationHeaderValue("Bearer", config.ApiKey)

                let payload =
                    JsonSerializer.Serialize(
                        {| model = config.Model
                           messages = [| {| role = "user"; content = prompt |} |] |}
                    )

                use content = new StringContent(payload, Encoding.UTF8, "application/json")
                use! response = client.PostAsync("chat/completions", content)
                let! body = response.Content.ReadAsStringAsync()

                if response.IsSuccessStatusCode then
                    return Ok body
                else
                    return Error(sprintf "OpenRouter returned %d: %s" (int response.StatusCode) body)
            with ex ->
                return Error(sprintf "OpenRouter request failed: %s" ex.Message)
    }
