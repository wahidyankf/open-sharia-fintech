module BeaverNestBe.Tests.Unit.Steps.BddState

open Microsoft.AspNetCore.TestHost
open Microsoft.AspNetCore.Hosting
open Microsoft.AspNetCore.Builder
open Microsoft.Extensions.DependencyInjection
open Giraffe
open BeaverNestBe.Api.SecurityHeaders
open BeaverNestBe.Api.StaticContent

let private staticRoot =
    System.IO.Path.Combine(System.AppContext.BaseDirectory, "Fixtures", "flutter")

/// Build an in-process test server from a Giraffe HttpHandler.
let buildClient (handler: HttpHandler) : System.Net.Http.HttpClient =
    let builder =
        WebHostBuilder()
            .ConfigureServices(fun (s: IServiceCollection) -> s.AddGiraffe() |> ignore)
            .Configure(fun app -> app.UseGiraffe(handler))

    let server = new TestServer(builder)
    server.CreateClient()

/// Build an in-process combined static/API server using a test Flutter shell.
let buildStaticClient (handler: HttpHandler) : System.Net.Http.HttpClient =
    let builder =
        WebHostBuilder()
            .UseWebRoot(staticRoot)
            .ConfigureServices(fun (s: IServiceCollection) -> s.AddGiraffe() |> ignore)
            .Configure(fun app -> app.Use(middleware).UseStaticFiles(staticFileOptions).UseGiraffe(handler))

    let server = new TestServer(builder)
    server.CreateClient()
