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
let ``requireNatsUrl returns the configured URL when set`` () =
    withNatsUrl (Some "nats://example.internal:4222") (fun () ->
        Assert.Equal("nats://example.internal:4222", requireNatsUrl ()))

[<Fact>]
let ``requireNatsUrl fails fast when ORGANICLEVER_BE_NATS_URL is unset`` () =
    withNatsUrl None (fun () ->
        let ex = Assert.Throws<Exception>(fun () -> requireNatsUrl () |> ignore)
        Assert.Contains("ORGANICLEVER_BE_NATS_URL", ex.Message))

[<Fact>]
let ``requireNatsUrl fails fast when ORGANICLEVER_BE_NATS_URL is blank`` () =
    withNatsUrl (Some "") (fun () ->
        let ex = Assert.Throws<Exception>(fun () -> requireNatsUrl () |> ignore)
        Assert.Contains("ORGANICLEVER_BE_NATS_URL", ex.Message))

// connectAsync's success path requires a live NATS broker and is excluded from
// unit coverage (see NatsClient.fs); this test proves the documented
// graceful-failure behavior on a connection that cannot succeed, with no
// broker required.
[<Fact>]
let ``connectAsync returns None instead of throwing when the broker is unreachable`` () =
    let result =
        connectAsync "nats://127.0.0.1:1" |> Async.AwaitTask |> Async.RunSynchronously

    Assert.True(result.IsNone)
