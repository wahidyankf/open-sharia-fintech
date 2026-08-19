//! Cucumber-rs integration tests for the Codex platform binding
//! (`specs/apps/rhino/behavior/rhino-cli/gherkin/harness/codex-binding.feature`).
//!
//! The feature file lives in the shared `gherkin/harness/` directory that
//! `tests/agents.rs` also runs, so both runners filter on the feature-level
//! `@codex-binding` tag: this runner takes the tagged features, `agents.rs`
//! takes everything else. Without the filter each runner would meet the
//! other's undefined steps and fail under `fail_on_skipped`.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::needless_pass_by_value)] // cucumber-rs binds regex captures by value
#![allow(clippy::panic)]

use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Feature-level tag both this runner and `agents.rs` filter on.
const CODEX_BINDING_TAG: &str = "codex-binding";

/// Role subfolder the fixture agent is authored under, proving the mirror
/// flattens role nesting away.
const FIXTURE_ROLE_DIR: &str = "pr-review";

/// `name:` frontmatter value of the fixture agent.
const FIXTURE_AGENT_NAME: &str = "fixture-codex-maker";

/// `(role subfolder, filename stem, name frontmatter)` triples where the stem
/// and the `name` deliberately disagree, so an emitter that keys on the path
/// produces different filenames than one that keys on `name`.
const NAME_KEYED_FIXTURES: &[(&str, &str, &str)] = &[
    ("pr-review", "alpha-file-stem", "alpha-named-agent"),
    ("swe", "beta-file-stem", "beta-named-agent"),
];

/// Shared scenario state. Each scenario gets a fresh git-rooted temp workspace
/// so the binary's git-root lookup resolves inside the fixture.
/// Fixture `.codex/config.toml` prologue: the three hand-maintained tables the
/// region rewriter must leave untouched.
const HAND_MAINTAINED_CONFIG: &str = concat!(
    "[mcp_servers.nx-mcp]\n",
    "command = \"npx\"\n",
    "args = [ \"nx-mcp@latest\", \"--minimal\" ]\n",
    "\n",
    "[features]\n",
    "default_mode_request_user_input = true\n",
    "multi_agent = true\n",
    "\n",
    "[agents.ci-monitor-subagent]\n",
    "description = \"CI helper for /monitor-ci.\"\n",
    "config_file = \"ci-monitor-subagent.toml\"\n",
);

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct CodexWorld {
    work: TempDir,
    output: Option<Output>,
    /// `.codex/config.toml` bytes captured after the first of two generate runs.
    first_config: Option<String>,
}

impl std::fmt::Debug for CodexWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CodexWorld").finish_non_exhaustive()
    }
}

impl CodexWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        init_git_repo(work.path());
        Self {
            work,
            output: None,
            first_config: None,
        }
    }

    fn root(&self) -> &Path {
        self.work.path()
    }

    fn write(&self, rel: &str, content: &str) {
        let path = self.root().join(rel);
        if let Some(parent) = path.parent() {
            std::fs::create_dir_all(parent).expect("create fixture parent dir");
        }
        std::fs::write(path, content).expect("write fixture file");
    }

    fn write_three_harness_registry(&self) {
        self.write(
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
                "    config: .codex/config.toml\n",
                "coverage:\n  projects: []\n",
            ),
        );
    }

    fn exec(&mut self, args: &[&str]) {
        let mut cmd_args: Vec<String> = args.iter().map(|s| (*s).to_string()).collect();
        cmd_args.push("--no-color".to_string());
        let out = std::process::Command::new(cargo_bin("rhino-cli"))
            .args(&cmd_args)
            .current_dir(self.root())
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
    }

    fn combined_output(&self) -> String {
        let out = self.output.as_ref().expect("a command has run");
        format!(
            "{}{}",
            String::from_utf8_lossy(&out.stdout),
            String::from_utf8_lossy(&out.stderr)
        )
    }

    fn exit_code(&self) -> i32 {
        self.output
            .as_ref()
            .expect("a command has run")
            .status
            .code()
            .unwrap_or(-1)
    }

    /// Every `.toml` file directly under `.codex/agents/`, sorted by filename.
    fn codex_agent_files(&self) -> Vec<PathBuf> {
        let dir = self.root().join(".codex/agents");
        let mut found: Vec<PathBuf> = std::fs::read_dir(&dir)
            .into_iter()
            .flatten()
            .flatten()
            .map(|e| e.path())
            .filter(|p| p.extension().is_some_and(|e| e == "toml"))
            .collect();
        found.sort();
        found
    }

    fn read_codex_config(&self) -> String {
        let path = self.root().join(".codex/config.toml");
        std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("read {}: {e}", path.display()))
    }

    fn read_fixture_agent_toml(&self) -> String {
        let path = self
            .root()
            .join(".codex/agents")
            .join(format!("{FIXTURE_AGENT_NAME}.toml"));
        std::fs::read_to_string(&path).unwrap_or_else(|e| panic!("read {}: {e}", path.display()))
    }
}

fn init_git_repo(dir: &Path) {
    let status = std::process::Command::new("git")
        .args(["init", "-q"])
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .status()
        .expect("git init");
    assert!(status.success(), "git init failed in {}", dir.display());
}

/// True when `content` declares TOML key `key` at the start of a line.
fn declares_key(content: &str, key: &str) -> bool {
    content
        .lines()
        .any(|line| line.trim_start().starts_with(&format!("{key} =")))
}

#[given("a repository whose .claude/agents/ directory holds one agent under a role subfolder")]
fn given_one_agent_under_role_subfolder(w: &mut CodexWorld) {
    w.write_three_harness_registry();
    w.write(
        &format!(".claude/agents/{FIXTURE_ROLE_DIR}/{FIXTURE_AGENT_NAME}.md"),
        concat!(
            "---\n",
            "name: fixture-codex-maker\n",
            "description: Fixture agent for the Codex binding.\n",
            "tools: Read, Write\n",
            "model: opus\n",
            "color: blue\n",
            "---\n",
            "\n",
            "# Fixture\n",
            "\n",
            "Body prose the emitter carries into developer_instructions.\n",
        ),
    );
}

#[given(
    "a repository whose .claude/agents/ holds two agents in different role subfolders whose name frontmatter differs from their filename"
)]
fn given_two_agents_named_apart_from_their_filenames(w: &mut CodexWorld) {
    w.write_three_harness_registry();
    for (role, stem, name) in NAME_KEYED_FIXTURES {
        w.write(
            &format!(".claude/agents/{role}/{stem}.md"),
            &format!("---\nname: {name}\ndescription: Fixture {name}.\n---\n\n# {name}\n"),
        );
    }
}

#[then(".codex/agents/ holds one flat TOML file per agent keyed on the name frontmatter")]
fn then_flat_files_keyed_on_name(w: &mut CodexWorld) {
    let mut expected: Vec<String> = NAME_KEYED_FIXTURES
        .iter()
        .map(|(_, _, name)| format!("{name}.toml"))
        .collect();
    expected.sort();
    let names: Vec<String> = w
        .codex_agent_files()
        .iter()
        .map(|p| {
            p.file_name()
                .unwrap_or_default()
                .to_string_lossy()
                .into_owned()
        })
        .collect();
    assert_eq!(
        names, expected,
        "identity must come from `name:`, not the filename or subfolder"
    );
}

#[then("no emitted filename repeats a role subfolder name")]
fn then_no_role_subfolder_in_filenames(w: &mut CodexWorld) {
    let dir = w.root().join(".codex/agents");
    for (role, _, _) in NAME_KEYED_FIXTURES {
        assert!(
            !dir.join(role).exists(),
            "role subfolder {role} must be flattened away, not recreated under .codex/agents/"
        );
    }
    for path in w.codex_agent_files() {
        let name = path
            .file_name()
            .unwrap_or_default()
            .to_string_lossy()
            .into_owned();
        for (role, _, _) in NAME_KEYED_FIXTURES {
            assert!(
                !name.contains(role),
                "{name} leaks its role subfolder {role}"
            );
        }
    }
}

#[given(
    "a repository whose .codex/config.toml carries hand-maintained mcp_servers, features, and ci-monitor-subagent tables"
)]
fn given_hand_maintained_codex_config(w: &mut CodexWorld) {
    given_one_agent_under_role_subfolder(w);
    w.write(".codex/config.toml", HAND_MAINTAINED_CONFIG);
}

#[when("the developer runs harness bindings generate twice")]
fn when_generate_twice(w: &mut CodexWorld) {
    w.exec(&["harness", "bindings", "generate", "--quiet"]);
    assert_eq!(
        w.exit_code(),
        0,
        "first generate run failed:\n{}",
        w.combined_output()
    );
    w.first_config = Some(w.read_codex_config());
    w.exec(&["harness", "bindings", "generate", "--quiet"]);
}

#[then(".codex/config.toml declares a generated agents table for the fixture agent")]
fn then_config_declares_generated_agent_table(w: &mut CodexWorld) {
    let content = w.read_codex_config();
    assert!(
        content.contains(&format!("[agents.{FIXTURE_AGENT_NAME}]")),
        "expected a generated table for {FIXTURE_AGENT_NAME}; got:\n{content}"
    );
}

#[then("the hand-maintained mcp_servers, features, and ci-monitor-subagent tables are unchanged")]
fn then_hand_maintained_tables_survive(w: &mut CodexWorld) {
    let content = w.read_codex_config();
    assert!(
        content.contains(HAND_MAINTAINED_CONFIG.trim_end()),
        "the hand-maintained prologue must survive byte-for-byte; got:\n{content}"
    );
}

#[then("the second run left .codex/config.toml byte-identical to the first")]
fn then_config_is_idempotent(w: &mut CodexWorld) {
    let first = w.first_config.clone().expect("first run captured");
    let second = w.read_codex_config();
    assert_eq!(
        first, second,
        "a second generate run must not change .codex/config.toml"
    );
}

#[when("the developer runs harness bindings generate")]
fn when_generate(w: &mut CodexWorld) {
    w.exec(&["harness", "bindings", "generate", "--quiet"]);
}

#[then("the command exits successfully")]
fn then_exits_successfully(w: &mut CodexWorld) {
    assert_eq!(
        w.exit_code(),
        0,
        "expected exit 0; got {}\n{}",
        w.exit_code(),
        w.combined_output()
    );
}

#[then(".codex/agents/ holds exactly one TOML file named for that agent")]
fn then_one_toml_named_for_agent(w: &mut CodexWorld) {
    let files = w.codex_agent_files();
    let names: Vec<String> = files
        .iter()
        .map(|p| {
            p.file_name()
                .unwrap_or_default()
                .to_string_lossy()
                .into_owned()
        })
        .collect();
    assert_eq!(
        names,
        vec![format!("{FIXTURE_AGENT_NAME}.toml")],
        "expected exactly the flat Codex counterpart; got {names:?}"
    );
}

#[then("the emitted Codex agent declares name, description, and developer_instructions")]
fn then_declares_required_keys(w: &mut CodexWorld) {
    let content = w.read_fixture_agent_toml();
    for key in ["name", "description", "developer_instructions"] {
        assert!(
            declares_key(&content, key),
            "expected key `{key}` in emitted Codex agent; got:\n{content}"
        );
    }
}

#[then("the emitted Codex agent declares no model field")]
fn then_declares_no_model(w: &mut CodexWorld) {
    let content = w.read_fixture_agent_toml();
    assert!(
        !declares_key(&content, "model"),
        "model is DropWarn for Codex agent files (DD-4); got:\n{content}"
    );
}

#[tokio::main]
async fn main() {
    CodexWorld::cucumber()
        .fail_on_skipped()
        .filter_run_and_exit(feature_dir(), |feature, _rule, _scenario| {
            feature.tags.iter().any(|t| t == CODEX_BINDING_TAG)
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
