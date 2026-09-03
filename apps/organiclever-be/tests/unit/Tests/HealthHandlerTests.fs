module OrganicleverBe.Tests.Unit.Tests.HealthHandlerTests

open System.Net
open Xunit
open OrganicleverBe.WebApp
open OrganicleverBe.Tests.Unit.Steps.BddState

[<Fact>]
let ``health handler returns 200`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/health").Result
    Assert.Equal(HttpStatusCode.OK, resp.StatusCode)

// @covers specs/apps/organiclever/be/behaviors/health/health-check.feature:Health endpoint reports the service as UP
[<Fact>]
let ``health handler returns JSON status ok`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/health").Result
    let body = resp.Content.ReadAsStringAsync().Result
    Assert.Contains("\"status\"", body)
    Assert.Contains("ok", body)
    Assert.Equal("application/json", resp.Content.Headers.ContentType.MediaType)

// @covers specs/apps/organiclever/be/behaviors/health/health-check.feature:Anonymous health check does not expose component details
[<Fact>]
let ``health handler does not expose component details`` () =
    let client = buildClient webApp
    let resp = client.GetAsync("/health").Result
    Assert.Equal(HttpStatusCode.OK, resp.StatusCode)
    let body = resp.Content.ReadAsStringAsync().Result
    Assert.DoesNotContain("database", body)
    Assert.DoesNotContain("components", body)
