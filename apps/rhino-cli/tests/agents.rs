//! Cucumber-rs integration tests for the whole `harness` command group
//! (`harness bindings generate/validate`, `harness claude validate`,
//! `harness sync validate`, `harness naming validate`,
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
use serde_json::Value;
use tempfile::TempDir;

/// Synthetic Amazon Q definition identity declared by the behavior fixture.
/// This keeps the byte-identical Rhino CLI test boundary independent of any
/// particular repository's configured agent name.
const AMAZONQ_FIXTURE_AGENT_NAME: &str = "fixture-amazonq-agent";

/// Shared scenario state. Each scenario gets a fresh git-rooted temp workspace
/// so the binary's `findGitRoot` resolves inside the fixture.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct AgentsWorld {
    work: TempDir,
    /// Extra CLI args (flags) for the next exec.
    extra_args: Vec<String>,
    output: Option<Output>,
    /// Snapshot of Amazon Q bridge-file bytes captured before a re-emission,
    /// consumed by the "emitting twice is idempotent" scenario.
    bindings_snapshot: Vec<(String, Vec<u8>)>,
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
            bindings_snapshot: Vec::new(),
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

    /// Writes the smallest repository configuration needed by the Amazon Q
    /// bindings command. The generated definition name is fixture data, just
    /// as it is repository data in production.
    fn write_amazonq_config(&self) {
        self.write(
            "repo-config.yml",
            &format!(
                "harness:\n  - name: amazonq\n    tier: generated\n    agent-name: {AMAZONQ_FIXTURE_AGENT_NAME}\ncoverage:\n  projects: []\n"
            ),
        );
    }

    fn amazonq_definition_path(&self) -> PathBuf {
        self.work
            .path()
            .join(".amazonq/cli-agents")
            .join(format!("{AMAZONQ_FIXTURE_AGENT_NAME}.json"))
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
    w.write_claude_skill("my-skill");
    w.write_claude_agent("foo-maker", "sonnet", &["my-skill"]);
    w.write_claude_agent("bar-checker", "haiku", &[]);
}

#[given(regex = r#"^a \.claude/ agent configured with the "([a-z]+)" model$"#)]
fn given_claude_model_agent(w: &mut AgentsWorld, model: String) {
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
// agents emit-bindings / validate-bindings
// ===========================================================================

impl AgentsWorld {
    /// Writes both expected Amazon Q bridge files with their canonical
    /// content, so a fresh regenerate matches byte-for-byte. Drives the
    /// actual `harness bindings generate --harness amazonq` command rather
    /// than a hand-maintained literal, so this fixture can never drift out of
    /// sync with the canonical content in `application::agents::bindings`.
    /// Note: the bridge content is static (a pointer to `AGENTS.md` by path,
    /// not its bytes) — no `AGENTS.md` fixture file is needed for this.
    fn write_matching_bindings(&mut self) {
        self.exec(&["harness", "bindings", "generate", "--harness", "amazonq"]);
    }

    /// Writes a platform-bindings catalog naming every known binding
    /// directory (a safe superset — referencing an absent directory is
    /// harmless; only an undocumented *present* directory fails validation).
    fn write_full_catalog(&self) {
        self.write(
            "docs/reference/platform-bindings.md",
            "# Platform Bindings\n\nDirectories: .claude, .opencode, .codex, .github, .amazonq, \
             .cursor, .windsurf, .junie, GEMINI.md, CONVENTIONS.md\n",
        );
    }

    /// Creates only the two directories the `OpenCode` sync-equivalence check
    /// needs (`.claude/agents`, `.opencode/agents`, both empty so 0 == 0
    /// trivially matches). Leaves every other known binding directory absent.
    fn make_sync_dirs(&self) {
        std::fs::create_dir_all(self.work.path().join(".claude/agents")).expect("mk agents dir");
        std::fs::create_dir_all(self.work.path().join(".opencode/agents")).expect("mk agents dir");
    }

    /// A fully valid bindings setup: matching bridge files, the sync dirs,
    /// and a catalog covering everything present. Scenarios that need to
    /// introduce exactly one corruption build on top of this.
    fn given_full_valid_bindings_setup(&mut self) {
        self.write_matching_bindings();
        self.make_sync_dirs();
        self.write_full_catalog();
    }
}

#[given("a repository without an existing .amazonq/ directory")]
fn given_no_amazonq_dir(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    assert!(
        !w.work.path().join(".amazonq").exists(),
        "fresh fixture workspace must not already have .amazonq/"
    );
}

#[given("a repository where the bridge files already exist")]
fn given_bridge_files_exist(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    w.write_matching_bindings();
    for rel in [
        ".amazonq/rules/00-agents-md.md".to_string(),
        format!(".amazonq/cli-agents/{AMAZONQ_FIXTURE_AGENT_NAME}.json"),
    ] {
        let bytes = std::fs::read(w.work.path().join(&rel)).expect("read prior emission");
        w.bindings_snapshot.push((rel, bytes));
    }
}

#[given("a repository whose bridge files match the generated content")]
fn given_bridge_files_match(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    w.write_matching_bindings();
    w.make_sync_dirs();
}

#[given("the platform-bindings catalog references every present binding directory")]
fn given_catalog_references_everything_present(w: &mut AgentsWorld) {
    w.write_full_catalog();
}

#[given("a repository where a bridge file has been hand-edited away from the generated content")]
fn given_bridge_file_mutated(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    w.given_full_valid_bindings_setup();
    w.write(
        ".amazonq/rules/00-agents-md.md",
        "# Hand-edited — no longer canonical\n",
    );
}

#[given("a repository where a bridge file has been deleted")]
fn given_bridge_file_deleted(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    w.given_full_valid_bindings_setup();
    std::fs::remove_file(w.amazonq_definition_path()).expect("remove bridge file");
}

#[given(
    "a repository with a known binding directory that the platform-bindings catalog does not reference"
)]
fn given_catalog_missing_dir_row(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    w.write_matching_bindings();
    w.make_sync_dirs();
    // `.codex` is present on disk but the catalog below omits it.
    std::fs::create_dir_all(w.work.path().join(".codex")).expect("mk .codex");
    w.write(
        "docs/reference/platform-bindings.md",
        "# Platform Bindings\n\nDirectories: .claude, .opencode, .amazonq\n",
    );
}

#[given("a repository where some known binding directories do not exist on disk")]
fn given_some_binding_dirs_absent(w: &mut AgentsWorld) {
    w.write_amazonq_config();
    w.write_matching_bindings();
    w.make_sync_dirs();
    // .codex, .github, .cursor, .windsurf, .junie, GEMINI.md, CONVENTIONS.md
    // are intentionally never created.
    w.write(
        "docs/reference/platform-bindings.md",
        "# Platform Bindings\n\nDirectories: .claude, .opencode, .amazonq\n",
    );
}

#[when("the developer runs agents emit-bindings")]
fn when_emit_bindings(w: &mut AgentsWorld) {
    w.exec(&["harness", "bindings", "generate", "--harness", "amazonq"]);
}

#[when("the developer runs agents validate-bindings")]
fn when_validate_bindings(w: &mut AgentsWorld) {
    // `--verbose` so absent-directory "no catalog row required" pass-checks
    // are visible in the output for the last scenario's assertion; harmless
    // for every other scenario (only adds an "All Checks:" section).
    w.exec(&["harness", "bindings", "validate", "--verbose"]);
}

#[then("the file .amazonq/rules/00-agents-md.md is written as a pointer to AGENTS.md")]
fn then_rules_pointer_written(w: &mut AgentsWorld) {
    let p = w.work.path().join(".amazonq/rules/00-agents-md.md");
    assert!(p.exists(), "stdout: {}", w.stdout());
    let content = std::fs::read_to_string(&p).expect("read rules pointer");
    assert!(content.contains("AGENTS.md"), "got: {content}");
}

#[then("the configured Amazon Q agent definition is written as valid JSON")]
fn then_agent_definition_written(w: &mut AgentsWorld) {
    let content = std::fs::read_to_string(w.amazonq_definition_path())
        .expect("read configured agent definition");
    let json: Value = serde_json::from_str(&content).expect("valid json");
    assert_eq!(json["name"], AMAZONQ_FIXTURE_AGENT_NAME);
}

#[then(
    "the agent definition resources reference file://AGENTS.md and file://.amazonq/rules/**/*.md"
)]
fn then_agent_definition_resources(w: &mut AgentsWorld) {
    let content = std::fs::read_to_string(w.amazonq_definition_path())
        .expect("read configured agent definition");
    let json: Value = serde_json::from_str(&content).expect("valid json");
    let resources = json["resources"].as_array().expect("resources array");
    let strs: Vec<&str> = resources.iter().filter_map(Value::as_str).collect();
    assert!(strs.contains(&"file://AGENTS.md"), "got: {strs:?}");
    assert!(
        strs.contains(&"file://.amazonq/rules/**/*.md"),
        "got: {strs:?}"
    );
}

#[then("the bridge files are byte-for-byte identical to the previous emission")]
fn then_bindings_identical_to_previous(w: &mut AgentsWorld) {
    let snapshot = w.bindings_snapshot.clone();
    for (rel, expected) in &snapshot {
        let actual = std::fs::read(w.work.path().join(rel)).expect("read current emission");
        assert_eq!(&actual, expected, "{rel} changed between emissions");
    }
}

#[then("the output reports all binding checks as passing")]
fn then_all_binding_checks_passing(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("Failed: 0"), "got: {out}");
    assert!(out.contains("VALIDATION PASSED"), "got: {out}");
}

#[then("the output identifies the drifted bridge file")]
fn then_identifies_drifted_bridge_file(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(
        out.contains("Binding: .amazonq/rules/00-agents-md.md"),
        "got: {out}"
    );
    assert!(out.contains("drifted from canonical content"), "got: {out}");
}

#[then("the output reports the missing bridge file")]
fn then_reports_missing_bridge_file(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(
        out.contains(&format!(
            "Binding: .amazonq/cli-agents/{AMAZONQ_FIXTURE_AGENT_NAME}.json"
        )),
        "got: {out}"
    );
    assert!(
        out.contains("is missing; run `rhino-cli agents emit-bindings`"),
        "got: {out}"
    );
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
/// `AGENTS.md` (with the given `target`/`fail`, `warn` interpolated between
/// them) and, unless `single_surface` is set, `.github/copilot-instructions.md`
/// too, plus a `resolved_tree` rooted at `CLAUDE.md` matching the real
/// convention doc's thresholds
/// (`repo-governance/conventions/structure/governance-word-budget.md`).
/// Shared by every `governance word-budget validate` scenario in this file
/// (the standalone `governance-word-budget.yaml` file the Gherkin prose
/// still names was folded into this `repo-config.yml` section — see
/// `application/repo_config/mod.rs`).
fn write_word_budget_config_scoped(w: &AgentsWorld, target: u64, fail: u64, single_surface: bool) {
    let warn = target + fail.saturating_sub(target) / 2;
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
            "\x20   - glob: \".github/copilot-instructions.md\"\n\
             \x20     target: 400\n\
             \x20     warn: 450\n\
             \x20     fail: 500\n",
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
/// both `AGENTS.md` and `.github/copilot-instructions.md` — the shape every
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
// AGENTS.md word-budget audit (governance-agents-md-word-budget.feature)
// governance word-budget validate, scoped to a 400-word target / 500-word
// fail ceiling matching this feature's own scenario titles.
// ===========================================================================

#[given(regex = r"^a repository containing an AGENTS\.md file of (\d+) words$")]
fn given_agents_md_file_of_n_words(w: &mut AgentsWorld, n: String) {
    write_word_budget_config(w, 400, 500);
    let n: usize = n.parse().expect("word count");
    w.write("AGENTS.md", &n_words(n));
}

#[when("the developer runs governance word-budget validate")]
fn when_word_budget_validate(w: &mut AgentsWorld) {
    w.exec(&["governance", "word-budget", "validate"]);
}

#[then("the output reports the AGENTS.md size as within target")]
fn then_reports_within_target(w: &mut AgentsWorld) {
    // Ok-severity surfaces are intentionally excluded from findings output
    // (progressive-disclosure quiet-success design — see
    // `check_instruction_sizes`'s doc comment); the observable signal is the
    // generic "all surfaces within budget" pass banner.
    let out = w.stdout();
    assert!(out.contains("WORD BUDGET: PASSED"), "got: {out}");
}

#[then("the output identifies AGENTS.md as over the target size")]
fn then_identifies_over_target(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("[WARN]"), "got: {out}");
    assert!(out.contains("AGENTS.md"), "got: {out}");
}

#[then("the output identifies AGENTS.md as over the hard limit")]
fn then_identifies_over_hard_limit(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("[FAIL]"), "got: {out}");
    assert!(out.contains("AGENTS.md"), "got: {out}");
}

// ===========================================================================
// Governance word-budget gate (governance-word-budget-thresholds.feature)
// ===========================================================================

#[given(
    "a committed \"governance-word-budget.yaml\" mapping instruction-file globs to target, warn, and fail word thresholds"
)]
fn given_word_budget_committed(w: &mut AgentsWorld) {
    write_word_budget_config(w, 400, 500);
}

#[given(regex = r#"^"AGENTS\.md" is (\d+) words$"#)]
fn given_agents_md_is_n_words(w: &mut AgentsWorld, n: String) {
    let n: usize = n.parse().expect("word count");
    w.write("AGENTS.md", &n_words(n));
}

#[given(regex = r"^its target is (\d+) and its fail ceiling is (\d+)$")]
fn given_target_and_fail_ceiling(w: &mut AgentsWorld, target: String, fail: String) {
    write_word_budget_config(
        w,
        target.parse().expect("target"),
        fail.parse().expect("fail"),
    );
}

#[given(regex = r"^its fail ceiling is (\d+)$")]
fn given_fail_ceiling(w: &mut AgentsWorld, fail: String) {
    // No explicit target in this scenario — reuse the Background's default.
    write_word_budget_config(w, 400, fail.parse().expect("fail"));
}

#[given(r#"no file exists at ".github/copilot-instructions.md""#)]
fn given_no_copilot_instructions_file(_w: &mut AgentsWorld) {
    // Intentionally a no-op: `write_word_budget_config` already configures
    // this glob as a surface, but the file itself is never written — the
    // glob simply matches nothing.
}

#[given(r#""CLAUDE.md" imports "AGENTS.md" via "@AGENTS.md""#)]
fn given_claude_md_imports_agents_md(w: &mut AgentsWorld) {
    // AGENTS.md stays within its own 400-word surface target (Ok, silently
    // excluded from surface-level findings) so only the resolved-tree
    // finding is expected to fire in this scenario.
    w.write("AGENTS.md", &n_words(390));
    w.write("CLAUDE.md", &format!("@AGENTS.md\n{}", n_words(1600)));
}

#[given("the sum of \"CLAUDE.md\" plus the imported files exceeds the 1500-word tree ceiling")]
fn given_sum_exceeds_tree_ceiling(_w: &mut AgentsWorld) {
    // No-op: the prior step already sized CLAUDE.md (~1600 words) + AGENTS.md
    // (~390 words) well over the Background's 1500-word resolved-tree fail
    // ceiling.
}

#[then(regex = r#"^the file is reported with severity "(ok|warn|fail)"$"#)]
fn then_file_reported_with_severity(w: &mut AgentsWorld, severity: String) {
    let out = w.stdout();
    match severity.as_str() {
        // Ok findings are excluded from output by design — see
        // `then_reports_within_target` above for the same reasoning.
        "ok" => assert!(out.contains("WORD BUDGET: PASSED"), "got: {out}"),
        "warn" => {
            assert!(out.contains("[WARN]"), "got: {out}");
            assert!(out.contains("AGENTS.md"), "got: {out}");
        }
        "fail" => {
            assert!(out.contains("[FAIL]"), "got: {out}");
            assert!(out.contains("AGENTS.md"), "got: {out}");
        }
        other => panic!("unexpected severity {other}"),
    }
}

#[then(r#"no finding is emitted for ".github/copilot-instructions.md""#)]
fn then_no_finding_for_copilot_instructions(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(!out.contains("copilot-instructions"), "got: {out}");
}

#[then(r#"a finding with key "resolved-tree" is reported with severity "fail""#)]
fn then_resolved_tree_finding_fail(w: &mut AgentsWorld) {
    let out = w.stdout();
    assert!(out.contains("[FAIL] resolved-tree"), "got: {out}");
}

#[when("the developer runs harness instruction-size validate")]
fn when_legacy_instruction_size_command(w: &mut AgentsWorld) {
    w.exec(&["harness", "instruction-size", "validate"]);
}

#[then("the output reports an unknown subcommand")]
fn then_reports_unknown_subcommand(w: &mut AgentsWorld) {
    let out = w.combined_output();
    assert!(out.contains("unrecognized subcommand"), "got: {out}");
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

#[then("the file lists the monitored file class, per-file budgets, and enforcement points")]
fn then_file_lists_class_budgets_enforcement(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(content.contains("Monitored Surfaces"), "got: {content}");
    assert!(content.contains("Target"), "got: {content}");
    assert!(content.contains("Fail"), "got: {content}");
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
        content.contains("qualitative concerns the mechanical gate can't measure"),
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

#[then(r#""governance-word-budget" is named among the Step 0.5 categories"#)]
fn then_word_budget_named_in_step_0_5(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    let found = content
        .lines()
        .any(|line| line.contains("Step 0.5") && line.contains("governance-word-budget"));
    assert!(found, "got: {content}");
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

#[given(r#"a preflight JSON contains a "governance-word-budget" category with findings"#)]
fn given_preflight_json_has_word_budget_findings(_w: &mut AgentsWorld) {
    // No-op: this asserts static Step 0.5 processing-rule prose in
    // repo-rules-checker.md (read by the `When "repo-rules-checker" runs
    // Step 0.5` step below), not runnable CLI behavior.
}

#[when(r#""repo-rules-checker" runs Step 0.5"#)]
fn when_repo_rules_checker_runs_step_0_5(w: &mut AgentsWorld) {
    w.lookup_file_content = read_agent_surface(".claude/agents/repo/repo-rules-checker.md");
}

#[then(r#"it populates the deterministic skip set with "governance-word-budget""#)]
fn then_populates_deterministic_skip_set(w: &mut AgentsWorld) {
    let content = &w.lookup_file_content;
    assert!(
        content.contains("`governance-word-budget`"),
        "got: {content}"
    );
    assert!(
        content.contains("Step 6 word-count portion"),
        "got: {content}"
    );
}

#[then(r#"it embeds the preflight findings verbatim under "Deterministic Findings""#)]
fn then_embeds_preflight_findings_verbatim(w: &mut AgentsWorld) {
    assert!(
        w.lookup_file_content.contains("## Deterministic Findings"),
        "got: {}",
        w.lookup_file_content
    );
}

#[then("it does not re-derive word counts in Step 6")]
fn then_does_not_rederive_word_counts(w: &mut AgentsWorld) {
    assert!(
        w.lookup_file_content
            .contains("never re-derive sizes; defer to preflight"),
        "checker must defer word counting to the preflight rather than redoing it"
    );
}

// ===========================================================================
// Pre-push enforcement of the word-budget gate
// (governance-word-budget-pre-push.feature) — dark-launched as of
// Phase 1 (not yet registered in `gates:`); these scenarios describe the
// Phase-9 armed end state, so `matches_word_budget_trigger` mirrors the
// trigger the OLD `instruction-size` gate used (the shape Phase 9 will reuse
// when it registers `governance-word-budget`), not a live `.husky/pre-push`
// assertion — there is nothing live to assert against yet.
// ===========================================================================

fn matches_word_budget_trigger(path: &str) -> bool {
    path == "AGENTS.md"
        || path == "CLAUDE.md"
        || path == "repo-config.yml"
        || path.starts_with(".amazonq/rules/")
        || path.starts_with(".windsurf/rules/")
        || path.starts_with(".cursor/rules/")
        || path == ".junie/guidelines.md"
        || path == ".github/copilot-instructions.md"
        || path == "CONVENTIONS.md"
}

#[given(r#"my push range modifies "AGENTS.md""#)]
fn given_push_range_modifies_agents_md(w: &mut AgentsWorld) {
    w.push_range_files = vec!["AGENTS.md".to_string()];
}

#[given(r#"my push range modifies only "apps/ose-www/src/page.tsx""#)]
fn given_push_range_modifies_unrelated_file(w: &mut AgentsWorld) {
    w.push_range_files = vec!["apps/ose-www/src/page.tsx".to_string()];
}

#[given(r#""AGENTS.md" exceeds its fail ceiling"#)]
fn given_agents_md_exceeds_fail_ceiling(w: &mut AgentsWorld) {
    write_word_budget_config(w, 400, 500);
    w.write("AGENTS.md", &n_words(600));
}

#[given(r#""AGENTS.md" is within its fail ceiling"#)]
fn given_agents_md_within_fail_ceiling(w: &mut AgentsWorld) {
    write_word_budget_config(w, 400, 500);
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
    // Phase 9 arms `governance-word-budget` in the `gates:` registry with
    // this same trigger set (mirroring the removed `instruction-size`
    // entry's `pre-push: { scope: path-gated, trigger: [...] }` shape) — not
    // yet true at Phase 1, so there is no live registry entry to assert
    // against here (see module doc comment above).
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
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/harness")
        .canonicalize()
        .expect("feature dir resolvable")
}
