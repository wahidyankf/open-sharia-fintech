namespace OseBe.Contexts.GapAnalysis

open System.Threading.Tasks
open OseBe.Infrastructure.OpenRouterClient
open OseBe.Infrastructure.OpenRouterConnect

/// Infrastructure adapters for the gap-analysis bounded context.
///
/// Gap analysis orchestrates LLM-assisted comparison via OpenRouter (core, not
/// media); it adapts the shared OpenRouter HTTP client into a comparison port.
module Infrastructure =

    /// Issues an LLM comparison prompt over the OpenRouter completion port.
    let compareWithLlm (prompt: string) : Task<Result<string, string>> = complete (loadConfig ()) prompt

    /// Whether the OpenRouter integration has an API key configured.
    let isLlmConfigured () : bool = isConfigured (loadConfig ())
