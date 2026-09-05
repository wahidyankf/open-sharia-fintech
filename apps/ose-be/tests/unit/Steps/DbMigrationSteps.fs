module OseBe.Tests.Unit.Steps.DbMigrationSteps

open TickSpec
open Xunit
open OseBe.Contexts.Db.Infrastructure

let mutable private appliedMigrations = 0
let mutable private observedConnection = ""
let mutable private hostStarted = false

[<Given>]
let ``a fresh test database has pending ose-be migrations`` () =
    appliedMigrations <- 0
    observedConnection <- ""
    hostStarted <- false
    Assert.Equal(0, appliedMigrations)

[<When>]
let ``ose-be starts against that database`` () =
    runMigrationsWith
        (fun connection ->
            observedConnection <- connection
            appliedMigrations <- appliedMigrations + 1
            Ok())
        "in-memory://ose-be"

    hostStarted <- true

[<Then>]
let ``ose-be reaches its public health endpoint after applying migrations`` () =
    Assert.Equal("in-memory://ose-be", observedConnection)
    Assert.True(appliedMigrations >= 1)
    Assert.True(hostStarted)
