/// Port of the Rust `governance` namespace's `readme-index` validator —
/// core sibling-index audit (orphan/ghost/missing detection across a
/// directory's `README.md` and, for a split directory, its parent's
/// sibling `<name>.md` index file)
/// [Repo-grounded — `apps/rhino-cli/src/application/governance/readme_index.rs`,
/// `apps/rhino-cli/src/commands/governance_validate_readme_index.rs`] for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/governance/governance-readme-index.feature`'s
/// scenarios 1-9 ("A complete index passes" through "A generated mirror
/// directory is not scanned").
///
/// This is PR8a of a three-way split (the feature file's 19 scenarios
/// exceed this repository's per-PR line ceilings — see `delivery.md`'s
/// `governance-readme-index.feature` heading). PR8b adds the `Unannotated`
/// finding kind, `hasFailingFinding`, the gate-id-rename registry check,
/// and the `--paths`/`--fail-kinds` flags (scenarios 10-14); PR8c adds
/// `generate`/`rewrite-paths` (scenarios 15-19) and asserts
/// `specs:behavior:coverage` green for the whole feature file.
///
/// Findings use a bespoke `ReadmeIndexFinding` record carrying a structured
/// `Kind` (`Orphan`/`Ghost`/`Missing` here; `Unannotated` arrives in PR8b),
/// not the shared `RhinoCli.Domain.Types.Finding` record — the eventual
/// `--fail-kinds` scenario needs to filter on kind structurally, which the
/// shared record cannot express, same rationale `Md.fs`'s mermaid section
/// already used for its own bespoke types.
///
/// `governance` is not yet listed in `FSHARP_NAMESPACES` (that flip is
/// later, separate Wave D integration work), so — matching every other
/// Wave D PR's precedent — `auditReadmeIndex` is called directly by step
/// definitions with an explicit path list, never through CLI argv parsing.
module RhinoCli.Application.Governance

open System
open System.IO
open System.Text.RegularExpressions

/// Machine-readable violation category
/// [Repo-grounded — `readme_index.rs::ReadmeIndexFinding::kind`]. The
/// `Unannotated` case arrives in PR8b.
[<RequireQualifiedAccess>]
type ReadmeIndexFindingKind =
    | Orphan
    | Ghost
    | Missing

    /// The lowercase name this kind is addressed by in `--fail-kinds`.
    member this.Name =
        match this with
        | Orphan -> "orphan"
        | Ghost -> "ghost"
        | Missing -> "missing"

/// One reported problem from the README index audit
/// [Repo-grounded — `readme_index.rs::ReadmeIndexFinding`].
type ReadmeIndexFinding =
    { File: string
      Severity: string
      Kind: ReadmeIndexFindingKind
      Message: string }

/// Directory names skipped during every recursive walk
/// [Repo-grounded — `readme_index.rs::SKIP_DIRS`].
let private skipDirs: Set<string> =
    set [ "node_modules"; "target"; "dist"; "build"; ".next"; ".git" ]

/// Matches a Markdown link whose href ends with `.md` (optionally with a
/// fragment or query string), tolerating one level of nested square brackets
/// in the link text [Repo-grounded — `readme_index.rs::readme_link_re`].
let private readmeLinkRegex =
    Regex(@"\[(?:[^\[\]]|\[[^\[\]]*\])+\]\(([^)]*\.md(?:[#?][^)]*)?)\)", RegexOptions.Compiled)

/// Every content tree the repository governs by default when `--paths` is
/// absent [Repo-grounded —
/// `governance_validate_readme_index.rs::DEFAULT_PATHS`]. The generated
/// harness mirrors (`.opencode/`, `.codex/`) are deliberately absent — see
/// that constant's doc comment.
let defaultPaths: string list =
    [ "docs/"; "repo-governance/"; "specs/"; ".claude/" ]

/// Resolves the scan-path list for a `validate` invocation: an explicit,
/// non-empty `paths` list wins; `defaultPaths` is used unchanged otherwise
/// [Repo-grounded — `governance_validate_readme_index.rs::resolve_scan_paths`].
let resolveScanPaths (paths: string list) : string list =
    if List.isEmpty paths then defaultPaths else paths

/// Splits a raw markdown link target into its path part and any trailing
/// `#fragment`/`?query` suffix [Repo-grounded —
/// `readme_index.rs::split_link_suffix`].
let private splitLinkSuffix (target: string) : string * string =
    let idx = target.IndexOfAny([| '#'; '?' |])

    if idx >= 0 then
        target.Substring(0, idx), target.Substring(idx)
    else
        target, ""

/// Normalises a raw markdown link target into the canonical sibling-target
/// form the audit logic compares on, or `None` when it is not a sibling
/// target at all (empty, absolute, parent-relative, or a URL)
/// [Repo-grounded — `readme_index.rs::normalize_link_target`].
let private normalizeLinkTarget (raw: string) : string option =
    let raw = raw.Trim()

    if raw = "" then
        None
    else
        let raw =
            if raw.StartsWith("./", StringComparison.Ordinal) then
                raw.Substring(2)
            else
                raw

        let raw, _ = splitLinkSuffix raw

        if
            raw = ""
            || raw.StartsWith("/", StringComparison.Ordinal)
            || raw.StartsWith("..", StringComparison.Ordinal)
        then
            None
        else
            let colonIdx = raw.IndexOf(':')

            let urlLike =
                if colonIdx > 0 then
                    let slashIdx = raw.IndexOf('/')
                    slashIdx < 0 || colonIdx < slashIdx
                else
                    false

            if urlLike then None else Some(raw.Replace('\\', '/'))

/// Extracts every sibling `.md` link target found anywhere in `content`,
/// normalised by [`normalizeLinkTarget`]
/// [Repo-grounded — `readme_index.rs::extract_readme_links`].
let private extractReadmeLinks (content: string) : Set<string> =
    readmeLinkRegex.Matches(content)
    |> Seq.cast<Match>
    |> Seq.choose (fun m -> normalizeLinkTarget m.Groups.[1].Value)
    |> Set.ofSeq

/// The set of linkable targets adjacent to an index file
/// [Repo-grounded — `readme_index.rs::SiblingTargets`].
type private SiblingTargets =
    { Files: Set<string>
      SubDirs: Set<string> }

    static member Empty: SiblingTargets =
        { Files = Set.empty
          SubDirs = Set.empty }

    /// Every linkable target name, sorted.
    member this.SortedNames: string list =
        Set.union this.Files this.SubDirs |> Set.toList |> List.sort

    /// Returns `true` when `link` refers to a file or subdirectory present on
    /// disk, including a bare-directory link (`"structure"` resolves to
    /// `"structure/README.md"`).
    member this.Present(link: string) : bool =
        let normalized = link.Replace('\\', '/').TrimEnd('/')

        if this.Files.Contains normalized || this.SubDirs.Contains normalized then
            true
        else
            this.SubDirs.Contains(normalized + "/README.md")

/// Lists the sibling `.md` files and subdirectories that contain a
/// `README.md` adjacent to an index file at `dir`
/// [Repo-grounded — `readme_index.rs::list_sibling_targets`].
let private listSiblingTargets (dir: string) : SiblingTargets =
    if not (Directory.Exists dir) then
        SiblingTargets.Empty
    else
        Directory.GetFileSystemEntries dir
        |> Array.sort
        |> Array.fold
            (fun (acc: SiblingTargets) full ->
                let name = Path.GetFileName full

                if Directory.Exists full then
                    if name.StartsWith(".", StringComparison.Ordinal) || skipDirs.Contains name then
                        acc
                    else
                        let subReadme = Path.Combine(full, "README.md")

                        if File.Exists subReadme then
                            { acc with
                                SubDirs = Set.add (name + "/README.md") acc.SubDirs }
                        else
                            acc
                elif
                    name.StartsWith(".", StringComparison.Ordinal)
                    || name = "README.md"
                    || not (name.EndsWith(".md", StringComparison.Ordinal))
                then
                    acc
                else
                    { acc with
                        Files = Set.add name acc.Files })
            SiblingTargets.Empty

/// Recursively lists every directory reachable from `root` (including `root`
/// itself), skipping [`skipDirs`]. Dot-directories are deliberately NOT
/// skipped by this walker — only by [`listSiblingTargets`]'s per-child
/// exclusion — since a dot-directory (`.claude/`, `.codex/`) is first-class
/// governed content, not build junk [Repo-grounded —
/// `readme_index.rs::list_all_dirs`/`walk_dirs_recursive`].
let rec private walkDirsRecursive (dir: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        Directory.GetDirectories dir
        |> Array.sort
        |> Array.filter (fun d -> not (skipDirs.Contains(Path.GetFileName d)))
        |> Array.toList
        |> List.collect (fun d -> d :: walkDirsRecursive d)

let private listAllDirs (root: string) : string list =
    if not (Directory.Exists root) then
        []
    else
        root :: walkDirsRecursive root

/// Returns `Some dirName` when `name` is a subdirectory target
/// (`"<dirName>/README.md"`), else `None`.
let private trySubdirName (name: string) : string option =
    if name.EndsWith("/README.md", StringComparison.Ordinal) then
        Some(name.Substring(0, name.Length - "/README.md".Length))
    else
        None

/// Audits a single index file (`README.md`, or a split directory's sibling
/// `<name>.md`) against the sibling targets present under `targetDir`:
/// every sibling target must be linked (`Orphan` otherwise), and every
/// linked sibling target must exist on disk (`Ghost` otherwise). PR8b adds
/// the `Unannotated` finding kind to this same function
/// [Repo-grounded — `readme_index.rs::audit_index_file`].
let private auditIndexFile (indexPath: string) (targetDir: string) : ReadmeIndexFinding list =
    let content = File.ReadAllText indexPath
    let indexDir = Path.GetDirectoryName(indexPath: string)

    // A split-directory index file lives in `targetDir`'s parent, not in
    // `targetDir` itself, so its link targets carry an explicit
    // "<targetDir-name>/" prefix that must be stripped before comparing
    // against `targetDir`'s own sibling names.
    let linkPrefix =
        if String.Equals(indexDir, targetDir, StringComparison.Ordinal) then
            None
        else
            Some(Path.GetFileName targetDir + "/")

    let normalize (raw: string) : string =
        match linkPrefix with
        | Some p when raw.StartsWith(p, StringComparison.Ordinal) -> raw.Substring(p.Length)
        | _ -> raw

    let linked = extractReadmeLinks content |> Set.map normalize
    let targets = listSiblingTargets targetDir

    let orphanFindings =
        targets.SortedNames
        |> List.choose (fun name ->
            if linked.Contains name then
                None
            else
                match trySubdirName name with
                | Some dirName when linked.Contains(dirName + ".md") -> None
                | _ ->
                    let full = Path.Combine(targetDir, name)

                    Some
                        { File = full
                          Severity = "high"
                          Kind = ReadmeIndexFindingKind.Orphan
                          Message = sprintf "orphan: %s exists but is not linked from %s" name indexPath })

    let ghostFindings =
        linked
        |> Set.toList
        |> List.sort
        |> List.choose (fun link ->
            if not (targets.Present link) then
                let full = Path.Combine(targetDir, link)

                if File.Exists full || Directory.Exists full then
                    None
                else
                    Some
                        { File = full
                          Severity = "high"
                          Kind = ReadmeIndexFindingKind.Ghost
                          Message = sprintf "ghost: %s references %s but the target does not exist" indexPath link }
            else
                None)

    orphanFindings @ ghostFindings

/// Audits a single directory: mandatory-README detection, additive
/// sibling-index auditing (both a directory's own `README.md` and, for a
/// split directory, its parent's `<name>.md` sibling index), and
/// orphan/ghost detection [Repo-grounded — `readme_index.rs::audit_one_dir`].
let private auditOneDir (dir: string) (root: string) : ReadmeIndexFinding list =
    let splitIndexFindings =
        if String.Equals(dir, root, StringComparison.Ordinal) then
            []
        else
            let parent = Path.GetDirectoryName(dir: string)
            let name = Path.GetFileName dir

            if String.IsNullOrEmpty parent || String.IsNullOrEmpty name then
                []
            else
                let splitIndex = Path.Combine(parent, name + ".md")

                if File.Exists splitIndex then
                    auditIndexFile splitIndex dir
                else
                    []

    let readmePath = Path.Combine(dir, "README.md")

    if File.Exists readmePath then
        splitIndexFindings @ auditIndexFile readmePath dir
    elif String.Equals(dir, root, StringComparison.Ordinal) then
        // The scan root itself is never required to carry a README — a
        // caller passes a covered-tree root deliberately. A descendant
        // directory is never exempt.
        splitIndexFindings
    else
        let targets = listSiblingTargets dir

        if not (Set.isEmpty targets.Files) || not (Set.isEmpty targets.SubDirs) then
            splitIndexFindings
            @ [ { File = dir
                  Severity = "high"
                  Kind = ReadmeIndexFindingKind.Missing
                  Message = sprintf "missing: %s contains indexable content but has no README.md" dir } ]
        else
            splitIndexFindings

/// Audits every directory reachable from `root`
/// [Repo-grounded — `readme_index.rs::audit_root`].
let private auditRoot (root: string) : ReadmeIndexFinding list =
    listAllDirs root |> List.collect (fun d -> auditOneDir d root)

/// Audits every covered directory found under each root in `paths`, relative
/// to `repoRoot` when a path is not already absolute
/// [Repo-grounded — `readme_index.rs::audit_readme_index`].
let auditReadmeIndex (repoRoot: string) (paths: string list) : ReadmeIndexFinding list =
    paths
    |> List.collect (fun p ->
        let full = if Path.IsPathRooted p then p else Path.Combine(repoRoot, p)
        auditRoot full)
    |> List.sortBy (fun f -> f.File, f.Kind.Name)
