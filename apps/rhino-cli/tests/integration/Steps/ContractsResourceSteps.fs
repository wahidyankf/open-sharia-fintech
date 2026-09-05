/// TickSpec step definitions binding
/// `contracts/contracts-dart-scaffold.feature`'s 3 scenarios to
/// `RhinoCli.Application.Contracts`'s `contracts dart-scaffold` port
/// [Repo-grounded — `apps/rhino-cli/src/internal/contracts/dart_scaffold.rs`].
///
/// Every scenario drives `scaffoldDart` against a throwaway temp directory,
/// the same way `dart_scaffold.rs`'s own unit tests do — no scenario shells
/// out to `dart` or `pub`.
module RhinoCli.Tests.Integration.Steps.ContractsResourceSteps

/// Explicit static-coverage ownership; the validator scopes this file's
/// TickSpec bindings to these canonical features.
let private behaviourFeatureOwnership =
    [ "specs/apps/rhino/cli/behaviours/contracts/contracts-dart-scaffold.feature" ]


open System
open System.IO
open TickSpec
open Xunit
open RhinoCli.Application.Contracts

/// Instance step-definition container — see `ConventionSteps.fs`'s module
/// doc comment for why TickSpec's one-instance-per-scenario lifecycle makes
/// instance-level mutable fields the idiomatic state-threading mechanism
/// here.
type ContractsResourceSteps() =
    let mutable dir: string option = None
    let mutable outcome: Result<DartScaffoldResult, string> option = None

    let scaffoldRoot () : string =
        match dir with
        | Some existing -> existing
        | None ->
            let created =
                Path.Combine(Path.GetTempPath(), "rhino-cli-dart-scaffold-" + Guid.NewGuid().ToString("N"))

            Directory.CreateDirectory created |> ignore
            dir <- Some created
            created

    let writeFile (rel: string) (content: string) : unit =
        let path =
            Path.Combine(scaffoldRoot (), rel.Replace('/', Path.DirectorySeparatorChar))

        Directory.CreateDirectory(Path.GetDirectoryName path) |> ignore
        File.WriteAllText(path, content)

    let readFile (rel: string) : string =
        File.ReadAllText(Path.Combine(scaffoldRoot (), rel.Replace('/', Path.DirectorySeparatorChar)))

    let result () : DartScaffoldResult =
        match outcome with
        | Some(Ok value) -> value
        | Some(Error message) -> failwith message
        | None -> failwith "contracts dart-scaffold never ran"

    // ---- Given ----

    [<Given>]
    member _.``a generated-contracts directory with model Dart files``() =
        writeFile "lib/model/user.dart" "// model\n"
        writeFile "lib/model/account.dart" "// model\n"

    [<Given>]
    member _.``a generated-contracts directory with no model files``() = scaffoldRoot () |> ignore

    [<Given>]
    member _.``an existing generated-contracts directory with old scaffold files``() =
        writeFile "pubspec.yaml" "name: stale_package\n"
        writeFile "lib/crud_contracts.dart" "// stale barrel\n"

    // ---- When ----

    [<When>]
    member _.``the developer runs specs scaffold dart on the directory``() =
        outcome <- Some(scaffoldDart { Dir = scaffoldRoot () })

    // ---- Then ----

    [<Then>]
    member _.``the command exits successfully``() =
        match outcome with
        | Some(Ok _) -> ()
        | Some(Error message) -> failwith message
        | None -> failwith "contracts dart-scaffold never ran"

    [<Then>]
    member _.``pubspec.yaml is created with correct content``() =
        Assert.True(result().PubspecCreated)
        Assert.Equal(PubspecContent, readFile "pubspec.yaml")

    [<Then>]
    member _.``pubspec.yaml is created``() =
        Assert.True(result().PubspecCreated)
        Assert.Equal(PubspecContent, readFile "pubspec.yaml")

    [<Then>]
    member _.``the barrel library is created with part directives for each model``() =
        Assert.True(result().BarrelCreated)
        Assert.Equal<string list>([ "account.dart"; "user.dart" ], result().ModelFiles)
        let barrel = readFile "lib/crud_contracts.dart"

        Assert.Equal(
            BarrelHeader
            + "part 'model/account.dart';\npart 'model/user.dart';\n"
            + BarrelUtils,
            barrel
        )

    [<Then>]
    member _.``the barrel library is created without part directives``() =
        Assert.True(result().BarrelCreated)
        Assert.Empty(result().ModelFiles)
        Assert.Equal(BarrelHeader + BarrelUtils, readFile "lib/crud_contracts.dart")

    [<Then>]
    member _.``the existing files are overwritten with fresh scaffold``() =
        Assert.Equal(PubspecContent, readFile "pubspec.yaml")
        Assert.Equal(BarrelHeader + BarrelUtils, readFile "lib/crud_contracts.dart")

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
                "contracts",
                "contracts-dart-scaffold.feature"
            )
        )

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

    /// Runs the single scenario named `scenarioTitle`, bound against
    /// `ContractsSteps`.
    let run (scenarioTitle: string) : unit =
        let allLines = File.ReadAllLines featurePath
        let snippet = extractScenario allLines scenarioTitle
        let definitions = StepDefinitions([| typeof<ContractsResourceSteps> |])
        let feature = definitions.GenerateFeature(featurePath, snippet)
        let scenario = Seq.exactlyOne feature.Scenarios
        scenario.Action.Invoke()

[<Fact>]
let ``Normal scaffold with model files`` () =
    FeatureRunner.run "Normal scaffold with model files"

[<Fact>]
let ``Scaffold with no model files`` () =
    FeatureRunner.run "Scaffold with no model files"

[<Fact>]
let ``Scaffold overwrites existing files`` () =
    FeatureRunner.run "Scaffold overwrites existing files"
