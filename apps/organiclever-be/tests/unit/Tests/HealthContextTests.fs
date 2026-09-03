module OrganicleverBe.Tests.Unit.Tests.HealthContextTests

open System.Net
open Xunit
open OrganicleverBe.Contexts.Health.Application
open OrganicleverBe.Contexts.Health.Api
open OrganicleverBe.Tests.Unit.Steps.BddState

[<Fact>]
let ``the health context declares it has no infrastructure dependencies`` () =
    Assert.False(OrganicleverBe.Contexts.Health.Infrastructure.hasInfrastructureDependencies)

[<Fact>]
let ``getHealth reports healthy`` () =
    let status = getHealth ()
    Assert.Equal("ok", status.Status)

[<Fact>]
let ``health context route returns 200 JSON`` () =
    let client = buildClient routes
    let resp = client.GetAsync("/api/v1/health").Result
    Assert.Equal(HttpStatusCode.OK, resp.StatusCode)
    let body = resp.Content.ReadAsStringAsync().Result
    Assert.Contains("\"status\"", body)
