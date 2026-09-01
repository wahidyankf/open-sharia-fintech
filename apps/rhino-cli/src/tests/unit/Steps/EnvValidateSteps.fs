/// TickSpec step definitions binding `env-validate-app-drift.feature`'s 3
/// scenarios to `RhinoCli.Application.Env`'s `validateAppSurface` port
/// [Repo-grounded —
/// `specs/apps/rhino/cli/behaviors/env/env-validate-app-drift.feature`,
/// `apps/rhino-cli/src/application/env/validate.rs`].
///
/// Follows `EnvRestoreSteps.fs`'s per-scenario slicing convention: each
/// xunit `[<Fact>]` below runs exactly one scenario, extracted from the
/// real, frozen feature file rather than a duplicated/rewritten copy of its
/// wording. There is no CLI wiring in this PR (deferred to the Wave B
/// integration PR) — "the command exits with a failure code"/"exits
/// successfully" and "the output names the key as X" are asserted directly
/// against `validateAppSurface`'s returned `Finding list`: a non-empty list
/// carrying the expected `Drift`/`Key` stands in for "failure code" plus
/// "names the key as X"; an empty list stands in for "exits successfully".
module RhinoCli.Tests.Unit.Steps.EnvValidateSteps

open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Env

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type EnvValidateSteps() =
    let mutable repoRoot: string option = None
    let mutable surface: SurfaceConfig option = None
    let mutable findingsResult: Result<Finding list, string> option = None
    let mutable ownedDirs: string list = []

    let newTempDir () : string =
        let dir =
            Path.Combine(Path.GetTempPath(), "rhino-cli-env-validate-" + Guid.NewGuid().ToString("N"))

        Directory.CreateDirectory(dir) |> ignore
        ownedDirs <- dir :: ownedDirs
        dir

    let writeFile (root: string) (relativePath: string) (content: string) =
        let full = Path.Combine(root, relativePath)
        Directory.CreateDirectory(Path.GetDirectoryName(full)) |> ignore
        File.WriteAllText(full, content)

    let ensureRoot () : string =
        match repoRoot with
        | Some dir -> dir
        | None ->
            let dir = newTempDir ()
            repoRoot <- Some dir
            dir

    let findings () : Finding list =
        match findingsResult with
        | Some(Ok findings) -> findings
        | Some(Error message) -> failwith (sprintf "expected env validate to return findings, got error: %s" message)
        | None -> failwith "no command has been run by a When step"

    // ---- Given ----

    [<Given>]
    member _.``an app surface whose .env.example declares a key the source code never reads``() =
        let root = ensureRoot ()
        writeFile root "surface/.env.example" "UNREAD_KEY=some-value\n"
        writeFile root "surface/src/main.rs" "fn main() {}\n"

        surface <-
            Some
                { Root = "surface"
                  Kind = App
                  Lang = "rust"
                  Allowlist = [] }

    [<Given>]
    member _.``an app surface whose source code reads a key absent from .env.example``() =
        let root = ensureRoot ()
        writeFile root "surface/.env.example" ""
        writeFile root "surface/src/main.rs" "let x = env::var(\"UNDECLARED_KEY\").unwrap();\n"

        surface <-
            Some
                { Root = "surface"
                  Kind = App
                  Lang = "rust"
                  Allowlist = [] }

    // TickSpec 2.0.5's line lexer treats a literal `#` anywhere in a step
    // line as a comment marker (not just at line-start, unlike the Gherkin
    // spec) — confirmed empirically: it truncates this scenario's frozen
    // `Given an F# app surface ...` line to `an F` before step resolution,
    // so no bound pattern can ever see the text after the `#` at runtime. F#
    // step names double as regexes in TickSpec (see `speccoverage`'s own
    // `add_fsharp_step_pattern`, which anchors this text as `^…$` when
    // checking spec coverage against the real, untruncated Gherkin line), so
    // `.*` here stands in for everything TickSpec itself never gets to see:
    // it satisfies TickSpec's truncated `an F` match at runtime AND the
    // coverage tool's anchored match against the full untruncated sentence.
    [<Given>]
    member _.``an F.*``() =
        let root = ensureRoot ()
        writeFile root "surface/.env.example" "WRAPPED_KEY=some-value\n"

        writeFile
            root
            "surface/src/Config.fs"
            "let wrapped = readEnvironment \"WRAPPED_KEY\"\nlet inContainer = System.Environment.GetEnvironmentVariable(\"DOTNET_RUNNING_IN_CONTAINER\")\n"

        surface <-
            Some
                { Root = "surface"
                  Kind = App
                  Lang = "fsharp"
                  Allowlist = [] }

    // ---- When ----

    [<When>]
    member _.``the developer runs env validate``() =
        let root = ensureRoot ()

        let activeSurface =
            match surface with
            | Some s -> s
            | None -> failwith "no surface has been prepared by a Given step"

        findingsResult <- Some(validateAppSurface root activeSurface)

    // ---- Then ----

    [<Then>]
    member _.``the command exits with a failure code``() = Assert.NotEmpty(findings ())

    [<Then>]
    member _.``the command exits successfully``() = Assert.Empty(findings ())

    [<Then>]
    member _.``the output names the key as declared-but-unread``() =
        Assert.Contains(findings (), fun (f: Finding) -> f.Drift = DeclaredButUnread && f.Key = "UNREAD_KEY")

    [<Then>]
    member _.``the output names the key as read-but-undeclared``() =
        Assert.Contains(findings (), fun (f: Finding) -> f.Drift = ReadButUndeclared && f.Key = "UNDECLARED_KEY")

    [<AfterScenario>]
    member _.Cleanup() =
        for dir in ownedDirs do
            if Directory.Exists dir then
                Directory.Delete(dir, true)

/// Reads one named `Scenario:` block out of the real, frozen
/// `env-validate-app-drift.feature` file (leaving the file itself untouched)
/// and runs it through TickSpec bound only against `EnvValidateSteps` — see
/// `EnvSteps.fs`'s `FeatureRunner` for why this is per-scenario rather than
/// per-file.
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
                "cli",
                "behaviors",
                "env",
                "env-validate-app-drift.feature"
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
                || trimmed.StartsWith("Scenario Outline:", StringComparison.Ordinal)
                // env-validate-app-drift.feature tags only the feature itself
                // (`@env-validate-app-drift`), with no per-scenario tags — a
                // `@`-prefixed line still ends the slice, matching
                // `EnvRestoreSteps.fs`'s tag-aware convention, even though no
                // scenario here actually carries one.
                || trimmed.StartsWith("@", StringComparison.Ordinal))
            |> Option.map (fun relativeIdx -> startIdx + 1 + relativeIdx)
            |> Option.defaultValue featureLines.Length

        Array.append [| featureLine; "" |] featureLines.[startIdx .. endIdx - 1]

    /// Runs the single scenario named `scenarioTitle` from
    /// `env-validate-app-drift.feature`, bound against `EnvValidateSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<EnvValidateSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``A key declared in .env.example but never read by the app fails validation`` () =
    FeatureRunner.run "A key declared in .env.example but never read by the app fails validation"

[<Fact>]
let ``A key read by the app but never declared in .env.example fails validation`` () =
    FeatureRunner.run "A key read by the app but never declared in .env.example fails validation"

[<Fact>]
let ``F# environment wrapper reads remain detectable after convergence`` () =
    FeatureRunner.run "F# environment wrapper reads remain detectable after convergence"
