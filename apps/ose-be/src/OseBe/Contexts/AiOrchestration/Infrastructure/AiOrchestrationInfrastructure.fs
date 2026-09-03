namespace OseBe.Contexts.AiOrchestration

open System.Threading.Tasks
open OseBe.Infrastructure.OpenRouterClient
open OseBe.Infrastructure.OpenRouterConnect

/// Infrastructure adapters for the ai-orchestration bounded context.
///
/// This context owns the OpenRouter LLM integration (core, not media): it adapts
/// the shared OpenRouter HTTP client into a context-local completion port.
module Infrastructure =

    /// The OpenRouter completion port for this context, bound to the
    /// environment-driven configuration.
    let completion (prompt: string) : Task<Result<string, string>> = complete (loadConfig ()) prompt

    /// Whether the OpenRouter integration has an API key configured.
    let isLlmConfigured () : bool = isConfigured (loadConfig ())
