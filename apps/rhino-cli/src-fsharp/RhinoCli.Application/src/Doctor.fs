/// Port of `rhino-cli doctor`'s cargo shared-target-directory symlinking and
/// prune-cache GC step for
/// `specs/apps/rhino/behavior/rhino-cli/gherkin/system/cargo-target-share.feature`'s
/// 18 scenarios [Repo-grounded —
/// `apps/rhino-cli/src/application/doctor/target_share.rs`,
/// `apps/rhino-cli/src/commands/doctor.rs`]. Redirects each Rust crate's
/// `target/` directory to a symlink into a shared, persistent cache keyed by
/// repo name and crate leaf name (`<cache_root>/<repo_name>/<crate_leaf>`),
/// so every git worktree of the same repo shares one physical build
/// directory per crate.
///
/// Scope: this PR ports only the pure, testable `target_share.rs` slice
/// (discovery, cache-root/shared-path resolution, worktree enumeration,
/// check/fix/prune/sweep, and their text formatters) — the general `doctor`
/// tool-check command and its CLI wiring
/// (`specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature`) are
/// a separate, later PR in this same wave.
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
        match Path.GetFileName(parent) with
        | null -> ""
        | name -> name

/// Returns the shared-cache path a crate's `target/` should be symlinked to:
/// `<cacheRoot>/<repoName>/<crateLeaf>`, where `crateLeaf` is `crateDir`'s
/// final path component (e.g. `rhino-cli`)
/// [Repo-grounded — `target_share.rs::shared_target_path`].
let sharedTargetPath (cacheRoot: string) (repoNameValue: string) (crateDir: string) : string =
    let leaf =
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
