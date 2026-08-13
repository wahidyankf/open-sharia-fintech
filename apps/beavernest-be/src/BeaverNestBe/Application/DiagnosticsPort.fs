module BeaverNestBe.Application.DiagnosticsPort

open System
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.Domain.Diagnostics
open BeaverNestBe.Domain.Readiness

/// Seams keep the observable diagnostics contract deterministic in handler tests.
type DiagnosticsDependencies =
    { Readiness: ReadinessPort
      Clock: unit -> DateTimeOffset
      Version: unit -> string
      Uptime: unit -> TimeSpan }

type DiagnosticsPort = unit -> DiagnosticsResult

let create dependencies : DiagnosticsPort =
    fun () ->
        match dependencies.Readiness() with
        | Ready ->
            DiagnosticsReady(
                BeaverNestBe.Domain.Diagnostics.readyResponse
                    (dependencies.Version())
                    (dependencies.Uptime())
                    (dependencies.Clock())
            )
        | Unavailable -> DiagnosticsUnavailable
