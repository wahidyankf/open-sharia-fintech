module OrganicleverBe.Tests.Unit.Steps.DbMigrationSteps

open TickSpec
open Xunit
open OrganicleverBe.Contexts.Db.Infrastructure

let mutable private appliedMigrations = 0
let mutable private observedConnection = ""
let mutable private hostStarted = false

[<Given>]
let ``a fresh test database has pending organiclever-be migrations`` () =
    appliedMigrations <- 0
    observedConnection <- ""
    hostStarted <- false
    Assert.Equal(0, appliedMigrations)

[<When>]
let ``organiclever-be starts against that database`` () =
    runMigrationsWith
        (fun connection ->
            observedConnection <- connection
            appliedMigrations <- appliedMigrations + 1
            Ok())
        "in-memory://organiclever-be"

    hostStarted <- true

[<Then>]
let ``organiclever-be reaches its public health endpoint after applying migrations`` () =
    Assert.Equal("in-memory://organiclever-be", observedConnection)
    Assert.True(appliedMigrations >= 1)
    Assert.True(hostStarted)
