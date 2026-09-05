module OrganicleverBe.WebApp

open Microsoft.Extensions.DependencyInjection
open Giraffe
open OrganicleverBe.Handlers.HealthHandler
open OrganicleverBe.Infrastructure.AppDbContext
open OrganicleverBe.Contexts.Db.Application
open OrganicleverBe.Contexts.Journal.Infrastructure

/// Resolves a request-scoped AppDbContext, builds the EF journal repository over
/// it, and dispatches to the journal CRUD routes. Building the repository inside
/// the handler keeps the DbContext scoped to the request.
let private journalRoutes: HttpHandler =
    fun next ctx ->
        let db = ctx.RequestServices.GetRequiredService<AppDbContext>()
        let repo = efRepository db
        OrganicleverBe.Contexts.Journal.Api.routes repo next ctx

/// Composes the HTTP routes for every bounded context into a single handler,
/// bound to the database and messaging lifecycle status surfaces. The legacy
/// /health route is retained alongside the health context's /api/v1/health for
/// the web tier's existing liveness probe.
let buildWebAppWithMigrationStatus
    (migrationStatus: SharedMigrationStatus)
    (messagingStatus: OrganicleverBe.Contexts.Messaging.Application.SharedMessagingStatus)
    : HttpHandler =
    choose
        [ GET >=> route "/health" >=> healthHandler
          OrganicleverBe.Contexts.Health.Api.routes
          OrganicleverBe.Contexts.Db.Api.routes migrationStatus
          journalRoutes
          OrganicleverBe.Contexts.Messaging.Api.routes messagingStatus
          RequestErrors.NOT_FOUND "Not Found" ]

/// Composes the application with an already-applied migration state for
/// in-process route tests that do not cross the real PostgreSQL boundary.
let buildWebApp (messagingStatus: OrganicleverBe.Contexts.Messaging.Application.SharedMessagingStatus) : HttpHandler =
    buildWebAppWithMigrationStatus (appliedMigrationStatus ()) messagingStatus

/// Default composed handler with a fresh (pending) messaging status, used by
/// in-process unit tests of the routing surface.
let webApp: HttpHandler =
    buildWebApp (OrganicleverBe.Contexts.Messaging.Application.newShared ())
