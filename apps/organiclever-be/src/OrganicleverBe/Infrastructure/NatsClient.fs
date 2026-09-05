module OrganicleverBe.Infrastructure.NatsClient

open System
open System.Diagnostics.CodeAnalysis

/// Reads ORGANICLEVER_BE_NATS_URL or fails fast. Messaging configuration is required
/// (see .env.example) — there is no default broker URL, so a misconfigured deployment
/// aborts at startup with a clear error rather than silently connecting to the wrong
/// (or no) broker. Mirrors the `requireDatabaseUrl` fail-fast pattern in Database.fs.
let requireNatsUrlWith (readEnvironment: string -> string) : string =
    match readEnvironment "ORGANICLEVER_BE_NATS_URL" with
    | null
    | "" -> failwith "ORGANICLEVER_BE_NATS_URL is required (NATS connection URL)"
    | value -> value

[<ExcludeFromCodeCoverage(Justification = "Real process-environment adapter; covered by Integration tests")>]
let requireNatsUrl () : string =
    requireNatsUrlWith Environment.GetEnvironmentVariable
