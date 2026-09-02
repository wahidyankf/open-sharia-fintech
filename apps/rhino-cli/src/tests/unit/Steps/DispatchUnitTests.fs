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

[<Fact>]
let ``route fails env validate and lists a declared-but-unread finding`` () =
    let root = newTempDir ()

    writeFile
        root
        "repo-config.yml"
        "env-contract:\n  surfaces:\n    - root: surface\n      kind: app\n      lang: rust\n      allowlist: []\n"

    writeFile root "surface/.env.example" "UNREAD_KEY=some-value\n"
    writeFile root "surface/src/main.rs" "fn main() {}\n"

    let code, _, err = runCaptured (okRoot root) [| "env"; "validate" |]

    Assert.Equal(1, code)
    Assert.Contains("DRIFT  surface  declared-but-unread  UNREAD_KEY", err)
    Assert.Contains("Error: env validate: 1 finding(s)", err)

[<Fact>]
let ``route passes env validate in warn-only mode despite findings`` () =
    let root = newTempDir ()

    writeFile
        root
        "repo-config.yml"
        "env-contract:\n  surfaces:\n    - root: surface\n      kind: app\n      lang: rust\n      allowlist: []\n"

    writeFile root "surface/.env.example" "UNREAD_KEY=some-value\n"
    writeFile root "surface/src/main.rs" "fn main() {}\n"

    let code, _, err = runCaptured (okRoot root) [| "env"; "validate"; "--warn-only" |]

    Assert.Equal(0, code)
    Assert.Contains("warn-only mode, not failing", err)

// ---- env backup / env restore: worktree-aware, resolve-dir, json/markdown output ----

let private runGit (cwd: string) (args: string list) : unit =
    use proc = new Diagnostics.Process()
    proc.StartInfo.FileName <- "git"
    args |> List.iter proc.StartInfo.ArgumentList.Add
    proc.StartInfo.WorkingDirectory <- cwd
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false
    proc.StartInfo.EnvironmentVariables.Remove("GIT_DIR")
    proc.StartInfo.EnvironmentVariables.Remove("GIT_WORK_TREE")
    proc.Start() |> ignore
    let stderr = proc.StandardError.ReadToEnd()
    proc.WaitForExit()

    if proc.ExitCode <> 0 then
        failwithf "git %s failed in %s: %s" (String.concat " " args) cwd stderr

let private newGitRepoFixture () : string =
    let dir = newTempDir ()
    runGit dir [ "init"; "-q"; "-b"; "main" ]
    runGit dir [ "config"; "user.name"; "Rhino CLI Test" ]
    runGit dir [ "config"; "user.email"; "rhino-cli-test@example.invalid" ]
    dir

let private withHome (value: string option) (body: unit -> unit) =
    let original = Environment.GetEnvironmentVariable("HOME")

    try
        Environment.SetEnvironmentVariable("HOME", (value |> Option.defaultValue null))
        body ()
    finally
        Environment.SetEnvironmentVariable("HOME", original)

[<Fact>]
let ``route applies --worktree-aware for env backup at a real git root`` () =
    let root = newGitRepoFixture ()
    let backupDir = newTempDir ()
    writeFile root ".env" "SECRET=1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "env"; "backup"; "--dir"; backupDir; "--worktree-aware" |]

    Assert.Equal(0, code)
    Assert.Contains("Backup complete", out)

[<Fact>]
let ``route surfaces a env backup worktree detection failure`` () =
    let root = newTempDir ()
    let backupDir = newTempDir ()
    writeFile root ".env" "SECRET=1\n"

    let code, _, err =
        runCaptured (okRoot root) [| "env"; "backup"; "--dir"; backupDir; "--worktree-aware" |]

    Assert.Equal(1, code)
    Assert.Contains("worktree detection failed", err)

[<Fact>]
let ``route surfaces a env backup failure when --dir is inside the repo root`` () =
    let root = newTempDir ()
    writeFile root ".env" "SECRET=1\n"
    let insideDir = Path.Combine(root, "backup")

    let code, _, err =
        runCaptured (okRoot root) [| "env"; "backup"; "--dir"; insideDir |]

    Assert.Equal(1, code)
    Assert.Contains("is inside repo root", err)

[<Fact>]
let ``route surfaces a env backup resolve-dir failure when HOME is unset`` () =
    let root = newTempDir ()
    writeFile root ".env" "SECRET=1\n"

    withHome None (fun () ->
        let code, _, err = runCaptured (okRoot root) [| "env"; "backup" |]
        Assert.Equal(1, code)
        Assert.Contains("HOME not set", err))

[<Fact>]
let ``route surfaces a env restore resolve-dir failure when HOME is unset`` () =
    let root = newTempDir ()

    withHome None (fun () ->
        let code, _, err = runCaptured (okRoot root) [| "env"; "restore" |]
        Assert.Equal(1, code)
        Assert.Contains("HOME not set", err))

[<Fact>]
let ``route prints json output for env backup`` () =
    let root = newTempDir ()
    let backupDir = newTempDir ()
    writeFile root ".env" "SECRET=1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "env"; "backup"; "--dir"; backupDir; "-o"; "json" |]

    Assert.Equal(0, code)
    Assert.Contains("\"direction\": \"backup\"", out)

[<Fact>]
let ``route prints markdown output for env restore`` () =
    let root = newTempDir ()
    let backupDir = newTempDir ()
    writeFile backupDir ".env" "SECRET=1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "env"; "restore"; "--dir"; backupDir; "-o"; "markdown" |]

    Assert.Equal(0, code)
    Assert.Contains("## Restore Report", out)

// ---- env staged-guard validate ----

[<Fact>]
let ``route blocks env staged-guard validate when a real .env file is staged`` () =
    let root = newGitRepoFixture ()
    writeFile root ".env" "SECRET=1\n"
    runGit root [ "add"; ".env" ]

    let code, out, err =
        runCaptured (okRoot root) [| "env"; "staged-guard"; "validate" |]

    Assert.Equal(1, code)
    Assert.Contains(".env", out)
    Assert.Contains("offending .env file(s) staged", err)

[<Fact>]
let ``route passes env staged-guard validate when only .env.example is staged`` () =
    let root = newGitRepoFixture ()
    writeFile root ".env.example" "X=1\n"
    runGit root [ "add"; ".env.example" ]

    let code, _, _ = runCaptured (okRoot root) [| "env"; "staged-guard"; "validate" |]

    Assert.Equal(0, code)

[<Fact>]
let ``route surfaces a env staged-guard validate failure for a non-git repoRoot`` () =
    let root = newTempDir ()

    let code, _, err = runCaptured (okRoot root) [| "env"; "staged-guard"; "validate" |]

    Assert.Equal(1, code)
    Assert.StartsWith("Error: ", err)

// ---- doctor ----

[<Fact>]
let ``route rejects an unknown doctor tool selection before probing`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "doctor"; "--tools"; "bogus-tool-xyz" |]

    Assert.Equal(1, code)
    Assert.Contains("Error: unknown Doctor tool", err)

[<Fact>]
let ``route reports doctor json output for a minimal-scope single-tool selection`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "doctor"; "-o"; "json"; "--scope"; "minimal"; "--tools"; "git" |]

    Assert.Equal(0, code)
    Assert.Contains("\"status\"", out)
    Assert.Contains("\"scope\": \"minimal\"", out)

[<Fact>]
let ``route reports doctor markdown output for a minimal-scope single-tool selection`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "doctor"; "-o"; "markdown"; "--scope"; "minimal"; "--tools"; "git" |]

    Assert.Equal(0, code)
    Assert.Contains("## Doctor Report", out)

[<Fact>]
let ``route reports doctor text output without a target-share section outside a git repository`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "doctor"; "--scope"; "minimal"; "--tools"; "git" |]

    Assert.Equal(0, code)
    Assert.DoesNotContain("Target-share:", out)

[<Fact>]
let ``route runs the target-share step against a real git repository root`` () =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Error message -> Assert.Fail(sprintf "expected findRoot Ok, got Error %s" message)
    | Ok realRepoRoot ->
        let code, out, _ =
            runCaptured (okRoot realRepoRoot) [| "doctor"; "--scope"; "minimal"; "--tools"; "git" |]

        Assert.Equal(0, code)
        Assert.Contains("Target-share:", out)

[<Fact>]
let ``route runs doctor with no --tools selection at all`` () =
    let root = newTempDir ()

    let code, out, _ =
        runCaptured (okRoot root) [| "doctor"; "-o"; "json"; "--scope"; "minimal" |]

    Assert.True(code = 0 || code = 1, sprintf "expected exit 0 or 1, got %d" code)
    Assert.Contains("\"status\"", out)

[<Fact>]
let ``route runs doctor --fix --prune-cargo-cache --dry-run against a crate-free git repo`` () =
    // A fresh `git init` fixture has neither `apps/` nor `libs/`, so
    // `discoverCrates` finds zero crates — `Doctor.fixTargetShares` is then
    // a guaranteed no-op (nothing to symlink) and `pruneOrphans`/`sweepStale`
    // only ever look under this fixture's own never-before-seen repo-name
    // namespace in the shared cache, so this exercises the doctor `--fix` /
    // `--prune-cargo-cache` target-share wiring without mutating anything
    // outside this temp directory.
    let root = newGitRepoFixture ()

    let code, out, _ =
        runCaptured
            (okRoot root)
            [| "doctor"
               "--scope"
               "minimal"
               "--tools"
               "git"
               "--fix"
               "--prune-cargo-cache"
               "--dry-run" |]

    Assert.Equal(0, code)
    Assert.Contains("Target-share:", out)
    Assert.Contains("Target-share fix:", out)
    Assert.Contains("Nothing to fix", out)

// ---- test-coverage validate ----

[<Fact>]
let ``route reports the clap-style missing-arguments error for bare test-coverage validate`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "test-coverage"; "validate" |]

    Assert.Equal(2, code)
    Assert.Contains("<COVERAGE_FILE>", err)
    Assert.Contains("<THRESHOLD>", err)
    Assert.Contains("Usage: rhino-cli test-coverage validate <COVERAGE_FILE> <THRESHOLD>", err)

[<Fact>]
let ``route echoes --help in the missing-arguments usage line`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "--help" |]

    Assert.Equal(2, code)
    Assert.Contains("Usage: rhino-cli test-coverage validate --help <COVERAGE_FILE> <THRESHOLD>", err)

[<Fact>]
let ``route echoes --output <OUTPUT> in the missing-arguments usage line`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "-o"; "json" |]

    Assert.Equal(2, code)
    Assert.Contains("Usage: rhino-cli test-coverage validate --output <OUTPUT> <COVERAGE_FILE> <THRESHOLD>", err)

[<Fact>]
let ``route echoes --verbose in the missing-arguments usage line`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "test-coverage"; "validate"; "-v" |]

    Assert.Equal(2, code)
    Assert.Contains("Usage: rhino-cli test-coverage validate --verbose <COVERAGE_FILE> <THRESHOLD>", err)

[<Fact>]
let ``route echoes --quiet in the missing-arguments usage line`` () =
    let root = newTempDir ()
    let code, _, err = runCaptured (okRoot root) [| "test-coverage"; "validate"; "-q" |]

    Assert.Equal(2, code)
    Assert.Contains("Usage: rhino-cli test-coverage validate --quiet <COVERAGE_FILE> <THRESHOLD>", err)

[<Fact>]
let ``route echoes --no-color in the missing-arguments usage line`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "--no-color" |]

    Assert.Equal(2, code)
    Assert.Contains("Usage: rhino-cli test-coverage validate --no-color <COVERAGE_FILE> <THRESHOLD>", err)

[<Fact>]
let ``route reports only the missing threshold when the coverage file positional is already given`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "cover.out" |]

    Assert.Equal(2, code)
    Assert.DoesNotContain("  <COVERAGE_FILE>\n", err)
    Assert.Contains("  <THRESHOLD>\n", err)

[<Fact>]
let ``route surfaces a repo-root lookup failure for test-coverage validate`` () =
    let code, _, err =
        runCaptured (errRoot "boom") [| "test-coverage"; "validate"; "cover.out"; "50" |]

    Assert.Equal(1, code)
    Assert.Contains("Error: failed to find git repository root: boom", err)

[<Fact>]
let ``route rejects a non-numeric threshold`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "cover.out"; "not-a-number" |]

    Assert.Equal(1, code)
    Assert.Contains("Error: invalid threshold \"not-a-number\"", err)

[<Fact>]
let ``route surfaces a TestCoverage.validate error for a missing coverage file`` () =
    let root = newTempDir ()

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "does-not-exist.out"; "50" |]

    Assert.Equal(1, code)
    Assert.StartsWith("Error: ", err)

[<Fact>]
let ``route passes test-coverage validate text output for coverage at the threshold`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "cover.out"; "50" |]

    Assert.Equal(0, code)
    Assert.Contains("100.00%", out)

[<Fact>]
let ``route passes test-coverage validate json output`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "-o"; "json"; "cover.out"; "50" |]

    Assert.Equal(0, code)
    Assert.Contains("\"pct\"", out)

[<Fact>]
let ``route passes test-coverage validate markdown output`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "-o"; "markdown"; "cover.out"; "50" |]

    Assert.Equal(0, code)
    Assert.Contains("## Coverage Report", out)

[<Fact>]
let ``route passes test-coverage validate with per-file and exclude flags`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\nbar.go:1.1,2.2 1 1\n"

    let code, out, _ =
        runCaptured
            (okRoot root)
            [| "test-coverage"
               "validate"
               "--per-file"
               "--exclude"
               "nomatch/**"
               "cover.out"
               "50" |]

    Assert.Equal(0, code)
    Assert.Contains("100.00%", out)

[<Fact>]
let ``route passes test-coverage validate with a valid below-threshold filter`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, _, _ =
        runCaptured
            (okRoot root)
            [| "test-coverage"
               "validate"
               "--per-file"
               "--below-threshold"
               "10"
               "cover.out"
               "50" |]

    Assert.Equal(0, code)

[<Fact>]
let ``route ignores an unparseable below-threshold value`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, _, _ =
        runCaptured
            (okRoot root)
            [| "test-coverage"
               "validate"
               "--below-threshold"
               "not-a-number"
               "cover.out"
               "50" |]

    Assert.Equal(0, code)

[<Fact>]
let ``route fails test-coverage validate when coverage is below the threshold`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 0\n"

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "cover.out"; "50" |]

    Assert.Equal(1, code)
    Assert.Contains("Error: coverage 0.00% is below threshold 50%", err)
    Assert.StartsWith("Error: ", err)

[<Fact>]
let ``route prints help for test-coverage validate when positionals are already satisfied`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, out, _ =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "cover.out"; "50"; "--help" |]

    Assert.Equal(0, code)
    Assert.Equal(RhinoCli.Cli.HelpText.Text, out)

[<Fact>]
let ``route rejects an unknown output format for test-coverage validate`` () =
    let root = newTempDir ()
    writeFile root "cover.out" "mode: set\nfoo.go:1.1,2.2 1 1\n"

    let code, _, err =
        runCaptured (okRoot root) [| "test-coverage"; "validate"; "cover.out"; "50"; "-o"; "xml" |]

    Assert.Equal(1, code)
    Assert.Contains("unknown output format", err)

// ---- test-contract policy leaves ----
//
// The four policy verbs share one leaf, so these cases pin the leaf's own
// argv handling once and then prove each verb reaches its own engine. They
// drive `route` in-process against the repository's checked-in corpora; no
// child process is spawned.

/// Runs one policy verb against the real repository root, where the four
/// corpora live, and returns the leaf's exit code with its captured streams.
let private runPolicyVerb (check: string) (fixture: string) : int * string * string =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Error message -> failwithf "expected findRoot Ok, got Error %s" message
    | Ok realRepoRoot ->
        runCaptured (okRoot realRepoRoot) [| "test-contract"; check; "validate"; "--fixture"; fixture |]

[<Fact>]
let ``route validates a conforming layout document and exits 0`` () =
    let code, out, _ = runPolicyVerb "layout" "e2e-only-project.json"
    Assert.Equal(0, code)
    Assert.Contains("native-layout-valid", out)

[<Fact>]
let ``route reports a layout contract failure as exit 1`` () =
    let code, _, err = runPolicyVerb "layout" "executable-test-in-src.json"
    Assert.Equal(1, code)
    Assert.Contains("layout-test-in-forbidden-directory", err)

[<Fact>]
let ``route validates a conforming manifest document and exits 0`` () =
    let code, out, _ = runPolicyVerb "manifest" "retained-web-app.json"
    Assert.Equal(0, code)
    Assert.Contains("native-manifest-valid", out)

[<Fact>]
let ``route reports a manifest contract failure as exit 1`` () =
    let code, _, err = runPolicyVerb "manifest" "invalid-consumer-nx-discovery.json"
    Assert.Equal(1, code)
    Assert.Contains("manifest-invalid-consumer", err)

[<Fact>]
let ``route reaches the coverage engine and reports its diagnostic`` () =
    let code, _, err = runPolicyVerb "coverage" "98-percent.json"
    Assert.Equal(1, code)
    Assert.Contains("coverage-below-floor", err)

[<Fact>]
let ``route reaches the bdd engine and reports its diagnostic`` () =
    let code, _, err = runPolicyVerb "bdd" "missing-binding.json"
    Assert.Equal(1, code)
    Assert.Contains("bdd-", err)

[<Fact>]
let ``a policy verb without --fixture or --project is CLI misuse`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "test-contract"; "coverage"; "validate" |]

    Assert.Equal(2, code)
    Assert.Contains("one of --fixture or --project is required", err)
    Assert.Contains("coverage validation", err)

[<Fact>]
let ``a policy verb rejects an option it does not accept`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "test-contract"; "manifest"; "validate"; "--owner"; "O-ANY-OWNER" |]

    Assert.Equal(2, code)
    Assert.Contains("--owner", err)

[<Fact>]
let ``a policy verb rejects a traversal fixture path`` () =
    let code, _, err = runPolicyVerb "layout" "../../../etc/passwd"
    Assert.Equal(2, code)
    Assert.Contains("traversal segment", err)

[<Fact>]
let ``test-contract --help still prints the namespace help`` () =
    let code, out, _ =
        runCaptured (errRoot "unused") [| "test-contract"; "layout"; "validate"; "--help" |]

    Assert.Equal(0, code)
    Assert.Equal(RhinoCli.Cli.HelpText.TestContractText, out)

// ---- test-contract argv rejection ----
//
// Every leaf in this namespace rejects malformed argv before it reads the
// repository, so these cases need no fixture and no repository root. They
// pin the exit-2 misuse contract the namespace's help text documents.

[<Fact>]
let ``a policy verb surfaces a repo-root lookup failure as exit 1`` () =
    let code, _, err =
        runCaptured (errRoot "not a git repo") [| "test-contract"; "layout"; "validate"; "--fixture"; "any.json" |]

    Assert.Equal(1, code)
    Assert.Contains("failed to find git repository root", err)

[<Fact>]
let ``registry compare rejects an option it does not accept`` () =
    let code, _, err =
        runCaptured (errRoot "unused") [| "test-contract"; "registry"; "compare"; "--source"; "legacy" |]

    Assert.Equal(2, code)
    Assert.Contains("--source", err)

[<Fact>]
let ``registry compare requires --legacy`` () =
    let code, _, err =
        runCaptured (errRoot "unused") [| "test-contract"; "registry"; "compare"; "--canonical"; "c.tsv" |]

    Assert.Equal(2, code)
    Assert.Contains("--legacy is required", err)

[<Fact>]
let ``registry compare requires --canonical`` () =
    let code, _, err =
        runCaptured (errRoot "unused") [| "test-contract"; "registry"; "compare"; "--legacy"; "l.tsv" |]

    Assert.Equal(2, code)
    Assert.Contains("--canonical is required", err)

[<Fact>]
let ``registry validate rejects a --require-state outside the lifecycle`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "test-contract"; "registry"; "validate"; "--require-state"; "molten" |]

    Assert.Equal(2, code)
    Assert.Contains("expanded, migrating, verified, or contracted", err)

[<Fact>]
let ``registry validate-mapping requires one of --all or --project`` () =
    let code, _, err =
        runCaptured (okRoot (newTempDir ())) [| "test-contract"; "registry"; "validate-mapping" |]

    Assert.Equal(2, code)
    Assert.Contains("one of --all or --project", err)

[<Fact>]
let ``registry validate-mapping rejects a --require-state outside its lifecycle`` () =
    let code, _, err =
        runCaptured
            (okRoot (newTempDir ()))
            [| "test-contract"
               "registry"
               "validate-mapping"
               "--all"
               "--require-state"
               "molten" |]

    Assert.Equal(2, code)
    Assert.Contains("identity, redirected, or verified", err)

[<Fact>]
let ``the owner fixture leaf requires --owner`` () =
    let code, _, err =
        runCaptured
            (okRoot (newTempDir ()))
            [| "test-contract"; "validate"; "--check"; "layout"; "--fixture"; "f.json" |]

    Assert.Equal(2, code)
    Assert.Contains("--owner is required", err)

[<Fact>]
let ``the owner fixture leaf rejects a check outside the four`` () =
    let code, _, err =
        runCaptured
            (okRoot (newTempDir ()))
            [| "test-contract"
               "validate"
               "--owner"
               "O-ANY-OWNER"
               "--check"
               "smoke"
               "--fixture"
               "f.json" |]

    Assert.Equal(2, code)
    Assert.Contains("layout, coverage, bdd, or manifest", err)

[<Fact>]
let ``the owner fixture leaf requires --fixture`` () =
    let code, _, err =
        runCaptured
            (okRoot (newTempDir ()))
            [| "test-contract"; "validate"; "--owner"; "O-ANY-OWNER"; "--check"; "bdd" |]

    Assert.Equal(2, code)
    Assert.Contains("--fixture is required", err)

/// The owner corpus is repository-specific — `ose-public` files `O-PUB-*`
/// owners and `ose-private` files `O-PRI-*` ones — while this file is
/// byte-identical across both. So the case reads whichever owner the checkout
/// declares first rather than naming one.
[<Fact>]
let ``the owner fixture leaf loads a checked-in owner document`` () =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Error message -> Assert.Fail(sprintf "expected findRoot Ok, got Error %s" message)
    | Ok realRepoRoot ->
        let owner =
            Directory.GetDirectories(Path.Combine(realRepoRoot, RhinoCli.Application.TestContract.FixtureRoot))
            |> Array.map Path.GetFileName
            |> Array.sort
            |> Array.head

        let code, out, _ =
            runCaptured
                (okRoot realRepoRoot)
                [| "test-contract"
                   "validate"
                   "--owner"
                   owner
                   "--check"
                   "coverage"
                   "--fixture"
                   sprintf "%s/%s/coverage-98.json" RhinoCli.Application.TestContract.FixtureRoot owner |]

        Assert.Equal(0, code)
        Assert.Contains(sprintf "fixture-loaded owner=%s check=coverage" owner, out)
