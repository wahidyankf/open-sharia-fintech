//! `gate run` command adapter.

use std::io::Write;
use std::path::Path;
use std::process::Command;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::git::port::StagedFileProvider;
use crate::application::repo_config::{self, GateSurface, ScopeKind};
use crate::domain::cliout::OutputFormat;
use crate::infrastructure::git::staged_files::GitStagedFileProvider;
use crate::internal::git;

/// Arguments for `gate run`.
#[derive(Args, Debug)]
pub struct RunArgs {
    /// Surface whose declared gates to run.
    #[arg(long)]
    pub surface: String,
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
    run_at_root(&repo_root, &args.surface, &mut std::io::stdout())
}

/// Run gates declared on a surface at a known repository root.
///
/// # Errors
///
/// Returns an error when the surface is invalid, `repo-config.yml` cannot be
/// read, or a declared command cannot be started.
pub fn run_at_root(repo_root: &Path, surface: &str, writer: &mut dyn Write) -> Result<(), Error> {
    let surface = parse_surface(surface)?;
    let config = repo_config::load(repo_root)?;
    let changed_paths = config
        .gates
        .iter()
        .filter_map(|gate| gate.surfaces.get(&surface))
        .any(|scope| scope.scope == ScopeKind::PathGated)
        .then(|| changed_paths(repo_root, &surface))
        .transpose()?;
    for gate in config
        .gates
        .iter()
        .filter(|gate| gate.surfaces.contains_key(&surface))
    {
        let scope = &gate.surfaces[&surface];
        if scope.scope == ScopeKind::PathGated
            && !changed_paths
                .as_deref()
                .is_some_and(|paths| trigger_matches(paths, &scope.trigger))
        {
            continue;
        }
        writeln!(writer, "Running gate {}", gate.id)?;
        let status = Command::new("sh")
            .args(["-c", &gate.command])
            .current_dir(repo_root)
            .status()?;
        if !status.success() {
            return Err(anyhow!("gate {} failed", gate.id));
        }
    }
    Ok(())
}

fn changed_paths(repo_root: &Path, _surface: &GateSurface) -> Result<Vec<String>, Error> {
    GitStagedFileProvider.get_staged(repo_root)
}

fn trigger_matches(paths: &[String], triggers: &[String]) -> bool {
    paths.iter().any(|path| {
        triggers.iter().any(|trigger| {
            let directory = trigger.trim_end_matches('/');
            path == directory || path.starts_with(trigger)
        })
    })
}

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
fn path_gated_skip() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::create_dir_all(repo.path().join("docs")).unwrap();
    std::fs::write(repo.path().join("docs/untouched.md"), "unrelated change\n").unwrap();
    assert!(
        Command::new("git")
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );
    assert!(
        Command::new("git")
            .args(["add", "docs/untouched.md"])
            .current_dir(repo.path())
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
        Command::new("git")
            .args(["init", "--quiet"])
            .current_dir(repo.path())
            .status()
            .unwrap()
            .success()
    );
    assert!(
        Command::new("git")
            .args(["add", ".claude/agents/example.md"])
            .current_dir(repo.path())
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
        let status = Command::new("git")
            .args(args)
            .current_dir(&main)
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
        },
        OutputFormat::Text,
    )
    .expect("gate run must resolve repo-config.yml from the linked worktree");
    assert!(worktree.join("worktree-config-was-used.txt").exists());
    assert!(!main.join("worktree-config-was-used.txt").exists());
}
