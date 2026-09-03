module OrganicleverBe.Infrastructure.NatsClient

open System

/// Reads ORGANICLEVER_BE_NATS_URL or falls back to the default local NATS URL.
let natsUrl () : string =
    match Environment.GetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL") with
    | null
    | "" -> "nats://localhost:4222"
    | value -> value
