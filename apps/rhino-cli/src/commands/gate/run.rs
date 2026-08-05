//! `gate run` command adapter.

use std::collections::BTreeSet;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::Command;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::repo_config::{self, GateKind, GateSurface, GateType, ScopeKind};
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
    run_at_root_with_only_and_message_file(repo_root, surface, only, None, writer)
}

/// Run gates declared on a surface, optionally selecting one gate and forwarding a commit message.
fn run_at_root_with_only_and_message_file(
    repo_root: &Path,
    surface: &str,
    only: Option<&str>,
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
    validate_registry_semantics(&config, writer)?;
    let selected_gates = surface_gates
        .into_iter()
        .filter(|gate| only.is_none_or(|id| gate.id == id))
        .collect::<Vec<_>>();
    let (changed_paths, tracked_paths) = candidate_paths(repo_root, &selected_gates, &surface)?;
    let mut batch_ran = false;
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
            CandidateScope::StagedFiles => matching_files(
                changed_paths.as_deref().unwrap_or_default(),
                scope,
                excludes,
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
            writeln!(writer, "Running lint-staged batch")?;
            let status = Command::new("npx")
                .args(["--no", "--", "lint-staged"])
                .current_dir(repo_root)
                .status()?;
            if !status.success() {
                return Err(anyhow!("lint-staged batch failed"));
            }
            batch_ran = true;
            continue;
        }
        writeln!(writer, "Running gate {}", gate.id)?;
        let changed_before = gate
            .restages
            .then(|| worktree_changed_paths(repo_root))
            .transpose()?;
        let status = run_leaf(
            &gate.kind,
            &gate.command,
            &repo_config::fixed_arguments(gate),
            &files,
            &scope.scope,
            commit_message_file,
            repo_root,
        )?;
        if !status.success() {
            return Err(anyhow!("gate {} failed", gate.id));
        }
        if let Some(changed_before) = changed_before {
            restage_mutation_outputs(repo_root, &changed_before)?;
        }
    }
    Ok(())
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
        _ => vec!["exec", "nx", "--", "affected", "-t", target],
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
    {
        return changed_paths_from_base(repo_root, base.trim(), GATE_CHANGED_BASE_ENV);
    }
    if matches!(surface, GateSurface::PrePush | GateSurface::Ci) {
        return merge_base_paths(repo_root);
    }
    Ok(Vec::new())
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
/// # Errors
///
/// Returns an error when Git cannot inspect or stage mutation outputs.
fn restage_mutation_outputs(
    repo_root: &Path,
    changed_before: &BTreeSet<String>,
) -> Result<(), Error> {
    let changed_after = worktree_changed_paths(repo_root)?;
    let outputs = mutation_output_delta(changed_before, &changed_after);
    if outputs.is_empty() {
        return Ok(());
    }
    let status = Command::new("git")
        .arg("add")
        .arg("--")
        .args(outputs)
        .current_dir(repo_root)
        .env_remove("GIT_DIR")
        .env_remove("GIT_WORK_TREE")
        .status()?;
    if !status.success() {
        return Err(anyhow!("git add mutation outputs failed"));
    }
    Ok(())
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
            commit_message_file: None,
        },
        OutputFormat::Text,
    )
    .expect("gate run must resolve repo-config.yml from the linked worktree");
    assert!(worktree.join("worktree-config-was-used.txt").exists());
    assert!(!main.join("worktree-config-was-used.txt").exists());
}
