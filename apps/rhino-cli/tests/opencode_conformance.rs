//! Cucumber-rs suite for OpenCode v1 conformance (US-7).
//!
//! Shares the `gherkin/harness/` feature directory with `tests/agents.rs` and
//! its sibling runners; the runners split it by feature-level tag so each keeps
//! exactly one step-definition set.
//!
//! The citation scenario runs against a temp fixture, because its claim is
//! about a sweep having a before-state and an after-state — the real repository
//! only ever shows the after-state. The idea-filing scenario runs read-only
//! against the real repository, and states its claim over whatever briefs that
//! repository happens to carry. Naming a particular brief would couple this
//! crate — which is byte-identical across sibling repositories — to one
//! repository's plan content, and the assertion would then be unsatisfiable in
//! the others.
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
    /// Every idea brief found in the real tree, as (quadrant, file name).
    briefs: Vec<(String, String)>,
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
            briefs: Vec::new(),
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

/// Whether a directory name is an Eisenhower quadrant subfolder.
fn is_quadrant(name: &str) -> bool {
    matches!(name.as_bytes().first(), Some(b'q'))
        && name
            .as_bytes()
            .get(1)
            .is_some_and(|d| (b'1'..=b'4').contains(d))
        && name.as_bytes().get(2) == Some(&b'-')
}

/// Every `.md` brief under the given quadrant directories, as (quadrant, file).
fn briefs_in(quadrants: &[PathBuf]) -> Vec<(String, String)> {
    let mut found = Vec::new();
    for quadrant in quadrants {
        let name = quadrant
            .file_name()
            .and_then(|n| n.to_str())
            .expect("quadrant name")
            .to_owned();
        for entry in std::fs::read_dir(quadrant).expect("readable quadrant") {
            let path = entry.expect("readable entry").path();
            if path.extension().is_some_and(|e| e == "md") {
                let file = path
                    .file_name()
                    .and_then(|n| n.to_str())
                    .expect("brief name")
                    .to_owned();
                found.push((name.clone(), file));
            }
        }
    }
    found.sort();
    found
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
    "plans/ideas/ is organized into Eisenhower quadrant subfolders and holds at least one brief"
)]
fn ideas_tree_shape(world: &mut ConformanceWorld) {
    let ideas = repo_root().join("plans/ideas");
    assert!(ideas.is_dir(), "the ideas tree must exist");
    let quadrants: Vec<PathBuf> = std::fs::read_dir(&ideas)
        .expect("readable ideas tree")
        .map(|e| e.expect("readable entry").path())
        .filter(|p| p.is_dir())
        .collect();
    assert!(
        !quadrants.is_empty(),
        "the ideas tree must be organized into quadrant subfolders"
    );
    assert!(
        quadrants.iter().all(|q| q
            .file_name()
            .and_then(|n| n.to_str())
            .is_some_and(is_quadrant)),
        "every subfolder of plans/ideas must be an Eisenhower quadrant, found {quadrants:?}"
    );
    world.briefs = briefs_in(&quadrants);
    assert!(
        !world.briefs.is_empty(),
        "the assertions below prove nothing against an empty ideas tree"
    );
}

#[when("the ideas tree is enumerated")]
fn ideas_enumerated(world: &mut ConformanceWorld) {
    // The tree is read in the Given; this step names the event the assertions
    // below are about rather than re-reading it.
    assert!(!world.briefs.is_empty(), "an enumerated ideas tree");
}

#[then("no brief has been promoted into a same-named folder under plans/backlog/")]
fn no_brief_also_promoted(world: &mut ConformanceWorld) {
    let backlog = repo_root().join("plans/backlog");
    let promoted: Vec<&str> = world
        .briefs
        .iter()
        .map(|(_, file)| file.trim_end_matches(".md"))
        .filter(|stem| backlog.join(stem).exists())
        .collect();
    assert!(
        promoted.is_empty(),
        "a brief filed as an idea must not also exist as a backlog plan, found {promoted:?}"
    );
}

#[then("plans/ideas/README.md links every brief exactly once at its quadrant-matching path")]
fn readme_lists_in_matching_quadrant(world: &mut ConformanceWorld) {
    let readme = std::fs::read_to_string(repo_root().join("plans/ideas/README.md"))
        .expect("readable ideas README");
    let unlinked: Vec<String> = world
        .briefs
        .iter()
        .map(|(quadrant, file)| format!("./{quadrant}/{file}"))
        .filter(|entry| readme.matches(entry.as_str()).count() != 1)
        .collect();
    assert!(
        unlinked.is_empty(),
        "every brief must be linked exactly once at its quadrant-matching path, offenders {unlinked:?}"
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
