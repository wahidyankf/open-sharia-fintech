//! Cucumber-rs integration tests for `specs/apps/rhino/behavior/rhino-cli/gherkin/specs/`.
//!
//! Wires all 13 feature files under `gherkin/specs/`, spanning eight distinct
//! validator domains:
//!
//! - `behavior-coverage.feature` / `domain-coverage.feature`: the per-level
//!   `@covers` engine at `application::behavior_coverage::validator::validate`
//!   (plus `application::domain_coverage`'s allowlist gate). **Historical
//!   note, corrected**: this doc comment used to say the live CLI verb
//!   `specs behavior-coverage validate` (`commands::specs_coverage::run`)
//!   never called this engine — true when these scenarios were first wired,
//!   no longer true. `commands::specs_coverage::run_three_level` now calls
//!   `validator::validate` directly (see `spec_coverage.rs`'s own runtime
//!   cross-check scenarios, which drive the real CLI subprocess end-to-end
//!   in three-level mode). The scenarios below still call the engine
//!   in-process rather than through the CLI, but now purely as a testing-style
//!   choice — isolating `validate`'s pure matching logic against hand-built
//!   `ScenarioSpec`/`CoversMarker` values, the same precedent already set for
//!   `ddd`/`test-coverage` — not because the CLI path is unreachable.
//! - `env-staged-guard.feature`: the real `env staged-guard validate` CLI verb,
//!   driven as a subprocess against a synthetic git-rooted fixture.
//! - `e2e-coverage.feature`: the real `specs e2e-coverage validate` CLI verb
//!   (`commands::specs_e2e_coverage::run`), driven as a subprocess against a
//!   synthetic playwright-bdd-shaped fixture — `.feature` files declaring
//!   `@e2e`-tagged scenarios, generated `.spec.js` output containing
//!   `test.fixme(...)` calls, and (where the scenario needs one) a
//!   checked-in baseline manifest. The manifest is bootstrapped via the
//!   command's own `--update-baseline` flag rather than hand-written, so its
//!   `feature` paths are byte-identical to the absolute, glob-resolved paths
//!   the real command computes at runtime.
//! - `harness-bindings.feature` / `harness-registry-driven.feature`: harness
//!   binding/naming/instruction-size/duplication validators. `harness bindings
//!   validate`'s core (`application::agents::bindings::validate_bindings`) is
//!   driven in-process against the real repository's `repo-config.yml` (its
//!   own `#[cfg(test)]` module already proves the exact "all 11 harnesses"
//!   claim this feature makes); naming/instruction-size/duplication are driven
//!   as subprocesses against a synthetic repo-config.yml with renamed
//!   (non-`.claude`/`.opencode`) tier directories, to prove they are
//!   registry-driven rather than hard-coded.
//! - `validate-adoption.feature` / `validate-tree.feature`: `specs
//!   validate-adoption` / `specs validate-tree` no longer exist as CLI verbs —
//!   `cli.rs`'s own test suite documents both were merged into `specs
//!   structure validate`. That merged command also runs unrelated
//!   counts/bc/ul layers the scenarios don't set up fixtures for, so these
//!   scenarios call the underlying `application::specs::validate_spec_adoption`
//!   / `validate_spec_tree` functions directly in-process instead (same
//!   precedent as `ddd`/`test-coverage`).
//! - `validate-counts.feature`: `specs counts validate` is a real, still-live
//!   standalone CLI leaf (kept for spec trees outside `specs/apps/`, e.g.
//!   `specs/libs/*` — see `commands::specs_validate_counts`'s own doc comment)
//!   — driven here via its public `run_at_root` testable entry point.
//! - `validate-links.feature`: `specs validate-links` was deleted outright
//!   (not merged) — `md links validate`'s own regression test
//!   (`md_links_validate_covers_specs_dir`) proves the generic link validator
//!   already covers `specs/**`. Since no dormant per-folder wrapper exists,
//!   [`run_validate_links_at`] composes the still-live
//!   `application::docs::links::validate_all_links` with a folder-existence
//!   precheck (the "does not exist" scenario), replicating what a standalone
//!   `specs validate-links <folder>` leaf would have done.
//! - `worktree-agnostic.feature`: replicates the existing regression test
//!   `find_root_from_worktree_returns_worktree_path` in
//!   `infrastructure::git::root`, whose own doc comment already quotes this
//!   exact Gherkin.
//! - `specs-audit.feature`: the real `specs audit` CLI verb (aggregates
//!   `structure-validate`, `validate-links`, and `gherkin-cardinality`),
//!   driven as a subprocess against the same synthetic git-rooted `work`
//!   fixture the other subprocess-driven domains above share.
//! - `gherkin-cardinality.feature`: the real `specs gherkin-cardinality
//!   validate` CLI verb (`application::repo_governance::gherkin_keyword_cardinality_audit`),
//!   driven as a subprocess against a single synthetic offending `.feature`
//!   file written into the shared `work` fixture.

// Test step-definition scaffolding: private World state and step fns are
// self-documenting via their #[given]/#[when]/#[then] gherkin strings.
#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::needless_pass_by_value)] // cucumber-rs binds regex captures by value
#![allow(clippy::used_underscore_binding)] // cucumber-rs macro-generated call sites reference every bound capture by name

use std::collections::HashSet;
use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::process::{Command, Output};

use assert_cmd::cargo::cargo_bin;
use cucumber::{World as _, given, then, when};
use rhino_cli::application::agents::bindings::{
    KNOWN_BINDING_DIRS, PLATFORM_BINDINGS_CATALOG, emit_bindings, validate_bindings,
};
use rhino_cli::application::agents::types::ValidationResult;
use rhino_cli::application::behavior_coverage::types::{
    BehaviorCoverageViolation, CoversMarker, ProjectEnvelope, ScenarioSpec, TestLevel,
};
use rhino_cli::application::behavior_coverage::validator::validate;
use rhino_cli::application::docs::links::{ScanOptions, validate_all_links};
use rhino_cli::application::domain_coverage;
use rhino_cli::application::repo_config::{self, HarnessEntry};
use rhino_cli::application::specs::{
    SpecFinding, validate_spec_adoption, validate_spec_tree as validate_spec_tree_fn,
};
use rhino_cli::commands::specs_validate_counts::{self, ValidateCountsArgs};
use rhino_cli::infrastructure::git::root::find_root_from;
use tempfile::TempDir;

/// Repo-relative feature-file path shared by every synthetic `@covers`
/// scenario/marker built in the behavior-coverage/domain-coverage steps.
const BC_FEATURE_PATH: &str = "specs/apps/example/foo.feature";

/// Project-relative glob (relative to the synthetic project root in `work`)
/// matching every `.feature` file the e2e-coverage.feature subprocess
/// fixtures declare scenarios into. Passed verbatim as `--features` to every
/// `specs e2e-coverage validate` invocation in that block.
const EC_FEATURES_GLOB: &str = "features/*.feature";
/// Project-relative directory the [`EC_FEATURES_GLOB`] fixture lives under.
const EC_FEATURES_DIR: &str = "features";
/// Filename of the single shared `.feature` file scenarios 1-5 and 7-8 of
/// e2e-coverage.feature declare scenarios into. ("Output identifies each new
/// gap by feature path and scenario title" uses its own dedicated
/// file/title instead, matching its Gherkin's explicit filename.)
const EC_FEATURE_FILE: &str = "example.feature";
/// Project-relative directory playwright-bdd's generated `.spec.js` output
/// lives in for the e2e-coverage.feature subprocess fixtures.
const EC_FEATURES_GEN_DIR: &str = ".features-gen";
/// Filename of the generated `.spec.js` fixture written under
/// [`EC_FEATURES_GEN_DIR`]. Deliberately keeps [`EC_FEATURE_FILE`]'s
/// `.feature` extension and appends `.spec.js` (i.e.
/// `example.feature.spec.js`, not `example.spec.js`) to match playwright-bdd's
/// real generated-filename convention — the same convention the `is_fixme`/
/// `path_ends_with` pairing logic in `commands/specs_e2e_coverage.rs` relies
/// on to match a declared scenario to its originating generated file. Using
/// the pre-convention name here made `is_fixme` return `false` for every
/// scenario this fixture writes (see the cycle-2 PR review finding that
/// caught this).
const EC_SPEC_JS_FILE: &str = "example.feature.spec.js";
/// Project-relative path to the checked-in baseline manifest.
const EC_BASELINE_PATH: &str = "e2e-coverage-baseline.json";

/// Shared scenario state spanning all 13 feature files under `gherkin/specs/`.
#[derive(cucumber::World)]
#[world(init = Self::new)]
struct SpecsTreeWorld {
    /// Generic fixture workspace for the file-tree-based domains (adoption,
    /// tree, counts, links, env-staged-guard). Always a git repo (harmless
    /// for the non-git domains) so the env-staged-guard scenarios can stage
    /// files and the CLI subprocess can resolve a git root.
    work: TempDir,

    // --- behavior-coverage.feature / domain-coverage.feature (pure engine) ---
    bc_scenarios: Vec<ScenarioSpec>,
    bc_markers: Vec<CoversMarker>,
    bc_envelope: ProjectEnvelope,
    bc_violations: Vec<BehaviorCoverageViolation>,
    bc_exempt_count: usize,
    dc_project_name: String,
    dc_domain_areas: Vec<String>,
    dc_eligible: bool,

    // --- env-staged-guard.feature (subprocess) ---
    output: Option<Output>,

    // --- e2e-coverage.feature (subprocess) ---
    /// `@e2e`-tagged scenario titles declared so far into the shared
    /// [`EC_FEATURE_FILE`] fixture — cumulative across a scenario's Given
    /// steps regardless of their Gherkin order, since [`SpecsTreeWorld::ec_write_feature_file`]
    /// always regenerates the whole file from this list.
    ec_declared_titles: Vec<String>,
    /// `@unit`-only (non-`@e2e`) scenario titles declared into the shared
    /// fixture — used by the "not `@e2e`-tagged" ignore scenario.
    ec_unit_only_titles: Vec<String>,
    /// The most recently written "current" `test.fixme` title set (may
    /// differ from any set used to bootstrap the baseline earlier in the
    /// same scenario) — lets Then steps assert fixture-level invariants the
    /// CLI's own text output does not expose (e.g. a total count).
    ec_fixme_titles: Vec<String>,

    // --- validate-adoption.feature / validate-tree.feature / validate-counts.feature /
    // validate-links.feature (in-process, shared exit/output slots) ---
    last_output: String,
    last_exit_ok: bool,

    // --- harness-bindings.feature (in-process, real repo-config.yml) ---
    hb_harness: Vec<HarnessEntry>,
    hb_result: Option<ValidationResult>,

    // --- harness-registry-driven.feature (subprocess, synthetic repo-config.yml) ---
    hrd_work: Option<TempDir>,
    hrd_naming_output: Option<Output>,
    hrd_instr_output: Option<Output>,
    hrd_dup_output: Option<Output>,

    // --- worktree-agnostic.feature (in-process) ---
    wt_main: Option<TempDir>,
    wt_worktree_dir: Option<TempDir>,
    wt_path: Option<PathBuf>,
    wt_resolved: Option<anyhow::Result<PathBuf>>,
}

impl std::fmt::Debug for SpecsTreeWorld {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("SpecsTreeWorld")
            .field("dc_project_name", &self.dc_project_name)
            .finish_non_exhaustive()
    }
}

impl SpecsTreeWorld {
    fn new() -> Self {
        let work = TempDir::new().expect("temp workspace");
        run_git(work.path(), &["init", "-q"]);
        Self {
            work,
            bc_scenarios: Vec::new(),
            bc_markers: Vec::new(),
            bc_envelope: ProjectEnvelope {
                levels: HashSet::new(),
            },
            bc_violations: Vec::new(),
            bc_exempt_count: 0,
            dc_project_name: String::new(),
            dc_domain_areas: Vec::new(),
            dc_eligible: false,
            output: None,
            ec_declared_titles: Vec::new(),
            ec_unit_only_titles: Vec::new(),
            ec_fixme_titles: Vec::new(),
            last_output: String::new(),
            last_exit_ok: false,
            hb_harness: Vec::new(),
            hb_result: None,
            hrd_work: None,
            hrd_naming_output: None,
            hrd_instr_output: None,
            hrd_dup_output: None,
            wt_main: None,
            wt_worktree_dir: None,
            wt_path: None,
            wt_resolved: None,
        }
    }

    /// Writes `content` at repo-relative path `rel` inside `self.work`,
    /// creating parent directories as needed.
    fn write(&self, rel: &str, content: &str) {
        let p = self.work.path().join(rel);
        if let Some(parent) = p.parent() {
            std::fs::create_dir_all(parent).expect("mk fixture dir");
        }
        std::fs::write(p, content).expect("write fixture");
    }

    /// Writes `content` at `rel` inside `self.work` and `git add`s it.
    fn write_and_stage(&self, rel: &str, content: &str) {
        self.write(rel, content);
        self.git(&["add", rel]);
    }

    fn git(&self, args: &[&str]) {
        run_git(self.work.path(), args);
    }

    /// Runs the compiled `rhino-cli` binary against `self.work` and records
    /// the result in `self.output`.
    fn exec(&mut self, args: &[&str]) {
        self.output = Some(run_rhino(self.work.path(), args));
    }

    /// Regenerates [`EC_FEATURE_FILE`] from `self.ec_declared_titles`
    /// (`@e2e`-tagged) and `self.ec_unit_only_titles` (`@unit`-only),
    /// overwriting any previous content. Safe to call repeatedly as Given
    /// steps grow either list, in any order.
    fn ec_write_feature_file(&self) {
        let mut body = String::from("Feature: fixture\n\n");
        for t in &self.ec_declared_titles {
            let _ = writeln!(body, "@e2e\nScenario: {t}\n  Given a step\n");
        }
        for t in &self.ec_unit_only_titles {
            let _ = writeln!(body, "@unit\nScenario: {t}\n  Given a step\n");
        }
        self.write(&format!("{EC_FEATURES_DIR}/{EC_FEATURE_FILE}"), &body);
    }

    /// Adds any of `titles` not yet tracked to `self.ec_declared_titles`
    /// (the `@e2e` declared set) and regenerates [`EC_FEATURE_FILE`].
    fn ec_ensure_declared(&mut self, titles: &[&str]) {
        for t in titles.iter().copied() {
            if !self.ec_declared_titles.iter().any(|d| d.as_str() == t) {
                self.ec_declared_titles.push(t.to_string());
            }
        }
        self.ec_write_feature_file();
    }

    /// Overwrites the generated `.spec.js` fixture at [`EC_SPEC_JS_FILE`] so
    /// exactly `titles` are marked `test.fixme` — the "current" unbound set
    /// a subsequent validate run observes. Also records `titles` into
    /// `self.ec_fixme_titles` for Then-step introspection.
    ///
    /// Every OTHER currently-tracked `@e2e` declared title (in
    /// `self.ec_declared_titles`, not present in `titles`) is emitted as an
    /// ordinary bound `test(...)` call — faithfully mirroring real
    /// playwright-bdd output, where every declared scenario in a processed
    /// `.feature` file gets EITHER a `test`/`test.fixme` call. Omitting a
    /// non-fixme'd declared title from the generated fixture entirely (as
    /// this helper did before the cycle-4 general absence fix) would now be
    /// misread as "absent from rendered output" and falsely reported as a
    /// gap — this is what the general fix is designed to catch for a REAL
    /// zero-row Outline, so the fixture must not manufacture a false
    /// positive of that same shape for an ordinary bound scenario.
    fn ec_write_fixme(&mut self, titles: &[&str]) {
        self.ec_fixme_titles = titles.iter().map(|t| (*t).to_string()).collect();
        let mut body = String::new();
        for t in titles {
            let _ = writeln!(body, "test.fixme(\"{t}\", async ({{ page }}) => {{}});");
        }
        for t in &self.ec_declared_titles {
            if !titles.contains(&t.as_str()) {
                let _ = writeln!(body, "test(\"{t}\", async ({{ page }}) => {{}});");
            }
        }
        self.write(&format!("{EC_FEATURES_GEN_DIR}/{EC_SPEC_JS_FILE}"), &body);
    }

    /// Bootstraps the checked-in baseline manifest at [`EC_BASELINE_PATH`]
    /// to exactly `titles` by running the real CLI's `--update-baseline`
    /// flag against a temporary `test.fixme` fixture matching `titles`.
    ///
    /// This is the only way to get the manifest's `feature` paths
    /// byte-identical to what the real command later computes (an
    /// absolute, glob-resolved path) instead of guessing them by hand.
    fn ec_bootstrap_baseline(&mut self, titles: &[&str]) {
        self.ec_ensure_declared(titles);
        self.ec_write_fixme(titles);
        let out = run_rhino(
            self.work.path(),
            &[
                "specs",
                "e2e-coverage",
                "validate",
                "--update-baseline",
                "--features",
                EC_FEATURES_GLOB,
                "--features-gen",
                EC_FEATURES_GEN_DIR,
                "--baseline",
                EC_BASELINE_PATH,
                "--project",
                "test-project",
            ],
        );
        assert!(
            out.status.success(),
            "baseline bootstrap must succeed: {}",
            combined_output(&out)
        );
    }
}

/// Runs `git` with `args` inside `dir`, using a fixed synthetic identity.
fn run_git(dir: &Path, args: &[&str]) {
    Command::new("git")
        .args(args)
        .current_dir(dir)
        .env("GIT_AUTHOR_NAME", "t")
        .env("GIT_AUTHOR_EMAIL", "t@t")
        .env("GIT_COMMITTER_NAME", "t")
        .env("GIT_COMMITTER_EMAIL", "t@t")
        .output()
        .expect("git command");
}

/// Runs the compiled `rhino-cli` binary with `args` inside `dir` and returns
/// its captured `Output`.
fn run_rhino(dir: &Path, args: &[&str]) -> Output {
    let mut cmd = Command::new(cargo_bin("rhino-cli"));
    cmd.args(args).arg("--no-color").current_dir(dir);
    cmd.output().expect("run rhino-cli")
}

/// Concatenates stdout and stderr, mirroring how a developer watching a
/// terminal sees both streams interleaved.
fn combined_output(out: &Output) -> String {
    format!(
        "{}{}",
        String::from_utf8_lossy(&out.stdout),
        String::from_utf8_lossy(&out.stderr)
    )
}

/// Renders `findings` the same way the sibling `specs *validate*` commands
/// do (`"{file}: {criticality}: {evidence}"` per line, or a `0 finding(s)`
/// summary line when clean), returning `(text, exit_ok)`.
fn render_spec_findings(findings: &[SpecFinding]) -> (String, bool) {
    if findings.is_empty() {
        return ("0 finding(s)\n".to_string(), true);
    }
    let mut out = String::new();
    for f in findings {
        let _ = writeln!(out, "{}: {}: {}", f.file, f.criticality, f.evidence);
    }
    (out, false)
}

/// Composes a folder-existence precheck with [`validate_all_links`] to
/// replicate the deleted `specs validate-links <folder>` leaf: no dormant
/// wrapper exists to call directly (see the module doc), so this rebuilds
/// its historical behavior from the still-live building blocks.
fn run_validate_links_at(folder: &Path) -> (String, bool) {
    if !folder.exists() {
        return (
            format!("spec folder does not exist: {}\n", folder.display()),
            false,
        );
    }
    let opts = ScanOptions {
        repo_root: folder.to_path_buf(),
        staged_only: false,
        skip_paths: Vec::new(),
    };
    match validate_all_links(&opts) {
        Ok(result) if result.broken_links.is_empty() => ("0 finding(s)\n".to_string(), true),
        Ok(result) => {
            let mut out = String::new();
            for b in &result.broken_links {
                let _ = writeln!(
                    out,
                    "broken link: {}:{}: {}",
                    b.source_file, b.line_number, b.link_text
                );
            }
            (out, false)
        }
        Err(e) => (e.to_string(), false),
    }
}

// ===========================================================================
// behavior-coverage.feature — Given steps
// ===========================================================================

#[given("a scenario with no @unit, @integration, or @e2e level tag")]
fn given_bc_untagged(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: BC_FEATURE_PATH.to_string(),
        title: "Untagged scenario".to_string(),
        level_tags: HashSet::new(),
        is_wip: false,
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit].into_iter().collect(),
    };
}

#[given("a project whose coverage registry declares only the unit level")]
fn given_bc_envelope_unit_only(w: &mut SpecsTreeWorld) {
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit].into_iter().collect(),
    };
}

#[given("a scenario in that project tagged @integration")]
fn given_bc_scenario_tagged_integration(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: BC_FEATURE_PATH.to_string(),
        title: "Integration scenario".to_string(),
        level_tags: [TestLevel::Integration].into_iter().collect(),
        is_wip: false,
    });
}

#[given("a scenario tagged @unit and @e2e")]
fn given_bc_scenario_unit_and_e2e(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: BC_FEATURE_PATH.to_string(),
        title: "Multi-level scenario".to_string(),
        level_tags: [TestLevel::Unit, TestLevel::E2e].into_iter().collect(),
        is_wip: false,
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit, TestLevel::E2e].into_iter().collect(),
    };
}

#[given("a test marks it @covers at the unit level only")]
fn given_bc_marker_unit_only(w: &mut SpecsTreeWorld) {
    let title = w
        .bc_scenarios
        .last()
        .expect("scenario set first")
        .title
        .clone();
    w.bc_markers.push(CoversMarker {
        source_file: "apps/example/src/test.rs".to_string(),
        level: TestLevel::Unit,
        feature_path: BC_FEATURE_PATH.to_string(),
        scenario_title: title,
    });
}

#[given("a scenario tagged @unit only")]
fn given_bc_scenario_unit_only(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: BC_FEATURE_PATH.to_string(),
        title: "Unit-only scenario".to_string(),
        level_tags: [TestLevel::Unit].into_iter().collect(),
        is_wip: false,
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit, TestLevel::E2e].into_iter().collect(),
    };
}

#[given("a test marks it @covers at the e2e level")]
fn given_bc_marker_e2e(w: &mut SpecsTreeWorld) {
    let title = w
        .bc_scenarios
        .last()
        .expect("scenario set first")
        .title
        .clone();
    w.bc_markers.push(CoversMarker {
        source_file: "apps/example-e2e/tests/test.spec.ts".to_string(),
        level: TestLevel::E2e,
        feature_path: BC_FEATURE_PATH.to_string(),
        scenario_title: title,
    });
}

#[given("a test with an @covers marker referencing a scenario title that no feature file contains")]
fn given_bc_orphan_marker(w: &mut SpecsTreeWorld) {
    w.bc_markers.push(CoversMarker {
        source_file: "apps/example/src/test.rs".to_string(),
        level: TestLevel::Unit,
        feature_path: BC_FEATURE_PATH.to_string(),
        scenario_title: "Non-existent scenario".to_string(),
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit].into_iter().collect(),
    };
}

#[given("a scenario tagged @wip with no @covers markers")]
fn given_bc_wip_scenario(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: BC_FEATURE_PATH.to_string(),
        title: "WIP scenario".to_string(),
        level_tags: HashSet::new(),
        is_wip: true,
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit].into_iter().collect(),
    };
}

// ===========================================================================
// behavior-coverage.feature — When + Then steps
// ===========================================================================

#[when("rhino-cli specs behavior-coverage validate runs")]
fn when_bc_validate_runs(w: &mut SpecsTreeWorld) {
    w.bc_violations = validate(&w.bc_scenarios, &w.bc_markers, &w.bc_envelope);
    w.bc_exempt_count = w.bc_scenarios.iter().filter(|s| s.is_wip).count();
}

#[then("it fails and names the untagged scenario")]
fn then_bc_names_untagged(w: &mut SpecsTreeWorld) {
    assert!(
        w.bc_violations.iter().any(|v| matches!(
            v,
            BehaviorCoverageViolation::UntaggedScenario { title, .. } if title == "Untagged scenario"
        )),
        "got: {:?}",
        w.bc_violations
    );
}

#[then("it fails because the scenario requires a level not in the project envelope")]
fn then_bc_level_outside_envelope(w: &mut SpecsTreeWorld) {
    assert!(
        w.bc_violations
            .iter()
            .any(|v| matches!(v, BehaviorCoverageViolation::LevelOutsideEnvelope { .. })),
        "got: {:?}",
        w.bc_violations
    );
}

#[then("it fails and names the missing e2e coverage")]
fn then_bc_missing_e2e(w: &mut SpecsTreeWorld) {
    assert!(
        w.bc_violations.iter().any(|v| matches!(
            v,
            BehaviorCoverageViolation::MissingCoverage {
                missing_level: TestLevel::E2e,
                ..
            }
        )),
        "got: {:?}",
        w.bc_violations
    );
}

#[then("it fails because the e2e level is not declared for that scenario")]
fn then_bc_undeclared_e2e(w: &mut SpecsTreeWorld) {
    assert!(
        w.bc_violations.iter().any(|v| matches!(
            v,
            BehaviorCoverageViolation::CoverageAtUndeclaredLevel { .. }
        )),
        "got: {:?}",
        w.bc_violations
    );
}

#[then("it fails and names the orphan marker")]
fn then_bc_orphan(w: &mut SpecsTreeWorld) {
    assert!(
        w.bc_violations.iter().any(|v| matches!(
            v,
            BehaviorCoverageViolation::OrphanMarker { scenario_title, .. }
                if scenario_title == "Non-existent scenario"
        )),
        "got: {:?}",
        w.bc_violations
    );
}

#[then("it does not fail and reports the scenario in the exempt count")]
fn then_bc_wip_exempt(w: &mut SpecsTreeWorld) {
    assert!(w.bc_violations.is_empty(), "got: {:?}", w.bc_violations);
    assert_eq!(w.bc_exempt_count, 1);
}

// ===========================================================================
// domain-coverage.feature
// ===========================================================================

#[given("a project listed in the specs.domain-areas allowlist")]
fn given_dc_project_listed(w: &mut SpecsTreeWorld) {
    w.dc_domain_areas = vec!["ose-be".to_string()];
    w.dc_project_name = "ose-be".to_string();
}

#[given("a domain scenario not covered at its required level by any @covers marker")]
fn given_dc_uncovered_scenario(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: "specs/apps/ose/behavior/be/domain/foo.feature".to_string(),
        title: "Uncovered domain scenario".to_string(),
        level_tags: [TestLevel::Unit].into_iter().collect(),
        is_wip: false,
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit].into_iter().collect(),
    };
}

#[given("a project not listed in the specs.domain-areas allowlist")]
fn given_dc_project_not_listed(w: &mut SpecsTreeWorld) {
    w.dc_domain_areas = vec!["ose-be".to_string()];
    w.dc_project_name = "rhino-cli".to_string();
}

#[given("that project has domain/** feature files")]
fn given_dc_project_has_domain_features(w: &mut SpecsTreeWorld) {
    w.bc_scenarios.push(ScenarioSpec {
        feature_path: "specs/apps/rhino/behavior/rhino-cli/domain/bar.feature".to_string(),
        title: "Domain scenario for skipped project".to_string(),
        level_tags: [TestLevel::Unit].into_iter().collect(),
        is_wip: false,
    });
    w.bc_envelope = ProjectEnvelope {
        levels: [TestLevel::Unit].into_iter().collect(),
    };
}

#[when("rhino-cli specs domain-coverage validate runs")]
fn when_dc_validate_runs(w: &mut SpecsTreeWorld) {
    w.dc_eligible = domain_coverage::is_eligible(&w.dc_project_name, &w.dc_domain_areas);
    if w.dc_eligible {
        let domain_scenarios: Vec<ScenarioSpec> =
            domain_coverage::filter_domain_scenarios(&w.bc_scenarios)
                .into_iter()
                .cloned()
                .collect();
        w.bc_violations = validate(&domain_scenarios, &w.bc_markers, &w.bc_envelope);
    } else {
        w.bc_violations = Vec::new();
    }
}

#[then("it fails and names the uncovered domain scenario")]
fn then_dc_names_uncovered(w: &mut SpecsTreeWorld) {
    assert!(w.dc_eligible, "project must be eligible for this scenario");
    assert!(
        w.bc_violations.iter().any(|v| matches!(
            v,
            BehaviorCoverageViolation::MissingCoverage { title, .. }
                if title == "Uncovered domain scenario"
        )),
        "got: {:?}",
        w.bc_violations
    );
}

#[then("the project is skipped and no violation is reported")]
fn then_dc_project_skipped(w: &mut SpecsTreeWorld) {
    assert!(
        !w.dc_eligible,
        "project must be skipped (not in domain-areas allowlist)"
    );
    assert!(w.bc_violations.is_empty(), "got: {:?}", w.bc_violations);
}

// ===========================================================================
// env-staged-guard.feature
// ===========================================================================

#[given("a real .env file is staged for commit")]
fn given_env_real_staged(w: &mut SpecsTreeWorld) {
    w.write_and_stage(".env", "SECRET=shh\n");
}

#[given("only .env.example is staged for commit")]
fn given_env_example_staged(w: &mut SpecsTreeWorld) {
    w.write_and_stage(".env.example", "SECRET=\n");
}

#[when("the pre-commit hook runs rhino-cli env staged-guard validate")]
fn when_env_staged_guard_runs(w: &mut SpecsTreeWorld) {
    w.exec(&["env", "staged-guard", "validate"]);
}

#[then("it exits non-zero and names the offending file")]
fn then_env_exits_nonzero_names_file(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    assert!(!out.status.success(), "got: {}", combined_output(out));
    let combined = combined_output(out);
    assert!(combined.contains(".env"), "got: {combined}");
}

#[then("the commit is aborted")]
fn then_env_commit_aborted(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    assert!(!out.status.success(), "got: {}", combined_output(out));
}

#[then("it exits zero and does not block the commit")]
fn then_env_exits_zero(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    assert!(out.status.success(), "got: {}", combined_output(out));
}

// ===========================================================================
// harness-bindings.feature (in-process, against the real repository)
// ===========================================================================

#[given("the harness binding commands and the repo-config.yml harness section")]
fn given_hb_repo_config(w: &mut SpecsTreeWorld) {
    let repo_root = find_root_from(None).expect("real repo root resolvable in test");
    let config = repo_config::load(&repo_root).expect("real repo-config.yml parses");
    w.hb_harness = config.harness;
}

#[when("the harness coverage is inspected")]
fn when_hb_inspected(w: &mut SpecsTreeWorld) {
    let tmp = TempDir::new().expect("temp workspace");
    let root = tmp.path();
    std::fs::create_dir_all(root.join(".claude/agents")).expect("mkdir .claude/agents");
    std::fs::create_dir_all(root.join(".opencode/agents")).expect("mkdir .opencode/agents");
    emit_bindings(root).expect("emit bindings");
    let catalog = root.join(PLATFORM_BINDINGS_CATALOG);
    std::fs::create_dir_all(catalog.parent().expect("catalog has parent"))
        .expect("mkdir catalog parent");
    std::fs::write(
        &catalog,
        "# Platform Bindings\n\n- `.amazonq` row\n- `.claude` row\n- `.opencode` row\n",
    )
    .expect("write catalog");
    w.hb_result = Some(validate_bindings(root));
}

#[then(
    "all 11 supported harnesses are listed (Claude Code, OpenCode, Amazon Q, Codex, Copilot, Cursor, Windsurf, Junie, Antigravity, Pi, Aider)"
)]
fn then_hb_all_11_listed(w: &mut SpecsTreeWorld) {
    let names: HashSet<&str> = w.hb_harness.iter().map(|h| h.name.as_str()).collect();
    assert_eq!(w.hb_harness.len(), 11, "harness list: {names:?}");
    for expected in [
        "claude-code",
        "opencode",
        "amazonq",
        "codex",
        "copilot",
        "cursor",
        "windsurf",
        "junie",
        "antigravity",
        "pi",
        "aider",
    ] {
        assert!(
            names.contains(expected),
            "missing harness {expected:?} in {names:?}"
        );
    }
}

#[then("the generated tier (OpenCode, Amazon Q) is regenerated and byte-parity-validated")]
fn then_hb_generated_tier(w: &mut SpecsTreeWorld) {
    let generated: Vec<&str> = w
        .hb_harness
        .iter()
        .filter(|h| h.tier == "generated")
        .map(|h| h.name.as_str())
        .collect();
    assert_eq!(generated.len(), 2, "generated tier: {generated:?}");
    assert!(generated.contains(&"opencode"));
    assert!(generated.contains(&"amazonq"));

    let result = w.hb_result.as_ref().expect("validate_bindings ran");
    assert_eq!(result.failed_checks, 0, "result: {result:#?}");
    let has_opencode_check = result.checks.iter().any(|c| {
        let n = c.name.to_lowercase();
        n.contains("opencode") || n.contains("sync") || n.contains("agent")
    });
    assert!(
        has_opencode_check,
        "checks: {:?}",
        result.checks.iter().map(|c| &c.name).collect::<Vec<_>>()
    );
}

#[then(
    "the native tier (Copilot, Cursor, Windsurf, Junie, Antigravity, Pi, Aider) is validated by the no-shadowing rule plus the AGENTS.md instruction-size budget"
)]
fn then_hb_native_tier(w: &mut SpecsTreeWorld) {
    let native: Vec<&HarnessEntry> = w.hb_harness.iter().filter(|h| h.tier == "native").collect();
    let native_names: Vec<&str> = native.iter().map(|h| h.name.as_str()).collect();
    assert_eq!(native.len(), 7, "native tier: {native_names:?}");
    for expected in [
        "copilot",
        "cursor",
        "windsurf",
        "junie",
        "antigravity",
        "pi",
        "aider",
    ] {
        assert!(
            native_names.contains(&expected),
            "missing native harness {expected:?} in {native_names:?}"
        );
    }

    // No-shadowing rule: every shadow-bearing native entry's surface is a known binding dir/file.
    for h in &native {
        if let Some(shadow) = &h.shadow {
            let base = shadow.split('/').next().unwrap_or(shadow);
            assert!(
                KNOWN_BINDING_DIRS.contains(&base) || KNOWN_BINDING_DIRS.contains(&shadow.as_str()),
                "shadow surface {shadow:?} for harness {:?} not in KNOWN_BINDING_DIRS",
                h.name
            );
        }
    }

    // AGENTS.md instruction-size budget: every native entry reads AGENTS.md.
    for h in &native {
        assert!(
            h.instruction.iter().any(|i| i == "AGENTS.md"),
            "native harness {:?} must read AGENTS.md; instruction: {:?}",
            h.name,
            h.instruction
        );
    }
}

#[then(
    "the harness set is data in repo-config.yml, identical across all three repos, not a hard-coded directory list"
)]
fn then_hb_data_driven(w: &mut SpecsTreeWorld) {
    // Cross-check: every KNOWN_BINDING_DIRS entry (the constant `harness bindings validate`
    // itself uses) corresponds to some repo-config.yml harness declaration — proving the
    // authoritative, repo-identical source of the harness set is the YAML data, not a
    // source-hard-coded list maintained independently of it.
    let declared_paths: Vec<&str> = w
        .hb_harness
        .iter()
        .flat_map(|h| {
            [
                h.agent_dir.as_deref(),
                h.rules_dir.as_deref(),
                h.shadow.as_deref(),
                h.config.as_deref(),
                h.forbid_dir.as_deref(),
            ]
            .into_iter()
            .flatten()
        })
        .collect();
    for known in KNOWN_BINDING_DIRS.iter().copied() {
        let matches = declared_paths
            .iter()
            .any(|p| *p == known || p.starts_with(known));
        assert!(
            matches,
            "KNOWN_BINDING_DIRS entry {known:?} has no corresponding repo-config.yml harness \
             declaration: {declared_paths:?}"
        );
    }
}

// ===========================================================================
// harness-registry-driven.feature (subprocess, synthetic repo-config.yml)
// ===========================================================================

#[given(
    "the repo-config.yml harness section lists an agent-bearing tier (Amazon Q) and a native instruction surface"
)]
fn given_hrd_registry(w: &mut SpecsTreeWorld) {
    let tmp = TempDir::new().expect("temp workspace");
    let root = tmp.path();
    run_git(root, &["init", "-q"]);

    // Custom (non-`.claude`/`.opencode`) tier directories — proves the naming/duplication/
    // instruction-size validators derive target sets from the registry, not hard-coded paths.
    let config = concat!(
        "harness:\n",
        "  - { name: claude-code-like, tier: source, agent-dir: .custom-src/agents,",
        " skills-dir: .custom-src/skills }\n",
        "  - { name: opencode-like, tier: generated, agent-dir: .custom-gen/opencode-like,",
        " mirrors: .custom-src/agents }\n",
        "  - name: amazonq\n",
        "    tier: generated\n",
        "    agent-dir: .custom-gen/amazonq\n",
        "    mirrors: .custom-src/agents\n",
        "  - name: custom-native\n",
        "    tier: native\n",
        "    instruction:\n",
        "      - .custom-native/SURFACE.md\n",
        "coverage:\n  projects: []\n",
        "specs:\n  ddd-areas: []\n  domain-areas: []\n",
    );
    std::fs::write(root.join("repo-config.yml"), config).expect("write repo-config.yml");

    // Source tier: two agents (different roles AND domains, so
    // `is_sanctioned_template_family` does NOT exempt the match) sharing a
    // 10+-line verbatim duplicate block.
    std::fs::create_dir_all(root.join(".custom-src/agents")).expect("mkdir");
    let mut dup_lines = String::new();
    for i in 0..15 {
        let _ = writeln!(dup_lines, "Duplicated line {i}");
    }
    let foo_body = format!("---\nname: foo-maker\n---\n{dup_lines}");
    let bar_body = format!("---\nname: widget-checker\n---\n{dup_lines}");
    std::fs::write(root.join(".custom-src/agents/foo-maker.md"), &foo_body).expect("write");
    std::fs::write(root.join(".custom-src/agents/widget-checker.md"), &bar_body).expect("write");

    // Generated tier 1 (opencode-like): fully mirrored, clean.
    std::fs::create_dir_all(root.join(".custom-gen/opencode-like")).expect("mkdir");
    std::fs::write(
        root.join(".custom-gen/opencode-like/foo-maker.md"),
        "---\n---\n",
    )
    .expect("write");
    std::fs::write(
        root.join(".custom-gen/opencode-like/widget-checker.md"),
        "---\n---\n",
    )
    .expect("write");

    // Generated tier 2 (amazonq): missing the widget-checker mirror -> mirror-drift.
    std::fs::create_dir_all(root.join(".custom-gen/amazonq")).expect("mkdir");
    std::fs::write(root.join(".custom-gen/amazonq/foo-maker.md"), "---\n---\n").expect("write");

    // Native tier: oversized custom instruction surface (registry default fail budget = 16,000 B).
    std::fs::create_dir_all(root.join(".custom-native")).expect("mkdir");
    std::fs::write(root.join(".custom-native/SURFACE.md"), "x".repeat(50_000)).expect("write");

    run_git(root, &["add", "-A"]);
    run_git(root, &["commit", "-q", "-m", "seed"]);

    w.hrd_work = Some(tmp);
}

#[when(
    "harness naming validate, harness instruction-size validate, and harness duplication validate run"
)]
fn when_hrd_run_all_three(w: &mut SpecsTreeWorld) {
    let root = w
        .hrd_work
        .as_ref()
        .expect("fixture built by Given step")
        .path()
        .to_path_buf();
    w.hrd_naming_output = Some(run_rhino(&root, &["harness", "naming", "validate"]));
    w.hrd_instr_output = Some(run_rhino(
        &root,
        &["harness", "instruction-size", "validate"],
    ));
    w.hrd_dup_output = Some(run_rhino(&root, &["harness", "duplication", "validate"]));
}

#[then("each derives its target set from the registry, not a hard-coded .claude/.opencode pair")]
fn then_hrd_registry_driven(w: &mut SpecsTreeWorld) {
    let naming = w.hrd_naming_output.as_ref().expect("naming ran");
    let naming_text = combined_output(naming);
    assert!(!naming.status.success(), "naming output: {naming_text}");
    assert!(
        naming_text.contains(".custom-gen") || naming_text.contains(".custom-src"),
        "got: {naming_text}"
    );

    let dup = w.hrd_dup_output.as_ref().expect("duplication ran");
    let dup_text = combined_output(dup);
    assert!(!dup.status.success(), "dup output: {dup_text}");
    assert!(
        dup_text.contains(".custom-src") || dup_text.contains("foo-maker"),
        "got: {dup_text}"
    );

    let instr = w.hrd_instr_output.as_ref().expect("instruction-size ran");
    let instr_text = combined_output(instr);
    assert!(!instr.status.success(), "instr output: {instr_text}");
    assert!(instr_text.contains(".custom-native"), "got: {instr_text}");
}

#[then("harness naming validate checks the Amazon Q agent dir and the N-way mirror")]
fn then_hrd_naming_checks_amazonq(w: &mut SpecsTreeWorld) {
    let naming = w.hrd_naming_output.as_ref().expect("naming ran");
    let text = combined_output(naming);
    assert!(text.contains("amazonq"), "got: {text}");
}

#[then("a config-only addition of a new agent-bearing tier is covered with no source edit")]
fn then_hrd_config_only(w: &mut SpecsTreeWorld) {
    // The Given step wrote only `repo-config.yml` plus fixture data files under the synthetic
    // temp root -- no `.rs` source under the crate was touched. All three registry-driven
    // validators still detected their respective custom-tier violations (asserted above),
    // proving the config-only addition is covered end to end.
    assert!(!w.hrd_naming_output.as_ref().expect("ran").status.success());
    assert!(!w.hrd_instr_output.as_ref().expect("ran").status.success());
    assert!(!w.hrd_dup_output.as_ref().expect("ran").status.success());
}

// ===========================================================================
// validate-adoption.feature / validate-tree.feature / validate-counts.feature /
// validate-links.feature — shared Given fixture builders
// ===========================================================================

#[given(
    regex = r#"^an app "([\w-]+)" that has at least one feature file under specs/apps/[\w-]+/behavior/ and a bounded-contexts\.yaml at specs/apps/[\w-]+/ddd/bounded-contexts\.yaml$"#
)]
fn given_adopt_complete(w: &mut SpecsTreeWorld, app: String) {
    w.write(
        &format!("specs/apps/{app}/behavior/a.feature"),
        "Feature: fixture\n",
    );
    w.write(
        &format!("specs/apps/{app}/ddd/bounded-contexts.yaml"),
        "version: 2\n",
    );
}

#[given(
    regex = r#"^an app "([\w-]+)" that has no feature files under specs/apps/[\w-]+/behavior/$"#
)]
fn given_adopt_no_features(w: &mut SpecsTreeWorld, app: String) {
    w.write(&format!("specs/apps/{app}/behavior/.gitkeep"), "");
    w.write(
        &format!("specs/apps/{app}/ddd/bounded-contexts.yaml"),
        "version: 2\n",
    );
}

#[given(
    regex = r#"^an app "([\w-]+)" that has feature files but no bounded-contexts\.yaml at specs/apps/[\w-]+/ddd/bounded-contexts\.yaml$"#
)]
fn given_adopt_no_bc_yaml(w: &mut SpecsTreeWorld, app: String) {
    w.write(
        &format!("specs/apps/{app}/behavior/a.feature"),
        "Feature: fixture\n",
    );
}

#[given(regex = r#"^an app "([\w-]+)" with no spec tree at all$"#)]
fn given_adopt_nothing(_w: &mut SpecsTreeWorld, _app: String) {
    // No-op: deliberately create nothing under specs/apps/<app>.
}

/// Writes `content` at `{prefix}/{sub}/{filename}` for every required spec
/// folder except `skip` (when non-empty). Shared fixture-construction helper
/// for the tree/counts "missing folder/subfolder" scenarios.
fn write_required_folders(
    w: &SpecsTreeWorld,
    prefix: &str,
    filename: &str,
    content: &str,
    skip: &str,
) {
    for sub in rhino_cli::application::specs::required_spec_folders() {
        if *sub == skip {
            continue;
        }
        w.write(&format!("{prefix}/{sub}/{filename}"), content);
    }
}

/// Like [`write_required_folders`], but instead of skipping `override_sub`
/// entirely, writes `override_content` at `override_filename` there — used
/// for the "folder/subfolder exists but is sparse" scenarios (missing
/// README, empty subfolder).
fn write_required_folders_with_override(
    w: &SpecsTreeWorld,
    prefix: &str,
    filename: &str,
    content: &str,
    override_sub: &str,
    override_filename: &str,
    override_content: &str,
) {
    for sub in rhino_cli::application::specs::required_spec_folders() {
        if *sub == override_sub {
            w.write(
                &format!("{prefix}/{sub}/{override_filename}"),
                override_content,
            );
        } else {
            w.write(&format!("{prefix}/{sub}/{filename}"), content);
        }
    }
}

#[given(
    regex = r#"^a spec tree for "([\w-]+)" with all five required folders and their README\.md files$"#
)]
fn given_tree_complete(w: &mut SpecsTreeWorld, app: String) {
    write_required_folders(
        w,
        &format!("specs/apps/{app}"),
        "README.md",
        "# readme\n",
        "",
    );
}

#[given(regex = r#"^a spec tree for "([\w-]+)" missing the "([\w-]+)" folder$"#)]
fn given_tree_missing_folder(w: &mut SpecsTreeWorld, app: String, missing: String) {
    write_required_folders(
        w,
        &format!("specs/apps/{app}"),
        "README.md",
        "# readme\n",
        &missing,
    );
}

#[given(
    regex = r#"^a spec tree for "([\w-]+)" where the "([\w-]+)" folder exists but has no README\.md$"#
)]
fn given_tree_missing_readme(w: &mut SpecsTreeWorld, app: String, bare: String) {
    write_required_folders_with_override(
        w,
        &format!("specs/apps/{app}"),
        "README.md",
        "# readme\n",
        &bare,
        ".gitkeep",
        "",
    );
}

#[given(regex = r#"^no spec tree exists for "([\w-]+)"$"#)]
fn given_tree_nothing(_w: &mut SpecsTreeWorld, _app: String) {
    // No-op: deliberately create nothing under specs/apps/<app>.
}

#[given(
    regex = r#"^a spec folder at "([^"]+)" with at least one non-README \.md file in each required subfolder$"#
)]
fn given_counts_complete(w: &mut SpecsTreeWorld, folder: String) {
    write_required_folders(w, &folder, "spec.md", "# spec\n", "");
}

#[given(
    regex = r#"^a spec folder at "([^"]+)" where the "([\w-]+)" subfolder contains only README\.md$"#
)]
fn given_counts_empty_subfolder(w: &mut SpecsTreeWorld, folder: String, empty_sub: String) {
    write_required_folders_with_override(
        w,
        &folder,
        "spec.md",
        "# spec\n",
        &empty_sub,
        "README.md",
        "# readme\n",
    );
}

#[given(regex = r#"^a spec folder at "([^"]+)" where the "([\w-]+)" subfolder does not exist$"#)]
fn given_counts_missing_subfolder(w: &mut SpecsTreeWorld, folder: String, missing_sub: String) {
    write_required_folders(w, &folder, "spec.md", "# spec\n", &missing_sub);
}

#[given(regex = r#"^no directory exists at "([^"]+)"$"#)]
fn given_no_directory_exists(_w: &mut SpecsTreeWorld, _folder: String) {
    // No-op: deliberately create nothing at the named path.
}

#[given(
    regex = r#"^a spec folder at "([^"]+)" where all internal markdown links resolve to existing files$"#
)]
fn given_links_all_valid(w: &mut SpecsTreeWorld, folder: String) {
    w.write(&format!("{folder}/a.md"), "# A\nSee [b](./b.md).\n");
    w.write(&format!("{folder}/b.md"), "# B\n");
}

#[given(
    regex = r#"^a spec folder at "([^"]+)" containing a markdown file with a broken internal link$"#
)]
fn given_links_broken(w: &mut SpecsTreeWorld, folder: String) {
    w.write(
        &format!("{folder}/a.md"),
        "# A\nSee [missing](./does-not-exist.md).\n",
    );
}

#[given(
    regex = r#"^a spec folder at "([^"]+)" containing only markdown files with external HTTPS links$"#
)]
fn given_links_external_only(w: &mut SpecsTreeWorld, folder: String) {
    w.write(
        &format!("{folder}/a.md"),
        "# A\nSee [ext](https://example.com/page).\n",
    );
}

// ===========================================================================
// validate-adoption.feature / validate-tree.feature / validate-counts.feature /
// validate-links.feature — shared When + Then steps
// ===========================================================================

#[when(regex = r#"^the developer runs "rhino-cli specs (validate-[a-z]+) ([^"]+)"$"#)]
fn when_specs_validate_x(w: &mut SpecsTreeWorld, verb: String, arg: String) {
    match verb.as_str() {
        "validate-adoption" => {
            let findings = validate_spec_adoption(w.work.path(), &arg);
            let (out, ok) = render_spec_findings(&findings);
            w.last_output = out;
            w.last_exit_ok = ok;
        }
        "validate-tree" => {
            let findings = validate_spec_tree_fn(w.work.path(), &arg);
            let (out, ok) = render_spec_findings(&findings);
            w.last_output = out;
            w.last_exit_ok = ok;
        }
        "validate-counts" => {
            let args = ValidateCountsArgs {
                folder: Some(arg),
                apps: Vec::new(),
            };
            let mut buf: Vec<u8> = Vec::new();
            let result = specs_validate_counts::run_at_root(w.work.path(), &args, &mut buf);
            w.last_output = String::from_utf8_lossy(&buf).into_owned();
            w.last_exit_ok = result.is_ok();
        }
        "validate-links" => {
            let folder_path = w.work.path().join(&arg);
            let (out, ok) = run_validate_links_at(&folder_path);
            w.last_output = out;
            w.last_exit_ok = ok;
        }
        other => unreachable!("unhandled `specs {other}` verb in gherkin/specs/ step text"),
    }
}

#[then("the command exits successfully")]
fn then_specs_exits_successfully(w: &mut SpecsTreeWorld) {
    assert!(w.last_exit_ok, "output: {}", w.last_output);
}

#[then("the command exits with a failure code")]
fn then_specs_exits_failure(w: &mut SpecsTreeWorld) {
    assert!(!w.last_exit_ok, "output: {}", w.last_output);
}

#[then(regex = r#"^the output contains "([^"]+)"$"#)]
fn then_specs_output_contains(w: &mut SpecsTreeWorld, needle: String) {
    assert!(
        w.last_output.contains(&needle),
        "expected {needle:?} in output: {}",
        w.last_output
    );
}

// ===========================================================================
// specs-audit.feature
// ===========================================================================

#[given("a repository with no spec-tree violations")]
fn given_specs_audit_clean(_w: &mut SpecsTreeWorld) {
    // No-op: `SpecsTreeWorld::new()`'s fixture workspace is a freshly
    // `git init`ed temp dir with no files at all, so `structure-validate`,
    // `validate-links`, and `gherkin-cardinality` (the three `specs audit`
    // members) each trivially report zero findings.
}

#[when("the developer runs rhino-cli specs audit")]
fn when_specs_audit_runs(w: &mut SpecsTreeWorld) {
    w.exec(&["specs", "audit"]);
    let out = w.output.as_ref().expect("ran");
    w.last_exit_ok = out.status.success();
    w.last_output = combined_output(out);
}

// ===========================================================================
// gherkin-cardinality.feature
// ===========================================================================

#[given(r#"a feature file containing a scenario with two primary "When" keywords"#)]
fn given_gc_double_when(w: &mut SpecsTreeWorld) {
    w.write(
        "offender.feature",
        "Feature: Sample\n\n  Scenario: Double when\n    Given a precondition\n    When the first action runs\n    When the second action runs\n    Then the outcome is checked\n",
    );
}

#[when("the developer runs specs gherkin-cardinality validate on the file")]
fn when_gc_validate_runs(w: &mut SpecsTreeWorld) {
    w.exec(&[
        "specs",
        "gherkin-cardinality",
        "validate",
        "offender.feature",
    ]);
    let out = w.output.as_ref().expect("ran");
    w.last_exit_ok = out.status.success();
    w.last_output = combined_output(out);
}

#[then("the output names the offending file and scenario")]
fn then_gc_names_offender(w: &mut SpecsTreeWorld) {
    assert!(
        w.last_output.contains("offender.feature"),
        "got: {}",
        w.last_output
    );
    assert!(
        w.last_output.contains("Double when"),
        "got: {}",
        w.last_output
    );
}

// ===========================================================================
// e2e-coverage.feature (subprocess)
// ===========================================================================

#[given(
    regex = r#"^a playwright-bdd project whose generated output marks scenarios "([^"]+)" and "([^"]+)" as test\.fixme$"#
)]
fn given_ec_project_marks_pair_fixme(w: &mut SpecsTreeWorld, a: String, b: String) {
    w.ec_ensure_declared(&[&a, &b]);
    w.ec_write_fixme(&[&a, &b]);
}

#[given(
    regex = r#"^generated output that marks scenarios "([^"]+)" and "([^"]+)" as test\.fixme$"#
)]
fn given_ec_generated_marks_pair_fixme(w: &mut SpecsTreeWorld, a: String, b: String) {
    w.ec_ensure_declared(&[&a, &b]);
    w.ec_write_fixme(&[&a, &b]);
}

#[given(regex = r#"^generated output that marks only scenario "([^"]+)" as test\.fixme$"#)]
fn given_ec_generated_marks_one_fixme(w: &mut SpecsTreeWorld, a: String) {
    w.ec_ensure_declared(&[&a]);
    w.ec_write_fixme(&[&a]);
}

#[given(
    regex = r#"^a baseline manifest that lists exactly scenarios "([^"]+)" and "([^"]+)" as allowed unbound$"#
)]
fn given_ec_baseline_exactly_pair(w: &mut SpecsTreeWorld, a: String, b: String) {
    w.ec_bootstrap_baseline(&[&a, &b]);
}

#[given(
    regex = r#"^a baseline manifest that lists exactly scenario "([^"]+)" as allowed unbound$"#
)]
fn given_ec_baseline_exactly_one(w: &mut SpecsTreeWorld, a: String) {
    w.ec_bootstrap_baseline(&[&a]);
}

#[given(
    regex = r#"^a baseline manifest that lists scenarios "([^"]+)" and "([^"]+)" as allowed unbound$"#
)]
fn given_ec_baseline_pair(w: &mut SpecsTreeWorld, a: String, b: String) {
    w.ec_bootstrap_baseline(&[&a, &b]);
}

#[given("a baseline manifest that lists no allowed unbound scenarios")]
fn given_ec_baseline_empty(w: &mut SpecsTreeWorld) {
    w.write(
        EC_BASELINE_PATH,
        "{\"project\": \"test-project\", \"allowedUnbound\": []}\n",
    );
}

#[given("a scenario tagged @unit only that appears as test.fixme in the generated output")]
fn given_ec_unit_only_fixme(w: &mut SpecsTreeWorld) {
    let title = "Unit only scenario";
    w.ec_unit_only_titles.push(title.to_string());
    w.ec_write_feature_file();
    w.ec_write_fixme(&[title]);
}

/// Declared title of the `Scenario Outline` [`given_ec_outline_with_unbound_example`]
/// writes — shared with [`then_ec_reports_one_new_gap_for_outline`] so both
/// sides of the fixture agree on the exact text without duplicating it.
const EC_OUTLINE_TITLE: &str = "Renders the field correctly";

#[given("an @e2e Scenario Outline whose generated Examples-row tests include one test.fixme")]
fn given_ec_outline_with_unbound_example(w: &mut SpecsTreeWorld) {
    // playwright-bdd wraps a Scenario Outline's Examples-row-derived tests in
    // one `test.describe(...)` block titled with the outline's own raw
    // Gherkin title; each row inside is titled per playwright-bdd's own
    // convention (`Example #<N>` by default), never the outline's own title
    // — see `parser::scan_unbound_describe_titles`'s doc comment. Only ONE
    // of the two Examples rows is `test.fixme`.
    w.write(
        &format!("{EC_FEATURES_DIR}/{EC_FEATURE_FILE}"),
        &format!(
            "Feature: fixture\n\n@e2e\nScenario Outline: {EC_OUTLINE_TITLE}\n  Given a field\n\n  Examples:\n    | field |\n    | name  |\n    | email |\n"
        ),
    );
    w.write(
        &format!("{EC_FEATURES_GEN_DIR}/{EC_SPEC_JS_FILE}"),
        &format!(
            "test.describe('{EC_OUTLINE_TITLE}', () => {{\n  test.fixme('Example #1', async ({{ page }}) => {{\n  }});\n  test('Example #2', async ({{ page }}) => {{\n  }});\n}});\n"
        ),
    );
}

/// Declared title of the zero-row `Scenario Outline`
/// [`given_ec_zero_row_outline`] writes — shared with
/// [`then_ec_names_zero_row_outline`] so both sides of the fixture agree on
/// the exact text without duplicating it.
const EC_ZERO_ROW_OUTLINE_TITLE: &str = "Renders the field correctly with no examples";

#[given("an @e2e Scenario Outline whose Examples table has zero data rows")]
fn given_ec_zero_row_outline(w: &mut SpecsTreeWorld) {
    // playwright-bdd's renderScenarioOutline emits NOTHING at all for a
    // zero-row outline (`scenario.examples.forEach(...)` iterates zero rows,
    // so it returns before emitting a single test/test.fixme/describe — see
    // `parser::scan_all_rendered_titles`'s doc comment) — an empty generated
    // file faithfully reproduces that real-world output.
    w.write(
        &format!("{EC_FEATURES_DIR}/{EC_FEATURE_FILE}"),
        &format!(
            "Feature: fixture\n\n@e2e\nScenario Outline: {EC_ZERO_ROW_OUTLINE_TITLE}\n  Given a field <field>\n\n  Examples:\n    | field |\n"
        ),
    );
    w.write(&format!("{EC_FEATURES_GEN_DIR}/{EC_SPEC_JS_FILE}"), "");
}

#[then("it reports exactly one new unbound scenario for the zero-row outline")]
fn then_ec_reports_one_new_gap_for_zero_row_outline(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(!out.status.success(), "expected failure, got: {text}");
    assert!(
        text.contains("1 new unbound scenario(s) found"),
        "got: {text}"
    );
    assert!(text.contains(EC_ZERO_ROW_OUTLINE_TITLE), "got: {text}");
}

/// Declared title of the apostrophe-bearing scenario
/// [`given_ec_apostrophe_titled_fixme`] writes — shared with
/// [`then_ec_reports_one_new_gap_for_apostrophe_title`] so both sides of the
/// fixture agree on the exact text without duplicating it.
const EC_APOSTROPHE_TITLE: &str = "A user's profile renders correctly";

#[given(
    "an @e2e scenario titled with an apostrophe that appears as test.fixme using playwright-bdd's escaped single-quote convention"
)]
fn given_ec_apostrophe_titled_fixme(w: &mut SpecsTreeWorld) {
    w.write(
        &format!("{EC_FEATURES_DIR}/{EC_FEATURE_FILE}"),
        &format!("Feature: fixture\n\n@e2e\nScenario: {EC_APOSTROPHE_TITLE}\n  Given a step\n"),
    );
    // playwright-bdd's default single-quote `jsStringWrap` escapes a literal
    // `'` in the title to `\'` — the exact convention
    // `parser::fixme_title_re`'s regression tests reproduce.
    w.write(
        &format!("{EC_FEATURES_GEN_DIR}/{EC_SPEC_JS_FILE}"),
        "test.fixme('A user\\'s profile renders correctly', async ({ page }) => {\n});\n",
    );
}

#[given("a project with no baseline manifest yet")]
fn given_ec_no_baseline_yet(_w: &mut SpecsTreeWorld) {
    // No-op: deliberately never write a baseline manifest. `types::load_baseline`
    // treats a missing path as an empty manifest, matching this scenario's setup.
}

#[given(regex = r#"^a new unbound scenario "([^"]+)" in "([^"]+)"$"#)]
fn given_ec_new_gap_scenario(w: &mut SpecsTreeWorld, title: String, file_name: String) {
    w.write(
        &format!("{EC_FEATURES_DIR}/{file_name}"),
        &format!("Feature: fixture\n\n@e2e\nScenario: {title}\n  Given a step\n"),
    );
    // Mirrors playwright-bdd's real convention: the generated file keeps the
    // declared `.feature` file's name (including its `.feature` extension)
    // and appends `.spec.js` — matching `EC_SPEC_JS_FILE`'s convention and
    // what `is_fixme`'s file-pairing logic in `specs_e2e_coverage.rs` relies
    // on. A hardcoded `gap.spec.js` (unrelated to `file_name`) never pairs
    // with the declared scenario's `.feature` path.
    w.write(
        &format!("{EC_FEATURES_GEN_DIR}/{file_name}.spec.js"),
        &format!("test.fixme(\"{title}\", async ({{ page }}) => {{}});\n"),
    );
}

#[given("a project whose .features-gen directory does not exist")]
fn given_ec_no_features_gen_dir(_w: &mut SpecsTreeWorld) {
    // No-op: deliberately never create `.features-gen` (the "bddgen never ran" case).
}

#[when("rhino-cli specs e2e-coverage validate runs for that project")]
fn when_ec_validate_runs(w: &mut SpecsTreeWorld) {
    w.exec(&[
        "specs",
        "e2e-coverage",
        "validate",
        "--features",
        EC_FEATURES_GLOB,
        "--features-gen",
        EC_FEATURES_GEN_DIR,
        "--baseline",
        EC_BASELINE_PATH,
        "--project",
        "test-project",
    ]);
}

#[when("rhino-cli specs e2e-coverage validate runs and detects it as a new gap")]
fn when_ec_validate_detects_new_gap(w: &mut SpecsTreeWorld) {
    w.exec(&[
        "specs",
        "e2e-coverage",
        "validate",
        "--features",
        EC_FEATURES_GLOB,
        "--features-gen",
        EC_FEATURES_GEN_DIR,
        "--baseline",
        EC_BASELINE_PATH,
        "--project",
        "test-project",
    ]);
}

#[when("rhino-cli specs e2e-coverage validate runs with the --update-baseline flag")]
fn when_ec_validate_update_baseline_runs(w: &mut SpecsTreeWorld) {
    w.exec(&[
        "specs",
        "e2e-coverage",
        "validate",
        "--update-baseline",
        "--features",
        EC_FEATURES_GLOB,
        "--features-gen",
        EC_FEATURES_GEN_DIR,
        "--baseline",
        EC_BASELINE_PATH,
        "--project",
        "test-project",
    ]);
}

#[then("it passes with exit code 0")]
fn then_ec_passes(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    assert!(out.status.success(), "got: {}", combined_output(out));
}

#[then("it fails with a non-zero exit code")]
fn then_ec_fails(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    assert!(!out.status.success(), "got: {}", combined_output(out));
}

#[then("it reports 2 declared-but-unbound scenarios all covered by the baseline")]
fn then_ec_two_covered_by_baseline(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(out.status.success(), "got: {text}");
    assert_eq!(
        w.ec_fixme_titles.len(),
        2,
        "fixture must currently mark exactly 2 scenarios as test.fixme"
    );
    assert!(
        text.contains("0 new unbound scenario(s) beyond baseline"),
        "got: {text}"
    );
}

#[then(
    regex = r#"^it names scenario "([^"]+)" and its containing \.feature file as a new unbound gap$"#
)]
fn then_ec_names_new_gap(w: &mut SpecsTreeWorld, title: String) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(text.contains(&title), "got: {text}");
    assert!(text.contains(EC_FEATURE_FILE), "got: {text}");
}

#[then(regex = r#"^it does not report scenario "([^"]+)" as a new gap$"#)]
fn then_ec_not_new_gap(w: &mut SpecsTreeWorld, title: String) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    let marker = format!("\"{title}\"");
    assert!(!text.contains(&marker), "got: {text}");
}

#[then(regex = r#"^it reports scenario "([^"]+)" as newly bound relative to the baseline$"#)]
fn then_ec_newly_bound(w: &mut SpecsTreeWorld, title: String) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(out.status.success(), "got: {text}");
    assert!(text.contains("stale baseline entries"), "got: {text}");
    let marker = format!("\"{title}\"");
    assert!(text.contains(&marker), "got: {text}");
}

#[then(regex = r#"^it reports scenario "([^"]+)" as a stale baseline entry that can be pruned$"#)]
fn then_ec_stale_entry_prunable(w: &mut SpecsTreeWorld, title: String) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(out.status.success(), "got: {text}");
    assert!(text.contains("stale baseline entries"), "got: {text}");
    let marker = format!("\"{title}\"");
    assert!(text.contains(&marker), "got: {text}");
}

#[then("it does not report the @unit-only scenario as an unbound gap")]
fn then_ec_unit_only_ignored(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(out.status.success(), "got: {text}");
    for title in &w.ec_unit_only_titles {
        assert!(!text.contains(title.as_str()), "got: {text}");
    }
}

#[then("it reports exactly one new unbound scenario for the outline")]
fn then_ec_reports_one_new_gap_for_outline(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(!out.status.success(), "expected failure, got: {text}");
    assert!(
        text.contains("1 new unbound scenario(s) found"),
        "got: {text}"
    );
    assert!(text.contains(EC_OUTLINE_TITLE), "got: {text}");
}

#[then("it reports exactly one new unbound scenario for the apostrophe-bearing title")]
fn then_ec_reports_one_new_gap_for_apostrophe_title(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(!out.status.success(), "expected failure, got: {text}");
    assert!(
        text.contains("1 new unbound scenario(s) found"),
        "got: {text}"
    );
    assert!(text.contains(EC_APOSTROPHE_TITLE), "got: {text}");
}

#[then(regex = r#"^the failure output contains the scenario title "([^"]+)"$"#)]
fn then_ec_failure_contains_title(w: &mut SpecsTreeWorld, title: String) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(!out.status.success(), "expected failure, got: {text}");
    assert!(text.contains(&title), "got: {text}");
}

#[then(regex = r#"^the failure output contains the feature file path ending in "([^"]+)"$"#)]
fn then_ec_failure_contains_path_suffix(w: &mut SpecsTreeWorld, suffix: String) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(text.contains(&suffix), "got: {text}");
}

#[then("the failure output states the delta is an increase of 1 over baseline")]
fn then_ec_failure_states_increase_of_one(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(text.contains("increase of 1"), "got: {text}");
}

#[then(
    regex = r#"^it writes a baseline manifest listing scenarios "([^"]+)" and "([^"]+)" as allowed unbound$"#
)]
fn then_ec_writes_baseline_manifest(w: &mut SpecsTreeWorld, a: String, b: String) {
    let out = w.output.as_ref().expect("ran");
    assert!(out.status.success(), "got: {}", combined_output(out));
    let baseline_path = w.work.path().join(EC_BASELINE_PATH);
    assert!(baseline_path.exists(), "baseline manifest was not written");
    let content = std::fs::read_to_string(&baseline_path).expect("read baseline manifest");
    assert!(content.contains(&format!("\"{a}\"")), "got: {content}");
    assert!(content.contains(&format!("\"{b}\"")), "got: {content}");
}

#[then("a subsequent validate run for that project passes with exit code 0")]
fn then_ec_subsequent_validate_passes(w: &mut SpecsTreeWorld) {
    let out = run_rhino(
        w.work.path(),
        &[
            "specs",
            "e2e-coverage",
            "validate",
            "--features",
            EC_FEATURES_GLOB,
            "--features-gen",
            EC_FEATURES_GEN_DIR,
            "--baseline",
            EC_BASELINE_PATH,
            "--project",
            "test-project",
        ],
    );
    assert!(out.status.success(), "got: {}", combined_output(&out));
}

#[then("it reports that bddgen output was not found and must be generated first")]
fn then_ec_reports_missing_features_gen(w: &mut SpecsTreeWorld) {
    let out = w.output.as_ref().expect("ran");
    let text = combined_output(out);
    assert!(text.contains(".features-gen"), "got: {text}");
    assert!(text.contains("bddgen"), "got: {text}");
}

// ===========================================================================
// worktree-agnostic.feature
// ===========================================================================

#[given("a synthetic linked worktree in the rhino-cli test suite")]
fn given_wt_linked_worktree(w: &mut SpecsTreeWorld) {
    let main_repo = TempDir::new().expect("tempdir main");
    let main = main_repo.path();
    run_git(main, &["init", "-q"]);
    std::fs::write(main.join("README.md"), "test").expect("write readme");
    run_git(main, &["add", "."]);
    run_git(main, &["commit", "-q", "-m", "init"]);

    let wt_dir = TempDir::new().expect("tempdir wt");
    let wt_path = wt_dir.path().to_path_buf();
    let status = Command::new("git")
        .args(["worktree", "add", &wt_path.to_string_lossy(), "HEAD"])
        .current_dir(main)
        .status()
        .expect("git worktree add");
    assert!(status.success(), "git worktree add must succeed");

    w.wt_path = Some(wt_path);
    w.wt_main = Some(main_repo);
    w.wt_worktree_dir = Some(wt_dir);
}

#[when("a guardrail command runs inside it")]
fn when_wt_guardrail_runs(w: &mut SpecsTreeWorld) {
    let wt_path = w.wt_path.clone().expect("worktree path set by Given step");
    w.wt_resolved = Some(find_root_from(Some(&wt_path)));
}

#[then("it resolves to the worktree's own toplevel and exits successfully")]
fn then_wt_resolves_to_worktree(w: &mut SpecsTreeWorld) {
    let resolved = w
        .wt_resolved
        .take()
        .expect("When step ran")
        .expect("find_root_from must succeed inside a linked worktree");
    let resolved_canonical = std::fs::canonicalize(&resolved).expect("canonicalize resolved");
    let wt_canonical =
        std::fs::canonicalize(w.wt_path.as_ref().expect("wt path set")).expect("canonicalize wt");
    assert_eq!(
        resolved_canonical, wt_canonical,
        "find_root_from must return the linked worktree path when invoked from it"
    );
}

#[tokio::main]
async fn main() {
    SpecsTreeWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_dir())
        .await;
}

fn feature_dir() -> PathBuf {
    let manifest = PathBuf::from(env!("CARGO_MANIFEST_DIR"));
    manifest
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/specs")
        .canonicalize()
        .expect("feature dir resolvable")
}
