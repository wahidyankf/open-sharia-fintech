module BeaverNestBe.Tests.Unit.Steps.ReadinessSteps

open System.Net.Http
open TickSpec
open Xunit
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

let mutable private client: HttpClient option = None
let mutable private lastStatus = 0
let mutable private lastBody = ""
let mutable private cacheControl = ""
let mutable private containsValidator = false

let private runReadiness port =
    let response =
        buildClient (webAppWith port)
        |> fun http -> http.GetAsync("/api/v1/readiness").Result

    lastStatus <- int response.StatusCode
    lastBody <- response.Content.ReadAsStringAsync().Result
    cacheControl <- response.Headers.GetValues("Cache-Control") |> Seq.head

    containsValidator <-
        response.Headers.Contains("ETag")
        || response.Content.Headers.Contains("Last-Modified")

[<Given>]
let ``startup migrations completed and SQLite accepts queries`` () = runReadiness alwaysReady

[<Given>]
let ``SQLite cannot complete the readiness query`` () =
    runReadiness (fromProbe (fun () -> false))

[<When>]
let ``I send a GET request to "/api/v1/readiness"`` () = ()

[<Then>]
let ``the response status is 200`` () = Assert.Equal(200, lastStatus)

[<Then>]
let ``the response status is 503`` () = Assert.Equal(503, lastStatus)

[<Then>]
let ``the JSON response reports status "ready", database "ready" and schema "current"`` () =
    Assert.Equal("{\"status\":\"ready\",\"components\":{\"database\":\"ready\",\"schema\":\"current\"}}", lastBody)

[<Then>]
let ``the JSON response reports status "not-ready"`` () =
    Assert.Equal(
        "{\"status\":\"not-ready\",\"components\":{\"database\":\"unavailable\",\"schema\":\"unknown\"}}",
        lastBody
    )

[<Then>]
let ``the response reveals no database path, SQL text or exception detail`` () =
    Assert.DoesNotContain("/", lastBody)
    Assert.DoesNotContain("select", lastBody, System.StringComparison.OrdinalIgnoreCase)
    Assert.DoesNotContain("exception", lastBody, System.StringComparison.OrdinalIgnoreCase)

[<Then>]
let ``the response sends "Cache-Control: no-store" without a cache validator`` () =
    Assert.Equal("no-store", cacheControl)
    Assert.False(containsValidator)
