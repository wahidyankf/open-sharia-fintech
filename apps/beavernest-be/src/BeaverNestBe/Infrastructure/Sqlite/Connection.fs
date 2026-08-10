module BeaverNestBe.Infrastructure.Sqlite.Connection

open System.IO
open Microsoft.Data.Sqlite
open BeaverNestBe.Domain.DatabaseConfiguration

/// Microsoft.Data.Sqlite re-applies `sqlite3_busy_timeout` from the
/// connection's `Default Timeout` (seconds; provider default 30) before
/// every command — a PRAGMA busy_timeout statement issued once only survives
/// until the next command uses a fresh SqliteCommand instance. Configuring
/// it on the connection string itself is the only way it survives every
/// command issued on the connection, not just the one that ran the PRAGMA.
let private applyBusyTimeout configuration (builder: SqliteConnectionStringBuilder) =
    let seconds =
        max 1 (int (ceil (float (busyTimeoutMilliseconds configuration) / 1000.0)))

    builder.DefaultTimeout <- seconds
    builder

let connectionString configuration =
    let builder = SqliteConnectionStringBuilder()
    builder.DataSource <- databasePath configuration
    builder.Mode <- SqliteOpenMode.ReadWriteCreate
    (applyBusyTimeout configuration builder).ToString()

let readOnlyConnectionString configuration =
    let builder = SqliteConnectionStringBuilder()
    builder.DataSource <- databasePath configuration
    builder.Mode <- SqliteOpenMode.ReadOnly
    // Readiness probes must observe a database file atomically replaced by a
    // restore (BeaverNestBe.Operations.Database.restoreAt) rather than
    // reusing a pooled native handle still bound to the old, moved-aside
    // inode.
    builder.Pooling <- false
    (applyBusyTimeout configuration builder).ToString()

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
