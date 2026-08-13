module BeaverNestBe.Tests.Unit.Tests.HttpMethodSemanticsTests

open System.Net.Http
open Giraffe
open Xunit
open BeaverNestBe.Application.DiagnosticsPort
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

let private headerRepresentation (response: HttpResponseMessage) =
    response.Headers
    |> Seq.append response.Content.Headers
    |> Seq.filter (fun header ->
        not (System.String.Equals(header.Key, "Date", System.StringComparison.OrdinalIgnoreCase)))
    |> Seq.map (fun header -> header.Key, header.Value |> Seq.sort |> List.ofSeq)
    |> Map.ofSeq

let private assertHeadMatchesGet (handler: HttpHandler) (path: string) =
    let client = buildClient handler
    let getResponse = client.GetAsync(path).Result
    use headRequest = new HttpRequestMessage(HttpMethod.Head, path)
    let headResponse = client.SendAsync(headRequest).Result
    let getHeaders = headerRepresentation getResponse
    let headHeaders = headerRepresentation headResponse

    Assert.Equal(getResponse.StatusCode, headResponse.StatusCode)

    if getHeaders <> headHeaders then
        failwithf "GET headers: %A; HEAD headers: %A" getHeaders headHeaders

    Assert.Equal("", headResponse.Content.ReadAsStringAsync().Result)

[<Theory>]
[<InlineData("/api/v1/health")>]
[<InlineData("/api/v1/readiness")>]
let ``declared safe routes return HEAD with the GET status and headers but no body`` path =
    assertHeadMatchesGet (webAppWith alwaysReady) path

[<Fact>]
let ``diagnostics returns HEAD with the GET status and headers but no body`` () =
    let diagnostics =
        create
            { Readiness = alwaysReady
              // GET and HEAD are separate requests, so use a stable payload when
              // proving their representation headers (including Content-Length).
              Clock = fun () -> System.DateTimeOffset(2026, 8, 13, 12, 34, 56, System.TimeSpan.Zero)
              Version = fun () -> "unknown"
              Uptime = fun () -> System.TimeSpan.Zero }

    assertHeadMatchesGet (webAppWithDiagnostics alwaysReady diagnostics) "/api/v1/diagnostics"

[<Fact>]
let ``unavailable readiness returns HEAD with the GET status and headers but no body`` () =
    assertHeadMatchesGet (webAppWith (fromProbe (fun () -> false))) "/api/v1/readiness"

[<Fact>]
let ``unavailable diagnostics returns HEAD with the GET status and headers but no body`` () =
    let diagnostics =
        create
            { Readiness = fromProbe (fun () -> false)
              Clock = fun () -> System.DateTimeOffset.UtcNow
              Version = fun () -> "unknown"
              Uptime = fun () -> System.TimeSpan.Zero }

    assertHeadMatchesGet (webAppWithDiagnostics alwaysReady diagnostics) "/api/v1/diagnostics"
