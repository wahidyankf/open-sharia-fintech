module BeaverNestBe.Api.SecurityHeaders

open System
open System.Threading.Tasks
open Microsoft.AspNetCore.Http
open Giraffe

/// Immutable policy applied before every API, static, and fallback response.
let policy: Map<string, string> =
    Map.ofList
        [ "Content-Security-Policy",
          "default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; script-src 'self' 'wasm-unsafe-eval'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; font-src 'self'; connect-src 'self'"
          "X-Content-Type-Options", "nosniff"
          "Referrer-Policy", "strict-origin-when-cross-origin"
          "X-Frame-Options", "DENY"
          "Permissions-Policy", "camera=(), microphone=(), geolocation=()" ]

let apply (context: HttpContext) : unit =
    policy |> Map.iter (fun name value -> context.Response.Headers[name] <- value)

let handler: HttpHandler =
    fun next context ->
        apply context
        next context

let middleware =
    Func<HttpContext, RequestDelegate, Task>(fun context next ->
        apply context
        next.Invoke(context))
