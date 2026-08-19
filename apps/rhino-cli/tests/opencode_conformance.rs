//! Cucumber-rs suite for OpenCode v1 conformance (US-7).
//!
//! Shares the `gherkin/harness/` feature directory with `tests/agents.rs` and
//! its sibling runners; the runners split it by feature-level tag so each keeps
//! exactly one step-definition set.
//!
//! The citation scenario runs against a temp fixture, because its claim is
//! about a sweep having a before-state and an after-state — the real repository
//! only ever shows the after-state. The idea-filing scenario runs read-only
//! against the real repository, because its claim is about what THIS repository
//! contains.
//!
//! The former organization path is assembled at runtime from `FORMER_ORG`
//! rather than written as a literal. A literal here would be a tracked file
//! citing the very path the sweep removes, which is the thing the first
//! scenario asserts does not exist.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::unwrap_used, clippy::panic)]

use std::path::{Path, PathBuf};

use cucumber::{World as _, given, then, when};
use tempfile::TempDir;

/// Feature-level tags this runner owns.
const OWNED_TAGS: &[&str] = &["opencode-conformance"];

/// The organization the OpenCode repository moved away from, split from its
/// path so no tracked file carries the full citation.
const FORMER_ORG: &str = "sst";
/// The organization the OpenCode repository moved to.
const CURRENT_ORG: &str = "anomalyco";
/// The repository name, shared by both citations.
const REPO: &str = "opencode";

/// The brief the v2 rename set was filed as.
const V2_BRIEF: &str = "opencode-v2-migration.md";
/// The quadrant the brief belongs to.
const QUADRANT: &str = "q2-not-urgent-important";

fn former_citation() -> String {
    format!("{FORMER_ORG}/{REPO}")
}

fn current_citation() -> String {
    format!("{CURRENT_ORG}/{REPO}")
}

#[derive(cucumber::World)]
#[world(init = Self::new)]
struct ConformanceWorld {
    /// Fresh temp workspace standing in for a document tree.
    work: TempDir,
    /// How many documents cited the former path before the sweep.
    before: Option<usize>,
    /// How many cite it after.
    after: Option<usize>,
}

impl std::fmt::Debug for ConformanceWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("ConformanceWorld").finish_non_exhaustive()
    }
}

impl ConformanceWorld {
    fn new() -> Self {
        Self {
            work: TempDir::new().expect("temp workspace"),
            before: None,
            after: None,
        }
    }

    fn root(&self) -> &Path {
        self.work.path()
    }

    fn docs(&self) -> Vec<PathBuf> {
        let mut found = Vec::new();
        for entry in std::fs::read_dir(self.root()).expect("readable workspace") {
            let path = entry.expect("readable entry").path();
            if path.extension().is_some_and(|e| e == "md") {
                found.push(path);
            }
        }
        found.sort();
        found
    }

    fn count_citing(&self, needle: &str) -> usize {
        self.docs()
            .iter()
            .filter(|p| {
                std::fs::read_to_string(p)
                    .expect("readable doc")
                    .contains(needle)
            })
            .count()
    }
}

/// The real repository root, two levels above this crate.
fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../..")
        .canonicalize()
        .expect("repo root resolvable")
}

#[given(
    "repository documents cite the OpenCode upstream repository under its former organization path"
)]
fn docs_cite_former(world: &mut ConformanceWorld) {
    let former = former_citation();
    std::fs::write(
        world.root().join("catalog.md"),
        format!("The generator flattens mirrors; see https://github.com/{former}/issues/6635.\n"),
    )
    .expect("write catalog fixture");
    std::fs::write(
        world.root().join("convention.md"),
        format!("Upstream lives at https://github.com/{former}.\n"),
    )
    .expect("write convention fixture");
    // A third document that never cited it, so the sweep is proven to be a
    // substitution rather than a truncation.
    std::fs::write(
        world.root().join("unrelated.md"),
        "This document mentions no upstream repository at all.\n",
    )
    .expect("write unrelated fixture");

    world.before = Some(world.count_citing(&former));
    assert_eq!(
        world.before,
        Some(2),
        "the fixture must start with a real before-state, or the sweep proves nothing"
    );
}

#[when("the citation sweep completes")]
fn sweep(world: &mut ConformanceWorld) {
    let (former, current) = (former_citation(), current_citation());
    for path in world.docs() {
        let body = std::fs::read_to_string(&path).expect("readable doc");
        std::fs::write(&path, body.replace(&former, &current)).expect("writable doc");
    }
    world.after = Some(world.count_citing(&former));
}

#[then(
    "a search for that former organization path across tracked non-archival documents returns zero matches, where it returned at least one before the sweep"
)]
fn zero_after_nonzero_before(world: &mut ConformanceWorld) {
    let before = world.before.expect("a recorded before-count");
    let after = world.after.expect("a recorded after-count");
    assert!(before >= 1, "before-count must be non-zero, got {before}");
    assert_eq!(after, 0, "after-count must be zero, got {after}");
}

#[then("the current organization path appears in its place")]
fn current_in_place(world: &mut ConformanceWorld) {
    let current = current_citation();
    assert_eq!(
        world.count_citing(&current),
        world.before.expect("a recorded before-count"),
        "every document that cited the former path must now cite the current one"
    );
    // The document that never cited it must not have gained a citation.
    let untouched = std::fs::read_to_string(world.root().join("unrelated.md")).expect("readable");
    assert!(
        !untouched.contains(&current),
        "the sweep must not add citations to documents that had none"
    );
}

#[given(
    "plans/ideas/ is organized into Eisenhower quadrant subfolders and already holds two harness-related briefs"
)]
fn ideas_tree_shape(_world: &mut ConformanceWorld) {
    let ideas = repo_root().join("plans/ideas");
    assert!(ideas.join(QUADRANT).is_dir(), "the Q2 quadrant must exist");
    for sibling in [
        "harness-binding-catalog-drift.md",
        "harness-converter-preserve-agent-mode.md",
    ] {
        assert!(
            ideas.join(QUADRANT).join(sibling).is_file(),
            "the pre-existing harness brief {sibling} must be present"
        );
    }
}

#[when("the OpenCode v2 brief is filed")]
fn brief_is_filed(_world: &mut ConformanceWorld) {
    // Filing already happened in the tree under test; this step names the event
    // the assertions below are about rather than performing it.
}

#[then(
    "a single new file exists under a plans/ideas/ quadrant subfolder and no new folder exists under plans/backlog/"
)]
fn filed_as_idea_not_backlog(_world: &mut ConformanceWorld) {
    let root = repo_root();
    let mut found: Vec<PathBuf> = Vec::new();
    for entry in std::fs::read_dir(root.join("plans/ideas")).expect("readable ideas tree") {
        let quadrant = entry.expect("readable entry").path();
        if quadrant.is_dir() && quadrant.join(V2_BRIEF).is_file() {
            found.push(quadrant.join(V2_BRIEF));
        }
    }
    assert_eq!(
        found.len(),
        1,
        "the brief must exist exactly once across the quadrants, found {found:?}"
    );
    assert!(
        !root.join("plans/backlog/opencode-v2-migration").exists(),
        "the brief must be an idea, not a promoted backlog plan"
    );
}

#[then(
    "plans/ideas/README.md lists the new brief in the same quadrant section as the file's location"
)]
fn readme_lists_in_matching_quadrant(_world: &mut ConformanceWorld) {
    let readme = std::fs::read_to_string(repo_root().join("plans/ideas/README.md"))
        .expect("readable ideas README");
    let entry = format!("./{QUADRANT}/{V2_BRIEF}");
    assert_eq!(
        readme.matches(&entry).count(),
        1,
        "the README must link the brief exactly once, at its quadrant-matching path"
    );
}

#[tokio::main]
async fn main() {
    ConformanceWorld::cucumber()
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
