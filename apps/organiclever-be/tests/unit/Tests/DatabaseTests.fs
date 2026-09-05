module OrganicleverBe.Tests.Unit.Tests.DatabaseTests

open System
open Xunit
open OrganicleverBe.Infrastructure.Database
open OrganicleverBe.Contexts.Db.Application
open OrganicleverBe.Contexts.Db.Infrastructure
open OrganicleverBe.Tests.Unit.Steps.BddState

[<Fact>]
let ``requireDatabaseUrlWith returns the configured connection string`` () =
    let value = "Host=fake;Database=organiclever_be"
    Assert.Equal(value, requireDatabaseUrlWith (fun _ -> value))

[<Fact>]
let ``requireDatabaseUrlWith fails fast when DATABASE_URL is absent`` () =
    let ex =
        Assert.Throws<Exception>(fun () -> requireDatabaseUrlWith (fun _ -> null) |> ignore)

    Assert.Contains("DATABASE_URL", ex.Message)

[<Fact>]
let ``runMigrationsWith invokes the upgrade adapter exactly once`` () =
    let mutable calls = 0
    let mutable observed = ""

    runMigrationsWith
        (fun connection ->
            calls <- calls + 1
            observed <- connection
            Ok())
        "in-memory://organiclever-be"

    Assert.Equal(1, calls)
    Assert.Equal("in-memory://organiclever-be", observed)

[<Fact>]
let ``runMigrationsWith fails with the upgrade adapter error`` () =
    let ex =
        Assert.Throws<Exception>(fun () -> runMigrationsWith (fun _ -> Error "broken script") "in-memory")

    Assert.Contains("broken script", ex.Message)

[<Fact>]
let ``migration status transitions from pending to applied`` () =
    let status = newMigrationStatus ()
    Assert.Equal(Pending, status.Get())
    Assert.Equal("pending", stateToString (status.Get()))

    status.MarkApplied()

    Assert.Equal(Applied, status.Get())
    Assert.Equal("applied", stateToString (status.Get()))

[<Fact>]
let ``database status route reports an applied startup migration`` () =
    let client =
        buildClient (OrganicleverBe.Contexts.Db.Api.routes (appliedMigrationStatus ()))

    let response = client.GetAsync("/api/v1/system/status/database").Result
    let body = response.Content.ReadAsStringAsync().Result

    Assert.True(response.IsSuccessStatusCode)
    Assert.Contains("\"migration_state\":\"applied\"", body)
