/// Contract cases for materializing a layout document from the real
/// repository. The fixture corpus pins what each rule rejects; these cases pin
/// what the repository reader reports, so `--project` measures the project
/// rather than a document somebody typed.
module RhinoCli.Tests.Unit.Steps.TestContractProjectUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Application

// ---------------------------------------------------------------------------
// Throwaway repository builder
// ---------------------------------------------------------------------------

let private newTempRepo () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-test-contract-project-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

let private write (root: string) (relative: string) (body: string) : unit =
    let absolute =
        Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar))

    Directory.CreateDirectory(Path.GetDirectoryName(absolute: string)) |> ignore
    File.WriteAllText(absolute, body)

let private materialized
    (root: string)
    (project: string)
    (layers: TestContractLayout.Layer list)
    : TestContractLayout.LayoutDocument =
    match TestContractProject.materialize root project layers with
    | Ok document -> document
    | Error(TestContract.Misuse message) -> failwith ("materialize rejected as misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("materialize rejected: " + message)

let private rejection (document: TestContractLayout.LayoutDocument) : string =
    match TestContractLayout.validateDocument document with
    | Error(TestContract.ContractFailure message) -> message
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok _ -> failwith "the document passed; it must fail"

let private selectorsFor (document: TestContractLayout.LayoutDocument) (path: string) : string list =
    match document.Files |> List.tryFind (fun file -> file.Path = path) with
    | Some file -> file.SelectedBy
    | None -> failwith ("the document does not carry " + path)

let private fileFor (document: TestContractLayout.LayoutDocument) (path: string) : TestContractLayout.LayoutFile =
    match document.Files |> List.tryFind (fun file -> file.Path = path) with
    | Some file -> file
    | None -> failwith ("the document does not carry " + path)

// ---------------------------------------------------------------------------
// Owned layers come from the registry, never from the directory listing
// ---------------------------------------------------------------------------

let private adapter (disposition: TestContract.Disposition) (project: string option) : TestContract.AdapterEntry =
    { Disposition = disposition
      Project = project
      Driver =
        project
        |> Option.map (fun name -> "libs/" + name + "/tests/unit/bdd/unit-driver.ts")
      Reason =
        match disposition with
        | TestContract.Inapplicable -> Some "no isolated local-resource boundary"
        | _ -> None }

let private row (name: string) (adapters: TestContract.Adapters) : TestContract.ProjectRow =
    { Project = name
      Profile = TestContract.ProfileLibrary
      MigrationState = TestContract.Verified
      Behavior =
        { Id = Some(name + ":default")
          LifecycleState = Some TestContract.Active
          Owner = Some name
          Corpus = []
          Seed = None
          Adapters = adapters } }

[<Fact>]
let ``a project owns only the layers its own required adapters name`` () =
    let adapters: TestContract.Adapters =
        { Unit = adapter TestContract.Required (Some "widget")
          Integration = adapter TestContract.Delegated (Some "widget-e2e")
          E2e = adapter TestContract.Inapplicable None }

    Assert.Equal<TestContractLayout.Layer list>(
        [ TestContractLayout.LayerUnit ],
        TestContractProject.ownedLayers (row "widget" adapters)
    )

[<Fact>]
let ``a dedicated runtime project owns the layer whose required adapter names it`` () =
    let adapters: TestContract.Adapters =
        { Unit = adapter TestContract.Inapplicable None
          Integration = adapter TestContract.Required (Some "widget-e2e")
          E2e = adapter TestContract.Inapplicable None }

    Assert.Equal<TestContractLayout.Layer list>(
        [ TestContractLayout.LayerIntegration ],
        TestContractProject.ownedLayers (row "widget-e2e" adapters)
    )

[<Fact>]
let ``a required adapter hosted by another project does not make this project own the layer`` () =
    let adapters: TestContract.Adapters =
        { Unit = adapter TestContract.Required (Some "other")
          Integration = adapter TestContract.Inapplicable None
          E2e = adapter TestContract.Inapplicable None }

    Assert.Empty(TestContractProject.ownedLayers (row "widget" adapters))

// ---------------------------------------------------------------------------
// Runner discovery: .NET
// ---------------------------------------------------------------------------

let private dotnetProjectJson =
    """{
  "name": "widget",
  "targets": {
    "test:unit": {
      "executor": "nx:run-commands",
      "options": { "command": "dotnet test libs/widget/tests/unit/widget-unit-tests.fsproj" }
    }
  }
}
"""

let private dotnetFsproj =
    """<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <Compile Include="Tests/CoreTests.fs" />
  </ItemGroup>
</Project>
"""

let private seedDotnetProject (root: string) : unit =
    write root "libs/widget/project.json" dotnetProjectJson
    write root "libs/widget/tests/unit/widget-unit-tests.fsproj" dotnetFsproj
    write root "libs/widget/tests/unit/Tests/CoreTests.fs" "module CoreTests\n"
    write root "libs/widget/src/Core.fs" "module Core\n"

[<Fact>]
let ``a dotnet test project selects exactly the files its compile list names`` () =
    let root = newTempRepo ()
    seedDotnetProject root
    let document = materialized root "widget" [ TestContractLayout.LayerUnit ]

    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/widget/tests/unit/Tests/CoreTests.fs")

[<Fact>]
let ``the dotnet-shaped project satisfies the layout rule`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    match TestContractLayout.validateDocument (materialized root "widget" [ TestContractLayout.LayerUnit ]) with
    | Ok report -> Assert.Equal(1, report.ExecutableFiles)
    | Error(TestContract.ContractFailure message) -> failwith ("the shape must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("the shape must pass, found misuse: " + message)

// ---------------------------------------------------------------------------
// Runner discovery: vitest
// ---------------------------------------------------------------------------

let private vitestProjectJson =
    """{
  "name": "gadget",
  "targets": {
    "test:unit": {
      "executor": "nx:run-commands",
      "options": { "command": "npx vitest run", "cwd": "libs/gadget" }
    }
  }
}
"""

let private vitestConfig =
    """import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["tests/unit/**/*.test.ts"],
  },
});
"""

[<Fact>]
let ``a vitest project selects exactly the files its include globs match`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" vitestProjectJson
    write root "libs/gadget/vitest.config.ts" vitestConfig
    write root "libs/gadget/tests/unit/core.test.ts" "export {};\n"
    write root "libs/gadget/src/core.ts" "export {};\n"

    let document = materialized root "gadget" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/gadget/tests/unit/core.test.ts")

[<Fact>]
let ``a vitest include rooted at src leaves the test in a forbidden directory`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" vitestProjectJson

    write root "libs/gadget/vitest.config.ts" (vitestConfig.Replace("tests/unit/**/*.test.ts", "src/**/*.unit.test.ts"))

    write root "libs/gadget/src/core.unit.test.ts" "export {};\n"
    write root "libs/gadget/tests/unit/core.test.ts" "export {};\n"

    let message =
        rejection (materialized root "gadget" [ TestContractLayout.LayerUnit ])

    Assert.Contains("layout-test-in-forbidden-directory", message)
    Assert.Contains("libs/gadget/src/core.unit.test.ts", message)

// ---------------------------------------------------------------------------
// The reader's own findings
// ---------------------------------------------------------------------------

[<Fact>]
let ``an executable test no runtime target selects is reported unselected`` () =
    let root = newTempRepo ()
    seedDotnetProject root
    write root "libs/widget/tests/unit/Tests/StrayTests.fs" "module StrayTests\n"

    let message =
        rejection (materialized root "widget" [ TestContractLayout.LayerUnit ])

    Assert.Contains("layout-file-unselected", message)
    Assert.Contains("libs/widget/tests/unit/Tests/StrayTests.fs", message)

[<Fact>]
let ``a layer directory the project does not own is reported as a placeholder`` () =
    let root = newTempRepo ()
    seedDotnetProject root
    write root "libs/widget/tests/e2e/.gitkeep" ""

    let message =
        rejection (materialized root "widget" [ TestContractLayout.LayerUnit ])

    Assert.Contains("layout-placeholder-directory", message)
    Assert.Contains("libs/widget/tests/e2e", message)

[<Fact>]
let ``non-test material under the tests root is materialized as non-executable`` () =
    let root = newTempRepo ()
    seedDotnetProject root
    write root "libs/widget/tests/fixtures/sample.json" "{}\n"

    let document = materialized root "widget" [ TestContractLayout.LayerUnit ]
    Assert.False((fileFor document "libs/widget/tests/fixtures/sample.json").Executable)

[<Fact>]
let ``a build output directory is never scanned`` () =
    let root = newTempRepo ()
    seedDotnetProject root
    write root "libs/widget/tests/unit/bin/Debug/GhostTests.fs" "module GhostTests\n"

    let document = materialized root "widget" [ TestContractLayout.LayerUnit ]

    Assert.DoesNotContain(document.Files, fun file -> file.Path = "libs/widget/tests/unit/bin/Debug/GhostTests.fs")

[<Fact>]
let ``a project no scanned root declares is a misuse, not a contract failure`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    match TestContractProject.materialize root "absent" [ TestContractLayout.LayerUnit ] with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok _ -> failwith "an unknown project must be rejected"

[<Fact>]
let ``one file selected by two runtime targets is reported twice-selected`` () =
    let root = newTempRepo ()

    write
        root
        "libs/gadget/project.json"
        """{
  "name": "gadget",
  "targets": {
    "test:unit": {
      "executor": "nx:run-commands",
      "options": { "command": "npx vitest run", "cwd": "libs/gadget" }
    },
    "test:integration": {
      "executor": "nx:run-commands",
      "options": { "command": "npx vitest run --config vitest.integration.config.ts", "cwd": "libs/gadget" }
    }
  }
}
"""

    write root "libs/gadget/vitest.config.ts" vitestConfig
    write root "libs/gadget/vitest.integration.config.ts" vitestConfig
    write root "libs/gadget/tests/unit/core.test.ts" "export {};\n"

    let message =
        rejection (materialized root "gadget" [ TestContractLayout.LayerUnit ])

    Assert.Contains("layout-file-selected-twice", message)
    Assert.Contains("test:unit,test:integration", message)

// ---------------------------------------------------------------------------
// Manifest policy against a real project
// ---------------------------------------------------------------------------

[<Fact>]
let ``a project with no package.json is manifest-compliant by default`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    match TestContractProject.validateManifestForProject root "widget" with
    | Ok rendered -> Assert.Contains("manifest-not-present", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

[<Fact>]
let ``a package.json another project actually depends on is manifest-compliant`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" """{ "name": "gadget", "targets": {} }"""
    write root "libs/gadget/package.json" """{ "name": "@scope/gadget" }"""
    write root "apps/consumer/project.json" """{ "name": "consumer", "targets": {} }"""

    write
        root
        "apps/consumer/package.json"
        """{ "name": "@scope/consumer", "dependencies": { "@scope/gadget": "0.1.0" } }"""

    match TestContractProject.validateManifestForProject root "gadget" with
    | Ok rendered -> Assert.Contains("manifest-consumer-verified", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

[<Fact>]
let ``a package.json no other project depends on or imports fails manifest policy`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" """{ "name": "gadget", "targets": {} }"""
    write root "libs/gadget/package.json" """{ "name": "@scope/gadget" }"""

    match TestContractProject.validateManifestForProject root "gadget" with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("manifest-no-direct-consumer", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

// ---------------------------------------------------------------------------
// Coverage policy against a real project
// ---------------------------------------------------------------------------

let private projectJsonWithCoverage (command: string) : string =
    "{ \"name\": \"widget\", \"targets\": { \"test:coverage\": { \"executor\": \"nx:run-commands\", \"options\": { \"command\": \""
    + command
    + "\" } } } }"

[<Fact>]
let ``a native threshold at or above the repository floor passes coverage policy`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" (projectJsonWithCoverage "dotnet test x.fsproj /p:Threshold=99")

    match TestContractProject.validateCoveragePolicyForProject root "widget" with
    | Ok rendered -> Assert.Contains("threshold=99", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

[<Fact>]
let ``a native threshold below the repository floor fails coverage policy`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" (projectJsonWithCoverage "dotnet test x.fsproj /p:Threshold=95")

    match TestContractProject.validateCoveragePolicyForProject root "widget" with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("coverage-below-floor", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``an echo placeholder fails coverage policy`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" (projectJsonWithCoverage "echo 'no-op'")

    match TestContractProject.validateCoveragePolicyForProject root "widget" with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("coverage-echo-placeholder", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``a missing test:coverage target fails coverage policy`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""

    match TestContractProject.validateCoveragePolicyForProject root "widget" with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("coverage-target-missing", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)
