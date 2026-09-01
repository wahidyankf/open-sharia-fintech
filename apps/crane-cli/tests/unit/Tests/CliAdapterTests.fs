module CraneCli.Tests.Unit.Tests.CliAdapterTests

/// Exercises CraneCli.Adapters.In.CliAdapter.run end-to-end (Argu parsing + command
/// dispatch), the only place where "crane pdf info/type", "crane check-all", and
/// "crane --version" are wired together. These commands have no dedicated
/// Core.Logic function of their own to unit test directly, and the integration
/// test project's TickSpec Steps/*.fs files never execute (Suite.fs's gherkinRoot
/// fallback path is stale — it looks for "behavior/cli/gherkin", which does not
/// exist, instead of "cli/behaviors" — so it always falls back to a
/// single no-op placeholder scenario). run() itself is public and safe to call
/// directly with a FakePdfAdapter, so these scenarios are exercised here instead.
open System
open System.IO
open System.Text.Json
open Xunit
open CraneCore.Ports
open CraneCore.Adapters.Out.PdfAdapter
open CraneCli.Adapters.In.CliAdapter

/// Redirects Console.Out for the duration of `f`, returning its captured output
/// alongside the exit code. Safe because this test assembly runs with
/// maxParallelThreads = 1 (see tests/unit/xunit.runner.json).
let private withCapturedOutput (f: unit -> int) : string * int =
    let original = Console.Out
    use sw = new StringWriter()
    Console.SetOut(sw)

    try
        let code = f ()
        (sw.ToString(), code)
    finally
        Console.SetOut(original)

let private withTempMdFile (content: string) (f: string -> unit) =
    let path =
        Path.Combine(Path.GetTempPath(), sprintf "crane-cli-adapter-test-%s.md" (Guid.NewGuid().ToString("N").[..11]))

    File.WriteAllText(path, content)

    try
        f path
    finally
        if File.Exists(path) then
            File.Delete(path)

// @covers specs/apps/crane/cli/behaviors/pdf/pdf-commands.feature:Get page count from text PDF
[<Fact>]
let ``run pdf info returns pages and size_bytes as valid JSON`` () =
    let adapter = FakePdfAdapter("sample pdf text content", 42, 123456L) :> IPdfPort

    let output, _ =
        withCapturedOutput (fun () -> run adapter [| "pdf"; "--info"; "fake.pdf" |])

    use doc = JsonDocument.Parse(output)
    Assert.Equal(42, doc.RootElement.GetProperty("pages").GetInt32())
    Assert.True(doc.RootElement.GetProperty("size_bytes").GetInt64() > 0L)

// @covers specs/apps/crane/cli/behaviors/pdf/pdf-commands.feature:Text-based PDF is detected
[<Fact>]
let ``run pdf type returns type text and exit code 0 for word-rich sample`` () =
    let wordRichText = String.replicate 12 "word "
    let adapter = FakePdfAdapter(wordRichText, 3, 1000L) :> IPdfPort

    let output, code =
        withCapturedOutput (fun () -> run adapter [| "pdf"; "--type"; "fake.pdf" |])

    Assert.Contains("\"type\":\"text\"", output)
    Assert.Equal(0, code)

// @covers specs/apps/crane/cli/behaviors/pdf/pdf-commands.feature:Image-only PDF is detected
[<Fact>]
let ``run pdf type returns type image and exit code 1 for sparse sample`` () =
    let sparseText = "scan noise"
    let adapter = FakePdfAdapter(sparseText, 5, 2000L) :> IPdfPort

    let output, code =
        withCapturedOutput (fun () -> run adapter [| "pdf"; "--type"; "fake.pdf" |])

    Assert.Contains("\"type\":\"image\"", output)
    Assert.Equal(1, code)

// @covers specs/apps/crane/cli/behaviors/system/check-all.feature:Aggregator with matching PDF and MD produces no findings
[<Fact>]
let ``run check-all returns empty findings and exit code 0 when PDF and MD match`` () =
    let sampleText = "no headings or tables or figures appear in this content"
    let adapter = FakePdfAdapter(sampleText, 1, 500L) :> IPdfPort

    withTempMdFile sampleText (fun mdPath ->
        let output, code =
            withCapturedOutput (fun () -> run adapter [| "check-all"; "fake.pdf"; mdPath |])

        Assert.Equal("[]", output.Trim())
        Assert.Equal(0, code))

// @covers specs/apps/crane/cli/behaviors/system/check-all.feature:Aggregator with mismatched MD produces findings tagged by dimension
[<Fact>]
let ``run check-all returns findings and exit code 1 when MD is missing PDF content`` () =
    let sampleText = "no headings or tables or figures appear in this content"
    let adapter = FakePdfAdapter(sampleText, 1, 500L) :> IPdfPort

    withTempMdFile "completely unrelated markdown content with different information" (fun mdPath ->
        let output, code =
            withCapturedOutput (fun () -> run adapter [| "check-all"; "fake.pdf"; mdPath |])

        Assert.NotEqual<string>("[]", output.Trim())
        Assert.Equal(1, code))

// @covers specs/apps/crane/cli/behaviors/system/version.feature:--version prints a version string
[<Fact>]
let ``run --version prints a SemVer-shaped version string`` () =
    let adapter = FakePdfAdapter("", 0, 0L) :> IPdfPort
    let output, code = withCapturedOutput (fun () -> run adapter [| "--version" |])
    Assert.Matches(@"^\d+\.\d+\.\d+", output.Trim())
    Assert.Equal(0, code)
