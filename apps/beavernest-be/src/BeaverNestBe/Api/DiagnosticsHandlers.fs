module BeaverNestBe.Api.DiagnosticsHandlers

open Giraffe
open BeaverNestBe.Application.DiagnosticsPort
open BeaverNestBe.Domain.Diagnostics

let private noStore: HttpHandler = setHttpHeader "Cache-Control" "no-store"

/// Emits a bounded operational snapshot only when the underlying readiness
/// observation succeeds; unavailable responses deliberately omit every cause.
let diagnosticsHandler (diagnostics: DiagnosticsPort) : HttpHandler =
    fun next context ->
        match diagnostics () with
        | DiagnosticsReady response -> (noStore >=> json response) next context
        | DiagnosticsUnavailable -> (noStore >=> setStatusCode 503 >=> json unavailableResponse) next context
