module BeaverNestBe.Tests.Unit.Tests.HealthHandlerTests

open System.Net
open Xunit
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/health/liveness.feature:Live process reports liveness without database details
[<Fact>]
let ``health route returns 200 with status ok`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/api/v1/health").Result
    Assert.Equal(HttpStatusCode.OK, resp.StatusCode)
    let body = resp.Content.ReadAsStringAsync().Result
    Assert.Contains("\"status\":\"ok\"", body)

// Rule-16 finding AET-001: every response carries the nosniff hardening header.
[<Fact>]
let ``health route response carries the X-Content-Type-Options header`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/api/v1/health").Result
    let headerValue = resp.Headers.GetValues("X-Content-Type-Options") |> Seq.head
    Assert.Equal("nosniff", headerValue)
