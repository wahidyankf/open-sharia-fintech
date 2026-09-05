/// Published-process E2E proof for repository-governance commands.
module RhinoCli.Tests.E2E.Steps.RepoGovernanceProcessSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-audit.feature"
      "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-layer-coherence.feature"
      "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-traceability-audit.feature"
      "specs/apps/rhino/cli/behaviours/repo-governance/repo-governance-vendor-audit.feature" ]

open System
open System.Diagnostics
open System.IO
open System.Text.Json
open TickSpec
open Xunit

type private ProcessResult =
    { ExitCode: int
      Stdout: string
      Stderr: string }

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private executable =
    Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

type RepoGovernanceProcessSteps() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-repo-governance-e2e-" + Guid.NewGuid().ToString("N"))

    let mutable result: ProcessResult option = None
    let mutable auditRuns: string list = []

    let run arguments =
        let info =
            ProcessStartInfo(
                executable,
                WorkingDirectory = root,
                RedirectStandardOutput = true,
                RedirectStandardError = true
            )

        arguments |> List.iter info.ArgumentList.Add
        info.Environment.["RHINO_AUDIT_NOW"] <- "2026-01-01T00:00:00Z"
        info.Environment.["GIT_CONFIG_GLOBAL"] <- "/dev/null"
        info.Environment.["GIT_CONFIG_SYSTEM"] <- "/dev/null"
        use childProcess = Process.Start info
        let stdout = childProcess.StandardOutput.ReadToEnd()
        let stderr = childProcess.StandardError.ReadToEnd()
        childProcess.WaitForExit()

        { ExitCode = childProcess.ExitCode
          Stdout = stdout
          Stderr = stderr }

    do
        Directory.CreateDirectory root |> ignore
        let info = ProcessStartInfo("git", WorkingDirectory = root)
        info.ArgumentList.Add "init"
        info.ArgumentList.Add "--quiet"
        use childProcess = Process.Start info
        childProcess.WaitForExit()
        Assert.Equal(0, childProcess.ExitCode)

    let write (path: string) (content: string) =
        let absolute = Path.Combine(root, path.Replace('/', Path.DirectorySeparatorChar))
        Directory.CreateDirectory(Path.GetDirectoryName absolute) |> ignore
        File.WriteAllText(absolute, content)

    let renderLayers layers =
        layers
        |> List.map (fun (number, name: string) ->
            sprintf "## Layer %d: %s (the %s layer)" number name (name.ToLowerInvariant()))
        |> String.concat "\n\n"
        |> fun body -> "# Governance\n\n" + body + "\n"

    let layers =
        [ 0, "Vision"
          1, "Principles"
          2, "Conventions"
          3, "Development"
          4, "Workflows"
          5, "Glossary" ]

    let writeLayers arch readme =
        write "repo-governance/repository-governance-architecture.md" (renderLayers arch)
        write "repo-governance/README.md" (renderLayers readme)

    let cleanTrace () =
        write "repo-governance/principles/p.md" "# P\n\n## Vision Supported\n"
        write "repo-governance/conventions/c.md" "# C\n\n## Principles Implemented/Respected\n"

        write
            "repo-governance/development/d.md"
            "# D\n\n## Principles Implemented/Respected\n\n## Conventions Implemented/Respected\n"

        write "repo-governance/workflows/w.md" "# W\n\n## Platform Binding Examples\n\n.claude/agents/example.md\n"

    let cleanRepository () =
        writeLayers layers layers
        cleanTrace ()

    let invoke args = result <- Some(run args)

    let outcome () =
        result
        |> Option.defaultWith (fun () -> failwith "published Rhino process did not run")

    let combined () =
        let current = outcome () in current.Stdout + current.Stderr

    let auditJson () =
        JsonDocument.Parse(outcome().Stdout).RootElement

    member private _.HandleGiven(step: string) =
        if step.Contains("both governance docs list layers 0 through 5", StringComparison.Ordinal) then
            writeLayers layers layers
        elif step.Contains("layers 0, 1, and 3", StringComparison.Ordinal) then
            let gapped = [ 0, "Vision"; 1, "Principles"; 3, "Development" ] in writeLayers gapped gapped
        elif step.Contains("assign different names", StringComparison.Ordinal) then
            writeLayers [ 0, "Vision"; 1, "Principles" ] [ 0, "Vision"; 1, "Foundations" ]
        elif step.Contains("every governance document carries", StringComparison.Ordinal) then
            cleanTrace ()
        elif step.Contains("principle file", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/principles/untraced.md" "# Untraced\n"
        elif step.Contains("convention file", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/conventions/untraced.md" "# Untraced\n"
        elif step.Contains("development file", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/development/untraced.md" "# Untraced\n\n## Principles Implemented/Respected\n"
        elif step.Contains("workflow file", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/workflows/unreferenced.md" "# Workflow\n"
        elif step.Contains("split into a child directory", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/conventions/split.md" "# Split\n\n## Principles Implemented/Respected\n"
            write "repo-governance/conventions/split/README.md" "# Index\n"
            write "repo-governance/conventions/split/plain-child.md" "# Child\n"
        elif step.Contains("split across nested", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/conventions/nested.md" "# Nested\n\n## Principles Implemented/Respected\n"
            write "repo-governance/conventions/nested/README.md" "# Index\n"
            write "repo-governance/conventions/nested/deep/fragment.md" "# Child\n"
        elif step.Contains("indexed child carries", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/conventions/carried.md" "# Carried\n"
            write "repo-governance/conventions/carried/README.md" "# Index\n"
            write "repo-governance/conventions/carried/child.md" "# Principles Implemented/Respected\n"
        elif step.Contains("indexed category directory", StringComparison.Ordinal) then
            cleanTrace ()
            write "repo-governance/conventions/category/README.md" "# Index\n"
            write "repo-governance/conventions/category/doc.md" "# Doc\n"
        elif step.Contains("governance markdown file", StringComparison.Ordinal) then
            let body =
                if step.Contains("binding-example fence", StringComparison.Ordinal) then
                    "````md\n```yaml\nharness: Claude Code\n```\n````\n"
                elif step.Contains("code fence", StringComparison.Ordinal) then
                    sprintf
                        "```\n%s\n```\n"
                        (if step.Contains("Skills", StringComparison.Ordinal) then
                             "Skills"
                         else
                             "Claude Code")
                elif step.Contains("under a", StringComparison.Ordinal) then
                    sprintf
                        "## Platform Binding Examples\n\n%s reads this.\n"
                        (if step.Contains("Junie", StringComparison.Ordinal) then
                             "Junie"
                         else
                             "Claude Code")
                elif step.Contains("Skills", StringComparison.Ordinal) then
                    "Skills are declared.\n"
                elif step.Contains("Junie", StringComparison.Ordinal) then
                    "Junie is used.\n"
                elif step.Contains("Amazon Q", StringComparison.Ordinal) then
                    "Amazon Q is used.\n"
                elif step.Contains("Antigravity", StringComparison.Ordinal) then
                    "Antigravity is used.\n"
                elif step.Contains("3.14159", StringComparison.Ordinal) then
                    "The value of pi is 3.14159.\n"
                else
                    "Claude Code is used.\n"

            write "repo-governance/doc.md" ("# Doc\n\n" + body)
        elif step.Contains("directory with no forbidden terms", StringComparison.Ordinal) then
            write "repo-governance/a.md" "# A\n\nVendor-neutral prose.\n"
        elif step.Contains("every deterministic governance category reports zero", StringComparison.Ordinal) then
            cleanRepository ()
        elif step.Contains("forbidden vendor terms in repo-governance prose", StringComparison.Ordinal) then
            cleanRepository ()
            let leak = "# Doc\n\nClaude Code reads this.\n" in

            [ "repo-governance/in.md"
              "AGENTS.md"
              "CLAUDE.md"
              "node_modules/cache.md"
              "apps/demo/source.md"
              "worktrees/side/doc.md" ]
            |> List.iter (fun path -> write path leak)
        elif step.Contains("two deterministic governance categories", StringComparison.Ordinal) then
            cleanRepository ()
            writeLayers [ 0, "Vision"; 2, "Conventions" ] [ 0, "Vision"; 2, "Conventions" ]
            write "repo-governance/principles/untraced.md" "# Missing\n"
        elif step.Contains("fixed finding set", StringComparison.Ordinal) then
            cleanRepository ()
            write "repo-governance/vendor.md" "# Doc\n\nClaude Code is used.\n"
        elif step.Contains("known-false-positives", StringComparison.Ordinal) then
            cleanRepository ()
            write "repo-governance/vendor.md" "# Doc\n\nClaude Code is used.\n"
            let discovery = run [ "repo-governance"; "audit"; "--output"; "json" ]
            use json = JsonDocument.Parse(discovery.Stdout)

            let key =
                json.RootElement.GetProperty("result").GetProperty("categories").EnumerateArray()
                |> Seq.collect (fun category -> category.GetProperty("findings").EnumerateArray())
                |> Seq.head
                |> fun finding -> finding.GetProperty("key").GetString()

            write "local-tmp/.known-false-positives.md" (sprintf "# Known false positives\n\n- `%s`\n" key)
        elif step.Contains("return any finding set", StringComparison.Ordinal) then
            cleanRepository ()
            write "repo-governance/vendor.md" "# Doc\n\nClaude Code is used.\n"
        else
            failwithf "unhandled repo-governance E2E Given: %s" step

    member private _.HandleWhen(step: string) =
        if step.Contains("layer-coherence", StringComparison.Ordinal) then
            invoke [ "repo-governance"; "layer-coherence"; "validate" ]
        elif step.Contains("traceability", StringComparison.Ordinal) then
            invoke [ "repo-governance"; "traceability"; "validate" ]
        elif step.Contains("vendor validate", StringComparison.Ordinal) then
            invoke [ "repo-governance"; "vendor"; "validate"; "repo-governance" ]
        elif step.Contains("ten consecutive times", StringComparison.Ordinal) then
            auditRuns <- [ for _ in 1..10 -> (run [ "repo-governance"; "audit"; "--output"; "json" ]).Stdout ]
            result <- Some(run [ "repo-governance"; "audit"; "--output"; "json" ])
        elif step.Contains("include-category", StringComparison.Ordinal) then
            invoke
                [ "repo-governance"
                  "audit"
                  "--output"
                  "json"
                  "--include-category"
                  "vendor-audit" ]
        elif step.Contains("repo-governance audit", StringComparison.Ordinal) then
            invoke [ "repo-governance"; "audit"; "--output"; "json" ]
        else
            failwithf "unhandled repo-governance E2E When: %s" step

    member private _.HandleThen(step: string) =
        let actual = outcome ()

        if step = "the command exits successfully" then
            Assert.True(actual.ExitCode = 0, combined ())
        elif step = "the command exits with a failure code" then
            Assert.NotEqual(0, actual.ExitCode)
        elif step.Contains("reports zero findings", StringComparison.Ordinal) then
            Assert.Contains("PASSED", combined (), StringComparison.Ordinal)
        elif step.Contains("numbering gap", StringComparison.Ordinal) then
            Assert.Contains("numbering-gap", combined (), StringComparison.Ordinal)
        elif step.Contains("layer name disagreement", StringComparison.Ordinal) then
            Assert.Contains("cross-file-name-mismatch", combined (), StringComparison.Ordinal)
        elif step.Contains("missing Vision Supported", StringComparison.Ordinal) then
            Assert.Contains("missing-vision-supported", combined (), StringComparison.Ordinal)
        elif step.Contains("missing Principles Implemented", StringComparison.Ordinal) then
            Assert.Contains("missing-principles-implemented", combined (), StringComparison.Ordinal)
        elif step.Contains("missing Conventions Implemented", StringComparison.Ordinal) then
            Assert.Contains("missing-conventions-implemented", combined (), StringComparison.Ordinal)
        elif step.Contains("missing agent reference", StringComparison.Ordinal) then
            Assert.Contains("missing-agent-reference", combined (), StringComparison.Ordinal)
        elif step.Contains("forbidden term and its location", StringComparison.Ordinal) then
            Assert.Contains("repo-governance", combined (), StringComparison.Ordinal)
        elif step.Contains("total_findings equal to zero", StringComparison.Ordinal) then
            Assert.Equal(0, auditJson().GetProperty("result").GetProperty("total_findings").GetInt32())
        elif step.Contains("category reports findings only", StringComparison.Ordinal) then
            let json = auditJson () in

            json.GetProperty("result").GetProperty("categories").EnumerateArray()
            |> Seq.filter (fun category -> category.GetProperty("name").GetString() = "vendor-audit")
            |> Seq.collect (fun category -> category.GetProperty("findings").EnumerateArray())
            |> Seq.iter (fun finding ->
                let reported = finding.GetProperty("file").GetString()

                let normalized = reported.Replace('\\', '/')
                let rootMarker = "/" + Path.GetFileName(root) + "/"

                let file =
                    if Path.IsPathRooted reported then
                        let markerIndex = normalized.IndexOf(rootMarker, StringComparison.Ordinal)

                        Assert.True(markerIndex >= 0, sprintf "finding is outside isolated repository: %s" normalized)
                        normalized.Substring(markerIndex + rootMarker.Length)
                    else
                        normalized

                Assert.True(
                    file.StartsWith("repo-governance/", StringComparison.Ordinal)
                    || file = "AGENTS.md"
                    || file = "CLAUDE.md",
                    sprintf "vendor-audit reported out-of-scope file: %s" file
                ))
        elif step.Contains("do not appear", StringComparison.Ordinal) then
            Assert.DoesNotContain("node_modules", outcome().Stdout)
            Assert.DoesNotContain("apps/demo", outcome().Stdout)
            Assert.DoesNotContain("worktrees", outcome().Stdout)
        elif step.Contains("equal to the sum", StringComparison.Ordinal) then
            let resultJson = auditJson().GetProperty("result") in
            let total = resultJson.GetProperty("total_findings").GetInt32() in

            let sum =
                resultJson.GetProperty("categories").EnumerateArray()
                |> Seq.sumBy (fun category -> category.GetProperty("findings").GetArrayLength()) in

            Assert.Equal(sum, total)
        elif step.Contains("byte-identical", StringComparison.Ordinal) then
            Assert.Equal(10, List.length auditRuns)
            Assert.All(auditRuns, fun item -> Assert.Equal(List.head auditRuns, item))
        elif step.Contains("appears under skipped_false_positives", StringComparison.Ordinal) then
            Assert.True(auditJson().GetProperty("result").GetProperty("skipped_false_positives").GetArrayLength() > 0)
        elif step.Contains("does not count toward total_findings", StringComparison.Ordinal) then
            Assert.Equal(0, auditJson().GetProperty("result").GetProperty("total_findings").GetInt32())
        elif step.Contains("only the listed category", StringComparison.Ordinal) then
            let categories = auditJson().GetProperty("result").GetProperty("categories") in
            Assert.Equal(1, categories.GetArrayLength())
            Assert.Equal("vendor-audit", categories.[0].GetProperty("name").GetString())
        else
            failwithf "unhandled repo-governance E2E Then: %s" step

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
    let private directory =
        Path.Combine(repositoryRoot, "specs", "apps", "rhino", "cli", "behaviours", "repo-governance")

    let run featureFileName =
        let path = Path.Combine(directory, featureFileName) in
        let definitions = StepDefinitions([| typeof<RepoGovernanceProcessSteps> |]) in
        let feature = definitions.GenerateFeature(path, File.ReadAllLines path) in
        feature.Scenarios |> Seq.iter (fun scenario -> scenario.Action.Invoke())

[<Theory>]
[<InlineData("repo-governance-audit.feature")>]
[<InlineData("repo-governance-layer-coherence.feature")>]
[<InlineData("repo-governance-traceability-audit.feature")>]
[<InlineData("repo-governance-vendor-audit.feature")>]
let ``published Rhino proves repository-governance behaviours`` featureFileName = FeatureRunner.run featureFileName
