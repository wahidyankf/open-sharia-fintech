module OseBe.WebApp

open Giraffe
open OseBe.Contexts.Db.Application

/// Composes the HTTP routes for every bounded context into a single handler,
/// bound to the database and messaging lifecycle status surfaces.
let buildWebAppWithMigrationStatus
    (migrationStatus: SharedMigrationStatus)
    (messagingStatus: OseBe.Contexts.Messaging.Application.SharedMessagingStatus)
    : HttpHandler =
    choose
        [ OseBe.Contexts.Health.Api.routes
          OseBe.Contexts.Db.Api.routes migrationStatus
          OseBe.Contexts.RegulatorySource.Api.routes
          OseBe.Contexts.InternalPolicy.Api.routes
          OseBe.Contexts.GapAnalysis.Api.routes
          OseBe.Contexts.AiOrchestration.Api.routes
          OseBe.Contexts.Messaging.Api.routes messagingStatus
          RequestErrors.NOT_FOUND "Not Found" ]

/// Composes the application with an already-applied migration state for
/// in-process route tests that do not cross the real PostgreSQL boundary.
let buildWebApp (messagingStatus: OseBe.Contexts.Messaging.Application.SharedMessagingStatus) : HttpHandler =
    buildWebAppWithMigrationStatus (appliedMigrationStatus ()) messagingStatus

/// Default composed handler with a fresh (pending) messaging status, used by
/// in-process unit tests of the routing surface.
let webApp: HttpHandler =
    buildWebApp (OseBe.Contexts.Messaging.Application.newShared ())
