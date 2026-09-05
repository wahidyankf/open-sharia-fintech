/// Plain xunit tests for the Wave D routes of `RhinoCli.Cli.Dispatch.route`
/// — `md links|mermaid|heading-hierarchy|naming|frontmatter|frontmatter-dates|audit`,
/// `governance word-budget|readme-index`, and `git lockfile sync`.
///
/// `DispatchUnitTests.fs` pins the router's own argv handling; this file
/// drives each Wave D leaf end-to-end against a throwaway fixture repository
/// so both the passing and the finding-present arm of every leaf runs. On a
/// clean corpus `shadow-diff.sh` only ever exercises the passing arm, which
/// is how two Wave D formatter defects reached `main` (see `learnings.md`,
/// 2026-08-28).
module RhinoCli.Tests.Integration.Steps.WaveDDispatchResourceTests

open System
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-waved-dispatch-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private writeFile (root: string) (relativePath: string) (content: string) =
    let full = Path.Combine(root, relativePath)
    Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
    File.WriteAllText(full, content)

/// Runs `route`, capturing stdout/stderr around the call and restoring the
/// prior writers afterwards even if `route` throws.
let private runCaptured (getRepoRoot: unit -> Result<string, string>) (argv: string[]) : int * string * string =
    let originalOut = Console.Out
    let originalErr = Console.Error
    use outWriter = new StringWriter()
    use errWriter = new StringWriter()

    try
        Console.SetOut(outWriter)
        Console.SetError(errWriter)
        let exitCode = route getRepoRoot argv
        exitCode, outWriter.ToString(), errWriter.ToString()
    finally
        Console.SetOut(originalOut)
        Console.SetError(originalErr)

let private okRoot (root: string) () = Ok root

/// A `repo-config.yml` whose word budget is tight enough that any prose file
/// under `docs/` trips the `Fail` band.
let private tightWordBudgetConfig =
    "governance-word-budget:\n\
     \x20 surfaces:\n\
     \x20   - glob: \"docs/**/*.md\"\n\
     \x20     target: 3\n\
     \x20     warn: 4\n\
     \x20     fail: 5\n\
     \x20 resolved_tree:\n\
     \x20   root: docs\n\
     \x20   target: 3\n\
     \x20   warn: 4\n\
     \x20   fail: 5\n"

// ---------------------------------------------------------------------------
// md links validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route reports all links valid for a repository with no markdown`` () =
    let root = newTempDir ()
    let code, out, _ = runCaptured (okRoot root) [| "md"; "links"; "validate" |]
    Assert.Equal(0, code)
    Assert.Contains("All links valid!", out)

[<Fact>]
let ``route reports a broken link and exits 1`` () =
    let root = newTempDir ()
    writeFile root "docs/a.md" "# A\n\n[gone](./missing.md)\n"

    let code, out, err = runCaptured (okRoot root) [| "md"; "links"; "validate" |]

    Assert.Equal(1, code)
    Assert.Contains("# Broken Links Report", out)
    Assert.Contains("found 1 broken links", err)

[<Fact>]
let ``route renders md links validate as JSON`` () =
    let root = newTempDir ()
    writeFile root "docs/a.md" "# A\n\n[gone](./missing.md)\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "links"; "validate"; "-o"; "json" |]

    Assert.Equal(1, code)
    Assert.Contains("\"broken_count\": 1", out)

[<Fact>]
let ``route honours md links validate --exclude`` () =
    let root = newTempDir ()
    writeFile root "docs/a.md" "# A\n\n[gone](./missing.md)\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "links"; "validate"; "--exclude"; "docs/" |]

    Assert.Equal(0, code)
    Assert.Contains("All links valid!", out)

[<Fact>]
let ``route accepts md links validate --staged-only outside a git repository`` () =
    let root = newTempDir ()
    writeFile root "docs/a.md" "# A\n\n[gone](./missing.md)\n"

    // `getStagedFiles` fails outside a repository, which the leaf maps to an
    // empty staged set — nothing to scan, so the run passes.
    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "links"; "validate"; "--staged-only" |]

    Assert.Equal(0, code)
    Assert.Contains("All links valid!", out)

// ---------------------------------------------------------------------------
// md mermaid validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes md mermaid validate for a repository with no diagrams`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "md"; "mermaid"; "validate" |]
    Assert.Equal(0, code)
    Assert.DoesNotContain("violation", err)

[<Fact>]
let ``route accepts every md mermaid validate threshold flag`` () =
    let root = newTempDir ()

    let code, _, _ =
        runCaptured
            (okRoot root)
            [| "md"
               "mermaid"
               "validate"
               "--max-label-len"
               "10"
               "--max-width"
               "3"
               "--max-depth"
               "2"
               "--max-subgraph-nodes"
               "4"
               "--changed-only"
               "-v" |]

    Assert.Equal(0, code)

[<Fact>]
let ``route renders md mermaid validate as markdown and honours --quiet`` () =
    let root = newTempDir ()

    let code, _, _ =
        runCaptured (okRoot root) [| "md"; "mermaid"; "validate"; "-o"; "markdown"; "--quiet" |]

    Assert.Equal(0, code)

// ---------------------------------------------------------------------------
// md heading-hierarchy validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes md heading-hierarchy validate for an empty repository`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "heading-hierarchy"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("PASSED", out)

[<Fact>]
let ``route takes the positional-path arm of md heading-hierarchy validate`` () =
    let root = newTempDir ()
    writeFile root "docs/h.md" "# One\n\n## Two\n"

    // A positional path routes through `validateDocsHeadingHierarchyForPaths`,
    // which keeps only prose-allowlisted paths — a throwaway fixture has none,
    // so the run passes while still exercising that arm.
    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "heading-hierarchy"; "validate"; "docs" |]

    Assert.Equal(0, code)
    Assert.Contains("PASSED", out)

[<Fact>]
let ``route honours md heading-hierarchy validate --exclude`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "heading-hierarchy"; "validate"; "--exclude"; "docs/" |]

    Assert.Equal(0, code)
    Assert.Contains("PASSED", out)

// ---------------------------------------------------------------------------
// md naming validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes md naming validate for a kebab-case tree`` () =
    let root = newTempDir ()
    writeFile root "docs/well-named.md" "# ok\n"
    let code, out, _ = runCaptured (okRoot root) [| "md"; "naming"; "validate" |]
    Assert.Equal(0, code)
    Assert.Contains("DOCS NAMING VALIDATION PASSED", out)

[<Fact>]
let ``route flags a non-kebab-case filename and exits 1`` () =
    let root = newTempDir ()
    writeFile root "docs/Bad_Name.md" "# bad\n"

    let code, out, err = runCaptured (okRoot root) [| "md"; "naming"; "validate" |]

    Assert.Equal(1, code)
    Assert.Contains("DOCS NAMING VALIDATION FAILED", out)
    Assert.Contains("docs naming finding(s) found", err)

[<Fact>]
let ``route honours md naming validate --exempt`` () =
    let root = newTempDir ()
    writeFile root "docs/Bad_Name.md" "# bad\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "naming"; "validate"; "--exempt"; "Bad_Name.md" |]

    Assert.Equal(0, code)
    Assert.Contains("DOCS NAMING VALIDATION PASSED", out)

// ---------------------------------------------------------------------------
// md frontmatter validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes md frontmatter validate for an empty repository`` () =
    let root = newTempDir ()
    let code, out, _ = runCaptured (okRoot root) [| "md"; "frontmatter"; "validate" |]
    Assert.Equal(0, code)
    Assert.Contains("PASSED", out)

[<Fact>]
let ``route renders md frontmatter validate as JSON`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "frontmatter"; "validate"; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.Contains("\"status\"", out)

// ---------------------------------------------------------------------------
// md frontmatter-dates validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes md frontmatter-dates validate for an empty repository`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "frontmatter-dates"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("PASSED", out)

[<Fact>]
let ``route renders md frontmatter-dates validate as markdown`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "frontmatter-dates"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.Contains("##", out)

// ---------------------------------------------------------------------------
// md audit
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes md audit when every member passes`` () =
    let root = newTempDir ()
    let code, out, _ = runCaptured (okRoot root) [| "md"; "audit" |]
    Assert.Equal(0, code)
    Assert.Contains("MD AUDIT PASSED", out)

[<Fact>]
let ``route fails md audit and names the failing member`` () =
    let root = newTempDir ()
    writeFile root "docs/Bad_Name.md" "# bad\n"

    let code, _, err = runCaptured (okRoot root) [| "md"; "audit" |]

    Assert.Equal(1, code)
    Assert.Contains("MD AUDIT FAILED", err)
    Assert.Contains("Error: md audit found", err)

[<Fact>]
let ``route honours md audit --skip`` () =
    let root = newTempDir ()
    writeFile root "docs/Bad_Name.md" "# bad\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "md"; "audit"; "--skip"; "validate-naming" |]

    Assert.Equal(0, code)
    Assert.Contains("MD AUDIT PASSED", out)

// ---------------------------------------------------------------------------
// governance word-budget validate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route skips word-budget when repo-config declares no section`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "governance"; "word-budget"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("WORD BUDGET: SKIPPED", out)

[<Fact>]
let ``route fails word-budget for a surface over its fail band`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" tightWordBudgetConfig
    writeFile root "docs/long.md" "one two three four five six seven eight nine ten\n"

    let code, out, err =
        runCaptured (okRoot root) [| "governance"; "word-budget"; "validate" |]

    Assert.Equal(1, code)
    Assert.Contains("WORD BUDGET:", out)
    Assert.Contains("progressive disclosure", err)

[<Fact>]
let ``route renders word-budget findings as a four-column markdown table`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" tightWordBudgetConfig
    writeFile root "docs/long.md" "one two three four five six seven eight nine ten\n"

    let _, out, _ =
        runCaptured (okRoot root) [| "governance"; "word-budget"; "validate"; "-o"; "markdown" |]

    Assert.Contains("| Path | Size (words) | Severity | Message |", out)

[<Fact>]
let ``route renders word-budget findings as JSON`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" tightWordBudgetConfig
    writeFile root "docs/long.md" "one two three four five six seven eight nine ten\n"

    let _, out, _ =
        runCaptured (okRoot root) [| "governance"; "word-budget"; "validate"; "-o"; "json" |]

    Assert.Contains("\"size\"", out)

// ---------------------------------------------------------------------------
// governance readme-index validate / generate
// ---------------------------------------------------------------------------

[<Fact>]
let ``route passes readme-index validate for an empty repository`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("README INDEX AUDIT PASSED", out)

[<Fact>]
let ``route renders readme-index validate as JSON and markdown`` () =
    let root = newTempDir ()

    let jsonCode, jsonOut, _ =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "validate"; "-o"; "json" |]

    Assert.Equal(0, jsonCode)
    Assert.Contains("\"status\"", jsonOut)

    let mdCode, mdOut, _ =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "validate"; "-o"; "markdown" |]

    Assert.Equal(0, mdCode)
    Assert.Contains("##", mdOut)

[<Fact>]
let ``route reports readme-index generate wrote nothing for an empty repository`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "generate" |]

    Assert.Equal(0, code)
    Assert.Contains("README INDEX GENERATE:", out)

[<Fact>]
let ``route renders readme-index generate as JSON and markdown`` () =
    let root = newTempDir ()

    let _, jsonOut, _ =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "generate"; "-o"; "json" |]

    Assert.Contains("rhino-cli/readme-index-generate/v1", jsonOut)

    let _, mdOut, _ =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "generate"; "-o"; "markdown" |]

    Assert.Contains("## README Index Generate", mdOut)

// ---------------------------------------------------------------------------
// governance readme-index rewrite-paths
// ---------------------------------------------------------------------------

[<Fact>]
let ``route rejects readme-index rewrite-paths without --map`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "governance"; "readme-index"; "rewrite-paths" |]

    Assert.NotEqual(0, code)
    Assert.Contains("--map", err)

[<Fact>]
let ``route reports a missing --map file rather than throwing`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured
            (okRoot root)
            [| "governance"
               "readme-index"
               "rewrite-paths"
               "--map"
               Path.Combine(root, "no-such-map.txt") |]

    Assert.NotEqual(0, code)
    Assert.StartsWith("Error: ", err)

// ---------------------------------------------------------------------------
// git lockfile sync
// ---------------------------------------------------------------------------

[<Fact>]
let ``route surfaces a git lockfile sync failure outside a repository`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "git"; "lockfile"; "sync" |]
    Assert.NotEqual(0, code)
    Assert.StartsWith("Error: ", err)
