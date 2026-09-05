module OseBe.Infrastructure.NatsClient

open System
open System.Diagnostics.CodeAnalysis

/// Reads OSE_BE_NATS_URL or fails fast. A missing NATS URL is a
/// configuration error and must not be silently defaulted — see
/// specs/apps/ose/be/behaviours/messaging/nats-config.feature. Once
/// configured, an unreachable broker is a separate, non-fatal concern
/// handled by `NatsConnect.connectAsync`.
let requireNatsUrlWith (readEnvironment: string -> string) : string =
    match readEnvironment "OSE_BE_NATS_URL" with
    | null
    | "" -> failwith "OSE_BE_NATS_URL is required (NATS connection URL)"
    | value -> value

[<ExcludeFromCodeCoverage(Justification = "Real process-environment adapter; covered by Integration tests")>]
let requireNatsUrl () : string =
    requireNatsUrlWith Environment.GetEnvironmentVariable
