module OseBe.Tests.Unit.Tests.RegulatorySourceTests

open Xunit
open OseBe.Contexts.RegulatorySource.Application
open OseBe.Contexts.RegulatorySource.Domain

// @covers specs/apps/ose/be/behaviors/regulatory-source/regulatory-source.feature:Regulatory source context is declared
[<Fact>]
let ``regulatory-source reports ready to accept regulatory documents`` () =
    let readiness = initializeContext ()
    Assert.Equal(ContextReadiness.Ready, readiness.State)
    Assert.Contains("regulatory", readiness.Capability)
