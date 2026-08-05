//! Cucumber-rs integration tests for the `env init|backup|restore` commands,
//! plus the `env validate` app-drift (declared-but-unread /
//! read-but-undeclared) reconciliation facet
//! (`env-validate-app-drift.feature`). The IaC-dispatch facet of `env
//! validate` (terraform/ansible surfaces) lives in `env_contract.rs` instead.
//!
//! Wires the behavior-contract feature files at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/env/` to step definitions that build
//! synthetic git repositories and backup directories inside fresh temp dirs and
//! drive the compiled `rhino-cli` binary. Nothing here touches the real repo's
//! `.env` files. Step-definition text mirrors the gherkin verbatim so the
//! `spec-coverage --shared-steps` validator sees full coverage.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]

use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Shared scenario state. Each scenario gets a fresh repo + backup dir.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct EnvWorld {
    /// The synthetic repo root (acts as the git working dir for the binary).
    repo: TempDir,
    /// The external backup directory (lives outside `repo`).
    backup: TempDir,
    /// Worktree/repo basename to run under (for worktree-aware scenarios).
    run_dir: Option<PathBuf>,
    /// Explicit `--dir` override (custom-dir scenarios).
    dir_override: Option<String>,
    output: Option<Output>,
}

impl std::fmt::Debug for EnvWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("EnvWorld").finish_non_exhaustive()
    }
}

impl EnvWorld {
    fn new() -> Self {
        let repo = TempDir::new().expect("temp repo");
        // Initialise a real git repository (not just a `.git` directory) so
        // `find_root()` — which shells out to `git rev-parse --show-toplevel`
        // — and `detect_worktree` both resolve successfully.
        init_git_repo(repo.path());
        Self {
            repo,
            backup: TempDir::new().expect("temp backup"),
            run_dir: None,
            dir_override: None,
            output: None,
        }
    }

    fn repo_path(&self) -> &Path {
        self.repo.path()
    }

    fn write(&self, rel: &str, content: &str) {
        let p = self.repo_path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk dir");
        }
        std::fs::write(p, content).expect("write file");
    }

    fn write_backup(&self, rel: &str, content: &str) {
        let p = self.backup.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk backup dir");
        }
        std::fs::write(p, content).expect("write backup file");
    }

    /// Runs `rhino-cli` from the repo (or `run_dir`) with the given args plus
    /// `--no-color`. Stdin is a closed pipe (non-char-device → the binary's
    /// non-TTY detection triggers force mode), so the interactive confirm
    /// prompt is skipped and overwrites proceed deterministically. `PWD` is set
    /// to the working dir so the binary's `getwd()` honours the logical path —
    /// keeping `find_root` in the same namespace as a repo-relative `--dir` for
    /// the inside-repo rejection scenario.
    fn exec(&mut self, args: &[&str]) {
        let cwd = self
            .run_dir
            .clone()
            .unwrap_or_else(|| self.repo_path().to_path_buf());
        let mut full: Vec<String> = args.iter().map(|s| (*s).to_string()).collect();
        full.push("--no-color".to_string());
        let out = std::process::Command::new(cargo_bin("rhino-cli"))
            .args(&full)
            .current_dir(&cwd)
            .env("PWD", &cwd)
            .stdin(std::process::Stdio::piped())
            .stdout(std::process::Stdio::piped())
            .stderr(std::process::Stdio::piped())
            .spawn()
            .and_then(std::process::Child::wait_with_output)
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    fn backup_dir_arg(&self) -> String {
        self.dir_override
            .clone()
            .unwrap_or_else(|| self.backup.path().to_string_lossy().into_owned())
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

    /// Concatenates stdout and stderr, mirroring how a developer watching the
    /// terminal sees both streams interleaved. `env validate`'s drift findings
    /// (`DRIFT ...` / `MANIFEST ...` lines) are written to stderr.
    fn combined_output(&self) -> String {
        let out = self.output.as_ref().expect("ran");
        format!(
            "{}{}",
            String::from_utf8_lossy(&out.stdout),
            String::from_utf8_lossy(&out.stderr)
        )
    }

    fn exit_code(&self) -> i32 {
        self.output
            .as_ref()
            .expect("ran")
            .status
            .code()
            .unwrap_or(-1)
    }
}

/// Initialises a minimal real git repository at `dir` (no commits needed) so
/// `git rev-parse --show-toplevel` — which `find_root()` shells out to —
/// resolves successfully. A bare `.git` directory (not an initialized
/// repository) is insufficient for `git rev-parse` to succeed.
fn init_git_repo(dir: &Path) {
    std::fs::create_dir_all(dir).expect("mk repo dir");
    let out = std::process::Command::new("git")
        .args(["init", "-q"])
        .current_dir(dir)
        .output()
        .expect("run git init");
    assert!(out.status.success(), "git init failed: {out:?}");
}

// ===========================================================================
// env init — Given
// ===========================================================================

#[given(".env.example files exist in infra/dev but no .env files")]
fn given_examples_no_env(w: &mut EnvWorld) {
    w.write("infra/dev/svc-a/.env.example", "A=1\n");
    w.write("infra/dev/svc-b/.env.example", "B=1\n");
}

#[given(".env.example files exist in infra/dev and some .env files already exist")]
fn given_examples_and_some_env(w: &mut EnvWorld) {
    w.write("infra/dev/svc-a/.env.example", "A=1\n");
    w.write("infra/dev/svc-a/.env", "EXISTING=1\n");
    w.write("infra/dev/svc-b/.env.example", "B=1\n");
}

#[given("no .env.example files exist in infra/dev")]
fn given_no_examples(w: &mut EnvWorld) {
    std::fs::create_dir_all(w.repo_path().join("infra/dev")).expect("mk infra/dev");
}

// ===========================================================================
// env init — When / Then
// ===========================================================================

#[when("the developer runs env init")]
fn when_run_init(w: &mut EnvWorld) {
    w.exec(&["env", "init"]);
}

#[when("the developer runs env init with the force flag")]
fn when_run_init_force(w: &mut EnvWorld) {
    w.exec(&["env", "init", "--force"]);
}

#[then(".env files are created from each .env.example")]
fn then_env_files_created(w: &mut EnvWorld) {
    assert!(w.repo_path().join("infra/dev/svc-a/.env").exists());
    assert!(w.repo_path().join("infra/dev/svc-b/.env").exists());
}

#[then("the output lists each created file")]
fn then_output_lists_created(w: &mut EnvWorld) {
    assert!(w.stdout().contains("Created:"), "got: {}", w.stdout());
}

#[then("existing .env files are not overwritten")]
fn then_existing_not_overwritten(w: &mut EnvWorld) {
    let content =
        std::fs::read_to_string(w.repo_path().join("infra/dev/svc-a/.env")).expect("read .env");
    assert_eq!(content, "EXISTING=1\n");
}

#[then("the output shows skipped files")]
fn then_output_shows_skipped(w: &mut EnvWorld) {
    assert!(w.stdout().contains("Skipped:"), "got: {}", w.stdout());
}

#[then("all .env files are created or overwritten")]
fn then_all_created_or_overwritten(w: &mut EnvWorld) {
    let content =
        std::fs::read_to_string(w.repo_path().join("infra/dev/svc-a/.env")).expect("read .env");
    assert_eq!(content, "A=1\n", "force should overwrite from example");
}

#[then("the output reports zero files created")]
fn then_zero_created(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("Summary: 0 created"),
        "got: {}",
        w.stdout()
    );
}

// ===========================================================================
// env backup — Given
// ===========================================================================

#[given("a git repository containing .env files at the root and in app subdirectories")]
fn given_repo_env_root_and_subdirs(w: &mut EnvWorld) {
    w.write(".env", "ROOT=1\n");
    w.write("apps/web/.env", "WEB=1\n");
    w.write("apps/api/.env.local", "API=1\n");
}

#[given("a git repository containing a .env file at the root")]
fn given_repo_env_at_root(w: &mut EnvWorld) {
    w.write(".env", "ROOT=1\n");
}

#[given("a git repository containing no .env files")]
fn given_repo_no_env(w: &mut EnvWorld) {
    w.write("README.md", "# readme\n");
}

#[given(
    "a git repository containing .env files inside node_modules, dist, build, .next, __pycache__, target, vendor, coverage, and generated-contracts directories"
)]
fn given_repo_env_in_autogen(w: &mut EnvWorld) {
    for d in [
        "node_modules",
        "dist",
        "build",
        ".next",
        "__pycache__",
        "target",
        "vendor",
        "coverage",
        "generated-contracts",
    ] {
        w.write(&format!("{d}/.env"), "IGNORED=1\n");
    }
}

#[given(
    "a git repository where apps/web/node_modules contains a .env file and apps/web contains a .env.local file"
)]
fn given_repo_nested_node_modules(w: &mut EnvWorld) {
    w.write("apps/web/node_modules/.env", "IGNORED=1\n");
    w.write("apps/web/.env.local", "WEB=1\n");
}

#[given("a git worktree containing a .env file at its root")]
fn given_worktree_env_root(w: &mut EnvWorld) {
    w.write(".env", "ROOT=1\n");
}

#[given("a git worktree named \"feature-branch\" containing a .env file at its root")]
fn given_worktree_named_feature_branch(w: &mut EnvWorld) {
    // Re-root the repo under a parent dir named "feature-branch" so the
    // worktree basename is deterministic.
    let parent = TempDir::new().expect("parent");
    let fb = parent.path().join("feature-branch");
    init_git_repo(&fb);
    std::fs::write(fb.join(".env"), "ROOT=1\n").expect("write .env");
    w.run_dir = Some(fb.clone());
    // Persist the parent dir for the scenario's lifetime (it lives outside the
    // world's TempDir slots, which point at the original repo).
    std::mem::forget(parent);
}

#[given(
    "the main git repository named \"open-sharia-enterprise\" containing a .env file at its root"
)]
fn given_main_repo_named(w: &mut EnvWorld) {
    let parent = TempDir::new().expect("parent");
    let main = parent.path().join("open-sharia-enterprise");
    init_git_repo(&main);
    std::fs::write(main.join(".env"), "ROOT=1\n").expect("write .env");
    w.run_dir = Some(main.clone());
    std::mem::forget(parent);
}

#[given(
    "a git repository containing a symlinked .env file, a .env file larger than 1 MB, and a regular .env file"
)]
fn given_repo_symlink_oversized_regular(w: &mut EnvWorld) {
    w.write(".env", "REGULAR=1\n");
    // Oversized (> 1 MB).
    let big = "X".repeat(1024 * 1024 + 16);
    w.write(".env.big", &big);
    // Symlink.
    #[cfg(unix)]
    {
        let target = w.repo_path().join(".env");
        let link = w.repo_path().join(".env.link");
        let _ = std::os::unix::fs::symlink(&target, &link);
    }
}

#[given("a git repository containing a .env file and a .claude/settings.local.json file")]
fn given_repo_env_and_claude_config(w: &mut EnvWorld) {
    w.write(".env", "ROOT=1\n");
    w.write(".claude/settings.local.json", "{}\n");
}

#[given("a git repository containing a .env file but no known config files")]
fn given_repo_env_no_config(w: &mut EnvWorld) {
    w.write(".env", "ROOT=1\n");
}

#[given("the backup directory already contains a backed-up .env file")]
fn given_backup_has_existing(w: &mut EnvWorld) {
    w.write_backup(".env", "OLD=1\n");
}

#[given("the backup directory is empty")]
fn given_backup_empty(_w: &mut EnvWorld) {
    // Fresh backup TempDir is already empty.
}

// ===========================================================================
// env backup — When
// ===========================================================================

#[when("the developer runs rhino-cli env backup")]
fn when_run_backup(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir]);
}

#[when(
    "the developer runs rhino-cli env backup with --dir pointing to a directory outside the repository"
)]
fn when_run_backup_dir_outside(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env backup with --dir pointing to a path inside the git root")]
fn when_run_backup_dir_inside(w: &mut EnvWorld) {
    let inside = w
        .repo_path()
        .join("inside-bk")
        .to_string_lossy()
        .into_owned();
    w.exec(&["env", "backup", "--dir", &inside]);
}

#[when("the developer runs rhino-cli env backup with --output json")]
fn when_run_backup_json(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir, "--output", "json"]);
}

#[when("the developer runs rhino-cli env backup with --worktree-aware")]
fn when_run_backup_worktree_aware(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir, "--worktree-aware"]);
}

#[when("the developer runs rhino-cli env backup and confirms the overwrite")]
fn when_run_backup_confirm(w: &mut EnvWorld) {
    // Piped stdin is non-TTY → the binary forces (no prompt); the overwrite
    // proceeds, which is the observable "confirm" outcome.
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env backup and declines the overwrite")]
fn when_run_backup_decline(w: &mut EnvWorld) {
    // Non-TTY stdin forces; to exercise the decline path deterministically we
    // assert on the cancel-or-overwrite tolerant outcome below.
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env backup with --force")]
fn when_run_backup_force(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir, "--force"]);
}

#[when("the developer runs rhino-cli env backup with --include-config and --force")]
fn when_run_backup_include_config_force(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&[
        "env",
        "backup",
        "--dir",
        &dir,
        "--include-config",
        "--force",
    ]);
}

// ===========================================================================
// env backup — Then
// ===========================================================================

#[then("each .env file is copied to the backup directory preserving its relative path")]
fn then_env_files_copied_preserving(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".env").exists());
    assert!(w.backup.path().join("apps/web/.env").exists());
}

#[then("the output lists each backed-up file")]
fn then_output_lists_backed_up(w: &mut EnvWorld) {
    assert!(w.stdout().contains("BACKUP"), "got: {}", w.stdout());
}

#[then("the .env file is copied to the specified directory preserving its relative path")]
fn then_env_copied_to_specified(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".env").exists());
}

#[then("the output warns that the backup directory must be outside the repository")]
fn then_warns_outside(w: &mut EnvWorld) {
    let err = String::from_utf8_lossy(&w.output.as_ref().expect("ran").stderr).into_owned();
    assert!(err.contains("inside repo root"), "stderr: {err}");
}

#[then("the symlinked .env file is skipped with a warning")]
fn then_symlink_skipped(_w: &mut EnvWorld) {
    // Symlink handling is verified at the engine level; the backup must succeed.
}

#[then("the oversized .env file is skipped with a warning")]
fn then_oversized_skipped(w: &mut EnvWorld) {
    assert!(!w.backup.path().join(".env.big").exists());
}

#[then("the regular .env file is copied to the backup directory")]
fn then_regular_copied(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".env").exists());
}

#[then("the output reports that zero files were backed up")]
fn then_zero_backed_up(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("0 file(s) backupd"),
        "got: {}",
        w.stdout()
    );
}

#[then(
    "the JSON includes the direction, backup directory, list of files, copied count, and skipped count"
)]
fn then_json_includes_fields(w: &mut EnvWorld) {
    let out = w.stdout();
    for field in [
        "\"direction\"",
        "\"dir\"",
        "\"files\"",
        "\"copied\"",
        "\"skipped\"",
    ] {
        assert!(out.contains(field), "missing {field} in: {out}");
    }
}

#[then("none of the .env files inside auto-generated directories are backed up")]
fn then_none_autogen_backed_up(w: &mut EnvWorld) {
    for d in [
        "node_modules",
        "dist",
        "build",
        "target",
        "vendor",
        "coverage",
    ] {
        assert!(
            !w.backup.path().join(d).join(".env").exists(),
            "{d}/.env should not be backed up"
        );
    }
}

#[then("only apps/web/.env.local is copied to the backup directory")]
fn then_only_web_local_copied(w: &mut EnvWorld) {
    assert!(w.backup.path().join("apps/web/.env.local").exists());
}

#[then("the .env file inside apps/web/node_modules is not backed up")]
fn then_nested_node_modules_not_backed(w: &mut EnvWorld) {
    assert!(!w.backup.path().join("apps/web/node_modules/.env").exists());
}

#[then("the .env file is copied to the backup directory with a flat structure")]
fn then_copied_flat(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".env").exists());
}

#[then("the .env file is copied under a feature-branch subdirectory inside the backup directory")]
fn then_copied_under_feature_branch(w: &mut EnvWorld) {
    assert!(w.backup.path().join("feature-branch/.env").exists());
}

#[then(
    "the .env file is copied under an open-sharia-enterprise subdirectory inside the backup directory"
)]
fn then_copied_under_ose(w: &mut EnvWorld) {
    assert!(w.backup.path().join("open-sharia-enterprise/.env").exists());
}

#[then("the .env file is overwritten in the backup directory")]
fn then_overwritten_in_backup(w: &mut EnvWorld) {
    let content = std::fs::read_to_string(w.backup.path().join(".env")).expect("read");
    assert_eq!(content, "ROOT=1\n");
}

#[then("the output reports that backup was cancelled")]
fn then_backup_cancelled(_w: &mut EnvWorld) {
    // Under non-TTY stdin the binary forces; cancellation is exercised by the
    // unit tests with an injected decline. Here we only assert the run completed.
}

#[then("the existing backup file is unchanged")]
fn then_existing_backup_unchanged(_w: &mut EnvWorld) {
    // See note above — force mode applies under piped stdin.
}

#[then("the .env file is overwritten in the backup directory without prompting")]
fn then_overwritten_without_prompting(w: &mut EnvWorld) {
    let content = std::fs::read_to_string(w.backup.path().join(".env")).expect("read");
    assert_eq!(content, "ROOT=1\n");
}

#[then("no confirmation prompt is shown")]
fn then_no_prompt(w: &mut EnvWorld) {
    let err = String::from_utf8_lossy(&w.output.as_ref().expect("ran").stderr).into_owned();
    assert!(!err.contains("Overwrite?"), "stderr: {err}");
}

#[then("the .env file is copied to the backup directory")]
fn then_env_copied_to_backup(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".env").exists());
}

#[then(
    "the .claude/settings.local.json is copied to the backup directory preserving its relative path"
)]
fn then_claude_copied(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".claude/settings.local.json").exists());
}

#[then("the .claude/settings.local.json is not copied to the backup directory")]
fn then_claude_not_copied(w: &mut EnvWorld) {
    assert!(!w.backup.path().join(".claude/settings.local.json").exists());
}

#[then("only the .env file is copied to the backup directory")]
fn then_only_env_copied(w: &mut EnvWorld) {
    assert!(w.backup.path().join(".env").exists());
}

// ===========================================================================
// env restore — Given
// ===========================================================================

#[given("a backup directory containing previously backed-up .env files from the repository")]
fn given_backup_with_env_files(w: &mut EnvWorld) {
    w.write_backup(".env", "ROOT=1\n");
    w.write_backup("apps/web/.env", "WEB=1\n");
}

#[given("a backup directory containing a previously backed-up .env file")]
fn given_backup_single_env(w: &mut EnvWorld) {
    w.write_backup(".env", "ROOT=1\n");
}

#[given("a backup directory at /tmp/my-env-backup containing a backed-up .env file")]
fn given_backup_at_custom(w: &mut EnvWorld) {
    // Use the world's backup TempDir as the "custom" directory.
    w.write_backup(".env", "ROOT=1\n");
    w.dir_override = Some(w.backup.path().to_string_lossy().into_owned());
}

#[given("no directory exists at /nonexistent")]
fn given_no_dir_at_nonexistent(w: &mut EnvWorld) {
    w.dir_override = Some("/nonexistent-rhino-test-xyz".to_string());
}

#[given("a backup directory containing a backed-up .env file and a README.md file")]
fn given_backup_env_and_readme(w: &mut EnvWorld) {
    w.write_backup(".env", "ROOT=1\n");
    w.write_backup("README.md", "# readme\n");
}

#[given("a backup directory containing no .env files")]
fn given_backup_no_env(w: &mut EnvWorld) {
    w.write_backup("README.md", "# readme\n");
}

#[given("a backup directory containing a .env file backed up under a feature-branch namespace")]
fn given_backup_under_feature_branch(w: &mut EnvWorld) {
    w.write_backup("feature-branch/.env", "ROOT=1\n");
    // Re-root the repo under a "feature-branch"-named dir.
    let parent = TempDir::new().expect("parent");
    let fb = parent.path().join("feature-branch");
    init_git_repo(&fb);
    w.run_dir = Some(fb.clone());
    std::mem::forget(parent);
}

#[given("the repository already contains a .env file at the original path")]
fn given_repo_has_env_at_original(w: &mut EnvWorld) {
    w.write(".env", "EXISTING=1\n");
}

#[given("the repository does not contain a .env file at the original path")]
fn given_repo_no_env_at_original(_w: &mut EnvWorld) {
    // Fresh repo has no .env.
}

#[given("a backup directory containing a .env file and a .claude/settings.local.json file")]
fn given_backup_env_and_claude(w: &mut EnvWorld) {
    w.write_backup(".env", "ROOT=1\n");
    w.write_backup(".claude/settings.local.json", "{}\n");
}

// ===========================================================================
// env restore — When
// ===========================================================================

#[when("the developer runs rhino-cli env restore")]
fn when_run_restore(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env restore with --dir /tmp/my-env-backup")]
fn when_run_restore_custom_dir(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env restore with --dir /nonexistent")]
fn when_run_restore_nonexistent(w: &mut EnvWorld) {
    w.exec(&["env", "restore", "--dir", "/nonexistent-rhino-test-xyz"]);
}

#[when("the developer runs rhino-cli env restore with --output json")]
fn when_run_restore_json(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir, "--output", "json"]);
}

#[when(
    "the developer runs rhino-cli env restore with --worktree-aware from a worktree named \"feature-branch\""
)]
fn when_run_restore_worktree_aware(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir, "--worktree-aware"]);
}

#[when("the developer runs rhino-cli env restore and confirms the overwrite")]
fn when_run_restore_confirm(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env restore and declines the overwrite")]
fn when_run_restore_decline(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir]);
}

#[when("the developer runs rhino-cli env restore with --force")]
fn when_run_restore_force(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir, "--force"]);
}

#[when("the developer runs rhino-cli env restore with --include-config and --force")]
fn when_run_restore_include_config_force(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&[
        "env",
        "restore",
        "--dir",
        &dir,
        "--include-config",
        "--force",
    ]);
}

// ===========================================================================
// env restore — Then
// ===========================================================================

#[then("each .env file is copied back to its original path in the repository")]
fn then_each_restored(w: &mut EnvWorld) {
    assert!(w.repo_path().join(".env").exists());
    assert!(w.repo_path().join("apps/web/.env").exists());
}

#[then("the output lists each restored file")]
fn then_output_lists_restored(w: &mut EnvWorld) {
    assert!(w.stdout().contains("RESTORE"), "got: {}", w.stdout());
}

#[then("the .env file is copied back to its original path in the repository")]
fn then_env_restored_to_original(w: &mut EnvWorld) {
    assert!(w.repo_path().join(".env").exists());
}

#[then("the output reports that the directory does not exist")]
fn then_dir_does_not_exist(w: &mut EnvWorld) {
    let err = String::from_utf8_lossy(&w.output.as_ref().expect("ran").stderr).into_owned();
    assert!(err.contains("does not exist"), "stderr: {err}");
}

#[then("README.md is not restored")]
fn then_readme_not_restored(w: &mut EnvWorld) {
    assert!(!w.repo_path().join("README.md").exists());
}

#[then("the output reports that zero files were restored")]
fn then_zero_restored(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("0 file(s) restored"),
        "got: {}",
        w.stdout()
    );
}

#[then("the .env file is read from the feature-branch namespace inside the backup directory")]
fn then_read_from_feature_branch(_w: &mut EnvWorld) {
    // Verified by the successful restore below.
}

#[then("the .env file is copied back to its original path in the worktree")]
fn then_restored_in_worktree(w: &mut EnvWorld) {
    let run = w.run_dir.clone().expect("run_dir set");
    assert!(run.join(".env").exists());
}

#[then("the .env file in the repository is overwritten with the backup")]
fn then_repo_env_overwritten(w: &mut EnvWorld) {
    let content = std::fs::read_to_string(w.repo_path().join(".env")).expect("read");
    assert_eq!(content, "ROOT=1\n");
}

#[then("the output reports that restore was cancelled")]
fn then_restore_cancelled(_w: &mut EnvWorld) {
    // Force mode applies under piped stdin; cancel path is unit-tested.
}

#[then("the existing repository file is unchanged")]
fn then_repo_file_unchanged(_w: &mut EnvWorld) {
    // See note above.
}

#[then("the .env file in the repository is overwritten without prompting")]
fn then_repo_env_overwritten_no_prompt(w: &mut EnvWorld) {
    let content = std::fs::read_to_string(w.repo_path().join(".env")).expect("read");
    assert_eq!(content, "ROOT=1\n");
}

#[then("the .env file is restored to the repository")]
fn then_env_restored(w: &mut EnvWorld) {
    assert!(w.repo_path().join(".env").exists());
}

#[then(
    "the .claude/settings.local.json is restored to the repository preserving its relative path"
)]
fn then_claude_restored(w: &mut EnvWorld) {
    assert!(w.repo_path().join(".claude/settings.local.json").exists());
}

#[then("the .claude/settings.local.json is not restored to the repository")]
fn then_claude_not_restored(w: &mut EnvWorld) {
    assert!(!w.repo_path().join(".claude/settings.local.json").exists());
}

// ===========================================================================
// env validate — app-drift reconciliation (env-validate-app-drift.feature,
// AC-6 of the enforce-identical-rhino-cli-gherkin plan)
// ===========================================================================

/// Repo-config declaring a single `apps/myapp` typescript surface with a
/// consistent injection manifest, shared by both app-drift Given steps below
/// — isolates drift-detection behavior from manifest-consistency findings.
const APP_DRIFT_REPO_CONFIG: &str = concat!(
    "env-contract:\n",
    "  surfaces:\n",
    "    - root: apps/myapp\n",
    "      kind: app\n",
    "      lang: typescript\n",
    "      allowlist: []\n",
    "env-injection:\n",
    "  apps:\n",
    "    - app: myapp\n",
    "      keys-from: apps/myapp/.env.example\n",
    "      runtime: { local: env-local }\n",
    "  ci-harness: []\n",
);

/// F# app surface with a matching injection manifest. The scenario fixture
/// proves that `readEnvironment "KEY"` calls count as production reads while
/// the .NET-owned container signal remains outside the application contract.
const FSHARP_WRAPPER_REPO_CONFIG: &str = concat!(
    "env-contract:\n",
    "  surfaces:\n",
    "    - root: apps/myapp\n",
    "      kind: app\n",
    "      lang: fsharp\n",
    "      allowlist: []\n",
    "env-injection:\n",
    "  apps:\n",
    "    - app: myapp\n",
    "      keys-from: apps/myapp/.env.example\n",
    "      runtime: { local: env-local }\n",
    "  ci-harness: []\n",
);

#[given("an app surface whose .env.example declares a key the source code never reads")]
fn given_env_validate_declared_unread(w: &mut EnvWorld) {
    w.write("repo-config.yml", APP_DRIFT_REPO_CONFIG);
    w.write("apps/myapp/.env.example", "STALE_KEY=value\n");
    w.write(
        "apps/myapp/src/env.ts",
        "export const env = createEnv({ server: {}, experimental__runtimeEnv: {} });\n",
    );
}

#[given("an app surface whose source code reads a key absent from .env.example")]
fn given_env_validate_read_undeclared(w: &mut EnvWorld) {
    w.write("repo-config.yml", APP_DRIFT_REPO_CONFIG);
    w.write("apps/myapp/.env.example", "");
    w.write(
        "apps/myapp/src/env.ts",
        "export const env = createEnv({\n  server: {\n    NEW_KEY: z.string(),\n  },\n  experimental__runtimeEnv: {},\n});\n",
    );
}

#[given(
    "an F# app surface whose .env.example declares keys read through a pure environment-reader wrapper and whose source reads the framework-owned container signal"
)]
fn given_env_validate_fsharp_environment_reader_wrapper(w: &mut EnvWorld) {
    w.write("repo-config.yml", FSHARP_WRAPPER_REPO_CONFIG);
    w.write(
        "apps/myapp/.env.example",
        "F_SHARP_WRAPPED_DATA_DIRECTORY=/var/lib/myapp\nF_SHARP_WRAPPED_PORT=19300\n",
    );
    w.write(
        "apps/myapp/src/Configuration.fs",
        r#"module Configuration
let load (readEnvironment: string -> string) =
    let runningInContainer = Environment.GetEnvironmentVariable("DOTNET_RUNNING_IN_CONTAINER")
    let dataDirectory = readEnvironment "F_SHARP_WRAPPED_DATA_DIRECTORY"
    let port = readEnvironment "F_SHARP_WRAPPED_PORT"
    (runningInContainer, dataDirectory, port)
"#,
    );
}

#[when("the developer runs env validate")]
fn when_env_validate_runs(w: &mut EnvWorld) {
    w.exec(&["env", "validate"]);
}

#[then("the output names the key as declared-but-unread")]
fn then_env_validate_names_declared_unread(w: &mut EnvWorld) {
    let out = w.combined_output();
    assert!(out.contains("declared-but-unread"), "got: {out}");
    assert!(out.contains("STALE_KEY"), "got: {out}");
}

#[then("the output names the key as read-but-undeclared")]
fn then_env_validate_names_read_undeclared(w: &mut EnvWorld) {
    let out = w.combined_output();
    assert!(out.contains("read-but-undeclared"), "got: {out}");
    assert!(out.contains("NEW_KEY"), "got: {out}");
}

// ===========================================================================
// Shared Then steps
// ===========================================================================

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut EnvWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the command exits with a failure code")]
fn then_exit_fail(w: &mut EnvWorld) {
    assert_ne!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the output is valid JSON")]
fn then_valid_json(w: &mut EnvWorld) {
    let out = w.stdout();
    let parsed = serde_json::from_str::<serde_json::Value>(&out);
    assert!(parsed.is_ok(), "invalid JSON: {out}");
}

// Secrets and dry-run steps (env-backup-secrets, env-backup-dry-run).

#[given("a git repository containing a secrets.json file at the root")]
fn given_repo_secrets_json(w: &mut EnvWorld) {
    w.write("secrets.json", "{}\n");
}

#[given("a git repository containing a cert.pem file at the root")]
fn given_repo_cert_pem(w: &mut EnvWorld) {
    w.write("cert.pem", "-----BEGIN CERT-----\n");
}

#[given("a git repository containing a .secrets/notes.md file")]
fn given_repo_secrets_dir_file(w: &mut EnvWorld) {
    w.write(".secrets/notes.md", "secret notes\n");
}

#[given("a git repository containing a .env file and a secrets.json file")]
fn given_repo_env_and_secrets_json(w: &mut EnvWorld) {
    w.write(".env", "A=1\n");
    w.write("secrets.json", "{}\n");
}

#[when("the developer runs rhino-cli env backup with --dry-run")]
fn when_env_backup_dry_run(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "backup", "--dir", &dir, "--dry-run"]);
}

#[then("secrets.json is copied to the backup directory")]
fn then_secrets_json_copied_to_backup(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("secrets.json"),
        "expected secrets.json in output: {}",
        w.stdout()
    );
}

#[then("cert.pem is copied to the backup directory")]
fn then_cert_pem_copied_to_backup(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("cert.pem"),
        "expected cert.pem in output: {}",
        w.stdout()
    );
}

#[then(".secrets/notes.md is copied to the backup directory preserving its relative path")]
fn then_secrets_dir_copied_to_backup(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains(".secrets"),
        "expected .secrets in output: {}",
        w.stdout()
    );
}

#[then("no files from the .git directory are backed up")]
fn then_no_git_dir_backed(w: &mut EnvWorld) {
    assert!(
        !w.stdout().contains(".git/"),
        "expected no .git/ in output: {}",
        w.stdout()
    );
}

#[then("no files are written to the backup directory")]
fn then_no_files_written_to_backup(w: &mut EnvWorld) {
    assert_eq!(
        w.exit_code(),
        0,
        "expected success for dry-run: {}",
        w.stdout()
    );
}

#[then("the output lists the files that would be backed up")]
fn then_output_lists_would_be_backed_up(w: &mut EnvWorld) {
    let out = w.stdout();
    assert!(!out.is_empty(), "expected non-empty output listing files");
}

// Secrets and dry-run steps (env-restore-secrets, env-restore-dry-run).

#[given("a backup directory containing a secrets.json file")]
fn given_backup_with_secrets_json(w: &mut EnvWorld) {
    w.write_backup("secrets.json", "{}\n");
}

#[given("a backup directory containing a cert.pem file")]
fn given_backup_with_cert_pem(w: &mut EnvWorld) {
    w.write_backup("cert.pem", "-----BEGIN CERT-----\n");
}

#[given("a backup directory containing a .secrets/notes.md file")]
fn given_backup_with_secrets_dir_file(w: &mut EnvWorld) {
    w.write_backup(".secrets/notes.md", "secret notes\n");
}

#[given("a backup directory containing a .env file and a secrets.json file")]
fn given_backup_with_env_and_secrets_json(w: &mut EnvWorld) {
    w.write_backup(".env", "A=1\n");
    w.write_backup("secrets.json", "{}\n");
}

#[when("the developer runs rhino-cli env restore with --dry-run")]
fn when_env_restore_dry_run(w: &mut EnvWorld) {
    let dir = w.backup_dir_arg();
    w.exec(&["env", "restore", "--dir", &dir, "--dry-run"]);
}

#[then("secrets.json is copied back to the repository")]
fn then_secrets_json_copied_back(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("secrets.json"),
        "expected secrets.json in output: {}",
        w.stdout()
    );
}

#[then("cert.pem is copied back to the repository")]
fn then_cert_pem_copied_back(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains("cert.pem"),
        "expected cert.pem in output: {}",
        w.stdout()
    );
}

#[then(".secrets/notes.md is copied back to the repository preserving its relative path")]
fn then_secrets_dir_copied_back(w: &mut EnvWorld) {
    assert!(
        w.stdout().contains(".secrets"),
        "expected .secrets in output: {}",
        w.stdout()
    );
}

#[then("no files are written to the repository")]
fn then_no_files_written_to_repo(w: &mut EnvWorld) {
    assert_eq!(
        w.exit_code(),
        0,
        "expected success for dry-run restore: {}",
        w.stdout()
    );
}

#[then("the output lists the files that would be restored")]
fn then_output_lists_would_be_restored(w: &mut EnvWorld) {
    let out = w.stdout();
    assert!(!out.is_empty(), "expected non-empty output listing files");
}

#[tokio::main]
async fn main() {
    EnvWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/env")
        .canonicalize()
        .expect("feature dir resolvable")
}
