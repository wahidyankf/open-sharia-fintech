module OrganicleverBe.IntegrationTests.DatabaseBootTests

open System
open Microsoft.EntityFrameworkCore
open Npgsql
open Xunit
open OrganicleverBe.Infrastructure.AppDbContext
open OrganicleverBe.Contexts.Db.Infrastructure

let private connectionString () =
    match Environment.GetEnvironmentVariable("DATABASE_URL") with
    | null
    | "" -> failwith "DATABASE_URL must be set for integration tests"
    | value -> value

let private tableExists (connStr: string) (tableName: string) : bool =
    use conn = new NpgsqlConnection(connStr)
    conn.Open()

    use cmd =
        new NpgsqlCommand("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = @t)", conn)

    cmd.Parameters.AddWithValue("t", tableName) |> ignore
    cmd.ExecuteScalar() :?> bool

[<Fact>]
let ``DbUp creates the SchemaVersions tracking table on boot`` () =
    let connStr = connectionString ()
    runMigrations connStr
    Assert.True(tableExists connStr "schemaversions", "DbUp SchemaVersions table should exist after boot")

[<Fact>]
let ``DbUp applies the journal schema on boot`` () =
    let connStr = connectionString ()
    runMigrations connStr
    Assert.True(tableExists connStr "journal_entries", "journal_entries table should exist after migration")

let private appliedMigrationCount (connStr: string) : int =
    use conn = new NpgsqlConnection(connStr)
    conn.Open()

    use cmd = new NpgsqlCommand("SELECT COUNT(*) FROM schemaversions", conn)
    cmd.ExecuteScalar() :?> int64 |> int

// @covers specs/apps/organiclever/be/behaviors/db/migrations.feature:Backend applies pending migrations on startup
[<Fact>]
let ``backend applies pending migrations on startup`` () =
    let connStr = connectionString ()
    runMigrations connStr
    Assert.True(appliedMigrationCount connStr >= 1, "at least one migration should be recorded after boot")

[<Fact>]
let ``EF context boots against PostgreSQL after migration`` () =
    let connStr = connectionString ()
    runMigrations connStr

    let options =
        DbContextOptionsBuilder<AppDbContext>().UseNpgsql(connStr).UseSnakeCaseNamingConvention().Options

    use ctx = new AppDbContext(options)
    Assert.True(ctx.Database.CanConnect(), "EF context should connect to PostgreSQL")
