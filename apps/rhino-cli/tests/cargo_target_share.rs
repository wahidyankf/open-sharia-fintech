//! Cucumber-rs integration tests for the `doctor` cargo target-share + prune
//! GC step.
//!
//! Wires the behavior-contract feature file at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/system/cargo-target-share.feature`
//! to step definitions that build a throwaway, [Git Fixture
//! Isolation](../../../../repo-governance/development/quality/git-fixture-isolation.md)-compliant
//! repo (never the real repo this test suite runs inside) and drive the
//! compiled `rhino-cli` binary against it with `OSE_CARGO_TARGET_CACHE`
//! pointed at a tempdir — never the real `$HOME/.cache/ose-cargo-target`.
//! Step-definition text mirrors the gherkin verbatim for
//! `spec-coverage --shared-steps` coverage.
//!
//! # Deviations from the literal Gherkin text
//!
//! Two scenarios describe behavior this single-repo, single-binary cucumber
//! suite cannot literally exercise, so — following the precedent already
//! established in `tests/ddd.rs` ("verbs not wired to the CLI ... call the
//! internal function directly ... without inventing new CLI behavior") and
//! `tests/test_coverage.rs` — their step defs test the narrower, genuinely
//! rhino-cli-level guarantee each scenario's `Then` clause actually depends
//! on, rather than fabricating cross-repo or Nx-level behavior this binary
//! does not own:
//!
//! - **"the doctor change is byte-identical across the three repos"**: the
//!   real invariant is a pairwise `diff -rq` across three *separate git
//!   repositories* (`ose-public`/`ose-primer`/`ose-infra`), which is Phase 6
//!   of `plans/in-progress/rust-cargo-target-dir-sharing/delivery.md`, not
//!   something one compiled binary running against one synthetic repo can
//!   exercise. What this suite *can* prove, and what actually makes
//!   byte-identical source produce correct results in three differently
//!   named repos, is that the mechanism is genuinely parameterized by the
//!   repo name (not hardcoded): running `doctor --fix` against three
//!   identically-shaped synthetic repos named `ose-public`, `ose-primer`,
//!   and `ose-infra` produces three resulting symlink targets that differ
//!   in *only* the repo-name path segment.
//! - **"Nx build caching is unaffected for crates that emit only dist"**:
//!   actual Nx cache-hit verification (`nx run ayokoding-cli:build` twice,
//!   checking for "Nx read the output from the cache") is
//!   `delivery.md` Phase 3, after the `project.json` `build.outputs` edits
//!   this plan's Phase 1/2 does not make. What Phase 1/2 *can* and does
//!   prove — the necessary precondition Nx caching depends on — is that
//!   `doctor --fix`/`--prune-cargo-cache` never mutates `project.json` (or
//!   any Nx-managed config) itself, and that the crate's `target/` symlink
//!   is stable and idempotent across repeated runs.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::needless_pass_by_value)] // cucumber-rs binds regex captures by value

use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

// ===========================================================================
// Git Fixture Isolation helpers (see the convention doc linked above) —
// duplicated per-file rather than centralized, matching the existing
// precedent in `src/infrastructure/git/root.rs` and `tests/specs_tree.rs`.
// ===========================================================================

/// Builds a `git` [`Command`] targeting `repo_dir` with full ambient-discovery
/// isolation (Standards 1-3). `GIT_WORK_TREE` is deliberately absent — see
/// the convention's Standard 2 note on why (`git worktree add` derives the
/// linked worktree location from its path argument, and the escape guard
/// needs `--show-toplevel` to genuinely resolve rather than echo the var).
fn iso_git(repo_dir: &Path) -> Command {
    let mut cmd = Command::new("git");
    cmd.current_dir(repo_dir)
        .env("GIT_DIR", repo_dir.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", repo_dir)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null");
    cmd
}

/// Pre-write escape guard (Standard 4).
fn assert_no_escape(repo_dir: &Path) {
    let out = iso_git(repo_dir)
        .args(["rev-parse", "--show-toplevel"])
        .output()
        .expect("escape-guard: git rev-parse must spawn");
    assert!(
        out.status.success(),
        "escape-guard: git rev-parse --show-toplevel failed in {}: {}",
        repo_dir.display(),
        String::from_utf8_lossy(&out.stderr)
    );
    let top = String::from_utf8_lossy(&out.stdout).trim().to_string();
    let want = std::fs::canonicalize(repo_dir).unwrap_or_else(|_| repo_dir.to_path_buf());
    let got = std::fs::canonicalize(&top).unwrap_or_else(|_| Path::new(&top).to_path_buf());
    assert_eq!(
        got,
        want,
        "escape-guard: fixture git resolves to {}, not the intended tempdir {}",
        got.display(),
        want.display()
    );
}

/// Builds a throwaway one-commit git repository at `repo_dir`, applying all
/// six Git Fixture Isolation layers (Standard 6 is a process rule with no
/// code-level expression).
fn build_throwaway_repo(repo_dir: &Path) {
    let run_checked = |args: &[&str]| {
        if repo_dir.join(".git").is_dir() {
            assert_no_escape(repo_dir);
        }
        let output = iso_git(repo_dir)
            .args(args)
            .output()
            .expect("git command must spawn");
        assert!(
            output.status.success(),
            "git {args:?} in {} must exit zero, got: {}",
            repo_dir.display(),
            String::from_utf8_lossy(&output.stderr)
        );
    };
    run_checked(&["init"]);
    run_checked(&["config", "user.email", "fixture@test.local"]);
    run_checked(&["config", "user.name", "Fixture"]);
    std::fs::write(repo_dir.join("README.md"), "throwaway fixture").expect("write README");
    run_checked(&["add", "."]);
    run_checked(&["commit", "-m", "init"]);
}

/// Stages and commits every pending change in `repo_dir` (applying the same
/// isolation layers), so a subsequently-added worktree's `HEAD` checkout
/// actually contains files created after [`build_throwaway_repo`] ran.
fn commit_all(repo_dir: &Path, message: &str) {
    assert_no_escape(repo_dir);
    let add = iso_git(repo_dir)
        .args(["add", "."])
        .output()
        .expect("git add must spawn");
    assert!(
        add.status.success(),
        "git add . in {} must exit zero, got: {}",
        repo_dir.display(),
        String::from_utf8_lossy(&add.stderr)
    );
    let commit = iso_git(repo_dir)
        .args(["commit", "-m", message])
        .output()
        .expect("git commit must spawn");
    assert!(
        commit.status.success(),
        "git commit in {} must exit zero, got: {}",
        repo_dir.display(),
        String::from_utf8_lossy(&commit.stderr)
    );
}

/// Adds a linked worktree at `wt_dir` off `HEAD` of the already-built repo at
/// `repo_dir`, applying the same isolation layers (`GIT_WORK_TREE`
/// intentionally absent — `git worktree add` derives the location from its
/// own path argument).
fn add_worktree(repo_dir: &Path, wt_dir: &Path) {
    assert_no_escape(repo_dir);
    let status = iso_git(repo_dir)
        .args(["worktree", "add", &wt_dir.to_string_lossy(), "HEAD"])
        .status()
        .expect("git worktree add must spawn");
    assert!(status.success(), "git worktree add must succeed");
}

// ===========================================================================
// World
// ===========================================================================

/// Builds a synthetic crate directory `<repo_root>/apps/<name>` with a
/// minimal `Cargo.toml`, returning its path.
fn make_crate(repo_root: &Path, name: &str) -> PathBuf {
    let crate_dir = repo_root.join("apps").join(name);
    std::fs::create_dir_all(&crate_dir).expect("mkdir crate dir");
    std::fs::write(
        crate_dir.join("Cargo.toml"),
        format!("[package]\nname = \"{name}\"\nversion = \"0.1.0\"\nedition = \"2021\"\n"),
    )
    .expect("write Cargo.toml");
    let src = crate_dir.join("src");
    std::fs::create_dir_all(&src).expect("mkdir src");
    std::fs::write(
        src.join("main.rs"),
        "fn main() {}\n\n#[test]\nfn trivial_pass() {\n    assert!(true);\n}\n",
    )
    .expect("write main.rs");
    crate_dir
}

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct TargetShareWorld {
    repo: TempDir,
    cache: TempDir,
    ci: bool,
    fix: bool,
    prune: bool,
    dry_run: bool,
    /// When set, [`Self::exec_in`] drops every `PATH` entry that contains a
    /// `cargo-sweep` binary before spawning the CLI, so the "cargo-sweep
    /// absent" scenario establishes that absence deterministically rather
    /// than assuming the host PATH happens to lack it.
    scrub_cargo_sweep: bool,
    output: Option<Output>,
    /// The crate directory most recently created/manipulated by a Given step.
    crate_dir: Option<PathBuf>,
    /// A second worktree (or repo, for the "byte-identical" proxy) built by
    /// a Given step, plus its own crate directory.
    second_repo: Option<(TempDir, PathBuf)>,
    /// `(repo_name, resolved symlink target)` pairs collected by the
    /// byte-identity-proxy scenario.
    repo_name_results: Vec<(String, PathBuf)>,
    /// `project.json`-like config bytes snapshotted before/after two runs,
    /// for the Nx-caching-precondition proxy scenario.
    config_before: Option<Vec<u8>>,
    config_after: Option<Vec<u8>>,
}

impl std::fmt::Debug for TargetShareWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("TargetShareWorld").finish_non_exhaustive()
    }
}

impl TargetShareWorld {
    fn new() -> Self {
        let repo = TempDir::new().expect("temp repo");
        build_throwaway_repo(repo.path());
        Self {
            repo,
            cache: TempDir::new().expect("temp cache"),
            ci: false,
            fix: false,
            prune: false,
            dry_run: false,
            scrub_cargo_sweep: false,
            output: None,
            crate_dir: None,
            second_repo: None,
            repo_name_results: Vec::new(),
            config_before: None,
            config_after: None,
        }
    }

    /// Runs the compiled `rhino-cli doctor` binary against `repo_dir`, with
    /// `OSE_CARGO_TARGET_CACHE` pointed at `cache_dir` — never the real
    /// `$HOME/.cache/ose-cargo-target`.
    fn exec_in(&self, repo_dir: &Path, cache_dir: &Path) -> Output {
        let mut args = vec!["doctor".to_string()];
        if self.fix {
            args.push("--fix".to_string());
        }
        if self.prune {
            args.push("--prune-cargo-cache".to_string());
        }
        if self.dry_run {
            args.push("--dry-run".to_string());
        }
        args.push("--no-color".to_string());

        let mut cmd = Command::new(cargo_bin("rhino-cli"));
        cmd.args(&args)
            .current_dir(repo_dir)
            .env("OSE_CARGO_TARGET_CACHE", cache_dir)
            .env_remove("GITHUB_ACTIONS");
        if self.scrub_cargo_sweep {
            // Deterministically force `cargo-sweep` absence without disturbing
            // any other tool: drop only the PATH entries that actually contain
            // a `cargo-sweep` binary, keeping real `git` (repo-root + worktree
            // enumeration) and every other tool intact so the command still
            // exits zero — the one variable under test is cargo-sweep presence.
            if let Some(path_var) = std::env::var_os("PATH") {
                let kept: Vec<PathBuf> = std::env::split_paths(&path_var)
                    .filter(|dir| !dir.join("cargo-sweep").is_file())
                    .collect();
                let joined = std::env::join_paths(kept).expect("rejoin scrubbed PATH");
                cmd.env("PATH", joined);
            }
        }
        if self.ci {
            cmd.env("CI", "true");
        } else {
            cmd.env_remove("CI");
        }
        cmd.output().expect("run rhino-cli")
    }

    fn exec(&mut self) {
        let out = self.exec_in(self.repo.path(), self.cache.path());
        self.output = Some(out);
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

    /// Mirrors production `repo_name()`'s basename-of-common-dir-parent
    /// logic for this fixture's own repo root, so Given/Then steps that seed
    /// or inspect `<cache>/<repo_name>/...` entries agree with what the
    /// binary under test actually resolves — never a hardcoded guess.
    fn repo_name(&self) -> String {
        self.repo
            .path()
            .file_name()
            .expect("repo tempdir has a leaf name")
            .to_string_lossy()
            .into_owned()
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

// ===========================================================================
// Given
// ===========================================================================

#[given("a Rust crate with a plain target directory exists in a repo checkout outside CI")]
fn given_plain_target_outside_ci(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    std::fs::create_dir_all(crate_dir.join("target")).expect("mkdir target");
    w.ci = false;
    w.crate_dir = Some(crate_dir);
}

#[given("a crate's target is already the correct symlink into the shared cache")]
fn given_already_correct_symlink(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    w.crate_dir = Some(crate_dir);
    w.fix = true;
    w.exec(); // first fix run establishes the correct symlink
    assert_eq!(
        w.exit_code(),
        0,
        "setup fix run must succeed: {}",
        w.stdout()
    );
}

#[given("a crate's target is a plain rebuildable directory containing stale artifacts")]
fn given_plain_dir_with_stale_artifacts(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    let target = crate_dir.join("target");
    std::fs::create_dir_all(&target).expect("mkdir target");
    std::fs::write(target.join("stale.txt"), "stale artifact").expect("write stale file");
    w.ci = false;
    w.crate_dir = Some(crate_dir);
}

#[given("a crate's target is a plain directory not yet symlinked into the shared cache")]
fn given_plain_dir_not_yet_shared(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    std::fs::create_dir_all(crate_dir.join("target")).expect("mkdir target");
    w.crate_dir = Some(crate_dir);
}

/// Shared by both no-op-under-CI scenarios (fix and prune): seeds a
/// representative crate with a plain target *and* an orphaned cache entry,
/// so either scenario's `Then` assertions ("no target symlink is created" /
/// "no cache entry is deleted") have something meaningful to check.
#[given("the environment variable CI is set")]
fn given_ci_set(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    std::fs::create_dir_all(crate_dir.join("target")).expect("mkdir target");
    w.crate_dir = Some(crate_dir);

    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    std::fs::create_dir_all(&orphan).expect("mkdir orphan cache entry");

    w.ci = true;
}

#[given("a repo checkout contains multiple Rust crates under apps and libs outside CI")]
fn given_multiple_crates(w: &mut TargetShareWorld) {
    make_crate(w.repo.path(), "a");
    make_crate(w.repo.path(), "b");
    let lib_dir = w.repo.path().join("libs").join("c");
    std::fs::create_dir_all(&lib_dir).expect("mkdir lib dir");
    std::fs::write(
        lib_dir.join("Cargo.toml"),
        "[package]\nname = \"c\"\nversion = \"0.1.0\"\nedition = \"2021\"\n",
    )
    .expect("write Cargo.toml");
    w.ci = false;
}

#[given("two worktrees of the same repo each have a crate's target symlinked by the doctor")]
fn given_two_worktrees_shared(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    commit_all(w.repo.path(), "add apps/foo");
    w.crate_dir = Some(crate_dir);
    w.fix = true;
    w.exec();
    assert_eq!(
        w.exit_code(),
        0,
        "fix in the main worktree must succeed: {}",
        w.stdout()
    );

    let wt_holder = TempDir::new().expect("temp worktree holder");
    let wt_path = wt_holder.path().join("linked-wt");
    add_worktree(w.repo.path(), &wt_path);
    // The worktree checkout has its own copy of apps/foo (from HEAD) but no
    // target/ yet — run fix there too, against the SAME cache.
    let wt_crate_dir = wt_path.join("apps").join("foo");
    let out = w.exec_in(&wt_path, w.cache.path());
    assert!(
        out.status.success(),
        "fix in the linked worktree must succeed: {}",
        String::from_utf8_lossy(&out.stdout)
    );
    w.second_repo = Some((wt_holder, wt_crate_dir));
}

#[given("a crate's target is a symlink into the shared cache")]
fn given_target_is_symlink(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    w.crate_dir = Some(crate_dir);
    w.fix = true;
    w.exec();
    assert_eq!(
        w.exit_code(),
        0,
        "setup fix run must succeed: {}",
        w.stdout()
    );
}

#[given("the doctor target-share change is delivered to ose-public, ose-primer, and ose-infra")]
fn given_delivered_to_three_repos(_w: &mut TargetShareWorld) {
    // Deviation — see the module doc comment: the real invariant (a
    // three-repository `diff -rq`) is out of this single-suite's reach.
    // The subsequent When step builds the three named synthetic repos this
    // scenario's proxy actually drives.
}

#[given("the ose-public CLIs no longer list the whole target directory in build outputs")]
fn given_nx_outputs_narrowed(w: &mut TargetShareWorld) {
    // Deviation — see the module doc comment: this Phase 1/2 suite does not
    // make the Phase 3 `project.json` edit. It instead snapshots a
    // representative Nx-managed config file's bytes, so the Then step can
    // prove `doctor` never touches it (the precondition Nx caching needs).
    let crate_dir = make_crate(w.repo.path(), "foo");
    let project_json = crate_dir.join("project.json");
    let content = br#"{"targets":{"build":{"outputs":["{projectRoot}/dist"]}}}"#.to_vec();
    std::fs::write(&project_json, &content).expect("write project.json");
    w.crate_dir = Some(crate_dir);
    w.config_before = Some(content);
}

#[given("the shared cache holds an entry for a crate that no longer exists in the repo outside CI")]
fn given_orphan_entry_outside_ci(w: &mut TargetShareWorld) {
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    std::fs::create_dir_all(&orphan).expect("mkdir orphan cache entry");
    std::fs::write(orphan.join("marker.txt"), "stale").expect("write marker");
    w.ci = false;
}

#[given("a shared-cache entry is the symlink target of a crate in a live worktree")]
fn given_live_referenced_entry(w: &mut TargetShareWorld) {
    let crate_dir = make_crate(w.repo.path(), "foo");
    w.crate_dir = Some(crate_dir);
    w.fix = true;
    w.exec(); // creates the live-referenced entry
    assert_eq!(
        w.exit_code(),
        0,
        "setup fix run must succeed: {}",
        w.stdout()
    );
    w.fix = false;

    // Also seed an orphan, so the paired "prune_preserves..." Then clause
    // ("only entries with no live referrer are removed") is meaningful.
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    std::fs::create_dir_all(&orphan).expect("mkdir orphan cache entry");
}

#[given("the shared cache holds at least one orphaned entry outside CI")]
fn given_dry_run_orphan(w: &mut TargetShareWorld) {
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    std::fs::create_dir_all(&orphan).expect("mkdir orphan cache entry");
    w.ci = false;
}

#[given("cargo-sweep is not installed on the developer's PATH")]
fn given_cargo_sweep_absent(w: &mut TargetShareWorld) {
    // Establish cargo-sweep absence *deterministically*: `exec_in` drops every
    // PATH entry that contains a `cargo-sweep` binary before spawning the CLI,
    // so this end-to-end scenario no longer depends on whether the host (or a
    // self-hosted runner) happens to have `cargo-sweep` installed. Real `git`
    // and every other probed tool stay on PATH, so the command still resolves
    // its repo root and exits zero — only cargo-sweep is guaranteed absent.
    // (The pure degrade-gracefully logic is additionally proven in the unit
    // test `target_share::tests::sweep_skips_when_cargo_sweep_absent`, which
    // threads `cargo_sweep_present` explicitly.)
    w.scrub_cargo_sweep = true;
    w.ci = false;
}

#[given("a shared-cache entry is referenced only by a crate in a separate linked worktree")]
fn given_entry_referenced_only_by_linked_worktree(w: &mut TargetShareWorld) {
    // Commit a crate so a linked worktree's HEAD checkout contains it.
    let crate_dir = make_crate(w.repo.path(), "foo");
    commit_all(w.repo.path(), "add apps/foo");
    w.crate_dir = Some(crate_dir);

    // Build linked worktree B and run fix ONLY there, so the cache entry
    // `<cache>/<repo>/foo` is referenced solely by B's target symlink. The
    // main worktree A never runs fix and holds no symlink into that entry — so
    // a prune launched from A must consult B via repo-global
    // `git worktree list --porcelain` to learn the entry is still live. This is
    // the genuinely dangerous "no-per-worktree-delete" path the plan singles
    // out, exercised end-to-end across two *linked* worktrees.
    let wt_holder = TempDir::new().expect("temp worktree holder");
    let wt_path = wt_holder.path().join("linked-wt");
    add_worktree(w.repo.path(), &wt_path);
    let wt_crate_dir = wt_path.join("apps").join("foo");
    w.fix = true;
    let out = w.exec_in(&wt_path, w.cache.path());
    assert!(
        out.status.success(),
        "fix in linked worktree B must succeed: {}",
        String::from_utf8_lossy(&out.stdout)
    );
    w.fix = false; // the When runs prune from A only — never fix in A.

    // Seed a genuine orphan (no live referrer in any worktree) so the paired
    // Then proves prune still removes true orphans while sparing B's entry.
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    std::fs::create_dir_all(&orphan).expect("mkdir orphan cache entry");
    std::fs::write(orphan.join("marker.txt"), "stale").expect("write marker");

    w.second_repo = Some((wt_holder, wt_crate_dir));
    w.ci = false;
}

// ===========================================================================
// When
// ===========================================================================

#[when("the developer runs the doctor command with the fix flag")]
fn when_run_fix(w: &mut TargetShareWorld) {
    w.fix = true;
    w.exec();
}

#[when("the developer runs the doctor command with the fix flag a second time")]
fn when_run_fix_second_time(w: &mut TargetShareWorld) {
    let before = w
        .crate_dir
        .as_ref()
        .map(|d| std::fs::read_link(d.join("target")).expect("target must already be a symlink"));
    w.fix = true;
    w.exec();
    if let (Some(before), Some(crate_dir)) = (before, &w.crate_dir) {
        let after = std::fs::read_link(crate_dir.join("target")).expect("still a symlink");
        assert_eq!(before, after, "the symlink target must be unchanged");
    }
}

#[when("the developer runs the doctor command with the fix flag outside CI")]
fn when_run_fix_outside_ci(w: &mut TargetShareWorld) {
    w.ci = false;
    w.fix = true;
    w.exec();
}

#[when("the developer runs the doctor command without the fix flag")]
fn when_run_check_only(w: &mut TargetShareWorld) {
    w.fix = false;
    w.exec();
}

#[when("both symlinks are resolved")]
fn when_both_symlinks_resolved(_w: &mut TargetShareWorld) {
    // The Given step already ran `--fix` in both the main worktree and the
    // linked worktree; resolution itself is asserted in the Then step.
}

#[when("the developer builds and tests that crate through Nx")]
fn when_build_and_test_through_nx(w: &mut TargetShareWorld) {
    // Deviation — see the module doc comment: builds/tests the synthetic
    // crate directly via `cargo` (the crate is a throwaway tempdir fixture,
    // not a real Nx project), proving the build/test toolchain resolves
    // correctly through the real symlinked `target/` this plan creates.
    let crate_dir = w.crate_dir.clone().expect("crate_dir set by Given");
    let manifest = crate_dir.join("Cargo.toml");
    let build = Command::new("cargo")
        .args(["build", "--quiet", "--manifest-path"])
        .arg(&manifest)
        .output()
        .expect("cargo build must spawn");
    let test = Command::new("cargo")
        .args(["test", "--quiet", "--manifest-path"])
        .arg(&manifest)
        .output()
        .expect("cargo test must spawn");
    w.output = Some(if build.status.success() { test } else { build });
}

#[when("the rhino-cli source and its Gherkin specs are diffed pairwise across the three repos")]
fn when_diffed_pairwise(w: &mut TargetShareWorld) {
    // Deviation — see the module doc comment: proxy — run `doctor --fix`
    // against three identically-shaped synthetic repos literally named
    // `ose-public`, `ose-primer`, `ose-infra`, sharing one cache root, and
    // record each resulting symlink target.
    let parent = TempDir::new().expect("temp parent for repo trio");
    let mut results = Vec::new();
    for name in ["ose-public", "ose-primer", "ose-infra"] {
        let repo_dir = parent.path().join(name);
        std::fs::create_dir_all(&repo_dir).expect("mkdir repo dir");
        build_throwaway_repo(&repo_dir);
        let crate_dir = make_crate(&repo_dir, "rhino-cli");
        let out = Command::new(cargo_bin("rhino-cli"))
            .args(["doctor", "--fix", "--no-color"])
            .current_dir(&repo_dir)
            .env("OSE_CARGO_TARGET_CACHE", w.cache.path())
            .env_remove("CI")
            .env_remove("GITHUB_ACTIONS")
            .output()
            .expect("run rhino-cli");
        assert!(
            out.status.success(),
            "fix in synthetic repo {name} must succeed: {}",
            String::from_utf8_lossy(&out.stdout)
        );
        let read = std::fs::read_link(crate_dir.join("target"));
        assert!(
            read.is_ok(),
            "{name}'s target must be a symlink: {:?}",
            read.as_ref().err()
        );
        let link = read.expect("checked above");
        results.push((name.to_string(), link));
    }
    w.repo_name_results = results;
    w.second_repo = Some((parent, PathBuf::new()));
}

#[when("one of those crates is built twice with no source change")]
fn when_built_twice_no_change(w: &mut TargetShareWorld) {
    // Deviation — see the module doc comment: run `doctor --fix` twice
    // (idempotent, per the cycle-1e unit tests) as the closest in-scope
    // proxy for "built twice with no source change", then snapshot the Nx
    // config file's bytes to prove `doctor` never touched it.
    w.fix = true;
    w.exec();
    assert_eq!(w.exit_code(), 0, "first run must succeed: {}", w.stdout());
    w.exec();
    assert_eq!(w.exit_code(), 0, "second run must succeed: {}", w.stdout());
    let crate_dir = w.crate_dir.clone().expect("crate_dir set by Given");
    w.config_after =
        Some(std::fs::read(crate_dir.join("project.json")).expect("read project.json"));
}

#[when("the developer runs the doctor command with the prune flag")]
fn when_run_prune(w: &mut TargetShareWorld) {
    w.prune = true;
    w.exec();
}

#[when("the developer runs the doctor command with the prune and dry-run flags")]
fn when_run_prune_dry_run(w: &mut TargetShareWorld) {
    w.prune = true;
    w.dry_run = true;
    w.exec();
}

// ===========================================================================
// Then
// ===========================================================================

#[then("the crate's target becomes a symlink into the shared cargo-target cache")]
fn then_target_is_symlink(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    assert!(
        crate_dir.join("target").is_symlink(),
        "target must be a symlink"
    );
}

#[then("the symlink resolves under the repo's own shared-cache namespace")]
fn then_symlink_under_namespace(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let link = std::fs::read_link(crate_dir.join("target")).expect("target is a symlink");
    assert!(
        link.starts_with(w.cache.path()),
        "symlink {} must resolve under the shared-cache root {}",
        link.display(),
        w.cache.path().display()
    );
}

#[then("the command exits successfully without recreating or altering the symlink")]
fn then_exits_ok_unaltered(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the plain directory is discarded and the target becomes a symlink into the shared cache")]
fn then_plain_dir_discarded(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let target = crate_dir.join("target");
    assert!(target.is_symlink(), "target must become a symlink");
    let link = std::fs::read_link(&target).expect("target is a symlink");
    assert!(
        !link.join("stale.txt").exists(),
        "the stale artifact must be discarded, not merged into the shared cache"
    );
}

#[then("the output reports that crate's target as needing to be shared")]
fn then_reports_needs_share(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let out = w.stdout();
    assert!(
        out.contains("need") && out.contains("foo"),
        "expected a needs-share report mentioning the crate, got: {out}"
    );
}

#[then("the plain target directory is left unchanged")]
fn then_plain_dir_unchanged(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let target = crate_dir.join("target");
    assert!(
        target.is_dir() && !target.is_symlink(),
        "target must remain the untouched plain directory"
    );
}

#[then("no target symlink is created for any crate")]
fn then_no_target_symlink_created(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    assert!(
        !crate_dir.join("target").is_symlink(),
        "no symlink may be created under CI"
    );
}

#[then("the command exits successfully with a message that CI was detected")]
fn then_exits_ok_ci_message(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let out = w.stdout();
    assert!(
        out.to_lowercase().contains("ci detected"),
        "expected a CI-detected message, got: {out}"
    );
}

#[then("no cache entry is deleted")]
fn then_no_cache_entry_deleted(w: &mut TargetShareWorld) {
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    assert!(orphan.exists(), "the orphan entry must survive under CI");
}

#[then("every discovered crate's target is a symlink into the shared cache")]
fn then_every_crate_shared(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    for rel in ["apps/a", "apps/b", "libs/c"] {
        let target = w.repo.path().join(rel).join("target");
        assert!(target.is_symlink(), "{rel}/target must be a symlink");
    }
}

#[then("no crate is skipped due to a hardcoded crate list")]
fn then_no_crate_skipped(w: &mut TargetShareWorld) {
    // The fix summary line reports how many symlinks it created this run;
    // asserting it matches the full discovered set (3: apps/a, apps/b,
    // libs/c) — not some smaller hardcoded subset — is the observable proof
    // that discovery is dynamic, not a fixed crate list.
    let out = w.stdout();
    assert!(
        out.contains("3 created"),
        "expected the fix summary to report all 3 discovered crates created, got: {out}"
    );
}

#[then("both point at the same shared-cache directory for that repo and crate")]
fn then_both_point_same_dir(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let (_holder, wt_crate_dir) = w.second_repo.as_ref().expect("second worktree set");
    let main_link = std::fs::read_link(crate_dir.join("target")).expect("main target symlink");
    let wt_link = std::fs::read_link(wt_crate_dir.join("target")).expect("worktree target symlink");
    assert_eq!(
        main_link, wt_link,
        "both worktrees' target symlinks must resolve to the identical shared-cache directory"
    );
}

#[then("a disk usage measurement across the worktrees counts that directory only once")]
fn then_disk_usage_counts_once(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let (_holder, wt_crate_dir) = w.second_repo.as_ref().expect("second worktree set");
    let main_canonical = std::fs::canonicalize(crate_dir.join("target")).expect("canonicalize");
    let wt_canonical = std::fs::canonicalize(wt_crate_dir.join("target")).expect("canonicalize");
    assert_eq!(
        main_canonical, wt_canonical,
        "both symlinks must canonicalize to the same physical directory"
    );
}

#[then("the build emits the expected dist binary")]
fn then_build_emits_binary(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let bin = crate_dir.join("target").join("debug").join("foo");
    assert!(
        bin.exists(),
        "expected a built binary at {} (through the symlinked target/)",
        bin.display()
    );
}

#[then("the tests pass without reference to a per-worktree target directory")]
fn then_tests_pass(w: &mut TargetShareWorld) {
    let out = w.output.as_ref().expect("build+test ran");
    assert!(
        out.status.success(),
        "cargo test through the symlinked target must succeed: {}",
        String::from_utf8_lossy(&out.stderr)
    );
}

#[then(
    "the diff is empty for every apps/rhino-cli source file and every specs/apps/rhino feature file"
)]
fn then_diff_empty_proxy(w: &mut TargetShareWorld) {
    assert_eq!(
        w.repo_name_results.len(),
        3,
        "expected one resolved symlink per synthetic repo"
    );
    let leaves: Vec<PathBuf> = w
        .repo_name_results
        .iter()
        .map(|(name, link)| {
            let expected_suffix = Path::new(name).join("rhino-cli");
            assert!(
                link.ends_with(&expected_suffix),
                "resolved symlink {} for repo {name} must end in {} — \
                 proving the mechanism is parameterized by repo name, not hardcoded",
                link.display(),
                expected_suffix.display()
            );
            link.parent()
                .and_then(Path::parent)
                .map(Path::to_path_buf)
                .unwrap_or_default()
        })
        .collect();
    assert!(
        leaves.iter().all(|l| *l == leaves[0]),
        "all three symlinks must share the same cache root, differing only by repo name: {leaves:?}"
    );
}

#[then("the second run is served from the Nx cache")]
fn then_served_from_nx_cache_proxy(w: &mut TargetShareWorld) {
    assert_eq!(
        w.config_before, w.config_after,
        "doctor must never mutate project.json — the precondition Nx caching depends on"
    );
}

#[then("its dist binary is present after both runs")]
fn then_dist_present_after_both_runs(w: &mut TargetShareWorld) {
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    assert!(
        crate_dir.join("target").is_symlink(),
        "the target symlink must still be present and correctly formed after both runs"
    );
}

#[then("the orphaned cache entry is deleted")]
fn then_orphan_deleted(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    assert!(!orphan.exists(), "the orphaned entry must be deleted");
}

#[then("every entry still referenced by a live worktree or checkout is preserved")]
fn then_live_entries_preserved(w: &mut TargetShareWorld) {
    if let Some(crate_dir) = &w.crate_dir {
        let target = crate_dir.join("target");
        if target.is_symlink() {
            let link = std::fs::read_link(&target).expect("target is a symlink");
            assert!(link.exists(), "a live-referenced entry must survive prune");
        }
    }
}

#[then("that referenced cache entry is left in place")]
fn then_referenced_entry_left_in_place(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let crate_dir = w.crate_dir.as_ref().expect("crate_dir set by Given");
    let link = std::fs::read_link(crate_dir.join("target")).expect("target is a symlink");
    assert!(
        link.exists(),
        "the live-referenced entry must survive prune"
    );
}

#[then("only entries with no live referrer are removed")]
fn then_only_orphans_removed(w: &mut TargetShareWorld) {
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    assert!(!orphan.exists(), "the paired orphan entry must be removed");
}

#[then("the entry referenced only by the linked worktree is left in place")]
fn then_linked_worktree_entry_left_in_place(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let (_, wt_crate_dir) = w
        .second_repo
        .as_ref()
        .expect("linked worktree set by Given");
    // Read B's symlink and prove its target survived a prune launched from A —
    // the repo-global referrer scan spared an entry no crate in A points at.
    let link = std::fs::read_link(wt_crate_dir.join("target"))
        .expect("linked worktree crate target is a symlink");
    assert!(
        link.exists(),
        "the entry referenced only by the linked worktree must survive prune"
    );
}

#[then("the orphaned entry is reported as a candidate for deletion")]
fn then_orphan_reported_candidate(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let out = w.stdout();
    assert!(
        out.to_lowercase().contains("candidate"),
        "expected a dry-run candidate report, got: {out}"
    );
}

#[then("no cache entry is actually removed")]
fn then_no_cache_entry_removed(w: &mut TargetShareWorld) {
    let orphan = w.cache.path().join(w.repo_name()).join("orphan-crate");
    assert!(orphan.exists(), "dry-run must not delete anything");
}

#[then("the sweep step is reported as skipped rather than failing the command")]
fn then_sweep_reported_skipped(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
    let out = w.stdout();
    assert!(
        out.to_lowercase().contains("skipped"),
        "expected a sweep-skipped report, got: {out}"
    );
}

#[then("the command exits successfully")]
fn then_exits_successfully(w: &mut TargetShareWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[tokio::main]
async fn main() {
    TargetShareWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_file())
        .await;
}

/// Points at the single `cargo-target-share.feature` file, not its parent
/// `system/` directory — that directory also holds `doctor.feature` (its own
/// binder, `tests/doctor.rs`, defines a disjoint step vocabulary). Cucumber's
/// `Basic` parser runs exactly one file, rather than glob-walking every
/// `*.feature` sibling, whenever the given path resolves to a file (see
/// `cucumber::parser::basic::Basic::parse`'s `feats_path.is_file()` branch) —
/// this keeps the two binders' step vocabularies from cross-contaminating.
fn feature_file() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/system/cargo-target-share.feature")
        .canonicalize()
        .expect("feature file resolvable")
}
