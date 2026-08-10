module BeaverNestBe.Program

open Microsoft.AspNetCore.Builder
open Microsoft.AspNetCore.Hosting
open Microsoft.Extensions.DependencyInjection
open Microsoft.Extensions.Hosting
open Giraffe
open BeaverNestBe.Api.SecurityHeaders
open BeaverNestBe.Api.StaticContent
open BeaverNestBe.WebApp
open BeaverNestBe.Domain.HttpConfiguration
open BeaverNestBe.Domain.DatabaseConfiguration
open BeaverNestBe.Infrastructure.Migrations
open BeaverNestBe.Infrastructure.Sqlite.Errors
open BeaverNestBe.Operations.Database
open BeaverNestBe.Application.ReadinessPort

let private configureApp readiness (app: IApplicationBuilder) =
    app.Use(middleware).UseStaticFiles(staticFileOptions).UseGiraffe(webAppWith readiness)

let private configureServices (services: IServiceCollection) = services.AddGiraffe() |> ignore

let private fail error =
    eprintfn "%s" error
    1

let private configuration () =
    fromEnvironment System.Environment.GetEnvironmentVariable

let private databaseReadiness databaseConfiguration =
    fromProbe (fun () -> isReady databaseConfiguration)

/// Application composition seam: durable migration completes before the caller
/// can construct Kestrel or publish an HTTP listener.
let prepareApplication readEnvironment =
    match fromEnvironment readEnvironment, parse readEnvironment with
    | Error error, _ -> Error error
    | _, Error error -> Error error
    | Ok databaseConfiguration, Ok listener ->
        match initialize databaseConfiguration with
        | Ok() -> Ok listener
        | Error error -> Error(safeMessage error)

let private commandMode args databaseConfiguration =
    match args with
    | [| "backup"; "--name"; name |] ->
        match backup databaseConfiguration name with
        | Ok _ -> Some 0
        | Error error -> Some(fail error)
    | [| "integrity" |] ->
        match integrity databaseConfiguration with
        | Ok() -> Some 0
        | Error error -> Some(fail error)
    | [| "restore"; "--name"; name |] ->
        match restore databaseConfiguration name with
        | Ok() -> Some 0
        | Error error -> Some(fail error)
    | [||] -> None
    | _ -> Some(fail "invalid command")

[<EntryPoint>]
let main args =
    match configuration () with
    | Error error -> fail error
    | Ok databaseConfiguration ->
        match commandMode args databaseConfiguration with
        | Some exitCode -> exitCode
        | None ->
            match prepareApplication System.Environment.GetEnvironmentVariable with
            | Error error -> fail error
            | Ok listener ->
                match acquireDataDirectoryServiceLock databaseConfiguration with
                | Error error -> fail error
                | Ok serviceLock ->
                    use _serviceLock = serviceLock

                    Host
                        .CreateDefaultBuilder(args)
                        .ConfigureWebHostDefaults(fun webHostBuilder ->
                            webHostBuilder
                                .UseUrls(url listener)
                                // Suppresses the "Server: Kestrel" response header — Rule-16 finding AET-001.
                                .ConfigureKestrel(fun opts -> opts.AddServerHeader <- false)
                                .Configure(configureApp (databaseReadiness databaseConfiguration))
                                .ConfigureServices(configureServices)
                            |> ignore)
                        .Build()
                        .Run()

                    0
