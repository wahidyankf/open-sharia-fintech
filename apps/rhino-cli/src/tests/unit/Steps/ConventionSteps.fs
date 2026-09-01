/// TickSpec step definitions binding the `convention` namespace's three
/// Gherkin feature files to `RhinoCli.Application.Convention`
/// [Repo-grounded —
/// `specs/apps/rhino/cli/behaviors/convention/convention-audit.feature`,
/// `.../repo-governance-emoji-audit.feature`,
/// `.../repo-governance-license-audit.feature`].
///
/// Each xunit `[<Fact>]` below runs exactly one scenario at a time: it slices
/// the single named scenario's lines out of the real, frozen feature file
/// (never rewriting or duplicating its wording) and hands that snippet to
/// `TickSpec.StepDefinitions.GenerateFeature`, so binding is per-scenario
/// rather than per-file — an unbound scenario elsewhere in the same feature
/// file cannot block a scenario whose steps are already implemented.
module RhinoCli.Tests.Unit.Steps.ConventionSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Convention

/// Instance step-definition container. TickSpec instantiates one fresh
/// instance per scenario invocation, so instance-level mutable fields are
/// the idiomatic way to thread state from Given through When to Then without
/// leaking it across scenarios or xunit test parallelism.
type ConventionSteps() =
    let mutable rootDir: string option = None
    let mutable targetPath: string option = None
    let mutable result: ValidatorResult option = None

    let root () =
        match rootDir with
        | Some dir -> dir
        | None -> failwith "no repository root has been prepared by a Given step"

    let target () =
        match targetPath with
        | Some path -> path
        | None -> failwith "no target path has been prepared by a Given step"

    let outcome () =
        match result with
        | Some r -> r
        | None -> failwith "no command has been run by a When step"

    let newTempDir () =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-convention-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        dir

    let writeFile (relativePath: string) (content: string) =
        let full = Path.Combine(root (), relativePath)
        Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
        File.WriteAllText(full, content)

    // ---- Given: repo-governance-emoji-audit.feature ----

    [<Given>]
    member _.``a source tree containing no emoji codepoints in forbidden file types``() =
        rootDir <- Some(newTempDir ())
        writeFile "clean.json" "{ \"label\": \"hello there\" }\n"
        targetPath <- rootDir

    [<Given>]
    member _.``a JSON file containing an emoji codepoint``() =
        rootDir <- Some(newTempDir ())
        writeFile "emoji.json" "{ \"label\": \"hi \u2705 there\" }\n"
        targetPath <- Some(Path.Combine(root (), "emoji.json"))

    [<Given>]
    member _.``a Go source file containing an emoji codepoint``() =
        rootDir <- Some(newTempDir ())
        writeFile "main.go" "package main\n\n// hi \u2705 there\n"
        targetPath <- Some(Path.Combine(root (), "main.go"))

    [<Given>]
    member _.``a forbidden file containing multibyte non-emoji unicode such as Arabic``() =
        rootDir <- Some(newTempDir ())
        writeFile "arabic.json" "{ \"label\": \"مرحبا\" }\n"
        targetPath <- Some(Path.Combine(root (), "arabic.json"))

    [<Given>]
    member _.``a source tree with an emoji-containing file inside the archived directory``() =
        rootDir <- Some(newTempDir ())
        writeFile "archived/old.json" "{ \"label\": \"hi \u2705 there\" }\n"
        targetPath <- rootDir

    [<Given>]
    member _.``a source tree with an emoji-containing agent skill source file``() =
        rootDir <- Some(newTempDir ())
        writeFile ".claude/skills/sample/SKILL.md" "# Sample skill \u2705\n"
        targetPath <- rootDir

    // ---- Given: repo-governance-license-audit.feature ----

    [<Given>]
    member _.``a repository where every required directory has a matching MIT LICENSE file``() =
        rootDir <- Some(newTempDir ())
        writeFile "apps/foo/LICENSE" "MIT License\n"
        writeFile "libs/bar/LICENSE" "MIT License\n"
        writeFile "specs/LICENSE" "MIT License\n"

    [<Given>]
    member _.``a repository where one app directory is missing its LICENSE file``() =
        rootDir <- Some(newTempDir ())
        Directory.CreateDirectory(Path.Combine(root (), "apps", "foo")) |> ignore

    [<Given>]
    member _.``a repository where one lib directory is missing its LICENSE file``() =
        rootDir <- Some(newTempDir ())
        Directory.CreateDirectory(Path.Combine(root (), "libs", "bar")) |> ignore

    [<Given>]
    member _.``a repository where a LICENSING-NOTICE.md table row claims a license that disagrees with the on-disk LICENSE file``
        ()
        =
        rootDir <- Some(newTempDir ())
        writeFile "apps/foo/LICENSE" "MIT License\n"

        writeFile "LICENSING-NOTICE.md" "# Notice\n\n| Path | License |\n| --- | --- |\n| apps/foo | Apache-2.0 |\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs convention emoji validate on the tree``() =
        result <- Some(runEmojiValidate [ target () ])

    [<When>]
    member _.``the developer runs convention emoji validate on the file``() =
        result <- Some(runEmojiValidate [ target () ])

    [<When>]
    member _.``the developer runs convention license validate``() =
        result <- Some(runLicenseValidate (root ()))

    [<When>]
    member _.``the developer runs "rhino-cli convention audit"``() =
        result <- Some(runConventionAudit (root ()) [])

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() =
        let r = outcome ()
        Assert.True(r.Success, sprintf "expected success, got output:\n%s" r.Output)

    [<Then>]
    member _.``the command exits with a failure code``() =
        let r = outcome ()
        Assert.False(r.Success, sprintf "expected failure, got output:\n%s" r.Output)

    [<Then>]
    member _.``the output reports zero emoji findings``() = Assert.Empty((outcome ()).Findings)

    [<Then>]
    member _.``the output identifies the offending file line and codepoint``() =
        let r = outcome ()
        Assert.NotEmpty(r.Findings)
        let finding = List.head r.Findings
        Assert.Contains("U+", finding.Message)
        Assert.Contains(finding.Message, r.Output)

    [<Then>]
    member _.``the output reports zero license findings``() = Assert.Empty((outcome ()).Findings)

    [<Then>]
    member _.``the output identifies the missing LICENSE app directory``() =
        let r = outcome ()

        Assert.Contains(
            r.Findings,
            fun (f: RhinoCli.Domain.Types.Finding) -> f.Message.Contains("missing-license") && f.Path = Some "apps/foo"
        )

    [<Then>]
    member _.``the output identifies the missing LICENSE lib directory``() =
        let r = outcome ()

        Assert.Contains(
            r.Findings,
            fun (f: RhinoCli.Domain.Types.Finding) -> f.Message.Contains("missing-license") && f.Path = Some "libs/bar"
        )

    [<Then>]
    member _.``the output identifies the SPDX mismatch``() =
        let r = outcome ()

        Assert.Contains(r.Findings, fun (f: RhinoCli.Domain.Types.Finding) -> f.Message.Contains("spdx-mismatch"))

    [<Then>]
    member _.``the output names the failing "(.*)" validator``(name: string) =
        let r = outcome ()
        Assert.Contains(sprintf "%s:" name, r.Output)

    [<AfterScenario>]
    member _.Cleanup() =
        match rootDir with
        | Some dir when Directory.Exists dir -> Directory.Delete(dir, true)
        | _ -> ()

/// Reads one named `Scenario:` block out of a real, frozen feature file
/// (leaving the file itself untouched) and runs it through TickSpec bound
/// only against `ConventionSteps` — see the module doc comment for why this
/// is per-scenario rather than per-file.
module private FeatureRunner =

    let private specsRoot: string =
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
                "convention"
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
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from `featureFileName`
    /// (a file name under the `convention` Gherkin directory), bound against
    /// `ConventionSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(specsRoot, featureFileName)
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<ConventionSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

// ---- convention-audit.feature ----

[<Fact>]
let ``A missing LICENSE fails the aggregate convention audit`` () =
    FeatureRunner.run "convention-audit.feature" "A missing LICENSE fails the aggregate convention audit"

// ---- repo-governance-license-audit.feature ----

[<Fact>]
let ``Clean repository where every app/lib/specs has matching LICENSE passes`` () =
    FeatureRunner.run
        "repo-governance-license-audit.feature"
        "Clean repository where every app/lib/specs has matching LICENSE passes"

[<Fact>]
let ``App directory missing LICENSE file fails`` () =
    FeatureRunner.run "repo-governance-license-audit.feature" "App directory missing LICENSE file fails"

[<Fact>]
let ``Lib directory missing LICENSE file fails`` () =
    FeatureRunner.run "repo-governance-license-audit.feature" "Lib directory missing LICENSE file fails"

[<Fact>]
let ``LICENSING-NOTICE.md table row mismatching SPDX in LICENSE fails`` () =
    FeatureRunner.run
        "repo-governance-license-audit.feature"
        "LICENSING-NOTICE.md table row mismatching SPDX in LICENSE fails"

// ---- repo-governance-emoji-audit.feature ----

[<Fact>]
let ``Clean source tree passes`` () =
    FeatureRunner.run "repo-governance-emoji-audit.feature" "Clean source tree passes"

[<Fact>]
let ``Emoji codepoint in a JSON file fails`` () =
    FeatureRunner.run "repo-governance-emoji-audit.feature" "Emoji codepoint in a JSON file fails"

[<Fact>]
let ``Emoji codepoint in a Go source file fails`` () =
    FeatureRunner.run "repo-governance-emoji-audit.feature" "Emoji codepoint in a Go source file fails"

[<Fact>]
let ``Multibyte non-emoji unicode does not trigger a finding`` () =
    FeatureRunner.run "repo-governance-emoji-audit.feature" "Multibyte non-emoji unicode does not trigger a finding"

[<Fact>]
let ``emoji-audit skips archived directory`` () =
    FeatureRunner.run "repo-governance-emoji-audit.feature" "emoji-audit skips archived directory"

[<Fact>]
let ``emoji-audit skips policy-permitted agent skill files`` () =
    FeatureRunner.run "repo-governance-emoji-audit.feature" "emoji-audit skips policy-permitted agent skill files"
