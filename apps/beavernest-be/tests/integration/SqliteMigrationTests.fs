module BeaverNestBe.Tests.Integration.SqliteMigrationTests

open System
open System.IO
open Microsoft.Data.Sqlite
open Xunit
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Migrations
open BeaverNestBe.Program

let private temporaryDirectory () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-integration-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(directory) |> ignore
    directory

[<Fact>]
let ``fresh database receives a migration journal without product tables`` () =
    let directory = temporaryDirectory ()
    let configuration = create directory 1000 |> Result.defaultWith failwith
    Assert.Equal(Ok(), initialize configuration)
    use connection = new SqliteConnection($"Data Source={databasePath configuration}")
    connection.Open()
    use command = connection.CreateCommand()
    command.CommandText <- "SELECT COUNT(*) FROM SchemaVersions;"
    Assert.Equal(1, Convert.ToInt32(command.ExecuteScalar()))

[<Fact>]
let ``restarting does not duplicate the migration journal`` () =
    let directory = temporaryDirectory ()
    let configuration = create directory 1000 |> Result.defaultWith failwith
    Assert.Equal(Ok(), initialize configuration)
    Assert.Equal(Ok(), initialize configuration)
    Assert.Equal("current", journalState [ initializationScriptName ] [ initializationScriptName ])

[<Fact>]
let ``migration SQL is loaded deterministically from the embedded migration resource`` () =
    let scripts = embeddedScripts ()

    Assert.Equal<string>([ initializationScriptName ], scripts |> List.map fst)
    Assert.Contains("migration journal", scripts |> List.head |> snd)

[<Fact>]
let ``readiness requires an unchanged migration journal without creating database state`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-readiness-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 1000 |> Result.defaultWith failwith
    Assert.False(isReady configuration)
    Assert.False(Directory.Exists directory)

    Assert.Equal(Ok(), initialize configuration)
    Assert.True(isReady configuration)

    use connection = new SqliteConnection($"Data Source={databasePath configuration}")
    connection.Open()
    use command = connection.CreateCommand()
    command.CommandText <- "DELETE FROM SchemaVersions;"
    command.ExecuteNonQuery() |> ignore
    Assert.False(isReady configuration)

[<Fact>]
let ``readiness observes a database file atomically replaced after an earlier readiness probe warmed a pooled connection``
    ()
    =
    let directory = temporaryDirectory ()
    let configuration = create directory 1000 |> Result.defaultWith failwith
    Assert.Equal(Ok(), initialize configuration)
    // Warms any pooled read-only connection Microsoft.Data.Sqlite may cache
    // for this exact connection string, mirroring a live service that has
    // already answered at least one readiness probe.
    Assert.True(isReady configuration)

    // A restore replaces the live file at the OS level (same pattern as
    // BeaverNestBe.Operations.Database.restoreAt): the old inode is moved
    // aside and an unrelated, non-migrated file takes the live path's name.
    let replacementPath = Path.Combine(temporaryDirectory (), "replacement.sqlite3")

    File.WriteAllText(replacementPath, "not a migrated database")
    let livePath = databasePath configuration
    File.Delete(livePath + "-wal")
    File.Delete(livePath + "-shm")
    File.Move(replacementPath, livePath, true)

    Assert.False(isReady configuration)

[<Fact>]
let ``invalid SQL fails before a service can listen`` () =
    let directory = temporaryDirectory ()
    let configuration = create directory 1000 |> Result.defaultWith failwith
    Assert.True(apply configuration [ "broken.sql", "not valid sql" ] |> Result.isError)

[<Fact>]
let ``application preparation migrates before it returns a listener`` () =
    let directory = temporaryDirectory ()

    let environment key =
        Map.ofList
            [ "BEAVERNEST_BE_DATA_DIRECTORY", directory
              "BEAVERNEST_BE_HTTP_LISTEN_PORT", "19320" ]
        |> Map.tryFind key
        |> Option.toObj

    let listener = prepareApplication environment |> Result.defaultWith failwith
    let configuration = create directory 5000 |> Result.defaultWith failwith
    use connection = new SqliteConnection($"Data Source={databasePath configuration}")
    connection.Open()
    use command = connection.CreateCommand()
    command.CommandText <- "SELECT COUNT(*) FROM SchemaVersions;"
    Assert.Equal("http://127.0.0.1:19320", BeaverNestBe.Domain.HttpConfiguration.url listener)
    Assert.Equal(1, Convert.ToInt32(command.ExecuteScalar()))
