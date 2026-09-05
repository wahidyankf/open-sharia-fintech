module OseBe.Tests.Unit.Steps.LiveMessagingSteps

open System.Net
open System.Threading.Tasks
open TickSpec
open Xunit
open OseBe.Contexts.Messaging.Domain
open OseBe.Tests.Unit.Steps.BddState

let private interactions = ResizeArray<string>()
let mutable private connection: string option = None
let mutable private demoOutcome: JetStreamDemoOutcome option = None

[<Given>]
let ``OSE_BE_NATS_URL points to a running NATS server with JetStream enabled`` () =
    interactions.Clear()
    connection <- None

[<When>]
let ``ose-be starts up`` () =
    connection <-
        OseBe.Infrastructure.NatsConnect.connectWith
            (fun url ->
                interactions.Add($"create:{url}")
                url)
            (fun _ ->
                interactions.Add("connect")
                Task.CompletedTask)
            (fun _ ->
                interactions.Add("dispose")
                Task.CompletedTask)
            "nats://fake"
        |> Async.AwaitTask
        |> Async.RunSynchronously

[<Then>]
let ``the NATS connection is established`` () =
    Assert.Equal(Some "nats://fake", connection)
    Assert.Equal<string list>([ "create:nats://fake"; "connect" ], List.ofSeq interactions)

[<Then>]
let ``the backend reports healthy after connecting`` () =
    Assert.True(connection.IsSome)
    let client = buildClient OseBe.WebApp.webApp
    let response = client.GetAsync("/api/v1/health").Result
    Assert.Equal(HttpStatusCode.OK, response.StatusCode)

[<Given>]
let ``NATS JetStream is running and ose-be is stopped`` () =
    interactions.Clear()
    demoOutcome <- None

[<When>]
let ``ose-be publishes a demo message to that subject`` () =
    let ports: OseBe.Contexts.Messaging.Infrastructure.JetStreamDemoPorts =
        { EnsureStream =
            fun () ->
                interactions.Add("stream")
                Task.CompletedTask
          EnsureConsumer =
            fun () ->
                interactions.Add("consumer")
                Task.CompletedTask
          Publish =
            fun () ->
                interactions.Add("publish")
                Task.CompletedTask
          ReceiveAndAcknowledge =
            fun () ->
                interactions.Add("receive-and-ack")
                Task.FromResult true }

    demoOutcome <-
        OseBe.Contexts.Messaging.Infrastructure.runDemoWith ports
        |> Async.AwaitTask
        |> Async.RunSynchronously
        |> Some

[<Then>]
let ``the durable consumer receives the message`` () =
    Assert.Contains("receive-and-ack", interactions)

[<Then>]
let ``the message is acknowledged`` () =
    Assert.Equal(Some DeliveredAndAcked, demoOutcome)

[<Then>]
let ``the messaging status surface reports the demo delivered and acked`` () =
    let status = OseBe.Contexts.Messaging.Application.newShared ()
    status.Set(demoOutcome.Value)
    let client = buildClient (OseBe.Contexts.Messaging.Api.routes status)
    let body = client.GetStringAsync("/api/v1/system/status/messaging").Result
    Assert.Contains("delivered_and_acked", body)
