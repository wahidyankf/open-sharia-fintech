//! Cucumber-rs suite for the generated platform-binding catalog (US-5).
//!
//! Shares the `gherkin/harness/` feature directory with `tests/agents.rs` and
//! its sibling runners; the runners split it by feature-level tag so each keeps
//! exactly one step-definition set.
//!
//! Both scenarios run against a git-rooted temp fixture rather than the real
//! repository. The first mutates the catalog document, and the second needs a
//! clean `git diff` it can dirty on purpose — neither is safe to do to the tree
//! the test itself is running out of.
//!
//! The fixture registry declares three harness entries because the claim under
//! test is "one row per entry", and a fixture with one entry cannot distinguish
//! a per-entry renderer from a hardcoded single row.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::Path;
use std::process::Output;

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use rhino_cli::application::agents::catalog::{REGION_END, REGION_START};
use tempfile::TempDir;

/// Feature-level tags this runner owns.
const OWNED_TAGS: &[&str] = &["catalog-generation"];

/// Repository-relative path of the catalog document in the fixture.
const CATALOG_DOC: &str = "docs/reference/platform-bindings.md";

/// How many harness entries the fixture registry declares.
const FIXTURE_ENTRIES: usize = 3;

/// Prose the fixture carries ABOVE the generated region. Byte-identity of this
/// text after a generate run is what proves the emitter rewrites only its own
/// region.
const PROSE_BEFORE: &str = "\
# Platform Bindings

Fixture prose that the emitter must never touch. It carries a `pipe | character`
and a trailing sentence so a naive whole-file rewrite is detectable.
";

/// Prose the fixture carries BELOW the generated region, including a footnote
/// definition. Footnote definitions live outside the markers on purpose: the
/// table cells reference them, but the emitter does not own their text.
const PROSE_AFTER: &str = "\
[^mcp]: A footnote definition the emitter does not own.

## Related

- A trailing list item.
";

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct CatalogWorld {
    /// Fresh git-rooted temp workspace for every scenario.
    work: TempDir,
    /// Output of the most recent binary invocation.
    output: Option<Output>,
    /// The catalog document's text before the most recent generate run.
    before: Option<String>,
}

impl std::fmt::Debug for CatalogWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("CatalogWorld").finish_non_exhaustive()
    }
}

impl CatalogWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        run_git(work.path(), &["init", "-q"]);
        Self {
            work,
            output: None,
            before: None,
        }
    }

    fn root(&self) -> &Path {
        self.work.path()
    }

    fn doc_path(&self) -> std::path::PathBuf {
        self.root().join(CATALOG_DOC)
    }

    fn doc(&self) -> String {
        std::fs::read_to_string(self.doc_path()).expect("readable catalog document")
    }

    /// The text strictly between the two markers, marker lines excluded.
    fn region(&self) -> String {
        let body = self.doc();
        let start = body.find(REGION_START).expect("start marker present");
        let end = body.find(REGION_END).expect("end marker present");
        assert!(start < end, "markers must appear in order");
        body[start + REGION_START.len()..end].to_owned()
    }

    /// Everything outside the markers, with the region collapsed away, so a
    /// before/after comparison isolates the prose.
    fn outside(&self) -> String {
        let body = self.doc();
        let start = body.find(REGION_START).expect("start marker present");
        let end = body.find(REGION_END).expect("end marker present");
        format!("{}{}", &body[..start], &body[end + REGION_END.len()..])
    }

    /// Table rows inside the region — data rows only, excluding the header and
    /// the `| --- |` separator.
    fn row_count(&self) -> usize {
        self.region()
            .lines()
            .filter(|line| line.trim_start().starts_with('|'))
            .filter(|line| !line.contains("---"))
            .count()
            .saturating_sub(1)
    }
}

/// Writes a fixture registry whose three harness entries each carry a full
/// `catalog:` block, plus the sibling `harness-catalog:` block naming the
/// document and the verification date.
fn write_fixture_registry(root: &Path) {
    let config = "\
harness-catalog:
  document: docs/reference/platform-bindings.md
  verified: 2026-05-24

harness:
  - name: alpha-harness
    tier: source
    agent-dir: .alpha/agents
    catalog:
      platform: Alpha Harness
      reads-agents-md: 'No -- reads `ALPHA.md`'
      instruction-surface: '`ALPHA.md`, `.alpha/`'
      mcp-config: '`.mcp.json`'
      agent-surface: '`.alpha/agents/*.md`'
      skills-surface: '`.alpha/skills/*/SKILL.md`'
      status: Active
  - name: beta-harness
    tier: generated
    agent-dir: .beta/agents
    mirrors: .alpha/agents
    catalog:
      platform: Beta Harness
      reads-agents-md: 'Yes'
      instruction-surface: '`.beta/agents/` (auto-synced)'
      mcp-config: '`beta.json`'
      agent-surface: '`.beta/agents/*.md`'
      skills-surface: 'reads `.alpha/skills/`'
      status: Active
  - name: gamma-harness
    tier: generated
    agent-dir: .gamma/agents
    mirrors: .alpha/agents
    catalog:
      platform: Gamma Harness
      reads-agents-md: 'Yes (since Apr 2025)'
      instruction-surface: '`.gamma/config.toml`'
      mcp-config: '`.gamma/config.toml` `[mcp_servers]`[^mcp]'
      agent-surface: '`.gamma/agents/<name>.toml`'
      skills-surface: '`.agents/skills/`'
      status: Partial
";
    std::fs::write(root.join("repo-config.yml"), config).expect("write fixture registry");
}

/// Writes the catalog document with an EMPTY generated region, so a generate run
/// has something to fill and the before-state carries no rows.
fn write_fixture_document(root: &Path) {
    let doc = root.join(CATALOG_DOC);
    std::fs::create_dir_all(doc.parent().expect("doc has a parent")).expect("create docs dir");
    let body = format!("{PROSE_BEFORE}\n{REGION_START}\n{REGION_END}\n\n{PROSE_AFTER}");
    std::fs::write(&doc, body).expect("write fixture document");
}

#[given(
    "each harness entry in repo-config.yml carries catalog fields including display name, instruction surfaces, agent surface, skills surface, and status"
)]
fn registry_carries_catalog_fields(world: &mut CatalogWorld) {
    write_fixture_registry(world.root());
    write_fixture_document(world.root());
    world.before = Some(world.doc());
    assert_eq!(
        world.row_count(),
        0,
        "the fixture must start with an empty region, or a filled one proves nothing"
    );
}

#[when("rhino-cli harness catalog generate runs")]
fn generate_runs(world: &mut CatalogWorld) {
    world.output = Some(run_bin(world.root(), &["harness", "catalog", "generate"]));
}

#[then(
    "docs/reference/platform-bindings.md contains one table row per registry entry between the generated-region markers"
)]
fn one_row_per_entry(world: &mut CatalogWorld) {
    let output = world.output.as_ref().expect("a recorded invocation");
    assert!(
        output.status.success(),
        "generate failed: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert_eq!(
        world.row_count(),
        FIXTURE_ENTRIES,
        "region:\n{}",
        world.region()
    );
    for platform in ["Alpha Harness", "Beta Harness", "Gamma Harness"] {
        assert!(
            world.region().contains(platform),
            "row for {platform} missing from region:\n{}",
            world.region()
        );
    }
}

#[then("prose outside those markers is byte-identical to its pre-run content")]
fn prose_outside_unchanged(world: &mut CatalogWorld) {
    let before = world.before.as_ref().expect("a recorded before-state");
    let start = before.find(REGION_START).expect("start marker present");
    let end = before.find(REGION_END).expect("end marker present");
    let outside_before = format!("{}{}", &before[..start], &before[end + REGION_END.len()..]);
    assert_eq!(
        world.outside(),
        outside_before,
        "the emitter rewrote prose outside its own region"
    );
    // The footnote definition below the table is the specific thing a
    // whole-file rewrite would lose, so assert it by name rather than trusting
    // the aggregate comparison alone.
    assert!(
        world.doc().contains("[^mcp]: A footnote definition"),
        "the footnote definition outside the region was lost"
    );
}

#[given("a freshly generated catalog with a clean git diff")]
fn freshly_generated_clean(world: &mut CatalogWorld) {
    write_fixture_registry(world.root());
    write_fixture_document(world.root());
    let generated = run_bin(world.root(), &["harness", "catalog", "generate"]);
    assert!(
        generated.status.success(),
        "fixture generate failed: {}",
        String::from_utf8_lossy(&generated.stderr)
    );
    run_git(world.root(), &["add", "-A"]);
    run_git(world.root(), &["commit", "-qm", "fixture"]);
    let status = run_git(world.root(), &["status", "--porcelain"]);
    assert!(
        String::from_utf8_lossy(&status.stdout).trim().is_empty(),
        "fixture must start from a clean diff"
    );
}

#[when("one cell inside the generated region is edited by hand")]
fn hand_edit_inside_region(world: &mut CatalogWorld) {
    let body = world.doc();
    let edited = body.replace("Alpha Harness", "Tampered Harness");
    assert_ne!(
        edited, body,
        "the hand edit must actually change the region"
    );
    std::fs::write(world.doc_path(), edited).expect("write hand edit");
}

#[then("rhino-cli harness catalog validate exits non-zero naming the drifted region")]
fn validate_rejects_drift(world: &mut CatalogWorld) {
    let output = run_bin(world.root(), &["harness", "catalog", "validate"]);
    assert!(
        !output.status.success(),
        "validate accepted a hand-edited region"
    );
    let combined = format!(
        "{}{}",
        String::from_utf8_lossy(&output.stdout),
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(
        combined.contains(CATALOG_DOC),
        "the failure must name the drifted document, got:\n{combined}"
    );
    world.output = Some(output);
}

#[then("it exits 0 after rhino-cli harness catalog generate is re-run")]
fn validate_clean_after_regeneration(world: &mut CatalogWorld) {
    let regenerated = run_bin(world.root(), &["harness", "catalog", "generate"]);
    assert!(
        regenerated.status.success(),
        "regeneration failed: {}",
        String::from_utf8_lossy(&regenerated.stderr)
    );
    let output = run_bin(world.root(), &["harness", "catalog", "validate"]);
    assert!(
        output.status.success(),
        "validate still failing after regeneration: {}",
        String::from_utf8_lossy(&output.stderr)
    );
    assert!(
        !world.doc().contains("Tampered Harness"),
        "regeneration left the hand edit in place"
    );
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

#[tokio::main]
async fn main() {
    CatalogWorld::cucumber()
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

fn feature_dir() -> std::path::PathBuf {
    std::path::PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/harness")
        .canonicalize()
        .expect("feature dir resolvable")
}
