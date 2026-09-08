module RhinoCli.Tests.Unit.Steps.DoctorCoverageTests

open System
open Xunit
open RhinoCli.Application.Doctor

let private check name status installed required note : ToolCheck =
    { Name = name
      Binary = name
      Status = status
      InstalledVersion = installed
      RequiredVersion = required
      Source = "repo-config.yml"
      Note = note }

let private definition name useStderr parse compare install : ToolDef =
    { Name = name
      Binary = name
      Source = "fixture"
      Args = [ "--version" ]
      UseStderr = useStderr
      ParseVer = parse
      Compare = compare
      ReadReq = fun () -> "2.0.0"
      InstallCmd = install }

[<Fact>]
let ``Doctor value parsers and status codes cover every pure decision`` () =
    Assert.True(isCi true false)
    Assert.True(isCi false true)
    Assert.False(isCi false false)
    Assert.Equal("override", cacheRootFrom (Some "override") (Some "home"))
    Assert.EndsWith(".cache/ose-cargo-target", cacheRootFrom None (Some "home"))
    Assert.EndsWith(".cache/ose-cargo-target", cacheRootFrom None None)
    Assert.Equal("repo", repoName "/tmp/repo/.git")
    Assert.Equal("", repoName "/")
    Assert.EndsWith("repo/crate", sharedTargetPath "cache" "repo" "apps/crate/")

    Assert.Equal("ok", toolStatusCode Passing)
    Assert.Equal("warning", toolStatusCode Warning)
    Assert.Equal("missing", toolStatusCode Missing)
    Assert.Equal("full", doctorScopeCode FullScope)
    Assert.Equal("minimal", doctorScopeCode MinimalScope)
    Assert.Equal(Some FullScope, parseDoctorScope "")
    Assert.Equal(Some FullScope, parseDoctorScope "full")
    Assert.Equal(Some MinimalScope, parseDoctorScope "minimal")
    Assert.Equal(None, parseDoctorScope "other")
    Assert.True(isMinimalTool "git")
    Assert.False(isMinimalTool "rust")
    Assert.True(Result.isError (parseDoctorToolName builtinDoctorToolInventory "  "))
    Assert.True(Result.isError (parseDoctorToolName builtinDoctorToolInventory "unknown"))
    Assert.Equal(Ok "git", parseDoctorToolName builtinDoctorToolInventory " git ")

[<Fact>]
let ``Version comparators cover semantic ordering and malformed fallbacks`` () =
    Assert.Equal("1.2.3", normalizeSimpleVersion "v1.2.3")
    Assert.Equal("1.2.3", normalizeSimpleVersion "1.2.3")
    Assert.Equal((Passing, "no version requirement"), compareExact "1" "")
    Assert.Equal(Passing, compareExact "v1" "1" |> fst)
    Assert.Equal(Warning, compareExact "1" "2" |> fst)
    Assert.Equal(Some(1L, 2L, 0L), parseVersionParts "v1.2")
    Assert.Equal(None, parseVersionParts "one.two")

    for installed, required, expected in
        [ "2.0.0", "1.9.9", Passing
          "1.3.0", "1.2.9", Passing
          "1.2.3", "1.2.3", Passing
          "1.2.2", "1.2.3", Warning
          "bad", "also-bad", Warning ] do
        Assert.Equal(expected, compareGte installed required |> fst)

    Assert.Equal(Passing, compareGte "1" "" |> fst)
    Assert.Equal(Passing, compareMajorGte "3.0" "2.9" |> fst)
    Assert.Equal(Warning, compareMajorGte "1.9" "2.0" |> fst)
    Assert.Equal(Warning, compareMajorGte "bad" "also-bad" |> fst)
    Assert.Equal(Passing, compareMajorGte "1" "" |> fst)

[<Fact>]
let ``Every version parser handles its success and empty shape`` () =
    Assert.Equal("1.2.3", parseTrimVersion " v1.2.3 ")
    Assert.Equal("2.4", parseLineWord "skip\ngit version v2.4" "git version " 2 "v")
    Assert.Equal("", parseLineWord "git version" "git version" 9 "")
    Assert.Equal("", parseLineWord "other" "git version" 2 "")
    Assert.Equal("2.1", parseGitVersion "git version 2.1")
    Assert.Equal("1.8", parseTofuVersion "OpenTofu v1.8")
    Assert.Equal("1.80", parseRustVersion "rustc 1.80")
    Assert.Equal("0.6", parseCargoLlvmCovVersion "cargo-llvm-cov 0.6")
    Assert.Equal("8.0", parseDotnetVersion " 8.0 ")
    Assert.Equal("27.1.1", parseDockerVersion "Docker version 27.1.1, build abc")
    Assert.Equal("", parseDockerVersion "Docker version")
    Assert.Equal("0.10", parseShellcheckVersion "name: ShellCheck\nversion: 0.10")
    Assert.Equal("", parseShellcheckVersion "none")
    Assert.Equal("2.12", parseHadolintVersion "Haskell Dockerfile Linter 2.12")
    Assert.Equal("1.7", parseActionlintVersion " 1.7 \nextra")
    Assert.Equal("1.7", parseJqVersion " jq-1.7 ")
    Assert.Equal("raw", parseJqVersion "raw")
    Assert.Equal("1.50", parsePlaywrightVersion "Version 1.50")
    Assert.Equal("18.1.2", parseClangFormatVersion "Ubuntu clang-format version 18.1.2")
    Assert.Equal("", parseClangFormatVersion "clang-format version")
    Assert.EndsWith("Library/Caches/ms-playwright", playwrightCacheDirFor true "/home")
    Assert.EndsWith(".cache/ms-playwright", playwrightCacheDirFor false "/home")

[<Fact>]
let ``Rust toolchain component parser covers inline multiline comments and omissions`` () =
    Assert.Equal<string list>(
        [ "rustfmt"; "clippy" ],
        readRustToolchainComponents "components = [\"rustfmt\", 'clippy'] # ok"
    )

    Assert.Equal<string list>(
        [ "rustfmt"; "clippy" ],
        readRustToolchainComponents "components = [\n \"rustfmt\",\n \"clippy\"\n]"
    )

    Assert.Empty(readRustToolchainComponents "channel = \"stable\"\ncomponents = nope")

    Assert.True(
        rustToolchainLintComponentCheck "toolchain" "components=[\"rustfmt\",\"clippy\"]"
        |> Option.isNone
    )

    let warning =
        rustToolchainLintComponentCheck "toolchain" "components=[\"clippy\"]"
        |> Option.get

    Assert.Contains("rustfmt", warning.Note)

[<Fact>]
let ``Install builders cover every supported platform branch`` () =
    let builders =
        [ installGit
          installVolta
          installNode
          installNpm
          installRust
          installCargoLlvmCov
          installDotnet
          installDocker
          installJq
          installShellcheck
          installActionlint
          installHadolint
          installShfmt
          installTofu
          installClangFormat
          installPlaywright ]

    for builder in builders do
        for platform in [ "darwin"; "linux"; "other" ] do
            let steps = builder "1.2.3" platform

            steps
            |> List.iter (fun step -> Assert.False(String.IsNullOrWhiteSpace step.Command))

    Assert.Equal("8.0", dotnetChannel "8.0.401")
    Assert.Equal("10.0", dotnetChannel "preview")
    let inventory = buildToolDefs "/synthetic/repo"
    Assert.Equal(builtinDoctorToolInventory.Length, inventory.Length)
    Assert.Equal("", inventory.[0].ReadReq())
    Assert.Equal("", inventory.[1].ReadReq())

[<Fact>]
let ``Tool selection runner aggregation and reports cover every pure outcome`` () =
    let defs =
        [ definition "git" false parseTrimVersion compareExact None
          definition "rust" true parseTrimVersion compareExact None ]

    Assert.Single(selectToolDefs defs MinimalScope None []) |> ignore
    Assert.Single(selectToolDefs defs FullScope (Some [ "rust" ]) []) |> ignore
    Assert.Single(selectToolDefs defs FullScope None [ "rust" ]) |> ignore

    let passing = runOneDef (fun _ _ -> Ok("2.0.0", "", 0)) defs.[0]
    let stderr = runOneDef (fun _ _ -> Ok("", "2.0.0", 1)) defs.[1]
    let missing = runOneDef (fun _ _ -> Error "absent") defs.[0]
    Assert.Equal(Passing, passing.Status)
    Assert.Equal(Passing, stderr.Status)
    Assert.Equal(Missing, missing.Status)

    let result =
        aggregateDoctorChecks MinimalScope [ passing; { stderr with Status = Warning }; missing ]

    Assert.Equal((1, 1, 1), (result.OkCount, result.WarnCount, result.MissingCount))
    Assert.True(needsRemediation missing)

    Assert.True(
        needsRemediation
            { missing with
                Name = "tofu"
                Status = Warning }
    )

    Assert.False(
        needsRemediation
            { missing with
                Name = "git"
                Status = Warning }
    )

    Assert.True(hasRemediationWork result)
    Assert.False(hasRemediationWork (aggregateDoctorChecks FullScope [ passing ]))
    Assert.Equal("darwin", platformFromFlags true false)
    Assert.Equal("linux", platformFromFlags false true)
    Assert.Equal("other", platformFromFlags false false)

    let text = formatDoctorText result false
    Assert.Contains("scope: minimal", text)
    Assert.DoesNotContain("Doctor Report", formatDoctorText result true)

    let json =
        formatDoctorJsonAt (DateTimeOffset(2026, 1, 2, 3, 4, 5, TimeSpan.Zero)) result 9L

    Assert.Contains("\"status\": \"missing\"", json)
    Assert.Contains("\"duration_ms\": 9", json)

    let warningOnly =
        aggregateDoctorChecks FullScope [ { passing with Status = Warning } ]

    Assert.Contains("\"status\": \"warning\"", formatDoctorJsonAt DateTimeOffset.UnixEpoch warningOnly 0L)

    let passingOnly =
        aggregateDoctorChecks
            FullScope
            [ { passing with
                  Source = ""
                  Note = ""
                  RequiredVersion = "" } ]

    Assert.Contains("\"status\": \"ok\"", formatDoctorJsonAt DateTimeOffset.UnixEpoch passingOnly 0L)

    let markdown =
        formatDoctorMarkdownAt (DateTimeOffset(2026, 1, 2, 3, 4, 5, TimeSpan.Zero)) result

    Assert.Contains("## Doctor Report", markdown)
    Assert.Contains("| Missing | 1 |", markdown)

[<Fact>]
let ``Pure fix engine covers success failure skip dry-run and missing definition`` () =
    let actionable = check "tofu" Missing "" "1.2.3" "missing"
    let okay = check "git" Passing "2" "2" "ok"
    let noInstall = definition "tofu" false id compareExact None
    let noSteps = definition "tofu" false id compareExact (Some(fun _ _ -> []))

    let oneStep =
        definition
            "tofu"
            false
            id
            compareExact
            (Some(fun _ _ ->
                [ { Description = "install"
                    Command = "tool"
                    Args = [ "arg" ] } ]))

    let twoSteps =
        definition
            "tofu"
            false
            id
            compareExact
            (Some(fun _ _ ->
                [ { Description = "first"
                    Command = "tool"
                    Args = [] }
                  { Description = "second"
                    Command = "tool"
                    Args = [] } ]))

    let result = aggregateDoctorChecks FullScope [ actionable; okay ]
    let messages = Text.StringBuilder()
    let emit (text: string) = messages.Append(text) |> ignore

    let skipped =
        fixAtPlatform
            "linux"
            result
            [ noInstall ]
            { DryRun = false
              Runner = Some(fun _ _ -> Ok()) }
            emit

    Assert.Equal(1, skipped.Skipped)
    Assert.Equal(1, skipped.AlreadyOk)

    let empty =
        fixAtPlatform
            "other"
            (aggregateDoctorChecks FullScope [ actionable ])
            [ noSteps ]
            { DryRun = false
              Runner = Some(fun _ _ -> Ok()) }
            emit

    Assert.Equal(1, empty.Skipped)

    let preview =
        fixAtPlatform
            "darwin"
            (aggregateDoctorChecks FullScope [ actionable ])
            [ oneStep ]
            { DryRun = true
              Runner = Some(fun _ _ -> failwith "runner called") }
            emit

    Assert.Equal(0, preview.Fixed)

    let fixedResult =
        fixAtPlatform
            "linux"
            (aggregateDoctorChecks FullScope [ actionable ])
            [ oneStep ]
            { DryRun = false
              Runner = Some(fun _ _ -> Ok()) }
            emit

    Assert.Equal(1, fixedResult.Fixed)

    let mutable calls = 0

    let twoStepResult =
        fixAtPlatform
            "linux"
            (aggregateDoctorChecks FullScope [ actionable ])
            [ twoSteps ]
            { DryRun = false
              Runner =
                Some(fun _ _ ->
                    calls <- calls + 1
                    Ok()) }
            emit

    Assert.Equal(2, calls)
    Assert.Equal(1, twoStepResult.Fixed)

    let failed =
        fixAtPlatform
            "linux"
            (aggregateDoctorChecks FullScope [ actionable ])
            [ oneStep ]
            { DryRun = false
              Runner = Some(fun _ _ -> Error "boom") }
            emit

    Assert.Equal(1, failed.Failed)

    let unmatched =
        fixAtPlatform
            "linux"
            (aggregateDoctorChecks FullScope [ actionable ])
            []
            { DryRun = false
              Runner = Some(fun _ _ -> Ok()) }
            emit

    Assert.Equal(1, unmatched.Skipped)

    Assert.Contains(
        "1 fixed",
        formatFixSummary
            { Fixed = 1
              Failed = 2
              AlreadyOk = 3
              Skipped = 4 }
    )

[<Fact>]
let ``Target-share planners and formatters cover all pure states`` () =
    let crates = [ "/repo/apps/a"; "/repo/libs/b" ]

    let kind (crate: string) (_: string) =
        if crate.EndsWith("a") then CorrectTargetLink
        elif crate.EndsWith("b") then PlainTargetDirectory
        elif crate.EndsWith("c") then TargetAbsent
        else ReplaceableTargetEntry

    let allCrates = crates @ [ "/repo/apps/c"; "/repo/apps/d" ]
    let plans = planTargetShares "/cache" "repo" false allCrates kind
    Assert.Equal(4, plans.Length)
    Assert.True(planTargetShares "/cache" "repo" true crates kind |> List.isEmpty)
    let summary = summarizeTargetSharePlan false plans
    Assert.Equal(3, summary.Created)
    Assert.Equal(1, summary.AlreadyCorrect)
    Assert.True((summarizeTargetSharePlan true plans).SkippedCi)

    let live = Set.ofList [ "/cache/live" ]
    let dry = planPruneOrphans [ "/cache/live"; "/cache/orphan" ] (Some live) true false
    Assert.Single(dry.Candidates) |> ignore
    Assert.True((planPruneOrphans [] None false false).EnumerationFailed)
    Assert.True((planPruneOrphans [] (Some Set.empty) false true).SkippedCi)
    Assert.Contains("CI detected", formatCheckReport [] true)
    Assert.Contains("all crates", formatCheckReport [] false)

    Assert.Contains(
        "need sharing",
        formatCheckReport
            [ { CrateDir = "crate"
                SharedPath = "cache" } ]
            false
    )

    Assert.Contains("CI detected", formatFixReport { summary with SkippedCi = true })
    Assert.Contains("already correct", formatFixReport summary)
    Assert.Contains("could not enumerate", formatPruneReport { dry with EnumerationFailed = true } false)
    Assert.Contains("candidate", formatPruneReport dry true)

    Assert.Contains(
        "deleted",
        formatPruneReport
            { dry with
                Deleted = [ "a" ]
                Candidates = [] }
            false
    )

    Assert.Contains(
        "0 orphaned",
        formatPruneReport
            { dry with
                Deleted = []
                Candidates = [] }
            false
    )

    Assert.Contains(
        "skipped",
        formatSweepReport
            { Skipped = true
              SkippedCi = false
              Ran = false }
    )

    Assert.Contains(
        "CI detected",
        formatSweepReport
            { Skipped = false
              SkippedCi = true
              Ran = false }
    )

    Assert.Equal(
        "",
        formatSweepReport
            { Skipped = false
              SkippedCi = false
              Ran = true }
    )

[<Fact>]
let ``Configured extra tools join the inventory, stay rejectable, and probe stderr`` () =
    let javaTool: RhinoCli.Application.RepoConfig.DoctorExtraTool =
        { Name = "java"
          Binary = "java"
          VersionArgs = [ "-version" ]
          VersionStream = RhinoCli.Application.RepoConfig.StderrStream
          RequiredVersion = "25"
          Install = Map.ofList [ "brew", [ "brew"; "install"; "--cask"; "temurin@25" ] ] }

    let configured =
        { RhinoCli.Application.RepoConfig.empty with
            Doctor =
                { RhinoCli.Application.RepoConfig.empty.Doctor with
                    ExtraTools = [ javaTool ] } }

    // A declared extra tool joins the inventory the CLI validates `--tools` against.
    let resolved = doctorToolInventoryFor configured
    Assert.Contains("java", resolved)
    Assert.Equal(builtinDoctorToolInventory.Length + 1, resolved.Length)
    Assert.Equal(Ok "java", parseDoctorToolName resolved " java ")

    // A name in neither inventory is still rejected, and a configured name is
    // still rejected against an inventory that does not declare it.
    Assert.True(Result.isError (parseDoctorToolName resolved "not-a-doctor-tool"))
    Assert.True(Result.isError (parseDoctorToolName resolved "  "))
    Assert.True(Result.isError (parseDoctorToolName builtinDoctorToolInventory "java"))

    // The default configuration adds nothing, so the refactor is a no-op until
    // a tool is actually declared.
    Assert.Equal<string list>(builtinDoctorToolInventory, doctorToolInventoryFor RhinoCli.Application.RepoConfig.empty)

    // A tool whose version lands on stderr parses from stderr, not stdout.
    let javaDef = extraToolDef javaTool
    Assert.True(javaDef.UseStderr)
    Assert.Equal<string list>([ "-version" ], javaDef.Args)

    let stderrOnly =
        runOneDef (fun _ _ -> Ok("", "openjdk version \"25.0.4\" 2026-07-15", 0)) javaDef

    Assert.Equal(Passing, stderrOnly.Status)
    Assert.Equal("25.0.4", stderrOnly.InstalledVersion)

    // The same probe reading stdout would see nothing — this is why
    // `version-stream` exists at all.
    let stdoutReader = { javaDef with UseStderr = false }

    Assert.Equal(
        Warning,
        (runOneDef (fun _ _ -> Ok("", "openjdk version \"25.0.4\" 2026-07-15", 0)) stdoutReader).Status
    )

    // Extra tools are appended to the built-in defs so selection filters them
    // exactly like a built-in.
    let defs = buildToolDefsFor configured "/synthetic/repo"
    Assert.Equal(builtinDoctorToolInventory.Length + 1, defs.Length)
    Assert.Single(selectToolDefs defs FullScope (Some [ "java" ]) []) |> ignore
    Assert.Empty(selectToolDefs defs FullScope (Some [ "java" ]) [ "java" ])

    // An extra tool carries its declared per-platform install command.
    let steps = (Option.get javaDef.InstallCmd) "25" "darwin"
    Assert.Single(steps) |> ignore
    Assert.Equal("brew", steps.Head.Command)
    Assert.Equal<string list>([ "install"; "--cask"; "temurin@25" ], steps.Head.Args)
    Assert.Empty((Option.get javaDef.InstallCmd) "25" "other")

[<Fact>]
let ``Extra-tool declarations round-trip through the repo-config parser`` () =
    let document =
        String.concat
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
              "        apt: [apt-get, install, -y, temurin-25-jdk]"
              // Every optional field omitted: proves each one has a default
              // rather than throwing on a sparse declaration.
              "    - name: sparse"
              "    - name: odd"
              "      binary: odd"
              "      version-stream: stdout"
              "" ]

    let config =
        match RhinoCli.Application.RepoConfig.parse document with
        | Ok config -> config
        | Error message -> failwithf "expected a parse, got: %s" message

    let tools = config.Doctor.ExtraTools
    Assert.Equal(3, tools.Length)
    Assert.Equal<string list>([ "java"; "sparse"; "odd" ], tools |> List.map (fun t -> t.Name))

    let java = tools.Head
    Assert.Equal("java", java.Binary)
    Assert.Equal<string list>([ "-version" ], java.VersionArgs)
    Assert.Equal(RhinoCli.Application.RepoConfig.StderrStream, java.VersionStream)
    Assert.Equal("25", java.RequiredVersion)
    Assert.Equal<string list>([ "apt-get"; "install"; "-y"; "temurin-25-jdk" ], java.Install.["apt"])

    let sparse = tools.[1]
    Assert.Equal("", sparse.Binary)
    Assert.Empty(sparse.VersionArgs)
    Assert.Equal(RhinoCli.Application.RepoConfig.StdoutStream, sparse.VersionStream)
    Assert.Equal("", sparse.RequiredVersion)
    Assert.Empty(sparse.Install)

    Assert.Equal(RhinoCli.Application.RepoConfig.StdoutStream, tools.[2].VersionStream)

    // An unrecognized stream is a hard parse fault, not a silent fallback to
    // stdout: a mis-spelled stream on a stderr tool would otherwise report an
    // installed tool as missing.
    match
        RhinoCli.Application.RepoConfig.parse
            "doctor:\n  extra-tools:\n    - name: odd\n      version-stream: sideways\n"
    with
    | Ok _ -> failwith "an unknown version-stream must not parse"
    | Error message ->
        Assert.Contains("doctor.extra-tools[0].version-stream", message)
        Assert.Contains("unknown variant `sideways`", message)
        Assert.Contains("`stdout`, `stderr`", message)

    // A declaration with no install map carries no remediation rather than an
    // install command that would run with no arguments.
    Assert.True((extraToolDef sparse).InstallCmd.IsNone)

    // Both package managers Doctor knows how to dispatch to, plus the platform
    // that has neither.
    Assert.Equal(Some "brew", installManagerFor "darwin")
    Assert.Equal(Some "apt", installManagerFor "linux")
    Assert.Equal(None, installManagerFor "other")

    let installer = (extraToolDef java).InstallCmd |> Option.get
    Assert.Equal("apt-get", (installer "25" "linux").Head.Command)

    // Declared for a manager this platform does not use: no steps, not a crash.
    let brewOnly =
        { java with
            Install = Map.ofList [ "brew", [ "brew"; "install" ] ] }

    Assert.Empty(((extraToolDef brewOnly).InstallCmd |> Option.get) "25" "linux")

[<Fact>]
let ``Extra-tool declarations must be runnable and must not shadow a built-in`` () =
    let findings document =
        match RhinoCli.Application.RepoConfig.parse document with
        | Ok config -> RhinoCli.Application.RepoConfig.semanticFindings config
        | Error message -> failwithf "expected a parse, got: %s" message

    // A complete declaration is accepted — the conforming direction, without
    // which the checks below prove only that something always fails.
    Assert.Empty(
        findings (
            String.concat
                "\n"
                [ "doctor:"
                  "  extra-tools:"
                  "    - name: java"
                  "      binary: java"
                  "      version-args: [\"-version\"]"
                  "" ]
        )
    )

    let blank =
        findings (String.concat "\n" [ "doctor:"; "  extra-tools:"; "    - version-args: []"; "" ])

    Assert.Contains("doctor.extra-tools[0].name: required field is missing or blank", blank)
    Assert.Contains("doctor.extra-tools[0].binary: required field is missing or blank", blank)
    Assert.Contains(blank, fun f -> f.StartsWith("doctor.extra-tools[0].version-args: required field"))

    let shadowing =
        findings (
            String.concat
                "\n"
                [ "doctor:"
                  "  extra-tools:"
                  "    - name: jq"
                  "      binary: jq"
                  "      version-args: [\"--version\"]"
                  "" ]
        )

    Assert.Contains("doctor.extra-tools[0].name: \"jq\" is already a built-in Doctor tool", shadowing)

    let duplicated =
        findings (
            String.concat
                "\n"
                [ "doctor:"
                  "  extra-tools:"
                  "    - name: java"
                  "      binary: java"
                  "      version-args: [\"-version\"]"
                  "    - name: java"
                  "      binary: java"
                  "      version-args: [\"-version\"]"
                  "" ]
        )

    Assert.Contains("doctor.extra-tools[1].name: duplicate Doctor tool \"java\"", duplicated)
