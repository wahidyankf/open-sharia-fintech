module OrganicleverBe.Tests.Unit.Tests.NatsClientTests

open System
open Xunit
open OrganicleverBe.Infrastructure.NatsClient
open OrganicleverBe.Infrastructure.NatsConnect

let private withNatsUrl (value: string option) (body: unit -> unit) =
    let previous = Environment.GetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL")

    try
        Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", (defaultArg value null))
        body ()
    finally
        Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", previous)

[<Fact>]
let ``natsUrl defaults to the local NATS URL when unset`` () =
    withNatsUrl None (fun () -> Assert.Equal("nats://localhost:4222", natsUrl ()))

[<Fact>]
let ``natsUrl returns the configured URL when set`` () =
    withNatsUrl (Some "nats://example.internal:4222") (fun () ->
        Assert.Equal("nats://example.internal:4222", natsUrl ()))

// connectAsync's success path requires a live NATS broker and is excluded from
// unit coverage (see NatsClient.fs); this test proves the documented
// graceful-failure behavior on a connection that cannot succeed, with no
// broker required.
[<Fact>]
let ``connectAsync returns None instead of throwing when the broker is unreachable`` () =
    let result =
        connectAsync "nats://127.0.0.1:1" |> Async.AwaitTask |> Async.RunSynchronously

    Assert.True(result.IsNone)
