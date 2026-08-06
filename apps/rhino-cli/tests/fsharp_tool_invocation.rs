//! Regression coverage for manifest-backed Fantomas lint targets.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::panic, clippy::unwrap_used)]

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::Command;

use cucumber::{World as _, given, then, when};
use tempfile::Builder;
use walkdir::WalkDir;

#[derive(Debug, cucumber::World)]
#[world(init = Self::new)]
struct FsharpToolInvocationWorld {
    configured: usize,
    evaluated: usize,
    missing_local_restores: Vec<PathBuf>,
    missing_manifest_commands: Vec<PathBuf>,
    bare_global_invocations: Vec<PathBuf>,
    malformed_source_rejected: Option<bool>,
}

impl FsharpToolInvocationWorld {
    fn new() -> Self {
        Self {
            configured: 0,
            evaluated: 0,
            missing_local_restores: Vec::new(),
            missing_manifest_commands: Vec::new(),
            bare_global_invocations: Vec::new(),
            malformed_source_rejected: None,
        }
    }
}

#[given("the local F# lint targets are discovered")]
fn given_fsharp_lint_targets(w: &mut FsharpToolInvocationWorld) {
    assert_audit_detects_noncompliant_candidates();
    assert_empty_workspace_does_not_require_manifest_tool();

    let workspace_root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    let audit = audit_fantomas_lint_targets(&workspace_root);

    w.configured = audit.candidates.len();
    w.evaluated = audit.evaluated_candidates;
    w.missing_local_restores = audit.missing_local_restores;
    w.missing_manifest_commands = audit.missing_manifest_commands;
    w.bare_global_invocations = audit.bare_global_invocations;
}

#[when("every locally discovered F# lint target is evaluated")]
fn when_fsharp_lint_targets_are_inspected(w: &mut FsharpToolInvocationWorld) {
    let workspace_root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    w.malformed_source_rejected =
        check_malformed_source_if_targets_exist(&workspace_root, w.configured);
}

#[then("every discovered F# lint target is evaluated")]
fn then_every_fsharp_lint_target_is_evaluated(w: &mut FsharpToolInvocationWorld) {
    assert_eq!(
        w.evaluated, w.configured,
        "every discovered F# lint target must be evaluated"
    );
}

#[then("each target restores the local .NET tool manifest before running Fantomas")]
fn then_targets_restore_manifest(w: &mut FsharpToolInvocationWorld) {
    assert!(
        w.missing_local_restores.is_empty(),
        "Fantomas targets missing `dotnet tool restore`: {:?}",
        w.missing_local_restores
    );
    assert!(
        w.missing_manifest_commands.is_empty(),
        "Fantomas targets missing `dotnet tool run fantomas --check`: {:?}",
        w.missing_manifest_commands
    );
}

#[then("no target invokes the global Fantomas app host directly")]
fn then_targets_do_not_use_global_fantomas(w: &mut FsharpToolInvocationWorld) {
    assert!(
        w.bare_global_invocations.is_empty(),
        "Fantomas targets invoking the global app host: {:?}",
        w.bare_global_invocations
    );
}

#[then("an unformatted source file is checked only when F# lint targets exist")]
fn then_configuration_keeps_check_mode(w: &mut FsharpToolInvocationWorld) {
    if w.configured == 0 {
        assert!(
            w.malformed_source_rejected.is_none(),
            "a workspace without F# lint targets must not invoke the manifest Fantomas tool"
        );
        return;
    }

    assert_eq!(
        w.malformed_source_rejected,
        Some(true),
        "the manifest-backed Fantomas check must reject malformed source"
    );
}

fn check_malformed_source_if_targets_exist(
    workspace_root: &Path,
    configured_targets: usize,
) -> Option<bool> {
    if configured_targets == 0 {
        return None;
    }

    let mut malformed_source = Builder::new()
        .prefix("fantomas-regression-")
        .suffix(".fs")
        .tempfile()
        .expect("create malformed F# fixture");
    writeln!(malformed_source, "module Malformed\nlet value= 1")
        .expect("write malformed F# fixture");

    let status = Command::new("dotnet")
        .current_dir(workspace_root)
        .args([
            "tool",
            "run",
            "fantomas",
            "--check",
            malformed_source
                .path()
                .to_str()
                .expect("UTF-8 fixture path"),
        ])
        .status()
        .expect("run manifest Fantomas check");
    Some(!status.success())
}

#[derive(Debug, Eq, PartialEq)]
struct FantomasLintTargetAudit {
    candidates: Vec<PathBuf>,
    evaluated_candidates: usize,
    missing_local_restores: Vec<PathBuf>,
    missing_manifest_commands: Vec<PathBuf>,
    bare_global_invocations: Vec<PathBuf>,
}

fn audit_fantomas_lint_targets(workspace_root: &Path) -> FantomasLintTargetAudit {
    let mut candidates = WalkDir::new(workspace_root)
        .into_iter()
        .filter_entry(|entry| {
            !matches!(
                entry.file_name().to_str(),
                Some(".git" | "node_modules" | "target" | "dist")
            )
        })
        .filter_map(Result::ok)
        .map(walkdir::DirEntry::into_path)
        .filter(|path| path.file_name().is_some_and(|name| name == "project.json"))
        .filter(|path| {
            let project = fs::read_to_string(path)
                .unwrap_or_else(|error| panic!("read {}: {error}", path.display()));
            project.contains("fantomas --check")
        })
        .collect::<Vec<_>>();
    candidates.sort();

    let mut missing_local_restores = Vec::new();
    let mut missing_manifest_commands = Vec::new();
    let mut bare_global_invocations = Vec::new();
    let mut evaluated_candidates = 0;
    for project_path in &candidates {
        evaluated_candidates += 1;
        let project = fs::read_to_string(project_path)
            .unwrap_or_else(|error| panic!("read {}: {error}", project_path.display()));
        if !project.contains("dotnet tool restore") {
            missing_local_restores.push(project_path.clone());
        }
        if !project.contains("dotnet tool run fantomas --check") {
            missing_manifest_commands.push(project_path.clone());
        }
        if project
            .lines()
            .any(|line| line.contains("fantomas --check") && !line.contains("dotnet tool run"))
        {
            bare_global_invocations.push(project_path.clone());
        }
    }

    FantomasLintTargetAudit {
        candidates,
        evaluated_candidates,
        missing_local_restores,
        missing_manifest_commands,
        bare_global_invocations,
    }
}

#[tokio::main]
async fn main() {
    FsharpToolInvocationWorld::cucumber()
        .fail_on_skipped()
        .run_and_exit(feature_path())
        .await;
}

fn feature_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .join("../../specs/apps/rhino/behavior/rhino-cli/gherkin/system/fsharp-tool-invocation.feature")
        .canonicalize()
        .expect("feature file resolvable")
}

fn assert_audit_detects_noncompliant_candidates() {
    let fixture_root = tempfile::tempdir().expect("create target fixture workspace");
    write_project_fixture(
        fixture_root.path(),
        "apps/manifest-backed/project.json",
        r#"{"commands":["dotnet tool restore","dotnet tool run fantomas --check src"]}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "apps/missing-restore/project.json",
        r#"{"commands":["dotnet tool run fantomas --check src"]}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "libs/bare-global/project.json",
        r#"{"commands":["fantomas --check src"]}"#,
    );

    let audit = audit_fantomas_lint_targets(fixture_root.path());

    assert_eq!(audit.candidates.len(), 3);
    assert_eq!(audit.evaluated_candidates, 3);
    assert_eq!(
        audit.missing_local_restores,
        vec![
            fixture_root
                .path()
                .join("apps/missing-restore/project.json"),
            fixture_root.path().join("libs/bare-global/project.json"),
        ]
    );
    assert_eq!(
        audit.missing_manifest_commands,
        vec![fixture_root.path().join("libs/bare-global/project.json")]
    );
    assert_eq!(
        audit.bare_global_invocations,
        vec![fixture_root.path().join("libs/bare-global/project.json")]
    );
}

fn assert_empty_workspace_does_not_require_manifest_tool() {
    let fixture_root = tempfile::tempdir().expect("create empty fixture workspace");
    let audit = audit_fantomas_lint_targets(fixture_root.path());

    assert!(audit.candidates.is_empty());
    assert_eq!(audit.evaluated_candidates, 0);
    assert_eq!(
        check_malformed_source_if_targets_exist(fixture_root.path(), audit.candidates.len()),
        None,
        "an empty topology must not require a local tool manifest"
    );
}

fn write_project_fixture(root: &Path, relative_path: &str, contents: &str) {
    let path = root.join(relative_path);
    fs::create_dir_all(path.parent().expect("fixture project directory"))
        .expect("create fixture project directory");
    fs::write(path, contents).expect("write fixture project configuration");
}
