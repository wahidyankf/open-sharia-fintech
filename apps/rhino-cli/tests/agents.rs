//! Cucumber-rs integration tests for the whole `harness` command group
//! (`harness bindings generate/validate`, `harness claude validate`,
//! `harness sync validate`,
//! `harness duplication validate`, `harness instruction-size validate`,
//! `harness audit`) plus the governance-meta facts the `instruction-size`
//! gate depends on
//! (`repo-governance audit` category wiring, the pre-push hook trigger, and
//! the convention/workflow/checker docs that describe the gate). Some feature
//! file names and Gherkin step text still say "agents" for historical reasons
//! — the underlying CLI subcommands live under the `harness` and `governance`
//! nouns today; see `gherkin/harness/README.md`.
//!
//! Wires the behavior-contract feature files at
//! `specs/apps/rhino/behavior/rhino-cli/gherkin/harness/` to step definitions that
//! synthesize `.claude/` and `.opencode/` fixtures inside a fresh git-rooted
//! temp workspace and drive the compiled `rhino-cli` binary, asserting on
//! output and exit code. A handful of scenarios assert facts about the real
//! repository tree this crate lives in (governance docs, the `.husky/pre-push`
//! hook) rather than the synthetic fixture — see `real_repo_root()`.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::needless_pass_by_value)] // cucumber-rs binds regex captures by value
#![allow(clippy::panic)] // panic!() in an unreachable match arm inside a test step
#![allow(clippy::format_collect)] // idiomatic fixture-body builder: (0..n).map(format!).collect()

use std::fmt::Write as _;
use std::path::PathBuf;
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use rhino_cli::application::agents::bindings::{KNOWN_BINDING_DIRS, expected_bindings};
use serde_json::Value;
use tempfile::TempDir;

/// Feature-level tags owned by a *different* runner over the same shared
/// `gherkin/harness/` directory. Every sibling runner takes exactly its own
/// tags; this runner takes everything else. One list rather than one constant
/// per sibling, so adding a runner is a single entry here and a forgotten
/// entry cannot hide behind a differently-named constant.
///
/// | Tag                          | Owning runner              |
/// | ---------------------------- | -------------------------- |
/// | `codex-binding`              | `tests/codex_binding.rs`   |
/// | `agents-skills-mirror`       | `tests/skills_mirror.rs`   |
/// | `vendored-skill-preservation`| `tests/skills_mirror.rs`   |
/// | `opencode-skills-removal`    | `tests/skills_mirror.rs`   |
/// | `binding-ownership`          | `tests/harness_ownership.rs` |
/// | `sync-triage`                | `tests/harness_sync_triage.rs` |
/// | `opencode-conformance`       | `tests/opencode_conformance.rs` |
/// | `catalog-generation`         | `tests/harness_catalog.rs` |
const FOREIGN_TAGS: &[&str] = &[
    "codex-binding",
    "agents-skills-mirror",
    "vendored-skill-preservation",
    "opencode-skills-removal",
    "binding-ownership",
    "sync-triage",
    "opencode-conformance",
    "catalog-generation",
];

/// Shared scenario state. Each scenario gets a fresh git-rooted temp workspace
/// so the binary's `findGitRoot` resolves inside the fixture.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct AgentsWorld {
    work: TempDir,
    /// Extra CLI args (flags) for the next exec.
    extra_args: Vec<String>,
    output: Option<Output>,
    /// Dropped-harness binding paths the purge scenario checks.
    purge_paths: Vec<String>,
    /// `(path, tracked-file-count)` pairs the purge scenario collected.
    purge_tracked: Vec<(String, usize)>,
    /// Simulated `git diff --name-only` push range for pre-push-hook scenarios.
    push_range_files: Vec<String>,
    /// Whether the simulated pre-push instruction-size gate triggered.
    hook_invoked: bool,
    /// Directory recorded by a governance-meta "When I look under ..." step.
    lookup_dir: String,
    /// Content of the file most recently confirmed to exist by a
    /// governance-meta "Then ... exists" step; consumed by the following step.
    lookup_file_content: String,
}

impl std::fmt::Debug for AgentsWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("AgentsWorld")
            .field("extra_args", &self.extra_args)
            .finish_non_exhaustive()
    }
}

impl AgentsWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        init_git_repo(work.path());
        Self {
            work,
            extra_args: Vec::new(),
            output: None,
            purge_paths: Vec::new(),
            purge_tracked: Vec::new(),
            push_range_files: Vec::new(),
            hook_invoked: false,
            lookup_dir: String::new(),
            lookup_file_content: String::new(),
        }
    }

    fn write(&self, rel: &str, content: &str) {
        let p = self.work.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk fixture dir");
        }
        std::fs::write(p, content).expect("write fixture");
    }

    /// Writes a valid Claude agent file under `.claude/agents/`.
    fn write_claude_agent(&self, name: &str, model: &str, skills: &[&str]) {
        let mut content = format!(
            "---\nname: {name}\ndescription: Agent {name}.\ntools: Read, Write\nmodel: {model}\ncolor: blue\n"
        );
        if !skills.is_empty() {
            content.push_str("skills:\n");
            for s in skills {
                let _ = writeln!(content, "  - {s}");
            }
        }
        content.push_str("---\n# Body\n");
        self.write(&format!(".claude/agents/{name}.md"), &content);
    }

    /// Writes a valid Claude skill directory.
    fn write_claude_skill(&self, name: &str) {
        self.write(
            &format!(".claude/skills/{name}/SKILL.md"),
            &format!("---\nname: {name}\ndescription: Skill {name}.\n---\n# Skill body\n"),
        );
    }

    fn bin() -> PathBuf {
        cargo_bin("rhino-cli")
    }

    fn exec(&mut self, base: &[&str]) {
        let mut args: Vec<String> = base.iter().map(|s| (*s).to_string()).collect();
        args.extend(self.extra_args.iter().cloned());
        args.push("--no-color".to_string());
        let out = std::process::Command::new(Self::bin())
            .args(&args)
            .current_dir(self.work.path())
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    fn stdout(&self) -> String {
        String::from_utf8_lossy(&self.output.as_ref().expect("ran").stdout).into_owned()
    }

    /// Concatenates stdout and stderr, mirroring how a developer watching the
    /// terminal sees both streams interleaved. `harness audit`'s aggregate
    /// pass/fail summary and per-member failure lines are written to stderr.
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

fn run_git(dir: &std::path::Path, args: &[&str]) {
    std::process::Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git command");
}

/// Initialises a minimal real git repo so `findGitRoot` resolves here.
fn init_git_repo(dir: &std::path::Path) {
    run_git(dir, &["init", "-q"]);
}

// ===========================================================================
// agents sync — Given steps
// ===========================================================================

#[given("a .claude/ directory with valid agents and skills")]
#[given("a .claude/ directory with agents and skills to convert")]
#[given("a .claude/ directory with both agents and skills")]
fn given_claude_agents_and_skills(w: &mut AgentsWorld) {
    // `--harness <name>` is validated against the registry, so a fixture repo
    // needs the same repo-config.yml a real repository has.
    write_three_harness_registry(w);
    w.write_claude_skill("my-skill");
    w.write_claude_agent("foo-maker", "sonnet", &["my-skill"]);
    w.write_claude_agent("bar-checker", "haiku", &[]);
}

#[given(regex = r#"^a \.claude/ agent configured with the "([a-z]+)" model$"#)]
fn given_claude_model_agent(w: &mut AgentsWorld, model: String) {
    write_three_harness_registry(w);
    w.write_claude_agent("foo-maker", &model, &[]);
}

// ===========================================================================
// agents sync — When steps
// ===========================================================================

#[when("the developer runs agents sync")]
fn when_sync(w: &mut AgentsWorld) {
    w.exec(&["harness", "bindings", "generate", "--harness", "opencode"]);
}

#[when("the developer runs agents sync with the --dry-run flag")]
fn when_sync_dry_run(w: &mut AgentsWorld) {
    w.exec(&[
        "harness",
        "bindings",
        "generate",
        "--harness",
        "opencode",
        "--dry-run",
    ]);
}

#[when("the developer runs agents sync with the --agents-only flag")]
fn when_sync_agents_only(w: &mut AgentsWorld) {
    // `harness bindings generate` has no per-step `--agents-only` flag: the
    // OpenCode sync step never copies skills either way (OpenCode reads
    // `.claude/skills/<name>/SKILL.md` natively), so the plain opencode-only
    // invocation already exhibits the "agents only" behavior this scenario checks.
    w.exec(&["harness", "bindings", "generate", "--harness", "opencode"]);
}

// ===========================================================================
// agents sync — Then steps
// ===========================================================================

#[then("the .opencode/ directory contains the converted configuration")]
fn then_opencode_has_config(w: &mut AgentsWorld) {
    let p = w.work.path().join(".opencode/agents/foo-maker.md");
    assert!(p.exists(), "expected {} to exist", p.display());
    let content = std::fs::read_to_string(&p).expect("read converted agent");
    assert!(
        content.contains("model: zai-coding-plan/glm-5.2"),
        "got: {content}"
    );
    assert!(
        content.contains("permission:\n  read: allow\n  write: allow"),
        "got: {content}"
    );
}

#[then("the output describes the planned operations")]
fn then_output_describes_plan(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Agents: 2 converted"), "got: {out}");
}

#[then("no files are written to the .opencode/ directory")]
fn then_no_opencode_files(w: &mut AgentsWorld) {
    let p = w.work.path().join(".opencode/agents/foo-maker.md");
    assert!(
        !p.exists(),
        "expected {} NOT to exist after dry-run",
        p.display()
    );
}

#[then("only agent files are written to the .opencode/ directory")]
fn then_only_agents_written(w: &mut AgentsWorld) {
    // Agents are written; skills are never copied (read natively).
    assert!(w.work.path().join(".opencode/agents/foo-maker.md").exists());
    assert!(!w.work.path().join(".opencode/skills").exists());
    assert!(!w.work.path().join(".opencode/skill").exists());
}

#[then(r#"the corresponding .opencode/ agent uses the "zai-coding-plan/glm-5.2" model identifier"#)]
fn then_opencode_model_minimax(w: &mut AgentsWorld) {
    let content =
        std::fs::read_to_string(w.work.path().join(".opencode/agents/foo-maker.md")).expect("read");
    assert!(
        content.contains("model: zai-coding-plan/glm-5.2"),
        "got: {content}"
    );
}

// ===========================================================================
// agents validate-sync — Given steps
// ===========================================================================

/// Writes a synced pair: a Claude agent and its byte-correct OpenCode form.
fn write_synced_pair(w: &AgentsWorld, name: &str) {
    w.write_claude_agent(name, "", &[]);
    w.write(
        &format!(".opencode/agents/{name}.md"),
        &format!(
            "---\ndescription: Agent {name}.\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n  write: allow\n---\n# Body\n"
        ),
    );
}

#[given(".claude/ and .opencode/ configurations that are fully synchronised")]
fn given_fully_synced(w: &mut AgentsWorld) {
    write_synced_pair(w, "foo-maker");
    write_synced_pair(w, "bar-checker");
}

#[given("an agent in .claude/ whose description differs from its .opencode/ counterpart")]
fn given_description_mismatch(w: &mut AgentsWorld) {
    write_synced_pair(w, "foo-maker");
    // Overwrite the opencode side with a different description.
    w.write(
        ".opencode/agents/foo-maker.md",
        "---\ndescription: A totally different description.\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n  write: allow\n---\n# Body\n",
    );
}

#[given(".claude/ containing more agents than .opencode/")]
fn given_count_mismatch(w: &mut AgentsWorld) {
    write_synced_pair(w, "foo-maker");
    // Extra Claude agent with no OpenCode counterpart.
    w.write_claude_agent("bar-checker", "", &[]);
}

// ===========================================================================
// agents validate-sync — When/Then steps
// ===========================================================================

#[when("the developer runs agents validate-sync")]
fn when_validate_sync(w: &mut AgentsWorld) {
    w.exec(&["harness", "sync", "validate"]);
}

#[then("the output reports all sync checks as passing")]
fn then_sync_all_passing(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Failed: 0"), "got: {out}");
    assert!(out.contains("VALIDATION PASSED"), "got: {out}");
}

#[then("the output identifies the agent with the mismatched description")]
fn then_identifies_desc_mismatch(w: &mut AgentsWorld) {
    let out = w.stdout();
    // The sync validator names agents by agent name, not by filename.
    assert!(out.contains("Agent: foo-maker"), "got: {out}");
    assert!(out.contains("Description mismatch"), "got: {out}");
}

#[then("the output reports the agent count mismatch")]
fn then_reports_count_mismatch(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Agent Count"), "got: {out}");
    assert!(
        out.contains("missing one or more Claude agents"),
        "got: {out}"
    );
}

// ===========================================================================
// agents validate-claude — Given steps
// ===========================================================================

#[given("a .claude/ directory where all agents and skills are valid")]
fn given_all_valid(w: &mut AgentsWorld) {
    w.write_claude_skill("my-skill");
    w.write_claude_agent("foo-maker", "", &["my-skill"]);
}

#[given(r#"a .claude/ directory where one agent is missing the required "description" field"#)]
fn given_missing_description(w: &mut AgentsWorld) {
    w.write_claude_skill("my-skill");
    w.write(
        ".claude/agents/foo-maker.md",
        "---\nname: foo-maker\ntools: Read\nmodel:\ncolor: blue\n---\n# Body\n",
    );
}

#[given("a .claude/ directory containing two agent files declaring the same name")]
fn given_duplicate_name(w: &mut AgentsWorld) {
    // Two files; both declare name `dup-maker`. The filename-match rule will
    // also flag one, but the uniqueness rule fires on the second by name.
    w.write(
        ".claude/agents/dup-maker.md",
        "---\nname: dup-maker\ndescription: d\ntools: Read\nmodel:\ncolor: blue\n---\n# Body\n",
    );
    w.write(
        ".claude/agents/other-maker.md",
        "---\nname: dup-maker\ndescription: d\ntools: Read\nmodel:\ncolor: blue\n---\n# Body\n",
    );
}

#[given("a .claude/ directory where agents are valid but skills have issues")]
fn given_valid_agents_bad_skills(w: &mut AgentsWorld) {
    // Skill missing description (invalid), but agent does not reference it.
    w.write(
        ".claude/skills/broken/SKILL.md",
        "---\nname: broken\n---\n# body\n",
    );
    w.write_claude_agent("foo-maker", "", &[]);
}

#[given("a .claude/ directory where skills are valid but agents have issues")]
fn given_valid_skills_bad_agents(w: &mut AgentsWorld) {
    w.write_claude_skill("my-skill");
    // Agent with an invalid color (issue), but we will only validate skills.
    w.write(
        ".claude/agents/foo-maker.md",
        "---\nname: foo-maker\ndescription: d\ntools: Read\nmodel:\ncolor: chartreuse\n---\n# Body\n",
    );
}

// ===========================================================================
// agents validate-claude — When/Then steps
// ===========================================================================

#[when("the developer runs agents validate-claude")]
fn when_validate_claude(w: &mut AgentsWorld) {
    w.exec(&["harness", "claude", "validate"]);
}

#[when("the developer runs agents validate-claude with the --agents-only flag")]
fn when_validate_claude_agents_only(w: &mut AgentsWorld) {
    w.exec(&["harness", "claude", "validate", "--agents-only"]);
}

#[when("the developer runs agents validate-claude with the --skills-only flag")]
fn when_validate_claude_skills_only(w: &mut AgentsWorld) {
    w.exec(&["harness", "claude", "validate", "--skills-only"]);
}

#[then("the output reports all checks as passing")]
fn then_claude_all_passing(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Failed: 0"), "got: {out}");
    assert!(out.contains("VALIDATION PASSED"), "got: {out}");
}

#[then("the output identifies the agent and the missing field")]
fn then_identifies_missing_field(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("foo-maker.md"), "got: {out}");
    assert!(out.contains("Required Fields"), "got: {out}");
    assert!(out.contains("description"), "got: {out}");
}

#[then("the output reports the duplicate agent name")]
fn then_reports_duplicate(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Name Uniqueness"), "got: {out}");
    assert!(out.contains("dup-maker"), "got: {out}");
}

// ===========================================================================
// agents detect-duplication (harness duplication validate)
// ===========================================================================

#[given("a repository with agent and skill files whose bodies share no 10-line verbatim windows")]
fn given_no_shared_duplication(w: &mut AgentsWorld) {
    let body_a: String = (0..12)
        .map(|i| format!("Alpha unique line {i}\n"))
        .collect();
    let body_b: String = (0..12)
        .map(|i| format!("Beta distinct line {i}\n"))
        .collect();
    w.write(
        ".claude/agents/alpha-widget.md",
        &format!("---\nname: alpha-widget\n---\n{body_a}"),
    );
    w.write(
        ".claude/skills/beta-skill/SKILL.md",
        &format!("---\nname: beta-skill\n---\n{body_b}"),
    );
}

#[given("a repository with two agent files that share 12 consecutive lines verbatim")]
fn given_two_agents_sharing_12_lines(w: &mut AgentsWorld) {
    // Different domains ("alpha" vs "beta") AND different role suffixes
    // (-maker vs -checker) — not exempt as a sanctioned template family.
    let shared: String = (0..12)
        .map(|i| format!("Shared workflow line {i}\n"))
        .collect();
    w.write(
        ".claude/agents/alpha-maker.md",
        &format!("---\nname: alpha-maker\n---\n{shared}"),
    );
    w.write(
        ".claude/agents/beta-checker.md",
        &format!("---\nname: beta-checker\n---\n{shared}"),
    );
}

#[given("a repository with an agent file whose body matches 11 consecutive lines of a SKILL.md")]
fn given_agent_matches_skill_body(w: &mut AgentsWorld) {
    let shared: String = (0..11)
        .map(|i| format!("Shared prose line {i}\n"))
        .collect();
    w.write(
        ".claude/agents/gadget-widget.md",
        &format!("---\nname: gadget-widget\n---\n{shared}"),
    );
    w.write(
        ".claude/skills/other-thing/SKILL.md",
        &format!("---\nname: other-thing\n---\n{shared}"),
    );
}

#[given(
    "a repository where two agent files share a 10-line window composed only of headings or blank lines"
)]
fn given_heading_only_window(w: &mut AgentsWorld) {
    let shared: String = (0..10).map(|i| format!("## Heading {i}\n")).collect();
    w.write(
        ".claude/agents/one-widget.md",
        &format!("---\nname: one-widget\n---\n{shared}"),
    );
    w.write(
        ".claude/agents/two-widget.md",
        &format!("---\nname: two-widget\n---\n{shared}"),
    );
}

#[when("the developer runs agents detect-duplication")]
fn when_detect_duplication(w: &mut AgentsWorld) {
    w.exec(&["harness", "duplication", "validate"]);
}

#[then("the output reports zero duplication clusters")]
fn then_zero_duplication_clusters(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("PASSED: 0 clusters"), "got: {out}");
}

#[then("the output identifies the duplicated cluster across both agents")]
fn then_identifies_cluster_across_agents(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("alpha-maker.md"), "got: {out}");
    assert!(out.contains("beta-checker.md"), "got: {out}");
}

#[then("the output identifies the duplicated cluster across the agent and the skill")]
fn then_identifies_cluster_across_agent_and_skill(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("gadget-widget.md"), "got: {out}");
    assert!(out.contains("SKILL.md"), "got: {out}");
}

// ===========================================================================
// harness bindings generate / validate
// ===========================================================================

impl AgentsWorld {
    /// Writes a platform-bindings catalog naming every known binding
    /// directory (a safe superset — referencing an absent directory is
    /// harmless; only an undocumented *present* directory fails validation).
    fn write_full_catalog(&self) {
        self.write(
            "docs/reference/platform-bindings.md",
            "# Platform Bindings\n\nDirectories: .claude, .opencode, .codex, .agents, .github\n",
        );
    }

    /// Creates only the two directories the `OpenCode` sync-equivalence check
    /// needs (`.claude/agents`, `.opencode/agents`, both empty so 0 == 0
    /// trivially matches). Leaves every other known binding directory absent.
    fn make_sync_dirs(&self) {
        std::fs::create_dir_all(self.work.path().join(".claude/agents")).expect("mk agents dir");
        std::fs::create_dir_all(self.work.path().join(".opencode/agents")).expect("mk agents dir");
    }
}

/// Absolute path of the repository this test binary was built from, used by
/// the purge scenario to assert against real tracked files rather than a
/// synthetic fixture (the claim under test is about this repository).
fn built_from_repo_root() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .ancestors()
        .find(|dir| dir.join(".git").exists())
        .expect("test binary must be built inside a git repository")
        .to_path_buf()
}

#[given(
    ".cursor/ tracked 93 files, .amazonq/ tracked 2 files, and .pi/ tracked 1 file before the purge"
)]
fn given_dropped_binding_dirs_were_tracked(w: &mut AgentsWorld) {
    w.purge_paths = vec![
        ".cursor".to_string(),
        ".amazonq".to_string(),
        ".pi".to_string(),
    ];
}

#[when("git ls-files is run against those three paths after the purge")]
fn when_git_ls_files_dropped_paths(w: &mut AgentsWorld) {
    let root = built_from_repo_root();
    w.purge_tracked.clear();
    for path in w.purge_paths.clone() {
        let out = std::process::Command::new("git")
            .arg("-C")
            .arg(&root)
            .args(["ls-files", "--", &path])
            .output()
            .expect("run git ls-files");
        let listed = String::from_utf8_lossy(&out.stdout)
            .lines()
            .filter(|l| !l.trim().is_empty())
            .count();
        w.purge_tracked.push((path, listed));
    }
}

#[then("each returns zero tracked files")]
fn then_each_returns_zero_tracked_files(w: &mut AgentsWorld) {
    for (path, count) in &w.purge_tracked {
        assert_eq!(*count, 0, "{path} still has {count} tracked file(s)");
    }
    assert_eq!(w.purge_tracked.len(), 3, "all three paths must be checked");
}

#[then(
    "harness bindings validate exits successfully, where before the purge it required .amazonq/ byte-parity"
)]
fn then_bindings_validate_passes_without_amazonq(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
    w.make_sync_dirs();
    w.write_full_catalog();
    w.exec(&["harness", "bindings", "validate"]);
    assert!(
        w.output.as_ref().expect("ran").status.success(),
        "got: {}",
        w.stdout()
    );
}

#[given("a repository whose generated binding files match the generated content")]
fn given_generated_files_match(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
    w.make_sync_dirs();
}

#[given("the platform-bindings catalog references every present binding directory")]
fn given_catalog_references_everything_present(w: &mut AgentsWorld) {
    w.write_full_catalog();
}

#[given(
    "a repository with a known binding directory that the platform-bindings catalog does not reference"
)]
fn given_catalog_missing_dir_row(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
    w.make_sync_dirs();
    // `.codex` is present on disk but the catalog below omits it.
    std::fs::create_dir_all(w.work.path().join(".codex")).expect("mk .codex");
    w.write(
        "docs/reference/platform-bindings.md",
        "# Platform Bindings\n\nDirectories: .claude, .opencode\n",
    );
}

#[given("a repository where some known binding directories do not exist on disk")]
fn given_some_binding_dirs_absent(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
    w.make_sync_dirs();
    // .codex, .agents and .github are intentionally never created.
    w.write(
        "docs/reference/platform-bindings.md",
        "# Platform Bindings\n\nDirectories: .claude, .opencode\n",
    );
}

#[given("a repository whose .codex/agents directory holds a standalone .toml agent file")]
fn given_codex_agents_holds_toml(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
    w.make_sync_dirs();
    w.write_full_catalog();
    w.write(
        ".codex/agents/probe-maker.toml",
        "description = \"probe\"\n",
    );
}

#[given("a repository whose .codex/agents directory holds a .md agent file")]
fn given_codex_agents_holds_md(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
    w.make_sync_dirs();
    w.write_full_catalog();
    w.write(".codex/agents/probe-maker.md", "# probe\n");
}

#[then("the output names .toml as the officially-correct extension")]
fn then_output_names_toml_extension(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains(".toml"), "got: {out}");
    assert!(out.contains("probe-maker.md"), "got: {out}");
}

#[when("the developer runs harness bindings validate")]
fn when_validate_bindings(w: &mut AgentsWorld) {
    // `--verbose` so absent-directory "no catalog row required" pass-checks
    // are visible in the output for the last scenario's assertion; harmless
    // for every other scenario (only adds an "All Checks:" section).
    w.exec(&["harness", "bindings", "validate", "--verbose"]);
}

#[then("the output reports all binding checks as passing")]
fn then_all_binding_checks_passing(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Failed: 0"), "got: {out}");
    assert!(out.contains("VALIDATION PASSED"), "got: {out}");
}

#[then("the output identifies the binding directory missing a catalog row")]
fn then_identifies_binding_dir_missing_catalog_row(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Catalog Coverage: .codex"), "got: {out}");
    assert!(out.contains("absent from catalog"), "got: {out}");
}

#[then("no catalog row is required for the absent binding directories")]
fn then_no_catalog_row_required_for_absent_dirs(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(
        out.contains("absent on disk; no catalog row required"),
        "got: {out}"
    );
}

// ===========================================================================
// Instruction-size shared fixture helper
// ===========================================================================

/// Writes a `repo-config.yml` with an `instruction-size:` section covering
/// `AGENTS.md` (with the given `target`/`fail` and `warn` equal to the fail
/// ceiling) and, unless `single_surface` is set, `.codex/**/*.md`
/// too, plus a `resolved_tree` rooted at `CLAUDE.md` matching the real
/// convention doc's thresholds
/// (`repo-governance/conventions/structure/governance-word-budget.md`).
/// Shared by every `governance word-budget validate` scenario in this file
/// (the standalone `governance-word-budget.yaml` file the Gherkin prose
/// still names was folded into this `repo-config.yml` section — see
/// `application/repo_config/mod.rs`).
fn write_word_budget_config_scoped(w: &AgentsWorld, target: u64, fail: u64, single_surface: bool) {
    let warn = fail;
    let mut yaml = format!(
        "harness: []\n\
         coverage:\n  projects: []\n\
         specs:\n  ddd-areas: []\n  domain-areas: []\n\
         governance-word-budget:\n\
         \x20 surfaces:\n\
         \x20   - glob: \"AGENTS.md\"\n\
         \x20     target: {target}\n\
         \x20     warn: {warn}\n\
         \x20     fail: {fail}\n"
    );
    if !single_surface {
        yaml.push_str(
            "\x20   - glob: \".codex/**/*.md\"\n\
             \x20     target: 650\n\
             \x20     warn: 750\n\
             \x20     fail: 750\n",
        );
    }
    yaml.push_str(
        "\x20 resolved_tree:\n\
         \x20   root: \"CLAUDE.md\"\n\
         \x20   target: 1200\n\
         \x20   warn: 1350\n\
         \x20   fail: 1500\n",
    );
    w.write("repo-config.yml", &yaml);
}

/// Convenience wrapper for [`write_word_budget_config_scoped`] covering
/// both `AGENTS.md` and `.codex/**/*.md` — the shape every
/// scenario except the "legacy registry-merge alias" (single-surface) one needs.
fn write_word_budget_config(w: &AgentsWorld, target: u64, fail: u64) {
    write_word_budget_config_scoped(w, target, fail, false);
}

/// Builds a whitespace-delimited fixture of exactly `n` words.
fn n_words(n: usize) -> String {
    vec!["w"; n].join(" ")
}

/// Root of the real monorepo containing this crate (two levels up from
/// `apps/rhino-cli`). Used by governance-meta scenarios that assert facts
/// about the real repository tree — governance docs, workflow docs, agent
/// instruction files, and `.husky/pre-push` — rather than the synthetic
/// git-rooted fixture every other scenario in this file drives the binary
/// against.
fn real_repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .expect("repo root resolvable")
}

// ===========================================================================
// Governance of the word-budget rule
// (governance-word-budget-rule.feature) — asserts facts
// about the real repository tree this crate lives in, not the synthetic
// fixture. See `real_repo_root()`.
// ===========================================================================

/// Reads a governance document the way its author sees it: the parent
/// `<name>.md` plus every child in the sibling `<name>/` directory that
/// progressive disclosure split it into. Asserting against the parent alone
/// would fail the moment a document is split, even though nothing about the
/// rule changed.
fn read_document_tree(rel: &str) -> String {
    let parent = real_repo_root().join(rel);
    let mut out = std::fs::read_to_string(&parent).unwrap_or_else(|e| panic!("read {rel}: {e}"));
    let children = parent.with_extension("");
    if children.is_dir() {
        let mut paths: Vec<PathBuf> = std::fs::read_dir(&children)
            .expect("read split-children directory")
            .filter_map(Result::ok)
            .map(|e| e.path())
            .filter(|p| p.extension().is_some_and(|x| x == "md"))
            .collect();
        paths.sort();
        for child in paths {
            out.push('\n');
            out.push_str(&std::fs::read_to_string(&child).expect("read split child"));
        }
    }
    out
}

/// Reads an agent's full instruction surface: its own definition plus every
/// skill it declares in `skills:` (each skill's `SKILL.md` and every file under
/// its `reference/`). Agent-Skill separation moves procedural detail out of the
/// agent body, so a rule the agent must follow commonly lives in a skill.
fn read_agent_surface(agent_rel: &str) -> String {
    let root = real_repo_root();
    let agent = root.join(agent_rel);
    let mut out =
        std::fs::read_to_string(&agent).unwrap_or_else(|e| panic!("read {agent_rel}: {e}"));
    let mut in_skills = false;
    let mut declared: Vec<String> = Vec::new();
    for line in out.lines() {
        if line.starts_with("skills:") {
            in_skills = true;
            continue;
        }
        if in_skills {
            if let Some(name) = line.strip_prefix("  - ") {
                declared.push(name.trim().to_string());
            } else {
                in_skills = false;
            }
        }
    }
    for skill in declared {
        let dir = root.join(".claude/skills").join(&skill);
        let mut paths: Vec<PathBuf> = vec![dir.join("SKILL.md")];
        if dir.join("reference").is_dir() {
            let mut refs: Vec<PathBuf> = std::fs::read_dir(dir.join("reference"))
                .expect("read skill reference directory")
                .filter_map(Result::ok)
                .map(|e| e.path())
                .filter(|p| p.extension().is_some_and(|x| x == "md"))
                .collect();
            refs.sort();
            paths.extend(refs);
        }
        for path in paths {
            if let Ok(text) = std::fs::read_to_string(&path) {
                out.push('\n');
                out.push_str(&text);
            }
        }
    }
    out
}

#[given("the plan is complete")]
fn given_the_plan_is_complete(_w: &mut AgentsWorld) {
    // No-op: this precondition is about the real repository's governance
    // artifacts already existing — the following `When`/`Then` steps read
    // them directly from `real_repo_root()`.
}

#[when(regex = r#"^I look under "([^"]+)"$"#)]
fn when_i_look_under(w: &mut AgentsWorld, dir: String) {
    w.lookup_dir = dir;
}

#[then(regex = r#"^"([^"]+)" exists$"#)]
fn then_file_exists_under_lookup_dir(w: &mut AgentsWorld, filename: String) {
    let path = real_repo_root().join(&w.lookup_dir).join(&filename);
    assert!(path.is_file(), "expected {} to exist", path.display());
    w.lookup_file_content = std::fs::read_to_string(&path).expect("read looked-up file");
}

#[then(
    "the file lists the monitored file classes, configured threshold source, and enforcement points"
)]
fn then_file_lists_class_budgets_enforcement(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(content.contains("Monitored Surfaces"), "got: {content}");
    assert!(content.contains("repo-config.yml"), "got: {content}");
    assert!(content.contains("target"), "got: {content}");
    assert!(content.contains("fail"), "got: {content}");
    assert!(content.contains("Enforcement Points"), "got: {content}");
}

#[when(r#""repo-rules-checker" runs Step 6"#)]
fn when_repo_rules_checker_runs_step_6(w: &mut AgentsWorld) {
    w.lookup_file_content = read_agent_surface(".claude/agents/repo/repo-rules-checker.md");
}

#[then("it reports qualitative bloat concerns across the whole instruction-file class")]
fn then_reports_qualitative_bloat(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(
        content.contains("qualitative concerns a mechanical gate cannot measure"),
        "checker must own the qualitative half of the budget rule"
    );
    assert!(
        content.contains("progressive disclosure"),
        "checker must name the sanctioned remediation"
    );
}

#[then(r#"it annotates that the word ceiling is enforced by the deterministic "governance-word-budget" gate"#)]
fn then_annotates_deterministic_ceiling(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(
        content.contains("enforced by the deterministic"),
        "got: {content}"
    );
    assert!(
        content.contains("governance word-budget validate"),
        "got: {content}"
    );
}

#[when(regex = r#"^I read "([^"]+)"$"#)]
fn when_i_read(w: &mut AgentsWorld, path: String) {
    w.lookup_file_content = read_document_tree(&path);
}

#[then(r#""governance-word-budget" is skipped locally and delegated from Step 0.5"#)]
fn then_word_budget_delegated_from_step_0_5(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(
        content.contains("governance-word-budget` skipped"),
        "got: {content}"
    );
    assert!(content.contains("`delegated-gate-ids`"), "got: {content}");
}

#[given("a repo with instruction files within the configured budgets")]
fn given_repo_within_budgets(_w: &mut AgentsWorld) {
    // No-op: a fresh fixture workspace has no instruction files at all, which
    // is trivially "within budget" — no `repo-config.yml` means
    // `merged_budget_config` returns `None` and the word-budget category
    // reports zero findings regardless of the other categories.
}

#[when(r#"the developer runs "rhino-cli repo-governance audit" with JSON output"#)]
fn when_repo_governance_audit_json(w: &mut AgentsWorld) {
    w.exec(&["repo-governance", "audit", "--output", "json"]);
}

#[then(r#"the envelope schema is "rhino-cli/repo-governance-audit/v1""#)]
fn then_envelope_schema(w: &mut AgentsWorld) {
    let out = w.stdout();
    let json: Value = serde_json::from_str(&out).expect("valid json");
    assert_eq!(json["schema"], "rhino-cli/repo-governance-audit/v1");
}

#[then(r#""result.categories" contains a category named "governance-word-budget""#)]
fn then_result_categories_contains_word_budget(w: &mut AgentsWorld) {
    let out = w.stdout();
    let json: Value = serde_json::from_str(&out).expect("valid json");
    let categories = json["result"]["categories"]
        .as_array()
        .expect("categories array");
    assert!(
        categories
            .iter()
            .any(|c| c["name"] == "governance-word-budget"),
        "got: {categories:?}"
    );
}

#[given(r#"lifecycle evidence contains a current "governance-word-budget" result"#)]
fn given_lifecycle_evidence_has_word_budget_result(_w: &mut AgentsWorld) {
    // No-op: this asserts static lifecycle processing-rule prose in
    // repo-rules-checker.md (read by the `When "repo-rules-checker" runs
    // Step 0.5` step below), not runnable CLI behavior.
}

#[when(r#""repo-rules-checker" runs Step 0.5"#)]
fn when_repo_rules_checker_runs_step_0_5(w: &mut AgentsWorld) {
    w.lookup_file_content = read_agent_surface(".claude/agents/repo/repo-rules-checker.md");
}

#[then(r#"it consumes the exact delegated gate ID "governance-word-budget""#)]
fn then_consumes_delegated_word_budget_gate(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(content.contains("`delegated-gate-ids`"), "got: {content}");
    assert!(
        content.contains("word budgets are all mechanically enforced"),
        "got: {content}"
    );
}

#[then("it does not re-derive word counts in Step 6")]
fn then_does_not_rederive_word_counts(w: &mut AgentsWorld) {
    let normalized = w
        .lookup_file_content
        .split_whitespace()
        .collect::<Vec<_>>()
        .join(" ");
    assert!(
        normalized.contains("Do not run or AI-rederive those predicates"),
        "checker must defer word counting to lifecycle-gate evidence rather than redoing it"
    );
}

// ===========================================================================
// Pre-push enforcement of the word-budget gate
// (governance-word-budget-pre-push.feature). The gate is an armed `gates:`
// entry as of Phase 9 of plans/done/2026-08-15__optimize-governance-md, so the
// trigger set is read from the LIVE registry rather than restated here. The
// earlier hand-written list mirrored the retired `instruction-size` gate and
// still named `.cursor/rules/`, `.amazonq/rules/`, `.windsurf/rules/`,
// `.junie/guidelines.md`, and `.github/copilot-instructions.md` — harnesses
// this repository dropped. A restated list drifts silently: it keeps passing
// while asserting a trigger set that no longer exists.
// ===========================================================================

/// The `governance-word-budget` gate's live pre-push trigger prefixes.
fn word_budget_trigger_prefixes() -> Vec<String> {
    let config = rhino_cli::application::repo_config::load(&real_repo_root())
        .expect("live repo-config.yml parses");
    let gate = config
        .gates
        .iter()
        .find(|gate| gate.id == "governance-word-budget")
        .expect("repo-config.yml registers a governance-word-budget gate");
    gate.surfaces
        .get(&rhino_cli::application::repo_config::GateSurface::PrePush)
        .expect("the gate declares a pre-push surface")
        .trigger
        .clone()
}

fn matches_word_budget_trigger(path: &str) -> bool {
    word_budget_trigger_prefixes()
        .iter()
        .any(|trigger| path == trigger || path.starts_with(trigger.as_str()))
}

#[given(r#"my push range modifies "AGENTS.md""#)]
fn given_push_range_modifies_agents_md(w: &mut AgentsWorld) {
    w.push_range_files = vec!["AGENTS.md".to_string()];
}

#[given(r#"my push range modifies "RTK.md""#)]
fn given_push_range_modifies_rtk_md(w: &mut AgentsWorld) {
    w.push_range_files = vec!["RTK.md".to_string()];
}

#[given(r#"my push range modifies only "apps/ose-www/src/page.tsx""#)]
fn given_push_range_modifies_unrelated_file(w: &mut AgentsWorld) {
    w.push_range_files = vec!["apps/ose-www/src/page.tsx".to_string()];
}

#[given(r#""AGENTS.md" exceeds its fail ceiling"#)]
fn given_agents_md_exceeds_fail_ceiling(w: &mut AgentsWorld) {
    write_word_budget_config(w, 650, 750);
    w.write("AGENTS.md", &n_words(800));
}

#[given(r#""AGENTS.md" is within its fail ceiling"#)]
fn given_agents_md_within_fail_ceiling(w: &mut AgentsWorld) {
    write_word_budget_config(w, 650, 750);
    w.write("AGENTS.md", &n_words(200));
}

#[when("the pre-push hook runs")]
fn when_pre_push_hook_runs(w: &mut AgentsWorld) {
    let triggered = w
        .push_range_files
        .iter()
        .any(|f| matches_word_budget_trigger(f));
    w.hook_invoked = triggered;
    if triggered {
        w.exec(&["governance", "word-budget", "validate"]);
    } else {
        w.output = None;
    }
}

#[then("the word-budget gate runs")]
fn then_word_budget_target_runs(w: &mut AgentsWorld) {
    assert!(
        w.hook_invoked,
        "expected the word-budget gate to trigger for this push range"
    );
    assert!(
        w.output.is_some(),
        "expected `governance word-budget validate` to have executed"
    );
    // The trigger decision above reads the live gate registry, so this proves
    // the current pre-push declaration invokes the validator.
}

#[then("the push is aborted with a non-zero exit")]
fn then_push_aborted(w: &mut AgentsWorld) {
    assert_ne!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the word-budget validation target is not invoked")]
fn then_word_budget_target_not_invoked(w: &mut AgentsWorld) {
    assert!(!w.hook_invoked);
    assert!(w.output.is_none());
}

#[then("the word-budget validation target runs and exits 0")]
fn then_word_budget_target_runs_exit_0(w: &mut AgentsWorld) {
    assert!(w.hook_invoked);
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the push proceeds")]
fn then_push_proceeds(w: &mut AgentsWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

// ===========================================================================
// harness audit steps (harness-audit.feature)
// ===========================================================================

#[given("a repository with no .claude or .opencode agent directories")]
fn given_harness_audit_no_dirs(_w: &mut AgentsWorld) {
    // No-op: a fresh fixture workspace has no `.claude/`, `.opencode/`, or
    // `repo-config.yml` at all, so `detect-duplication` trivially reports zero
    // violations while `validate-claude`, `validate-sync`, and
    // `validate-bindings` each fail on the missing directories/catalog.
}

#[when(regex = r#"^the developer runs "rhino-cli harness audit"$"#)]
fn when_run_harness_audit(w: &mut AgentsWorld) {
    w.exec(&["harness", "audit"]);
}

#[then(regex = r#"^the output names the failing "([a-z-]+)" harness validator$"#)]
#[allow(clippy::needless_pass_by_value)] // cucumber-rs binds the capture by value
fn then_harness_audit_names_failure(w: &mut AgentsWorld, member: String) {
    let out = w.combined_output();
    assert!(out.contains("HARNESS AUDIT FAILED"), "got: {out}");
    assert!(out.contains(&member), "got: {out}");
}

// ===========================================================================
// Shared Then steps (exit codes)
// ===========================================================================

// ===========================================================================
// binding surface set — KNOWN_BINDING_DIRS and expected_bindings
// ===========================================================================

/// Surfaces belonging to harnesses this repository no longer supports. Any one
/// of them surviving in the compiled set is dead weight the purge missed.
const DROPPED_SURFACES: &[&str] = &[
    ".amazonq",
    ".cursor",
    ".pi",
    ".windsurf",
    ".junie",
    "GEMINI.md",
    "CONVENTIONS.md",
];

#[given("the compiled set of known binding directories")]
fn given_known_binding_dirs(_w: &mut AgentsWorld) {}

#[when("the set is inspected")]
#[when("the expected binding files are computed")]
fn when_binding_surface_inspected(_w: &mut AgentsWorld) {}

#[then("it contains exactly .claude, .opencode, .codex, .agents, and .github")]
fn then_known_dirs_are_the_five_survivors(_w: &mut AgentsWorld) {
    let mut actual: Vec<&str> = KNOWN_BINDING_DIRS.to_vec();
    actual.sort_unstable();
    let mut expected = vec![".agents", ".claude", ".codex", ".github", ".opencode"];
    expected.sort_unstable();
    assert_eq!(
        actual, expected,
        "KNOWN_BINDING_DIRS: {KNOWN_BINDING_DIRS:?}"
    );
}

#[then("it names no dropped harness surface")]
fn then_known_dirs_name_no_dropped_surface(_w: &mut AgentsWorld) {
    for dropped in DROPPED_SURFACES {
        assert!(
            !KNOWN_BINDING_DIRS.contains(dropped),
            "dropped surface {dropped:?} survives in KNOWN_BINDING_DIRS"
        );
    }
}

#[then("no expected file lives under a dropped harness surface")]
fn then_no_expected_file_under_dropped_surface(w: &mut AgentsWorld) {
    let root = w.work.path();
    let files = expected_bindings(root).expect("expected_bindings resolves");
    for file in &files {
        for dropped in DROPPED_SURFACES {
            assert!(
                !file.rel_path.starts_with(dropped),
                "expected binding {:?} lives under dropped surface {dropped:?}",
                file.rel_path
            );
        }
    }
}

// ===========================================================================
// harness bindings generate — registry-derived --harness name set
// ===========================================================================

/// Writes a three-entry registry matching the repository's own, so the fixture
/// exercises the same lookup production uses rather than a bespoke shape.
fn write_three_harness_registry(w: &AgentsWorld) {
    w.write(
        "repo-config.yml",
        concat!(
            "harness:\n",
            "  - { name: claude-code, tier: source, agent-dir: .claude/agents, skills-dir: .claude/skills }\n",
            "  - name: opencode\n",
            "    tier: generated\n",
            "    agent-dir: .opencode/agents\n",
            "    mirrors: .claude/agents\n",
            "  - name: codex\n",
            "    tier: generated\n",
            "    agent-dir: .codex/agents\n",
            "    mirrors: .claude/agents\n",
            "coverage:\n  projects: []\n",
        ),
    );
}

#[given("the repo-config.yml harness registry declares codex")]
#[given("the repo-config.yml harness registry does not declare cursor")]
fn given_three_harness_registry(w: &mut AgentsWorld) {
    write_three_harness_registry(w);
}

#[when("the developer runs harness bindings generate for codex")]
fn when_generate_for_codex(w: &mut AgentsWorld) {
    w.exec(&["harness", "bindings", "generate", "--harness", "codex"]);
}

#[when("the developer runs harness bindings generate for cursor")]
fn when_generate_for_cursor(w: &mut AgentsWorld) {
    w.exec(&["harness", "bindings", "generate", "--harness", "cursor"]);
}

#[then("the harness name is not rejected as unknown")]
fn then_harness_name_accepted(w: &mut AgentsWorld) {
    let out = w.combined_output();
    assert!(
        !out.contains("unknown harness name"),
        "a registry-declared harness name must not be rejected; got: {out}"
    );
}

#[then("the error names the registry-derived accepted set")]
fn then_error_names_registry_set(w: &mut AgentsWorld) {
    let out = w.combined_output();
    assert!(
        out.contains("unknown harness name"),
        "an unregistered harness name must be rejected; got: {out}"
    );
    for expected in ["claude-code", "opencode", "codex"] {
        assert!(
            out.contains(expected),
            "the error must list the registry-derived accepted set; \
             missing {expected} in: {out}"
        );
    }
}

#[then("the command exits successfully")]
fn then_exit_ok(w: &mut AgentsWorld) {
    assert_eq!(w.exit_code(), 0, "stdout: {}", w.stdout());
}

#[then("the command exits with a failure code")]
fn then_exit_fail(w: &mut AgentsWorld) {
    assert_eq!(w.exit_code(), 1, "stdout: {}", w.stdout());
}

/// Distinct from [`then_exit_fail`] (app-level validation failure, exit 1):
/// clap's own "unrecognized subcommand" parse error exits 2, not 1 — the
/// removed `harness instruction-size validate` alias hits this path.
#[then("the command exits with a usage error")]
fn then_exit_usage_error(w: &mut AgentsWorld) {
    assert_eq!(w.exit_code(), 2, "stdout: {}", w.stdout());
}

#[tokio::main]
async fn main() {
    AgentsWorld::cucumber()
        .fail_on_skipped()
        // Several features live in the same `gherkin/harness/` directory but
        // are owned by sibling runners. Skipping them here (and taking only
        // them there) keeps one step-definition set per runner; without the
        // split each runner meets the other's undefined steps and
        // `fail_on_skipped` turns those into failures.
        .filter_run_and_exit(feature_dir(), |feature, _rule, _scenario| {
            !feature
                .tags
                .iter()
                .any(|t| FOREIGN_TAGS.contains(&t.as_str()))
        })
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/harness")
        .canonicalize()
        .expect("feature dir resolvable")
}
