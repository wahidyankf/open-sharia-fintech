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
open BeaverNestBe.Infrastructure.EnvTierLoader
open BeaverNestBe.Infrastructure.Migrations
open BeaverNestBe.Infrastructure.Sqlite.Errors
open BeaverNestBe.Operations.Database
open BeaverNestBe.Application.ReadinessPort
open BeaverNestBe.Application.DiagnosticsPort

let private runningVersion () =
    System.Reflection.Assembly.GetExecutingAssembly().GetName().Version.ToString()

let private configureApp readiness (app: IApplicationBuilder) =
    let startedAt = System.DateTimeOffset.UtcNow

    let diagnostics =
        create
            { Readiness = readiness
              Clock = fun () -> System.DateTimeOffset.UtcNow
              Version = runningVersion
              Uptime = fun () -> System.DateTimeOffset.UtcNow - startedAt }

    app.Use(middleware).UseStaticFiles(staticFileOptions).UseGiraffe(webAppWithDiagnostics readiness diagnostics)

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

/// True when argv carries nothing but a `--port` override, in either spelling. Without this the
/// catch-all below would classify `--port 4000` as an unrecognised SUBCOMMAND and refuse to boot —
/// the reason a port flag was previously impossible here.
let private isOnlyPortFlags (args: string[]) : bool =
    match args with
    | [||] -> true
    | [| "--port"; _ |] -> true
    | [| single |] -> single.StartsWith("--port=", System.StringComparison.Ordinal)
    | _ -> false

/// Applies the repo-wide `--port` flag on top of an already-parsed listener.
///
/// `parse` has resolved the env-var and default tiers already, so passing its port through as the
/// fallback yields exactly the shared precedence — flag, then BEAVERNEST_BE_HTTP_LISTEN_PORT, then
/// the 19300 default — without changing `parse`'s signature or weakening its loopback/wildcard
/// guard, which still owns the address half of the decision.
let private applyPortFlag
    (argv: string[])
    (readEnvironment: string -> string)
    (listener: ListenerConfiguration)
    : Result<ListenerConfiguration, string> =
    FsharpEnvLoader.PortResolver.resolvePort argv readEnvironment "BEAVERNEST_BE_HTTP_LISTEN_PORT" listener.Port
    |> Result.map (fun port -> { listener with Port = port })

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
    | _ when isOnlyPortFlags args -> None
    | _ -> Some(fail "invalid command")

[<EntryPoint>]
let main args =
    // Loads .env.<APP_ENV> if present; process env always wins — see
    // Infrastructure/EnvTierLoader.fs. Must run before any config read below.
    loadEnvTier ()

    match configuration () with
    | Error error -> fail error
    | Ok databaseConfiguration ->
        match commandMode args databaseConfiguration with
        | Some exitCode -> exitCode
        | None ->
            match
                prepareApplication System.Environment.GetEnvironmentVariable
                |> Result.bind (applyPortFlag args System.Environment.GetEnvironmentVariable)
            with
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
