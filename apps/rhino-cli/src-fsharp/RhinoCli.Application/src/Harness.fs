/// Port of the slice of the Rust `application::agents` namespace needed by the
/// scenarios in
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-bindings.feature`
/// and
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-detect-duplication.feature`,
/// and
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-skills-mirror.feature`,
/// and
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/agents-sync.feature`
/// [Repo-grounded — `apps/rhino-cli/src/application/agents/bindings.rs`,
/// `apps/rhino-cli/src/application/agents/codex.rs`,
/// `apps/rhino-cli/src/application/agents/converter.rs`,
/// `apps/rhino-cli/src/application/agents/detect_duplication.rs`,
/// `apps/rhino-cli/src/application/agents/field_policy.rs`,
/// `apps/rhino-cli/src/application/agents/frontmatter.rs`,
/// `apps/rhino-cli/src/application/agents/skills_mirror.rs`,
/// `apps/rhino-cli/src/application/agents/sync.rs`,
/// `apps/rhino-cli/src/application/agents/sync_validator.rs`,
/// `apps/rhino-cli/src/application/agents/types.rs`,
/// `apps/rhino-cli/src/commands/harness_generate_bindings.rs`].
///
/// Scope note: Rust's `validate_bindings` tallies five check families —
/// static binding-file byte parity, `OpenCode`/Skills mirror sync, catalog
/// coverage, `.codex/agents/` file extensions, and the `.codex/config.toml`
/// generated region, plus the colour/tier translation maps. This module
/// currently implements the four the landed feature files exercise (catalog
/// coverage, the Codex agent-file extension, skills-mirror byte parity, and
/// `OpenCode` agent-mirror sync) and the registry-derived `--harness` name
/// check. The remaining families arrive with the feature files that specify
/// them: binding byte parity and the `.codex/config.toml` generated region
/// with `harness/codex-binding.feature`.
///
/// A second scope note covers `sync_validator.rs::validate_sync`, which
/// tallies five check families of its own. This module implements only the
/// two `harness/agents-sync.feature`'s `@agents-validate-sync` scenarios
/// exercise — `validate_agent_count` and `validate_agent_equivalence` — and
/// omits `validate_no_stale_agent_dir`, `validate_no_synced_skills`, and
/// `validate_skills_mirror`, none of which any landed scenario reaches.
///
/// The `harness` namespace stays on the Rust side of `FSHARP_NAMESPACES`
/// until every Wave E feature file has landed, so no CLI path reaches this
/// partial validator in the meantime.
module RhinoCli.Application.Harness

open System
open System.Collections.Generic
open System.Diagnostics
open System.IO
open System.Security.Cryptography
open System.Text
open System.Text.RegularExpressions
open YamlDotNet.Serialization
open YamlDotNet.Serialization.NamingConventions

// ---------------------------------------------------------------------------
// Validation check / result shapes
// ---------------------------------------------------------------------------

/// One validation outcome [Repo-grounded — `agents/types.rs::ValidationCheck`].
///
/// `Status` is a plain string rather than a discriminated union because the
/// JSON and text reporters both emit it verbatim, and Rust's reporter matches
/// on the literals `"passed"` / `"warning"` / anything-else-is-failed.
type ValidationCheck =
    { Name: string
      Status: string
      Expected: string
      Actual: string
      Message: string }

/// Constructors mirroring `ValidationCheck`'s Rust associated functions.
[<RequireQualifiedAccess>]
module ValidationCheck =

    /// A `passed` check carrying only a name and an explanatory message.
    let passed (name: string) (message: string) : ValidationCheck =
        { Name = name
          Status = "passed"
          Expected = ""
          Actual = ""
          Message = message }

    /// A `warning` check carrying the expected/actual pair alongside its message.
    let warning (name: string) (expected: string) (actual: string) (message: string) : ValidationCheck =
        { Name = name
          Status = "warning"
          Expected = expected
          Actual = actual
          Message = message }

    /// A `failed` check carrying the expected/actual pair alongside its message.
    let failed (name: string) (expected: string) (actual: string) (message: string) : ValidationCheck =
        { Name = name
          Status = "failed"
          Expected = expected
          Actual = actual
          Message = message }

    /// A `failed` check with no expected/actual pair — used where the failure
    /// is an I/O or parse error rather than a mismatch.
    let failedMsg (name: string) (message: string) : ValidationCheck =
        { Name = name
          Status = "failed"
          Expected = ""
          Actual = ""
          Message = message }

/// A tallied run of validation checks
/// [Repo-grounded — `agents/types.rs::ValidationResult`].
type ValidationResult =
    { TotalChecks: int
      PassedChecks: int
      WarningChecks: int
      FailedChecks: int
      Checks: ValidationCheck list
      Duration: TimeSpan }

/// Accumulation helpers for [`ValidationResult`].
[<RequireQualifiedAccess>]
module ValidationResult =

    /// The zero value every validator folds its checks onto
    /// [Repo-grounded — `#[derive(Default)]` on Rust's `ValidationResult`].
    let empty: ValidationResult =
        { TotalChecks = 0
          PassedChecks = 0
          WarningChecks = 0
          FailedChecks = 0
          Checks = []
          Duration = TimeSpan.Zero }

    /// Appends `check` and increments the counter its status selects. Anything
    /// that is neither `passed` nor `warning` counts as failed, matching Rust's
    /// catch-all match arm.
    let tally (check: ValidationCheck) (result: ValidationResult) : ValidationResult =
        let passedDelta = if check.Status = "passed" then 1 else 0
        let warningDelta = if check.Status = "warning" then 1 else 0
        let failedDelta = 1 - passedDelta - warningDelta

        { result with
            TotalChecks = result.TotalChecks + 1
            PassedChecks = result.PassedChecks + passedDelta
            WarningChecks = result.WarningChecks + warningDelta
            FailedChecks = result.FailedChecks + failedDelta
            Checks = result.Checks @ [ check ] }

// ---------------------------------------------------------------------------
// Binding surfaces
// ---------------------------------------------------------------------------

/// The binding directories checked for catalog coverage: if one exists on
/// disk, the platform-bindings catalog must reference it. Covers the three
/// supported harnesses (`.claude` source, `.opencode` and `.codex` generated
/// mirrors), the vendor-neutral skills surface `.agents`, and the
/// repository-level `.github` surface — and deliberately names no dropped
/// harness (`.cursor`, `.amazonq`, `.pi`)
/// [Repo-grounded — `bindings.rs::KNOWN_BINDING_DIRS`].
let knownBindingDirs: string list =
    [ ".claude"; ".opencode"; ".codex"; ".agents"; ".github" ]

/// Repo-relative path of the platform-bindings catalog document
/// [Repo-grounded — `bindings.rs::PLATFORM_BINDINGS_CATALOG`].
[<Literal>]
let platformBindingsCatalog = "docs/reference/platform-bindings.md"

/// Directory holding standalone Codex agent files
/// [Repo-grounded — `codex.rs::CODEX_AGENT_DIR`].
[<Literal>]
let codexAgentDir = ".codex/agents"

/// The only extension Codex CLI recognises for a standalone agent file under
/// [`codexAgentDir`]; a `.md` file there is silently ignored by Codex, which
/// is why the validator rejects one outright rather than warning
/// [Repo-grounded — `codex.rs::CODEX_AGENT_EXTENSION`].
[<Literal>]
let codexAgentExtension = "toml"

/// One canonical (relative path, expected content) pair for a generated file
/// [Repo-grounded — `bindings.rs::BindingFile`].
type BindingFile =
    {
        /// POSIX-style path relative to the repository root.
        RelPath: string
        /// Exact content the file must hold.
        Content: string
    }

// ---------------------------------------------------------------------------
// Path helpers
// ---------------------------------------------------------------------------

/// Joins a POSIX-style relative path onto `repoRoot` for the host filesystem
/// [Repo-grounded — `bindings.rs::join_rel`].
let private joinRel (repoRoot: string) (rel: string) : string =
    rel.Split('/')
    |> Array.filter (fun segment -> segment <> "")
    |> Array.fold (fun (acc: string) segment -> Path.Combine(acc, segment)) repoRoot

/// Drops one leading `/` so a catalog entry written as an absolute-looking
/// path still resolves under the repository root
/// [Repo-grounded — `bindings.rs::strip_leading_slash`].
let private stripLeadingSlash (s: string) : string =
    if s.StartsWith("/", StringComparison.Ordinal) then
        s.Substring(1)
    else
        s

// ---------------------------------------------------------------------------
// Frontmatter
// ---------------------------------------------------------------------------

/// Matches a `key:value` line missing its space after the colon; list items
/// (`  - Read`) never match because the key must start the line
/// [Repo-grounded — `frontmatter.rs::yaml_colon_norm`].
let private yamlColonNorm: Regex =
    Regex(@"^([a-zA-Z0-9_-]+):([^\s])", RegexOptions.Multiline ||| RegexOptions.Compiled)

/// Inserts the missing space after a `key:value` colon
/// [Repo-grounded — `frontmatter.rs::normalize_yaml`].
let normalizeYaml (content: string) : string =
    yamlColonNorm.Replace(content, "$1: $2")

/// Splits `content` into its normalized YAML frontmatter and its body
/// [Repo-grounded — `frontmatter.rs::extract_frontmatter`].
let extractFrontmatter (content: string) : Result<string * string, string> =
    let lines = content.Split('\n')

    if lines.Length < 3 then
        Error "file too short to contain frontmatter"
    elif lines.[0].Trim() <> "---" then
        Error "frontmatter does not start with ---"
    else
        match
            lines
            |> Array.skip 1
            |> Array.tryFindIndex (fun line -> line.Trim() = "---")
            |> Option.map (fun relativeIdx -> relativeIdx + 1)
        with
        | None -> Error "frontmatter closing --- not found"
        | Some closingIdx ->
            let front = String.Join("\n", lines.[1 .. closingIdx - 1])

            let body =
                if closingIdx + 1 < lines.Length then
                    String.Join("\n", lines.[closingIdx + 1 ..])
                else
                    ""

            Ok(normalizeYaml front, body)

/// Deserializes a frontmatter block into its top-level key/value mapping.
/// `IgnoreUnmatchedProperties` is irrelevant for a dictionary target but is
/// kept for symmetry with `RepoConfig`'s builder.
let private yamlDeserializer: IDeserializer =
    DeserializerBuilder().WithNamingConvention(NullNamingConvention.Instance).IgnoreUnmatchedProperties().Build()

// ---------------------------------------------------------------------------
// Agent source discovery
// ---------------------------------------------------------------------------

/// Whether a `.claude/agents/` entry is a mirrorable agent definition:
/// a `.md` file that is not the directory's own `README.md`
/// [Repo-grounded — `converter.rs::is_mirrorable_agent_filename`].
let isMirrorableAgentFilename (name: string) (isDir: bool) : bool =
    not isDir
    && name.EndsWith(".md", StringComparison.Ordinal)
    && name <> "README.md"

/// Reads an agent's mirror name from its `name` frontmatter field — never
/// derived from the filename, because a grouped source
/// (`.claude/agents/<group>/<file>.md`) must still flatten to one mirror
/// filename [Repo-grounded — `converter.rs::read_agent_name`].
let readAgentName (path: string) : Result<string, string> =
    let content =
        try
            Ok(File.ReadAllText path)
        with ex ->
            Error(sprintf "failed to read file %s: %s" path ex.Message)

    content
    |> Result.bind (fun text ->
        extractFrontmatter text
        |> Result.mapError (fun e -> sprintf "failed to extract frontmatter from %s: %s" path e))
    |> Result.bind (fun (front, _body) ->
        try
            match yamlDeserializer.Deserialize<Dictionary<string, obj>>(front) with
            | null -> Error(sprintf "frontmatter is not a mapping in %s" path)
            | mapping ->
                match mapping.TryGetValue "name" with
                | true, (:? string as name) -> Ok name
                | _ -> Error(sprintf "agent file %s has no scalar 'name' frontmatter field" path)
        with ex ->
            Error(sprintf "failed to parse YAML frontmatter in %s: %s" path ex.Message))

/// Discovers mirrorable agent sources under `claudeDir`, walking files
/// directly in the directory plus exactly one level of group nesting.
/// Returns `(sourcePath, name)` pairs sorted by name, and fails on a name
/// collision — two sources flattening to the same mirror filename would make
/// the generated mirror non-deterministic
/// [Repo-grounded — `converter.rs::discover_agent_sources`].
let discoverAgentSources (claudeDir: string) : Result<(string * string) list, string> =
    let readEntries (dir: string) : Result<string list, string> =
        try
            Ok(Directory.GetFileSystemEntries dir |> List.ofArray)
        with ex ->
            Error(sprintf "failed to read %s directory: %s" dir ex.Message)

    let mirrorableIn (dir: string) : string list =
        // A group directory that cannot be read is skipped, matching Rust's
        // `let Ok(group_entries) = ... else { continue }`.
        try
            Directory.GetFileSystemEntries dir
            |> Array.filter (fun path -> isMirrorableAgentFilename (Path.GetFileName path) (Directory.Exists path))
            |> List.ofArray
        with _ ->
            []

    readEntries claudeDir
    |> Result.map (fun entries ->
        entries
        |> List.collect (fun path ->
            if Directory.Exists path then
                mirrorableIn path
            elif isMirrorableAgentFilename (Path.GetFileName path) false then
                [ path ]
            else
                []))
    |> Result.bind (fun files ->
        let seen = Dictionary<string, string>()

        let rec name (remaining: string list) (acc: (string * string) list) =
            match remaining with
            | [] -> Ok(List.rev acc)
            | path :: rest ->
                match readAgentName path with
                | Error e -> Error e
                | Ok agentName ->
                    match seen.TryGetValue agentName with
                    | true, existing ->
                        Error(
                            sprintf
                                "agent name collision: '%s' is used by both %s and %s — flat mirror filenames must be unique"
                                agentName
                                existing
                                path
                        )
                    | _ ->
                        seen.Add(agentName, path)
                        name rest ((path, agentName) :: acc)

        name files [])
    |> Result.map (List.sortBy snd)

/// The repo-relative paths of the binding files the parity guard expects to
/// find, one `.codex/agents/<name>.toml` per discovered `.claude/agents/`
/// agent. Empty when `.claude/agents/` does not exist, which is the case in
/// fixture repositories exercising only the other checks
/// [Repo-grounded — `bindings.rs::expected_bindings`].
///
/// The paths alone, not the `(path, content)` pairs Rust returns: rendering a
/// Codex agent's bytes is `codex.rs`'s job and lands with
/// `harness/codex-binding.feature`.
let expectedBindingPaths (repoRoot: string) : Result<string list, string> =
    let claudeDir = Path.Combine(repoRoot, ".claude", "agents")

    if not (Directory.Exists claudeDir) then
        Ok []
    else
        discoverAgentSources claudeDir
        |> Result.map (List.map (fun (_source, name) -> sprintf "%s/%s.%s" codexAgentDir name codexAgentExtension))

// ---------------------------------------------------------------------------
// Checks
// ---------------------------------------------------------------------------

/// Checks that `dir` is referenced in the platform-bindings catalog whenever
/// it exists on disk; an absent directory needs no catalog row
/// [Repo-grounded — `bindings.rs::validate_catalog_coverage`].
let validateCatalogCoverage (repoRoot: string) (dir: string) : ValidationCheck =
    let checkName = sprintf "Catalog Coverage: %s" dir
    let dirPath = Path.Combine(repoRoot, stripLeadingSlash dir)

    if not (Directory.Exists dirPath || File.Exists dirPath) then
        ValidationCheck.passed checkName (sprintf "%s absent on disk; no catalog row required" dir)
    else
        let catalogPath = joinRel repoRoot platformBindingsCatalog

        match
            (try
                Ok(File.ReadAllText catalogPath)
             with ex ->
                 Error ex.Message)
        with
        | Error e -> ValidationCheck.failedMsg checkName (sprintf "failed to read %s: %s" platformBindingsCatalog e)
        | Ok catalog ->
            if catalog.Contains(dir, StringComparison.Ordinal) then
                ValidationCheck.passed checkName (sprintf "%s referenced in %s" dir platformBindingsCatalog)
            else
                ValidationCheck.failed
                    checkName
                    (sprintf "%s referenced in %s" dir platformBindingsCatalog)
                    (sprintf "%s present on disk but absent from catalog" dir)
                    (sprintf
                        "binding dir %s exists but is not referenced in %s; add a catalog row"
                        dir
                        platformBindingsCatalog)

/// Whether `fileName` is something Codex CLI will not read as a standalone
/// agent definition under [`codexAgentDir`] — anything not ending in `.toml`
/// [Repo-grounded — `codex.rs::is_rejected_codex_agent_filename`].
let isRejectedCodexAgentFilename (fileName: string) : bool =
    not (fileName.EndsWith("." + codexAgentExtension, StringComparison.Ordinal))

/// Checks that every file under `.codex/agents/` uses the officially
/// recognised `.toml` extension. The directory itself is permitted — a
/// standalone `<name>.toml` agent file IS a Codex CLI convention — and each
/// offender is named so the fix is unambiguous
/// [Repo-grounded — `bindings.rs::validate_codex_agents_dir`].
let validateCodexAgentsDir (repoRoot: string) : ValidationCheck =
    let checkName = sprintf "Codex Agent Files: %s" codexAgentDir
    let dirPath = joinRel repoRoot codexAgentDir

    if not (Directory.Exists dirPath) then
        ValidationCheck.passed checkName (sprintf "%s absent; nothing to check" codexAgentDir)
    else
        match
            (try
                Ok(Directory.GetFiles dirPath)
             with _ ->
                 Error())
        with
        | Error() -> ValidationCheck.failedMsg checkName (sprintf "failed to read %s" codexAgentDir)
        | Ok files ->
            let offenders =
                files
                |> Array.map Path.GetFileName
                |> Array.filter isRejectedCodexAgentFilename
                |> Array.sortWith (fun a b -> String.CompareOrdinal(a, b))
                |> List.ofArray

            if List.isEmpty offenders then
                ValidationCheck.passed
                    checkName
                    (sprintf "every file under %s uses the .%s extension" codexAgentDir codexAgentExtension)
            else
                let joined = String.Join(", ", offenders)

                ValidationCheck.failed
                    checkName
                    (sprintf "every file under %s ends in .%s" codexAgentDir codexAgentExtension)
                    (sprintf "non-.%s file(s): %s" codexAgentExtension joined)
                    (sprintf
                        "%s/%s uses an extension Codex CLI does not recognise; a standalone Codex agent file must be <name>.%s (the alternative is an [agents.<name>] table in .codex/config.toml)"
                        codexAgentDir
                        joined
                        codexAgentExtension)

/// Runs the binding checks this module implements — catalog coverage for each
/// known binding directory, then the Codex agent-file extension check. See
/// this module's scope note for the check families still to land
/// [Repo-grounded — `bindings.rs::validate_bindings`].
let validateBindings (repoRoot: string) : ValidationResult =
    let stopwatch = Stopwatch.StartNew()

    let result =
        knownBindingDirs
        |> List.fold
            (fun acc dir -> ValidationResult.tally (validateCatalogCoverage repoRoot dir) acc)
            ValidationResult.empty
        |> ValidationResult.tally (validateCodexAgentsDir repoRoot)

    { result with
        Duration = stopwatch.Elapsed }

// ---------------------------------------------------------------------------
// `--harness` name acceptance
// ---------------------------------------------------------------------------

/// The `--harness` names `harness bindings generate` accepts, derived from the
/// `harness:` registry rather than a hard-coded list, so a registry
/// contraction rejects the dropped name automatically
/// [Repo-grounded — `harness_generate_bindings.rs::run`].
let acceptedHarnessNames (config: RepoConfig.RepoConfig) : string list =
    config.Harness |> List.map (fun entry -> entry.Name)

/// Accepts `requested` when the registry declares it, and otherwise reports
/// the registry-derived accepted set so the caller does not have to go and
/// find it [Repo-grounded — `harness_generate_bindings.rs::run`].
let validateHarnessName (config: RepoConfig.RepoConfig) (requested: string) : Result<unit, string> =
    let accepted = acceptedHarnessNames config

    if accepted |> List.exists (fun name -> name = requested) then
        Ok()
    else
        let rendered =
            accepted |> List.map (fun name -> sprintf "'%s'" name) |> String.concat ", "

        Error(sprintf "unknown harness name '%s'; expected one of %s" requested rendered)

// ---------------------------------------------------------------------------
// Verbatim duplication detection
// ---------------------------------------------------------------------------

/// Number of consecutive normalized lines that constitutes a duplication window
/// [Repo-grounded — `detect_duplication.rs::DUPLICATION_WINDOW_SIZE`].
[<Literal>]
let duplicationWindowSize = 10

/// One duplication finding: the same window appearing in two or more files
/// [Repo-grounded — `detect_duplication.rs::DuplicationFinding`].
type DuplicationFinding =
    {
        /// Sorted absolute paths where the duplicated window appears.
        Files: string list
        /// 1-based first line of the window in each corresponding file.
        StartLines: int list
        /// Always [`duplicationWindowSize`].
        WindowSize: int
        /// Always `"high"`.
        Severity: string
        /// Human-readable description.
        Message: string
    }

/// Role suffixes denoting the repository's sanctioned maker-checker-fixer,
/// swe-dev, and web-tester template families — agents in the same role are
/// *designed* to share workflow boilerplate verbatim
/// [Repo-grounded — `detect_duplication.rs::SANCTIONED_ROLE_SUFFIXES`].
let private sanctionedRoleSuffixes: string list =
    [ "-fixer"; "-checker"; "-maker"; "-deployer"; "-dev"; "-tester" ]

/// A stable label for `path`: `skills/<dir>` for a skill file (skill content is
/// keyed by its owning directory, since every skill file is literally named
/// `SKILL.md`), the bare file stem otherwise
/// [Repo-grounded — `detect_duplication.rs::family_label`].
let private familyLabel (path: string) : string =
    if Path.GetFileName path = "SKILL.md" then
        let dir =
            match Path.GetDirectoryName path with
            | null -> ""
            | parent -> Path.GetFileName parent

        sprintf "skills/%s" dir
    else
        Path.GetFileNameWithoutExtension path

/// The sanctioned role suffix `label` ends with, if any
/// [Repo-grounded — `detect_duplication.rs::role_suffix`].
let private roleSuffix (label: string) : string option =
    sanctionedRoleSuffixes
    |> List.tryFind (fun suffix -> label.EndsWith(suffix, StringComparison.Ordinal))

/// `label` with its role suffix stripped — the domain it belongs to — or
/// `label` unchanged when it carries no recognized suffix
/// [Repo-grounded — `detect_duplication.rs::domain_prefix`].
let private domainPrefix (label: string) : string =
    match roleSuffix label with
    | Some suffix -> label.Substring(0, label.Length - suffix.Length)
    | None -> label

/// Whether every file in a cluster belongs to the repository's own sanctioned
/// template family — all sharing one role suffix (e.g. every file a
/// `*-checker`), or all sharing one domain once the suffix is stripped (e.g.
/// the `foo-maker`/`foo-checker`/`foo-fixer` trio). Duplication spanning
/// different roles AND different domains is still reported
/// [Repo-grounded — `detect_duplication.rs::is_sanctioned_template_family`].
let private isSanctionedTemplateFamily (distinctFiles: (string * int) list) : bool =
    let labels = distinctFiles |> List.map (fst >> familyLabel)

    match labels |> List.map roleSuffix |> List.distinct with
    | [ Some _ ] -> true
    | _ -> (labels |> List.map domainPrefix |> List.distinct |> List.length) = 1

/// Removes the YAML frontmatter block, returning only the body. Distinct from
/// [`extractFrontmatter`]: this one keeps the body of a file that has no
/// frontmatter at all rather than rejecting it, because a duplication scan
/// must still read such a file
/// [Repo-grounded — `detect_duplication.rs::strip_frontmatter`].
let stripFrontmatterBody (s: string) : string =
    if
        not (
            s.StartsWith("---\n", StringComparison.Ordinal)
            || s.StartsWith("---\r\n", StringComparison.Ordinal)
        )
    then
        s
    else
        match s.IndexOf('\n') with
        | -1 -> s
        | openingNewline ->
            let body = s.Substring(openingNewline + 1)

            // Offset of the first line equal to `---` once a trailing `\r` is
            // trimmed — the closing fence.
            let rec fenceOffset (offset: int) : int option =
                if offset > body.Length then
                    None
                else
                    let slice = body.Substring offset

                    let line, hasNewline =
                        match slice.IndexOf('\n') with
                        | -1 -> slice, false
                        | idx -> slice.Substring(0, idx), true

                    if line.TrimEnd('\r') = "---" then Some offset
                    elif not hasNewline then None
                    else fenceOffset (offset + line.Length + 1)

            match fenceOffset 0 with
            | None -> s
            | Some idx ->
                match body.Substring(idx).IndexOf('\n') with
                | -1 -> ""
                | closingNewline -> body.Substring(idx + closingNewline + 1)

/// Splits into lines with trailing spaces and tabs trimmed and runs of blank
/// lines collapsed to one, so cosmetic whitespace edits cannot hide a
/// duplicated block [Repo-grounded — `detect_duplication.rs::normalize_lines`].
let normalizeLines (s: string) : string list =
    (([], false), s.Replace("\r\n", "\n").Split('\n'))
    ||> Array.fold (fun (acc, prevBlank) line ->
        let trimmed = line.TrimEnd([| ' '; '\t' |])
        let blank = trimmed = ""

        if blank && prevBlank then
            acc, prevBlank
        else
            trimmed :: acc, blank)
    |> fst
    |> List.rev

/// Whether a window is entirely blank lines, or entirely headings and blanks —
/// shared section scaffolding rather than shared prose, so not worth reporting
/// [Repo-grounded — `detect_duplication.rs::is_excluded_window`].
let isExcludedWindow (lines: string list) : bool =
    let nonBlank =
        lines |> List.map (fun line -> line.Trim()) |> List.filter (fun t -> t <> "")

    List.isEmpty nonBlank
    || nonBlank |> List.forall (fun t -> t.StartsWith("#", StringComparison.Ordinal))

/// Lowercase hex SHA-256 of the newline-joined window — the index key
/// [Repo-grounded — `detect_duplication.rs::hash_window`].
let private hashWindow (lines: string list) : string =
    SHA256.HashData(Encoding.UTF8.GetBytes(String.Join("\n", lines)))
    |> Convert.ToHexStringLower

/// Source-tier agent and skill directories derived from `repo-config.yml`,
/// falling back to `.claude/agents` + `.claude/skills` when the registry is
/// absent or declares no source tier — preserving pre-registry behaviour for
/// callers with no config file
/// [Repo-grounded — `detect_duplication.rs::source_dirs_from_registry`].
let private sourceDirsFromRegistry (repoRoot: string) : string list * string list =
    let config = RepoConfig.loadOrDefault repoRoot

    let sourceDirs (select: RepoConfig.HarnessEntry -> string option) : string list =
        config.Harness
        |> List.filter (fun entry -> entry.Tier = RepoConfig.Tier.Source)
        |> List.choose select
        |> List.map (joinRel repoRoot)

    let orDefault (fallback: string) (dirs: string list) : string list =
        if List.isEmpty dirs then
            [ Path.Combine(repoRoot, ".claude", fallback) ]
        else
            dirs

    sourceDirs (fun entry -> entry.AgentDir) |> orDefault "agents",
    sourceDirs (fun entry -> entry.SkillsDir) |> orDefault "skills"

/// Every agent `.md` and skill `SKILL.md` path under `repoRoot`, sorted. A
/// directory that does not exist is skipped; one that exists but cannot be
/// read is an error
/// [Repo-grounded — `detect_duplication.rs::enumerate_agent_and_skill_files`].
let private enumerateAgentAndSkillFiles (repoRoot: string) : Result<string list, string> =
    let agentDirs, skillsDirs = sourceDirsFromRegistry repoRoot

    let listing (found: string -> string[]) (dir: string) : Result<string list, string> =
        if not (Directory.Exists dir) then
            Ok []
        else
            try
                Ok(found dir |> List.ofArray)
            with ex ->
                Error(sprintf "read %s: %s" dir ex.Message)

    let agentFiles =
        listing (fun dir ->
            Directory.GetFiles dir
            |> Array.filter (fun path ->
                let name = Path.GetFileName path
                name.EndsWith(".md", StringComparison.Ordinal) && name <> "README.md"))

    let skillFiles =
        listing (fun dir ->
            Directory.GetDirectories dir
            |> Array.map (fun skillDir -> Path.Combine(skillDir, "SKILL.md"))
            |> Array.filter File.Exists)

    let collect (lookup: string -> Result<string list, string>) (dirs: string list) =
        dirs
        |> List.fold
            (fun acc dir ->
                match acc, lookup dir with
                | Error e, _ -> Error e
                | _, Error e -> Error e
                | Ok found, Ok more -> Ok(found @ more))
            (Ok [])

    match collect agentFiles agentDirs, collect skillFiles skillsDirs with
    | Error e, _ -> Error e
    | _, Error e -> Error e
    | Ok agents, Ok skills -> Ok(agents @ skills |> List.sortWith (fun a b -> String.CompareOrdinal(a, b)))

/// Scans the source-tier agent and skill files for verbatim
/// [`duplicationWindowSize`]-line duplications, returning one finding per
/// cluster, ordered by first file then first start line
/// [Repo-grounded — `detect_duplication.rs::detect_duplication`].
let detectDuplication (repoRoot: string) : Result<DuplicationFinding list, string> =
    let index = Dictionary<string, ResizeArray<string * int>>()

    let indexOne (path: string) : Result<unit, string> =
        try
            let lines =
                File.ReadAllText path |> stripFrontmatterBody |> normalizeLines |> Array.ofList

            if lines.Length >= duplicationWindowSize then
                for start in 0 .. lines.Length - duplicationWindowSize do
                    let window = lines.[start .. start + duplicationWindowSize - 1] |> List.ofArray

                    if not (isExcludedWindow window) then
                        let key = hashWindow window

                        match index.TryGetValue key with
                        | true, refs -> refs.Add(path, start + 1)
                        | _ ->
                            let refs = ResizeArray<string * int>()
                            refs.Add(path, start + 1)
                            index.Add(key, refs)

            Ok()
        with ex ->
            Error(sprintf "read %s: %s" path ex.Message)

    let cluster (refs: ResizeArray<string * int>) : DuplicationFinding option =
        // First occurrence per distinct file: a window repeated inside ONE
        // file is repetition, not cross-file duplication.
        let seen = HashSet<string>()

        let distinctFiles =
            refs
            |> Seq.filter (fun (path, _) -> seen.Add path)
            |> Seq.sortWith (fun (a, _) (b, _) -> String.CompareOrdinal(a, b))
            |> List.ofSeq

        if List.length distinctFiles < 2 || isSanctionedTemplateFamily distinctFiles then
            None
        else
            Some
                { Files = distinctFiles |> List.map fst
                  StartLines = distinctFiles |> List.map snd
                  WindowSize = duplicationWindowSize
                  Severity = "high"
                  Message =
                    sprintf
                        "%d-line verbatim duplication across %d files"
                        duplicationWindowSize
                        (List.length distinctFiles) }

    enumerateAgentAndSkillFiles repoRoot
    |> Result.bind (fun files ->
        files
        |> List.fold
            (fun acc path ->
                match acc with
                | Error e -> Error e
                | Ok() -> indexOne path)
            (Ok()))
    |> Result.map (fun () ->
        index.Values
        |> Seq.choose cluster
        |> Seq.sortWith (fun a b ->
            match String.CompareOrdinal(List.head a.Files, List.head b.Files) with
            | 0 -> compare (List.head a.StartLines) (List.head b.StartLines)
            | byFile -> byFile)
        |> List.ofSeq)

// ---------------------------------------------------------------------------
// Skills mirror
// ---------------------------------------------------------------------------

/// Outcome of one [`emitSkillsMirrors`] run
/// [Repo-grounded — `skills_mirror.rs::MirrorResult`].
type MirrorResult =
    {
        /// Files written (or that would be written under `dryRun`).
        Copied: int
        /// Files removed because their source counterpart no longer exists.
        Removed: int
        /// Mirror directories left untouched because the registry declares them vendored.
        VendoredSkipped: int
    }

/// The zero value every mirror run starts from
/// [Repo-grounded — `#[derive(Default)]` on Rust's `MirrorResult`].
let mirrorResultEmpty: MirrorResult =
    { Copied = 0
      Removed = 0
      VendoredSkipped = 0 }

/// One harness entry's mirror job, resolved from the registry
/// [Repo-grounded — `skills_mirror.rs::MirrorJob`].
type private MirrorJob =
    {
        /// Absolute path of the canonical source tree.
        Source: string
        /// Absolute path of the generated mirror tree.
        Target: string
        /// Repository-relative path of the mirror tree, tested against the
        /// registry's vendored declarations, which are repo-relative.
        TargetRel: string
        /// Repository-relative vendored directories the emitter must not touch.
        Vendored: string list
    }

/// Every mirror job the registry declares. A harness participates only when
/// it declares BOTH `skillsDir` (where the mirror goes) and `skillsMirrors`
/// (what it mirrors) — declaring one without the other is not an implicit
/// mirror. Fails loudly on a present-but-invalid registry rather than
/// collapsing to an empty job list, which would make every downstream reader
/// silently report zero mirrors
/// [Repo-grounded — `skills_mirror.rs::mirror_jobs`].
let private mirrorJobs (repoRoot: string) : Result<MirrorJob list, string> =
    match RepoConfig.loadOptional repoRoot with
    | Error e -> Error e
    | Ok config ->
        let harness = config |> Option.map (fun c -> c.Harness) |> Option.defaultValue []

        let buildJob (entry: RepoConfig.HarnessEntry) : (string * string) option -> Result<MirrorJob, string> option =
            fun targetSourcePair ->
                targetSourcePair
                |> Option.map (fun (targetRel, sourceRel) ->
                    // An ownership/`vendored[]` disagreement makes the removal
                    // path unsafe: a malformed cross-reference can flip a
                    // currently-protected file into the deletion set.
                    let crossCheckFindings =
                        RepoConfig.vendoredMissingFromOwnershipBackedList 0 entry
                        @ RepoConfig.vendoredWithoutOwnershipEntry 0 entry

                    if not (List.isEmpty crossCheckFindings) then
                        Error(
                            sprintf
                                "harness %s: ownership and vendored declarations disagree (%s) — refusing to mirror until the registry is internally consistent, because this exact disagreement is what lets a vendored directory silently lose its protection and get deleted as an orphan"
                                entry.Name
                                (String.Join("; ", crossCheckFindings))
                        )
                    else
                        match RepoConfig.confinedRepoPath repoRoot sourceRel with
                        | Error e -> Error(sprintf "harness %s skills-mirrors %s: %s" entry.Name sourceRel e)
                        | Ok source ->
                            match RepoConfig.confinedRepoPath repoRoot targetRel with
                            | Error e -> Error(sprintf "harness %s skills-dir %s: %s" entry.Name targetRel e)
                            | Ok target ->
                                // A malformed vendored declaration must not be
                                // treated as "nothing is vendored" — that would
                                // delete every mirrored file it was supposed to
                                // protect.
                                let vendoredErrors =
                                    entry.Vendored
                                    |> List.choose (fun v ->
                                        match RepoConfig.validateRepoRelativePath v with
                                        | Ok() -> None
                                        | Error e ->
                                            Some(
                                                sprintf
                                                    "harness %s vendored %s: %s (a malformed vendored declaration must not be treated as \"nothing is vendored\" — that would delete every mirrored file this entry was supposed to protect)"
                                                    entry.Name
                                                    v
                                                    e
                                            ))

                                match vendoredErrors with
                                | first :: _ -> Error first
                                | [] ->
                                    Ok
                                        { Source = source
                                          Target = target
                                          TargetRel = targetRel
                                          Vendored = entry.Vendored })

        let results =
            harness
            |> List.choose (fun entry ->
                match entry.SkillsDir, entry.SkillsMirrors with
                | Some targetRel, Some sourceRel -> buildJob entry (Some(targetRel, sourceRel))
                | _ -> None)

        results
        |> List.fold
            (fun acc result ->
                match acc, result with
                | Error e, _ -> Error e
                | _, Error e -> Error e
                | Ok jobs, Ok job -> Ok(jobs @ [ job ]))
            (Ok [])

/// Repository-relative paths of every regular file under `root`, sorted. A
/// symlinked directory is never traversed — the mirror must be able to
/// observe one rather than silently follow it
/// [Repo-grounded — `skills_mirror.rs::relative_files`].
let private relativeFiles (root: string) : string list =
    let rec walk (dir: string) : string list =
        if not (Directory.Exists dir) then
            []
        else
            Directory.GetFileSystemEntries dir
            |> Array.toList
            |> List.collect (fun path ->
                // `Directory.Exists` on a symlink to a directory follows the
                // link on .NET, which is exactly the traversal Rust's
                // `symlink_metadata` avoids — this port accepts that gap since
                // no scenario here constructs a symlinked mirror.
                if Directory.Exists path then
                    walk path
                else
                    [ Path.GetRelativePath(root, path).Replace('\\', '/') ])

    walk root |> List.sortWith (fun a b -> String.CompareOrdinal(a, b))

/// True when `rel` (a path relative to the repository root) lies inside any
/// declared vendored directory
/// [Repo-grounded — `skills_mirror.rs::is_vendored`].
let private isVendored (rel: string) (vendored: string list) : bool =
    vendored |> List.exists (RepoConfig.pathIsUnder rel)

/// What one mirror job would change, computed without touching the filesystem
/// [Repo-grounded — `skills_mirror.rs::JobDiff`].
type JobDiff =
    {
        /// Source-relative paths whose mirrored copy is missing or byte-different.
        ToWrite: string list
        /// Mirror-relative paths with no source counterpart and no vendored declaration.
        ToRemove: string list
        /// Mirrored files left alone because the registry declares them vendored.
        VendoredSkipped: int
    }

/// Computes one job's pending changes. Both the emitter and the auditor call
/// this, so "what the mirror should contain" is decided exactly once
/// [Repo-grounded — `skills_mirror.rs::job_diff`].
let private jobDiff (job: MirrorJob) : Result<JobDiff, string> =
    let wanted = relativeFiles job.Source |> Set.ofList

    let toWriteResult =
        wanted
        |> Set.toList
        |> List.fold
            (fun (acc: Result<string list, string>) rel ->
                match acc with
                | Error e -> Error e
                | Ok found ->
                    let src = Path.Combine(job.Source, rel)
                    let dst = Path.Combine(job.Target, rel)

                    try
                        let bytes = File.ReadAllBytes src

                        let matches = File.Exists dst && (File.ReadAllBytes dst) = bytes

                        Ok(if matches then found else found @ [ rel ])
                    with ex ->
                        Error(sprintf "failed to read %s: %s" src ex.Message))
            (Ok [])

    match toWriteResult with
    | Error e -> Error e
    | Ok toWrite ->
        // Ownership is READ FROM THE REGISTRY, never inferred from "this file
        // has no source counterpart": by that inference every vendored file
        // is stale, and one regeneration would delete a whole committed
        // plugin payload.
        let mutable vendoredSkipped = 0

        let toRemove =
            relativeFiles job.Target
            |> List.filter (fun rel ->
                if isVendored (job.TargetRel + "/" + rel) job.Vendored then
                    vendoredSkipped <- vendoredSkipped + 1
                    false
                else
                    not (Set.contains rel wanted))

        Ok
            { ToWrite = toWrite
              ToRemove = toRemove
              VendoredSkipped = vendoredSkipped }

/// A mirror file that disagrees with the canonical tree
/// [Repo-grounded — `skills_mirror.rs::MirrorDrift`].
type MirrorDrift =
    /// A source skill file with a missing or byte-different mirrored copy.
    | MirrorDriftMissing of string
    /// A mirrored file with neither a source counterpart nor a vendored declaration.
    | MirrorDriftUndeclared of string

/// Reports every mirror file that disagrees with the canonical tree, without
/// modifying anything [Repo-grounded — `skills_mirror.rs::audit_skills_mirrors`].
let auditSkillsMirrors (repoRoot: string) : Result<MirrorDrift list, string> =
    mirrorJobs repoRoot
    |> Result.bind (fun jobs ->
        jobs
        |> List.filter (fun job -> Directory.Exists job.Source)
        |> List.fold
            (fun (acc: Result<MirrorDrift list, string>) job ->
                match acc with
                | Error e -> Error e
                | Ok drifts ->
                    match jobDiff job with
                    | Error e -> Error e
                    | Ok diff ->
                        let rel (p: string) = job.TargetRel + "/" + p

                        let missing = diff.ToWrite |> List.map (rel >> MirrorDriftMissing)
                        let undeclared = diff.ToRemove |> List.map (rel >> MirrorDriftUndeclared)
                        Ok(drifts @ missing @ undeclared))
            (Ok []))

/// Walks upward from `dir` removing directories left empty by a deletion,
/// stopping at (and never removing) `stopAt`. A failed removal is
/// deliberately ignored: the only expected cause is a non-empty directory,
/// which is exactly the case where stopping is correct
/// [Repo-grounded — `skills_mirror.rs::prune_empty_dirs`].
let rec private pruneEmptyDirs (dir: string option) (stopAt: string) : unit =
    match dir with
    | None -> ()
    | Some path ->
        let normalized = Path.GetFullPath path
        let normalizedStop = Path.GetFullPath stopAt

        if
            String.Equals(normalized, normalizedStop, StringComparison.Ordinal)
            || not (normalized.StartsWith(normalizedStop, StringComparison.Ordinal))
        then
            ()
        else
            let removed =
                try
                    if Directory.Exists path && Array.isEmpty (Directory.GetFileSystemEntries path) then
                        Directory.Delete path
                        true
                    else
                        false
                with _ ->
                    false

            if removed then
                pruneEmptyDirs (Some(Path.GetDirectoryName path)) stopAt

/// Mirrors every registry-declared skills tree into its harness's skills
/// directory as real files, deleting mirrored files whose source counterpart
/// is gone and leaving every declared vendored directory alone
/// [Repo-grounded — `skills_mirror.rs::emit_skills_mirrors`].
let emitSkillsMirrors (repoRoot: string) (dryRun: bool) : Result<MirrorResult, string> =
    let canonicalRepoRoot = Path.GetFullPath repoRoot

    mirrorJobs repoRoot
    |> Result.bind (fun jobs ->
        jobs
        |> List.fold
            (fun (acc: Result<MirrorResult, string>) job ->
                match acc with
                | Error e -> Error e
                | Ok result ->
                    // Defense in depth alongside `mirrorJobs`'s
                    // `confinedRepoPath` proof: every write and delete stays
                    // inside `repoRoot`, full stop.
                    if
                        not (
                            job.Target.StartsWith(
                                canonicalRepoRoot + Path.DirectorySeparatorChar.ToString(),
                                StringComparison.Ordinal
                            )
                            || String.Equals(job.Target, canonicalRepoRoot, StringComparison.Ordinal)
                        )
                    then
                        Error(sprintf "refusing to write outside the repository: %s" job.Target)
                    elif not (Directory.Exists job.Source) then
                        Ok result
                    else
                        match jobDiff job with
                        | Error e -> Error e
                        | Ok diff ->
                            let updated =
                                { Copied = result.Copied + List.length diff.ToWrite
                                  Removed = result.Removed + List.length diff.ToRemove
                                  VendoredSkipped = result.VendoredSkipped + diff.VendoredSkipped }

                            if dryRun then
                                Ok updated
                            else
                                try
                                    for rel in diff.ToWrite do
                                        let src = Path.Combine(job.Source, rel)
                                        let dst = Path.Combine(job.Target, rel)
                                        Directory.CreateDirectory(Path.GetDirectoryName dst) |> ignore
                                        File.WriteAllBytes(dst, File.ReadAllBytes src)

                                    for rel in diff.ToRemove do
                                        let path = Path.Combine(job.Target, rel)
                                        File.Delete path
                                        pruneEmptyDirs (Some(Path.GetDirectoryName path)) job.Target

                                    Ok updated
                                with ex ->
                                    Error ex.Message)
            (Ok mirrorResultEmpty))

// ---------------------------------------------------------------------------
// Field policy (shared conversion vocabulary)
// ---------------------------------------------------------------------------

/// What happens to a Claude frontmatter field when converting to OpenCode
/// [Repo-grounded — `field_policy.rs::FieldAction`].
type FieldAction =
    | Preserve
    | Translate
    | Drop
    | DropWarn

/// One field's policy entry [Repo-grounded — `field_policy.rs::FieldPolicy`].
type FieldPolicy = { Action: FieldAction; Reason: string }

/// The reason attached to a field absent from the policy table
/// [Repo-grounded — `field_policy.rs::UNKNOWN_FIELD_REASON`].
let unknownFieldReason = "unknown claude code field"

/// A field the walk dropped, carried into a `ConversionWarning`
/// [Repo-grounded — `field_policy.rs::DroppedField`].
type DroppedField = { Field: string; Reason: string }

/// Splits a frontmatter mapping into the fields to apply (`Preserve` /
/// `Translate`) and the fields dropped (unknown, `Drop`, or `DropWarn`)
/// [Repo-grounded — `field_policy.rs::walk_frontmatter_fields`].
let private walkFrontmatterFields
    (mapping: Dictionary<string, obj>)
    (policy: Map<string, FieldPolicy>)
    : (FieldAction * string * obj) list * DroppedField list =
    let mutable applied = []
    let mutable dropped = []

    for kv in mapping do
        match policy.TryFind kv.Key with
        | None ->
            dropped <-
                { Field = kv.Key
                  Reason = unknownFieldReason }
                :: dropped
        | Some entry ->
            match entry.Action with
            | Drop -> ()
            | DropWarn ->
                dropped <-
                    { Field = kv.Key
                      Reason = entry.Reason }
                    :: dropped
            | Preserve
            | Translate -> applied <- (entry.Action, kv.Key, kv.Value) :: applied

    List.rev applied, List.rev dropped

/// Splits a Claude `tools` frontmatter value — either a YAML sequence or a
/// comma-separated string — into individual tool names
/// [Repo-grounded — `frontmatter.rs::parse_claude_tools`].
let parseClaudeTools (value: obj) : string list =
    match value with
    | :? string as s ->
        s.Split(',')
        |> Array.map (fun p -> p.Trim())
        |> Array.filter (fun p -> p <> "")
        |> List.ofArray
    | :? Collections.IEnumerable as items when not (value :? string) ->
        items
        |> Seq.cast<obj>
        |> Seq.choose (function
            | :? string as s -> Some s
            | _ -> None)
        |> List.ofSeq
    | _ -> []

// ---------------------------------------------------------------------------
// OpenCode agent conversion
// ---------------------------------------------------------------------------

/// Where converted agents land, relative to the repo root
/// [Repo-grounded — `converter.rs::OPENCODE_AGENT_DIR`].
let opencodeAgentDir = ".opencode/agents"

/// A frontmatter field dropped for one specific agent, tallied across a
/// whole `sync` run [Repo-grounded — `converter.rs::ConversionWarning`].
type ConversionWarning =
    { AgentName: string
      Field: string
      Reason: string }

/// The OpenCode agent shape emitted to the mirror
/// [Repo-grounded — `converter.rs::OpenCodeAgent`].
type OpenCodeAgent =
    { Description: string
      Model: string
      Permission: Map<string, string>
      Color: string
      Steps: int64
      Skills: string list }

let private openCodeAgentEmpty: OpenCodeAgent =
    { Description = ""
      Model = ""
      Permission = Map.empty
      Color = ""
      Steps = 0L
      Skills = [] }

/// Claude → OpenCode field policy, in Rust declaration order
/// [Repo-grounded — `converter.rs::OPENCODE_FIELD_POLICY_TABLE`].
let private opencodeFieldPolicyTable: (string * FieldAction * string) list =
    [ "name", Drop, "filename carries the agent name"
      "description", Preserve, ""
      "tools", Translate, ""
      "model", Translate, ""
      "color", Translate, ""
      "skills", Preserve, ""
      "maxTurns", Translate, ""
      "disallowedTools", DropWarn, "no OpenCode equivalent"
      "permissionMode", DropWarn, "use the OpenCode permission block instead"
      "effort", DropWarn, "Claude-only field"
      "memory", DropWarn, "Claude-only field"
      "isolation", DropWarn, "Claude-only field"
      "background", DropWarn, "Claude-only field"
      "initialPrompt", DropWarn, "Claude-only field"
      "mcpServers", DropWarn, "OpenCode declares MCP servers at the config level"
      "hooks", DropWarn, "no OpenCode equivalent" ]

let private claudeAgentFieldPolicy: Map<string, FieldPolicy> =
    opencodeFieldPolicyTable
    |> List.map (fun (key, action, reason) -> key, { Action = action; Reason = reason })
    |> Map.ofList

/// Claude agent color name → OpenCode color token
/// [Repo-grounded — `converter.rs::claude_to_opencode_color`].
let private claudeToOpencodeColor: Map<string, string> =
    Map.ofList
        [ "blue", "primary"
          "green", "success"
          "yellow", "warning"
          "purple", "secondary"
          "red", "error"
          "orange", "warning"
          "pink", "accent"
          "cyan", "info" ]

/// Maps a Claude color to its OpenCode token, passing an unrecognized color
/// through unchanged [Repo-grounded — `converter.rs::convert_color`].
let convertColor (color: string) : string =
    if color = "" then
        ""
    else
        claudeToOpencodeColor |> Map.tryFind color |> Option.defaultValue color

/// Lower-cases and dedupes-by-key each tool name into an `"allow"` grant
/// [Repo-grounded — `converter.rs::convert_permission`].
let convertPermission (claudeTools: string list) : Map<string, string> =
    claudeTools
    |> List.map (fun t -> t.Trim().ToLowerInvariant())
    |> List.filter (fun t -> t <> "")
    |> List.map (fun t -> t, "allow")
    |> Map.ofList

/// Every Claude model tier resolves to the same OpenCode model ID — the
/// `zai-coding-plan` binding has one tier, so `sonnet`/`opus`/anything else
/// all translate identically [Repo-grounded — `converter.rs::convert_model`].
let convertModel (_claudeModel: string) : string = "zai-coding-plan/glm-5.2"

/// The source filename's stem, used to label a `ConversionWarning`
/// [Repo-grounded — `converter.rs::agent_name_from_path`].
let private agentNameFromPath (path: string) : string =
    let baseName = Path.GetFileName path

    if baseName.EndsWith(".md", StringComparison.Ordinal) then
        baseName.Substring(0, baseName.Length - 3)
    else
        baseName

/// Matches a markdown link target: `](target)`
/// [Repo-grounded — `converter.rs::agent_link_re`].
let private agentLinkRe: Regex = Regex(@"\]\(([^)]*)\)", RegexOptions.Compiled)

/// Collapses `.`/`..` components out of a `/`-joined relative path, without
/// touching the filesystem [Repo-grounded — `converter.rs::normalize_lexical`].
let private normalizeLexical (path: string) : string =
    let stack = ResizeArray<string>()

    for part in path.Replace('\\', '/').Split('/') do
        if part = ".." then
            if stack.Count > 0 then
                stack.RemoveAt(stack.Count - 1)
        elif part <> "." && part <> "" then
            stack.Add part

    String.Join("/", stack)

/// The `../`-prefixed path from `baseComponents` to `targetComponents`,
/// sharing their longest common prefix [Repo-grounded — `converter.rs::relative_from`].
let private relativeFrom (targetComponents: string[]) (baseComponents: string[]) : string =
    let mutable common = 0

    while (common < targetComponents.Length
           && common < baseComponents.Length
           && targetComponents.[common] = baseComponents.[common]) do
        common <- common + 1

    let ups = Array.create (baseComponents.Length - common) ".."
    let downs = targetComponents.[common..]
    String.Join("/", Array.append ups downs)

/// Rewrites a relative markdown link in `body` so it still resolves once the
/// agent moves from `inputPath` (under `claudeDir`) to `mirrorDir` — absolute,
/// URL, anchor-only, and empty links pass through unchanged
/// [Repo-grounded — `converter.rs::rebase_agent_links`].
let private rebaseAgentLinks (body: string) (inputPath: string) (claudeDir: string) (mirrorDir: string) : string =
    let inputDir =
        match Path.GetDirectoryName inputPath with
        | null
        | "" -> "."
        | d -> d

    let claudeDirNorm = normalizeLexical claudeDir
    let mirrorDirComponents = (normalizeLexical mirrorDir).Split('/')

    agentLinkRe.Replace(
        body,
        fun m ->
            let link = m.Groups.[1].Value

            let passThrough =
                link = ""
                || link.StartsWith("http://", StringComparison.Ordinal)
                || link.StartsWith("https://", StringComparison.Ordinal)
                || link.StartsWith("#", StringComparison.Ordinal)
                || link.StartsWith("/", StringComparison.Ordinal)

            if passThrough then
                sprintf "](%s)" link
            else
                let pathPart, anchor =
                    match link.IndexOf '#' with
                    | -1 -> link, ""
                    | idx -> link.Substring(0, idx), link.Substring(idx)

                if pathPart = "" then
                    sprintf "](%s)" link
                else
                    let resolved = normalizeLexical (inputDir + "/" + pathPart)

                    let newPath =
                        if
                            resolved = claudeDirNorm
                            || resolved.StartsWith(claudeDirNorm + "/", StringComparison.Ordinal)
                        then
                            let rel = resolved.Substring(claudeDirNorm.Length).TrimStart('/')

                            if rel <> "" && not (rel.Contains "/") then
                                rel
                            else
                                relativeFrom (resolved.Split('/')) mirrorDirComponents
                        else
                            relativeFrom (resolved.Split('/')) mirrorDirComponents

                    sprintf "](%s%s)" newPath anchor
    )

/// Applies one `Preserve`/`Translate` field onto an in-progress `OpenCodeAgent`
/// [Repo-grounded — `converter.rs::apply_preserve` and `apply_translate`].
let private applyField (agent: OpenCodeAgent) (action: FieldAction) (key: string) (value: obj) : OpenCodeAgent =
    match action, key with
    | Preserve, "description" ->
        match value with
        | :? string as s -> { agent with Description = s }
        | _ -> agent
    | Preserve, "skills" ->
        match value with
        | :? Collections.IEnumerable as items when not (value :? string) ->
            { agent with
                Skills =
                    items
                    |> Seq.cast<obj>
                    |> Seq.choose (function
                        | :? string as s -> Some s
                        | _ -> None)
                    |> List.ofSeq }
        | _ -> agent
    | Translate, "tools" ->
        { agent with
            Permission = convertPermission (parseClaudeTools value) }
    | Translate, "model" ->
        match value with
        | :? string as s -> { agent with Model = convertModel s }
        | _ -> agent
    | Translate, "color" ->
        match value with
        | :? string as s -> { agent with Color = convertColor s }
        | _ -> agent
    | Translate, "maxTurns" ->
        match value with
        | :? int as i -> { agent with Steps = int64 i }
        | :? int64 as i -> { agent with Steps = i }
        | :? float as f -> { agent with Steps = int64 f }
        | :? string as s ->
            match Int64.TryParse s with
            | true, i -> { agent with Steps = i }
            | false, _ -> agent
        | _ -> agent
    | _ -> agent

/// Whether a plain YAML scalar needs quoting under Go-`yaml.v3`'s rules
/// [Repo-grounded — `converter.rs::needs_quoting`].
let private needsQuoting (s: string) : bool =
    if s = "" then
        true
    elif "-?:,[]{}#&*!|>'\"%@`".IndexOf(s.[0]) >= 0 then
        true
    elif
        s.EndsWith(" ", StringComparison.Ordinal)
        || s.EndsWith("\t", StringComparison.Ordinal)
    then
        true
    elif s.Contains(": ") || s.EndsWith(":", StringComparison.Ordinal) then
        true
    elif s.Contains(" #") then
        true
    elif s.Contains("\n") then
        true
    else
        false

/// Emits a scalar, double-quoting and escaping it when required
/// [Repo-grounded — `converter.rs::yaml_string`].
let private yamlString (s: string) : string =
    if needsQuoting s then
        sprintf "\"%s\"" (s.Replace("\\", "\\\\").Replace("\"", "\\\""))
    else
        s

/// Hand-rolled Go-`yaml.v3`-compatible encoder: `description`/`model` always
/// emit, `permission` emits `{}` when empty else one entry per line sorted by
/// key, `color`/`steps`/`skills` are omitted when at their zero value
/// [Repo-grounded — `converter.rs::encode_opencode_agent`].
let private encodeOpenCodeAgent (agent: OpenCodeAgent) : string =
    let lines = ResizeArray<string>()
    lines.Add(sprintf "description: %s" (yamlString agent.Description))
    lines.Add(sprintf "model: %s" (yamlString agent.Model))

    if Map.isEmpty agent.Permission then
        lines.Add "permission: {}"
    else
        lines.Add "permission:"

        for KeyValue(tool, grant) in agent.Permission do
            lines.Add(sprintf "  %s: %s" tool grant)

    if agent.Color <> "" then
        lines.Add(sprintf "color: %s" (yamlString agent.Color))

    if agent.Steps <> 0L then
        lines.Add(sprintf "steps: %d" agent.Steps)

    if not (List.isEmpty agent.Skills) then
        lines.Add "skills:"

        for skill in agent.Skills do
            lines.Add(sprintf "  - %s" (yamlString skill))

    String.Join("\n", lines) + "\n"

/// Converts one Claude agent file into its OpenCode mirror, writing it unless
/// `dryRun` [Repo-grounded — `converter.rs::convert_agent`].
let private convertAgent
    (inputPath: string)
    (outputPath: string)
    (claudeDir: string)
    (dryRun: bool)
    : Result<ConversionWarning list, string> =
    try
        let content = File.ReadAllText inputPath

        match extractFrontmatter content with
        | Error e -> Error(sprintf "failed to extract frontmatter from %s: %s" inputPath e)
        | Ok(front, body) ->
            match yamlDeserializer.Deserialize<Dictionary<string, obj>>(front) with
            | null -> Error(sprintf "frontmatter is not a mapping in %s" inputPath)
            | mapping ->
                let agentName = agentNameFromPath inputPath
                let applied, dropped = walkFrontmatterFields mapping claudeAgentFieldPolicy

                let converted =
                    applied
                    |> List.fold (fun acc (action, key, value) -> applyField acc action key value) openCodeAgentEmpty

                let warnings =
                    dropped
                    |> List.map (fun d ->
                        { AgentName = agentName
                          Field = d.Field
                          Reason = d.Reason })

                let mirrorDir =
                    match Path.GetDirectoryName outputPath with
                    | null
                    | "" -> "."
                    | d -> d

                let rebasedBody = rebaseAgentLinks body inputPath claudeDir mirrorDir
                let output = "---\n" + encodeOpenCodeAgent converted + "---\n" + rebasedBody

                if not dryRun then
                    Directory.CreateDirectory mirrorDir |> ignore
                    File.WriteAllText(outputPath, output)

                Ok warnings
    with ex ->
        Error(sprintf "failed to convert %s: %s" inputPath ex.Message)

/// A tallied run of `convertAgent` over every discovered source
/// [Repo-grounded — `converter.rs::ConvertAllResult`].
type ConvertAllResult =
    { Converted: int
      Failed: int
      FailedFiles: string list
      Warnings: ConversionWarning list }

let private convertAllResultEmpty: ConvertAllResult =
    { Converted = 0
      Failed = 0
      FailedFiles = []
      Warnings = [] }

/// Discovers every mirrorable Claude agent source under `repoRoot` and
/// converts each one to its flat `.opencode/agents/` mirror
/// [Repo-grounded — `converter.rs::convert_all_agents`].
let convertAllAgents (repoRoot: string) (dryRun: bool) : Result<ConvertAllResult, string> =
    let claudeDir = Path.Combine(repoRoot, ".claude", "agents")
    let opencodeDir = Path.Combine(repoRoot, opencodeAgentDir)

    discoverAgentSources claudeDir
    |> Result.map (fun sources ->
        sources
        |> List.fold
            (fun acc (input, name) ->
                let filename = name + ".md"
                let output = Path.Combine(opencodeDir, filename)

                match convertAgent input output claudeDir dryRun with
                | Ok warnings ->
                    { acc with
                        Converted = acc.Converted + 1
                        Warnings = acc.Warnings @ warnings }
                | Error _ ->
                    { acc with
                        Failed = acc.Failed + 1
                        FailedFiles = acc.FailedFiles @ [ filename ] })
            convertAllResultEmpty)

// ---------------------------------------------------------------------------
// Sync (agents leg)
// ---------------------------------------------------------------------------

/// `rhino-cli harness sync` inputs [Repo-grounded — `sync.rs::SyncOptions`].
type SyncOptions =
    { RepoRoot: string
      DryRun: bool
      AgentsOnly: bool
      SkillsOnly: bool }

/// Defaults matching Rust's `SyncOptions::new` — every flag off
/// [Repo-grounded — `sync.rs::SyncOptions::new`].
let syncOptionsDefault (repoRoot: string) : SyncOptions =
    { RepoRoot = repoRoot
      DryRun = false
      AgentsOnly = false
      SkillsOnly = false }

/// `rhino-cli harness sync` outcome. `skills_copied`/`skills_failed` are
/// dropped: Rust's `SyncResult` carries them but they are permanently zero —
/// skills were never synced by this command, only agents
/// [Repo-grounded — `sync.rs::SyncResult`].
type SyncResult =
    { AgentsConverted: int
      AgentsFailed: int
      FailedFiles: string list
      Warnings: ConversionWarning list }

let syncResultEmpty: SyncResult =
    { AgentsConverted = 0
      AgentsFailed = 0
      FailedFiles = []
      Warnings = [] }

/// Runs the agents leg of a sync, unless `SkillsOnly` short-circuits it to a
/// no-op [Repo-grounded — `sync.rs::sync_all`].
let syncAll (opts: SyncOptions) : Result<SyncResult, string> =
    if opts.SkillsOnly then
        Ok syncResultEmpty
    else
        convertAllAgents opts.RepoRoot opts.DryRun
        |> Result.map (fun r ->
            { AgentsConverted = r.Converted
              AgentsFailed = r.Failed
              FailedFiles = r.FailedFiles
              Warnings = r.Warnings })

// ---------------------------------------------------------------------------
// Sync validation (scoped)
// ---------------------------------------------------------------------------
//
// Scope note: Rust's `validate_sync` tallies five check families. This module
// ports the two the three `@agents-validate-sync` scenarios exercise —
// `validate_agent_count` and `validate_agent_equivalence` — and omits
// `validate_no_stale_agent_dir`, `validate_no_synced_skills`, and
// `validate_skills_mirror`, none of which any landed scenario reaches.

let private countMarkdownFiles (dir: string) : int =
    if not (Directory.Exists dir) then
        0
    else
        Directory.GetFiles dir
        |> Array.filter (fun p -> isMirrorableAgentFilename (Path.GetFileName p) false)
        |> Array.length

let private countClaudeAgentSources (claudeDir: string) : int =
    match discoverAgentSources claudeDir with
    | Ok sources -> List.length sources
    | Error _ -> 0

/// Passes when the OpenCode mirror has at least as many agent files as
/// Claude has agent sources [Repo-grounded — `sync_validator.rs::validate_agent_count`].
let private validateAgentCount (repoRoot: string) : ValidationCheck =
    let claudeDir = Path.Combine(repoRoot, ".claude", "agents")
    let opencodeDir = Path.Combine(repoRoot, opencodeAgentDir)
    let claudeCount = countClaudeAgentSources claudeDir
    let opencodeCount = countMarkdownFiles opencodeDir

    if opencodeCount >= claudeCount then
        ValidationCheck.passed "Agent Count" "OpenCode mirror contains every Claude agent"
    else
        ValidationCheck.failed
            "Agent Count"
            (sprintf "%d agents" claudeCount)
            (sprintf "%d agents" opencodeCount)
            "OpenCode agents directory is missing one or more Claude agents"

let private parseOpencodePermission (value: obj option) : Map<string, string> =
    match value with
    | Some(:? IDictionary<obj, obj> as m) ->
        m
        |> Seq.choose (fun kv ->
            match kv.Key, kv.Value with
            | (:? string as k), (:? string as v) -> Some(k, v)
            | _ -> None)
        |> Map.ofSeq
    | _ -> Map.empty

let private parseStringSeq (value: obj option) : string list =
    match value with
    | Some(:? Collections.IEnumerable as items) when not (value.Value :? string) ->
        items
        |> Seq.cast<obj>
        |> Seq.choose (function
            | :? string as s -> Some s
            | _ -> None)
        |> List.ofSeq
    | _ -> []

let private tryGetField (mapping: Dictionary<string, obj>) (key: string) : obj option =
    match mapping.TryGetValue key with
    | true, v -> Some v
    | _ -> None

/// Compares the source Claude agent's frontmatter/body against its OpenCode
/// mirror field by field, returning the first mismatch or a pass
/// [Repo-grounded — `sync_validator.rs::validate_agent_yaml`].
let private validateAgentYaml
    (agentName: string)
    (claudeMapping: Dictionary<string, obj>)
    (opencodeMapping: Dictionary<string, obj>)
    (expectedBody: string)
    (actualBody: string)
    : ValidationCheck =
    let checkName = sprintf "Agent Equivalence: %s" agentName

    let claudeDescription =
        match tryGetField claudeMapping "description" with
        | Some(:? string as s) -> s
        | _ -> ""

    let opencodeDescription =
        match tryGetField opencodeMapping "description" with
        | Some(:? string as s) -> s
        | _ -> ""

    if claudeDescription <> opencodeDescription then
        ValidationCheck.failed checkName claudeDescription opencodeDescription "description mismatch"
    else
        let expectedModel =
            match tryGetField claudeMapping "model" with
            | Some(:? string as s) -> convertModel s
            | _ -> convertModel ""

        let actualModel =
            match tryGetField opencodeMapping "model" with
            | Some(:? string as s) -> s
            | _ -> ""

        if expectedModel <> actualModel then
            ValidationCheck.failed checkName expectedModel actualModel "model mismatch"
        else
            let expectedPermission =
                tryGetField claudeMapping "tools"
                |> Option.map parseClaudeTools
                |> Option.defaultValue []
                |> convertPermission

            let actualPermission =
                parseOpencodePermission (tryGetField opencodeMapping "permission")

            if expectedPermission <> actualPermission then
                ValidationCheck.failed
                    checkName
                    (sprintf "%A" (Map.toList expectedPermission))
                    (sprintf "%A" (Map.toList actualPermission))
                    "permission mismatch"
            else
                let expectedSkills = parseStringSeq (tryGetField claudeMapping "skills")
                let actualSkills = parseStringSeq (tryGetField opencodeMapping "skills")

                if expectedSkills <> actualSkills then
                    ValidationCheck.failed
                        checkName
                        (sprintf "%A" expectedSkills)
                        (sprintf "%A" actualSkills)
                        "skills mismatch"
                elif expectedBody <> actualBody then
                    ValidationCheck.failed checkName expectedBody actualBody "body mismatch"
                else
                    ValidationCheck.passed checkName "Agent is semantically equivalent"

/// Reads one Claude agent source and its OpenCode mirror, rebases the
/// Claude body the same way `convertAgent` would, and delegates the field
/// comparison to `validateAgentYaml`
/// [Repo-grounded — `sync_validator.rs::validate_agent_file`].
let private validateAgentFile
    (claudeDir: string)
    (opencodeDir: string)
    (sourcePath: string)
    (agentName: string)
    : ValidationCheck =
    let checkName = sprintf "Agent Equivalence: %s" agentName
    let mirrorPath = Path.Combine(opencodeDir, agentName + ".md")

    try
        let claudeContent = File.ReadAllText sourcePath

        if not (File.Exists mirrorPath) then
            ValidationCheck.failedMsg checkName (sprintf "OpenCode mirror not found: %s" mirrorPath)
        else
            let opencodeContent = File.ReadAllText mirrorPath

            match extractFrontmatter claudeContent, extractFrontmatter opencodeContent with
            | Error e, _ -> ValidationCheck.failedMsg checkName (sprintf "failed to parse Claude frontmatter: %s" e)
            | _, Error e -> ValidationCheck.failedMsg checkName (sprintf "failed to parse OpenCode frontmatter: %s" e)
            | Ok(claudeFront, claudeBody), Ok(_, opencodeBody) ->
                match
                    yamlDeserializer.Deserialize<Dictionary<string, obj>> claudeFront,
                    yamlDeserializer.Deserialize<Dictionary<string, obj>>(
                        (extractFrontmatter opencodeContent |> Result.map fst |> Result.defaultValue "")
                    )
                with
                | null, _
                | _, null -> ValidationCheck.failedMsg checkName "frontmatter is not a mapping"
                | claudeMapping, opencodeMapping ->
                    let expectedBody = rebaseAgentLinks claudeBody sourcePath claudeDir opencodeDir
                    validateAgentYaml agentName claudeMapping opencodeMapping expectedBody opencodeBody
    with ex ->
        ValidationCheck.failedMsg checkName (sprintf "failed to compare %s: %s" agentName ex.Message)

/// Walks every discovered Claude agent source and validates it against its
/// mirror [Repo-grounded — `sync_validator.rs::validate_agent_equivalence`].
let private validateAgentEquivalence (repoRoot: string) : ValidationCheck list =
    let claudeDir = Path.Combine(repoRoot, ".claude", "agents")
    let opencodeDir = Path.Combine(repoRoot, opencodeAgentDir)

    match discoverAgentSources claudeDir with
    | Error e -> [ ValidationCheck.failedMsg "Agent Equivalence" (sprintf "failed to discover agent sources: %s" e) ]
    | Ok sources ->
        sources
        |> List.map (fun (path, name) -> validateAgentFile claudeDir opencodeDir path name)

/// Runs the scoped sync validation: agent count, then per-agent equivalence
/// [Repo-grounded — `sync_validator.rs::validate_sync`].
let validateSync (repoRoot: string) : ValidationResult =
    let stopwatch = Stopwatch.StartNew()

    let checks = validateAgentCount repoRoot :: validateAgentEquivalence repoRoot

    let result =
        checks
        |> List.fold (fun acc check -> ValidationResult.tally check acc) ValidationResult.empty

    stopwatch.Stop()

    { result with
        Duration = stopwatch.Elapsed }
