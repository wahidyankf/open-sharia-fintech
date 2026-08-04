//! `gate emit` command adapter.

use std::collections::BTreeMap;
use std::io::Write;
use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;

use crate::application::repo_config::{self, GateSurface, ScopeKind};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Arguments for `gate emit`.
#[derive(Args, Debug)]
pub struct EmitArgs {
    /// Surface whose generated artifact to emit.
    #[arg(long)]
    pub surface: String,
}

/// Emit the configured gate surface into its generated artifact.
///
/// # Errors
///
/// Returns an error when the repository root cannot be found or emission
/// fails.
pub fn run(args: &EmitArgs, _output_format: OutputFormat) -> Result<(), Error> {
    let repo_root = git::root::find_root()
        .map_err(|error| anyhow!("failed to find git repository root: {error}"))?;
    emit_at_root(&repo_root, &args.surface, &mut std::io::stdout())
}

/// Emit the configured gate surface into its generated artifact at a known root.
///
/// # Errors
///
/// Returns an error if the requested surface is not `pre-commit`, either
/// configuration file cannot be read, or `package.json` cannot be rewritten.
pub fn emit_at_root(repo_root: &Path, surface: &str, writer: &mut dyn Write) -> Result<(), Error> {
    if surface != "pre-commit" {
        return Err(anyhow!(
            "gate emit currently supports only surface pre-commit"
        ));
    }

    let config = repo_config::load(repo_root)?;
    let mut commands_by_glob: BTreeMap<String, Vec<String>> = BTreeMap::new();
    for gate in &config.gates {
        let Some(scope) = gate.surfaces.get(&GateSurface::PreCommit) else {
            continue;
        };
        if scope.scope != ScopeKind::AffectedFileType {
            continue;
        }
        for glob in scope.glob.iter().chain(&scope.globs) {
            commands_by_glob
                .entry(glob.clone())
                .or_default()
                .push(gate.command.clone());
        }
    }

    let lint_staged = commands_by_glob
        .into_iter()
        .map(|(glob, commands)| (glob, serde_json::json!(commands)))
        .collect();
    let package_path = repo_root.join("package.json");
    let mut package: serde_json::Value = serde_json::from_slice(
        &std::fs::read(&package_path)
            .with_context(|| format!("cannot read {}", package_path.display()))?,
    )?;
    replace_lint_staged_marker_first(&mut package, lint_staged)?;
    std::fs::write(
        &package_path,
        format!("{}\n", serde_json::to_string_pretty(&package)?),
    )
    .with_context(|| format!("cannot write {}", package_path.display()))?;
    writeln!(writer, "Emitted lint-staged from gate surface pre-commit")?;
    Ok(())
}

fn replace_lint_staged_marker_first(
    package: &mut serde_json::Value,
    lint_staged: serde_json::Map<String, serde_json::Value>,
) -> Result<(), Error> {
    let package_object = package
        .as_object_mut()
        .ok_or_else(|| anyhow!("package.json must contain a JSON object"))?;
    let generated_block = serde_json::Value::Object(lint_staged);

    if let Some(existing_marker) = package_object.get_mut("lint-staged") {
        *existing_marker = generated_block;
    } else {
        package_object.insert("lint-staged".to_string(), generated_block);
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn pre_commit_emits_per_file_gates_in_declaration_order() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: format-markdown\n",
            "    type: mutation\n",
            "    command: prettier --write\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: markdownlint\n",
            "    type: check\n",
            "    command: markdownlint-cli2\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: ci-only\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        repo.path().join("package.json"),
        "{\"name\":\"fixture\",\"lint-staged\":{\"old\":[\"old command\"]}}\n",
    )
    .unwrap();

    emit_at_root(repo.path(), "pre-commit", &mut Vec::new())
        .expect("gate emit must generate lint-staged from pre-commit per-file gates");

    let package: serde_json::Value =
        serde_json::from_slice(&std::fs::read(repo.path().join("package.json")).unwrap()).unwrap();
    assert_eq!(
        package["lint-staged"]["*.md"],
        serde_json::json!(["prettier --write", "markdownlint-cli2"])
    );
    assert_eq!(package["lint-staged"].as_object().unwrap().len(), 1);
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn re_emitting_replaces_the_existing_lint_staged_marker_once() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: format-markdown\n",
            "    type: mutation\n",
            "    command: prettier --write\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        repo.path().join("package.json"),
        "{\"name\":\"fixture\",\"lint-staged\":{\"old\":[\"old command\"]}}\n",
    )
    .unwrap();

    emit_at_root(repo.path(), "pre-commit", &mut Vec::new()).unwrap();
    let first = std::fs::read_to_string(repo.path().join("package.json")).unwrap();
    emit_at_root(repo.path(), "pre-commit", &mut Vec::new()).unwrap();
    let second = std::fs::read_to_string(repo.path().join("package.json")).unwrap();

    assert_eq!(second, first);
    assert_eq!(second.matches("\"lint-staged\"").count(), 1);
}
