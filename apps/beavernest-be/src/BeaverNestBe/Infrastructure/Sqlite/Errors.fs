module BeaverNestBe.Infrastructure.Sqlite.Errors

open Microsoft.Data.Sqlite

type DatabaseError =
    | Busy
    | FailedMigration
    | InvalidDatabase

let classify (exceptionValue: exn) =
    match exceptionValue with
    | :? SqliteException as sqliteException when
        sqliteException.SqliteErrorCode = 5 || sqliteException.SqliteErrorCode = 6
        ->
        Busy
    | :? SqliteException -> InvalidDatabase
    | _ -> FailedMigration

let safeMessage error =
    match error with
    | Busy -> "database is busy"
    | FailedMigration -> "database migration failed"
    | InvalidDatabase -> "database operation failed"
