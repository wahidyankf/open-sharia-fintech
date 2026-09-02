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
let private rhinoCorpus = "specs/apps/rhino/cli/behaviors/**"

/// The repository's real frozen `coverage.projects` values for `rhino-cli`,
/// used only by the two cases that parse the tracked `repo-config.yml`.
let private rhinoLegacySpecs = "specs/apps/rhino/cli/behaviors/**"
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

let private rhinoUnitDriver = "apps/rhino-cli/tests/unit/Steps/ContractsSteps.fs"

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
                [ "specs/apps/ose/app-web/behaviors/**" ]
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
                  (legacyHalf true (Some "specs/apps/ose/app-web/behaviors/**") [ "unit" ])
                  (canonicalHalf
                      (Some "ose-app-web")
                      (Some "specs/apps/ose/app-web/behaviors/**")
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
                [ "specs/apps/ose/be/behaviors/**" ]
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
                [ "specs/apps/ose/app-web/behaviors/**" ]
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
                  (legacyHalf true (Some "specs/apps/ose/be/behaviors/**") [ "unit" ])
                  (canonicalHalf (Some "ose-be") (Some "specs/apps/ose/be/behaviors/**") [])
              mapping
                  "ose-app-web"
                  (Some "ose-app-web:default")
                  MappingIdentity
                  (legacyHalf true (Some "specs/apps/ose/app-web/behaviors/**") [ "unit" ])
                  (canonicalHalf (Some "ose-app-web") (Some "specs/apps/ose/app-web/behaviors/**") []) ]

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
                [ "specs/apps/ose/be/behaviors/**" ]
                (standardAdapters "ose-be" "apps/ose-be/src/tests/unit/Steps/BeSteps.fs"))

    let registry =
        registryOf
            [ rhinoRow; other ]
            [ rhinoMapping
              mapping
                  "ose-be"
                  (Some "rhino-cli:default")
                  MappingIdentity
                  (legacyHalf true (Some "specs/apps/ose/be/behaviors/**") [ "unit" ])
                  (canonicalHalf (Some "ose-be") (Some "specs/apps/ose/be/behaviors/**") []) ]

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
                    Specs = "./specs/apps/rhino/cli/behaviors/**" } ] }

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
    let absolute = "/specs/apps/rhino/cli/behaviors/**"

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

// ---------------------------------------------------------------------------
// End-to-end CLI behavior against a populated registry
// ---------------------------------------------------------------------------

/// A complete two-project registry: one owner whose E2E adapter is delegated,
/// and the dedicated harness that reciprocates it. The parser-shape cases
/// above deliberately resolve to zero rows, so the leaves that read, project,
/// and compare real rows need a root that actually carries them.
let private populatedRegistryYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects:"
          "    - name: widget-app"
          "      levels: [unit]"
          "      specs: \"specs/apps/widget/behavior/app/**\""
          "    - name: widget-app-e2e"
          "      levels: [e2e]"
          "      specs: \"specs/apps/widget/behavior/app/**\""
          "testing:"
          "  schema: ose-test-contract/v1"
          "  coverage:"
          "    minimum-line: 99"
          "  compatibility:"
          "    mappings:"
          "      - project: widget-app"
          "        behavior-id: widget-app:default"
          "        state: identity"
          "        legacy:"
          "          present: true"
          "          corpus: \"specs/apps/widget/behavior/app/**\""
          "          levels: [unit]"
          "        canonical:"
          "          owner: widget-app"
          "          corpus: \"specs/apps/widget/behavior/app/**\""
          "          runtimes:"
          "            - level: e2e"
          "              project: widget-app-e2e"
          "            - level: unit"
          "              project: widget-app"
          "      - project: widget-app-e2e"
          "        behavior-id: widget-app:default"
          "        state: identity"
          "        legacy:"
          "          present: true"
          "          corpus: \"specs/apps/widget/behavior/app/**\""
          "          levels: [e2e]"
          "        canonical:"
          "          owner: widget-app"
          "          corpus: null"
          "          runtimes:"
          "            - level: e2e"
          "              project: widget-app-e2e"
          "  projects:"
          "    - project: widget-app"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        id: widget-app:default"
          "        lifecycle-state: active"
          "        owner: widget-app"
          "        corpus:"
          "          - \"specs/apps/widget/behavior/app/**\""
          "        adapters:"
          "          unit:"
          "            disposition: required"
          "            project: widget-app"
          "            driver: apps/widget-app/tests/unit/bdd/unit-driver.ts"
          "          integration:"
          "            disposition: inapplicable"
          "            reason: no isolated local-resource boundary"
          "          e2e:"
          "            disposition: delegated"
          "            project: widget-app-e2e"
          "            driver: apps/widget-app-e2e/tests/e2e/bdd/e2e-driver.ts"
          "    - project: widget-app-e2e"
          "      profile: e2e"
          "      migration-state: expanded"
          "      behavior:"
          "        id: widget-app:default"
          "        lifecycle-state: active"
          "        owner: widget-app"
          "        corpus: []"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "            reason: the owning project hosts the unit adapter"
          "          integration:"
          "            disposition: inapplicable"
          "            reason: no isolated local-resource boundary"
          "          e2e:"
          "            disposition: required"
          "            project: widget-app-e2e"
          "            driver: apps/widget-app-e2e/tests/e2e/bdd/e2e-driver.ts"
          "" ]

/// Writes one `project.json` so [`enumerateNxProjects`] discovers `name`.
let private seedNxProject (root: string) (name: string) : unit =
    let directory = Path.Combine(root, "apps", name)
    Directory.CreateDirectory(directory) |> ignore
    File.WriteAllText(Path.Combine(directory, "project.json"), sprintf "{ \"name\": \"%s\" }" name)

/// A temp root carrying [`populatedRegistryYaml`] and both `project.json`
/// files its two rows must map onto.
let private newPopulatedRoot () : string =
    let root = newTempDir ()
    File.WriteAllText(Path.Combine(root, "repo-config.yml"), populatedRegistryYaml)
    seedNxProject root "widget-app"
    seedNxProject root "widget-app-e2e"
    root

/// Runs `route` against an explicit root, capturing stdout and stderr.
let private runAt (root: string) (argv: string[]) : int * string =
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

let private expectExit (case: string) (expected: int) (actual: int, text: string) : string =
    Assert.True(
        (actual = expected),
        sprintf "contract case '%s': expected exit %d but got %d with output: %s" case expected actual text
    )

    text

[<Fact>]
let ``registry validate accepts a populated two-project registry`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate" |]
        |> expectExit "populated-validate" 0

    Assert.True(
        containsOrdinal "registry-valid state=expanded projects=2" text,
        sprintf "contract case 'populated-validate': expected the expanded two-project summary but got: %s" text
    )

    Assert.True(
        containsOrdinal "behavior=bootstrap:0,active:2" text,
        sprintf "contract case 'populated-validate': expected both owners active but got: %s" text
    )

[<Fact>]
let ``registry validate honours a matching --require-state`` () =
    runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate"; "--require-state"; "expanded" |]
    |> expectExit "require-state-match" 0
    |> ignore

[<Fact>]
let ``registry validate rejects a --require-state the rows have not reached`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate"; "--require-state"; "verified" |]
        |> expectExit "require-state-unreached" 1

    Assert.True(
        containsOrdinal "widget-app" text,
        sprintf "contract case 'require-state-unreached': expected the failing project named but got: %s" text
    )

[<Fact>]
let ``registry validate rejects an unknown --require-state value as misuse`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate"; "--require-state"; "sideways" |]
        |> expectExit "require-state-unknown" 2

    Assert.True(
        containsOrdinal "expanded, migrating, verified, or contracted" text,
        sprintf "contract case 'require-state-unknown': expected the allowed-state diagnostic but got: %s" text
    )

[<Fact>]
let ``registry validate accepts a matching --require-behavior-state`` () =
    runAt
        (newPopulatedRoot ())
        [| "test-contract"
           "registry"
           "validate"
           "--require-behavior-state"
           "active" |]
    |> expectExit "require-behavior-active" 0
    |> ignore

[<Fact>]
let ``registry validate rejects an unknown --require-behavior-state value as misuse`` () =
    let text =
        runAt
            (newPopulatedRoot ())
            [| "test-contract"
               "registry"
               "validate"
               "--require-behavior-state"
               "dormant" |]
        |> expectExit "require-behavior-unknown" 2

    Assert.True(
        containsOrdinal "bootstrap or active" text,
        sprintf "contract case 'require-behavior-unknown': expected the allowed-lifecycle diagnostic but got: %s" text
    )

[<Fact>]
let ``registry validate --forbid-legacy fails while the frozen block survives`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate"; "--forbid-legacy" |]
        |> expectExit "forbid-legacy-cli" 1

    Assert.True(
        containsOrdinal "coverage.projects" text,
        sprintf "contract case 'forbid-legacy-cli': expected the frozen block named but got: %s" text
    )

[<Fact>]
let ``registry validate --forbid-compatibility fails while the mappings survive`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate"; "--forbid-compatibility" |]
        |> expectExit "forbid-compatibility-cli" 1

    Assert.True(
        containsOrdinal "compatibility" text,
        sprintf "contract case 'forbid-compatibility-cli': expected the mapping root named but got: %s" text
    )

[<Fact>]
let ``registry validate accepts a repeated --allow-bootstrap option`` () =
    runAt
        (newPopulatedRoot ())
        [| "test-contract"
           "registry"
           "validate"
           "--allow-bootstrap"
           "widget-app"
           "--allow-bootstrap"
           "widget-app-e2e" |]
    |> expectExit "allow-bootstrap-repeatable" 0
    |> ignore

[<Fact>]
let ``registry validate-mapping reports both mappings for a populated registry`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate-mapping"; "--all" |]
        |> expectExit "populated-mapping" 0

    Assert.True(
        containsOrdinal "registry-mapping-valid state=identity mappings=2" text,
        sprintf "contract case 'populated-mapping': expected the identity two-mapping summary but got: %s" text
    )

[<Fact>]
let ``registry validate-mapping accepts a --project selector`` () =
    runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate-mapping"; "--project"; "widget-app" |]
    |> expectExit "mapping-project-selector" 0
    |> ignore

[<Fact>]
let ``registry validate-mapping requires one of --all or --project`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "validate-mapping" |]
        |> expectExit "mapping-selector-required" 2

    Assert.True(
        containsOrdinal "one of --all or --project" text,
        sprintf "contract case 'mapping-selector-required': expected the selector diagnostic but got: %s" text
    )

[<Fact>]
let ``registry validate-mapping rejects an unknown --require-state value as misuse`` () =
    let text =
        runAt
            (newPopulatedRoot ())
            [| "test-contract"
               "registry"
               "validate-mapping"
               "--all"
               "--require-state"
               "sideways" |]
        |> expectExit "mapping-state-unknown" 2

    Assert.True(
        containsOrdinal "identity, redirected, or verified" text,
        sprintf "contract case 'mapping-state-unknown': expected the allowed-state diagnostic but got: %s" text
    )

[<Fact>]
let ``registry validate-mapping rejects a mapping state the rows have not reached`` () =
    runAt
        (newPopulatedRoot ())
        [| "test-contract"
           "registry"
           "validate-mapping"
           "--all"
           "--require-state"
           "verified" |]
    |> expectExit "mapping-state-unreached" 1
    |> ignore

/// Projects both sides of the dual reader into `root` and returns the two
/// output paths, asserting each leaf exits 0.
let private projectBothSnapshots (root: string) : string * string =
    let legacy = Path.Combine(root, "legacy.tsv")
    let canonical = Path.Combine(root, "canonical.tsv")

    runAt
        root
        [| "test-contract"
           "registry"
           "snapshot"
           "--source"
           "legacy"
           "--output"
           legacy |]
    |> expectExit "snapshot-legacy-rows" 0
    |> ignore

    runAt
        root
        [| "test-contract"
           "registry"
           "snapshot"
           "--source"
           "canonical"
           "--project-list-from"
           legacy
           "--output"
           canonical |]
    |> expectExit "snapshot-canonical-rows" 0
    |> ignore

    legacy, canonical

[<Fact>]
let ``the legacy snapshot projects one sorted row per registered project`` () =
    let root = newPopulatedRoot ()
    let legacy, _ = projectBothSnapshots root
    let rows = File.ReadAllLines legacy

    Assert.Equal<string[]>(
        [| "widget-app\twidget-app\twidget-app:default\te2e@widget-app-e2e,unit@widget-app"
           "widget-app-e2e\twidget-app\twidget-app:default\te2e@widget-app-e2e" |],
        rows
    )

[<Fact>]
let ``compare accepts byte-equal legacy and canonical projections`` () =
    let root = newPopulatedRoot ()
    let legacy, canonical = projectBothSnapshots root

    let text =
        runAt
            root
            [| "test-contract"
               "registry"
               "compare"
               "--legacy"
               legacy
               "--canonical"
               canonical |]
        |> expectExit "compare-equal" 0

    Assert.True(
        containsOrdinal "registry-preservation: equal rows=2" text,
        sprintf "contract case 'compare-equal': expected the equal-rows summary but got: %s" text
    )

[<Fact>]
let ``compare rejects a canonical projection whose row changed`` () =
    let root = newPopulatedRoot ()
    let legacy, canonical = projectBothSnapshots root

    File.WriteAllText(canonical, (File.ReadAllText canonical).Replace("unit@widget-app", "unit@widget-tool"))

    let text =
        runAt
            root
            [| "test-contract"
               "registry"
               "compare"
               "--legacy"
               legacy
               "--canonical"
               canonical |]
        |> expectExit "compare-changed" 1

    Assert.True(
        containsOrdinal "widget-app" text,
        sprintf "contract case 'compare-changed': expected the changed row named but got: %s" text
    )

[<Fact>]
let ``compare rejects a projection file that does not exist`` () =
    let root = newPopulatedRoot ()
    let legacy, canonical = projectBothSnapshots root
    File.Delete canonical

    runAt
        root
        [| "test-contract"
           "registry"
           "compare"
           "--legacy"
           legacy
           "--canonical"
           canonical |]
    |> expectExit "compare-missing-file" 2
    |> ignore

[<Fact>]
let ``an unrouted test-contract subcommand is CLI misuse`` () =
    let text =
        runAt (newPopulatedRoot ()) [| "test-contract"; "registry"; "rewrite" |]
        |> expectExit "test-contract-unrouted" 2

    Assert.True(
        containsOrdinal "test-contract" text,
        sprintf "contract case 'test-contract-unrouted': expected the namespace named but got: %s" text
    )

// ---------------------------------------------------------------------------
// Owner fixture leaf, end to end
// ---------------------------------------------------------------------------

/// Builds one owner-fixture document for `check` around `mutation`, which the
/// four cases below vary. `owner` is repeated inside the document because the
/// loader requires the path owner, `owner-id`, and `--owner` to agree.
let private fixtureBody (owner: string) (check: string) (code: string) (mutation: string list) : string =
    String.concat
        "\n"
        ([ "{"
           sprintf "  \"schema\": \"%s\"," FixtureSchemaVersion
           sprintf "  \"owner-id\": \"%s\"," owner
           sprintf "  \"check\": \"%s\"," check
           "  \"mutation\": {" ]
         @ mutation
         @ [ "  },"
             "  \"expected-diagnostic\": {"
             sprintf "    \"code\": \"%s\"," code
             "    \"fields\": [\"path\"]"
             "  }"
             "}"
             "" ])

let private layoutMutation =
    [ "    \"kind\": \"layout-overlap\","
      "    \"path\": \"apps/rhino-cli/tests/unit\","
      "    \"layers\": [\"unit\", \"integration\"]" ]

let private bddMutation =
    [ "    \"kind\": \"bdd-remove-binding\","
      "    \"feature\": \"specs/apps/rhino/cli/behaviors/specs/parity.feature\","
      "    \"scenario\": \"The manifest is current\","
      "    \"step\": \"Then the manifest is current\","
      "    \"adapter\": \"unit\"" ]

let private manifestMutation =
    [ "    \"kind\": \"manifest-forwarder\","
      "    \"path\": \"apps/rhino-cli/package.json\","
      "    \"direct-consumers\": [],"
      "    \"script-name\": \"test\","
      "    \"script\": \"npx nx run rhino-cli:test\"" ]

/// Seeds one fixture for `check` and runs the leaf against it.
let private runFixtureLeaf (check: string) (fileName: string) (body: string) : int * string =
    let root = newTempDir ()
    let relative = seedFixture root "O-PUB-RHINO" fileName body

    runAt
        root
        [| "test-contract"
           "validate"
           "--owner"
           "O-PUB-RHINO"
           "--check"
           check
           "--fixture"
           relative |]

[<Fact>]
let ``the fixture leaf loads a layout-overlap document`` () =
    let text =
        runFixtureLeaf
            "layout"
            "layout-misplaced.json"
            (fixtureBody "O-PUB-RHINO" "layout" "layout-overlap" layoutMutation)
        |> expectExit "fixture-leaf-layout" 0

    Assert.True(
        containsOrdinal "fixture-loaded owner=O-PUB-RHINO check=layout code=layout-overlap" text,
        sprintf "contract case 'fixture-leaf-layout': expected the loaded-fixture summary but got: %s" text
    )

[<Fact>]
let ``the fixture leaf loads a coverage-threshold document`` () =
    let text =
        runFixtureLeaf "coverage" "coverage-98.json" coverageFixtureBody
        |> expectExit "fixture-leaf-coverage" 0

    Assert.True(
        containsOrdinal "check=coverage code=coverage-below-floor" text,
        sprintf "contract case 'fixture-leaf-coverage': expected the coverage summary but got: %s" text
    )

[<Fact>]
let ``the fixture leaf loads a bdd-remove-binding document`` () =
    let text =
        runFixtureLeaf "bdd" "bdd-missing-step.json" (fixtureBody "O-PUB-RHINO" "bdd" "bdd-step-unbound" bddMutation)
        |> expectExit "fixture-leaf-bdd" 0

    Assert.True(
        containsOrdinal "check=bdd code=bdd-step-unbound" text,
        sprintf "contract case 'fixture-leaf-bdd': expected the bdd summary but got: %s" text
    )

[<Fact>]
let ``the fixture leaf loads a manifest-forwarder document`` () =
    let text =
        runFixtureLeaf
            "manifest"
            "manifest-proxy.json"
            (fixtureBody "O-PUB-RHINO" "manifest" "manifest-proxy-script" manifestMutation)
        |> expectExit "fixture-leaf-manifest" 0

    Assert.True(
        containsOrdinal "check=manifest code=manifest-proxy-script" text,
        sprintf "contract case 'fixture-leaf-manifest': expected the manifest summary but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects a mutation kind bound to another check`` () =
    let text =
        runFixtureLeaf
            "layout"
            "layout-misplaced.json"
            (fixtureBody "O-PUB-RHINO" "layout" "layout-overlap" manifestMutation)
        |> expectExit "fixture-leaf-wrong-kind" 2

    Assert.True(
        containsOrdinal "is not the mutation kind bound to the \"layout\" check" text,
        sprintf "contract case 'fixture-leaf-wrong-kind': expected the bound-kind diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects a mutation missing a required field`` () =
    let text =
        runFixtureLeaf
            "layout"
            "layout-misplaced.json"
            (fixtureBody "O-PUB-RHINO" "layout" "layout-overlap" [ "    \"kind\": \"layout-overlap\"" ])
        |> expectExit "fixture-leaf-missing-field" 2

    Assert.True(
        containsOrdinal "mutation.path" text,
        sprintf "contract case 'fixture-leaf-missing-field': expected the missing-key diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects an unknown mutation key`` () =
    let text =
        runFixtureLeaf "coverage" "coverage-98.json" (coverageFixtureBody.Replace("\"slice\"", "\"module\""))
        |> expectExit "fixture-leaf-unknown-key" 2

    Assert.True(
        containsOrdinal "unknown key" text,
        sprintf "contract case 'fixture-leaf-unknown-key': expected the unknown-key diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf requires --owner`` () =
    let root = newTempDir ()

    let text =
        runAt root [| "test-contract"; "validate"; "--check"; "coverage"; "--fixture"; "x.json" |]
        |> expectExit "fixture-leaf-owner-required" 2

    Assert.True(
        containsOrdinal "--owner is required" text,
        sprintf "contract case 'fixture-leaf-owner-required': expected the owner diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf requires --fixture`` () =
    let text =
        runAt (newTempDir ()) [| "test-contract"; "validate"; "--owner"; "O-PUB-RHINO"; "--check"; "bdd" |]
        |> expectExit "fixture-leaf-fixture-required" 2

    Assert.True(
        containsOrdinal "--fixture is required" text,
        sprintf "contract case 'fixture-leaf-fixture-required': expected the fixture diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects an unknown --check value`` () =
    let text =
        runAt
            (newTempDir ())
            [| "test-contract"
               "validate"
               "--owner"
               "O-PUB-RHINO"
               "--check"
               "typing"
               "--fixture"
               "x.json" |]
        |> expectExit "fixture-leaf-check-unknown" 2

    Assert.True(
        containsOrdinal "layout, coverage, bdd, or manifest" text,
        sprintf "contract case 'fixture-leaf-check-unknown': expected the allowed-check diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects an unknown option`` () =
    let text =
        runAt
            (newTempDir ())
            [| "test-contract"
               "validate"
               "--owner"
               "O-PUB-RHINO"
               "--check"
               "bdd"
               "--strict" |]
        |> expectExit "fixture-leaf-unknown-option" 2

    Assert.True(
        containsOrdinal "unknown option: --strict" text,
        sprintf "contract case 'fixture-leaf-unknown-option': expected the unknown-option diagnostic but got: %s" text
    )

// ---------------------------------------------------------------------------
// Reciprocity, behavior-free rows, and the remaining mapping identities
// ---------------------------------------------------------------------------

/// The three adapters a dedicated harness declares when it hosts none of the
/// levels its owner delegates — the shape that breaks reciprocity.
let private nonReciprocalAdapters: Adapters =
    adapters
        (inapplicableAdapter "the owning project hosts the unit adapter")
        (inapplicableAdapter "no isolated local-resource boundary")
        (inapplicableAdapter "no user-facing surface")

/// A row whose project owns no behavior, but which still declares one of the
/// fields only an owner may carry.
let private unownedBehavior (lifecycle: LifecycleState option) (seed: Seed option) (corpus: string list) : Behavior =
    { Id = None
      LifecycleState = lifecycle
      Owner = None
      Corpus = corpus
      Seed = seed
      Adapters = unownedAdapters }

let private unownedRegistry (behavior: Behavior) : Registry =
    registryOf [ projectRow "rhino-cli" ProfileTool Expanded behavior ] [ rhinoMapping ]

[<Fact>]
let ``a delegated adapter whose target does not host that level is rejected`` () =
    let owner =
        projectRow
            "rhino-cli"
            ProfileTool
            Expanded
            (activeBehavior
                "rhino-cli:default"
                "rhino-cli"
                [ rhinoCorpus ]
                (adapters
                    (requiredAdapter "rhino-cli" rhinoUnitDriver)
                    (inapplicableAdapter "no isolated local-resource boundary")
                    (delegatedAdapter "rhino-cli-e2e" rhinoUnitDriver)))

    let harness =
        projectRow
            "rhino-cli-e2e"
            ProfileE2e
            Expanded
            (activeBehavior "rhino-cli:default" "rhino-cli" [] nonReciprocalAdapters)

    validate (registryOf [ owner; harness ] [ rhinoMapping ]) [ "rhino-cli"; "rhino-cli-e2e" ] defaultValidateOptions
    |> expectContractFailure
        "delegation-not-reciprocal"
        "adapters.e2e.project"
        "rhino-cli"
        "required"
        "inapplicable"
        "rather than hosting the e2e adapter"

[<Fact>]
let ``a behavior-free row declaring a lifecycle state is rejected`` () =
    validate (unownedRegistry (unownedBehavior (Some Active) None [])) nxProjects defaultValidateOptions
    |> expectContractFailure
        "unowned-lifecycle"
        "behavior.lifecycle-state"
        "rhino-cli"
        "absent"
        "active"
        "owns no behavior but declares"

[<Fact>]
let ``a behavior-free row declaring a seed is rejected`` () =
    validate (unownedRegistry (unownedBehavior None (Some rhinoSeed) [])) nxProjects defaultValidateOptions
    |> expectContractFailure
        "unowned-seed"
        "behavior.seed"
        "rhino-cli"
        "absent"
        rhinoSeed.Target
        "owns no behavior but declares"

[<Fact>]
let ``a behavior-free row declaring a corpus is rejected`` () =
    validate (unownedRegistry (unownedBehavior None None [ rhinoCorpus ])) nxProjects defaultValidateOptions
    |> expectContractFailure
        "unowned-corpus"
        "behavior.corpus"
        "rhino-cli"
        "empty"
        rhinoCorpus
        "owns no behavior but declares a corpus"

[<Fact>]
let ``validate rejects a map whose canonical owner disagrees with the row`` () =
    let drifted =
        { rhinoMapping with
            Canonical = canonicalHalf (Some "widget-app") (Some rhinoCorpus) rhinoRuntimes }

    validate (withMapping drifted baseRegistry) nxProjects defaultValidateOptions
    |> expectContractFailure
        "validate-canonical-owner-drift"
        "testing.compatibility.mappings[].canonical.owner"
        "rhino-cli"
        "rhino-cli"
        "widget-app"
        "canonical.owner"

[<Fact>]
let ``validate rejects an active owner when bootstrap was required`` () =
    let options =
        { defaultValidateOptions with
            RequireBehaviorState = Some Bootstrap }

    validate baseRegistry nxProjects options
    |> expectContractFailure
        "require-behavior-bootstrap"
        "behavior.lifecycle-state"
        "rhino-cli"
        "active"
        "bootstrap"
        "was required"

[<Fact>]
let ``validate-mapping rejects a frozen legacy corpus that was rewritten`` () =
    let rewritten =
        { rhinoMapping with
            Legacy = legacyHalf true (Some "specs/apps/widget/behavior/app/**") [ "unit" ] }

    validateMapping (withMapping rewritten baseRegistry) nxProjects None
    |> expectContractFailure
        "mapping-legacy-corpus-rewritten"
        "testing.compatibility.mappings[].legacy.corpus"
        "rhino-cli"
        rhinoCorpus
        "specs/apps/widget/behavior/app/**"
        "legacy.corpus"

[<Fact>]
let ``validate-mapping rejects frozen legacy levels that were rewritten`` () =
    let rewritten =
        { rhinoMapping with
            Legacy = legacyHalf true (Some rhinoCorpus) [ "e2e" ] }

    validateMapping (withMapping rewritten baseRegistry) nxProjects None
    |> expectContractFailure
        "mapping-legacy-levels-rewritten"
        "testing.compatibility.mappings[].legacy.levels"
        "rhino-cli"
        "unit"
        "e2e"
        "legacy.levels"

[<Fact>]
let ``validate-mapping rejects a behavior id that disagrees with its row`` () =
    let drifted =
        { rhinoMapping with
            BehaviorId = Some "rhino-cli:documents" }

    validateMapping (withMapping drifted baseRegistry) nxProjects None
    |> expectContractFailure
        "mapping-behavior-id-drift"
        "testing.compatibility.mappings[].behavior-id"
        "rhino-cli"
        "rhino-cli:default"
        "rhino-cli:documents"
        "behavior-id"

[<Fact>]
let ``validate-mapping rejects a canonical owner that disagrees with its row`` () =
    let drifted =
        { rhinoMapping with
            Canonical = canonicalHalf (Some "widget-app") (Some rhinoCorpus) rhinoRuntimes }

    validateMapping (withMapping drifted baseRegistry) nxProjects None
    |> expectContractFailure
        "mapping-canonical-owner-drift"
        "testing.compatibility.mappings[].canonical.owner"
        "rhino-cli"
        "rhino-cli"
        "widget-app"
        "canonical.owner"

[<Fact>]
let ``a fixture document without a mutation object is rejected`` () =
    let body =
        String.concat
            "\n"
            [ "{"
              sprintf "  \"schema\": \"%s\"," FixtureSchemaVersion
              "  \"owner-id\": \"O-PUB-RHINO\","
              "  \"check\": \"coverage\","
              "  \"expected-diagnostic\": { \"code\": \"coverage-below-floor\", \"fields\": [] }"
              "}"
              "" ]

    let text =
        runFixtureLeaf "coverage" "coverage-98.json" body
        |> expectExit "fixture-no-mutation" 2

    Assert.True(
        containsOrdinal "mutation is required" text,
        sprintf "contract case 'fixture-no-mutation': expected the required-mutation diagnostic but got: %s" text
    )

[<Fact>]
let ``a fixture document without an expected diagnostic is rejected`` () =
    let body =
        String.concat
            "\n"
            [ "{"
              sprintf "  \"schema\": \"%s\"," FixtureSchemaVersion
              "  \"owner-id\": \"O-PUB-RHINO\","
              "  \"check\": \"layout\","
              "  \"mutation\": { \"kind\": \"layout-overlap\", \"path\": \"apps/rhino-cli\", \"layers\": [] }"
              "}"
              "" ]

    let text =
        runFixtureLeaf "layout" "layout-misplaced.json" body
        |> expectExit "fixture-no-diagnostic" 2

    Assert.True(
        containsOrdinal "expected-diagnostic is required" text,
        sprintf "contract case 'fixture-no-diagnostic': expected the required-diagnostic message but got: %s" text
    )

[<Fact>]
let ``a fixture expected diagnostic without a code is rejected`` () =
    let text =
        runFixtureLeaf "coverage" "coverage-98.json" (coverageFixtureBody.Replace("\"code\"", "\"identifier\""))
        |> expectExit "fixture-no-code" 2

    Assert.True(
        containsOrdinal "unknown key" text,
        sprintf "contract case 'fixture-no-code': expected the unknown-key diagnostic but got: %s" text
    )

[<Fact>]
let ``a fixture document carrying an unknown top-level key is rejected`` () =
    let text =
        runFixtureLeaf
            "coverage"
            "coverage-98.json"
            (coverageFixtureBody.Replace("  \"check\": \"coverage\",", "  \"check\": \"coverage\",\n  \"note\": \"x\","))
        |> expectExit "fixture-unknown-top-level" 2

    Assert.True(
        containsOrdinal "unknown key \"note\"" text,
        sprintf "contract case 'fixture-unknown-top-level': expected the unknown-key diagnostic but got: %s" text
    )

// ---------------------------------------------------------------------------
// Behavior and adapter findings not yet exercised above
// ---------------------------------------------------------------------------

[<Fact>]
let ``an owner row declaring no behavior id and no lifecycle state is rejected`` () =
    let behavior =
        { rhinoBehavior with
            Id = None
            LifecycleState = None }

    let result =
        validate (withBehavior behavior baseRegistry) nxProjects defaultValidateOptions

    result
    |> expectContractFailure
        "owner-missing-behavior-id"
        "behavior.id"
        "rhino-cli"
        "rhino-cli:default"
        "absent"
        "declares an owner but no behavior id"

    result
    |> expectContractFailure
        "owner-missing-lifecycle-state"
        "behavior.lifecycle-state"
        "rhino-cli"
        "active"
        "absent"
        "declares an owner but no lifecycle state"

[<Fact>]
let ``a bootstrap owner declaring a blank seed target is rejected`` () =
    let blankSeed = { Target = "   "; Driver = seedDriver }

    let behavior =
        bootstrapBehavior "rhino-cli:default" "rhino-cli" (Some blankSeed) rhinoAdapters

    validate (withBehavior behavior baseRegistry) nxProjects defaultValidateOptions
    |> expectContractFailure
        "bootstrap-seed-target-blank"
        "behavior.seed.target"
        "rhino-cli"
        "test:behavior:seed"
        "blank"
        "declares a blank Nx target"

[<Fact>]
let ``a non-owner row delegating to an owner with no resolved corpus is rejected`` () =
    let ownerRow =
        { rhinoRow with
            Behavior = { rhinoBehavior with Corpus = [] } }

    let delegateRow =
        projectRow
            "rhino-cli-docs"
            ProfileTool
            Expanded
            { rhinoBehavior with
                Corpus = []
                Adapters = nonReciprocalAdapters }

    let registry = registryOf [ ownerRow; delegateRow ] [ rhinoMapping ]

    validate registry [ "rhino-cli"; "rhino-cli-docs" ] defaultValidateOptions
    |> expectContractFailure
        "delegate-corpus-empty-owner"
        "behavior.corpus"
        "rhino-cli-docs"
        "non-empty"
        "empty"
        "delegates to rhino-cli, which resolves no corpus"

[<Fact>]
let ``a single adapter block surfaces an inapplicable driver a delegated reason and self-delegation`` () =
    let entries =
        adapters
            (adapterEntry Inapplicable (Some "stray-project") (Some rhinoUnitDriver) None)
            (adapterEntry Delegated (Some "other-project") (Some rhinoUnitDriver) (Some "extra context"))
            (adapterEntry Delegated (Some "rhino-cli") (Some rhinoUnitDriver) None)

    let text =
        match validate (withAdapters entries baseRegistry) [ "rhino-cli"; "other-project" ] defaultValidateOptions with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    Assert.Contains(
        sprintf "behavior.adapters.unit.driver: rhino-cli declares \"%s\" on an inapplicable adapter" rhinoUnitDriver,
        text
    )

    Assert.Contains(
        "behavior.adapters.unit.reason: rhino-cli must explain an inapplicable adapter, found \"<absent>\"",
        text
    )

    Assert.Contains(
        "behavior.adapters.integration.reason: rhino-cli declares \"extra context\" on a delegated adapter",
        text
    )

    Assert.Contains("behavior.adapters.e2e.project: rhino-cli cannot delegate an adapter to itself", text)

// ---------------------------------------------------------------------------
// validate and validate-mapping root-level and aggregate cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``validate rejects a registry whose canonical root is missing`` () =
    validate { baseRegistry with Testing = None } nxProjects defaultValidateOptions
    |> expectContractFailure
        "validate-testing-root-missing"
        "testing"
        "rhino-cli"
        "present"
        "absent"
        "the canonical registry root is missing"

[<Fact>]
let ``validate-mapping rejects a registry whose canonical root is missing`` () =
    validateMapping { baseRegistry with Testing = None } nxProjects None
    |> expectContractFailure
        "validate-mapping-testing-root-missing"
        "testing"
        "rhino-cli"
        "present"
        "absent"
        "the canonical registry root is missing"

[<Fact>]
let ``validate accepts an owner row that carries no compatibility mapping at all`` () =
    let report =
        expectOk "owner-without-mapping" (validate (registryOf [ rhinoRow ] []) nxProjects defaultValidateOptions)

    Assert.False(report.CompatibilityPresent)

[<Fact>]
let ``validate reports a mixed migration state when two rows disagree`` () =
    let rowB =
        projectRow
            "rhino-cli-tools"
            ProfileTool
            Migrating
            (activeBehavior
                "rhino-cli-tools:default"
                "rhino-cli-tools"
                [ rhinoCorpus ]
                (standardAdapters "rhino-cli-tools" rhinoUnitDriver))

    let registry = registryOf [ rhinoRow; rowB ] []

    let report =
        expectOk "mixed-migration-state" (validate registry [ "rhino-cli"; "rhino-cli-tools" ] defaultValidateOptions)

    Assert.Equal("mixed", report.State)

[<Fact>]
let ``validate-mapping rejects a legacy half that contradicts the frozen block on both sides`` () =
    let presentButFrozenAbsent =
        mapping
            "rhino-cli"
            (Some "rhino-cli:default")
            MappingIdentity
            (legacyHalf false None [])
            (canonicalHalf (Some "rhino-cli") (Some rhinoCorpus) rhinoRuntimes)

    let absentButRecordedPresent =
        mapping
            "widget-app-x"
            None
            MappingIdentity
            (legacyHalf true (Some "specs/apps/widget-x/behavior/**") [ "unit" ])
            (canonicalHalf None None [])

    let registry: Registry =
        { Legacy = legacyProjects
          Testing = Some(testingRegistry [] [ presentButFrozenAbsent; absentButRecordedPresent ]) }

    let text =
        match validateMapping registry [ "rhino-cli"; "widget-app-x" ] None with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    Assert.Contains(
        "testing.compatibility.mappings[].legacy.present: rhino-cli is in the frozen legacy block but records \"false\"",
        text
    )

    Assert.Contains(
        "testing.compatibility.mappings[].legacy.present: widget-app-x is absent from the frozen legacy block but records \"true\"",
        text
    )

    Assert.Contains(
        "testing.compatibility.mappings[].legacy.corpus: widget-app-x is legacy-absent but records \"specs/apps/widget-x/behavior/**\"",
        text
    )

// ---------------------------------------------------------------------------
// Transitions not yet exercised above
// ---------------------------------------------------------------------------

[<Fact>]
let ``validateTransition rejects a project newly added to the frozen legacy block`` () =
    let before: Registry = { Legacy = []; Testing = None }

    let after: Registry =
        { Legacy =
            [ { Name = "rhino-cli"
                Levels = [ "unit" ]
                Specs = rhinoCorpus } ]
          Testing = None }

    validateTransition before after
    |> expectContractFailure
        "legacy-project-added"
        "coverage.projects"
        "rhino-cli"
        "absent"
        "present"
        "was added to the frozen legacy block"

[<Fact>]
let ``validateTransition accepts an unchanged empty legacy block when the canonical root is absent on both sides`` () =
    let registry: Registry = { Legacy = []; Testing = None }

    validateTransition registry registry
    |> expectOk "legacy-empty-noop-transition"
    |> ignore

[<Fact>]
let ``validateTransition rejects a frozen legacy row whose corpus and levels were both rewritten`` () =
    let before: Registry =
        { Legacy =
            [ { Name = "rhino-cli"
                Levels = [ "unit" ]
                Specs = rhinoCorpus } ]
          Testing = None }

    let after: Registry =
        { Legacy =
            [ { Name = "rhino-cli"
                Levels = [ "unit"; "integration" ]
                Specs = "specs/apps/rhino/other/**" } ]
          Testing = None }

    let text =
        match validateTransition before after with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    Assert.Contains(
        "coverage.projects: rhino-cli freezes \""
        + rhinoCorpus
        + "\" but now records \"specs/apps/rhino/other/**\"",
        text
    )

    Assert.Contains("coverage.projects: rhino-cli freezes [unit] but now records [integration,unit]", text)

[<Fact>]
let ``validateTransition accepts a project and mapping that first appear in the after revision`` () =
    let before: Registry =
        { Legacy = []
          Testing = Some(testingRegistry [] []) }

    let after: Registry =
        { Legacy = []
          Testing = Some(testingRegistry [ rhinoRow ] [ rhinoMapping ]) }

    validateTransition before after
    |> expectOk "project-and-mapping-first-appear"
    |> ignore

[<Fact>]
let ``validateTransition rejects an activation that resolves no corpus and still declares its seed`` () =
    let beforeBehavior =
        bootstrapBehavior "rhino-cli:default" "rhino-cli" (Some rhinoSeed) rhinoAdapters

    let afterBehavior =
        { beforeBehavior with
            LifecycleState = Some Active
            Corpus = [] }

    let before: Registry =
        { Legacy = []
          Testing =
            Some(
                testingRegistry
                    [ { rhinoRow with
                          Behavior = beforeBehavior } ]
                    []
            ) }

    let after: Registry =
        { Legacy = []
          Testing =
            Some(
                testingRegistry
                    [ { rhinoRow with
                          Behavior = afterBehavior } ]
                    []
            ) }

    let text =
        match validateTransition before after with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    Assert.Contains("behavior.corpus: rhino-cli activated without resolving a corpus", text)

    Assert.Contains(
        "behavior.seed: rhino-cli activated but still declares the seed target \"test:behavior:seed\"",
        text
    )

[<Fact>]
let ``validateTransition rejects a compatibility mapping whose behavior id was rewritten`` () =
    let before: Registry =
        { Legacy = []
          Testing = Some(testingRegistry [ rhinoRow ] [ rhinoMapping ]) }

    let after: Registry =
        { Legacy = []
          Testing =
            Some(
                testingRegistry
                    [ rhinoRow ]
                    [ { rhinoMapping with
                          BehaviorId = Some "rhino-cli:renamed" } ]
            ) }

    validateTransition before after
    |> expectContractFailure
        "mapping-behavior-id-frozen"
        "testing.compatibility.mappings[].behavior-id"
        "rhino-cli"
        "rhino-cli:default"
        "rhino-cli:renamed"
        "freezes \"rhino-cli:default\" but now records \"rhino-cli:renamed\""

[<Fact>]
let ``validateTransition accepts an unchanged legacy-absent mapping corpus on both sides`` () =
    let legacyAbsentMapping =
        mapping
            "rhino-cli"
            (Some "rhino-cli:default")
            MappingIdentity
            (legacyHalf false None [])
            (canonicalHalf (Some "rhino-cli") (Some rhinoCorpus) rhinoRuntimes)

    let registry: Registry =
        { Legacy = []
          Testing = Some(testingRegistry [ rhinoRow ] [ legacyAbsentMapping ]) }

    validateTransition registry registry
    |> expectOk "mapping-corpus-none-both-sides"
    |> ignore

[<Fact>]
let ``validateTransition rejects a mapping whose legacy corpus moved between absent and present`` () =
    let beforeMapping =
        { rhinoMapping with
            Legacy = legacyHalf false None [] }

    let afterMapping =
        { rhinoMapping with
            Legacy = legacyHalf true (Some rhinoCorpus) [ "unit" ] }

    let before: Registry =
        { Legacy = []
          Testing = Some(testingRegistry [ rhinoRow ] [ beforeMapping ]) }

    let after: Registry =
        { Legacy = []
          Testing = Some(testingRegistry [ rhinoRow ] [ afterMapping ]) }

    let text =
        match validateTransition before after with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    Assert.Contains(
        "testing.compatibility.mappings[].legacy.corpus: rhino-cli freezes \"<absent>\" but now records \""
        + rhinoCorpus
        + "\"",
        text
    )

// ---------------------------------------------------------------------------
// Snapshot and comparison edge cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``snapshot rejects a registry whose canonical root is missing`` () =
    snapshot { baseRegistry with Testing = None } SourceLegacy None
    |> expectContractFailure
        "snapshot-testing-root-missing"
        "testing"
        "rhino-cli"
        "present"
        "absent"
        "the canonical registry root is missing"

[<Fact>]
let ``a legacy snapshot renders sentinel dashes for a mapping without a behavior id`` () =
    let idlessMapping = { rhinoMapping with BehaviorId = None }
    let registry = withMapping idlessMapping baseRegistry

    let rows =
        expectOk "legacy-snapshot-idless-mapping" (snapshot registry SourceLegacy None)

    Assert.Equal<string list>([ "rhino-cli\t-\t-\t-" ], rows |> List.map renderRow)

[<Fact>]
let ``a legacy snapshot renders a dash for a mapping with no resolved runtimes`` () =
    let runtimelessMapping =
        { rhinoMapping with
            Canonical = canonicalHalf (Some "rhino-cli") (Some rhinoCorpus) [] }

    let registry = withMapping runtimelessMapping baseRegistry

    let rows =
        expectOk "legacy-snapshot-no-runtimes" (snapshot registry SourceLegacy None)

    Assert.Equal<string list>([ "rhino-cli\trhino-cli\trhino-cli:default\t-" ], rows |> List.map renderRow)

[<Fact>]
let ``a canonical snapshot renders sentinel dashes for a project row without a behavior id`` () =
    let idlessRow =
        { rhinoRow with
            Behavior = { rhinoBehavior with Id = None } }

    let registry = withRow idlessRow baseRegistry

    let rows =
        expectOk "canonical-snapshot-idless-row" (snapshot registry SourceCanonical (Some [ "rhino-cli" ]))

    Assert.Equal<string list>([ "rhino-cli\t-\t-\t-" ], rows |> List.map renderRow)

[<Fact>]
let ``a canonical snapshot falls back to derived runtimes for a delegate with no compatibility mapping`` () =
    let delegateRow = projectRow "rhino-cli-docs" ProfileTool Expanded rhinoBehavior
    let registry = withRow delegateRow baseRegistry

    let rows =
        expectOk "canonical-snapshot-delegate-fallback" (snapshot registry SourceCanonical (Some [ "rhino-cli-docs" ]))

    Assert.Equal<string list>(
        [ "rhino-cli-docs\trhino-cli\trhino-cli:default\tunit@rhino-cli" ],
        rows |> List.map renderRow
    )

[<Fact>]
let ``a canonical snapshot renders a dash when an owner resolves no runtimes`` () =
    let noRuntimeRow =
        { rhinoRow with
            Behavior =
                { rhinoBehavior with
                    Adapters = unownedAdapters } }

    let registry = withRow noRuntimeRow baseRegistry

    let rows =
        expectOk "canonical-snapshot-no-runtimes" (snapshot registry SourceCanonical (Some [ "rhino-cli" ]))

    Assert.Equal<string list>([ "rhino-cli\trhino-cli\trhino-cli:default\t-" ], rows |> List.map renderRow)

[<Fact>]
let ``comparing snapshots reports a project present only in the legacy snapshot`` () =
    let legacy =
        [ { Project = "rhino-cli"
            CanonicalOwner = "rhino-cli"
            BehaviorId = "rhino-cli:default"
            RuntimeIdentities = "unit@rhino-cli" } ]

    compareSnapshots legacy []
    |> expectContractFailure
        "snapshot-legacy-only"
        "rhino-cli"
        "rhino-cli"
        "present"
        "missing"
        "present in the legacy snapshot and missing from the canonical snapshot"

// ---------------------------------------------------------------------------
// Nx project enumeration edge cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``enumerateNxProjects falls back to the folder name and skips an unparsable project.json`` () =
    let root = newTempDir ()
    let noNameDir = Path.Combine(root, "apps", "no-name-project")
    Directory.CreateDirectory noNameDir |> ignore
    File.WriteAllText(Path.Combine(noNameDir, "project.json"), "{}")

    let brokenDir = Path.Combine(root, "apps", "broken-json-project")
    Directory.CreateDirectory brokenDir |> ignore
    File.WriteAllText(Path.Combine(brokenDir, "project.json"), "{ not valid json")

    let projects = enumerateNxProjects root

    Assert.Contains("no-name-project", projects)
    Assert.DoesNotContain("broken-json-project", projects)

// ---------------------------------------------------------------------------
// Owner fixture loading edge cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``loadFixture rejects a blank fixture path`` () =
    loadFixture (repositoryRoot ()) "O-PUB-RHINO" CheckCoverage ""
    |> expectMisuse "fixture-path-blank" "requires a repository-relative path"

[<Fact>]
let ``loadFixture rejects a fixture document that is not a JSON object`` () =
    let root = newTempDir ()
    let relative = seedFixture root "O-PUB-RHINO" "coverage-98.json" "[]\n"

    loadFixture root "O-PUB-RHINO" CheckCoverage relative
    |> expectMisuse "fixture-not-json-object" "expected a JSON object"

[<Fact>]
let ``loadFixture rejects a fixture whose internal check field disagrees with the requested check`` () =
    let root = newTempDir ()

    let body =
        coverageFixtureBody.Replace("\"check\": \"coverage\"", "\"check\": \"layout\"")

    let relative = seedFixture root "O-PUB-RHINO" "coverage-98.json" body

    loadFixture root "O-PUB-RHINO" CheckCoverage relative
    |> expectContractFailure
        "fixture-internal-check-mismatch"
        "check"
        "O-PUB-RHINO"
        "coverage"
        "layout"
        "check expected \"coverage\", found \"layout\""

[<Fact>]
let ``loadFixture rejects a fixture whose expected diagnostic omits a code`` () =
    let root = newTempDir ()

    let body =
        String.concat
            "\n"
            [ "{"
              sprintf "  \"schema\": \"%s\"," FixtureSchemaVersion
              "  \"owner-id\": \"O-PUB-RHINO\","
              "  \"check\": \"coverage\","
              "  \"mutation\": {"
              "    \"kind\": \"coverage-threshold\","
              "    \"slice\": \"apps/rhino-cli\","
              "    \"threshold\": 99,"
              "    \"covered-lines\": 98,"
              "    \"total-lines\": 100"
              "  },"
              "  \"expected-diagnostic\": { \"fields\": [] }"
              "}"
              "" ]

    let relative = seedFixture root "O-PUB-RHINO" "coverage-98.json" body

    loadFixture root "O-PUB-RHINO" CheckCoverage relative
    |> expectMisuse "fixture-diagnostic-code-missing" "expected-diagnostic.code is required"

[<Fact>]
let ``loadFixture defaults an owner fixture's implicit layers to an empty list`` () =
    let root = newTempDir ()

    let body =
        fixtureBody
            "O-PUB-RHINO"
            "layout"
            "layout-overlap"
            [ "    \"kind\": \"layout-overlap\","; "    \"path\": \"apps/rhino-cli\"" ]

    let relative = seedFixture root "O-PUB-RHINO" "layout-misplaced.json" body

    let document =
        expectOk "fixture-implicit-empty-layers" (loadFixture root "O-PUB-RHINO" CheckLayout relative)

    match document.Mutation with
    | LayoutOverlap(path, layers) ->
        Assert.Equal("apps/rhino-cli", path)
        Assert.Empty(layers)
    | other -> Assert.True(false, sprintf "expected a layout mutation but got %A" other)

// ---------------------------------------------------------------------------
// Fixture leaf mutation-shape edge cases
// ---------------------------------------------------------------------------

[<Fact>]
let ``the fixture leaf rejects an unknown layout mutation key`` () =
    let mutation =
        [ "    \"kind\": \"layout-overlap\","
          "    \"path\": \"apps/rhino-cli/tests/unit\","
          "    \"layers\": [\"unit\", \"integration\"],"
          "    \"note\": \"unexpected\"" ]

    let text =
        runFixtureLeaf "layout" "layout-misplaced.json" (fixtureBody "O-PUB-RHINO" "layout" "layout-overlap" mutation)
        |> expectExit "fixture-leaf-layout-unknown-key" 2

    Assert.True(
        containsOrdinal "unknown key \"note\"" text,
        sprintf "contract case 'fixture-leaf-layout-unknown-key': expected the unknown-key diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects a coverage mutation missing its numeric fields`` () =
    let mutation =
        [ "    \"kind\": \"coverage-threshold\","; "    \"slice\": \"apps/rhino-cli\"" ]

    let text =
        runFixtureLeaf
            "coverage"
            "coverage-98.json"
            (fixtureBody "O-PUB-RHINO" "coverage" "coverage-below-floor" mutation)
        |> expectExit "fixture-leaf-coverage-missing-numbers" 2

    Assert.True(
        containsOrdinal "requires slice, threshold, covered-lines, and total-lines" text,
        sprintf
            "contract case 'fixture-leaf-coverage-missing-numbers': expected the missing-fields diagnostic but got: %s"
            text
    )

[<Fact>]
let ``the fixture leaf rejects a non-integral coverage threshold`` () =
    let mutation =
        [ "    \"kind\": \"coverage-threshold\","
          "    \"slice\": \"apps/rhino-cli\","
          "    \"threshold\": 99.5,"
          "    \"covered-lines\": 98,"
          "    \"total-lines\": 100" ]

    let text =
        runFixtureLeaf
            "coverage"
            "coverage-98.json"
            (fixtureBody "O-PUB-RHINO" "coverage" "coverage-below-floor" mutation)
        |> expectExit "fixture-leaf-coverage-non-integral-threshold" 2

    Assert.True(
        containsOrdinal "requires slice, threshold, covered-lines, and total-lines" text,
        sprintf
            "contract case 'fixture-leaf-coverage-non-integral-threshold': expected the missing-fields diagnostic but got: %s"
            text
    )

[<Fact>]
let ``the fixture leaf rejects an unknown bdd mutation key`` () =
    let mutation =
        [ "    \"kind\": \"bdd-remove-binding\","
          "    \"feature\": \"specs/apps/rhino/cli/behaviors/specs/parity.feature\","
          "    \"scenario\": \"The manifest is current\","
          "    \"step\": \"Then the manifest is current\","
          "    \"adapter\": \"unit\","
          "    \"note\": \"unexpected\"" ]

    let text =
        runFixtureLeaf "bdd" "bdd-missing-step.json" (fixtureBody "O-PUB-RHINO" "bdd" "bdd-step-unbound" mutation)
        |> expectExit "fixture-leaf-bdd-unknown-key" 2

    Assert.True(
        containsOrdinal "unknown key \"note\"" text,
        sprintf "contract case 'fixture-leaf-bdd-unknown-key': expected the unknown-key diagnostic but got: %s" text
    )

[<Fact>]
let ``the fixture leaf rejects a bdd mutation missing its required fields`` () =
    let mutation =
        [ "    \"kind\": \"bdd-remove-binding\","
          "    \"feature\": \"specs/apps/rhino/cli/behaviors/specs/parity.feature\"" ]

    let text =
        runFixtureLeaf "bdd" "bdd-missing-step.json" (fixtureBody "O-PUB-RHINO" "bdd" "bdd-step-unbound" mutation)
        |> expectExit "fixture-leaf-bdd-missing-fields" 2

    Assert.True(
        containsOrdinal "requires feature, scenario, step, and adapter" text,
        sprintf
            "contract case 'fixture-leaf-bdd-missing-fields': expected the missing-fields diagnostic but got: %s"
            text
    )

[<Fact>]
let ``the fixture leaf rejects an unknown manifest mutation key`` () =
    let mutation =
        [ "    \"kind\": \"manifest-forwarder\","
          "    \"path\": \"apps/rhino-cli/package.json\","
          "    \"direct-consumers\": [],"
          "    \"script-name\": \"test\","
          "    \"script\": \"npx nx run rhino-cli:test\","
          "    \"note\": \"unexpected\"" ]

    let text =
        runFixtureLeaf
            "manifest"
            "manifest-proxy.json"
            (fixtureBody "O-PUB-RHINO" "manifest" "manifest-proxy-script" mutation)
        |> expectExit "fixture-leaf-manifest-unknown-key" 2

    Assert.True(
        containsOrdinal "unknown key \"note\"" text,
        sprintf
            "contract case 'fixture-leaf-manifest-unknown-key': expected the unknown-key diagnostic but got: %s"
            text
    )

[<Fact>]
let ``the fixture leaf rejects a manifest mutation missing its required fields`` () =
    let mutation =
        [ "    \"kind\": \"manifest-forwarder\","
          "    \"path\": \"apps/rhino-cli/package.json\"" ]

    let text =
        runFixtureLeaf
            "manifest"
            "manifest-proxy.json"
            (fixtureBody "O-PUB-RHINO" "manifest" "manifest-proxy-script" mutation)
        |> expectExit "fixture-leaf-manifest-missing-fields" 2

    Assert.True(
        containsOrdinal "requires path, script-name, and script" text,
        sprintf
            "contract case 'fixture-leaf-manifest-missing-fields': expected the missing-fields diagnostic but got: %s"
            text
    )

// ---------------------------------------------------------------------------
// The dual reader's own parse-level contract cases
// ---------------------------------------------------------------------------

/// A throwaway root seeded with an arbitrary `repo-config.yml` body, used by
/// the parse-level cases below to exercise the strict YAML reader directly
/// rather than through the `Registry`-typed builders above.
let private newRootWithConfig (yaml: string) : string =
    let root = newTempDir ()
    File.WriteAllText(Path.Combine(root, "repo-config.yml"), yaml)
    root

let private testingRootMissingSchemaYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects: []"
          "testing:"
          "  coverage:"
          "    minimum-line: 99"
          "    extra-key: 1"
          "  compatibility:"
          "    mappings: []"
          "  projects: []"
          "" ]

[<Fact>]
let ``parseRegistry rejects a canonical root missing its schema key alongside an unknown coverage key`` () =
    let text =
        match parseRegistry (newRootWithConfig testingRootMissingSchemaYaml) with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    Assert.Contains("testing.schema: required key is missing", text)
    Assert.Contains("testing.coverage: unknown key \"extra-key\"", text)

let private testingCoverageMissingMinimumLineYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects: []"
          "testing:"
          "  schema: ose-test-contract/v1"
          "  coverage: {}"
          "  compatibility:"
          "    mappings: []"
          "  projects: []"
          "" ]

[<Fact>]
let ``parseRegistry rejects a coverage block missing its minimum-line key`` () =
    parseRegistry (newRootWithConfig testingCoverageMissingMinimumLineYaml)
    |> expectContractFailure
        "coverage-minimum-line-missing"
        "testing.coverage.minimum-line"
        "repo-config.yml"
        "present"
        "absent"
        "testing.coverage.minimum-line: required key is missing"

let private testingCoverageAndCompatibilityMissingYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects: []"
          "testing:"
          "  schema: ose-test-contract/v1"
          "  projects: []"
          "" ]

[<Fact>]
let ``parseRegistry rejects a canonical root missing its coverage mapping`` () =
    parseRegistry (newRootWithConfig testingCoverageAndCompatibilityMissingYaml)
    |> expectContractFailure
        "coverage-block-missing"
        "testing.coverage"
        "repo-config.yml"
        "present"
        "absent"
        "testing.coverage: required mapping is missing"

let private testingCoverageNonNumericMinimumLineYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects: []"
          "testing:"
          "  schema: ose-test-contract/v1"
          "  coverage:"
          "    minimum-line: abc"
          "  compatibility:"
          "    mappings: []"
          "  projects: []"
          "" ]

[<Fact>]
let ``parseRegistry rejects a non-numeric coverage minimum-line`` () =
    parseRegistry (newRootWithConfig testingCoverageNonNumericMinimumLineYaml)
    |> expectContractFailure
        "coverage-minimum-line-non-numeric"
        "testing.coverage.minimum-line"
        "repo-config.yml"
        "99"
        "abc"
        "testing.coverage.minimum-line: invalid integer \"abc\""

let private testingProjectsKeyAbsentYaml =
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
          "" ]

[<Fact>]
let ``parseRegistry treats a canonical root without an explicit projects key as zero projects`` () =
    let registry =
        expectOk "testing-projects-key-absent" (parseRegistry (newRootWithConfig testingProjectsKeyAbsentYaml))

    Assert.Empty((Option.get registry.Testing).Projects)

[<Fact>]
let ``parseRegistry rejects a repository root without a repo-config.yml file`` () =
    parseRegistry (newTempDir ())
    |> expectMisuse "repo-config-file-missing" "repo-config.yml not found under"

[<Fact>]
let ``parseRegistry rejects an empty repo-config.yml file`` () =
    parseRegistry (newRootWithConfig "")
    |> expectContractFailure
        "repo-config-empty"
        "repo-config.yml"
        "repo-config.yml"
        "mapping"
        "empty"
        "repo-config.yml: expected a top-level mapping"

[<Fact>]
let ``parseRegistry rejects a repo-config.yml whose top-level node is a sequence`` () =
    let yaml = String.concat "\n" [ "- just"; "- a"; "- list"; "" ]

    parseRegistry (newRootWithConfig yaml)
    |> expectContractFailure
        "repo-config-sequence-root"
        "repo-config.yml"
        "repo-config.yml"
        "mapping"
        "sequence"
        "repo-config.yml: expected a top-level mapping"

[<Fact>]
let ``parseRegistry rejects a frozen coverage row missing its name and specs`` () =
    let yaml =
        String.concat "\n" [ "coverage:"; "  projects:"; "    - levels: [unit]"; "" ]

    parseRegistry (newRootWithConfig yaml)
    |> expectContractFailure
        "coverage-row-missing-name-and-specs"
        "coverage.projects[0]"
        "repo-config.yml"
        "present"
        "absent"
        "coverage.projects[0]: requires both a name and a specs glob"

[<Fact>]
let ``parseRegistry accepts a repo-config.yml without a canonical testing root`` () =
    let yaml = String.concat "\n" [ "coverage:"; "  projects: []"; "" ]
    let registry = expectOk "no-canonical-root" (parseRegistry (newRootWithConfig yaml))
    Assert.True(Option.isNone registry.Testing)

/// One project row per way `testing.projects[]` can be malformed. Every row
/// parses independently, so a single `parseRegistry` call aggregates every
/// finding in one pass instead of needing one fixture per defect.
let private malformedProjectRowsYaml =
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
          "    - project: dp1-bad-literals"
          "      profile: sideways"
          "      migration-state: sideways"
          "      behavior:"
          "        lifecycle-state: sideways"
          "        adapters:"
          "          unit:"
          "            disposition: sideways"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp2-adapter-unknown-key"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        lifecycle-state: bootstrap"
          "        seed:"
          "          target: test:seed"
          "          driver: apps/dp2/seed-driver.ts"
          "        adapters:"
          "          unit:"
          "            disposition: required"
          "            project: dp2-adapter-unknown-key"
          "            driver: apps/dp2/unit-driver.ts"
          "            note: unexpected"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp3-seed-missing-target"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        lifecycle-state: bootstrap"
          "        seed:"
          "          driver: apps/dp3/seed-driver.ts"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp4-seed-missing-driver"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        lifecycle-state: bootstrap"
          "        seed:"
          "          target: test:seed"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp5-seed-not-mapping"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        lifecycle-state: bootstrap"
          "        seed: not-a-mapping"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp6-adapter-entry-missing"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        adapters:"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp7-adapters-missing"
          "      profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        id: dp7-adapters-missing:default"
          "    - project: dp8-behavior-missing"
          "      profile: application"
          "      migration-state: expanded"
          "    - profile: application"
          "      migration-state: expanded"
          "      behavior:"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - not-a-mapping-project-row"
          "    - project: dp11-profile-not-scalar"
          "      profile: {}"
          "      migration-state: expanded"
          "      behavior:"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp12-migrating"
          "      profile: application"
          "      migration-state: migrating"
          "      behavior:"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "    - project: dp13-contracted"
          "      profile: application"
          "      migration-state: contracted"
          "      behavior:"
          "        adapters:"
          "          unit:"
          "            disposition: inapplicable"
          "          integration:"
          "            disposition: inapplicable"
          "          e2e:"
          "            disposition: inapplicable"
          "" ]

[<Fact>]
let ``parseRegistry aggregates every kind of malformed project row in one pass`` () =
    let text =
        match parseRegistry (newRootWithConfig malformedProjectRowsYaml) with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    // Catch-all literals: profile, migration-state, lifecycle-state, disposition.
    Assert.Contains("testing.projects[0].profile: invalid value \"sideways\"", text)
    Assert.Contains("testing.projects[0].migration-state: invalid value \"sideways\"", text)
    Assert.Contains("testing.projects[0].behavior.lifecycle-state: invalid value \"sideways\"", text)
    Assert.Contains("testing.projects[0].adapters.unit.disposition: invalid value \"sideways\"", text)

    // An unknown adapter key alongside an otherwise clean bootstrap seed.
    Assert.Contains("testing.projects[1].adapters.unit: unknown key \"note\"", text)

    // Seed shape defects: missing target, missing driver, not a mapping.
    Assert.Contains("testing.projects[2].seed.target: required key is missing", text)
    Assert.Contains("testing.projects[3].seed.driver: required key is missing", text)
    Assert.Contains("testing.projects[4].seed: required mapping is missing", text)

    // Missing adapter entry, missing adapters block, missing behavior block.
    Assert.Contains("testing.projects[5].adapters.unit: required adapter mapping is missing", text)
    Assert.Contains("testing.projects[6].adapters: required three-key mapping is missing", text)
    Assert.Contains("testing.projects[7].behavior: required mapping is missing", text)

    // Missing project key and a row that is not a mapping at all.
    Assert.Contains("testing.projects[8].project: required key is missing", text)
    Assert.Contains("testing.projects[9]: expected a mapping", text)

    // A profile declared as a mapping rather than a scalar renders as absent.
    Assert.Contains("testing.projects[10].profile: invalid value \"<absent>\"", text)

    // Rows 11 and 12 are otherwise clean and contribute no finding of their
    // own; they exist only to prove the "migrating" and "contracted"
    // migration-state literals also parse.
    Assert.DoesNotContain("testing.projects[11]", text)
    Assert.DoesNotContain("testing.projects[12]", text)

/// One compatibility mapping row per way `testing.compatibility.mappings[]`
/// can be malformed, aggregated the same way as the project rows above.
let private malformedMappingRowsYaml =
    String.concat
        "\n"
        [ "coverage:"
          "  projects: []"
          "testing:"
          "  schema: ose-test-contract/v1"
          "  coverage:"
          "    minimum-line: 99"
          "  compatibility:"
          "    mappings:"
          "      - project: dm1-redirected"
          "        state: redirected"
          "        legacy:"
          "          present: false"
          "        canonical:"
          "          owner: dm1-redirected"
          "          runtimes: []"
          "      - project: dm2-verified"
          "        state: verified"
          "        legacy:"
          "          present: false"
          "        canonical:"
          "          owner: dm2-verified"
          "          runtimes: []"
          "      - project: dm3-bad-state"
          "        state: sideways"
          "        legacy:"
          "          present: false"
          "        canonical:"
          "          owner: dm3-bad-state"
          "          runtimes: []"
          "      - project: dm4-bad-present"
          "        state: identity"
          "        legacy:"
          "          present: maybe"
          "        canonical:"
          "          owner: dm4-bad-present"
          "          runtimes: []"
          "      - project: dm5-legacy-missing"
          "        state: identity"
          "        canonical:"
          "          owner: dm5-legacy-missing"
          "          runtimes: []"
          "      - project: dm6-runtime-defects"
          "        state: identity"
          "        legacy:"
          "          present: false"
          "        canonical:"
          "          owner: dm6-runtime-defects"
          "          runtimes:"
          "            - level: unit"
          "              project: dm6-runtime-defects"
          "              note: unexpected"
          "            - level: integration"
          "            - not-a-mapping-runtime"
          "      - project: dm7-canonical-missing"
          "        state: identity"
          "        legacy:"
          "          present: false"
          "      - state: identity"
          "        legacy:"
          "          present: false"
          "        canonical:"
          "          owner: dm8-owner"
          "          runtimes: []"
          "      - not-a-mapping-row"
          "  projects: []"
          "" ]

[<Fact>]
let ``parseRegistry aggregates every kind of malformed compatibility mapping row in one pass`` () =
    let text =
        match parseRegistry (newRootWithConfig malformedMappingRowsYaml) with
        | Error(ContractFailure message) -> message
        | other -> failwith (sprintf "expected a contract failure but got %A" other)

    // The bad-state literal, since redirected/verified above it are the
    // otherwise-clean rows that prove the two accepted literals also parse.
    Assert.Contains("testing.compatibility.mappings[2].state: invalid value \"sideways\"", text)

    // An invalid legacy.present boolean and a row missing legacy entirely.
    Assert.Contains("testing.compatibility.mappings[3].legacy.present: invalid boolean \"maybe\"", text)
    Assert.Contains("testing.compatibility.mappings[4].legacy: required mapping is missing", text)

    // Runtime defects: unknown key, missing project, not a mapping.
    Assert.Contains("testing.compatibility.mappings[5].canonical.runtimes[0]: unknown key \"note\"", text)

    Assert.Contains(
        "testing.compatibility.mappings[5].canonical.runtimes[1]: requires both a level and a project",
        text
    )

    Assert.Contains("testing.compatibility.mappings[5].canonical.runtimes[2]: expected a mapping", text)

    // Missing canonical block, missing project key, and a non-mapping row.
    Assert.Contains("testing.compatibility.mappings[6].canonical: required mapping is missing", text)
    Assert.Contains("testing.compatibility.mappings[7].project: required key is missing", text)
    Assert.Contains("testing.compatibility.mappings[8]: expected a mapping", text)
