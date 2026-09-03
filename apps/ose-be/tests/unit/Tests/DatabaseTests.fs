module OseBe.Tests.Unit.Tests.DatabaseTests

open System
open Xunit
open OseBe.Infrastructure.Database

/// Saves and restores DATABASE_URL around a test body so this module's
/// mutations of process-wide environment state never leak into other tests.
let private withDatabaseUrl (value: string option) (body: unit -> unit) =
    let previous = Environment.GetEnvironmentVariable("DATABASE_URL")

    try
        Environment.SetEnvironmentVariable("DATABASE_URL", (defaultArg value null))
        body ()
    finally
        Environment.SetEnvironmentVariable("DATABASE_URL", previous)

[<Fact>]
let ``requireDatabaseUrl returns the configured connection string`` () =
    withDatabaseUrl (Some "Host=localhost;Database=ose_be;Username=x;Password=x") (fun () ->
        Assert.Equal("Host=localhost;Database=ose_be;Username=x;Password=x", requireDatabaseUrl ()))

[<Fact>]
let ``requireDatabaseUrl fails fast when DATABASE_URL is unset`` () =
    withDatabaseUrl None (fun () ->
        let ex = Assert.Throws<Exception>(fun () -> requireDatabaseUrl () |> ignore)
        Assert.Contains("DATABASE_URL", ex.Message))

[<Fact>]
let ``requireDatabaseUrl fails fast when DATABASE_URL is blank`` () =
    withDatabaseUrl (Some "") (fun () ->
        let ex = Assert.Throws<Exception>(fun () -> requireDatabaseUrl () |> ignore)
        Assert.Contains("DATABASE_URL", ex.Message))
