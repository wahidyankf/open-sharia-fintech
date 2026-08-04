//! Regression coverage for manifest-backed Fantomas lint targets.

#![allow(clippy::missing_docs_in_private_items)]
#![allow(clippy::doc_markdown)]
#![allow(clippy::panic, clippy::unwrap_used)]

use std::fs;
use std::io::Write;
use std::path::PathBuf;
use std::process::Command;

use cucumber::{World as _, given, then, when};
use tempfile::Builder;

#[derive(Debug, cucumber::World)]
#[world(init = Self::new)]
struct FsharpToolInvocationWorld {
    configured: usize,
    manifest: usize,
    bare_global: usize,
    malformed_source_rejected: bool,
}

impl FsharpToolInvocationWorld {
    fn new() -> Self {
        Self {
            configured: 0,
            manifest: 0,
            bare_global: 0,
            malformed_source_rejected: false,
        }
    }
}

#[given("the F# lint targets are configured")]
fn given_fsharp_lint_targets(w: &mut FsharpToolInvocationWorld) {
    let workspace_root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
    let targets = [
        ("apps/crane-cli/project.json", "apps/crane-cli/src"),
        ("apps/ose-be/project.json", "apps/ose-be/src"),
        (
            "apps/organiclever-be/project.json",
            "apps/organiclever-be/src",
        ),
        (
            "libs/fsharp-crane-core/project.json",
            "libs/fsharp-crane-core/src",
        ),
    ];

    w.configured = targets.len();
    for (project_path, source_path) in targets {
        let project = fs::read_to_string(workspace_root.join(project_path))
            .unwrap_or_else(|error| panic!("read {project_path}: {error}"));
        let manifest_restore = "\"dotnet tool restore\"";
        let manifest_command = format!("dotnet tool run fantomas --check {source_path}");
        let bare_global_command = format!("\"fantomas --check {source_path}\"");

        if project.contains(manifest_restore) && project.contains(&manifest_command) {
            w.manifest += 1;
        }
        if project.contains(&bare_global_command) {
            w.bare_global += 1;
        }
    }
}

#[when("the configured F# lint targets are inspected")]
fn when_fsharp_lint_targets_are_inspected(w: &mut FsharpToolInvocationWorld) {
    let workspace_root = PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("../..");
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
    w.malformed_source_rejected = !status.success();
}

#[then("each target restores the local .NET tool manifest before running Fantomas")]
fn then_targets_restore_manifest(w: &mut FsharpToolInvocationWorld) {
    assert_eq!(w.manifest, w.configured);
}

#[then("no target invokes the global Fantomas app host directly")]
fn then_targets_do_not_use_global_fantomas(w: &mut FsharpToolInvocationWorld) {
    assert_eq!(w.bare_global, 0);
}

#[then("an unformatted source file still makes the lint target fail")]
fn then_configuration_keeps_check_mode(w: &mut FsharpToolInvocationWorld) {
    assert!(
        w.malformed_source_rejected,
        "the manifest-backed Fantomas check must reject malformed source"
    );
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
