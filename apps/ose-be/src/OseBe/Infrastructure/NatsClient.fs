module OseBe.Infrastructure.NatsClient

open System

/// Reads OSE_BE_NATS_URL or fails fast. A missing NATS URL is a
/// configuration error and must not be silently defaulted — see
/// specs/apps/ose/be/behaviors/messaging/nats-config.feature. Once
/// configured, an unreachable broker is a separate, non-fatal concern
/// handled by `NatsConnect.connectAsync`.
let requireNatsUrl () : string =
    match Environment.GetEnvironmentVariable("OSE_BE_NATS_URL") with
    | null
    | "" -> failwith "OSE_BE_NATS_URL is required (NATS connection URL)"
    | value -> value
