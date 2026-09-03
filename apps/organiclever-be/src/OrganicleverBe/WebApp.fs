module OrganicleverBe.WebApp

open Microsoft.Extensions.DependencyInjection
open Giraffe
open OrganicleverBe.Handlers.HealthHandler
open OrganicleverBe.Infrastructure.AppDbContext
open OrganicleverBe.Contexts.Journal.Infrastructure
open OrganicleverBe.Contexts.Messaging.Application

/// Resolves a request-scoped AppDbContext, builds the EF journal repository over
/// it, and dispatches to the journal CRUD routes. Building the repository inside
/// the handler keeps the DbContext scoped to the request.
let private journalRoutes: HttpHandler =
    fun next ctx ->
        let db = ctx.RequestServices.GetRequiredService<AppDbContext>()
        let repo = efRepository db
        OrganicleverBe.Contexts.Journal.Api.routes repo next ctx

/// Composes the HTTP routes for every bounded context into a single handler,
/// bound to the shared messaging status surface. The legacy /health route is
/// retained alongside the health context's /api/v1/health for the web tier's
/// existing liveness probe.
let buildWebApp (status: SharedMessagingStatus) : HttpHandler =
    choose
        [ GET >=> route "/health" >=> healthHandler
          OrganicleverBe.Contexts.Health.Api.routes
          journalRoutes
          OrganicleverBe.Contexts.Messaging.Api.routes status
          RequestErrors.NOT_FOUND "Not Found" ]

/// Default composed handler with a fresh (pending) messaging status, used by
/// in-process unit tests of the routing surface.
let webApp: HttpHandler = buildWebApp (newShared ())
