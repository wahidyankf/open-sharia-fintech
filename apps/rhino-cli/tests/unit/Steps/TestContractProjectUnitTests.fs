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
// Runner discovery: .NET wrapper scripts
//
// A docker-compose-orchestrated integration suite commonly lives behind a
// wrapper script (bring dependencies up, export env, run `dotnet test`, tear
// down even on failure via a trap) rather than a direct `dotnet test`
// command in project.json — `apps/organiclever-be/scripts/run-integration.sh`
// and `apps/ose-be/scripts/run-integration.sh` both do this. Without reading
// into the script, its command string names no `.fsproj`, so every file the
// suite it runs owns is wrongly reported unselected.
// ---------------------------------------------------------------------------

let private wrapperScriptProjectJson =
    """{
  "name": "widget-wrapped",
  "targets": {
    "test:integration": {
      "executor": "nx:run-commands",
      "options": { "command": "libs/widget-wrapped/scripts/run-integration.sh" }
    }
  }
}
"""

/// Mirrors the real repository's own `scripts/run-integration.sh` convention:
/// a `ROOT` variable computed from the script's own location, then every path
/// addressed from it with a `${ROOT}/` prefix.
let private wrapperScriptBody (fsprojRelativePath: string) : string =
    "#!/usr/bin/env bash\n"
    + "set -euo pipefail\n"
    + "ROOT=\"$(cd \"$(dirname \"${BASH_SOURCE[0]}\")/../../..\" && pwd)\"\n"
    + "docker compose -f \"${ROOT}/libs/widget-wrapped/docker-compose.integration.yml\" up -d --wait\n"
    + "dotnet test \"${ROOT}/"
    + fsprojRelativePath
    + "\" --logger \"console;verbosity=normal\"\n"

[<Fact>]
let ``a wrapper-script test:integration command selects the files its inner dotnet test compile list names`` () =
    let root = newTempRepo ()
    write root "libs/widget-wrapped/project.json" wrapperScriptProjectJson

    write
        root
        "libs/widget-wrapped/scripts/run-integration.sh"
        (wrapperScriptBody "libs/widget-wrapped/tests/integration/widget-wrapped-integration-tests.fsproj")

    write
        root
        "libs/widget-wrapped/tests/integration/widget-wrapped-integration-tests.fsproj"
        """<Project Sdk="Microsoft.NET.Sdk">
  <ItemGroup>
    <Compile Include="IntegrationCoreTests.fs" />
  </ItemGroup>
</Project>
"""

    write root "libs/widget-wrapped/tests/integration/IntegrationCoreTests.fs" "module IntegrationCoreTests\n"

    let document =
        materialized root "widget-wrapped" [ TestContractLayout.LayerIntegration ]

    Assert.Equal<string list>(
        [ "test:integration" ],
        selectorsFor document "libs/widget-wrapped/tests/integration/IntegrationCoreTests.fs"
    )

[<Fact>]
let ``a wrapper script that never calls dotnet test still leaves its files genuinely unselected`` () =
    let root = newTempRepo ()
    write root "libs/widget-wrapped/project.json" wrapperScriptProjectJson

    write
        root
        "libs/widget-wrapped/scripts/run-integration.sh"
        "#!/usr/bin/env bash\nset -euo pipefail\necho 'nothing to run yet'\n"

    write root "libs/widget-wrapped/tests/integration/StrayIntegrationTests.fs" "module StrayIntegrationTests\n"

    let message =
        rejection (materialized root "widget-wrapped" [ TestContractLayout.LayerIntegration ])

    Assert.Contains("layout-file-unselected", message)
    Assert.Contains("libs/widget-wrapped/tests/integration/StrayIntegrationTests.fs", message)

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

[<Fact>]
let ``a multi-project vitest config unions every project's include globs, not just the first`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" vitestProjectJson

    // `coverage.include` is a top-level `include:` key that appears, textually, before either
    // named project's own `test.include` — the exact shape `ayokoding-www`'s real config has.
    // A reader that stops at the first `include:` match in the file would resolve only
    // `coverage.include`'s glob (`src/**/*.{ts,tsx}`) and never see either project's real
    // selection globs.
    write
        root
        "libs/gadget/vitest.config.ts"
        """import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      include: ["src/**/*.ts"],
    },
    projects: [
      { test: { name: "unit", include: ["tests/unit/**/*.unit.test.ts"] } },
      { test: { name: "unit-fe", include: ["tests/unit/**/*.test.tsx"] } },
    ],
  },
});
"""

    write root "libs/gadget/tests/unit/core.unit.test.ts" "export {};\n"
    write root "libs/gadget/tests/unit/widget.test.tsx" "export {};\n"

    let document = materialized root "gadget" [ TestContractLayout.LayerUnit ]

    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/gadget/tests/unit/core.unit.test.ts")
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/gadget/tests/unit/widget.test.tsx")

[<Fact>]
let ``a prose comment inside an include array never contaminates the real glob list`` () =
    let root = newTempRepo ()
    write root "libs/gadget/project.json" vitestProjectJson

    // An odd number of quote-like characters (`"`, `'`, `` ` ``) inside the array before a real
    // glob entry shifts every open/close pairing after it by one — exactly what a lone
    // apostrophe in ordinary prose ("it's") does. A naive quote-delimited scan (no comment
    // stripping) then pairs this entry's own opening quote with the apostrophe instead of its
    // real closing quote, and its real closing quote is left dangling with no partner — the glob
    // is silently dropped rather than merely garbled. This is the exact shape that made
    // `ayokoding-www`'s real `vitest.config.ts` misresolve its last, real glob entry.
    write
        root
        "libs/gadget/vitest.config.ts"
        """import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: [
      "tests/unit/keep.test.ts",
      // it's a note
      "tests/unit/lose.test.ts",
    ],
  },
});
"""

    write root "libs/gadget/tests/unit/keep.test.ts" "export {};\n"
    write root "libs/gadget/tests/unit/lose.test.ts" "export {};\n"

    let document = materialized root "gadget" [ TestContractLayout.LayerUnit ]

    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/gadget/tests/unit/keep.test.ts")
    Assert.Equal<string list>([ "test:unit" ], selectorsFor document "libs/gadget/tests/unit/lose.test.ts")

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
let ``a content directory sample file is never scanned as an executable test`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    write root "libs/widget/content/en/learn/courses/example/code/test_sample.py" "def test_x(): pass\n"

    let document = materialized root "widget" [ TestContractLayout.LayerUnit ]

    Assert.DoesNotContain(
        document.Files,
        fun file -> file.Path = "libs/widget/content/en/learn/courses/example/code/test_sample.py"
    )

[<Fact>]
let ``a playwright-bdd .features-gen output directory is never scanned as an executable test`` () =
    let root = newTempRepo ()
    seedDotnetProject root

    write root "libs/widget/.features-gen/specs/apps/widget/behaviors/example.feature.spec.js" "// generated\n"

    let document = materialized root "widget" [ TestContractLayout.LayerUnit ]

    Assert.DoesNotContain(
        document.Files,
        fun file -> file.Path = "libs/widget/.features-gen/specs/apps/widget/behaviors/example.feature.spec.js"
    )

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
let ``a playwright-bdd config with a computed testDir still selects files its literal steps glob matches`` () =
    let root = newTempRepo ()
    write root "apps/portal/project.json" playwrightProjectJson

    // `playwright-bdd`'s `defineBddConfig({ ... })` returns a generated output directory that
    // every real project in this repository assigns to `testDir` as a bare variable reference —
    // never a string literal `playwrightTestDir` can read. The `steps:` option it also takes is a
    // literal glob, and is the real, authored surface a BDD e2e project owns; the generated
    // `testDir` output is machine-written and already excluded via `.features-gen`.
    write
        root
        "apps/portal/playwright.config.ts"
        """import { defineConfig } from "@playwright/test";
import { defineBddConfig } from "playwright-bdd";

const testDir = defineBddConfig({
  steps: "./tests/e2e/steps/**/*.steps.ts",
});

export default defineConfig({ testDir });
"""

    write root "apps/portal/tests/e2e/steps/checkout.steps.ts" "export {};\n"

    let document = materialized root "portal" [ TestContractLayout.LayerE2e ]
    Assert.Equal<string list>([ "test:e2e" ], selectorsFor document "apps/portal/tests/e2e/steps/checkout.steps.ts")

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

// ---------------------------------------------------------------------------
// BDD coverage against a real project: materializeBdd / validateBehaviorCoverageForProject
// ---------------------------------------------------------------------------

/// One `testing.projects[]` row's YAML, indented to nest under `projects:`.
/// `unitLines`/`integrationLines`/`e2eLines` supply each adapter's own body
/// lines verbatim (already `disposition:`-first), matching how
/// `layoutRegistryYaml` above hand-writes its own single row.
let private bddProjectRowYaml
    (project: string)
    (owner: string)
    (corpus: string list)
    (unitLines: string list)
    (integrationLines: string list)
    (e2eLines: string list)
    : string =
    let corpusRendered = corpus |> List.map (sprintf "\"%s\"") |> String.concat ", "

    String.concat
        "\n"
        ([ sprintf "    - project: %s" project
           "      profile: library"
           "      migration-state: verified"
           "      behavior:"
           sprintf "        id: %s:default" project
           "        lifecycle-state: active"
           sprintf "        owner: %s" owner
           sprintf "        corpus: [%s]" corpusRendered
           "        adapters:"
           "          unit:" ]
         @ (unitLines |> List.map (fun line -> "            " + line))
         @ [ "          integration:" ]
         @ (integrationLines |> List.map (fun line -> "            " + line))
         @ [ "          e2e:" ]
         @ (e2eLines |> List.map (fun line -> "            " + line)))

let private inapplicableLines (reason: string) : string list =
    [ "disposition: inapplicable"; sprintf "reason: %s" reason ]

let private requiredLines (project: string) (driver: string) : string list =
    [ "disposition: required"
      sprintf "project: %s" project
      sprintf "driver: %s" driver ]

let private requiredNoDriverLines (project: string) : string list =
    [ "disposition: required"; sprintf "project: %s" project ]

let private delegatedLines (project: string) (driver: string) : string list =
    [ "disposition: delegated"
      sprintf "project: %s" project
      sprintf "driver: %s" driver ]

let private bddRegistryYaml (rows: string list) : string =
    String.concat
        "\n"
        ([ "coverage:"
           "  projects: []"
           "testing:"
           "  schema: ose-test-contract/v1"
           "  coverage:"
           "    minimum-line: 99"
           "  compatibility:"
           "    mappings: []"
           "  projects:" ]
         @ rows
         @ [ "" ])

/// Renders a step-definition attribute (Given, When, Then, ...) at run time
/// rather than as a literal in this file's own source text. This temp-repo
/// fixture content is only ever meant to be scanned as a TickSpec-shaped
/// driver once it is written to disk under a throwaway repo root — but
/// `Specs.fs`'s own step scanner reads raw `.fs` text line by line with no
/// notion of string-literal context, so writing the bracketed attribute text
/// as a literal right here would itself be misread by
/// `specs behavior-coverage validate` (and every other caller of that
/// scanner) as a genuine, uncovered step implementation living in this file.
/// Building the bracket text from a keyword argument keeps this source line
/// free of the literal substring the scanner matches on, while still writing
/// the exact same bytes into the fixture files below.
let private stepAttribute (keyword: string) : string = sprintf "[<%s>]" keyword

let private simpleFeature (title: string) (scenarioTitle: string) : string =
    String.concat
        "\n"
        [ sprintf "Feature: %s" title
          sprintf "  Scenario: %s" scenarioTitle
          "    Given a cart with one item"
          "    When I check out"
          "    Then I see a receipt"
          "" ]

let private simpleStepsFs (moduleName: string) : string =
    String.concat
        "\n"
        [ sprintf "module %s" moduleName
          ""
          (stepAttribute "Given")
          "let ``a cart with one item`` () = ()"
          ""
          (stepAttribute "When")
          "let ``I check out`` () = ()"
          ""
          (stepAttribute "Then")
          "let ``I see a receipt`` () = ()"
          "" ]

let private widgetUnitRow (driver: string) : string =
    bddProjectRowYaml
        "widget"
        "widget"
        [ "specs/widget/behaviors/**" ]
        (requiredLines "widget" driver)
        (inapplicableLines "no isolated local-resource boundary")
        (inapplicableLines "no user-facing surface")

[<Fact>]
let ``validateBehaviorCoverageForProject passes a required adapter whose driver tree binds the whole corpus`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" (simpleFeature "Checkout" "Checkout succeeds")
    write root "libs/widget/tests/unit/steps/WidgetSteps.fs" (simpleStepsFs "Widget.Tests.Unit.Steps.WidgetSteps")

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Ok rendered ->
        Assert.Contains("behavior-coverage-valid", rendered)
        Assert.Contains("files=1/1", rendered)
        Assert.Contains("scenarios=1/1", rendered)
        Assert.Contains("steps=3/3", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

[<Fact>]
let ``validateBehaviorCoverageForProject reports an undefined binding for a step no driver file implements`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" (simpleFeature "Checkout" "Checkout succeeds")

    write
        root
        "specs/widget/behaviors/refund.feature"
        (String.concat
            "\n"
            [ "Feature: Refund"
              "  Scenario: Refund issued"
              "    Given a completed order"
              "    When I request a refund"
              "    Then the refund is issued"
              "" ])

    write root "libs/widget/tests/unit/steps/WidgetSteps.fs" (simpleStepsFs "Widget.Tests.Unit.Steps.WidgetSteps")

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.ContractFailure message) ->
        Assert.Contains("bdd-undefined-binding", message)
        Assert.Contains("specs/widget/behaviors/refund.feature|Refund issued|1|Given a completed order", message)
        Assert.Contains("bdd-uncovered-feature", message)
        Assert.Contains("files=1/2", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

let private outlineFeature =
    String.concat
        "\n"
        [ "Feature: Checkout"
          "  Scenario Outline: Checkout with <item> items"
          "    Given a cart with <item> items"
          "    When I check out"
          "    Then I see a receipt"
          ""
          "    Examples:"
          "      | item |"
          "      | one  |"
          "      | two  |"
          "" ]

let private outlineStepsFs =
    String.concat
        "\n"
        [ "module Widget.Tests.Unit.Steps.OutlineSteps"
          ""
          (stepAttribute "Given")
          "let ``a cart with one items`` () = ()"
          ""
          (stepAttribute "When")
          "let ``I check out`` () = ()"
          ""
          (stepAttribute "Then")
          "let ``I see a receipt`` () = ()"
          "" ]

[<Fact>]
let ``validateBehaviorCoverageForProject reports one scenario-outline example the driver never binds`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" outlineFeature
    write root "libs/widget/tests/unit/steps/OutlineSteps.fs" outlineStepsFs

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.ContractFailure message) ->
        Assert.Contains("bdd-uncovered-example", message)
        Assert.Contains("bdd-undefined-binding", message)
        Assert.Contains("examples=1/2", message)
        Assert.DoesNotContain("100%", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

let private stepsFsWithOrphan =
    String.concat
        "\n"
        [ "module Widget.Tests.Unit.Steps.WidgetSteps"
          ""
          (stepAttribute "Given")
          "let ``a cart with one item`` () = ()"
          ""
          (stepAttribute "When")
          "let ``I check out`` () = ()"
          ""
          (stepAttribute "Then")
          "let ``I see a receipt`` () = ()"
          ""
          (stepAttribute "Given")
          "let ``a step nothing in the corpus ever asks for`` () = ()"
          "" ]

[<Fact>]
let ``validateBehaviorCoverageForProject reports an orphan step implementation as an unused binding`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" (simpleFeature "Checkout" "Checkout succeeds")
    write root "libs/widget/tests/unit/steps/WidgetSteps.fs" stepsFsWithOrphan

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.ContractFailure message) ->
        Assert.Contains("bdd-unused-binding", message)
        Assert.Contains("unbound-driver-entry|", message)
        Assert.Contains("a step nothing in the corpus ever asks for", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject passes an inapplicable adapter without requiring a corpus`` () =
    let root = newTempRepo ()

    write
        root
        "repo-config.yml"
        (bddRegistryYaml
            [ bddProjectRowYaml
                  "widget"
                  "widget"
                  [ "specs/widget/behaviors/**" ]
                  (inapplicableLines "no user-facing surface")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface") ])

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Ok rendered ->
        Assert.Contains("behavior-coverage-not-applicable", rendered)
        Assert.Contains("reason=no user-facing surface", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

[<Fact>]
let ``validateBehaviorCoverageForProject resolves a delegated adapter's driver through the reciprocal project`` () =
    let root = newTempRepo ()

    write
        root
        "repo-config.yml"
        (bddRegistryYaml
            [ bddProjectRowYaml
                  "widget"
                  "widget"
                  [ "specs/widget/behaviors/**" ]
                  (delegatedLines "widget-e2e-host" "libs/widget-e2e-host/tests/e2e/steps/driver.fs")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface") ])

    write root "libs/widget-e2e-host/project.json" """{ "name": "widget-e2e-host", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" (simpleFeature "Checkout" "Checkout succeeds")

    write
        root
        "libs/widget-e2e-host/tests/e2e/steps/HostSteps.fs"
        (simpleStepsFs "WidgetE2eHost.Tests.E2e.Steps.HostSteps")

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Ok rendered ->
        Assert.Contains("behavior-coverage-valid", rendered)
        Assert.Contains("project=widget", rendered)
        Assert.Contains("disposition=delegated", rendered)
        Assert.Contains("files=1/1", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

let private manyScenariosFeature (count: int) : string =
    let scenarios =
        [ for i in 1..count do
              yield sprintf "  Scenario: Case %d" i
              yield sprintf "    Given case %d starts" i
              yield "    When I check out"
              yield "    Then I see a receipt" ]

    String.concat "\n" ([ "Feature: Bulk" ] @ scenarios @ [ "" ])

let private manyStepsFs (count: int) : string =
    let givens =
        [ for i in 1..count do
              yield (stepAttribute "Given")
              yield sprintf "let ``case %d starts`` () = ()" i
              yield "" ]

    String.concat
        "\n"
        ([ "module Widget.Tests.Unit.Steps.BulkSteps"; "" ]
         @ givens
         @ [ (stepAttribute "When")
             "let ``I check out`` () = ()"
             ""
             (stepAttribute "Then")
             "let ``I see a receipt`` () = ()"
             "" ])

[<Fact>]
let ``validateBehaviorCoverageForProject fails a large corpus missing exactly one step, never rounding to a pass`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/bulk.feature" (manyScenariosFeature 50)
    // 49 of the 50 "case N starts" steps are implemented; case 50 is not.
    write root "libs/widget/tests/unit/steps/BulkSteps.fs" (manyStepsFs 49)

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.ContractFailure message) ->
        Assert.Contains("steps=149/150", message)
        Assert.DoesNotContain("100%", message)
        Assert.Contains("bdd-undefined-binding", message)
        Assert.Contains("case 50 starts", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject surfaces a registry parse failure unchanged`` () =
    let root = newTempRepo ()

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.Misuse message) -> Assert.Contains("repo-config.yml", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("a missing registry must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject is a misuse when the registry has no testing root`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" legacyOnlyRegistryYaml

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.Misuse message) -> Assert.Contains("testing: is absent", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("an absent testing root must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject is a misuse when the registry declares no row for the project`` () =
    let root = newTempRepo ()

    write
        root
        "repo-config.yml"
        (bddRegistryYaml
            [ bddProjectRowYaml
                  "widget"
                  "widget"
                  [ "specs/widget/behaviors/**" ]
                  (inapplicableLines "no user-facing surface")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface") ])

    match TestContractProject.validateBehaviorCoverageForProject root "absent-project" TestContractBdd.AdapterUnit with
    | Error(TestContract.Misuse message) -> Assert.Contains("absent-project", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("an unknown row must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject fails as a contract violation when a required adapter omits its driver`` () =
    let root = newTempRepo ()

    write
        root
        "repo-config.yml"
        (bddRegistryYaml
            [ bddProjectRowYaml
                  "widget"
                  "widget"
                  [ "specs/widget/behaviors/**" ]
                  (requiredNoDriverLines "widget")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface") ])

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("bdd-driver-undeclared", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject is a misuse when the adapter's host project has no project.json`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    // Deliberately no libs/widget/project.json.

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.Misuse message) ->
        Assert.Contains("no project.json under apps/, libs/, or specs/ declares the project", message)
    | Error(TestContract.ContractFailure message) -> failwith ("expected misuse, found contract failure: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject fails as a contract violation when the row resolves no corpus`` () =
    let root = newTempRepo ()

    write
        root
        "repo-config.yml"
        (bddRegistryYaml
            [ bddProjectRowYaml
                  "widget"
                  "widget"
                  []
                  (requiredLines "widget" "libs/widget/tests/unit/steps/driver.fs")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface") ])

    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Error(TestContract.ContractFailure message) -> Assert.Contains("bdd-corpus-empty", message)
    | Error(TestContract.Misuse message) -> failwith ("expected a contract failure, found misuse: " + message)
    | Ok rendered -> failwith ("must fail, found: " + rendered)

[<Fact>]
let ``validateBehaviorCoverageForProject inherits the corpus from behavior.owner when a delegate row leaves it empty``
    ()
    =
    let root = newTempRepo ()

    write
        root
        "repo-config.yml"
        (bddRegistryYaml
            [ bddProjectRowYaml
                  "widget"
                  "widget"
                  [ "specs/widget/behaviors" ]
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface")
              bddProjectRowYaml
                  "widget-part"
                  "widget"
                  []
                  (requiredLines "widget-part" "libs/widget-part/tests/unit/steps/driver.fs")
                  (inapplicableLines "no isolated local-resource boundary")
                  (inapplicableLines "no user-facing surface") ])

    write root "libs/widget-part/project.json" """{ "name": "widget-part", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" (simpleFeature "Checkout" "Checkout succeeds")

    write root "libs/widget-part/tests/unit/steps/PartSteps.fs" (simpleStepsFs "WidgetPart.Tests.Unit.Steps.PartSteps")

    match TestContractProject.validateBehaviorCoverageForProject root "widget-part" TestContractBdd.AdapterUnit with
    | Ok rendered ->
        Assert.Contains("behavior-coverage-valid", rendered)
        Assert.Contains("project=widget-part", rendered)
        Assert.Contains("files=1/1", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

let private featureWithBackground =
    String.concat
        "\n"
        [ "Feature: Checkout"
          "  Background:"
          "    Given the store is open"
          ""
          "  Scenario: Checkout succeeds"
          "    Given a cart with one item"
          "    When I check out"
          "    Then I see a receipt"
          "" ]

let private stepsFsWithBackground =
    String.concat
        "\n"
        [ "module Widget.Tests.Unit.Steps.BackgroundSteps"
          ""
          (stepAttribute "Given")
          "let ``the store is open`` () = ()"
          ""
          (stepAttribute "Given")
          "let ``a cart with one item`` () = ()"
          ""
          (stepAttribute "When")
          "let ``I check out`` () = ()"
          ""
          (stepAttribute "Then")
          "let ``I see a receipt`` () = ()"
          "" ]

[<Fact>]
let ``validateBehaviorCoverageForProject folds a Background's steps into the one real scenario, not a second scenario``
    ()
    =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" featureWithBackground
    write root "libs/widget/tests/unit/steps/BackgroundSteps.fs" stepsFsWithBackground

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Ok rendered ->
        Assert.Contains("scenarios=1/1", rendered)
        Assert.Contains("steps=4/4", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)

let private wipOnlyFeature =
    String.concat
        "\n"
        [ "Feature: Draft"
          "  @wip"
          "  Scenario: Not ready yet"
          "    Given a step nobody implements"
          "    When something incomplete happens"
          "    Then nothing is asserted"
          "" ]

[<Fact>]
let ``validateBehaviorCoverageForProject drops a feature file whose only scenario is work-in-progress tagged`` () =
    let root = newTempRepo ()
    write root "repo-config.yml" (bddRegistryYaml [ widgetUnitRow "libs/widget/tests/unit/steps/driver.fs" ])
    write root "libs/widget/project.json" """{ "name": "widget", "targets": {} }"""
    write root "specs/widget/behaviors/checkout.feature" (simpleFeature "Checkout" "Checkout succeeds")
    write root "specs/widget/behaviors/draft.feature" wipOnlyFeature
    write root "libs/widget/tests/unit/steps/WidgetSteps.fs" (simpleStepsFs "Widget.Tests.Unit.Steps.WidgetSteps")

    match TestContractProject.validateBehaviorCoverageForProject root "widget" TestContractBdd.AdapterUnit with
    | Ok rendered ->
        // The corpus walk sees both files on disk, but `draft.feature`
        // carries no real (non-@wip) scenario, so it is dropped before the
        // denominator is built rather than counted as a gap: 1/1, not 1/2.
        Assert.Contains("files=1/1", rendered)
        Assert.Contains("scenarios=1/1", rendered)
    | Error(TestContract.ContractFailure message) -> failwith ("must pass, found: " + message)
    | Error(TestContract.Misuse message) -> failwith ("must pass, found misuse: " + message)
