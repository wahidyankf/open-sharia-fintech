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

let private buildHost (args: string[]) (connStr: string) (handler: HttpHandler) =
    Host
        .CreateDefaultBuilder(args)
        .ConfigureWebHostDefaults(fun webHostBuilder ->
            webHostBuilder.Configure(configureApp handler).ConfigureServices(configureServices connStr)
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

    // 3. Messaging: best-effort NATS connect + JetStream durable demo (non-fatal).
    let status = newShared ()

    let natsConnection =
        connectAsync (natsUrl ()) |> Async.AwaitTask |> Async.RunSynchronously

    match natsConnection with
    | Some conn ->
        let outcome = runDemo conn |> Async.AwaitTask |> Async.RunSynchronously
        status.Set outcome
    | None -> status.Set(Failed "NATS unavailable at startup")

    // 4. HTTP host (Giraffe routes for all bounded contexts + EF DbContext).
    let host = buildHost args connStr (buildWebApp status)

    host.Run()

    natsConnection |> Option.iter (fun c -> c.DisposeAsync().AsTask().Wait())
    0
