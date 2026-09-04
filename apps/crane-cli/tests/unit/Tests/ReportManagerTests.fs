module CraneCli.Tests.Unit.Tests.ReportManagerTests

open System
open System.IO
open System.Text.RegularExpressions
open Xunit
open CraneCore.Domain.PdfMetadata
open CraneCore.Domain.Report
open CraneCore.Logic.ReportManager

[<Fact>]
let ``PdfMetadata type has pages field`` () =
    let meta =
        { Pages = 10
          Title = Some "Test"
          Author = None
          File = "test.pdf"
          SizeBytes = 1024L }

    Assert.Equal(10, meta.Pages)

[<Fact>]
let ``SkipListEntry type has md_basename field`` () =
    let entry =
        { MdBasename = "test.md"
          Category = "text-completeness"
          Description = "some text"
          Key = "abc123"
          Accepted = "2026-01-01"
          Reason = "false positive" }

    Assert.Equal("test.md", entry.MdBasename)

[<Fact>]
let ``utc7Timestamp returns a timestamp string`` () =
    let result = utc7Timestamp ()
    Assert.Matches(@"^\d{4}-\d{2}-\d{2}--\d{2}-\d{2}$", result)

// @covers specs/apps/crane/cli/behaviors/reporting/report-management.feature:New chain creates a 6-character UUID report
[<Fact>]
let ``initReport creates a report file in the local-tmp pdf-to-md family directory`` () =
    let scope = sprintf "test-scope-%s" (System.Guid.NewGuid().ToString("N").[..5])

    match initReport scope "test.pdf" "test.md" with
    | Ok path ->
        Assert.True(path.StartsWith("local-tmp/pdf-to-md/"))
        Assert.True(File.Exists(path))
        // Filename matches "{scope}__{6-hex}__{YYYY-MM-DD--HH-MM}__audit.md"
        let fileName = Path.GetFileName(path)

        let pattern =
            sprintf @"^%s__[0-9a-f]{6}__\d{4}-\d{2}-\d{2}--\d{2}-\d{2}__audit\.md$" (Regex.Escape scope)

        Assert.Matches(pattern, fileName)
        // cleanup
        File.Delete(path)
        let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

        if File.Exists(chainFile) then
            File.Delete(chainFile)
    | Error msg -> Assert.Fail(sprintf "initReport failed: %s" msg)

[<Fact>]
let ``finalizeReport returns Error for non-existent report`` () =
    match finalizeReport "nonexistent-report.md" "DONE" with
    | Error _ -> ()
    | Ok() -> Assert.Fail("expected error for non-existent report")

[<Fact>]
let ``finalizeReport updates status in existing report`` () =
    let scope = sprintf "finalize-test-%s" (System.Guid.NewGuid().ToString("N").[..5])

    match initReport scope "test.pdf" "test.md" with
    | Ok path ->
        match finalizeReport path "DONE" with
        | Ok() ->
            let content = File.ReadAllText(path)
            Assert.Contains("Status: DONE", content)
            File.Delete(path)
        | Error msg -> Assert.Fail(sprintf "finalizeReport failed: %s" msg)

        let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

        if File.Exists(chainFile) then
            File.Delete(chainFile)
    | Error msg -> Assert.Fail(sprintf "initReport failed: %s" msg)

[<Fact>]
let ``getOrExtendChain returns same chain within window`` () =
    let scope = sprintf "chain-test-%s" (System.Guid.NewGuid().ToString("N").[..5])
    let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

    try
        let chain1 = getOrExtendChain scope
        let chain2 = getOrExtendChain scope
        // Second call should extend the chain (contain first id)
        Assert.True(chain2.Contains("__"), "Chain should be extended with __")
        Assert.True(chain2.StartsWith(chain1.Split("__").[0]))
    finally
        if File.Exists(chainFile) then
            File.Delete(chainFile)

// @covers specs/apps/crane/cli/behaviors/reporting/report-management.feature:Chain extends when chain file is fresh (< 30s)
[<Fact>]
let ``getOrExtendChain extends existing fresh chain with known id`` () =
    let scope = sprintf "chain-fresh-%s" (System.Guid.NewGuid().ToString("N").[..5])
    let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

    try
        Directory.CreateDirectory("local-tmp") |> ignore
        // Chain file created 5 seconds ago with a known UUID, well inside the 30s window.
        let fiveSecondsAgo = DateTimeOffset.UtcNow.ToUnixTimeSeconds() - 5L
        File.WriteAllText(chainFile, sprintf "%d abc123" fiveSecondsAgo)
        let chain = getOrExtendChain scope
        // Chain should extend "abc123" with a new 6-hex id, not replace it.
        Assert.Matches(@"^abc123__[0-9a-f]{6}$", chain)
    finally
        if File.Exists(chainFile) then
            File.Delete(chainFile)

[<Fact>]
let ``getOrExtendChain starts fresh chain when chain file has invalid format`` () =
    let scope = sprintf "chain-invalid-%s" (System.Guid.NewGuid().ToString("N").[..5])
    let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

    try
        Directory.CreateDirectory("local-tmp") |> ignore
        // Write a chain file with invalid format (no space separator)
        File.WriteAllText(chainFile, "invalidformat")
        let chain = getOrExtendChain scope
        // Should not contain __ since chain starts fresh
        Assert.False(chain.Contains("__"), "Fresh chain should not contain __")
    finally
        if File.Exists(chainFile) then
            File.Delete(chainFile)

// @covers specs/apps/crane/cli/behaviors/reporting/report-management.feature:Chain resets when chain file is stale (>= 30s)
[<Fact>]
let ``getOrExtendChain starts fresh chain when chain file timestamp is too old`` () =
    let scope = sprintf "chain-expired-%s" (System.Guid.NewGuid().ToString("N").[..5])
    let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

    try
        Directory.CreateDirectory("local-tmp") |> ignore
        // Write a chain file with expired timestamp (0 = epoch)
        File.WriteAllText(chainFile, "0 oldchain123")
        let chain = getOrExtendChain scope
        // Old chain should be discarded, new chain starts fresh
        Assert.False(chain.Contains("__"), "Expired chain should not be extended")
    finally
        if File.Exists(chainFile) then
            File.Delete(chainFile)
