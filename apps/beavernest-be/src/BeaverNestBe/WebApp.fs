module BeaverNestBe.WebApp

open Giraffe
open BeaverNestBe.Domain.ErrorBody
open BeaverNestBe.Api.HealthHandlers
open BeaverNestBe.Api.ReadinessHandlers
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.Api.SecurityHeaders
open BeaverNestBe.Api.StaticContent

/// Single error-formatting function every non-2xx response goes through.
let private errorBody (message: string) : ErrorBody = { Error = message }

let private notFoundHandler: HttpHandler =
    setStatusCode 404 >=> json (errorBody "not found")

/// API routes precede JSON API errors, static assets, and the final SPA
/// fallback so no API or file-like path can become a client-side route.
let webAppWith (readiness: ReadinessPort) : HttpHandler =
    handler
    >=> choose
            [ GET >=> route "/api/v1/health" >=> healthHandler
              GET >=> route "/api/v1/readiness" >=> readinessHandler readiness
              routeStartsWith "/api/" >=> notFoundHandler
              routeStartsWith "/assets/" >=> notFoundHandler
              spaFallbackHandler
              notFoundHandler ]

/// Default composition keeps the existing in-process handler tests focused on
/// routing; the executable injects its real database-backed readiness port.
let webApp: HttpHandler = webAppWith alwaysReady
