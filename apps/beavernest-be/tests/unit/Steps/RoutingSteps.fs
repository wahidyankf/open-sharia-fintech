module BeaverNestBe.Tests.Unit.Steps.RoutingSteps

open System.Net.Http
open TickSpec
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

let mutable private client: HttpClient option = None
let mutable private lastStatus = 0

[<When>]
let ``I send a GET request to "/api/v1/hello"`` () =
    let response = client.Value.GetAsync("/api/v1/hello").Result
    lastStatus <- int response.StatusCode

[<When>]
let ``I send a GET request to "/assets/missing.js"`` () =
    let response = client.Value.GetAsync("/assets/missing.js").Result
    lastStatus <- int response.StatusCode

[<When>]
let ``I send a GET request to "/future-client-route"`` () =
    let response = client.Value.GetAsync("/future-client-route").Result
    lastStatus <- int response.StatusCode
