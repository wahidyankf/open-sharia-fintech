//! Cucumber-rs suite for divergence triage and reviewed promotion (US-9).
//!
//! Shares the `gherkin/harness/` feature directory with `tests/agents.rs` and
//! its sibling runners; the split is by feature-level tag so each runner keeps
//! exactly one step-definition set.
//!
//! Every mutating scenario runs inside a fresh git-rooted temp fixture. The one
//! integration scenario runs read-only against the real repository, because
//! "this tree's mirrors are what the generator produces" is only meaningful
//! against the real tree.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::{Path, PathBuf};
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Feature-level tags this runner owns.
const OWNED_TAGS: &[&str] = &["sync-triage"];

/// The vendored plugin directory the fixture registry declares.
const VENDOR_DIR: &str = "vendor-plugin";

/// The plain agent: nothing in its frontmatter is unrepresentable downstream.
const PLAIN: &str = "alpha";

/// The rich agent: carries two fields every downstream policy drops with a
/// warning, so the at-risk list has something real to compute.
const RICH: &str = "rich";

/// The two canonical fields [`RICH`] carries that no mirror schema can hold.
const UNREPRESENTABLE: &[&str] = &["permissionMode", "isolation"];

/// The detection path. Nothing here may read a filesystem clock.
const DETECTION_PATH: &str = "src/application/agents/triage.rs";

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct TriageWorld {
    work: TempDir,
    /// Set when a scenario runs against a fresh clone rather than the fixture.
    clone: Option<TempDir>,
    /// Set when a scenario runs read-only against the real repository.
    real: bool,
    output: Option<Output>,
    /// Canonical file bytes captured before a promote run.
    canonical_before: Option<Vec<u8>>,
}

impl std::fmt::Debug for TriageWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("TriageWorld").finish_non_exhaustive()
    }
}

impl TriageWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        run_git(work.path(), &["init", "-q"]);
        Self {
            work,
            clone: None,
            real: false,
            output: None,
            canonical_before: None,
        }
    }

    /// Where the next command runs: the real repository, a fresh clone, or the
    /// fixture.
    fn root(&self) -> PathBuf {
        if self.real {
            return real_repo_root();
        }
        self.clone.as_ref().map_or_else(
            || self.work.path().to_path_buf(),
            |c| c.path().to_path_buf(),
        )
    }

    fn write(&self, rel: &str, content: &str) {
        write_file(&self.root(), rel, content);
    }

    fn append(&self, rel: &str, line: &str) {
        let path = self.root().join(rel);
        let mut content = std::fs::read_to_string(&path).expect("read for append");
        content.push_str(line);
        std::fs::write(path, content).expect("append");
    }

    fn restore(&self, rel: &str) {
        run_git(&self.root(), &["checkout", "--", rel]);
    }

    /// A complete fixture: registry, supporting docs, two agents, one skill,
    /// one vendored plugin directory. Generated, then committed so the
    /// classifier (which reads the git index) and the attribution step (which
    /// compares against HEAD) both have something to read.
    fn build_and_commit(&mut self) {
        self.write("repo-config.yml", &registry_yaml());
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
        self.write(
            &format!(".claude/agents/{PLAIN}.md"),
            &format!(
                "---\nname: {PLAIN}\ndescription: Agent {PLAIN}.\ntools: Read, Write\n\
                 model: sonnet\n---\n# Body\n"
            ),
        );
        self.write(
            &format!(".claude/agents/{RICH}.md"),
            &format!(
                "---\nname: {RICH}\ndescription: Agent {RICH}.\ntools: Read, Write\n\
                 model: sonnet\npermissionMode: acceptEdits\nisolation: worktree\n---\n# Body\n"
            ),
        );
        self.write(
            ".claude/skills/beta/SKILL.md",
            "---\nname: beta\ndescription: Skill beta.\n---\n# Skill body\n",
        );
        self.write(
            &format!(".agents/skills/{VENDOR_DIR}/SKILL.md"),
            "---\nname: vendor-plugin\ndescription: Third-party.\n---\n# Vendored\n",
        );

        self.exec(&["harness", "bindings", "generate"]);
        assert_eq!(self.exit_code(), 0, "fixture generate: {}", self.combined());
        run_git(&self.root(), &["add", "-A"]);
        run_git(&self.root(), &["commit", "-q", "-m", "fixture"]);
    }

    fn exec(&mut self, args: &[&str]) {
        self.output = Some(run_bin(&self.root(), args));
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

/// The fixture registry: one source harness and two generated ones, every
/// binding path classified, one vendored plugin directory declared.
fn registry_yaml() -> String {
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
         \x20     - {{ path: .opencode/agents, class: generated, reason: emitted from .claude/agents }}\n\
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

/// The real repository this crate lives in. Read-only.
fn real_repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .expect("repo root resolvable")
}

/// The hard-stop block alone, so an assertion about what it does NOT offer is
/// not satisfied — or defeated — by a neighbouring file's block.
fn hard_stop_block(output: &str) -> String {
    let marker = output.find("HARD STOP").expect("a hard stop block");
    // Start at the beginning of the marker's own line: the mirror path sits
    // before "HARD STOP" on it, and an assertion that the block names both
    // files would otherwise never see the mirror.
    let start = output[..marker].rfind('\n').map_or(0, |i| i + 1);
    let rest = &output[start..];
    // Search from after the marker so the block's own leading failure marker
    // does not end it immediately. Indexing past the first byte would split that
    // multi-byte character.
    rest[marker - start..].find("\n\u{2718}").map_or_else(
        || rest.to_string(),
        |end| rest[..marker - start + end].to_string(),
    )
}

// ---------------------------------------------------------------------------
// Given
// ---------------------------------------------------------------------------

#[given("every generated mirror matches what the generator produces from canonical source")]
fn given_in_sync(world: &mut TriageWorld) {
    world.build_and_commit();
}

#[given(
    "a fixture repository cloned fresh, so every file's modification time is its checkout time and carries no information"
)]
fn given_fresh_clone(world: &mut TriageWorld) {
    world.build_and_commit();
    let clone = TempDir::new().expect("clone dir");
    let src = world.work.path().to_string_lossy().into_owned();
    let dst = clone.path().to_string_lossy().into_owned();
    let out = run_git(clone.path(), &["clone", "-q", &src, &dst]);
    assert!(
        out.status.success(),
        "clone failed: {}",
        String::from_utf8_lossy(&out.stderr)
    );
    world.clone = Some(clone);
}

#[given(
    "a tree that reported zero divergences and then had exactly one generated mirror hand-edited"
)]
fn given_one_sided_mirror(world: &mut TriageWorld) {
    world.build_and_commit();
    world.exec(&["harness", "sync", "triage"]);
    assert_eq!(
        world.exit_code(),
        0,
        "the tree must start in sync: {}",
        world.combined()
    );
    world.append(&format!(".opencode/agents/{PLAIN}.md"), "\n<!-- edit -->\n");
}

#[given("a canonical source agent was hand-edited and the generator has not been run since")]
fn given_canonical_ahead(world: &mut TriageWorld) {
    world.build_and_commit();
    world.append(
        &format!(".claude/agents/{PLAIN}.md"),
        "\nExtra canonical prose.\n",
    );
}

#[given(
    "a canonical source file and its corresponding generated mirror have both been hand-edited"
)]
fn given_both_diverged(world: &mut TriageWorld) {
    world.build_and_commit();
    world.append(
        &format!(".claude/agents/{PLAIN}.md"),
        "\nExtra canonical prose.\n",
    );
    world.append(&format!(".opencode/agents/{PLAIN}.md"), "\n<!-- edit -->\n");
}

#[given("a generated OpenCode mirror carries a hand edit worth keeping")]
fn given_mirror_edit_worth_keeping(world: &mut TriageWorld) {
    world.build_and_commit();
    world.append(
        &format!(".opencode/agents/{PLAIN}.md"),
        "\nA paragraph worth keeping.\n",
    );
    world.canonical_before =
        Some(std::fs::read(world.root().join(format!(".claude/agents/{PLAIN}.md"))).expect("read"));
}

#[given(
    "a canonical agent carrying fields the editing harness's field policy drops with a warning"
)]
fn given_rich_agent(world: &mut TriageWorld) {
    world.build_and_commit();
}

#[given(
    "a vendored skill directory declared in the registry and a generated mirror file beside it"
)]
fn given_vendored_and_generated(world: &mut TriageWorld) {
    world.build_and_commit();
    assert!(
        world.root().join(".agents/skills/beta/SKILL.md").is_file(),
        "the generated mirror must exist beside the vendored directory"
    );
}

#[given("a generated mirror carries a hand edit")]
fn given_generated_mirror_edit(world: &mut TriageWorld) {
    world.build_and_commit();
    world.append(&format!(".codex/agents/{PLAIN}.toml"), "\n# edit\n");
}

#[given("this repository's generated mirrors were produced by the current generator")]
fn given_real_repo(world: &mut TriageWorld) {
    world.real = true;
}

// ---------------------------------------------------------------------------
// When
// ---------------------------------------------------------------------------

#[when("rhino-cli harness sync triage runs")]
#[when("rhino-cli harness sync triage runs against it")]
fn when_triage(world: &mut TriageWorld) {
    world.exec(&["harness", "sync", "triage"]);
}

#[when("rhino-cli harness sync promote runs against that mirror")]
fn when_promote_plain(world: &mut TriageWorld) {
    world.exec(&[
        "harness",
        "sync",
        "promote",
        "--from",
        &format!(".opencode/agents/{PLAIN}.md"),
    ]);
}

#[when("rhino-cli harness sync promote runs against that harness's mirror")]
fn when_promote_rich(world: &mut TriageWorld) {
    world.exec(&[
        "harness",
        "sync",
        "promote",
        "--from",
        &format!(".opencode/agents/{RICH}.md"),
    ]);
}

#[when("the vendored file is hand-edited and rhino-cli harness sync triage runs")]
fn when_vendored_edited(world: &mut TriageWorld) {
    world.append(
        &format!(".agents/skills/{VENDOR_DIR}/SKILL.md"),
        "\n<!-- vendor edit -->\n",
    );
    world.exec(&["harness", "sync", "triage"]);
}

#[when("rhino-cli harness bindings validate runs without triage")]
fn when_bindings_validate(world: &mut TriageWorld) {
    world.exec(&["harness", "bindings", "validate"]);
}

// ---------------------------------------------------------------------------
// Then
// ---------------------------------------------------------------------------

#[then("it exits 0 reporting zero divergences")]
#[then(
    "it exits 0 reporting zero divergences, because detection compares content and never a clock"
)]
fn then_zero_divergences(world: &mut TriageWorld) {
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
    assert!(
        world.combined().contains("0 divergence(s)"),
        "{}",
        world.combined()
    );
}

#[then("no clock-reading call appears anywhere on the detection path")]
fn then_no_clock_call(world: &mut TriageWorld) {
    let _ = world;
    let source =
        std::fs::read_to_string(PathBuf::from(env!("CARGO_MANIFEST_DIR")).join(DETECTION_PATH))
            .expect("detection path readable");
    for forbidden in [".modified()", "SystemTime", "mtime"] {
        assert!(
            !source.contains(forbidden),
            "{DETECTION_PATH} contains `{forbidden}`: detection must never read a clock, \
             because git stores none and a fresh clone would report the whole tree as changed"
        );
    }
}

#[then(
    "it exits non-zero naming that mirror as the hand-edited side and naming the promote command"
)]
fn then_names_mirror_and_promote(world: &mut TriageWorld) {
    assert_ne!(world.exit_code(), 0, "{}", world.combined());
    let out = world.combined();
    assert!(
        out.contains(&format!(".opencode/agents/{PLAIN}.md")),
        "{out}"
    );
    assert!(out.contains("the mirror was hand-edited"), "{out}");
    assert!(out.contains("harness sync promote --from"), "{out}");
}

#[then(
    "it exits 0 again once the mirror is restored, so the detection is falsifiable in both directions"
)]
fn then_restored_mirror_passes(world: &mut TriageWorld) {
    world.restore(&format!(".opencode/agents/{PLAIN}.md"));
    world.exec(&["harness", "sync", "triage"]);
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
}

#[then(
    "it exits non-zero naming the canonical side and naming the generate command rather than the promote command"
)]
fn then_names_canonical_and_generate(world: &mut TriageWorld) {
    assert_ne!(world.exit_code(), 0, "{}", world.combined());
    let out = world.combined();
    assert!(out.contains("the canonical source is ahead"), "{out}");
    assert!(out.contains(&format!(".claude/agents/{PLAIN}.md")), "{out}");
    assert!(out.contains("harness bindings generate"), "{out}");
    assert!(!out.contains("harness sync promote"), "{out}");
}

#[then("it exits 0 once the generator is run")]
fn then_after_generate_passes(world: &mut TriageWorld) {
    world.exec(&["harness", "bindings", "generate"]);
    assert_eq!(world.exit_code(), 0, "generate: {}", world.combined());
    world.exec(&["harness", "sync", "triage"]);
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
}

#[then("it exits non-zero naming both files")]
fn then_names_both_files(world: &mut TriageWorld) {
    assert_ne!(world.exit_code(), 0, "{}", world.combined());
    let block = hard_stop_block(&world.combined());
    assert!(
        block.contains(&format!(".opencode/agents/{PLAIN}.md")),
        "{block}"
    );
    assert!(
        block.contains(&format!(".claude/agents/{PLAIN}.md")),
        "{block}"
    );
}

#[then(
    "it offers neither promotion nor any automatic resolution, because no correct automatic answer exists"
)]
fn then_offers_nothing(world: &mut TriageWorld) {
    let block = hard_stop_block(&world.combined());
    assert!(!block.contains("promote"), "{block}");
    assert!(!block.contains("bindings generate"), "{block}");
}

#[then("it exits 0 once both files are restored")]
fn then_restored_both_pass(world: &mut TriageWorld) {
    world.restore(&format!(".claude/agents/{PLAIN}.md"));
    world.restore(&format!(".opencode/agents/{PLAIN}.md"));
    world.exec(&["harness", "sync", "triage"]);
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
}

#[then("a proposed unified diff against the canonical source is emitted")]
fn then_diff_emitted(world: &mut TriageWorld) {
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
    let out = world.combined();
    assert!(
        out.contains(&format!("--- a/.claude/agents/{PLAIN}.md")),
        "{out}"
    );
    assert!(
        out.contains(&format!("+++ b/.claude/agents/{PLAIN}.md")),
        "{out}"
    );
    assert!(out.contains("+A paragraph worth keeping."), "{out}");
}

#[then(
    "the canonical source file is byte-identical to what it was before the promote run, proving nothing was overwritten"
)]
fn then_canonical_untouched(world: &mut TriageWorld) {
    let after = std::fs::read(world.root().join(format!(".claude/agents/{PLAIN}.md")))
        .expect("read canonical");
    assert_eq!(
        world.canonical_before.as_deref(),
        Some(after.as_slice()),
        "promote wrote to canonical source"
    );
}

#[then("the output lists exactly those fields under an at-risk heading")]
fn then_at_risk_listed(world: &mut TriageWorld) {
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
    let out = world.combined();
    assert!(out.contains("At risk of loss"), "{out}");
    for field in UNREPRESENTABLE {
        assert!(
            out.contains(&format!("- {field} (")),
            "missing {field}: {out}"
        );
    }
}

#[then(
    "an agent whose canonical source carries none of them lists nothing, proving the list is computed rather than hardcoded"
)]
fn then_plain_agent_lists_nothing(world: &mut TriageWorld) {
    world.exec(&[
        "harness",
        "sync",
        "promote",
        "--from",
        &format!(".opencode/agents/{PLAIN}.md"),
    ]);
    let out = world.combined();
    assert_eq!(world.exit_code(), 0, "{out}");
    assert!(out.contains("(none)"), "{out}");
    for field in UNREPRESENTABLE {
        assert!(!out.contains(field), "{field} must not be listed: {out}");
    }
}

#[then("no divergence is reported for the vendored file, because the generator does not own it")]
fn then_vendored_ignored(world: &mut TriageWorld) {
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
    assert!(
        world.combined().contains("0 divergence(s)"),
        "{}",
        world.combined()
    );
}

#[then("hand-editing the generated file instead does report a divergence")]
fn then_generated_reported(world: &mut TriageWorld) {
    world.restore(&format!(".agents/skills/{VENDOR_DIR}/SKILL.md"));
    world.append(
        ".agents/skills/beta/SKILL.md",
        "\n<!-- generated edit -->\n",
    );
    world.exec(&["harness", "sync", "triage"]);
    assert_ne!(world.exit_code(), 0, "{}", world.combined());
    assert!(
        world.combined().contains(".agents/skills/beta/SKILL.md"),
        "{}",
        world.combined()
    );
}

#[then("it exits non-zero exactly as it did before triage existed")]
fn then_validate_still_fails(world: &mut TriageWorld) {
    assert_ne!(world.exit_code(), 0, "{}", world.combined());
}

#[then(
    "the failure message names both the canonical source file to edit and the harness sync promote command"
)]
fn then_validate_message_names_both(world: &mut TriageWorld) {
    let out = world.combined();
    assert!(out.contains(&format!(".claude/agents/{PLAIN}.md")), "{out}");
    assert!(out.contains("harness sync promote --from"), "{out}");
}

#[then("it exits 0 and reports the number of generated files compared")]
fn then_real_repo_in_sync(world: &mut TriageWorld) {
    assert_eq!(world.exit_code(), 0, "{}", world.combined());
    let out = world.combined();
    assert!(out.contains("generated file(s) compared"), "{out}");
    assert!(out.contains("0 divergence(s)"), "{out}");
}

#[tokio::main]
async fn main() {
    TriageWorld::cucumber()
        .fail_on_skipped()
        .filter_run_and_exit(feature_dir(), |feature, _rule, _scenario| {
            feature
                .tags
                .iter()
                .any(|t| OWNED_TAGS.contains(&t.as_str()))
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
