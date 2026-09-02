/// Plain xunit tests for `RhinoCli.Application.Doctor`'s tool-check engine —
/// behaviour with no dedicated Gherkin scenario, or exercised only
/// indirectly there (mirrors the rationale `DoctorUnitTests.fs`'s module doc
/// comment states for its own split from `DoctorSteps.fs`). Ported from
/// `apps/rhino-cli/src/application/doctor/checker.rs`,
/// `apps/rhino-cli/src/application/doctor/fixer.rs`,
/// `apps/rhino-cli/src/application/doctor/reporter.rs`'s
/// `#[cfg(test)] mod tests`.
module RhinoCli.Tests.Unit.Steps.DoctorToolCheckUnitTests

open System
open System.IO
open System.Runtime.InteropServices
open System.Text.Json
open Xunit
open RhinoCli.Application.Doctor

// ---- toolStatusCode / doctorScopeCode / parseDoctorScope / isMinimalTool ----

[<Fact>]
let ``toolStatusCode maps every status to its wire code`` () =
    Assert.Equal("ok", toolStatusCode Passing)
    Assert.Equal("warning", toolStatusCode Warning)
    Assert.Equal("missing", toolStatusCode Missing)

[<Fact>]
let ``doctorScopeCode maps every scope to its wire code`` () =
    Assert.Equal("full", doctorScopeCode FullScope)
    Assert.Equal("minimal", doctorScopeCode MinimalScope)

[<Fact>]
let ``parseDoctorScope recognizes full, minimal, and blank`` () =
    Assert.Equal(Some FullScope, parseDoctorScope "")
    Assert.Equal(Some FullScope, parseDoctorScope "full")
    Assert.Equal(Some MinimalScope, parseDoctorScope "minimal")
    Assert.Equal(None, parseDoctorScope "bogus")

[<Fact>]
let ``isMinimalTool recognizes exactly the six core tools`` () =
    for name in [ "git"; "volta"; "node"; "npm"; "docker"; "jq" ] do
        Assert.True(isMinimalTool name, name)

    for name in [ "rust"; "dotnet"; "tofu"; "shellcheck" ] do
        Assert.False(isMinimalTool name, name)

// ---- parseDoctorToolName ----

[<Fact>]
let ``parseDoctorToolName accepts every inventory entry`` () =
    for name in doctorToolInventory do
        Assert.Equal(Ok name, parseDoctorToolName name)

[<Fact>]
let ``parseDoctorToolName rejects a blank value`` () =
    match parseDoctorToolName "   " with
    | Error message -> Assert.Contains("must not be blank", message)
    | Ok _ -> failwith "blank name must be rejected"

[<Fact>]
let ``parseDoctorToolName rejects an unknown tool`` () =
    match parseDoctorToolName "not-a-doctor-tool" with
    | Error message -> Assert.Contains("unknown Doctor tool \"not-a-doctor-tool\"", message)
    | Ok _ -> failwith "unknown name must be rejected"

// ---- comparators ----

[<Fact>]
let ``compareExact passes with no requirement`` () =
    Assert.Equal(Passing, fst (compareExact "1.0" ""))

[<Fact>]
let ``compareExact matches after stripping a leading v`` () =
    let status, _ = compareExact "v1.2.3" "1.2.3"
    Assert.Equal(Passing, status)

[<Fact>]
let ``compareExact warns on mismatch`` () =
    let status, note = compareExact "1.2.3" "1.2.4"
    Assert.Equal(Warning, status)
    Assert.Contains("version mismatch", note)

[<Fact>]
let ``compareGte passes with no requirement`` () =
    Assert.Equal(Passing, fst (compareGte "1.0.0" ""))

[<Fact>]
let ``compareGte passes when installed is higher`` () =
    let status, note = compareGte "1.25.0" "1.24.0"
    Assert.Equal(Passing, status)
    Assert.Contains("required: ≥", note)

[<Fact>]
let ``compareGte passes when installed equals required`` () =
    Assert.Equal(Passing, fst (compareGte "1.24.0" "1.24.0"))

[<Fact>]
let ``compareGte warns when installed is lower`` () =
    let status, note = compareGte "1.22.0" "1.24.0"
    Assert.Equal(Warning, status)
    Assert.Contains("too old", note)

[<Fact>]
let ``compareGte falls back to compareExact when a version fails to parse`` () =
    let status, _ = compareGte "abc" "1.24.0"
    Assert.Equal(Warning, status)

[<Fact>]
let ``compareMajorGte passes with no requirement`` () =
    Assert.Equal(Passing, fst (compareMajorGte "10.0" ""))

[<Fact>]
let ``compareMajorGte passes when major is higher or equal`` () =
    Assert.Equal(Passing, fst (compareMajorGte "28.0.1" "27.0.0"))
    Assert.Equal(Passing, fst (compareMajorGte "27.0.1" "27.0.0"))

[<Fact>]
let ``compareMajorGte warns when major is lower`` () =
    let status, note = compareMajorGte "26.0.0" "27.0.0"
    Assert.Equal(Warning, status)
    Assert.Contains("(major)", note)

[<Fact>]
let ``compareMajorGte falls back to compareExact when a major component fails to parse`` () =
    let status, _ = compareMajorGte "abc.0" "27.0.0"
    Assert.Equal(Warning, status)

// ---- version readers ----

let private withTempDir (body: string -> unit) : unit =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-toolcheck-unit-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore

    try
        body dir
    finally
        Directory.Delete(dir, true)

[<Fact>]
let ``readNodeVersion and readNpmVersion read volta versions from package.json`` () =
    withTempDir (fun dir ->
        let path = Path.Combine(dir, "package.json")
        File.WriteAllText(path, "{\"volta\":{\"node\":\"24.11.1\",\"npm\":\"10.9.0\"}}")
        Assert.Equal(Some "24.11.1", readNodeVersion path)
        Assert.Equal(Some "10.9.0", readNpmVersion path))

[<Fact>]
let ``readNodeVersion returns None for a missing or malformed file`` () =
    Assert.Equal(None, readNodeVersion "/nonexistent/package.json")

    withTempDir (fun dir ->
        let path = Path.Combine(dir, "package.json")
        File.WriteAllText(path, "not json")
        Assert.Equal(None, readNodeVersion path))

[<Fact>]
let ``readDotnetVersion reads sdk.version from global.json`` () =
    withTempDir (fun dir ->
        let path = Path.Combine(dir, "global.json")
        File.WriteAllText(path, "{\"sdk\":{\"version\":\"8.0.401\"}}")
        Assert.Equal(Some "8.0.401", readDotnetVersion path))

[<Fact>]
let ``readRustToolchainChannel reads the pinned channel`` () =
    withTempDir (fun dir ->
        let path = Path.Combine(dir, "rust-toolchain.toml")
        File.WriteAllText(path, "[toolchain]\nchannel = \"1.75.0\"\ncomponents = [\"clippy\"]\n")
        Assert.Equal(Some "1.75.0", readRustToolchainChannel path))

[<Fact>]
let ``readRustToolchainChannel returns None when the file is missing or lacks a channel key`` () =
    Assert.Equal(None, readRustToolchainChannel "/nonexistent/rust-toolchain.toml")

    withTempDir (fun dir ->
        let path = Path.Combine(dir, "rust-toolchain.toml")
        File.WriteAllText(path, "[toolchain]\n")
        Assert.Equal(None, readRustToolchainChannel path))

// ---- readRustToolchainComponents ----
//
// Mirrors `checker.rs`'s six-case matrix: A/B are baseline-pass forms, C-F
// each reproduce a distinct parser defect a substring-based extractor gets
// wrong (false rejection for C/D, false acceptance for E/F).

[<Fact>]
let ``readRustToolchainComponents case A baseline single line`` () =
    let contents =
        "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\", \"rustfmt\", \"llvm-tools\"]\n"

    Assert.Equal<string list>([ "clippy"; "rustfmt"; "llvm-tools" ], readRustToolchainComponents contents)

[<Fact>]
let ``readRustToolchainComponents case B multi line no comments`` () =
    let contents =
        "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\n  \"clippy\",\n  \"rustfmt\",\n]\n"

    Assert.Equal<string list>([ "clippy"; "rustfmt" ], readRustToolchainComponents contents)

[<Fact>]
let ``readRustToolchainComponents case C multi line with per entry comments`` () =
    let contents =
        "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\n  \"clippy\",  # linter\n  \"rustfmt\", # formatter\n]\n"

    Assert.Equal<string list>([ "clippy"; "rustfmt" ], readRustToolchainComponents contents)

[<Fact>]
let ``readRustToolchainComponents case D single quoted literal strings`` () =
    let contents =
        "[toolchain]\nchannel = \"1.95.0\"\ncomponents = ['clippy', 'rustfmt']\n"

    Assert.Equal<string list>([ "clippy"; "rustfmt" ], readRustToolchainComponents contents)

[<Fact>]
let ``readRustToolchainComponents case E commented out decoy is ignored`` () =
    let contents =
        "# components = [\"clippy\", \"rustfmt\"]\n[toolchain]\nchannel = \"1.95.0\"\n"

    Assert.Equal<string list>([], readRustToolchainComponents contents)

[<Fact>]
let ``readRustToolchainComponents case F unrelated key is ignored`` () =
    let contents =
        "[toolchain]\nchannel = \"1.95.0\"\nexcluded_components = [\"clippy\", \"rustfmt\"]\n"

    Assert.Equal<string list>([], readRustToolchainComponents contents)

// ---- rustToolchainManifests ----

[<Fact>]
let ``rustToolchainManifests covers the root file and apps/libs project dirs`` () =
    withTempDir (fun repo ->
        let body =
            "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\", \"rustfmt\"]\n"

        File.WriteAllText(Path.Combine(repo, "rust-toolchain.toml"), body)

        for project in [ "apps/rhino-cli"; "libs/rust-commons" ] do
            let dir = Path.Combine(repo, project.Replace('/', Path.DirectorySeparatorChar))
            Directory.CreateDirectory(dir) |> ignore
            File.WriteAllText(Path.Combine(dir, "rust-toolchain.toml"), body)

        Assert.Equal<string list>(
            [ "rust-toolchain.toml"
              "apps/rhino-cli/rust-toolchain.toml"
              "libs/rust-commons/rust-toolchain.toml" ],
            rustToolchainManifests repo
        ))

[<Fact>]
let ``rustToolchainManifests returns an empty list when apps and libs do not exist`` () =
    withTempDir (fun repo -> Assert.Equal<string list>([], rustToolchainManifests repo))

// ---- rustToolchainLintComponentChecks ----

[<Fact>]
let ``rustToolchainLintComponentChecks names only the genuinely missing component`` () =
    withTempDir (fun repo ->
        let project = Path.Combine(repo, "apps", "coralpolyp-be")
        Directory.CreateDirectory(project) |> ignore

        File.WriteAllText(
            Path.Combine(project, "rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\"]\n"
        )

        let checks = rustToolchainLintComponentChecks repo
        Assert.Equal(1, List.length checks)
        Assert.Equal("rust-toolchain-components", checks.[0].Name)
        Assert.Equal(Warning, checks.[0].Status)
        Assert.Contains("rustfmt", checks.[0].Note)
        Assert.DoesNotContain("clippy component", checks.[0].Note))

[<Fact>]
let ``rustToolchainLintComponentChecks is empty when every component is declared`` () =
    withTempDir (fun repo ->
        let project = Path.Combine(repo, "apps", "rhino-cli")
        Directory.CreateDirectory(project) |> ignore

        File.WriteAllText(
            Path.Combine(project, "rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\", \"rustfmt\"]\n"
        )

        Assert.Empty(rustToolchainLintComponentChecks repo))

// ---- dotnetChannel ----

[<Fact>]
let ``dotnetChannel extracts the major minor channel from a full SDK version`` () =
    Assert.Equal("10.0", dotnetChannel "10.0.204")

[<Fact>]
let ``dotnetChannel falls back to the default channel for an unparsable requirement`` () =
    Assert.Equal("10.0", dotnetChannel "")
    Assert.Equal("10.0", dotnetChannel "not-a-version")
    Assert.Equal("10.0", dotnetChannel "10;rm -rf /")

// ---- checkPlaywrightBrowsersAt ----

[<Fact>]
let ``checkPlaywrightBrowsersAt returns false when home is None`` () =
    Assert.False(checkPlaywrightBrowsersAt None)

[<Fact>]
let ``checkPlaywrightBrowsersAt finds a chromium bundle under the platform cache dir`` () =
    withTempDir (fun home ->
        let cacheDir =
            if RuntimeInformation.IsOSPlatform(OSPlatform.OSX) then
                Path.Combine(home, "Library", "Caches", "ms-playwright")
            else
                Path.Combine(home, ".cache", "ms-playwright")

        Directory.CreateDirectory(Path.Combine(cacheDir, "chromium-1234")) |> ignore
        Assert.True(checkPlaywrightBrowsersAt (Some home)))

[<Fact>]
let ``checkPlaywrightBrowsersAt returns false when the cache dir does not exist`` () =
    withTempDir (fun home -> Assert.False(checkPlaywrightBrowsersAt (Some home)))

[<Fact>]
let ``checkPlaywrightBrowsersAmbient runs without throwing`` () =
    checkPlaywrightBrowsersAmbient () |> ignore

// ---- install* step builders (both platform branches, independent of host) ----

[<Fact>]
let ``installGit builds the darwin and linux remediation steps`` () =
    Assert.Equal<InstallStep list>(
        [ { Description = "Install Xcode Command Line Tools"
            Command = "xcode-select"
            Args = [ "--install" ] } ],
        installGit "" "darwin"
    )

    Assert.Equal<InstallStep list>(
        [ { Description = "Install git"
            Command = "sudo"
            Args = [ "apt-get"; "install"; "-y"; "git" ] } ],
        installGit "" "linux"
    )

[<Fact>]
let ``installVolta builds a single platform-independent step`` () =
    Assert.Equal(1, (installVolta "" "darwin").Length)
    Assert.Equal<InstallStep list>(installVolta "" "darwin", installVolta "" "linux")

[<Fact>]
let ``installNode names the requested version via Volta`` () =
    let steps = installNode "24.11.1" "darwin"
    Assert.Equal("volta", steps.[0].Command)
    Assert.Equal<string list>([ "install"; "node@24.11.1" ], steps.[0].Args)

[<Fact>]
let ``installNpm names the requested version via Volta`` () =
    let steps = installNpm "11.0.0" "linux"
    Assert.Equal("volta", steps.[0].Command)
    Assert.Equal<string list>([ "install"; "npm@11.0.0" ], steps.[0].Args)

[<Fact>]
let ``installRust builds a single platform-independent rustup step`` () =
    Assert.Equal<InstallStep list>(installRust "" "darwin", installRust "" "linux")

[<Fact>]
let ``installCargoLlvmCov builds a single platform-independent step`` () =
    Assert.Equal<InstallStep list>(installCargoLlvmCov "" "darwin", installCargoLlvmCov "" "linux")

[<Fact>]
let ``installDotnet installs via Homebrew on darwin and the signed script on linux`` () =
    let darwinSteps = installDotnet "10.0.103" "darwin"
    Assert.Equal("brew", darwinSteps.[0].Command)
    Assert.Equal<string list>([ "install"; "dotnet" ], darwinSteps.[0].Args)

    let linuxSteps = installDotnet "10.0.103" "linux"
    Assert.Equal("bash", linuxSteps.[0].Command)
    Assert.Contains("--channel 10.0 --install-dir", linuxSteps.[0].Args.[1])

[<Fact>]
let ``installDocker is a no-op on darwin and installs via apt on linux`` () =
    Assert.Equal<InstallStep list>([], installDocker "" "darwin")
    let linuxSteps = installDocker "" "linux"
    Assert.Equal("sudo", linuxSteps.[0].Command)
    Assert.Contains("docker.io", linuxSteps.[0].Args)

[<Fact>]
let ``installJq installs via Homebrew on darwin and apt on linux`` () =
    Assert.Equal("brew", (installJq "" "darwin").[0].Command)
    Assert.Equal("sudo", (installJq "" "linux").[0].Command)

[<Fact>]
let ``installShellcheck installs via Homebrew on darwin and apt on linux`` () =
    Assert.Equal("brew", (installShellcheck "" "darwin").[0].Command)
    Assert.Equal("sudo", (installShellcheck "" "linux").[0].Command)

[<Fact>]
let ``installActionlint installs via Homebrew on darwin and the download script on linux`` () =
    Assert.Equal("brew", (installActionlint "" "darwin").[0].Command)
    let linuxSteps = installActionlint "" "linux"
    Assert.Equal("sudo", linuxSteps.[0].Command)
    Assert.Contains("download-actionlint.bash", linuxSteps.[0].Args.[2])

[<Fact>]
let ``installHadolint installs via Homebrew on darwin and a two-step download on linux`` () =
    Assert.Equal(1, (installHadolint "" "darwin").Length)
    let linuxSteps = installHadolint "" "linux"
    Assert.Equal(2, linuxSteps.Length)
    Assert.Equal("Make hadolint executable", linuxSteps.[1].Description)

[<Fact>]
let ``installShfmt installs via Homebrew on darwin and a two-step download on linux`` () =
    Assert.Equal(1, (installShfmt "" "darwin").Length)
    let linuxSteps = installShfmt "" "linux"
    Assert.Equal(2, linuxSteps.Length)
    Assert.Equal("Make shfmt executable", linuxSteps.[1].Description)

[<Fact>]
let ``installTofu builds a checksum-verified script for darwin, linux, and rejects other platforms`` () =
    let darwinSteps = installTofu "" "darwin"
    Assert.Contains("shasum -a 256", darwinSteps.[0].Args.[1])

    let linuxSteps = installTofu "" "linux"
    Assert.Contains("sha256sum", linuxSteps.[0].Args.[1])

    Assert.Equal<InstallStep list>([], installTofu "" "other")

[<Fact>]
let ``installClangFormat installs via Homebrew on darwin and apt on linux`` () =
    Assert.Equal("brew", (installClangFormat "" "darwin").[0].Command)
    Assert.Equal("sudo", (installClangFormat "" "linux").[0].Command)

[<Fact>]
let ``installPlaywright installs browsers only on darwin and browsers plus system deps on linux`` () =
    Assert.Equal(1, (installPlaywright "" "darwin").Length)
    let linuxSteps = installPlaywright "" "linux"
    Assert.Equal(2, linuxSteps.Length)
    Assert.Equal("Install Playwright system deps", linuxSteps.[1].Description)

// ---- runOneDef / realRunner ----

let private trivialDef (name: string) : ToolDef =
    { Name = name
      Binary = name
      Source = ""
      Args = [ "--version" ]
      UseStderr = false
      ParseVer = (fun s -> s.Trim())
      Compare = compareExact
      ReadReq = (fun () -> "")
      InstallCmd = None }

[<Fact>]
let ``runOneDef reports Missing when the runner cannot find the binary`` () =
    let runner: CommandRunner = fun _ _ -> Error "not found"
    let check = runOneDef runner (trivialDef "ghosttool")
    Assert.Equal(Missing, check.Status)
    Assert.Equal("not found in PATH", check.Note)

[<Fact>]
let ``runOneDef reports Passing with a fake runner`` () =
    let runner: CommandRunner = fun _ _ -> Ok("1.0.0\n", "", 0)
    let check = runOneDef runner (trivialDef "fake")
    Assert.Equal(Passing, check.Status)
    Assert.Equal("1.0.0", check.InstalledVersion)

[<Fact>]
let ``realRunner reports Missing for a binary absent from PATH`` () =
    match realRunner "definitely-not-a-real-binary-xyz" [ "--version" ] with
    | Error message -> Assert.Contains("not found in PATH", message)
    | Ok _ -> failwith "must not find a nonexistent binary"

// ---- checkAll / selectedToolDefs ----

[<Fact>]
let ``checkAll full scope without repo-config checks every tool`` () =
    withTempDir (fun repo ->
        File.WriteAllText(Path.Combine(repo, "package.json"), "{}")
        let runner: CommandRunner = fun _ _ -> Ok("1.0.0\n", "", 0)

        let options: CheckOptions =
            { RepoRoot = repo
              Runner = Some runner
              Scope = FullScope
              SelectedTools = None }

        let result = checkAll options
        Assert.Equal(16, List.length result.Checks))

[<Fact>]
let ``checkAll respects repo-config doctor skip-tools`` () =
    withTempDir (fun repo ->
        File.WriteAllText(Path.Combine(repo, "package.json"), "{}")

        File.WriteAllText(
            Path.Combine(repo, "repo-config.yml"),
            "doctor:\n  skip-tools: [shfmt, tofu, clang-format]\n"
        )

        let runner: CommandRunner =
            fun name _ ->
                if List.contains name [ "shfmt"; "tofu"; "clang-format" ] then
                    failwithf "skip-tools entry %s must never be probed" name
                else
                    Ok("1.0.0\n", "", 0)

        let options: CheckOptions =
            { RepoRoot = repo
              Runner = Some runner
              Scope = FullScope
              SelectedTools = None }

        let result = checkAll options
        Assert.Equal(13, List.length result.Checks)

        Assert.False(
            result.Checks
            |> List.exists (fun c -> List.contains c.Name [ "shfmt"; "tofu"; "clang-format" ])
        ))

[<Fact>]
let ``explicit empty tool selection runs zero probes`` () =
    withTempDir (fun repo ->
        File.WriteAllText(Path.Combine(repo, "package.json"), "{}")
        let runner: CommandRunner = fun name _ -> failwithf "must not probe %s" name

        let options: CheckOptions =
            { RepoRoot = repo
              Runner = Some runner
              Scope = FullScope
              SelectedTools = Some [] }

        let result = checkAll options
        Assert.Empty(result.Checks))

// ---- needsRemediation / hasRemediationWork ----

let private missing (name: string) : ToolCheck =
    { Name = name
      Binary = name
      Status = Missing
      InstalledVersion = ""
      RequiredVersion = ""
      Source = ""
      Note = "not found in PATH" }

let private ok (name: string) : ToolCheck =
    { Name = name
      Binary = name
      Status = Passing
      InstalledVersion = "1"
      RequiredVersion = ""
      Source = ""
      Note = "no version requirement" }

let private warn (name: string) : ToolCheck =
    { Name = name
      Binary = name
      Status = Warning
      InstalledVersion = "1.0.0"
      RequiredVersion = "2.0.0"
      Source = ""
      Note = "required: 2.0.0, version mismatch" }

[<Fact>]
let ``needsRemediation is true for a missing tool`` () =
    Assert.True(needsRemediation (missing "a"))

[<Fact>]
let ``needsRemediation is true only for a tofu version warning`` () =
    Assert.True(needsRemediation (warn "tofu"))
    Assert.False(needsRemediation (warn "node"))
    Assert.False(needsRemediation (ok "git"))

[<Fact>]
let ``hasRemediationWork reflects whether any check needs remediation`` () =
    let allOk: DoctorResult =
        { Checks = [ ok "git" ]
          OkCount = 1
          WarnCount = 0
          MissingCount = 0
          Scope = FullScope }

    Assert.False(hasRemediationWork allOk)

    let oneMissing =
        { allOk with
            Checks = [ ok "git"; missing "shellcheck" ]
            MissingCount = 1 }

    Assert.True(hasRemediationWork oneMissing)

// ---- fix ----

[<Fact>]
let ``fix counts already-ok checks without invoking the runner`` () =
    let result: DoctorResult =
        { Checks = [ ok "git" ]
          OkCount = 1
          WarnCount = 0
          MissingCount = 0
          Scope = FullScope }

    let defs = [ trivialDef "git" ]
    let mutable log = ""
    let fr = fix result defs { DryRun = false; Runner = None } (fun m -> log <- log + m)
    Assert.Equal(1, fr.AlreadyOk)
    Assert.Equal(0, fr.Fixed)

[<Fact>]
let ``fix skips a missing tool with no install command`` () =
    let result: DoctorResult =
        { Checks = [ missing "a" ]
          OkCount = 0
          WarnCount = 0
          MissingCount = 1
          Scope = FullScope }

    let defs = [ trivialDef "a" ]
    let mutable log = ""
    let fr = fix result defs { DryRun = false; Runner = None } (fun m -> log <- log + m)
    Assert.Equal(1, fr.Skipped)
    Assert.Contains("no auto-install", log)

[<Fact>]
let ``fix skips a check with no corresponding def when defs is shorter than Checks`` () =
    let result: DoctorResult =
        { Checks = [ missing "a" ]
          OkCount = 0
          WarnCount = 0
          MissingCount = 1
          Scope = FullScope }

    let mutable log = ""
    let fr = fix result [] { DryRun = false; Runner = None } (fun m -> log <- log + m)
    Assert.Equal(1, fr.Skipped)
    Assert.Contains("no auto-install", log)

[<Fact>]
let ``fix skips a missing tool whose install function returns no steps for this platform`` () =
    let result: DoctorResult =
        { Checks = [ missing "a" ]
          OkCount = 0
          WarnCount = 0
          MissingCount = 1
          Scope = FullScope }

    let defs =
        [ { trivialDef "a" with
              InstallCmd = Some(fun _ _ -> []) } ]

    let mutable log = ""
    let fr = fix result defs { DryRun = false; Runner = None } (fun m -> log <- log + m)
    Assert.Equal(1, fr.Skipped)
    Assert.Contains("no install steps", log)

[<Fact>]
let ``fix dry-run previews without invoking the runner`` () =
    let result: DoctorResult =
        { Checks = [ missing "a" ]
          OkCount = 0
          WarnCount = 0
          MissingCount = 1
          Scope = FullScope }

    let installEcho (_req: string) (_platform: string) : InstallStep list =
        [ { Description = "echo"
            Command = "/bin/echo"
            Args = [ "x" ] } ]

    let defs =
        [ { trivialDef "a" with
              InstallCmd = Some installEcho } ]

    let mutable invoked = 0

    let runner: FixRunner =
        fun _ _ ->
            invoked <- invoked + 1
            Ok()

    let mutable log = ""

    let fr =
        fix result defs { DryRun = true; Runner = Some runner } (fun m -> log <- log + m)

    Assert.Equal(0, invoked)
    Assert.Equal(0, fr.Fixed)
    Assert.Contains("Would install", log)

[<Fact>]
let ``fix counts a successful live install as fixed`` () =
    let result: DoctorResult =
        { Checks = [ missing "a" ]
          OkCount = 0
          WarnCount = 0
          MissingCount = 1
          Scope = FullScope }

    let installEcho (_req: string) (_platform: string) : InstallStep list =
        [ { Description = "echo"
            Command = "/bin/echo"
            Args = [ "x" ] } ]

    let defs =
        [ { trivialDef "a" with
              InstallCmd = Some installEcho } ]

    let runner: FixRunner = fun _ _ -> Ok()
    let fr = fix result defs { DryRun = false; Runner = Some runner } ignore
    Assert.Equal(1, fr.Fixed)
    Assert.Equal(0, fr.Failed)

[<Fact>]
let ``fix counts a failed live install as failed`` () =
    let result: DoctorResult =
        { Checks = [ missing "a" ]
          OkCount = 0
          WarnCount = 0
          MissingCount = 1
          Scope = FullScope }

    let installEcho (_req: string) (_platform: string) : InstallStep list =
        [ { Description = "echo"
            Command = "/bin/echo"
            Args = [ "x" ] } ]

    let defs =
        [ { trivialDef "a" with
              InstallCmd = Some installEcho } ]

    let runner: FixRunner = fun _ _ -> Error "boom"
    let fr = fix result defs { DryRun = false; Runner = Some runner } ignore
    Assert.Equal(1, fr.Failed)
    Assert.Equal(0, fr.Fixed)

[<Fact>]
let ``fix skips remediation for a stale non-tofu version warning`` () =
    let result: DoctorResult =
        { Checks = [ warn "node" ]
          OkCount = 0
          WarnCount = 1
          MissingCount = 0
          Scope = FullScope }

    let defs = [ trivialDef "node" ]
    let fr = fix result defs { DryRun = false; Runner = None } ignore
    Assert.Equal(1, fr.AlreadyOk)
    Assert.Equal(0, fr.Fixed)

[<Fact>]
let ``fixAll uses the same tool selection as checkAll`` () =
    withTempDir (fun repo ->
        File.WriteAllText(Path.Combine(repo, "package.json"), "{}")

        let result: DoctorResult =
            { Checks = [ missing "tofu" ]
              OkCount = 0
              WarnCount = 0
              MissingCount = 1
              Scope = FullScope }

        let options: CheckOptions =
            { RepoRoot = repo
              Runner = None
              Scope = FullScope
              SelectedTools = Some [ "tofu" ] }

        let mutable log = ""

        let fr =
            fixAll result options { DryRun = true; Runner = None } (fun m -> log <- log + m)

        Assert.Equal(0, fr.Fixed)
        Assert.Contains("Would install: tofu", log)
        Assert.Contains("tofu_1.12.3_", log)
        Assert.Contains("expected_checksum=", log)
        Assert.DoesNotContain("install-opentofu.sh", log))

[<Fact>]
let ``realFixRunner reports the exit code of a failing command`` () =
    match realFixRunner "false" [] with
    | Error message -> Assert.Contains("exit", message)
    | Ok _ -> failwith "the false(1) command must never succeed"

[<Fact>]
let ``realFixRunner succeeds for a trivially successful command`` () =
    match realFixRunner "true" [] with
    | Ok _ -> ()
    | Error message -> failwithf "the true(1) command must always succeed, got: %s" message

[<Fact>]
let ``realFixRunner returns the spawn error message for a nonexistent absolute path`` () =
    match realFixRunner "/definitely/not/a/real/path/rhino-cli-fixture-binary" [] with
    | Error _ -> ()
    | Ok _ -> failwith "must not successfully spawn a nonexistent absolute-path binary"

// ---- format* ----

[<Fact>]
let ``formatFixSummary reports the fixed failed already-ok counts`` () =
    let text =
        formatFixSummary
            { Fixed = 3
              Failed = 1
              AlreadyOk = 5
              Skipped = 0 }

    Assert.Contains("3 fixed, 1 failed, 5 already OK", text)

[<Fact>]
let ``formatNothingToFix reports nothing to fix`` () =
    Assert.Contains("Nothing to fix", formatNothingToFix)

[<Fact>]
let ``formatDoctorText suppresses the header when quiet`` () =
    let result: DoctorResult =
        { Checks = [ ok "git" ]
          OkCount = 1
          WarnCount = 0
          MissingCount = 0
          Scope = FullScope }

    Assert.Contains("Doctor Report", formatDoctorText result false)
    Assert.DoesNotContain("Doctor Report", formatDoctorText result true)

[<Fact>]
let ``formatDoctorText marks a minimal-scope run`` () =
    let result: DoctorResult =
        { Checks = []
          OkCount = 0
          WarnCount = 0
          MissingCount = 0
          Scope = MinimalScope }

    Assert.Contains("(scope: minimal)", formatDoctorText result false)

[<Fact>]
let ``formatDoctorJson round-trips through JsonDocument`` () =
    let result: DoctorResult =
        { Checks = [ ok "git"; warn "node"; missing "ghost" ]
          OkCount = 1
          WarnCount = 1
          MissingCount = 1
          Scope = FullScope }

    use doc = JsonDocument.Parse(formatDoctorJson result 0L)
    let root = doc.RootElement
    Assert.Equal("missing", root.GetProperty("status").GetString())
    Assert.Equal(1, root.GetProperty("ok_count").GetInt32())
    Assert.Equal(3, root.GetProperty("tools").GetArrayLength())

[<Fact>]
let ``formatDoctorJson prioritizes missing over warning over ok`` () =
    let warningOnly: DoctorResult =
        { Checks = [ warn "node" ]
          OkCount = 0
          WarnCount = 1
          MissingCount = 0
          Scope = FullScope }

    use doc = JsonDocument.Parse(formatDoctorJson warningOnly 0L)
    Assert.Equal("warning", doc.RootElement.GetProperty("status").GetString())

    let okOnly =
        { warningOnly with
            Checks = [ ok "git" ]
            WarnCount = 0
            OkCount = 1 }

    use doc2 = JsonDocument.Parse(formatDoctorJson okOnly 0L)
    Assert.Equal("ok", doc2.RootElement.GetProperty("status").GetString())

// ---- Additional plain unit tests targeting coverage gaps not reached
// above: parseLineWord's insufficient-word-count branch, parseDockerVersion's
// insufficient-field branch, readJsonStringProperty's non-string-value
// branch, readRustToolchainChannel's no-equals-sign branch,
// readRustToolchainComponents' non-array-value branch,
// rustToolchainLintComponentChecks' unreadable-manifest exception handler,
// checkPlaywrightBrowsersAt's unreadable-cache-dir exception handler,
// checkPlaywrightBrowsersAmbient's empty-HOME branch, and comparePlaywright's
// Warning branch.

[<Fact>]
let ``parseGitVersion returns empty when the matching line has too few words`` () =
    Assert.Equal("", parseGitVersion "git version\n")

[<Fact>]
let ``parseDockerVersion returns empty when the matching line has too few fields`` () =
    Assert.Equal("", parseDockerVersion "Docker version\n")

[<Fact>]
let ``readNodeVersion returns None when the volta.node value is not a string`` () =
    withTempDir (fun dir ->
        let path = Path.Combine(dir, "package.json")
        File.WriteAllText(path, "{\"volta\":{\"node\":24}}")
        Assert.Equal(None, readNodeVersion path))

[<Fact>]
let ``readRustToolchainChannel returns None for a channel line with no equals sign`` () =
    withTempDir (fun dir ->
        let path = Path.Combine(dir, "rust-toolchain.toml")
        File.WriteAllText(path, "[toolchain]\nchannelWithNoEquals\n")
        Assert.Equal(None, readRustToolchainChannel path))

[<Fact>]
let ``readRustToolchainComponents ignores a components key whose value is not an array`` () =
    let contents = "[toolchain]\nchannel = \"1.95.0\"\ncomponents = \"clippy\"\n"
    Assert.Equal<string list>([], readRustToolchainComponents contents)

[<Fact>]
let ``rustToolchainLintComponentChecks silently skips an unreadable manifest`` () =
    withTempDir (fun repo ->
        let project = Path.Combine(repo, "apps", "unreadable-app")
        Directory.CreateDirectory(project) |> ignore
        let manifest = Path.Combine(project, "rust-toolchain.toml")
        File.WriteAllText(manifest, "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\"]\n")

        try
            File.SetUnixFileMode(manifest, UnixFileMode.None)
            Assert.Empty(rustToolchainLintComponentChecks repo)
        finally
            File.SetUnixFileMode(manifest, UnixFileMode.UserRead ||| UnixFileMode.UserWrite))

[<Fact>]
let ``checkPlaywrightBrowsersAt returns false when the cache dir cannot be read`` () =
    withTempDir (fun home ->
        let cacheDir =
            if RuntimeInformation.IsOSPlatform(OSPlatform.OSX) then
                Path.Combine(home, "Library", "Caches", "ms-playwright")
            else
                Path.Combine(home, ".cache", "ms-playwright")

        Directory.CreateDirectory(cacheDir) |> ignore

        try
            File.SetUnixFileMode(cacheDir, UnixFileMode.None)
            Assert.False(checkPlaywrightBrowsersAt (Some home))
        finally
            File.SetUnixFileMode(
                cacheDir,
                UnixFileMode.UserRead ||| UnixFileMode.UserWrite ||| UnixFileMode.UserExecute
            ))

[<Fact>]
let ``checkPlaywrightBrowsersAmbient treats an empty HOME the same as an absent one`` () =
    let originalHome = Environment.GetEnvironmentVariable("HOME")

    try
        Environment.SetEnvironmentVariable("HOME", "")
        Assert.False(checkPlaywrightBrowsersAmbient ())
    finally
        Environment.SetEnvironmentVariable("HOME", originalHome)

[<Fact>]
let ``comparePlaywright reports Warning when no browsers are installed at the ambient HOME`` () =
    withTempDir (fun home ->
        let originalHome = Environment.GetEnvironmentVariable("HOME")

        try
            Environment.SetEnvironmentVariable("HOME", home)
            let status, message = comparePlaywright "" ""
            Assert.Equal(Warning, status)
            Assert.Contains("browsers not installed", message)
        finally
            Environment.SetEnvironmentVariable("HOME", originalHome))

[<Fact>]
let ``realRunner reports Missing for an absolute path with no file present`` () =
    withTempDir (fun dir ->
        let absolutePath = Path.Combine(dir, "nonexistent-binary")

        match realRunner absolutePath [] with
        | Error message -> Assert.Contains("not found in PATH", message)
        | Ok _ -> failwith "must not find a nonexistent absolute-path binary")

[<Fact>]
let ``realRunner reports Missing for a bare name when PATH is unset`` () =
    let originalPath = Environment.GetEnvironmentVariable("PATH")

    try
        Environment.SetEnvironmentVariable("PATH", null)

        match realRunner "git" [] with
        | Error message -> Assert.Contains("not found in PATH", message)
        | Ok _ -> failwith "must not find any binary when PATH is unset"
    finally
        Environment.SetEnvironmentVariable("PATH", originalPath)

[<Fact>]
let ``realRunner returns the process error message when the binary exists but cannot be executed`` () =
    withTempDir (fun dir ->
        let fakeToolPath = Path.Combine(dir, "fake-tool")
        File.WriteAllText(fakeToolPath, "#!/bin/sh\necho hi\n")
        File.SetUnixFileMode(fakeToolPath, UnixFileMode.UserRead ||| UnixFileMode.UserWrite)

        let originalPath = Environment.GetEnvironmentVariable("PATH")

        try
            Environment.SetEnvironmentVariable("PATH", dir + string Path.PathSeparator + originalPath)

            match realRunner "fake-tool" [] with
            | Error _ -> ()
            | Ok _ -> failwith "must not successfully execute a non-executable file"
        finally
            Environment.SetEnvironmentVariable("PATH", originalPath))
