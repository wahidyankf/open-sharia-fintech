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

// ---------------------------------------------------------------------------
// Project name resolution: absent name key and malformed JSON
// ---------------------------------------------------------------------------

[<Fact>]
let ``a project.json with no name key infers the project name from its directory`` () =
    let root = newTempRepo ()
    write root "libs/inferred/project.json" """{ "targets": {} }"""

    match TestContractProject.locate root "inferred" with
    | Some path -> Assert.Equal("libs/inferred", path)
    | None -> failwith "the inferred directory name must resolve the project"

[<Fact>]
let ``a project.json that is not valid JSON is never matched by locate, even by inferred directory name`` () =
    let root = newTempRepo ()
    write root "libs/broken/project.json" "{ not valid json"

    Assert.True(Option.isNone (TestContractProject.locate root "broken"), "malformed JSON must never be matched")

// ---------------------------------------------------------------------------
// Executable-test classification: Python's test_ prefix
// ---------------------------------------------------------------------------

[<Fact>]
let ``a python test_-prefixed file is classified executable even without the _test.py suffix`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "libs/widget/tests/unit/test_core.py" "def test_something(): pass\n"

    let document = materialized root "widget" []
    Assert.True((fileFor document "libs/widget/tests/unit/test_core.py").Executable)

// ---------------------------------------------------------------------------
// Glob edge cases: double-star, question-mark, and brace forms
// ---------------------------------------------------------------------------

[<Fact>]
let ``a double-star glob not immediately followed by a slash still matches across directories`` () =
    let root = newTempRepo ()
    write root "libs/mystic/project.json" (vitestProjectJson.Replace("gadget", "mystic"))
    write root "libs/mystic/vitest.config.ts" (vitestConfig.Replace("tests/unit/**/*.test.ts", "tests/**.test.ts"))
    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/mystic/tests/unit/core.test.ts")

[<Fact>]
let ``a question-mark glob matches exactly one non-separator character`` () =
    let root = newTempRepo ()
    write root "libs/mystic/project.json" (vitestProjectJson.Replace("gadget", "mystic"))

    write
        root
        "libs/mystic/vitest.config.ts"
        (vitestConfig.Replace("tests/unit/**/*.test.ts", "tests/unit/co?e.test.ts"))

    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"
    write root "libs/mystic/tests/unit/coreextra.test.ts" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/mystic/tests/unit/core.test.ts")
    Assert.Equal<string list>([], selectorsFor document "libs/mystic/tests/unit/coreextra.test.ts")

[<Fact>]
let ``an unmatched opening brace in a glob is treated as a literal character`` () =
    let root = newTempRepo ()
    write root "libs/mystic/project.json" (vitestProjectJson.Replace("gadget", "mystic"))

    write
        root
        "libs/mystic/vitest.config.ts"
        (vitestConfig.Replace("tests/unit/**/*.test.ts", "tests/unit/{unclosed.test.ts"))

    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([], selectorsFor document "libs/mystic/tests/unit/core.test.ts")

[<Fact>]
let ``a brace alternation glob matches any of its comma-separated options`` () =
    let root = newTempRepo ()
    write root "libs/mystic/project.json" (vitestProjectJson.Replace("gadget", "mystic"))

    write
        root
        "libs/mystic/vitest.config.ts"
        (vitestConfig.Replace("tests/unit/**/*.test.ts", "tests/unit/*.{test.ts,test.tsx}"))

    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"
    write root "libs/mystic/tests/unit/widget.test.tsx" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/mystic/tests/unit/core.test.ts")
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/mystic/tests/unit/widget.test.tsx")

// ---------------------------------------------------------------------------
// Runner discovery: the combined --config=<path> flag form
// ---------------------------------------------------------------------------

[<Fact>]
let ``a vitest command's combined --config=<path> flag form is resolved`` () =
    let root = newTempRepo ()

    write
        root
        "libs/mystic/project.json"
        """{
  "name": "mystic",
  "targets": {
    "test:unit": {
      "executor": "nx:run-commands",
      "options": { "command": "npx vitest run --config=vitest.custom.config.ts", "cwd": "libs/mystic" }
    }
  }
}
"""

    write root "libs/mystic/vitest.custom.config.ts" vitestConfig
    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/mystic/tests/unit/core.test.ts")

// ---------------------------------------------------------------------------
// Runner discovery: absent or unrecognized configuration
// ---------------------------------------------------------------------------

[<Fact>]
let ``a vitest command with no config file selects nothing`` () =
    let root = newTempRepo ()
    write root "libs/mystic/project.json" (vitestProjectJson.Replace("gadget", "mystic"))
    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([], selectorsFor document "libs/mystic/tests/unit/core.test.ts")

[<Fact>]
let ``a vitest config without an include array selects nothing`` () =
    let root = newTempRepo ()
    write root "libs/mystic/project.json" (vitestProjectJson.Replace("gadget", "mystic"))

    write
        root
        "libs/mystic/vitest.config.ts"
        """import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {},
});
"""

    write root "libs/mystic/tests/unit/core.test.ts" "export {};\n"

    let document = materialized root "mystic" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([], selectorsFor document "libs/mystic/tests/unit/core.test.ts")

[<Fact>]
let ``an unrecognized runner command selects nothing`` () =
    let root = newTempRepo ()

    write
        root
        "libs/widget-odd/project.json"
        """{ "name": "widget-odd", "targets": { "test:unit": { "executor": "nx:run-commands", "options": { "command": "npm run something-else" } } } }"""

    write root "libs/widget-odd/tests/unit/SomeTests.fs" "module SomeTests\n"

    let document = materialized root "widget-odd" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([], selectorsFor document "libs/widget-odd/tests/unit/SomeTests.fs")

// ---------------------------------------------------------------------------
// Runner discovery: Playwright
// ---------------------------------------------------------------------------

let private playwrightProjectJson =
    """{
  "name": "portal",
  "targets": {
    "test:e2e": {
      "executor": "nx:run-commands",
      "options": { "command": "npx playwright test", "cwd": "apps/portal" }
    }
  }
}
"""

let private playwrightConfigWithTestDir =
    """import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "tests/e2e",
});
"""

let private playwrightConfigWithoutTestDir =
    """import { defineConfig } from "@playwright/test";

export default defineConfig({});
"""

[<Fact>]
let ``a playwright project selects exactly the files under its testDir`` () =
    let root = newTempRepo ()
    write root "apps/portal/project.json" playwrightProjectJson
    write root "apps/portal/playwright.config.ts" playwrightConfigWithTestDir
    write root "apps/portal/tests/e2e/smoke.spec.ts" "export {};\n"

    let document = materialized root "portal" [ TestContractLayout.LayerE2e ]
    Assert.Equal<string list>([ "test:e2e" ], selectorsFor document "apps/portal/tests/e2e/smoke.spec.ts")

[<Fact>]
let ``a playwright config missing testDir selects nothing`` () =
    let root = newTempRepo ()
    write root "apps/portal/project.json" playwrightProjectJson
    write root "apps/portal/playwright.config.ts" playwrightConfigWithoutTestDir
    write root "apps/portal/tests/e2e/smoke.spec.ts" "export {};\n"

    let document = materialized root "portal" [ TestContractLayout.LayerE2e ]
    Assert.Equal<string list>([], selectorsFor document "apps/portal/tests/e2e/smoke.spec.ts")

[<Fact>]
let ``a playwright command whose config file cannot be resolved selects nothing`` () =
    let root = newTempRepo ()
    write root "apps/portal/project.json" playwrightProjectJson
    write root "apps/portal/tests/e2e/smoke.spec.ts" "export {};\n"

    let document = materialized root "portal" [ TestContractLayout.LayerE2e ]
    Assert.Equal<string list>([], selectorsFor document "apps/portal/tests/e2e/smoke.spec.ts")

// ---------------------------------------------------------------------------
// Target command shapes: absent options and a commands array
// ---------------------------------------------------------------------------

[<Fact>]
let ``a target with no options at all selects nothing`` () =
    let root = newTempRepo ()

    write
        root
        "libs/widget-bare/project.json"
        """{ "name": "widget-bare", "targets": { "test:unit": { "executor": "nx:run-commands" } } }"""

    write root "libs/widget-bare/tests/unit/SomeTests.fs" "module SomeTests\n"

    let document = materialized root "widget-bare" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([], selectorsFor document "libs/widget-bare/tests/unit/SomeTests.fs")

let private commandsArrayProjectJson =
    """{
  "name": "widget-multi",
  "targets": {
    "test:unit": {
      "executor": "nx:run-commands",
      "options": {
        "commands": [
          "dotnet test libs/widget-multi/tests/unit/a.fsproj",
          { "command": "dotnet test libs/widget-multi/tests/unit/b.fsproj" },
          { "forwardAllArgs": true }
        ]
      }
    }
  }
}
"""

let private singleCompileFsproj (fileName: string) : string =
    sprintf
        """<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <Compile Include="%s" />
  </ItemGroup>
</Project>
"""
        fileName

[<Fact>]
let ``a target's commands array combines string and object entries, dropping entries without a command`` () =
    let root = newTempRepo ()
    write root "libs/widget-multi/project.json" commandsArrayProjectJson
    write root "libs/widget-multi/tests/unit/a.fsproj" (singleCompileFsproj "ATests.fs")
    write root "libs/widget-multi/tests/unit/b.fsproj" (singleCompileFsproj "BTests.fs")
    write root "libs/widget-multi/tests/unit/ATests.fs" "module ATests\n"
    write root "libs/widget-multi/tests/unit/BTests.fs" "module BTests\n"

    let document = materialized root "widget-multi" [ TestContractLayout.LayerUnit ]

    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/widget-multi/tests/unit/ATests.fs")
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/widget-multi/tests/unit/BTests.fs")

// ---------------------------------------------------------------------------
// A project.json with no targets key at all
// ---------------------------------------------------------------------------

[<Fact>]
let ``a project.json with no targets key selects nothing for any file`` () =
    let root = newTempRepo ()
    write root "libs/widget-notargets/project.json" """{ "name": "widget-notargets" }"""
    write root "libs/widget-notargets/tests/unit/SomeTests.fs" "module SomeTests\n"

    let document = materialized root "widget-notargets" [ TestContractLayout.LayerUnit ]
    Assert.Equal<string list>([], selectorsFor document "libs/widget-notargets/tests/unit/SomeTests.fs")

// ---------------------------------------------------------------------------
// A project with no tests directory
// ---------------------------------------------------------------------------

[<Fact>]
let ``a project with no tests directory reports no directories`` () =
    let root = newTempRepo ()
    write root "libs/widget-notests/project.json" """{ "name": "widget-notests", "targets": {} }"""
    write root "libs/widget-notests/src/Core.fs" "module Core\n"

    let document = materialized root "widget-notests" []
    Assert.Empty(document.Directories)

// ---------------------------------------------------------------------------
// materializeLayout and validateLayoutForProject against the canonical registry
// ---------------------------------------------------------------------------

let private layoutRegistryYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects: []"
          "testing:"
          "  schema: ose-test-contract/v1"
          "  coverage:"
          "    minimum-line: 99"
          "  compatibility:"
          "    mappings: []"
          "  projects:"
          "    - project: widget"
          "      profile: library"
          "      migration-state: verified"
          "      behavior:"
          "        id: widget:default"
          "        lifecycle-state: active"
          "        owner: widget"
          "        corpus: []"
          "        adapters:"
          "          unit:"
          "            disposition: required"
          "            project: widget"
          "            driver: libs/widget/tests/unit/bdd/unit-driver.ts"
          "          integration:"
          "            disposition: inapplicable"
          "            reason: no isolated local-resource boundary"
          "          e2e:"
          "            disposition: inapplicable"
          "            reason: no isolated local-resource boundary"
          "" ]

let private legacyOnlyRegistryYaml =
    String.concat "\n" [ "coverage:"; "  projects: []"; "" ]

let private newLayoutRegistryRoot () : string =
    let root = newTempRepo ()
    write root "repo-config.yml" layoutRegistryYaml
    seedDotnetProject root
    root

[<Fact>]
let ``materializeLayout surfaces a registry parse failure unchanged`` () =
    let root = newTempRepo ()

    match TestContractProject.materializeLayout root "widget" with
    | Error(TestContract.Misuse message) -> Assert.Contains("repo-config.yml", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok _ -> failwith "a missing registry must fail"

[<Fact>]
let ``materializeLayout is a misuse when the registry has no testing root`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" legacyOnlyRegistryYaml
    seedDotnetProject root

    match TestContractProject.materializeLayout root "widget" with
    | Error(TestContract.Misuse message) -> Assert.Contains("testing: is absent", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok _ -> failwith "an absent testing root must fail"

[<Fact>]
let ``materializeLayout is a misuse when the registry declares no row for the project`` () =
    let root = newLayoutRegistryRoot ()

    match TestContractProject.materializeLayout root "absent-project" with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent-project", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok _ -> failwith "an unknown row must fail"

[<Fact>]
let ``materializeLayout resolves the owner from the registry and materializes the real project`` () =
    let root = newLayoutRegistryRoot ()

    match TestContractProject.materializeLayout root "widget" with
    | Ok document ->
        Assert.Equal("widget", document.Owner)
        Assert.Equal<TestContractLayout.Layer list>([ TestContractLayout.LayerUnit ], document.OwnedLayers)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)

[<Fact>]
let ``validateLayoutForProject measures the real project end to end against the canonical registry`` () =
    let root = newLayoutRegistryRoot ()

    match TestContractProject.validateLayoutForProject root "widget" with
    | Ok rendered ->
        Assert.Contains("native-layout-valid", rendered)
        Assert.Contains("project=widget", rendered)
        Assert.Contains("owner=widget", rendered)
        Assert.Contains("layers=unit", rendered)
        Assert.Contains("executable=1", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

// ---------------------------------------------------------------------------
// Manifest policy: further real-project edge cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``a malformed sibling package.json is never counted as a declared dependency`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" """{ "name": "gadget", "targets": {} }"""
    write root "libs/gadget/package.json" """{ "name": "@scope/gadget" }"""
    write root "apps/consumer/project.json" """{ "name": "consumer", "targets": {} }"""
    write root "apps/consumer/package.json" "{ this is not valid json"

    match TestContractProject.validateManifestForProject root "gadget" with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("manifest-no-direct-consumer", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``a source file elsewhere importing the package name by content is a direct consumer`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" """{ "name": "gadget", "targets": {} }"""
    write root "libs/gadget/package.json" """{ "name": "@scope/gadget" }"""
    write root "apps/consumer/project.json" """{ "name": "consumer", "targets": {} }"""
    write root "apps/consumer/src/main.ts" "import \"@scope/gadget\";\n"

    match TestContractProject.validateManifestForProject root "gadget" with
    | Ok rendered -> Assert.Contains("manifest-consumer-verified", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

[<Fact>]
let ``an unreadable candidate source file never counts as a direct consumer`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" """{ "name": "gadget", "targets": {} }"""
    write root "libs/gadget/package.json" """{ "name": "@scope/gadget" }"""
    write root "apps/consumer/project.json" """{ "name": "consumer", "targets": {} }"""
    write root "apps/consumer/src/broken.ts" "import \"@scope/gadget\";\n"

    let brokenPath = Path.Combine(root, "apps", "consumer", "src", "broken.ts")

    File.SetUnixFileMode(brokenPath, UnixFileMode.None)

    try
        match TestContractProject.validateManifestForProject root "gadget" with
        | Error(TestContract.ContractFailure message) -> Assert.Contains("manifest-no-direct-consumer", message)
        | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
        | Ok rendered -> failwith ("must fail, found: " + rendered)
    finally
        File.SetUnixFileMode(brokenPath, UnixFileMode.UserRead ||| UnixFileMode.UserWrite)

[<Fact>]
let ``an unknown project fails manifest policy as misuse`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    match TestContractProject.validateManifestForProject root "absent" with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("an unknown project must fail, found: " + rendered)

[<Fact>]
let ``a package.json with no name key fails manifest policy as misuse`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "libs/widget/package.json" "{}"

    match TestContractProject.validateManifestForProject root "widget" with
    | Error(TestContract.Misuse message) -> Assert.Contains("has no \"name\"", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``a malformed package.json fails manifest policy as misuse`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "libs/widget/package.json" "{ not valid json"

    match TestContractProject.validateManifestForProject root "widget" with
    | Error(TestContract.Misuse message) -> Assert.Contains("is not valid JSON", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

// ---------------------------------------------------------------------------
// Coverage policy: further real-project edge cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``an unknown project fails coverage policy as misuse`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    match TestContractProject.validateCoveragePolicyForProject root "absent" with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("an unknown project must fail, found: " + rendered)

[<Fact>]
let ``a project.json with no targets key fails coverage policy as misuse`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" """{ "name": "widget" }"""

    match TestContractProject.validateCoveragePolicyForProject root "widget" with
    | Error(TestContract.Misuse message) -> Assert.Contains("has no targets", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``a coverage command declaring no threshold fails as threshold-undeclared`` () =
    let root = newTempRepo ()
    write root "libs/widget/project.json" (projectJsonWithCoverage "dotnet test x.fsproj --collect XPlat-Code-Coverage")

    match TestContractProject.validateCoveragePolicyForProject root "widget" with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("coverage-threshold-undeclared", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)
