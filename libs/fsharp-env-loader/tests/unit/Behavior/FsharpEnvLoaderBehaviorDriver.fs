/// TickSpec step definitions and scenario runner binding both of
/// `fsharp-env-loader`'s Gherkin feature files —
/// `specs/libs/fsharp-env-loader/behaviors/env-tier/env-tier.feature` and
/// `specs/libs/fsharp-env-loader/behaviors/port-resolver/port-resolver.feature`
/// — to `FsharpEnvLoader.EnvTier` and `FsharpEnvLoader.PortResolver`. This is
/// the registry's declared `behavior.adapters.unit.driver` for
/// `fsharp-env-loader` in `repo-config.yml`.
///
/// One instance-mutable-field step class (the pattern established by
/// `apps/rhino-cli/src/tests/unit/Steps/EnvSteps.fs`), consumed by a
/// `[<Theory>][<MemberData>]` runner per feature file (the pattern
/// established by `libs/fsharp-crane-core/tests/unit/Tests/
/// PdfToMarkdownRoutingFeatureRunner.fs`) so `Scenario Outline` `Examples`
/// tables expand naturally through TickSpec itself rather than a hand-rolled
/// per-title slice. `[<AfterScenario>]` resets every real-process-environment
/// side effect (`APP_ENV` plus any key a scenario wrote) so scenario order
/// never changes a result — the env-tier scenarios are precedence tests, so
/// leaked state from an earlier scenario would silently pass a case that
/// should fail.
module FsharpEnvLoader.Tests.Unit.Behavior.FsharpEnvLoaderBehaviorDriver

open System
open System.Collections.Generic
open System.IO
open System.Reflection
open TickSpec
open Xunit
open FsharpEnvLoader

/// The env-tier scenarios below mutate `APP_ENV` and other real process
/// environment variables — process-global state that would race every other
/// file's tests (including `EnvTierTests.fs`'s own `withAppEnv` facts) under
/// xunit's default one-collection-per-module parallelism. Matches the same
/// assembly-wide opt-out already established by
/// `apps/rhino-cli/src/tests/unit/Steps/GitRootUnitTests.fs` and
/// `apps/organiclever-be/tests/integration/TestCollections.fs`.
[<assembly: CollectionBehavior(DisableTestParallelization = true)>]
do ()

type FsharpEnvLoaderBehaviorSteps() =
    // --- shared temp-directory bookkeeping (env-tier scenarios) ------------
    let namedDirs = Dictionary<string, string>()
    let mutable ownedDirs: string list = []
    let touchedEnvKeys = HashSet<string>()
    let originalAppEnv = Environment.GetEnvironmentVariable("APP_ENV")

    let newTempDir () : string =
        let dir =
            Path.Combine(Path.GetTempPath(), "fsharp-env-loader-behavior-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        dir

    let ensureDir (name: string) : string =
        match namedDirs.TryGetValue name with
        | true, dir -> dir
        | false, _ ->
            let dir = newTempDir ()
            namedDirs.[name] <- dir
            ownedDirs <- dir :: ownedDirs
            dir

    // --- PortResolver scenario state ----------------------------------------
    let mutable declaredVar = ""
    let mutable declaredFallback = 0
    let mutable envMap: Map<string, string> = Map.empty
    let mutable resolveOutcome: Result<int, string> option = None

    let runResolve (argv: string list) : Result<int, string> =
        let readEnvironment =
            fun (key: string) ->
                match envMap.TryFind key with
                | Some v -> v
                | None -> null

        PortResolver.resolvePort (List.toArray argv) readEnvironment declaredVar declaredFallback

    // --- env-tier.feature ---------------------------------------------------

    [<Given>]
    member _.``a fresh temporary search directory``() = ensureDir "primary" |> ignore

    [<Given>]
    member _.``a fresh temporary search directory named "([^"]+)"``(name: string) = ensureDir name |> ignore

    [<Given>]
    member _.``a search directory that does not exist``() =
        let dir =
            Path.Combine(Path.GetTempPath(), "fsharp-env-loader-behavior-missing-" + Guid.NewGuid().ToString("N"))

        namedDirs.["primary"] <- dir

    [<Given>]
    member _.``the search directory has a "([^"]+)" file setting "([^"]+)" to "([^"]*)"``
        (fileName: string, key: string, value: string)
        =
        let dir = ensureDir "primary"
        File.WriteAllText(Path.Combine(dir, fileName), sprintf "%s=%s\n" key value)
        touchedEnvKeys.Add(key) |> ignore

    [<Given>]
    member _.``directory "([^"]+)" has a "([^"]+)" file setting "([^"]+)" to "([^"]*)"``
        (name: string, fileName: string, key: string, value: string)
        =
        let dir = ensureDir name
        File.WriteAllText(Path.Combine(dir, fileName), sprintf "%s=%s\n" key value)
        touchedEnvKeys.Add(key) |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with no content``(fileName: string) =
        let dir = ensureDir "primary"
        File.WriteAllText(Path.Combine(dir, fileName), "")

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with the raw line "([^"]*)"``(fileName: string, line: string) =
        let dir = ensureDir "primary"
        File.WriteAllText(Path.Combine(dir, fileName), line + "\n")

        match line.IndexOf('=') with
        | -1 -> ()
        | idx -> touchedEnvKeys.Add(line.Substring(0, idx)) |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with CRLF lines setting "([^"]+)" to "([^"]*)" and "([^"]+)" to "([^"]*)"``
        (fileName: string, keyA: string, valueA: string, keyB: string, valueB: string)
        =
        let dir = ensureDir "primary"
        File.WriteAllText(Path.Combine(dir, fileName), sprintf "%s=%s\r\n%s=%s\r\n" keyA valueA keyB valueB)
        touchedEnvKeys.Add(keyA) |> ignore
        touchedEnvKeys.Add(keyB) |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with a leading comment, a blank line, then "([^"]+)" set to "([^"]*)", then a trailing comment``
        (fileName: string, key: string, value: string)
        =
        let dir = ensureDir "primary"

        File.WriteAllText(
            Path.Combine(dir, fileName),
            sprintf "# a leading comment\n\n   \n%s=%s\n# a trailing comment\n" key value
        )

        touchedEnvKeys.Add(key) |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file with a line with no "=" followed by "([^"]+)" set to "([^"]*)"``
        (fileName: string, key: string, value: string)
        =
        let dir = ensureDir "primary"
        File.WriteAllText(Path.Combine(dir, fileName), sprintf "this line has no equals sign\n%s=%s\n" key value)
        touchedEnvKeys.Add(key) |> ignore

    [<Given>]
    member _.``the search directory has a "([^"]+)" file setting padded "([^"]+)" to "([^"]*)"``
        (fileName: string, key: string, value: string)
        =
        let dir = ensureDir "primary"
        File.WriteAllText(Path.Combine(dir, fileName), sprintf "   %s   =   %s   \n" key value)
        touchedEnvKeys.Add(key) |> ignore

    [<Given>]
    member _.``the process environment already has "([^"]+)" set to "([^"]*)"``(key: string, value: string) =
        Environment.SetEnvironmentVariable(key, value)
        touchedEnvKeys.Add(key) |> ignore

    [<Given>]
    member _.``APP_ENV is unset``() =
        Environment.SetEnvironmentVariable("APP_ENV", null)

    [<Given>]
    member _.``APP_ENV is set to "([^"]*)"``(value: string) =
        Environment.SetEnvironmentVariable("APP_ENV", value)

    [<When>]
    member _.``the env tier loads from the search directory``() =
        EnvTier.loadEnvTierFrom [ ensureDir "primary" ]

    [<When>]
    member _.``the env tier loads from search directories "([^"]+)" then "([^"]+)"``(a: string, b: string) =
        EnvTier.loadEnvTierFrom [ ensureDir a; ensureDir b ]

    [<Then>]
    member _.``the resolved tier is "([^"]*)"``(expected: string) =
        Assert.Equal(expected, EnvTier.resolveTier ())

    [<Then>]
    member _.``"([^"]+)" is "([^"]*)"``(key: string, expected: string) =
        Assert.Equal(expected, Environment.GetEnvironmentVariable(key))

    [<Then>]
    member _.``loading completes without raising``() = Assert.True(true)

    // --- port-resolver.feature ----------------------------------------------

    [<Given>]
    member _.``the app declares the prefixed variable "([^"]+)" with fallback (\d+)``(varName: string, fallback: int) =
        declaredVar <- varName
        declaredFallback <- fallback

    [<Given>]
    member _.``the environment sets "([^"]+)" to "([^"]*)"``(key: string, value: string) =
        envMap <- envMap.Add(key, value)

    [<Given>]
    member _.``the environment does not set "([^"]+)"``(key: string) = envMap <- envMap.Remove(key)

    [<When>]
    member _.``the port resolves with a "([^"]+)" flag of "([^"]*)"``(flagName: string, value: string) =
        resolveOutcome <- Some(runResolve [ flagName; value ])

    [<When>]
    member _.``the port resolves with no "([^"]+)" flag``(_flagName: string) = resolveOutcome <- Some(runResolve [])

    [<Then>]
    member _.``the resolved port is (\d+)``(expected: int) =
        match resolveOutcome with
        | Some(Ok actual) -> Assert.Equal(expected, actual)
        | Some(Error msg) -> Assert.Fail(sprintf "expected Ok %d but resolution errored: %s" expected msg)
        | None -> Assert.Fail("no resolution has been attempted")

    [<Then>]
    member _.``resolution throws, naming "([^"]+)" and the valid range``(sourceName: string) =
        match resolveOutcome with
        | Some(Error msg) ->
            Assert.Contains(sourceName, msg)
            Assert.Contains("between", msg)
        | Some(Ok actual) ->
            Assert.Fail(sprintf "expected an error naming \"%s\" but resolution returned Ok %d" sourceName actual)
        | None -> Assert.Fail("no resolution has been attempted")

    // --- cleanup --------------------------------------------------------------

    /// Restores every real-process-environment side effect a scenario made,
    /// so scenario execution order never changes a result. PortResolver
    /// scenarios never touch the real environment (they thread an in-memory
    /// `envMap` through a caller-supplied `readEnvironment` seam instead), so
    /// only the env-tier bookkeeping needs resetting here.
    [<AfterScenario>]
    member _.Cleanup() =
        for key in touchedEnvKeys do
            Environment.SetEnvironmentVariable(key, null)

        touchedEnvKeys.Clear()
        Environment.SetEnvironmentVariable("APP_ENV", originalAppEnv)

        for dir in ownedDirs do
            if Directory.Exists dir then
                Directory.Delete(dir, true)

        // The step class instance is shared across every scenario generated
        // from one `GenerateFeature` call (see `FeatureRunner` below), so
        // `namedDirs` must be cleared too — otherwise the next scenario's
        // "a fresh temporary search directory" step would resolve "primary"
        // back to a path this cleanup just deleted from disk.
        ownedDirs <- []
        namedDirs.Clear()
        declaredVar <- ""
        declaredFallback <- 0
        envMap <- Map.empty
        resolveOutcome <- None

/// Reads the Gherkin feature files TickSpec's `CopyGherkinSpecs` build target
/// copies into this test binary's own output directory, and runs every
/// scenario in `featureFileName` through `FsharpEnvLoaderBehaviorSteps`.
module private FeatureRunner =
    let private assembly = Assembly.GetExecutingAssembly()

    let private specsDir =
        let assemblyDir = Path.GetDirectoryName(assembly.Location)
        Path.Combine(assemblyDir, "specs")

    let private getFeatureFile (featureFileName: string) : string option =
        if Directory.Exists specsDir then
            Directory.GetFiles(specsDir, "*.feature", SearchOption.AllDirectories)
            |> Array.tryFind (fun f -> Path.GetFileName(f) = featureFileName)
        else
            None

    let scenarios (featureFileName: string) : seq<obj[]> =
        match getFeatureFile featureFileName with
        | Some path ->
            let defs = StepDefinitions([| typeof<FsharpEnvLoaderBehaviorSteps> |])
            let lines = File.ReadAllLines path
            let feature = defs.GenerateFeature(path, lines)
            feature.Scenarios |> Seq.map (fun scenario -> [| scenario :> obj |])
        | None -> Seq.empty

type EnvTierFeatureTests() =
    static member Scenarios() : seq<obj[]> =
        FeatureRunner.scenarios "env-tier.feature" |> Seq.toList :> seq<_>

    [<Theory>]
    [<MemberData("Scenarios")>]
    member _.``Tiered .env file loading``(scenario: Scenario) = scenario.Action.Invoke()

type PortResolverFeatureTests() =
    static member Scenarios() : seq<obj[]> =
        FeatureRunner.scenarios "port-resolver.feature" |> Seq.toList :> seq<_>

    [<Theory>]
    [<MemberData("Scenarios")>]
    member _.``Runtime listener port resolution``(scenario: Scenario) = scenario.Action.Invoke()
