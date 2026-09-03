module OseBe.Infrastructure.NatsClient

open System

/// Reads OSE_BE_NATS_URL or falls back to the default local NATS URL.
let natsUrl () : string =
    match Environment.GetEnvironmentVariable("OSE_BE_NATS_URL") with
    | null
    | "" -> "nats://localhost:4222"
    | value -> value
