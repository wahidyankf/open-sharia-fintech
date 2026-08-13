module BeaverNestBe.Tests.Unit.Tests.DiagnosticsHandlerTests

open System
open System.Net
open System.Net.Http
open System.Text.Json
open TickSpec
open Xunit
open BeaverNestBe.Application.DiagnosticsPort
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.WebApp
open BeaverNestBe.Tests.Unit.Steps.BddState

let private diagnosticsResponse port =
    let client = buildClient (webAppWithDiagnostics alwaysReady port)
    client.GetAsync("/api/v1/diagnostics").Result

let private assertNoStoreWithoutValidator (response: HttpResponseMessage) =
    Assert.Equal("no-store", response.Headers.GetValues("Cache-Control") |> Seq.head)
    Assert.False(response.Headers.Contains("ETag"))
    Assert.False(response.Content.Headers.Contains("Last-Modified"))

let private hasProperty (name: string) (element: JsonElement) =
    let mutable value = Unchecked.defaultof<JsonElement>
    element.TryGetProperty(name, &value)

let private deterministicReadyPort =
    create
        { Readiness = alwaysReady
          Clock = fun () -> DateTimeOffset(2026, 8, 13, 12, 34, 56, TimeSpan.Zero)
          Version = fun () -> "1.2.3"
          Uptime = fun () -> TimeSpan.FromMilliseconds(9999.0) }

let private unavailablePort =
    create
        { Readiness = fromProbe (fun () -> false)
          Clock = fun () -> failwith "unavailable diagnostics must not read the clock"
          Version = fun () -> failwith "unavailable diagnostics must not read the version"
          Uptime = fun () -> failwith "unavailable diagnostics must not read the uptime" }

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/ready.feature:Ready workspace returns a safe live snapshot
[<Fact>]
let ``ready diagnostics returns a deterministic safe snapshot`` () =
    let response = diagnosticsResponse deterministicReadyPort
    Assert.Equal(HttpStatusCode.OK, response.StatusCode)
    assertNoStoreWithoutValidator response

    use body = JsonDocument.Parse(response.Content.ReadAsStringAsync().Result)
    let root = body.RootElement
    Assert.Equal("ready", root.GetProperty("status").GetString())
    Assert.Equal("1.2.3", root.GetProperty("version").GetString())
    Assert.Equal(9L, root.GetProperty("uptimeSeconds").GetInt64())
    Assert.Equal("2026-08-13T12:34:56+00:00", root.GetProperty("serverTimeUtc").GetString())
    Assert.Equal("ready", root.GetProperty("components").GetProperty("database").GetString())
    Assert.Equal("current", root.GetProperty("components").GetProperty("schema").GetString())

// @covers specs/apps/beavernest/behavior/beavernest-be/gherkin/diagnostics/unavailable.feature:Unavailable workspace withholds diagnostic causes
[<Fact>]
let ``unavailable diagnostics returns only the safe unavailable response`` () =
    let response = diagnosticsResponse unavailablePort
    Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode)
    assertNoStoreWithoutValidator response

    use body = JsonDocument.Parse(response.Content.ReadAsStringAsync().Result)
    let root = body.RootElement
    Assert.Equal("unavailable", root.GetProperty("status").GetString())
    Assert.Equal(2, root.EnumerateObject() |> Seq.length)
    Assert.Equal("unavailable", root.GetProperty("components").GetProperty("database").GetString())
    Assert.Equal("unknown", root.GetProperty("components").GetProperty("schema").GetString())
    Assert.Equal(2, root.GetProperty("components").EnumerateObject() |> Seq.length)
    Assert.False(hasProperty "version" root)
    Assert.False(hasProperty "uptimeSeconds" root)
    Assert.False(hasProperty "serverTimeUtc" root)

let mutable private bddResponse: HttpResponseMessage option = None
let mutable private bddPort = deterministicReadyPort

[<Given>]
let ``the diagnostics clock, version and uptime are deterministic`` () = bddPort <- deterministicReadyPort

[<When>]
let ``I send a GET request to "/api/v1/diagnostics"`` () =
    bddResponse <- Some(diagnosticsResponse bddPort)

[<Then>]
let ``the JSON response reports status "ready", safe version, whole-second uptime and UTC server time`` () =
    let response = bddResponse |> Option.get
    use body = JsonDocument.Parse(response.Content.ReadAsStringAsync().Result)
    let root = body.RootElement
    Assert.Equal("ready", root.GetProperty("status").GetString())
    Assert.Equal("1.2.3", root.GetProperty("version").GetString())
    Assert.Equal(9L, root.GetProperty("uptimeSeconds").GetInt64())
    Assert.Equal("2026-08-13T12:34:56+00:00", root.GetProperty("serverTimeUtc").GetString())

[<Then>]
let ``the response reports the named database and schema readiness components`` () =
    let response = bddResponse |> Option.get
    use body = JsonDocument.Parse(response.Content.ReadAsStringAsync().Result)
    let components = body.RootElement.GetProperty("components")
    Assert.Equal("ready", components.GetProperty("database").GetString())
    Assert.Equal("current", components.GetProperty("schema").GetString())

[<Given>]
let ``diagnostics observes unavailable readiness`` () = bddPort <- unavailablePort

[<Then>]
let ``the JSON response reports status "unavailable" with only unavailable readiness components`` () =
    let response = bddResponse |> Option.get
    use body = JsonDocument.Parse(response.Content.ReadAsStringAsync().Result)
    let root = body.RootElement
    Assert.Equal("unavailable", root.GetProperty("status").GetString())
    Assert.Equal(2, root.EnumerateObject() |> Seq.length)
    Assert.Equal("unavailable", root.GetProperty("components").GetProperty("database").GetString())
    Assert.Equal("unknown", root.GetProperty("components").GetProperty("schema").GetString())

[<Then>]
let ``the diagnostics response reveals no cause, version, uptime or server time`` () =
    let response = bddResponse |> Option.get
    use body = JsonDocument.Parse(response.Content.ReadAsStringAsync().Result)
    let root = body.RootElement
    Assert.False(hasProperty "cause" root)
    Assert.False(hasProperty "version" root)
    Assert.False(hasProperty "uptimeSeconds" root)
    Assert.False(hasProperty "serverTimeUtc" root)
