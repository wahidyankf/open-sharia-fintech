/// TickSpec step definitions binding `doctor.feature`'s 17 scenarios to
/// `RhinoCli.Application.Doctor`'s tool-check engine [Repo-grounded —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature`,
/// `apps/rhino-cli/tests/doctor.rs`].
///
/// Named `DoctorToolCheckSteps` rather than `DoctorSteps` (already taken by
/// `DoctorSteps.fs`, which binds the sibling `cargo-target-share.feature`)
/// — follows `EnvSteps.fs`/`EnvInitSteps.fs`'s precedent of one Steps file
/// per feature file sharing an application module.
///
/// Mirrors `apps/rhino-cli/tests/doctor.rs`'s cucumber-rs `DoctorWorld`
/// strategy almost exactly: a synthetic repo directory holding `package.json`
/// and `apps/rhino-cli/rust-toolchain.toml`, plus a fake [`CommandRunner`]
/// that returns the same canned per-binary version strings as the Rust
/// suite's stub scripts — deterministic regardless of what the host actually
/// has installed. Unlike the Rust suite (which spawns the compiled binary
/// with a restricted `PATH`), these steps call `Doctor.checkAll`/`fixAll`
/// directly, the same "call the internal function directly" precedent
/// `DoctorSteps.fs`/`EnvInitSteps.fs` already establish for this port.
module RhinoCli.Tests.Unit.Steps.DoctorToolCheckSteps

open System
open System.IO
open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Application.Doctor

/// Canned per-binary `(stdout)` output, mirroring
/// `apps/rhino-cli/tests/doctor.rs`'s `STUB_TOOLS` table — every entry
/// satisfies the default config `writeConfig` below writes, so "all present"
/// never depends on what the host happens to have installed.
let private cannedOutput (binary: string) : string option =
    match binary with
    | "git" -> Some "git version 2.43.0"
    | "volta" -> Some "2.0.2"
    | "node" -> Some "v24.11.1"
    | "npm" -> Some "11.0.0"
    | "rustc" -> Some "rustc 1.90.0 (abc 2025-01-01)"
    | "cargo" -> Some "cargo-llvm-cov 0.6.0"
    | "dotnet" -> Some "10.0.103"
    | "docker" -> Some "Docker version 29.0.0, build abc"
    | "jq" -> Some "jq-1.7.1"
    | "shellcheck" -> Some "version: 0.10.0"
    | "hadolint" -> Some "Haskell Dockerfile Linter 2.12.0"
    | "actionlint" -> Some "1.7.7"
    | "shfmt" -> Some "v3.13.1"
    | "tofu" -> Some "OpenTofu v1.12.3"
    | "clang-format" -> Some "clang-format version 18.1.0"
    | "npx" -> Some "Version 1.58.0"
    | _ -> None

/// Finds the report line for the check named `name` in `report`'s plain-text
/// `formatDoctorText` output — matched by the report line's second
/// whitespace-delimited token (the name column) being exactly `name`, not
/// merely a substring match [Repo-grounded — `tests/doctor.rs::rust_report_
/// line`/`component_check_line`].
let private findCheckLine (name: string) (report: string) : string =
    report.Split('\n')
    |> Array.filter (fun line ->
        line.StartsWith("\u2713")
        || line.StartsWith("\u26A0")
        || line.StartsWith("\u2717"))
    |> Array.tryFind (fun line ->
        let parts = line.Split([| ' ' |], StringSplitOptions.RemoveEmptyEntries)
        parts.Length > 1 && parts.[1] = name)
    |> Option.defaultValue ""

/// Counts non-overlapping occurrences of `needle` in `haystack`.
let private countOccurrences (needle: string) (haystack: string) : int =
    let rec loop (fromIdx: int) (acc: int) : int =
        match haystack.IndexOf(needle, fromIdx, StringComparison.Ordinal) with
        | -1 -> acc
        | found -> loop (found + needle.Length) (acc + 1)

    loop 0 0

type DoctorToolCheckSteps() =
    let repoRoot =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-doctor-toolcheck-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        dir

    let mutable rustChannelOverride: string option = None
    let mutable scope: string option = None
    let mutable selectedTools: string list = []
    let mutable fixFlag = false
    let mutable dryRunFlag = false
    let mutable jsonFlag = false
    let mutable missingBinaries: Set<string> = Set.empty
    let mutable outputText = ""
    let mutable errorMessage: string option = None
    let mutable exitSuccess = true

    let writeConfig (nodeReq: string) (rustChannel: string) : unit =
        File.WriteAllText(
            Path.Combine(repoRoot, "package.json"),
            sprintf "{\"name\":\"t\",\"volta\":{\"node\":\"%s\",\"npm\":\"11.0.0\"}}" nodeReq
        )

        let rustDir = Path.Combine(repoRoot, "apps", "rhino-cli")
        Directory.CreateDirectory(rustDir) |> ignore

        File.WriteAllText(
            Path.Combine(rustDir, "rust-toolchain.toml"),
            sprintf
                "[toolchain]\nchannel = \"%s\"\ncomponents = [\"clippy\", \"rustfmt\", \"llvm-tools\"]\n"
                rustChannel
        )

    let ensureDefaultConfig () =
        if not (File.Exists(Path.Combine(repoRoot, "package.json"))) then
            writeConfig "24.11.1" "1.90.0"

    let fakeRunner: CommandRunner =
        fun binary _args ->
            if Set.contains binary missingBinaries then
                Error(sprintf "binary not found in PATH: %s" binary)
            else
                match cannedOutput binary with
                | Some out -> Ok(out, "", 0)
                | None -> Error(sprintf "binary not found in PATH: %s" binary)

    let fakeFixRunner: FixRunner = fun _command _args -> Ok()

    /// Runs the doctor check/fix pipeline against `repoRoot`, mirroring
    /// `commands/doctor.rs::run`'s composition — see this file's module doc
    /// comment for why this calls straight into `Doctor`'s functions rather
    /// than spawning a compiled binary.
    let exec () : unit =
        ensureDefaultConfig ()

        let invalidSelection =
            selectedTools
            |> List.tryPick (fun t ->
                match parseDoctorToolName t with
                | Error message -> Some message
                | Ok _ -> None)

        match invalidSelection with
        | Some message ->
            outputText <- ""
            errorMessage <- Some message
            exitSuccess <- false
        | None ->
            let options: CheckOptions =
                { RepoRoot = repoRoot
                  Runner = Some fakeRunner
                  Scope = (if scope = Some "minimal" then MinimalScope else FullScope)
                  SelectedTools =
                    (if List.isEmpty selectedTools then
                         None
                     else
                         Some selectedTools) }

            let result = checkAll options
            let sb = Text.StringBuilder()

            if jsonFlag then
                sb.Append(formatDoctorJson result 0L) |> ignore
            else
                sb.Append(formatDoctorText result false) |> ignore

            let mutable failed = false
            let mutable earlyOk = false

            if fixFlag && hasRemediationWork result then
                let fixBuf = Text.StringBuilder()

                let fr =
                    fixAll
                        result
                        options
                        { DryRun = dryRunFlag
                          Runner = Some fakeFixRunner }
                        (fun m -> fixBuf.Append(m: string) |> ignore)

                sb.Append(fixBuf.ToString()) |> ignore
                sb.Append(formatFixSummary fr) |> ignore

                if fr.Failed > 0 then
                    failed <- true
                elif not dryRunFlag && fr.Fixed > 0 then
                    earlyOk <- true

            if fixFlag && not (hasRemediationWork result) then
                sb.Append(formatNothingToFix) |> ignore

            outputText <- sb.ToString()
            errorMessage <- None

            exitSuccess <-
                if failed then false
                elif earlyOk then true
                elif result.MissingCount > 0 then false
                else true

    // ---- Given ----

    [<Given>]
    member _.``all required development tools are present with matching versions``() = writeConfig "24.11.1" "1.90.0"

    [<Given>]
    member _.``a required development tool is not found in the system PATH``() =
        writeConfig "24.11.1" "1.90.0"
        missingBinaries <- Set.add "shellcheck" missingBinaries

    [<Given>]
    member _.``the tofu tool is not found in the system PATH``() =
        writeConfig "24.11.1" "1.90.0"
        missingBinaries <- Set.add "tofu" missingBinaries

    [<Given>]
    member _.``the unselected shellcheck tool is not found in the system PATH``() =
        missingBinaries <- Set.add "shellcheck" missingBinaries

    [<Given>]
    member _.``only the tofu tool is selected``() = selectedTools <- [ "tofu" ]

    [<Given>]
    member _.``an unknown Doctor tool is selected``() =
        selectedTools <- [ "not-a-doctor-tool" ]

    [<Given>]
    member _.``a required development tool is installed with a non-matching version``() =
        // node requirement "1.0.0" but the fake runner reports v24.11.1 → warning.
        writeConfig "1.0.0" "1.90.0"

    [<Given>]
    member _.``a tool is listed under the doctor skip-tools section of repo-config.yml``() =
        writeConfig "24.11.1" "1.90.0"
        // Deliberately mark the skipped tool's binary missing too: if the
        // engine still probed it despite the skip-tools declaration, it would
        // come back Missing and the exit-successfully assertion would catch it.
        missingBinaries <- Set.add "shfmt" missingBinaries

        File.WriteAllText(Path.Combine(repoRoot, "repo-config.yml"), "doctor:\n  skip-tools: [shfmt]\n")

    [<Given>]
    member _.``the installed rustc differs from the pinned rust-toolchain.toml channel``() =
        // The fake runner's rustc stub always reports "1.90.0"; pin a
        // different channel to force a mismatch → warning.
        let rustChannel = "1.95.0"
        rustChannelOverride <- Some rustChannel
        writeConfig "24.11.1" rustChannel

    [<Given>]
    member _.``a rust-toolchain.toml pins a channel and declares no lint components``() =
        writeConfig "24.11.1" "1.90.0"

        File.WriteAllText(
            Path.Combine(repoRoot, "apps", "rhino-cli", "rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.90.0\"\n"
        )

    [<Given>]
    member _.``a rust-toolchain.toml declares only the clippy lint component``() =
        writeConfig "24.11.1" "1.90.0"

        File.WriteAllText(
            Path.Combine(repoRoot, "apps", "rhino-cli", "rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.90.0\"\ncomponents = [\"clippy\"]\n"
        )

    // ---- When ----

    [<When>]
    member _.``the developer runs the doctor command``() = exec ()

    [<When>]
    member _.``the developer runs the doctor command with JSON output``() =
        jsonFlag <- true
        exec ()

    [<When>]
    member _.``the developer runs the doctor command with minimal scope``() =
        scope <- Some "minimal"
        exec ()

    [<When>]
    member _.``the developer runs the doctor command with the fix flag``() =
        fixFlag <- true
        exec ()

    [<When>]
    member _.``the developer runs the doctor command with fix and dry-run flags``() =
        fixFlag <- true
        dryRunFlag <- true
        exec ()

    [<When>]
    member _.``"npm run doctor" runs``() = exec ()

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() = Assert.True(exitSuccess, outputText)

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.False(exitSuccess, outputText)

    [<Then>]
    member _.``the output reports each tool as passing``() =
        Assert.Contains("Doctor Report", outputText)
        Assert.DoesNotContain("\u2717", outputText)

    [<Then>]
    member _.``the output identifies the missing tool``() =
        let lower = outputText.ToLowerInvariant()

        Assert.True(
            outputText.Contains("\u2717")
            || lower.Contains("missing")
            || lower.Contains("not found"),
            outputText
        )

    [<Then>]
    member _.``the output reports the tool as a warning rather than a failure``() =
        Assert.True(exitSuccess, outputText)

        Assert.True(
            outputText.Contains("\u26A0")
            || outputText.ToLowerInvariant().Contains("warning"),
            outputText
        )

    [<Then>]
    member _.``the output is valid JSON``() =
        use _doc = JsonDocument.Parse(outputText)
        ()

    [<Then>]
    member _.``the JSON lists every checked tool with its status``() =
        use doc = JsonDocument.Parse(outputText)
        let tools = doc.RootElement.GetProperty("tools")
        Assert.Equal(16, tools.GetArrayLength())

        for tool in tools.EnumerateArray() do
            let hasStatus, _ = tool.TryGetProperty("status")
            Assert.True(hasStatus, "every tool entry must carry a status")

    [<Then>]
    member _.``the output checks only the minimal tool set``() =
        Assert.Contains("(scope: minimal)", outputText)
        Assert.Contains("Summary: 6/6 tools OK", outputText)
        Assert.Equal("", findCheckLine "rust" outputText)

    [<Then>]
    member _.``the output contains fix progress``() =
        Assert.True(
            outputText.Contains("Fix summary")
            || outputText.Contains("Installing")
            || outputText.Contains("Skip:"),
            outputText
        )

    [<Then>]
    member _.``the output contains a dry-run preview``() =
        Assert.True(outputText.Contains("Would install") || outputText.Contains("Skip:"), outputText)

    [<Then>]
    member _.``the output handles verified OpenTofu remediation safely``() =
        Assert.Contains("Would install: tofu", outputText)
        Assert.Contains("https://github.com/opentofu/opentofu/releases/download/v1.12.3", outputText)
        Assert.Contains("tofu_1.12.3_", outputText)
        Assert.Contains("expected_checksum=", outputText)
        Assert.Contains("checksum mismatch", outputText)
        Assert.DoesNotContain("install-opentofu.sh", outputText)

    [<Then>]
    member _.``the output reports only the selected tofu tool``() =
        let checkLines =
            outputText.Split('\n')
            |> Array.filter (fun l -> l.StartsWith("\u2713") || l.StartsWith("\u26A0") || l.StartsWith("\u2717"))

        Assert.Equal(1, checkLines.Length)
        Assert.Contains("tofu", checkLines.[0])
        Assert.DoesNotContain("shellcheck", outputText)
        Assert.Contains("Summary: 1/1 tools OK", outputText)

    [<Then>]
    member _.``the selected tofu dry run previews only its remediation``() =
        Assert.Contains("Would install: tofu", outputText)
        Assert.Contains("expected_checksum=", outputText)
        Assert.Contains("Summary: 0/1 tools OK", outputText)
        Assert.Equal(1, countOccurrences "Would install:" outputText)

    [<Then>]
    member _.``the invalid selection is rejected before any tool is probed``() =
        Assert.DoesNotContain("Doctor Report", outputText)
        Assert.DoesNotContain("Summary:", outputText)

        Assert.True(
            errorMessage
            |> Option.map (fun m -> m.Contains("unknown Doctor tool \"not-a-doctor-tool\""))
            |> Option.defaultValue false,
            sprintf "unexpected error: %A" errorMessage
        )

    [<Then>]
    member _.``the output reports nothing to fix``() =
        Assert.Contains("Nothing to fix", outputText)

    [<Then>]
    member _.``the output does not include the skipped tool``() =
        Assert.DoesNotContain("shfmt", outputText)

    [<Then>]
    member _.``it reports the Rust toolchain as mismatched``() =
        Assert.True(exitSuccess, outputText)
        let line = findCheckLine "rust" outputText
        Assert.True(line.StartsWith("\u26A0") || line.ToLowerInvariant().Contains("warning"), line)

    [<Then>]
    member _.``it names the pinned channel as the expected value``() =
        let expected =
            rustChannelOverride
            |> Option.defaultWith (fun () -> failwith "rustChannelOverride set by a prior Given step")

        let line = findCheckLine "rust" outputText
        Assert.Contains(sprintf "required: %s" expected, line)

    [<Then>]
    member _.``it reports the toolchain component check as a warning naming rustfmt and clippy``() =
        let line = findCheckLine "rust-toolchain-components" outputText
        Assert.True(line.StartsWith("\u26A0") || line.ToLowerInvariant().Contains("warning"), line)
        Assert.Contains("rustfmt", line)
        Assert.Contains("clippy", line)

    [<Then>]
    member _.``it reports the toolchain component check as a warning naming only rustfmt``() =
        let line = findCheckLine "rust-toolchain-components" outputText
        Assert.True(line.StartsWith("\u26A0") || line.ToLowerInvariant().Contains("warning"), line)
        Assert.Contains("does not declare the rustfmt component", line)
        Assert.DoesNotContain("rustfmt, clippy", line)
        Assert.DoesNotContain("clippy, rustfmt", line)

    [<AfterScenario>]
    member _.Cleanup() =
        if Directory.Exists repoRoot then
            Directory.Delete(repoRoot, true)

// ---------------------------------------------------------------------------
// FeatureRunner
// ---------------------------------------------------------------------------

/// Reads one named `Scenario:` block out of the real, frozen `doctor.feature`
/// file (leaving the file itself untouched) and runs it through TickSpec
/// bound only against `DoctorToolCheckSteps` — see `EnvSteps.fs`'s
/// `FeatureRunner` for why this is per-scenario rather than per-file.
module private FeatureRunner =

    let private featurePath: string =
        Path.GetFullPath(
            Path.Combine(
                __SOURCE_DIRECTORY__,
                "..",
                "..",
                "..",
                "..",
                "..",
                "..",
                "specs",
                "apps",
                "rhino",
                "behavior",
                "rhino-cli",
                "gherkin",
                "system",
                "doctor.feature"
            )
        )

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let scenarioHeader = sprintf "Scenario: %s" scenarioTitle
        let startIdx = featureLines |> Array.findIndex (fun l -> l.Trim() = scenarioHeader)

        let endIdx =
            featureLines
            |> Array.skip (startIdx + 1)
            |> Array.tryFindIndex (fun l ->
                let trimmed = l.Trim()

                trimmed.StartsWith("Scenario:", StringComparison.Ordinal)
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from `doctor.feature`,
    /// bound against `DoctorToolCheckSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<DoctorToolCheckSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``All required tools are installed and versions match`` () =
    FeatureRunner.run "All required tools are installed and versions match"

[<Fact>]
let ``A required tool is missing from the environment`` () =
    FeatureRunner.run "A required tool is missing from the environment"

[<Fact>]
let ``A tool is installed but its version does not match the requirement`` () =
    FeatureRunner.run "A tool is installed but its version does not match the requirement"

[<Fact>]
let ``JSON output lists all tool check results`` () =
    FeatureRunner.run "JSON output lists all tool check results"

[<Fact>]
let ``Minimal scope checks only core tools`` () =
    FeatureRunner.run "Minimal scope checks only core tools"

[<Fact>]
let ``Full scope is the default behavior`` () =
    FeatureRunner.run "Full scope is the default behavior"

[<Fact>]
let ``An explicit tool selection probes and reports only that tool`` () =
    FeatureRunner.run "An explicit tool selection probes and reports only that tool"

[<Fact>]
let ``A selected missing tool has only its remediation previewed`` () =
    FeatureRunner.run "A selected missing tool has only its remediation previewed"

[<Fact>]
let ``An unknown selected tool is rejected before environment checks`` () =
    FeatureRunner.run "An unknown selected tool is rejected before environment checks"

[<Fact>]
let ``Fix installs missing tools`` () =
    FeatureRunner.run "Fix installs missing tools"

[<Fact>]
let ``Fix with dry-run previews without executing`` () =
    FeatureRunner.run "Fix with dry-run previews without executing"

[<Fact>]
let ``Fix dry-run previews a verified, platform-safe OpenTofu release archive`` () =
    FeatureRunner.run "Fix dry-run previews a verified, platform-safe OpenTofu release archive"

[<Fact>]
let ``Fix reports nothing to fix when all tools are present`` () =
    FeatureRunner.run "Fix reports nothing to fix when all tools are present"

[<Fact>]
let ``A repo-config-declared tool is skipped from the check`` () =
    FeatureRunner.run "A repo-config-declared tool is skipped from the check"

[<Fact>]
let ``doctor compares rustc against the toolchain that builds`` () =
    FeatureRunner.run "doctor compares rustc against the toolchain that builds"

[<Fact>]
let ``A pinned Rust toolchain without lint components is reported as a warning`` () =
    FeatureRunner.run "A pinned Rust toolchain without lint components is reported as a warning"

[<Fact>]
let ``A pinned Rust toolchain declaring only one lint component names just the missing one`` () =
    FeatureRunner.run "A pinned Rust toolchain declaring only one lint component names just the missing one"
