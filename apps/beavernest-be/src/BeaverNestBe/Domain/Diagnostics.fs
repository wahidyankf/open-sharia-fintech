module BeaverNestBe.Domain.Diagnostics

open System
open BeaverNestBe.Domain.Readiness

/// Safe ready-only data that HTTP can serialize without exposing host, process,
/// database, or exception detail.
type DiagnosticsReadyResponse =
    { Status: string
      Version: string
      UptimeSeconds: int64
      ServerTimeUtc: DateTimeOffset
      Components: ReadinessComponents }

/// Safe unavailable data deliberately omits version, clock, uptime, and cause.
type DiagnosticsUnavailableResponse =
    { Status: string
      Components: ReadinessComponents }

type DiagnosticsResult =
    | DiagnosticsReady of DiagnosticsReadyResponse
    | DiagnosticsUnavailable

let private readyComponents: ReadinessComponents =
    { Database = "ready"
      Schema = "current" }

let unavailableResponse: DiagnosticsUnavailableResponse =
    { Status = "unavailable"
      Components =
        { Database = "unavailable"
          Schema = "unknown" } }

let readyResponse (version: string) (uptime: TimeSpan) (serverTimeUtc: DateTimeOffset) : DiagnosticsReadyResponse =
    { Status = "ready"
      Version = version
      UptimeSeconds = max 0L (int64 (Math.Floor(uptime.TotalSeconds)))
      ServerTimeUtc = serverTimeUtc.ToUniversalTime()
      Components = readyComponents }
