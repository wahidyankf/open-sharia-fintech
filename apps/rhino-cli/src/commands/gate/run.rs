//! `gate run` command adapter.

use std::collections::BTreeSet;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::Command;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::repo_config::{
    self, GateKind, GateSurface, GateType, GateWiring, ScopeKind,
};
use crate::commands::repo_config_validate;
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

use super::list;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
/// Source of candidate paths used by a gate scope.
enum CandidateScope {
    /// Files staged for the current Git operation.
    StagedFiles,
    /// Files tracked by Git in the repository.
    TrackedFiles,
    /// Paths whose changes are tested against configured triggers.
    PathTriggers,
    /// A scope that does not require candidate paths.
    None,
}

/// CI event baseline supplied by the workflow for a push-to-main run.
const GATE_CHANGED_BASE_ENV: &str = "GATE_CHANGED_BASE";

/// Changed and tracked repository paths needed by a gate selection.
type CandidatePaths = (Option<Vec<String>>, Option<Vec<String>>);

/// Arguments for `gate run`.
#[derive(Args, Debug)]
pub struct RunArgs {
    /// Surface whose declared gates to run.
    #[arg(long)]
    pub surface: String,
    /// Run only the gate with this id.
    #[arg(long)]
    pub only: Option<String>,
    /// Run only gates whose declared `ci_group` matches this id.
    #[arg(long)]
    pub group: Option<String>,
    /// Commit-message file forwarded only to the `commit-msg` surface.
    #[arg(last = true)]
    pub commit_message_file: Option<PathBuf>,
}

/// Run gates declared on a surface from the current repository root.
///
/// # Errors
///
/// Returns an error when the repository root cannot be found, the surface is
/// invalid, or a declared command cannot be started.
pub fn run(args: &RunArgs, _output_format: OutputFormat) -> Result<(), Error> {
    let repo_root = git::root::find_root()
        .map_err(|error| anyhow!("failed to find git repository root: {error}"))?;
    run_at_root_with_only_and_message_file(
        &repo_root,
        &args.surface,
        args.only.as_deref(),
        args.group.as_deref(),
        args.commit_message_file.as_deref(),
        &mut std::io::stdout(),
    )
}

/// Run gates declared on a surface at a known repository root.
///
/// # Errors
///
/// Returns an error when the surface is invalid, `repo-config.yml` cannot be
/// read, or a declared command cannot be started.
pub fn run_at_root(repo_root: &Path, surface: &str, writer: &mut dyn Write) -> Result<(), Error> {
    run_at_root_with_only(repo_root, surface, None, writer)
}

/// Run gates declared on a surface at a known root, optionally selecting one gate.
///
/// # Errors
///
/// Returns an error when the surface is invalid, `repo-config.yml` cannot be
/// read, a command cannot be started, or a selected gate fails.
pub fn run_at_root_with_only(
    repo_root: &Path,
    surface: &str,
    only: Option<&str>,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    run_at_root_with_only_and_message_file(repo_root, surface, only, None, None, writer)
}

/// Run gates declared on a surface at a known root, restricted to one declared CI group.
///
/// Unlike [`run_at_root_with_only`], every gate in the selected group runs
/// regardless of an earlier gate's failure, and a per-gate summary line
/// (`PASS`/`FAIL`) is written for every gate in the group once the group
/// finishes.
///
/// # Errors
///
/// Returns an error when the surface is invalid, `repo-config.yml` cannot be
/// read, the group id matches no declared gate, a command cannot be started,
/// or any gate in the group fails.
pub fn run_at_root_with_group(
    repo_root: &Path,
    surface: &str,
    group: &str,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    run_at_root_with_only_and_message_file(repo_root, surface, None, Some(group), None, writer)
}

/// Run gates declared on a surface, optionally selecting one gate or CI group and forwarding a commit message.
fn run_at_root_with_only_and_message_file(
    repo_root: &Path,
    surface: &str,
    only: Option<&str>,
    group: Option<&str>,
    commit_message_file: Option<&Path>,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let surface = parse_surface(surface)?;
    if commit_message_file.is_some() && surface != GateSurface::CommitMsg {
        return Err(anyhow!(
            "a commit-message file is only valid for the commit-msg surface"
        ));
    }
    let config = repo_config::load(repo_root)?;
    let surface_gates = config
        .gates
        .iter()
        .filter(|gate| gate.surfaces.contains_key(&surface))
        .collect::<Vec<_>>();
    if only.is_some() {
        list::validate_gate_ids(&surface_gates, only)?;
    }
    let group_gates = resolve_group_gates(&surface_gates, group)?;
    validate_registry_semantics(&config, writer)?;
    let selected_gates = group_gates
        .unwrap_or(surface_gates)
        .into_iter()
        .filter(|gate| only.is_none_or(|id| gate.id == id))
        .collect::<Vec<_>>();
    let (changed_paths, tracked_paths) = candidate_paths(repo_root, &selected_gates, &surface)?;
    let mut batch_ran = false;
    // Threaded worktree snapshot for restaging gates: gate N's "after" snapshot
    // is, by construction, gate N+1's "before" snapshot whenever nothing else
    // mutates the worktree between them (true today — every `restages: true`
    // gate skips or continues immediately when it is not selected, and the
    // lint-staged batch below invalidates this cache on the rare path where it
    // runs between two restaging gates). Threading it here halves the Git
    // process spawns for back-to-back restaging gates (4 -> 2 per gate) with no
    // loss of per-gate mutation-output attribution — see
    // `worktree_changed_paths` and `restage_mutation_outputs`.
    let mut worktree_snapshot: Option<BTreeSet<String>> = None;
    // Every gate's outcome when running a selected group, reported as a
    // trailing summary once the whole group finishes (see below) — unlike the
    // ungrouped path, a group run does not stop at the first failure so every
    // group member gets an observable outcome line.
    let mut group_summary: Vec<(String, bool)> = Vec::new();
    for gate in selected_gates {
        let scope = &gate.surfaces[&surface];
        if scope.scope == ScopeKind::PathGated
            && !changed_paths
                .as_deref()
                .is_some_and(|paths| trigger_matches(paths, &scope.trigger))
        {
            continue;
        }
        let candidate_scope = candidate_scope(&scope.scope);
        let excludes = gate.args.get("exclude").map_or(&[][..], Vec::as_slice);
        let files = match candidate_scope {
            CandidateScope::StagedFiles => retain_existing_paths(
                repo_root,
                matching_files(
                    changed_paths.as_deref().unwrap_or_default(),
                    scope,
                    excludes,
                ),
            ),
            CandidateScope::TrackedFiles => matching_files(
                if scope_has_file_patterns(scope) {
                    tracked_paths.as_deref().unwrap_or_default()
                } else {
                    &[]
                },
                scope,
                excludes,
            ),
            _ => Vec::new(),
        };
        if scope_has_file_patterns(scope)
            && report_empty_scope_skip(writer, &gate.id, candidate_scope, &files)?
        {
            continue;
        }
        if is_pre_commit_batch_eligible(gate, scope, &surface, only) {
            if batch_ran {
                continue;
            }
            run_lint_staged_batch(repo_root, writer)?;
            batch_ran = true;
            // The batch mutates an arbitrary, gate-independent file set, so any
            // cached snapshot from an earlier restaging gate no longer reflects
            // the worktree; force the next restaging gate to recompute fresh.
            worktree_snapshot = None;
            continue;
        }
        writeln!(writer, "Running gate {}", gate.id)?;
        let changed_before = restaging_before_snapshot(gate, &mut worktree_snapshot, repo_root)?;
        let status = run_leaf(
            &gate.kind,
            &gate.command,
            &repo_config::fixed_arguments(gate),
            &files,
            &scope.scope,
            commit_message_file,
            repo_root,
        )?;
        match group {
            Some(_) => group_summary.push((gate.id.clone(), status.success())),
            None if !status.success() => return Err(anyhow!("gate {} failed", gate.id)),
            None => {}
        }
        if status.success() {
            if let Some(changed_before) = changed_before {
                let changed_after = restage_mutation_outputs(repo_root, &changed_before)?;
                worktree_snapshot = Some(changed_after);
            } else if gate.gate_type == GateType::Mutation {
                // A non-restaging mutation (none exist in the registry today, but
                // the schema permits one) can also change the worktree; drop the
                // cache defensively rather than let a future gate misattribute
                // outputs to the wrong gate.
                worktree_snapshot = None;
            }
        }
    }
    if let Some(group_id) = group {
        report_group_summary(group_id, &group_summary, writer)?;
    }
    Ok(())
}

/// Resolves the gates selected by a declared CI group, sharing the
/// "select gates by `ci_group`" predicate with `gate list --by-group`'s
/// bucketing (via [`list::gates_in_ci_group`]) so neither command file
/// carries its own copy.
///
/// Hand-wired gates (`wiring: hand-wired`) are excluded from the returned
/// members: they are dispatched by their own dedicated CI workflow job, not
/// by `--group`, matching `gate list --format=json --by-group`'s own
/// hand-wired exclusion. Without this, a `--group` run would redundantly
/// re-execute a hand-wired gate inside its CI-group job, which can fail
/// there even though the gate's dedicated job runs it correctly (e.g. an
/// `nx`-kind hand-wired gate needs `node_modules`, which a CI-group job may
/// skip installing when none of its *other* members need it).
///
/// # Errors
///
/// Returns an error when `group` is set and matches no gate on the surface.
fn resolve_group_gates<'a>(
    surface_gates: &[&'a repo_config::GateEntry],
    group: Option<&str>,
) -> Result<Option<Vec<&'a repo_config::GateEntry>>, Error> {
    let Some(group_id) = group else {
        return Ok(None);
    };
    let members = list::gates_in_ci_group(surface_gates, group_id)
        .into_iter()
        .filter(|gate| gate.wiring.as_ref() != Some(&GateWiring::HandWired))
        .collect::<Vec<_>>();
    if members.is_empty() {
        return Err(anyhow!(
            "--group id {group_id:?} matched no gates on surface"
        ));
    }
    Ok(Some(members))
}

/// Writes every group member's `PASS`/`FAIL` outcome line, then fails the
/// overall group run if any member failed.
///
/// # Errors
///
/// Returns an error when a summary line cannot be written or any gate in
/// `group_summary` failed.
fn report_group_summary(
    group_id: &str,
    group_summary: &[(String, bool)],
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let mut any_failed = false;
    for (id, passed) in group_summary {
        writeln!(writer, "{id}\t{}", if *passed { "PASS" } else { "FAIL" })?;
        any_failed |= !passed;
    }
    if any_failed {
        return Err(anyhow!("gate group {group_id} failed"));
    }
    Ok(())
}

/// Runs the batched `lint-staged` invocation for eligible pre-commit gates.
///
/// # Errors
///
/// Returns an error when the batch process fails to start or exits non-zero.
fn run_lint_staged_batch(repo_root: &Path, writer: &mut dyn Write) -> Result<(), Error> {
    writeln!(writer, "Running lint-staged batch")?;
    let status = Command::new("npx")
        .args(["--no", "--", "lint-staged"])
        .current_dir(repo_root)
        .status()?;
    if !status.success() {
        return Err(anyhow!("lint-staged batch failed"));
    }
    Ok(())
}

/// Resolves a restaging gate's pre-mutation worktree snapshot, reusing the
/// previous restaging gate's post-mutation snapshot when it is still valid
/// (see the threading rationale at this function's call site) rather than
/// rescanning the worktree. Returns `None` for a non-restaging gate.
///
/// # Errors
///
/// Returns an error when a fresh scan is required and Git cannot list paths.
fn restaging_before_snapshot(
    gate: &repo_config::GateEntry,
    worktree_snapshot: &mut Option<BTreeSet<String>>,
    repo_root: &Path,
) -> Result<Option<BTreeSet<String>>, Error> {
    if !gate.restages {
        return Ok(None);
    }
    Ok(Some(match worktree_snapshot.take() {
        Some(snapshot) => snapshot,
        None => worktree_changed_paths(repo_root)?,
    }))
}

/// Load the candidate paths required by a collection of selected gates.
///
/// # Errors
///
/// Returns an error when Git cannot derive the required changed or tracked paths.
fn candidate_paths(
    repo_root: &Path,
    selected_gates: &[&repo_config::GateEntry],
    surface: &GateSurface,
) -> Result<CandidatePaths, Error> {
    let scopes = selected_gates
        .iter()
        .map(|gate| &gate.surfaces[surface])
        .collect::<Vec<_>>();
    let changed_paths = scopes
        .iter()
        .any(|scope| {
            matches!(
                candidate_scope(&scope.scope),
                CandidateScope::StagedFiles | CandidateScope::PathTriggers
            )
        })
        .then(|| changed_paths(repo_root, surface))
        .transpose()?;
    let tracked_paths = scopes
        .iter()
        .any(|scope| {
            candidate_scope(&scope.scope) == CandidateScope::TrackedFiles
                && scope_has_file_patterns(scope)
        })
        .then(|| tracked_paths(repo_root))
        .transpose()?;
    Ok((changed_paths, tracked_paths))
}

/// Reject malformed gate configuration before selecting a gate or starting a leaf.
fn validate_registry_semantics(
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let findings = repo_config_validate::gate_semantic_findings(config);
    if findings.is_empty() {
        return Ok(());
    }
    for finding in &findings {
        writeln!(writer, "{finding}")?;
    }
    Err(anyhow!(
        "gate run: {} registry semantic finding(s); fix the key(s) listed above",
        findings.len()
    ))
}

/// Returns whether this entry belongs to the single aggregate pre-commit batch.
fn is_pre_commit_batch_eligible(
    gate: &repo_config::GateEntry,
    scope: &repo_config::SurfaceScope,
    surface: &GateSurface,
    only: Option<&str>,
) -> bool {
    *surface == GateSurface::PreCommit
        && only.is_none()
        && scope.scope == ScopeKind::AffectedFileType
        && (gate.gate_type == GateType::Check
            || (gate.gate_type == GateType::Mutation
                && gate.category.as_deref() == Some("formatter")))
}

/// Reports and signals when a file-scoped gate has no matching candidates.
///
/// # Errors
///
/// Returns an error when the skip message cannot be written.
fn report_empty_scope_skip(
    writer: &mut dyn Write,
    gate_id: &str,
    candidate_scope: CandidateScope,
    files: &[String],
) -> Result<bool, Error> {
    if matches!(
        candidate_scope,
        CandidateScope::StagedFiles | CandidateScope::TrackedFiles
    ) && files.is_empty()
    {
        writeln!(writer, "Skipping gate {gate_id}")?;
        return Ok(true);
    }
    Ok(false)
}

/// Maps a registry scope to its candidate-path source.
fn candidate_scope(scope: &ScopeKind) -> CandidateScope {
    match scope {
        ScopeKind::AffectedFileType => CandidateScope::StagedFiles,
        ScopeKind::AllFileType => CandidateScope::TrackedFiles,
        ScopeKind::PathGated => CandidateScope::PathTriggers,
        ScopeKind::AffectedProjects | ScopeKind::AllProjects | ScopeKind::Other => {
            CandidateScope::None
        }
    }
}

/// Runs one declared gate through the executor for its declared kind.
///
/// # Errors
///
/// Returns an error when the selected executor cannot prepare or start its command.
fn run_leaf(
    kind: &GateKind,
    command: &str,
    fixed_arguments: &[String],
    files: &[String],
    scope: &ScopeKind,
    commit_message_file: Option<&Path>,
    repo_root: &Path,
) -> Result<std::process::ExitStatus, Error> {
    match kind {
        GateKind::RhinoCli => run_rhino_cli_leaf(command, fixed_arguments, files, repo_root),
        GateKind::External => run_external_leaf(
            command,
            fixed_arguments,
            files,
            commit_message_file,
            repo_root,
        ),
        GateKind::Nx => run_nx_leaf(command, scope, repo_root),
    }
}

/// Selects candidate paths matching a surface scope and gate exclusions.
fn matching_files(
    changed_paths: &[String],
    scope: &repo_config::SurfaceScope,
    excludes: &[String],
) -> Vec<String> {
    let patterns = scope.glob.iter().chain(&scope.globs).collect::<Vec<_>>();
    filter_candidates(changed_paths, &patterns, excludes)
}

/// Drops candidate paths no longer present in the working tree.
///
/// `changed_paths` (the source `matching_files` filters from) is
/// deliberately left unfiltered by Git change-type, because a `path-gated`
/// gate reads it directly to decide whether *anything* under its trigger
/// changed — including a deletion (see the `PathGated` branch above, which
/// never calls this function). A `StagedFiles`-scoped gate command instead
/// receives file paths to read, lint, or format; a deleted path satisfies
/// none of those, so it is dropped here, at the one consumption point that
/// needs it, rather than upstream where doing so would also blind trigger
/// detection to deletions.
fn retain_existing_paths(repo_root: &Path, files: Vec<String>) -> Vec<String> {
    files
        .into_iter()
        .filter(|path| repo_root.join(path).exists())
        .collect()
}

/// Returns whether a file-scoped gate declares candidate-path patterns.
fn scope_has_file_patterns(scope: &repo_config::SurfaceScope) -> bool {
    scope.glob.is_some() || !scope.globs.is_empty()
}

/// Filters candidate paths by configured glob patterns and exclusions.
fn filter_candidates(
    candidates: &[String],
    patterns: &[&String],
    excludes: &[String],
) -> Vec<String> {
    candidates
        .iter()
        .filter(|path| {
            !is_excluded(path, excludes)
                && (patterns.is_empty()
                    || patterns.iter().any(|pattern| {
                        glob::Pattern::new(pattern).is_ok_and(|pattern| pattern.matches(path))
                    }))
        })
        .cloned()
        .collect()
}

/// Returns whether a path is equal to or below a configured exclusion.
fn is_excluded(path: &str, excludes: &[String]) -> bool {
    excludes.iter().any(|exclude| {
        let prefix = exclude.trim_end_matches('/');
        path == prefix
            || path
                .strip_prefix(prefix)
                .is_some_and(|suffix| suffix.starts_with('/'))
    })
}

/// Runs a Rhino CLI gate with any matching files appended as arguments.
///
/// # Errors
///
/// Returns an error when its argument list is empty or the current executable cannot run.
fn run_rhino_cli_leaf(
    command: &str,
    fixed_arguments: &[String],
    files: &[String],
    repo_root: &Path,
) -> Result<std::process::ExitStatus, Error> {
    let arguments = arguments_with_derived_files(command, fixed_arguments, files)?;
    Command::new(std::env::current_exe()?)
        .args(arguments)
        .current_dir(repo_root)
        .status()
        .map_err(Error::from)
}

/// Runs an external shell command with matching files appended as arguments.
///
/// # Errors
///
/// Returns an error when its command is empty or the shell cannot run.
fn run_external_leaf(
    command: &str,
    fixed_arguments: &[String],
    files: &[String],
    commit_message_file: Option<&Path>,
    repo_root: &Path,
) -> Result<std::process::ExitStatus, Error> {
    if command.trim().is_empty() {
        return Err(anyhow!("external gate command cannot be empty"));
    }
    let command_with_files = format!("{command} \"$@\"");
    let mut arguments = fixed_arguments.to_vec();
    arguments.extend(files.iter().cloned());
    if let Some(commit_message_file) = commit_message_file {
        arguments.push(commit_message_file.to_string_lossy().into_owned());
    }
    let inherited_path = std::env::var_os("PATH");
    let path = external_command_path(repo_root, inherited_path.as_deref())?;
    Command::new("sh")
        .args([
            "-c",
            if commit_message_file.is_some() {
                command
            } else {
                &command_with_files
            },
            "gate-external",
        ])
        .args(arguments)
        .current_dir(repo_root)
        .env("PATH", path)
        .status()
        .map_err(Error::from)
}

/// Prepend the repository's local Node executable directory to a child PATH.
///
/// CI setup installs JavaScript tools in `node_modules/.bin`, but direct shell
/// dispatch does not receive npm-script PATH augmentation. Keeping this child-
/// only preserves the caller's process environment and gives generic external
/// gates the same local-tool resolution as npm scripts.
fn external_command_path(
    repo_root: &Path,
    inherited_path: Option<&std::ffi::OsStr>,
) -> Result<std::ffi::OsString, Error> {
    let mut paths = inherited_path
        .map(std::env::split_paths)
        .map(Iterator::collect::<Vec<_>>)
        .unwrap_or_default();
    paths.insert(0, repo_root.join("node_modules/.bin"));
    std::env::join_paths(paths)
        .map_err(|error| anyhow!("failed to construct external gate PATH: {error}"))
}

/// Runs an Nx target over all or affected projects for the declared scope.
///
/// # Errors
///
/// Returns an error when npm cannot start the selected Nx command.
fn run_nx_leaf(
    target: &str,
    scope: &ScopeKind,
    repo_root: &Path,
) -> Result<std::process::ExitStatus, Error> {
    let arguments = match scope {
        ScopeKind::AllProjects => vec!["exec", "nx", "--", "run-many", "--all", "-t", target],
        // Every other scope kind runs against only the affected project set today.
        // Matched explicitly (rather than via `_`) so that adding a new `ScopeKind`
        // variant is a compile error here until this arm is deliberately updated,
        // mirroring `candidate_scope`'s exhaustive match in this same file.
        ScopeKind::AffectedProjects
        | ScopeKind::AffectedFileType
        | ScopeKind::AllFileType
        | ScopeKind::Other
        | ScopeKind::PathGated => vec!["exec", "nx", "--", "affected", "-t", target],
    };
    Command::new("npm")
        .args(arguments)
        .current_dir(repo_root)
        .status()
        .map_err(Error::from)
}

/// Splits a declared command and appends files derived from its scope.
///
/// # Errors
///
/// Returns an error when the declared command is empty.
fn arguments_with_derived_files(
    command: &str,
    fixed_arguments: &[String],
    files: &[String],
) -> Result<Vec<String>, Error> {
    let mut arguments = command
        .split_whitespace()
        .map(std::string::ToString::to_string)
        .collect::<Vec<_>>();
    if arguments.is_empty() {
        return Err(anyhow!("gate command cannot be empty"));
    }
    arguments.extend(fixed_arguments.iter().cloned());
    arguments.extend(files.iter().cloned());
    Ok(arguments)
}

/// Returns files staged in the Git index for a file-scoped surface.
///
/// # Errors
///
/// Returns an error when Git cannot provide the staged files.
fn changed_paths(repo_root: &Path, surface: &GateSurface) -> Result<Vec<String>, Error> {
    if *surface == GateSurface::PreCommit {
        return staged_paths(repo_root);
    }
    if *surface == GateSurface::Ci
        && let Some(base) = std::env::var(GATE_CHANGED_BASE_ENV)
            .ok()
            .filter(|base| !base.trim().is_empty())
            .filter(|base| commit_resolves(repo_root, base.trim()))
    {
        return changed_paths_from_base(repo_root, base.trim(), GATE_CHANGED_BASE_ENV);
    }
    if matches!(surface, GateSurface::PrePush | GateSurface::Ci) {
        return merge_base_paths(repo_root);
    }
    Ok(Vec::new())
}

/// Returns whether `rev` names a commit reachable in `repo_root`.
///
/// `GATE_CHANGED_BASE` carries `github.event.before`, which is not always a commit this checkout
/// holds: it is all-zeroes on branch creation, absent after a force-push, and absent from any
/// unrelated repository -- including the disposable fixtures the unit tests build, which inherit
/// the ambient CI environment because they call `run_at_root` in-process. Treating an unresolvable
/// base as "no explicit base" lets the caller fall through to the merge base, which computes the
/// same answer the gate would have used without the variable at all. Failing hard instead would
/// break every gate on a force-push for no gain.
fn commit_resolves(repo_root: &Path, rev: &str) -> bool {
    Command::new("git")
        .args([
            "rev-parse",
            "--verify",
            "--quiet",
            &format!("{rev}^{{commit}}"),
        ])
        .current_dir(repo_root)
        .output()
        .is_ok_and(|output| output.status.success())
}

/// Returns paths changed from the branch merge base to `HEAD`.
fn merge_base_paths(repo_root: &Path) -> Result<Vec<String>, Error> {
    let merge_base = Command::new("git")
        .args(["merge-base", "origin/main", "HEAD"])
        .current_dir(repo_root)
        .output()?;
    if !merge_base.status.success() {
        // Disposable fixtures may not configure an origin or make an initial commit. They have no
        // merge base, so use their staged setup state rather than treating it as a production base.
        return staged_paths(repo_root);
    }
    let base = String::from_utf8(merge_base.stdout)?;
    changed_paths_from_base(repo_root, base.trim(), "the branch merge base")
}

/// Returns paths changed from an explicit baseline commit to `HEAD`.
fn changed_paths_from_base(
    repo_root: &Path,
    base: &str,
    label: &str,
) -> Result<Vec<String>, Error> {
    let output = Command::new("git")
        .args(["diff", "--name-only", base.trim(), "HEAD"])
        .current_dir(repo_root)
        .output()?;
    if !output.status.success() {
        return Err(anyhow!("git diff from {label} to HEAD failed"));
    }
    Ok(String::from_utf8(output.stdout)?
        .lines()
        .map(std::string::ToString::to_string)
        .collect())
}

/// Returns paths staged in the Git index at the explicit repository root.
fn staged_paths(repo_root: &Path) -> Result<Vec<String>, Error> {
    let output = Command::new("git")
        .args(["diff", "--cached", "--name-only"])
        .current_dir(repo_root)
        .env("GIT_DIR", repo_root.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", repo_root)
        .output()?;
    if !output.status.success() {
        return Err(anyhow!("git diff --cached --name-only failed"));
    }
    Ok(String::from_utf8(output.stdout)?
        .lines()
        .map(std::string::ToString::to_string)
        .collect())
}

/// Returns paths tracked by Git at the repository root.
///
/// # Errors
///
/// Returns an error when Git cannot list tracked paths or its output is not UTF-8.
fn tracked_paths(repo_root: &Path) -> Result<Vec<String>, Error> {
    let output = Command::new("git")
        .args(["ls-files"])
        .current_dir(repo_root)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .output()?;
    if !output.status.success() {
        return Err(anyhow!("git ls-files failed"));
    }
    Ok(String::from_utf8(output.stdout)?
        .lines()
        .map(std::string::ToString::to_string)
        .collect())
}

/// Returns modified and untracked worktree paths for mutation output detection.
///
/// # Errors
///
/// Returns an error when Git cannot list either path set.
fn worktree_changed_paths(repo_root: &Path) -> Result<BTreeSet<String>, Error> {
    let modified = git_path_set(repo_root, &["diff", "--name-only"])?;
    let untracked = git_path_set(repo_root, &["ls-files", "--others", "--exclude-standard"])?;
    Ok(modified.union(&untracked).cloned().collect())
}

/// Stages files newly changed by a successful mutation gate.
///
/// Returns the post-mutation worktree snapshot (`changed_after`, with this
/// gate's own just-staged outputs removed) so the caller can thread it
/// forward as the next restaging gate's `changed_before` baseline without a
/// redundant rescan.
///
/// The returned snapshot deliberately excludes `outputs`: `changed_after` is
/// captured *before* the `git add` below runs, so a raw pass-through would
/// leave this gate's now-staged-and-clean paths sitting in the cache. A later
/// gate that re-touches one of those same paths would then have its own
/// re-mutation silently absorbed into the inherited baseline and never
/// staged — the cached baseline would disagree with what a fresh rescan
/// would report at that point, even though the whole point of the cache is
/// to stand in for one. Removing `outputs` here keeps the threaded snapshot
/// equivalent to a fresh rescan while still saving the rescan itself.
///
/// # Errors
///
/// Returns an error when Git cannot inspect or stage mutation outputs.
fn restage_mutation_outputs(
    repo_root: &Path,
    changed_before: &BTreeSet<String>,
) -> Result<BTreeSet<String>, Error> {
    let changed_after = worktree_changed_paths(repo_root)?;
    let outputs = mutation_output_delta(changed_before, &changed_after);
    if outputs.is_empty() {
        return Ok(changed_after);
    }
    let status = Command::new("git")
        .arg("add")
        .arg("--")
        .args(&outputs)
        .current_dir(repo_root)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .status()?;
    if !status.success() {
        return Err(anyhow!("git add mutation outputs failed"));
    }
    let mut threaded_snapshot = changed_after;
    for output in &outputs {
        threaded_snapshot.remove(output);
    }
    Ok(threaded_snapshot)
}

/// Returns paths introduced into the worktree after a mutation gate runs.
fn mutation_output_delta(
    changed_before: &BTreeSet<String>,
    changed_after: &BTreeSet<String>,
) -> Vec<String> {
    changed_after.difference(changed_before).cloned().collect()
}

/// Runs Git and parses its line-oriented path output into a set.
///
/// # Errors
///
/// Returns an error when Git fails or writes non-UTF-8 output.
fn git_path_set(repo_root: &Path, args: &[&str]) -> Result<BTreeSet<String>, Error> {
    let output = Command::new("git")
        .args(args)
        .current_dir(repo_root)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .output()?;
    if !output.status.success() {
        return Err(anyhow!("git {args:?} failed"));
    }
    Ok(String::from_utf8(output.stdout)?
        .lines()
        .map(std::string::ToString::to_string)
        .collect())
}

/// Returns whether any changed path is equal to or under a configured trigger.
fn trigger_matches(paths: &[String], triggers: &[String]) -> bool {
    paths.iter().any(|path| {
        triggers.iter().any(|trigger| {
            let directory = trigger.trim_end_matches('/');
            path == directory || path.starts_with(trigger)
        })
    })
}

/// Parses a command-line surface name into its registry variant.
///
/// # Errors
///
/// Returns an error when the surface name is not supported by the registry.
fn parse_surface(surface: &str) -> Result<GateSurface, Error> {
    match surface {
        "commit-msg" => Ok(GateSurface::CommitMsg),
        "pre-commit" => Ok(GateSurface::PreCommit),
        "pre-push" => Ok(GateSurface::PrePush),
        "ci" => Ok(GateSurface::Ci),
        _ => Err(anyhow!("unknown gate surface {surface:?}")),
    }
}

#[cfg(test)]
fn fixture_git_command(repo_root: &Path) -> Command {
    if repo_root.join(".git").exists() {
        let output = Command::new("git")
            .args(["rev-parse", "--show-toplevel"])
            .current_dir(repo_root)
            .env("GIT_DIR", repo_root.join(".git"))
            .env("GIT_CEILING_DIRECTORIES", repo_root)
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null")
            .output()
            .expect("fixture escape guard must start git");
        assert!(
            output.status.success(),
            "fixture escape guard must find its repository"
        );
        assert_eq!(
            std::fs::canonicalize(String::from_utf8_lossy(&output.stdout).trim())
                .expect("fixture escape guard must return a canonical repository root"),
            std::fs::canonicalize(repo_root)
                .expect("fixture repository root must be canonicalizable"),
            "fixture escape guard must refuse a Git command outside its temporary repository"
        );
    }
    let mut command = Command::new("git");
    command
        .current_dir(repo_root)
        .env("GIT_DIR", repo_root.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", repo_root)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null");
    command
}

/// Binds the Gherkin scenario "A failing gate inside a group is named in the
/// output"
/// (specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature).
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn failing_gate_inside_a_group_is_named_in_the_output() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: group-first\n",
            "    type: check\n",
            "    command: true\n",
            "    kind: external\n",
            "    ci-group: sample-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
            "  - id: group-failing\n",
            "    type: check\n",
            "    command: false\n",
            "    kind: external\n",
            "    ci-group: sample-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
            "  - id: group-third\n",
            "    type: check\n",
            "    command: true\n",
            "    kind: external\n",
            "    ci-group: sample-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
            "  - id: other-group-gate\n",
            "    type: check\n",
            "    command: touch must-not-run.txt\n",
            "    kind: external\n",
            "    ci-group: other-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root_with_group(repo.path(), "ci", "sample-group", &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains("group-first")
            && rendered.contains("group-failing")
            && rendered.contains("group-third")
            && rendered
                .lines()
                .any(|line| line.contains("group-failing") && line.contains("FAIL")),
        "a failing gate inside a group must be named on a FAIL line, alongside every other \
         gate in the group; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
    assert!(
        !repo.path().join("must-not-run.txt").exists(),
        "a gate outside the selected group must not run"
    );
}

/// Binds the Gherkin scenario "A hand-wired gate never runs a second time
/// inside its CI group"
/// (specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature).
///
/// A hand-wired gate (`wiring: hand-wired`) is dispatched by its own
/// dedicated CI workflow job, never by `gate run --group`. Before this fix,
/// `--group` execution ran every gate whose `ci_group` matched, including
/// hand-wired ones — silently redundant (and harmless) whenever the
/// hand-wired gate's underlying command happened to succeed in the matrix
/// job's environment, but a real failure once that environment stopped
/// matching the hand-wired gate's dedicated job (e.g. missing `node_modules`
/// for an `nx`-kind hand-wired gate once a CI-group job skips `npm ci`).
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn hand_wired_gate_never_reruns_inside_its_ci_group() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: auto-dispatched\n",
            "    type: check\n",
            "    command: true\n",
            "    kind: external\n",
            "    ci-group: sample-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
            "  - id: hand-wired-gate\n",
            "    type: check\n",
            "    command: false\n",
            "    kind: external\n",
            "    wiring: hand-wired\n",
            "    ci-group: sample-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root_with_group(repo.path(), "ci", "sample-group", &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_ok(),
        "a group containing only an auto-dispatched gate (after excluding the hand-wired one) \
         must succeed: {rendered}"
    );
    assert!(
        rendered.contains("auto-dispatched") && !rendered.contains("hand-wired-gate"),
        "the hand-wired gate must never appear in the group's summary — it is dispatched by its \
         own dedicated CI job, not by --group: {rendered}"
    );
}

/// Binds the Gherkin scenario "An unknown group id fails before execution"
/// (specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-execution.feature).
///
/// Mirrors `--only`'s "Unknown or duplicate only ids fail before execution"
/// coverage for the sibling `--group` selector: `resolve_group_gates`'s
/// "no matching gates" `Err` path (LOG5) previously had zero test coverage.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn unknown_group_id_fails_before_execution() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: group-member\n",
            "    type: check\n",
            "    command: touch must-not-run.txt\n",
            "    kind: external\n",
            "    ci-group: real-group\n",
            "    surfaces:\n",
            "      ci: { scope: other }\n",
        ),
    )
    .unwrap();

    let error = run_at_root_with_group(repo.path(), "ci", "unregistered-group", &mut Vec::new())
        .unwrap_err()
        .to_string();

    assert!(
        error.contains("unregistered-group"),
        "an unknown --group id must fail before any leaf invocation and name the offending id; \
         error={error:?}"
    );
    assert!(
        !repo.path().join("must-not-run.txt").exists(),
        "no gate must run when the selected group id matches nothing"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn declaration_order() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: first\n",
            "    type: check\n",
            "    command: printf 'first\\n' >> execution-order.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
            "  - id: second\n",
            "    type: check\n",
            "    command: printf 'second\\n' >> execution-order.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
        ),
    )
    .unwrap();

    run_at_root(repo.path(), "pre-push", &mut Vec::new())
        .expect("gate run must execute declared gates in declaration order");
    assert_eq!(
        std::fs::read_to_string(repo.path().join("execution-order.txt")).unwrap(),
        "first\nsecond\n"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn external_leaf_forwards_derived_paths_as_literal_shell_arguments() {
    let repo = tempfile::TempDir::new().unwrap();
    let path = "derived path; touch must-not-run.txt".to_string();

    let status = run_external_leaf(
        "printf '%s\\n' > received-files.txt",
        &[],
        std::slice::from_ref(&path),
        None,
        repo.path(),
    )
    .expect("external shell command must start");

    assert!(status.success());
    assert_eq!(
        std::fs::read_to_string(repo.path().join("received-files.txt")).unwrap(),
        format!("{path}\n")
    );
    assert!(!repo.path().join("must-not-run.txt").exists());
}

#[cfg(unix)]
#[test]
#[allow(clippy::unwrap_used, clippy::panic)]
fn external_leaf_resolves_repository_local_node_binary() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().unwrap();
    let bin = repo.path().join("node_modules/.bin");
    std::fs::create_dir_all(&bin).unwrap();
    let executable = bin.join("p2-local-external-gate");
    std::fs::write(
        &executable,
        "#!/usr/bin/env sh\nprintf 'local tool\\n' > local-tool-output.txt\n",
    )
    .unwrap();
    let mut permissions = std::fs::metadata(&executable).unwrap().permissions();
    permissions.set_mode(0o755);
    std::fs::set_permissions(&executable, permissions).unwrap();

    let status = run_external_leaf("p2-local-external-gate", &[], &[], None, repo.path())
        .expect("repository-local external gate must start");

    assert!(status.success());
    assert_eq!(
        std::fs::read_to_string(repo.path().join("local-tool-output.txt")).unwrap(),
        "local tool\n"
    );
}

#[test]
#[allow(clippy::unwrap_used, clippy::panic)]
fn external_command_path_precedes_inherited_path() {
    let repo = tempfile::TempDir::new().unwrap();
    let inherited_path = std::ffi::OsStr::new("/usr/bin:/bin");
    let path = external_command_path(repo.path(), Some(inherited_path)).unwrap();
    let paths = std::env::split_paths(&path).collect::<Vec<_>>();
    assert_eq!(paths.first(), Some(&repo.path().join("node_modules/.bin")));
    assert_eq!(paths.get(1), Some(&std::path::PathBuf::from("/usr/bin")));
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn commit_message_file_is_forwarded_to_external_gate() {
    let repo = tempfile::TempDir::new().unwrap();
    let message = repo.path().join("message.txt");
    std::fs::write(&message, "feat: fixture\n").unwrap();

    let status = run_external_leaf(
        "printf '%s\\n' \"$1\" > received-message-file.txt",
        &[],
        &[],
        Some(&message),
        repo.path(),
    )
    .expect("commit-msg external gate must start");

    assert!(status.success());
    assert_eq!(
        std::fs::read_to_string(repo.path().join("received-message-file.txt")).unwrap(),
        format!("{}\n", message.display())
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn stop_at_first_failure() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: failing-first\n",
            "    type: check\n",
            "    command: false\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
            "  - id: must-not-run\n",
            "    type: check\n",
            "    command: printf second > should-not-run.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
        ),
    )
    .unwrap();
    let result = run_at_root(repo.path(), "pre-push", &mut Vec::new());
    let second_ran = repo.path().join("should-not-run.txt").exists();
    assert!(
        result.is_err() && !second_ran,
        "a failing first gate must fail the run and prevent the second gate; result_ok={}, second_ran={second_ran}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn invalid_registry_glob_blocks_dispatch_before_a_leaf_runs() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: malformed-glob\n",
            "    type: check\n",
            "    command: touch must-not-run.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-file-type, glob: '[' }\n",
        ),
    )
    .unwrap();
    std::fs::write(repo.path().join("candidate.md"), "fixture\n").unwrap();
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .status()
            .unwrap()
            .success(),
        "initialize fixture repository"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "candidate.md"])
            .status()
            .unwrap()
            .success(),
        "stage fixture candidate"
    );

    let result = run_at_root(repo.path(), "pre-push", &mut Vec::new());

    assert!(
        result.is_err(),
        "a malformed registry glob must reject dispatch"
    );
    assert!(
        !repo.path().join("must-not-run.txt").exists(),
        "semantic validation must run before a malformed registry can invoke a leaf"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn repository_wide_all_file_type_gate_without_glob_receives_no_paths() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("capture.sh"),
        "#!/bin/sh\nprintf '%s' \"$*\" > argv.txt\n",
    )
    .unwrap();
    std::fs::write(repo.path().join("tracked.md"), "fixture\n").unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: repo-wide\n",
            "    type: check\n",
            "    command: sh capture.sh\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: all-file-type }\n",
        ),
    )
    .unwrap();
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .status()
            .unwrap()
            .success(),
        "initialize fixture repository"
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "capture.sh", "tracked.md", "repo-config.yml"])
            .status()
            .unwrap()
            .success(),
        "stage fixture files"
    );

    run_at_root(repo.path(), "pre-push", &mut Vec::new()).expect("repository-wide gate must run");

    assert_eq!(
        std::fs::read_to_string(repo.path().join("argv.txt")).unwrap(),
        "",
        "an all-file-type gate without a glob must retain its no-argument repository-wide mode"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn path_gated_skip() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::create_dir_all(repo.path().join("docs")).unwrap();
    std::fs::write(repo.path().join("docs/untouched.md"), "unrelated change\n").unwrap();
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .status()
            .unwrap()
            .success()
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", "docs/untouched.md"])
            .status()
            .unwrap()
            .success()
    );
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: path-gated-check\n",
            "    type: check\n",
            "    command: touch should-not-run.txt; false\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: path-gated\n",
            "        trigger:\n",
            "          - .claude/\n",
        ),
    )
    .unwrap();

    let result = run_at_root(repo.path(), "pre-commit", &mut Vec::new());
    let executed = repo.path().join("should-not-run.txt").exists();
    assert!(
        result.is_ok() && !executed,
        "a path-gated gate with no trigger intersection must be skipped; result_ok={}, executed={executed}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn path_gated_run() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::create_dir_all(repo.path().join(".claude/agents")).unwrap();
    std::fs::write(
        repo.path().join(".claude/agents/example.md"),
        "changed agent\n",
    )
    .unwrap();
    assert!(
        fixture_git_command(repo.path())
            .args(["init", "--quiet"])
            .status()
            .unwrap()
            .success()
    );
    assert!(
        fixture_git_command(repo.path())
            .args(["add", ".claude/agents/example.md"])
            .status()
            .unwrap()
            .success()
    );
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: path-gated-check\n",
            "    type: check\n",
            "    command: touch was-run.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push:\n",
            "        scope: path-gated\n",
            "        trigger:\n",
            "          - .claude/\n",
        ),
    )
    .unwrap();

    let result = run_at_root(repo.path(), "pre-push", &mut Vec::new());
    let executed = repo.path().join("was-run.txt").exists();
    assert!(
        result.is_ok() && executed,
        "a path-gated gate must run when a trigger path changes; result_ok={}, executed={executed}",
        result.is_ok()
    );
}

/// A deleted file can never satisfy a `check`/`mutation` gate (e.g.
/// `rustfmt --check`) because the path no longer exists on disk. This test
/// covers the `ci`-surface path, which resolves candidates via
/// `merge_base_paths` -> `changed_paths_from_base`. `retain_existing_paths`
/// filters both this and the `pre-commit`-surface `staged_paths` path (see
/// `affected_file_type_scope_excludes_deleted_paths_from_staged_diff` below)
/// at their sole shared consumption point — the `StagedFiles` arm in
/// `run_at_root_with_only_and_message_file` — rather than in the diff
/// commands themselves, so `path-gated` gates (which read `changed_paths`
/// directly) still see deletions; see `path_gated_run_survives_deleted_trigger_path`.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn affected_file_type_scope_excludes_deleted_paths_from_merge_base_diff() {
    let repo = tempfile::TempDir::new().unwrap();

    let git = |args: &[&str]| {
        let status = fixture_git_command(repo.path())
            .args(args)
            .env("GIT_AUTHOR_NAME", "Rhino CLI Test")
            .env("GIT_AUTHOR_EMAIL", "rhino-cli-test@example.invalid")
            .env("GIT_COMMITTER_NAME", "Rhino CLI Test")
            .env("GIT_COMMITTER_EMAIL", "rhino-cli-test@example.invalid")
            .status()
            .unwrap();
        assert!(status.success(), "git {args:?} must succeed");
    };

    git(&["init", "--quiet"]);
    std::fs::write(repo.path().join("kept.rs"), "fn kept() {}\n").unwrap();
    std::fs::write(repo.path().join("deleted.rs"), "fn deleted() {}\n").unwrap();
    std::fs::write(
        repo.path().join("capture.sh"),
        "#!/bin/sh\nprintf '%s\\n' \"$@\" >> argv.txt\n",
    )
    .unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: capture-affected-rs\n",
            "    type: check\n",
            "    command: sh capture.sh\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      ci: { scope: affected-file-type, glob: '*.rs' }\n",
        ),
    )
    .unwrap();
    git(&["add", "."]);
    git(&["commit", "--quiet", "-m", "base"]);
    // `merge_base_paths` diffs against a ref literally named `origin/main`; a
    // local branch by that name stands in for a real remote-tracking ref.
    git(&["branch", "origin/main"]);

    std::fs::write(repo.path().join("kept.rs"), "fn kept() { /* changed */ }\n").unwrap();
    std::fs::remove_file(repo.path().join("deleted.rs")).unwrap();
    git(&["add", "-A"]);
    git(&[
        "commit",
        "--quiet",
        "-m",
        "delete one .rs file, modify another",
    ]);

    run_at_root(repo.path(), "ci", &mut Vec::new()).expect(
        "a gate whose affected-file-type candidates include a deleted path must not fail — the \
         deleted path must never reach the gate command",
    );

    let argv = std::fs::read_to_string(repo.path().join("argv.txt")).unwrap();
    assert!(
        argv.contains("kept.rs"),
        "the modified file must still be an affected-file-type candidate: {argv:?}"
    );
    assert!(
        !argv.contains("deleted.rs"),
        "a deleted file must never be passed to a gate command — it cannot be linted, \
         formatted, or checked because it no longer exists: {argv:?}"
    );
}

/// Regression: `GATE_CHANGED_BASE` is a workflow-level environment variable, so it is visible to
/// every process in the job -- including `cargo test`, whose in-process fixtures build throwaway
/// repositories that have never heard of the outer repository's commits. Before `commit_resolves`
/// guarded the lookup, `changed_paths` took the explicit-base branch, `git diff <foreign-sha> HEAD`
/// failed inside the fixture, and
/// `affected_file_type_scope_excludes_deleted_paths_from_merge_base_diff` panicked in CI while
/// passing on every developer machine. The same shape is real in production: `github.event.before`
/// is all-zeroes on branch creation and unreachable after a force-push.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn an_unresolvable_changed_base_is_ignored_rather_than_failing_the_gate() {
    let repo = tempfile::TempDir::new().unwrap();
    let git = |args: &[&str]| {
        let status = fixture_git_command(repo.path())
            .args(args)
            .env("GIT_AUTHOR_NAME", "Rhino CLI Test")
            .env("GIT_AUTHOR_EMAIL", "rhino-cli-test@example.invalid")
            .env("GIT_COMMITTER_NAME", "Rhino CLI Test")
            .env("GIT_COMMITTER_EMAIL", "rhino-cli-test@example.invalid")
            .status()
            .unwrap();
        assert!(status.success(), "git {args:?} failed");
    };
    git(&["init", "--quiet", "--initial-branch=main", "."]);
    std::fs::write(repo.path().join("kept.rs"), "fn kept() {}\n").unwrap();
    git(&["add", "."]);
    git(&["commit", "--quiet", "-m", "base"]);

    assert!(
        commit_resolves(repo.path(), "HEAD"),
        "a commit this repository holds must resolve"
    );
    assert!(
        !commit_resolves(repo.path(), "0000000000000000000000000000000000000000"),
        "the all-zeroes sha GitHub sends on branch creation must not resolve"
    );
    assert!(
        !commit_resolves(repo.path(), "8632122e4bcd0000000000000000000000000000"),
        "a sha from an unrelated repository must not resolve, so the caller falls back to the \
         merge base instead of failing every gate"
    );
}

/// Same defect as
/// `affected_file_type_scope_excludes_deleted_paths_from_merge_base_diff`,
/// exercised via `staged_paths` on the `pre-commit` surface instead of
/// `changed_paths_from_base` on `ci` — a real `pre-commit: { scope:
/// affected-file-type }` gate (e.g. `rustfmt`) reads staged paths directly
/// and must never receive a staged deletion.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn affected_file_type_scope_excludes_deleted_paths_from_staged_diff() {
    let repo = tempfile::TempDir::new().unwrap();

    let git = |args: &[&str]| {
        let status = fixture_git_command(repo.path())
            .args(args)
            .env("GIT_AUTHOR_NAME", "Rhino CLI Test")
            .env("GIT_AUTHOR_EMAIL", "rhino-cli-test@example.invalid")
            .env("GIT_COMMITTER_NAME", "Rhino CLI Test")
            .env("GIT_COMMITTER_EMAIL", "rhino-cli-test@example.invalid")
            .status()
            .unwrap();
        assert!(status.success(), "git {args:?} must succeed");
    };

    git(&["init", "--quiet"]);
    std::fs::write(repo.path().join("kept.rs"), "fn kept() {}\n").unwrap();
    std::fs::write(repo.path().join("deleted.rs"), "fn deleted() {}\n").unwrap();
    std::fs::write(
        repo.path().join("capture.sh"),
        "#!/bin/sh\nprintf '%s\\n' \"$@\" >> argv.txt\n",
    )
    .unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: capture-affected-rs\n",
            "    type: mutation\n",
            "    command: sh capture.sh\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.rs' }\n",
        ),
    )
    .unwrap();
    git(&["add", "."]);
    git(&["commit", "--quiet", "-m", "base"]);

    std::fs::write(repo.path().join("kept.rs"), "fn kept() { /* changed */ }\n").unwrap();
    std::fs::remove_file(repo.path().join("deleted.rs")).unwrap();
    git(&["add", "-A"]);

    run_at_root(repo.path(), "pre-commit", &mut Vec::new()).expect(
        "a gate whose affected-file-type candidates include a staged deletion must not fail — \
         the deleted path must never reach the gate command",
    );

    let argv = std::fs::read_to_string(repo.path().join("argv.txt")).unwrap();
    assert!(
        argv.contains("kept.rs"),
        "the modified file must still be an affected-file-type candidate: {argv:?}"
    );
    assert!(
        !argv.contains("deleted.rs"),
        "a staged deletion must never be passed to a gate command — it cannot be linted, \
         formatted, or checked because it no longer exists: {argv:?}"
    );
}

/// Falsifies Architecture cycle-2 Finding 1 against `b555d320b`: filtering
/// deleted paths must happen only at the `StagedFiles` consumption point, not
/// at the shared `changed_paths` source — otherwise a `path-gated` gate
/// (which reads `changed_paths` directly via `trigger_matches`, bypassing
/// `retain_existing_paths` entirely) would stop firing on a delete-only
/// change under its trigger directory. This mirrors `path_gated_run` but
/// deletes the triggering path instead of adding it.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn path_gated_run_survives_deleted_trigger_path() {
    let repo = tempfile::TempDir::new().unwrap();

    let git = |args: &[&str]| {
        let status = fixture_git_command(repo.path())
            .args(args)
            .env("GIT_AUTHOR_NAME", "Rhino CLI Test")
            .env("GIT_AUTHOR_EMAIL", "rhino-cli-test@example.invalid")
            .env("GIT_COMMITTER_NAME", "Rhino CLI Test")
            .env("GIT_COMMITTER_EMAIL", "rhino-cli-test@example.invalid")
            .status()
            .unwrap();
        assert!(status.success(), "git {args:?} must succeed");
    };

    git(&["init", "--quiet"]);
    std::fs::create_dir_all(repo.path().join(".claude/agents")).unwrap();
    std::fs::write(repo.path().join(".claude/agents/example.md"), "an agent\n").unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: path-gated-check\n",
            "    type: check\n",
            "    command: touch was-run.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push:\n",
            "        scope: path-gated\n",
            "        trigger:\n",
            "          - .claude/\n",
        ),
    )
    .unwrap();
    git(&["add", "."]);
    git(&["commit", "--quiet", "-m", "base"]);
    // `merge_base_paths` diffs against a ref literally named `origin/main`; a
    // local branch by that name stands in for a real remote-tracking ref.
    git(&["branch", "origin/main"]);

    std::fs::remove_file(repo.path().join(".claude/agents/example.md")).unwrap();
    git(&["add", "-A"]);
    git(&[
        "commit",
        "--quiet",
        "-m",
        "delete the triggering agent file",
    ]);

    let result = run_at_root(repo.path(), "pre-push", &mut Vec::new());
    let executed = repo.path().join("was-run.txt").exists();
    assert!(
        result.is_ok() && executed,
        "a path-gated gate must still run when the ONLY change under its trigger directory is a \
         deletion — deletion-exclusion for check/mutation gates must not blind trigger \
         detection; result_ok={}, executed={executed}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn linked_worktree_uses_its_own_repo_config() {
    let _cwd = crate::test_support::CwdLock::acquire();
    let fixture = tempfile::TempDir::new().unwrap();
    let main = fixture.path().join("main");
    let worktree = fixture.path().join("linked-worktree");
    std::fs::create_dir(&main).unwrap();

    let git = |args: &[&str]| {
        let status = fixture_git_command(&main)
            .args(args)
            .env("GIT_CEILING_DIRECTORIES", &main)
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null")
            .env("GIT_AUTHOR_NAME", "Rhino CLI Test")
            .env("GIT_AUTHOR_EMAIL", "rhino-cli-test@example.invalid")
            .env("GIT_COMMITTER_NAME", "Rhino CLI Test")
            .env("GIT_COMMITTER_EMAIL", "rhino-cli-test@example.invalid")
            .status()
            .unwrap();
        assert!(status.success(), "git {args:?} must succeed");
    };

    git(&["init", "--quiet"]);
    std::fs::write(main.join("README.md"), "fixture\n").unwrap();
    std::fs::write(main.join("repo-config.yml"), "gates: []\n").unwrap();
    git(&["add", "."]);
    git(&["commit", "--quiet", "-m", "fixture"]);
    git(&[
        "worktree",
        "add",
        "--quiet",
        worktree.to_str().unwrap(),
        "HEAD",
    ]);
    std::fs::write(
        worktree.join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: worktree-gate\n",
            "    type: check\n",
            "    command: touch worktree-config-was-used.txt\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
        ),
    )
    .unwrap();

    std::env::set_current_dir(&worktree).unwrap();
    run(
        &RunArgs {
            surface: "pre-push".to_string(),
            only: None,
            group: None,
            commit_message_file: None,
        },
        OutputFormat::Text,
    )
    .expect("gate run must resolve repo-config.yml from the linked worktree");
    assert!(worktree.join("worktree-config-was-used.txt").exists());
    assert!(!main.join("worktree-config-was-used.txt").exists());
}
