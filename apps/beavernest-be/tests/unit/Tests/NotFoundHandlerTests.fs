module BeaverNestBe.Tests.Unit.Tests.NotFoundHandlerTests

open System.Net
open System.Net.Http
open System.Text.Json
open Xunit
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/routing/unknown-api.feature:Unknown API path returns JSON not SPA HTML
[<Fact>]
let ``unknown route returns 404 with a non-empty JSON error`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/api/v1/does-not-exist").Result
    Assert.Equal(HttpStatusCode.NotFound, resp.StatusCode)
    let body = resp.Content.ReadAsStringAsync().Result
    let doc = JsonDocument.Parse(body)
    let error = doc.RootElement.GetProperty("error").GetString()
    Assert.False(System.String.IsNullOrEmpty(error))

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/routing/greeting-retirement.feature:Greeting route is no longer part of the API
[<Fact>]
let ``retired greeting route returns a JSON 404`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/api/v1/hello").Result
    Assert.Equal(HttpStatusCode.NotFound, resp.StatusCode)
    Assert.Equal("application/json", resp.Content.Headers.ContentType.MediaType)

// Rule-16 finding SG-003 (deferred as a Gherkin scenario, kept as a plain regression test —
// see delivery.md for rationale): a wrong HTTP method on a declared route falls through to the
// same 404 handler as a genuinely unknown path.
[<Theory>]
[<InlineData("POST", "/api/v1/hello")>]
[<InlineData("PUT", "/api/v1/hello")>]
[<InlineData("DELETE", "/api/v1/hello")>]
[<InlineData("POST", "/api/v1/health")>]
let ``a wrong HTTP method on a declared route returns 404 with a non-empty JSON error`` (method: string, path: string) =
    let client = buildClient webApp
    let request = new HttpRequestMessage(HttpMethod(method), path)
    let resp = client.SendAsync(request).Result
    Assert.Equal(HttpStatusCode.NotFound, resp.StatusCode)
    let body = resp.Content.ReadAsStringAsync().Result
    let doc = JsonDocument.Parse(body)
    let error = doc.RootElement.GetProperty("error").GetString()
    Assert.False(System.String.IsNullOrEmpty(error))
