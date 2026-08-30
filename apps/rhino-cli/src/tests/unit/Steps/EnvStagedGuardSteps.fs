/// TickSpec step definitions binding `specs/env-staged-guard.feature`'s 3
/// scenarios (the third a `Scenario Outline` with 6 `Examples` rows) to
/// `RhinoCli.Application.Env`'s `env staged-guard validate` port
/// [Repo-grounded — `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/env-staged-guard.feature`,
/// `apps/rhino-cli/src/commands/env_staged_guard.rs`]. Relocated into Wave B
/// from a mis-scheduled Wave E slot — see `Env.fs`'s module doc comment.
///
/// The scenarios describe "a real .env file is staged for commit" /
/// "a git index with staged", but — same as `env_staged_guard.rs`'s own unit
/// tests, which call `run_with_staged_files` directly rather than shelling
/// to a real git repository — these steps drive `checkStagedFiles` with a
/// literal staged-file list, never a real git fixture. No step here shells
/// out to `git`, so the Git Fixture Isolation Convention this wave's header
/// otherwise requires does not apply to this file.
module RhinoCli.Tests.Unit.Steps.EnvStagedGuardSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Env

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type EnvStagedGuardSteps() =
    let mutable stagedFiles: string list = []
    let mutable offending: string list option = None

    let runCheck () =
        offending <- Some(checkStagedFiles stagedFiles)

    let outcome () : string list =
        match offending with
        | Some o -> o
        | None -> failwith "no command has been run by a When step"

    // ---- Given ----

    [<Given>]
    member _.``a real .env file is staged for commit``() = stagedFiles <- [ ".env" ]

    [<Given>]
    member _.``only .env.example is staged for commit``() = stagedFiles <- [ ".env.example" ]

    [<Given>]
    member _.``a git index with "(.*)" staged``(file: string) = stagedFiles <- [ file ]

    // ---- When ----

    [<When>]
    member _.``the pre-commit hook runs rhino-cli env staged-guard validate``() = runCheck ()

    [<When>]
    member _.``"rhino-cli env staged-guard validate" runs``() = runCheck ()

    // ---- Then ----

    [<Then>]
    member _.``it exits non-zero and names the offending file``() =
        let result = outcome ()
        Assert.NotEmpty(result)
        Assert.Contains(".env", result)

    [<Then>]
    member _.``the commit is aborted``() = Assert.NotEmpty(outcome ())

    [<Then>]
    member _.``it exits zero and does not block the commit``() = Assert.Empty(outcome ())

    [<Then>]
    member _.``the command exits non-zero``() = Assert.NotEmpty(outcome ())

    [<Then>]
    member _.``the output names "(.*)" as offending``(file: string) = Assert.Contains(file, outcome ())

/// Reads one named `Scenario:`/`Scenario Outline:` block out of the real,
/// frozen `specs/env-staged-guard.feature` file (leaving the file itself
/// untouched) and runs it through TickSpec bound only against
/// `EnvStagedGuardSteps` — see `EnvSteps.fs`'s `FeatureRunner` for why this
/// is per-scenario rather than per-file.
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
                "behavior",
                "rhino-cli",
                "gherkin",
                "specs",
                "env-staged-guard.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIdx =
            featureLines
            |> Array.findIndex (fun l ->
                let trimmed = l.Trim()

                trimmed = sprintf "Scenario: %s" scenarioTitle
                || trimmed = sprintf "Scenario Outline: %s" scenarioTitle)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal)
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs every generated sub-scenario for `scenarioTitle` from
    /// `specs/env-staged-guard.feature`, bound against `EnvStagedGuardSteps`.
    /// A plain `Scenario:` generates exactly one; a `Scenario Outline:`
    /// generates one per `Examples:` row — this runs all of them, since the
    /// plan's "one Gherkin scenario per behavior cycle" counting treats a
    /// whole outline as a single scenario.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<EnvStagedGuardSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)

        for scenario in feature.Scenarios do
            scenario.Action.Invoke()

[<Fact>]
let ``Committing a real .env file is rejected`` () =
    FeatureRunner.run "Committing a real .env file is rejected"

[<Fact>]
let ``Staging .env.example is allowed`` () =
    FeatureRunner.run "Staging .env.example is allowed"

[<Fact>]
let ``Staging any real env file is rejected at commit time`` () =
    FeatureRunner.run "Staging any real env file is rejected at commit time"
