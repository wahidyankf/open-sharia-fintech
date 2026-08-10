module BeaverNestBe.Tests.Unit.Tests.ReadinessHandlerTests

open System.Net
open System.Net.Http
open Xunit
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.Domain.Readiness
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

let private readinessResponse port =
    let client = buildClient (webAppWith port)
    client.GetAsync("/api/v1/readiness").Result

let private assertNoStoreWithoutValidator (response: HttpResponseMessage) =
    Assert.Equal("no-store", response.Headers.GetValues("Cache-Control") |> Seq.head)
    Assert.False(response.Headers.Contains("ETag"))
    Assert.False(response.Content.Headers.Contains("Last-Modified"))

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/health/readiness-ready.feature:Ready workspace reports database and schema state
[<Fact>]
let ``ready port produces a safe current readiness response`` () =
    let response = readinessResponse alwaysReady
    Assert.Equal(HttpStatusCode.OK, response.StatusCode)
    assertNoStoreWithoutValidator response
    let body = response.Content.ReadAsStringAsync().Result
    Assert.Equal("{\"status\":\"ready\",\"components\":{\"database\":\"ready\",\"schema\":\"current\"}}", body)

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/health/readiness-unready.feature:Unready workspace returns a safe response
[<Fact>]
let ``unavailable port maps every failure to a safe 503 response`` () =
    let response = readinessResponse (fromProbe (fun () -> false))
    Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode)
    assertNoStoreWithoutValidator response
    let body = response.Content.ReadAsStringAsync().Result

    Assert.Equal(
        "{\"status\":\"not-ready\",\"components\":{\"database\":\"unavailable\",\"schema\":\"unknown\"}}",
        body
    )

[<Fact>]
let ``schema state is current only when expected and recorded migrations match`` () =
    Assert.Equal("current", schemaState [ "002.sql"; "001.sql" ] [ "001.sql"; "002.sql" ])
    Assert.Equal("pending", schemaState [ "001.sql"; "002.sql" ] [ "001.sql" ])
