/// TickSpec step definitions binding `ddd/ddd-bc.feature`'s 11 scenarios to
/// `RhinoCli.Application.Ddd`'s bounded-context registry validator
/// [Repo-grounded — `apps/rhino-cli/src/application/bcregistry.rs`,
/// `apps/rhino-cli/tests/ddd.rs`].
///
/// Every scenario builds a throwaway registry plus matching filesystem under a
/// temp directory and calls `validateBoundedContexts` in-process. The
/// `OSE_RHINO_DDD_SEVERITY` scenario feeds its value straight to
/// `resolveSeverity`'s `envVal` parameter rather than mutating the real
/// process environment — the same choice `tests/ddd.rs` makes, and the reason
/// its own doc comment gives: a real `set_var` is a cross-test data race.
module RhinoCli.Tests.Unit.Steps.DddSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Ddd

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type DddSteps() =
    let mutable repoRoot: string option = None
    let mutable envSeverity: string = ""
    let mutable output: string = ""
    let mutable exitOk: bool = true

    let root () : string =
        match repoRoot with
        | Some existing -> existing
        | None ->
            let created =
                Path.Combine(Path.GetTempPath(), "rhino-cli-ddd-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory created |> ignore
            repoRoot <- Some created
            created

    let write (rel: string) (content: string) : unit =
        let path = Path.Combine(root (), rel.Replace('/', Path.DirectorySeparatorChar))
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    let mkdir (rel: string) : unit =
        Directory.CreateDirectory(Path.Combine(root (), rel.Replace('/', Path.DirectorySeparatorChar)))
        |> ignore

    let codeDir (name: string) =
        sprintf "apps/organiclever-app-web/src/contexts/%s" name

    let glossaryPath (name: string) =
        sprintf "specs/apps/organiclever/ddd/glossary/%s.md" name

    let gherkinDir (name: string) =
        sprintf "specs/apps/organiclever/behavior/%s/gherkin" name

    /// One context entry, with `relationships` appended verbatim when given.
    let contextYaml (name: string) (layers: string list) (relationships: string) : string =
        sprintf
            "  - name: %s\n    summary: The %s context\n    layers: [%s]\n    code: [%s]\n    code_lang: [ts, tsx]\n    glossary: %s\n    gherkin: [%s]\n%s"
            name
            name
            (String.concat ", " layers)
            (codeDir name)
            (glossaryPath name)
            (gherkinDir name)
            relationships

    let writeRegistry (contexts: string list) : unit =
        write
            "specs/apps/organiclever/ddd/bounded-contexts.yaml"
            ("version: 2\napp: organiclever\ncontexts:\n" + String.concat "" contexts)

    /// Creates every filesystem artefact one context declares.
    let materialize (name: string) (layers: string list) : unit =
        for layer in layers do
            mkdir (sprintf "%s/%s" (codeDir name) layer)

        write (glossaryPath name) (sprintf "# %s glossary\n" name)
        write (sprintf "%s/%s.feature" (gherkinDir name) name) "Feature: Example\n"

    /// The clean single-context baseline every scenario starts from; later
    /// `Given` steps break exactly one part of it.
    let scaffoldJournal (layers: string list) : unit =
        writeRegistry [ contextYaml "journal" layers "" ]
        materialize "journal" layers

    let defaultLayers = [ "domain"; "application"; "infrastructure"; "presentation" ]

    let runBc (app: string) (severityFlag: string) : unit =
        let severity, _ = resolveSeverity severityFlag envSeverity

        match
            validateBoundedContexts
                { RepoRoot = root ()
                  App = app
                  Severity = Some severity }
        with
        | Ok findings ->
            let rendered, ok = renderDddFindings findings
            output <- rendered
            exitOk <- ok
        | Error message ->
            output <- message
            exitOk <- false

    // ---- Given ----

    [<Given>]
    member _.``a registry with one bounded context "journal" declaring layers "\[domain, application, infrastructure, presentation\]"``
        ()
        =
        scaffoldJournal defaultLayers

    [<Given>]
    member _.``a glossary file exists at the registered glossary path``() =
        write (glossaryPath "journal") "# journal glossary\n"

    [<Given>]
    member _.``a gherkin folder exists at the registered gherkin path containing at least one feature file``() =
        write (sprintf "%s/journal.feature" (gherkinDir "journal")) "Feature: Example\n"

    [<Given>]
    member _.``the code folder contains exactly the declared layer subfolders``() =
        for layer in defaultLayers do
            mkdir (sprintf "%s/%s" (codeDir "journal") layer)

    [<Given>]
    member _.``a registry that does not list a context named "phantom"``() = scaffoldJournal defaultLayers

    [<Given>]
    member _.``a folder "apps/organiclever-app-web/src/contexts/phantom/" exists on the filesystem``() =
        mkdir (codeDir "phantom")

    [<Given>]
    member _.``a registry listing context "journal" with a registered glossary path``() = scaffoldJournal defaultLayers

    [<Given>]
    member _.``the glossary file does not exist at that path``() =
        File.Delete(Path.Combine(root (), (glossaryPath "journal").Replace('/', Path.DirectorySeparatorChar)))

    [<Given>]
    member _.``a registry listing context "journal" with layers "\[domain, application, infrastructure, presentation\]"``
        ()
        =
        scaffoldJournal defaultLayers

    [<Given>]
    member _.``the code folder is missing the "infrastructure" subfolder``() =
        Directory.Delete(
            Path.Combine(
                root (),
                (sprintf "%s/infrastructure" (codeDir "journal")).Replace('/', Path.DirectorySeparatorChar)
            ),
            true
        )

    [<Given>]
    member _.``a registry listing context "journal" with layers "\[domain, application, presentation\]"``() =
        scaffoldJournal [ "domain"; "application"; "presentation" ]

    [<Given>]
    member _.``the code folder contains an extra "infrastructure" subfolder not declared in the registry``() =
        mkdir (sprintf "%s/infrastructure" (codeDir "journal"))

    [<Given>]
    member _.``a registry listing context "journal" with a registered gherkin path``() = scaffoldJournal defaultLayers

    [<Given>]
    member _.``the gherkin folder does not exist at that path``() =
        Directory.Delete(Path.Combine(root (), (gherkinDir "journal").Replace('/', Path.DirectorySeparatorChar)), true)

    [<Given>]
    member _.``the gherkin folder exists but contains no "\.feature" files``() =
        File.Delete(
            Path.Combine(
                root (),
                (sprintf "%s/journal.feature" (gherkinDir "journal")).Replace('/', Path.DirectorySeparatorChar)
            )
        )

    [<Given>]
    member _.``a registry where context "workout-session" declares a customer-supplier relationship to "journal" as customer``
        ()
        =
        writeRegistry
            [ contextYaml "journal" defaultLayers ""
              contextYaml
                  "workout-session"
                  defaultLayers
                  "    relationships:\n      - to: journal\n        kind: customer-supplier\n        role: customer\n" ]

        materialize "journal" defaultLayers
        materialize "workout-session" defaultLayers

    [<Given>]
    member _.``context "journal" declares no reciprocal relationship``() =
        // The registry the previous step wrote already omits it — this step
        // names the precondition rather than changing the fixture.
        ()

    [<Given>]
    member _.``a registry with an orphan code folder present on the filesystem``() =
        scaffoldJournal defaultLayers
        mkdir (codeDir "phantom")

    [<Given>]
    member _.``the environment variable "OSE_RHINO_DDD_SEVERITY" is set to "warn"``() = envSeverity <- "warn"

    // ---- When ----

    [<When>]
    member _.``the bounded-context validator runs for "([^"]+)"``(app: string) = runBc app ""

    [<When>]
    member _.``the bounded-context validator runs for "([^"]+)" with severity "([^"]+)"``
        (app: string, severity: string)
        =
        runBc app severity

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(exitOk, output)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.False(exitOk, output)

    [<Then>]
    member _.``no findings are printed to stdout``() = Assert.Equal("", output)

    [<Then>]
    member _.``the output mentions "([^"]+)"``(expected: string) =
        Assert.Contains(expected, output, StringComparison.Ordinal)

    [<Then>]
    member _.``the output mentions "not found" or "unknownapp"``() =
        Assert.True(output.Contains "not found" || output.Contains "unknownapp", output)

    [<Then>]
    member _.``the output contains the word "warning"``() =
        Assert.Contains("warn", output.ToLowerInvariant(), StringComparison.Ordinal)

module private FeatureRunner =

    let private featureDir: string =
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
                "ddd"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIdx =
            featureLines
            |> Array.findIndex (fun l -> l.Trim() = sprintf "Scenario: %s" scenarioTitle)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from `featureFileName`
    /// (a file inside `gherkin/ddd/`), bound against `DddSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(featureDir, featureFileName)
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<DddSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact(DisplayName = "Clean registry matches filesystem exactly — exits zero")>]
let ``Clean registry matches filesystem exactly`` () =
    FeatureRunner.run "ddd-bc.feature" "Clean registry matches filesystem exactly — exits zero"

[<Fact>]
let ``Orphan code folder not in registry is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Orphan code folder not in registry is flagged"

[<Fact>]
let ``Missing glossary file is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Missing glossary file is flagged"

[<Fact>]
let ``Missing layer subfolder is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Missing layer subfolder is flagged"

[<Fact>]
let ``Extra layer subfolder not in registry is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Extra layer subfolder not in registry is flagged"

[<Fact>]
let ``Missing gherkin folder is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Missing gherkin folder is flagged"

[<Fact>]
let ``Gherkin folder with no feature files is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Gherkin folder with no feature files is flagged"

[<Fact>]
let ``Relationship asymmetry is flagged`` () =
    FeatureRunner.run "ddd-bc.feature" "Relationship asymmetry is flagged"

[<Fact>]
let ``Severity warn flag downgrades findings to warnings and exits zero`` () =
    FeatureRunner.run "ddd-bc.feature" "Severity warn flag downgrades findings to warnings and exits zero"

[<Fact(DisplayName = "OSE_RHINO_DDD_SEVERITY env var overrides default severity")>]
let ``OSE RHINO DDD SEVERITY env var overrides default severity`` () =
    FeatureRunner.run "ddd-bc.feature" "OSE_RHINO_DDD_SEVERITY env var overrides default severity"

[<Fact>]
let ``Registry file not found for unknown app is an error`` () =
    FeatureRunner.run "ddd-bc.feature" "Registry file not found for unknown app is an error"
