/// Port of the Rust `md` namespace's `docs validate-frontmatter` validator
/// [Repo-grounded — `apps/rhino-cli/src/application/docs/frontmatter.rs`,
/// `apps/rhino-cli/src/commands/md_validate_frontmatter.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/md/docs-validate-frontmatter.feature`'s
/// 11 scenarios.
///
/// Scope: this PR ports only the frontmatter validator — the `md` namespace's
/// other five feature files (heading-hierarchy, links, mermaid, naming,
/// audit) land in later Wave D PRs against this same file. Findings reuse
/// the shared `RhinoCli.Domain.Types.Finding` record (`Severity`/`Message`/
/// `Path`) rather than a bespoke `DocsFrontmatterFinding` type, matching
/// `Convention.fs`'s established "shared Finding over bespoke per-validator
/// types" precedent — the Rust source's separate `kind` field (e.g.
/// `"missing-title"`) is folded into each finding's `Message` text instead of
/// becoming a fourth field on the shared record, since every Rust `kind`
/// value is already reproduced verbatim inside its finding's message text,
/// and no scenario here needs the two split apart.
///
/// `md` is not yet listed in `FSHARP_NAMESPACES` (that flip is later,
/// separate Wave D integration work), so — matching `TestCoverage.fs`'s
/// `validate`-before-the-Wave-C-flip precedent — this validator is called
/// directly by its step definitions with a path list built by hand, not
/// parsed from CLI argv. No text/JSON/Markdown rendering lives in this file
/// for the same reason `reporter.rs`'s formatting stays out of `Doctor.fs`
/// until a scenario needs it: none of this feature file's 11 scenarios
/// assert on rendered output, only on the structured `Finding` list.
module RhinoCli.Application.Md

open System
open System.Collections.Generic
open System.IO
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
/// directories named in `skipDirs`. Mirrors `WalkDir`'s ability to accept
/// either a single file or a directory as its root
/// [Repo-grounded — `frontmatter.rs::walk_frontmatter_path`'s `WalkDir` use].
let rec private collectFiles (root: string) : string list =
    if File.Exists root then
        [ root ]
    elif Directory.Exists root then
        Directory.GetFileSystemEntries(root)
        |> Array.sort
        |> Array.toList
        |> List.collect (fun entry ->
            if Directory.Exists entry then
                if Set.contains (Path.GetFileName entry) skipDirs then
                    []
                else
                    collectFiles entry
            else
                [ entry ])
    else
        []

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
