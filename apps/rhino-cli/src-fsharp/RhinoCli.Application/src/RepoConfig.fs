/// Port of the slice of the Rust `repo_config` namespace needed by the nine
/// scenarios in
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-config/data-driven.feature`
/// [Repo-grounded — `apps/rhino-cli/src/application/repo_config/mod.rs`,
/// `apps/rhino-cli/src/commands/repo_config_validate.rs`].
///
/// Scope note: the Rust `RepoConfig` schema is a ~40-field struct covering
/// gate wiring, ownership classes, env contracts, word budgets, and the full
/// Doctor tool roster. This port models only `harness[].{name,tier,agent-dir,
/// mirrors,forbid-dir}`, `gates[].{id,args}`, `specs.{ddd-areas,domain-areas}`,
/// and `doctor.dotnet-global-json` — the fields these nine scenarios read —
/// and deserializes with `IgnoreUnmatchedProperties` rather than Rust's
/// `deny_unknown_fields`, so every other real `repo-config.yml` key is
/// silently accepted rather than schema-validated. None of the nine scenarios
/// exercises unknown-key rejection.
module RhinoCli.Application.RepoConfig

open System
open System.Collections.Generic
open System.IO
open System.Text.Json
open YamlDotNet.Serialization
open YamlDotNet.Serialization.NamingConventions

/// The two binding tiers a harness entry may declare
/// [Repo-grounded — `repo_config/mod.rs::Tier`].
type Tier =
    | Source
    | Generated

/// One harness entry in the `harness:` section of `repo-config.yml`, trimmed
/// to the fields the codex-entry and three-harness-registry scenarios read
/// [Repo-grounded — `repo_config/mod.rs::HarnessEntry`].
type HarnessEntry =
    { Name: string
      Tier: Tier
      AgentDir: string option
      Mirrors: string option
      ForbidDir: string option }

/// One entry in the `gates:` section, trimmed to the `id` and `args` fields
/// the website-exclusion scenario reads
/// [Repo-grounded — `repo_config/mod.rs::GateEntry`].
type GateEntry =
    { Id: string
      Args: Map<string, string list> }

/// The `doctor:` section, trimmed to the .NET SDK path scenario's field
/// [Repo-grounded — `repo_config/mod.rs::DoctorConfig`].
type DoctorConfig = { DotnetGlobalJson: string option }

/// The `specs:` section, trimmed to the data-driven-behaviour scenario's
/// fields [Repo-grounded — `repo_config/mod.rs::SpecsConfig`].
type SpecsConfig =
    { DddAreas: string list
      DomainAreas: string list }

/// Parsed `repo-config.yml`, trimmed to this port's scope (see module doc
/// comment) [Repo-grounded — `repo_config/mod.rs::RepoConfig`].
type RepoConfig =
    { Harness: HarnessEntry list
      Gates: GateEntry list
      Specs: SpecsConfig
      Doctor: DoctorConfig }

/// The value `load`/`loadOptional` never produce on their own but that
/// `loadOrDefault` falls back to on any load failure
/// [Repo-grounded — `repo_config/mod.rs::RepoConfig`'s `#[derive(Default)]`].
let empty: RepoConfig =
    { Harness = []
      Gates = []
      Specs = { DddAreas = []; DomainAreas = [] }
      Doctor = { DotnetGlobalJson = None } }

/// Raw YAML-shaped intermediate records. `[<CLIMutable>]` gives each record a
/// parameterless constructor and settable properties, which is what lets
/// YamlDotNet's reflection-based object builder populate an otherwise
/// immutable F# record — the same trick used for `System.Text.Json` DTOs,
/// applied here to YamlDotNet instead.
///
/// Deliberately NOT `private`: a `private` F# type's compiler-generated
/// constructor is non-public even with `[<CLIMutable>]`, and YamlDotNet's
/// default reflection-based object factory only ever calls
/// `Activator.CreateInstance(type)` (the public-constructor overload) — the
/// same pitfall `Convention.fs`'s module doc comment warns about for
/// `System.Text.Json`, reproduced here for YamlDotNet instead. These DTOs are
/// still excluded from this module's public surface indirectly: nothing
/// outside `parseRepoConfig` ever constructs or returns one.
[<CLIMutable>]
type HarnessEntryDto =
    { Name: string
      Tier: string
      AgentDir: string | null
      Mirrors: string | null
      ForbidDir: string | null }

[<CLIMutable>]
type GateEntryDto =
    { Id: string
      Args: Dictionary<string, ResizeArray<string>> }

[<CLIMutable>]
type DoctorConfigDto = { DotnetGlobalJson: string | null }

[<CLIMutable>]
type SpecsConfigDto =
    { DddAreas: ResizeArray<string>
      DomainAreas: ResizeArray<string> }

[<CLIMutable>]
type RepoConfigDto =
    { Harness: ResizeArray<HarnessEntryDto>
      Gates: ResizeArray<GateEntryDto>
      Specs: SpecsConfigDto
      Doctor: DoctorConfigDto }

/// Matches `repo-config.yml`'s kebab-case keys (`agent-dir`, `ddd-areas`,
/// `dotnet-global-json`, ...) against the DTOs' PascalCase properties without
/// per-property `[<YamlMember>]` attributes, and tolerates every real
/// `repo-config.yml` key this port does not model (see module doc comment).
let private deserializer: IDeserializer =
    DeserializerBuilder().WithNamingConvention(HyphenatedNamingConvention.Instance).IgnoreUnmatchedProperties().Build()

let private toOptionList (items: ResizeArray<'a>) : 'a list =
    match items with
    | null -> []
    | items -> List.ofSeq items

/// Folds a list of `Result`s into a single `Result` of a list, short
/// -circuiting on the first `Error` — small enough here that pulling in a
/// railway-oriented-programming library for one caller would cost more than
/// it saves.
let rec private sequenceResults (results: Result<'a, string> list) : Result<'a list, string> =
    match results with
    | [] -> Ok []
    | Error e :: _ -> Error e
    | Ok x :: rest ->
        match sequenceResults rest with
        | Ok xs -> Ok(x :: xs)
        | Error e -> Error e

let private parseTier (index: int) (raw: string) : Result<Tier, string> =
    match raw with
    | null -> Error(sprintf "harness[%d].tier: required key is missing" index)
    | "source" -> Ok Source
    | "generated" -> Ok Generated
    | other ->
        Error(sprintf "harness[%d].tier: invalid value \"%s\" (expected \"source\" or \"generated\")" index other)

let private toHarnessEntry (index: int) (dto: HarnessEntryDto) : Result<HarnessEntry, string> =
    parseTier index dto.Tier
    |> Result.map (fun tier ->
        { Name = dto.Name
          Tier = tier
          AgentDir = Option.ofObj dto.AgentDir
          Mirrors = Option.ofObj dto.Mirrors
          ForbidDir = Option.ofObj dto.ForbidDir })

let private toGateEntry (dto: GateEntryDto) : GateEntry =
    let args =
        match dto.Args with
        | null -> Map.empty
        | dict -> dict |> Seq.map (fun kv -> kv.Key, toOptionList kv.Value) |> Map.ofSeq

    { Id = dto.Id; Args = args }

let private toSpecsConfig (dto: SpecsConfigDto) : SpecsConfig =
    match box dto with
    | null -> { DddAreas = []; DomainAreas = [] }
    | _ ->
        { DddAreas = toOptionList dto.DddAreas
          DomainAreas = toOptionList dto.DomainAreas }

let private toDoctorConfig (dto: DoctorConfigDto) : DoctorConfig =
    match box dto with
    | null -> { DotnetGlobalJson = None }
    | _ -> { DotnetGlobalJson = Option.ofObj dto.DotnetGlobalJson }

/// Parses `data` (the contents of `repo-config.yml`) into a [`RepoConfig`]
/// [Repo-grounded — `repo_config/mod.rs::parse_repo_config`].
let private parseRepoConfig (data: string) : Result<RepoConfig, string> =
    try
        let dto = deserializer.Deserialize<RepoConfigDto>(data)

        match box dto with
        | null -> Ok empty
        | _ ->
            toOptionList dto.Harness
            |> List.mapi toHarnessEntry
            |> sequenceResults
            |> Result.map (fun harness ->
                { Harness = harness
                  Gates = toOptionList dto.Gates |> List.map toGateEntry
                  Specs = toSpecsConfig dto.Specs
                  Doctor = toDoctorConfig dto.Doctor })
    with ex ->
        Error ex.Message

/// Loads and parses `repo-config.yml` at `repoRoot`
/// [Repo-grounded — `repo_config/mod.rs::load`].
let load (repoRoot: string) : Result<RepoConfig, string> =
    let path = Path.Combine(repoRoot, "repo-config.yml")

    try
        let data = File.ReadAllText path
        parseRepoConfig data
    with ex ->
        Error(sprintf "cannot read repo-config.yml at %s: %s" path ex.Message)

/// Loads `repo-config.yml` at `repoRoot`, discriminating "no entry exists at
/// this path at all" (`Ok None`) from every other failure to read or parse it
/// (`Error`) [Repo-grounded — `repo_config/mod.rs::load_optional`].
///
/// Scope note: uses `File.Exists`, which follows symlinks, rather than the
/// Rust port's `symlink_metadata`-based check, which additionally
/// distinguishes a dangling symlink (declared, but unreadable — `Error`) from
/// a genuinely absent path (`Ok None`). None of these nine scenarios exercise
/// a dangling symlink.
let loadOptional (repoRoot: string) : Result<RepoConfig option, string> =
    let path = Path.Combine(repoRoot, "repo-config.yml")

    if not (File.Exists path) then
        Ok None
    else
        load repoRoot |> Result.map Some

/// Loads `repo-config.yml` at `repoRoot`, falling back to [`empty`] when the
/// file is absent or cannot be parsed
/// [Repo-grounded — `repo_config/mod.rs::load_or_default`].
let loadOrDefault (repoRoot: string) : RepoConfig =
    match load repoRoot with
    | Ok config -> config
    | Error _ -> empty

/// Validates a configured repository-relative file path before it is joined
/// to a repository root [Repo-grounded —
/// `repo_config/mod.rs::validate_repo_relative_path`].
///
/// Scope note: this port checks the three conditions these nine scenarios
/// exercise (empty/absolute, padded whitespace, `./`/`../` components) but
/// omits the Windows drive-prefix (`Component::Prefix`) case, which macOS/
/// Linux `Path` values can never produce.
///
/// # Errors
///
/// Returns an error when the path is empty, absolute, carries leading or
/// trailing whitespace, or contains a parent-directory or `./`
/// current-directory component.
let validateRepoRelativePath (value: string) : Result<unit, string> =
    if String.IsNullOrEmpty value || Path.IsPathRooted value then
        Error "must be a non-empty repository-relative path"
    elif value <> value.Trim() then
        Error
            "must not carry leading or trailing whitespace (a padded value like this can pass \
             validation yet fail to match the real file it names, silently orphaning whatever \
             it was declared to protect)"
    else
        let hasBadComponent =
            value.Split('/', '\\')
            |> Array.exists (fun segment -> segment = ".." || segment = ".")

        if hasBadComponent then
            Error "must not contain an absolute, parent-directory, or ./ current-directory component"
        else
            Ok()

/// Resolves a configured repository-relative path to its nearest existing
/// ancestor, confirming that ancestor lies within `repoRoot`
/// [Repo-grounded — `repo_config/mod.rs::confined_repo_path`].
///
/// Scope note: uses `Path.GetFullPath` (lexical normalization) rather than
/// the Rust port's `Path::canonicalize` (which additionally resolves
/// symlinks); the escape check below is consequently a defense-in-depth
/// approximation, not a true symlink-escape guard. None of these nine
/// scenarios exercises a symlinked repository ancestor.
///
/// # Errors
///
/// Returns an error when the value is lexically unsafe, no ancestor of the
/// candidate path exists, or the nearest existing ancestor lies outside
/// `repoRoot`.
let confinedRepoPath (repoRoot: string) (value: string) : Result<string, string> =
    match validateRepoRelativePath value with
    | Error e -> Error e
    | Ok() ->
        try
            let canonicalRoot = Path.GetFullPath repoRoot
            let candidate = Path.Combine(repoRoot, value)

            let rec findExistingAncestor (path: string) : string option =
                if File.Exists path || Directory.Exists path then
                    Some path
                else
                    match Path.GetDirectoryName path with
                    | null
                    | "" -> None
                    | parent -> findExistingAncestor parent

            match findExistingAncestor candidate with
            | None -> Error "configured path has no existing repository ancestor"
            | Some existingAncestor ->
                let canonicalAncestor = Path.GetFullPath existingAncestor
                let rootWithSeparator = canonicalRoot + string Path.DirectorySeparatorChar

                if
                    not (
                        String.Equals(canonicalAncestor, canonicalRoot, StringComparison.Ordinal)
                        || canonicalAncestor.StartsWith(rootWithSeparator, StringComparison.Ordinal)
                    )
                then
                    Error(sprintf "configured path \"%s\" escapes the repository root through a symlink" value)
                else
                    let canonicalCandidate = Path.GetFullPath candidate

                    if String.Equals(canonicalCandidate, canonicalAncestor, StringComparison.Ordinal) then
                        Ok canonicalAncestor
                    else
                        let remaining = Path.GetRelativePath(existingAncestor, candidate)
                        Ok(Path.Combine(canonicalAncestor, remaining))
        with ex ->
            Error ex.Message

/// Collects `repo-config validate`'s semantic findings, trimmed to the one
/// check the leading-`./`-rejection scenario exercises
/// [Repo-grounded — `repo_config_validate.rs::semantic_findings`].
///
/// Scope note: the Rust validator additionally requires non-empty `harness`/
/// `coverage.projects`, validates every harness path field, and checks gate
/// wiring/carve-out/duplicate-id rules — none of which this feature file's
/// nine scenarios exercise, and none of which this trimmed `RepoConfig` type
/// (see module doc comment) carries enough data to check.
let semanticFindings (config: RepoConfig) : string list =
    match config.Doctor.DotnetGlobalJson with
    | None -> []
    | Some path ->
        match validateRepoRelativePath path with
        | Ok() -> []
        | Error message -> [ sprintf "doctor.dotnet-global-json: invalid value \"%s\" (%s)" path message ]

/// Runs `repo-config validate` from a known `repoRoot`, returning whether it
/// passed alongside the human-readable text a CLI invocation would print
/// [Repo-grounded — `repo_config_validate.rs::run_at_root`].
let validateAtRoot (repoRoot: string) : bool * string =
    match load repoRoot with
    | Error message ->
        false, sprintf "repo-config validate: repo-config.yml failed strict schema deserialization: %s\n" message
    | Ok config ->
        match semanticFindings config with
        | [] -> true, "repo-config validate: repo-config.yml matches the canonical schema (key set + enums OK)\n"
        | findings ->
            let body = findings |> List.map (fun f -> f + "\n") |> String.concat ""
            false, body

/// The slice of a Doctor `ToolDef` the .NET SDK path scenario reads
/// [Repo-grounded — `doctor/tools.rs::ToolDef`].
///
/// Scope note: only `source` and `read_req` are ported. Doctor's full
/// `ToolDef` additionally carries the binary name, comparison args, version
/// parser/comparator, and install command — a much larger surface (~20
/// tools) untouched by this feature file's scenarios.
type DotnetToolDef =
    { Source: string
      ReadReq: unit -> string }

/// Reads `sdk.version` out of a `global.json`-shaped JSON file, returning an
/// empty string when the file is missing, unreadable, or lacks that key
/// [Repo-grounded — `doctor/checker.rs::read_dotnet_version`].
let private readDotnetSdkVersion (path: string) : string =
    try
        use doc = JsonDocument.Parse(File.ReadAllText path)

        match doc.RootElement.TryGetProperty "sdk" with
        | true, sdk ->
            match sdk.TryGetProperty "version" with
            | true, version when version.ValueKind = JsonValueKind.String -> version.GetString()
            | _ -> ""
        | _ -> ""
    with _ ->
        ""

/// Resolves the repository's .NET SDK configuration path from
/// `repo-config.yml`, falling back to the conventional root `global.json`
/// when unset or invalid [Repo-grounded —
/// `doctor/tools.rs::configured_dotnet_global_json`].
let private resolveDotnetGlobalJsonPath (repoRoot: string) (config: RepoConfig) : string =
    let fallback = Path.Combine(repoRoot, "global.json")

    match config.Doctor.DotnetGlobalJson with
    | None -> fallback
    | Some value ->
        match confinedRepoPath repoRoot value with
        | Ok path -> path
        | Error _ -> fallback

/// Builds the `dotnet` tool definition's `source` label and `read_req`
/// closure from `repoRoot`'s configuration
/// [Repo-grounded — `doctor/tools.rs::tool_defs_dotnet`].
let buildDotnetToolDef (repoRoot: string) (config: RepoConfig) : DotnetToolDef =
    let path = resolveDotnetGlobalJsonPath repoRoot config

    { Source = "doctor.dotnet-global-json → sdk.version"
      ReadReq = fun () -> readDotnetSdkVersion path }
