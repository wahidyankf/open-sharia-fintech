module OseBe.Infrastructure.NatsConnect

open System.Diagnostics.CodeAnalysis
open System.Threading.Tasks
open NATS.Client.Core

/// Opens a best-effort NATS.Net connection on boot. Messaging is exercised at the
/// e2e level (JetStream demo, later phases); a failed connect here logs and is
/// non-fatal so the HTTP host still serves /health.
///
/// The success path requires a live NATS broker; e2e-tested per the
/// @e2e-tagged specs/apps/ose/be/behaviours/messaging/live/nats-connect.feature,
/// owned by ose-be-e2e. The graceful-failure path is unit-tested directly in
/// Tests/NatsClientTests.fs. Kept in its own file (rather than alongside the
/// pure, fully unit-tested `requireNatsUrl` in NatsClient.fs) so the
/// project-level coverage `/p:ExcludeByFile` can exclude exactly this
/// live-broker-only surface.
let connectWith
    (create: string -> 'connection)
    (connect: 'connection -> Task)
    (dispose: 'connection -> Task)
    (url: string)
    : Task<'connection option> =
    task {
        let conn = create url

        try
            do! connect conn
            printfn "NATS connected: %s" url
            return Some conn
        with ex ->
            eprintfn "NATS connect failed (%s): %s" url ex.Message
            do! dispose conn
            return None
    }

[<ExcludeFromCodeCoverage(Justification = "Requires a live NATS broker to connect — see module doc comment above")>]
let connectAsync (url: string) : Task<NatsConnection option> =
    connectWith
        (fun connectionUrl -> new NatsConnection(NatsOpts(Url = connectionUrl)))
        (fun connection -> connection.ConnectAsync().AsTask())
        (fun connection -> connection.DisposeAsync().AsTask())
        url
