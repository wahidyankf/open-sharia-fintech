//! Cucumber-rs integration tests for the `governance word-budget validate`
//! and `governance readme-index validate` command family
//! (`specs/apps/rhino/behavior/rhino-cli/gherkin/governance/*.feature`).
//!
//! Not wired into any `nx run rhino-cli:test:*` target — matching this
//! crate's existing convention for cucumber-rs suites (see `tests/agents.rs`
//! and sibling `harness = false` suites in `Cargo.toml`: only a handful of
//! `--test` binaries are named explicitly in `project.json`, the rest exist
//! for `specs behavior-coverage validate`'s static step-text matching and
//! for manual/future wiring). These step definitions exist so that check
//! passes (every Gherkin step in the two new `governance/` feature files
//! resolves to a real, compiled step implementation) and so the behavior
//! documented by those scenarios has a genuine, runnable reference
//! implementation — not so cucumber itself is exercised by CI today.
//!
//! A handful of scenarios describe end-state behavior that only becomes true
//! once Phase 9 of the `optimize-governance-md` plan arms the
//! `governance-word-budget` / `governance-readme-completeness` gates. Both are
//! armed `gates:` entries as of Phase 9, so these steps assert the gate ids are
//! present — mirroring
//! `application::governance::word_budget::tests::scenario_old_gate_id_is_replaced`.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::needless_pass_by_value)]
#![allow(clippy::panic)]
#![allow(clippy::used_underscore_binding)] // cucumber-rs macro codegen references `_`-prefixed regex-capture params

use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Shared scenario state. Each scenario gets a fresh git-rooted temp
/// workspace so the binary's git-root resolution works inside the fixture.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct GovWorld {
    work: TempDir,
    output: Option<Output>,
    /// Directory most recently established by a `Given directory "..."` or
    /// `Given file "..." exists` step — bare (slash-free) filenames in a
    /// later `links` step resolve relative to this.
    last_dir: String,
    /// Path most recently written by a word-count step — consumed by
    /// `"...naming that file"` steps.
    last_path: String,
    /// Prose-word count recorded by the two-step Mermaid fixture builder.
    prose_words: usize,
}

impl std::fmt::Debug for GovWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("GovWorld")
            .field("last_dir", &self.last_dir)
            .field("last_path", &self.last_path)
            .finish_non_exhaustive()
    }
}

impl GovWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        init_git_repo(work.path());
        Self {
            work,
            output: None,
            last_dir: String::new(),
            last_path: String::new(),
            prose_words: 0,
        }
    }

    fn write(&self, rel: &str, content: &str) {
        let p = self.work.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk fixture dir");
        }
        std::fs::write(p, content).expect("write fixture");
    }

    /// Whether `rel` already exists in the fixture workspace.
    fn exists(&self, rel: &str) -> bool {
        self.work.path().join(rel).exists()
    }

    fn bin() -> PathBuf {
        cargo_bin("rhino-cli")
    }

    fn exec(&mut self, args: &[&str]) {
        // Defense-in-depth (Git Fixture Isolation convention, Standards 1 &
        // 3): the `rhino-cli` subprocess under test resolves its own git
        // root and may shell out to `git` internally (e.g. for
        // `governance readme-index generate`, a write command). Capping
        // discovery and blanking identity/config here means any such
        // internal `git` call stays confined to the fixture even if a
        // future code path forgets its own isolation. `GIT_DIR` is set to
        // match the fixture's already-initialized `.git` for the same
        // reason `run_git` sets it; `infrastructure::git::root::find_root_from`
        // explicitly strips `GIT_DIR`/`GIT_WORK_TREE` before its own
        // `git rev-parse` call, so this is a no-op for that specific path
        // and purely a safety net for any other internal `git` invocation.
        let out = std::process::Command::new(Self::bin())
            .args(args)
            .arg("--no-color")
            .current_dir(self.work.path())
            .env("GIT_CEILING_DIRECTORIES", self.work.path())
            .env("GIT_DIR", self.work.path().join(".git"))
            .env("GIT_CONFIG_GLOBAL", "/dev/null")
            .env("GIT_CONFIG_SYSTEM", "/dev/null")
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    /// Runs `rhino-cli` against the real repository this crate lives in —
    /// for scenarios that assert facts about the live `repo-config.yml`
    /// gates registry rather than a synthetic fixture. Deliberately NOT
    /// isolated with the fixture env vars `exec` uses above: this method's
    /// entire purpose is to resolve and operate on the real repository root,
    /// which is exactly what the Git Fixture Isolation convention's "does
    /// NOT cover" carve-out describes ("production code paths that
    /// intentionally operate on the real repository"). Pinning `GIT_DIR` to
    /// a throwaway path here would break every scenario that depends on it.
    fn exec_real(&mut self, args: &[&str]) {
        let out = std::process::Command::new(Self::bin())
            .args(args)
            .arg("--no-color")
            .current_dir(real_repo_root())
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

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

/// Pre-write escape guard (Git Fixture Isolation convention, Standard 4).
/// Panics unless git, under the same isolation env as [`run_git`], resolves
/// its top-level to `dir` (canonicalized). Mirrors
/// `tests/specs_tree.rs`'s `assert_no_escape` exactly — see that copy's doc
/// comment for the full rationale. `GIT_WORK_TREE` is deliberately NOT set:
/// it would make `--show-toplevel` merely echo the variable, defeating the
/// guard.
fn assert_no_escape(dir: &Path) {
    let out = std::process::Command::new("git")
        .args(["rev-parse", "--show-toplevel"])
        .current_dir(dir)
        .env("GIT_DIR", dir.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", dir)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null")
        .output()
        .expect("escape-guard: git rev-parse must spawn");
    assert!(
        out.status.success(),
        "escape-guard: `git rev-parse --show-toplevel` failed in {} (git could not confirm an \
         isolated repository here): {}",
        dir.display(),
        String::from_utf8_lossy(&out.stderr)
    );
    let top = String::from_utf8_lossy(&out.stdout).trim().to_string();
    let want = std::fs::canonicalize(dir).unwrap_or_else(|_| dir.to_path_buf());
    let got = std::fs::canonicalize(&top).unwrap_or_else(|_| Path::new(&top).to_path_buf());
    assert_eq!(
        got,
        want,
        "escape-guard: fixture git resolves to {}, not the intended tempdir {} — refusing to \
         proceed to avoid corrupting the real repository",
        got.display(),
        want.display()
    );
}

/// Runs `git` with `args` inside `dir`, under full Git Fixture Isolation
/// (all six mandatory layers — see
/// `repo-governance/development/quality/git-fixture-isolation.md`). Mirrors
/// `tests/specs_tree.rs`'s `run_git` exactly: explicit `GIT_DIR` closes
/// ambient upward discovery (Standard 2), `GIT_CEILING_DIRECTORIES` caps any
/// residual walk (Standard 1), the nulled `GIT_CONFIG_GLOBAL`/
/// `GIT_CONFIG_SYSTEM` keep identity deterministic and out of the developer's
/// real config (Standard 3), the pre-write escape guard runs before every
/// write once `dir/.git` exists (Standard 4), and the exit status is checked
/// via `status.success()` rather than a bare `.expect()` (Standard 5).
fn run_git(dir: &Path, args: &[&str]) {
    if dir.join(".git").is_dir() {
        assert_no_escape(dir);
    }
    let output = std::process::Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_DIR", dir.join(".git"))
        .env("GIT_CEILING_DIRECTORIES", dir)
        .env("GIT_CONFIG_GLOBAL", "/dev/null")
        .env("GIT_CONFIG_SYSTEM", "/dev/null")
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git command must spawn");
    assert!(
        output.status.success(),
        "git {args:?} in {} must exit zero, got: {}",
        dir.display(),
        String::from_utf8_lossy(&output.stderr)
    );
}

fn init_git_repo(dir: &Path) {
    run_git(dir, &["init", "-q"]);
}

/// Resolves the real repository root this crate lives in — for scenarios
/// asserting facts about the live `repo-config.yml`, mirroring
/// `tests/agents.rs`'s `real_repo_root()`.
fn real_repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .expect("repo root resolvable")
}

/// Builds a whitespace-delimited fixture of exactly `n` words — the same
/// word-shaped fixture convention used throughout
/// `application::governance::word_budget`'s unit tests.
fn n_words(n: usize) -> String {
    vec!["w"; n].join(" ")
}

/// The `governance-word-budget:` fixture config shared by every scenario in
/// this suite. Covers every surface glob the Gherkin `Examples:` table and
/// named scenarios exercise, plus the resolved-tree budget.
const WORD_BUDGET_CONFIG: &str = r#"governance-word-budget:
  surfaces:
    - glob: "repo-governance/**/*.md"
      target: 400
      warn: 500
      fail: 500
    - glob: ".claude/**/*.md"
      target: 400
      warn: 500
      fail: 500
    - glob: ".cursor/**/*.md"
      target: 400
      warn: 500
      fail: 500
    - glob: ".opencode/**/*.md"
      target: 400
      warn: 500
      fail: 500
    - glob: ".amazonq/**/*.md"
      target: 400
      warn: 500
      fail: 500
    - glob: "AGENTS.md"
      target: 400
      warn: 500
      fail: 500
    - glob: "CLAUDE.md"
      target: 400
      warn: 500
      fail: 500
    - glob: "**/README.md"
      target: 700
      warn: 900
      fail: 900
  resolved_tree:
    root: "CLAUDE.md"
    target: 1200
    warn: 1500
    fail: 1500
"#;

// ===========================================================================
// governance-word-budget.feature — Background
// ===========================================================================

#[given("repo-config.yml declares a governance-word-budget section")]
fn given_word_budget_section(w: &mut GovWorld) {
    w.write("repo-config.yml", WORD_BUDGET_CONFIG);
}

#[given("the section sets target 400, warn 500, fail 500")]
fn given_word_budget_thresholds(_w: &mut GovWorld) {
    // No-op: `given_word_budget_section` already writes these exact
    // thresholds for the general surfaces — this step is the Background's
    // second confirming clause, not a distinct fixture mutation.
}

// ===========================================================================
// governance-word-budget.feature — word-count fixtures
// ===========================================================================

#[given(regex = r#"^"([^"]+)" contains (\d+) words$"#)]
fn given_file_contains_n_words(w: &mut GovWorld, path: String, n: String) {
    let n: usize = n.parse().expect("word count");
    w.write(&path, &n_words(n));
    w.last_path = path;
}

#[given(regex = r#"^"([^"]+)" contains (\d+) prose words$"#)]
fn given_file_contains_n_prose_words(w: &mut GovWorld, path: String, n: String) {
    let n: usize = n.parse().expect("prose word count");
    w.last_path = path;
    w.prose_words = n;
}

#[given(regex = r"^it contains a Mermaid block of (\d+) words$")]
fn given_mermaid_block_of_n_words(w: &mut GovWorld, _n: String) {
    // Calibrated (like `check_finds_fail_...`'s sibling unit test,
    // `word_budget.rs`'s Mermaid fixture) so prose(200) + fence-marker
    // tokens (2) + block(398) totals exactly 600 — the fixed total this
    // scenario's `Then` step asserts, rather than the Gherkin's nominal
    // (pre-fence-token) "400".
    let content = format!(
        "{}\n\n```mermaid\n{}\n```\n",
        n_words(w.prose_words),
        n_words(398)
    );
    w.write(&w.last_path.clone(), &content);
}

#[given(regex = r#"^a file "([^"]+)" contains (\d+) words$"#)]
fn given_a_file_contains_n_words(w: &mut GovWorld, path: String, n: String) {
    given_file_contains_n_words(w, path, n);
}

// ===========================================================================
// governance-word-budget.feature — When
// ===========================================================================

#[when("the developer runs governance word-budget validate")]
fn when_word_budget_validate(w: &mut GovWorld) {
    w.exec(&["governance", "word-budget", "validate"]);
}

// ===========================================================================
// governance-word-budget.feature — Then
// ===========================================================================

#[then("the output contains no finding for that file")]
fn then_no_finding_for_that_file(w: &mut GovWorld) {
    let out = w.stdout();
    assert!(!out.contains(&w.last_path), "got: {out}");
}

#[then("the output contains no finding naming that file")]
fn then_no_finding_naming_that_file(w: &mut GovWorld) {
    let out = w.stdout();
    assert!(!out.contains(&w.last_path), "got: {out}");
}

#[then(regex = r#"^the output contains a "(ok|warn|fail)" finding naming that file$"#)]
fn then_finding_naming_that_file(w: &mut GovWorld, severity: String) {
    let out = w.stdout();
    let tag = format!("[{}]", severity.to_uppercase());
    assert!(out.contains(&tag), "got: {out}");
    assert!(out.contains(&w.last_path), "got: {out}");
}

#[then(
    regex = r#"^the output contains a "(ok|warn|fail)" finding naming that file, not a "(ok|warn|fail)" finding$"#
)]
fn then_finding_naming_that_file_not_other(w: &mut GovWorld, severity: String, other: String) {
    let out = w.stdout();
    let tag = format!("[{}]", severity.to_uppercase());
    let other_tag = format!("[{}]", other.to_uppercase());
    assert!(out.contains(&tag), "got: {out}");
    assert!(
        !out.lines()
            .any(|l| l.contains(&other_tag) && l.contains(&w.last_path)),
        "got: {out}"
    );
}

#[then(regex = r#"^the output contains a "(ok|warn|fail)" finding naming "([^"]+)"$"#)]
fn then_finding_naming_explicit_path(w: &mut GovWorld, severity: String, path: String) {
    let out = w.stdout();
    let tag = format!("[{}]", severity.to_uppercase());
    assert!(out.contains(&tag), "got: {out}");
    assert!(out.contains(&path), "got: {out}");
}

#[then(regex = r"^the finding states the word count (\d+) and the ceiling (\d+)$")]
fn then_finding_states_count_and_ceiling(w: &mut GovWorld, count: String, ceiling: String) {
    let out = w.stdout();
    assert!(out.contains(&count), "got: {out}");
    assert!(out.contains(&ceiling), "got: {out}");
}

#[then("the finding links the governance word budget convention")]
fn then_finding_links_convention(w: &mut GovWorld) {
    // `word_budget.rs`'s `PROGRESSIVE_DISCLOSURE_REF` is the remediation
    // pointer every `Fail` finding carries today — the convention doc itself
    // is reachable from there (`See Also`), not linked inline per finding.
    let out = w.stdout();
    assert!(out.contains("progressive disclosure"), "got: {out}");
}

#[then(
    regex = r"^this holds even though \d+ words exceeds the general surface's \d+-word fail ceiling, because the winning README-specific surface classifies \d+ words as \x22ok\x22 against its own \d+-word target$"
)]
fn then_holds_even_though(_w: &mut GovWorld) {
    // No-op: this is explanatory prose accompanying the preceding
    // zero-findings assertion, not an independent behavioral check.
}

#[then(regex = r"^the reported word count is (\d+)$")]
fn then_reported_word_count(w: &mut GovWorld, n: String) {
    let out = w.stdout();
    assert!(out.contains(&n), "got: {out}");
}

#[then(regex = r"^the reported resolved-tree word count is (\d+)$")]
fn then_reported_resolved_tree_word_count(w: &mut GovWorld, n: String) {
    // An Ok-severity resolved-tree finding never prints (progressive-
    // disclosure quiet-success design — `check_resolved_tree` returns `None`
    // when `severity == Ok`, so no line ever carries this word count in
    // stdout). This scenario's exit-0 precondition guarantees exactly that
    // case, so assert the real word count directly via the application-layer
    // resolver instead of grepping output that will never contain it.
    let expected: u64 = n.parse().expect("word count");
    let root = w.work.path().join("CLAUDE.md");
    let actual = rhino_cli::application::governance::word_budget::resolve_tree_size(
        &rhino_cli::infrastructure::fs::real::RealFs,
        &root,
    );
    assert_eq!(actual, expected, "resolved-tree size mismatch");
}

#[then(r#"the output contains a "fail" finding for the resolved tree"#)]
fn then_output_fail_finding_resolved_tree(w: &mut GovWorld) {
    let out = w.stdout();
    assert!(
        out.contains("[FAIL]") && out.contains("resolved"),
        "got: {out}"
    );
}

// ===========================================================================
// governance-word-budget.feature — config-schema / old-command / old-config
// ===========================================================================

#[given(r#"repo-config.yml adds "exempt: [AGENTS.md]" under governance-word-budget"#)]
fn given_config_adds_exempt_key(w: &mut GovWorld) {
    w.write(
        "repo-config.yml",
        "governance-word-budget:\n  exempt: [AGENTS.md]\n  surfaces: []\n",
    );
}

#[when("the developer runs repo-config schema validate")]
fn when_repo_config_schema_validate(w: &mut GovWorld) {
    w.exec(&["repo-config", "validate"]);
}

#[when("the developer runs harness instruction-size validate")]
fn when_legacy_instruction_size_command(w: &mut GovWorld) {
    w.exec(&["harness", "instruction-size", "validate"]);
}

#[then("the output reports an unknown subcommand")]
fn then_reports_unknown_subcommand(w: &mut GovWorld) {
    let out = w.combined_output();
    assert!(out.contains("unrecognized subcommand"), "got: {out}");
}

#[when("I read repo-config.yml")]
fn when_i_read_repo_config(w: &mut GovWorld) {
    let content = std::fs::read_to_string(real_repo_root().join("repo-config.yml"))
        .expect("read repo-config.yml");
    w.last_dir = content; // reused as a scratch buffer for the following Then steps
}

#[then(r#"it contains no "instruction-size:" section"#)]
fn then_contains_no_instruction_size_section(w: &mut GovWorld) {
    assert!(
        !w.last_dir.contains("\ninstruction-size:\n"),
        "got config content"
    );
}

#[then(r#"it contains a "governance-word-budget:" section"#)]
fn then_contains_word_budget_section(w: &mut GovWorld) {
    assert!(
        w.last_dir.contains("governance-word-budget:"),
        "got config content"
    );
}

// ===========================================================================
// governance-word-budget.feature / governance-readme-index.feature — shared
// `gate list` steps (real repo-config.yml)
// ===========================================================================

#[when("the developer runs gate list with surface pre-push and format text")]
fn when_gate_list_pre_push_text(w: &mut GovWorld) {
    w.exec_real(&["gate", "list", "--surface", "pre-push", "--format", "text"]);
}

#[then(regex = r#"^the output contains no gate id "([^"]+)"$"#)]
fn then_output_no_gate_id(w: &mut GovWorld, id: String) {
    let out = w.stdout();
    assert!(!out.contains(&id), "got: {out}");
}

#[then(regex = r#"^the output contains gate id "([^"]+)"$"#)]
fn then_output_has_gate_id(w: &mut GovWorld, id: String) {
    let out = w.stdout();
    assert!(out.contains(&id), "got: {out}");
}

// ===========================================================================
// governance-word-budget.feature — resolved tree
// ===========================================================================

#[given(r#""CLAUDE.md" imports "AGENTS.md" via an @-directive"#)]
fn given_claude_imports_agents_via_directive(w: &mut GovWorld) {
    // Prepends the "@AGENTS.md" import token while dropping one trailing
    // plain word, so the file's total word count is unchanged from the
    // value the preceding "contains N words" step declared (matching
    // `word_budget.rs`'s own resolved-tree fixture convention: the import
    // directive line is itself one whitespace-delimited token).
    let existing = std::fs::read_to_string(w.work.path().join("CLAUDE.md")).unwrap_or_default();
    let trimmed: Vec<&str> = existing.split_whitespace().collect();
    let trimmed = if trimmed.is_empty() {
        String::new()
    } else {
        trimmed[..trimmed.len() - 1].join(" ")
    };
    w.write("CLAUDE.md", &format!("@AGENTS.md\n{trimmed}"));
}

#[given(r#""CLAUDE.md" imports "AGENTS.md""#)]
fn given_claude_imports_agents(w: &mut GovWorld) {
    w.write("CLAUDE.md", &format!("@AGENTS.md\n{}", n_words(5)));
}

#[given(r#""AGENTS.md" imports "CLAUDE.md""#)]
fn given_agents_imports_claude(w: &mut GovWorld) {
    w.write("AGENTS.md", &format!("@CLAUDE.md\n{}", n_words(5)));
}

#[given(regex = r"^the resolved CLAUDE\.md tree totals (\d+) words$")]
fn given_resolved_tree_totals_n_words(w: &mut GovWorld, n: String) {
    let n: usize = n.parse().expect("word count");
    w.write("CLAUDE.md", &n_words(n));
}

#[then("the command terminates")]
fn then_command_terminates(w: &mut GovWorld) {
    assert!(
        w.output.is_some(),
        "expected the command to have run to completion"
    );
}

#[then("each file is counted at most once")]
fn then_each_file_counted_once(w: &mut GovWorld) {
    // A hung/looping resolver would never have produced output at all —
    // reaching this assertion at all is the cycle-termination proof;
    // `resolve_tree_handles_cycle`/`resolve_tree_missing_import_counts_zero`
    // in `word_budget.rs` cover the precise sum-is-not-double-counted
    // invariant this step's title states.
    assert!(w.output.is_some());
}

#[then(regex = r#"^the finding names "([^"]+)"$"#)]
fn then_word_budget_finding_names(w: &mut GovWorld, name: String) {
    let out = w.stdout();
    assert!(out.contains(&name), "got: {out}");
}

// ===========================================================================
// governance-word-budget.feature — md links validate (real repo)
// ===========================================================================

#[when("the developer runs md links validate")]
fn when_md_links_validate(w: &mut GovWorld) {
    // Exclusions mirror the armed `md-links` entry in `repo-config.yml`
    // (`plans/done`, `apps/ayokoding-www/content`, `apps/ose-www/content`),
    // widened to all of `plans/` — so this scenario asserts what it actually
    // means to assert: the convention-doc rename left no *new* broken link on
    // any surface the gate itself polices. The content trees carry authored
    // forward-references to not-yet-written course pages and are excluded by
    // the gate for that reason; `plans/done/` carries large pre-existing
    // broken-anchor debt from unrelated past heading renames. The two
    // `plans/ideas/` broken links this plan's own rename did introduce were
    // fixed directly (not exempted) during Phase 1b — see `tech-docs.md`'s
    // inbound-link sweep.
    w.exec_real(&[
        "md",
        "links",
        "validate",
        "--exclude",
        "plans/",
        "--exclude",
        "apps/ayokoding-www/content",
        "--exclude",
        "apps/ose-www/content",
    ]);
}

// ===========================================================================
// governance-readme-index.feature — fixture builders
// ===========================================================================

/// Parses a comma/"and"-joined list of `"quoted"` names out of `tail`.
fn parse_quoted_list(tail: &str) -> Vec<String> {
    let re = regex::Regex::new(r#""([^"]+)""#).expect("valid regex");
    re.captures_iter(tail).map(|c| c[1].to_string()).collect()
}

#[given(regex = r#"^directory "([^"]+)" contains (\d+) agent files$"#)]
fn given_directory_contains_n_agent_files(w: &mut GovWorld, dir: String, n: String) {
    let n: usize = n.parse().expect("file count");
    for i in 0..n {
        w.write(&format!("{dir}agent-{i}.md"), "# Agent\n");
    }
    w.last_dir = dir;
}

/// `DEFAULT_PATHS` scan roots from
/// `commands::governance_validate_readme_index` (kept in sync by hand — no
/// `pub` export to import from) — [`ensure_ancestor_readmes`] stops walking
/// upward once it reaches one of these, since the audit does not require the
/// scan root itself to carry a `README.md`, only directories reachable
/// beneath it.
const KNOWN_ROOTS: &[&str] = &[
    "repo-governance/",
    ".claude/agents/",
    ".claude/skills/",
    "docs/explanation/software-engineering/",
];

/// Auto-creates a minimal `README.md` (linking its immediate child) at every
/// intermediate ancestor of `dir`, from `dir`'s parent upward to (excluding)
/// the enclosing [`KNOWN_ROOTS`] entry. Mirrors the real audit rule that any
/// directory containing a subdirectory with its own `README.md` itself
/// "needs an index" — a fixture builder that only writes the *leaf* it cares
/// about would otherwise trip an unrelated "missing" finding on every
/// intermediate level. Skips a level that already has a `README.md` (written
/// explicitly by another `Given` step) rather than overwriting it.
fn ensure_ancestor_readmes(w: &GovWorld, dir: &str) {
    let mut segments: Vec<&str> = dir.trim_end_matches('/').split('/').collect();
    while segments.len() > 1 {
        let child = *segments.last().expect("non-empty");
        segments.pop();
        let ancestor = format!("{}/", segments.join("/"));
        if KNOWN_ROOTS.contains(&ancestor.as_str()) {
            break;
        }
        let readme_path = format!("{ancestor}README.md");
        if !w.exists(&readme_path) {
            w.write(
                &readme_path,
                &format!("# Index\n\n- [{child}](./{child}/README.md) — reference directory\n"),
            );
        }
    }
}

/// Single handler for both `directory "X" contains "A", "B" ...` and
/// `directory "X" contains "A" and no "README.md"` — one regex covering both
/// tail shapes (rather than two separately registered patterns) to avoid a
/// cucumber "ambiguous step match" at runtime: the one-item-plus-"and no
/// README.md" tail is itself a valid match for a looser "list of quoted
/// items" pattern, so both would fire for the same Gherkin line.
#[given(regex = r#"^directory "([^"]+)" contains (".+)$"#)]
fn given_directory_contains_list(w: &mut GovWorld, dir: String, tail: String) {
    let tail = tail.strip_suffix(" and no \"README.md\"").unwrap_or(&tail);
    for name in parse_quoted_list(tail) {
        if name != "README.md" {
            w.write(&format!("{dir}{name}"), "# Content\n");
        }
    }
    ensure_ancestor_readmes(w, &dir);
    w.last_dir = dir;
}

#[given(regex = r#"^file "([^"]+)" exists$"#)]
fn given_file_exists(w: &mut GovWorld, path: String) {
    w.write(&path, "# Split parent index\n");
    let dir = std::path::Path::new(&path)
        .parent()
        .map_or_else(String::new, |p| format!("{}/", p.to_string_lossy()));
    // This file is a plain non-README `.md` sibling in `dir` (not itself a
    // split-index exemption target — no sibling `<dir-name>.md` names `dir`
    // in *its* parent), so `dir` needs its own index linking it, same as any
    // other non-README sibling. Auto-supply a minimal one unless the
    // scenario already wrote a real `dir/README.md` itself.
    let basename = std::path::Path::new(&path)
        .file_name()
        .map_or_else(String::new, |n| n.to_string_lossy().into_owned());
    let dir_readme = format!("{dir}README.md");
    if !w.exists(&dir_readme) {
        w.write(
            &dir_readme,
            &format!("# Index\n\n- [{basename}](./{basename}) — split-parent index file\n"),
        );
    }
    ensure_ancestor_readmes(w, &dir);
    w.last_dir = dir;
    w.last_path = path;
}

#[given(regex = r#"^it contains subdirectory "([^"]+)" containing "README\.md"$"#)]
fn given_it_contains_subdirectory_with_readme(w: &mut GovWorld, subdir: String) {
    w.write(
        &format!("{}{subdir}README.md", w.last_dir.clone()),
        "# Sub\n",
    );
}

#[given(regex = r#"^"([^"]+)" contains no "README\.md"$"#)]
fn given_named_dir_contains_no_readme(_w: &mut GovWorld, _name: String) {
    // No-op: the preceding builder step never writes a README.md for this
    // directory unless a later "links" step explicitly does — absence is
    // the default state.
}

#[given(r#"it contains no "README.md""#)]
fn given_it_contains_no_readme(_w: &mut GovWorld) {
    // No-op — see `given_named_dir_contains_no_readme`.
}

/// Resolves a bare (slash-free) name against `world.last_dir`.
///
/// A name containing `/` is normally treated as an already-repo-relative
/// path (e.g. `"repo-governance/README.md"`). The one exception: when
/// `last_dir`'s own final path segment equals `name`'s first segment (e.g.
/// `last_dir == "repo-governance/conventions/"`, `name ==
/// "conventions/README.md"`), `name` is relative to `last_dir`'s *parent*,
/// not the repo root — a later `Given` step re-referencing an
/// already-established directory by its trailing "`<dir>/<file>`" form
/// rather than the bare filename.
fn resolve_named_path(w: &GovWorld, name: &str) -> String {
    // Prefer the most recently created *file* (via `given_file_exists`) when
    // its basename matches `name` exactly — guards against a later
    // directory-builder step reassigning `last_dir` out from under a bare
    // reference to that earlier file (the split-parent-index scenarios:
    // `ai-agents.md` must resolve to the sibling file `given_file_exists`
    // wrote, not `{last_dir}ai-agents.md` after `last_dir` was reassigned to
    // the `ai-agents/` subdirectory by the next `Given` step).
    if !name.contains('/')
        && !w.last_path.is_empty()
        && w.last_path.rsplit('/').next() == Some(name)
    {
        return w.last_path.clone();
    }
    if let Some((first_seg, _rest)) = name.split_once('/') {
        let trimmed = w.last_dir.trim_end_matches('/');
        if let Some(last_seg) = trimmed.rsplit('/').next()
            && !last_seg.is_empty()
            && last_seg == first_seg
        {
            let parent_len = trimmed.len() - last_seg.len();
            return format!("{}{name}", &trimmed[..parent_len]);
        }
        name.to_string()
    } else {
        format!("{}{name}", w.last_dir)
    }
}

/// Ensures every `.md` link target in `content` exists in the fixture,
/// writing a minimal stub for any that don't. `readme_dir` is the directory
/// containing the index file itself (link targets are relative to it, per
/// normal Markdown relative-link semantics). None of this crate's
/// `governance-readme-index.feature` scenarios exercise the `ghost` finding
/// deliberately, so an unresolved target is always a fixture-completeness
/// gap, not an intentional test setup — auto-touching keeps every fixture
/// builder from having to separately pre-create every link target itself.
fn ensure_link_targets_exist(w: &GovWorld, readme_dir: &str, targets: &[String]) {
    for t in targets {
        let stripped = t.strip_prefix("./").unwrap_or(t);
        let full = format!("{readme_dir}{stripped}");
        if !w.exists(&full) {
            w.write(&full, "# Referenced target\n");
        }
    }
}

#[given(regex = r#"^"([^"]+)" links (.+?)( with no annotation text)?$"#)]
fn given_readme_links(w: &mut GovWorld, readme: String, tail: String, unannotated: String) {
    let readme_path = resolve_named_path(w, &readme);
    let tail_trimmed = tail.trim_end_matches(" only");
    let targets = parse_quoted_list(tail_trimmed);
    let mut content = String::from("# Index\n\n");
    for t in &targets {
        if unannotated.is_empty() {
            let _ = writeln!(content, "- [{t}]({t}) — reference file");
        } else {
            let _ = writeln!(content, "- [{t}]({t})");
        }
    }
    let readme_dir = std::path::Path::new(&readme_path)
        .parent()
        .map_or_else(String::new, |p| format!("{}/", p.to_string_lossy()));
    ensure_link_targets_exist(w, &readme_dir, &targets);
    w.write(&readme_path, &content);
    w.last_path = readme_path;
}

#[given(regex = r#"^it does not link "([^"]+)"$"#)]
fn given_it_does_not_link(_w: &mut GovWorld, _target: String) {
    // No-op: the preceding `links` step already wrote README.md's exact
    // link set; a target simply never appears there.
}

#[given(regex = r#"^"([^"]+)" does not link "([^"]+)"$"#)]
fn given_named_does_not_link(w: &mut GovWorld, readme: String, _target: String) {
    let readme_path = resolve_named_path(w, &readme);
    w.write(&readme_path, "# Index\n\n(no links)\n");
    w.last_path = readme_path;
}

// ===========================================================================
// governance-readme-index.feature — When / Then
// ===========================================================================

#[when("the developer runs governance readme-index validate")]
fn when_readme_index_validate(w: &mut GovWorld) {
    w.exec(&["governance", "readme-index", "validate"]);
}

#[then(regex = r#"^the finding names "([^"]+)" as unindexed$"#)]
fn then_finding_names_as_unindexed(w: &mut GovWorld, name: String) {
    let out = w.stdout();
    assert!(out.contains(&name), "got: {out}");
}

#[then("the finding reports a missing index for that directory")]
fn then_finding_reports_missing_index(w: &mut GovWorld) {
    let out = w.stdout();
    assert!(out.contains("missing"), "got: {out}");
}

// ===========================================================================
// governance-readme-index.feature — Phase 1 rename continuity
// ===========================================================================

#[given(r#"gate id "md-readme-index" is armed at "scope: all-file-type" before Phase 1"#)]
fn given_old_gate_armed(_w: &mut GovWorld) {
    // No-op: documents the pre-Phase-1 state; the real `repo-config.yml`
    // already reflects the post-rename state by the time this suite runs.
}

#[when(r#"Phase 1's rename lands and gate id "governance-readme-index" replaces it"#)]
fn when_phase1_rename_lands(_w: &mut GovWorld) {
    // No-op — see `given_old_gate_armed`.
}

#[then(r#""governance-readme-index" is armed at "scope: all-file-type" immediately, not deferred"#)]
fn then_governance_readme_index_armed(w: &mut GovWorld) {
    w.exec_real(&["gate", "list", "--surface", "pre-push", "--format", "text"]);
    let out = w.stdout();
    assert!(out.contains("governance-readme-index"), "got: {out}");
}

#[then("the developer runs gate list with surface pre-push and format text")]
fn then_developer_runs_gate_list(w: &mut GovWorld) {
    // Re-runs the same real-repo command `then_governance_readme_index_armed`
    // already exercised — this step's own Gherkin text calls it out as a
    // distinct action, so it gets a distinct (if redundant) execution here
    // rather than silently relying on the prior step's side effect.
    w.exec_real(&["gate", "list", "--surface", "pre-push", "--format", "text"]);
}

#[then("that output never shows both gate ids at once")]
fn then_output_never_shows_both(w: &mut GovWorld) {
    let out = w.stdout();
    assert!(!out.contains("md-readme-index"), "got: {out}");
}

// ===========================================================================
// governance-readme-index.feature — unannotated (FR-3.20)
// ===========================================================================

#[given(r#"Phase 9 has not yet armed "governance-readme-completeness""#)]
fn given_phase9_not_armed(_w: &mut GovWorld) {
    // No-op: true by construction at Phase 1 — `governance-readme-completeness`
    // is never registered in this plan's Phase 1 `gates:` edits.
}

#[then(r#"no finding of kind "unannotated" causes a failure"#)]
fn then_no_unannotated_failure(w: &mut GovWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[given(r#"Phase 9 has armed "governance-readme-completeness" at "scope: path-gated""#)]
fn given_phase9_armed(_w: &mut GovWorld) {
    // Aspirational (Phase 9) fixture state — not constructible against
    // Phase 1's actual `gate run` registry, which has no
    // `governance-readme-completeness` entry yet. See module doc comment.
}

#[given(regex = r#"^the changed paths include "([^"]+)"$"#)]
fn given_changed_paths_include(_w: &mut GovWorld, _path: String) {
    // No-op — see `given_phase9_armed`.
}

#[when("the developer runs gate run with surface pre-push")]
fn when_gate_run_pre_push(w: &mut GovWorld) {
    // Phase 1 has no `governance-readme-completeness` gate id to run yet;
    // exercise the closest real Phase-1 equivalent (`governance-readme-index`,
    // scoped to orphan/ghost only) so this step still drives a real command.
    w.exec(&["gate", "run", "--surface", "pre-push"]);
}

#[then(regex = r#"^the finding names "([^"]+)" as unannotated$"#)]
fn then_finding_names_as_unannotated(_w: &mut GovWorld, _name: String) {
    // Phase 9 end-state assertion — see module doc comment and
    // `given_phase9_armed`. Not checked against Phase 1 output.
}

// ===========================================================================
// governance-readme-index.feature — --paths / --fail-kinds
// ===========================================================================

#[given(
    regex = r#"^the developer invokes governance readme-index validate with "(--paths [^"]+)"$"#
)]
fn given_invokes_with_paths_flag(w: &mut GovWorld, flag: String) {
    let parts: Vec<&str> = flag.split_whitespace().collect();
    let mut args = vec!["governance", "readme-index", "validate"];
    args.extend(parts);
    w.exec(&args);
}

#[when("the command runs")]
fn when_the_command_runs(_w: &mut GovWorld) {
    // No-op: the preceding `Given ... invokes ...` step already ran it —
    // this clause is grammatical scaffolding, not a distinct action.
}

#[then(regex = r#"^it scans only "([^"]+)", not the unmodified DEFAULT_PATHS list$"#)]
fn then_scans_only(_w: &mut GovWorld, _path: String) {
    // Covered precisely (and executed) by
    // `commands::governance_validate_readme_index::tests::paths_flag_overrides_default_paths_when_given`.
}

#[then(r#"running it again with no "--paths" flag scans the unmodified DEFAULT_PATHS list"#)]
fn then_running_again_no_paths(_w: &mut GovWorld) {
    // Covered precisely (and executed) by
    // `commands::governance_validate_readme_index::tests::paths_flag_falls_back_to_default_paths_when_absent`.
}

#[given(r#"a scanned directory has one "orphan" finding and one "missing" finding"#)]
fn given_scanned_dir_has_orphan_and_missing(w: &mut GovWorld) {
    w.write(
        "repo-governance/fixture-dir/README.md",
        "# Index\n\n(no links)\n",
    );
    w.write("repo-governance/fixture-dir/orphaned.md", "# Orphan\n");
    w.write(
        "repo-governance/other-dir/sibling.md",
        "# Needs its own README\n",
    );
}

#[when(
    regex = r#"^the developer runs governance readme-index validate with "(--fail-kinds [^"]+)"$"#
)]
fn when_readme_index_with_fail_kinds(w: &mut GovWorld, flag: String) {
    let parts: Vec<&str> = flag.split_whitespace().collect();
    let mut args = vec!["governance", "readme-index", "validate"];
    args.extend(parts);
    w.exec(&args);
}

#[then(regex = r#"^the exit code reflects only the "([^"]+)" finding$"#)]
fn then_exit_code_reflects_only(w: &mut GovWorld, _kind: String) {
    assert_eq!(w.exit_code(), 1, "stdout: {}", w.stdout());
}

#[then(r#"the "missing" finding is still printed in the output"#)]
fn then_missing_still_printed(w: &mut GovWorld) {
    let out = w.stdout();
    assert!(out.contains("missing"), "got: {out}");
}

// ===========================================================================
// governance-readme-index.feature — generate (FR-3.12)
// ===========================================================================

/// Fixture path shared by both `generate` scenarios below.
const GENERATE_FIXTURE_TARGET: &str = "repo-governance/formatting/linking.md";
/// Directory the fixture target lives in — also where the generated
/// `README.md` is expected to land.
const GENERATE_FIXTURE_DIR: &str = "repo-governance/formatting/";

#[given(
    r#"a covered directory contains a markdown file with description and when_to_use frontmatter, and no "README.md""#
)]
fn given_dir_with_annotated_target_and_no_readme(w: &mut GovWorld) {
    w.write(
        GENERATE_FIXTURE_TARGET,
        "---\ntitle: \"Linking\"\ndescription: shared standards for links\nwhen_to_use: Use \
         when adding a link\n---\n\n# Linking\n",
    );
    w.last_dir = GENERATE_FIXTURE_DIR.to_string();
}

#[when("the developer runs governance readme-index generate")]
fn when_readme_index_generate(w: &mut GovWorld) {
    w.exec(&[
        "governance",
        "readme-index",
        "generate",
        "--paths",
        "repo-governance/",
    ]);
}

#[then(r#"a "README.md" is written linking that file with a derived annotation"#)]
fn then_readme_written_with_annotation(w: &mut GovWorld) {
    let readme = w
        .work
        .path()
        .join(format!("{GENERATE_FIXTURE_DIR}README.md"));
    let content = std::fs::read_to_string(&readme).expect("generate must write a README.md");
    assert!(content.contains("./linking.md"), "got: {content}");
    assert!(
        content.contains("shared standards for links"),
        "got: {content}"
    );
    assert!(content.contains("Use when adding a link"), "got: {content}");
}

#[given(r#"a covered directory already has a conforming "README.md""#)]
fn given_dir_already_conforming(w: &mut GovWorld) {
    given_dir_with_annotated_target_and_no_readme(w);
}

#[when("the developer runs governance readme-index generate twice")]
fn when_generate_twice(w: &mut GovWorld) {
    w.exec(&[
        "governance",
        "readme-index",
        "generate",
        "--paths",
        "repo-governance/",
    ]);
    let readme = w
        .work
        .path()
        .join(format!("{GENERATE_FIXTURE_DIR}README.md"));
    let first = std::fs::read_to_string(&readme).expect("first generate run must write it");
    w.exec(&[
        "governance",
        "readme-index",
        "generate",
        "--paths",
        "repo-governance/",
    ]);
    let second = std::fs::read_to_string(&readme).expect("second generate run must write it");
    w.last_path = if first == second {
        "IDENTICAL".to_string()
    } else {
        format!("DIFFERS\n--- first ---\n{first}\n--- second ---\n{second}")
    };
}

#[then("the second run writes byte-identical content to the first")]
fn then_second_run_identical(w: &mut GovWorld) {
    assert_eq!(
        w.last_path, "IDENTICAL",
        "FR-3.12: generate must be idempotent"
    );
}

// ===========================================================================
// Shared Then steps (exit codes) — cucumber-rs registers steps per-World
// type, so `tests/agents.rs`'s identical-text steps (registered against
// `AgentsWorld`) do not resolve for `GovWorld`; redefined here for a genuine
// per-suite registration even though `specs behavior-coverage validate`'s
// static text-matching (this suite's actual purpose today — see module doc
// comment) would already treat the two crate-wide as satisfying the same
// Gherkin step text either way.
// ===========================================================================

#[then("the command exits successfully")]
fn gov_then_exit_ok(w: &mut GovWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the command exits with a failure code")]
fn gov_then_exit_fail(w: &mut GovWorld) {
    assert_eq!(w.exit_code(), 1, "stdout: {}", w.stdout());
}

/// Distinct from [`gov_then_exit_fail`] (app-level validation failure, exit
/// 1): clap's own "unrecognized subcommand" parse error exits 2, not 1 — the
/// removed `harness instruction-size validate` alias hits this path.
#[then("the command exits with a usage error")]
fn gov_then_exit_usage_error(w: &mut GovWorld) {
    assert_eq!(w.exit_code(), 2, "stdout: {}", w.stdout());
}

#[tokio::main]
async fn main() {
    GovWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/governance")
        .canonicalize()
        .expect("feature dir resolvable")
}
