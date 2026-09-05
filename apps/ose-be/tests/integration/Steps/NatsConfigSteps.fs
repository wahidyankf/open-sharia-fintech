module OseBe.Tests.Integration.Steps.NatsConfigSteps

open System
open TickSpec
open Xunit
open OseBe.Infrastructure.NatsClient

let mutable private previousValue: string = null
let mutable private caughtException: exn option = None

[<Given>]
let ``OSE_BE_NATS_URL is unset`` () =
    previousValue <- Environment.GetEnvironmentVariable("OSE_BE_NATS_URL")
    Environment.SetEnvironmentVariable("OSE_BE_NATS_URL", null)
    caughtException <- None

[<When>]
let ``ose-be reads its messaging configuration`` () =
    caughtException <-
        try
            requireNatsUrl () |> ignore
            None
        with ex ->
            Some ex

    Environment.SetEnvironmentVariable("OSE_BE_NATS_URL", previousValue)

[<Then>]
let ``startup aborts with a clear missing-variable error`` () =
    Assert.True(caughtException.IsSome)
    Assert.Contains("OSE_BE_NATS_URL", caughtException.Value.Message)
