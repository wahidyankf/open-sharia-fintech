module CraneCli.Tests.Unit.Steps.ReportSteps

open System
open System.IO
open TickSpec
open Xunit
open CraneCore.Logic.ReportManager
open CraneCli.Tests.Unit.Steps.BddState

// ---- BDD shared state ----
let mutable private lastReportPath: string = ""
let mutable private currentScope: string = "pdf-to-md"

// ---- BDD Given steps ----

[<Given>]
let ``no existing chain file for scope "([^"]*)"`` (scope: string) =
    currentScope <- scope
    let chainFile = sprintf "local-tmp/.execution-chain-%s" scope

    if File.Exists(chainFile) then
        File.Delete(chainFile)

[<Given>]
let ``a chain file for "([^"]*)" created (\d+) seconds ago with UUID "([^"]*)"``
    (scope: string)
    (seconds: int)
    (uuid: string)
    =
    currentScope <- scope
    let chainFile = sprintf "local-tmp/.execution-chain-%s" scope
    let ts = DateTimeOffset.UtcNow.ToUnixTimeSeconds() - int64 seconds
    Directory.CreateDirectory("local-tmp") |> ignore
    File.WriteAllText(chainFile, sprintf "%d %s" ts uuid)

// ---- BDD When steps ----

[<When>]
let ``I run "crane report init" with scope "([^"]*)"`` (scope: string) =
    currentScope <- scope

    RunWithWriter(fun w ->
        let code =
            match initReport scope "test.pdf" "test.md" with
            | Ok path ->
                lastReportPath <- path
                let opts = System.Text.Json.JsonSerializerOptions()
                opts.DefaultIgnoreCondition <- System.Text.Json.Serialization.JsonIgnoreCondition.WhenWritingNull
                w.WriteLine(System.Text.Json.JsonSerializer.Serialize({| path = path |}, opts))
                0
            | Error msg ->
                eprintfn "Error: %s" msg
                1

        code)

// ---- BDD Then steps ----

[<Then>]
let ``a report file is created in "([^"]*)"`` (dir: string) =
    Assert.True(File.Exists(lastReportPath), sprintf "Report file should exist: %s" lastReportPath)
    Assert.True(lastReportPath.StartsWith(dir), sprintf "Path should start with %s" dir)

[<Then>]
let ``the filename matches the pattern "([^"]*)"`` (_pattern: string) =
    let filename = Path.GetFileName(lastReportPath)
    Assert.True(filename.EndsWith("__audit.md"), sprintf "Filename should end with __audit.md: %s" filename)
    Assert.True(filename.StartsWith(currentScope + "__"), sprintf "Filename should start with scope: %s" filename)
    let parts = filename.Replace("__audit.md", "").Split("__")
    Assert.True(parts.Length >= 3, sprintf "Filename should have at least 3 parts: %s" filename)
    let chain = parts.[1]
    Assert.Matches(@"^[0-9a-f]{6}$", chain)

[<Then>]
let ``the JSON output contains the report path`` () =
    let doc = System.Text.Json.JsonDocument.Parse(LastOutput)
    let path = doc.RootElement.GetProperty("path").GetString()
    Assert.NotEmpty(path)

[<Then>]
let ``the report filename contains "([^"]*)" followed by a new 6-hex UUID`` (prefix: string) =
    let filename = Path.GetFileName(lastReportPath)
    Assert.True(filename.Contains(prefix), sprintf "Filename should contain '%s': %s" prefix filename)

[<Then>]
let ``the report filename contains only the new 6-hex UUID .no "([^"]*)".`` (uuid: string) =
    let filename = Path.GetFileName(lastReportPath)
    Assert.DoesNotContain(uuid, filename)
    // Cleanup
    if File.Exists(lastReportPath) then
        File.Delete(lastReportPath)

    let chainFile = sprintf "local-tmp/.execution-chain-%s" currentScope

    if File.Exists(chainFile) then
        File.Delete(chainFile)
