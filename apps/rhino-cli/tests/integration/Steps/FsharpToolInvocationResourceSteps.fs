/// TickSpec step definitions binding `fsharp-tool-invocation.feature`'s 1
/// scenario to `RhinoCli.Application.Doctor`'s F# lint-target Fantomas
/// tool-invocation check [Repo-grounded —
/// `specs/apps/rhino/cli/behaviours/system/fsharp-tool-invocation.feature`].
/// No Rust source underlies this feature — `apps/rhino-cli/src` never
/// invoked Fantomas — so unlike every other `Steps.fs` file in this
/// directory there is no legacy Rust BDD counterpart to mirror.
///
/// Named `FsharpToolInvocationSteps` rather than reusing `DoctorSteps`
/// (already bound to `cargo-target-share.feature`) or `DoctorToolCheckSteps`
/// (already bound to `doctor.feature`) — follows `DoctorToolCheckSteps.fs`'s
/// own documented precedent of one Steps file per feature file sharing an
/// application module.
///
/// Unlike the synthetic-fixture repos every other Doctor Steps file builds,
/// this scenario is a genuine self-check of the real, live repository
/// checkout: `repoRoot` is resolved from this source file's own on-disk
/// location (the same fixed-offset convention `DoctorSteps.fs`'s
/// `fsharpProjectJsonPath` already uses to read the real
/// `src-fsharp/project.json`), so the scenario asserts every F# lint target
/// actually checked into this repo today is compliant.
module RhinoCli.Tests.Integration.Steps.FsharpToolInvocationResourceSteps

/// Explicit static-coverage ownership; the validator scopes this file's
/// TickSpec bindings to these canonical features.
let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/system/fsharp-tool-invocation.feature" ]


open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Doctor
open RhinoCli.Domain.Types

type FsharpToolInvocationSteps() =
    let mutable targets: FsharpLintTarget list = []
    let mutable checks: FsharpToolInvocationCheck list = []

    /// `tests/unit/Steps` → `tests/unit` → `tests` → `src-fsharp` →
    /// `rhino-cli` → `apps` → repo root — the same six-level offset
    /// `FeatureRunner.featurePath` below uses to reach `specs/`.
    let repoRoot: string =
        Path.GetFullPath(Path.Combine(__SOURCE_DIRECTORY__, "..", "..", "..", "..", ".."))

    // TickSpec 2.0.5's line lexer treats a literal `#` anywhere in a step
    // line as a comment marker (not just at line-start, unlike the Gherkin
    // spec) — the same behaviour `EnvValidateSteps.fs`'s `` ``an F.*`` `` step
    // documents and works around. It truncates this scenario's frozen
    // `Given the local F# lint targets are discovered` line to
    // `the local F` before step resolution, so no bound pattern can ever see
    // the text after the `#` at runtime. Step names double as regexes in
    // TickSpec, so `.*` stands in for everything TickSpec itself never gets
    // to see: it satisfies TickSpec's truncated match at runtime AND
    // `speccoverage`'s anchored match against the full, untruncated Gherkin
    // line.
    [<Given>]
    member _.``the local F.*``() =
        targets <- discoverFsharpLintTargets repoRoot

    [<When>]
    member _.``every locally discovered F.*``() =
        checks <- evaluateFsharpToolInvocation targets

    [<Then>]
    member _.``every discovered F.*``() =
        Assert.Equal(targets.Length, checks.Length)
        // Sanity check that discovery genuinely found something in this
        // real repo checkout, rather than the assertion above passing
        // vacuously on two empty lists.
        Assert.NotEmpty(targets)

    [<Then>]
    member _.``each target restores its local .NET tool manifest before running Fantomas``() =
        for c in checks do
            Assert.DoesNotContain(
                c.Findings,
                fun (f: Finding) -> f.Message.Contains("does not restore the local .NET tool manifest")
            )

    [<Then>]
    member _.``no target invokes the global Fantomas app host directly``() =
        for c in checks do
            Assert.DoesNotContain(
                c.Findings,
                fun (f: Finding) -> f.Message.Contains("invokes the global Fantomas app host directly")
            )

    [<Then>]
    member _.``an unformatted source file is checked only when F.*``() =
        let mutable probeCalls = 0

        let probe: UnformattedSampleProbe =
            fun _ ->
                probeCalls <- probeCalls + 1
                Ok true

        let result = checkUnformattedSample targets "sample.fs" probe

        if List.isEmpty targets then
            Assert.Equal(0, probeCalls)
            Assert.True(Option.isNone result)
        else
            Assert.Equal(1, probeCalls)
            Assert.True(Option.isSome result)

// ---------------------------------------------------------------------------
// FeatureRunner
// ---------------------------------------------------------------------------

/// Reads the single `Scenario:` block out of the real, frozen
/// `fsharp-tool-invocation.feature` file (leaving the file itself untouched)
/// and runs it through TickSpec bound only against
/// `FsharpToolInvocationSteps` — see `DoctorToolCheckSteps.fs`'s
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
                "specs",
                "apps",
                "rhino",
                "cli",
                "behaviours",
                "system",
                "fsharp-tool-invocation.feature"
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

    /// Runs the single scenario named `scenarioTitle` from
    /// `fsharp-tool-invocation.feature`, bound against
    /// `FsharpToolInvocationSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<FsharpToolInvocationSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Every locally discovered F# lint target uses the pinned local Fantomas tool`` () =
    FeatureRunner.run "Every locally discovered F# lint target uses the pinned local Fantomas tool"
