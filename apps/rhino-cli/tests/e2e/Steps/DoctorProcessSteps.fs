/// Published-process proof for `doctor.feature`. The executable is real; its
/// external tool environment is a deterministic disposable PATH fixture.
module RhinoCli.Tests.E2E.Steps.DoctorProcessSteps

open System
open System.Diagnostics
open System.IO
open System.Text.Json
open TickSpec
open Xunit

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/system/doctor.feature" ]

let private repositoryRoot =
    Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

let private cli =
    lazy
        (let executable =
            Path.Combine(repositoryRoot, "apps", "rhino-cli", "src", "dist", "rhino-cli-fsharp")

         if not (File.Exists executable) then
             let info =
                 ProcessStartInfo(FileName = "dotnet", WorkingDirectory = repositoryRoot, UseShellExecute = false)

             [ "publish"
               "apps/rhino-cli/src/RhinoCli.Program/RhinoCli.Program.fsproj"
               "-c"
               "Release"
               "--self-contained"
               "true"
               "--use-current-runtime"
               "-o"
               "apps/rhino-cli/src/dist" ]
             |> List.iter info.ArgumentList.Add

             use proc = Process.Start info
             proc.WaitForExit()
             Assert.Equal(0, proc.ExitCode)

         executable)

type private Result =
    { ExitCode: int
      Stdout: string
      Stderr: string }

let private run executable args cwd environment =
    let info =
        ProcessStartInfo(
            FileName = executable,
            WorkingDirectory = cwd,
            UseShellExecute = false,
            RedirectStandardOutput = true,
            RedirectStandardError = true
        )

    args |> List.iter info.ArgumentList.Add
    environment |> List.iter (fun (key, value) -> info.Environment.[key] <- value)
    use proc = Process.Start info
    let stdout = proc.StandardOutput.ReadToEnd()
    let stderr = proc.StandardError.ReadToEnd()
    proc.WaitForExit()

    { ExitCode = proc.ExitCode
      Stdout = stdout
      Stderr = stderr }

let private realGit =
    let result = run "/usr/bin/which" [ "git" ] repositoryRoot []
    result.Stdout.Trim()

let private makeExecutable (path: string) =
    File.SetUnixFileMode(
        path,
        UnixFileMode.UserRead
        ||| UnixFileMode.UserWrite
        ||| UnixFileMode.UserExecute
        ||| UnixFileMode.GroupRead
        ||| UnixFileMode.GroupExecute
        ||| UnixFileMode.OtherRead
        ||| UnixFileMode.OtherExecute
    )

type DoctorProcessWorld() =
    let root =
        Path.Combine(Path.GetTempPath(), "rhino-doctor-e2e-" + Guid.NewGuid().ToString("N"))

    let bin = Path.Combine(root, "bin")
    let mutable args = [ "doctor" ]
    let mutable result: Result option = None

    let output () =
        result |> Option.map (fun r -> r.Stdout + r.Stderr) |> Option.defaultValue ""

    let stub (name: string) (text: string) =
        let path = Path.Combine(bin, name)
        File.WriteAllText(path, "#!/bin/sh\nprintf '%s\\n' '" + text.Replace("'", "'\\''") + "'\n")
        makeExecutable path

    /// Same as `stub`, but the banner goes to stderr with stdout left empty —
    /// the shape `java -version` actually has, and the only shape that proves
    /// `version-stream: stderr` is load-bearing.
    let stubStderr (name: string) (text: string) =
        let path = Path.Combine(bin, name)

        File.WriteAllText(path, "#!/bin/sh\nprintf '%s\\n' '" + text.Replace("'", "'\\''") + "' >&2\n")

        makeExecutable path

    let write (relative: string) (text: string) =
        let path = Path.Combine(root, relative)
        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, text)

    let removeStub (name: string) =
        let path = Path.Combine(bin, name)

        if File.Exists path then
            File.Delete path

    do
        Directory.CreateDirectory bin |> ignore

        Directory.CreateDirectory(Path.Combine(root, "home", "Library", "Caches", "ms-playwright", "chromium-1"))
        |> ignore

        write "package.json" "{\"name\":\"fixture\",\"volta\":{\"node\":\"24.11.1\",\"npm\":\"11.0.0\"}}"
        write "global.json" "{\"sdk\":{\"version\":\"10.0.103\"}}"

        write
            "apps/rhino-cli/rust-toolchain.toml"
            "[toolchain]\nchannel = \"1.90.0\"\ncomponents = [\"clippy\", \"rustfmt\"]\n"

        stub "git" "git version 2.43.0"
        // Doctor's target-share step also invokes Git commands. Delegate all
        // non-version calls to the host Git executable while retaining the
        // deterministic version probe above.
        let gitStub = Path.Combine(bin, "git")

        File.WriteAllText(
            gitStub,
            "#!/bin/sh\nif [ \"$1\" = \"--version\" ]; then printf '%s\\n' 'git version 2.43.0'; else exec '"
            + realGit
            + "' \"$@\"; fi\n"
        )

        makeExecutable gitStub

        [ "volta", "2.0.2"
          "node", "v24.11.1"
          "npm", "11.0.0"
          "rustc", "rustc 1.90.0 (fixture)"
          "cargo", "cargo-llvm-cov 0.6.0"
          "dotnet", "10.0.103"
          "docker", "Docker version 29.0.0, build fixture"
          "jq", "jq-1.7.1"
          "shellcheck", "version: 0.10.0"
          "hadolint", "Haskell Dockerfile Linter 2.12.0"
          "actionlint", "1.7.7"
          "npx", "Version 1.58.0"
          "shfmt", "v3.13.1"
          "tofu", "OpenTofu v1.12.3"
          "clang-format", "clang-format version 18.1.0" ]
        |> List.iter (fun (name, text) -> stub name text)

        let init = run realGit [ "init"; "--quiet" ] root []
        Assert.Equal(0, init.ExitCode)

    [<Given>]
    member _.``all required development tools are present with matching versions``() =
        [ "git"
          "volta"
          "node"
          "npm"
          "rustc"
          "cargo"
          "dotnet"
          "docker"
          "jq"
          "shellcheck"
          "hadolint"
          "actionlint"
          "npx"
          "shfmt"
          "tofu"
          "clang-format" ]
        |> List.iter (fun name ->
            Assert.True(File.Exists(Path.Combine(bin, name)), sprintf "%s fixture is absent" name))

    [<Given>]
    member _.``a required development tool is not found in the system PATH``() = removeStub "shellcheck"

    [<Given>]
    member _.``the tofu tool is not found in the system PATH``() = removeStub "tofu"

    [<Given>]
    member _.``the unselected shellcheck tool is not found in the system PATH``() = removeStub "shellcheck"

    [<Given>]
    member _.``only the tofu tool is selected``() = args <- args @ [ "--tools"; "tofu" ]

    [<Given>]
    member _.``an unknown Doctor tool is selected``() =
        args <- args @ [ "--tools"; "not-a-doctor-tool" ]

    [<Given>]
    member _.``a required development tool is installed with a non-matching version``() = stub "node" "v1.0.0"

    [<Given>]
    member _.``a tool is listed under the doctor skip-tools section of repo-config.yml``() =
        write "repo-config.yml" "doctor:\n  skip-tools: [shfmt]\n"
        removeStub "shfmt"

    [<Given>]
    member _.``a tool is listed under the doctor extra-tools section of repo-config.yml``() =
        stubStderr "java" "openjdk version \"25.0.4\" 2026-07-15"

        write
            "repo-config.yml"
            (String.concat
                "\n"
                [ "doctor:"
                  "  extra-tools:"
                  "    - name: java"
                  "      binary: java"
                  "      version-args: [\"-version\"]"
                  "      version-stream: stderr"
                  "      required-version: \"25\""
                  "      install:"
                  "        brew: [brew, install, --cask, temurin@25]"
                  "" ])

    [<Given>]
    member _.``a rust-toolchain.toml pins a channel and declares no lint components``() =
        write "apps/rhino-cli/rust-toolchain.toml" "[toolchain]\nchannel = \"1.90.0\"\n"

    [<Given>]
    member _.``a rust-toolchain.toml declares only the clippy lint component``() =
        write "apps/rhino-cli/rust-toolchain.toml" "[toolchain]\nchannel = \"1.90.0\"\ncomponents = [\"clippy\"]\n"

    member private _.Execute(extra: string list) =
        let environment =
            [ "PATH", bin
              "HOME", Path.Combine(root, "home")
              "GIT_CONFIG_GLOBAL", "/dev/null"
              "GIT_CONFIG_SYSTEM", "/dev/null"
              "CARGO_TARGET_DIR", Path.Combine(root, "cargo-target")
              "RHINO_CARGO_CACHE_DIR", Path.Combine(root, "cargo-cache") ]

        result <- Some(run cli.Value (args @ extra) root environment)

    [<When>]
    member this.``the developer runs the doctor command``() = this.Execute []

    [<When>]
    member this.``the developer runs the doctor command with JSON output``() = this.Execute [ "-o"; "json" ]

    [<When>]
    member this.``the developer runs the doctor command with minimal scope``() =
        args <- args @ [ "--scope"; "minimal" ]
        this.Execute []

    [<When>]
    member this.``the developer runs the doctor command with the fix flag``() =
        args <- args @ [ "--fix" ]
        this.Execute []

    [<When>]
    member this.``the developer runs the doctor command with fix and dry-run flags``() =
        args <- args @ [ "--fix"; "--dry-run" ]
        this.Execute []

    [<When>]
    member this.``"npm run doctor" runs``() = this.Execute []

    [<Then>]
    member _.``the command exits successfully``() = Assert.Equal(0, result.Value.ExitCode)

    [<Then>]
    member _.``the command exits with a failure code``() =
        Assert.NotEqual(0, result.Value.ExitCode)

    [<Then>]
    member _.``the output reports each tool as passing``() =
        Assert.DoesNotContain("\u2717", output ())

    [<Then>]
    member _.``the output identifies the missing tool``() =
        Assert.Contains("shellcheck", output ())

    [<Then>]
    member _.``the output reports the tool as a warning rather than a failure``() =
        Assert.Contains("\u26A0 node", output ())
        Assert.DoesNotContain("\u2717 node", output ())

    [<Then>]
    member _.``the output is valid JSON``() =
        use _document = JsonDocument.Parse(result.Value.Stdout) in ()

    [<Then>]
    member _.``the JSON lists every checked tool with its status``() =
        use document = JsonDocument.Parse(result.Value.Stdout)
        Assert.Equal(16, document.RootElement.GetProperty("tools").GetArrayLength())

    [<Then>]
    member _.``the output checks only the minimal tool set``() =
        Assert.Contains("Summary: 6/6 tools OK", output ())
        Assert.DoesNotContain(" rust ", output ())

    [<Then>]
    member _.``the output reports only the selected tofu tool``() =
        Assert.Contains("Summary: 1/1 tools OK", output ())
        Assert.DoesNotContain("shellcheck", output ())

    [<Then>]
    member _.``the selected tofu dry run previews only its remediation``() =
        Assert.Contains("Would install: tofu", output ())
        Assert.DoesNotContain("Would install: shellcheck", output ())

    [<Then>]
    member _.``the invalid selection is rejected before any tool is probed``() =
        Assert.Contains("unknown Doctor tool", result.Value.Stderr)
        Assert.DoesNotContain("Doctor Report", result.Value.Stdout)

    [<Then>]
    member _.``the output contains a dry-run preview``() =
        Assert.Contains("Would install: shellcheck", output ())

    [<Then>]
    member _.``the output handles verified OpenTofu remediation safely``() =
        Assert.Contains("expected_checksum=", output ())
        Assert.Contains("checksum mismatch", output ())

    [<Then>]
    member _.``the output reports nothing to fix``() =
        Assert.Contains("Nothing to fix", output ())

    [<Then>]
    member _.``the output does not include the skipped tool``() =
        Assert.DoesNotContain("shfmt", output ())

    [<Then>]
    member _.``the output includes the configured extra tool``() =
        Assert.Contains("java", output ())
        Assert.Contains("25.0.4", output ())

    [<Then>]
    member _.``it reports the toolchain component check as a warning naming rustfmt and clippy``() =
        Assert.Contains("does not declare the rustfmt, clippy component", output ())

    [<Then>]
    member _.``it reports the toolchain component check as a warning naming only rustfmt``() =
        Assert.Contains("does not declare the rustfmt component", output ())
        Assert.DoesNotContain("rustfmt, clippy", output ())

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists root then
            Directory.Delete(root, true)

module private FeatureRunner =
    let private featurePath =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "cli",
                "behaviours",
                "system",
                "doctor.feature"
            )
        )

    let run title =
        let lines = File.ReadAllLines featurePath

        let featureLine =
            lines |> Array.find (fun line -> line.TrimStart().StartsWith("Feature:"))

        let header = "Scenario: " + title
        let start = lines |> Array.findIndex (fun line -> line.Trim() = header)

        let finish =
            lines
            |> Array.skip (start + 1)
            |> Array.tryFindIndex (fun line ->
                line.TrimStart().StartsWith("Scenario:") || line.TrimStart().StartsWith("@"))
            |> Option.map (fun offset -> start + 1 + offset)
            |> Option.defaultValue lines.Length

        let snippet = Array.append [| featureLine; "" |] lines.[start .. finish - 1]

        let feature =
            StepDefinitions([| typeof<DoctorProcessWorld> |]).GenerateFeature(featurePath, snippet)

        (Seq.exactlyOne feature.Scenarios).Action.Invoke()

[<Theory>]
[<InlineData("All required tools are installed and versions match")>]
[<InlineData("A required tool is missing from the environment")>]
[<InlineData("A tool is installed but its version does not match the requirement")>]
[<InlineData("JSON output lists all tool check results")>]
[<InlineData("Minimal scope checks only core tools")>]
[<InlineData("Full scope is the default behaviour")>]
[<InlineData("An explicit tool selection probes and reports only that tool")>]
[<InlineData("A selected missing tool has only its remediation previewed")>]
[<InlineData("An unknown selected tool is rejected before environment checks")>]
[<InlineData("Fix with dry-run previews without executing")>]
[<InlineData("Fix dry-run previews a verified, platform-safe OpenTofu release archive")>]
[<InlineData("Fix reports nothing to fix when all tools are present")>]
[<InlineData("A repo-config-declared tool is skipped from the check")>]
[<InlineData("A pinned Rust toolchain without lint components is reported as a warning")>]
[<InlineData("A pinned Rust toolchain declaring only one lint component names just the missing one")>]
let ``doctor behaviour crosses the published process boundary`` title = FeatureRunner.run title
