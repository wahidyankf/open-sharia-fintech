module OseBe.Infrastructure.NatsConnect

open System.Diagnostics.CodeAnalysis
open System.Threading.Tasks
open NATS.Client.Core

/// Opens a best-effort NATS.Net connection on boot. Messaging is exercised at the
/// e2e level (JetStream demo, later phases); a failed connect here logs and is
/// non-fatal so the HTTP host still serves /health.
///
/// The success path requires a live NATS broker; e2e-tested per the
/// @e2e-tagged specs/apps/ose/be/behaviors/messaging/live/nats-connect.feature,
/// owned by ose-be-e2e. The graceful-failure path is unit-tested directly in
/// Tests/NatsClientTests.fs. Kept in its own file (rather than alongside the
/// pure, fully unit-tested `requireNatsUrl` in NatsClient.fs) so the
/// project-level coverage `/p:ExcludeByFile` can exclude exactly this
/// live-broker-only surface.
[<ExcludeFromCodeCoverage(Justification = "Requires a live NATS broker to connect — see module doc comment above")>]
let connectAsync (url: string) : Task<NatsConnection option> =
    task {
        let conn = new NatsConnection(NatsOpts(Url = url))

        try
            do! conn.ConnectAsync()
            printfn "NATS connected: %s" url
            return Some conn
        with ex ->
            eprintfn "NATS connect failed (%s): %s" url ex.Message
            do! conn.DisposeAsync()
            return None
    }
