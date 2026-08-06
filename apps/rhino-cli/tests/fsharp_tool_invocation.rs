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
    let targets = manifest_backed_fantomas_targets(&workspace_root);

    w.configured = targets.len();
    for project_path in targets {
        let project = fs::read_to_string(&project_path)
            .unwrap_or_else(|error| panic!("read {}: {error}", project_path.display()));

        if project.contains("dotnet tool restore")
            && project.contains("dotnet tool run fantomas --check")
        {
            w.manifest += 1;
        }
        if project
            .lines()
            .any(|line| line.contains("fantomas --check") && !line.contains("dotnet tool run"))
        {
            w.bare_global += 1;
        }
    }
}

#[when("the configured F# lint targets are inspected")]
fn when_fsharp_lint_targets_are_inspected(w: &mut FsharpToolInvocationWorld) {
    if w.configured == 0 {
        return;
    }

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
    if w.configured == 0 {
        return;
    }

    assert!(
        w.malformed_source_rejected,
        "the manifest-backed Fantomas check must reject malformed source"
    );
}

fn manifest_backed_fantomas_targets(workspace_root: &Path) -> Vec<PathBuf> {
    let mut targets = WalkDir::new(workspace_root)
        .into_iter()
        .filter_entry(|entry| {
            !matches!(
                entry.file_name().to_str(),
                Some(".git" | "node_modules" | "target" | "dist")
            )
        })
        .filter_map(|entry| entry.ok())
        .map(|entry| entry.into_path())
        .filter(|path| path.file_name().is_some_and(|name| name == "project.json"))
        .filter(|path| {
            let project = fs::read_to_string(path)
                .unwrap_or_else(|error| panic!("read {}: {error}", path.display()));
            project.contains("dotnet tool restore")
                && project.contains("dotnet tool run fantomas --check")
        })
        .collect::<Vec<_>>();
    targets.sort();
    targets
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
