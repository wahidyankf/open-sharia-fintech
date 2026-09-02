/// Port of `rhino-cli doctor`'s cargo shared-target-directory symlinking and
/// prune-cache GC step for
/// `specs/apps/rhino/cli/behaviors/system/cargo-target-share.feature`'s
/// 18 scenarios [Repo-grounded —
/// `apps/rhino-cli/src/application/doctor/target_share.rs`,
/// `apps/rhino-cli/src/commands/doctor.rs`]. Redirects each Rust crate's
/// `target/` directory to a symlink into a shared, persistent cache keyed by
/// repo name and crate leaf name (`<cache_root>/<repo_name>/<crate_leaf>`),
/// so every git worktree of the same repo shares one physical build
/// directory per crate.
///
/// Scope: the first PR to touch this file ported only the pure, testable
/// `target_share.rs` slice above (discovery, cache-root/shared-path
/// resolution, worktree enumeration, check/fix/prune/sweep, and their text
/// formatters). This file now also carries the tool-check engine —
/// `checker.rs`/`fixer.rs`/`reporter.rs`/`tools.rs` — for
/// `specs/apps/rhino/cli/behaviors/system/doctor.feature`'s 17
/// scenarios, below the "Tool-check engine" banner comment. CLI argument
/// parsing and dispatch wiring (`commands/doctor.rs::run`) remain out of
/// scope for both features — every scenario here, like the target-share ones
/// above, calls straight into this module's pure functions rather than a
/// wired-up `doctor` verb.
///
/// Below the "F# lint-target Fantomas tool-invocation check" banner comment,
/// this file also carries an F#-native meta-check with no Rust equivalent
/// (`apps/rhino-cli/src` never invoked Fantomas) for
/// `specs/apps/rhino/cli/behaviors/system/fsharp-tool-invocation.feature`'s
/// 1 scenario: every locally discovered Nx `project.json` `lint` target that
/// invokes Fantomas must restore the local `.NET` tool manifest first and
/// must never invoke a bare global `fantomas` binary.
///
/// # Deviation from the Rust source's ambient-environment reads
///
/// Mirroring `target_share.rs`'s own module-level "Deviation" note: every
/// function below takes explicit parameters (`ci`, `home`, `overrideDir`,
/// `cargoSweepPresent`) instead of reading `CI`/`GITHUB_ACTIONS`/
/// `OSE_CARGO_TARGET_CACHE`/`HOME`/`PATH` directly, so each stays a pure,
/// deterministic unit under test. Each parameterized function has a matching
/// `*Ambient` sibling that reads the real environment once.
module RhinoCli.Application.Doctor

open System
open System.Diagnostics
open System.IO
open System.Runtime.InteropServices
open System.Text.Encodings.Web
open System.Text.Json
open System.Text.Json.Nodes
open RhinoCli.Domain.Types

// ---------------------------------------------------------------------------
// CI detection
// ---------------------------------------------------------------------------

/// Returns `true` when the process should be treated as running under CI —
/// either the `CI` or `GITHUB_ACTIONS` signal being set is sufficient
/// [Repo-grounded — `target_share.rs::is_ci`].
///
/// Gherkin (underpins) — "the doctor symlink step no-ops under CI":
///   Given the environment variable CI is set
///   When the developer runs the doctor command with the fix flag
///   Then no target symlink is created for any crate
///   And the command exits successfully with a message that CI was detected
let isCi (ciEnvSet: bool) (ghaEnvSet: bool) : bool = ciEnvSet || ghaEnvSet

/// Reads the real `CI`/`GITHUB_ACTIONS` environment variables and returns
/// [`isCi`]'s verdict for the current process.
let isCiAmbient () : bool =
    isCi
        (not (String.IsNullOrEmpty(Environment.GetEnvironmentVariable("CI"))))
        (not (String.IsNullOrEmpty(Environment.GetEnvironmentVariable("GITHUB_ACTIONS"))))

// ---------------------------------------------------------------------------
// Crate discovery
// ---------------------------------------------------------------------------

/// Discovers every Rust crate directory under `repoRoot/apps/*` and
/// `repoRoot/libs/*` that contains a `Cargo.toml`
/// [Repo-grounded — `target_share.rs::discover_crates`].
///
/// Walks the two top-level directories — no hardcoded crate list — so a
/// newly-added crate is picked up automatically. A top-level directory that
/// does not exist contributes zero entries rather than an error. The
/// returned list is sorted and deduplicated for deterministic iteration
/// order.
///
/// Gherkin (binds) — "dynamic discovery covers every crate under apps and
/// libs":
///   Given a repo checkout contains multiple Rust crates under apps and libs outside CI
///   When the developer runs the doctor command with the fix flag
///   Then every discovered crate's target is a symlink into the shared cache
///   And no crate is skipped due to a hardcoded crate list
let discoverCrates (repoRoot: string) : string list =
    [ "apps"; "libs" ]
    |> List.collect (fun top ->
        let topDir = Path.Combine(repoRoot, top)

        if Directory.Exists(topDir) then
            Directory.GetDirectories(topDir)
            |> Array.filter (fun d -> File.Exists(Path.Combine(d, "Cargo.toml")))
            |> Array.toList
        else
            [])
    |> List.distinct
    |> List.sort

// ---------------------------------------------------------------------------
// Cache-root / shared-path resolution
// ---------------------------------------------------------------------------

/// Resolves the shared-cache root directory
/// [Repo-grounded — `target_share.rs::cache_root_from`].
///
/// `overrideDir` mirrors the `OSE_CARGO_TARGET_CACHE` environment variable
/// (an explicit override wins outright); `home` mirrors `HOME`, used to
/// build the default `<home>/.cache/ose-cargo-target` when no override is
/// given. Returns a relative path (`.cache/ose-cargo-target`) when neither is
/// available — a degenerate case the real [`cacheRootAmbient`] caller never
/// hits in practice.
let cacheRootFrom (overrideDir: string option) (home: string option) : string =
    match overrideDir with
    | Some dir -> dir
    | None ->
        match home with
        | Some h -> Path.Combine(h, ".cache", "ose-cargo-target")
        | None -> Path.Combine(".cache", "ose-cargo-target")

/// Reads the real `OSE_CARGO_TARGET_CACHE`/`HOME` environment variables and
/// returns [`cacheRootFrom`]'s verdict for the current process.
let cacheRootAmbient () : string =
    let envOpt (name: string) : string option =
        match Environment.GetEnvironmentVariable(name) with
        | null
        | "" -> None
        | value -> Some value

    cacheRootFrom (envOpt "OSE_CARGO_TARGET_CACHE") (envOpt "HOME")

/// Returns the basename of the directory containing the git common dir
/// [Repo-grounded — `target_share.rs::repo_name`].
///
/// `commonDir` is the value of
/// `git rev-parse --path-format=absolute --git-common-dir` (typically
/// `<repo-root>/.git`). Using the common dir — rather than the worktree
/// path — is what makes every linked worktree of the same repo resolve to
/// the same cache namespace. Returns an empty string when `commonDir` has no
/// parent (degenerate input; not expected from a real git invocation).
///
/// Gherkin (underpins) — "two worktrees of the same repo share one physical
/// target":
///   Given two worktrees of the same repo each have a crate's target symlinked by the doctor
///   When both symlinks are resolved
///   Then both point at the same shared-cache directory for that repo and crate
///   And a disk usage measurement across the worktrees counts that directory only once
let repoName (commonDir: string) : string =
    let parent = Path.GetDirectoryName(commonDir: string)

    if String.IsNullOrEmpty(parent) then
        ""
    else
        // Coverage note: `Path.GetFileName` only ever returns `null` when
        // its argument itself is `null`; `parent` is guaranteed non-null
        // (and non-empty) by the `String.IsNullOrEmpty` check two lines
        // above, in the same synchronous call, so this branch is
        // unreachable via .NET's own `Path.GetFileName` contract.
        match Path.GetFileName(parent) with
        | null -> ""
        | name -> name

/// Returns the shared-cache path a crate's `target/` should be symlinked to:
/// `<cacheRoot>/<repoName>/<crateLeaf>`, where `crateLeaf` is `crateDir`'s
/// final path component (e.g. `rhino-cli`)
/// [Repo-grounded — `target_share.rs::shared_target_path`].
let sharedTargetPath (cacheRoot: string) (repoNameValue: string) (crateDir: string) : string =
    let leaf =
        // Coverage note: `String.TrimEnd` never returns `null` (it throws
        // `NullReferenceException` before returning at all when `crateDir`
        // itself is `null`, never producing a `null` result), so
        // `Path.GetFileName` here — which only returns `null` for a `null`
        // argument — can never take the `null` arm below.
        match Path.GetFileName(crateDir.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)) with
        | null -> ""
        | name -> name

    Path.Combine(cacheRoot, repoNameValue, leaf)

// ---------------------------------------------------------------------------
// Symlink primitives
// ---------------------------------------------------------------------------

/// Returns the raw, unresolved symlink target stored at `path`, or `None`
/// when `path` is not a symlink (including when nothing exists there at
/// all) — mirrors `std::fs::read_link`'s "does not follow, works on broken
/// links" contract via .NET's `FileSystemInfo.LinkTarget`.
let private linkTargetOf (path: string) : string option =
    match DirectoryInfo(path).LinkTarget with
    | null -> None
    | target -> Some target

/// Returns `true` when `link` is a symlink whose raw target equals
/// `expectedTarget` [Repo-grounded — `target_share.rs::is_correct_symlink`].
let private isCorrectSymlink (link: string) (expectedTarget: string) : bool =
    match linkTargetOf link with
    | Some actual -> actual = expectedTarget
    | None -> false

/// Discards whatever currently exists at `path` — a symlink (whatever it
/// resolves to), a plain directory, or a plain file — leaving nothing behind.
/// Returns `true` when the discarded entry was a plain, rebuildable
/// directory (never a symlink), matching `FixOutcome.ReplacedPlainDir`'s
/// semantics [Repo-grounded — `target_share.rs::fix_target_shares`'s
/// `symlink_metadata` match].
///
/// `Directory.Delete` never follows a symlink into its target's contents —
/// documented .NET behavior since .NET Core 3.0 — so deleting a directory
/// -type symlink here removes only the link itself, exactly like Rust's
/// `remove_file` branch for the symlink case.
let private removeExistingEntry (path: string) : bool =
    match linkTargetOf path with
    | Some _ ->
        Directory.Delete(path, false)
        false
    | None ->
        if Directory.Exists(path) then
            Directory.Delete(path, true)
            true
        elif File.Exists(path) then
            File.Delete(path)
            false
        else
            false

// ---------------------------------------------------------------------------
// Git worktree enumeration
// ---------------------------------------------------------------------------

/// Runs `git worktree list --porcelain` from `repoRoot` and returns every
/// listed worktree path, sorted and deduplicated, or `None` when the
/// enumeration itself fails (spawn error or non-zero exit)
/// [Repo-grounded — `target_share.rs::worktree_roots`].
let private worktreeRoots (repoRoot: string) : string list option =
    use proc = new Process()
    proc.StartInfo.FileName <- "git"
    proc.StartInfo.ArgumentList.Add("worktree")
    proc.StartInfo.ArgumentList.Add("list")
    proc.StartInfo.ArgumentList.Add("--porcelain")
    proc.StartInfo.WorkingDirectory <- repoRoot
    proc.StartInfo.EnvironmentVariables.Remove("GIT_DIR")
    proc.StartInfo.EnvironmentVariables.Remove("GIT_WORK_TREE")
    proc.StartInfo.RedirectStandardOutput <- true
    proc.StartInfo.RedirectStandardError <- true
    proc.StartInfo.UseShellExecute <- false

    try
        proc.Start() |> ignore
        let stdout = proc.StandardOutput.ReadToEnd()
        proc.StandardError.ReadToEnd() |> ignore
        proc.WaitForExit()

        if proc.ExitCode <> 0 then
            None
        else
            stdout.Split('\n')
            |> Array.choose (fun line ->
                if line.StartsWith("worktree ", StringComparison.Ordinal) then
                    Some(line.Substring("worktree ".Length))
                else
                    None)
            |> Array.distinct
            |> Array.sort
            |> Array.toList
            |> Some
    with :? System.ComponentModel.Win32Exception ->
        None

/// [`worktreeRoots`] with the fix/check step's degraded fallback applied:
/// falls back to just `repoRoot` when the enumeration fails
/// [Repo-grounded — `target_share.rs::roots_or_self`].
let private rootsOrSelf (repoRoot: string) : string list =
    worktreeRoots repoRoot |> Option.defaultValue [ repoRoot ]

/// Lexically normalizes `path` for stable equality comparison, falling back
/// to the raw string when normalization fails — mirrors
/// `std::path::Path::canonicalize`'s "resolve, fall back to the original on
/// failure" contract from `target_share.rs::live_referenced_entries`/
/// `prune_orphans`, without requiring the path to exist.
let private canonicalize (path: string) : string =
    try
        Path.GetFullPath(path)
    with _ ->
        path

/// Returns the shared-cache path currently referenced by every crate's
/// `target/` symlink across every live worktree (plus the main checkout) of
/// the repo rooted at `repoRoot`
/// [Repo-grounded — `target_share.rs::live_referenced_entries`].
///
/// Returns `None` when the query itself fails. `None` is distinct from
/// `Some (empty set)`: a successful enumeration that finds no referencing
/// symlinks is a genuine empty live set (prune may delete orphans), whereas
/// a *failed* enumeration means we cannot know what is referenced, so the
/// caller must fail closed and delete nothing.
let private liveReferencedEntries (repoRoot: string) : Set<string> option =
    worktreeRoots repoRoot
    |> Option.map (fun worktrees ->
        worktrees
        |> List.collect discoverCrates
        |> List.choose (fun crateDir -> linkTargetOf (Path.Combine(crateDir, "target")))
        |> List.map canonicalize
        |> Set.ofList)

// ---------------------------------------------------------------------------
// check
// ---------------------------------------------------------------------------

/// One crate whose `target/` is not yet the correct shared-cache symlink
/// [Repo-grounded — `target_share.rs::TargetShareStatus`].
type TargetShareStatus =
    { CrateDir: string; SharedPath: string }

/// Reports every crate in every checkout of this repo — the main checkout
/// and each linked worktree — whose `target/` is not yet the correct symlink
/// into the shared cache. Read-only — never mutates the filesystem. Returns
/// an empty list under CI [Repo-grounded —
/// `target_share.rs::check_target_shares`].
///
/// Gherkin (binds) — "doctor check reports a crate whose target is not yet
/// shared":
///   Given a crate's target is a plain directory not yet symlinked into the shared cache
///   When the developer runs the doctor command without the fix flag
///   Then the output reports that crate's target as needing to be shared
///   And the plain target directory is left unchanged
let checkTargetShares
    (repoRoot: string)
    (cacheRoot: string)
    (repoNameValue: string)
    (ci: bool)
    : TargetShareStatus list =
    if ci then
        []
    else
        rootsOrSelf repoRoot
        |> List.collect discoverCrates
        |> List.choose (fun crateDir ->
            let target = Path.Combine(crateDir, "target")
            let sharedPath = sharedTargetPath cacheRoot repoNameValue crateDir

            if isCorrectSymlink target sharedPath then
                None
            else
                Some
                    { CrateDir = crateDir
                      SharedPath = sharedPath })

// ---------------------------------------------------------------------------
// fix
// ---------------------------------------------------------------------------

/// Outcome of a [`fixTargetShares`] run
/// [Repo-grounded — `target_share.rs::FixOutcome`].
type FixOutcome =
    { Created: int
      AlreadyCorrect: int
      ReplacedPlainDir: int
      SkippedCi: bool }

/// Creates or repairs each discovered crate's `target/` symlink into the
/// shared cache, across the main checkout **and every linked worktree**. No
/// -ops entirely under CI [Repo-grounded —
/// `target_share.rs::fix_target_shares`].
///
/// Gherkin (binds) — "doctor --fix symlinks a crate's target into the shared
/// cache":
///   Given a Rust crate with a plain target directory exists in a repo checkout outside CI
///   When the developer runs the doctor command with the fix flag
///   Then the crate's target becomes a symlink into the shared cargo-target cache
///   And the symlink resolves under the repo's own shared-cache namespace
let fixTargetShares (repoRoot: string) (cacheRoot: string) (repoNameValue: string) (ci: bool) : FixOutcome =
    if ci then
        { Created = 0
          AlreadyCorrect = 0
          ReplacedPlainDir = 0
          SkippedCi = true }
    else
        rootsOrSelf repoRoot
        |> List.collect discoverCrates
        |> List.fold
            (fun acc crateDir ->
                let target = Path.Combine(crateDir, "target")
                let sharedPath = sharedTargetPath cacheRoot repoNameValue crateDir
                Directory.CreateDirectory(sharedPath) |> ignore

                if isCorrectSymlink target sharedPath then
                    { acc with
                        AlreadyCorrect = acc.AlreadyCorrect + 1 }
                else
                    let replacedPlainDir = removeExistingEntry target

                    try
                        Directory.CreateSymbolicLink(target, sharedPath) |> ignore

                        { acc with
                            Created = acc.Created + 1
                            ReplacedPlainDir = acc.ReplacedPlainDir + (if replacedPlainDir then 1 else 0) }
                    with _ ->
                        acc)
            { Created = 0
              AlreadyCorrect = 0
              ReplacedPlainDir = 0
              SkippedCi = false }

// ---------------------------------------------------------------------------
// prune
// ---------------------------------------------------------------------------

/// Outcome of a [`pruneOrphans`] run
/// [Repo-grounded — `target_share.rs::PruneOutcome`].
type PruneOutcome =
    { Deleted: string list
      Preserved: string list
      Candidates: string list
      SkippedCi: bool
      EnumerationFailed: bool }

/// The zero-valued [`PruneOutcome`] shared by every early-return branch.
let private prunedNothing =
    { Deleted = []
      Preserved = []
      Candidates = []
      SkippedCi = false
      EnumerationFailed = false }

/// Deletes shared-cache entries under `<cacheRoot>/<repoNameValue>/*` that no
/// live worktree or checkout of the repo references. Never touches an entry
/// present in [`liveReferencedEntries`]'s result
/// [Repo-grounded — `target_share.rs::prune_orphans`].
///
/// Gherkin (binds) — "prune removes an orphaned shared-cache entry":
///   Given the shared cache holds an entry for a crate that no longer exists in the repo outside CI
///   When the developer runs the doctor command with the prune flag
///   Then the orphaned cache entry is deleted
///   And every entry still referenced by a live worktree or checkout is preserved
let pruneOrphans
    (repoRoot: string)
    (cacheRoot: string)
    (repoNameValue: string)
    (dryRun: bool)
    (ci: bool)
    : PruneOutcome =
    if ci then
        { prunedNothing with SkippedCi = true }
    else
        match liveReferencedEntries repoRoot with
        | None ->
            { prunedNothing with
                EnumerationFailed = true }
        | Some live ->
            let repoCacheDir = Path.Combine(cacheRoot, repoNameValue)

            if not (Directory.Exists(repoCacheDir)) then
                prunedNothing
            else
                Directory.GetDirectories(repoCacheDir)
                |> Array.toList
                |> List.fold
                    (fun acc entryPath ->
                        if Set.contains (canonicalize entryPath) live then
                            { acc with
                                Preserved = acc.Preserved @ [ entryPath ] }
                        elif dryRun then
                            { acc with
                                Candidates = acc.Candidates @ [ entryPath ] }
                        else
                            Directory.Delete(entryPath, true)

                            { acc with
                                Deleted = acc.Deleted @ [ entryPath ] })
                    prunedNothing

// ---------------------------------------------------------------------------
// sweep
// ---------------------------------------------------------------------------

/// Outcome of a [`sweepStale`] run
/// [Repo-grounded — `target_share.rs::SweepOutcome`].
type SweepOutcome =
    { Skipped: bool
      SkippedCi: bool
      Ran: bool }

/// Returns `true` when the `cargo-sweep` binary is present on `PATH`
/// [Repo-grounded — `target_share.rs::cargo_sweep_present`].
let cargoSweepPresent () : bool =
    match Environment.GetEnvironmentVariable("PATH") with
    | null -> false
    | pathVar ->
        pathVar.Split(Path.PathSeparator)
        |> Array.exists (fun dir -> dir <> "" && File.Exists(Path.Combine(dir, "cargo-sweep")))

/// The repo-scoped subtree `cargo-sweep` reclaims within —
/// `<cacheRoot>/<repoNameValue>`, never the whole shared `cacheRoot`
/// [Repo-grounded — `target_share.rs::sweep_scope`].
let private sweepScope (cacheRoot: string) (repoNameValue: string) : string = Path.Combine(cacheRoot, repoNameValue)

/// Runs `cargo-sweep`'s stale-artifact reclamation over this repo's cache
/// namespace when the binary is present, degrading gracefully to `Skipped`
/// (never an error) when it is absent
/// [Repo-grounded — `target_share.rs::sweep_stale`].
///
/// Gherkin (binds) — "stale-artifact sweep degrades gracefully when
/// cargo-sweep is absent":
///   Given cargo-sweep is not installed on the developer's PATH
///   When the developer runs the doctor command with the prune flag
///   Then the sweep step is reported as skipped rather than failing the command
///   And the command exits successfully
let sweepStale
    (cacheRoot: string)
    (repoNameValue: string)
    (dryRun: bool)
    (cargoSweepPresentValue: bool)
    (ci: bool)
    : SweepOutcome =
    if ci then
        { Skipped = false
          SkippedCi = true
          Ran = false }
    elif not cargoSweepPresentValue then
        { Skipped = true
          SkippedCi = false
          Ran = false }
    elif dryRun then
        { Skipped = false
          SkippedCi = false
          Ran = false }
    else
        use proc = new Process()
        proc.StartInfo.FileName <- "cargo-sweep"
        proc.StartInfo.ArgumentList.Add("--time")
        proc.StartInfo.ArgumentList.Add("30")
        proc.StartInfo.ArgumentList.Add("--recursive")
        proc.StartInfo.ArgumentList.Add(sweepScope cacheRoot repoNameValue)
        proc.StartInfo.RedirectStandardOutput <- true
        proc.StartInfo.RedirectStandardError <- true
        proc.StartInfo.UseShellExecute <- false

        (try
            proc.Start() |> ignore
            proc.WaitForExit()
         with _ ->
             ())

        { Skipped = false
          SkippedCi = false
          Ran = true }

// ---------------------------------------------------------------------------
// Text formatters [Repo-grounded — `commands/doctor.rs::run_target_share_step`]
// ---------------------------------------------------------------------------

/// Formats a [`checkTargetShares`] report as the plain text
/// `doctor` prints ahead of any `--fix`/`--prune-cargo-cache` output.
///
/// Gherkin (binds) — "the doctor symlink step no-ops under CI":
///   Given the environment variable CI is set
///   When the developer runs the doctor command with the fix flag
///   Then no target symlink is created for any crate
///   And the command exits successfully with a message that CI was detected
let formatCheckReport (statuses: TargetShareStatus list) (ci: bool) : string =
    if ci then
        "\nTarget-share: CI detected — skipped."
    elif List.isEmpty statuses then
        "\nTarget-share: all crates already share their target/ via the cache."
    else
        statuses
        |> List.map (fun s -> sprintf "  %s" s.CrateDir)
        |> String.concat "\n"
        |> sprintf "\nTarget-share: %d crate(s) need sharing:\n%s" (List.length statuses)

/// Formats a [`fixTargetShares`] outcome as the plain text `doctor --fix`
/// prints for the target-share step.
let formatFixReport (outcome: FixOutcome) : string =
    if outcome.SkippedCi then
        "Target-share fix: CI detected — skipped."
    else
        sprintf
            "Target-share fix: %d created, %d already correct, %d plain dir(s) replaced"
            outcome.Created
            outcome.AlreadyCorrect
            outcome.ReplacedPlainDir

/// Formats a [`pruneOrphans`] outcome as the plain text
/// `doctor --prune-cargo-cache` prints.
///
/// Gherkin (binds) — "prune dry-run previews deletions without removing
/// anything":
///   Given the shared cache holds at least one orphaned entry outside CI
///   When the developer runs the doctor command with the prune and dry-run flags
///   Then the orphaned entry is reported as a candidate for deletion
///   And no cache entry is actually removed
let formatPruneReport (outcome: PruneOutcome) (dryRun: bool) : string =
    if outcome.SkippedCi then
        "Prune: CI detected — skipped."
    elif outcome.EnumerationFailed then
        "Prune: could not enumerate worktrees — skipped (nothing deleted)."
    elif dryRun then
        outcome.Candidates
        |> List.map (fun c -> sprintf "  %s" c)
        |> String.concat "\n"
        |> sprintf "Prune (dry-run): %d candidate(s) for deletion\n%s" (List.length outcome.Candidates)
    else
        sprintf "Prune: %d orphaned entrie(s) deleted" (List.length outcome.Deleted)

/// Formats a [`sweepStale`] outcome as the plain text
/// `doctor --prune-cargo-cache` prints for the sweep sub-step. Returns an
/// empty string when the sweep neither skipped nor was CI-guarded (i.e. it
/// ran), matching `run_target_share_step`'s "only print on skip" behaviour.
let formatSweepReport (outcome: SweepOutcome) : string =
    if outcome.SkippedCi then
        "Sweep: CI detected — skipped."
    elif outcome.Skipped then
        "Sweep: cargo-sweep not installed — skipped."
    else
        ""

// ---------------------------------------------------------------------------
// Tool-check engine [Repo-grounded — `application/doctor/mod.rs`,
// `checker.rs`, `fixer.rs`, `reporter.rs`, `tools.rs`] for
// `specs/apps/rhino/cli/behaviors/system/doctor.feature`'s 17
// scenarios.
// ---------------------------------------------------------------------------

/// Health status of one tool check [Repo-grounded — `mod.rs::ToolStatus`].
/// Named `Passing` rather than the Rust source's `Ok` to avoid colliding with
/// `FSharp.Core`'s `Result.Ok` case — see
/// `RhinoCli.Domain.Types.Severity`'s doc comment for the same
/// GRA-UNIONCASE-001 rationale.
type ToolStatus =
    | Passing
    | Warning
    | Missing

/// Stable wire/status code for `status`: `"ok"`, `"warning"`, or `"missing"`.
let toolStatusCode (status: ToolStatus) : string =
    match status with
    | Passing -> "ok"
    | Warning -> "warning"
    | Missing -> "missing"

/// Controls which tools [`checkAll`] probes [Repo-grounded — `mod.rs::Scope`].
type DoctorScope =
    | FullScope
    | MinimalScope

/// Stable code for `scope`: `"full"` or `"minimal"`.
let doctorScopeCode (scope: DoctorScope) : string =
    match scope with
    | FullScope -> "full"
    | MinimalScope -> "minimal"

/// Parses a scope string: `""`/`"full"` maps to [`FullScope`],
/// `"minimal"` to [`MinimalScope`], anything else to `None`
/// [Repo-grounded — `mod.rs::Scope::parse`].
///
/// Gherkin (binds) — "Full scope is the default behavior":
///   Given all required development tools are present with matching versions
///   When the developer runs the doctor command
///   Then the command exits successfully
///   And the output reports each tool as passing
let parseDoctorScope (s: string) : DoctorScope option =
    match s with
    | ""
    | "full" -> Some FullScope
    | "minimal" -> Some MinimalScope
    | _ -> None

/// The minimal core tool set every environment needs
/// [Repo-grounded — `mod.rs::is_minimal_tool`].
///
/// Gherkin (binds) — "Minimal scope checks only core tools":
///   Given all required development tools are present with matching versions
///   When the developer runs the doctor command with minimal scope
///   Then the command exits successfully
///   And the output checks only the minimal tool set
let isMinimalTool (name: string) : bool =
    List.contains name [ "git"; "volta"; "node"; "npm"; "docker"; "jq" ]

/// Every Doctor tool name `--tools` may select
/// [Repo-grounded — `repo_config/mod.rs::DOCTOR_TOOL_INVENTORY`].
let doctorToolInventory: string list =
    [ "git"
      "volta"
      "node"
      "npm"
      "rust"
      "cargo-llvm-cov"
      "dotnet"
      "docker"
      "jq"
      "shellcheck"
      "hadolint"
      "actionlint"
      "playwright"
      "shfmt"
      "tofu"
      "clang-format" ]

/// Rejects a blank or unrecognized `--tools` selection before any tool is
/// probed [Repo-grounded — `commands/doctor.rs::parse_doctor_tool_name`].
///
/// Gherkin (binds) — "An unknown selected tool is rejected before
/// environment checks":
///   Given an unknown Doctor tool is selected
///   When the developer runs the doctor command
///   Then the command exits with a failure code
///   And the invalid selection is rejected before any tool is probed
let parseDoctorToolName (value: string) : Result<string, string> =
    let name = value.Trim()

    if name = "" then
        Error "Doctor tool name must not be blank"
    elif not (List.contains name doctorToolInventory) then
        Error(sprintf "unknown Doctor tool \"%s\"" name)
    else
        Ok name

/// Result of checking one tool [Repo-grounded — `mod.rs::ToolCheck`].
type ToolCheck =
    { Name: string
      Binary: string
      Status: ToolStatus
      InstalledVersion: string
      RequiredVersion: string
      Source: string
      Note: string }

/// Aggregated results from a full doctor run
/// [Repo-grounded — `mod.rs::DoctorResult`].
type DoctorResult =
    { Checks: ToolCheck list
      OkCount: int
      WarnCount: int
      MissingCount: int
      Scope: DoctorScope }

/// Output of a command invocation: `Ok (stdout, stderr, exitCode)`, or
/// `Error` when the binary was not found in `PATH`
/// [Repo-grounded — `mod.rs::CommandOutput`].
type CommandOutput = Result<string * string * int, string>

/// Injectable command runner used for testing
/// [Repo-grounded — `mod.rs::CommandRunner`].
type CommandRunner = string -> string list -> CommandOutput

/// One step in an auto-install sequence
/// [Repo-grounded — `tools.rs::InstallStep`].
type InstallStep =
    { Description: string
      Command: string
      Args: string list }

/// Complete specification for checking (and optionally fixing) one tool
/// [Repo-grounded — `tools.rs::ToolDef`].
type ToolDef =
    { Name: string
      Binary: string
      Source: string
      Args: string list
      UseStderr: bool
      ParseVer: string -> string
      Compare: string -> string -> ToolStatus * string
      ReadReq: unit -> string
      InstallCmd: (string -> string -> InstallStep list) option }

/// Configuration for [`checkAll`]/[`fixAll`]
/// [Repo-grounded — `mod.rs::CheckOptions`].
type CheckOptions =
    { RepoRoot: string
      Runner: CommandRunner option
      Scope: DoctorScope
      SelectedTools: string list option }

// --- Comparators [Repo-grounded — `checker.rs`'s "Comparators" section] ---

/// Strips a leading `v` from a version string.
let normalizeSimpleVersion (s: string) : string =
    if s.StartsWith("v", StringComparison.Ordinal) then
        s.Substring(1)
    else
        s

/// Compares two version strings for exact equality (after stripping a
/// leading `v`). `Passing` immediately when `required` is empty
/// [Repo-grounded — `checker.rs::compare_exact`].
///
/// Gherkin (binds) — "A tool is installed but its version does not match the
/// requirement":
///   Given a required development tool is installed with a non-matching version
///   When the developer runs the doctor command
///   Then the command exits successfully
///   And the output reports the tool as a warning rather than a failure
let compareExact (installed: string) (required: string) : ToolStatus * string =
    if required = "" then
        Passing, "no version requirement"
    else
        let inst = normalizeSimpleVersion installed
        let req = normalizeSimpleVersion required

        if inst = req then
            Passing, sprintf "required: %s" required
        else
            Warning, sprintf "required: %s, version mismatch" required

/// Parses a semver-style string into `(major, minor, patch)`, returning
/// `None` when any component fails to parse as an integer
/// [Repo-grounded — `checker.rs::parse_version_parts`].
let parseVersionParts (s: string) : (int64 * int64 * int64) option =
    let parts = (normalizeSimpleVersion s).Split('.') |> Array.truncate 3
    let nums = Array.create 3 0L
    let mutable ok = true

    parts
    |> Array.iteri (fun i p ->
        match Int64.TryParse(p) with
        | true, n -> nums.[i] <- n
        | false, _ -> ok <- false)

    if ok then Some(nums.[0], nums.[1], nums.[2]) else None

/// Checks the installed version is `>=` the required version by full semver
/// comparison. Falls back to [`compareExact`] when either version fails to
/// parse. `Passing` immediately when `required` is empty
/// [Repo-grounded — `checker.rs::compare_gte`].
let compareGte (installed: string) (required: string) : ToolStatus * string =
    if required = "" then
        Passing, "no version requirement"
    else
        match parseVersionParts installed, parseVersionParts required with
        | Some(iMaj, iMin, iPat), Some(rMaj, rMin, rPat) ->
            if
                iMaj > rMaj
                || (iMaj = rMaj && iMin > rMin)
                || (iMaj = rMaj && iMin = rMin && iPat >= rPat)
            then
                Passing, sprintf "required: ≥%s" required
            else
                Warning, sprintf "required: ≥%s, version too old" required
        | _ -> compareExact installed required

/// Checks the installed major version is `>=` the required major version.
/// Falls back to [`compareExact`] when either major component fails to
/// parse. `Passing` immediately when `required` is empty
/// [Repo-grounded — `checker.rs::compare_major_gte`].
let compareMajorGte (installed: string) (required: string) : ToolStatus * string =
    if required = "" then
        Passing, "no version requirement"
    else
        let inst = normalizeSimpleVersion installed
        let req = normalizeSimpleVersion required
        let iMajorStr = inst.Split('.').[0]
        let rMajorStr = req.Split('.').[0]

        match Int64.TryParse(iMajorStr), Int64.TryParse(rMajorStr) with
        | (true, iMaj), (true, rMaj) ->
            if iMaj >= rMaj then
                Passing, sprintf "required: ≥%s (major)" required
            else
                Warning, sprintf "required: ≥%s (major), version too old" required
        | _ -> compareExact installed required

// --- Output parsers [Repo-grounded — `checker.rs`'s "Parsers for tool
// output" section] ---

/// Trims then strips a leading `v`.
let parseTrimVersion (s: string) : string = normalizeSimpleVersion (s.Trim())

/// Returns the `wordIdx`-th space-separated token from the first line
/// starting with `linePrefix` (after trimming), stripping `tokenPrefix` from
/// the matched token when non-empty [Repo-grounded —
/// `checker.rs::parse_line_word`].
let parseLineWord (output: string) (linePrefix: string) (wordIdx: int) (tokenPrefix: string) : string =
    output.Split('\n')
    |> Array.tryPick (fun line ->
        let trimmed = line.Trim()

        if trimmed.StartsWith(linePrefix, StringComparison.Ordinal) then
            let parts = trimmed.Split([| ' '; '\t' |], StringSplitOptions.RemoveEmptyEntries)

            if wordIdx < parts.Length then
                let word = parts.[wordIdx]

                if tokenPrefix <> "" && word.StartsWith(tokenPrefix, StringComparison.Ordinal) then
                    Some(word.Substring(tokenPrefix.Length))
                else
                    Some word
            else
                None
        else
            None)
    |> Option.defaultValue ""

let parseGitVersion (s: string) : string = parseLineWord s "git version " 2 ""

/// Extracts the `OpenTofu` version from `tofu --version` output
/// [Repo-grounded — `tools.rs::parse_tofu_version`].
///
/// Gherkin (binds) — "Fix dry-run previews a verified, platform-safe
/// OpenTofu release archive":
///   Given the tofu tool is not found in the system PATH
///   When the developer runs the doctor command with fix and dry-run flags
///   Then the command exits with a failure code
///   And the output handles verified OpenTofu remediation safely
let parseTofuVersion (s: string) : string = parseLineWord s "OpenTofu " 1 "v"

let parseRustVersion (out: string) : string = parseLineWord out "rustc " 1 ""

let parseCargoLlvmCovVersion (out: string) : string =
    parseLineWord out "cargo-llvm-cov " 1 ""

let parseDotnetVersion (out: string) : string = out.Trim()

let parseDockerVersion (out: string) : string =
    out.Split('\n')
    |> Array.tryPick (fun line ->
        let t = line.Trim()

        if t.StartsWith("Docker version", StringComparison.Ordinal) then
            let fields = t.Split([| ' '; '\t' |], StringSplitOptions.RemoveEmptyEntries)

            if fields.Length >= 3 then
                Some(fields.[2].TrimEnd(','))
            else
                None
        else
            None)
    |> Option.defaultValue ""

let parseShellcheckVersion (out: string) : string =
    out.Split('\n')
    |> Array.tryPick (fun line ->
        let t = line.Trim()

        if t.StartsWith("version:", StringComparison.Ordinal) then
            Some(t.Substring("version:".Length).Trim())
        else
            None)
    |> Option.defaultValue ""

let parseHadolintVersion (out: string) : string =
    parseLineWord out "Haskell Dockerfile Linter" 3 ""

let parseActionlintVersion (out: string) : string =
    // Coverage note: `String.Split` never returns an empty array for any
    // input — even `""` splits to `[| "" |]` — so this `[||]` arm is
    // unreachable via .NET's own `String.Split` contract, regardless of
    // what `out` contains.
    match out.Split('\n') with
    | [||] -> ""
    | lines -> lines.[0].Trim()

let parseJqVersion (out: string) : string =
    let t = out.Trim()

    if t.StartsWith("jq-", StringComparison.Ordinal) then
        t.Substring(3)
    else
        t

let parsePlaywrightVersion (out: string) : string = parseLineWord out "Version " 1 ""

let parseClangFormatVersion (out: string) : string =
    out.Split('\n')
    |> Array.tryPick (fun line ->
        let words = line.Split([| ' '; '\t' |], StringSplitOptions.RemoveEmptyEntries)

        words
        |> Array.tryFindIndex (fun w -> w = "version")
        |> Option.bind (fun idx ->
            if idx + 1 < words.Length then
                Some words.[idx + 1]
            else
                None))
    |> Option.defaultValue ""

// --- Version readers [Repo-grounded — `checker.rs`'s "Version readers"
// section] ---

/// Reads a string property at `propertyPath` out of the JSON file at `path`,
/// returning `None` when the file is missing, malformed, or lacks that path.
let private readJsonStringProperty (path: string) (propertyPath: string list) : string option =
    try
        use doc = JsonDocument.Parse(File.ReadAllText path)

        let rec walk (element: JsonElement) (remaining: string list) : string option =
            match remaining with
            | [] ->
                if element.ValueKind = JsonValueKind.String then
                    Some(element.GetString())
                else
                    None
            | head :: tail ->
                match element.TryGetProperty head with
                | true, next -> walk next tail
                | false, _ -> None

        walk doc.RootElement propertyPath
    with _ ->
        None

/// Reads the `volta.node` version from a `package.json` file
/// [Repo-grounded — `checker.rs::read_node_version`].
let readNodeVersion (path: string) : string option =
    readJsonStringProperty path [ "volta"; "node" ]

/// Reads the `volta.npm` version from a `package.json` file
/// [Repo-grounded — `checker.rs::read_npm_version`].
let readNpmVersion (path: string) : string option =
    readJsonStringProperty path [ "volta"; "npm" ]

/// Reads the .NET SDK version from a `global.json` file
/// [Repo-grounded — `checker.rs::read_dotnet_version`].
let readDotnetVersion (path: string) : string option =
    readJsonStringProperty path [ "sdk"; "version" ]

/// Reads the pinned `channel` from a `rust-toolchain.toml` file
/// [Repo-grounded — `checker.rs::read_rust_toolchain_channel`].
///
/// Gherkin (binds) — "doctor compares rustc against the toolchain that
/// builds":
///   Given the installed rustc differs from the pinned rust-toolchain.toml channel
///   When "npm run doctor" runs
///   Then it reports the Rust toolchain as mismatched
///   And it names the pinned channel as the expected value
let readRustToolchainChannel (path: string) : string option =
    try
        File.ReadAllLines(path)
        |> Array.tryPick (fun line ->
            let t = line.Trim()

            if t.StartsWith("channel", StringComparison.Ordinal) then
                match t.IndexOf('=') with
                | -1 -> None
                | idx -> Some(t.Substring(idx + 1).Trim().Trim('"'))
            else
                None)
    with _ ->
        None

/// Components every pinned Rust toolchain must declare so lint gates can run
/// [Repo-grounded — `checker.rs::REQUIRED_RUST_TOOLCHAIN_COMPONENTS`].
let requiredRustToolchainComponents: string list = [ "rustfmt"; "clippy" ]

/// Enumerates repo-relative `rust-toolchain.toml` paths, workspace root
/// first, then sorted `apps/*` and `libs/*` project directories
/// [Repo-grounded — `checker.rs::rust_toolchain_manifests`].
let rustToolchainManifests (repoRoot: string) : string list =
    let fileName = "rust-toolchain.toml"

    let rootFile =
        if File.Exists(Path.Combine(repoRoot, fileName)) then
            [ fileName ]
        else
            []

    let underParent (parent: string) : string list =
        let dir = Path.Combine(repoRoot, parent)

        if Directory.Exists(dir) then
            Directory.GetDirectories(dir)
            |> Array.filter (fun d -> File.Exists(Path.Combine(d, fileName)))
            |> Array.map (fun d -> sprintf "%s/%s/%s" parent (Path.GetFileName(d: string)) fileName)
            |> Array.sort
            |> Array.toList
        else
            []

    rootFile @ underParent "apps" @ underParent "libs"

/// Strips a trailing `#` comment from one line.
let private stripTrailingComment (line: string) : string =
    match line.IndexOf('#') with
    | -1 -> line
    | idx -> line.Substring(0, idx)

/// Splits a comma-separated array segment into trimmed, unquoted entries,
/// recognizing both TOML basic (`"clippy"`) and literal (`'clippy'`) strings.
let private parseComponentEntries (segment: string) : string list =
    segment.Split(',')
    |> Array.map (fun e -> e.Trim())
    |> Array.filter (fun e -> e <> "")
    |> Array.map (fun e -> e.Trim('"').Trim('\''))
    |> Array.filter (fun e -> e <> "")
    |> Array.toList

/// Extracts the `components` array declared under `[toolchain]` in a
/// `rust-toolchain.toml` body [Repo-grounded —
/// `checker.rs::read_rust_toolchain_components`].
let readRustToolchainComponents (contents: string) : string list =
    let rec loop (lines: string list) (inArray: bool) (acc: string list) : string list =
        match lines with
        | [] -> acc
        | raw :: rest ->
            let line = stripTrailingComment raw

            if not inArray then
                let trimmedLine = line.Trim()

                match trimmedLine.IndexOf('=') with
                | -1 -> loop rest false acc
                | eqIdx ->
                    let key = trimmedLine.Substring(0, eqIdx).Trim()

                    if key <> "components" then
                        loop rest false acc
                    else
                        let rhs = trimmedLine.Substring(eqIdx + 1).Trim()

                        if not (rhs.StartsWith("[", StringComparison.Ordinal)) then
                            loop rest false acc
                        else
                            let afterOpen = rhs.Substring(1)

                            match afterOpen.IndexOf(']') with
                            | -1 -> loop rest true (acc @ parseComponentEntries afterOpen)
                            | closeIdx -> acc @ parseComponentEntries (afterOpen.Substring(0, closeIdx))
            else
                match line.IndexOf(']') with
                | -1 -> loop rest true (acc @ parseComponentEntries line)
                | closeIdx -> acc @ parseComponentEntries (line.Substring(0, closeIdx))

    loop (contents.Replace("\r\n", "\n").Split('\n') |> Array.toList) false []

/// Builds one [`ToolCheck`] per scanned `rust-toolchain.toml` that omits a
/// required lint component, reported as [`Warning`] rather than [`Missing`]
/// [Repo-grounded — `checker.rs::rust_toolchain_lint_component_checks`].
///
/// Gherkin (binds) — "A pinned Rust toolchain without lint components is
/// reported as a warning" and "A pinned Rust toolchain declaring only one
/// lint component names just the missing one":
///   Given a rust-toolchain.toml pins a channel and declares no lint components
///   When "npm run doctor" runs
///   Then the command exits successfully
///   And it reports the toolchain component check as a warning naming rustfmt and clippy
let rustToolchainLintComponentChecks (repoRoot: string) : ToolCheck list =
    rustToolchainManifests repoRoot
    |> List.choose (fun relative ->
        let fullPath =
            Path.Combine(repoRoot, relative.Replace('/', Path.DirectorySeparatorChar))

        try
            let declared = readRustToolchainComponents (File.ReadAllText fullPath)

            let missing =
                requiredRustToolchainComponents
                |> List.filter (fun required -> not (List.contains required declared))

            if List.isEmpty missing then
                None
            else
                let note =
                    sprintf
                        "%s pins a Rust toolchain but does not declare the %s component(s); a lint gate running cargo fmt/clippy under that channel fails whenever rustup installed it with --profile minimal"
                        relative
                        (String.concat ", " missing)

                Some
                    { Name = "rust-toolchain-components"
                      Binary = ""
                      Status = Warning
                      InstalledVersion = String.concat ", " declared
                      RequiredVersion = String.concat ", " requiredRustToolchainComponents
                      Source = relative
                      Note = note }
        with _ ->
            None)

// --- Playwright browser detection [Repo-grounded — `checker.rs`'s
// "Playwright browser detection" section] ---

/// Pure decision behind [`checkPlaywrightBrowsersAt`]'s platform-specific
/// cache directory choice, split out of the `bool`-driven `if` so both
/// branches are directly testable: a single-OS test process (this
/// development machine is always macOS) can only ever make the real
/// `RuntimeInformation.IsOSPlatform` check take one side, leaving the other
/// permanently unreachable through the ambient wrapper alone.
let playwrightCacheDirFor (isMacOS: bool) (home: string) : string =
    if isMacOS then
        Path.Combine(home, "Library", "Caches", "ms-playwright")
    else
        Path.Combine(home, ".cache", "ms-playwright")

/// Returns `true` when at least one Chromium Playwright browser bundle is
/// found under `home`'s platform-specific Playwright cache directory.
let checkPlaywrightBrowsersAt (home: string option) : bool =
    match home with
    | None -> false
    | Some h ->
        let cacheDir =
            playwrightCacheDirFor (RuntimeInformation.IsOSPlatform(OSPlatform.OSX)) h

        try
            Directory.Exists(cacheDir)
            && Directory.GetDirectories(cacheDir)
               |> Array.exists (fun d -> Path.GetFileName(d: string).StartsWith("chromium-", StringComparison.Ordinal))
        with _ ->
            false

/// Reads the real `HOME` environment variable and returns
/// [`checkPlaywrightBrowsersAt`]'s verdict for the current process.
let checkPlaywrightBrowsersAmbient () : bool =
    match Environment.GetEnvironmentVariable("HOME") with
    | null
    | "" -> checkPlaywrightBrowsersAt None
    | home -> checkPlaywrightBrowsersAt (Some home)

/// Checks whether Playwright browsers are installed, ignoring version
/// strings [Repo-grounded — `checker.rs::compare_playwright`].
let comparePlaywright (_installed: string) (_required: string) : ToolStatus * string =
    if not (checkPlaywrightBrowsersAmbient ()) then
        Warning, "browsers not installed — run: npx playwright install"
    else
        Passing, "no version requirement"

// --- Install-step builders [Repo-grounded — `tools.rs`'s "Install commands"
// section] ---

let private noReq () : string = ""

let installGit (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install Xcode Command Line Tools"
            Command = "xcode-select"
            Args = [ "--install" ] } ]
    else
        [ { Description = "Install git"
            Command = "sudo"
            Args = [ "apt-get"; "install"; "-y"; "git" ] } ]

let installVolta (_req: string) (_platform: string) : InstallStep list =
    [ { Description = "Install Volta"
        Command = "bash"
        Args = [ "-c"; "curl https://get.volta.sh | bash" ] } ]

let installNode (req: string) (_platform: string) : InstallStep list =
    [ { Description = sprintf "Install Node.js %s via Volta" req
        Command = "volta"
        Args = [ "install"; sprintf "node@%s" req ] } ]

let installNpm (req: string) (_platform: string) : InstallStep list =
    [ { Description = sprintf "Install npm %s via Volta" req
        Command = "volta"
        Args = [ "install"; sprintf "npm@%s" req ] } ]

let installRust (_req: string) (_platform: string) : InstallStep list =
    [ { Description = "Install Rust via rustup"
        Command = "bash"
        Args =
          [ "-c"
            "curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y" ] } ]

let installCargoLlvmCov (_req: string) (_platform: string) : InstallStep list =
    [ { Description = "Install cargo-llvm-cov"
        Command = "bash"
        Args = [ "-c"; "source \"$HOME/.cargo/env\" && cargo install cargo-llvm-cov" ] } ]

let private dotnetDefaultChannel = "10.0"

/// Extracts the `major.minor` release channel from a full SDK version
/// string, rejecting any non-digit character in either segment as a
/// shell-injection guard [Repo-grounded — `tools.rs::dotnet_channel`].
let dotnetChannel (req: string) : string =
    let parts = req.Split('.')

    if
        parts.Length >= 2
        && parts.[0] <> ""
        && parts.[1] <> ""
        && parts.[0] |> Seq.forall Char.IsDigit
        && parts.[1] |> Seq.forall Char.IsDigit
    then
        sprintf "%s.%s" parts.[0] parts.[1]
    else
        dotnetDefaultChannel

let private dotnetInstallShGpgFingerprint =
    "2B930AB1228D11D5D7F6B6ACB9CF1A51FC7D3ACF"

let installDotnet (req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install .NET via Homebrew"
            Command = "brew"
            Args = [ "install"; "dotnet" ] } ]
    else
        let channel = dotnetChannel req

        let script =
            String.concat
                "\n"
                [ "set -eu"
                  "temp_dir=$(mktemp -d)"
                  "trap 'rm -rf \"$temp_dir\"' EXIT"
                  "curl --proto '=https' --tlsv1.2 -fsSL https://dot.net/v1/dotnet-install.sh -o \"$temp_dir/dotnet-install.sh\""
                  "curl --proto '=https' --tlsv1.2 -fsSL https://dot.net/v1/dotnet-install.sig -o \"$temp_dir/dotnet-install.sig\""
                  "curl --proto '=https' --tlsv1.2 -fsSL https://dot.net/v1/dotnet-install.asc -o \"$temp_dir/dotnet-install.asc\""
                  "export GNUPGHOME=\"$temp_dir/gnupg\""
                  "mkdir -m 700 \"$GNUPGHOME\""
                  "gpg --batch --import \"$temp_dir/dotnet-install.asc\" >/dev/null 2>&1"
                  "actual_fingerprint=$(gpg --batch --with-colons --fingerprint | awk -F: '/^fpr:/ {print $10; exit}')"
                  sprintf "if [ \"$actual_fingerprint\" != \"%s\" ]; then" dotnetInstallShGpgFingerprint
                  sprintf
                      "  echo \"dotnet-install.sh signing key fingerprint mismatch: expected %s, got $actual_fingerprint\" >&2"
                      dotnetInstallShGpgFingerprint
                  "  exit 1"
                  "fi"
                  "gpg --batch --verify \"$temp_dir/dotnet-install.sig\" \"$temp_dir/dotnet-install.sh\""
                  "sudo mkdir -p /usr/share/dotnet"
                  "sudo chown \"$(id -u):$(id -g)\" /usr/share/dotnet"
                  sprintf "bash \"$temp_dir/dotnet-install.sh\" --channel %s --install-dir /usr/share/dotnet" channel
                  "sudo ln -sf /usr/share/dotnet/dotnet /usr/local/bin/dotnet" ]

        [ { Description = sprintf "Install .NET %s via the official install script" channel
            Command = "bash"
            Args = [ "-c"; script ] } ]

let installDocker (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        []
    else
        [ { Description = "Install Docker"
            Command = "sudo"
            Args = [ "apt-get"; "install"; "-y"; "docker.io"; "docker-compose-v2" ] } ]

let installJq (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install jq via Homebrew"
            Command = "brew"
            Args = [ "install"; "jq" ] } ]
    else
        [ { Description = "Install jq"
            Command = "sudo"
            Args = [ "apt-get"; "install"; "-y"; "jq" ] } ]

let installShellcheck (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install shellcheck via Homebrew"
            Command = "brew"
            Args = [ "install"; "shellcheck" ] } ]
    else
        [ { Description = "Install shellcheck"
            Command = "sudo"
            Args = [ "apt-get"; "install"; "-y"; "shellcheck" ] } ]

let installActionlint (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install actionlint via Homebrew"
            Command = "brew"
            Args = [ "install"; "actionlint" ] } ]
    else
        [ { Description = "Install actionlint via the official download script"
            Command = "sudo"
            Args =
              [ "bash"
                "-c"
                "curl -sSL https://raw.githubusercontent.com/rhysd/actionlint/v1.7.12/scripts/download-actionlint.bash | bash -s -- 1.7.12 /usr/local/bin" ] } ]

let installHadolint (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install hadolint via Homebrew"
            Command = "brew"
            Args = [ "install"; "hadolint" ] } ]
    else
        [ { Description = "Download hadolint binary"
            Command = "sudo"
            Args =
              [ "curl"
                "-sSL"
                "-o"
                "/usr/local/bin/hadolint"
                "https://github.com/hadolint/hadolint/releases/download/v2.14.0/hadolint-Linux-x86_64" ] }
          { Description = "Make hadolint executable"
            Command = "sudo"
            Args = [ "chmod"; "+x"; "/usr/local/bin/hadolint" ] } ]

let installShfmt (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install shfmt via Homebrew"
            Command = "brew"
            Args = [ "install"; "shfmt" ] } ]
    else
        [ { Description = "Download shfmt binary"
            Command = "sudo"
            Args =
              [ "curl"
                "-sSL"
                "-o"
                "/usr/local/bin/shfmt"
                "https://github.com/mvdan/sh/releases/download/v3.13.1/shfmt_v3.13.1_linux_amd64" ] }
          { Description = "Make shfmt executable"
            Command = "sudo"
            Args = [ "chmod"; "+x"; "/usr/local/bin/shfmt" ] } ]

/// Exact `OpenTofu` version installed by the macOS and Linux doctor
/// bootstrappers [Repo-grounded — `tools.rs::OPENTOFU_VERSION`].
let private openTofuVersion = "1.12.3"

let private openTofuReleaseBaseUrl =
    "https://github.com/opentofu/opentofu/releases/download/v1.12.3"

let private openTofuDarwinAmd64Sha256 =
    "0898350dcc5b2ae31ad104cf4882228d08f858ba28f4e8bea693b51d1b267c57"

let private openTofuDarwinArm64Sha256 =
    "2b81c065cdcf5e573cfb5d9e0c663ac4cfc32512927078b645b58ef81cec2474"

let private openTofuLinuxAmd64Sha256 =
    "46b48c3438c65cf479fc076c9281422ffa2f493548d1e813d154c835c5986a08"

let private openTofuLinuxArm64Sha256 =
    "b2110d1ce46e366ce861b7f53d293dad99080075629aed7fb50d7328916d91c2"

let private readTofuVersion () : string = openTofuVersion

/// Returns install steps for `tofu` (`OpenTofu`): a pinned official release
/// archive whose checksum is authenticated against the hash committed
/// alongside this installer, never a mutable shell script fetched and
/// executed from the network [Repo-grounded — `tools.rs::install_tofu`].
///
/// Gherkin (binds) — "Fix dry-run previews a verified, platform-safe
/// OpenTofu release archive":
///   Given the tofu tool is not found in the system PATH
///   When the developer runs the doctor command with fix and dry-run flags
///   Then the command exits with a failure code
///   And the output handles verified OpenTofu remediation safely
let installTofu (_req: string) (platform: string) : InstallStep list =
    let checksums =
        match platform with
        | "darwin" -> Some("darwin", "shasum -a 256", openTofuDarwinAmd64Sha256, openTofuDarwinArm64Sha256)
        | "linux" -> Some("linux", "sha256sum", openTofuLinuxAmd64Sha256, openTofuLinuxArm64Sha256)
        | _ -> None

    match checksums with
    | None -> []
    | Some(os, checksumCommand, amd64Checksum, arm64Checksum) ->
        let script =
            String.concat
                "\n"
                [ "set -eu"
                  "case \"$(uname -m)\" in"
                  sprintf "  x86_64) arch=amd64; expected_checksum=%s ;;" amd64Checksum
                  sprintf "  arm64|aarch64) arch=arm64; expected_checksum=%s ;;" arm64Checksum
                  "  *) echo \"Unsupported OpenTofu architecture: $(uname -m)\" >&2; exit 1 ;;"
                  "esac"
                  sprintf "artifact=tofu_%s_%s_${arch}.zip" openTofuVersion os
                  "temp_dir=$(mktemp -d)"
                  "trap 'rm -rf \"$temp_dir\"' EXIT"
                  sprintf
                      "curl --proto '=https' --tlsv1.2 -fsSL %s/\"$artifact\" -o \"$temp_dir/$artifact\""
                      openTofuReleaseBaseUrl
                  sprintf "actual_checksum=$(%s \"$temp_dir/$artifact\" | awk '{print $1}')" checksumCommand
                  "if [ \"$actual_checksum\" != \"$expected_checksum\" ]; then"
                  "  echo \"OpenTofu archive checksum mismatch\" >&2"
                  "  exit 1"
                  "fi"
                  "unzip -q \"$temp_dir/$artifact\" -d \"$temp_dir/extract\""
                  "sudo install -m 0755 \"$temp_dir/extract/tofu\" /usr/local/bin/tofu" ]

        [ { Description = "Install verified OpenTofu release archive"
            Command = "bash"
            Args = [ "-c"; script ] } ]

let installClangFormat (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install clang-format via Homebrew"
            Command = "brew"
            Args = [ "install"; "clang-format" ] } ]
    else
        [ { Description = "Install clang-format"
            Command = "sudo"
            Args = [ "apt-get"; "install"; "-y"; "clang-format" ] } ]

let installPlaywright (_req: string) (platform: string) : InstallStep list =
    if platform = "darwin" then
        [ { Description = "Install Playwright browsers"
            Command = "npx"
            Args = [ "playwright"; "install" ] } ]
    else
        [ { Description = "Install Playwright browsers"
            Command = "npx"
            Args = [ "playwright"; "install" ] }
          { Description = "Install Playwright system deps"
            Command = "npx"
            Args = [ "playwright"; "install-deps" ] } ]

/// Builds the ordered list of tool defs for `repoRoot`
/// [Repo-grounded — `tools.rs::build_tool_defs`].
let buildToolDefs (repoRoot: string) : ToolDef list =
    let packageJsonPath = Path.Combine(repoRoot, "package.json")

    let rustToolchainTomlPath =
        Path.Combine(repoRoot, "apps", "rhino-cli", "rust-toolchain.toml")

    // `doctor.dotnet-global-json` in `repo-config.yml` overrides the .NET SDK
    // config-file location (defaulting to the root `global.json`) — this repo
    // configures `apps/ose-be/global.json` — mirroring
    // `tools.rs::configured_dotnet_global_json`'s repo-config lookup, which a
    // hardcoded root-relative path cannot reproduce.
    let dotnetToolDef =
        RhinoCli.Application.RepoConfig.buildDotnetToolDef
            repoRoot
            (RhinoCli.Application.RepoConfig.loadOrDefault repoRoot)

    [ { Name = "git"
        Binary = "git"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseGitVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installGit }
      { Name = "volta"
        Binary = "volta"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseTrimVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installVolta }
      { Name = "node"
        Binary = "node"
        Source = "package.json → volta.node"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseTrimVersion
        Compare = compareExact
        ReadReq = (fun () -> readNodeVersion packageJsonPath |> Option.defaultValue "")
        InstallCmd = Some installNode }
      { Name = "npm"
        Binary = "npm"
        Source = "package.json → volta.npm"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseTrimVersion
        Compare = compareExact
        ReadReq = (fun () -> readNpmVersion packageJsonPath |> Option.defaultValue "")
        InstallCmd = Some installNpm }
      { Name = "rust"
        Binary = "rustc"
        Source = "apps/rhino-cli/rust-toolchain.toml → channel"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseRustVersion
        Compare = compareExact
        ReadReq = (fun () -> readRustToolchainChannel rustToolchainTomlPath |> Option.defaultValue "")
        InstallCmd = Some installRust }
      { Name = "cargo-llvm-cov"
        Binary = "cargo"
        Source = "(no config file)"
        Args = [ "llvm-cov"; "--version" ]
        UseStderr = false
        ParseVer = parseCargoLlvmCovVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installCargoLlvmCov }
      { Name = "dotnet"
        Binary = "dotnet"
        Source = dotnetToolDef.Source
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseDotnetVersion
        Compare = compareMajorGte
        ReadReq = dotnetToolDef.ReadReq
        InstallCmd = Some installDotnet }
      { Name = "docker"
        Binary = "docker"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseDockerVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installDocker }
      { Name = "jq"
        Binary = "jq"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseJqVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installJq }
      { Name = "shellcheck"
        Binary = "shellcheck"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseShellcheckVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installShellcheck }
      { Name = "hadolint"
        Binary = "hadolint"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseHadolintVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installHadolint }
      { Name = "actionlint"
        Binary = "actionlint"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseActionlintVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installActionlint }
      { Name = "playwright"
        Binary = "npx"
        Source = "node_modules (npx playwright)"
        Args = [ "playwright"; "--version" ]
        UseStderr = false
        ParseVer = parsePlaywrightVersion
        Compare = comparePlaywright
        ReadReq = noReq
        InstallCmd = Some installPlaywright }
      { Name = "shfmt"
        Binary = "shfmt"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseTrimVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installShfmt }
      { Name = "tofu"
        Binary = "tofu"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseTofuVersion
        Compare = compareGte
        ReadReq = readTofuVersion
        InstallCmd = Some installTofu }
      { Name = "clang-format"
        Binary = "clang-format"
        Source = "(no config file)"
        Args = [ "--version" ]
        UseStderr = false
        ParseVer = parseClangFormatVersion
        Compare = compareExact
        ReadReq = noReq
        InstallCmd = Some installClangFormat } ]

/// Builds the tool definitions selected by scope, explicit selection, and the
/// repository's `doctor.skip-tools` configuration
/// [Repo-grounded — `mod.rs::selected_tool_defs`].
///
/// Gherkin (binds) — "An explicit tool selection probes and reports only
/// that tool" and "A repo-config-declared tool is skipped from the check":
///   Given all required development tools are present with matching versions
///   And the unselected shellcheck tool is not found in the system PATH
///   And only the tofu tool is selected
///   When the developer runs the doctor command
///   Then the command exits successfully
///   And the output reports only the selected tofu tool
let selectedToolDefs (options: CheckOptions) : ToolDef list =
    let scoped =
        buildToolDefs options.RepoRoot
        |> List.filter (fun d -> options.Scope <> MinimalScope || isMinimalTool d.Name)

    let explicitlySelected =
        match options.SelectedTools with
        | None -> scoped
        | Some selected -> scoped |> List.filter (fun d -> List.contains d.Name selected)

    let skipTools =
        (RhinoCli.Application.RepoConfig.loadOrDefault options.RepoRoot).Doctor.SkipTools

    explicitlySelected
    |> List.filter (fun d -> not (List.contains d.Name skipTools))

// --- Runner [Repo-grounded — `checker.rs`'s "Runner" section] ---

/// Mirrors `exec.LookPath`/`binary_in_path`: walks `PATH` for an executable
/// file named `name`, or checks the path directly when it contains a
/// separator.
let private binaryInPath (name: string) : bool =
    if name.Contains('/') then
        File.Exists(name)
    else
        match Environment.GetEnvironmentVariable("PATH") with
        | null -> false
        | pathVar ->
            pathVar.Split(Path.PathSeparator)
            |> Array.exists (fun dir -> dir <> "" && File.Exists(Path.Combine(dir, name)))

/// Executes `name` with `args` and returns `(stdout, stderr, exitCode)`.
/// Returns `Error` when `name` is not found in `PATH` (no process is
/// started) [Repo-grounded — `checker.rs::real_runner`].
let realRunner: CommandRunner =
    fun name args ->
        if not (binaryInPath name) then
            Error(sprintf "binary not found in PATH: %s" name)
        else
            try
                use proc = new Process()
                proc.StartInfo.FileName <- name
                args |> List.iter proc.StartInfo.ArgumentList.Add
                proc.StartInfo.RedirectStandardOutput <- true
                proc.StartInfo.RedirectStandardError <- true
                proc.StartInfo.UseShellExecute <- false
                proc.Start() |> ignore
                let stdout = proc.StandardOutput.ReadToEnd()
                let stderr = proc.StandardError.ReadToEnd()
                proc.WaitForExit()
                Ok(stdout, stderr, proc.ExitCode)
            with ex ->
                Error ex.Message

/// Executes a single [`ToolDef`] check using `runner` and returns a
/// [`ToolCheck`]. When `runner` returns `Error` (binary not found), the check
/// is immediately recorded as [`Missing`] without calling any parser or
/// comparator [Repo-grounded — `checker.rs::run_one_def`].
///
/// Gherkin (binds) — "A required tool is missing from the environment":
///   Given a required development tool is not found in the system PATH
///   When the developer runs the doctor command
///   Then the command exits with a failure code
///   And the output identifies the missing tool
let runOneDef (runner: CommandRunner) (def: ToolDef) : ToolCheck =
    let requiredVersion = def.ReadReq()

    match runner def.Binary def.Args with
    | Error _ ->
        { Name = def.Name
          Binary = def.Binary
          Status = Missing
          InstalledVersion = ""
          RequiredVersion = requiredVersion
          Source = def.Source
          Note = "not found in PATH" }
    | Ok(stdout, stderr, _code) ->
        let output = if def.UseStderr then stderr else stdout
        let installed = def.ParseVer output
        let status, note = def.Compare installed requiredVersion

        { Name = def.Name
          Binary = def.Binary
          Status = status
          InstalledVersion = installed
          RequiredVersion = requiredVersion
          Source = def.Source
          Note = note }

/// Runs all tool checks described in `options` and returns aggregated
/// results [Repo-grounded — `checker.rs::check_all`].
///
/// Gherkin (binds) — "All required tools are installed and versions match":
///   Given all required development tools are present with matching versions
///   When the developer runs the doctor command
///   Then the command exits successfully
///   And the output reports each tool as passing
let checkAll (options: CheckOptions) : DoctorResult =
    let runner = options.Runner |> Option.defaultValue realRunner
    let defs = selectedToolDefs options
    let baseChecks = defs |> List.map (runOneDef runner)

    let checks =
        if defs |> List.exists (fun d -> d.Name = "rust") then
            baseChecks @ rustToolchainLintComponentChecks options.RepoRoot
        else
            baseChecks

    let ok, warn, missing =
        checks
        |> List.fold
            (fun (okAcc, warnAcc, missingAcc) c ->
                match c.Status with
                | Passing -> okAcc + 1, warnAcc, missingAcc
                | Warning -> okAcc, warnAcc + 1, missingAcc
                | Missing -> okAcc, warnAcc, missingAcc + 1)
            (0, 0, 0)

    { Checks = checks
      OkCount = ok
      WarnCount = warn
      MissingCount = missing
      Scope = options.Scope }

// --- Fixer [Repo-grounded — `fixer.rs`] ---

/// Returns whether a Doctor check needs an installation/remediation attempt:
/// missing tools always, and a version warning only for `tofu`, whose
/// minimum version is a security requirement
/// [Repo-grounded — `fixer.rs::needs_remediation`].
let needsRemediation (check: ToolCheck) : bool =
    check.Status = Missing || (check.Status = Warning && check.Name = "tofu")

/// `true` when at least one check in `result` needs remediation
/// [Repo-grounded — `commands/doctor.rs::has_remediation_work`].
///
/// Gherkin (binds) — "Fix reports nothing to fix when all tools are present":
///   Given all required development tools are present with matching versions
///   When the developer runs the doctor command with the fix flag
///   Then the command exits successfully
///   And the output reports nothing to fix
let hasRemediationWork (result: DoctorResult) : bool =
    result.Checks |> List.exists needsRemediation

/// Pure decision table behind [`currentPlatform`], split out so every
/// branch is directly testable: a single-OS test process (this development
/// machine is always macOS) can only ever make the real
/// `RuntimeInformation.IsOSPlatform` checks take one of the three paths,
/// leaving the other two permanently unreachable through the real,
/// ambient-reading wrapper alone.
let platformFromFlags (isOSX: bool) (isLinux: bool) : string =
    if isOSX then "darwin"
    elif isLinux then "linux"
    else "other"

let private currentPlatform () : string =
    platformFromFlags
        (RuntimeInformation.IsOSPlatform(OSPlatform.OSX))
        (RuntimeInformation.IsOSPlatform(OSPlatform.Linux))

/// Summary of a completed fix run [Repo-grounded — `fixer.rs::FixResult`].
type FixResult =
    { Fixed: int
      Failed: int
      AlreadyOk: int
      Skipped: int }

let private zeroFixResult =
    { Fixed = 0
      Failed = 0
      AlreadyOk = 0
      Skipped = 0 }

/// Executes a single install-command step; `Error` on non-zero exit or spawn
/// failure [Repo-grounded — `fixer.rs::FixRunnerFunc`].
type FixRunner = string -> string list -> Result<unit, string>

/// Default fix runner: executes `command` with `args`, inheriting
/// stdout/stderr [Repo-grounded — `fixer.rs::real_fix_runner`].
let realFixRunner: FixRunner =
    fun command args ->
        try
            use proc = new Process()
            proc.StartInfo.FileName <- command
            args |> List.iter proc.StartInfo.ArgumentList.Add
            proc.StartInfo.UseShellExecute <- false
            proc.Start() |> ignore
            proc.WaitForExit()

            if proc.ExitCode = 0 then
                Ok()
            else
                Error(sprintf "exit %d" proc.ExitCode)
        with ex ->
            Error ex.Message

/// Options controlling a fix run [Repo-grounded — `fixer.rs::FixOptions`].
type FixOptions =
    { DryRun: bool
      Runner: FixRunner option }

/// Attempts to install actionable tools from a pre-built `defs` list,
/// emitting progress messages via `printf`. When `options.DryRun` is `true`,
/// steps are printed but not executed and [`FixResult.Fixed`] stays zero
/// [Repo-grounded — `fixer.rs::fix`].
///
/// Gherkin (binds) — "Fix installs missing tools" and "Fix with dry-run
/// previews without executing":
///   Given a required development tool is not found in the system PATH
///   When the developer runs the doctor command with the fix flag
///   Then the output contains fix progress
let fix (result: DoctorResult) (defs: ToolDef list) (options: FixOptions) (printf: string -> unit) : FixResult =
    let platform = currentPlatform ()
    let runner = options.Runner |> Option.defaultValue realFixRunner
    let defsArray = List.toArray defs

    let rec runSteps (name: string) (steps: InstallStep list) : bool =
        match steps with
        | [] -> false
        | step :: rest ->
            if options.DryRun then
                printf (sprintf "Would install: %s via %s %s\n" name step.Command (String.concat " " step.Args))
                runSteps name rest
            else
                printf (sprintf "Installing %s: %s\n" name step.Description)

                match runner step.Command step.Args with
                | Error e ->
                    printf (sprintf "  Failed: %s\n" e)
                    true
                | Ok() -> runSteps name rest

    result.Checks
    |> List.indexed
    |> List.fold
        (fun acc (i, check) ->
            if not (needsRemediation check) then
                { acc with
                    AlreadyOk = acc.AlreadyOk + 1 }
            else
                let installCmd =
                    if i < defsArray.Length then
                        defsArray.[i].InstallCmd
                    else
                        None

                match installCmd with
                | None ->
                    printf (sprintf "Skip: %s — no auto-install available\n" check.Name)
                    { acc with Skipped = acc.Skipped + 1 }
                | Some installFn ->
                    let steps = installFn check.RequiredVersion platform

                    if List.isEmpty steps then
                        printf (sprintf "Skip: %s — no install steps for platform %s\n" check.Name platform)
                        { acc with Skipped = acc.Skipped + 1 }
                    else
                        let failed = runSteps check.Name steps

                        if options.DryRun then acc
                        elif failed then { acc with Failed = acc.Failed + 1 }
                        else { acc with Fixed = acc.Fixed + 1 })
        zeroFixResult

/// Builds tool definitions from `options` and then delegates to [`fix`]
/// [Repo-grounded — `fixer.rs::fix_all`].
///
/// Gherkin (binds) — "A selected missing tool has only its remediation
/// previewed":
///   Given the tofu tool is not found in the system PATH
///   And only the tofu tool is selected
///   When the developer runs the doctor command with fix and dry-run flags
///   Then the command exits with a failure code
///   And the selected tofu dry run previews only its remediation
let fixAll
    (result: DoctorResult)
    (options: CheckOptions)
    (fixOptions: FixOptions)
    (printf: string -> unit)
    : FixResult =
    fix result (selectedToolDefs options) fixOptions printf

/// Returns a one-line human-readable summary of a [`FixResult`]
/// [Repo-grounded — `fixer.rs::format_fix_summary`].
let formatFixSummary (fr: FixResult) : string =
    sprintf "\nFix summary: %d fixed, %d failed, %d already OK\n" fr.Fixed fr.Failed fr.AlreadyOk

/// The plain text `doctor --fix` prints when every check already passes
/// [Repo-grounded — `commands/doctor.rs::run`'s
/// `"\nNothing to fix — all tools are installed."` branch].
let formatNothingToFix: string = "\nNothing to fix — all tools are installed.\n"

// --- Reporter [Repo-grounded — `reporter.rs`] ---

let private symbolFor (status: ToolStatus) : string =
    match status with
    | Passing -> "\u2713" // check mark
    | Warning -> "\u26A0" // warning sign
    | Missing -> "\u2717" // ballot X

let private displayVersion (c: ToolCheck) : string =
    if c.Status = Missing then "not found"
    elif c.InstalledVersion = "" then "(unknown)"
    else sprintf "v%s" c.InstalledVersion

/// Formats `result` as human-readable text [Repo-grounded —
/// `reporter.rs::format_text`].
///
/// Gherkin (binds) — "Full scope is the default behavior":
///   Given all required development tools are present with matching versions
///   When the developer runs the doctor command
///   Then the command exits successfully
///   And the output reports each tool as passing
let formatDoctorText (result: DoctorResult) (quiet: bool) : string =
    let sb = Text.StringBuilder()

    if not quiet then
        sb.Append("Doctor Report\n").Append("=============\n\n") |> ignore

    for check in result.Checks do
        sb.Append(sprintf "%s %-10s %-14s (%s)\n" (symbolFor check.Status) check.Name (displayVersion check) check.Note)
        |> ignore

    let total = result.OkCount + result.WarnCount + result.MissingCount

    let scopeSuffix =
        if result.Scope = MinimalScope then
            " (scope: minimal)"
        else
            ""

    sb.Append(
        sprintf
            "\nSummary: %d/%d tools OK, %d warning, %d missing%s\n"
            result.OkCount
            total
            result.WarnCount
            result.MissingCount
            scopeSuffix
    )
    |> ignore

    sb.ToString()

/// Serialises `result` to a pretty-printed JSON string
/// [Repo-grounded — `reporter.rs::format_json`].
///
/// `durationMs` is the caller-measured wall-clock duration of the check run
/// in milliseconds — `DoctorResult` itself carries no timing field (this
/// port's `checkAll` is synchronous and pure-enough that callers time it
/// externally), matching `reporter.rs::format_json`'s always-present
/// `duration_ms`/`timestamp` fields byte-for-byte for `shadow-diff.sh`
/// (both are masked as volatile before comparison, so the exact value never
/// needs to match — only the field's presence, position, and JSON shape do).
///
/// Gherkin (binds) — "JSON output lists all tool check results":
///   Given all required development tools are present with matching versions
///   When the developer runs the doctor command with JSON output
///   Then the command exits successfully
///   And the output is valid JSON
///   And the JSON lists every checked tool with its status
let formatDoctorJson (result: DoctorResult) (durationMs: int64) : string =
    let toolNode (c: ToolCheck) : JsonNode =
        let node = JsonObject()
        node.["name"] <- JsonValue.Create(c.Name)
        node.["binary"] <- JsonValue.Create(c.Binary)
        node.["status"] <- JsonValue.Create(toolStatusCode c.Status)

        if c.InstalledVersion <> "" then
            node.["installed_version"] <- JsonValue.Create(c.InstalledVersion)

        if c.RequiredVersion <> "" then
            node.["required_version"] <- JsonValue.Create(c.RequiredVersion)

        if c.Source <> "" then
            node.["source"] <- JsonValue.Create(c.Source)

        if c.Note <> "" then
            node.["note"] <- JsonValue.Create(c.Note)

        node :> JsonNode

    let overallStatus =
        if result.MissingCount > 0 then "missing"
        elif result.WarnCount > 0 then "warning"
        else "ok"

    let root = JsonObject()
    root.["status"] <- JsonValue.Create(overallStatus)
    // `Scope::code()` never returns an empty string (`"full"` or `"minimal"`),
    // so `reporter.rs::format_json`'s `skip_serializing_if = "str::is_empty"`
    // on this field never actually skips it — always present.
    root.["scope"] <- JsonValue.Create(doctorScopeCode result.Scope)
    root.["timestamp"] <- JsonValue.Create(DateTimeOffset.Now.ToString("yyyy-MM-ddTHH:mm:sszzz"))
    root.["ok_count"] <- JsonValue.Create(result.OkCount)
    root.["warn_count"] <- JsonValue.Create(result.WarnCount)
    root.["missing_count"] <- JsonValue.Create(result.MissingCount)
    root.["duration_ms"] <- JsonValue.Create(durationMs)
    root.["tools"] <- JsonArray(result.Checks |> List.map toolNode |> Array.ofList)

    let serializeOptions = JsonSerializerOptions()
    serializeOptions.WriteIndented <- true
    serializeOptions.Encoder <- JavaScriptEncoder.UnsafeRelaxedJsonEscaping
    root.ToJsonString(serializeOptions)

/// Formats `result` as a Markdown report with a summary table and a per-tool
/// table [Repo-grounded — `reporter.rs::format_markdown`]. `durationMs` is
/// unused here — the Markdown report has no duration field, only
/// `**Generated**` (masked as volatile by `shadow-diff.sh`, same as the JSON
/// formatter's `timestamp`).
let formatDoctorMarkdown (result: DoctorResult) : string =
    let sb = Text.StringBuilder()
    sb.Append("## Doctor Report\n\n") |> ignore

    sb.Append(sprintf "**Generated**: %s\n\n" (DateTimeOffset.Now.ToString("yyyy-MM-ddTHH:mm:sszzz")))
    |> ignore

    let total = result.OkCount + result.WarnCount + result.MissingCount
    sb.Append("### Summary\n\n") |> ignore
    sb.Append("| Metric | Value |\n") |> ignore
    sb.Append("|--------|-------|\n") |> ignore
    sb.Append(sprintf "| OK | %d |\n" result.OkCount) |> ignore
    sb.Append(sprintf "| Warning | %d |\n" result.WarnCount) |> ignore
    sb.Append(sprintf "| Missing | %d |\n" result.MissingCount) |> ignore
    sb.Append(sprintf "| Total | %d |\n" total) |> ignore
    sb.Append("\n") |> ignore

    sb.Append("### Tools\n\n") |> ignore
    sb.Append("| Tool | Status | Installed | Required | Note |\n") |> ignore
    sb.Append("|------|--------|-----------|----------|------|\n") |> ignore

    for c in result.Checks do
        sb.Append(
            sprintf
                "| %s | %s %s | %s | %s | %s |\n"
                c.Name
                (symbolFor c.Status)
                (toolStatusCode c.Status)
                (displayVersion c)
                c.RequiredVersion
                c.Note
        )
        |> ignore

    sb.ToString()

// ---------------------------------------------------------------------------
// F# lint-target Fantomas tool-invocation check [F#-native meta-check — no
// Rust equivalent; `apps/rhino-cli/src` never invoked Fantomas] for
// `specs/apps/rhino/cli/behaviors/system/fsharp-tool-invocation.feature`'s
// 1 scenario.
// ---------------------------------------------------------------------------

/// One `project.json` file whose `lint` target's `commands` array invokes
/// Fantomas at least once, together with that array for evaluation.
type FsharpLintTarget =
    { ProjectJsonPath: string
      Commands: string list }

/// Directory names a `project.json` scan never descends into: build output,
/// dependency, and VCS directories that are never themselves project
/// boundaries.
let private excludedProjectJsonDirNames: Set<string> =
    Set.ofList [ "node_modules"; "obj"; "bin"; ".git"; ".nx"; "dist" ]

/// Recursively walks `dir`, skipping [`excludedProjectJsonDirNames`],
/// returning every `project.json` file path found at any depth — deeper than
/// [`discoverCrates`]'s single-level walk, since an F# Nx project can nest a
/// `project.json` below its app directory (e.g.
/// `apps/rhino-cli/src-fsharp/project.json`).
let rec private findProjectJsonFiles (dir: string) : string list =
    if not (Directory.Exists dir) then
        []
    else
        let here =
            let candidate = Path.Combine(dir, "project.json")
            if File.Exists candidate then [ candidate ] else []

        let nested =
            Directory.GetDirectories dir
            |> Array.filter (fun d -> not (Set.contains (Path.GetFileName(d: string)) excludedProjectJsonDirNames))
            |> Array.toList
            |> List.collect findProjectJsonFiles

        here @ nested

/// Extracts the `targets.lint.options.commands` JSON string array from the
/// `project.json` at `projectJsonPath`, returning an empty list when the
/// file is missing, malformed, or lacks that path.
let private readLintCommands (projectJsonPath: string) : string list =
    try
        use doc = JsonDocument.Parse(File.ReadAllText projectJsonPath)

        match doc.RootElement.TryGetProperty "targets" with
        | false, _ -> []
        | true, targetsEl ->
            match targetsEl.TryGetProperty "lint" with
            | false, _ -> []
            | true, lintEl ->
                match lintEl.TryGetProperty "options" with
                | false, _ -> []
                | true, optionsEl ->
                    match optionsEl.TryGetProperty "commands" with
                    | true, commandsEl when commandsEl.ValueKind = JsonValueKind.Array ->
                        commandsEl.EnumerateArray()
                        |> Seq.choose (fun c ->
                            if c.ValueKind = JsonValueKind.String then
                                Some(c.GetString())
                            else
                                None)
                        |> Seq.toList
                    | _ -> []
    with _ ->
        []

/// Returns `true` when `command` invokes Fantomas in any form.
let private commandInvokesFantomas (command: string) : bool = command.Contains("fantomas")

/// Returns `true` when `command` restores the local `.NET` tool manifest
/// declared in `.config/dotnet-tools.json`.
let private commandRestoresToolManifest (command: string) : bool = command.Contains("dotnet tool restore")

/// Returns `true` when `command` invokes Fantomas through the pinned local
/// tool manifest (`dotnet tool run fantomas`) or the equivalent
/// `dotnet fantomas` driver form, rather than a bare global `fantomas`
/// binary call.
let private commandInvokesFantomasViaLocalTool (command: string) : bool =
    command.Contains("dotnet tool run fantomas")
    || command.Contains("dotnet fantomas")

/// Discovers every `project.json` under `repoRoot/apps` and `repoRoot/libs`
/// (at any depth) whose `lint` target's `commands` array invokes Fantomas at
/// least once, sorted by repo-relative path for deterministic iteration
/// order [F#-native meta-check].
///
/// Gherkin (binds) — "Every locally discovered F# lint target uses the
/// pinned local Fantomas tool":
///   Given the local F# lint targets are discovered
let discoverFsharpLintTargets (repoRoot: string) : FsharpLintTarget list =
    [ "apps"; "libs" ]
    |> List.collect (fun top -> findProjectJsonFiles (Path.Combine(repoRoot, top)))
    |> List.choose (fun path ->
        let commands = readLintCommands path

        if commands |> List.exists commandInvokesFantomas then
            let relative =
                Path.GetRelativePath(repoRoot, path).Replace(Path.DirectorySeparatorChar, '/')

            Some
                { ProjectJsonPath = relative
                  Commands = commands }
        else
            None)
    |> List.sortBy (fun t -> t.ProjectJsonPath)

/// Returns `true` when `commands` runs `dotnet tool restore` at some point
/// strictly before the first command invoking Fantomas — proving the local
/// tool manifest is consulted before Fantomas runs. `false` when either
/// command is absent.
let private restoresManifestBeforeFantomas (commands: string list) : bool =
    let fantomasIdx = commands |> List.tryFindIndex commandInvokesFantomas
    let restoreIdx = commands |> List.tryFindIndex commandRestoresToolManifest

    match restoreIdx, fantomasIdx with
    | Some r, Some f -> r < f
    | _ -> false

/// Returns `true` when at least one command invokes Fantomas via a bare
/// global `fantomas` binary call rather than through the pinned local tool.
let private invokesFantomasGlobally (commands: string list) : bool =
    commands
    |> List.exists (fun c -> commandInvokesFantomas c && not (commandInvokesFantomasViaLocalTool c))

/// Result of evaluating one [`FsharpLintTarget`]: the target itself plus
/// every [`Finding`] describing a Fantomas-invocation compliance violation
/// (empty when the target is fully compliant). Reuses the shared `Finding`
/// record from `RhinoCli.Domain.Types` rather than a bespoke type, following
/// `Convention.fs`'s "shared Finding over bespoke per-validator types"
/// precedent.
type FsharpToolInvocationCheck =
    { Target: FsharpLintTarget
      Findings: Finding list }

/// Evaluates one [`FsharpLintTarget`], returning every [`Finding`]
/// describing a Fantomas-invocation compliance violation.
let private evaluateOneFsharpLintTarget (target: FsharpLintTarget) : FsharpToolInvocationCheck =
    let findings =
        [ if not (restoresManifestBeforeFantomas target.Commands) then
              { Severity = Severity.Blocking
                Message = "does not restore the local .NET tool manifest (dotnet tool restore) before running Fantomas"
                Path = Some target.ProjectJsonPath }
          if invokesFantomasGlobally target.Commands then
              { Severity = Severity.Blocking
                Message =
                  "invokes the global Fantomas app host directly instead of the pinned local tool (dotnet tool run fantomas / dotnet fantomas)"
                Path = Some target.ProjectJsonPath } ]

    { Target = target; Findings = findings }

/// Evaluates every locally discovered F# lint target for compliant Fantomas
/// invocation, returning one [`FsharpToolInvocationCheck`] per target — the
/// same count as `targets`, whether or not each target is compliant
/// [F#-native meta-check].
///
/// Gherkin (binds) — "Every locally discovered F# lint target uses the
/// pinned local Fantomas tool":
///   When every locally discovered F# lint target is evaluated
///   Then every discovered F# lint target is evaluated
///   And each target restores its local .NET tool manifest before running Fantomas
///   And no target invokes the global Fantomas app host directly
let evaluateFsharpToolInvocation (targets: FsharpLintTarget list) : FsharpToolInvocationCheck list =
    targets |> List.map evaluateOneFsharpLintTarget

/// Injectable single-file Fantomas format-check probe: given a source-file
/// path, reports whether Fantomas considers it already formatted, or
/// `Error` when the probe itself could not run.
type UnformattedSampleProbe = string -> Result<bool, string>

/// Probes `sampleFile` for Fantomas-detectable formatting drift via `probe`,
/// but only when at least one F# lint target was discovered — a checkout
/// with zero F# lint targets never invokes the probe, so an environment
/// missing the local Fantomas tool never becomes a false failure when there
/// is no F# code to check in the first place [F#-native meta-check].
///
/// Gherkin (binds) — "Every locally discovered F# lint target uses the
/// pinned local Fantomas tool":
///   And an unformatted source file is checked only when F# lint targets exist
let checkUnformattedSample
    (targets: FsharpLintTarget list)
    (sampleFile: string)
    (probe: UnformattedSampleProbe)
    : Result<bool, string> option =
    if List.isEmpty targets then
        None
    else
        Some(probe sampleFile)
