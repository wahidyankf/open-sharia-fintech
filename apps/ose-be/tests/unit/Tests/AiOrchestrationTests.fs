module OseBe.Tests.Unit.Tests.AiOrchestrationTests

open Xunit
open OseBe.Contexts.AiOrchestration.Application
open OseBe.Contexts.AiOrchestration.Domain

// @covers specs/apps/ose/be/behaviors/ai-orchestration/ai-orchestration.feature:AI orchestration context is declared
[<Fact>]
let ``ai-orchestration reports ready to wrap LLM calls via OpenRouter`` () =
    let readiness = initializeContext ()
    Assert.Equal(ContextReadiness.Ready, readiness.State)
    Assert.Contains("OpenRouter", readiness.Capability)
