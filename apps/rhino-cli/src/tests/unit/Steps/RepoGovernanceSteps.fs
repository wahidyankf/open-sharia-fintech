/// TickSpec step definitions binding the `repo-governance/` feature files to
/// `RhinoCli.Application.RepoGovernance`
/// [Repo-grounded — `apps/rhino-cli/src/application/repo_governance/`].
///
/// Every scenario builds a throwaway governance tree under a temp directory
/// and drives the audit functions directly, the same way the Rust modules'
/// own unit tests do — no scenario shells out to `git` or to the CLI.
module RhinoCli.Tests.Unit.Steps.RepoGovernanceSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.RepoGovernance

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type RepoGovernanceSteps() =
    let mutable repoRoot: string option = None
    let mutable layerFindings: LayerCoherenceFinding list = []
    let mutable traceFindings: TraceabilityFinding list = []
    let mutable vendorFindings: VendorFinding list = []
    let mutable vendorTarget: string option = None
    let mutable auditRunner: (string -> AuditOptions -> AuditFinding list) option = None
    let mutable auditEnvelope: AuditEnvelope option = None
    let mutable auditJsonRuns: string list = []
    let mutable auditSuppressedKey: string = ""
    let mutable output: string = ""
    let mutable exitCode: int = 0

    let root () : string =
        match repoRoot with
        | Some existing -> existing
        | None ->
            let created =
                Path.Combine(Path.GetTempPath(), "rhino-cli-repogov-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory created |> ignore
            repoRoot <- Some created
            created

    /// Writes both governance index documents from `## Layer N: Name (…)`
    /// heading lines, the declaration form the audit's heading regex reads.
    let writeGovernanceDocs (archLayers: (int * string) list) (readmeLayers: (int * string) list) =
        let render (layers: (int * string) list) =
            layers
            |> List.map (fun (number, name) ->
                sprintf "## Layer %d: %s (the %s layer)" number name (name.ToLowerInvariant()))
            |> String.concat "\n\n"
            |> fun body -> "# Governance\n\n" + body + "\n"

        let dir = Path.Combine(root (), "repo-governance")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, "repository-governance-architecture.md"), render archLayers)
        File.WriteAllText(Path.Combine(dir, "README.md"), render readmeLayers)

    /// Writes `content` at `repo-governance/<rel>` under the fixture root.
    let writeDoc (rel: string) (content: string) : unit =
        let path =
            Path.Combine(root (), "repo-governance", rel.Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    /// Writes one governance Markdown file and records it as the vendor
    /// audit's target.
    let writeVendorFile (content: string) : unit =
        let dir = Path.Combine(root (), "repo-governance")
        Directory.CreateDirectory dir |> ignore
        let path = Path.Combine(dir, "doc.md")
        File.WriteAllText(path, content)
        vendorTarget <- Some path

    /// Builds an injected category runner from a per-category finding table,
    /// so a scenario can state a category's outcome without a fixture tree.
    let fixedRunner (table: (string * AuditFinding list) list) =
        fun (name: string) (_: AuditOptions) ->
            table
            |> List.tryFind (fun (key, _) -> key = name)
            |> Option.map snd
            |> Option.defaultValue []

    /// A finding with a caller-chosen key, the one field suppression matches on.
    let auditFindingWithKey (key: string) (file: string) (message: string) : AuditFinding =
        { Key = key
          Severity = "high"
          Criticality = "HIGH"
          File = file
          Line = 0
          Message = message }

    let auditOptions () : AuditOptions =
        { RepoRoot = root ()
          Skip = []
          IncludeOnly = []
          Now = Some "2026-01-01T00:00:00Z"
          KnownFalsePositivesPath = None
          ExcludeGlobs = [] }

    let runAuditScenario (opts: AuditOptions) : AuditEnvelope =
        let envelope =
            runAuditWith (auditRunner |> Option.defaultValue runAuditCategory) opts

        auditEnvelope <- Some envelope
        exitCode <- (if envelope.Result.TotalFindings > 0 then 1 else 0)
        output <- formatAuditJson envelope
        envelope

    let requireEnvelope () : AuditEnvelope =
        match auditEnvelope with
        | Some envelope -> envelope
        | None -> failwith "repo-governance audit never ran"

    let sixLayers =
        [ 0, "Vision"
          1, "Principles"
          2, "Conventions"
          3, "Development"
          4, "Workflows"
          5, "Glossary" ]

    // ---- Given (`repo-governance-layer-coherence.feature`) ----

    [<Given>]
    member _.``a repository where both governance docs list layers 0 through 5 with identical names``() =
        writeGovernanceDocs sixLayers sixLayers

    [<Given>]
    member _.``a repository where the governance docs list layers 0, 1, and 3 with no layer 2``() =
        let layers = [ 0, "Vision"; 1, "Principles"; 3, "Development" ]
        writeGovernanceDocs layers layers

    [<Given>]
    member _.``a repository where the two governance docs assign different names to the same layer number``() =
        writeGovernanceDocs [ 0, "Vision"; 1, "Principles" ] [ 0, "Vision"; 1, "Foundations" ]

    // ---- When ----

    [<When>]
    member _.``the developer runs repo-governance layer-coherence validate``() =
        layerFindings <- auditLayerCoherence (root ())
        output <- formatLayerCoherenceText layerFindings
        exitCode <- (if List.isEmpty layerFindings then 0 else 1)

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, exitCode)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEqual(0, exitCode)

    [<Then>]
    member _.``the layer-coherence output reports zero findings``() =
        Assert.Empty layerFindings
        Assert.Contains("LAYER COHERENCE AUDIT PASSED: zero findings", output, StringComparison.Ordinal)

    [<Then>]
    member _.``the layer-coherence output identifies the numbering gap``() =
        Assert.Contains(layerFindings, (fun f -> f.Kind = KindNumberingGap))
        Assert.Contains("Layer 2 is missing between 0 and 3", output, StringComparison.Ordinal)

    [<Then>]
    member _.``the layer-coherence output identifies the layer name disagreement``() =
        Assert.Contains(layerFindings, (fun f -> f.Kind = KindCrossFileNameMismatch))
        Assert.Contains("Layer 1 named \"Principles\"", output, StringComparison.Ordinal)
        Assert.Contains("but \"Foundations\" in", output, StringComparison.Ordinal)

    // ---- Given (`repo-governance-traceability-audit.feature`) ----

    /// Writes one compliant document into each audited governance family.
    member private _.WriteCleanTree() =
        writeDoc "principles/p.md" "# P\n\n## Vision Supported\n\n- vision\n"
        writeDoc "conventions/c.md" "# C\n\n## Principles Implemented/Respected\n\n- p\n"

        writeDoc
            "development/d.md"
            "# D\n\n## Principles Implemented/Respected\n\n- p\n\n## Conventions Implemented/Respected\n\n- c\n"

        writeDoc "workflows/w.md" "# W\n\nRun .claude/agents/pr-review/pr-review-fixer.md\n"

    [<Given>]
    member this.``a repository where every governance document carries the required traceability sections``() =
        this.WriteCleanTree()

    // TickSpec reads `#` as a Gherkin inline comment and truncates this step's
    // text at the quoted heading, while the spec-coverage checker matches the
    // whole `.feature` line — so the tail is an optional group, satisfying both
    // readers with one binding. Same for the two sibling steps below.
    [<Given>]
    member this.``a repository with a principle file that is missing the "(?:## Vision Supported" heading)?``() =
        this.WriteCleanTree()
        writeDoc "principles/untraced.md" "# Untraced\n\nno traceability section here\n"

    [<Given>]
    member this.``a repository with a convention file that is missing the "(?:## Principles Implemented/Respected" heading)?``
        ()
        =
        this.WriteCleanTree()
        writeDoc "conventions/untraced.md" "# Untraced\n\nno traceability section here\n"

    [<Given>]
    member this.``a repository with a development file that is missing the "(?:## Conventions Implemented/Respected" heading)?``
        ()
        =
        this.WriteCleanTree()
        writeDoc "development/untraced.md" "# Untraced\n\n## Principles Implemented/Respected\n\n- p\n"

    [<Given>]
    member this.``a repository with a workflow file that contains no reference to any \.claude/agents/ file``() =
        this.WriteCleanTree()
        writeDoc "workflows/unreferenced.md" "# Workflow\n\nno agent reference here\n"

    [<Given>]
    member this.``a repository with a governance document split into a child directory whose children carry plain kebab-case names``
        ()
        =
        this.WriteCleanTree()
        writeDoc "conventions/split.md" "# Split\n\n## Principles Implemented/Respected\n\n- p\n"
        writeDoc "conventions/split/README.md" "# Split index\n\n- [child](./plain-child.md)\n"
        writeDoc "conventions/split/plain-child.md" "# Plain child\n\nfragment body\n"

    [<Given>]
    member this.``a repository with a governance document split across nested indexed child directories``() =
        this.WriteCleanTree()
        writeDoc "conventions/nested.md" "# Nested\n\n## Principles Implemented/Respected\n\n- p\n"
        writeDoc "conventions/nested/README.md" "# Nested index\n\n- [deep](./deep/fragment.md)\n"
        writeDoc "conventions/nested/deep/fragment.md" "# Deep fragment\n\nfragment body\n"

    [<Given>]
    member this.``a split convention whose indexed child carries the required traceability section``() =
        this.WriteCleanTree()
        writeDoc "conventions/carried.md" "# Carried\n\nparent body with no traceability section\n"
        writeDoc "conventions/carried/README.md" "# Carried index\n\n- [child](./child.md)\n"
        writeDoc "conventions/carried/child.md" "# Principles Implemented/Respected\n\n- p\n"

    [<Given>]
    member this.``a repository with an indexed category directory that has no same-named parent document``() =
        this.WriteCleanTree()
        writeDoc "conventions/category/README.md" "# Category index\n\n- [doc](./doc.md)\n"
        writeDoc "conventions/category/doc.md" "# Doc\n\nno traceability section here\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs repo-governance traceability validate``() =
        traceFindings <- auditTraceability (root ())
        output <- formatTraceabilityText traceFindings
        exitCode <- (if List.isEmpty traceFindings then 0 else 1)

    // ---- Then ----

    [<Then>]
    member _.``the traceability output reports zero findings``() =
        Assert.Empty traceFindings
        Assert.Contains("TRACEABILITY AUDIT PASSED: zero findings", output, StringComparison.Ordinal)

    [<Then>]
    member _.``the traceability output identifies the missing Vision Supported section``() =
        Assert.Contains(traceFindings, (fun f -> f.Kind = KindMissingVisionSupported))
        Assert.Contains("untraced.md", output, StringComparison.Ordinal)

    [<Then>]
    member _.``the traceability output identifies the missing Principles Implemented section``() =
        Assert.Contains(traceFindings, (fun f -> f.Kind = KindMissingPrinciplesImplemented))

    [<Then>]
    member _.``the traceability output identifies the missing Conventions Implemented section``() =
        Assert.Contains(traceFindings, (fun f -> f.Kind = KindMissingConventionsImplemented))
        Assert.Contains("untraced.md", output, StringComparison.Ordinal)

    [<Then>]
    member _.``the traceability output identifies the missing agent reference``() =
        Assert.Contains(traceFindings, (fun f -> f.Kind = KindMissingAgentReference))
        Assert.Contains("unreferenced.md", output, StringComparison.Ordinal)

    // ---- Given (`repo-governance-vendor-audit.feature`) ----

    [<Given>]
    member _.``a governance markdown file containing "Claude Code" in plain prose``() =
        writeVendorFile "# Doc\n\nThe agent runs under Claude Code today.\n"

    [<Given>]
    member _.``a governance markdown file containing "Claude Code" inside a code fence``() =
        writeVendorFile "# Doc\n\n```\nClaude Code\n```\n"

    [<Given>]
    member _.``a governance markdown file containing "Claude Code" inside a binding-example fence``() =
        writeVendorFile "# Doc\n\n````md\n```yaml\nharness: Claude Code\n```\n````\n"

    [<Given>]
    member _.``a governance markdown file containing "Claude Code" under a "(?:Platform Binding Examples" heading)?``
        ()
        =
        writeVendorFile "# Doc\n\n## Platform Binding Examples\n\nClaude Code reads this directory.\n"

    [<Given>]
    member _.``a governance directory with no forbidden terms in prose``() =
        let dir = Path.Combine(root (), "repo-governance")
        Directory.CreateDirectory dir |> ignore
        File.WriteAllText(Path.Combine(dir, "a.md"), "# A\n\nThe coding agent reads this.\n")
        File.WriteAllText(Path.Combine(dir, "b.md"), "# B\n\nVendor-neutral prose only.\n")
        vendorTarget <- Some dir

    [<Given>]
    member _.``a governance markdown file containing "Skills" in plain prose``() =
        writeVendorFile "# Doc\n\nSkills are declared per harness.\n"

    [<Given>]
    member _.``a governance markdown file containing "Skills" inside a code fence``() =
        writeVendorFile "# Doc\n\n```\nSkills\n```\n"

    [<Given>]
    member _.``a governance markdown file containing "Junie" in plain prose``() =
        writeVendorFile "# Doc\n\nJunie is one such agent.\n"

    [<Given>]
    member _.``a governance markdown file containing "Amazon Q" in plain prose``() =
        writeVendorFile "# Doc\n\nAmazon Q is one such agent.\n"

    [<Given>]
    member _.``a governance markdown file containing "Antigravity" in plain prose``() =
        writeVendorFile "# Doc\n\nAntigravity is one such editor.\n"

    [<Given>]
    member _.``a governance markdown file containing "The value of pi is 3.14159." in plain prose``() =
        writeVendorFile "# Doc\n\nThe value of pi is 3.14159.\n"

    [<Given>]
    member _.``a governance markdown file containing "Junie" under a "(?:Platform Binding Examples" heading)?``() =
        writeVendorFile "# Doc\n\n## Platform Binding Examples\n\nJunie reads this directory.\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs repo-governance vendor validate on the file``() =
        vendorFindings <-
            match vendorTarget with
            | Some path -> scanVendorFile path
            | None -> failwith "no governance file was written"

        output <- formatVendorText vendorFindings
        exitCode <- (if List.isEmpty vendorFindings then 0 else 1)

    [<When>]
    member _.``the developer runs repo-governance vendor validate on the directory``() =
        vendorFindings <-
            match vendorTarget with
            | Some dir -> walkVendor dir
            | None -> failwith "no governance directory was written"

        output <- formatVendorText vendorFindings
        exitCode <- (if List.isEmpty vendorFindings then 0 else 1)

    // ---- Then ----

    [<Then>]
    member _.``the output identifies the forbidden term and its location``() =
        let finding = List.head vendorFindings
        Assert.Contains(finding.Match, output, StringComparison.Ordinal)
        Assert.Contains(sprintf "%s:%d" finding.Path finding.Line, output, StringComparison.Ordinal)

    [<Then>]
    member _.``the output reports zero findings``() =
        Assert.Empty vendorFindings
        Assert.Contains("GOVERNANCE VENDOR AUDIT PASSED", output, StringComparison.Ordinal)

    // ---- Given (`repo-governance-audit.feature`) ----

    [<Given>]
    member _.``a repository where every deterministic governance category reports zero findings``() =
        auditRunner <- Some(fixedRunner [])

    [<Given>]
    member _.``a repository with forbidden vendor terms in repo-governance prose and also in out-of-scope paths such as build caches, app source, and worktrees``
        ()
        =
        let write (rel: string) (content: string) =
            let path = Path.Combine(root (), rel.Replace('/', Path.DirectorySeparatorChar))
            Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
            File.WriteAllText(path, content)

        let leak = "# Doc\n\nClaude Code reads this.\n"
        write "repo-governance/in-scope.md" leak
        write "AGENTS.md" leak
        write "CLAUDE.md" leak
        write "node_modules/.cache/cached.md" leak
        write "apps/demo/src/app-source.md" leak
        write "worktrees/side/worktree-doc.md" leak

    [<Given>]
    member _.``a repository where two deterministic governance categories report findings and the rest pass``() =
        auditRunner <-
            Some(
                fixedRunner
                    [ "layer-coherence",
                      [ auditFindingWithKey "layer-coherence|a.md|00000001" "a.md" "first"
                        auditFindingWithKey "layer-coherence|b.md|00000002" "b.md" "second" ]
                      "traceability-audit", [ auditFindingWithKey "traceability-audit|c.md|00000003" "c.md" "third" ] ]
            )

    [<Given>]
    member _.``a repository where deterministic governance categories return a fixed finding set``() =
        auditRunner <-
            Some(
                fixedRunner
                    [ "vendor-audit", [ auditFindingWithKey "vendor-audit|d.md|00000004" "d.md" "fixed finding" ] ]
            )

    [<Given>]
    member _.``a repository where a finding key matches a known-false-positives entry``() =
        auditSuppressedKey <- "vendor-audit|suppressed.md|00000005"

        auditRunner <-
            Some(
                fixedRunner
                    [ "vendor-audit", [ auditFindingWithKey auditSuppressedKey "suppressed.md" "known false positive" ] ]
            )

        let dir = Path.Combine(root (), "generated-reports")
        Directory.CreateDirectory dir |> ignore

        File.WriteAllText(
            Path.Combine(dir, ".known-false-positives.md"),
            sprintf "# Known false positives\n\n- `%s`\n" auditSuppressedKey
        )

    [<Given>]
    member _.``a repository where deterministic governance categories return any finding set``() =
        auditRunner <-
            Some(
                fixedRunner
                    [ "layer-coherence", [ auditFindingWithKey "layer-coherence|e.md|00000006" "e.md" "layer" ]
                      "vendor-audit", [ auditFindingWithKey "vendor-audit|f.md|00000007" "f.md" "vendor" ] ]
            )

    // ---- When ----

    [<When>]
    member _.``the developer runs repo-governance audit``() =
        runAuditScenario (auditOptions ()) |> ignore

    [<When>]
    member _.``the developer runs repo-governance audit ten consecutive times with a fixed clock``() =
        auditJsonRuns <- [ for _ in 1..10 -> formatAuditJson (runAuditScenario (auditOptions ())) ]

    [<When>]
    member _.``the developer runs repo-governance audit with include-category limited to one category``() =
        runAuditScenario
            { auditOptions () with
                IncludeOnly = [ "vendor-audit" ] }
        |> ignore

    // ---- Then ----

    [<Then>]
    member _.``the output reports total_findings equal to zero across all categories``() =
        let envelope = requireEnvelope ()
        Assert.Equal(0, envelope.Result.TotalFindings)
        Assert.Equal("ok", envelope.Status)
        Assert.All(envelope.Result.Categories, (fun c -> Assert.True c.Passed))

    [<Then>]
    member _.``the vendor-audit category reports findings only from repo-governance, AGENTS.md, and CLAUDE.md``() =
        let vendor =
            requireEnvelope().Result.Categories
            |> List.find (fun c -> c.Name = "vendor-audit")

        Assert.NotEmpty vendor.Findings

        Assert.All(
            vendor.Findings,
            fun f ->
                let name = Path.GetFileName f.File

                Assert.True(f.File.Contains "repo-governance" || name = "AGENTS.md" || name = "CLAUDE.md", f.File)
        )

    [<Then>]
    member _.``forbidden vendor terms in build caches, app source, and worktrees do not appear in the result``() =
        let files =
            requireEnvelope().Result.Categories
            |> List.collect (fun c -> c.Findings)
            |> List.map (fun f -> f.File)

        for fragment in [ "node_modules"; "apps/demo"; "worktrees" ] do
            Assert.DoesNotContain(fragment, String.Join("\n", files), StringComparison.Ordinal)

    [<Then>]
    member _.``the output reports total_findings equal to the sum of category findings``() =
        let envelope = requireEnvelope ()

        let sum = envelope.Result.Categories |> List.sumBy (fun c -> List.length c.Findings)

        Assert.Equal(sum, envelope.Result.TotalFindings)
        Assert.Equal(3, envelope.Result.TotalFindings)

    [<Then>]
    member _.``every run produces byte-identical JSON output``() =
        Assert.Equal(10, List.length auditJsonRuns)
        Assert.All(auditJsonRuns, (fun run -> Assert.Equal(List.head auditJsonRuns, run)))

    [<Then>]
    member _.``the matching finding appears under skipped_false_positives``() =
        let envelope = requireEnvelope ()

        Assert.Contains(envelope.Result.SkippedFalsePositives, fun f -> f.Key = auditSuppressedKey)

    [<Then>]
    member _.``the matching finding does not count toward total_findings``() =
        Assert.Equal(0, requireEnvelope().Result.TotalFindings)

    [<Then>]
    member _.``only the listed category appears in the result categories list``() =
        let names = requireEnvelope().Result.Categories |> List.map (fun c -> c.Name)
        Assert.Equal<string list>([ "vendor-audit" ], names)

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
                "cli",
                "behaviors",
                "repo-governance"
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
    /// (a file inside `gherkin/repo-governance/`), bound against
    /// `RepoGovernanceSteps`.
    let run (featureFileName: string) (scenarioTitle: string) : unit =
        let featurePath = Path.Combine(featureDir, featureFileName)
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<RepoGovernanceSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Both docs list identical layer numbers and names passes`` () =
    FeatureRunner.run
        "repo-governance-layer-coherence.feature"
        "Both docs list identical layer numbers and names passes"

[<Fact>]
let ``Layer numbering has a gap fails`` () =
    FeatureRunner.run "repo-governance-layer-coherence.feature" "Layer numbering has a gap fails"

[<Fact>]
let ``Two docs disagree on a layer name for the same number fails`` () =
    FeatureRunner.run
        "repo-governance-layer-coherence.feature"
        "Two docs disagree on a layer name for the same number fails"

[<Fact>]
let ``A clean repository passes the traceability audit`` () =
    FeatureRunner.run "repo-governance-traceability-audit.feature" "A clean repository passes the traceability audit"

[<Fact>]
let ``A principle missing the Vision Supported heading fails the audit`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A principle missing the Vision Supported heading fails the audit"

[<Fact(DisplayName = "A convention missing the Principles Implemented/Respected heading fails the audit")>]
let ``A convention missing the Principles Implemented heading fails the audit`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A convention missing the Principles Implemented/Respected heading fails the audit"

[<Fact(DisplayName = "A development document missing the Conventions Implemented/Respected heading fails the audit")>]
let ``A development document missing the Conventions Implemented heading fails the audit`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A development document missing the Conventions Implemented/Respected heading fails the audit"

[<Fact>]
let ``A workflow with no agent reference fails the audit`` () =
    FeatureRunner.run "repo-governance-traceability-audit.feature" "A workflow with no agent reference fails the audit"

[<Fact>]
let ``A progressive-disclosure split child is exempt regardless of its filename`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A progressive-disclosure split child is exempt regardless of its filename"

[<Fact>]
let ``A nested progressive-disclosure fragment is audited through its parent family`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A nested progressive-disclosure fragment is audited through its parent family"

[<Fact>]
let ``A split document may keep its traceability section in an indexed child`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A split document may keep its traceability section in an indexed child"

[<Fact>]
let ``A document in an indexed category directory is still audited`` () =
    FeatureRunner.run
        "repo-governance-traceability-audit.feature"
        "A document in an indexed category directory is still audited"

[<Fact>]
let ``A forbidden term in plain prose fails the audit`` () =
    FeatureRunner.run "repo-governance-vendor-audit.feature" "A forbidden term in plain prose fails the audit"

[<Fact>]
let ``A forbidden term inside a code fence passes the audit`` () =
    FeatureRunner.run "repo-governance-vendor-audit.feature" "A forbidden term inside a code fence passes the audit"

[<Fact>]
let ``A forbidden term inside a binding-example fence passes the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "A forbidden term inside a binding-example fence passes the audit"

[<Fact>]
let ``A forbidden term under a Platform Binding Examples heading passes the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "A forbidden term under a Platform Binding Examples heading passes the audit"

[<Fact>]
let ``A governance directory with no forbidden terms passes the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "A governance directory with no forbidden terms passes the audit"

[<Fact>]
let ``Capitalized branded Skills in plain prose fails the audit`` () =
    FeatureRunner.run "repo-governance-vendor-audit.feature" "Capitalized branded Skills in plain prose fails the audit"

[<Fact>]
let ``Capitalized Skills inside a code fence passes the audit`` () =
    FeatureRunner.run "repo-governance-vendor-audit.feature" "Capitalized Skills inside a code fence passes the audit"

[<Fact>]
let ``A newly forbidden coding-agent vendor name in plain prose fails the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "A newly forbidden coding-agent vendor name in plain prose fails the audit"

[<Fact>]
let ``The Amazon Q vendor name in plain prose fails the audit`` () =
    FeatureRunner.run "repo-governance-vendor-audit.feature" "The Amazon Q vendor name in plain prose fails the audit"

[<Fact>]
let ``The Antigravity vendor name in plain prose fails the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "The Antigravity vendor name in plain prose fails the audit"

[<Fact>]
let ``The mathematical constant pi in plain prose passes the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "The mathematical constant pi in plain prose passes the audit"

[<Fact>]
let ``A newly forbidden vendor name under a Platform Binding Examples heading passes the audit`` () =
    FeatureRunner.run
        "repo-governance-vendor-audit.feature"
        "A newly forbidden vendor name under a Platform Binding Examples heading passes the audit"

[<Fact(DisplayName = "Clean repository: all categories pass, total_findings is 0, exit 0")>]
let ``Clean repository all categories pass`` () =
    FeatureRunner.run
        "repo-governance-audit.feature"
        "Clean repository: all categories pass, total_findings is 0, exit 0"

[<Fact(DisplayName = "Vendor-audit scope is limited to governance prose and root instruction surfaces")>]
let ``Vendor-audit scope is limited to governance prose and root instruction surfaces`` () =
    FeatureRunner.run
        "repo-governance-audit.feature"
        "Vendor-audit scope is limited to governance prose and root instruction surfaces"

[<Fact(DisplayName = "Mixed findings: some categories pass, some fail; total_findings is the sum; exit 1")>]
let ``Mixed findings total is the sum`` () =
    FeatureRunner.run
        "repo-governance-audit.feature"
        "Mixed findings: some categories pass, some fail; total_findings is the sum; exit 1"

[<Fact(DisplayName = "Byte-determinism: running the orchestrator 10 times in a row produces byte-identical JSON")>]
let ``Byte-determinism ten runs produce identical JSON`` () =
    FeatureRunner.run
        "repo-governance-audit.feature"
        "Byte-determinism: running the orchestrator 10 times in a row produces byte-identical JSON"

[<Fact(DisplayName = "Skip list honored: false-positive entries do not count toward total_findings")>]
let ``Skip list honored`` () =
    FeatureRunner.run
        "repo-governance-audit.feature"
        "Skip list honored: false-positive entries do not count toward total_findings"

[<Fact(DisplayName = "Include-category filter: only listed categories run")>]
let ``Include-category filter only listed categories run`` () =
    FeatureRunner.run "repo-governance-audit.feature" "Include-category filter: only listed categories run"
