module OrganicleverBe.Tests.Integration.Steps.NatsConfigSteps

open System
open TickSpec
open Xunit
open OrganicleverBe.Infrastructure.NatsClient

let mutable private previousValue: string = null
let mutable private caughtException: exn option = None

[<Given>]
let ``ORGANICLEVER_BE_NATS_URL is unset`` () =
    previousValue <- Environment.GetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL")
    Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", null)
    caughtException <- None

[<When>]
let ``organiclever-be reads its messaging configuration`` () =
    caughtException <-
        try
            requireNatsUrl () |> ignore
            None
        with ex ->
            Some ex

    Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", previousValue)

[<Then>]
let ``startup aborts with a clear missing-variable error`` () =
    Assert.True(caughtException.IsSome)
    Assert.Contains("ORGANICLEVER_BE_NATS_URL", caughtException.Value.Message)
