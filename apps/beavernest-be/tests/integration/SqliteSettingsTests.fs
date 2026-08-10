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

[<Fact>]
let ``configured busy timeout survives a second command, not just the one that set the PRAGMA`` () =
    // Microsoft.Data.Sqlite re-applies sqlite3_busy_timeout from the
    // connection's DefaultTimeout (default 30s) before every command,
    // silently overriding a PRAGMA busy_timeout set by an earlier command on
    // the same connection. Contention must resolve near the configured
    // timeout, not the ADO.NET provider's 30-second default.
    let directory =
        Path.Combine(Path.GetTempPath(), "beavernest-busy-timeout-" + Guid.NewGuid().ToString("N"))

    let configuration = create directory 250 |> Result.defaultWith failwith
    use first = openConfigured configuration
    use setup = first.CreateCommand()
    setup.CommandText <- "CREATE TABLE IF NOT EXISTS BusyTimeoutFixture (Id INTEGER PRIMARY KEY);"
    setup.ExecuteNonQuery() |> ignore
    use lockCommand = first.CreateCommand()
    lockCommand.CommandText <- "BEGIN IMMEDIATE; INSERT INTO BusyTimeoutFixture DEFAULT VALUES;"
    lockCommand.ExecuteNonQuery() |> ignore

    use second = openConfigured configuration
    // A fresh SqliteCommand instance is exactly what reproduces the bug: the
    // provider re-applies its own busy_timeout default just before this
    // ExecuteNonQuery call.
    use secondCommand = second.CreateCommand()
    secondCommand.CommandText <- "INSERT INTO BusyTimeoutFixture DEFAULT VALUES;"
    let started = DateTime.UtcNow

    Assert.Throws<SqliteException>(fun () -> secondCommand.ExecuteNonQuery() |> ignore)
    |> ignore

    let elapsed = (DateTime.UtcNow - started).TotalMilliseconds

    Assert.True(
        elapsed < 2_000.0,
        $"expected contention to resolve near the 250ms configured timeout, took {elapsed}ms"
    )
