/// Contract cases for the owner RED corpus under
/// `apps/rhino-cli/tests/fixtures/test-contract/owners/`. Each owner declares
/// one fixture per check, and the corpus is only useful if every document
/// loads: an owner fixture that no longer parses silently removes the RED
/// signal its owner migration is accepted against.
///
/// This file sits inside the byte-identical Rhino parity boundary while the
/// corpus it reads does not — `ose-public` files `O-PUB-*` owners and
/// `ose-private` files `O-PRI-*` ones. So the cases enumerate whatever owners
/// the checkout actually declares and assert the invariants that must hold for
/// each, rather than a list of owner ids that could only ever be right in one
/// of the two repositories.
module RhinoCli.Tests.Unit.Steps.TestContractOwnerFixturesUnitTests

open System.IO
open Xunit
open RhinoCli.Application

let private repoRoot: string =
    match RhinoCli.Infrastructure.GitRoot.findRoot () with
    | Ok root -> root
    | Error message -> failwithf "locate repository root: %s" message

/// The four fixture file names the loader admits, each bound to its check and
/// to the diagnostic code that check emits for the mutation the file describes.
let private checks: (string * TestContract.FixtureCheck * string) list =
    [ "layout-misplaced.json", TestContract.CheckLayout, "layout-file-selected-twice"
      "coverage-98.json", TestContract.CheckCoverage, "coverage-below-floor"
      "bdd-missing-step.json", TestContract.CheckBdd, "bdd-undefined-binding"
      "manifest-proxy.json", TestContract.CheckManifest, "manifest-script-proxies-nx-target" ]

let private corpusRoot: string = Path.Combine(repoRoot, TestContract.FixtureRoot)

/// Every owner this checkout declares, read from the corpus rather than named,
/// so the same file binds in both repositories.
let private declaredOwners: string list =
    Assert.True(Directory.Exists corpusRoot, "missing owner corpus root " + corpusRoot)

    Directory.GetDirectories corpusRoot
    |> Array.map Path.GetFileName
    |> Array.sort
    |> Array.toList

let private fixturePath (owner: string) (name: string) : string =
    sprintf "%s/%s/%s" TestContract.FixtureRoot owner name

let private load (owner: string) (check: TestContract.FixtureCheck) (name: string) : TestContract.FixtureDocument =
    match TestContract.loadFixture repoRoot owner check (fixturePath owner name) with
    | Ok document -> document
    | Error(TestContract.ContractFailure message) -> failwithf "%s/%s: contract failure: %s" owner name message
    | Error(TestContract.Misuse message) -> failwithf "%s/%s: misuse: %s" owner name message

[<Fact>]
let ``the corpus declares at least one owner`` () = Assert.NotEmpty declaredOwners

[<Fact>]
let ``every declared owner id carries this repository's owner prefix`` () =
    for owner in declaredOwners do
        Assert.True(
            owner.StartsWith "O-PUB-" || owner.StartsWith "O-PRI-",
            sprintf "owner directory \"%s\" is not a stable owner id" owner
        )

[<Fact>]
let ``every declared owner declares all four check fixtures`` () =
    for owner in declaredOwners do
        for name, _, _ in checks do
            let path = Path.Combine(repoRoot, fixturePath owner name)
            Assert.True(File.Exists path, "missing owner fixture " + path)

[<Fact>]
let ``an owner directory holds nothing but the four admitted documents`` () =
    let admitted = checks |> List.map (fun (name, _, _) -> name) |> Set.ofList

    for owner in declaredOwners do
        let found =
            Directory.GetFiles(Path.Combine(corpusRoot, owner))
            |> Array.map Path.GetFileName
            |> Set.ofArray

        Assert.Equal<Set<string>>(admitted, found)

[<Fact>]
let ``every owner fixture loads under the check it is bound to`` () =
    for owner in declaredOwners do
        for name, check, _ in checks do
            let document = load owner check name
            Assert.Equal(owner, document.OwnerId)
            Assert.Equal(check, document.Check)
            Assert.Equal(TestContract.FixtureSchemaVersion, document.Schema)

[<Fact>]
let ``every owner fixture asserts its check's own diagnostic code`` () =
    for owner in declaredOwners do
        for name, check, code in checks do
            let document = load owner check name
            Assert.Equal(code, document.ExpectedDiagnostic.Code)
            Assert.NotEmpty document.ExpectedDiagnostic.Fields

[<Fact>]
let ``a fixture rejects the check it is not bound to`` () =
    let owner = List.head declaredOwners

    match
        TestContract.loadFixture repoRoot owner TestContract.CheckCoverage (fixturePath owner "layout-misplaced.json")
    with
    | Error(TestContract.Misuse message) -> Assert.Contains("disagrees with the \"layout\" check", message)
    | Error(TestContract.ContractFailure message) -> failwithf "expected misuse, found contract failure: %s" message
    | Ok _ -> failwith "expected the coverage check to reject a layout-bound fixture"

[<Fact>]
let ``a fixture below one owner is rejected for another`` () =
    match declaredOwners with
    | first :: second :: _ ->
        match
            TestContract.loadFixture repoRoot second TestContract.CheckCoverage (fixturePath first "coverage-98.json")
        with
        | Error(TestContract.Misuse message) -> Assert.Contains("must resolve below the owner directory", message)
        | Error(TestContract.ContractFailure message) -> failwithf "expected misuse, found contract failure: %s" message
        | Ok _ -> failwith "expected one owner's directory to reject another owner's fixture"
    | _ ->
        // A single-owner corpus cannot express this rejection; the loader's own
        // prefix check is covered by the wrong-check case above.
        ()
