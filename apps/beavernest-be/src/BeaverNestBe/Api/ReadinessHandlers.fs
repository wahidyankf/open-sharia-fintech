module BeaverNestBe.Api.ReadinessHandlers

open Giraffe
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.Domain.Readiness

let private noStore: HttpHandler = setHttpHeader "Cache-Control" "no-store"

/// Emits only the documented safe readiness contracts. Giraffe does not add
/// ETag or Last-Modified validators, and this handler never sets either.
let readinessHandler (readiness: ReadinessPort) : HttpHandler =
    fun next context ->
        match readiness () with
        | Ready -> (noStore >=> json readyResponse) next context
        | Unavailable -> (noStore >=> setStatusCode 503 >=> json unavailableResponse) next context
