module OseBe.IntegrationTests.DatabaseBootTests

open System
open Microsoft.EntityFrameworkCore
open Npgsql
open Xunit
open OseBe.Infrastructure.AppDbContext
open OseBe.Contexts.Db.Infrastructure

let private connectionString () =
    match Environment.GetEnvironmentVariable("DATABASE_URL") with
    | null
    | "" -> failwith "DATABASE_URL must be set for integration tests"
    | value -> value

let private schemaVersionsExists (connStr: string) : bool =
    use conn = new NpgsqlConnection(connStr)
    conn.Open()

    use cmd =
        new NpgsqlCommand(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'schemaversions')",
            conn
        )

    cmd.ExecuteScalar() :?> bool

[<Fact>]
let ``DbUp creates the SchemaVersions tracking table on boot`` () =
    let connStr = connectionString ()
    runMigrations connStr
    Assert.True(schemaVersionsExists connStr, "DbUp SchemaVersions table should exist after boot")

let private appliedMigrationCount (connStr: string) : int =
    use conn = new NpgsqlConnection(connStr)
    conn.Open()

    use cmd = new NpgsqlCommand("SELECT COUNT(*) FROM schemaversions", conn)
    cmd.ExecuteScalar() :?> int64 |> int

// @covers specs/apps/ose/be/behaviors/db/migrations.feature:Backend applies pending migrations on startup
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

let private dbContext (connStr: string) =
    let options =
        DbContextOptionsBuilder<AppDbContext>().UseNpgsql(connStr).UseSnakeCaseNamingConvention().Options

    new AppDbContext(options)

[<Fact>]
let ``regulatory-source repository persists and lists documents`` () =
    let connStr = connectionString ()
    runMigrations connStr
    use ctx = dbContext connStr
    let repo = OseBe.Contexts.RegulatorySource.Infrastructure.repository ctx

    let entity: RegulatoryDocumentEntity =
        { Id = Guid.NewGuid()
          Title = "Circular 2026/01"
          Issuer = "Regulator"
          Jurisdiction = "ID"
          DocumentType = "circular"
          CreatedAt = DateTime.UtcNow }

    let created = repo.Create(entity).Result
    Assert.Equal(entity.Id, created.Id)
    let found = repo.FindById(entity.Id).Result
    Assert.True(found.IsSome, "regulatory document should be retrievable by id")

[<Fact>]
let ``internal-policy repository persists and lists documents`` () =
    let connStr = connectionString ()
    runMigrations connStr
    use ctx = dbContext connStr
    let repo = OseBe.Contexts.InternalPolicy.Infrastructure.repository ctx

    let entity: InternalPolicyDocumentEntity =
        { Id = Guid.NewGuid()
          Title = "SOP-100"
          Version = "1.0"
          Scope = "company-wide"
          CreatedAt = DateTime.UtcNow }

    let created = repo.Create(entity).Result
    Assert.Equal(entity.Id, created.Id)
    let found = repo.FindById(entity.Id).Result
    Assert.True(found.IsSome, "internal policy document should be retrievable by id")
