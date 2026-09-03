module OseBe.Program

open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Hosting
open Microsoft.EntityFrameworkCore
open Microsoft.Extensions.DependencyInjection
open Microsoft.Extensions.Hosting
open Giraffe
open OseBe.Infrastructure.AppDbContext
open OseBe.Infrastructure.Database
open OseBe.Contexts.Config.Infrastructure
open OseBe.Infrastructure.NatsClient
open OseBe.Infrastructure.NatsConnect
open OseBe.Contexts.Db.Infrastructure
open OseBe.Contexts.Messaging.Application
open OseBe.Contexts.Messaging.Infrastructure
open OseBe.Contexts.Messaging.Domain
open OseBe.WebApp

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
    // 1. Env tier (loads .env.<APP_ENV> if present; process env always wins — see
    //    Infrastructure/EnvTier.fs). Must run before any config read below.
    loadEnvTier ()

    // 2. Config (fail-fast on missing DATABASE_URL).
    let connStr = requireDatabaseUrl ()

    // 3. Schema migration on boot (db context — DbUp embedded scripts).
    runMigrations connStr

    // 4. Messaging: fail-fast on missing OSE_BE_NATS_URL (a configuration error);
    //    once configured, the connect attempt itself + JetStream durable demo
    //    stay best-effort (non-fatal) if the broker is unreachable.
    let status = newShared ()

    let natsConnection =
        connectAsync (requireNatsUrl ()) |> Async.AwaitTask |> Async.RunSynchronously

    match natsConnection with
    | Some conn ->
        let outcome = runDemo conn |> Async.AwaitTask |> Async.RunSynchronously
        status.Set outcome
    | None -> status.Set(Failed "NATS unavailable at startup")

    // 5. HTTP host (Giraffe routes for all bounded contexts + EF DbContext), bound to the port
    //    resolved by the repo-wide `--port` > OSE_BE_PORT > 8302 contract — see
    //    libs/fsharp-env-loader/src/PortResolver.fs, shared with every other port-binding app here.
    let readEnvironment (key: string) =
        System.Environment.GetEnvironmentVariable key

    let listenUrl =
        match FsharpEnvLoader.PortResolver.resolvePort args readEnvironment "OSE_BE_PORT" 8302 with
        | Ok port -> FsharpEnvLoader.PortResolver.listenUrl readEnvironment port
        | Error message ->
            eprintfn "%s" message
            exit 1

    let host = buildHost args connStr (buildWebApp status) listenUrl

    host.Run()

    natsConnection |> Option.iter (fun c -> c.DisposeAsync().AsTask().Wait())
    0
