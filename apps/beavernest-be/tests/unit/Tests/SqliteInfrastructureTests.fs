module BeaverNestBe.Tests.Unit.Tests.SqliteInfrastructureTests

open System
open System.IO
open Microsoft.Data.Sqlite
open Xunit
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Domain.Readiness
open BeaverNestBe.Infrastructure.Migrations
open BeaverNestBe.Infrastructure.Sqlite.Connection
open BeaverNestBe.Infrastructure.Sqlite.Errors

[<Fact>]
let ``migration journal is current when completed scripts match in any order`` () =
    let expected = [ "001-initialize.sql"; "002-add-workspace.sql" ]
    let recorded = [ "002-add-workspace.sql"; "001-initialize.sql" ]

    Assert.Equal("current", BeaverNestBe.Infrastructure.Migrations.journalState expected recorded)

[<Fact>]
let ``migration journal is pending when a completed script is missing`` () =
    let expected = [ "001-initialize.sql"; "002-add-workspace.sql" ]
    let recorded = [ "001-initialize.sql" ]

    Assert.Equal("pending", BeaverNestBe.Infrastructure.Migrations.journalState expected recorded)

[<Fact>]
let ``readiness schema is current only when expected and recorded scripts agree`` () =
    Assert.Equal("current", BeaverNestBe.Domain.Readiness.schemaState [ "001-initialize.sql" ] [ "001-initialize.sql" ])

    Assert.Equal(
        "pending",
        BeaverNestBe.Domain.Readiness.schemaState [ "001-initialize.sql" ] [ "002-add-workspace.sql" ]
    )

[<Theory>]
[<InlineData(5)>]
[<InlineData(6)>]
let ``SQLite busy and locked provider codes classify as controlled busy errors`` (errorCode: int) =
    let exceptionValue = SqliteException("database unavailable", errorCode)

    Assert.Equal(Busy, classify exceptionValue)
    Assert.Equal("database is busy", safeMessage Busy)

[<Fact>]
let ``non-lock SQLite errors and non-SQLite errors remain safely classified`` () =
    let sqliteException = SqliteException("database unavailable", 19)

    Assert.Equal(InvalidDatabase, classify sqliteException)
    Assert.Equal(FailedMigration, classify (InvalidOperationException("migration failed")))
    Assert.Equal("database operation failed", safeMessage InvalidDatabase)
    Assert.Equal("database migration failed", safeMessage FailedMigration)

[<Fact>]
let ``SQLite connection string uses the validated fixed database path and write-create mode`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-sqlite-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 1000 |> Result.defaultWith failwith
    let builder = SqliteConnectionStringBuilder(connectionString configuration)

    Assert.Equal(databasePath configuration, builder.DataSource)
    Assert.Equal(SqliteOpenMode.ReadWriteCreate, builder.Mode)

[<Fact>]
let ``readiness connections require an existing database and never create one`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-readonly-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 1000 |> Result.defaultWith failwith
    let builder = SqliteConnectionStringBuilder(readOnlyConnectionString configuration)

    Assert.Equal(databasePath configuration, builder.DataSource)
    Assert.Equal(SqliteOpenMode.ReadOnly, builder.Mode)
    Assert.False(builder.Pooling)
