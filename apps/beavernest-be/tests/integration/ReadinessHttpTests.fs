module BeaverNestBe.Tests.Integration.ReadinessHttpTests

open System.Net
open System.Net.Http
open System.Net.Sockets
open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Hosting
open Microsoft.Extensions.DependencyInjection
open Microsoft.Extensions.Hosting
open Giraffe
open Xunit
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.WebApp

let private availableLoopbackAddress () =
    use listener = new TcpListener(IPAddress.Loopback, 0)
    listener.Start()
    let port = (listener.LocalEndpoint :?> IPEndPoint).Port
    listener.Stop()
    $"http://127.0.0.1:{port}"

let private serve handler =
    let address = availableLoopbackAddress ()

    let host =
        Host
            .CreateDefaultBuilder([||])
            .ConfigureWebHostDefaults(fun webHostBuilder ->
                webHostBuilder
                    .UseUrls(address)
                    .ConfigureServices(fun (services: IServiceCollection) -> services.AddGiraffe() |> ignore)
                    .Configure(fun (app: IApplicationBuilder) -> app.UseGiraffe(handler))
                |> ignore)
            .Build()

    host.Start()

    host, address

let private assertNoStoreWithoutValidator (response: HttpResponseMessage) =
    Assert.Equal("no-store", response.Headers.GetValues("Cache-Control") |> Seq.head)
    Assert.False(response.Headers.Contains("ETag"))
    Assert.False(response.Content.Headers.Contains("Last-Modified"))

[<Fact>]
let ``real HTTP readiness reports ready after the database probe succeeds`` () =
    let host, address = serve (webAppWith alwaysReady)
    use host = host

    use client = new HttpClient(new HttpClientHandler(UseProxy = false))
    let response = client.GetAsync(address + "/api/v1/readiness").Result
    Assert.Equal(HttpStatusCode.OK, response.StatusCode)
    assertNoStoreWithoutValidator response

[<Fact>]
let ``real HTTP readiness maps an unavailable probe to safe service unavailable`` () =
    let host, address = serve (webAppWith (fromProbe (fun () -> false)))
    use host = host

    use client = new HttpClient(new HttpClientHandler(UseProxy = false))
    let response = client.GetAsync(address + "/api/v1/readiness").Result
    Assert.Equal(HttpStatusCode.ServiceUnavailable, response.StatusCode)
    assertNoStoreWithoutValidator response
