module FsharpEnvLoader.Tests.Unit.Tests.PortResolverTests

open Xunit
open FsharpEnvLoader.PortResolver

/// These cases mirror, one for one, the scenarios in
/// `specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature`
/// and their TypeScript step definitions in
/// `libs/ts-env-loader/src/port-resolver.unit.test.ts`. The two
/// implementations are only "the same mechanism" if they agree case by case,
/// so the pairing is load-bearing: a case added on one side without its twin
/// on the other means the repo has two port contracts, not one.
/// Builds a `readEnvironment` seam over an in-memory pair list, returning null
/// for anything unset — exactly what `Environment.GetEnvironmentVariable`
/// does for an absent variable. No test here touches the real process
/// environment.
let private envFrom (pairs: (string * string) list) : string -> string =
    fun key ->
        pairs
        |> List.tryFind (fun (name, _) -> name = key)
        |> Option.map snd
        |> Option.defaultValue null

let private noEnv: string -> string = envFrom []

// --- Precedence ------------------------------------------------------------

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:The CLI flag outranks every other source
[<Fact>]
let ``the CLI flag outranks every other source`` () =
    let readEnvironment = envFrom [ "OSE_WWW_PORT", "4000" ]
    let actual = resolvePort [| "--port"; "5000" |] readEnvironment "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 5000, actual)

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:The prefixed variable outranks the fallback
[<Fact>]
let ``the prefixed variable outranks the fallback`` () =
    let readEnvironment = envFrom [ "OSE_WWW_PORT", "4000" ]
    let actual = resolvePort [||] readEnvironment "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 4000, actual)

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:The fallback applies when nothing else supplies a port
[<Fact>]
let ``the fallback applies when nothing else supplies a port`` () =
    let actual = resolvePort [||] noEnv "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 3100, actual)

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:A bare PORT variable never moves the listener
[<Fact>]
let ``a bare PORT variable never moves the listener`` () =
    // A bare PORT is Next.js's own knob; this repo deliberately does NOT honour
    // it as a port source, so one exported PORT cannot silently retarget every
    // app at once.
    let readEnvironment = envFrom [ "PORT", "4000" ]
    let actual = resolvePort [||] readEnvironment "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 3100, actual)

// --- Blank values fall through ---------------------------------------------

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:A blank value at a tier falls through to the next tier
[<Theory>]
[<InlineData("", "4000", 4000)>]
[<InlineData("", "", 3100)>]
[<InlineData("5000", "", 5000)>]
[<InlineData("   ", "  ", 3100)>]
let ``a blank value at a tier falls through to the next tier`` (flagValue: string) (envValue: string) (expected: int) =
    let argv = if flagValue = "" then [||] else [| "--port"; flagValue |]
    let readEnvironment = envFrom [ "OSE_WWW_PORT", envValue ]
    let actual = resolvePort argv readEnvironment "OSE_WWW_PORT" 3100
    Assert.Equal(Ok expected, actual)

// --- Malformed values fail loudly ------------------------------------------

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:A present but malformed port fails loudly instead of falling through
[<Theory>]
[<InlineData("0")>]
[<InlineData("65536")>]
[<InlineData("abc")>]
[<InlineData("3100abc")>]
[<InlineData("31.5")>]
[<InlineData("-1")>]
let ``a present but malformed port fails loudly instead of falling through`` (flagValue: string) =
    match resolvePort [| "--port"; flagValue |] noEnv "OSE_WWW_PORT" 3100 with
    | Ok port -> Assert.Fail($"expected an error, but resolved to %d{port}")
    | Error message ->
        Assert.Contains("--port", message)
        Assert.Contains("65535", message)

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:A malformed prefixed variable names that variable in the error
[<Fact>]
let ``a malformed prefixed variable names that variable in the error`` () =
    let readEnvironment = envFrom [ "OSE_WWW_PORT", "not-a-port" ]

    match resolvePort [||] readEnvironment "OSE_WWW_PORT" 3100 with
    | Ok port -> Assert.Fail($"expected an error, but resolved to %d{port}")
    | Error message ->
        Assert.Contains("OSE_WWW_PORT", message)
        Assert.Contains("65535", message)

// --- F#-side flag spellings ------------------------------------------------
// The TypeScript twin receives an already-parsed flag value from its wrapper,
// so argv spelling is this side's own concern and has no Gherkin counterpart.

[<Fact>]
let ``the joined --port=N spelling is accepted`` () =
    let actual = resolvePort [| "--port=4000" |] noEnv "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 4000, actual)

[<Fact>]
let ``a --port flag among other arguments is found`` () =
    let actual = resolvePort [| "backup"; "--port"; "4000" |] noEnv "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 4000, actual)

[<Fact>]
let ``a trailing bare --port with no value falls through to the env var`` () =
    let readEnvironment = envFrom [ "OSE_WWW_PORT", "4000" ]
    let actual = resolvePort [| "--port" |] readEnvironment "OSE_WWW_PORT" 3100
    Assert.Equal(Ok 4000, actual)

// @covers specs/libs/ts-env-loader/behavior/gherkin/port-resolver/port-resolver.feature:An out-of-range compiled-in fallback is caught at startup
[<Fact>]
let ``an out-of-range compiled-in fallback is caught at startup`` () =
    match resolvePort [||] noEnv "OSE_WWW_PORT" 70000 with
    | Ok port -> Assert.Fail($"expected an error, but resolved to %d{port}")
    | Error message -> Assert.Contains("fallback", message)

// --- Listener URL shaping --------------------------------------------------

[<Fact>]
let ``listenUrl binds loopback outside a container`` () =
    Assert.Equal("http://localhost:8302", listenUrl noEnv 8302)

[<Fact>]
let ``listenUrl binds the wildcard inside a container`` () =
    // Without this, a published container port would connect to a loopback-only
    // listener and the service would be unreachable from outside the container.
    let readEnvironment = envFrom [ "DOTNET_RUNNING_IN_CONTAINER", "true" ]
    Assert.Equal("http://+:8302", listenUrl readEnvironment 8302)

[<Fact>]
let ``listenUrl treats any non-true container flag as not-a-container`` () =
    let readEnvironment = envFrom [ "DOTNET_RUNNING_IN_CONTAINER", "false" ]
    Assert.Equal("http://localhost:8302", listenUrl readEnvironment 8302)
