module FsharpEnvLoader.Tests.Integration.Behaviour.EnvTierIntegrationBehaviourDriver

open System
open System.Collections.Generic
open System.IO
open System.Reflection
open TickSpec
open Xunit
open FsharpEnvLoader

[<assembly: CollectionBehavior(DisableTestParallelization = true)>]
do ()

type EnvTierIntegrationSteps() =
    let namedDirs = Dictionary<string, string>()
    let mutable ownedDirs: string list = []
    let touchedEnvKeys = HashSet<string>()
    let originalAppEnv = Environment.GetEnvironmentVariable("APP_ENV")
    let mutable resolvedTier: string option = None
    let mutable loadOutcome: Result<unit, exn> option = None

    let newTempDir () : string =
        let path =
            Path.Combine(Path.GetTempPath(), $"fsharp-env-loader-integration-{Guid.NewGuid():N}")

        Directory.CreateDirectory(path) |> ignore
        ownedDirs <- path :: ownedDirs
        path

    let ensureDir (name: string) : string =
        match namedDirs.TryGetValue name with
        | true, path -> path
        | false, _ ->
            let path = newTempDir ()
            namedDirs[name] <- path
            path

    [<Given>]
    member _.``a fresh temporary search directory``() = ensureDir "primary" |> ignore

    [<Given>]
    member _.``a fresh temporary search directory named "([^"]+)"``(name: string) = ensureDir name |> ignore

    [<Given>]
    member _.``a search directory that does not exist``() =
        namedDirs["primary"] <- Path.Combine(Path.GetTempPath(), $"missing-{Guid.NewGuid():N}")

    [<Given>]
    member _.``the search directory has a "([^"]+)" file setting "([^"]+)" to "([^"]*)"``
        (fileName: string, key: string, value: string)
        =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), $"{key}={value}\n")
        touchedEnvKeys.Add key |> ignore

    [<Given>]
    member _.``directory "([^"]+)" has a "([^"]+)" file setting "([^"]+)" to "([^"]*)"``
        (name: string, fileName: string, key: string, value: string)
        =
        File.WriteAllText(Path.Combine(ensureDir name, fileName), $"{key}={value}\n")
        touchedEnvKeys.Add key |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with no content``(fileName: string) =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), "")

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with the raw line "([^"]*)"``(fileName: string, line: string) =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), line + "\n")

        match line.IndexOf('=') with
        | -1 -> ()
        | index -> touchedEnvKeys.Add(line.Substring(0, index).Trim()) |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with CRLF lines setting "([^"]+)" to "([^"]*)" and "([^"]+)" to "([^"]*)"``
        (fileName: string, keyA: string, valueA: string, keyB: string, valueB: string)
        =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), $"{keyA}={valueA}\r\n{keyB}={valueB}\r\n")
        touchedEnvKeys.Add keyA |> ignore
        touchedEnvKeys.Add keyB |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with a leading comment, a blank line, then "([^"]+)" set to "([^"]*)", then a trailing comment``
        (fileName: string, key: string, value: string)
        =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), $"# first\n\n   \n{key}={value}\n# last\n")
        touchedEnvKeys.Add key |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with a line with no "=" followed by "([^"]+)" set to "([^"]*)"``
        (fileName: string, key: string, value: string)
        =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), $"invalid\n{key}={value}\n")
        touchedEnvKeys.Add key |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file setting padded "([^"]+)" to "([^"]*)"``
        (fileName: string, key: string, value: string)
        =
        File.WriteAllText(Path.Combine(ensureDir "primary", fileName), $"   {key}   =   {value}   \n")
        touchedEnvKeys.Add key |> ignore

    [<Given>]
    member _.``the process environment already has "([^"]+)" set to "([^"]*)"``(key: string, value: string) =
        Environment.SetEnvironmentVariable(key, value)
        touchedEnvKeys.Add key |> ignore

    [<Given>]
    member _.``APP_ENV is unset``() =
        Environment.SetEnvironmentVariable("APP_ENV", null)

    [<Given>]
    member _.``APP_ENV is set to "([^"]*)"``(value: string) =
        Environment.SetEnvironmentVariable("APP_ENV", value)

    [<When>]
    member _.``the env tier resolves``() =
        resolvedTier <- Some(EnvTier.resolveTier ())

    [<When>]
    member _.``the env tier loads from the search directory``() =
        loadOutcome <-
            try
                EnvTier.loadEnvTierFrom [ ensureDir "primary" ]
                Some(Ok())
            with error ->
                Some(Error error)

    [<When>]
    member _.``the env tier loads from search directories "([^"]+)" then "([^"]+)"``(a: string, b: string) =
        loadOutcome <-
            try
                EnvTier.loadEnvTierFrom [ ensureDir a; ensureDir b ]
                Some(Ok())
            with error ->
                Some(Error error)

    [<Then>]
    member _.``the resolved tier is "([^"]*)"``(expected: string) =
        Assert.Equal(expected, resolvedTier.Value)

    [<Then>]
    member _.``"([^"]+)" is "([^"]*)"``(key: string, expected: string) =
        Assert.Equal(expected, Environment.GetEnvironmentVariable key)

    [<Then>]
    member _.``loading completes without raising``() =
        match loadOutcome with
        | Some(Ok()) -> ()
        | Some(Error error) -> Assert.Fail($"environment loading raised: %s{error.Message}")
        | None -> Assert.Fail("environment loading was not invoked")

    [<AfterScenario>]
    member _.Cleanup() =
        for key in touchedEnvKeys do
            Environment.SetEnvironmentVariable(key, null)

        Environment.SetEnvironmentVariable("APP_ENV", originalAppEnv)

        for path in ownedDirs do
            if Directory.Exists path then
                Directory.Delete(path, true)

        namedDirs.Clear()
        touchedEnvKeys.Clear()
        ownedDirs <- []
        resolvedTier <- None
        loadOutcome <- None

module private FeatureRunner =
    let private assembly = Assembly.GetExecutingAssembly()

    let scenarios () : seq<obj[]> =
        let assemblyDir = Path.GetDirectoryName assembly.Location
        let featurePath = Path.Combine(assemblyDir, "specs", "env-tier", "env-tier.feature")
        let definitions = StepDefinitions([| typeof<EnvTierIntegrationSteps> |])

        let feature =
            definitions.GenerateFeature(featurePath, File.ReadAllLines featurePath)

        feature.Scenarios |> Seq.map (fun scenario -> [| scenario :> obj |])

type EnvTierIntegrationFeatureTests() =
    static member Scenarios() : seq<obj[]> =
        FeatureRunner.scenarios () |> Seq.toList :> seq<_>

    [<Theory>]
    [<MemberData("Scenarios")>]
    member _.``Tiered env file loading through real OS adapters``(scenario: Scenario) = scenario.Action.Invoke()
