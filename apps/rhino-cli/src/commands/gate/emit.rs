//! `gate emit` command adapter.

use std::io::Write;
use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;

use crate::application::repo_config::{self, GateSurface, GateType, RepoConfig, ScopeKind};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// The lightweight resolver shim that generated `rhino-cli` gate kind
/// commands invoke instead of the old `cargo`-based invocation (`cargo`,
/// then `run`, `--release`, `--quiet`, `--manifest-path
/// apps/rhino-cli/Cargo.toml`, `--`). The old form paid cargo's
/// invocation-check tax (hundreds of milliseconds) on every single hook/gate
/// call even when the binary is already built; the shim resolves straight to
/// the built binary. Single source of truth for every generated artifact
/// that must invoke the rhino-cli binary: this module's `lint-staged`
/// rendering, the generated Husky shims (pre-commit/pre-push/commit-msg),
/// and `gate::validate`'s composition checks, should all reference this
/// constant rather than duplicating the literal path.
pub(crate) const RHINO_CLI_RESOLVER_SHIM: &str = "apps/rhino-cli/scripts/rhino-bin.sh";

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
        repo_config::GateKind::RhinoCli => {
            format!("{RHINO_CLI_RESOLVER_SHIM} {}", gate.command)
        }
        repo_config::GateKind::External if is_node_resolved(gate) => {
            node_modules_bin_command(&gate.command)
        }
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

/// Whether a gate's `kind: external` command resolves its tool from this
/// repository's `node_modules` (an npm package) rather than a system `PATH`
/// binary. `doctor-tools: [npm]` is the registry's existing signal for a
/// tool provisioned by `npm install`; reusing it here needs no new schema
/// field, matching how `doctor-tools: [shellcheck]` already flags a system
/// tool's own prerequisite.
fn is_node_resolved(gate: &repo_config::GateEntry) -> bool {
    gate.doctor_tools.iter().any(|tool| tool == "npm")
}

/// Rewrite a node-resolved gate's command to invoke its tool through the
/// repository-local `node_modules/.bin` directory instead of `npx`. `npx`
/// pays its own resolution/download-check overhead on every invocation even
/// when the package is already installed; resolving straight to the binary
/// mirrors the `RHINO_CLI_RESOLVER_SHIM` shortcut for `kind: rhino-cli`
/// gates.
///
/// Handles both a bare tool invocation (`prettier --write`) and an
/// `npx`-wrapped one (`npx --no -- commitlint --edit "$1"`), skipping `npx`'s
/// own flags and `--` separator to find the wrapped tool's name.
fn node_modules_bin_command(command: &str) -> String {
    let (mut tool, mut arguments) = split_leading_token(command);
    if tool == "npx" {
        loop {
            let (next_tool, next_arguments) = split_leading_token(arguments);
            if next_tool.starts_with('-') {
                arguments = next_arguments;
                continue;
            }
            tool = next_tool;
            arguments = next_arguments;
            break;
        }
    }
    if arguments.is_empty() {
        format!("node_modules/.bin/{tool}")
    } else {
        format!("node_modules/.bin/{tool} {arguments}")
    }
}

/// Split a command string into its leading whitespace-delimited token and
/// the (whitespace-trimmed) remainder.
fn split_leading_token(command: &str) -> (&str, &str) {
    match command.split_once(char::is_whitespace) {
        Some((first, rest)) => (first, rest.trim_start()),
        None => (command, ""),
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
        ci_group: None,
    };

    assert_eq!(
        command_with_fixed_arguments(&gate),
        "fixture-command --exclude \"contains spaces\" --exclude \"it's quoted\" --path \"back\\\\\\\\slash\""
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn command_with_fixed_arguments_invokes_rhino_cli_through_the_resolver_shim() {
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
        ci_group: None,
    };

    assert_eq!(
        command_with_fixed_arguments(&gate),
        "apps/rhino-cli/scripts/rhino-bin.sh md mermaid validate --exclude \"apps/example/content\" --exempt \"*__draft__*.md\""
    );
}

/// Binds the Gherkin scenario "Rhino CLI kind renders a resolver shim
/// invocation"
/// (specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature).
/// The `cargo run` form pays cargo's invocation-check tax on every gate call;
/// generated commands must instead invoke the lightweight resolver shim.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn rhino_cli_kind_renders_a_resolver_shim_invocation() {
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
        args: BTreeMap::new(),
        surfaces: BTreeMap::new(),
        carve_out: None,
        verifies: None,
        category: None,
        ci_group: None,
    };

    let rendered = command_with_fixed_arguments(&gate);

    assert!(
        rendered.contains("apps/rhino-cli/scripts/rhino-bin.sh"),
        "expected the generated command to invoke the resolver shim at \
         apps/rhino-cli/scripts/rhino-bin.sh, got {rendered:?}"
    );
    assert!(
        !rendered.contains("cargo run"),
        "expected the generated command to contain no cargo run substring, got {rendered:?}"
    );
}

/// Binds the Gherkin scenario "Node-resolved external tools render a
/// repository-local bin path"
/// (specs/apps/rhino/behavior/rhino-cli/gherkin/gate/gate-emission.feature).
/// `npx` pays its own resolution/download-check tax on every invocation even
/// when the tool is already installed in `node_modules`; generated commands
/// for node-resolved external tools must instead invoke the repository-local
/// `node_modules/.bin` path directly.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn external_node_resolved_kind_renders_a_node_modules_bin_invocation() {
    use std::collections::BTreeMap;

    use crate::application::repo_config::{GateKind, GateType};

    let gate = repo_config::GateEntry {
        id: "fixture".to_string(),
        gate_type: GateType::Check,
        command: r#"npx --no -- commitlint --edit "$1""#.to_string(),
        kind: GateKind::External,
        doctor_tools: vec!["npm".to_string()],
        wiring: None,
        restages: false,
        args: BTreeMap::new(),
        surfaces: BTreeMap::new(),
        carve_out: None,
        verifies: None,
        category: None,
        ci_group: None,
    };

    let rendered = command_with_fixed_arguments(&gate);

    assert!(
        rendered.contains("node_modules/.bin/commitlint"),
        "expected the generated command to invoke the tool through \
         node_modules/.bin/commitlint, got {rendered:?}"
    );
    assert!(
        !rendered.contains("npx"),
        "expected the generated command to contain no npx substring, got {rendered:?}"
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
                    "bash -c 'apps/rhino-cli/scripts/rhino-bin.sh repo-config validate' --"
                ]),
            ),
            (
                "repo-settings.yml".to_string(),
                serde_json::json!([
                    "bash -c 'apps/rhino-cli/scripts/rhino-bin.sh repo-config validate' --"
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

/// Regression: a `lint-staged-shell` template that used a bare
/// `for f; do <command> -f "$f" ...; done` loop with no `set -e` masked an
/// earlier file's failure whenever a later file in the same batch succeeded —
/// a POSIX `for` loop's exit status is the *last* command's, not the first
/// failure's. The fix hands the whole batch to the wrapped command in one
/// call (`{{command}} "$@"`) so that command's own exit status propagates
/// untouched. This is a self-contained fixture (not the repository's own
/// `repo-config.yml`, which is not required to be identical across the
/// sibling repositories this file's parity manifest covers): it drives the
/// exact emitted, wrapped command this file produces against a fixture batch
/// whose checker fails on the first file and succeeds on the second, so a
/// regression back to the fail-open shape is caught here rather than only in
/// a specific repository's own registry declaration.
#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn lint_staged_shell_forwarding_the_whole_batch_fails_fast_on_a_leading_failure() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: fixture-checker\n",
            "    type: check\n",
            "    command: sh check.sh\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit:\n",
            "        scope: affected-file-type\n",
            "        glob: '*.fixture'\n",
            "        lint-staged-shell: '{{command}} \"$@\"'\n",
        ),
    )
    .unwrap();
    std::fs::write(
        repo.path().join("check.sh"),
        // Mirrors the shape of a real per-file wrapper script: it owns its
        // own fail-fast loop over every argument it is handed.
        "#!/bin/sh\nset -eu\nfor f; do\n  if grep -q FAIL \"$f\"; then\n    exit 1\n  fi\ndone\n",
    )
    .unwrap();

    let config = repo_config::load(repo.path()).unwrap();
    let command = lint_staged_from_config(&config)["*.fixture"][0]
        .as_str()
        .unwrap()
        .to_string();

    let invalid = repo.path().join("invalid.fixture");
    std::fs::write(&invalid, "FAIL\n").unwrap();
    let valid = repo.path().join("valid.fixture");
    std::fs::write(&valid, "ok\n").unwrap();

    // Forward the fixture files as "$@" to the emitted command exactly as
    // lint-staged appends matched files after the configured command line.
    let script = repo.path().join("run.sh");
    std::fs::write(&script, format!("#!/bin/sh\n{command} \"$@\"\n")).unwrap();

    let status = std::process::Command::new("sh")
        .arg(&script)
        .arg(&invalid)
        .arg(&valid)
        .current_dir(repo.path())
        .status()
        .expect("run the generated lint-staged command");
    assert!(
        !status.success(),
        "an earlier failing file must fail the batch even when a later file passes"
    );

    // Control: an all-passing batch must still succeed.
    let status = std::process::Command::new("sh")
        .arg(&script)
        .arg(&valid)
        .current_dir(repo.path())
        .status()
        .expect("run the generated lint-staged command");
    assert!(status.success(), "an all-passing batch must still succeed");
}
