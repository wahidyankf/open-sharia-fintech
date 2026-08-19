//! Cucumber-rs suite for total ownership of binding files (US-8).
//!
//! Shares the `gherkin/harness/` feature directory with `tests/agents.rs`,
//! `tests/codex_binding.rs`, and `tests/skills_mirror.rs`; the runners split it
//! by feature-level tag so each keeps exactly one step-definition set.
//!
//! Every mutating scenario runs inside a fresh git-rooted temp fixture. The one
//! integration scenario runs read-only against the real repository, because the
//! claim it makes — that THIS repository has no unclassified binding file — is
//! only meaningful against the real tree.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Feature-level tags this runner owns.
const OWNED_TAGS: &[&str] = &["binding-ownership"];

/// The undeclared file the falsifiability probe introduces.
const PROBE: &str = ".opencode/probe-unowned.md";

/// The single vendored directory the fixture registry declares.
const VENDOR_DIR: &str = "vendor-plugin";

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct OwnershipWorld {
    /// Fresh git-rooted temp workspace for every mutating scenario.
    work: TempDir,
    /// Output of the most recent binary invocation.
    output: Option<Output>,
    /// Name of the emitted agent a scenario hand-edited.
    drifted: Option<String>,
    /// Hash of every declared source path, captured before a generate run.
    source_digest: Option<String>,
}

impl std::fmt::Debug for OwnershipWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("OwnershipWorld").finish_non_exhaustive()
    }
}

impl OwnershipWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        run_git(work.path(), &["init", "-q"]);
        Self {
            work,
            output: None,
            drifted: None,
            source_digest: None,
        }
    }

    fn root(&self) -> &Path {
        self.work.path()
    }

    fn write(&self, rel: &str, content: &str) {
        write_file(self.root(), rel, content);
    }

    /// The fixture registry: three harnesses, every binding path classified.
    fn write_registry(&self) {
        self.write("repo-config.yml", &registry_yaml(false));
    }

    /// A valid Claude agent. `model:` and `tools:` are present because the
    /// OpenCode equivalence check translates both; `color:` is omitted because
    /// its translation map is governance prose this fixture has no reason to
    /// carry.
    fn write_agent(&self, name: &str) {
        self.write(
            &format!(".claude/agents/{name}.md"),
            &format!(
                "---\nname: {name}\ndescription: Agent {name}.\ntools: Read, Write\n\
                 model: sonnet\n---\n# Body\n"
            ),
        );
    }

    fn write_skill(&self, name: &str) {
        self.write(
            &format!(".claude/skills/{name}/SKILL.md"),
            &format!("---\nname: {name}\ndescription: Skill {name}.\n---\n# Skill body\n"),
        );
    }

    /// `harness bindings validate` asserts every present binding directory is
    /// referenced in the catalog, and resolves agent `model:` values against a
    /// governance map. A fixture missing either fails for a reason unrelated to
    /// ownership.
    fn write_supporting_docs(&self) {
        self.write(
            "docs/reference/platform-bindings.md",
            "# Platform Bindings\n\nDirectories: .claude, .opencode, .codex, .agents, .github\n",
        );
        self.write(
            "repo-governance/development/agents/ai-agents.md",
            "# AI Agents\n\nColor translation: `blue`\n",
        );
        self.write(
            "repo-governance/development/agents/model-selection.md",
            "# Model Selection\n\nCapability tiers: `sonnet`, `haiku`, `opus`\n",
        );
    }

    /// Build a complete fixture, generate the bindings, and commit everything so
    /// the validator — which reads the git index — can see it.
    fn build_and_commit(&mut self) {
        self.write_registry();
        self.write_supporting_docs();
        self.write_agent("alpha");
        self.write_skill("beta");
        // A vendored plugin directory: present in the mirror, absent from
        // .claude/skills/, and therefore unregenerable by design.
        self.write(
            &format!(".agents/skills/{VENDOR_DIR}/SKILL.md"),
            "---\nname: vendor-plugin\ndescription: Third-party.\n---\n# Vendored\n",
        );
        self.exec(&["harness", "bindings", "generate"]);
        assert_eq!(self.exit_code(), 0, "fixture generate: {}", self.combined());
        self.commit_all();
    }

    fn commit_all(&self) {
        run_git(self.root(), &["add", "-A"]);
        run_git(self.root(), &["commit", "-q", "-m", "fixture"]);
    }

    fn exec(&mut self, args: &[&str]) {
        self.output = Some(run_bin(self.root(), args));
    }

    fn exit_code(&self) -> i32 {
        self.output
            .as_ref()
            .expect("a command ran")
            .status
            .code()
            .unwrap_or(-1)
    }

    fn combined(&self) -> String {
        let out = self.output.as_ref().expect("a command ran");
        format!(
            "{}{}",
            String::from_utf8_lossy(&out.stdout),
            String::from_utf8_lossy(&out.stderr)
        )
    }
}

/// The fixture registry. When `emitter_target_is_source`, the OpenCode entry
/// deliberately misdeclares its own output directory as source, which is the
/// condition the generator must refuse.
fn registry_yaml(emitter_target_is_source: bool) -> String {
    let opencode_agents_class = if emitter_target_is_source {
        "source"
    } else {
        "generated"
    };
    format!(
        "harness:\n\
         \x20 - name: claude-code\n\
         \x20   tier: source\n\
         \x20   agent-dir: .claude/agents\n\
         \x20   skills-dir: .claude/skills\n\
         \x20   ownership:\n\
         \x20     - {{ path: .claude/, class: source, reason: canonical hand-authored tree }}\n\
         \x20 - name: opencode\n\
         \x20   tier: generated\n\
         \x20   agent-dir: .opencode/agents\n\
         \x20   mirrors: .claude/agents\n\
         \x20   ownership:\n\
         \x20     - {{ path: .opencode/agents, class: {opencode_agents_class}, reason: emitted from .claude/agents }}\n\
         \x20 - name: codex\n\
         \x20   tier: generated\n\
         \x20   agent-dir: .codex/agents\n\
         \x20   mirrors: .claude/agents\n\
         \x20   config: .codex/config.toml\n\
         \x20   skills-dir: .agents/skills\n\
         \x20   skills-mirrors: .claude/skills\n\
         \x20   vendored:\n\
         \x20     - .agents/skills/{VENDOR_DIR}\n\
         \x20   ownership:\n\
         \x20     - {{ path: .codex/agents, class: generated, reason: emitted from .claude/agents }}\n\
         \x20     - {{ path: .codex/config.toml, class: vendored, reason: tooling config with a delimited region }}\n\
         \x20     - {{ path: .agents/skills, class: generated, reason: mirrored from .claude/skills }}\n\
         \x20     - {{ path: .agents/skills/{VENDOR_DIR}, class: vendored, reason: third-party plugin skill; no in-repo source }}\n\
         coverage:\n  projects: []\n"
    )
}

fn write_file(root: &Path, rel: &str, content: &str) {
    let p = root.join(rel);
    std::fs::create_dir_all(p.parent().expect("parent")).expect("mkdir");
    std::fs::write(p, content).expect("write");
}

fn run_git(dir: &Path, args: &[&str]) -> Output {
    std::process::Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git")
}

fn run_bin(dir: &Path, args: &[&str]) -> Output {
    let mut all: Vec<&str> = args.to_vec();
    all.push("--no-color");
    std::process::Command::new(cargo_bin("rhino-cli"))
        .args(&all)
        .current_dir(dir)
        .output()
        .expect("run rhino-cli")
}

/// The real repository this crate lives in. Used only for read-only assertions.
fn real_repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .expect("repo root resolvable")
}

/// A stable digest of every file under `rel`, so a before/after comparison
/// catches a rewrite as well as an addition or deletion.
fn tree_digest(root: &Path, rel: &str) -> String {
    fn walk(dir: &Path, base: &Path, out: &mut Vec<(String, Vec<u8>)>) {
        let Ok(entries) = std::fs::read_dir(dir) else {
            return;
        };
        for entry in entries.flatten() {
            let path = entry.path();
            let Ok(meta) = std::fs::symlink_metadata(&path) else {
                continue;
            };
            if meta.file_type().is_dir() {
                walk(&path, base, out);
            } else if let (Ok(r), Ok(bytes)) = (path.strip_prefix(base), std::fs::read(&path)) {
                out.push((r.to_string_lossy().into_owned(), bytes));
            }
        }
    }
    let mut files = Vec::new();
    walk(&root.join(rel), root, &mut files);
    files.sort_by(|a, b| a.0.cmp(&b.0));
    files
        .iter()
        .map(|(p, b)| format!("{p}:{}", b.len()))
        .collect::<Vec<_>>()
        .join("|")
}

// ---------------------------------------------------------------------------
// Scenario 1 — an unclassified file fails, and its removal restores green
// ---------------------------------------------------------------------------

#[given("a fixture repository whose binding files are all declared generated, vendored, or source")]
fn given_fully_classified_fixture(w: &mut OwnershipWorld) {
    w.build_and_commit();
    w.exec(&["harness", "ownership", "validate"]);
    assert_eq!(
        w.exit_code(),
        0,
        "the fixture must start classified, or the probe below proves nothing: {}",
        w.combined()
    );
}

#[when("a tracked file with no declared class is introduced under a binding directory")]
fn when_unowned_file_introduced(w: &mut OwnershipWorld) {
    w.write(PROBE, "# unowned\n");
    // Tracked, because the validator reads the git index: an untracked scratch
    // file is deliberately not a failure.
    run_git(w.root(), &["add", PROBE]);
}

#[then(
    "rhino-cli harness ownership validate exits non-zero naming that exact file as unclassified"
)]
fn then_names_the_unclassified_file(w: &mut OwnershipWorld) {
    w.exec(&["harness", "ownership", "validate"]);
    assert_ne!(w.exit_code(), 0, "must fail: {}", w.combined());
    assert!(
        w.combined().contains(PROBE),
        "the failure must name the exact file, not merely report a count; got: {}",
        w.combined()
    );
}

#[then(
    "it exits 0 once the file is removed, proving the check is falsifiable in both directions rather than always-green"
)]
fn then_zero_after_removal(w: &mut OwnershipWorld) {
    run_git(w.root(), &["rm", "-q", "-f", PROBE]);
    w.exec(&["harness", "ownership", "validate"]);
    assert_eq!(
        w.exit_code(),
        0,
        "must return to green once the residue is gone: {}",
        w.combined()
    );
}

// ---------------------------------------------------------------------------
// Scenario 2 — a generated file must reproduce byte-for-byte
// ---------------------------------------------------------------------------

#[given("a fixture repository whose mirror trees are declared generated")]
fn given_generated_fixture(w: &mut OwnershipWorld) {
    w.build_and_commit();
}

#[when("one emitted file is hand-edited")]
fn when_generated_file_edited(w: &mut OwnershipWorld) {
    let rel = ".opencode/agents/alpha.md";
    let path = w.root().join(rel);
    let body = std::fs::read_to_string(&path).expect("emitted agent exists");
    std::fs::write(&path, format!("{body}\nhand-edited\n")).expect("write");
    w.drifted = Some("alpha".to_owned());
}

#[then("rhino-cli harness ownership validate exits non-zero naming the drifted generated file")]
fn then_names_the_drifted_file(w: &mut OwnershipWorld) {
    w.exec(&["harness", "ownership", "validate"]);
    assert_ne!(w.exit_code(), 0, "must fail: {}", w.combined());
    let name = w.drifted.clone().expect("a file drifted");
    assert!(
        w.combined().contains(&name),
        "the failure must name the drifted agent {name}; got: {}",
        w.combined()
    );
}

#[then("it exits 0 after regeneration restores the canonical bytes")]
fn then_zero_after_regeneration(w: &mut OwnershipWorld) {
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0, "regenerate: {}", w.combined());
    w.exec(&["harness", "ownership", "validate"]);
    assert_eq!(
        w.exit_code(),
        0,
        "regeneration must restore green: {}",
        w.combined()
    );
}

// ---------------------------------------------------------------------------
// Scenario 3 — a vendored file carries no byte guard
// ---------------------------------------------------------------------------

#[given("a fixture repository declaring one vendored skill directory with a recorded reason")]
fn given_vendored_fixture(w: &mut OwnershipWorld) {
    w.build_and_commit();
}

#[when("the vendored file is hand-edited")]
fn when_vendored_file_edited(w: &mut OwnershipWorld) {
    let rel = format!(".agents/skills/{VENDOR_DIR}/SKILL.md");
    let path = w.root().join(&rel);
    let body = std::fs::read_to_string(&path).expect("vendored file exists");
    std::fs::write(&path, format!("{body}\nlocal edit\n")).expect("write");
}

#[then(
    "rhino-cli harness ownership validate still exits 0, because a vendored path has no in-repo source to compare against"
)]
fn then_vendored_edit_is_not_a_finding(w: &mut OwnershipWorld) {
    w.exec(&["harness", "ownership", "validate"]);
    assert_eq!(
        w.exit_code(),
        0,
        "a vendored path is exempt from the byte guard by design: {}",
        w.combined()
    );
}

#[then("the vendored file is still present, so nothing deleted it in passing")]
fn then_vendored_file_survives(w: &mut OwnershipWorld) {
    let path = w
        .root()
        .join(format!(".agents/skills/{VENDOR_DIR}/SKILL.md"));
    assert!(path.is_file(), "vendored file must survive validation");
    let body = std::fs::read_to_string(&path).expect("read");
    assert!(
        body.contains("local edit"),
        "the validator must not rewrite a vendored file either"
    );
}

// ---------------------------------------------------------------------------
// Scenario 4 — a source path is never written by the emitter
// ---------------------------------------------------------------------------

#[given("a fixture repository declaring the .claude tree as source")]
fn given_source_declared_fixture(w: &mut OwnershipWorld) {
    w.build_and_commit();
    w.source_digest = Some(tree_digest(w.root(), ".claude"));
}

#[when("rhino-cli harness bindings generate runs")]
fn when_generate_runs(w: &mut OwnershipWorld) {
    w.exec(&["harness", "bindings", "generate"]);
    assert_eq!(w.exit_code(), 0, "generate: {}", w.combined());
}

#[then("every declared source path is byte-identical to what it was before the run")]
fn then_source_untouched(w: &mut OwnershipWorld) {
    let before = w.source_digest.clone().expect("digest captured");
    assert_eq!(
        before,
        tree_digest(w.root(), ".claude"),
        "the emitter must not write into declared source"
    );
}

#[then(
    "a registry declaring an emitter output directory as source makes the generator refuse rather than silently succeed"
)]
fn then_generator_refuses_source_target(w: &mut OwnershipWorld) {
    w.write("repo-config.yml", &registry_yaml(true));
    w.exec(&["harness", "bindings", "generate"]);
    assert_ne!(
        w.exit_code(),
        0,
        "a generator whose target is declared source must refuse: {}",
        w.combined()
    );
    assert!(
        w.combined().contains(".opencode/agents"),
        "the refusal must name the offending target; got: {}",
        w.combined()
    );
}

// ---------------------------------------------------------------------------
// Scenario 5 — the real repository has no unclassified binding file
// ---------------------------------------------------------------------------

#[given("this repository's registry declares an ownership class for every binding path")]
fn given_real_repo(_w: &mut OwnershipWorld) {
    let config = real_repo_root().join("repo-config.yml");
    let text = std::fs::read_to_string(config).expect("read repo-config.yml");
    assert!(
        text.contains("ownership:"),
        "the real registry must carry ownership declarations"
    );
}

#[when("rhino-cli harness ownership validate runs against it")]
fn when_validate_real_repo(w: &mut OwnershipWorld) {
    w.output = Some(run_bin(
        &real_repo_root(),
        &["harness", "ownership", "validate"],
    ));
}

#[then("it exits 0")]
fn then_real_repo_exits_zero(w: &mut OwnershipWorld) {
    assert_eq!(w.exit_code(), 0, "{}", w.combined());
}

#[then("it reports a per-class count that sums to the total tracked binding-file count")]
fn then_counts_sum_to_total(w: &mut OwnershipWorld) {
    // The summary line prints only in verbose mode; the default output reports
    // the pass/fail tally alone.
    w.output = Some(run_bin(
        &real_repo_root(),
        &["harness", "ownership", "validate", "--verbose"],
    ));
    let out = w.combined();
    let line = out
        .lines()
        .find(|l| l.contains("tracked binding file(s):"))
        .unwrap_or_else(|| panic!("no per-class count line in output:\n{out}"));
    let numbers: Vec<usize> = line
        .split(|c: char| !c.is_ascii_digit())
        .filter(|s| !s.is_empty())
        .map(|s| s.parse().expect("digits parse"))
        .collect();
    assert_eq!(
        numbers.len(),
        4,
        "expected total + three class counts on: {line}"
    );
    let (total, classes) = (numbers[0], &numbers[1..]);
    assert_eq!(
        total,
        classes.iter().sum::<usize>(),
        "the three class counts must account for every tracked binding file: {line}"
    );
    assert!(total > 0, "a zero total would make the sum vacuous: {line}");
}

#[tokio::main]
async fn main() {
    OwnershipWorld::cucumber()
        .fail_on_skipped()
        // Takes only the feature this runner owns, leaving the rest of
        // `gherkin/harness/` to its sibling runners.
        .filter_run_and_exit(feature_dir(), |feature, _rule, _scenario| {
            feature
                .tags
                .iter()
                .any(|t| OWNED_TAGS.contains(&t.as_str()))
        })
        .await;
}

fn feature_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/harness")
        .canonicalize()
        .expect("feature dir resolvable")
}
