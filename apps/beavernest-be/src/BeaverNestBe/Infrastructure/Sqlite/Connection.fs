module BeaverNestBe.Infrastructure.Sqlite.Connection

open System.IO
open Microsoft.Data.Sqlite
open BeaverNestBe.Domain.DatabaseConfiguration

let connectionString configuration =
    let builder = SqliteConnectionStringBuilder()
    builder.DataSource <- databasePath configuration
    builder.Mode <- SqliteOpenMode.ReadWriteCreate
    builder.ToString()

let readOnlyConnectionString configuration =
    let builder = SqliteConnectionStringBuilder()
    builder.DataSource <- databasePath configuration
    builder.Mode <- SqliteOpenMode.ReadOnly
    builder.ToString()

/// Opens a short-lived connection and applies all required SQLite safeguards.
let openConfigured configuration =
    Directory.CreateDirectory(dataDirectory configuration) |> ignore
    let connection = new SqliteConnection(connectionString configuration)
    connection.Open()
    use command = connection.CreateCommand()

    command.CommandText <-
        $"PRAGMA foreign_keys = ON; PRAGMA journal_mode = WAL; PRAGMA busy_timeout = %d{busyTimeoutMilliseconds configuration};"

    command.ExecuteNonQuery() |> ignore
    connection

/// Opens an existing database without creating files or changing SQLite state.
let openReadOnly configuration =
    let connection = new SqliteConnection(readOnlyConnectionString configuration)
    connection.Open()
    connection
