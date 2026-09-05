/// Specification corpus structure, cardinality, links, and scaffold support.
module RhinoCli.Application.Specs

open System
open System.IO
open System.Text

// ---------------------------------------------------------------------------
// Spec-tree validators
// [Repo-grounded — `apps/rhino-cli/src/application/specs.rs`] for
// `validate-adoption.feature`, `validate-counts.feature`, and
// `validate-tree.feature`.
// ---------------------------------------------------------------------------

/// A single validation finding produced by one of the `validateSpec*`
/// functions.
type SpecFinding =
    {
        /// Validation category (`"adoption"`, `"count"`, `"links"`,
        /// `"tree-shape"`).
        Category: string
        /// Severity level: `"HIGH"`, `"MEDIUM"`, or `"LOW"`.
        Criticality: string
        /// Repo-relative path to the offending file or directory.
        File: string
        /// Human-readable description of what was found.
        Evidence: string
        /// Suggested remediation step.
        Expected: string
    }

/// In-memory specification tree used by mandatory Unit tests. Directories
/// are explicit so an empty `behaviours/` directory remains distinguishable
/// from an absent one; file content supports pure cardinality/link checks.
type SpecTree =
    { Directories: Set<string>
      Files: Map<string, string> }

let private treeRetiredSpecFolders =
    [ "product"; "system-context"; "containers"; "components"; "behavior" ]

let private normalizeSpecPath (path: string) : string = path.Replace('\\', '/').Trim('/')

let private treeHasDirectory (tree: SpecTree) (path: string) : bool =
    Set.contains (normalizeSpecPath path) tree.Directories

let private treeHasFile (tree: SpecTree) (path: string) : bool =
    Map.containsKey (normalizeSpecPath path) tree.Files

let private treeFilesUnder (tree: SpecTree) (root: string) : string list =
    let prefix = normalizeSpecPath root

    tree.Files
    |> Map.keys
    |> Seq.filter (fun path -> path = prefix || path.StartsWith(prefix + "/", StringComparison.Ordinal))
    |> Seq.sortWith (fun left right -> String.CompareOrdinal(left, right))
    |> List.ofSeq

let private treeImmediateDirectories (tree: SpecTree) (root: string) : string list =
    let prefix = normalizeSpecPath root
    let childPrefix = if prefix = "" then "" else prefix + "/"

    tree.Directories
    |> Seq.choose (fun path ->
        if path.StartsWith(childPrefix, StringComparison.Ordinal) then
            let rest = path.Substring(childPrefix.Length)

            if rest <> "" && not (rest.Contains('/')) then
                Some path
            else
                None
        else
            None)
    |> Seq.sortWith (fun left right -> String.CompareOrdinal(left, right))
    |> List.ofSeq

let private treeOwnerCorpusDirectories (tree: SpecTree) (productRel: string) : string list =
    treeImmediateDirectories tree productRel
    |> List.filter (fun owner -> treeHasFile tree (owner + "/architecture.md"))

let private missingEntry (ownerRel: string) (name: string) (expected: string) : SpecFinding =
    { Category = "tree-shape"
      Criticality = "HIGH"
      File = sprintf "%s/%s" ownerRel name
      Evidence = sprintf "missing required entry: %s" name
      Expected = expected }

/// Pure owner-corpus validation over an explicit in-memory tree.
let validateOwnerCorpusTree (tree: SpecTree) (ownerRel: string) : SpecFinding list =
    let readmeFindings =
        if treeHasFile tree (ownerRel + "/README.md") then
            []
        else
            [ missingEntry ownerRel "README.md" (sprintf "create %s/README.md indexing the corpus" ownerRel) ]

    let architectureFindings =
        if treeHasFile tree (ownerRel + "/architecture.md") then
            []
        else
            [ missingEntry
                  ownerRel
                  "architecture.md"
                  (sprintf "create %s/architecture.md describing the current as-built system" ownerRel) ]

    let behavioursRel = ownerRel + "/behaviours"

    let behavioursFindings =
        if not (treeHasDirectory tree behavioursRel) then
            [ missingEntry
                  ownerRel
                  "behaviours"
                  (sprintf "create %s/behaviours/ with at least one .feature file" ownerRel) ]
        elif
            treeFilesUnder tree behavioursRel
            |> List.exists (fun path -> path.EndsWith(".feature", StringComparison.OrdinalIgnoreCase))
            |> not
        then
            [ { Category = "adoption"
                Criticality = "HIGH"
                File = behavioursRel
                Evidence = sprintf "no feature files found under %s/" behavioursRel
                Expected = sprintf "add at least one .feature file under %s/" behavioursRel } ]
        elif not (treeHasFile tree (behavioursRel + "/README.md")) then
            [ missingEntry
                  ownerRel
                  "behaviours/README.md"
                  (sprintf "create %s/README.md indexing the corpus" behavioursRel) ]
        else
            []

    readmeFindings @ architectureFindings @ behavioursFindings

let private treeNotAdoptedFinding (app: string) : SpecFinding =
    { Category = "adoption"
      Criticality = "HIGH"
      File = sprintf "specs/apps/%s" app
      Evidence = sprintf "no logical owner corpus found under specs/apps/%s/" app
      Expected =
        sprintf "create specs/apps/%s/<owner>/ with README.md, architecture.md, and a non-empty behaviours/" app }

/// Pure adoption validation used by mandatory Unit scenarios.
let validateSpecAdoptionTree (tree: SpecTree) (app: string) : SpecFinding list =
    let productRel = sprintf "specs/apps/%s" app

    let dddFindings =
        if treeHasDirectory tree (productRel + "/ddd") then
            [ { Category = "adoption"
                Criticality = "HIGH"
                File = productRel + "/ddd"
                Evidence = sprintf "retired ddd/ tree still present at %s/ddd" productRel
                Expected = sprintf "remove %s/ddd/" productRel } ]
        else
            []

    if List.isEmpty (treeOwnerCorpusDirectories tree productRel) then
        treeNotAdoptedFinding app :: dddFindings
    else
        dddFindings

/// Pure product-tree validation used by mandatory Unit scenarios.
let validateSpecTreeEntries (tree: SpecTree) (app: string) : SpecFinding list =
    let productRel = sprintf "specs/apps/%s" app
    let owners = treeOwnerCorpusDirectories tree productRel

    if List.isEmpty owners then
        [ treeNotAdoptedFinding app ]
    else
        let ownerFindings = owners |> List.collect (validateOwnerCorpusTree tree)

        let leftovers =
            treeRetiredSpecFolders
            |> List.filter (fun name -> treeHasDirectory tree (productRel + "/" + name))
            |> List.map (fun name ->
                { Category = "tree-shape"
                  Criticality = "HIGH"
                  File = sprintf "%s/%s" productRel name
                  Evidence = sprintf "legacy folder %s survives beside a logical owner corpus" name
                  Expected =
                    sprintf "fold %s/%s into the owning corpus's architecture.md and delete it" productRel name })

        ownerFindings @ leftovers

/// Pure count/shape validation used by mandatory Unit scenarios.
let validateSpecCountsTree (tree: SpecTree) (folder: string) : SpecFinding list =
    let normalized = normalizeSpecPath folder

    if not (treeHasDirectory tree normalized || treeHasFile tree normalized) then
        [ { Category = "count"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "spec folder does not exist: %s" folder
            Expected = "create the spec folder as a logical owner corpus" } ]
    elif treeHasFile tree (normalized + "/architecture.md") then
        validateOwnerCorpusTree tree normalized
    elif not (List.isEmpty (treeOwnerCorpusDirectories tree normalized)) then
        []
    else
        [ { Category = "count"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "%s is neither a logical owner corpus nor a product holding one" folder
            Expected =
              sprintf "give %s a architecture.md and a non-empty behaviours/, or place its owners beneath it" folder } ]

/// Pure Markdown-link validation for one specification subtree.
let validateSpecLinksTree (tree: SpecTree) (folder: string) : SpecFinding list =
    let normalized = normalizeSpecPath folder

    if not (treeHasDirectory tree normalized) then
        [ { Category = "links"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "spec folder does not exist: %s" folder
            Expected = "create the spec folder with required subfolders" } ]
    else
        tree.Files
        |> Map.toList
        |> List.filter (fun (path, _) ->
            path = normalized || path.StartsWith(normalized + "/", StringComparison.Ordinal))
        |> fun documents -> Md.validateDocsLinksDocuments documents None []
        |> List.map (fun finding ->
            { Category = "links"
              Criticality = "HIGH"
              File = finding.Path |> Option.defaultValue folder
              Evidence = sprintf "broken link: %s" finding.Message
              Expected = "point the link at an existing file, or remove it" })

/// The five folder names the retired C4 tree used. No product is measured
/// against them any more; they survive only so a directory left behind beside a
/// logical owner corpus is reported rather than ignored.
let retiredSpecFolders: string list =
    [ "product"; "system-context"; "containers"; "components"; "behavior" ]

/// Ordinal path sort matching Rust's `PathBuf` ordering.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let private sortPaths (paths: string list) : string list =
    paths |> List.sortWith (fun a b -> String.CompareOrdinal(a, b))

/// Recursively walks `dir` returning all files whose name ends with
/// `suffix` (case-insensitively), in sorted order. Returns an empty list if
/// `dir` cannot be read.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let rec private walkBySuffix (dir: string) (suffix: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let entries =
            try
                Directory.GetFileSystemEntries dir |> List.ofArray |> sortPaths
            with _ ->
                []

        entries
        |> List.collect (fun path ->
            if Directory.Exists path then
                walkBySuffix path suffix
            elif Path.GetFileName(path).ToLowerInvariant().EndsWith(suffix, StringComparison.Ordinal) then
                [ path ]
            else
                [])

/// Recursively walks `dir` and returns all `.feature` files in sorted order.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let walkFeatureFiles (dir: string) : string list = walkBySuffix dir ".feature"

/// Recursively walks `dir` and returns all `.md` files in sorted order.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let walkMdFiles (dir: string) : string list = walkBySuffix dir ".md"

/// Counts `.feature` files and non-`README.md` `.md` files under `dir`
/// recursively. `README.md` is the required per-folder index, not a spec, so
/// it never counts.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let countNonReadmeMdFiles (dir: string) : int =
    if not (Directory.Exists dir) then
        0
    else
        Directory.EnumerateFiles(dir, "*", SearchOption.AllDirectories)
        |> Seq.filter (fun path ->
            let name = Path.GetFileName path
            let lower = name.ToLowerInvariant()

            lower.EndsWith(".feature", StringComparison.Ordinal)
            || (lower.EndsWith(".md", StringComparison.Ordinal)
                && not (String.Equals(name, "README.md", StringComparison.OrdinalIgnoreCase))))
        |> Seq.length

/// The canonical as-built C4 document every logical owner corpus carries.
[<Literal>]
let ArchitectureFileName = "architecture.md"

/// The recursive Gherkin root every logical owner corpus carries.
[<Literal>]
let BehavioursFolderName = "behaviours"

/// The immediate subdirectories of `productDir` that have adopted the logical
/// owner-corpus shape. Adoption is detected positively — the directory carries
/// an `architecture.md` — so a half-migrated product is measured against the
/// shape it is moving to rather than silently against the one it is leaving.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let ownerCorpusDirectories (productDir: string) : string list =
    if not (Directory.Exists productDir) then
        []
    else
        Directory.GetDirectories productDir
        |> List.ofArray
        |> sortPaths
        |> List.filter (fun dir -> File.Exists(Path.Combine(dir, ArchitectureFileName)))

/// Every finding for the one logical owner corpus rooted at `ownerRel`
/// (repository-relative). The corpus carries its index, its canonical as-built
/// architecture document, and a non-empty recursive `behaviours/` tree; an owner
/// that declares no behaviour is an owner nothing can prove.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let validateOwnerCorpus (repoRoot: string) (ownerRel: string) : SpecFinding list =
    let abs = Path.Combine(repoRoot, ownerRel)

    let missing (name: string) (expected: string) : SpecFinding =
        { Category = "tree-shape"
          Criticality = "HIGH"
          File = sprintf "%s/%s" ownerRel name
          Evidence = sprintf "missing required entry: %s" name
          Expected = expected }

    let readmeFindings =
        if File.Exists(Path.Combine(abs, "README.md")) then
            []
        else
            [ missing "README.md" (sprintf "create %s/README.md indexing the corpus" ownerRel) ]

    let architectureFindings =
        if File.Exists(Path.Combine(abs, ArchitectureFileName)) then
            []
        else
            [ missing
                  ArchitectureFileName
                  (sprintf "create %s/%s describing the current as-built system" ownerRel ArchitectureFileName) ]

    let behavioursDir = Path.Combine(abs, BehavioursFolderName)

    let behavioursFindings =
        if not (Directory.Exists behavioursDir) then
            [ missing
                  BehavioursFolderName
                  (sprintf "create %s/%s/ with at least one .feature file" ownerRel BehavioursFolderName) ]
        elif List.isEmpty (walkFeatureFiles behavioursDir) then
            [ { Category = "adoption"
                Criticality = "HIGH"
                File = sprintf "%s/%s" ownerRel BehavioursFolderName
                Evidence = sprintf "no feature files found under %s/%s/" ownerRel BehavioursFolderName
                Expected = sprintf "add at least one .feature file under %s/%s/" ownerRel BehavioursFolderName } ]
        elif not (File.Exists(Path.Combine(behavioursDir, "README.md"))) then
            [ missing
                  (BehavioursFolderName + "/README.md")
                  (sprintf "create %s/%s/README.md indexing the corpus" ownerRel BehavioursFolderName) ]
        else
            []

    readmeFindings @ architectureFindings @ behavioursFindings

/// Every finding for a product directory that has adopted the logical
/// owner-corpus shape: each corpus is validated, and any surviving five-folder
/// scaffolding beside it is reported, because a product cannot be half in one
/// shape and half in the other once the move has begun.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let validateProductCorpus (repoRoot: string) (app: string) : SpecFinding list =
    let productRel = sprintf "specs/apps/%s" app
    let productDir = Path.Combine(repoRoot, productRel)

    let ownerFindings =
        ownerCorpusDirectories productDir
        |> List.collect (fun dir -> validateOwnerCorpus repoRoot (sprintf "%s/%s" productRel (Path.GetFileName dir)))

    let leftovers =
        retiredSpecFolders
        |> List.filter (fun name -> Directory.Exists(Path.Combine(productDir, name)))
        |> List.map (fun name ->
            { Category = "tree-shape"
              Criticality = "HIGH"
              File = sprintf "%s/%s" productRel name
              Evidence = sprintf "legacy folder %s survives beside a logical owner corpus" name
              Expected =
                sprintf "fold %s/%s into the owning corpus's %s and delete it" productRel name ArchitectureFileName })

    ownerFindings @ leftovers

/// True when `dir` is itself a logical owner corpus root. A library owns
/// exactly one surface, so it adopts the shape at its own root with no product
/// directory to nest an owner under; the same positive signal — an
/// `architecture.md` — decides it.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let isOwnerCorpusRoot (dir: string) : bool =
    File.Exists(Path.Combine(dir, ArchitectureFileName))

/// True when `app` has begun the move to the logical owner-corpus shape, which
/// is the one place that decides which rule set the three product-level
/// validators apply.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let hasOwnerCorpus (repoRoot: string) (app: string) : bool =
    ownerCorpusDirectories (Path.Combine(repoRoot, "specs/apps", app))
    |> List.isEmpty
    |> not

/// The finding reported when `app` carries no logical owner corpus at all.
/// Adoption is positive: a product proves the shape by having one, so its
/// absence is the whole of the adoption failure.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let private notAdoptedFinding (app: string) : SpecFinding =
    { Category = "adoption"
      Criticality = "HIGH"
      File = sprintf "specs/apps/%s" app
      Evidence = sprintf "no logical owner corpus found under specs/apps/%s/" app
      Expected =
        sprintf "create specs/apps/%s/<owner>/ with README.md, %s, and a non-empty behaviours/" app ArchitectureFileName }

/// Checks that `app` has adopted the logical owner-corpus shape and carries no
/// retired `ddd/` tree. DDD is no longer an engineering-facing specification
/// surface, so any surviving `specs/apps/<app>/ddd/` directory is a finding
/// rather than a requirement.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let validateSpecAdoption (repoRoot: string) (app: string) : SpecFinding list =
    let dddDir = Path.Combine(repoRoot, "specs/apps", app, "ddd")

    let dddFindings =
        if Directory.Exists dddDir then
            [ { Category = "adoption"
                Criticality = "HIGH"
                File = sprintf "specs/apps/%s/ddd" app
                Evidence = sprintf "retired ddd/ tree still present at specs/apps/%s/ddd" app
                Expected = sprintf "remove specs/apps/%s/ddd/" app } ]
        else
            []

    if hasOwnerCorpus repoRoot app then
        dddFindings
    else
        notAdoptedFinding app :: dddFindings

/// Checks that `folder` is a logical owner corpus, or a product directory whose
/// owners are, and reports what the corpus rules find missing.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let validateSpecCounts (repoRoot: string) (folder: string) : SpecFinding list =
    let abs =
        if Path.IsPathRooted folder then
            folder
        else
            Path.Combine(repoRoot, folder)

    if not (Directory.Exists abs || File.Exists abs) then
        [ { Category = "count"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "spec folder does not exist: %s" folder
            Expected = "create the spec folder as a logical owner corpus" } ]
    elif isOwnerCorpusRoot abs then
        // A library carries its corpus at the folder root, so the corpus rules
        // are the whole check.
        let ownerRel =
            if Path.IsPathRooted folder then
                Path.GetRelativePath(repoRoot, abs).Replace('\\', '/')
            else
                folder.TrimEnd('/')

        validateOwnerCorpus repoRoot ownerRel
    elif not (List.isEmpty (ownerCorpusDirectories abs)) then
        // A product directory holds no corpus content of its own; each owner
        // beneath it is measured by the tree-shape rules instead.
        []
    else
        [ { Category = "count"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "%s is neither a logical owner corpus nor a product holding one" folder
            Expected =
              sprintf
                  "give %s a %s and a non-empty behaviours/, or place its owners beneath it"
                  folder
                  ArchitectureFileName } ]

/// Checks the spec tree for `app` against the logical owner-corpus shape, which
/// is now the only shape there is.
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let validateSpecTree (repoRoot: string) (app: string) : SpecFinding list =
    if hasOwnerCorpus repoRoot app then
        validateProductCorpus repoRoot app
    else
        [ notAdoptedFinding app ]

// ---------------------------------------------------------------------------
// `specs audit` aggregation
// [Repo-grounded — `apps/rhino-cli/src/commands/specs_audit.rs`] for
// `specs-audit.feature`.
// ---------------------------------------------------------------------------

/// Member validators `specs audit` runs, in order. Static behaviour coverage
/// remains an Nx project target because it requires owner/adapter arguments.
let specsAuditMembers: string list = [ "structure-validate"; "validate-links" ]

/// The aggregated result of one `specs audit` run.
type SpecsAuditOutcome =
    {
        /// `true` when every non-skipped member passed.
        Passed: bool
        /// The single summary line printed to stdout (pass) or stderr (fail).
        Summary: string
        /// `"<member>: <error>"` for each failing member, in member order.
        Failures: string list
    }

/// Runs each non-skipped member through `runMember` and aggregates the result.
let runSpecsAudit (skip: string list) (runMember: string -> Result<unit, string>) : SpecsAuditOutcome =
    let failures =
        specsAuditMembers
        |> List.filter (fun name -> not (List.contains name skip))
        |> List.choose (fun name ->
            match runMember name with
            | Ok() -> None
            | Error message -> Some(sprintf "%s: %s" name message))

    if List.isEmpty failures then
        { Passed = true
          Summary =
            sprintf "SPECS AUDIT PASSED: all %d validators passed" (List.length specsAuditMembers - List.length skip)
          Failures = [] }
    else
        { Passed = false
          Summary = sprintf "SPECS AUDIT FAILED: %d validator(s) reported failures" (List.length failures)
          Failures = failures }

/// Validates every relative markdown link reachable from `folder`, reported
/// as `"links"` findings. A `folder` that does not exist is itself a
/// `"HIGH"` finding rather than an empty pass
/// [Repo-grounded — `specs_audit.rs` routes `validate-links` through
/// `md_validate_links::run`, whose engine is `Md.validateDocsLinks`].
[<System.Diagnostics.CodeAnalysis.ExcludeFromCodeCoverage>]
let validateSpecLinks (repoRoot: string) (folder: string) : SpecFinding list =
    let abs =
        if Path.IsPathRooted folder then
            folder
        else
            Path.Combine(repoRoot, folder)

    if not (Directory.Exists abs) then
        [ { Category = "links"
            Criticality = "HIGH"
            File = folder
            Evidence = sprintf "spec folder does not exist: %s" folder
            Expected = "create the spec folder with required subfolders" } ]
    else
        Md.validateDocsLinks
            { RepoRoot = abs
              StagedFiles = None
              ExcludePrefixes = [] }
        |> List.map (fun finding ->
            { Category = "links"
              Criticality = "HIGH"
              File = finding.Path |> Option.defaultValue folder
              Evidence = sprintf "broken link: %s" finding.Message
              Expected = "point the link at an existing file, or remove it" })

/// Renders `findings` the way `specs structure validate` prints them —
/// `"<category>: <file>: HIGH: <evidence>"` per finding — followed by the
/// per-app `"0 finding(s)"` line when nothing was found
/// [Repo-grounded — `specs_structure_validate.rs::run_at_root`].
let formatSpecFindingsText (app: string) (findings: SpecFinding list) : string =
    if List.isEmpty findings then
        sprintf "specs structure validate: 0 finding(s) for \"%s\"\n" app
    else
        findings
        |> List.map (fun f -> sprintf "%s: %s: HIGH: %s\n" f.Category f.File f.Evidence)
        |> String.concat ""
