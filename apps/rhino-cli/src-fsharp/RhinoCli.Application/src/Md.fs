/// Port of the Rust `md` namespace's `docs validate-frontmatter` and
/// `docs validate-heading-hierarchy` validators
/// [Repo-grounded — `apps/rhino-cli/src/application/docs/frontmatter.rs`,
/// `apps/rhino-cli/src/commands/md_validate_frontmatter.rs`,
/// `apps/rhino-cli/src/application/docs/heading_hierarchy.rs`,
/// `apps/rhino-cli/src/commands/md_validate_heading_hierarchy.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-frontmatter.feature`'s
/// 11 scenarios and
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-heading-hierarchy.feature`'s
/// 12 scenarios.
///
/// Scope: this PR (Wave D PR2) additionally ports the heading-hierarchy
/// validator — the `md` namespace's remaining three feature files (links,
/// mermaid, naming, audit) land in later Wave D PRs against this same file.
/// Findings reuse the shared `RhinoCli.Domain.Types.Finding` record
/// (`Severity`/`Message`/`Path`) rather than a bespoke `DocsHeadingFinding`
/// type, matching `Convention.fs`'s established "shared Finding over bespoke
/// per-validator types" precedent and this file's own frontmatter-validator
/// precedent — the Rust source's separate `kind` and `line` fields are
/// folded into each finding's `Message` text instead of becoming extra
/// fields on the shared record, since every Rust `kind` value is already
/// reproduced verbatim inside its finding's message text and no scenario
/// here asserts on an exact line number.
///
/// `md` is not yet listed in `FSHARP_NAMESPACES` (that flip is later,
/// separate Wave D integration work), so — matching `TestCoverage.fs`'s
/// `validate`-before-the-Wave-C-flip precedent — both validators are called
/// directly by their step definitions with a path list (or repo root) built
/// by hand, not parsed from CLI argv. No text/JSON/Markdown rendering lives
/// in this file for the same reason `reporter.rs`'s formatting stays out of
/// `Doctor.fs` until a scenario needs it: none of these feature files'
/// scenarios assert on rendered output, only on the structured `Finding`
/// list.
module RhinoCli.Application.Md

open System
open System.Collections.Generic
open System.IO
open System.Text.RegularExpressions
open YamlDotNet.Serialization
open RhinoCli.Domain.Types

/// Path fragment that identifies software-engineering explanation documents
/// [Repo-grounded — `frontmatter.rs::SOFTWARE_DOC_PREFIX`].
let private softwareDocPrefix = "docs/explanation/software-engineering/"

/// Path fragments that identify governance documents
/// [Repo-grounded — `frontmatter.rs::GOVERNANCE_DOC_PREFIXES`].
let private governanceDocPrefixes: string list =
    [ "repo-governance/conventions/"
      "repo-governance/principles/"
      "repo-governance/development/"
      "repo-governance/workflows/" ]

/// The allowed values for the `category` frontmatter field (Diátaxis
/// framework) [Repo-grounded — `frontmatter.rs::VALID_CATEGORIES`].
let private validCategories: Set<string> =
    Set.ofList [ "tutorial"; "how-to"; "reference"; "explanation" ]

/// Directory names that are skipped during recursive walks
/// [Repo-grounded — `frontmatter.rs::SKIP_DIRS`].
let private skipDirs: Set<string> =
    Set.ofList [ "node_modules"; ".git"; ".next"; "dist"; "build"; "target" ]

/// Directory names that are skipped during the heading-hierarchy validator's
/// recursive walks — the Rust source keeps this as a second, separate
/// constant (`frontmatter.rs::SKIP_DIRS` above vs. `naming.rs::SKIP_DIRS`
/// here) rather than a single shared list, so this port mirrors that split
/// instead of merging them. A superset of `skipDirs` above: the same six
/// names, plus `generated-reports`
/// [Repo-grounded — `heading_hierarchy.rs`'s `use super::naming::SKIP_DIRS`,
/// `naming.rs::SKIP_DIRS`].
let private namingSkipDirs: Set<string> =
    Set.ofList
        [ "node_modules"
          ".git"
          ".next"
          "dist"
          "build"
          "target"
          "generated-reports" ]

/// Classifies a markdown file as belonging to a known documentation area
/// [Repo-grounded — `frontmatter.rs::DocArea`].
type private DocArea =
    /// The file is not in any recognised documentation area.
    | UnknownArea
    /// The file is in `docs/explanation/software-engineering/`.
    | SoftwareArea
    /// The file is under one of the `repo-governance/` sub-trees.
    | GovernanceArea

/// Determines which documentation area `path` belongs to
/// [Repo-grounded — `frontmatter.rs::classify_doc_area`].
let private classifyDocArea (path: string) : DocArea =
    let slashed = path.Replace('\\', '/')

    if slashed.Contains(softwareDocPrefix, StringComparison.Ordinal) then
        SoftwareArea
    elif
        governanceDocPrefixes
        |> List.exists (fun prefix -> slashed.Contains(prefix, StringComparison.Ordinal))
    then
        GovernanceArea
    else
        UnknownArea

/// Extracts the YAML content between the first pair of `---` fences.
/// Returns `None` when `content` does not begin with `---` or has no closing
/// fence [Repo-grounded — `frontmatter.rs::extract_frontmatter`].
let extractFrontmatter (content: string) : string option =
    let lines = content.Split('\n')

    if lines.Length = 0 || lines.[0].Trim() <> "---" then
        None
    else
        [ 1 .. lines.Length - 1 ]
        |> List.tryFind (fun i -> lines.[i].Trim() = "---")
        |> Option.map (fun i -> String.Join("\n", lines.[1 .. i - 1]))

/// Deserializes raw YAML into `obj` without a naming convention — every
/// lookup below matches literal frontmatter keys (`title`, `when_to_use`, …)
/// by exact string equality rather than through a strongly typed DTO, so no
/// naming-convention translation is needed [Repo-grounded — mirrors
/// `RepoConfig.fs`'s `checkNoUnknownHarnessKeys` raw-YAML-walk technique].
let private deserializer: IDeserializer = DeserializerBuilder().Build()

let private asRawMap (value: obj) : IDictionary<obj, obj> option =
    match value with
    | :? IDictionary<obj, obj> as dict -> Some dict
    | _ -> None

let private asRawList (value: obj) : obj list option =
    match value with
    | :? IDictionary<obj, obj> -> None
    | :? Collections.IEnumerable as items when not (value :? string) -> Some(items |> Seq.cast<obj> |> List.ofSeq)
    | _ -> None

let private tryGetRawValue (dict: IDictionary<obj, obj>) (key: string) : obj option =
    dict
    |> Seq.tryFind (fun kv ->
        match kv.Key with
        | :? string as candidate -> String.Equals(candidate, key, StringComparison.Ordinal)
        | _ -> false)
    |> Option.map (fun kv -> kv.Value)

/// Coerces a raw YAML value to a `String` for display and comparison
/// purposes. `None`/`null` map to an empty string
/// [Repo-grounded — `frontmatter.rs::string_value`].
let private stringValue (value: obj option) : string =
    match value with
    | None -> ""
    | Some null -> ""
    | Some(:? string as s) -> s
    | Some(:? bool as b) -> if b then "true" else "false"
    | Some other -> other.ToString()

/// Returns `true` when `fm[key]` is a non-empty, non-whitespace-only string
/// [Repo-grounded — `frontmatter.rs::has_non_empty_string`].
let private hasNonEmptyString (fm: IDictionary<obj, obj>) (key: string) : bool =
    (stringValue (tryGetRawValue fm key)).Trim() <> ""

/// Returns `true` when `fm[key]` is a YAML sequence with at least one element
/// [Repo-grounded — `frontmatter.rs::has_non_empty_list`].
let private hasNonEmptyList (fm: IDictionary<obj, obj>) (key: string) : bool =
    match tryGetRawValue fm key |> Option.bind asRawList with
    | Some items -> not (List.isEmpty items)
    | None -> false

/// Constructs a `Blocking`-severity finding
/// [Repo-grounded — `frontmatter.rs::mk_fail`].
let private mkFail (path: string) (message: string) : Finding =
    { Severity = Severity.Blocking
      Message = message
      Path = Some path }

/// Constructs an `Advisory`-severity finding — used only for the deprecated
/// `category: software` case
/// [Repo-grounded — `frontmatter.rs::validate_software_schema`'s
/// `SEVERITY_WARN` branch].
let private mkWarn (path: string) (message: string) : Finding =
    { Severity = Severity.Advisory
      Message = message
      Path = Some path }

/// Validates the full software-engineering frontmatter schema. Required
/// fields: `title`, `description`, `category` (one of `validCategories`, or
/// the deprecated `"software"` value, which reports `Advisory` rather than
/// `Blocking`), `subcategory`, `tags` (non-empty list)
/// [Repo-grounded — `frontmatter.rs::validate_software_schema`].
///
/// Gherkin (binds) — "Software-engineering doc with all required frontmatter
/// fields passes", "...category tutorial...", "...category how-to...",
/// "...category reference...", "...category explanation..." passing
/// scenarios, and "Software-engineering doc missing title fails", "...missing
/// category field fails", "...category other than software fails", and
/// "...deprecated software category emits warn not fail" — all from
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-frontmatter.feature`.
let private validateSoftwareSchema (path: string) (fm: IDictionary<obj, obj>) : Finding list =
    let titleFinding =
        if hasNonEmptyString fm "title" then
            []
        else
            [ mkFail path "required field \"title\" is missing or empty" ]

    let descriptionFinding =
        if hasNonEmptyString fm "description" then
            []
        else
            [ mkFail path "required field \"description\" is missing or empty" ]

    let categoryFindings =
        if hasNonEmptyString fm "category" then
            let v = stringValue (tryGetRawValue fm "category")

            if Set.contains v validCategories then
                []
            elif v = "software" then
                [ mkWarn
                      path
                      "field \"category\" value \"software\" is deprecated; use one of: tutorial, how-to, reference, explanation" ]
            else
                [ mkFail
                      path
                      (sprintf
                          "field \"category\" must be one of: tutorial, how-to, reference, explanation; found \"%s\""
                          v) ]
        else
            [ mkFail path "required field \"category\" is missing or empty" ]

    let subcategoryFinding =
        if hasNonEmptyString fm "subcategory" then
            []
        else
            [ mkFail path "required field \"subcategory\" is missing or empty" ]

    let tagsFinding =
        if hasNonEmptyList fm "tags" then
            []
        else
            [ mkFail path "required field \"tags\" must be a non-empty list" ]

    titleFinding
    @ descriptionFinding
    @ categoryFindings
    @ subcategoryFinding
    @ tagsFinding

/// Validates the lighter governance-document frontmatter schema. `title` is
/// required; `description` and `when_to_use` are both `Blocking` too — FR-4
/// armed at Phase 9/16, matching `frontmatter.rs`'s current (post-dark-launch)
/// behavior [Repo-grounded — `frontmatter.rs::validate_governance_schema`].
///
/// Gherkin (binds) — "Governance doc with only title fails once when_to_use
/// and description are armed" and "Governance doc with title, description,
/// and when_to_use passes the lighter schema" —
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-frontmatter.feature`.
let private validateGovernanceSchema (path: string) (fm: IDictionary<obj, obj>) : Finding list =
    let titleFinding =
        if hasNonEmptyString fm "title" then
            []
        else
            [ mkFail path "required field \"title\" is missing or empty" ]

    let descriptionFinding =
        if hasNonEmptyString fm "description" then
            []
        else
            [ mkFail path "recommended field \"description\" is missing or empty" ]

    let whenToUseFinding =
        if hasNonEmptyString fm "when_to_use" then
            []
        else
            [ mkFail path "recommended field \"when_to_use\" is missing or empty" ]

    titleFinding @ descriptionFinding @ whenToUseFinding

/// Reads `path`, extracts its frontmatter block, parses it as YAML, and
/// delegates to the area-specific schema validator. Returns a single
/// `missing-frontmatter` finding when no `---` fence is found, or a single
/// `invalid-yaml` finding when the block is not valid YAML. A block that
/// parses to `null` or a non-mapping scalar (e.g. an empty `---\n---\n`
/// block) is treated as an empty frontmatter map — matching
/// `serde_norway::Value::get` returning `None` for every key on a
/// non-mapping value, rather than as a parse failure
/// [Repo-grounded — `frontmatter.rs::scan_frontmatter_file`].
let private scanFrontmatterFile (path: string) (area: DocArea) : Finding list =
    let data = File.ReadAllText(path)

    match extractFrontmatter data with
    | None -> [ mkFail path "file has no YAML frontmatter (delimited by `---` fences)" ]
    | Some frontmatter ->
        try
            let parsed = deserializer.Deserialize<obj>(frontmatter)

            let fm =
                asRawMap parsed
                |> Option.defaultValue (Dictionary<obj, obj>() :> IDictionary<obj, obj>)

            match area with
            | SoftwareArea -> validateSoftwareSchema path fm
            | GovernanceArea -> validateGovernanceSchema path fm
            | UnknownArea -> []
        with ex ->
            [ mkFail path (sprintf "frontmatter is not valid YAML: %s" ex.Message) ]

/// Recursively collects every file path reachable from `root`, skipping
/// directories named in `skip`. Mirrors `WalkDir`'s ability to accept either
/// a single file or a directory as its root
/// [Repo-grounded — `frontmatter.rs::walk_frontmatter_path`'s and
/// `heading_hierarchy.rs::walk_heading_hierarchy_path`'s shared `WalkDir`
/// use — parameterised over which `SKIP_DIRS` constant applies, since the
/// two validators use different lists].
let rec private collectFilesSkipping (skip: Set<string>) (root: string) : string list =
    if File.Exists root then
        [ root ]
    elif Directory.Exists root then
        Directory.GetFileSystemEntries(root)
        |> Array.sort
        |> Array.toList
        |> List.collect (fun entry ->
            if Directory.Exists entry then
                if Set.contains (Path.GetFileName entry) skip then
                    []
                else
                    collectFilesSkipping skip entry
            else
                [ entry ])
    else
        []

/// `collectFilesSkipping` specialised to the frontmatter validator's
/// `skipDirs` [Repo-grounded — `frontmatter.rs::walk_frontmatter_path`'s
/// `WalkDir` use].
let private collectFiles (root: string) : string list = collectFilesSkipping skipDirs root

/// Walks `root` recursively and collects frontmatter findings from every
/// markdown file in a recognised documentation area. Returns an empty list
/// when `root` does not exist on the filesystem
/// [Repo-grounded — `frontmatter.rs::walk_frontmatter_path`].
let private walkFrontmatterPath (root: string) : Finding list =
    collectFiles root
    |> List.filter (fun p -> p.EndsWith(".md", StringComparison.Ordinal))
    |> List.collect (fun path ->
        match classifyDocArea path with
        | UnknownArea -> []
        | area -> scanFrontmatterFile path area)

/// Validates the YAML frontmatter of every markdown file reachable from
/// `paths`. Files outside the recognised documentation areas are silently
/// skipped. The returned list is sorted by file path, then by message
/// [Repo-grounded — `frontmatter.rs::validate_docs_frontmatter`].
///
/// Gherkin (binds) — "Software-engineering doc with all required frontmatter
/// fields passes":
///   Given a software-engineering doc with title, description, category, subcategory, and tags frontmatter
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
///
/// Gherkin (binds) — "Software-engineering doc missing title fails":
///   Given a software-engineering doc whose frontmatter omits the title field
///   When the developer runs docs validate-frontmatter
///   Then the command exits with a failure code
///   And the frontmatter output identifies the missing title field
///
/// Gherkin (binds) — "Software-engineering doc missing category field fails":
///   Given a software-engineering doc whose frontmatter omits the category field
///   When the developer runs docs validate-frontmatter
///   Then the command exits with a failure code
///   And the frontmatter output identifies the missing category field
///
/// Gherkin (binds) — "Software-engineering doc with category other than software fails":
///   Given a software-engineering doc whose frontmatter declares category as something other than software
///   When the developer runs docs validate-frontmatter
///   Then the command exits with a failure code
///   And the frontmatter output identifies the wrong category value
///
/// Gherkin (binds) — "Governance doc with only title fails once when_to_use and description are armed":
///   Given a governance doc carrying only a title frontmatter field
///   When the developer runs docs validate-frontmatter
///   Then the command exits with a failure code
///   And the frontmatter output identifies the missing when-to-use field
///   And the frontmatter output identifies the missing description field
///
/// Gherkin (binds) — "Governance doc with title, description, and when_to_use passes the lighter schema":
///   Given a governance doc with title, description, and when_to_use frontmatter
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
///
/// Gherkin (binds) — "Software-engineering doc with Diataxis tutorial category passes":
///   Given a software-engineering doc with title, description, category tutorial, subcategory, and tags frontmatter
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
///
/// Gherkin (binds) — "Software-engineering doc with Diataxis how-to category passes":
///   Given a software-engineering doc with title, description, category how-to, subcategory, and tags frontmatter
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
///
/// Gherkin (binds) — "Software-engineering doc with Diataxis reference category passes":
///   Given a software-engineering doc with title, description, category reference, subcategory, and tags frontmatter
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
///
/// Gherkin (binds) — "Software-engineering doc with Diataxis explanation category passes":
///   Given a software-engineering doc with title, description, category explanation, subcategory, and tags frontmatter
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
///
/// Gherkin (binds) — "Software-engineering doc with deprecated software category emits warn not fail":
///   Given a software-engineering doc with all required frontmatter fields
///   When the developer runs docs validate-frontmatter
///   Then the command exits successfully
///   And the frontmatter output reports zero fail-level findings
let validateDocsFrontmatter (paths: string list) : Result<Finding list, string> =
    if List.isEmpty paths then
        Error "at least one path is required"
    else
        paths
        |> List.collect walkFrontmatterPath
        |> List.sortBy (fun f -> (f.Path |> Option.defaultValue "", f.Message))
        |> Ok

// ---------------------------------------------------------------------------
// docs validate-heading-hierarchy
// ---------------------------------------------------------------------------

/// One parsed ATX heading: its one-based source line number and level (1-6)
/// [Repo-grounded — `heading_hierarchy.rs::Heading`].
type private Heading = { Line: int; Level: int }

/// Parses the opening of a fenced code block from the start of a
/// (leading-whitespace-trimmed) line. Returns `Some (fenceChar, length)`
/// when the line begins with three or more identical backtick or tilde
/// characters; otherwise `None`
/// [Repo-grounded — `heading_hierarchy.rs::parse_fence_open`].
let private parseFenceOpen (s: string) : (char * int) option =
    if String.IsNullOrEmpty s then
        None
    else
        let first = s.[0]

        if first <> '`' && first <> '~' then
            None
        else
            let mutable n = 0
            let mutable i = 0

            while i < s.Length && s.[i] = first do
                n <- n + 1
                i <- i + 1

            if n < 3 then None else Some(first, n)

/// Parses the ATX heading level (1-6) from the start of a
/// (leading-whitespace-trimmed) line. Returns `None` when the line is not a
/// valid ATX heading (wrong prefix, no space/tab after the `#` run, or empty
/// heading text) [Repo-grounded — `heading_hierarchy.rs::parse_heading_level`].
let private parseHeadingLevel (s: string) : int option =
    if String.IsNullOrEmpty s || s.[0] <> '#' then
        None
    else
        let mutable level = 0

        while level < s.Length && s.[level] = '#' do
            level <- level + 1

        if level < 1 || level > 6 then
            None
        elif level >= s.Length then
            None
        else
            let next = s.[level]

            if next <> ' ' && next <> '\t' then
                None
            else
                let rest = s.Substring(level + 1).Trim()
                if rest = "" then None else Some level

/// Collects all ATX heading titles from `content` (fence-aware) as
/// `(line, level, title)` tuples. Shared by `collectHeadings` below (which
/// only needs `line`/`level`) and the links validator's anchor-slug logic
/// further down (which also needs `title`) — folding what would otherwise
/// be two near-identical fence-tracking loops into one
/// [Repo-grounded — `links.rs::collect_atx_headings`].
let private collectAtxHeadingTitles (content: string) : (int * int * string) list =
    let lines = content.Split('\n')
    let mutable inFence = false
    let mutable fenceChar = ' '
    let mutable fenceLen = 0
    let out = ResizeArray<int * int * string>()

    for i in 0 .. lines.Length - 1 do
        let lineNum = i + 1
        let trimmed = lines.[i].TrimStart([| ' '; '\t' |])

        match parseFenceOpen trimmed with
        | Some(ch, length) ->
            if not inFence then
                inFence <- true
                fenceChar <- ch
                fenceLen <- length
            elif ch = fenceChar && length >= fenceLen then
                inFence <- false
                fenceChar <- ' '
                fenceLen <- 0
        | None ->
            if not inFence then
                match parseHeadingLevel trimmed with
                | Some level ->
                    let title = trimmed.Substring(level + 1).Trim()

                    if title <> "" then
                        out.Add(lineNum, level, title)
                | None -> ()

    out |> List.ofSeq

/// Parses all ATX headings from `content`, skipping lines inside fenced code
/// blocks. A line that opens or closes a fence is itself never treated as a
/// heading candidate, matching the Rust source's `continue`-before-heading-
/// check ordering [Repo-grounded — `heading_hierarchy.rs::collect_headings`].
let private collectHeadings (content: string) : Heading list =
    collectAtxHeadingTitles content
    |> List.map (fun (line, level, _) -> { Line = line; Level = level })

/// Applies the H1-uniqueness and no-level-skipping rules to a file's parsed
/// headings. Returns an empty list when `headings` is empty (the file has no
/// headings at all) [Repo-grounded — `heading_hierarchy.rs::analyze_headings`].
///
/// Gherkin (binds) — "Tree where every .md has exactly one H1 and no skipped
/// levels passes", "File with two H1 headings fails", "File with H2 followed
/// directly by H4 (skipping H3) fails", and "Single-line file with no
/// headings is ignored (passes)" — all from
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-heading-hierarchy.feature`.
let private analyzeHeadings (path: string) (headings: Heading list) : Finding list =
    match headings with
    | [] -> []
    | _ ->
        let h1s = headings |> List.filter (fun h -> h.Level = 1)
        let h1Count = h1s.Length

        let h1Finding =
            match h1Count with
            | 0 -> [ mkFail path "markdown file has no H1 heading; every documented file must have exactly one H1" ]
            | 1 -> []
            | _ ->
                let firstH1Line = h1s.[0].Line

                [ mkFail
                      path
                      (sprintf
                          "markdown file has %d H1 headings (first at line %d); every file must have exactly one H1"
                          h1Count
                          firstH1Line) ]

        let skipFindings =
            headings
            |> List.pairwise
            |> List.choose (fun (prev, cur) ->
                if cur.Level > prev.Level + 1 then
                    Some(
                        mkFail
                            path
                            (sprintf
                                "H%d heading follows H%d, skipping H%d; heading levels must not skip"
                                cur.Level
                                prev.Level
                                (prev.Level + 1))
                    )
                else
                    None)

        h1Finding @ skipFindings

/// Reads `path`, extracts its headings, and applies the hierarchy rules
/// [Repo-grounded — `heading_hierarchy.rs::scan_file_heading_hierarchy`].
let private scanFileHeadingHierarchy (path: string) : Finding list =
    File.ReadAllText(path) |> collectHeadings |> analyzeHeadings path

/// Walks `root` recursively and validates each markdown file. Returns an
/// empty list when `root` does not exist on the filesystem
/// [Repo-grounded — `heading_hierarchy.rs::walk_heading_hierarchy_path`].
let private walkHeadingHierarchyPath (root: string) : Finding list =
    collectFilesSkipping namingSkipDirs root
    |> List.filter (fun p -> p.EndsWith(".md", StringComparison.Ordinal))
    |> List.collect scanFileHeadingHierarchy

/// Returns `true` when the repository-relative path `repoRel` is in the
/// heading-hierarchy validator's prose allowlist:
/// `docs/`, `repo-governance/`, `plans/` (except `plans/done/`), `specs/`,
/// root-level `*.md` files, `apps/<name>/README.md` and
/// `libs/<name>/README.md`, and `apps/<name>/docs/**` and
/// `libs/<name>/docs/**`. Everything else — including `.claude/`,
/// `.opencode/`, deep `apps/`/`libs/` internals, `plans/done/`, and noise
/// directories — is default-deny
/// [Repo-grounded — `heading_hierarchy.rs::is_prose_allowlisted`].
let private isProseAllowlisted (repoRel: string) : bool =
    let r = repoRel.Replace('\\', '/')

    let stripPrefix (prefix: string) (value: string) : string option =
        if value.StartsWith(prefix, StringComparison.Ordinal) then
            Some(value.Substring(prefix.Length))
        else
            None

    if r.StartsWith("plans/done/", StringComparison.Ordinal) || r = "plans/done" then
        false
    elif
        r.StartsWith("docs/", StringComparison.Ordinal)
        || r.StartsWith("repo-governance/", StringComparison.Ordinal)
        || r.StartsWith("plans/", StringComparison.Ordinal)
        || r.StartsWith("specs/", StringComparison.Ordinal)
    then
        true
    elif not (r.Contains('/')) && r.EndsWith(".md", StringComparison.Ordinal) then
        true
    else
        match stripPrefix "apps/" r |> Option.orElse (stripPrefix "libs/" r) with
        | None -> false
        | Some rest ->
            match rest.IndexOf('/') with
            | -1 -> false
            | idx ->
                let tail = rest.Substring(idx + 1)
                tail = "README.md" || tail.StartsWith("docs/", StringComparison.Ordinal)

/// Performs an allowlisted heading-hierarchy scan rooted at `repoRoot`. Only
/// files whose repository-relative path satisfies `isProseAllowlisted` are
/// checked; `excludePrefixes` are additional repository-relative prefixes to
/// skip, applied after the allowlist filter. The returned list is sorted by
/// file path, then by message
/// [Repo-grounded — `heading_hierarchy.rs::validate_docs_heading_hierarchy_allowlisted`].
///
/// Gherkin (binds) — "prose-allowlist-runs — docs file triggers a heading
/// finding", "agent-skill-file-exempt — no finding for agent or skill
/// files", "plans-done-excluded — no finding for plans/done files",
/// "exclude-flag-suppresses-tree — --exclude docs suppresses docs findings",
/// "specs-allowlisted — specs tree triggers a heading finding",
/// "app-readme-allowlisted — project-root README triggers a heading
/// finding", "app-internals-default-deny — deep app files yield no finding",
/// and "project-docs-subtree-allowlisted — app and lib docs trees trigger
/// findings" — all from
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-heading-hierarchy.feature`.
let validateDocsHeadingHierarchyAllowlisted (repoRoot: string) (excludePrefixes: string list) : Finding list =
    collectFilesSkipping namingSkipDirs repoRoot
    |> List.filter (fun p -> p.EndsWith(".md", StringComparison.Ordinal))
    |> List.choose (fun path ->
        let rel = Path.GetRelativePath(repoRoot, path).Replace('\\', '/')

        if not (isProseAllowlisted rel) then
            None
        elif
            excludePrefixes
            |> List.exists (fun pfx -> rel.StartsWith(pfx, StringComparison.Ordinal))
        then
            None
        else
            Some path)
    |> List.collect scanFileHeadingHierarchy
    |> List.sortBy (fun f -> (f.Path |> Option.defaultValue "", f.Message))

/// Validates heading hierarchy in every markdown file reachable from
/// `paths`, without any prose-allowlist filtering — the counterpart callers
/// use when they already know every supplied path should be checked. The
/// returned list is sorted by file path, then by message
/// [Repo-grounded — `heading_hierarchy.rs::validate_docs_heading_hierarchy`].
let validateDocsHeadingHierarchy (paths: string list) : Result<Finding list, string> =
    if List.isEmpty paths then
        Error "at least one path is required"
    else
        paths
        |> List.collect walkHeadingHierarchyPath
        |> List.sortBy (fun f -> (f.Path |> Option.defaultValue "", f.Message))
        |> Ok

// ---------------------------------------------------------------------------
// docs validate-links
// ---------------------------------------------------------------------------

/// Directories skipped by the links validator's full-repo walk — the
/// cross-repo noise-skip set shared by the markdown gate validators
/// (mermaid, links, heading-hierarchy) in the Rust source, a superset of
/// both `skipDirs` and `namingSkipDirs` above
/// [Repo-grounded — `links.rs::FULL_REPO_SKIP_DIRS`].
let private linksSkipDirs: Set<string> =
    Set.ofList
        [ "node_modules"
          "dist"
          "build"
          "target"
          ".next"
          "coverage"
          "generated-reports"
          "local-tmp"
          "archived"
          "apps-labs"
          "worktrees"
          ".terraform"
          "generated-contracts"
          ".nx"
          ".fvm-cache"
          ".git"
          "deps"
          "_build"
          "cover" ]

/// Path fragments identifying a skill tree, whose files are exempt from link
/// validation. `.agents/skills/` holds a byte-for-byte mirror of
/// `.claude/skills/`, so a rule keyed on the canonical path alone would
/// validate the copy while exempting the original
/// [Repo-grounded — `links.rs::SKILL_TREE_MARKERS`].
let private skillTreeMarkers: string list = [ ".claude/skills/"; ".agents/skills/" ]

/// One relative markdown link parsed out of a source line, before
/// validation [Repo-grounded — `links.rs::LinkInfo`].
type private LinkInfo = { LineNumber: int; Url: string }

/// Matches `[text](url)` markdown link syntax [Repo-grounded — `links.rs::link_re`].
let private linkRegex = Regex(@"\[([^\]]+)\]\(([^)]+)\)", RegexOptions.Compiled)

/// Matches bracket-style placeholder tokens such as `[placeholder-name]`
/// [Repo-grounded — `links.rs::bracket_placeholder_re`].
let private bracketPlaceholderRegex = Regex(@"\[[\w-]+\]", RegexOptions.Compiled)

/// Replaces inline code spans (`` `...` `` / ` ``...`` `) with spaces,
/// preserving character offsets so regex match positions remain valid
/// [Repo-grounded — `links.rs::strip_inline_code_spans`].
let private stripInlineCodeSpans (line: string) : string =
    let chars = line.ToCharArray()
    let len = chars.Length
    let mutable i = 0

    while i < len do
        if chars.[i] = '`' then
            let tickCount = if i + 1 < len && chars.[i + 1] = '`' then 2 else 1
            let start = i
            i <- i + tickCount
            let mutable found = false

            while i < len && not found do
                if tickCount = 2 && i + 1 < len && chars.[i] = '`' && chars.[i + 1] = '`' then
                    i <- i + 2
                    found <- true
                elif tickCount = 1 && chars.[i] = '`' then
                    i <- i + 1
                    found <- true
                else
                    i <- i + 1

            if found then
                for j in start .. i - 1 do
                    chars.[j] <- ' '
        else
            i <- i + 1

    String(chars)

/// Returns `true` when `link` matches a known placeholder or documentation-
/// example pattern that must not be validated against the filesystem
/// [Repo-grounded — `links.rs::should_skip_link`].
let shouldSkipLink (link: string) : bool =
    if link.StartsWith("/", StringComparison.Ordinal) then
        true
    elif link.Contains("{{<") || link.Contains("{{%") then
        true
    else
        let placeholders =
            [ "path.md"
              "target"
              "link"
              "./path/to/"
              "../path/to/"
              "path/to/convention.md"
              "path/to/practice.md"
              "path/to/rule.md"
              "./relative/path/to/" ]

        if placeholders |> List.exists link.Contains then
            true
        elif bracketPlaceholderRegex.IsMatch(link) then
            true
        elif link = "path" || link = "target" || link = "link" then
            true
        elif
            link.Contains("/images/")
            && not (link.StartsWith("../", StringComparison.Ordinal))
        then
            true
        else
            let examplePatterns =
                [ "./overview"
                  "./guide.md"
                  "./examples.md"
                  "./reference.md"
                  "./diagram.png"
                  "./image.png"
                  "./screenshots/"
                  "./auth-guide.md"
                  "by-concept/beginner"
                  "./by-example/beginner"
                  "swe/prog-lang/"
                  "../parent"
                  "./ai/"
                  "../swe/"
                  "../../advanced/"
                  "url"
                  "./LICENSE"
                  "../../features.md"
                  "../../.opencode/" ]

            examplePatterns |> List.exists link.Contains

/// Extracts every relative markdown link from `path`, skipping fenced code
/// blocks (a bare-`` ``` ``-prefix toggle, deliberately simpler than
/// `parseFenceOpen`'s tilde/length-aware tracking above — this mirrors the
/// Rust source's own, separate fence check rather than reusing the
/// heading-hierarchy one) and inline code spans, discarding external URLs,
/// `mailto:` links, and known placeholder patterns
/// [Repo-grounded — `links.rs::extract_links`].
let private extractLinks (path: string) : LinkInfo list =
    let lines = (File.ReadAllText path).Split('\n')
    let mutable inCodeBlock = false
    let links = ResizeArray<LinkInfo>()

    for i in 0 .. lines.Length - 1 do
        let lineNum = i + 1
        let line = lines.[i]

        if line.TrimStart().StartsWith("```", StringComparison.Ordinal) then
            inCodeBlock <- not inCodeBlock
        elif not inCodeBlock then
            let stripped = stripInlineCodeSpans line

            for m in linkRegex.Matches(stripped) do
                let url = m.Groups.[2].Value.TrimStart('<').TrimEnd('>')

                let isExternal =
                    url.StartsWith("http://", StringComparison.Ordinal)
                    || url.StartsWith("https://", StringComparison.Ordinal)
                    || url.StartsWith("mailto:", StringComparison.Ordinal)

                if not isExternal && not (shouldSkipLink url) then
                    links.Add { LineNumber = lineNum; Url = url }

    links |> List.ofSeq

/// Converts a heading title string to a GitHub-flavoured markdown anchor
/// slug. Rules: lowercase, remove all chars that are not alphanumeric,
/// underscore, space, or hyphen, then replace spaces with hyphens (no
/// collapsing). Verified against the `github-slugger` v2 reference
/// implementation — underscores and Unicode letters/digits are kept
/// [Repo-grounded — `links.rs::github_slug`].
let githubSlug (title: string) : string =
    title.ToLowerInvariant()
    |> Seq.choose (fun c ->
        if Char.IsLetterOrDigit c || c = '-' || c = '_' then Some c
        elif c = ' ' then Some '-'
        else None)
    |> Seq.toArray
    |> String

/// Builds a `Set` of all GitHub-slugified anchor names (with duplicate
/// collision suffixes applied in heading order) for `content`
/// [Repo-grounded — `links.rs::slugs_from_content`].
let private slugsFromContent (content: string) : Set<string> =
    let headings = collectAtxHeadingTitles content
    let mutable counts: Map<string, int> = Map.empty
    let mutable result = Set.empty

    for _, _, title in headings do
        let baseSlug = githubSlug title
        let count = counts |> Map.tryFind baseSlug |> Option.defaultValue 0

        let slug =
            if count = 0 then
                baseSlug
            else
                sprintf "%s-%d" baseSlug count

        counts <- counts |> Map.add baseSlug (count + 1)
        result <- Set.add slug result

    result

/// Splits a link's URL into its path part and an optional anchor fragment
/// (everything after the first `#`) [Repo-grounded — `links.rs::validate_file`'s
/// `hash_pos` split].
let private splitUrlFragment (url: string) : string * string option =
    match url.IndexOf('#') with
    | -1 -> url, None
    | idx -> url.Substring(0, idx), Some(url.Substring(idx + 1))

/// Resolves a relative `link` against the directory containing
/// `sourceFile`. An empty `link` (pure anchor) returns `sourceFile`
/// unchanged [Repo-grounded — `links.rs::resolve_link`/`clean_path`].
let private resolveLink (sourceFile: string) (link: string) : string =
    if link = "" then
        sourceFile
    else
        let parent =
            Path.GetDirectoryName(sourceFile) |> Option.ofObj |> Option.defaultValue ""

        Path.GetFullPath(Path.Combine(parent, link))

/// Options controlling `validateDocsLinks`'s file-selection behavior.
/// `StagedFiles`, when `Some`, is the literal list of repository-relative
/// staged paths to scan in place of a full recursive walk — mirrors
/// `checkStagedFiles`'s precedent (see `Env.fs`) of taking the staged-file
/// list as a pure function parameter rather than shelling out to git from
/// application code; the real `git diff --cached` call is a CLI-layer
/// concern for later [Repo-grounded — `links.rs::ScanOptions`].
type LinkScanOptions =
    { RepoRoot: string
      StagedFiles: string list option
      ExcludePrefixes: string list }

/// Selects the absolute paths of markdown files to scan: `opts.StagedFiles`
/// (filtered to `.md`) when `Some`, otherwise every `.md` file reachable
/// from `opts.RepoRoot` via `linksSkipDirs`-filtered recursion; either way,
/// `opts.ExcludePrefixes` is then applied against each file's
/// repository-relative path [Repo-grounded — `links.rs::get_markdown_files`,
/// `links.rs::filter_skip_paths`].
let private getMarkdownLinkFiles (opts: LinkScanOptions) : string list =
    let files =
        match opts.StagedFiles with
        | Some staged ->
            staged
            |> List.filter (fun f -> f.EndsWith(".md", StringComparison.Ordinal))
            |> List.map (fun f -> Path.Combine(opts.RepoRoot, f))
        | None ->
            collectFilesSkipping linksSkipDirs opts.RepoRoot
            |> List.filter (fun p -> p.EndsWith(".md", StringComparison.Ordinal))

    if List.isEmpty opts.ExcludePrefixes then
        files
    else
        files
        |> List.filter (fun f ->
            let rel = Path.GetRelativePath(opts.RepoRoot, f).Replace('\\', '/')

            opts.ExcludePrefixes
            |> List.forall (fun skip -> not (rel.StartsWith(skip, StringComparison.Ordinal))))

/// Validates every extracted `links` entry against the filesystem, relative
/// to `filePath`. Files inside a skill tree (see `skillTreeMarkers`) are
/// unconditionally exempt. After confirming a non-anchor-only link's target
/// exists, any anchor fragment is validated against the target's (or, for a
/// pure `#fragment` link, the source file's) heading slugs
/// [Repo-grounded — `links.rs::validate_file`].
let private validateFileLinks (repoRoot: string) (filePath: string) (links: LinkInfo list) : Finding list =
    let normalizedPath = filePath.Replace('\\', '/')

    if skillTreeMarkers |> List.exists normalizedPath.Contains then
        []
    else
        let rel = Path.GetRelativePath(repoRoot, filePath).Replace('\\', '/')

        links
        |> List.collect (fun link ->
            let pathPart, fragment = splitUrlFragment link.Url

            if pathPart = "" then
                match fragment with
                | Some frag when frag <> "" ->
                    let slugs = slugsFromContent (File.ReadAllText filePath)

                    if Set.contains frag slugs then
                        []
                    else
                        [ mkFail
                              rel
                              (sprintf "link \"#%s\" in %s does not match any heading anchor in this file" frag rel) ]
                | _ -> []
            else
                let target = resolveLink filePath pathPart

                if not (File.Exists target || Directory.Exists target) then
                    [ mkFail rel (sprintf "link \"%s\" in %s points to a non-existent file: %s" link.Url rel target) ]
                else
                    match fragment with
                    | Some frag when frag <> "" ->
                        let slugs = slugsFromContent (File.ReadAllText target)

                        if Set.contains frag slugs then
                            []
                        else
                            let targetRel = Path.GetRelativePath(repoRoot, target).Replace('\\', '/')

                            [ mkFail
                                  rel
                                  (sprintf
                                      "link \"#%s\" in %s does not match any heading anchor in %s"
                                      frag
                                      rel
                                      targetRel) ]
                    | _ -> [])

/// Validates every relative markdown link (and anchor fragment) reachable
/// from `opts.RepoRoot`, per `opts`'s staged-file and exclude-prefix
/// filters. The returned list is sorted by file path, then by message
/// [Repo-grounded — `links.rs::validate_all_links`].
///
/// Gherkin (binds) — "A document set with all valid internal links passes
/// validation":
///   Given markdown files where all internal links point to existing files
///   When the developer runs docs validate-links
///   Then the command exits successfully
///   And the output reports no broken links found
///
/// Gherkin (binds) — "A broken internal link is detected and reported":
///   Given a markdown file with a link pointing to a non-existent file
///   When the developer runs docs validate-links
///   Then the command exits with a failure code
///   And the output identifies the file containing the broken link
///
/// Gherkin (binds) — "External URLs are not validated":
///   Given a markdown file containing only external HTTPS links
///   When the developer runs docs validate-links
///   Then the command exits successfully
///   And the output reports no broken links found
///
/// Gherkin (binds) — "With --staged-only only staged files are checked":
///   Given a markdown file with a broken link that has not been staged in git
///   When the developer runs docs validate-links with the --staged-only flag
///   Then the command exits successfully
///
/// Gherkin (binds) — "exclude flag skips the named subtree":
///   Given a markdown file under plans/done with a broken internal link
///   And a markdown file under docs with a different broken internal link
///   When the developer runs docs validate-links with --exclude plans/done
///   Then the command exits with a failure code
///   And the output does not mention the plans/done file
///   But the output does mention the docs file
///
/// Gherkin (binds) — "repo-wide scan finds broken link outside original
/// three-directory scope":
///   Given a markdown file under libs with a broken internal link
///   When the developer runs docs validate-links
///   Then the command exits with a failure code
///   And the output identifies the libs file containing the broken link
///
/// Gherkin (binds) — "valid anchor link passes validation":
///   Given a markdown file that links to an existing heading anchor in another file
///   When the developer runs docs validate-links
///   Then the command exits successfully
///   And the output reports no broken links found
///
/// Gherkin (binds) — "broken anchor link produces a broken-anchor finding":
///   Given a markdown file that links to a non-existent heading anchor in an existing file
///   When the developer runs docs validate-links
///   Then the command exits with a failure code
///   And the output identifies the broken anchor
///
/// Gherkin (binds) — "same-file anchor with no matching heading produces a
/// broken-anchor finding":
///   Given a markdown file containing a same-file anchor link that has no matching heading
///   When the developer runs docs validate-links
///   Then the command exits with a failure code
///   And the output identifies the broken same-file anchor
///
/// Gherkin (binds) — "anchor slugs keep underscores per the GitHub
/// reference algorithm":
///   Given a markdown file that links to the anchor "#snake_case" of a file whose heading is "snake_case"
///   When the developer runs docs validate-links
///   Then the command exits successfully
///   And the output reports no broken links found
let validateDocsLinks (opts: LinkScanOptions) : Finding list =
    getMarkdownLinkFiles opts
    |> List.collect (fun path -> validateFileLinks opts.RepoRoot path (extractLinks path))
    |> List.sortBy (fun f -> (f.Path |> Option.defaultValue "", f.Message))
