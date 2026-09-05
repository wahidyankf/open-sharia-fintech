/// TickSpec step definitions binding `gate-enumeration.feature`'s eight
/// scenarios to `RhinoCli.Cli.Gate`'s per-surface projection
/// [Repo-grounded —
/// `specs/apps/rhino/cli/behaviours/gate/gate-enumeration.feature`,
/// `apps/rhino-cli/tests/gate_specs.rs`].
module RhinoCli.Tests.Integration.Steps.GateEnumerationResourceSteps

let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/gate/gate-enumeration.feature" ]

open System
open System.IO
open System.Text.Json
open TickSpec
open Xunit
open RhinoCli.Domain.Types

let private repoRoot: string =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Ok root -> root
    | Error message -> failwithf "locate repository root: %s" message

/// Mirrors `gate_specs.rs::config`.
let private config (gates: string) : string = "gates:\n" + gates

/// Instance step-definition container — see `ConventionSteps.fs`'s module doc
/// comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism.
type GateEnumerationSteps() =
    let root =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-gate-enumeration-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory dir |> ignore
        dir

    let mutable succeeded: bool option = None
    let mutable output: string = ""
    let mutable jsonOutput: JsonDocument option = None

    let write (relative: string) (contents: string) =
        File.WriteAllText(Path.Combine(root, relative), contents)

    let list (surface: string) (format: OutputFormat) (byGroup: bool) =
        match RhinoCli.Cli.Gate.listAtRoot root surface format byGroup with
        | Ok rendered ->
            succeeded <- Some true
            output <- rendered

            jsonOutput <-
                if format = Json then
                    Some(JsonDocument.Parse rendered)
                else
                    None
        | Error message ->
            succeeded <- Some false
            output <- message
            jsonOutput <- None

    let entries () =
        jsonOutput.Value.RootElement.EnumerateArray() |> List.ofSeq

    let stringsOf (element: JsonElement) (key: string) =
        element.GetProperty(key).EnumerateArray()
        |> Seq.map (fun value -> value.GetString())
        |> List.ofSeq

    let entryWith (key: string) (value: string) =
        entries ()
        |> List.find (fun entry -> entry.GetProperty(key).GetString() = value)

    let isSuccess () =
        match succeeded with
        | Some value -> value
        | None -> failwith "scenario command ran"

    [<Given>]
    member _.``the registry declares gates on surface "ci"``() =
        write
            "repo-config.yml"
            (config (
                "  - id: ci-one\n    type: check\n    command: one\n    kind: external\n    doctor-tools: [git, node]\n    surfaces:\n      ci: { scope: affected-projects }\n"
                + "  - id: ci-two\n    type: check\n    command: two\n    kind: external\n    surfaces:\n      ci: { scope: all-file-type }\n"
                + "  - id: local-only\n    type: check\n    command: local\n    kind: external\n    surfaces:\n      pre-commit: { scope: other }\n"
            ))

    [<Given>]
    member _.``no gate declares surface "commit-msg"``() = write "repo-config.yml" "gates: []\n"

    [<Given>]
    member _.``"cron" is not a valid surface name``() = write "repo-config.yml" "gates: []\n"

    [<Given>]
    member _.``gate "test-quick" declares wiring "hand-wired" on surface "ci"``() =
        write
            "repo-config.yml"
            (config
                "  - id: test-quick\n    type: check\n    command: test:quick\n    kind: nx\n    wiring: hand-wired\n    surfaces:\n      ci: { scope: affected-projects }\n")

    [<Given>]
    member _.``the surfaces as shipped by this plan``() =
        write
            "repo-config.yml"
            (config (
                "  - id: env-staged-guard\n    type: check\n    command: env staged-guard validate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n"
                + "  - id: commitlint\n    type: check\n    command: commitlint\n    kind: external\n    surfaces:\n      commit-msg: { scope: other }\n"
                + "  - id: format-prettier\n    type: mutation\n    command: prettier --write\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n"
                + "  - id: format-rustfmt\n    type: mutation\n    command: rustfmt\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.rs' }\n"
                + "  - id: format-verify-prettier\n    type: check\n    command: prettier --check\n    kind: external\n    surfaces:\n      ci: { scope: all-file-type, glob: '*.md' }\n"
                + "  - id: format-verify-rustfmt\n    type: check\n    command: rustfmt --check\n    kind: external\n    surfaces:\n      ci: { scope: all-file-type, glob: '*.rs' }\n"
                + "  - id: harness-bindings-generate\n    type: mutation\n    command: harness bindings generate\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n"
                + "  - id: lockfile-sync\n    type: mutation\n    command: git lockfile sync\n    kind: rhino-cli\n    surfaces:\n      pre-commit: { scope: other }\n"
                + "  - id: test-quick\n    type: check\n    command: test:quick\n    kind: nx\n    surfaces:\n      ci: { scope: affected-projects }\n"
            ))

    [<Given>]
    member _.``every ci-surface gate in the registry declares a ci_group``() =
        write
            "repo-config.yml"
            (config (
                "  - id: markdown-links\n    type: check\n    command: md links validate\n    kind: rhino-cli\n    ci-group: markdown\n    surfaces:\n      ci: { scope: all-file-type }\n"
                + "  - id: markdown-mermaid\n    type: check\n    command: md mermaid validate\n    kind: rhino-cli\n    ci-group: markdown\n    surfaces:\n      ci: { scope: all-file-type }\n"
                + "  - id: shell-lint\n    type: check\n    command: shell lint\n    kind: external\n    ci-group: shell\n    surfaces:\n      ci: { scope: all-file-type }\n"
            ))

    [<Given>]
    member _.``a ci_group's member gates declare overlapping and non-overlapping doctor_tools``() =
        write
            "repo-config.yml"
            (config (
                "  - id: shell-lint\n    type: check\n    command: shell lint\n    kind: external\n    ci-group: shell\n    doctor-tools: [shellcheck, jq]\n    surfaces:\n      ci: { scope: all-file-type }\n"
                + "  - id: shell-format-check\n    type: check\n    command: shfmt --diff\n    kind: external\n    ci-group: shell\n    doctor-tools: [jq, shfmt]\n    surfaces:\n      ci: { scope: all-file-type }\n"
                + "  - id: markdown-links\n    type: check\n    command: md links validate\n    kind: rhino-cli\n    ci-group: markdown\n    surfaces:\n      ci: { scope: all-file-type }\n"
            ))

    [<When>]
    member _.``"rhino-cli gate list --surface=ci --format=json" runs``() = list "ci" Json false

    [<When>]
    member _.``"rhino-cli gate list --surface=ci --format=text" runs``() = list "ci" Text false

    [<When>]
    member _.``"rhino-cli gate list --surface=commit-msg --format=json" runs``() = list "commit-msg" Json false

    [<When>]
    member _.``"rhino-cli gate list --surface=cron --format=json" runs``() = list "cron" Json false

    [<When>]
    member _.``"rhino-cli gate list --surface=ci --format=json --by-group" runs``() = list "ci" Json true

    [<Then>]
    member _.``the output is a JSON array``() =
        Assert.True(isSuccess (), sprintf "gate list failed: %s" output)
        Assert.Equal(JsonValueKind.Array, jsonOutput.Value.RootElement.ValueKind)

    [<Then>]
    member _.``every element carries "id", "command", "scope", and "doctor_tools" keys``() =
        for entry in entries () do
            for key in [ "id"; "command"; "scope"; "doctor_tools" ] do
                Assert.True(fst (entry.TryGetProperty key), sprintf "missing %s in %s" key (entry.GetRawText()))

            Assert.Equal(JsonValueKind.Array, entry.GetProperty("doctor_tools").ValueKind)

    [<Then>]
    member _.``entry "([^"]+)" reports doctor_tools "([^"]+)" and "([^"]+)"``
        (id: string, firstTool: string, secondTool: string)
        =
        Assert.Equal<string list>([ firstTool; secondTool ], stringsOf (entryWith "id" id) "doctor_tools")

    [<Then>]
    member _.``the array contains exactly the matrix-wired gates declaring surface "ci"``() =
        let ids = entries () |> List.map (fun entry -> entry.GetProperty("id").GetString())

        Assert.Equal<string list>([ "ci-one"; "ci-two" ], ids)

    [<Then>]
    member _.``it exits zero``() =
        Assert.True(isSuccess (), sprintf "command failed: %s" output)

    [<Then>]
    member _.``the output is an empty JSON array``() = Assert.Empty(entries ())

    [<Then>]
    member _.``it exits non-zero``() =
        Assert.True(not (isSuccess ()), sprintf "command unexpectedly succeeded: %s" output)

    [<Then>]
    member _.``the message names the four valid surfaces``() =
        for surface in [ "commit-msg"; "pre-commit"; "pre-push"; "ci" ] do
            Assert.True(output.Contains(surface, StringComparison.Ordinal), sprintf "missing %s in %s" surface output)

    [<Then>]
    member _.``the output contains no entry with id "test-quick"``() =
        Assert.DoesNotContain("test-quick", entries () |> List.map (fun e -> e.GetProperty("id").GetString()))

    [<Then>]
    member _.``the output contains an entry with id "([^"]+)"``(id: string) =
        if jsonOutput.IsSome then
            Assert.Contains(id, entries () |> List.map (fun e -> e.GetProperty("id").GetString()))
        else
            Assert.True(
                output.Contains(id, StringComparison.Ordinal),
                sprintf "gate list output lacks %s: %s" id output
            )

    [<Then>]
    member _.``that entry is marked as hand-wired``() =
        Assert.True(output.Contains("hand-wired", StringComparison.Ordinal))

    [<Then>]
    member _.``that entry reports type "([^"]+)"``(gateType: string) =
        Assert.Contains(gateType, entries () |> List.map (fun e -> e.GetProperty("type").GetString()))

    [<Then>]
    member _.``it emits one entry per distinct ci_group value``() =
        Assert.True(isSuccess (), sprintf "gate list --by-group failed: %s" output)
        Assert.Equal(2, List.length (entries ()))

    [<Then>]
    member _.``each entry lists its member gate ids in registry declaration order``() =
        Assert.Equal<string list>(
            [ "markdown-links"; "markdown-mermaid" ],
            stringsOf (entryWith "group" "markdown") "gates"
        )

        Assert.Equal<string list>([ "shell-lint" ], stringsOf (entryWith "group" "shell") "gates")

    [<Then>]
    member _.``each group entry's doctor_tools is the deduped, sorted union of its members' doctor_tools``() =
        Assert.Equal<string list>([ "jq"; "shellcheck"; "shfmt" ], stringsOf (entryWith "group" "shell") "doctor_tools")

    [<Then>]
    member _.``a group whose members declare no doctor_tools reports an empty array``() =
        Assert.Empty(stringsOf (entryWith "group" "markdown") "doctor_tools")

module private FeatureRunner =

    let private featurePath: string =
        Path.Combine(repoRoot, "specs", "apps", "rhino", "cli", "behaviours", "gate", "gate-enumeration.feature")

    let private extractScenario (featureLines: string[]) (scenarioTitle: string) : string[] =
        let featureLine =
            featureLines
            |> Array.find (fun l -> l.TrimStart().StartsWith("Feature:", StringComparison.Ordinal))

        let startIdx =
            featureLines
            |> Array.findIndex (fun l -> l.Trim() = sprintf "Scenario: %s" scenarioTitle)

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

    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<GateEnumerationSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``JSON output drives a GitHub Actions matrix`` () =
    FeatureRunner.run "JSON output drives a GitHub Actions matrix"

[<Fact>]
let ``A surface with no declared gates yields an empty array, not an error`` () =
    FeatureRunner.run "A surface with no declared gates yields an empty array, not an error"

[<Fact>]
let ``An unknown surface name is rejected rather than returning empty`` () =
    FeatureRunner.run "An unknown surface name is rejected rather than returning empty"

[<Fact>]
let ``A hand-wired gate produces no matrix row`` () =
    FeatureRunner.run "A hand-wired gate produces no matrix row"

[<Fact>]
let ``A hand-wired gate is still listed in text output`` () =
    FeatureRunner.run "A hand-wired gate is still listed in text output"

[<Fact>]
let ``Shipped CI surface entries retain their declared type`` () =
    FeatureRunner.run "Shipped CI surface entries retain their declared type"

[<Fact>]
let ``Enumeration can group CI gates by declared group`` () =
    FeatureRunner.run "Enumeration can group CI gates by declared group"

[<Fact>]
let ``Grouped enumeration reports the union of each group's Doctor tools`` () =
    FeatureRunner.run "Grouped enumeration reports the union of each group's Doctor tools"
