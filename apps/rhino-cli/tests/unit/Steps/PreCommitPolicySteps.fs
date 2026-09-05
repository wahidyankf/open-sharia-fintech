/// Pure in-process proof of the Markdown policy orchestrated by the
/// repository pre-commit hook. Resource-bound git staging and filesystem
/// traversal remain covered by the Integration adapter.
module RhinoCli.Tests.Unit.Steps.PreCommitPolicySteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/git/git-pre-commit.feature" ]

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application
open RhinoCli.Domain

type PreCommitPolicySteps() =
    let repositoryRoot = Path.GetFullPath("/virtual/rhino-repository")
    let mutable targetFile = ""
    let mutable content = ""
    let mutable output = ""
    let mutable exitCode = 0

    let recordFindings findings =
        output <- Finding.formatText findings
        exitCode <- if Finding.hasBlocking findings then 1 else 0

    [<Given>]
    member _.``staged markdown files contain a link to a non-existent target``() =
        targetFile <- "docs/index.md"
        content <- "# Index\nSee [missing](./does-not-exist.md).\n"

    [<Given>]
    member _.``a staged markdown file under docs containing a mermaid diagram with a label exceeding the maximum length``
        ()
        =
        targetFile <- "docs/diagram.md"

        content <-
            "# Diagram\n\n```mermaid\nflowchart TD\n    A[This label is definitely longer than thirty characters total]\n```\n"

    [<Given>]
    member _.``a staged markdown file under docs containing two H1 headings``() =
        targetFile <- "docs/two-h1.md"
        content <- "# First\n\ntext\n\n# Second\n"

    [<Given>]
    member _.``a staged SKILL.md under .claude/skills with multiple H1 headings``() =
        targetFile <- ".claude/skills/my-skill/SKILL.md"
        content <- "# One\n\n# Two\n\n# Three\n"

    [<Given>]
    member _.``a staged markdown file under plans/done containing a broken internal link``() =
        targetFile <- "plans/done/2024-01-01__old/notes.md"
        content <- "# Notes\nSee [missing](./does-not-exist.md).\n"

    [<When>]
    member _.``the pre-commit hook runs md links validate on staged files``() =
        Md.validateDocsLinksContent repositoryRoot targetFile content [ "plans/done" ] (fun _ -> false) (fun _ -> "")
        |> recordFindings

    [<When>]
    member _.``the pre-commit hook runs md mermaid validate on the staged file``() =
        let blocks = Md.extractMermaidBlocks targetFile content
        let result = Md.validateMermaidBlocks blocks Md.defaultMermaidValidateOptions
        output <- Md.formatMermaidText result false false
        exitCode <- if List.isEmpty result.Violations then 0 else 1

    [<When>]
    member _.``the pre-commit hook runs md heading-hierarchy validate on the staged file``() =
        Md.validateDocsHeadingHierarchyContent targetFile content |> recordFindings

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.Equal(1, exitCode)

    [<Then>]
    member _.``the stderr output identifies the source file containing the broken link``() =
        Assert.Contains(targetFile, output)

    [<Then>]
    member _.``the stderr output identifies the line number of the broken link``() = Assert.Contains("Line 2:", output)

    [<Then>]
    member _.``the stderr output identifies the broken link target``() =
        Assert.Contains("./does-not-exist.md", output)

    [<Then>]
    member _.``the output indicates a mermaid violation was found``() =
        Assert.Contains("[FAIL]", output)
        Assert.Contains("Found 1 violation(s)", output)

    [<Then>]
    member _.``the output indicates a heading hierarchy violation was found``() =
        Assert.Contains("markdown file has 2 H1 headings", output)

    [<Then>]
    member _.``the heading hierarchy step does not block the commit for that file``() = Assert.Equal(0, exitCode)

    [<Then>]
    member _.``the link validation step does not report a broken link for the plans/done file``() =
        Assert.Equal(0, exitCode)
        Assert.DoesNotContain(targetFile, output)

let private runLinkFailure () =
    let steps = PreCommitPolicySteps()
    steps.``staged markdown files contain a link to a non-existent target`` ()
    steps.``the pre-commit hook runs md links validate on staged files`` ()
    steps.``the command exits with a failure code`` ()
    steps.``the stderr output identifies the source file containing the broken link`` ()
    steps.``the stderr output identifies the line number of the broken link`` ()
    steps.``the stderr output identifies the broken link target`` ()

[<Fact>]
let ``Broken-link detection in step 7 reports per-link details`` () = runLinkFailure ()

[<Fact>]
let ``staged malformed mermaid diagram blocks commit`` () =
    let steps = PreCommitPolicySteps()
    steps.``a staged markdown file under docs containing a mermaid diagram with a label exceeding the maximum length`` ()
    steps.``the pre-commit hook runs md mermaid validate on the staged file`` ()
    steps.``the command exits with a failure code`` ()
    steps.``the output indicates a mermaid violation was found`` ()

[<Fact>]
let ``staged docs file with bad heading hierarchy blocks commit`` () =
    let steps = PreCommitPolicySteps()
    steps.``a staged markdown file under docs containing two H1 headings`` ()
    steps.``the pre-commit hook runs md heading-hierarchy validate on the staged file`` ()
    steps.``the command exits with a failure code`` ()
    steps.``the output indicates a heading hierarchy violation was found`` ()

[<Fact>]
let ``staged SKILL file is outside the prose allowlist`` () =
    let steps = PreCommitPolicySteps()
    steps.``a staged SKILL.md under .claude/skills with multiple H1 headings`` ()
    steps.``the pre-commit hook runs md heading-hierarchy validate on the staged file`` ()
    steps.``the heading hierarchy step does not block the commit for that file`` ()

[<Fact>]
let ``plans done exclusion suppresses staged link findings`` () =
    let steps = PreCommitPolicySteps()
    steps.``a staged markdown file under plans/done containing a broken internal link`` ()
    steps.``the pre-commit hook runs md links validate on staged files`` ()
    steps.``the link validation step does not report a broken link for the plans/done file`` ()
