/// Port of the slice of the Rust `repo_config` namespace needed by the
/// scenarios in
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-config/data-driven.feature`
/// and
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/repo-config-validate/repo-config-validate.feature`,
/// and `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/harness-catalog.feature`
/// [Repo-grounded — `apps/rhino-cli/src/application/repo_config/mod.rs`,
/// `apps/rhino-cli/src/commands/repo_config_validate.rs`].
///
/// Scope note: the Rust `RepoConfig` schema is a ~40-field struct covering
/// gate wiring, env contracts, word budgets, and the full Doctor tool
/// roster. This port models only `harness[].{name,tier,agent-dir,mirrors,
/// forbid-dir,skills-dir,skills-mirrors,vendored,catalog,ownership}`,
/// `gates[].{id,args}`, `specs.{ddd-areas,domain-areas}`,
/// `doctor.dotnet-global-json`, and `harness-catalog.{document,verified}` —
/// the fields these three feature files' scenarios read — and deserializes
/// the rest of the document with
/// `IgnoreUnmatchedProperties` rather than Rust's `deny_unknown_fields`, so
/// every other real `repo-config.yml` key is silently accepted rather than
/// schema-validated. `harness[]` and `harness[].ownership[]` are the
/// exception: `checkNoUnknownHarnessKeys` below independently walks the raw
/// YAML structure to reject an unknown key in either, since the
/// repo-config-validate scenarios exercise exactly that. Widening this
/// strictness to the rest of the schema is future work for later waves.
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

/// The three ownership classes a binding path may declare in a harness
/// entry's `ownership:` list — named `Class*` rather than reusing `Tier`'s
/// `Source`/`Generated` case names, which would otherwise collide under a
/// single `open RhinoCli.Application.RepoConfig`
/// [Repo-grounded — `repo_config/mod.rs::OwnershipClass`].
type OwnershipClass =
    | ClassSource
    | ClassGenerated
    | ClassVendored

/// One entry in a harness entry's `ownership:` list, declaring which of the
/// three classes above a single binding path belongs to, and — for a
/// `vendored` path — why it is exempt from regeneration
/// [Repo-grounded — `repo_config/mod.rs::OwnershipEntry`].
type OwnershipEntry =
    { Path: string
      Class: OwnershipClass
      Reason: string option }

/// One harness's row in the generated platform-binding catalog table, read
/// from a harness entry's `catalog:` block
/// [Repo-grounded — `repo_config/mod.rs::CatalogEntry`].
type CatalogEntry =
    { Platform: string
      ReadsAgentsMd: string
      InstructionSurface: string
      McpConfig: string
      AgentSurface: string
      SkillsSurface: string
      Status: string }

/// One harness entry in the `harness:` section of `repo-config.yml`, trimmed
/// to the fields the codex-entry, three-harness-registry, and
/// repo-config-validate scenarios read
/// [Repo-grounded — `repo_config/mod.rs::HarnessEntry`].
type HarnessEntry =
    { Name: string
      Tier: Tier
      AgentDir: string option
      Mirrors: string option
      ForbidDir: string option
      SkillsDir: string option
      SkillsMirrors: string option
      Vendored: string list
      Catalog: CatalogEntry option
      Ownership: OwnershipEntry list }

/// One entry in the `gates:` section, trimmed to the `id` and `args` fields
/// the website-exclusion scenario reads
/// [Repo-grounded — `repo_config/mod.rs::GateEntry`].
type GateEntry =
    { Id: string
      Args: Map<string, string list> }

/// The `doctor:` section, trimmed to the .NET SDK path scenario's field plus
/// `skip-tools` (needed by
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature`'s "A
/// repo-config-declared tool is skipped from the check" scenario)
/// [Repo-grounded — `repo_config/mod.rs::DoctorConfig`].
type DoctorConfig =
    { DotnetGlobalJson: string option
      SkipTools: string list }

/// The `specs:` section, trimmed to the data-driven-behaviour scenario's
/// fields [Repo-grounded — `repo_config/mod.rs::SpecsConfig`].
type SpecsConfig =
    { DddAreas: string list
      DomainAreas: string list }

/// Document-level settings for the generated platform-binding catalog: where
/// it lives, and the date its claims were last verified against upstream
/// [Repo-grounded — `repo_config/mod.rs::HarnessCatalog`].
type HarnessCatalog = { Document: string; Verified: string }

/// Parsed `repo-config.yml`, trimmed to this port's scope (see module doc
/// comment) [Repo-grounded — `repo_config/mod.rs::RepoConfig`].
type RepoConfig =
    { Harness: HarnessEntry list
      Gates: GateEntry list
      Specs: SpecsConfig
      Doctor: DoctorConfig
      HarnessCatalog: HarnessCatalog option }

/// The value `load`/`loadOptional` never produce on their own but that
/// `loadOrDefault` falls back to on any load failure
/// [Repo-grounded — `repo_config/mod.rs::RepoConfig`'s `#[derive(Default)]`].
let empty: RepoConfig =
    { Harness = []
      Gates = []
      Specs = { DddAreas = []; DomainAreas = [] }
      Doctor =
        { DotnetGlobalJson = None
          SkipTools = [] }
      HarnessCatalog = None }

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
type OwnershipEntryDto =
    { Path: string
      Class: string
      Reason: string | null }

[<CLIMutable>]
type CatalogEntryDto =
    { Platform: string
      ReadsAgentsMd: string
      InstructionSurface: string
      McpConfig: string
      AgentSurface: string
      SkillsSurface: string
      Status: string }

[<CLIMutable>]
type HarnessEntryDto =
    { Name: string
      Tier: string
      AgentDir: string | null
      Mirrors: string | null
      ForbidDir: string | null
      SkillsDir: string | null
      SkillsMirrors: string | null
      Vendored: ResizeArray<string>
      Catalog: CatalogEntryDto
      Ownership: ResizeArray<OwnershipEntryDto> }

[<CLIMutable>]
type GateEntryDto =
    { Id: string
      Args: Dictionary<string, ResizeArray<string>> }

[<CLIMutable>]
type DoctorConfigDto =
    { DotnetGlobalJson: string | null
      SkipTools: ResizeArray<string> }

[<CLIMutable>]
type SpecsConfigDto =
    { DddAreas: ResizeArray<string>
      DomainAreas: ResizeArray<string> }

[<CLIMutable>]
type HarnessCatalogDto = { Document: string; Verified: string }

[<CLIMutable>]
type RepoConfigDto =
    { Harness: ResizeArray<HarnessEntryDto>
      Gates: ResizeArray<GateEntryDto>
      Specs: SpecsConfigDto
      Doctor: DoctorConfigDto
      HarnessCatalog: HarnessCatalogDto }

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

/// Parses one `ownership[].class` value
/// [Repo-grounded — `repo_config/mod.rs::OwnershipClass`'s `Deserialize`
/// impl].
let private parseOwnershipClass
    (harnessIndex: int)
    (ownershipIndex: int)
    (raw: string)
    : Result<OwnershipClass, string> =
    match raw with
    | null -> Error(sprintf "harness[%d].ownership[%d].class: required key is missing" harnessIndex ownershipIndex)
    | "source" -> Ok ClassSource
    | "generated" -> Ok ClassGenerated
    | "vendored" -> Ok ClassVendored
    | other ->
        Error(
            sprintf
                "harness[%d].ownership[%d].class: invalid value \"%s\" (expected \"source\", \"generated\", or \"vendored\")"
                harnessIndex
                ownershipIndex
                other
        )

let private toOwnershipEntry
    (harnessIndex: int)
    (ownershipIndex: int)
    (dto: OwnershipEntryDto)
    : Result<OwnershipEntry, string> =
    parseOwnershipClass harnessIndex ownershipIndex dto.Class
    |> Result.map (fun cls ->
        { Path = dto.Path
          Class = cls
          Reason = Option.ofObj dto.Reason })

let private toCatalogEntry (dto: CatalogEntryDto) : CatalogEntry =
    { Platform = dto.Platform
      ReadsAgentsMd = dto.ReadsAgentsMd
      InstructionSurface = dto.InstructionSurface
      McpConfig = dto.McpConfig
      AgentSurface = dto.AgentSurface
      SkillsSurface = dto.SkillsSurface
      Status = dto.Status }

let private toHarnessEntry (index: int) (dto: HarnessEntryDto) : Result<HarnessEntry, string> =
    parseTier index dto.Tier
    |> Result.bind (fun tier ->
        toOptionList dto.Ownership
        |> List.mapi (toOwnershipEntry index)
        |> sequenceResults
        |> Result.map (fun ownership ->
            { Name = dto.Name
              Tier = tier
              AgentDir = Option.ofObj dto.AgentDir
              Mirrors = Option.ofObj dto.Mirrors
              ForbidDir = Option.ofObj dto.ForbidDir
              SkillsDir = Option.ofObj dto.SkillsDir
              SkillsMirrors = Option.ofObj dto.SkillsMirrors
              Vendored = toOptionList dto.Vendored
              Catalog =
                match box dto.Catalog with
                | null -> None
                | _ -> Some(toCatalogEntry dto.Catalog)
              Ownership = ownership }))

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
    | null ->
        { DotnetGlobalJson = None
          SkipTools = [] }
    | _ ->
        { DotnetGlobalJson = Option.ofObj dto.DotnetGlobalJson
          SkipTools = toOptionList dto.SkipTools }

/// `harness[]` entries' allowed key set, matching `HarnessEntryDto`'s fields
/// in the kebab-case spelling `repo-config.yml` uses for them.
let private allowedHarnessKeys: Set<string> =
    Set.ofList
        [ "name"
          "tier"
          "agent-dir"
          "skills-dir"
          "rules-dir"
          "agent-name"
          "mirrors"
          "skills-mirrors"
          "vendored"
          "config"
          "forbid-dir"
          "shadow"
          "instruction"
          "catalog"
          "ownership" ]

/// `harness[].ownership[]` entries' allowed key set, matching
/// `OwnershipEntryDto`'s fields.
let private allowedOwnershipKeys: Set<string> =
    Set.ofList [ "path"; "class"; "reason" ]

let private asRawMap (value: obj) : IDictionary<obj, obj> option =
    match value with
    | :? IDictionary<obj, obj> as dict -> Some dict
    | _ -> None

let private asRawList (value: obj) : obj list option =
    match value with
    | :? IDictionary<obj, obj> -> None
    | :? System.Collections.IEnumerable as items when not (value :? string) ->
        Some(items |> Seq.cast<obj> |> List.ofSeq)
    | _ -> None

let private tryGetRawValue (dict: IDictionary<obj, obj>) (key: string) : obj option =
    dict
    |> Seq.tryFind (fun kv ->
        match kv.Key with
        | :? string as candidate -> String.Equals(candidate, key, StringComparison.Ordinal)
        | _ -> false)
    |> Option.map (fun kv -> kv.Value)

let private unknownKeyFindings (allowed: Set<string>) (dict: IDictionary<obj, obj>) (label: string) : string list =
    dict
    |> Seq.choose (fun kv ->
        match kv.Key with
        | :? string as key when not (Set.contains key allowed) ->
            Some(
                sprintf
                    "%s: unknown key \"%s\" (expected one of %s)"
                    label
                    key
                    (String.concat ", " (Set.toList allowed))
            )
        | _ -> None)
    |> List.ofSeq

/// Independently walks `data`'s raw YAML structure (rather than the lenient
/// `RepoConfigDto`) to reject an unknown key inside a `harness[]` entry or a
/// `harness[].ownership[]` sub-entry, reproducing Rust's
/// `#[serde(deny_unknown_fields)]` on `HarnessEntry`/`OwnershipEntry` for
/// exactly these two substructures.
///
/// Scope note: this does NOT reproduce `deny_unknown_fields` for the rest of
/// the ~40-field `RepoConfig` schema (`gates[]`, `specs`, `doctor`, and
/// everything this port does not model at all) — see the module doc comment.
/// Widening this check to more of the schema is future work for later
/// waves, as this port grows to cover more of `repo-config.yml`.
let private checkNoUnknownHarnessKeys (data: string) : Result<unit, string> =
    try
        let root = deserializer.Deserialize<obj>(data)

        match asRawMap root with
        | None -> Ok()
        | Some rootMap ->
            match tryGetRawValue rootMap "harness" |> Option.bind asRawList with
            | None -> Ok()
            | Some harnessItems ->
                let findings =
                    harnessItems
                    |> List.mapi (fun i item ->
                        match asRawMap item with
                        | None -> []
                        | Some entryMap ->
                            let ownershipFindings =
                                match tryGetRawValue entryMap "ownership" |> Option.bind asRawList with
                                | None -> []
                                | Some ownershipItems ->
                                    ownershipItems
                                    |> List.mapi (fun j oitem ->
                                        match asRawMap oitem with
                                        | None -> []
                                        | Some ownedMap ->
                                            unknownKeyFindings
                                                allowedOwnershipKeys
                                                ownedMap
                                                (sprintf "harness[%d].ownership[%d]" i j))
                                    |> List.collect id

                            unknownKeyFindings allowedHarnessKeys entryMap (sprintf "harness[%d]" i)
                            @ ownershipFindings)
                    |> List.collect id

                match findings with
                | [] -> Ok()
                | _ -> Error(String.concat "; " findings)
    with ex ->
        Error ex.Message

/// Parses `data` (the contents of `repo-config.yml`) into a [`RepoConfig`]
/// [Repo-grounded — `repo_config/mod.rs::parse_repo_config`].
let private parseRepoConfig (data: string) : Result<RepoConfig, string> =
    match checkNoUnknownHarnessKeys data with
    | Error message -> Error message
    | Ok() ->
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
                      Doctor = toDoctorConfig dto.Doctor
                      HarnessCatalog =
                        match box dto.HarnessCatalog with
                        | null -> None
                        | _ ->
                            Some
                                { Document = dto.HarnessCatalog.Document
                                  Verified = dto.HarnessCatalog.Verified } })
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
                let rootWithSeparator = canonicalRoot + Path.DirectorySeparatorChar.ToString()

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

/// Splits a path into its non-empty components, tolerating either separator
/// so a trailing separator does not manufacture a spurious empty component
/// [Repo-grounded — `repo_config/mod.rs::paths_equal`/`path_is_under`'s use
/// of `Path::components()`].
let private pathComponents (path: string) : string list =
    path.Split('/', '\\')
    |> Array.filter (fun segment -> segment <> "")
    |> List.ofArray

/// Component-wise path equality — tolerates a trailing separator difference
/// but not a real typo [Repo-grounded — `repo_config/mod.rs::paths_equal`].
let pathsEqual (a: string) (b: string) : bool = pathComponents a = pathComponents b

/// True when `path` lies under `dir` (component-wise prefix). False when
/// `dir` is empty [Repo-grounded — `repo_config/mod.rs::path_is_under`].
let pathIsUnder (path: string) (dir: string) : bool =
    if String.IsNullOrEmpty dir then
        false
    else
        let dirComponents = pathComponents dir
        let pathParts = pathComponents path

        dirComponents.Length <= pathParts.Length
        && (pathParts |> List.take dirComponents.Length) = dirComponents

/// Forward direction: an ownership entry declared `class: vendored` under
/// this harness entry's `skills-dir`, with no matching `vendored[]` entry.
/// A no-op when `skills-dir` is unset
/// [Repo-grounded —
/// `repo_config/mod.rs::vendored_missing_from_ownership_backed_list`].
let vendoredMissingFromOwnershipBackedList (index: int) (entry: HarnessEntry) : string list =
    match entry.SkillsDir with
    | None -> []
    | Some skillsDir ->
        entry.Ownership
        |> List.filter (fun owned ->
            owned.Class = ClassVendored
            && pathIsUnder owned.Path skillsDir
            && not (entry.Vendored |> List.exists (fun v -> pathsEqual v owned.Path)))
        |> List.map (fun owned ->
            sprintf
                "harness[%d].ownership: \"%s\" is declared class: vendored under skills-dir \"%s\" but has no matching harness[%d].vendored entry (the skills mirror will delete it on the next regeneration)"
                index
                owned.Path
                skillsDir
                index)

/// Reverse direction: a `vendored[]` entry with no matching `ownership`
/// entry declared `class: vendored`. Always checked, with no `skills-dir`
/// gate — `vendored[]` itself only makes sense under `skills-dir`
/// [Repo-grounded — `repo_config/mod.rs::vendored_without_ownership_entry`].
let vendoredWithoutOwnershipEntry (index: int) (entry: HarnessEntry) : string list =
    entry.Vendored
    |> List.mapi (fun k vendoredPath ->
        let declared =
            entry.Ownership
            |> List.exists (fun owned -> owned.Class = ClassVendored && pathsEqual owned.Path vendoredPath)

        if declared then
            None
        else
            Some(
                sprintf
                    "harness[%d].vendored[%d]: \"%s\" has no matching harness[%d].ownership entry with class: vendored (a vendored[] entry that fails to match its real directory — most commonly a typo — leaves that real directory unprotected and the skills mirror will delete it on the next regeneration)"
                    index
                    k
                    vendoredPath
                    index
            ))
    |> List.choose id

/// Per-harness-entry semantic findings: every `class: vendored` ownership
/// declaration must carry a non-empty `reason`, plus both cross-checks above
/// [Repo-grounded —
/// `repo_config_validate.rs::harness_entry_semantic_findings`].
let harnessEntrySemanticFindings (index: int) (entry: HarnessEntry) : string list =
    let reasonFindings =
        entry.Ownership
        |> List.mapi (fun j owned ->
            let blank =
                owned.Reason
                |> Option.map (fun r -> r.Trim())
                |> Option.forall (fun r -> r = "")

            if owned.Class = ClassVendored && blank then
                Some(
                    sprintf
                        "harness[%d].ownership[%d].reason: required non-empty value for path \"%s\" (a vendored path must record why it cannot be regenerated)"
                        index
                        j
                        owned.Path
                )
            else
                None)
        |> List.choose id

    reasonFindings
    @ vendoredMissingFromOwnershipBackedList index entry
    @ vendoredWithoutOwnershipEntry index entry

/// Collects `repo-config validate`'s semantic findings
/// [Repo-grounded — `repo_config_validate.rs::semantic_findings`,
/// `harness_entry_semantic_findings`].
///
/// Scope note: the Rust validator additionally requires non-empty `harness`/
/// `coverage.projects`, validates every harness path field, and checks gate
/// wiring/carve-out/duplicate-id rules — none of which either feature file's
/// scenarios exercise, and none of which this trimmed `RepoConfig` type (see
/// module doc comment) carries enough data to check.
let semanticFindings (config: RepoConfig) : string list =
    let doctorFindings =
        match config.Doctor.DotnetGlobalJson with
        | None -> []
        | Some path ->
            match validateRepoRelativePath path with
            | Ok() -> []
            | Error message -> [ sprintf "doctor.dotnet-global-json: invalid value \"%s\" (%s)" path message ]

    let harnessFindings =
        config.Harness |> List.mapi harnessEntrySemanticFindings |> List.collect id

    doctorFindings @ harnessFindings

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
