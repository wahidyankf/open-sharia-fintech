module BeaverNestBe.Tests.Unit.Steps.HealthSteps

open System.Net.Http
open TickSpec
open Xunit
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

// Step definitions binding the health/greeting Gherkin backgrounds and shared
// assertions to the in-process Giraffe routing surface, so the spec coverage
// validator resolves every step to executable code.

let mutable private client: HttpClient option = None
let mutable private lastStatus = 0
let mutable private lastBody = ""

[<Given>]
let ``the service has finished starting`` () = client <- Some(buildClient webApp)

[<Given>]
let ``the BeaverNest process is accepting HTTP requests`` () = client <- Some(buildClient webApp)

[<When>]
let ``I send a GET request to "/api/v1/health"`` () =
    let resp = client.Value.GetAsync("/api/v1/health").Result
    lastStatus <- int resp.StatusCode
    lastBody <- resp.Content.ReadAsStringAsync().Result

[<Then>]
let ``the response status is 200`` () = Assert.Equal(200, lastStatus)

[<Then>]
let ``the JSON response reports status "ok"`` () =
    Assert.Contains("\"status\":\"ok\"", lastBody.Replace(" ", ""))

[<Then>]
let ``the response reveals no database path or migration detail`` () =
    Assert.DoesNotContain("sqlite", lastBody, System.StringComparison.OrdinalIgnoreCase)
    Assert.DoesNotContain("migration", lastBody, System.StringComparison.OrdinalIgnoreCase)
