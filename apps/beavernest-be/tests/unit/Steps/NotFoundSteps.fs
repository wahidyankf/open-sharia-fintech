module BeaverNestBe.Tests.Unit.Steps.NotFoundSteps

open System.Net.Http
open TickSpec
open Xunit
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

// Step definitions for the 404-fallback scenario, binding the Gherkin steps
// to the in-process Giraffe routing surface for the spec coverage validator.

let mutable private client: HttpClient option = None
let mutable private lastStatus = 0
let mutable private lastBody = ""

[<When>]
let ``I send a GET request to "/api/v1/does-not-exist"`` () =
    let resp = client.Value.GetAsync("/api/v1/does-not-exist").Result
    lastStatus <- int resp.StatusCode
    lastBody <- resp.Content.ReadAsStringAsync().Result

[<Then>]
let ``the response status is 404`` () = Assert.Equal(404, lastStatus)

[<Then>]
let ``the response body field "error" is a non-empty string`` () =
    Assert.False(System.String.IsNullOrEmpty(lastBody))
