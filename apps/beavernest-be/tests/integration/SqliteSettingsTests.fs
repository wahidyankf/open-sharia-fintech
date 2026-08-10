module BeaverNestBe.Tests.Integration.SqliteSettingsTests

open System
open System.IO
open Microsoft.Data.Sqlite
open Xunit
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Sqlite.Connection

[<Fact>]
let ``configured connections enable SQLite safety settings`` () =
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-settings-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 250 |> Result.defaultWith failwith
    use connection = openConfigured configuration
    use command = connection.CreateCommand()
    command.CommandText <- "PRAGMA foreign_keys;"
    Assert.Equal(1L, unbox<int64> (command.ExecuteScalar()))
    command.CommandText <- "PRAGMA journal_mode;"
    Assert.Equal("wal", string (command.ExecuteScalar()))
    command.CommandText <- "PRAGMA busy_timeout;"
    Assert.Equal(250L, unbox<int64> (command.ExecuteScalar()))
