/// TickSpec step definitions binding `env-init.feature`'s 4 scenarios to
/// `RhinoCli.Application.Env`'s `env init` port [Repo-grounded —
/// `specs/apps/rhino/cli/behaviors/env/env-init.feature`,
/// `apps/rhino-cli/src/commands/env_init.rs`].
///
/// Follows `EnvSteps.fs`'s per-scenario slicing convention: each xunit
/// `[<Fact>]` below runs exactly one scenario, extracted from the real,
/// frozen feature file rather than a duplicated/rewritten copy of its
/// wording. Kept as its own file (rather than added to `EnvSteps.fs`) since
/// `env-init.feature` is its own PR-sized slice of the `env` namespace, same
/// as `env-backup.feature` was.
module RhinoCli.Tests.Unit.Steps.EnvInitSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Env

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type EnvInitSteps() =
    let mutable repoRoot: string option = None
    let mutable forceFlag = false
    let mutable result: EnvInitResult option = None
    let mutable ownedDirs: string list = []

    let newTempDir (prefix: string) : string =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-env-init-" + prefix + "-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        ownedDirs <- dir :: ownedDirs
        dir

    let writeFile (root: string) (relativePath: string) (content: string) =
        let full = Path.Combine(root, relativePath)
        Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
        File.WriteAllText(full, content)

    let ensureRoot () : string =
        match repoRoot with
        | Some dir -> dir
        | None ->
            let dir = newTempDir "repo"
            repoRoot <- Some dir
            dir

    let root () : string =
        match repoRoot with
        | Some dir -> dir
        | None -> failwith "no repository root has been prepared by a Given step"

    let outcome () : EnvInitResult =
        match result with
        | Some r -> r
        | None -> failwith "no command has been run by a When step"

    let runEnvInitStep () =
        result <- Some(runEnvInit (root ()) forceFlag)

    // ---- Given ----

    [<Given>]
    member _.``.env.example files exist in infra/dev but no .env.local files``() =
        let dir = ensureRoot ()
        writeFile dir "infra/dev/organiclever/.env.example" "organiclever=1"
        writeFile dir "infra/dev/ose-be/.env.example" "ose-be=1"

    [<Given>]
    member _.``.env.example files exist in infra/dev and some .env.local files already exist``() =
        let dir = ensureRoot ()
        writeFile dir "infra/dev/organiclever/.env.example" "organiclever=1"
        writeFile dir "infra/dev/ose-be/.env.example" "ose-be=1"
        writeFile dir "infra/dev/ose-be/.env.local" "pre-existing=1"

    [<Given>]
    member _.``no .env.example files exist in infra/dev``() =
        let dir = ensureRoot ()
        writeFile dir "infra/dev/.gitkeep" ""

    // ---- When ----

    [<When>]
    member _.``the developer runs env init``() = runEnvInitStep ()

    [<When>]
    member _.``the developer runs env init with the force flag``() =
        forceFlag <- true
        runEnvInitStep ()

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = outcome () |> ignore

    [<Then>]
    member _.``.env.local files are created from each .env.example``() =
        Assert.True(File.Exists(Path.Combine(root (), "infra/dev/organiclever/.env.local")))
        Assert.True(File.Exists(Path.Combine(root (), "infra/dev/ose-be/.env.local")))

    [<Then>]
    member _.``no bare .env file is created``() =
        Assert.False(File.Exists(Path.Combine(root (), "infra/dev/organiclever/.env")))
        Assert.False(File.Exists(Path.Combine(root (), "infra/dev/ose-be/.env")))

    [<Then>]
    member _.``the output lists each created file``() =
        let text = formatEnvInitText (outcome ())
        Assert.Contains("Created:", text)

    [<Then>]
    member _.``existing .env.local files are not overwritten``() =
        Assert.Equal("pre-existing=1", File.ReadAllText(Path.Combine(root (), "infra/dev/ose-be/.env.local")))

    [<Then>]
    member _.``the output shows skipped files``() =
        let text = formatEnvInitText (outcome ())
        Assert.Contains("Skipped:", text)

    [<Then>]
    member _.``all .env.local files are created or overwritten``() =
        Assert.True(File.Exists(Path.Combine(root (), "infra/dev/organiclever/.env.local")))
        Assert.Equal("ose-be=1", File.ReadAllText(Path.Combine(root (), "infra/dev/ose-be/.env.local")))

    [<Then>]
    member _.``the output reports zero files created``() =
        let r = outcome ()
        Assert.Equal(0, r.Created)
        Assert.Contains("Summary: 0 created", formatEnvInitText r)

    [<AfterScenario>]
    member _.Cleanup() =
        for dir in ownedDirs do
            if Directory.Exists dir then
                Directory.Delete(dir, true)

/// Reads one named `Scenario:` block out of the real, frozen `env-init.feature`
/// file (leaving the file itself untouched) and runs it through TickSpec
/// bound only against `EnvInitSteps` — see `EnvSteps.fs`'s `FeatureRunner`
/// for why this is per-scenario rather than per-file.
module private FeatureRunner =

    let private featurePath: string =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "cli",
                "behaviors",
                "env",
                "env-init.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let scenarioHeader = sprintf "Scenario: %s" scenarioTitle

        let startIdx = featureLines |> Array.findIndex (fun l -> l.Trim() = scenarioHeader)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal)
                // env-init.feature tags every scenario with a leading `@tag`
                // line, same as env-backup.feature — the next scenario's tag
                // line must also end the slice, or it gets pulled in as a
                // dangling trailing line with no scenario body to attach to.
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from `env-init.feature`,
    /// bound against `EnvInitSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<EnvInitSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Bootstrap env files from examples`` () =
    FeatureRunner.run "Bootstrap env files from examples"

[<Fact>]
let ``Skip existing env files`` () =
    FeatureRunner.run "Skip existing env files"

[<Fact>]
let ``Force overwrite existing env files`` () =
    FeatureRunner.run "Force overwrite existing env files"

[<Fact>]
let ``No env.example files found`` () =
    FeatureRunner.run "No env.example files found"
