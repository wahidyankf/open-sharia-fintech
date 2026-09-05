module OseBe.Infrastructure.Database

open System
open System.Diagnostics.CodeAnalysis

/// Reads DATABASE_URL or fails fast. ose-be is a server backend and
/// requires PostgreSQL — there is no SQLite dev fallback (see tech-docs
/// Deviations / Decisions). Migration execution lives in the db bounded context
/// (Contexts/Db/Infrastructure/DbMigrations.fs).
let requireDatabaseUrlWith (readEnvironment: string -> string) : string =
    match readEnvironment "DATABASE_URL" with
    | null
    | "" -> failwith "DATABASE_URL is required (PostgreSQL connection string)"
    | value -> value

[<ExcludeFromCodeCoverage(Justification = "Real process-environment adapter; covered by Integration tests")>]
let requireDatabaseUrl () : string =
    requireDatabaseUrlWith Environment.GetEnvironmentVariable
