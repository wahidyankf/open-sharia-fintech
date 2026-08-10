module BeaverNestBe.Tests.Integration.HostBootTests

open System.Net
open System.Net.Http
open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Hosting
open Microsoft.AspNetCore.Hosting.Server
open Microsoft.AspNetCore.Hosting.Server.Features
open Microsoft.Extensions.DependencyInjection
open Microsoft.Extensions.Hosting
open Giraffe
open Xunit
open BeaverNestBe.WebApp

/// Boots the real Kestrel host on an ephemeral port and serves a live HTTP
/// request — distinct from the unit-level in-memory `TestServer` harness,
/// this proves the process actually starts and accepts real network traffic.
[<Fact>]
let ``the host boots and serves /api/v1/health over real HTTP`` () =
    let host =
        Host
            .CreateDefaultBuilder([||])
            .ConfigureWebHostDefaults(fun webHostBuilder ->
                webHostBuilder
                    .UseUrls("http://127.0.0.1:0")
                    .ConfigureServices(fun (services: IServiceCollection) -> services.AddGiraffe() |> ignore)
                    .Configure(fun (app: IApplicationBuilder) -> app.UseGiraffe(webApp))
                |> ignore)
            .Build()

    host.Start()

    let address =
        host.Services.GetRequiredService<IServer>().Features.Get<IServerAddressesFeature>().Addresses
        |> Seq.head

    use client = new HttpClient(new HttpClientHandler(UseProxy = false))
    let resp = client.GetAsync(address + "/api/v1/health").Result
    Assert.Equal(HttpStatusCode.OK, resp.StatusCode)

    host.StopAsync().Wait()
