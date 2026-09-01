/// RED contract cases for the `ose-test-contract/v1` registry reader.
///
/// Every case names the contract rule, the offending field, the project, and
/// the old and new values, so a failure reads as a contract violation rather
/// than an opaque assertion. The reader is unimplemented, so all of these
/// fail against the deterministic `NotImplemented` placeholder; none of them
/// may fail by compile error, crash, or unrelated regression.
module RhinoCli.Tests.Unit.Steps.TestContractRegistryUnitTests

open System
open System.IO
open Xunit
open RhinoCli.Cli.Dispatch
open RhinoCli.Application
open RhinoCli.Application.TestContract

// ---------------------------------------------------------------------------
// Expectation helpers
// ---------------------------------------------------------------------------

/// Formats the contract case so a failing assertion states the rule, the
/// field, the project, and the old and new values that triggered it.
let private describe (case: string) (field: string) (project: string) (oldValue: string) (newValue: string) : string =
    sprintf
        "contract case '%s': field '%s' on project '%s' moved from '%s' to '%s'"
        case
        field
        project
        oldValue
        newValue

let private containsOrdinal (fragment: string) (text: string) : bool =
    text.Contains(fragment, StringComparison.Ordinal)

/// Asserts the operation failed the contract (exit 1) with a diagnostic
/// naming `fragment`.
let private expectContractFailure
    (case: string)
    (field: string)
    (project: string)
    (oldValue: string)
    (newValue: string)
    (fragment: string)
    (actual: Result<'a, Failure>)
    : unit =
    let context = describe case field project oldValue newValue

    match actual with
    | Error(ContractFailure message) ->
        Assert.True(
            containsOrdinal fragment message,
            sprintf "%s; expected diagnostic naming '%s' but got '%s'" context fragment message
        )
    | Error other -> Assert.True(false, sprintf "%s; expected a contract failure but got %A" context other)
    | Ok _ -> Assert.True(false, sprintf "%s; expected a contract failure but validation passed" context)

/// Asserts the operation rejected its input as CLI/input misuse (exit 2).
let private expectMisuse (case: string) (fragment: string) (actual: Result<'a, Failure>) : unit =
    match actual with
    | Error(Misuse message) ->
        Assert.True(
            containsOrdinal fragment message,
            sprintf "contract case '%s': expected misuse naming '%s' but got '%s'" case fragment message
        )
    | Error other -> Assert.True(false, sprintf "contract case '%s': expected misuse but got %A" case other)
    | Ok _ -> Assert.True(false, sprintf "contract case '%s': expected misuse but the input was accepted" case)

/// Asserts the operation accepted its input, returning the payload.
let private expectOk (case: string) (actual: Result<'a, Failure>) : 'a =
    match actual with
    | Ok value -> value
    | Error failure ->
        Assert.True(false, sprintf "contract case '%s': expected success but got %A" case failure)
        failwith "unreachable"

// ---------------------------------------------------------------------------
// Registry builders
//
// Fixture values are literal `ose-test-contract/v1` values: `behavior.id` is
// `<owner-project>:<partition>`, every owner is an Nx project name, every
// corpus is a recursive repository-relative glob, and `seed.target` is an Nx
// target while `seed.driver` is a repository-relative file.
// ---------------------------------------------------------------------------

/// The synthetic owner corpus used by the in-memory fixtures below. It is
/// deliberately narrower than the repository's own frozen legacy glob so a
/// fixture case can never be mistaken for a real-file assertion.
let private rhinoCorpus = "specs/apps/rhino/behavior/rhino-cli/gherkin/**"

/// The repository's real frozen `coverage.projects` values for `rhino-cli`,
/// used only by the two cases that parse the tracked `repo-config.yml`.
let private rhinoLegacySpecs = "specs/apps/rhino/behavior/rhino-cli/**"
let private rhinoLegacyLevels = [ "unit"; "integration" ]

/// Walks up from the test assembly's directory to the first ancestor holding
/// a tracked `repo-config.yml`, so the real-file cases do not depend on the
/// runner's working directory.
let private repositoryRoot () : string =
    let rec walk (dir: DirectoryInfo | null) =
        match dir with
        | null -> failwith "repo-config.yml not found above the test assembly directory"
        | dir ->
            if File.Exists(Path.Combine(dir.FullName, "repo-config.yml")) then
                dir.FullName
            else
                walk dir.Parent

    walk (DirectoryInfo(AppContext.BaseDirectory))

let private rhinoUnitDriver =
    "apps/rhino-cli/src/tests/unit/Steps/ContractsSteps.fs"

let private seedDriver =
    "libs/fsharp-env-loader/tests/unit/Behavior/FsharpEnvLoaderBehaviorDriver.fs"

let private adapterEntry
    (disposition: Disposition)
    (project: string option)
    (driver: string option)
    (reason: string option)
    : AdapterEntry =
    { Disposition = disposition
      Project = project
      Driver = driver
      Reason = reason }

let private requiredAdapter (project: string) (driver: string) : AdapterEntry =
    adapterEntry Required (Some project) (Some driver) None

let private delegatedAdapter (project: string) (driver: string) : AdapterEntry =
    adapterEntry Delegated (Some project) (Some driver) None

let private inapplicableAdapter (reason: string) : AdapterEntry =
    adapterEntry Inapplicable None None (Some reason)

let private adapters (unitEntry: AdapterEntry) (integration: AdapterEntry) (e2e: AdapterEntry) : Adapters =
    { Unit = unitEntry
      Integration = integration
      E2e = e2e }

let private standardAdapters (project: string) (driver: string) : Adapters =
    adapters
        (requiredAdapter project driver)
        (inapplicableAdapter "no isolated local-resource boundary")
        (inapplicableAdapter "no user-facing surface")

let private rhinoAdapters: Adapters = standardAdapters "rhino-cli" rhinoUnitDriver

let private activeBehavior (id: string) (owner: string) (corpus: string list) (entries: Adapters) : Behavior =
    { Id = Some id
      LifecycleState = Some Active
      Owner = Some owner
      Corpus = corpus
      Seed = None
      Adapters = entries }

let private bootstrapBehavior (id: string) (owner: string) (seed: Seed option) (entries: Adapters) : Behavior =
    { Id = Some id
      LifecycleState = Some Bootstrap
      Owner = Some owner
      Corpus = []
      Seed = seed
      Adapters = entries }

let private projectRow (project: string) (profile: Profile) (state: MigrationState) (behavior: Behavior) : ProjectRow =
    { Project = project
      Profile = profile
      MigrationState = state
      Behavior = behavior }

let private legacyHalf (present: bool) (corpus: string option) (levels: string list) : LegacyHalf =
    { Present = present
      Corpus = corpus
      Levels = levels }

let private canonicalHalf
    (owner: string option)
    (corpus: string option)
    (runtimes: RuntimeIdentity list)
    : CanonicalHalf =
    { Owner = owner
      Corpus = corpus
      Runtimes = runtimes }

let private mapping
    (project: string)
    (behaviorId: string option)
    (state: MappingState)
    (legacy: LegacyHalf)
    (canonical: CanonicalHalf)
    : CompatibilityMapping =
    { Project = project
      BehaviorId = behaviorId
      State = state
      Legacy = legacy
      Canonical = canonical }

/// The single canonical project used by most single-rule cases: an owner row
/// with a frozen legacy corpus and one resolved unit runtime.
let private rhinoBehavior: Behavior =
    activeBehavior "rhino-cli:default" "rhino-cli" [ rhinoCorpus ] rhinoAdapters

let private rhinoRow: ProjectRow =
    projectRow "rhino-cli" ProfileTool Expanded rhinoBehavior

let private rhinoRuntimes: RuntimeIdentity list =
    [ { Level = "unit"
        Project = "rhino-cli" } ]

let private rhinoMapping: CompatibilityMapping =
    mapping
        "rhino-cli"
        (Some "rhino-cli:default")
        MappingIdentity
        (legacyHalf true (Some rhinoCorpus) [ "unit" ])
        (canonicalHalf (Some "rhino-cli") (Some rhinoCorpus) rhinoRuntimes)

let private legacyProjects: LegacyProject list =
    [ { Name = "rhino-cli"
        Levels = [ "unit" ]
        Specs = rhinoCorpus } ]

let private testingRegistry (projects: ProjectRow list) (mappings: CompatibilityMapping list) : TestingRegistry =
    { Schema = "ose-test-contract/v1"
      Coverage = { MinimumLine = 99 }
      Mappings = mappings
      Projects = projects }

let private registryOf (projects: ProjectRow list) (mappings: CompatibilityMapping list) : Registry =
    { Legacy = legacyProjects
      Testing = Some(testingRegistry projects mappings) }

let private baseRegistry: Registry = registryOf [ rhinoRow ] [ rhinoMapping ]

let private nxProjects: string list = [ "rhino-cli" ]

let private withRow (row: ProjectRow) (registry: Registry) : Registry =
    match registry.Testing with
    | None -> registry
    | Some testing ->
        { registry with
            Testing = Some { testing with Projects = [ row ] } }

let private withMapping (map: CompatibilityMapping) (registry: Registry) : Registry =
    match registry.Testing with
    | None -> registry
    | Some testing ->
        { registry with
            Testing = Some { testing with Mappings = [ map ] } }

let private withBehavior (behavior: Behavior) (registry: Registry) : Registry =
    withRow { rhinoRow with Behavior = behavior } registry

let private withAdapters (entries: Adapters) (registry: Registry) : Registry =
    withBehavior
        { rhinoBehavior with
            Adapters = entries }
        registry

let private withState (state: MigrationState) (registry: Registry) : Registry =
    withRow { rhinoRow with MigrationState = state } registry

let private rhinoSeed: Seed =
    { Target = "test:behavior:seed"
      Driver = seedDriver }

let private unownedAdapters: Adapters =
    adapters
        (inapplicableAdapter "the project owns no behavior")
        (inapplicableAdapter "the project owns no behavior")
        (inapplicableAdapter "the project owns no behavior")

let private stateName (state: MigrationState) : string =
    match state with
    | Expanded -> "expanded"
    | Migrating -> "migrating"
    | Verified -> "verified"
    | Contracted -> "contracted"

let private mappingStateName (state: MappingState) : string =
    match state with
    | MappingIdentity -> "identity"
    | MappingRedirected -> "redirected"
    | MappingVerified -> "verified"

// ---------------------------------------------------------------------------
// Frozen legacy block and canonical root shapes
// ---------------------------------------------------------------------------

[<Fact>]
let ``the frozen legacy coverage projects block keeps its literal name levels and specs fields`` () =
    let registry = expectOk "legacy-block-shape" (parseRegistry (repositoryRoot ()))

    let row =
        registry.Legacy |> List.find (fun candidate -> candidate.Name = "rhino-cli")

    Assert.Equal<string list>(rhinoLegacyLevels, row.Levels)
    Assert.Equal(rhinoLegacySpecs, row.Specs)

[<Fact>]
let ``the canonical testing root carries schema coverage compatibility mappings and projects`` () =
    let registry = expectOk "canonical-root-shape" (parseRegistry (repositoryRoot ()))
    let testing = Option.get registry.Testing
    Assert.Equal("ose-test-contract/v1", testing.Schema)
    Assert.Equal(99, testing.Coverage.MinimumLine)
    Assert.NotEmpty(testing.Mappings)
    Assert.NotEmpty(testing.Projects)

[<Fact>]
let ``a canonical root declaring an unknown schema is rejected`` () =
    let registry =
        match baseRegistry.Testing with
        | None -> baseRegistry
        | Some testing ->
            { baseRegistry with
                Testing =
                    Some
                        { testing with
                            Schema = "ose-test-contract/v2" } }

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "schema-version"
        "testing.schema"
        "rhino-cli"
        "ose-test-contract/v1"
        "ose-test-contract/v2"
        "testing.schema"

[<Fact>]
let ``a coverage floor other than the single repository minimum is rejected`` () =
    let registry =
        match baseRegistry.Testing with
        | None -> baseRegistry
        | Some testing ->
            { baseRegistry with
                Testing =
                    Some
                        { testing with
                            Coverage = { MinimumLine = 80 } } }

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure "coverage-floor" "testing.coverage.minimum-line" "rhino-cli" "99" "80" "minimum-line"

// ---------------------------------------------------------------------------
// Profiles
// ---------------------------------------------------------------------------

[<Fact>]
let ``profile application is an accepted project profile`` () =
    let registry =
        withRow
            { rhinoRow with
                Profile = ProfileApplication }
            baseRegistry

    let report =
        expectOk "profile-application" (validate registry nxProjects defaultValidateOptions)

    Assert.Equal(1, report.Projects)

[<Fact>]
let ``profile library is an accepted project profile`` () =
    let registry =
        withRow
            { rhinoRow with
                Profile = ProfileLibrary }
            baseRegistry

    let report =
        expectOk "profile-library" (validate registry nxProjects defaultValidateOptions)

    Assert.Equal(1, report.Projects)

[<Fact>]
let ``profile tool is an accepted project profile`` () =
    let registry = withRow { rhinoRow with Profile = ProfileTool } baseRegistry

    let report =
        expectOk "profile-tool" (validate registry nxProjects defaultValidateOptions)

    Assert.Equal(1, report.Projects)

[<Fact>]
let ``profile e2e is an accepted project profile`` () =
    let registry = withRow { rhinoRow with Profile = ProfileE2e } baseRegistry

    let report =
        expectOk "profile-e2e" (validate registry nxProjects defaultValidateOptions)

    Assert.Equal(1, report.Projects)

// ---------------------------------------------------------------------------
// Adapter keys, dispositions, and conditional fields
// ---------------------------------------------------------------------------

[<Fact>]
let ``a required adapter carries both a project and a driver`` () =
    expectOk "adapter-required-complete" (validate baseRegistry nxProjects defaultValidateOptions)
    |> ignore

[<Fact>]
let ``a delegated adapter carries both a project and a driver`` () =
    let owner =
        projectRow
            "ose-app-web"
            ProfileApplication
            Expanded
            (activeBehavior
                "ose-app-web:default"
                "ose-app-web"
                [ "specs/apps/ose/behavior/app-web/**" ]
                (adapters
                    (requiredAdapter "ose-app-web" "apps/ose-app-web/src/testing/bdd/unit-driver.ts")
                    (inapplicableAdapter "no isolated local-resource boundary")
                    (delegatedAdapter "ose-app-web-e2e" "apps/ose-app-web-e2e/src/bdd/e2e-driver.ts")))

    let delegateRow =
        projectRow
            "ose-app-web-e2e"
            ProfileE2e
            Expanded
            (activeBehavior
                "ose-app-web:default"
                "ose-app-web"
                []
                (adapters
                    (inapplicableAdapter "the owner hosts the unit adapter")
                    (inapplicableAdapter "no isolated local-resource boundary")
                    (requiredAdapter "ose-app-web-e2e" "apps/ose-app-web-e2e/src/bdd/e2e-driver.ts")))

    let registry =
        registryOf
            [ owner; delegateRow ]
            [ mapping
                  "ose-app-web"
                  (Some "ose-app-web:default")
                  MappingIdentity
                  (legacyHalf true (Some "specs/apps/ose/behavior/app-web/**") [ "unit" ])
                  (canonicalHalf
                      (Some "ose-app-web")
                      (Some "specs/apps/ose/behavior/app-web/**")
                      [ { Level = "e2e"
                          Project = "ose-app-web-e2e" }
                        { Level = "unit"
                          Project = "ose-app-web" } ])
              mapping
                  "ose-app-web-e2e"
                  (Some "ose-app-web:default")
                  MappingIdentity
                  (legacyHalf false None [])
                  (canonicalHalf (Some "ose-app-web") None []) ]

    expectOk
        "adapter-delegated-complete"
        (validate registry [ "ose-app-web"; "ose-app-web-e2e" ] defaultValidateOptions)
    |> ignore

[<Fact>]
let ``an inapplicable adapter carries a reason instead of a project and driver`` () =
    let registry =
        withAdapters
            (adapters
                (requiredAdapter "rhino-cli" rhinoUnitDriver)
                (inapplicableAdapter "no isolated local-resource boundary")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    expectOk "adapter-inapplicable-complete" (validate registry nxProjects defaultValidateOptions)
    |> ignore

[<Fact>]
let ``a required unit adapter without a driver is rejected`` () =
    let registry =
        withAdapters
            (adapters
                (adapterEntry Required (Some "rhino-cli") None None)
                (inapplicableAdapter "no isolated local-resource boundary")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-conditional-fields"
        "behavior.adapters.unit.driver"
        "rhino-cli"
        rhinoUnitDriver
        "<absent>"
        "behavior.adapters.unit.driver"

[<Fact>]
let ``a required unit adapter without a project is rejected`` () =
    let registry =
        withAdapters
            (adapters
                (adapterEntry Required None (Some rhinoUnitDriver) None)
                (inapplicableAdapter "no isolated local-resource boundary")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-conditional-fields"
        "behavior.adapters.unit.project"
        "rhino-cli"
        "rhino-cli"
        "<absent>"
        "behavior.adapters.unit.project"

[<Fact>]
let ``a required unit adapter naming a different project is rejected`` () =
    let registry =
        withAdapters
            (adapters
                (requiredAdapter "ose-be" rhinoUnitDriver)
                (inapplicableAdapter "no isolated local-resource boundary")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-required-is-self"
        "behavior.adapters.unit.project"
        "rhino-cli"
        "rhino-cli"
        "ose-be"
        "behavior.adapters.unit.project"

[<Fact>]
let ``a delegated integration adapter without a driver is rejected against the integration key`` () =
    let registry =
        withAdapters
            (adapters
                (requiredAdapter "rhino-cli" rhinoUnitDriver)
                (adapterEntry Delegated (Some "ose-be") None None)
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-conditional-fields"
        "behavior.adapters.integration.driver"
        "rhino-cli"
        rhinoUnitDriver
        "<absent>"
        "behavior.adapters.integration.driver"

[<Fact>]
let ``an inapplicable e2e adapter carrying a project is rejected against the e2e key`` () =
    let registry =
        withAdapters
            (adapters
                (requiredAdapter "rhino-cli" rhinoUnitDriver)
                (inapplicableAdapter "no isolated local-resource boundary")
                (adapterEntry Inapplicable (Some "rhino-cli") None (Some "no user-facing surface")))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-conditional-fields"
        "behavior.adapters.e2e.project"
        "rhino-cli"
        "<absent>"
        "rhino-cli"
        "behavior.adapters.e2e.project"

[<Fact>]
let ``an inapplicable adapter with a blank reason is rejected`` () =
    let registry =
        withAdapters
            (adapters
                (requiredAdapter "rhino-cli" rhinoUnitDriver)
                (inapplicableAdapter "   ")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-conditional-fields"
        "behavior.adapters.integration.reason"
        "rhino-cli"
        "no isolated local-resource boundary"
        "<blank>"
        "behavior.adapters.integration.reason"

[<Fact>]
let ``a required adapter carrying a reason is rejected`` () =
    let registry =
        withAdapters
            (adapters
                (adapterEntry Required (Some "rhino-cli") (Some rhinoUnitDriver) (Some "not needed"))
                (inapplicableAdapter "no isolated local-resource boundary")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "adapter-conditional-fields"
        "behavior.adapters.unit.reason"
        "rhino-cli"
        "<absent>"
        "not needed"
        "behavior.adapters.unit.reason"

// ---------------------------------------------------------------------------
// Reciprocal delegation
// ---------------------------------------------------------------------------

[<Fact>]
let ``two projects delegating their integration adapter to each other are rejected`` () =
    let left =
        projectRow
            "ose-be"
            ProfileApplication
            Expanded
            (activeBehavior
                "ose-be:default"
                "ose-be"
                [ "specs/apps/ose/behavior/be/**" ]
                (adapters
                    (requiredAdapter "ose-be" "apps/ose-be/src/tests/unit/Steps/BeSteps.fs")
                    (delegatedAdapter "ose-app-web" "apps/ose-app-web/src/testing/bdd/unit-driver.ts")
                    (inapplicableAdapter "no user-facing surface")))

    let right =
        projectRow
            "ose-app-web"
            ProfileApplication
            Expanded
            (activeBehavior
                "ose-app-web:default"
                "ose-app-web"
                [ "specs/apps/ose/behavior/app-web/**" ]
                (adapters
                    (requiredAdapter "ose-app-web" "apps/ose-app-web/src/testing/bdd/unit-driver.ts")
                    (delegatedAdapter "ose-be" "apps/ose-be/src/tests/unit/Steps/BeSteps.fs")
                    (inapplicableAdapter "no user-facing surface")))

    let registry =
        registryOf
            [ left; right ]
            [ mapping
                  "ose-be"
                  (Some "ose-be:default")
                  MappingIdentity
                  (legacyHalf true (Some "specs/apps/ose/behavior/be/**") [ "unit" ])
                  (canonicalHalf (Some "ose-be") (Some "specs/apps/ose/behavior/be/**") [])
              mapping
                  "ose-app-web"
                  (Some "ose-app-web:default")
                  MappingIdentity
                  (legacyHalf true (Some "specs/apps/ose/behavior/app-web/**") [ "unit" ])
                  (canonicalHalf (Some "ose-app-web") (Some "specs/apps/ose/behavior/app-web/**") []) ]

    validate registry [ "ose-be"; "ose-app-web" ] defaultValidateOptions
    |> expectContractFailure
        "reciprocal-delegation"
        "behavior.adapters.integration.project"
        "ose-be"
        "ose-app-web"
        "ose-be"
        "reciprocal"

[<Fact>]
let ``delegating to a project that does not host the adapter is rejected`` () =
    let registry =
        withAdapters
            (adapters
                (requiredAdapter "rhino-cli" rhinoUnitDriver)
                (delegatedAdapter "not-a-project" rhinoUnitDriver)
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "delegation-target"
        "behavior.adapters.integration.project"
        "rhino-cli"
        "rhino-cli"
        "not-a-project"
        "behavior.adapters.integration.project"

// ---------------------------------------------------------------------------
// Migration states and their transitions
// ---------------------------------------------------------------------------

[<Fact>]
let ``migration state expanded is an accepted project state`` () =
    expectOk "migration-state-expanded" (validate (withState Expanded baseRegistry) nxProjects defaultValidateOptions)
    |> ignore

[<Fact>]
let ``migration state migrating is an accepted project state`` () =
    expectOk "migration-state-migrating" (validate (withState Migrating baseRegistry) nxProjects defaultValidateOptions)
    |> ignore

[<Fact>]
let ``migration state verified is an accepted project state`` () =
    expectOk "migration-state-verified" (validate (withState Verified baseRegistry) nxProjects defaultValidateOptions)
    |> ignore

[<Fact>]
let ``migration state contracted is an accepted project state`` () =
    expectOk
        "migration-state-contracted"
        (validate (withState Contracted baseRegistry) nxProjects defaultValidateOptions)
    |> ignore

let private expectAllowedMigration (before: MigrationState) (after: MigrationState) : unit =
    let case =
        sprintf "migration-transition-%s-to-%s" (stateName before) (stateName after)

    validateTransition (withState before baseRegistry) (withState after baseRegistry)
    |> expectOk case
    |> ignore

let private expectRejectedMigration (before: MigrationState) (after: MigrationState) (fragment: string) : unit =
    let case =
        sprintf "migration-transition-%s-to-%s" (stateName before) (stateName after)

    validateTransition (withState before baseRegistry) (withState after baseRegistry)
    |> expectContractFailure
        case
        "testing.projects[].migration-state"
        "rhino-cli"
        (stateName before)
        (stateName after)
        fragment

[<Fact>]
let ``the expanded to migrating transition is allowed`` () =
    expectAllowedMigration Expanded Migrating

[<Fact>]
let ``the migrating to verified transition is allowed`` () =
    expectAllowedMigration Migrating Verified

[<Fact>]
let ``the verified to contracted transition is allowed`` () =
    expectAllowedMigration Verified Contracted

[<Fact>]
let ``the expanded to verified transition is rejected as a skipped state`` () =
    expectRejectedMigration Expanded Verified "skipped"

[<Fact>]
let ``the expanded to contracted transition is rejected as a skipped state`` () =
    expectRejectedMigration Expanded Contracted "skipped"

[<Fact>]
let ``the migrating to contracted transition is rejected as a skipped state`` () =
    expectRejectedMigration Migrating Contracted "skipped"

[<Fact>]
let ``the migrating to expanded transition is rejected as a reversed state`` () =
    expectRejectedMigration Migrating Expanded "reversed"

[<Fact>]
let ``the verified to migrating transition is rejected as a reversed state`` () =
    expectRejectedMigration Verified Migrating "reversed"

[<Fact>]
let ``the contracted to verified transition is rejected as a reversed state`` () =
    expectRejectedMigration Contracted Verified "reversed"

// ---------------------------------------------------------------------------
// Compatibility mapping states and their transitions
// ---------------------------------------------------------------------------

let private withMappingState (state: MappingState) (registry: Registry) : Registry =
    withMapping { rhinoMapping with State = state } registry

let private expectAllowedMappingMove (before: MappingState) (after: MappingState) : unit =
    let case =
        sprintf "mapping-transition-%s-to-%s" (mappingStateName before) (mappingStateName after)

    validateTransition (withMappingState before baseRegistry) (withMappingState after baseRegistry)
    |> expectOk case
    |> ignore

let private expectRejectedMappingMove (before: MappingState) (after: MappingState) : unit =
    let case =
        sprintf "mapping-transition-%s-to-%s" (mappingStateName before) (mappingStateName after)

    validateTransition (withMappingState before baseRegistry) (withMappingState after baseRegistry)
    |> expectContractFailure
        case
        "testing.compatibility.mappings[].state"
        "rhino-cli"
        (mappingStateName before)
        (mappingStateName after)
        "reversed"

[<Fact>]
let ``the identity to redirected mapping transition is allowed`` () =
    expectAllowedMappingMove MappingIdentity MappingRedirected

[<Fact>]
let ``the redirected to verified mapping transition is allowed`` () =
    expectAllowedMappingMove MappingRedirected MappingVerified

[<Fact>]
let ``the identity to verified mapping transition is allowed`` () =
    expectAllowedMappingMove MappingIdentity MappingVerified

[<Fact>]
let ``the redirected to identity mapping transition is rejected as reversed`` () =
    expectRejectedMappingMove MappingRedirected MappingIdentity

[<Fact>]
let ``the verified to redirected mapping transition is rejected as reversed`` () =
    expectRejectedMappingMove MappingVerified MappingRedirected

[<Fact>]
let ``the verified to identity mapping transition is rejected as reversed`` () =
    expectRejectedMappingMove MappingVerified MappingIdentity

// ---------------------------------------------------------------------------
// Immutable legacy half
// ---------------------------------------------------------------------------

[<Fact>]
let ``mutating a frozen legacy corpus is rejected`` () =
    let mutated = "specs/apps/rhino/behavior/**"

    let after =
        withMapping
            { rhinoMapping with
                Legacy = legacyHalf true (Some mutated) [ "unit" ] }
            baseRegistry

    validateTransition baseRegistry after
    |> expectContractFailure
        "immutable-legacy-half"
        "testing.compatibility.mappings[].legacy.corpus"
        "rhino-cli"
        rhinoCorpus
        mutated
        "legacy.corpus"

[<Fact>]
let ``mutating a frozen legacy levels list is rejected`` () =
    let after =
        withMapping
            { rhinoMapping with
                Legacy = legacyHalf true (Some rhinoCorpus) [ "unit"; "integration" ] }
            baseRegistry

    validateTransition baseRegistry after
    |> expectContractFailure
        "immutable-legacy-half"
        "testing.compatibility.mappings[].legacy.levels"
        "rhino-cli"
        "unit"
        "unit,integration"
        "legacy.levels"

[<Fact>]
let ``mutating a frozen legacy present flag is rejected`` () =
    let after =
        withMapping
            { rhinoMapping with
                Legacy = legacyHalf false (Some rhinoCorpus) [ "unit" ] }
            baseRegistry

    validateTransition baseRegistry after
    |> expectContractFailure
        "immutable-legacy-half"
        "testing.compatibility.mappings[].legacy.present"
        "rhino-cli"
        "true"
        "false"
        "legacy.present"

[<Fact>]
let ``a project legacy omitted maps with present false a null corpus and no levels`` () =
    let absent =
        mapping
            "fsharp-env-loader"
            (Some "fsharp-env-loader:default")
            MappingIdentity
            (legacyHalf false None [])
            (canonicalHalf (Some "fsharp-env-loader") None [])

    let row =
        projectRow
            "fsharp-env-loader"
            ProfileLibrary
            Expanded
            (bootstrapBehavior
                "fsharp-env-loader:default"
                "fsharp-env-loader"
                (Some rhinoSeed)
                (standardAdapters "fsharp-env-loader" seedDriver))

    let registry = registryOf [ row ] [ absent ]

    let report =
        expectOk "legacy-absent-project" (validateMapping registry [ "fsharp-env-loader" ] None)

    Assert.Equal(1, report.Mappings)

// ---------------------------------------------------------------------------
// Behavior identity stability
// ---------------------------------------------------------------------------

[<Fact>]
let ``two projects declaring the same behavior id are rejected as duplicates`` () =
    let other =
        projectRow
            "ose-be"
            ProfileApplication
            Expanded
            (activeBehavior
                "rhino-cli:default"
                "ose-be"
                [ "specs/apps/ose/behavior/be/**" ]
                (standardAdapters "ose-be" "apps/ose-be/src/tests/unit/Steps/BeSteps.fs"))

    let registry =
        registryOf
            [ rhinoRow; other ]
            [ rhinoMapping
              mapping
                  "ose-be"
                  (Some "rhino-cli:default")
                  MappingIdentity
                  (legacyHalf true (Some "specs/apps/ose/behavior/be/**") [ "unit" ])
                  (canonicalHalf (Some "ose-be") (Some "specs/apps/ose/behavior/be/**") []) ]

    validate registry [ "rhino-cli"; "ose-be" ] defaultValidateOptions
    |> expectContractFailure
        "duplicate-behavior-id"
        "behavior.id"
        "ose-be"
        "ose-be:default"
        "rhino-cli:default"
        "duplicate behavior id"

[<Fact>]
let ``a behavior id that does not name its owning project is rejected`` () =
    let registry =
        withBehavior
            { rhinoBehavior with
                Id = Some "ose-be:default" }
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "behavior-id-names-owner"
        "behavior.id"
        "rhino-cli"
        "rhino-cli:default"
        "ose-be:default"
        "behavior.id"

[<Fact>]
let ``changing a behavior id across a revision is rejected as an unstable identity`` () =
    let after =
        withBehavior
            { rhinoBehavior with
                Id = Some "rhino-cli:core" }
            baseRegistry

    validateTransition baseRegistry after
    |> expectContractFailure
        "stable-behavior-id"
        "behavior.id"
        "rhino-cli"
        "rhino-cli:default"
        "rhino-cli:core"
        "behavior.id"

// ---------------------------------------------------------------------------
// Raw paths versus normalized runtime identity
// ---------------------------------------------------------------------------

[<Fact>]
let ``a canonical raw corpus path change that preserves the normalized identity is allowed`` () =
    let moved = "specs/apps/rhino-cli/behavior/**"

    let after =
        withMapping
            { rhinoMapping with
                State = MappingRedirected
                Canonical = canonicalHalf (Some "rhino-cli") (Some moved) rhinoRuntimes }
            (withBehavior
                { rhinoBehavior with
                    Corpus = [ moved ] }
                baseRegistry)

    validateTransition baseRegistry after
    |> expectOk "raw-path-change-stable-identity"
    |> ignore

[<Fact>]
let ``a legacy raw specs path rendering change that preserves the normalized identity is allowed`` () =
    let after =
        { baseRegistry with
            Legacy =
                [ { Name = "rhino-cli"
                    Levels = [ "unit" ]
                    Specs = "./specs/apps/rhino/behavior/rhino-cli/gherkin/**" } ] }

    validateTransition baseRegistry after
    |> expectOk "legacy-raw-path-change-stable-identity"
    |> ignore

[<Fact>]
let ``losing a normalized runtime identity is rejected`` () =
    let after =
        withMapping
            { rhinoMapping with
                Canonical = canonicalHalf (Some "rhino-cli") (Some rhinoCorpus) [] }
            baseRegistry

    validateTransition baseRegistry after
    |> expectContractFailure
        "normalized-identity-loss"
        "testing.compatibility.mappings[].canonical.runtimes"
        "rhino-cli"
        "unit@rhino-cli"
        "<empty>"
        "unit@rhino-cli"

[<Fact>]
let ``an absolute corpus path is rejected`` () =
    let absolute = "/specs/apps/rhino/behavior/rhino-cli/gherkin/**"

    let registry =
        withBehavior
            { rhinoBehavior with
                Corpus = [ absolute ] }
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure "repository-relative-paths" "behavior.corpus" "rhino-cli" rhinoCorpus absolute "absolute"

[<Fact>]
let ``a traversal corpus path is rejected`` () =
    let traversal = "specs/apps/rhino/../../../etc/gherkin/**"

    let registry =
        withBehavior
            { rhinoBehavior with
                Corpus = [ traversal ] }
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure "repository-relative-paths" "behavior.corpus" "rhino-cli" rhinoCorpus traversal "traversal"

[<Fact>]
let ``an empty corpus glob entry is rejected`` () =
    let registry = withBehavior { rhinoBehavior with Corpus = [ "" ] } baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "repository-relative-paths"
        "behavior.corpus"
        "rhino-cli"
        rhinoCorpus
        "<blank>"
        "behavior.corpus"

[<Fact>]
let ``an absolute seed driver is rejected`` () =
    let absolute =
        "/libs/fsharp-env-loader/tests/unit/Behavior/FsharpEnvLoaderBehaviorDriver.fs"

    let registry =
        withBehavior
            (bootstrapBehavior
                "rhino-cli:default"
                "rhino-cli"
                (Some
                    { Target = "test:behavior:seed"
                      Driver = absolute })
                rhinoAdapters)
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "repository-relative-paths"
        "behavior.seed.driver"
        "rhino-cli"
        seedDriver
        absolute
        "absolute"

[<Fact>]
let ``a traversal adapter driver is rejected`` () =
    let traversal = "apps/rhino-cli/../../etc/unit-driver.fs"

    let registry =
        withAdapters
            (adapters
                (requiredAdapter "rhino-cli" traversal)
                (inapplicableAdapter "no isolated local-resource boundary")
                (inapplicableAdapter "no user-facing surface"))
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "repository-relative-paths"
        "behavior.adapters.unit.driver"
        "rhino-cli"
        rhinoUnitDriver
        traversal
        "traversal"

// ---------------------------------------------------------------------------
// Nx project bijection
// ---------------------------------------------------------------------------

[<Fact>]
let ``an nx project absent from the testing projects is rejected`` () =
    validate baseRegistry [ "rhino-cli"; "ose-be" ] defaultValidateOptions
    |> expectContractFailure
        "project-bijection"
        "testing.projects[].project"
        "ose-be"
        "<declared in nx>"
        "<absent from testing.projects>"
        "ose-be"

[<Fact>]
let ``a testing project absent from the nx project list is rejected`` () =
    validate baseRegistry [] defaultValidateOptions
    |> expectContractFailure
        "project-bijection"
        "testing.projects[].project"
        "rhino-cli"
        "<absent from nx>"
        "rhino-cli"
        "rhino-cli"

[<Fact>]
let ``a duplicate testing project row is rejected`` () =
    let registry = registryOf [ rhinoRow; rhinoRow ] [ rhinoMapping ]

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure "duplicate-project-row" "testing.projects[].project" "rhino-cli" "1" "2" "duplicate"

[<Fact>]
let ``a compatibility mapping missing for an nx project is rejected`` () =
    let registry = registryOf [ rhinoRow ] []

    validateMapping registry nxProjects None
    |> expectContractFailure
        "mapping-bijection"
        "testing.compatibility.mappings[].project"
        "rhino-cli"
        "rhino-cli"
        "<absent>"
        "rhino-cli"

[<Fact>]
let ``a duplicate compatibility mapping for one project is rejected`` () =
    let registry = registryOf [ rhinoRow ] [ rhinoMapping; rhinoMapping ]

    validateMapping registry nxProjects None
    |> expectContractFailure
        "duplicate-mapping"
        "testing.compatibility.mappings[].project"
        "rhino-cli"
        "1"
        "2"
        "duplicate"

[<Fact>]
let ``a compatibility mapping for an unknown nx project is rejected`` () =
    let stray =
        mapping
            "not-a-project"
            (Some "not-a-project:default")
            MappingIdentity
            (legacyHalf false None [])
            (canonicalHalf None None [])

    let registry = registryOf [ rhinoRow ] [ rhinoMapping; stray ]

    validateMapping registry nxProjects None
    |> expectContractFailure
        "mapping-bijection"
        "testing.compatibility.mappings[].project"
        "not-a-project"
        "<absent from nx>"
        "not-a-project"
        "not-a-project"

// ---------------------------------------------------------------------------
// Behavior lifecycle
// ---------------------------------------------------------------------------

[<Fact>]
let ``a bootstrap owner without a seed is rejected`` () =
    let registry =
        withBehavior (bootstrapBehavior "rhino-cli:default" "rhino-cli" None rhinoAdapters) baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "bootstrap-requires-seed"
        "behavior.seed"
        "rhino-cli"
        "test:behavior:seed"
        "<absent>"
        "behavior.seed"

[<Fact>]
let ``a bootstrap owner carrying a corpus is rejected`` () =
    let seeded =
        bootstrapBehavior "rhino-cli:default" "rhino-cli" (Some rhinoSeed) rhinoAdapters

    let registry = withBehavior { seeded with Corpus = [ rhinoCorpus ] } baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "bootstrap-forbids-corpus"
        "behavior.corpus"
        "rhino-cli"
        "<empty>"
        rhinoCorpus
        "behavior.corpus"

[<Fact>]
let ``an active owner with an empty resolved corpus is rejected`` () =
    let registry = withBehavior { rhinoBehavior with Corpus = [] } baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "active-requires-corpus"
        "behavior.corpus"
        "rhino-cli"
        rhinoCorpus
        "<empty>"
        "behavior.corpus"

[<Fact>]
let ``an active owner carrying a seed is rejected`` () =
    let registry =
        withBehavior
            { rhinoBehavior with
                Seed = Some rhinoSeed }
            baseRegistry

    validate registry nxProjects defaultValidateOptions
    |> expectContractFailure
        "active-forbids-seed"
        "behavior.seed"
        "rhino-cli"
        "<absent>"
        "test:behavior:seed"
        "behavior.seed"

[<Fact>]
let ``the bootstrap to active lifecycle transition is allowed`` () =
    let before =
        withBehavior (bootstrapBehavior "rhino-cli:default" "rhino-cli" (Some rhinoSeed) rhinoAdapters) baseRegistry

    validateTransition before baseRegistry
    |> expectOk "lifecycle-bootstrap-to-active"
    |> ignore

[<Fact>]
let ``the active to bootstrap lifecycle transition is rejected as reversed`` () =
    let after =
        withBehavior (bootstrapBehavior "rhino-cli:default" "rhino-cli" (Some rhinoSeed) rhinoAdapters) baseRegistry

    validateTransition baseRegistry after
    |> expectContractFailure
        "lifecycle-active-to-bootstrap"
        "behavior.lifecycle-state"
        "rhino-cli"
        "active"
        "bootstrap"
        "reversed"

[<Fact>]
let ``a project with a null owner declares neither a behavior id nor a lifecycle state`` () =
    let unowned =
        { Id = None
          LifecycleState = None
          Owner = None
          Corpus = []
          Seed = None
          Adapters = unownedAdapters }

    let registry =
        withMapping
            { rhinoMapping with
                BehaviorId = None
                Canonical = canonicalHalf None None [] }
            (withBehavior unowned baseRegistry)

    expectOk "unowned-project" (validate registry nxProjects defaultValidateOptions)
    |> ignore

[<Fact>]
let ``a project with a null owner that still declares a behavior id is rejected`` () =
    let unowned =
        { Id = Some "rhino-cli:default"
          LifecycleState = None
          Owner = None
          Corpus = []
          Seed = None
          Adapters = unownedAdapters }

    validate (withBehavior unowned baseRegistry) nxProjects defaultValidateOptions
    |> expectContractFailure
        "unowned-forbids-identity"
        "behavior.id"
        "rhino-cli"
        "<absent>"
        "rhino-cli:default"
        "behavior.id"

[<Fact>]
let ``a project with a null owner declaring a required adapter is rejected`` () =
    let unowned =
        { Id = None
          LifecycleState = None
          Owner = None
          Corpus = []
          Seed = None
          Adapters = rhinoAdapters }

    validate (withBehavior unowned baseRegistry) nxProjects defaultValidateOptions
    |> expectContractFailure
        "unowned-forbids-adapters"
        "behavior.adapters.unit.disposition"
        "rhino-cli"
        "inapplicable"
        "required"
        "behavior.adapters.unit"

// ---------------------------------------------------------------------------
// require-state gating
// ---------------------------------------------------------------------------

[<Fact>]
let ``registry validate require-state expanded passes on a fully expanded registry`` () =
    let options =
        { defaultValidateOptions with
            RequireState = Some Expanded }

    let report =
        expectOk "require-state-expanded" (validate baseRegistry nxProjects options)

    Assert.Equal("expanded", report.State)
    Assert.Equal(1, report.Projects)
    Assert.Equal(0, report.BootstrapCount)
    Assert.Equal(1, report.ActiveCount)
    Assert.True(report.LegacyPresent)
    Assert.True(report.CompatibilityPresent)

[<Fact>]
let ``registry validate require-state expanded names the project that is off state`` () =
    let options =
        { defaultValidateOptions with
            RequireState = Some Expanded }

    validate (withState Migrating baseRegistry) nxProjects options
    |> expectContractFailure
        "require-state"
        "testing.projects[].migration-state"
        "rhino-cli"
        "expanded"
        "migrating"
        "rhino-cli"

[<Fact>]
let ``registry validate allow-bootstrap admits only the listed bootstrap project`` () =
    let options =
        { defaultValidateOptions with
            RequireState = Some Expanded
            AllowBootstrap = [ "fsharp-env-loader" ] }

    let registry =
        withBehavior (bootstrapBehavior "rhino-cli:default" "rhino-cli" (Some rhinoSeed) rhinoAdapters) baseRegistry

    validate registry nxProjects options
    |> expectContractFailure "allow-bootstrap" "behavior.lifecycle-state" "rhino-cli" "active" "bootstrap" "rhino-cli"

[<Fact>]
let ``registry validate forbid-legacy rejects a surviving frozen legacy block`` () =
    let options =
        { defaultValidateOptions with
            RequireState = Some Contracted
            ForbidLegacy = true
            ForbidCompatibility = true }

    validate (withState Contracted baseRegistry) nxProjects options
    |> expectContractFailure "forbid-legacy" "coverage.projects" "rhino-cli" "present" "absent" "coverage.projects"

[<Fact>]
let ``registry validate-mapping all reports the mapping count when every mapping is legal`` () =
    let report =
        expectOk "validate-mapping-all" (validateMapping baseRegistry nxProjects None)

    Assert.Equal("identity", report.State)
    Assert.Equal(1, report.Mappings)

[<Fact>]
let ``registry validate-mapping require-state verified rejects an identity mapping`` () =
    validateMapping baseRegistry nxProjects (Some MappingVerified)
    |> expectContractFailure
        "require-mapping-state"
        "testing.compatibility.mappings[].state"
        "rhino-cli"
        "verified"
        "identity"
        "rhino-cli"

// ---------------------------------------------------------------------------
// Snapshots and comparison
// ---------------------------------------------------------------------------

[<Fact>]
let ``the legacy snapshot renders sorted tab separated rows`` () =
    let rows = expectOk "legacy-snapshot" (snapshot baseRegistry SourceLegacy None)
    let rendered = rows |> List.map renderRow

    Assert.Equal<string list>([ "rhino-cli\trhino-cli\trhino-cli:default\tunit@rhino-cli" ], rendered)

[<Fact>]
let ``the canonical snapshot reproduces exactly the supplied project list`` () =
    let rows =
        expectOk "canonical-snapshot" (snapshot baseRegistry SourceCanonical (Some [ "rhino-cli" ]))

    Assert.Equal<string list>([ "rhino-cli" ], rows |> List.map (fun row -> row.Project))

[<Fact>]
let ``a legacy absent project renders sentinel dashes in the canonical snapshot`` () =
    let rows =
        expectOk
            "canonical-snapshot-legacy-absent"
            (snapshot baseRegistry SourceCanonical (Some [ "rhino-cli"; "web-ui-token" ]))

    let sentinel = rows |> List.tryFind (fun row -> row.Project = "web-ui-token")

    match sentinel with
    | None -> Assert.True(false, "contract case 'legacy-absent-sentinel': no row rendered for 'web-ui-token'")
    | Some row -> Assert.Equal("web-ui-token\t-\t-\t-", renderRow row)

[<Fact>]
let ``comparing byte equal snapshots reports the compared row count`` () =
    let rows =
        [ { Project = "rhino-cli"
            CanonicalOwner = "rhino-cli"
            BehaviorId = "rhino-cli:default"
            RuntimeIdentities = "unit@rhino-cli" } ]

    Assert.Equal(1, expectOk "compare-equal" (compareSnapshots rows rows))

[<Fact>]
let ``comparing divergent snapshots names the first differing project and both values`` () =
    let legacy =
        [ { Project = "rhino-cli"
            CanonicalOwner = "rhino-cli"
            BehaviorId = "rhino-cli:default"
            RuntimeIdentities = "unit@rhino-cli" } ]

    let canonical =
        [ { Project = "rhino-cli"
            CanonicalOwner = "rhino-cli-tools"
            BehaviorId = "rhino-cli:default"
            RuntimeIdentities = "unit@rhino-cli" } ]

    compareSnapshots legacy canonical
    |> expectContractFailure
        "snapshot-divergence"
        "canonical-owner"
        "rhino-cli"
        "rhino-cli"
        "rhino-cli-tools"
        "rhino-cli"

[<Fact>]
let ``a canonical snapshot without a project list is rejected as misuse`` () =
    snapshot baseRegistry SourceCanonical None
    |> expectMisuse "snapshot-requires-project-list" "--project-list-from"

[<Fact>]
let ``a legacy snapshot given a project list is rejected as misuse`` () =
    snapshot baseRegistry SourceLegacy (Some [ "rhino-cli" ])
    |> expectMisuse "legacy-snapshot-refuses-project-list" "--project-list-from"

// ---------------------------------------------------------------------------
// Tracked-byte immutability
// ---------------------------------------------------------------------------

[<Fact>]
let ``the registry reader mutates no tracked byte`` () =
    let digest = "aa5c4d03745fb13de774871b96eebe26052d5b97cd5c137c19ce16332bf5fb2a"

    validateNoTrackedMutation digest digest
    |> expectOk "tracked-byte-immutability"
    |> ignore

[<Fact>]
let ``a tracked byte mutation during a read is rejected`` () =
    let before = "aa5c4d03745fb13de774871b96eebe26052d5b97cd5c137c19ce16332bf5fb2a"
    let after = "0000000000000000000000000000000000000000000000000000000000000000"

    validateNoTrackedMutation before after
    |> expectContractFailure "tracked-byte-mutation" "repo-config.yml" "rhino-cli" before after "repo-config.yml"

// ---------------------------------------------------------------------------
// Owner fixture resolution
// ---------------------------------------------------------------------------

/// A throwaway directory standing in for a repository root.
let private newTempDir () : string =
    let dir =
        Path.Combine(Path.GetTempPath(), "rhino-cli-test-contract-" + Guid.NewGuid().ToString("N"))

    Directory.CreateDirectory(dir) |> ignore
    dir

/// Writes `body` at the contracted owner-fixture location below a throwaway
/// root and returns the repository-relative path the loader is given. The
/// four real owner fixtures are authored by the later owner-fixture leaves,
/// so the resolution cases here supply their own document rather than
/// depending on files this delivery does not own.
let private seedFixture (root: string) (owner: string) (fileName: string) (body: string) : string =
    let relative =
        String.concat "/" [ "apps/rhino-cli/tests/fixtures/test-contract/owners"; owner; fileName ]

    let absolute =
        Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar))

    Directory.CreateDirectory(Path.GetDirectoryName(absolute: string)) |> ignore
    File.WriteAllText(absolute, body)
    relative

let private coverageFixtureBody =
    String.concat
        "\n"
        [ "{"
          "  \"schema\": \"ose-test-contract-owner-fixture/v1\","
          "  \"owner-id\": \"O-PUB-RHINO\","
          "  \"check\": \"coverage\","
          "  \"mutation\": {"
          "    \"kind\": \"coverage-threshold\","
          "    \"slice\": \"apps/rhino-cli\","
          "    \"threshold\": 99,"
          "    \"covered-lines\": 98,"
          "    \"total-lines\": 100"
          "  },"
          "  \"expected-diagnostic\": {"
          "    \"code\": \"coverage-below-floor\","
          "    \"fields\": [\"slice\", \"threshold\", \"covered-lines\", \"total-lines\"]"
          "  }"
          "}"
          "" ]

[<Fact>]
let ``an owner fixture resolves under its own owner directory`` () =
    let root = newTempDir ()
    let relative = seedFixture root "O-PUB-RHINO" "coverage-98.json" coverageFixtureBody

    let document =
        expectOk "fixture-resolution" (loadFixture root "O-PUB-RHINO" CheckCoverage relative)

    Assert.Equal("ose-test-contract-owner-fixture/v1", document.Schema)
    Assert.Equal("O-PUB-RHINO", document.OwnerId)
    Assert.Equal("coverage-below-floor", document.ExpectedDiagnostic.Code)

    match document.Mutation with
    | CoverageThreshold(slice, threshold, covered, total) ->
        Assert.Equal("apps/rhino-cli", slice)
        Assert.Equal(99, threshold)
        Assert.Equal(98, covered)
        Assert.Equal(100, total)
    | other -> Assert.Fail(sprintf "contract case 'fixture-resolution': expected a coverage mutation but got %A" other)

[<Fact>]
let ``an owner fixture declaring an unknown schema is rejected`` () =
    let root = newTempDir ()

    let relative =
        seedFixture
            root
            "O-PUB-RHINO"
            "coverage-98.json"
            (coverageFixtureBody.Replace("ose-test-contract-owner-fixture/v1", "ose-test-contract-owner-fixture/v2"))

    loadFixture root "O-PUB-RHINO" CheckCoverage relative
    |> expectContractFailure
        "fixture-schema-version"
        "schema"
        "O-PUB-RHINO"
        "ose-test-contract-owner-fixture/v1"
        "ose-test-contract-owner-fixture/v2"
        "ose-test-contract-owner-fixture/v2"

[<Fact>]
let ``an owner fixture whose document owner disagrees with the path owner is rejected`` () =
    let root = newTempDir ()

    let relative =
        seedFixture root "O-PUB-FS-ENV" "coverage-98.json" coverageFixtureBody

    loadFixture root "O-PUB-FS-ENV" CheckCoverage relative
    |> expectContractFailure "fixture-document-owner" "owner-id" "O-PUB-FS-ENV" "O-PUB-FS-ENV" "O-PUB-RHINO" "owner-id"

[<Fact>]
let ``a fixture path that resolves to no file is rejected as a contract failure`` () =
    loadFixture
        (newTempDir ())
        "O-PUB-RHINO"
        CheckCoverage
        "apps/rhino-cli/tests/fixtures/test-contract/owners/O-PUB-RHINO/coverage-98.json"
    |> expectContractFailure
        "fixture-missing-file"
        "fixture"
        "O-PUB-RHINO"
        "present"
        "absent"
        "the owner fixture does not exist"

[<Fact>]
let ``a fixture whose ownerId disagrees with its path owner is rejected`` () =
    loadFixture
        (repositoryRoot ())
        "O-PUB-RHINO"
        CheckCoverage
        "apps/rhino-cli/tests/fixtures/test-contract/owners/O-PUB-FS-ENV/coverage-98.json"
    |> expectMisuse "fixture-owner-agreement" "owner"

[<Fact>]
let ``an absolute fixture path is rejected`` () =
    loadFixture (repositoryRoot ()) "O-PUB-RHINO" CheckLayout "/etc/layout-misplaced.json"
    |> expectMisuse "fixture-path-absolute" "absolute"

[<Fact>]
let ``a traversal fixture path is rejected`` () =
    loadFixture
        (repositoryRoot ())
        "O-PUB-RHINO"
        CheckBdd
        "apps/rhino-cli/tests/fixtures/test-contract/owners/../../../bdd-missing-step.json"
    |> expectMisuse "fixture-path-traversal" "traversal"

[<Fact>]
let ``a fixture whose check disagrees with the requested check is rejected`` () =
    loadFixture
        (repositoryRoot ())
        "O-PUB-RHINO"
        CheckManifest
        "apps/rhino-cli/tests/fixtures/test-contract/owners/O-PUB-RHINO/coverage-98.json"
    |> expectMisuse "fixture-check-agreement" "check"

[<Fact>]
let ``a fixture file outside the four allowed names is rejected`` () =
    loadFixture
        (repositoryRoot ())
        "O-PUB-RHINO"
        CheckLayout
        "apps/rhino-cli/tests/fixtures/test-contract/owners/O-PUB-RHINO/layout-extra.json"
    |> expectMisuse "fixture-allowed-names" "layout-misplaced.json"

// ---------------------------------------------------------------------------
// CLI parser and help surface
// ---------------------------------------------------------------------------

/// The smallest `repo-config.yml` the strict dual reader accepts: an empty
/// frozen legacy block and an empty, schema-correct canonical root. The
/// parser-shape cases below assert how the CLI parses its own arguments, so
/// they need a registry that reads cleanly and resolves to zero rows rather
/// than a populated one.
let private emptyRegistryYaml =
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
          "  projects: []"
          "" ]

/// A temp repository root seeded with [`emptyRegistryYaml`].
let private newSeededRoot () : string =
    let root = newTempDir ()
    File.WriteAllText(Path.Combine(root, "repo-config.yml"), emptyRegistryYaml)
    root

/// Runs `route`, capturing stdout/stderr around the call and restoring the
/// prior writers afterwards even if `route` throws.
let private runCaptured (argv: string[]) : int * string =
    let root = newSeededRoot ()
    let originalOut = Console.Out
    let originalErr = Console.Error
    use outWriter = new StringWriter()
    use errWriter = new StringWriter()

    try
        Console.SetOut(outWriter)
        Console.SetError(errWriter)
        let exitCode = route (fun () -> Ok root) argv
        exitCode, outWriter.ToString() + errWriter.ToString()
    finally
        Console.SetOut(originalOut)
        Console.SetError(originalErr)

[<Fact>]
let ``the snapshot parser accepts the legacy source form`` () =
    let output = Path.Combine(newTempDir (), "legacy.tsv")

    let exitCode, text =
        runCaptured
            [| "test-contract"
               "registry"
               "snapshot"
               "--source"
               "legacy"
               "--output"
               output |]

    Assert.True(
        (exitCode = 0),
        sprintf "contract case 'snapshot-form-legacy': expected exit 0 but got %d with output: %s" exitCode text
    )

[<Fact>]
let ``the snapshot parser accepts the canonical project-list-from form`` () =
    let root = newTempDir ()
    let legacy = Path.Combine(root, "legacy.tsv")
    File.WriteAllText(legacy, "rhino-cli\trhino-cli\trhino-cli:default\tunit@rhino-cli\n")
    let output = Path.Combine(root, "canonical.tsv")

    let exitCode, text =
        runCaptured
            [| "test-contract"
               "registry"
               "snapshot"
               "--source"
               "canonical"
               "--project-list-from"
               legacy
               "--output"
               output |]

    Assert.True(
        (exitCode = 0),
        sprintf "contract case 'snapshot-form-canonical': expected exit 0 but got %d with output: %s" exitCode text
    )

[<Fact>]
let ``the snapshot parser rejects a --project option as unknown`` () =
    let output = Path.Combine(newTempDir (), "legacy.tsv")

    let exitCode, text =
        runCaptured
            [| "test-contract"
               "registry"
               "snapshot"
               "--source"
               "legacy"
               "--project"
               "rhino-cli"
               "--output"
               output |]

    Assert.Equal(2, exitCode)

    Assert.True(
        containsOrdinal "unknown option: --project" text,
        sprintf
            "contract case 'snapshot-rejects-project': expected an unknown-option diagnostic naming '--project' but got: %s"
            text
    )

[<Fact>]
let ``snapshot help lists exactly the two supported invocation forms`` () =
    let _, text = runCaptured [| "test-contract"; "registry"; "snapshot"; "--help" |]

    Assert.True(
        containsOrdinal "snapshot --source legacy --output" text,
        sprintf "contract case 'snapshot-help-legacy-form': expected the legacy form in help but got: %s" text
    )

    Assert.True(
        containsOrdinal "snapshot --source canonical --project-list-from" text,
        sprintf "contract case 'snapshot-help-canonical-form': expected the canonical form in help but got: %s" text
    )

[<Fact>]
let ``snapshot help advertises no --project option`` () =
    let _, text = runCaptured [| "test-contract"; "registry"; "snapshot"; "--help" |]

    Assert.True(
        containsOrdinal "snapshot --source" text,
        sprintf "contract case 'snapshot-help-no-project': expected snapshot help text but got: %s" text
    )

    let snapshotLinesAdvertisingProject =
        text.Split('\n')
        |> Array.filter (fun line -> containsOrdinal "snapshot" line && containsOrdinal "--project" line)
        |> Array.filter (fun line -> not (containsOrdinal "--project-list-from" line))

    Assert.Equal<string[]>([||], snapshotLinesAdvertisingProject)

[<Fact>]
let ``registry validate exposes a require-state option in its help text`` () =
    let _, text = runCaptured [| "test-contract"; "registry"; "validate"; "--help" |]

    Assert.True(
        containsOrdinal "--require-state" text,
        sprintf "contract case 'validate-help-require-state': expected '--require-state' in help but got: %s" text
    )

[<Fact>]
let ``registry validate-mapping exposes an --all option in its help text`` () =
    let _, text =
        runCaptured [| "test-contract"; "registry"; "validate-mapping"; "--help" |]

    Assert.True(
        containsOrdinal "validate-mapping --all" text,
        sprintf "contract case 'validate-mapping-help-all': expected 'validate-mapping --all' in help but got: %s" text
    )

[<Fact>]
let ``the owner fixture validate leaf exposes its owner check and fixture options in help`` () =
    let _, text = runCaptured [| "test-contract"; "validate"; "--help" |]

    for option in [ "--owner"; "--check"; "--fixture" ] do
        Assert.True(
            containsOrdinal option text,
            sprintf "contract case 'fixture-help-options': expected '%s' in help but got: %s" option text
        )

[<Fact>]
let ``registry validate-mapping accepts a --require-count that matches the mapping total`` () =
    let exitCode, text =
        runCaptured
            [| "test-contract"
               "registry"
               "validate-mapping"
               "--all"
               "--require-count"
               "0" |]

    Assert.True(
        (exitCode = 0),
        sprintf "contract case 'require-count-match': expected exit 0 but got %d with output: %s" exitCode text
    )

    Assert.True(
        containsOrdinal "mappings=0" text,
        sprintf "contract case 'require-count-match': expected 'mappings=0' in output but got: %s" text
    )

[<Fact>]
let ``registry validate-mapping reports a contract failure when --require-count disagrees`` () =
    let exitCode, text =
        runCaptured
            [| "test-contract"
               "registry"
               "validate-mapping"
               "--all"
               "--require-count"
               "3" |]

    Assert.Equal(1, exitCode)

    Assert.True(
        containsOrdinal "--require-count 3 but the registry declares 0" text,
        sprintf "contract case 'require-count-mismatch': expected both counts in the diagnostic but got: %s" text
    )

[<Fact>]
let ``registry validate-mapping rejects a non-numeric --require-count as misuse`` () =
    let exitCode, text =
        runCaptured
            [| "test-contract"
               "registry"
               "validate-mapping"
               "--all"
               "--require-count"
               "three" |]

    Assert.Equal(2, exitCode)

    Assert.True(
        containsOrdinal "--require-count expects a non-negative integer" text,
        sprintf "contract case 'require-count-misuse': expected the misuse diagnostic but got: %s" text
    )
