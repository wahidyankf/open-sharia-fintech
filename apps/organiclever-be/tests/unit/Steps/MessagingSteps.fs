module OrganicleverBe.Tests.Unit.Steps.MessagingSteps

open TickSpec
open Xunit
open OrganicleverBe.Infrastructure.NatsClient

let mutable private readEnvironment: string -> string = fun _ -> null
let mutable private caughtException: exn option = None

[<Given>]
let ``ORGANICLEVER_BE_NATS_URL is unset`` () =
    readEnvironment <- fun _ -> null
    caughtException <- None

[<When>]
let ``organiclever-be reads its messaging configuration`` () =
    caughtException <-
        try
            requireNatsUrlWith readEnvironment |> ignore
            None
        with ex ->
            Some ex

[<Then>]
let ``startup aborts with a clear missing-variable error`` () =
    Assert.True(caughtException.IsSome)
    Assert.Contains("ORGANICLEVER_BE_NATS_URL", caughtException.Value.Message)
