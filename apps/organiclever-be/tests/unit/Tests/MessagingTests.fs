module OrganicleverBe.Tests.Unit.Tests.MessagingTests

open System.Net
open Xunit
open OrganicleverBe.Contexts.Messaging.Domain
open OrganicleverBe.Contexts.Messaging.Application
open OrganicleverBe.Contexts.Messaging.Api
open OrganicleverBe.Tests.Unit.Steps.BddState

[<Fact>]
let ``a fresh shared status reports pending`` () =
    let status = newShared ()
    Assert.Equal(Pending, status.Get())

[<Fact>]
let ``outcomeToString renders the delivered-and-acked outcome`` () =
    Assert.Equal("delivered_and_acked", outcomeToString DeliveredAndAcked)

[<Fact>]
let ``outcomeToString renders a failed outcome with its reason`` () =
    Assert.Equal("failed: NATS unavailable at startup", outcomeToString (Failed "NATS unavailable at startup"))

[<Fact>]
let ``messaging status endpoint reports pending before the demo runs`` () =
    let status = newShared ()
    let client = buildClient (routes status)
    let resp = client.GetAsync("/api/v1/system/status/messaging").Result
    Assert.Equal(HttpStatusCode.OK, resp.StatusCode)
    let body = resp.Content.ReadAsStringAsync().Result
    Assert.Contains("pending", body)

[<Fact>]
let ``messaging status endpoint reflects a recorded outcome`` () =
    let status = newShared ()
    status.Set DeliveredAndAcked
    let client = buildClient (routes status)
    let resp = client.GetAsync("/api/v1/system/status/messaging").Result
    let body = resp.Content.ReadAsStringAsync().Result
    Assert.Contains("delivered_and_acked", body)
