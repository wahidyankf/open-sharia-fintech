module OrganicleverBe.Program

open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Hosting
open Microsoft.EntityFrameworkCore
open Microsoft.Extensions.DependencyInjection
open Microsoft.Extensions.Hosting
open Giraffe
open OrganicleverBe.Infrastructure.AppDbContext
open OrganicleverBe.Infrastructure.Database
open OrganicleverBe.Infrastructure.NatsClient
open OrganicleverBe.Infrastructure.NatsConnect
open OrganicleverBe.Contexts.Db.Infrastructure
open OrganicleverBe.Contexts.Env.Infrastructure
open OrganicleverBe.Contexts.Messaging.Application
open OrganicleverBe.Contexts.Messaging.Infrastructure
open OrganicleverBe.Contexts.Messaging.Domain
open OrganicleverBe.WebApp

let private configureApp (handler: HttpHandler) (app: IApplicationBuilder) = app.UseGiraffe handler

let private configureServices (connStr: string) (services: IServiceCollection) =
    services.AddGiraffe() |> ignore

    services.AddDbContext<AppDbContext>(fun opts -> opts.UseNpgsql(connStr).UseSnakeCaseNamingConvention() |> ignore)
    |> ignore

let private buildHost (args: string[]) (connStr: string) (handler: HttpHandler) (url: string) =
    Host
        .CreateDefaultBuilder(args)
        .ConfigureWebHostDefaults(fun webHostBuilder ->
            webHostBuilder.UseUrls(url).Configure(configureApp handler).ConfigureServices(configureServices connStr)
            |> ignore)
        .Build()

[<EntryPoint>]
let main args =
    // 0. Tiered env-file load (APP_ENV-selected .env.<tier>; process env always wins).
    loadEnvTier ()

    // 1. Config (fail-fast on missing DATABASE_URL).
    let connStr = requireDatabaseUrl ()

    // 2. Schema migration on boot (db context — DbUp embedded scripts).
    runMigrations connStr

    // 3. Messaging: config is required (fail-fast on missing ORGANICLEVER_BE_NATS_URL);
    //    the connection itself is best-effort + non-fatal, including the JetStream
    //    durable demo (see NatsConnect.fs).
    let status = newShared ()

    let natsConnection =
        connectAsync (requireNatsUrl ()) |> Async.AwaitTask |> Async.RunSynchronously

    match natsConnection with
    | Some conn ->
        let outcome = runDemo conn |> Async.AwaitTask |> Async.RunSynchronously
        status.Set outcome
    | None -> status.Set(Failed "NATS unavailable at startup")

    // 4. HTTP host (Giraffe routes for all bounded contexts + EF DbContext), bound to the port
    //    resolved by the repo-wide `--port` > ORGANICLEVER_BE_PORT > 8202 contract — see
    //    libs/fsharp-env-loader/src/PortResolver.fs, shared with every other port-binding app here.
    let readEnvironment (key: string) =
        System.Environment.GetEnvironmentVariable key

    let listenUrl =
        match FsharpEnvLoader.PortResolver.resolvePort args readEnvironment "ORGANICLEVER_BE_PORT" 8202 with
        | Ok port -> FsharpEnvLoader.PortResolver.listenUrl readEnvironment port
        | Error message ->
            eprintfn "%s" message
            exit 1

    let host = buildHost args connStr (buildWebApp status) listenUrl

    host.Run()

    natsConnection |> Option.iter (fun c -> c.DisposeAsync().AsTask().Wait())
    0
