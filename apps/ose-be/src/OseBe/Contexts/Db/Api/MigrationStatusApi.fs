namespace OseBe.Contexts.Db

open Giraffe
open OseBe.Contexts.Db.Application

/// HTTP API for the database migration lifecycle.
module Api =

    /// Reports whether the current process completed its startup migrations.
    let statusHandler (status: SharedMigrationStatus) : HttpHandler =
        fun next ctx ->
            let state = status.Get() |> stateToString
            json {| migration_state = state |} next ctx

    /// Public system-status route bound to the current process migration state.
    let routes (status: SharedMigrationStatus) : HttpHandler =
        GET >=> route "/api/v1/system/status/database" >=> statusHandler status
