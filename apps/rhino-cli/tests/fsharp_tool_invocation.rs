//! Regression coverage for manifest-backed Fantomas lint targets.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::panic, clippy::unwrap_used)]

use std::fs;
use std::io::Write;
use std::path::{Path, PathBuf};
use std::process::Command;

use cucumber::{World as _, given, then, when};
use serde_json::Value;
use tempfile::Builder;
use walkdir::WalkDir;

#[derive(Debug, cucumber::World)]
#[world(init = Self::new)]
struct FsharpToolInvocationWorld {
    configured: usize,
    evaluated: usize,
    candidate_working_directories: Vec<PathBuf>,
    missing_local_restores: Vec<PathBuf>,
    missing_manifest_commands: Vec<PathBuf>,
    bare_global_invocations: Vec<PathBuf>,
    malformed_source_check: Option<Vec<MalformedSourceCheck>>,
}

impl FsharpToolInvocationWorld {
    fn new() -> Self {
        Self {
            configured: 0,
            evaluated: 0,
            candidate_working_directories: Vec::new(),
            missing_local_restores: Vec::new(),
            missing_manifest_commands: Vec::new(),
            bare_global_invocations: Vec::new(),
            malformed_source_check: None,
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
    w.candidate_working_directories = audit.candidate_working_directories;
    w.missing_local_restores = audit.missing_local_restores;
    w.missing_manifest_commands = audit.missing_manifest_commands;
    w.bare_global_invocations = audit.bare_global_invocations;
}

#[when("every locally discovered F# lint target is evaluated")]
fn when_fsharp_lint_targets_are_inspected(w: &mut FsharpToolInvocationWorld) {
    w.malformed_source_check =
        check_malformed_source_if_targets_exist(&w.candidate_working_directories);
}

#[then("every discovered F# lint target is evaluated")]
fn then_every_fsharp_lint_target_is_evaluated(w: &mut FsharpToolInvocationWorld) {
    assert_eq!(
        w.evaluated, w.configured,
        "every discovered F# lint target must be evaluated"
    );
}

#[then("each target restores its local .NET tool manifest before running Fantomas")]
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
            w.malformed_source_check.is_none(),
            "a workspace without F# lint targets must not invoke the manifest Fantomas tool"
        );
        return;
    }

    let checks = w
        .malformed_source_check
        .as_ref()
        .expect("a configured F# topology must run the manifest Fantomas checks");
    assert_eq!(checks.len(), w.candidate_working_directories.len());
    assert!(
        checks.iter().all(|check| check.restore_succeeded),
        "the local .NET tool manifest must restore before checking fixtures"
    );
    assert!(
        checks.iter().all(|check| check.formatted_source_accepted),
        "the manifest-backed Fantomas check must accept the formatted control source"
    );
    assert!(
        checks.iter().all(|check| check.malformed_source_rejected),
        "the manifest-backed Fantomas check must reject malformed source"
    );
}

#[derive(Debug, Eq, PartialEq)]
struct MalformedSourceCheck {
    restore_succeeded: bool,
    formatted_source_accepted: bool,
    malformed_source_rejected: bool,
}

fn check_malformed_source_if_targets_exist(
    candidate_working_directories: &[PathBuf],
) -> Option<Vec<MalformedSourceCheck>> {
    if candidate_working_directories.is_empty() {
        return None;
    }

    Some(
        candidate_working_directories
            .iter()
            .map(|working_directory| check_malformed_source(working_directory))
            .collect(),
    )
}

fn check_malformed_source(working_directory: &Path) -> MalformedSourceCheck {
    let restore_succeeded = Command::new("dotnet")
        .current_dir(working_directory)
        .args(["tool", "restore"])
        .status()
        .expect("restore local .NET tool manifest")
        .success();
    assert!(
        restore_succeeded,
        "the local .NET tool manifest must restore before Fantomas regression checks"
    );

    let mut formatted_source = Builder::new()
        .prefix("fantomas-formatted-control-")
        .suffix(".fs")
        .tempfile()
        .expect("create formatted F# control fixture");
    writeln!(formatted_source, "module Formatted\n\nlet value = 1")
        .expect("write formatted F# control fixture");
    let mut malformed_source = Builder::new()
        .prefix("fantomas-regression-")
        .suffix(".fs")
        .tempfile()
        .expect("create malformed F# fixture");
    writeln!(malformed_source, "module Malformed\nlet value= 1")
        .expect("write malformed F# fixture");

    let formatted_source_accepted =
        run_manifest_fantomas_check(working_directory, formatted_source.path());
    assert!(
        formatted_source_accepted,
        "the local Fantomas tool must accept the formatted control fixture before malformed-source rejection is evaluated"
    );
    let malformed_source_rejected =
        !run_manifest_fantomas_check(working_directory, malformed_source.path());

    MalformedSourceCheck {
        restore_succeeded,
        formatted_source_accepted,
        malformed_source_rejected,
    }
}

fn run_manifest_fantomas_check(workspace_root: &Path, source_path: &Path) -> bool {
    Command::new("dotnet")
        .current_dir(workspace_root)
        .args([
            "tool",
            "run",
            "fantomas",
            "--check",
            source_path.to_str().expect("UTF-8 fixture path"),
        ])
        .status()
        .expect("run manifest Fantomas check")
        .success()
}

#[derive(Debug, Eq, PartialEq)]
struct FantomasLintTargetAudit {
    candidates: Vec<PathBuf>,
    evaluated_candidates: usize,
    candidate_working_directories: Vec<PathBuf>,
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
        .filter(|path| !lint_commands(path).is_empty())
        .filter(|path| {
            lint_commands(path)
                .iter()
                .any(|command| !fantomas_invocations(command).is_empty())
        })
        .collect::<Vec<_>>();
    candidates.sort();

    let mut missing_local_restores = Vec::new();
    let mut missing_manifest_commands = Vec::new();
    let mut bare_global_invocations = Vec::new();
    let mut candidate_working_directories = Vec::new();
    let mut evaluated_candidates = 0;
    for project_path in &candidates {
        evaluated_candidates += 1;
        candidate_working_directories.push(lint_working_directory(project_path, workspace_root));
        let commands = lint_commands(project_path);
        let mut restore_seen = false;
        let mut local_run_seen = false;
        let mut local_run_without_prior_restore = false;
        let mut bare_global_seen = false;

        for command in commands {
            for segment in shell_segments(&command) {
                let invocations = fantomas_invocations(segment);
                local_run_seen |= invocations.iter().any(|invocation| invocation.is_local);
                bare_global_seen |= invocations.iter().any(|invocation| !invocation.is_local);
                if invocations.iter().any(|invocation| invocation.is_local) && !restore_seen {
                    local_run_without_prior_restore = true;
                }
                restore_seen |= contains_tool_restore(segment);
            }
        }

        if !local_run_seen {
            missing_manifest_commands.push(project_path.clone());
        }
        if !local_run_seen || local_run_without_prior_restore {
            missing_local_restores.push(project_path.clone());
        }
        if bare_global_seen {
            bare_global_invocations.push(project_path.clone());
        }
    }

    candidate_working_directories.sort();
    candidate_working_directories.dedup();

    FantomasLintTargetAudit {
        candidates,
        evaluated_candidates,
        candidate_working_directories,
        missing_local_restores,
        missing_manifest_commands,
        bare_global_invocations,
    }
}

#[derive(Debug, Eq, PartialEq)]
struct FantomasInvocation {
    is_local: bool,
}

fn lint_commands(project_path: &Path) -> Vec<String> {
    let project = fs::read_to_string(project_path)
        .unwrap_or_else(|error| panic!("read {}: {error}", project_path.display()));
    let parsed: Value = serde_json::from_str(&project)
        .unwrap_or_else(|error| panic!("parse {}: {error}", project_path.display()));
    parsed
        .pointer("/targets/lint/options/commands")
        .and_then(Value::as_array)
        .into_iter()
        .flatten()
        .filter_map(Value::as_str)
        .map(str::to_owned)
        .collect()
}

fn lint_working_directory(project_path: &Path, workspace_root: &Path) -> PathBuf {
    let project = fs::read_to_string(project_path)
        .unwrap_or_else(|error| panic!("read {}: {error}", project_path.display()));
    let parsed: Value = serde_json::from_str(&project)
        .unwrap_or_else(|error| panic!("parse {}: {error}", project_path.display()));
    let project_root = project_path
        .parent()
        .expect("project configuration directory");

    match parsed
        .pointer("/targets/lint/options/cwd")
        .and_then(Value::as_str)
    {
        Some("{workspaceRoot}") | None => workspace_root.to_path_buf(),
        Some("{projectRoot}") => project_root.to_path_buf(),
        Some(cwd) => {
            let cwd = PathBuf::from(cwd);
            if cwd.is_absolute() {
                cwd
            } else {
                workspace_root.join(cwd)
            }
        }
    }
}

fn shell_segments(command: &str) -> Vec<&str> {
    command
        .split([';', '\n'])
        .flat_map(|segment| segment.split("&&"))
        .flat_map(|segment| segment.split("||"))
        .map(str::trim)
        .filter(|segment| !segment.is_empty())
        .collect()
}

fn contains_tool_restore(segment: &str) -> bool {
    let tokens = shell_tokens(segment);
    tokens
        .windows(3)
        .any(|window| window == ["dotnet", "tool", "restore"])
}

fn fantomas_invocations(segment: &str) -> Vec<FantomasInvocation> {
    let tokens = shell_tokens(segment);
    tokens
        .windows(2)
        .enumerate()
        .filter(|(_, window)| *window == ["fantomas", "--check"])
        .map(|(index, _)| FantomasInvocation {
            is_local: index >= 3 && tokens[index - 3..index] == ["dotnet", "tool", "run"],
        })
        .collect()
}

fn shell_tokens(segment: &str) -> Vec<&str> {
    segment
        .split_whitespace()
        .map(|token| {
            token.trim_matches(|character: char| matches!(character, '(' | ')' | '"' | '\''))
        })
        .filter(|token| !token.is_empty())
        .collect()
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
        r#"{"targets":{"lint":{"options":{"cwd":"apps/manifest-backed","commands":["dotnet tool restore","dotnet tool run fantomas --check src"]}}}}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "apps/missing-restore/project.json",
        r#"{"targets":{"lint":{"options":{"commands":["dotnet tool run fantomas --check src"]}}}}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "libs/bare-global/project.json",
        r#"{"targets":{"lint":{"options":{"commands":["fantomas --check src"]}}}}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "apps/mixed-local-and-global/project.json",
        r#"{"targets":{"lint":{"options":{"commands":["dotnet tool restore && dotnet tool run fantomas --check src && fantomas --check src"]}}}}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "apps/restore-after-run/project.json",
        r#"{"targets":{"lint":{"options":{"commands":["dotnet tool run fantomas --check src && dotnet tool restore"]}}}}"#,
    );
    write_project_fixture(
        fixture_root.path(),
        "apps/unrelated-target/project.json",
        r#"{"description":"fantomas --check must not be audited here","targets":{"build":{"options":{"commands":["dotnet tool restore && fantomas --check src"]}},"lint":{"options":{"commands":["echo lint-only"]}}}}"#,
    );

    let audit = audit_fantomas_lint_targets(fixture_root.path());

    assert_eq!(audit.candidates.len(), 5);
    assert_eq!(audit.evaluated_candidates, 5);
    assert_eq!(
        audit.candidate_working_directories,
        vec![
            fixture_root.path().to_path_buf(),
            fixture_root.path().join("apps/manifest-backed"),
        ],
        "each distinct effective working directory must be checked once even when multiple lint targets share it"
    );
    assert_eq!(
        audit.missing_local_restores,
        vec![
            fixture_root
                .path()
                .join("apps/missing-restore/project.json"),
            fixture_root
                .path()
                .join("apps/restore-after-run/project.json"),
            fixture_root.path().join("libs/bare-global/project.json"),
        ]
    );
    assert_eq!(
        audit.missing_manifest_commands,
        vec![fixture_root.path().join("libs/bare-global/project.json")]
    );
    assert_eq!(
        audit.bare_global_invocations,
        vec![
            fixture_root
                .path()
                .join("apps/mixed-local-and-global/project.json"),
            fixture_root.path().join("libs/bare-global/project.json"),
        ]
    );

    assert_candidate_local_manifest_control_uses_declared_cwd();
}

fn assert_candidate_local_manifest_control_uses_declared_cwd() {
    let fixture_root = tempfile::tempdir().expect("create local-manifest fixture workspace");
    write_project_fixture(
        fixture_root.path(),
        "apps/local-manifest/project.json",
        r#"{"targets":{"lint":{"options":{"cwd":"apps/local-manifest","commands":["dotnet tool restore && dotnet tool run fantomas --check src"]}}}}"#,
    );
    write_tool_manifest_fixture(
        fixture_root.path(),
        "apps/local-manifest/.config/dotnet-tools.json",
    );

    let audit = audit_fantomas_lint_targets(fixture_root.path());

    assert_eq!(audit.candidates.len(), 1);
    assert_eq!(audit.evaluated_candidates, 1);
    assert_eq!(
        audit.candidate_working_directories,
        vec![fixture_root.path().join("apps/local-manifest")]
    );
    assert!(audit.missing_local_restores.is_empty());
    assert!(audit.missing_manifest_commands.is_empty());
    assert!(audit.bare_global_invocations.is_empty());
    assert!(
        check_malformed_source_if_targets_exist(&audit.candidate_working_directories).is_some(),
        "the local Fantomas control fixture must run from the candidate options.cwd"
    );
}

fn assert_empty_workspace_does_not_require_manifest_tool() {
    let fixture_root = tempfile::tempdir().expect("create empty fixture workspace");
    let audit = audit_fantomas_lint_targets(fixture_root.path());

    assert!(audit.candidates.is_empty());
    assert_eq!(audit.evaluated_candidates, 0);
    assert_eq!(
        check_malformed_source_if_targets_exist(&audit.candidate_working_directories),
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

fn write_tool_manifest_fixture(root: &Path, relative_path: &str) {
    let path = root.join(relative_path);
    fs::create_dir_all(path.parent().expect("fixture tool-manifest directory"))
        .expect("create fixture tool-manifest directory");
    fs::write(
        path,
        r#"{"version":1,"isRoot":true,"tools":{"fantomas":{"version":"7.0.5","commands":["fantomas"]}}}"#,
    )
    .expect("write fixture tool manifest");
}
