/// TickSpec step definitions binding `gate-emission.feature`'s five scenarios
/// to `RhinoCli.Cli.Gate`'s `lint-staged` emitter
/// [Repo-grounded —
/// `specs/apps/rhino/cli/behaviors/gate/gate-emission.feature`,
/// `apps/rhino-cli/tests/gate_specs.rs`].
///
/// Each scenario writes a self-contained `repo-config.yml` and `package.json`
/// into a throwaway temp directory and calls `Gate.emitAtRoot` in-process,
/// following `GateDeclarationSteps.fs`'s convention.
module RhinoCli.Tests.Unit.Steps.GateEmissionSteps

open System
open System.IO
open System.Text.Json
open TickSpec
open Xunit

let private repoRoot: string =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Ok root -> root
    | Error message -> failwithf "locate repository root: %s" message

/// Mirrors `gate_specs.rs::config`.
let private config (gates: string) : string = "gates:\n" + gates

/// Mirrors `gate_specs.rs::gate`.
let private gate (id: string) (gateType: string) (command: string) (kind: string) (surfaces: string) : string =
    sprintf
        "  - id: %s\n    type: %s\n    command: %s\n    kind: %s\n    surfaces:\n%s"
        id
        gateType
        command
        kind
        surfaces

let private emptyLintStagedPackage = "{\"name\":\"fixture\",\"lint-staged\":{}}\n"

/// Instance step-definition container — see `ConventionSteps.fs`'s module doc
/// comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism.
type GateEmissionSteps() =
    let root =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-gate-emission-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory dir |> ignore
        dir

    let mutable succeeded: bool option = None
    let mutable output: string = ""
    let mutable firstEmittedPackage: string option = None

    let write (relative: string) (contents: string) =
        File.WriteAllText(Path.Combine(root, relative), contents)

    let packageText () =
        File.ReadAllText(Path.Combine(root, "package.json"))

    let lintStaged () =
        JsonDocument.Parse(packageText ()).RootElement.GetProperty "lint-staged"

    let commandsFor (glob: string) =
        lintStaged().GetProperty(glob).EnumerateArray()
        |> Seq.map (fun element -> element.GetString())
        |> List.ofSeq

    let emit () =
        match RhinoCli.Cli.Gate.emitAtRoot root "pre-commit" with
        | Ok text ->
            succeeded <- Some true
            output <- text
        | Error message ->
            succeeded <- Some false
            output <- message

    let assertEmitted () =
        Assert.True((succeeded = Some true), sprintf "gate emit failed: %s" output)

    let writePerFileRegistry () =
        write
            "repo-config.yml"
            (config (
                "  - id: format-markdown\n    type: mutation\n    command: prettier --write\n    kind: external\n    category: formatter\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n"
                + "  - id: lint-markdown\n    type: check\n    command: markdownlint-cli2\n    kind: external\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.md' }\n"
                + "  - id: format-rust\n    type: mutation\n    command: rustfmt\n    kind: external\n    category: formatter\n    surfaces:\n      pre-commit: { scope: affected-file-type, glob: '*.rs' }\n"
            ))

        write "package.json" emptyLintStagedPackage

    [<Given>]
    member _.``the registry declares per-file gates on surface "pre-commit"``() = writePerFileRegistry ()

    [<Given>]
    member _.``a pre-commit gate declares an affected-file-type glob and a lint-staged shell template``() =
        write
            "repo-config.yml"
            (config (
                "  - id: repo-config-schema\n    type: check\n    command: repo-config validate\n    kind: rhino-cli\n    surfaces:\n      pre-commit:\n        scope: affected-file-type\n        glob: repo-config.yml\n        lint-staged-shell: '{{command}}'\n"
                + "  - id: docker-compose-config\n    type: check\n    command: docker compose config\n    kind: external\n    surfaces:\n      pre-commit:\n        scope: affected-file-type\n        glob: 'docker-compose*.{yml,yaml}'\n        lint-staged-shell: 'for f; do docker compose -f \"$f\" config > /dev/null; done'\n"
            ))

        write "package.json" emptyLintStagedPackage

    [<Given>]
    member _.``the registry declares a gate of kind "rhino-cli" on surface "pre-commit"``() =
        write
            "repo-config.yml"
            (config (
                gate
                    "md-mermaid"
                    "check"
                    "md mermaid validate"
                    "rhino-cli"
                    "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n"
            ))

        write "package.json" emptyLintStagedPackage

    [<Given>]
    member _.``the registry declares an external gate whose tool resolves from node_modules``() =
        let declaration =
            gate
                "markdownlint"
                "check"
                "markdownlint-cli2"
                "external"
                "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n"

        write
            "repo-config.yml"
            (config (declaration.Replace("kind: external\n", "kind: external\n    doctor-tools: [npm]\n")))

        write "package.json" emptyLintStagedPackage

    [<Given>]
    member _.``"rhino-cli gate emit --surface=pre-commit" has already run``() =
        writePerFileRegistry ()
        emit ()
        Assert.True((succeeded = Some true), sprintf "first emit failed: %s" output)
        firstEmittedPackage <- Some(packageText ())

    [<When>]
    member _.``"rhino-cli gate emit --surface=pre-commit" runs``() = emit ()

    [<When>]
    member _.``it runs a second time``() = emit ()

    [<Then>]
    member _.``the "lint-staged" block in package.json contains one glob key per declared glob in registry declaration order``
        ()
        =
        assertEmitted ()
        Assert.Equal(2, lintStaged().EnumerateObject() |> Seq.length)

    [<Then>]
    member _.``each key lists that glob's commands in declaration order``() =
        Assert.Equal<string list>([ "prettier --write"; "markdownlint-cli2" ], commandsFor "*.md")
        Assert.Equal<string list>([ "rustfmt" ], commandsFor "*.rs")

    [<Then>]
    member _.``package.json is byte-identical to the first result``() =
        assertEmitted ()
        Assert.Equal(firstEmittedPackage.Value, packageText ())

    [<Then>]
    member _.``the block appears exactly once``() =
        let text = packageText ()

        let rec count (from: int) (total: int) : int =
            match text.IndexOf("\"lint-staged\"", from, StringComparison.Ordinal) with
            | -1 -> total
            | at -> count (at + 1) (total + 1)

        Assert.Equal(1, count 0 0)

    [<Then>]
    member _.``the generated lint-staged command uses the declared wrapper``() =
        assertEmitted ()

        Assert.Equal<string list>(
            [ "bash -c 'for f; do docker compose -f \"$f\" config > /dev/null; done' --" ],
            commandsFor "docker-compose*.{yml,yaml}"
        )

    [<Then>]
    member _.``a {{command}} placeholder expands to the gate's kind-derived command exactly once``() =
        Assert.Equal<string list>(
            [ "bash -c 'apps/rhino-cli/scripts/rhino-bin.sh repo-config validate' --" ],
            commandsFor "repo-config.yml"
        )

    [<Then>]
    member _.``the generated command invokes the resolver shim at "apps/rhino-cli/scripts/rhino-bin.sh"``() =
        assertEmitted ()
        let command = commandsFor "*.md" |> List.head

        Assert.True(
            command.Contains("apps/rhino-cli/scripts/rhino-bin.sh", StringComparison.Ordinal),
            sprintf "expected the generated command to invoke the resolver shim: %s" command
        )

    [<Then>]
    member _.``the generated command contains no "cargo run" substring``() =
        let command = commandsFor "*.md" |> List.head

        Assert.False(
            command.Contains("cargo run", StringComparison.Ordinal),
            sprintf "expected the generated command to contain no cargo run substring: %s" command
        )

    [<Then>]
    member _.``the generated command invokes that tool through "node_modules/.bin"``() =
        assertEmitted ()
        let command = commandsFor "*.md" |> List.head

        Assert.True(
            command.Contains("node_modules/.bin/", StringComparison.Ordinal),
            sprintf "expected the generated command to invoke node_modules/.bin: %s" command
        )

    [<Then>]
    member _.``the generated command contains no "npx" substring``() =
        let command = commandsFor "*.md" |> List.head

        Assert.False(
            command.Contains("npx", StringComparison.Ordinal),
            sprintf "expected the generated command to contain no npx substring: %s" command
        )

module private FeatureRunner =

    let private featurePath: string =
        Path.Combine(repoRoot, "specs", "apps", "rhino", "cli", "behaviors", "gate", "gate-emission.feature")

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
        let definitions = StepDefinitions([| typeof<GateEmissionSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``The emitter reproduces the registry's per-file entries`` () =
    FeatureRunner.run "The emitter reproduces the registry's per-file entries"

[<Fact>]
let ``Re-running the emitter is idempotent`` () =
    FeatureRunner.run "Re-running the emitter is idempotent"

[<Fact>]
let ``Generated lint-staged commands may use a declared shell wrapper`` () =
    FeatureRunner.run "Generated lint-staged commands may use a declared shell wrapper"

[<Fact>]
let ``Rhino CLI kind renders a resolver shim invocation`` () =
    FeatureRunner.run "Rhino CLI kind renders a resolver shim invocation"

[<Fact>]
let ``Node-resolved external tools render a repository-local bin path`` () =
    FeatureRunner.run "Node-resolved external tools render a repository-local bin path"
