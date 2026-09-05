module OseBe.Tests.Unit.Tests.NatsClientTests

open System
open System.Threading.Tasks
open Xunit
open OseBe.Infrastructure.NatsClient
open OseBe.Infrastructure.NatsConnect

[<Fact>]
let ``requireNatsUrlWith fails fast when OSE_BE_NATS_URL is unset`` () =
    let ex =
        Assert.Throws<Exception>(fun () -> requireNatsUrlWith (fun _ -> null) |> ignore)

    Assert.Contains("OSE_BE_NATS_URL", ex.Message)

[<Fact>]
let ``requireNatsUrlWith returns the configured URL`` () =
    Assert.Equal("nats://fake", requireNatsUrlWith (fun _ -> "nats://fake"))

[<Fact>]
let ``connectWith returns a connected instance without touching a network`` () =
    let mutable connected = false

    let result =
        connectWith
            id
            (fun _ ->
                connected <- true
                Task.CompletedTask)
            (fun _ -> Task.CompletedTask)
            "nats://fake"
        |> Async.AwaitTask
        |> Async.RunSynchronously

    Assert.True(connected)
    Assert.Equal(Some "nats://fake", result)

[<Fact>]
let ``connectWith disposes and returns None when connection fails`` () =
    let mutable disposed = false

    let result =
        connectWith
            id
            (fun _ -> Task.FromException(Exception "unavailable"))
            (fun _ ->
                disposed <- true
                Task.CompletedTask)
            "nats://fake"
        |> Async.AwaitTask
        |> Async.RunSynchronously

    Assert.True(disposed)
    Assert.True(result.IsNone)
