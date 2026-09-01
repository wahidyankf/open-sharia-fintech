/// The `ose-test-contract/v1` registry: its typed surface, its strict dual
/// reader over `repo-config.yml`, and the read-only operations behind the
/// `test-contract` CLI grammar described by
/// [Registry Schema and Migration Contract](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/gherkin-coverage-and-adapter-design.md)
/// and the
/// [Owner RED Fixture Injection Contract](../../../../../plans/in-progress/adopt-beavernest-test-automation/tech-docs/target-contract-and-project-matrix.md).
///
/// Reader boundary: nothing here writes a tracked byte. The parser opens
/// `repo-config.yml` read-only, fixture overlays are applied to an in-memory
/// registry projection only, and `project.json`, specs, and tests are never
/// rewritten.
///
/// Failure separation follows the migration contract's exit codes: `Misuse`
/// is CLI or input misuse (exit 2) and `ContractFailure` is a contract
/// violation (exit 1). A contract failure carries every finding, newline
/// joined, so one run reports the whole violation set rather than only its
/// first member.
module RhinoCli.Application.TestContract

open System
open System.Globalization
open System.IO
open System.Text.Json
open YamlDotNet.RepresentationModel

/// The four project profiles a `testing.projects[].profile` may declare.
type Profile =
    | ProfileApplication
    | ProfileLibrary
    | ProfileTool
    | ProfileE2e

/// The four `testing.projects[].migration-state` values. Only the adjacent
/// forward transitions `expanded -> migrating -> verified -> contracted` are
/// legal; skipping or reversing fails closed.
type MigrationState =
    | Expanded
    | Migrating
    | Verified
    | Contracted

/// The two `behavior.lifecycle-state` values. Absent when `behavior.owner`
/// is null.
type LifecycleState =
    | Bootstrap
    | Active

/// The three adapter dispositions. `Required` and `Delegated` carry a project
/// and driver; `Inapplicable` carries a non-blank reason instead.
type Disposition =
    | Required
    | Delegated
    | Inapplicable

/// The three `testing.compatibility.mappings[].state` values. Only
/// `identity -> redirected -> verified` and `identity -> verified` are legal.
type MappingState =
    | MappingIdentity
    | MappingRedirected
    | MappingVerified

/// One of the exactly three adapter entries under `behavior.adapters`.
type AdapterEntry =
    { Disposition: Disposition
      Project: string option
      Driver: string option
      Reason: string option }

/// The closed three-key `behavior.adapters` mapping. A fourth adapter or an
/// omitted adapter is a schema failure, so this is a record rather than a map.
type Adapters =
    { Unit: AdapterEntry
      Integration: AdapterEntry
      E2e: AdapterEntry }

/// The bounded seed contract required by, and only by, a `bootstrap` owner.
type Seed = { Target: string; Driver: string }

/// The `testing.projects[].behavior` block. `Id` and `LifecycleState` are
/// absent exactly when `Owner` is `None`.
type Behavior =
    { Id: string option
      LifecycleState: LifecycleState option
      Owner: string option
      Corpus: string list
      Seed: Seed option
      Adapters: Adapters }

/// One canonical `testing.projects[]` row.
type ProjectRow =
    { Project: string
      Profile: Profile
      MigrationState: MigrationState
      Behavior: Behavior }

/// The immutable half of a compatibility map, frozen from `coverage.projects`.
type LegacyHalf =
    { Present: bool
      Corpus: string option
      Levels: string list }

/// One resolved `<level>@<runtime-project>` identity.
type RuntimeIdentity = { Level: string; Project: string }

/// The mutable half of a compatibility map, tracking the current canonical
/// owner, corpus, and resolved runtimes.
type CanonicalHalf =
    { Owner: string option
      Corpus: string option
      Runtimes: RuntimeIdentity list }

/// One `testing.compatibility.mappings[]` row. Exactly one exists per Nx
/// project until contraction, including projects legacy omitted.
type CompatibilityMapping =
    { Project: string
      BehaviorId: string option
      State: MappingState
      Legacy: LegacyHalf
      Canonical: CanonicalHalf }

/// The repository coverage floor. Never a per-project override.
type CoverageFloor = { MinimumLine: int }

/// The parsed `testing:` root.
type TestingRegistry =
    { Schema: string
      Coverage: CoverageFloor
      Mappings: CompatibilityMapping list
      Projects: ProjectRow list }

/// One frozen `coverage.projects[]` row. Read-only comparison source.
type LegacyProject =
    { Name: string
      Levels: string list
      Specs: string }

/// Both halves of the dual reader: the frozen legacy block and the canonical
/// `testing:` root, which is absent before expansion.
type Registry =
    { Legacy: LegacyProject list
      Testing: TestingRegistry option }

/// Which side of the dual reader a snapshot projects.
type SnapshotSource =
    | SourceLegacy
    | SourceCanonical

/// One sorted UTF-8 TSV row:
/// `project<TAB>canonical-owner<TAB>behavior-id<TAB>runtime-identities`.
/// A legacy-absent project renders `-` in the last three columns.
type SnapshotRow =
    { Project: string
      CanonicalOwner: string
      BehaviorId: string
      RuntimeIdentities: string }

/// The four owner checks a fixture may target.
type FixtureCheck =
    | CheckLayout
    | CheckCoverage
    | CheckBdd
    | CheckManifest

/// The four closed, typed fixture mutation payloads. Any other kind, or an
/// unknown key inside one, is misuse.
type FixtureMutation =
    | LayoutOverlap of path: string * layers: string list
    | CoverageThreshold of slice: string * threshold: int * coveredLines: int * totalLines: int
    | BddRemoveBinding of feature: string * scenario: string * step: string * adapter: string
    | ManifestForwarder of path: string * directConsumers: string list * scriptName: string * script: string

/// The diagnostic a fixture asserts the validator emits.
type ExpectedDiagnostic = { Code: string; Fields: string list }

/// One `ose-test-contract-owner-fixture/v1` document.
type FixtureDocument =
    { Schema: string
      OwnerId: string
      Check: FixtureCheck
      Mutation: FixtureMutation
      ExpectedDiagnostic: ExpectedDiagnostic }

/// Separates CLI or input misuse (exit 2) from a contract failure (exit 1).
type Failure =
    | Misuse of string
    | ContractFailure of string

/// The `registry validate` success line's fields.
type ValidateReport =
    { State: string
      Projects: int
      BootstrapCount: int
      ActiveCount: int
      LegacyPresent: bool
      CompatibilityPresent: bool }

/// The `registry validate-mapping` success line's fields.
type MappingReport = { State: string; Mappings: int }

/// Options accepted by `registry validate`.
type ValidateOptions =
    { RequireState: MigrationState option
      RequireBehaviorState: LifecycleState option
      AllowBootstrap: string list
      ForbidLegacy: bool
      ForbidCompatibility: bool }

/// The no-flag `registry validate` shape.
let defaultValidateOptions: ValidateOptions =
    { RequireState = None
      RequireBehaviorState = None
      AllowBootstrap = []
      ForbidLegacy = false
      ForbidCompatibility = false }

// ---------------------------------------------------------------------------
// Names, paths, and identities
// ---------------------------------------------------------------------------

/// The exact schema string the strict parser selects on.
[<Literal>]
let SchemaVersion = "ose-test-contract/v1"

/// The exact repository coverage floor. Never a per-project override.
[<Literal>]
let MinimumLine = 99

/// The exact owner fixture schema string.
[<Literal>]
let FixtureSchemaVersion = "ose-test-contract-owner-fixture/v1"

/// The only directory an owner fixture may be resolved from.
[<Literal>]
let FixtureRoot = "apps/rhino-cli/tests/fixtures/test-contract/owners"

let private absentMarker = "<absent>"
let private blankMarker = "<blank>"
let private levelNames = [ "unit"; "integration"; "e2e" ]

let private migrationStateName (state: MigrationState) : string =
    match state with
    | Expanded -> "expanded"
    | Migrating -> "migrating"
    | Verified -> "verified"
    | Contracted -> "contracted"

let private migrationStateRank (state: MigrationState) : int =
    match state with
    | Expanded -> 0
    | Migrating -> 1
    | Verified -> 2
    | Contracted -> 3

let private lifecycleName (state: LifecycleState) : string =
    match state with
    | Bootstrap -> "bootstrap"
    | Active -> "active"

let private mappingStateName (state: MappingState) : string =
    match state with
    | MappingIdentity -> "identity"
    | MappingRedirected -> "redirected"
    | MappingVerified -> "verified"

let private mappingStateRank (state: MappingState) : int =
    match state with
    | MappingIdentity -> 0
    | MappingRedirected -> 1
    | MappingVerified -> 2

let private dispositionName (disposition: Disposition) : string =
    match disposition with
    | Required -> "required"
    | Delegated -> "delegated"
    | Inapplicable -> "inapplicable"

let private checkName (check: FixtureCheck) : string =
    match check with
    | CheckLayout -> "layout"
    | CheckCoverage -> "coverage"
    | CheckBdd -> "bdd"
    | CheckManifest -> "manifest"

/// The four allowed fixture file names, each bound to exactly one check.
let private fixtureFiles: (string * FixtureCheck) list =
    [ "layout-misplaced.json", CheckLayout
      "coverage-98.json", CheckCoverage
      "bdd-missing-step.json", CheckBdd
      "manifest-proxy.json", CheckManifest ]

let private isBlank (value: string) : bool = String.IsNullOrWhiteSpace value

/// Renders a value for a diagnostic, collapsing absence and blankness into
/// the two stable placeholders the contract cases assert against.
let private render (value: string option) : string =
    match value with
    | None -> absentMarker
    | Some raw when isBlank raw -> blankMarker
    | Some raw -> raw

/// Repository-relative rendering: forward slashes, no `./` prefix, no
/// duplicate or trailing separator. Two raw spellings of one location
/// normalize to one identity, which is what lets a controlled move stay
/// identity stable.
let private normalizePath (value: string) : string =
    let unified = value.Replace('\\', '/')

    let collapsed =
        unified.Split('/')
        |> Array.filter (fun segment -> segment <> "" && segment <> ".")
        |> String.concat "/"

    if unified.StartsWith("/", StringComparison.Ordinal) then
        "/" + collapsed
    else
        collapsed

let private isAbsolutePath (value: string) : bool =
    value.StartsWith("/", StringComparison.Ordinal)
    || (value.Length > 1 && value.[1] = ':')

let private hasTraversal (value: string) : bool =
    value.Replace('\\', '/').Split('/')
    |> Array.exists (fun segment -> segment = "..")

/// The single path finding a repository-relative value may carry, or `None`
/// when the value is a usable repository-relative path.
let private pathFinding (field: string) (project: string) (value: string) : string option =
    if isBlank value then
        Some(sprintf "%s: %s declares a blank path" field project)
    elif isAbsolutePath value then
        Some(sprintf "%s: %s declares an absolute path \"%s\"" field project value)
    elif hasTraversal value then
        Some(sprintf "%s: %s declares a traversal path \"%s\"" field project value)
    else
        None

/// Renders a level list the one way every diagnostic spells it: sorted, so
/// two orderings of the same set never read as a difference.
let private renderLevels (levels: string list) : string = String.concat "," (List.sort levels)

/// Compares two optional repository-relative paths by normalized identity, so
/// a raw re-spelling of one location is not reported as a move.
let private sameNormalizedPath (left: string option) (right: string option) : bool =
    match left, right with
    | None, None -> true
    | Some left, Some right -> normalizePath left = normalizePath right
    | _ -> false

let private runtimeIdentity (runtime: RuntimeIdentity) : string =
    sprintf "%s@%s" runtime.Level runtime.Project

let private sortRuntimes (runtimes: RuntimeIdentity list) : RuntimeIdentity list =
    runtimes |> List.sortBy (fun runtime -> runtime.Level, runtime.Project)

let private adapterOf (adapters: Adapters) (level: string) : AdapterEntry =
    match level with
    | "unit" -> adapters.Unit
    | "integration" -> adapters.Integration
    | _ -> adapters.E2e

/// The runtime identities a row's own adapters resolve to, sorted.
let private derivedRuntimes (row: ProjectRow) : RuntimeIdentity list =
    levelNames
    |> List.choose (fun level ->
        let entry = adapterOf row.Behavior.Adapters level

        match entry.Disposition, entry.Project with
        | Inapplicable, _ -> None
        | _, None -> None
        | _, Some target -> Some { Level = level; Project = target })
    |> sortRuntimes

let private isOwnerRow (row: ProjectRow) : bool =
    match row.Behavior.Owner with
    | Some owner -> owner = row.Project
    | None -> false

let private duplicates (values: string list) : string list =
    values
    |> List.countBy id
    |> List.filter (fun (_, count) -> count > 1)
    |> List.map fst
    |> List.sort

// ---------------------------------------------------------------------------
// Strict YAML reader
// ---------------------------------------------------------------------------

let private scalarText (node: YamlNode) : string option =
    match node with
    | :? YamlScalarNode as scalar ->
        match scalar.Value with
        | null -> None
        | value when
            scalar.Style = YamlDotNet.Core.ScalarStyle.Plain
            && (value = "null" || value = "~" || value = "")
            ->
            None
        | value -> Some value
    | _ -> None

let private childNode (mapping: YamlMappingNode) (key: string) : YamlNode option =
    mapping.Children
    |> Seq.tryPick (fun pair ->
        match pair.Key with
        | :? YamlScalarNode as scalar when scalar.Value = key -> Some pair.Value
        | _ -> None)

let private childMapping (mapping: YamlMappingNode) (key: string) : YamlMappingNode option =
    match childNode mapping key with
    | Some(:? YamlMappingNode as child) -> Some child
    | _ -> None

let private childSequence (mapping: YamlMappingNode) (key: string) : YamlNode list =
    match childNode mapping key with
    | Some(:? YamlSequenceNode as sequence) -> List.ofSeq (Seq.cast<YamlNode> sequence)
    | _ -> []

let private childScalar (mapping: YamlMappingNode) (key: string) : string option =
    childNode mapping key |> Option.bind scalarText

let private childStrings (mapping: YamlMappingNode) (key: string) : string list =
    childSequence mapping key |> List.choose scalarText

let private keyNames (mapping: YamlMappingNode) : string list =
    mapping.Children
    |> Seq.choose (fun pair ->
        match pair.Key with
        | :? YamlScalarNode as scalar when not (isNull scalar.Value) -> Some scalar.Value
        | _ -> None)
    |> List.ofSeq

/// Fails closed on any key the `ose-test-contract/v1` schema does not declare.
let private rejectUnknownKeys (where: string) (allowed: string list) (mapping: YamlMappingNode) : string list =
    keyNames mapping
    |> List.filter (fun name -> not (List.contains name allowed))
    |> List.map (fun name -> sprintf "%s: unknown key \"%s\"" where name)

let private parseProfile (where: string) (raw: string option) : Result<Profile, string> =
    match raw with
    | Some "application" -> Ok ProfileApplication
    | Some "library" -> Ok ProfileLibrary
    | Some "tool" -> Ok ProfileTool
    | Some "e2e" -> Ok ProfileE2e
    | other -> Error(sprintf "%s.profile: invalid value \"%s\"" where (render other))

let private parseMigrationState (where: string) (raw: string option) : Result<MigrationState, string> =
    match raw with
    | Some "expanded" -> Ok Expanded
    | Some "migrating" -> Ok Migrating
    | Some "verified" -> Ok Verified
    | Some "contracted" -> Ok Contracted
    | other -> Error(sprintf "%s.migration-state: invalid value \"%s\"" where (render other))

let private parseLifecycle (where: string) (raw: string option) : Result<LifecycleState option, string> =
    match raw with
    | None -> Ok None
    | Some "bootstrap" -> Ok(Some Bootstrap)
    | Some "active" -> Ok(Some Active)
    | other -> Error(sprintf "%s.behavior.lifecycle-state: invalid value \"%s\"" where (render other))

let private parseDisposition (where: string) (raw: string option) : Result<Disposition, string> =
    match raw with
    | Some "required" -> Ok Required
    | Some "delegated" -> Ok Delegated
    | Some "inapplicable" -> Ok Inapplicable
    | other -> Error(sprintf "%s.disposition: invalid value \"%s\"" where (render other))

let private parseMappingState (where: string) (raw: string option) : Result<MappingState, string> =
    match raw with
    | Some "identity" -> Ok MappingIdentity
    | Some "redirected" -> Ok MappingRedirected
    | Some "verified" -> Ok MappingVerified
    | other -> Error(sprintf "%s.state: invalid value \"%s\"" where (render other))

let private parseBool (where: string) (raw: string option) : Result<bool, string> =
    match raw with
    | Some "true" -> Ok true
    | Some "false" -> Ok false
    | other -> Error(sprintf "%s: invalid boolean \"%s\"" where (render other))

let private parseInt (where: string) (raw: string option) : Result<int, string> =
    match raw with
    | Some value ->
        match Int32.TryParse(value, NumberStyles.Integer, CultureInfo.InvariantCulture) with
        | true, parsed -> Ok parsed
        | _ -> Error(sprintf "%s: invalid integer \"%s\"" where value)
    | None -> Error(sprintf "%s: required key is missing" where)

let private errorsOf (results: Result<'a, string> list) : string list =
    results
    |> List.choose (fun result ->
        match result with
        | Error message -> Some message
        | Ok _ -> None)

let private valuesOf (results: Result<'a, string> list) : 'a list =
    results
    |> List.choose (fun result ->
        match result with
        | Ok value -> Some value
        | Error _ -> None)

let private errorsOfMany (results: Result<'a, string list> list) : string list =
    results
    |> List.collect (fun result ->
        match result with
        | Error messages -> messages
        | Ok _ -> [])

let private valuesOfMany (results: Result<'a, string list> list) : 'a list =
    results
    |> List.choose (fun result ->
        match result with
        | Ok value -> Some value
        | Error _ -> None)

let private parseAdapterEntry (where: string) (node: YamlNode option) : Result<AdapterEntry, string> =
    match node with
    | Some(:? YamlMappingNode as mapping) ->
        let unknown =
            rejectUnknownKeys where [ "disposition"; "project"; "driver"; "reason" ] mapping

        match unknown with
        | first :: _ -> Error first
        | [] ->
            parseDisposition where (childScalar mapping "disposition")
            |> Result.map (fun disposition ->
                { Disposition = disposition
                  Project = childScalar mapping "project"
                  Driver = childScalar mapping "driver"
                  Reason = childScalar mapping "reason" })
    | _ -> Error(sprintf "%s: required adapter mapping is missing" where)

let private parseAdapters (where: string) (node: YamlNode option) : Result<Adapters, string list> =
    match node with
    | Some(:? YamlMappingNode as mapping) ->
        let unknown = rejectUnknownKeys (where + ".adapters") levelNames mapping

        let entries =
            levelNames
            |> List.map (fun level ->
                parseAdapterEntry (sprintf "%s.adapters.%s" where level) (childNode mapping level))

        match errorsOf entries @ unknown with
        | [] ->
            let parsed = valuesOf entries

            Ok
                { Unit = parsed.[0]
                  Integration = parsed.[1]
                  E2e = parsed.[2] }
        | findings -> Error findings
    | _ -> Error [ sprintf "%s.adapters: required three-key mapping is missing" where ]

let private parseSeed (where: string) (node: YamlNode option) : Result<Seed option, string list> =
    match node with
    | None -> Ok None
    | Some(:? YamlMappingNode as mapping) ->
        let unknown = rejectUnknownKeys (where + ".seed") [ "target"; "driver" ] mapping

        let target = childScalar mapping "target"
        let driver = childScalar mapping "driver"

        let missing =
            [ if Option.isNone target then
                  yield sprintf "%s.seed.target: required key is missing" where
              if Option.isNone driver then
                  yield sprintf "%s.seed.driver: required key is missing" where ]

        match unknown @ missing with
        | [] ->
            Ok(
                Some
                    { Target = defaultArg target ""
                      Driver = defaultArg driver "" }
            )
        | findings -> Error findings
    | Some _ -> Error [ sprintf "%s.seed: required mapping is missing" where ]

let private parseBehavior (where: string) (node: YamlNode option) : Result<Behavior, string list> =
    match node with
    | Some(:? YamlMappingNode as mapping) ->
        let unknown =
            rejectUnknownKeys
                (where + ".behavior")
                [ "id"; "lifecycle-state"; "owner"; "corpus"; "seed"; "adapters" ]
                mapping

        let lifecycle = parseLifecycle where (childScalar mapping "lifecycle-state")
        let seed = parseSeed where (childNode mapping "seed")
        let adapters = parseAdapters where (childNode mapping "adapters")

        let findings =
            unknown
            @ errorsOf [ lifecycle ]
            @ errorsOfMany [ Result.map ignore seed ]
            @ errorsOfMany [ Result.map ignore adapters ]

        match findings, lifecycle, seed, adapters with
        | [], Ok lifecycle, Ok seed, Ok adapters ->
            Ok
                { Id = childScalar mapping "id"
                  LifecycleState = lifecycle
                  Owner = childScalar mapping "owner"
                  Corpus = childStrings mapping "corpus"
                  Seed = seed
                  Adapters = adapters }
        | findings, _, _, _ -> Error findings
    | _ -> Error [ sprintf "%s.behavior: required mapping is missing" where ]

let private parseProjectRow (index: int) (node: YamlNode) : Result<ProjectRow, string list> =
    match node with
    | :? YamlMappingNode as mapping ->
        let where = sprintf "testing.projects[%d]" index

        let unknown =
            rejectUnknownKeys where [ "project"; "profile"; "migration-state"; "behavior" ] mapping

        let project = childScalar mapping "project"
        let profile = parseProfile where (childScalar mapping "profile")
        let state = parseMigrationState where (childScalar mapping "migration-state")
        let behavior = parseBehavior where (childNode mapping "behavior")

        let findings =
            unknown
            @ [ if Option.isNone project then
                    yield sprintf "%s.project: required key is missing" where ]
            @ errorsOf [ profile ]
            @ errorsOf [ state ]
            @ errorsOfMany [ Result.map ignore behavior ]

        match findings, project, profile, state, behavior with
        | [], Some project, Ok profile, Ok state, Ok behavior ->
            Ok
                { Project = project
                  Profile = profile
                  MigrationState = state
                  Behavior = behavior }
        | findings, _, _, _, _ -> Error findings
    | _ -> Error [ sprintf "testing.projects[%d]: expected a mapping" index ]

let private parseLegacyHalf (where: string) (node: YamlNode option) : Result<LegacyHalf, string list> =
    match node with
    | Some(:? YamlMappingNode as mapping) ->
        let unknown = rejectUnknownKeys where [ "present"; "corpus"; "levels" ] mapping
        let present = parseBool (where + ".present") (childScalar mapping "present")

        match unknown @ errorsOf [ present ], present with
        | [], Ok present ->
            Ok
                { Present = present
                  Corpus = childScalar mapping "corpus"
                  Levels = childStrings mapping "levels" }
        | findings, _ -> Error findings
    | _ -> Error [ sprintf "%s: required mapping is missing" where ]

let private parseRuntime (where: string) (index: int) (node: YamlNode) : Result<RuntimeIdentity, string> =
    match node with
    | :? YamlMappingNode as mapping ->
        let unknown =
            rejectUnknownKeys (sprintf "%s[%d]" where index) [ "level"; "project" ] mapping

        match unknown, childScalar mapping "level", childScalar mapping "project" with
        | [], Some level, Some project -> Ok { Level = level; Project = project }
        | first :: _, _, _ -> Error first
        | [], _, _ -> Error(sprintf "%s[%d]: requires both a level and a project" where index)
    | _ -> Error(sprintf "%s[%d]: expected a mapping" where index)

let private parseCanonicalHalf (where: string) (node: YamlNode option) : Result<CanonicalHalf, string list> =
    match node with
    | Some(:? YamlMappingNode as mapping) ->
        let unknown = rejectUnknownKeys where [ "owner"; "corpus"; "runtimes" ] mapping

        let runtimes =
            childSequence mapping "runtimes"
            |> List.mapi (fun index node -> parseRuntime (where + ".runtimes") index node)

        match unknown @ errorsOf runtimes with
        | [] ->
            Ok
                { Owner = childScalar mapping "owner"
                  Corpus = childScalar mapping "corpus"
                  Runtimes = valuesOf runtimes }
        | findings -> Error findings
    | _ -> Error [ sprintf "%s: required mapping is missing" where ]

let private parseMappingRow (index: int) (node: YamlNode) : Result<CompatibilityMapping, string list> =
    match node with
    | :? YamlMappingNode as mapping ->
        let where = sprintf "testing.compatibility.mappings[%d]" index

        let unknown =
            rejectUnknownKeys where [ "project"; "behavior-id"; "state"; "legacy"; "canonical" ] mapping

        let project = childScalar mapping "project"
        let state = parseMappingState where (childScalar mapping "state")
        let legacy = parseLegacyHalf (where + ".legacy") (childNode mapping "legacy")

        let canonical =
            parseCanonicalHalf (where + ".canonical") (childNode mapping "canonical")

        let findings =
            unknown
            @ [ if Option.isNone project then
                    yield sprintf "%s.project: required key is missing" where ]
            @ errorsOf [ state ]
            @ errorsOfMany [ Result.map ignore legacy ]
            @ errorsOfMany [ Result.map ignore canonical ]

        match findings, project, state, legacy, canonical with
        | [], Some project, Ok state, Ok legacy, Ok canonical ->
            Ok
                { Project = project
                  BehaviorId = childScalar mapping "behavior-id"
                  State = state
                  Legacy = legacy
                  Canonical = canonical }
        | findings, _, _, _, _ -> Error findings
    | _ -> Error [ sprintf "testing.compatibility.mappings[%d]: expected a mapping" index ]

let private parseTesting (mapping: YamlMappingNode) : Result<TestingRegistry, string list> =
    let unknown =
        rejectUnknownKeys "testing" [ "schema"; "coverage"; "compatibility"; "projects" ] mapping

    let schema =
        match childScalar mapping "schema" with
        | Some schema -> Ok schema
        | None -> Error "testing.schema: required key is missing"

    let floor =
        match childMapping mapping "coverage" with
        | Some coverage ->
            let unknownCoverage =
                rejectUnknownKeys "testing.coverage" [ "minimum-line" ] coverage

            match unknownCoverage with
            | first :: _ -> Error first
            | [] ->
                parseInt "testing.coverage.minimum-line" (childScalar coverage "minimum-line")
                |> Result.map (fun value -> { MinimumLine = value })
        | None -> Error "testing.coverage: required mapping is missing"

    let compatibilityUnknown, mappingResults =
        match childMapping mapping "compatibility" with
        | Some compatibility ->
            rejectUnknownKeys "testing.compatibility" [ "mappings" ] compatibility,
            childSequence compatibility "mappings" |> List.mapi parseMappingRow
        | None -> [], []

    let projectResults = childSequence mapping "projects" |> List.mapi parseProjectRow

    let findings =
        unknown
        @ errorsOf [ schema ]
        @ errorsOf [ floor ]
        @ compatibilityUnknown
        @ errorsOfMany mappingResults
        @ errorsOfMany projectResults

    match findings, schema, floor with
    | [], Ok schema, Ok floor ->
        Ok
            { Schema = schema
              Coverage = floor
              Mappings = valuesOfMany mappingResults
              Projects = valuesOfMany projectResults }
    | findings, _, _ -> Error findings

/// Parses the frozen `coverage.projects` block and the canonical `testing:`
/// root out of `<repoRoot>/repo-config.yml` without mutating either.
let parseRegistry (repoRoot: string) : Result<Registry, Failure> =
    let path = Path.Combine(repoRoot, "repo-config.yml")

    if not (File.Exists path) then
        Error(Misuse(sprintf "repo-config.yml not found under \"%s\"" repoRoot))
    else

        let data = File.ReadAllText path
        let stream = YamlStream()
        use reader = new StringReader(data)
        stream.Load reader

        let root =
            if stream.Documents.Count = 0 then
                None
            else
                match stream.Documents.[0].RootNode with
                | :? YamlMappingNode as mapping -> Some mapping
                | _ -> None

        match root with
        | None -> Error(ContractFailure "repo-config.yml: expected a top-level mapping")
        | Some root ->

            // The frozen half belongs to the `repo-config.yml` reader; only
            // the canonical `testing:` root is parsed here.
            match RepoConfig.parseCoverageProjects data with
            | Error findings -> Error(ContractFailure(String.concat "\n" findings))
            | Ok frozen ->
                let legacy =
                    frozen
                    |> List.map (fun row ->
                        { Name = row.Name
                          Levels = row.Levels
                          Specs = row.Specs })

                match childMapping root "testing" with
                | None -> Ok { Legacy = legacy; Testing = None }
                | Some testing ->
                    match parseTesting testing with
                    | Error findings -> Error(ContractFailure(String.concat "\n" findings))
                    | Ok testing ->
                        Ok
                            { Legacy = legacy
                              Testing = Some testing }

// ---------------------------------------------------------------------------
// validate
// ---------------------------------------------------------------------------

let private adapterFindings
    (row: ProjectRow)
    (rowsByProject: Map<string, ProjectRow>)
    (nxProjects: string list)
    : string list =
    levelNames
    |> List.collect (fun level ->
        let field = sprintf "behavior.adapters.%s" level
        let entry = adapterOf row.Behavior.Adapters level

        let conditional =
            match entry.Disposition with
            | Inapplicable ->
                [ match entry.Project with
                  | Some target ->
                      yield
                          sprintf "%s.project: %s declares \"%s\" on an inapplicable adapter" field row.Project target
                  | None -> ()
                  match entry.Driver with
                  | Some driver ->
                      yield sprintf "%s.driver: %s declares \"%s\" on an inapplicable adapter" field row.Project driver
                  | None -> ()
                  match entry.Reason with
                  | Some reason when not (isBlank reason) -> ()
                  | reason ->
                      yield
                          sprintf
                              "%s.reason: %s must explain an inapplicable adapter, found \"%s\""
                              field
                              row.Project
                              (render reason) ]
            | Required
            | Delegated ->
                [ match entry.Project with
                  | None -> yield sprintf "%s.project: %s omits the required adapter project" field row.Project
                  | Some target ->
                      if entry.Disposition = Required && target <> row.Project then
                          yield
                              sprintf
                                  "%s.project: %s must host its own required adapter, found \"%s\""
                                  field
                                  row.Project
                                  target
                      elif entry.Disposition = Delegated && target = row.Project then
                          yield sprintf "%s.project: %s cannot delegate an adapter to itself" field row.Project
                      elif not (List.contains target nxProjects) then
                          yield
                              sprintf
                                  "%s.project: %s names \"%s\", which is not an Nx project"
                                  field
                                  row.Project
                                  target
                  match entry.Driver with
                  | None -> yield sprintf "%s.driver: %s omits the required adapter driver" field row.Project
                  | Some driver ->
                      match pathFinding (field + ".driver") row.Project driver with
                      | Some finding -> yield finding
                      | None -> ()
                  match entry.Reason with
                  | Some reason ->
                      yield
                          sprintf
                              "%s.reason: %s declares \"%s\" on a %s adapter"
                              field
                              row.Project
                              reason
                              (dispositionName entry.Disposition)
                  | None -> () ]

        let delegation =
            match entry.Disposition, entry.Project with
            | Delegated, Some target when target <> row.Project ->
                match Map.tryFind target rowsByProject with
                | None -> []
                | Some targetRow ->
                    let reciprocal = adapterOf targetRow.Behavior.Adapters level

                    match reciprocal.Disposition with
                    | Delegated when reciprocal.Project = Some row.Project ->
                        [ sprintf
                              "%s.project: %s and %s declare a reciprocal delegation cycle at the %s level"
                              field
                              row.Project
                              target
                              level ]
                    | Required when reciprocal.Project = Some target -> []
                    | other ->
                        [ sprintf
                              "%s.project: %s delegates to %s, which declares \"%s\" rather than hosting the %s adapter"
                              field
                              row.Project
                              target
                              (dispositionName other)
                              level ]
            | _ -> []

        conditional @ delegation)

let private behaviorFindings
    (row: ProjectRow)
    (rowsByProject: Map<string, ProjectRow>)
    (nxProjects: string list)
    : string list =
    let behavior = row.Behavior

    match behavior.Owner with
    | None ->
        [ match behavior.Id with
          | Some id -> yield sprintf "behavior.id: %s owns no behavior but declares \"%s\"" row.Project id
          | None -> ()
          match behavior.LifecycleState with
          | Some state ->
              yield
                  sprintf
                      "behavior.lifecycle-state: %s owns no behavior but declares \"%s\""
                      row.Project
                      (lifecycleName state)
          | None -> ()
          match behavior.Seed with
          | Some seed -> yield sprintf "behavior.seed: %s owns no behavior but declares \"%s\"" row.Project seed.Target
          | None -> ()
          if not (List.isEmpty behavior.Corpus) then
              yield sprintf "behavior.corpus: %s owns no behavior but declares a corpus" row.Project
          for level in levelNames do
              let entry = adapterOf behavior.Adapters level

              if entry.Disposition <> Inapplicable then
                  yield
                      sprintf
                          "behavior.adapters.%s.disposition: %s owns no behavior but declares \"%s\""
                          level
                          row.Project
                          (dispositionName entry.Disposition) ]
    | Some owner ->
        let identity =
            [ match behavior.Id with
              | None -> yield sprintf "behavior.id: %s declares an owner but no behavior id" row.Project
              | Some id ->
                  if not (id.StartsWith(owner + ":", StringComparison.Ordinal)) then
                      yield
                          sprintf
                              "behavior.id: %s declares \"%s\", which does not name its owner \"%s\""
                              row.Project
                              id
                              owner
              if not (List.contains owner nxProjects) then
                  yield sprintf "behavior.owner: %s names \"%s\", which is not an Nx project" row.Project owner ]

        let lifecycle =
            match behavior.LifecycleState with
            | None -> [ sprintf "behavior.lifecycle-state: %s declares an owner but no lifecycle state" row.Project ]
            | Some Bootstrap ->
                [ if not (List.isEmpty behavior.Corpus) then
                      yield
                          sprintf
                              "behavior.corpus: %s is bootstrap and must declare an empty corpus, found \"%s\""
                              row.Project
                              (String.concat "," behavior.Corpus)
                  match behavior.Seed with
                  | None ->
                      yield
                          sprintf "behavior.seed: %s is bootstrap and must declare a seed target and driver" row.Project
                  | Some seed ->
                      if isBlank seed.Target then
                          yield sprintf "behavior.seed.target: %s declares a blank Nx target" row.Project

                      match pathFinding "behavior.seed.driver" row.Project seed.Driver with
                      | Some finding -> yield finding
                      | None -> () ]
            | Some Active ->
                [ match behavior.Seed with
                  | Some seed ->
                      yield
                          sprintf
                              "behavior.seed: %s is active but still declares the seed target \"%s\""
                              row.Project
                              seed.Target
                  | None -> ()
                  if isOwnerRow row && List.isEmpty behavior.Corpus then
                      yield
                          sprintf
                              "behavior.corpus: %s is an active owner and must resolve a non-empty corpus"
                              row.Project

                  if not (isOwnerRow row) && List.isEmpty behavior.Corpus then
                      match Map.tryFind owner rowsByProject with
                      | Some ownerRow when List.isEmpty ownerRow.Behavior.Corpus ->
                          yield
                              sprintf "behavior.corpus: %s delegates to %s, which resolves no corpus" row.Project owner
                      | _ -> () ]

        let paths =
            behavior.Corpus
            |> List.choose (fun glob -> pathFinding "behavior.corpus" row.Project glob)

        identity @ lifecycle @ paths

/// Checks the full typed schema, Nx-project bijection, lifecycle and
/// delegation rules, reciprocal delegation, paths, conditional fields, and
/// the canonical half of every owner row's compatibility map.
let validate
    (registry: Registry)
    (nxProjects: string list)
    (options: ValidateOptions)
    : Result<ValidateReport, Failure> =
    match registry.Testing with
    | None -> Error(ContractFailure "testing: the canonical registry root is missing")
    | Some testing ->

        let rows = testing.Projects
        let rowsByProject = rows |> List.map (fun row -> row.Project, row) |> Map.ofList

        let mappingsByProject =
            testing.Mappings |> List.map (fun map -> map.Project, map) |> Map.ofList

        let schemaFindings =
            [ if testing.Schema <> SchemaVersion then
                  yield sprintf "testing.schema: expected \"%s\", found \"%s\"" SchemaVersion testing.Schema
              if testing.Coverage.MinimumLine <> MinimumLine then
                  yield
                      sprintf
                          "testing.coverage.minimum-line: expected %d, found %d"
                          MinimumLine
                          testing.Coverage.MinimumLine ]

        let bijectionFindings =
            [ for project in duplicates (rows |> List.map (fun row -> row.Project)) do
                  yield sprintf "testing.projects[].project: duplicate row for %s" project
              for row in rows do
                  if not (List.contains row.Project nxProjects) then
                      yield sprintf "testing.projects[].project: %s is absent from the Nx project list" row.Project
              for project in nxProjects do
                  if not (Map.containsKey project rowsByProject) then
                      yield sprintf "testing.projects[].project: %s is absent from testing.projects" project ]

        let rowFindings =
            rows
            |> List.collect (fun row ->
                behaviorFindings row rowsByProject nxProjects
                @ adapterFindings row rowsByProject nxProjects)

        let identityFindings =
            [ for id in duplicates (rows |> List.filter isOwnerRow |> List.choose (fun row -> row.Behavior.Id)) do
                  yield sprintf "behavior.id: duplicate behavior id \"%s\" across owner rows" id ]

        let canonicalFindings =
            rows
            |> List.filter isOwnerRow
            |> List.collect (fun row ->
                match Map.tryFind row.Project mappingsByProject with
                | None -> []
                | Some map ->
                    let derived = derivedRuntimes row |> List.map runtimeIdentity
                    let recorded = sortRuntimes map.Canonical.Runtimes |> List.map runtimeIdentity

                    [ if derived <> recorded then
                          yield
                              sprintf
                                  "testing.compatibility.mappings[].canonical.runtimes: %s resolves [%s] but the map records [%s]"
                                  row.Project
                                  (String.concat "," derived)
                                  (String.concat "," recorded)
                      if map.Canonical.Owner <> row.Behavior.Owner then
                          yield
                              sprintf
                                  "testing.compatibility.mappings[].canonical.owner: %s resolves \"%s\" but the map records \"%s\""
                                  row.Project
                                  (render row.Behavior.Owner)
                                  (render map.Canonical.Owner)
                      match row.Behavior.Corpus, map.Canonical.Corpus with
                      | [ single ], Some recordedCorpus when normalizePath single <> normalizePath recordedCorpus ->
                          yield
                              sprintf
                                  "testing.compatibility.mappings[].canonical.corpus: %s resolves \"%s\" but the map records \"%s\""
                                  row.Project
                                  single
                                  recordedCorpus
                      | _ -> () ])

        let stateFindings =
            [ match options.RequireState with
              | None -> ()
              | Some required ->
                  for row in rows do
                      if row.MigrationState <> required then
                          yield
                              sprintf
                                  "testing.projects[].migration-state: %s is \"%s\" but \"%s\" was required"
                                  row.Project
                                  (migrationStateName row.MigrationState)
                                  (migrationStateName required)
              match options.RequireBehaviorState with
              | None -> ()
              | Some required ->
                  for row in rows do
                      match row.Behavior.LifecycleState with
                      | Some state when state <> required ->
                          yield
                              sprintf
                                  "behavior.lifecycle-state: %s is \"%s\" but \"%s\" was required"
                                  row.Project
                                  (lifecycleName state)
                                  (lifecycleName required)
                      | _ -> ()
              for row in rows do
                  if
                      row.Behavior.LifecycleState = Some Bootstrap
                      && not (List.contains row.Project options.AllowBootstrap)
                  then
                      yield
                          sprintf
                              "behavior.lifecycle-state: %s is \"bootstrap\" but was not admitted by --allow-bootstrap"
                              row.Project
              if options.ForbidLegacy && not (List.isEmpty registry.Legacy) then
                  yield
                      sprintf
                          "coverage.projects: the frozen legacy block is still present with %d rows"
                          (List.length registry.Legacy)
              if options.ForbidCompatibility && not (List.isEmpty testing.Mappings) then
                  yield
                      sprintf
                          "testing.compatibility: the compatibility mappings are still present with %d rows"
                          (List.length testing.Mappings) ]

        let findings =
            schemaFindings
            @ bijectionFindings
            @ rowFindings
            @ identityFindings
            @ canonicalFindings
            @ stateFindings

        match findings with
        | _ :: _ -> Error(ContractFailure(String.concat "\n" findings))
        | [] ->
            let states =
                rows
                |> List.map (fun row -> migrationStateName row.MigrationState)
                |> List.distinct

            Ok
                { State =
                    match states with
                    | [ single ] -> single
                    | _ -> "mixed"
                  Projects = List.length rows
                  BootstrapCount =
                    rows
                    |> List.filter (fun row -> row.Behavior.LifecycleState = Some Bootstrap)
                    |> List.length
                  ActiveCount =
                    rows
                    |> List.filter (fun row -> row.Behavior.LifecycleState = Some Active)
                    |> List.length
                  LegacyPresent = not (List.isEmpty registry.Legacy)
                  CompatibilityPresent = not (List.isEmpty testing.Mappings) }

// ---------------------------------------------------------------------------
// validate-mapping
// ---------------------------------------------------------------------------

/// Checks immutable legacy values against the frozen block, current canonical
/// values against the project rows, stable behavior IDs, the required mapping
/// state, and mapping/project bijection.
let validateMapping
    (registry: Registry)
    (nxProjects: string list)
    (requireState: MappingState option)
    : Result<MappingReport, Failure> =
    match registry.Testing with
    | None -> Error(ContractFailure "testing: the canonical registry root is missing")
    | Some testing ->

        let rowsByProject =
            testing.Projects |> List.map (fun row -> row.Project, row) |> Map.ofList

        let frozen = registry.Legacy |> List.map (fun row -> row.Name, row) |> Map.ofList
        let mappingProjects = testing.Mappings |> List.map (fun map -> map.Project)

        let bijectionFindings =
            [ for project in duplicates mappingProjects do
                  yield sprintf "testing.compatibility.mappings[].project: duplicate map for %s" project
              for project in nxProjects do
                  if not (List.contains project mappingProjects) then
                      yield sprintf "testing.compatibility.mappings[].project: %s has no compatibility map" project
              for project in mappingProjects do
                  if not (List.contains project nxProjects) then
                      yield
                          sprintf
                              "testing.compatibility.mappings[].project: %s is absent from the Nx project list"
                              project ]

        let rowFindings =
            testing.Mappings
            |> List.collect (fun map ->
                let legacyFindings =
                    match Map.tryFind map.Project frozen with
                    | Some row ->
                        [ if not map.Legacy.Present then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.present: %s is in the frozen legacy block but records \"false\""
                                      map.Project
                          match map.Legacy.Corpus with
                          | Some corpus when normalizePath corpus = normalizePath row.Specs -> ()
                          | corpus ->
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.corpus: %s freezes \"%s\" but records \"%s\""
                                      map.Project
                                      row.Specs
                                      (render corpus)
                          if List.sort map.Legacy.Levels <> List.sort row.Levels then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.levels: %s freezes [%s] but records [%s]"
                                      map.Project
                                      (renderLevels row.Levels)
                                      (renderLevels map.Legacy.Levels) ]
                    | None ->
                        [ if map.Legacy.Present then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.present: %s is absent from the frozen legacy block but records \"true\""
                                      map.Project
                          match map.Legacy.Corpus with
                          | Some corpus ->
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.corpus: %s is legacy-absent but records \"%s\""
                                      map.Project
                                      corpus
                          | None -> ()
                          if not (List.isEmpty map.Legacy.Levels) then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.levels: %s is legacy-absent but records [%s]"
                                      map.Project
                                      (renderLevels map.Legacy.Levels) ]

                let canonicalFindings =
                    match Map.tryFind map.Project rowsByProject with
                    | None -> []
                    | Some row ->
                        [ if map.BehaviorId <> row.Behavior.Id then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].behavior-id: %s resolves \"%s\" but the map records \"%s\""
                                      map.Project
                                      (render row.Behavior.Id)
                                      (render map.BehaviorId)
                          if map.Canonical.Owner <> row.Behavior.Owner then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].canonical.owner: %s resolves \"%s\" but the map records \"%s\""
                                      map.Project
                                      (render row.Behavior.Owner)
                                      (render map.Canonical.Owner)
                          if Option.isNone map.BehaviorId && not (List.isEmpty map.Canonical.Runtimes) then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].canonical.runtimes: %s owns no behavior but records [%s]"
                                      map.Project
                                      (map.Canonical.Runtimes |> List.map runtimeIdentity |> String.concat ",") ]

                let stateFindings =
                    match requireState with
                    | Some required when map.State <> required ->
                        [ sprintf
                              "testing.compatibility.mappings[].state: %s is \"%s\" but \"%s\" was required"
                              map.Project
                              (mappingStateName map.State)
                              (mappingStateName required) ]
                    | _ -> []

                legacyFindings @ canonicalFindings @ stateFindings)

        match bijectionFindings @ rowFindings with
        | _ :: _ as findings -> Error(ContractFailure(String.concat "\n" findings))
        | [] ->
            let states =
                testing.Mappings
                |> List.map (fun map -> mappingStateName map.State)
                |> List.distinct

            Ok
                { State =
                    match states with
                    | [ single ] -> single
                    | _ -> "mixed"
                  Mappings = List.length testing.Mappings }

// ---------------------------------------------------------------------------
// Transitions
// ---------------------------------------------------------------------------

/// Checks the move from one registry revision to the next: migration and
/// lifecycle state moves, mapping state moves, frozen legacy values, and
/// behavior-identity stability. Raw path spellings may change freely as long
/// as the normalized identity survives.
let validateTransition (before: Registry) (after: Registry) : Result<unit, Failure> =
    let beforeLegacy =
        before.Legacy |> List.map (fun row -> row.Name, row) |> Map.ofList

    let legacyFindings =
        [ for row in after.Legacy do
              match Map.tryFind row.Name beforeLegacy with
              | None -> yield sprintf "coverage.projects: %s was added to the frozen legacy block" row.Name
              | Some original ->
                  if normalizePath original.Specs <> normalizePath row.Specs then
                      yield
                          sprintf
                              "coverage.projects: %s freezes \"%s\" but now records \"%s\""
                              row.Name
                              original.Specs
                              row.Specs

                  if List.sort original.Levels <> List.sort row.Levels then
                      yield
                          sprintf
                              "coverage.projects: %s freezes [%s] but now records [%s]"
                              row.Name
                              (renderLevels original.Levels)
                              (renderLevels row.Levels)
          for row in before.Legacy do
              if not (after.Legacy |> List.exists (fun candidate -> candidate.Name = row.Name)) then
                  yield sprintf "coverage.projects: %s was removed from the frozen legacy block" row.Name ]

    match before.Testing, after.Testing with
    | None, _
    | _, None ->
        match legacyFindings with
        | [] -> Ok()
        | findings -> Error(ContractFailure(String.concat "\n" findings))
    | Some beforeTesting, Some afterTesting ->

        let beforeRows =
            beforeTesting.Projects |> List.map (fun row -> row.Project, row) |> Map.ofList

        let beforeMaps =
            beforeTesting.Mappings |> List.map (fun map -> map.Project, map) |> Map.ofList

        let rowFindings =
            afterTesting.Projects
            |> List.collect (fun row ->
                match Map.tryFind row.Project beforeRows with
                | None -> []
                | Some original ->
                    let migration =
                        let source = migrationStateRank original.MigrationState
                        let target = migrationStateRank row.MigrationState

                        if target < source then
                            [ sprintf
                                  "testing.projects[].migration-state: %s moved in a reversed direction from \"%s\" to \"%s\""
                                  row.Project
                                  (migrationStateName original.MigrationState)
                                  (migrationStateName row.MigrationState) ]
                        elif target - source > 1 then
                            [ sprintf
                                  "testing.projects[].migration-state: %s skipped a state moving from \"%s\" to \"%s\""
                                  row.Project
                                  (migrationStateName original.MigrationState)
                                  (migrationStateName row.MigrationState) ]
                        else
                            []

                    let lifecycle =
                        match original.Behavior.LifecycleState, row.Behavior.LifecycleState with
                        | Some Active, Some Bootstrap ->
                            [ sprintf
                                  "behavior.lifecycle-state: %s moved in a reversed direction from \"active\" to \"bootstrap\""
                                  row.Project ]
                        | Some Bootstrap, Some Active ->
                            [ if List.isEmpty row.Behavior.Corpus && isOwnerRow row then
                                  yield sprintf "behavior.corpus: %s activated without resolving a corpus" row.Project
                              match row.Behavior.Seed with
                              | Some seed ->
                                  yield
                                      sprintf
                                          "behavior.seed: %s activated but still declares the seed target \"%s\""
                                          row.Project
                                          seed.Target
                              | None -> () ]
                        | _ -> []

                    let identity =
                        if original.Behavior.Id <> row.Behavior.Id then
                            [ sprintf
                                  "behavior.id: %s freezes \"%s\" but now records \"%s\""
                                  row.Project
                                  (render original.Behavior.Id)
                                  (render row.Behavior.Id) ]
                        else
                            []

                    migration @ lifecycle @ identity)

        let mapFindings =
            afterTesting.Mappings
            |> List.collect (fun map ->
                match Map.tryFind map.Project beforeMaps with
                | None -> []
                | Some original ->
                    let state =
                        if mappingStateRank map.State < mappingStateRank original.State then
                            [ sprintf
                                  "testing.compatibility.mappings[].state: %s moved in a reversed direction from \"%s\" to \"%s\""
                                  map.Project
                                  (mappingStateName original.State)
                                  (mappingStateName map.State) ]
                        else
                            []

                    let legacyHalf =
                        [ if original.Legacy.Present <> map.Legacy.Present then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.present: %s freezes \"%b\" but now records \"%b\""
                                      map.Project
                                      original.Legacy.Present
                                      map.Legacy.Present
                          if not (sameNormalizedPath original.Legacy.Corpus map.Legacy.Corpus) then
                              let source, target = original.Legacy.Corpus, map.Legacy.Corpus

                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.corpus: %s freezes \"%s\" but now records \"%s\""
                                      map.Project
                                      (render source)
                                      (render target)
                          if List.sort original.Legacy.Levels <> List.sort map.Legacy.Levels then
                              yield
                                  sprintf
                                      "testing.compatibility.mappings[].legacy.levels: %s freezes [%s] but now records [%s]"
                                      map.Project
                                      (renderLevels original.Legacy.Levels)
                                      (renderLevels map.Legacy.Levels) ]

                    let identity =
                        if original.BehaviorId <> map.BehaviorId then
                            [ sprintf
                                  "testing.compatibility.mappings[].behavior-id: %s freezes \"%s\" but now records \"%s\""
                                  map.Project
                                  (render original.BehaviorId)
                                  (render map.BehaviorId) ]
                        else
                            []

                    let runtimes =
                        let recorded = map.Canonical.Runtimes |> List.map runtimeIdentity |> Set.ofList

                        original.Canonical.Runtimes
                        |> List.map runtimeIdentity
                        |> List.filter (fun identity -> not (Set.contains identity recorded))
                        |> List.map (fun identity ->
                            sprintf
                                "testing.compatibility.mappings[].canonical.runtimes: %s lost the runtime identity %s"
                                map.Project
                                identity)

                    state @ legacyHalf @ identity @ runtimes)

        match legacyFindings @ rowFindings @ mapFindings with
        | [] -> Ok()
        | findings -> Error(ContractFailure(String.concat "\n" findings))

/// Requires that reading the registry left every tracked file byte-identical.
let validateNoTrackedMutation (beforeDigest: string) (afterDigest: string) : Result<unit, Failure> =
    if beforeDigest = afterDigest then
        Ok()
    else
        Error(
            ContractFailure(
                sprintf
                    "repo-config.yml: a read command mutated a tracked byte, digest moved from \"%s\" to \"%s\""
                    beforeDigest
                    afterDigest
            )
        )

// ---------------------------------------------------------------------------
// Snapshots and comparison
// ---------------------------------------------------------------------------

let private sentinelRow (project: string) : SnapshotRow =
    { Project = project
      CanonicalOwner = "-"
      BehaviorId = "-"
      RuntimeIdentities = "-" }

/// Renders one snapshot row as its tab-separated on-disk form.
let renderRow (row: SnapshotRow) : string =
    String.Join("\t", [| row.Project; row.CanonicalOwner; row.BehaviorId; row.RuntimeIdentities |])

/// Projects one side of the dual reader into sorted snapshot rows. The
/// canonical source reproduces exactly the project list supplied by
/// `--project-list-from`, including legacy-absent sentinel rows.
let snapshot
    (registry: Registry)
    (source: SnapshotSource)
    (projectList: string list option)
    : Result<SnapshotRow list, Failure> =
    match source, projectList with
    | SourceLegacy, Some _ -> Error(Misuse "--project-list-from is accepted only with --source canonical")
    | SourceCanonical, None -> Error(Misuse "--project-list-from is required with --source canonical")
    | _ ->

        match registry.Testing with
        | None -> Error(ContractFailure "testing: the canonical registry root is missing")
        | Some testing ->
            match source with
            | SourceLegacy ->
                testing.Mappings
                |> List.sortBy (fun map -> map.Project)
                |> List.map (fun map ->
                    match map.BehaviorId with
                    | None -> sentinelRow map.Project
                    | Some behaviorId ->
                        { Project = map.Project
                          CanonicalOwner = defaultArg map.Canonical.Owner "-"
                          BehaviorId = behaviorId
                          RuntimeIdentities =
                            match sortRuntimes map.Canonical.Runtimes with
                            | [] -> "-"
                            | runtimes -> runtimes |> List.map runtimeIdentity |> String.concat "," })
                |> Ok
            | SourceCanonical ->
                let rowsByProject =
                    testing.Projects |> List.map (fun row -> row.Project, row) |> Map.ofList

                let mapsByProject =
                    testing.Mappings |> List.map (fun map -> map.Project, map) |> Map.ofList

                defaultArg projectList []
                |> List.sort
                |> List.map (fun project ->
                    match Map.tryFind project rowsByProject with
                    | None -> sentinelRow project
                    | Some row ->
                        match row.Behavior.Id with
                        | None -> sentinelRow project
                        | Some behaviorId ->
                            let runtimes =
                                if isOwnerRow row then
                                    derivedRuntimes row
                                else
                                    match Map.tryFind project mapsByProject with
                                    | Some map -> sortRuntimes map.Canonical.Runtimes
                                    | None -> derivedRuntimes row

                            { Project = project
                              CanonicalOwner = defaultArg row.Behavior.Owner "-"
                              BehaviorId = behaviorId
                              RuntimeIdentities =
                                match runtimes with
                                | [] -> "-"
                                | runtimes -> runtimes |> List.map runtimeIdentity |> String.concat "," })
                |> Ok

/// Requires byte equality of two normalized identity projections, returning
/// the equal row count on success.
let compareSnapshots (legacy: SnapshotRow list) (canonical: SnapshotRow list) : Result<int, Failure> =
    let canonicalByProject =
        canonical |> List.map (fun row -> row.Project, row) |> Map.ofList

    let legacyByProject = legacy |> List.map (fun row -> row.Project, row) |> Map.ofList

    let findings =
        [ for row in legacy do
              match Map.tryFind row.Project canonicalByProject with
              | None ->
                  yield sprintf "%s: present in the legacy snapshot and missing from the canonical snapshot" row.Project
              | Some other ->
                  if renderRow row <> renderRow other then
                      yield
                          sprintf
                              "%s: legacy renders \"%s\" but canonical renders \"%s\""
                              row.Project
                              (renderRow row)
                              (renderRow other)
          for row in canonical do
              if not (Map.containsKey row.Project legacyByProject) then
                  yield sprintf "%s: present in the canonical snapshot and missing from the legacy snapshot" row.Project ]

    match findings with
    | [] -> Ok(List.length legacy)
    | findings -> Error(ContractFailure(String.concat "\n" findings))

// ---------------------------------------------------------------------------
// Owner fixture resolution
// ---------------------------------------------------------------------------

let private jsonString (element: JsonElement) (name: string) : string option =
    match element.TryGetProperty name with
    | true, value when value.ValueKind = JsonValueKind.String -> Some(value.GetString())
    | _ -> None

let private jsonInt (element: JsonElement) (name: string) : int option =
    match element.TryGetProperty name with
    | true, value when value.ValueKind = JsonValueKind.Number ->
        match value.TryGetInt32() with
        | true, parsed -> Some parsed
        | _ -> None
    | _ -> None

let private jsonStrings (element: JsonElement) (name: string) : string list =
    match element.TryGetProperty name with
    | true, value when value.ValueKind = JsonValueKind.Array ->
        value.EnumerateArray()
        |> Seq.choose (fun item ->
            if item.ValueKind = JsonValueKind.String then
                Some(item.GetString())
            else
                None)
        |> List.ofSeq
    | _ -> []

let private jsonObject (element: JsonElement) (name: string) : JsonElement option =
    match element.TryGetProperty name with
    | true, value when value.ValueKind = JsonValueKind.Object -> Some value
    | _ -> None

let private jsonKeys (element: JsonElement) : string list =
    element.EnumerateObject()
    |> Seq.map (fun property -> property.Name)
    |> List.ofSeq

/// Directory names an Nx project scan never descends into: build output,
/// dependency, and VCS directories that are never themselves project
/// boundaries.
let private excludedScanDirNames: Set<string> =
    Set.ofList [ "node_modules"; "obj"; "bin"; ".git"; ".nx"; "dist"; "target" ]

/// The three workspace roots that host an Nx `project.json`. `specs/` is one
/// of them because the two contract projects live under
/// `specs/apps/<product>/containers/contracts/`.
let private nxScanRoots = [ "apps"; "libs"; "specs" ]

/// Recursively walks `dir`, skipping [`excludedScanDirNames`], returning
/// every `project.json` path found at any depth.
let rec private findProjectJsonFiles (dir: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let here =
            let candidate = Path.Combine(dir, "project.json")
            if File.Exists candidate then [ candidate ] else []

        let nested =
            Directory.GetDirectories dir
            |> Array.filter (fun child -> not (Set.contains (Path.GetFileName(child: string)) excludedScanDirNames))
            |> Array.toList
            |> List.collect findProjectJsonFiles

        here @ nested

/// The Nx project name one `project.json` declares. Nx infers the name from
/// the containing directory whenever the file omits an explicit `name`, and
/// most app projects here rely on that inference, so the fallback is part of
/// the contract rather than a convenience.
let private projectNameOf (projectJsonPath: string) : string option =
    let inferred =
        let directory = Path.GetDirectoryName(projectJsonPath: string)

        if String.IsNullOrEmpty directory then
            None
        else
            Some(Path.GetFileName directory)

    try
        use document = JsonDocument.Parse(File.ReadAllText projectJsonPath)

        match jsonString document.RootElement "name" with
        | Some name -> Some name
        | None -> inferred
    with _ ->
        None

/// Every Nx project name declared under `apps/`, `libs/`, or `specs/`,
/// deduplicated and sorted. This is the bijection partner both `validate` and
/// `validateMapping` compare the registry against.
let enumerateNxProjects (repoRoot: string) : string list =
    nxScanRoots
    |> List.collect (fun root -> findProjectJsonFiles (Path.Combine(repoRoot, root)))
    |> List.choose projectNameOf
    |> List.distinct
    |> List.sort

let private unknownJsonKeys (where: string) (allowed: string list) (element: JsonElement) : string list =
    jsonKeys element
    |> List.filter (fun name -> not (List.contains name allowed))
    |> List.map (fun name -> sprintf "%s: unknown key \"%s\"" where name)

let private parseMutation (check: FixtureCheck) (element: JsonElement) : Result<FixtureMutation, Failure> =
    let kind = jsonString element "kind"

    let requireStrings (name: string) : string list = jsonStrings element name

    match check, kind with
    | CheckLayout, Some "layout-overlap" ->
        match unknownJsonKeys "mutation" [ "kind"; "path"; "layers" ] element, jsonString element "path" with
        | [], Some path -> Ok(LayoutOverlap(path, requireStrings "layers"))
        | first :: _, _ -> Error(Misuse first)
        | [], None -> Error(Misuse "mutation.path: required key is missing")
    | CheckCoverage, Some "coverage-threshold" ->
        let unknown =
            unknownJsonKeys "mutation" [ "kind"; "slice"; "threshold"; "covered-lines"; "total-lines" ] element

        match
            unknown,
            jsonString element "slice",
            jsonInt element "threshold",
            jsonInt element "covered-lines",
            jsonInt element "total-lines"
        with
        | [], Some slice, Some threshold, Some covered, Some total ->
            Ok(CoverageThreshold(slice, threshold, covered, total))
        | first :: _, _, _, _, _ -> Error(Misuse first)
        | [], _, _, _, _ ->
            Error(Misuse "mutation: coverage-threshold requires slice, threshold, covered-lines, and total-lines")
    | CheckBdd, Some "bdd-remove-binding" ->
        let unknown =
            unknownJsonKeys "mutation" [ "kind"; "feature"; "scenario"; "step"; "adapter" ] element

        match
            unknown,
            jsonString element "feature",
            jsonString element "scenario",
            jsonString element "step",
            jsonString element "adapter"
        with
        | [], Some feature, Some scenario, Some step, Some adapter ->
            Ok(BddRemoveBinding(feature, scenario, step, adapter))
        | first :: _, _, _, _, _ -> Error(Misuse first)
        | [], _, _, _, _ -> Error(Misuse "mutation: bdd-remove-binding requires feature, scenario, step, and adapter")
    | CheckManifest, Some "manifest-forwarder" ->
        let unknown =
            unknownJsonKeys "mutation" [ "kind"; "path"; "direct-consumers"; "script-name"; "script" ] element

        match unknown, jsonString element "path", jsonString element "script-name", jsonString element "script" with
        | [], Some path, Some scriptName, Some script ->
            Ok(ManifestForwarder(path, requireStrings "direct-consumers", scriptName, script))
        | first :: _, _, _, _ -> Error(Misuse first)
        | [], _, _, _ -> Error(Misuse "mutation: manifest-forwarder requires path, script-name, and script")
    | _, kind ->
        Error(
            Misuse(
                sprintf
                    "mutation.kind: \"%s\" is not the mutation kind bound to the \"%s\" check"
                    (render kind)
                    (checkName check)
            )
        )

/// Resolves a repository-relative owner fixture, rejecting absolute paths and
/// traversal, and requiring the path owner, document `owner-id`, and `--owner`
/// to be identical and the document `check` to equal `--check`. The document
/// is read into memory only; no tracked file is opened for writing.
let loadFixture
    (repoRoot: string)
    (ownerId: string)
    (check: FixtureCheck)
    (fixturePath: string)
    : Result<FixtureDocument, Failure> =
    if isBlank fixturePath then
        Error(Misuse "--fixture requires a repository-relative path")
    elif isAbsolutePath fixturePath then
        Error(Misuse(sprintf "--fixture rejects the absolute path \"%s\"" fixturePath))
    elif hasTraversal fixturePath then
        Error(Misuse(sprintf "--fixture rejects the traversal path \"%s\"" fixturePath))
    else

        let normalized = normalizePath fixturePath
        let expectedPrefix = sprintf "%s/%s/" FixtureRoot ownerId

        if not (normalized.StartsWith(expectedPrefix, StringComparison.Ordinal)) then
            Error(
                Misuse(
                    sprintf
                        "--fixture must resolve below the owner directory \"%s\", found \"%s\""
                        expectedPrefix
                        normalized
                )
            )
        else

            let fileName = Path.GetFileName normalized

            match fixtureFiles |> List.tryFind (fun (name, _) -> name = fileName) with
            | None ->
                Error(
                    Misuse(
                        sprintf
                            "--fixture accepts only layout-misplaced.json, coverage-98.json, bdd-missing-step.json, and manifest-proxy.json, found \"%s\""
                            fileName
                    )
                )
            | Some(_, boundCheck) when boundCheck <> check ->
                Error(
                    Misuse(
                        sprintf
                            "--check \"%s\" disagrees with the \"%s\" check bound to fixture \"%s\""
                            (checkName check)
                            (checkName boundCheck)
                            fileName
                    )
                )
            | Some _ ->

                let absolutePath = Path.Combine(repoRoot, normalized)

                if not (File.Exists absolutePath) then
                    Error(ContractFailure(sprintf "%s: the owner fixture does not exist" normalized))
                else

                    use document = JsonDocument.Parse(File.ReadAllText absolutePath)
                    let root = document.RootElement

                    if root.ValueKind <> JsonValueKind.Object then
                        Error(Misuse(sprintf "%s: expected a JSON object" normalized))
                    else

                        match
                            unknownJsonKeys
                                normalized
                                [ "schema"; "owner-id"; "check"; "mutation"; "expected-diagnostic" ]
                                root
                        with
                        | first :: _ -> Error(Misuse first)
                        | [] ->

                            let schema = jsonString root "schema"
                            let documentOwner = jsonString root "owner-id"
                            let documentCheck = jsonString root "check"

                            if schema <> Some FixtureSchemaVersion then
                                Error(
                                    ContractFailure(
                                        sprintf
                                            "%s: schema expected \"%s\", found \"%s\""
                                            normalized
                                            FixtureSchemaVersion
                                            (render schema)
                                    )
                                )
                            elif documentOwner <> Some ownerId then
                                Error(
                                    ContractFailure(
                                        sprintf
                                            "%s: owner-id expected \"%s\", found \"%s\""
                                            normalized
                                            ownerId
                                            (render documentOwner)
                                    )
                                )
                            elif documentCheck <> Some(checkName check) then
                                Error(
                                    ContractFailure(
                                        sprintf
                                            "%s: check expected \"%s\", found \"%s\""
                                            normalized
                                            (checkName check)
                                            (render documentCheck)
                                    )
                                )
                            else

                                match jsonObject root "mutation", jsonObject root "expected-diagnostic" with
                                | None, _ ->
                                    Error(Misuse(sprintf "%s: mutation is required and must be an object" normalized))
                                | _, None ->
                                    Error(
                                        Misuse(
                                            sprintf
                                                "%s: expected-diagnostic is required and must be an object"
                                                normalized
                                        )
                                    )
                                | Some mutation, Some diagnostic ->
                                    match
                                        unknownJsonKeys "expected-diagnostic" [ "code"; "fields" ] diagnostic,
                                        jsonString diagnostic "code"
                                    with
                                    | first :: _, _ -> Error(Misuse first)
                                    | [], None ->
                                        Error(Misuse(sprintf "%s: expected-diagnostic.code is required" normalized))
                                    | [], Some code ->
                                        parseMutation check mutation
                                        |> Result.map (fun mutation ->
                                            { Schema = FixtureSchemaVersion
                                              OwnerId = ownerId
                                              Check = check
                                              Mutation = mutation
                                              ExpectedDiagnostic =
                                                { Code = code
                                                  Fields = jsonStrings diagnostic "fields" } })
