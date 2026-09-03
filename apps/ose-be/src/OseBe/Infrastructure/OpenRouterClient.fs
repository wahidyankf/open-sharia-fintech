module OseBe.Infrastructure.OpenRouterClient

open System

/// OpenRouter LLM client configuration, sourced from the OSE_BE_OPENROUTER_*
/// environment variables. The API key is a secret: it is read from the
/// environment only and is never committed (placeholder in .env.example).
type OpenRouterConfig =
    { ApiKey: string
      Model: string
      BaseUrl: string }

/// Default OpenRouter model identifier.
[<Literal>]
let DefaultModel = "openrouter/auto"

/// Default OpenRouter API base URL.
[<Literal>]
let DefaultBaseUrl = "https://openrouter.ai/api/v1"

let private envOr (name: string) (fallback: string) : string =
    match Environment.GetEnvironmentVariable(name) with
    | null
    | "" -> fallback
    | value -> value

/// Loads the OpenRouter configuration from the OSE_BE_OPENROUTER_* env vars.
/// A missing API key yields an empty string (LLM calls are disabled until a key
/// is provided); the model and base URL fall back to documented defaults.
let loadConfig () : OpenRouterConfig =
    { ApiKey = envOr "OSE_BE_OPENROUTER_API_KEY" ""
      Model = envOr "OSE_BE_OPENROUTER_MODEL" DefaultModel
      BaseUrl = envOr "OSE_BE_OPENROUTER_BASE_URL" DefaultBaseUrl }

/// Whether the client is configured with an API key and can issue live calls.
let isConfigured (config: OpenRouterConfig) : bool =
    not (String.IsNullOrWhiteSpace config.ApiKey)
