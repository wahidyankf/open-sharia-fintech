/// The permanent regression guard for the eight finite test-contract concerns
/// closed out by Phase 20B of the adopt-beavernest-test-automation plan:
/// registry, lifecycle, corpus, and target-composition (the four sub-checks
/// inside `TestContract.validate`), plus the four self-contained document
/// validators — layout, manifest, coverage, and BDD. Each fact proves the real
/// validator still rejects one deliberately-invalid case recorded in
/// `Fixtures/TestContract/Closure/closure.json`, so a future regression in any
/// of the eight wired concerns fails here first.
module RhinoCli.Tests.Unit.Steps.TestContractClosureUnitTests

open System
open System.IO
open System.Text.Json
open Xunit
open RhinoCli.Application
open RhinoCli.Application.TestContract

// ---------------------------------------------------------------------------
// The closure fixture
// ---------------------------------------------------------------------------

let private fixturePath =
    Path.Combine(AppContext.BaseDirectory, "Fixtures", "TestContract", "Closure", "closure.json")

let private closureText: string =
    Assert.True(File.Exists fixturePath, "missing fixture " + fixturePath)
    File.ReadAllText fixturePath

/// Re-parses the closure fixture and clones the named top-level section so
/// the returned `JsonElement` outlives the disposed `JsonDocument`.
let private section (name: string) : JsonElement =
    use document = JsonDocument.Parse closureText
    (document.RootElement.GetProperty name).Clone()

let private expectedDiagnostic (name: string) : string =
    (section name).GetProperty("expected-diagnostic").GetString()

/// The embedded `document` payload for one of the four self-contained
/// concerns, rendered back to JSON text for `parseDocument`.
let private embeddedDocumentText (name: string) : string =
    (section name).GetProperty("document").GetRawText()

// ---------------------------------------------------------------------------
// Registry-family concerns — the four sub-checks inside `TestContract.validate`
// ---------------------------------------------------------------------------

let private closureProject = "closure-owner"

let private closureDriver =
    "apps/rhino-cli/tests/unit/Steps/TestContractClosureUnitTests.fs"

let private closureCorpus = [ "specs/apps/rhino/cli/behaviors/closure/**" ]

/// The one clean, minimal owner row every registry-family case starts from:
/// an active owner hosting its own required unit adapter, with no other
/// finding `TestContract.validate` could raise.
let private closureAdaptersValid: Adapters =
    { Unit =
        { Disposition = Required
          Project = Some closureProject
          Driver = Some closureDriver
          Reason = None }
      Integration =
        { Disposition = Inapplicable
          Project = None
          Driver = None
          Reason = Some "no isolated local-resource boundary" }
      E2e =
        { Disposition = Inapplicable
          Project = None
          Driver = None
          Reason = Some "no user-facing surface" } }

let private closureBehaviorValid: Behavior =
    { Id = Some(closureProject + ":default")
      LifecycleState = Some Active
      Owner = Some closureProject
      Corpus = closureCorpus
      Seed = None
      Adapters = closureAdaptersValid }

let private closureRowValid: ProjectRow =
    { Project = closureProject
      Profile = ProfileTool
      MigrationState = Expanded
      Behavior = closureBehaviorValid }

let private closureTesting (schema: string) (row: ProjectRow) : TestingRegistry =
    { Schema = schema
      Coverage = { MinimumLine = 99 }
      Mappings = []
      Projects = [ row ] }

let private closureRegistry (schema: string) (row: ProjectRow) : Registry =
    { Legacy = []
      Testing = Some(closureTesting schema row) }

let private closureNxProjects = [ closureProject ]

/// Runs `TestContract.validate` and asserts it rejected the registry with a
/// contract failure, returning the diagnostic text.
let private closureContractFailure (registry: Registry) : string =
    match validate registry closureNxProjects defaultValidateOptions with
    | Error(ContractFailure message) -> message
    | Error(Misuse message) -> failwith ("expected a contract failure but got misuse: " + message)
    | Ok report -> failwith (sprintf "expected a contract failure but validation passed: %A" report)

[<Fact>]
let ``the registry closure case rejects a canonical root declaring an unrecognized schema version`` () =
    let registry = closureRegistry "ose-test-contract/v2" closureRowValid
    let message = closureContractFailure registry
    Assert.Contains(expectedDiagnostic "registry", message)

[<Fact>]
let ``the lifecycle closure case rejects an active owner that still declares a seed target`` () =
    let behavior =
        { closureBehaviorValid with
            Seed =
                Some
                    { Target = "test:behavior:seed"
                      Driver = closureDriver } }

    let row =
        { closureRowValid with
            Behavior = behavior }

    let registry = closureRegistry "ose-test-contract/v1" row
    let message = closureContractFailure registry
    Assert.Contains(expectedDiagnostic "lifecycle", message)

[<Fact>]
let ``the corpus closure case rejects an active owner that resolves an empty corpus`` () =
    let behavior =
        { closureBehaviorValid with
            Corpus = [] }

    let row =
        { closureRowValid with
            Behavior = behavior }

    let registry = closureRegistry "ose-test-contract/v1" row
    let message = closureContractFailure registry
    Assert.Contains(expectedDiagnostic "corpus", message)

[<Fact>]
let ``the target-composition closure case rejects a required adapter hosted by another project`` () =
    let adapters =
        { closureAdaptersValid with
            Unit =
                { closureAdaptersValid.Unit with
                    Project = Some "unrelated-project" } }

    let behavior =
        { closureBehaviorValid with
            Adapters = adapters }

    let row =
        { closureRowValid with
            Behavior = behavior }

    let registry = closureRegistry "ose-test-contract/v1" row
    let message = closureContractFailure registry
    Assert.Contains(expectedDiagnostic "target-composition", message)

// ---------------------------------------------------------------------------
// Document-shaped concerns — layout, manifest, coverage, and BDD each reuse an
// existing real negative-case fixture, embedded verbatim in the closure
// fixture, parsed and validated exactly as their own sibling suites do.
// ---------------------------------------------------------------------------

[<Fact>]
let ``the layout closure case rejects an executable test left in src with no owned layer`` () =
    let outcome =
        TestContractLayout.parseDocument (embeddedDocumentText "layout")
        |> Result.bind TestContractLayout.validateDocument

    match outcome with
    | Error(ContractFailure message) -> Assert.Contains(expectedDiagnostic "layout", message)
    | Error(Misuse message) -> failwith ("expected a contract failure but got misuse: " + message)
    | Ok report -> failwith (sprintf "expected a contract failure but validation passed: %A" report)

[<Fact>]
let ``the manifest closure case rejects a retained manifest naming no direct consumer`` () =
    let outcome =
        TestContractManifest.parseDocument (embeddedDocumentText "manifest")
        |> Result.bind TestContractManifest.validateDocument

    match outcome with
    | Error(ContractFailure message) -> Assert.Contains(expectedDiagnostic "manifest", message)
    | Error(Misuse message) -> failwith ("expected a contract failure but got misuse: " + message)
    | Ok report -> failwith (sprintf "expected a contract failure but validation passed: %A" report)

[<Fact>]
let ``the coverage closure case rejects a measured slice below the repository floor`` () =
    let outcome =
        TestContractCoverage.parseDocument (embeddedDocumentText "coverage")
        |> Result.bind TestContractCoverage.validateDocument

    match outcome with
    | Error(ContractFailure message) -> Assert.Contains(expectedDiagnostic "coverage", message)
    | Error(Misuse message) -> failwith ("expected a contract failure but got misuse: " + message)
    | Ok report -> failwith (sprintf "expected a contract failure but validation passed: %A" report)

[<Fact>]
let ``the bdd closure case rejects a scenario missing its required When keyword`` () =
    let outcome =
        TestContractBdd.parseDocument (embeddedDocumentText "bdd")
        |> Result.bind TestContractBdd.validateDocument

    match outcome with
    | Error(ContractFailure message) -> Assert.Contains(expectedDiagnostic "bdd", message)
    | Error(Misuse message) -> failwith ("expected a contract failure but got misuse: " + message)
    | Ok report -> failwith (sprintf "expected a contract failure but validation passed: %A" report)
