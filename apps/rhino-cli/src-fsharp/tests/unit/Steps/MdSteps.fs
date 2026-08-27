/// TickSpec step definitions binding
/// `docs-validate-frontmatter.feature`'s 11 scenarios to
/// `RhinoCli.Application.Md.validateDocsFrontmatter`
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-frontmatter.feature`,
/// `apps/rhino-cli/src/application/docs/frontmatter.rs`,
/// `apps/rhino-cli/src/commands/md_validate_frontmatter.rs`].
///
/// Follows `ConventionSteps.fs`'s/`TestCoverageSteps.fs`'s per-scenario
/// slicing convention: each xunit `[<Fact>]` below runs exactly one scenario,
/// extracted from the real, frozen feature file. `md` is not yet listed in
/// `FSHARP_NAMESPACES` (that flip is later, separate Wave D integration
/// work), so — matching `TestCoverageSteps.fs`'s own precedent for
/// `test-coverage validate` before its Wave C flip — every scenario below
/// calls `RhinoCli.Application.Md.validateDocsFrontmatter` directly with a
/// path list built by hand rather than parsing an argv string.
module RhinoCli.Tests.Unit.Steps.MdSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Md
open RhinoCli.Domain.Types

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type MdSteps() =
    let mutable rootDir: string option = None
    let mutable outcome: Result<Finding list, string> option = None

    let root () =
        match rootDir with
        | Some dir -> dir
        | None -> failwith "no repository root has been prepared by a Given step"

    let theOutcome () : Result<Finding list, string> =
        outcome
        |> Option.defaultWith (fun () -> failwith "no command has been run by a When step")

    let theFindings () : Finding list =
        match theOutcome () with
        | Ok findings -> findings
        | Error message ->
            failwith (sprintf "expected docs validate-frontmatter to produce findings, got error: %s" message)

    let newTempDir () =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-md-frontmatter-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        dir

    let writeDoc (relativePath: string) (content: string) =
        let full = Path.Combine(root (), relativePath)
        Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
        File.WriteAllText(full, content)

    let assertHasBlockingFindingContaining (needle: string) =
        let findings = theFindings ()

        Assert.Contains(
            findings,
            fun (f: Finding) ->
                f.Severity = Severity.Blocking
                && f.Message.Contains(needle, StringComparison.Ordinal)
        )

    // ---- Given ----

    [<Given>]
    member _.``a software-engineering doc with title, description, category, subcategory, and tags frontmatter``() =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: explanation\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc whose frontmatter omits the title field``() =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ndescription: D\ncategory: explanation\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc whose frontmatter omits the category field``() =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc whose frontmatter declares category as something other than software``() =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: random\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a governance doc carrying only a title frontmatter field``() =
        rootDir <- Some(newTempDir ())
        writeDoc "repo-governance/conventions/foo.md" "---\ntitle: T\n---\nbody\n"

    [<Given>]
    member _.``a governance doc with title, description, and when_to_use frontmatter``() =
        rootDir <- Some(newTempDir ())

        writeDoc
            "repo-governance/conventions/foo.md"
            "---\ntitle: T\ndescription: D\nwhen_to_use: Use when W.\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc with title, description, category tutorial, subcategory, and tags frontmatter``
        ()
        =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: tutorial\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc with title, description, category how-to, subcategory, and tags frontmatter``
        ()
        =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: how-to\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc with title, description, category reference, subcategory, and tags frontmatter``
        ()
        =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: reference\nsubcategory: S\ntags: [a]\n---\nbody\n"

    [<Given>]
    member _.``a software-engineering doc with title, description, category explanation, subcategory, and tags frontmatter``
        ()
        =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: explanation\nsubcategory: S\ntags: [a]\n---\nbody\n"

    /// The deprecated `category: software` value is itself the "all required
    /// frontmatter fields" fixture this scenario needs — every required
    /// field is present, `category` is merely the deprecated-but-recognised
    /// value, matching `frontmatter.rs::tests::software_deprecated_category_emits_warn`.
    [<Given>]
    member _.``a software-engineering doc with all required frontmatter fields``() =
        rootDir <- Some(newTempDir ())

        writeDoc
            "docs/explanation/software-engineering/foo.md"
            "---\ntitle: T\ndescription: D\ncategory: software\nsubcategory: S\ntags: [a]\n---\nbody\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs docs validate-frontmatter``() =
        outcome <- Some(validateDocsFrontmatter [ root () ])

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() =
        match theOutcome () with
        | Ok findings ->
            Assert.False(
                findings |> List.exists (fun f -> f.Severity = Severity.Blocking),
                "expected no fail-level findings"
            )
        | Error message -> failwith (sprintf "expected docs validate-frontmatter to succeed, got error: %s" message)

    [<Then>]
    member _.``the command exits with a failure code``() =
        match theOutcome () with
        | Ok findings ->
            Assert.True(
                findings |> List.exists (fun f -> f.Severity = Severity.Blocking),
                "expected at least one fail-level finding"
            )
        | Error _ -> ()

    [<Then>]
    member _.``the frontmatter output reports zero fail-level findings``() =
        let failFindings =
            theFindings () |> List.filter (fun f -> f.Severity = Severity.Blocking)

        Assert.Empty(failFindings)

    [<Then>]
    member _.``the frontmatter output identifies the missing title field``() =
        assertHasBlockingFindingContaining "\"title\" is missing"

    [<Then>]
    member _.``the frontmatter output identifies the missing category field``() =
        assertHasBlockingFindingContaining "\"category\" is missing"

    [<Then>]
    member _.``the frontmatter output identifies the wrong category value``() =
        assertHasBlockingFindingContaining "must be one of: tutorial, how-to, reference, explanation"

    [<Then>]
    member _.``the frontmatter output identifies the missing when-to-use field``() =
        assertHasBlockingFindingContaining "\"when_to_use\" is missing"

    [<Then>]
    member _.``the frontmatter output identifies the missing description field``() =
        assertHasBlockingFindingContaining "\"description\" is missing"

    [<AfterScenario>]
    member _.Cleanup() =
        match rootDir with
        | Some dir when Directory.Exists dir -> Directory.Delete(dir, true)
        | _ -> ()

/// Reads one named `Scenario:` block out of the real, frozen
/// `docs-validate-frontmatter.feature` file (leaving the file itself
/// untouched) and runs it through TickSpec bound only against `MdSteps` —
/// see `ConventionSteps.fs`'s `FeatureRunner` for why this is per-scenario
/// rather than per-file.
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
                "md",
                "docs-validate-frontmatter.feature"
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
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from
    /// `docs-validate-frontmatter.feature`, bound against `MdSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<MdSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Software-engineering doc with all required frontmatter fields passes`` () =
    FeatureRunner.run "Software-engineering doc with all required frontmatter fields passes"

[<Fact>]
let ``Software-engineering doc missing title fails`` () =
    FeatureRunner.run "Software-engineering doc missing title fails"

[<Fact>]
let ``Software-engineering doc missing category field fails`` () =
    FeatureRunner.run "Software-engineering doc missing category field fails"

[<Fact>]
let ``Software-engineering doc with category other than software fails`` () =
    FeatureRunner.run "Software-engineering doc with category other than software fails"

[<Fact>]
let ``Governance doc with only title fails once when_to_use and description are armed`` () =
    FeatureRunner.run "Governance doc with only title fails once when_to_use and description are armed"

[<Fact>]
let ``Governance doc with title, description, and when_to_use passes the lighter schema`` () =
    FeatureRunner.run "Governance doc with title, description, and when_to_use passes the lighter schema"

[<Fact>]
let ``Software-engineering doc with Diataxis tutorial category passes`` () =
    FeatureRunner.run "Software-engineering doc with Diataxis tutorial category passes"

[<Fact>]
let ``Software-engineering doc with Diataxis how-to category passes`` () =
    FeatureRunner.run "Software-engineering doc with Diataxis how-to category passes"

[<Fact>]
let ``Software-engineering doc with Diataxis reference category passes`` () =
    FeatureRunner.run "Software-engineering doc with Diataxis reference category passes"

[<Fact>]
let ``Software-engineering doc with Diataxis explanation category passes`` () =
    FeatureRunner.run "Software-engineering doc with Diataxis explanation category passes"

[<Fact>]
let ``Software-engineering doc with deprecated software category emits warn not fail`` () =
    FeatureRunner.run "Software-engineering doc with deprecated software category emits warn not fail"
