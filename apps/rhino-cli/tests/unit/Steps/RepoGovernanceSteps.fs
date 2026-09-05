/// Pure TickSpec bindings for repository-governance command behaviour.
module RhinoCli.Tests.Unit.Steps.RepoGovernanceSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-audit.feature"
      "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-layer-coherence.feature"
      "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-traceability-audit.feature"
      "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-vendor-audit.feature" ]

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.RepoGovernance

type RepoGovernanceSteps() =
    let mutable documents: Map<string, string> = Map.empty
    let mutable layerFindings: LayerCoherenceFinding list = []
    let mutable traceFindings: TraceabilityFinding list = []
    let mutable vendorFindings: VendorFinding list = []

    let mutable auditRunner: (string -> AuditOptions -> AuditFinding list) =
        fun _ _ -> []

    let mutable suppressionKeys: Set<string> = Set.empty
    let mutable auditEnvelope: AuditEnvelope option = None
    let mutable auditJsonRuns: string list = []
    let mutable output = ""
    let mutable exitCode = 0

    let write path content =
        documents <- Map.add path content documents

    let renderLayers layers =
        layers
        |> List.map (fun (number, name: string) ->
            sprintf "## Layer %d: %s (the %s layer)" number name (name.ToLowerInvariant()))
        |> String.concat "\n\n"
        |> fun body -> "# Governance\n\n" + body + "\n"

    let writeLayers arch readme =
        write "repo-governance/repository-governance-architecture.md" (renderLayers arch)
        write "repo-governance/README.md" (renderLayers readme)

    let writeCleanTraceability () =
        write "repo-governance/principles/p.md" "# P\n\n## Vision Supported\n\n- vision\n"
        write "repo-governance/conventions/c.md" "# C\n\n## Principles Implemented/Respected\n\n- p\n"

        write
            "repo-governance/development/d.md"
            "# D\n\n## Principles Implemented/Respected\n\n- p\n\n## Conventions Implemented/Respected\n\n- c\n"

        write "repo-governance/workflows/w.md" "# W\n\nRun .claude/agents/pr-review/pr-review-fixer.md\n"

    let finding key file message =
        { Key = key
          Severity = "high"
          Criticality = "HIGH"
          File = file
          Line = 0
          Message = message }

    let fixedRunner table name (_: AuditOptions) =
        table
        |> List.tryFind (fun (category, _) -> category = name)
        |> Option.map snd
        |> Option.defaultValue []

    let options includeOnly =
        { RepoRoot = "/virtual-rhino-repository"
          Skip = []
          IncludeOnly = includeOnly
          Now = Some "2026-01-01T00:00:00Z"
          KnownFalsePositivesPath = None
          ExcludeGlobs = [] }

    let runAudit includeOnly =
        let envelope =
            runAuditCore auditRunner suppressionKeys "abc1234" "2026-01-01T00:00:00Z" (options includeOnly)

        auditEnvelope <- Some envelope
        output <- formatAuditJson envelope
        exitCode <- if envelope.Result.TotalFindings = 0 then 0 else 1
        envelope

    let requireAudit () =
        auditEnvelope |> Option.defaultWith (fun () -> failwith "audit did not run")

    member private _.HandleGiven(step: string) =
        let layers =
            [ 0, "Vision"
              1, "Principles"
              2, "Conventions"
              3, "Development"
              4, "Workflows"
              5, "Glossary" ]

        if step.Contains("both governance docs list layers 0 through 5", StringComparison.Ordinal) then
            writeLayers layers layers
        elif step.Contains("layers 0, 1, and 3", StringComparison.Ordinal) then
            let gapped = [ 0, "Vision"; 1, "Principles"; 3, "Development" ] in writeLayers gapped gapped
        elif step.Contains("assign different names", StringComparison.Ordinal) then
            writeLayers [ 0, "Vision"; 1, "Principles" ] [ 0, "Vision"; 1, "Foundations" ]
        elif step.Contains("every governance document carries", StringComparison.Ordinal) then
            writeCleanTraceability ()
        elif step.Contains("principle file", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/principles/untraced.md" "# Untraced\n"
        elif step.Contains("convention file", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/conventions/untraced.md" "# Untraced\n"
        elif step.Contains("development file", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/development/untraced.md" "# Untraced\n\n## Principles Implemented/Respected\n"
        elif step.Contains("workflow file", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/workflows/unreferenced.md" "# Workflow\n"
        elif step.Contains("split into a child directory", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/conventions/split.md" "# Split\n\n## Principles Implemented/Respected\n"
            write "repo-governance/conventions/split/README.md" "# Index\n"
            write "repo-governance/conventions/split/plain-child.md" "# Child\n"
        elif step.Contains("split across nested", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/conventions/nested.md" "# Nested\n\n## Principles Implemented/Respected\n"
            write "repo-governance/conventions/nested/README.md" "# Index\n"
            write "repo-governance/conventions/nested/deep/fragment.md" "# Fragment\n"
        elif step.Contains("indexed child carries", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/conventions/carried.md" "# Carried\n"
            write "repo-governance/conventions/carried/README.md" "# Index\n"
            write "repo-governance/conventions/carried/child.md" "# Principles Implemented/Respected\n"
        elif step.Contains("indexed category directory", StringComparison.Ordinal) then
            writeCleanTraceability ()
            write "repo-governance/conventions/category/README.md" "# Index\n"
            write "repo-governance/conventions/category/doc.md" "# Doc\n"
        elif step.Contains("governance markdown file", StringComparison.Ordinal) then
            let body =
                if step.Contains("inside a binding-example fence", StringComparison.Ordinal) then
                    "````md\n```yaml\nharness: Claude Code\n```\n````\n"
                elif step.Contains("inside a code fence", StringComparison.Ordinal) then
                    sprintf
                        "```\n%s\n```\n"
                        (if step.Contains("Skills", StringComparison.Ordinal) then
                             "Skills"
                         else
                             "Claude Code")
                elif step.Contains("under a", StringComparison.Ordinal) then
                    sprintf
                        "## Platform Binding Examples\n\n%s reads this directory.\n"
                        (if step.Contains("Junie", StringComparison.Ordinal) then
                             "Junie"
                         else
                             "Claude Code")
                elif step.Contains("Skills", StringComparison.Ordinal) then
                    "Skills are declared per harness.\n"
                elif step.Contains("Junie", StringComparison.Ordinal) then
                    "Junie is one such agent.\n"
                elif step.Contains("Amazon Q", StringComparison.Ordinal) then
                    "Amazon Q is one such agent.\n"
                elif step.Contains("Antigravity", StringComparison.Ordinal) then
                    "Antigravity is one such editor.\n"
                elif step.Contains("3.14159", StringComparison.Ordinal) then
                    "The value of pi is 3.14159.\n"
                else
                    "Claude Code is the active harness.\n"

            write "repo-governance/doc.md" ("# Doc\n\n" + body)
        elif step.Contains("directory with no forbidden terms", StringComparison.Ordinal) then
            write "repo-governance/a.md" "# A\n\nVendor-neutral prose.\n"
            write "repo-governance/b.md" "# B\n\nThe coding agent reads this.\n"
        elif step.Contains("every deterministic governance category reports zero", StringComparison.Ordinal) then
            auditRunner <- fixedRunner []
        elif step.Contains("forbidden vendor terms in repo-governance prose", StringComparison.Ordinal) then
            let leak = "# Doc\n\nClaude Code reads this.\n"

            [ "repo-governance/in-scope.md"
              "AGENTS.md"
              "CLAUDE.md"
              "node_modules/cache.md"
              "apps/demo/source.md"
              "worktrees/side/doc.md" ]
            |> List.iter (fun path -> write path leak)

            auditRunner <-
                fun name _ ->
                    if name <> "vendor-audit" then
                        []
                    else
                        scanVendorGovernanceDocuments documents
                        |> List.map (fun item ->
                            finding (sprintf "vendor|%s|%d" item.Path item.Line) item.Path item.Match)
        elif step.Contains("two deterministic governance categories", StringComparison.Ordinal) then
            auditRunner <-
                fixedRunner
                    [ "layer-coherence", [ finding "layer|a" "a.md" "first"; finding "layer|b" "b.md" "second" ]
                      "traceability-audit", [ finding "trace|c" "c.md" "third" ] ]
        elif step.Contains("fixed finding set", StringComparison.Ordinal) then
            auditRunner <- fixedRunner [ "vendor-audit", [ finding "vendor|fixed" "d.md" "fixed" ] ]
        elif step.Contains("known-false-positives", StringComparison.Ordinal) then
            let key = "vendor-audit|suppressed.md|00000005" in
            suppressionKeys <- Set.singleton key
            auditRunner <- fixedRunner [ "vendor-audit", [ finding key "suppressed.md" "known false positive" ] ]
        elif step.Contains("return any finding set", StringComparison.Ordinal) then
            auditRunner <-
                fixedRunner
                    [ "layer-coherence", [ finding "layer|e" "e.md" "layer" ]
                      "vendor-audit", [ finding "vendor|f" "f.md" "vendor" ] ]
        else
            failwithf "unhandled repo-governance Given: %s" step

    member private _.HandleWhen(step: string) =
        if step.Contains("layer-coherence", StringComparison.Ordinal) then
            layerFindings <- auditLayerCoherenceDocuments documents
            output <- formatLayerCoherenceText layerFindings
            exitCode <- if List.isEmpty layerFindings then 0 else 1
        elif step.Contains("traceability", StringComparison.Ordinal) then
            traceFindings <- auditTraceabilityDocuments documents
            output <- formatTraceabilityText traceFindings
            exitCode <- if List.isEmpty traceFindings then 0 else 1
        elif step.Contains("vendor validate", StringComparison.Ordinal) then
            vendorFindings <-
                documents
                |> Map.toList
                |> List.collect (fun (path, content) -> scanVendorLines path content)

            output <- formatVendorText vendorFindings
            exitCode <- if List.isEmpty vendorFindings then 0 else 1
        elif step.Contains("ten consecutive times", StringComparison.Ordinal) then
            auditJsonRuns <- [ for _ in 1..10 -> formatAuditJson (runAudit []) ]
        elif step.Contains("include-category", StringComparison.Ordinal) then
            runAudit [ "vendor-audit" ] |> ignore
        elif step.Contains("repo-governance audit", StringComparison.Ordinal) then
            runAudit [] |> ignore
        else
            failwithf "unhandled repo-governance When: %s" step

    member private _.HandleThen(step: string) =
        match step with
        | "the command exits successfully" -> Assert.Equal(0, exitCode)
        | "the command exits with a failure code" -> Assert.NotEqual(0, exitCode)
        | text when text.Contains("reports zero findings", StringComparison.Ordinal) ->
            Assert.Contains("PASSED", output, StringComparison.Ordinal)
        | text when text.Contains("numbering gap", StringComparison.Ordinal) ->
            Assert.Contains(layerFindings, fun item -> item.Kind = KindNumberingGap)
        | text when text.Contains("layer name disagreement", StringComparison.Ordinal) ->
            Assert.Contains(layerFindings, fun item -> item.Kind = KindCrossFileNameMismatch)
        | text when text.Contains("missing Vision Supported", StringComparison.Ordinal) ->
            Assert.Contains(traceFindings, fun item -> item.Kind = KindMissingVisionSupported)
        | text when text.Contains("missing Principles Implemented", StringComparison.Ordinal) ->
            Assert.Contains(traceFindings, fun item -> item.Kind = KindMissingPrinciplesImplemented)
        | text when text.Contains("missing Conventions Implemented", StringComparison.Ordinal) ->
            Assert.Contains(traceFindings, fun item -> item.Kind = KindMissingConventionsImplemented)
        | text when text.Contains("missing agent reference", StringComparison.Ordinal) ->
            Assert.Contains(traceFindings, fun item -> item.Kind = KindMissingAgentReference)
        | text when text.Contains("forbidden term and its location", StringComparison.Ordinal) ->
            let item = List.head vendorFindings in
            Assert.Contains(item.Match, output, StringComparison.Ordinal)
            Assert.Contains(sprintf "%s:%d" item.Path item.Line, output, StringComparison.Ordinal)
        | text when text.Contains("total_findings equal to zero", StringComparison.Ordinal) ->
            Assert.Equal(0, requireAudit().Result.TotalFindings)
        | text when text.Contains("category reports findings only", StringComparison.Ordinal) ->
            let files =
                requireAudit().Result.Categories
                |> List.collect (fun category -> category.Findings)
                |> List.map (fun item -> item.File) in

            Assert.All(
                files,
                fun path -> Assert.True(path.StartsWith("repo-governance/") || path = "AGENTS.md" || path = "CLAUDE.md")
            )
        | text when text.Contains("do not appear in the result", StringComparison.Ordinal) ->
            let files =
                requireAudit().Result.Categories
                |> List.collect (fun category -> category.Findings)
                |> List.map (fun item -> item.File)
                |> String.concat "\n" in

            Assert.DoesNotContain("node_modules", files, StringComparison.Ordinal)
            Assert.DoesNotContain("apps/demo", files, StringComparison.Ordinal)
            Assert.DoesNotContain("worktrees", files, StringComparison.Ordinal)
        | text when text.Contains("equal to the sum", StringComparison.Ordinal) ->
            let result = requireAudit().Result in

            Assert.Equal(
                result.Categories |> List.sumBy (fun category -> List.length category.Findings),
                result.TotalFindings
            )
        | text when text.Contains("byte-identical", StringComparison.Ordinal) ->
            Assert.Equal(10, List.length auditJsonRuns)
            Assert.All(auditJsonRuns, fun item -> Assert.Equal(List.head auditJsonRuns, item))
        | text when text.Contains("appears under skipped_false_positives", StringComparison.Ordinal) ->
            Assert.Single(requireAudit().Result.SkippedFalsePositives) |> ignore
        | text when text.Contains("does not count toward total_findings", StringComparison.Ordinal) ->
            Assert.Equal(0, requireAudit().Result.TotalFindings)
        | text when text.Contains("only the listed category", StringComparison.Ordinal) ->
            Assert.Equal<string list>(
                [ "vendor-audit" ],
                requireAudit().Result.Categories |> List.map (fun category -> category.Name)
            )
        | unknown -> failwithf "unhandled repo-governance Then: %s" unknown

    // GENERATED EXACT BINDINGS START
    [<Given>]
    member this.``a governance directory with no forbidden terms in prose``() =
        this.HandleGiven("a governance directory with no forbidden terms in prose")

    [<Given>]
    member this.``a governance markdown file containing "Amazon Q" in plain prose``() =
        this.HandleGiven("a governance markdown file containing \"Amazon Q\" in plain prose")

    [<Given>]
    member this.``a governance markdown file containing "Antigravity" in plain prose``() =
        this.HandleGiven("a governance markdown file containing \"Antigravity\" in plain prose")

    [<Given>]
    member this.``a governance markdown file containing "Claude Code" in plain prose``() =
        this.HandleGiven("a governance markdown file containing \"Claude Code\" in plain prose")

    [<Given>]
    member this.``a governance markdown file containing "Claude Code" inside a binding-example fence``() =
        this.HandleGiven("a governance markdown file containing \"Claude Code\" inside a binding-example fence")

    [<Given>]
    member this.``a governance markdown file containing "Claude Code" inside a code fence``() =
        this.HandleGiven("a governance markdown file containing \"Claude Code\" inside a code fence")

    [<Given>]
    member this.``a governance markdown file containing "Claude Code" under a "Platform Binding Examples" heading``() =
        this.HandleGiven(
            "a governance markdown file containing \"Claude Code\" under a \"Platform Binding Examples\" heading"
        )

    [<Given>]
    member this.``a governance markdown file containing "Junie" in plain prose``() =
        this.HandleGiven("a governance markdown file containing \"Junie\" in plain prose")

    [<Given>]
    member this.``a governance markdown file containing "Junie" under a "Platform Binding Examples" heading``() =
        this.HandleGiven(
            "a governance markdown file containing \"Junie\" under a \"Platform Binding Examples\" heading"
        )

    [<Given>]
    member this.``a governance markdown file containing "Skills" in plain prose``() =
        this.HandleGiven("a governance markdown file containing \"Skills\" in plain prose")

    [<Given>]
    member this.``a governance markdown file containing "Skills" inside a code fence``() =
        this.HandleGiven("a governance markdown file containing \"Skills\" inside a code fence")

    [<Given>]
    member this.``a governance markdown file containing "The value of pi is 3\.14159\." in plain prose``() =
        this.HandleGiven("a governance markdown file containing \"The value of pi is 3.14159.\" in plain prose")

    [<Given>]
    member this.``a repository where a finding key matches a known-false-positives entry in local-tmp``() =
        this.HandleGiven("a repository where a finding key matches a known-false-positives entry in local-tmp")

    [<Given>]
    member this.``a repository where both governance docs list layers 0 through 5 with identical names``() =
        this.HandleGiven("a repository where both governance docs list layers 0 through 5 with identical names")

    [<Given>]
    member this.``a repository where deterministic governance categories return a fixed finding set``() =
        this.HandleGiven("a repository where deterministic governance categories return a fixed finding set")

    [<Given>]
    member this.``a repository where deterministic governance categories return any finding set``() =
        this.HandleGiven("a repository where deterministic governance categories return any finding set")

    [<Given>]
    member this.``a repository where every deterministic governance category reports zero findings``() =
        this.HandleGiven("a repository where every deterministic governance category reports zero findings")

    [<Given>]
    member this.``a repository where every governance document carries the required traceability sections``() =
        this.HandleGiven("a repository where every governance document carries the required traceability sections")

    [<Given>]
    member this.``a repository where the governance docs list layers 0, 1, and 3 with no layer 2``() =
        this.HandleGiven("a repository where the governance docs list layers 0, 1, and 3 with no layer 2")

    [<Given>]
    member this.``a repository where the two governance docs assign different names to the same layer number``() =
        this.HandleGiven("a repository where the two governance docs assign different names to the same layer number")

    [<Given>]
    member this.``a repository where two deterministic governance categories report findings and the rest pass``() =
        this.HandleGiven("a repository where two deterministic governance categories report findings and the rest pass")

    [<Given>]
    member this.``a repository with a convention file that is missing the "(?:## Principles Implemented/Respected" heading)?``
        ()
        =
        this.HandleGiven(
            "a repository with a convention file that is missing the \"## Principles Implemented/Respected\" heading"
        )

    [<Given>]
    member this.``a repository with a development file that is missing the "(?:## Conventions Implemented/Respected" heading)?``
        ()
        =
        this.HandleGiven(
            "a repository with a development file that is missing the \"## Conventions Implemented/Respected\" heading"
        )

    [<Given>]
    member this.``a repository with a governance document split across nested indexed child directories``() =
        this.HandleGiven("a repository with a governance document split across nested indexed child directories")

    [<Given>]
    member this.``a repository with a governance document split into a child directory whose children carry plain kebab-case names``
        ()
        =
        this.HandleGiven(
            "a repository with a governance document split into a child directory whose children carry plain kebab-case names"
        )

    [<Given>]
    member this.``a repository with a principle file that is missing the "(?:## Vision Supported" heading)?``() =
        this.HandleGiven("a repository with a principle file that is missing the \"## Vision Supported\" heading")

    [<Given>]
    member this.``a repository with a workflow file that contains no reference to any \.claude/agents/ file``() =
        this.HandleGiven("a repository with a workflow file that contains no reference to any .claude/agents/ file")

    [<Given>]
    member this.``a repository with an indexed category directory that has no same-named parent document``() =
        this.HandleGiven("a repository with an indexed category directory that has no same-named parent document")

    [<Given>]
    member this.``a repository with forbidden vendor terms in repo-governance prose and also in out-of-scope paths such as build caches, app source, and worktrees``
        ()
        =
        this.HandleGiven(
            "a repository with forbidden vendor terms in repo-governance prose and also in out-of-scope paths such as build caches, app source, and worktrees"
        )

    [<Given>]
    member this.``a split convention whose indexed child carries the required traceability section``() =
        this.HandleGiven("a split convention whose indexed child carries the required traceability section")

    [<When>]
    member this.``the developer runs repo-governance audit``() =
        this.HandleWhen("the developer runs repo-governance audit")

    [<When>]
    member this.``the developer runs repo-governance audit ten consecutive times with a fixed clock``() =
        this.HandleWhen("the developer runs repo-governance audit ten consecutive times with a fixed clock")

    [<When>]
    member this.``the developer runs repo-governance audit with include-category limited to one category``() =
        this.HandleWhen("the developer runs repo-governance audit with include-category limited to one category")

    [<When>]
    member this.``the developer runs repo-governance layer-coherence validate``() =
        this.HandleWhen("the developer runs repo-governance layer-coherence validate")

    [<When>]
    member this.``the developer runs repo-governance traceability validate``() =
        this.HandleWhen("the developer runs repo-governance traceability validate")

    [<When>]
    member this.``the developer runs repo-governance vendor validate on the directory``() =
        this.HandleWhen("the developer runs repo-governance vendor validate on the directory")

    [<When>]
    member this.``the developer runs repo-governance vendor validate on the file``() =
        this.HandleWhen("the developer runs repo-governance vendor validate on the file")

    [<Then>]
    member this.``every run produces byte-identical JSON output``() =
        this.HandleThen("every run produces byte-identical JSON output")

    [<Then>]
    member this.``forbidden vendor terms in build caches, app source, and worktrees do not appear in the result``() =
        this.HandleThen("forbidden vendor terms in build caches, app source, and worktrees do not appear in the result")

    [<Then>]
    member this.``only the listed category appears in the result categories list``() =
        this.HandleThen("only the listed category appears in the result categories list")

    [<Then>]
    member this.``the command exits successfully``() =
        this.HandleThen("the command exits successfully")

    [<Then>]
    member this.``the command exits with a failure code``() =
        this.HandleThen("the command exits with a failure code")

    [<Then>]
    member this.``the layer-coherence output identifies the layer name disagreement``() =
        this.HandleThen("the layer-coherence output identifies the layer name disagreement")

    [<Then>]
    member this.``the layer-coherence output identifies the numbering gap``() =
        this.HandleThen("the layer-coherence output identifies the numbering gap")

    [<Then>]
    member this.``the layer-coherence output reports zero findings``() =
        this.HandleThen("the layer-coherence output reports zero findings")

    [<Then>]
    member this.``the matching finding appears under skipped_false_positives``() =
        this.HandleThen("the matching finding appears under skipped_false_positives")

    [<Then>]
    member this.``the matching finding does not count toward total_findings``() =
        this.HandleThen("the matching finding does not count toward total_findings")

    [<Then>]
    member this.``the output identifies the forbidden term and its location``() =
        this.HandleThen("the output identifies the forbidden term and its location")

    [<Then>]
    member this.``the output reports total_findings equal to the sum of category findings``() =
        this.HandleThen("the output reports total_findings equal to the sum of category findings")

    [<Then>]
    member this.``the output reports total_findings equal to zero across all categories``() =
        this.HandleThen("the output reports total_findings equal to zero across all categories")

    [<Then>]
    member this.``the output reports zero findings``() =
        this.HandleThen("the output reports zero findings")

    [<Then>]
    member this.``the traceability output identifies the missing Conventions Implemented section``() =
        this.HandleThen("the traceability output identifies the missing Conventions Implemented section")

    [<Then>]
    member this.``the traceability output identifies the missing Principles Implemented section``() =
        this.HandleThen("the traceability output identifies the missing Principles Implemented section")

    [<Then>]
    member this.``the traceability output identifies the missing Vision Supported section``() =
        this.HandleThen("the traceability output identifies the missing Vision Supported section")

    [<Then>]
    member this.``the traceability output identifies the missing agent reference``() =
        this.HandleThen("the traceability output identifies the missing agent reference")

    [<Then>]
    member this.``the traceability output reports zero findings``() =
        this.HandleThen("the traceability output reports zero findings")

    [<Then>]
    member this.``the vendor-audit category reports findings only from repo-governance, AGENTS\.md, and CLAUDE\.md``() =
        this.HandleThen(
            "the vendor-audit category reports findings only from repo-governance, AGENTS.md, and CLAUDE.md"
        )

// GENERATED EXACT BINDINGS END

module private FeatureRunner =
    let private readEmbeddedFeature featureFileName =
        let assembly = typeof<RepoGovernanceSteps>.Assembly

        let resourceName =
            assembly.GetManifestResourceNames()
            |> Array.tryFind (fun name -> name.EndsWith("." + featureFileName, StringComparison.Ordinal))
            |> Option.defaultWith (fun () -> failwithf "embedded repo-governance feature not found: %s" featureFileName)

        use stream = assembly.GetManifestResourceStream(resourceName)
        use reader = new StreamReader(stream)
        reader.ReadToEnd().Split('\n')

    let run featureFileName =
        let definitions = StepDefinitions([| typeof<RepoGovernanceSteps> |])

        let feature =
            definitions.GenerateFeature(featureFileName, readEmbeddedFeature featureFileName)

        feature.Scenarios |> Seq.iter (fun scenario -> scenario.Action.Invoke())

[<Theory>]
[<InlineData("repo-governance-audit.feature")>]
[<InlineData("repo-governance-layer-coherence.feature")>]
[<InlineData("repo-governance-traceability-audit.feature")>]
[<InlineData("repo-governance-vendor-audit.feature")>]
let ``repository-governance behaviours have pure Unit proof`` featureFileName = FeatureRunner.run featureFileName

[<Fact>]
let ``pure layer and traceability audits cover malformed and asymmetric documents`` () =
    let architecture =
        "**Layer 0: Vision**\n"
        + "## Layer 0: Principles (conflict)\n"
        + "**Layer 1: Architecture only**\n"
        + "**Layer 999999999999999999999999999999: Overflow**\n"

    let readme = "**Layer 0: Vision**\n**Layer 2: README only**\n"

    let asymmetric =
        auditLayerCoherenceDocuments (
            Map.ofList
                [ "repo-governance/repository-governance-architecture.md", architecture
                  "repo-governance/README.md", readme ]
        )

    Assert.Contains(asymmetric, fun finding -> finding.Kind = KindIntraFileNameConflict)

    Assert.Equal(
        2,
        asymmetric
        |> List.filter (fun finding -> finding.Kind = KindCrossFileNumberMismatch)
        |> List.length
    )

    Assert.Empty(
        auditLayerCoherenceDocuments (
            Map.ofList
                [ "repo-governance/repository-governance-architecture.md", "# No layers\n"
                  "repo-governance/README.md", "# No layers\n" ]
        )
    )

    let missingDocuments = auditLayerCoherenceDocuments Map.empty
    Assert.Equal(2, missingDocuments.Length)

    let trace =
        auditTraceabilityDocuments (
            Map.ofList [ "repo-governance/development/missing.md", "\n# Development without traceability\n" ]
        )

    Assert.Contains(trace, fun finding -> finding.Kind = KindMissingPrinciplesImplemented)
    Assert.Contains(trace, fun finding -> finding.Kind = KindMissingConventionsImplemented)

[<Fact>]
let ``pure vendor scanner covers ignored scopes and resumes prose scanning`` () =
    let content =
        "---\ntitle: Claude Code\n---\n"
        + "Claude Code before <!-- an open comment\nClaude Code hidden\n-->\n"
        + "````\nClaude Code hidden in fence\n```\nClaude Code still hidden\n````\n"
        + "## Platform Binding Examples\nClaude Code hidden in binding section\n"
        + "## Neutral section\nClaude Code visible again\n"
        + "####### Claude Code invalid heading\n#Claude Code invalid heading spacing\n"
        + "`Claude Code` and [neutral](https://Claude Code.example)\n"

    let findings = scanVendorLines "repo-governance/complex.md" content

    Assert.Equal(
        4,
        findings
        |> List.filter (fun finding -> finding.Match = "Claude Code")
        |> List.length
    )

    let scoped =
        scanVendorGovernanceDocuments (
            Map.ofList
                [ "repo-governance\\included.md", "Claude Code\n"
                  "AGENTS.md", "Claude Code\n"
                  "repo-governance/not-markdown.txt", "Claude Code\n"
                  "apps/demo/ignored.md", "Claude Code\n" ]
        )

    Assert.Equal(2, scoped.Length)

[<Fact>]
let ``pure audit core covers keys globs sorting and optional JSON fields`` () =
    let finding category file line message =
        createAuditFinding category file line message

    let supplied =
        [ finding "vendor-audit" "exact.md" 0 "exact"
          finding "vendor-audit" "prefix-middle-tail" 3 "wildcard"
          finding "vendor-audit" "wanted/child.md" 2 "prefix subtree"
          finding "vendor-audit" "root/wanted/child.md" 2 "nested subtree"
          finding "vendor-audit" "root/wanted" 2 "subtree root"
          finding "vendor-audit" "wanted" 2 "segment"
          finding "vendor-audit" "same.md" 2 "z-last"
          finding "vendor-audit" "same.md" 1 "first"
          finding "vendor-audit" "same.md" 2 "a-first"
          finding "vendor-audit" "" 0 "no location" ]

    let runner name (_: AuditOptions) =
        if name = "vendor-audit" then supplied else []

    let options globs =
        { RepoRoot = "/virtual-rhino-repository"
          Skip = []
          IncludeOnly = [ "vendor-audit" ]
          Now = Some "2026-01-01T00:00:00Z"
          KnownFalsePositivesPath = None
          ExcludeGlobs = globs }

    let envelope =
        runAuditCore
            runner
            Set.empty
            "abc1234"
            "2026-01-01T00:00:00Z"
            (options [ "exact.md"; "prefix*middle*tail"; "wanted/**" ])

    Assert.Equal(4, envelope.Result.Categories.Head.Findings.Length)
    Assert.Equal("", auditCategoryCommand "unknown-category")

    [ [ "wrong*tail" ]; [ "prefix*missing*tail" ]; [ "prefix*tail" ] ]
    |> List.iter (fun globs ->
        let result =
            runAuditCore runner Set.empty "abc1234" "2026-01-01T00:00:00Z" (options globs)

        Assert.NotEmpty result.Result.Categories.Head.Findings)

    let json = formatAuditJson envelope
    Assert.Contains("\"line\": 1", json, StringComparison.Ordinal)
    Assert.Contains("\"message\": \"no location\"", json, StringComparison.Ordinal)
