/// TickSpec step definitions binding `docs-validate-frontmatter.feature`'s 11
/// scenarios to `RhinoCli.Application.Md.validateDocsFrontmatter` and
/// `docs-validate-heading-hierarchy.feature`'s 12 scenarios to
/// `RhinoCli.Application.Md.validateDocsHeadingHierarchy`/
/// `validateDocsHeadingHierarchyAllowlisted`
/// [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-frontmatter.feature`,
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-heading-hierarchy.feature`,
/// `apps/rhino-cli/src/application/docs/frontmatter.rs`,
/// `apps/rhino-cli/src/commands/md_validate_frontmatter.rs`,
/// `apps/rhino-cli/src/application/docs/heading_hierarchy.rs`,
/// `apps/rhino-cli/src/commands/md_validate_heading_hierarchy.rs`].
///
/// Follows `ConventionSteps.fs`'s/`TestCoverageSteps.fs`'s per-scenario
/// slicing convention: each xunit `[<Fact>]` below runs exactly one scenario,
/// extracted from the real, frozen feature file. `md` is not yet listed in
/// `FSHARP_NAMESPACES` (that flip is later, separate Wave D integration
/// work), so — matching `TestCoverageSteps.fs`'s own precedent for
/// `test-coverage validate` before its Wave C flip — every scenario below
/// calls one of `RhinoCli.Application.Md`'s validators directly with a path
/// list (or a repo root standing in for it) built by hand rather than
/// parsing an argv string. The heading-hierarchy scenarios that exercise the
/// prose allowlist (`docs`/`.claude`/`plans/done`/`specs`/`apps`/`libs`
/// trees) set the `useAllowlist` instance field from their `Given` step so
/// the single shared "the developer runs docs validate-heading-hierarchy"
/// `When` step — reused verbatim by both the plain-tree and the
/// allowlist-tree scenarios — knows which of the two validator entry points
/// to call.
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
    let mutable useAllowlist = false
    let mutable stagedFiles: string list = []

    let root () =
        match rootDir with
        | Some dir -> dir
        | None -> failwith "no repository root has been prepared by a Given step"

    /// Returns the scenario's shared temp-dir root, creating it on first
    /// use — lets a scenario with more than one `Given`/`And` fixture step
    /// (e.g. heading-hierarchy's "exclude-flag-suppresses-tree") write into
    /// the same tree instead of each step getting its own temp dir.
    let ensureRoot () =
        match rootDir with
        | Some dir -> dir
        | None ->
            let dir =
                Path.Combine(Path.GetTempPath(), "rhino-cli-md-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory(dir) |> ignore
            rootDir <- Some dir
            dir

    let theOutcome () : Result<Finding list, string> =
        outcome
        |> Option.defaultWith (fun () -> failwith "no command has been run by a When step")

    let theFindings () : Finding list =
        match theOutcome () with
        | Ok findings -> findings
        | Error message -> failwith (sprintf "expected the md validator to produce findings, got error: %s" message)

    let newTempDir () = ensureRoot ()

    let writeDoc (relativePath: string) (content: string) =
        let full = Path.Combine(ensureRoot (), relativePath)
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

    /// Substring unique to `analyzeHeadings`'s duplicate-H1 finding message
    /// (e.g. `"markdown file has 2 H1 headings (first at line 1); ..."`) —
    /// distinct from the missing-H1 message's "documented file must have
    /// exactly one H1" wording.
    let duplicateH1Needle = "H1 headings (first at line"

    /// Substring unique to `analyzeHeadings`'s skipped-level finding
    /// message.
    let skippedLevelNeedle = "heading levels must not skip"

    let assertHasBlockingFindingWithMessageAndPath (messageNeedle: string) =
        let findings = theFindings ()

        Assert.Contains(
            findings,
            fun (f: Finding) ->
                f.Severity = Severity.Blocking
                && f.Message.Contains(messageNeedle, StringComparison.Ordinal)
                && (f.Path |> Option.isSome)
        )

    let assertHasBlockingFindingInPathWithMessage (pathNeedle: string) (messageNeedle: string) =
        let findings = theFindings ()

        Assert.Contains(
            findings,
            fun (f: Finding) ->
                f.Severity = Severity.Blocking
                && f.Message.Contains(messageNeedle, StringComparison.Ordinal)
                && (f.Path |> Option.defaultValue "").Replace('\\', '/').Contains(pathNeedle, StringComparison.Ordinal)
        )

    let assertHasBlockingFindingInPath (pathNeedle: string) =
        let findings = theFindings ()

        Assert.Contains(
            findings,
            fun (f: Finding) ->
                f.Severity = Severity.Blocking
                && (f.Path |> Option.defaultValue "").Replace('\\', '/').Contains(pathNeedle, StringComparison.Ordinal)
        )

    let assertNoFindingInPath (pathNeedle: string) =
        let findings = theFindings ()

        Assert.DoesNotContain(
            findings,
            fun (f: Finding) ->
                (f.Path |> Option.defaultValue "").Replace('\\', '/').Contains(pathNeedle, StringComparison.Ordinal)
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

    // ---- Given (docs-validate-heading-hierarchy.feature) ----

    [<Given>]
    member _.``a documentation tree where every markdown file has exactly one H1 and no skipped heading levels``() =
        writeDoc "a.md" "# Title\n\n## Section\n\n### Sub\n\n## Section Two\n"
        writeDoc "sub/b.md" "# Other\n\n## X\n"

    [<Given>]
    member _.``a documentation tree containing a markdown file with two H1 headings``() =
        writeDoc "a.md" "# First\n\n# Second\n"

    [<Given>]
    member _.``a documentation tree containing a markdown file with an H2 followed directly by an H4``() =
        writeDoc "a.md" "## Two\n\n#### Four\n"

    [<Given>]
    member _.``a documentation tree containing a single-line markdown file with no headings``() =
        writeDoc "a.md" "just a single line\n"

    [<Given>]
    member _.``a docs directory containing a markdown file with two H1 headings``() =
        useAllowlist <- true
        writeDoc "docs/page.md" "# First\n\n# Second\n"

    [<Given>]
    member _.``a .claude/agents directory containing a markdown file with no H1 heading``() =
        useAllowlist <- true
        writeDoc ".claude/agents/my-agent.md" "## Not H1\n\n### Also not H1\n"

    [<Given>]
    member _.``a plans/done directory containing a markdown file with a skipped heading level``() =
        useAllowlist <- true
        writeDoc "plans/done/2024-01-01__old-plan/delivery.md" "# T\n\n### Skip\n"

    [<Given>]
    member _.``a repo-governance directory containing a markdown file with two H1 headings``() =
        useAllowlist <- true
        writeDoc "repo-governance/rule.md" "# X\n\n# Y\n"

    [<Given>]
    member _.``a specs directory containing a markdown file with two H1 headings``() =
        useAllowlist <- true
        writeDoc "specs/apps/foo/overview.md" "# A\n\n# B\n"

    [<Given>]
    member _.``an apps/example directory whose README.md contains a skipped heading level``() =
        useAllowlist <- true
        writeDoc "apps/example/README.md" "# App\n\n### Skip\n"

    [<Given>]
    member _.``an apps/example/src directory containing a markdown file with no H1 heading``() =
        useAllowlist <- true
        writeDoc "apps/example/src/notes.md" "## No H1\n"

    [<Given>]
    member _.``a libs/example/docs directory containing a markdown file with two H1 headings``() =
        useAllowlist <- true
        writeDoc "libs/example/docs/guide.md" "# A\n\n# B\n"

    // ---- Given (docs-validate-links.feature) ----

    [<Given>]
    member _.``markdown files where all internal links point to existing files``() =
        writeDoc "source.md" "See [destination](./destination.md) for details.\n"
        writeDoc "destination.md" "# Destination\n"

    [<Given>]
    member _.``a markdown file with a link pointing to a non-existent file``() =
        writeDoc "broken-source.md" "See [missing](./does-not-exist.md) for details.\n"

    [<Given>]
    member _.``a markdown file containing only external HTTPS links``() =
        writeDoc "external-only.md" "See [a](https://example.com) and [b](https://example.org/page).\n"

    [<Given>]
    member _.``a markdown file with a broken link that has not been staged in git``() =
        writeDoc "unstaged-broken.md" "See [missing](./does-not-exist.md) for details.\n"

    [<Given>]
    member _.``a markdown file under plans/done with a broken internal link``() =
        writeDoc "plans/done/2024-01-01__example/delivery.md" "See [missing](./does-not-exist.md).\n"

    [<Given>]
    member _.``a markdown file under docs with a different broken internal link``() =
        writeDoc "docs/reference/page.md" "See [missing](./also-missing.md).\n"

    [<Given>]
    member _.``a markdown file under libs with a broken internal link``() =
        writeDoc "libs/example/README.md" "See [missing](./does-not-exist.md).\n"

    [<Given>]
    member _.``a markdown file that links to an existing heading anchor in another file``() =
        writeDoc "anchor-source.md" "See [section](./anchor-doc.md#section).\n"
        writeDoc "anchor-doc.md" "# Title\n\n## Section\n"

    [<Given>]
    member _.``a markdown file that links to a non-existent heading anchor in an existing file``() =
        writeDoc "broken-anchor-source.md" "See [section](./broken-anchor-doc.md#missing).\n"
        writeDoc "broken-anchor-doc.md" "# Title\n"

    [<Given>]
    member _.``a markdown file containing a same-file anchor link that has no matching heading``() =
        writeDoc "same-file-anchor.md" "# Title\n\nSee [missing](#missing) below.\n"

    /// This scenario's Gherkin `Given` line reads (verbatim, from the frozen
    /// feature file): `a markdown file that links to the anchor
    /// "#snake_case" of a file whose heading is "snake_case"`. TickSpec's
    /// own Gherkin line-lexer treats `#` as a comment marker even inside a
    /// quoted string — unlike `rhino-cli specs behavior-coverage validate`'s
    /// Rust parser, which (correctly, per the Gherkin spec) only treats a
    /// `#` that *starts* a trimmed line as a comment — so by the time
    /// TickSpec tries to match a step against this line, everything from the
    /// `#` onward has already been stripped, leaving only `a markdown file
    /// that links to the anchor "` (a dangling, unterminated quote) as the
    /// text step matching actually sees at runtime — verified via the
    /// `[FAIL] Missing step definition` message that truncated text produced
    /// before this method's pattern covered it.
    ///
    /// Both `TickSpec` and `specs behavior-coverage validate` treat a
    /// backtick-quoted step name as a raw (unescaped) regex rather than a
    /// literal string — the existing `` a git index with "(.*)" staged ``
    /// step elsewhere in this file already relies on that. This method's
    /// name below exploits the same mechanism, spelling out a
    /// `(?:full|truncated)` alternation so ONE step pattern satisfies both
    /// checkers at once: `specs behavior-coverage validate` matches the
    /// first alternative against the frozen feature file's real,
    /// untruncated line (no "missing step" gap), while `TickSpec` matches
    /// the second alternative against the truncated text it actually
    /// presents at runtime (so the fixture body below really does run, and
    /// the step is not an "orphan" the coverage tool can only find via the
    /// first alternative).
    [<Given>]
    member _.``(?:a markdown file that links to the anchor "#snake_case" of a file whose heading is "snake_case"|a markdown file that links to the anchor ")``
        ()
        =
        writeDoc "snake-source.md" "See [snake](./snake-doc.md#snake_case).\n"
        writeDoc "snake-doc.md" "# snake_case\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs docs validate-frontmatter``() =
        outcome <- Some(validateDocsFrontmatter [ root () ])

    [<When>]
    member _.``the developer runs docs validate-heading-hierarchy``() =
        outcome <-
            Some(
                if useAllowlist then
                    Ok(validateDocsHeadingHierarchyAllowlisted (root ()) [])
                else
                    validateDocsHeadingHierarchy [ root () ]
            )

    [<When>]
    member _.``the developer runs docs validate-heading-hierarchy with --exclude docs``() =
        outcome <- Some(Ok(validateDocsHeadingHierarchyAllowlisted (root ()) [ "docs" ]))

    // ---- When (docs-validate-links.feature) ----

    [<When>]
    member _.``the developer runs docs validate-links``() =
        outcome <-
            Some(
                Ok(
                    validateDocsLinks
                        { RepoRoot = root ()
                          StagedFiles = None
                          ExcludePrefixes = [] }
                )
            )

    [<When>]
    member _.``the developer runs docs validate-links with the --staged-only flag``() =
        outcome <-
            Some(
                Ok(
                    validateDocsLinks
                        { RepoRoot = root ()
                          StagedFiles = Some stagedFiles
                          ExcludePrefixes = [] }
                )
            )

    [<When>]
    member _.``the developer runs docs validate-links with --exclude plans/done``() =
        outcome <-
            Some(
                Ok(
                    validateDocsLinks
                        { RepoRoot = root ()
                          StagedFiles = None
                          ExcludePrefixes = [ "plans/done" ] }
                )
            )

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() =
        match theOutcome () with
        | Ok findings ->
            Assert.False(
                findings |> List.exists (fun f -> f.Severity = Severity.Blocking),
                "expected no fail-level findings"
            )
        | Error message -> failwith (sprintf "expected the md command to succeed, got error: %s" message)

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

    // ---- Then (docs-validate-heading-hierarchy.feature) ----

    [<Then>]
    member _.``the output reports zero docs heading hierarchy findings``() = Assert.Empty(theFindings ())

    [<Then>]
    member _.``the output identifies the offending file and the duplicate H1 violation``() =
        assertHasBlockingFindingWithMessageAndPath duplicateH1Needle

    [<Then>]
    member _.``the output identifies the offending file and the skipped heading level``() =
        assertHasBlockingFindingWithMessageAndPath skippedLevelNeedle

    [<Then>]
    member _.``the output identifies the duplicate H1 violation in the docs file``() =
        assertHasBlockingFindingInPathWithMessage "/docs/" duplicateH1Needle

    [<Then>]
    member _.``the output does not mention the docs file``() = assertNoFindingInPath "/docs/"

    [<Then>]
    member _.``the output identifies the repo-governance file``() =
        assertHasBlockingFindingInPath "/repo-governance/"

    [<Then>]
    member _.``the output identifies the duplicate H1 violation in the specs file``() =
        assertHasBlockingFindingInPathWithMessage "/specs/" duplicateH1Needle

    [<Then>]
    member _.``the output identifies the skipped heading level in the app README``() =
        assertHasBlockingFindingInPathWithMessage "apps/example/README.md" skippedLevelNeedle

    [<Then>]
    member _.``the output identifies the duplicate H1 violation in the lib docs file``() =
        assertHasBlockingFindingInPathWithMessage "/libs/example/docs/" duplicateH1Needle

    // ---- Then (docs-validate-links.feature) ----

    [<Then>]
    member _.``the output reports no broken links found``() = Assert.Empty(theFindings ())

    [<Then>]
    member _.``the output identifies the file containing the broken link``() =
        assertHasBlockingFindingInPath "broken-source.md"

    [<Then>]
    member _.``the output does not mention the plans/done file``() = assertNoFindingInPath "plans/done"

    [<Then>]
    member _.``the output does mention the docs file``() =
        assertHasBlockingFindingInPath "docs/reference/page.md"

    [<Then>]
    member _.``the output identifies the libs file containing the broken link``() =
        assertHasBlockingFindingInPath "libs/example/README.md"

    [<Then>]
    member _.``the output identifies the broken anchor``() =
        assertHasBlockingFindingWithMessageAndPath "does not match any heading anchor"

    [<Then>]
    member _.``the output identifies the broken same-file anchor``() =
        assertHasBlockingFindingInPathWithMessage "same-file-anchor.md" "does not match any heading anchor in this file"

    [<AfterScenario>]
    member _.Cleanup() =
        match rootDir with
        | Some dir when Directory.Exists dir -> Directory.Delete(dir, true)
        | _ -> ()

/// Reads one named `Scenario:` block out of a real, frozen `*.feature` file
/// under the `md` Gherkin directory (leaving the file itself untouched) and
/// runs it through TickSpec bound only against `MdSteps` — see
/// `ConventionSteps.fs`'s `FeatureRunner` for why this is per-scenario
/// rather than per-file. Parameterised over the feature file name (rather
/// than one module per feature file) because `MdSteps` already binds more
/// than one feature file's scenarios; splitting this module per file would
/// duplicate `extractScenario`/`run` for no behavioral difference.
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
                "md"
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

    /// Runs the single scenario named `scenarioTitle` from `featureFileName`
    /// (a `*.feature` file under the `md` Gherkin directory), bound against
    /// `MdSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(featureDir, featureFileName)
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<MdSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Software-engineering doc with all required frontmatter fields passes`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with all required frontmatter fields passes"

[<Fact>]
let ``Software-engineering doc missing title fails`` () =
    FeatureRunner.run "docs-validate-frontmatter.feature" "Software-engineering doc missing title fails"

[<Fact>]
let ``Software-engineering doc missing category field fails`` () =
    FeatureRunner.run "docs-validate-frontmatter.feature" "Software-engineering doc missing category field fails"

[<Fact>]
let ``Software-engineering doc with category other than software fails`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with category other than software fails"

[<Fact>]
let ``Governance doc with only title fails once when_to_use and description are armed`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Governance doc with only title fails once when_to_use and description are armed"

[<Fact>]
let ``Governance doc with title, description, and when_to_use passes the lighter schema`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Governance doc with title, description, and when_to_use passes the lighter schema"

[<Fact>]
let ``Software-engineering doc with Diataxis tutorial category passes`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with Diataxis tutorial category passes"

[<Fact>]
let ``Software-engineering doc with Diataxis how-to category passes`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with Diataxis how-to category passes"

[<Fact>]
let ``Software-engineering doc with Diataxis reference category passes`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with Diataxis reference category passes"

[<Fact>]
let ``Software-engineering doc with Diataxis explanation category passes`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with Diataxis explanation category passes"

[<Fact>]
let ``Software-engineering doc with deprecated software category emits warn not fail`` () =
    FeatureRunner.run
        "docs-validate-frontmatter.feature"
        "Software-engineering doc with deprecated software category emits warn not fail"

[<Fact>]
let ``Tree where every .md has exactly one H1 and no skipped levels passes`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "Tree where every .md has exactly one H1 and no skipped levels passes"

[<Fact>]
let ``File with two H1 headings fails`` () =
    FeatureRunner.run "docs-validate-heading-hierarchy.feature" "File with two H1 headings fails"

[<Fact>]
let ``File with H2 followed directly by H4 (skipping H3) fails`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "File with H2 followed directly by H4 (skipping H3) fails"

[<Fact>]
let ``Single-line file with no headings is ignored (passes)`` () =
    FeatureRunner.run "docs-validate-heading-hierarchy.feature" "Single-line file with no headings is ignored (passes)"

[<Fact>]
let ``prose-allowlist-runs — docs file triggers a heading finding`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "prose-allowlist-runs — docs file triggers a heading finding"

[<Fact>]
let ``agent-skill-file-exempt — no finding for agent or skill files`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "agent-skill-file-exempt — no finding for agent or skill files"

[<Fact>]
let ``plans-done-excluded — no finding for plans/done files`` () =
    FeatureRunner.run "docs-validate-heading-hierarchy.feature" "plans-done-excluded — no finding for plans/done files"

[<Fact>]
let ``exclude-flag-suppresses-tree — --exclude docs suppresses docs findings`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "exclude-flag-suppresses-tree — --exclude docs suppresses docs findings"

[<Fact>]
let ``specs-allowlisted — specs tree triggers a heading finding`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "specs-allowlisted — specs tree triggers a heading finding"

[<Fact>]
let ``app-readme-allowlisted — project-root README triggers a heading finding`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "app-readme-allowlisted — project-root README triggers a heading finding"

[<Fact>]
let ``app-internals-default-deny — deep app files yield no finding`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "app-internals-default-deny — deep app files yield no finding"

[<Fact>]
let ``project-docs-subtree-allowlisted — app and lib docs trees trigger findings`` () =
    FeatureRunner.run
        "docs-validate-heading-hierarchy.feature"
        "project-docs-subtree-allowlisted — app and lib docs trees trigger findings"

[<Fact>]
let ``A document set with all valid internal links passes validation`` () =
    FeatureRunner.run "docs-validate-links.feature" "A document set with all valid internal links passes validation"

[<Fact>]
let ``A broken internal link is detected and reported`` () =
    FeatureRunner.run "docs-validate-links.feature" "A broken internal link is detected and reported"

[<Fact>]
let ``External URLs are not validated`` () =
    FeatureRunner.run "docs-validate-links.feature" "External URLs are not validated"

[<Fact>]
let ``With --staged-only only staged files are checked`` () =
    FeatureRunner.run "docs-validate-links.feature" "With --staged-only only staged files are checked"

[<Fact>]
let ``exclude flag skips the named subtree`` () =
    FeatureRunner.run "docs-validate-links.feature" "exclude flag skips the named subtree"

[<Fact>]
let ``repo-wide scan finds broken link outside original three-directory scope`` () =
    FeatureRunner.run
        "docs-validate-links.feature"
        "repo-wide scan finds broken link outside original three-directory scope"

[<Fact>]
let ``valid anchor link passes validation`` () =
    FeatureRunner.run "docs-validate-links.feature" "valid anchor link passes validation"

[<Fact>]
let ``broken anchor link produces a broken-anchor finding`` () =
    FeatureRunner.run "docs-validate-links.feature" "broken anchor link produces a broken-anchor finding"

[<Fact>]
let ``same-file anchor with no matching heading produces a broken-anchor finding`` () =
    FeatureRunner.run
        "docs-validate-links.feature"
        "same-file anchor with no matching heading produces a broken-anchor finding"

[<Fact>]
let ``anchor slugs keep underscores per the GitHub reference algorithm`` () =
    FeatureRunner.run "docs-validate-links.feature" "anchor slugs keep underscores per the GitHub reference algorithm"
