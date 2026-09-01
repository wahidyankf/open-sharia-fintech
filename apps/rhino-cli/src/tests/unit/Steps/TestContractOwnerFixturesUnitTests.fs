/// Contract cases for the public owner RED corpus under
/// `apps/rhino-cli/tests/fixtures/test-contract/owners/`. Each owner declares
/// one fixture per check, and the corpus is only useful if every document
/// loads: an owner fixture that no longer parses silently removes the RED
/// signal its owner migration is accepted against. These cases read the
/// repository tree rather than a copied corpus, because the fixtures are the
/// checked-in artefact the migration leaves consume by path.
module RhinoCli.Tests.Unit.Steps.TestContractOwnerFixturesUnitTests

open System.IO
open Xunit
open RhinoCli.Application

let private repoRoot: string =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Ok root -> root
    | Error message -> failwithf "locate repository root: %s" message

/// The public owners the plan's owner table declares, minus `O-PUB-WAHID`,
/// whose project left the repository before this corpus was authored.
let private publicOwners: string list =
    [ "O-PUB-CRANE"
      "O-PUB-RHINO"
      "O-PUB-FS-CORE"
      "O-PUB-FS-ENV"
      "O-PUB-TS-ENV"
      "O-PUB-WEB-TOKEN"
      "O-PUB-WEB-UI"
      "O-PUB-AYO"
      "O-PUB-OL-WEB"
      "O-PUB-OL-BE"
      "O-PUB-OL-WWW"
      "O-PUB-OSE-WEB"
      "O-PUB-OSE-BE"
      "O-PUB-OSE-WWW" ]

/// The four fixture file names the loader admits, each bound to its check and
/// to the diagnostic code that check emits for the mutation the file describes.
let private checks: (string * TestContract.FixtureCheck * string) list =
    [ "layout-misplaced.json", TestContract.CheckLayout, "layout-file-selected-twice"
      "coverage-98.json", TestContract.CheckCoverage, "coverage-below-floor"
      "bdd-missing-step.json", TestContract.CheckBdd, "bdd-undefined-binding"
      "manifest-proxy.json", TestContract.CheckManifest, "manifest-script-proxies-nx-target" ]

let private fixturePath (owner: string) (name: string) : string =
    sprintf "%s/%s/%s" TestContract.FixtureRoot owner name

let private load (owner: string) (check: TestContract.FixtureCheck) (name: string) : TestContract.FixtureDocument =
    match TestContract.loadFixture repoRoot owner check (fixturePath owner name) with
    | Ok document -> document
    | Error(TestContract.ContractFailure message) -> failwithf "%s/%s: contract failure: %s" owner name message
    | Error(TestContract.Misuse message) -> failwithf "%s/%s: misuse: %s" owner name message

[<Fact>]
let ``every public owner declares all four check fixtures`` () =
    for owner in publicOwners do
        for name, _, _ in checks do
            let path = Path.Combine(repoRoot, fixturePath owner name)
            Assert.True(File.Exists path, "missing owner fixture " + path)

[<Fact>]
let ``every public owner fixture loads under the check it is bound to`` () =
    for owner in publicOwners do
        for name, check, _ in checks do
            let document = load owner check name
            Assert.Equal(owner, document.OwnerId)
            Assert.Equal(check, document.Check)
            Assert.Equal(TestContract.FixtureSchemaVersion, document.Schema)

[<Fact>]
let ``every public owner fixture asserts its check's own diagnostic code`` () =
    for owner in publicOwners do
        for name, check, code in checks do
            let document = load owner check name
            Assert.Equal(code, document.ExpectedDiagnostic.Code)
            Assert.NotEmpty document.ExpectedDiagnostic.Fields

[<Fact>]
let ``a fixture rejects the check it is not bound to`` () =
    match
        TestContract.loadFixture
            repoRoot
            "O-PUB-RHINO"
            TestContract.CheckCoverage
            (fixturePath "O-PUB-RHINO" "layout-misplaced.json")
    with
    | Error(TestContract.Misuse message) -> Assert.Contains("disagrees with the \"layout\" check", message)
    | Error(TestContract.ContractFailure message) -> failwithf "expected misuse, found contract failure: %s" message
    | Ok _ -> failwith "expected the coverage check to reject a layout-bound fixture"

[<Fact>]
let ``a fixture below one owner is rejected for another`` () =
    match
        TestContract.loadFixture
            repoRoot
            "O-PUB-AYO"
            TestContract.CheckCoverage
            (fixturePath "O-PUB-RHINO" "coverage-98.json")
    with
    | Error(TestContract.Misuse message) -> Assert.Contains("must resolve below the owner directory", message)
    | Error(TestContract.ContractFailure message) -> failwithf "expected misuse, found contract failure: %s" message
    | Ok _ -> failwith "expected one owner's directory to reject another owner's fixture"

[<Fact>]
let ``the corpus holds no owner directory outside the declared set`` () =
    let root = Path.Combine(repoRoot, TestContract.FixtureRoot)
    Assert.True(Directory.Exists root, "missing owner corpus root " + root)

    let found =
        Directory.GetDirectories root
        |> Array.map Path.GetFileName
        |> Array.filter (fun name -> name.StartsWith "O-PUB-")
        |> Array.sort

    Assert.Equal<string array>(publicOwners |> List.sort |> List.toArray, found)
