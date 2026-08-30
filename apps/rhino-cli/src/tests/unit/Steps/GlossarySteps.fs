/// TickSpec step definitions binding `ddd/ddd-ul.feature`'s 7 scenarios to
/// `RhinoCli.Application.Glossary`'s ubiquitous-language validator
/// [Repo-grounded — `apps/rhino-cli/src/application/glossary.rs`,
/// `apps/rhino-cli/tests/ddd.rs`].
///
/// The Background builds one fully-valid context (`ctx-a`) with a registry,
/// source file, gherkin folder, and glossary; each scenario's `Given` then
/// breaks exactly one part of that baseline.
module RhinoCli.Tests.Unit.Steps.GlossarySteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Ddd
open RhinoCli.Application.Glossary

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism here.
type GlossarySteps() =
    let mutable repoRoot: string option = None
    let mutable app: string = "organiclever"
    let mutable glossaryPath: string = ""
    let mutable glossaryContent: string = ""
    let mutable output: string = ""
    let mutable exitOk: bool = true

    let root () : string =
        match repoRoot with
        | Some existing -> existing
        | None ->
            let created =
                Path.Combine(Path.GetTempPath(), "rhino-cli-ul-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory created |> ignore
            repoRoot <- Some created
            created

    let write (rel: string) (content: string) : unit =
        let path = Path.Combine(root (), rel.Replace('/', Path.DirectorySeparatorChar))
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    let mkdirs (rel: string) : unit =
        Directory.CreateDirectory(Path.Combine(root (), rel.Replace('/', Path.DirectorySeparatorChar)))
        |> ignore

    /// One `contexts:` entry, in the same shape the real registry uses.
    let contextYaml (name: string) (code: string) (glossary: string) (gherkin: string) : string =
        sprintf
            "  - name: %s\n    summary: fixture context\n    layers:\n      - domain\n    code:\n      - %s\n    code_lang: [ts]\n    glossary: %s\n    gherkin: %s\n    relationships: []\n"
            name
            code
            glossary
            gherkin

    let writeRegistry (contexts: string list) : unit =
        write
            (sprintf "specs/apps/%s/ddd/bounded-contexts.yaml" app)
            (sprintf "version: 2\napp: %s\ncontexts:\n" app + String.concat "" contexts)

    let validGlossaryContent () : string =
        "**Bounded context**: ctx-a\n\
**Maintainer**: tester\n\
**Last reviewed**: 2026-07-04\n\
\n\
## Terms\n\
\n\
| Term | Code identifier(s) | Used in features |\n\
|------|--------------------|------------------|\n\
| Foo  | `Foo`              | ctx-a.feature    |\n\
\n\
## Forbidden synonyms\n"

    /// Rewrites the baseline glossary through `transform`.
    let rewriteGlossary (transform: string -> string) : unit =
        let updated = transform glossaryContent
        write glossaryPath updated
        glossaryContent <- updated

    let runUl (targetApp: string) (severityFlag: string) : unit =
        app <- targetApp
        let severity, _ = resolveSeverity severityFlag ""

        match
            validateAll
                { RepoRoot = root ()
                  App = app
                  Severity = Some severity }
        with
        | Ok findings ->
            let rendered, ok = renderGlossaryFindings findings
            output <- rendered
            exitOk <- ok
        | Error message ->
            output <- message
            exitOk <- false

    // ---- Background ----

    [<Given>]
    member _.``the repository has a valid bounded-contexts\.yaml for "([\w-]+)"``(targetApp: string) =
        app <- targetApp
        let code = sprintf "apps/%s/src" app
        let glossary = sprintf "specs/apps/%s/ddd/glossary/ctx-a.md" app
        let gherkin = sprintf "specs/apps/%s/behavior/gherkin/ctx-a" app
        writeRegistry [ contextYaml "ctx-a" code glossary gherkin ]
        mkdirs (sprintf "%s/domain" code)
        write (sprintf "%s/domain/ctx-a.ts" code) "export const Foo = 1;\n"
        mkdirs gherkin
        write (sprintf "%s/ctx-a.feature" gherkin) "Feature: fixture\n"
        let content = validGlossaryContent ()
        write glossary content
        glossaryPath <- glossary
        glossaryContent <- content

    // ---- Given ----
    //
    // The four "everything is valid" Givens restate what the Background
    // already built, so each is deliberately a no-op.

    [<Given>]
    member _.``every registered glossary file has correct frontmatter keys``() = ()

    [<Given>]
    member _.``every terms table header is well-formed``() = ()

    [<Given>]
    member _.``every code identifier resolves in the BC code path``() = ()

    [<Given>]
    member _.``every feature reference resolves to an existing \.feature file``() = ()

    [<Given>]
    member _.``a glossary file is missing the "([\w ]+)" frontmatter key``(key: string) =
        let marker = sprintf "**%s**:" key

        rewriteGlossary (fun content ->
            content.Split('\n')
            |> Array.filter (fun line -> not (line.StartsWith(marker, StringComparison.Ordinal)))
            |> String.concat "\n")

    [<Given>]
    member _.``a glossary file has a terms table with a wrong column header``() =
        rewriteGlossary (fun content ->
            content.Replace("| Term | Code identifier(s) | Used in features |", "| Whatever | Wrong | Bad |"))

    [<Given>]
    member _.``a glossary file has a term with a code identifier not present in any source file``() =
        rewriteGlossary (fun content -> content.Replace("`Foo`", "`NonExistentSymbol`"))

    [<Given>]
    member _.``a glossary file has a term referencing a non-existent feature file``() =
        rewriteGlossary (fun content -> content.Replace("ctx-a.feature", "missing.feature"))

    [<Given>]
    member _.``two glossaries declare the same term without cross-linking via Forbidden synonyms``() =
        let entries =
            [ for name in [ "ctx-a"; "ctx-b" ] ->
                  let code = sprintf "apps/%s/src-%s" app name
                  let glossary = sprintf "specs/apps/%s/ddd/glossary/%s.md" app name
                  let gherkin = sprintf "specs/apps/%s/behavior/gherkin/%s" app name
                  mkdirs (sprintf "%s/domain" code)
                  write (sprintf "%s/domain/%s.ts" code name) "export const Foo = 1;\n"
                  mkdirs gherkin
                  write (sprintf "%s/%s.feature" gherkin name) "Feature: fixture\n"

                  write
                      glossary
                      (sprintf
                          "**Bounded context**: %s\n**Maintainer**: tester\n**Last reviewed**: 2026-07-04\n\n## Terms\n\n| Term | Code identifier(s) | Used in features |\n|------|--------------------|------------------|\n| Foo  | `Foo`              | %s.feature    |\n"
                          name
                          name)

                  contextYaml name code glossary gherkin ]

        writeRegistry entries

    // ---- When ----

    [<When>]
    member _.``the glossary validator runs for "([\w-]+)"``(targetApp: string) = runUl targetApp ""

    [<When>]
    member _.``the glossary validator runs for "([\w-]+)" with severity "(\w+)"``(targetApp: string, severity: string) =
        runUl targetApp severity

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(exitOk, output)

    [<Then>]
    member _.``the command exits with failure``() = Assert.False(exitOk, output)

    [<Then>]
    member _.``there are no findings in the output``() = Assert.Equal("", output.Trim())

    [<Then>]
    member _.``the output mentions "([^"]+)"``(expected: string) =
        Assert.Contains(expected, output, StringComparison.Ordinal)

    [<Then>]
    member _.``the output contains a warning``() =
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

    let private isBlockStart (line: string) : bool =
        let trimmed = line.Trim()

        trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
        || trimmed.StartsWith("Background:", StringComparison.Ordinal)
        || trimmed.StartsWith("@", StringComparison.Ordinal)

    /// Lines from `startIdx` up to (not including) the next block header.
    let private blockAt (lines: string[]) (startIdx: int) : string[] =
        let endIdx =
            lines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex isBlockStart
            |> Option.map (fun relative -> startIdx + 1 + relative)
            |> Option.defaultValue lines.Length

        lines.[startIdx .. endIdx - 1]

    /// Runs one scenario in isolation, prefixed by the feature's Background so
    /// TickSpec applies the same setup the real runner would.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(featureDir, featureFileName)
        let lines = File.ReadAllLines featurePath

        let featureLine =
            lines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let background =
            lines
            |> Array.tryFindIndex (fun l -> l.Trim() = "Background:")
            |> Option.map (blockAt lines)
            |> Option.defaultValue [||]

        let scenario =
            blockAt
                lines
                (lines
                 |> Array.findIndex (fun l -> l.Trim() = sprintf "Scenario: %s" scenarioTitle))

        let snippet = Array.concat [ [| featureLine; "" |]; background; [| "" |]; scenario ]

        let definitions = StepDefinitions([| typeof<GlossarySteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        Seq.exactlyOne(feature.Scenarios).Action.Invoke()

[<Fact(DisplayName = "All glossaries are valid — exits successfully with no findings")>]
let ``All glossaries are valid`` () =
    FeatureRunner.run "ddd-ul.feature" "All glossaries are valid — exits successfully with no findings"

[<Fact>]
let ``Glossary is missing a required frontmatter key`` () =
    FeatureRunner.run "ddd-ul.feature" "Glossary is missing a required frontmatter key"

[<Fact>]
let ``Terms table has a malformed header`` () =
    FeatureRunner.run "ddd-ul.feature" "Terms table has a malformed header"

[<Fact(DisplayName = "A code identifier is stale (not found in BC code path)")>]
let ``A code identifier is stale`` () =
    FeatureRunner.run "ddd-ul.feature" "A code identifier is stale (not found in BC code path)"

[<Fact(DisplayName = "A feature reference does not resolve to an existing .feature file")>]
let ``A feature reference does not resolve`` () =
    FeatureRunner.run "ddd-ul.feature" "A feature reference does not resolve to an existing .feature file"

[<Fact>]
let ``Same term appears in two glossaries without mutual Forbidden-synonyms cross-link`` () =
    FeatureRunner.run
        "ddd-ul.feature"
        "Same term appears in two glossaries without mutual Forbidden-synonyms cross-link"

[<Fact(DisplayName = "--severity=warn downgrades findings — exits successfully with warnings")>]
let ``severity warn downgrades findings`` () =
    FeatureRunner.run "ddd-ul.feature" "--severity=warn downgrades findings — exits successfully with warnings"
