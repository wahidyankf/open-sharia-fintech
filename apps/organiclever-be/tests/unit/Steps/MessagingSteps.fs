module OrganicleverBe.Tests.Unit.Steps.MessagingSteps

open System
open TickSpec
open Xunit
open OrganicleverBe.Infrastructure.NatsClient

// Step definitions for the be-messaging config context (nats-config.feature). These
// exercise the real `requireNatsUrl` fail-fast behavior directly against production
// code (Infrastructure/NatsClient.fs), saving and restoring
// ORGANICLEVER_BE_NATS_URL around the scenario so this module's mutation of
// process-wide environment state never leaks into other tests.

let mutable private previousNatsUrl: string = null
let mutable private caughtException: exn option = None

[<Given>]
let ``ORGANICLEVER_BE_NATS_URL is unset`` () =
    previousNatsUrl <- Environment.GetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL")
    Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", null)

[<When>]
let ``organiclever-be reads its messaging configuration`` () =
    caughtException <-
        try
            requireNatsUrl () |> ignore
            None
        with ex ->
            Some ex

    Environment.SetEnvironmentVariable("ORGANICLEVER_BE_NATS_URL", previousNatsUrl)

[<Then>]
let ``startup aborts with a clear missing-variable error`` () =
    match caughtException with
    | Some ex -> Assert.Contains("ORGANICLEVER_BE_NATS_URL", ex.Message)
    | None -> failwith "expected requireNatsUrl to throw when ORGANICLEVER_BE_NATS_URL is unset"
