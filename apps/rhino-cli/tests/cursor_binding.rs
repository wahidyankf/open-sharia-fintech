//! Cucumber-rs integration tests for the Cursor platform binding
//! (`specs/apps/rhino/behavior/rhino-cli/gherkin/cursor-binding/`).

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]
#![allow(clippy::needless_pass_by_value)]

use std::collections::BTreeMap;
use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use rhino_cli::application::agents::bindings::{
    KNOWN_BINDING_DIRS, PLATFORM_BINDINGS_CATALOG, emit_bindings,
};
use rhino_cli::application::agents::cursor::CURSOR_MODEL_ID;
use rhino_cli::application::agents::frontmatter::extract_frontmatter;
use rhino_cli::application::repo_config::{self, HarnessEntry};
use rhino_cli::infrastructure::git::root::find_root_from;
use tempfile::TempDir;

const FIXTURE_AGENT: &str = "fixture-agent";
const SMALL_ROSTER: usize = 2;
const LARGE_ROSTER: usize = 5;

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct CursorWorld {
    work: TempDir,
    output: Option<Output>,
    agent_stem: String,
    claude_body: Vec<u8>,
    cursor_snapshot: BTreeMap<String, Vec<u8>>,
    roster_size: usize,
    second_roster_size: usize,
    cursor_entry: Option<HarnessEntry>,
}

impl std::fmt::Debug for CursorWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CursorWorld")
            .field("agent_stem", &self.agent_stem)
            .finish_non_exhaustive()
    }
}

impl CursorWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        init_git_repo(work.path());
        let world = Self {
            work,
            output: None,
            agent_stem: FIXTURE_AGENT.to_string(),
            claude_body: b"# Body\n".to_vec(),
            cursor_snapshot: BTreeMap::new(),
            roster_size: 1,
            second_roster_size: 0,
            cursor_entry: None,
        };
        world.write_minimal_repo_config();
        world.write_bindings_support_dirs();
        world
    }

    fn root(&self) -> &Path {
        self.work.path()
    }

    fn write(&self, rel: &str, content: &str) {
        let p = self.root().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk dir");
        }
        std::fs::write(p, content).expect("write");
    }

    fn write_bytes(&self, rel: &str, content: &[u8]) {
        let p = self.root().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk dir");
        }
        std::fs::write(p, content).expect("write bytes");
    }

    fn write_minimal_repo_config(&self) {
        self.write(
            "repo-config.yml",
            concat!(
                "harness:\n",
                "  - name: claude-code\n",
                "    tier: source\n",
                "    agent-dir: .claude/agents\n",
                "  - name: cursor\n",
                "    tier: generated\n",
                "    agent-dir: .cursor/agents\n",
                "    mirrors: .claude/agents\n",
                "  - name: opencode\n",
                "    tier: generated\n",
                "    agent-dir: .opencode/agents\n",
                "    mirrors: .claude/agents\n",
                "  - name: amazonq\n",
                "    tier: generated\n",
                "    rules-dir: .amazonq/rules\n",
                "    agent-name: ose-default\n",
                "coverage:\n  projects: []\n",
                "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            ),
        );
    }

    fn write_full_catalog(&self) {
        let mut content = String::from("# Platform Bindings\n\n");
        for dir in KNOWN_BINDING_DIRS {
            let _ = writeln!(content, "- `{dir}` row");
        }
        self.write(PLATFORM_BINDINGS_CATALOG, &content);
    }

    fn write_governance_stubs(&self) {
        self.write(
            "repo-governance/development/agents/ai-agents.md",
            "# Agents\n\nColor translation for `blue`.\n",
        );
        self.write(
            "repo-governance/development/agents/model-selection.md",
            "# Models\n\nmodel: sonnet\n`sonnet`\nmodel: opus\n`opus`\nmodel: haiku\n`haiku`\n",
        );
    }

    fn write_bindings_support_dirs(&self) {
        std::fs::create_dir_all(self.root().join(".claude/agents")).expect("mk claude agents");
        std::fs::create_dir_all(self.root().join(".opencode/agents")).expect("mk opencode agents");
        emit_bindings(self.root()).expect("emit amazonq bindings");
        self.write_full_catalog();
        self.write_governance_stubs();
    }

    fn generate_all_bindings(&mut self) {
        self.exec(&["harness", "bindings", "generate", "--quiet"]);
    }

    fn write_claude_agent(&self, stem: &str, frontmatter: &str, body: &[u8]) {
        let mut content = String::from("---\n");
        content.push_str(frontmatter);
        if !frontmatter.ends_with('\n') {
            content.push('\n');
        }
        content.push_str("---\n");
        let mut bytes = content.into_bytes();
        bytes.extend_from_slice(body);
        self.write_bytes(&format!(".claude/agents/{stem}.md"), &bytes);
    }

    fn build_model_tier_agent(&self, model: Option<&str>) {
        let mut fm = format!(
            "name: {}\ndescription: Fixture agent.\ntools: Read, Write\n",
            self.agent_stem
        );
        if let Some(m) = model {
            let _ = writeln!(fm, "model: {m}");
        }
        let _ = writeln!(fm, "color: blue");
        self.write_claude_agent(&self.agent_stem, &fm, &self.claude_body);
    }

    fn bin() -> PathBuf {
        cargo_bin("rhino-cli")
    }

    fn exec(&mut self, args: &[&str]) {
        let mut cmd_args: Vec<String> = args.iter().map(|s| (*s).to_string()).collect();
        cmd_args.push("--no-color".to_string());
        let out = std::process::Command::new(Self::bin())
            .args(&cmd_args)
            .current_dir(self.root())
            .output()
            .expect("run rhino-cli");
        self.output = Some(out);
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

    fn cursor_agent_path(&self) -> PathBuf {
        self.root()
            .join(".cursor/agents")
            .join(format!("{}.md", self.agent_stem))
    }

    fn read_cursor_agent(&self) -> String {
        std::fs::read_to_string(self.cursor_agent_path()).expect("read cursor agent")
    }

    fn snapshot_cursor_dir(&mut self) {
        self.cursor_snapshot.clear();
        let dir = self.root().join(".cursor/agents");
        if !dir.is_dir() {
            return;
        }
        for entry in std::fs::read_dir(&dir).into_iter().flatten().flatten() {
            let name = entry.file_name().to_string_lossy().into_owned();
            if name.ends_with(".md") && name != "README.md" {
                let bytes = std::fs::read(entry.path()).expect("read snapshot");
                self.cursor_snapshot.insert(name, bytes);
            }
        }
    }

    fn count_cursor_agents(&self) -> usize {
        let dir = self.root().join(".cursor/agents");
        if !dir.is_dir() {
            return 0;
        }
        std::fs::read_dir(&dir)
            .into_iter()
            .flatten()
            .flatten()
            .filter(|e| {
                let name = e.file_name();
                let n = name.to_string_lossy();
                n.ends_with(".md") && n != "README.md"
            })
            .count()
    }

    fn count_claude_agents(&self) -> usize {
        let dir = self.root().join(".claude/agents");
        std::fs::read_dir(&dir)
            .into_iter()
            .flatten()
            .flatten()
            .filter(|e| {
                let name = e.file_name();
                let n = name.to_string_lossy();
                n.ends_with(".md") && n != "README.md"
            })
            .count()
    }

    fn frontmatter_model(&self) -> Option<String> {
        let content = self.read_cursor_agent();
        let mut in_fm = false;
        for line in content.lines() {
            if line == "---" {
                in_fm = !in_fm;
                continue;
            }
            if in_fm {
                if let Some(m) = line.strip_prefix("model:") {
                    return Some(m.trim().trim_matches('"').to_string());
                }
            } else {
                break;
            }
        }
        None
    }

    fn frontmatter_body_bytes(&self) -> Vec<u8> {
        let content = std::fs::read(self.cursor_agent_path()).expect("read bytes");
        let (_, body) = extract_frontmatter(&content).expect("extract frontmatter");
        body
    }
}

fn init_git_repo(dir: &Path) {
    std::process::Command::new("git")
        .args(["init", "-q"])
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git init");
}

// --- Shared generate steps ---

#[given("a Claude agent whose frontmatter declares the thinking-grade model alias")]
fn given_thinking_grade(w: &mut CursorWorld) {
    w.agent_stem = FIXTURE_AGENT.to_string();
    w.build_model_tier_agent(Some("opus"));
}

#[given("a Claude agent whose frontmatter declares the execution-grade model alias")]
fn given_execution_grade(w: &mut CursorWorld) {
    w.agent_stem = FIXTURE_AGENT.to_string();
    w.build_model_tier_agent(Some("sonnet"));
}

#[given("a Claude agent whose frontmatter carries no model field")]
fn given_no_model(w: &mut CursorWorld) {
    w.agent_stem = FIXTURE_AGENT.to_string();
    w.build_model_tier_agent(None);
}

#[given("a Claude agent whose frontmatter declares the fast-grade model alias")]
fn given_fast_grade(w: &mut CursorWorld) {
    w.agent_stem = FIXTURE_AGENT.to_string();
    w.build_model_tier_agent(Some("haiku"));
}

#[when("the developer runs harness bindings generate")]
fn when_generate(w: &mut CursorWorld) {
    w.exec(&["harness", "bindings", "generate", "--harness", "cursor"]);
}

#[when("the developer runs harness bindings generate a second time")]
fn when_generate_second(w: &mut CursorWorld) {
    when_generate(w);
}

#[when("the developer runs harness bindings generate in that repository")]
fn when_generate_in_repo(w: &mut CursorWorld) {
    when_generate(w);
}

#[when("the developer runs harness bindings validate")]
fn when_validate(w: &mut CursorWorld) {
    w.exec(&["harness", "bindings", "validate"]);
}

// --- Model tier Then steps ---

#[then("the emitted Cursor agent frontmatter declares the non-fast Composer 2.5 model identifier")]
fn then_model_is_composer(w: &mut CursorWorld) {
    assert_eq!(w.frontmatter_model().as_deref(), Some(CURSOR_MODEL_ID));
    assert!(!w.read_cursor_agent().contains("composer-2.5-fast"));
}

#[then("the emitted frontmatter carries no other model field")]
fn then_single_model_field(w: &mut CursorWorld) {
    let content = w.read_cursor_agent();
    assert_eq!(content.matches("model:").count(), 1);
}

#[then("the emitted identifier is byte-identical to the thinking-grade agent's identifier")]
fn then_same_as_thinking(w: &mut CursorWorld) {
    assert_eq!(w.frontmatter_model().as_deref(), Some(CURSOR_MODEL_ID));
}

#[then("no conversion warning is emitted for the absent model field")]
fn then_no_warning_absent_model(w: &mut CursorWorld) {
    let out = w.combined_output();
    assert!(
        !out.contains("dropped field \"model\""),
        "unexpected model warning: {out}"
    );
}

// --- Color / name / body ---

#[given("a Claude agent whose frontmatter declares a named color")]
fn given_named_color(w: &mut CursorWorld) {
    w.agent_stem = FIXTURE_AGENT.to_string();
    w.build_model_tier_agent(Some("sonnet"));
}

#[given("a Claude agent whose frontmatter declares a name")]
fn given_named_agent(w: &mut CursorWorld) {
    w.agent_stem = "custom-name".to_string();
    w.write_claude_agent(
        "named-agent",
        "name: custom-name\ndescription: \"Quoted: value\"\ntools: Read\nmodel: sonnet\ncolor: blue\n",
        b"# Body\n",
    );
}

#[given("a Claude agent whose body holds markdown headings and fenced code")]
fn given_body_with_code(w: &mut CursorWorld) {
    w.agent_stem = FIXTURE_AGENT.to_string();
    w.claude_body = b"# Heading\n\n```rust\nfn main() {}\n```\n".to_vec();
    w.build_model_tier_agent(Some("sonnet"));
}

#[then("the emitted Cursor agent frontmatter contains no color field")]
fn then_no_color(w: &mut CursorWorld) {
    assert!(!w.read_cursor_agent().contains("color:"));
}

#[then("a conversion warning records that color has no Cursor equivalent")]
fn then_color_warning(w: &mut CursorWorld) {
    use rhino_cli::application::agents::cursor::convert_cursor_agent;
    let input = w.root().join(format!(".claude/agents/{}.md", w.agent_stem));
    let claude_dir = w.root().join(".claude/agents");
    let warnings =
        convert_cursor_agent(&input, &w.cursor_agent_path(), &claude_dir, true).expect("convert");
    assert!(
        warnings.iter().any(|warning| {
            warning.field == "color" && warning.reason.contains("no cursor equivalent")
        }),
        "warnings: {warnings:?}"
    );
}

#[then("the emitted Cursor agent frontmatter declares the same name value")]
fn then_same_name(w: &mut CursorWorld) {
    assert!(w.read_cursor_agent().contains("name: custom-name"));
}

#[then("the emitted frontmatter declares the same description value")]
fn then_same_description(w: &mut CursorWorld) {
    assert!(
        w.read_cursor_agent()
            .contains("description: \"Quoted: value\"")
    );
}

#[then("the emitted Cursor agent body is byte-identical to the Claude agent body")]
fn then_body_identical(w: &mut CursorWorld) {
    let claude_path = w.root().join(format!(".claude/agents/{}.md", w.agent_stem));
    let claude_bytes = std::fs::read(claude_path).expect("read claude");
    let (_, claude_body) = extract_frontmatter(&claude_bytes).expect("extract claude");
    let cursor_body = w.frontmatter_body_bytes();
    assert_eq!(claude_body, cursor_body.as_slice());
}

#[then("the emitted file separates frontmatter from body with a single delimiter line")]
fn then_single_delimiter(w: &mut CursorWorld) {
    let bytes = std::fs::read(w.cursor_agent_path()).expect("read");
    let text = String::from_utf8(bytes).expect("utf8");
    assert!(text.starts_with("---\n"));
    assert_eq!(text.matches("\n---\n").count(), 1);
}

// --- Emit count ---

#[given("a repository whose .claude/agents/ directory holds three agent definitions and a README")]
fn given_three_agents_and_readme(w: &mut CursorWorld) {
    for i in 1..=3 {
        w.write_claude_agent(
            &format!("agent-{i}"),
            &format!("name: agent-{i}\ndescription: d\ntools: Read\nmodel: sonnet\ncolor: blue\n"),
            b"# Body\n",
        );
    }
    w.write(".claude/agents/README.md", "# Agents\n");
    w.roster_size = 3;
}

#[then("the command exits successfully")]
fn then_success(w: &mut CursorWorld) {
    assert_eq!(w.exit_code(), 0, "{}", w.combined_output());
}

#[then(".cursor/agents/ holds exactly three agent files")]
fn then_three_cursor_agents(w: &mut CursorWorld) {
    assert_eq!(w.count_cursor_agents(), 3);
}

#[then("each emitted filename matches its Claude source filename")]
fn then_filenames_match(w: &mut CursorWorld) {
    for i in 1..=3 {
        assert!(
            w.root()
                .join(format!(".cursor/agents/agent-{i}.md"))
                .exists()
        );
    }
}

// --- Idempotent ---

#[given("a repository whose Cursor mirror was already generated once")]
fn given_already_generated(w: &mut CursorWorld) {
    given_thinking_grade(w);
    when_generate(w);
    w.snapshot_cursor_dir();
}

#[then("every emitted Cursor agent file is byte-for-byte identical to the first emission")]
fn then_byte_identical_second_run(w: &mut CursorWorld) {
    for (name, first) in &w.cursor_snapshot {
        let second = std::fs::read(w.root().join(".cursor/agents").join(name)).expect("read");
        assert_eq!(first, &second);
    }
}

// --- README ---

#[given(
    "a repository whose .claude/agents/ directory holds a README alongside its agent definitions"
)]
fn given_readme_and_agents(w: &mut CursorWorld) {
    w.write_claude_agent(
        "foo-maker",
        "name: foo-maker\ndescription: d\ntools: Read\nmodel: sonnet\ncolor: blue\n",
        b"# Body\n",
    );
    w.write(".claude/agents/README.md", "# README\n");
}

#[then(".cursor/agents/ holds no README file")]
fn then_no_cursor_readme(w: &mut CursorWorld) {
    assert!(!w.root().join(".cursor/agents/README.md").exists());
}

#[then("every other Claude agent filename has a Cursor counterpart")]
fn then_counterpart_exists(w: &mut CursorWorld) {
    assert!(w.root().join(".cursor/agents/foo-maker.md").exists());
}

// --- Roster agnostic ---

#[given(
    "a repository whose .claude/agents/ directory holds a different number of agents than another repository"
)]
fn given_different_roster_sizes(w: &mut CursorWorld) {
    w.roster_size = SMALL_ROSTER;
    w.second_roster_size = LARGE_ROSTER;
    for i in 0..SMALL_ROSTER {
        w.write_claude_agent(
            &format!("small-{i}"),
            &format!("name: small-{i}\ndescription: d\ntools: Read\nmodel: sonnet\ncolor: blue\n"),
            b"#\n",
        );
    }
}

#[then(
    ".cursor/agents/ holds exactly as many agent files as that repository's .claude/agents/ directory"
)]
fn then_mirror_matches_source_count(w: &mut CursorWorld) {
    assert_eq!(w.count_cursor_agents(), w.count_claude_agents());
}

#[then("no roster size is hard-coded in the emitter")]
fn then_no_hardcoded_roster(_w: &mut CursorWorld) {
    let src = std::fs::read_to_string(
        PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("src/application/agents/cursor.rs"),
    )
    .expect("read cursor.rs");
    assert!(!src.contains("90 agents"));
    assert!(!src.contains("64 agents"));
}

// --- Validation ---

#[given("a repository whose Cursor mirror matches the generated content")]
fn given_matching_mirror(w: &mut CursorWorld) {
    given_thinking_grade(w);
    w.generate_all_bindings();
    assert_eq!(w.exit_code(), 0, "{}", w.combined_output());
}

#[then("the output reports the Cursor mirror checks as passing")]
fn then_cursor_checks_pass(w: &mut CursorWorld) {
    let out = w.combined_output();
    assert!(
        out.contains("VALIDATION PASSED")
            || out.contains("Cursor Agent")
            || out.contains("Cursor mirror"),
        "got: {out}"
    );
}

#[given(
    "a repository where one Cursor agent file has been hand-edited away from the generated content"
)]
fn given_hand_edited(w: &mut CursorWorld) {
    given_matching_mirror(w);
    let path = w.cursor_agent_path();
    let mut content = std::fs::read_to_string(&path).expect("read");
    content.push_str("\n<!-- drift -->\n");
    std::fs::write(path, content).expect("write drift");
}

#[then("the command exits with a failure code")]
fn then_failure(w: &mut CursorWorld) {
    assert_ne!(w.exit_code(), 0, "{}", w.combined_output());
}

#[then("the output names the drifted Cursor agent file")]
fn then_names_drifted(w: &mut CursorWorld) {
    assert!(w.combined_output().contains(&w.agent_stem));
}

#[then("the output advises re-running the binding generator")]
fn then_advises_regenerate(w: &mut CursorWorld) {
    assert!(w.combined_output().contains("harness bindings generate"));
}

#[given(
    "a repository whose Cursor mirror holds an agent file that no longer exists under .claude/agents/"
)]
fn given_stale_cursor_file(w: &mut CursorWorld) {
    given_matching_mirror(w);
    w.write(
        ".cursor/agents/orphan-agent.md",
        "---\nname: orphan\ndescription: d\nmodel: composer-2.5\n---\n# x\n",
    );
}

#[then("the output names the stale Cursor agent file")]
fn then_names_stale(w: &mut CursorWorld) {
    assert!(w.combined_output().contains("orphan"));
}

#[given("a repository whose Cursor mirror is missing one agent file present under .claude/agents/")]
fn given_missing_cursor_file(w: &mut CursorWorld) {
    given_matching_mirror(w);
    std::fs::remove_file(w.cursor_agent_path()).expect("remove cursor file");
}

#[then("the output names the missing Cursor agent file")]
fn then_names_missing(w: &mut CursorWorld) {
    assert!(w.combined_output().contains(&w.agent_stem));
}

#[given(
    "a repository with a generated Cursor mirror and a platform-bindings catalog that omits it"
)]
fn given_catalog_omits_cursor(w: &mut CursorWorld) {
    given_matching_mirror(w);
    w.write(
        "docs/reference/platform-bindings.md",
        "# Bindings\n\nNo cursor here.\n",
    );
}

#[then("the output identifies the Cursor directory as missing a catalog row")]
fn then_catalog_missing(w: &mut CursorWorld) {
    let out = w.combined_output();
    assert!(
        out.contains(".cursor") || out.contains("catalog"),
        "got: {out}"
    );
}

// --- Bindings validate: Cursor mirror drift ---

#[given(
    "a repository whose registry declares the cursor entry as a generated tier mirroring .claude/agents"
)]
fn given_registry_cursor_generated(w: &mut CursorWorld) {
    w.write_claude_agent(
        "mirror-a",
        "name: mirror-a\ndescription: d\ntools: Read\nmodel: sonnet\ncolor: blue\n",
        b"# Body\n",
    );
    w.write_claude_agent(
        "mirror-b",
        "name: mirror-b\ndescription: d\ntools: Read\nmodel: haiku\ncolor: blue\n",
        b"# Body\n",
    );
    when_generate(w);
    assert_eq!(w.exit_code(), 0, "{}", w.combined_output());
}

#[when("the developer deletes one Cursor agent file and runs harness bindings validate")]
fn when_delete_and_bindings(w: &mut CursorWorld) {
    std::fs::remove_file(w.root().join(".cursor/agents/mirror-a.md")).expect("delete cursor agent");
    w.exec(&["harness", "bindings", "validate"]);
}

#[when(
    "the developer adds a Cursor agent file with no Claude counterpart and runs harness bindings validate"
)]
fn when_add_orphan_and_bindings(w: &mut CursorWorld) {
    w.write(
        ".cursor/agents/unsourced-agent.md",
        "---\nname: unsourced\ndescription: d\nmodel: composer-2.5\n---\n# x\n",
    );
    w.exec(&["harness", "bindings", "validate"]);
}

#[then("the command reports Cursor mirror drift")]
fn then_mirror_drift(w: &mut CursorWorld) {
    // `harness bindings validate` reports drift as a failing Cursor check
    // rather than with the literal token the withdrawn naming validator used.
    assert_ne!(w.exit_code(), 0, "{}", w.combined_output());
    let out = w.combined_output();
    assert!(out.contains("Cursor"), "got: {out}");
}

#[then(
    regex = r"^the violation names the deleted agent as present in the source but absent from the Cursor mirror$"
)]
fn then_deleted_violation(w: &mut CursorWorld) {
    let out = w.combined_output();
    assert!(out.contains("Cursor mirror file missing"), "got: {out}");
    assert!(
        out.contains("mirror-a") || out.contains("fixture-agent"),
        "got: {out}"
    );
}

#[then(
    regex = r"^the violation names the added agent as present in the Cursor mirror but absent from the source$"
)]
fn then_added_violation(w: &mut CursorWorld) {
    let out = w.combined_output();
    assert!(out.contains("Cursor Orphan"), "got: {out}");
    assert!(out.contains("unsourced-agent"), "got: {out}");
}

// --- Registry (real repo) ---

#[given("the harness registry section of repo-config.yml")]
fn given_harness_registry(w: &mut CursorWorld) {
    let root = find_root_from(None).expect("repo root");
    let config = repo_config::load(&root).expect("load config");
    w.cursor_entry = config.harness.iter().find(|h| h.name == "cursor").cloned();
}

#[when("the cursor entry is read")]
fn when_cursor_read(w: &mut CursorWorld) {
    assert!(w.cursor_entry.is_some());
}

#[then("the entry declares the generated tier")]
fn then_generated_tier(w: &mut CursorWorld) {
    assert_eq!(w.cursor_entry.as_ref().unwrap().tier, "generated");
}

#[then("the entry declares .cursor/agents as its agent directory")]
fn then_agent_dir(w: &mut CursorWorld) {
    assert_eq!(
        w.cursor_entry.as_ref().unwrap().agent_dir.as_deref(),
        Some(".cursor/agents")
    );
}

#[then("the entry declares .claude/agents as the source it mirrors")]
fn then_mirror_source(w: &mut CursorWorld) {
    assert_eq!(
        w.cursor_entry.as_ref().unwrap().mirrors.as_deref(),
        Some(".claude/agents")
    );
}

#[tokio::main]
async fn main() {
    CursorWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/cursor-binding")
        .canonicalize()
        .expect("feature dir resolvable")
}
