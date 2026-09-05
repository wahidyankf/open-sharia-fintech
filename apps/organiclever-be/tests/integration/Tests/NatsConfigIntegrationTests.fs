module OrganicleverBe.Tests.Integration.Tests.NatsConfigIntegrationTests

open System
open Xunit
open OrganicleverBe.Infrastructure.NatsClient

[<Fact>]
let ``real process environment reports a missing ORGANICLEVER_BE_NATS_URL clearly`` () =
    let previous = Environment.GetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL")

    try
        Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", null)
        let ex = Assert.Throws<Exception>(fun () -> requireNatsUrl () |> ignore)
        Assert.Contains("ORGANICLEVER_BE_NATS_URL", ex.Message)
    finally
        Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", previous)
