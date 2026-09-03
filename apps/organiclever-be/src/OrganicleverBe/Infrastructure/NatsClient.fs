module OrganicleverBe.Infrastructure.NatsClient

open System

/// Reads ORGANICLEVER_BE_NATS_URL or fails fast. Messaging configuration is required
/// (see .env.example) — there is no default broker URL, so a misconfigured deployment
/// aborts at startup with a clear error rather than silently connecting to the wrong
/// (or no) broker. Mirrors the `requireDatabaseUrl` fail-fast pattern in Database.fs.
let requireNatsUrl () : string =
    match Environment.GetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL") with
    | null
    | "" -> failwith "ORGANICLEVER_BE_NATS_URL is required (NATS connection URL)"
    | value -> value
