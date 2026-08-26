/// Plain xunit tests for `RhinoCli.Cli.Dispatch.route` — the argv router
/// wired into `RhinoCli.Program.Program.main`. `shadow-diff.sh` already
/// proves the routed leaves byte-match Rust against real repo data; these
/// tests pin `route`'s own argv-parsing and exit-code-mapping behaviour
/// (help scanning, unrecognized routes, repo-root/output-format error
/// branches) with `getRepoRoot` stubbed so no test depends on this
/// checkout's own state.
module RhinoCli.Tests.Unit.Steps.DispatchUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch

let private newTempDir () =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-dispatch-unit-" + Guid.NewGuid().ToString("N"))

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
let private errRoot (message: string) () : Result<string, string> = Error message

// ---- help scanning ----

[<Fact>]
let ``route prints the canonical help text and exits 0 for bare -h`` () =
    let code, out, _ = runCaptured (errRoot "unused") [| "-h" |]
    Assert.Equal(0, code)
    Assert.Equal(RhinoCli.Cli.HelpText.Text, out)

[<Fact>]
let ``route prints help when --help trails a real subcommand`` () =
    let code, out, _ =
        runCaptured (errRoot "unused") [| "convention"; "emoji"; "validate"; "--help" |]

    Assert.Equal(0, code)
    Assert.Equal(RhinoCli.Cli.HelpText.Text, out)

// ---- unrecognized routes ----

[<Fact>]
let ``route exits 2 for an argv shape no flipped namespace recognizes`` () =
    let code, _, err = runCaptured (errRoot "unused") [| "md"; "validate" |]
    Assert.Equal(2, code)
    Assert.Contains("unrecognized or not-yet-routed invocation", err)

// ---- repo-root and output-format error branches ----

[<Fact>]
let ``route surfaces a repo-root lookup failure as exit 1`` () =
    let code, _, err =
        runCaptured (errRoot "not a git repo") [| "convention"; "audit" |]

    Assert.Equal(1, code)
    Assert.Contains("Error: failed to find git repository root: not a git repo", err)

[<Fact>]
let ``route rejects an unknown output format as exit 1`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "convention"; "audit"; "-o"; "xml" |]

    Assert.Equal(1, code)
    Assert.Contains("unknown output format", err)

// ---- convention emoji validate ----

[<Fact>]
let ``route reports PASSED for a clean emoji scan`` () =
    let root = newTempDir ()
    let code, out, _ = runCaptured (okRoot root) [| "convention"; "emoji"; "validate" |]
    Assert.Equal(0, code)
    Assert.Contains("EMOJI AUDIT PASSED", out)

[<Fact>]
let ``route reports FAILED and exit 1 for an emoji finding`` () =
    // U+2713 (check mark), written as an escape rather than a literal
    // glyph, so this file never trips the very emoji-audit gate it is
    // exercising here.
    let root = newTempDir ()
    writeFile root "src/example.ts" "\u2713\n"

    let code, out, err =
        runCaptured (okRoot root) [| "convention"; "emoji"; "validate"; "-o"; "json" |]

    Assert.Equal(1, code)
    Assert.Contains("\"status\": \"failed\"", out)
    Assert.Contains("Error: 1 emoji finding(s) found", err)

// ---- convention license validate ----

[<Fact>]
let ``route reports PASSED when no apps or libs directories exist`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "convention"; "license"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("LICENSE AUDIT PASSED", out)

[<Fact>]
let ``route reports FAILED and exit 1 for a missing LICENSE`` () =
    let root = newTempDir ()
    Directory.CreateDirectory(Path.Combine(root, "apps", "foo")) |> ignore

    let code, out, err =
        runCaptured (okRoot root) [| "convention"; "license"; "validate"; "-o"; "markdown" |]

    Assert.Equal(1, code)
    Assert.Contains("**FAILED**", out)
    Assert.Contains("Error: 1 license finding(s) found", err)

// ---- convention audit ----

[<Fact>]
let ``route passes convention audit when every member passes`` () =
    let root = newTempDir ()
    let code, out, _ = runCaptured (okRoot root) [| "convention"; "audit" |]
    Assert.Equal(0, code)
    Assert.Contains("CONVENTION AUDIT PASSED: all 2 validators passed", out)

[<Fact>]
let ``route fails convention audit and lists the failing member`` () =
    let root = newTempDir ()
    Directory.CreateDirectory(Path.Combine(root, "apps", "foo")) |> ignore
    let code, _, err = runCaptured (okRoot root) [| "convention"; "audit" |]
    Assert.Equal(1, code)
    Assert.Contains("CONVENTION AUDIT FAILED: 1 validator(s) reported failures", err)
    Assert.Contains("license: 1 license finding(s) found", err)
    Assert.Contains("Error: convention audit found 1 failure(s)", err)

[<Fact>]
let ``route passes convention audit when every member is skipped`` () =
    let root = newTempDir ()
    Directory.CreateDirectory(Path.Combine(root, "apps", "foo")) |> ignore

    let code, out, _ =
        runCaptured (okRoot root) [| "convention"; "audit"; "--skip"; "emoji"; "--skip"; "license" |]

    Assert.Equal(0, code)
    Assert.Contains("CONVENTION AUDIT PASSED: all 0 validators passed", out)

// ---- parity manifest generate / validate ----

[<Fact>]
let ``route surfaces a parity generate failure for a non-git repoRoot`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "parity"; "manifest"; "generate" |]
    Assert.Equal(1, code)
    Assert.StartsWith("Error: ", err)

[<Fact>]
let ``route surfaces a parity validate failure for a non-git repoRoot`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "parity"; "manifest"; "validate" |]
    Assert.Equal(1, code)
    Assert.StartsWith("Error: ", err)

// ---- repo-config validate ----

[<Fact>]
let ``route passes repo-config validate for a schema-clean fixture`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" "harness:\n  - name: probe\n    tier: source\n"

    let code, out, _ = runCaptured (okRoot root) [| "repo-config"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("matches the canonical schema", out)

[<Fact>]
let ``route fails repo-config validate and lists the finding`` () =
    let root = newTempDir ()

    writeFile
        root
        "repo-config.yml"
        "harness:\n  - name: probe\n    tier: source\n    ownership:\n      - { path: somewhere, class: vendored, reason: \"\" }\n"

    let code, out, err =
        runCaptured (okRoot root) [| "repo-config"; "validate"; "-o"; "json" |]

    Assert.Equal(1, code)
    Assert.Contains("required non-empty value", out)
    Assert.Contains("Error: repo-config validate: 1 schema finding(s)", err)

[<Fact>]
let ``route surfaces a repo-config validate schema failure to stderr only`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" "harness: \"not-a-list\"\n"

    let code, out, err = runCaptured (okRoot root) [| "repo-config"; "validate" |]

    Assert.Equal(1, code)
    Assert.Equal("", out)
    Assert.StartsWith("Error: repo-config validate: repo-config.yml failed strict schema deserialization", err)

// ---- env init ----

[<Fact>]
let ``route creates a env local file from a discovered example`` () =
    let root = newTempDir ()
    writeFile root "apps/foo/.env.example" "X=1\n"

    let code, out, _ = runCaptured (okRoot root) [| "env"; "init" |]

    Assert.Equal(0, code)
    Assert.Contains("Created: apps/foo/.env.local", out)
    Assert.True(File.Exists(Path.Combine(root, "apps", "foo", ".env.local")))

[<Fact>]
let ``route skips an existing env local file without --force`` () =
    let root = newTempDir ()
    writeFile root "apps/foo/.env.example" "X=1\n"
    writeFile root "apps/foo/.env.local" "X=0\n"

    let code, out, _ = runCaptured (okRoot root) [| "env"; "init" |]

    Assert.Equal(0, code)
    Assert.Contains("Skipped: apps/foo/.env.local", out)

// ---- env backup / env restore ----

[<Fact>]
let ``route backs up a discovered env file to --dir`` () =
    let root = newTempDir ()
    let backupDir = newTempDir ()
    writeFile root ".env" "SECRET=1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "env"; "backup"; "--dir"; backupDir |]

    Assert.Equal(0, code)
    Assert.Contains("Backup complete", out)
    Assert.True(File.Exists(Path.Combine(backupDir, ".env")))

[<Fact>]
let ``route restores a backed-up env file from --dir`` () =
    let root = newTempDir ()
    let backupDir = newTempDir ()
    writeFile backupDir ".env" "SECRET=1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "env"; "restore"; "--dir"; backupDir |]

    Assert.Equal(0, code)
    Assert.Contains("Restore complete", out)
    Assert.True(File.Exists(Path.Combine(root, ".env")))

[<Fact>]
let ``route surfaces a env restore failure for a missing backup dir`` () =
    let root = newTempDir ()
    let missingDir = Path.Combine(newTempDir (), "does-not-exist")

    let code, _, err =
        runCaptured (okRoot root) [| "env"; "restore"; "--dir"; missingDir |]

    Assert.Equal(1, code)
    Assert.Contains("backup dir does not exist", err)

// ---- env validate ----

[<Fact>]
let ``route passes env validate when the contract declares no surfaces`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" "env-contract:\n  surfaces: []\n"

    let code, out, _ = runCaptured (okRoot root) [| "env"; "validate" |]

    Assert.Equal(0, code)
    Assert.Contains("no drift detected", out)

[<Fact>]
let ``route surfaces a env validate contract-load failure`` () =
    let root = newTempDir ()
    writeFile root "repo-config.yml" "harness: []\n"

    let code, _, err = runCaptured (okRoot root) [| "env"; "validate" |]

    Assert.Equal(1, code)
    Assert.Contains("env-contract: section missing", err)
