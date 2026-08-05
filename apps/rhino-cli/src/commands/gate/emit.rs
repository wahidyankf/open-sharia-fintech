//! `gate emit` command adapter.

use std::io::Write;
use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;

use crate::application::repo_config::{self, GateSurface, GateType, RepoConfig, ScopeKind};
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
    let lint_staged = lint_staged_from_config(&config);
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

/// Derive the `lint-staged` JSON block from pre-commit affected-file gates.
#[must_use]
pub(crate) fn lint_staged_from_config(
    config: &RepoConfig,
) -> serde_json::Map<String, serde_json::Value> {
    // `lint-staged` executes each glob's commands in array order, and its
    // serialized key order is the plan artifact's declaration-order contract.
    // Keep first occurrence order instead of sorting glob names.
    let mut commands_by_glob: Vec<(String, Vec<String>)> = Vec::new();
    for gate in &config.gates {
        let Some(scope) = gate.surfaces.get(&GateSurface::PreCommit) else {
            continue;
        };
        if scope.scope != ScopeKind::AffectedFileType || !is_lint_staged_eligible(gate) {
            continue;
        }
        for glob in scope.glob.iter().chain(&scope.globs) {
            let command = lint_staged_command(gate, scope);
            if let Some((_, commands)) = commands_by_glob
                .iter_mut()
                .find(|(registered_glob, _)| registered_glob == glob)
            {
                commands.push(command);
            } else {
                commands_by_glob.push((glob.clone(), vec![command]));
            }
        }
    }

    commands_by_glob
        .into_iter()
        .map(|(glob, commands)| (glob, serde_json::json!(commands)))
        .collect()
}

/// Render one gate as the command lint-staged must execute for its glob.
fn lint_staged_command(gate: &repo_config::GateEntry, scope: &repo_config::SurfaceScope) -> String {
    let command = command_with_fixed_arguments(gate);
    let Some(shell_template) = &scope.lint_staged_shell else {
        return command;
    };

    let shell_body = shell_template.replacen("{{command}}", &command, 1);
    format!("bash -c {} --", shell_script_quote(&shell_body))
}

/// Whether a pre-commit file-scoped gate belongs to lint-staged's one batch.
///
/// Formatter mutations run inside the batch so their output is available to
/// subsequent validators. Other mutations, such as lockfile synchronization,
/// remain direct hook work and must not be emitted as lint-staged commands.
fn is_lint_staged_eligible(gate: &repo_config::GateEntry) -> bool {
    gate.gate_type == GateType::Check
        || (gate.gate_type == GateType::Mutation && gate.category.as_deref() == Some("formatter"))
}

/// Render a registry command with its fixed arguments for a generated shell command.
fn command_with_fixed_arguments(gate: &repo_config::GateEntry) -> String {
    let command = match gate.kind {
        repo_config::GateKind::RhinoCli => format!(
            "cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- {}",
            gate.command
        ),
        repo_config::GateKind::External | repo_config::GateKind::Nx => gate.command.clone(),
    };
    let fixed_arguments = repo_config::fixed_arguments(gate);
    if fixed_arguments.is_empty() {
        command
    } else {
        let quoted_arguments = fixed_arguments
            .iter()
            .enumerate()
            .map(|(index, argument)| {
                if index % 2 == 0 {
                    argument.clone()
                } else {
                    shell_quote(argument)
                }
            })
            .collect::<Vec<_>>();
        format!("{command} {}", quoted_arguments.join(" "))
    }
}

/// Quote one generated argument for lint-staged's POSIX-shell command string.
///
/// The emitted artifacts use double quotes consistently, including for values
/// that happen to be shell-safe. Escaping the characters with meaning inside
/// double quotes keeps configuration values literal when lint-staged passes
/// them through its shell.
fn shell_quote(argument: &str) -> String {
    format!(
        "\"{}\"",
        argument
            .replace('\\', "\\\\")
            .replace('"', "\\\"")
            .replace('$', "\\$")
            .replace('`', "\\`")
    )
}

/// Quote a whole script for `bash -c`, retaining literal shell expansion inside it.
fn shell_script_quote(script: &str) -> String {
    format!("'{}'", script.replace('\'', "'\"'\"'"))
}

/// Replaces or inserts the generated `lint-staged` entry in a package object.
///
/// # Errors
///
/// Returns an error when the provided package value is not a JSON object.
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
            "    category: formatter\n",
            "    args:\n",
            "      exempt:\n",
            "        - generated.md\n",
            "      exclude:\n",
            "        - generated\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: markdownlint\n",
            "    type: check\n",
            "    command: markdownlint-cli2\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
            "  - id: lockfile-sync\n",
            "    type: mutation\n",
            "    command: git lockfile sync\n",
            "    kind: rhino-cli\n",
            "    restages: true\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: 'apps/*/package.json' }\n",
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
        serde_json::json!([
            "prettier --write --exclude \"generated\" --exempt \"generated.md\"",
            "markdownlint-cli2"
        ])
    );
    assert_eq!(package["lint-staged"].as_object().unwrap().len(), 1);
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn lint_staged_preserves_first_glob_declaration_order() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: first-declared\n",
            "    type: check\n",
            "    command: first-command\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: 'z-first' }\n",
            "  - id: second-declared\n",
            "    type: check\n",
            "    command: second-command\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: 'a-second' }\n",
        ),
    )
    .unwrap();

    let config = repo_config::load(repo.path()).unwrap();
    let emitted = lint_staged_from_config(&config);
    let actual_keys = emitted.keys().cloned().collect::<Vec<_>>();

    assert_eq!(actual_keys, ["z-first", "a-second"]);
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

#[cfg(test)]
#[test]
fn command_with_fixed_arguments_quotes_shell_sensitive_values() {
    use std::collections::BTreeMap;

    use crate::application::repo_config::{GateKind, GateType};

    let gate = repo_config::GateEntry {
        id: "fixture".to_string(),
        gate_type: GateType::Check,
        command: "fixture-command".to_string(),
        kind: GateKind::External,
        doctor_tools: Vec::new(),
        wiring: None,
        restages: false,
        args: BTreeMap::from([
            (
                "exclude".to_string(),
                vec!["contains spaces".to_string(), "it's quoted".to_string()],
            ),
            ("path".to_string(), vec![r"back\\slash".to_string()]),
        ]),
        surfaces: BTreeMap::new(),
        carve_out: None,
        verifies: None,
        category: None,
    };

    assert_eq!(
        command_with_fixed_arguments(&gate),
        "fixture-command --exclude \"contains spaces\" --exclude \"it's quoted\" --path \"back\\\\\\\\slash\""
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn command_with_fixed_arguments_invokes_rhino_cli_through_the_local_manifest() {
    use std::collections::BTreeMap;

    use crate::application::repo_config::{GateKind, GateType};

    let gate = repo_config::GateEntry {
        id: "fixture".to_string(),
        gate_type: GateType::Check,
        command: "md mermaid validate".to_string(),
        kind: GateKind::RhinoCli,
        doctor_tools: Vec::new(),
        wiring: None,
        restages: false,
        args: BTreeMap::from([
            (
                "exclude".to_string(),
                vec!["apps/example/content".to_string()],
            ),
            ("exempt".to_string(), vec!["*__draft__*.md".to_string()]),
        ]),
        surfaces: BTreeMap::new(),
        carve_out: None,
        verifies: None,
        category: None,
    };

    assert_eq!(
        command_with_fixed_arguments(&gate),
        "cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- md mermaid validate --exclude \"apps/example/content\" --exempt \"*__draft__*.md\""
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn lint_staged_shell_overrides_wrap_or_own_the_derived_file_invocation() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: repo-config-schema\n",
            "    type: check\n",
            "    command: repo-config validate\n",
            "    kind: rhino-cli\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        globs:\n",
            "          - repo-config.yml\n",
            "          - repo-settings.yml\n",
            "        lint-staged-shell: '{{command}}'\n",
            "  - id: docker-compose-config\n",
            "    type: check\n",
            "    command: docker compose config\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        glob: 'docker-compose*.{yml,yaml}'\n",
            "        lint-staged-shell: 'for f; do docker compose -f \"$f\" config > /dev/null; done'\n",
        ),
    )
    .unwrap();

    let config = repo_config::load(repo.path()).unwrap();
    assert_eq!(
        lint_staged_from_config(&config),
        serde_json::Map::from_iter([
            (
                "repo-config.yml".to_string(),
                serde_json::json!([
                    "bash -c 'cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate' --"
                ]),
            ),
            (
                "repo-settings.yml".to_string(),
                serde_json::json!([
                    "bash -c 'cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- repo-config validate' --"
                ]),
            ),
            (
                "docker-compose*.{yml,yaml}".to_string(),
                serde_json::json!([
                    "bash -c 'for f; do docker compose -f \"$f\" config > /dev/null; done' --"
                ]),
            ),
        ]),
    );
}
