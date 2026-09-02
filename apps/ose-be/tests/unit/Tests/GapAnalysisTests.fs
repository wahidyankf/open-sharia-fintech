module OseBe.Tests.Unit.Tests.GapAnalysisTests

open Xunit
open OseBe.Contexts.GapAnalysis.Application
open OseBe.Contexts.GapAnalysis.Domain

// @covers specs/apps/ose/be/behaviors/gap-analysis/gap-analysis.feature:Gap analysis context is declared
[<Fact>]
let ``gap-analysis reports ready to compare regulatory and policy documents`` () =
    let readiness = initializeContext ()
    Assert.Equal(ContextReadiness.Ready, readiness.State)
    Assert.Contains("compare", readiness.Capability)
