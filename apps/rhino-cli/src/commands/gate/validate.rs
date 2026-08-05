//! `gate validate` command adapter.

use std::collections::BTreeMap;
use std::io::Write;
use std::path::Path;

use anyhow::{Error, anyhow};
use clap::Args;
use serde::Deserialize;

use crate::application::repo_config::{self, GateCarveOut, GateSurface, GateType, GateWiring};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

use super::emit;

/// Arguments for `gate validate`.
#[derive(Args, Debug)]
pub struct ValidateArgs {}

/// Validate gate-registry composition rules.
///
/// # Errors
///
/// Returns an error when the repository root or `repo-config.yml` cannot be
/// read, or when a composition rule is violated.
pub fn run(_args: &ValidateArgs, _output_format: OutputFormat) -> Result<(), Error> {
    let repo_root = git::root::find_root()?;
    run_at_root(&repo_root, &mut std::io::stdout())
}

/// Validate gate-registry composition rules at a known repository root.
///
/// # Errors
///
/// Returns an error when `repo-config.yml` cannot be read or when a check gate
/// declared for a local hook surface is missing its CI declaration.
pub fn run_at_root(repo_root: &Path, writer: &mut dyn Write) -> Result<(), Error> {
    let config = repo_config::load(repo_root)?;

    validate_local_hook_composition(&config, writer)?;
    validate_verifies_references(&config, writer)?;
    validate_formatter_verification(&config, writer)?;
    validate_local_hook_shims(repo_root, &config, writer)?;
    validate_ci_workflow(repo_root, &config, writer)?;
    validate_lint_staged(repo_root, &config, writer)
}

/// Validates the local-hook check-to-CI composition rule.
///
/// # Errors
///
/// Returns an error when a check gate declares pre-commit or pre-push without CI and lacks
/// the `staged-only` carve-out, or when the diagnostic cannot be written.
fn validate_local_hook_composition(
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for gate in &config.gates {
        let is_local_hook_check_without_ci = gate.gate_type == GateType::Check
            && (gate.surfaces.contains_key(&GateSurface::PreCommit)
                || gate.surfaces.contains_key(&GateSurface::PrePush))
            && !gate.surfaces.contains_key(&GateSurface::Ci)
            && gate.carve_out.as_ref() != Some(&GateCarveOut::StagedOnly);
        if is_local_hook_check_without_ci {
            let message = format!(
                "Gate Composition Rule violation: gate {:?} declares a local hook surface but is missing ci",
                gate.id
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
}

/// Validates that every `verifies` reference names a declared gate.
///
/// # Errors
///
/// Returns an error when a gate verifies an undeclared gate or the diagnostic
/// cannot be written.
fn validate_verifies_references(
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for gate in &config.gates {
        if let Some(verified_gate) = &gate.verifies {
            let target = config
                .gates
                .iter()
                .find(|candidate| candidate.id == *verified_gate);
            let Some(target) = target else {
                let message = format!(
                    "Gate {:?} verifies orphan gate {:?}",
                    gate.id, verified_gate
                );
                writeln!(writer, "{message}")?;
                return Err(anyhow!(message));
            };
            if gate.gate_type != GateType::Check
                || target.gate_type != GateType::Mutation
                || target.category.as_deref() != Some("formatter")
            {
                let message = format!(
                    "Gate {:?}.verifies must link a check to a formatter mutation, not {:?}",
                    gate.id, verified_gate
                );
                writeln!(writer, "{message}")?;
                return Err(anyhow!(message));
            }
        }
    }
    Ok(())
}

/// Validates that each formatter mutation is covered by a check gate.
///
/// # Errors
///
/// Returns an error when a formatter lacks a verifying check or the diagnostic
/// cannot be written.
fn validate_formatter_verification(
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for formatter in config.gates.iter().filter(|gate| {
        gate.gate_type == GateType::Mutation && gate.category.as_deref() == Some("formatter")
    }) {
        let verifier_count = config
            .gates
            .iter()
            .filter(|gate| {
                gate.gate_type == GateType::Check
                    && gate.verifies.as_deref() == Some(formatter.id.as_str())
            })
            .count();
        if verifier_count != 1 {
            let message = format!(
                "Formatter mutation {:?} requires exactly one check gate whose verifies field names it; found {verifier_count}",
                formatter.id,
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
}

/// Validates every generated Husky shim required by declared local-hook gates.
///
/// # Errors
///
/// Returns an error when the required registry invocation is absent or the
/// diagnostic cannot be written.
fn validate_local_hook_shims(
    repo_root: &Path,
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for (surface, shim_name) in [
        (GateSurface::CommitMsg, "commit-msg"),
        (GateSurface::PreCommit, "pre-commit"),
        (GateSurface::PrePush, "pre-push"),
    ] {
        if !config
            .gates
            .iter()
            .any(|gate| gate.surfaces.contains_key(&surface))
        {
            continue;
        }
        let shim = repo_root.join(".husky").join(shim_name);
        let expected_invocation = format!("gate run --surface={shim_name}");
        let has_registry_invocation = std::fs::read_to_string(&shim)
            .is_ok_and(|contents| has_executable_shell_invocation(&contents, &expected_invocation));
        if !has_executable_mode(&shim) || !has_registry_invocation {
            let message = format!(
                "Gate surface shim .husky/{shim_name} must be executable and invoke gate run --surface={shim_name}"
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
}

/// Returns whether a hook file has an executable permission bit.
fn has_executable_mode(path: &Path) -> bool {
    #[cfg(unix)]
    {
        use std::os::unix::fs::PermissionsExt;

        std::fs::metadata(path).is_ok_and(|metadata| metadata.permissions().mode() & 0o111 != 0)
    }
    #[cfg(not(unix))]
    {
        std::fs::metadata(path).is_ok()
    }
}

/// Returns whether a shell script contains a non-comment line with an invocation.
fn has_executable_shell_invocation(contents: &str, expected_invocation: &str) -> bool {
    contents.lines().any(|line| {
        let trimmed = line.trim_start();
        !trimmed.starts_with('#') && trimmed.contains(expected_invocation)
    })
}

/// Validates registry-backed commands and hand-wired jobs in the CI workflow.
///
/// # Errors
///
/// Returns an error when the workflow declares an unknown command, omits a
/// required hand-wired gate, or a diagnostic cannot be written.
fn validate_ci_workflow(
    repo_root: &Path,
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let workflow = workflow_jobs(repo_root, config, writer)?;
    validate_ci_matrix_contract(config, &workflow, writer)?;
    validate_ci_doctor_bootstrap(config, &workflow, writer)?;
    validate_ci_gate_invocations(config, &workflow, writer)?;
    validate_hand_wired_ci_jobs(config, &workflow, writer)
}

/// Loads the CI workflow only when the registry declares a CI surface.
///
/// # Errors
///
/// Returns an error when the workflow declares a command absent from the gate
/// registry or its diagnostic cannot be written.
fn workflow_jobs(
    repo_root: &Path,
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<Workflow, Error> {
    let pr_workflow = repo_root.join(".github/workflows/pr-quality-gate.yml");
    let has_ci_gates = config
        .gates
        .iter()
        .any(|gate| gate.surfaces.contains_key(&GateSurface::Ci));
    if !has_ci_gates {
        return Ok(Workflow::default());
    }
    let workflow_source = match std::fs::read_to_string(&pr_workflow) {
        Ok(workflow) => workflow,
        Err(error) => {
            let message = format!(
                "CI workflow pr-quality-gate.yml is required for declared CI gates: {error}"
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    };
    let workflow: Workflow = match serde_norway::from_str(&workflow_source) {
        Ok(workflow) => workflow,
        Err(error) => {
            let message = format!("CI workflow pr-quality-gate.yml is not valid YAML: {error}");
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    };
    if workflow.jobs.is_empty() {
        let hand_wired_ids = config
            .gates
            .iter()
            .filter(|gate| {
                gate.wiring.as_ref() == Some(&GateWiring::HandWired)
                    && gate.surfaces.contains_key(&GateSurface::Ci)
            })
            .map(|gate| gate.id.as_str())
            .collect::<Vec<_>>();
        let suffix = if hand_wired_ids.is_empty() {
            String::new()
        } else {
            format!(
                "; missing hand-wired gate job(s): {}",
                hand_wired_ids.join(", ")
            )
        };
        let message = format!(
            "CI workflow pr-quality-gate.yml must declare at least one job for declared CI gates{suffix}"
        );
        writeln!(writer, "{message}")?;
        return Err(anyhow!(message));
    }
    Ok(workflow)
}

/// Validates the generated CI matrix and its quality-gate dependency.
fn validate_ci_matrix_contract(
    config: &repo_config::RepoConfig,
    workflow: &Workflow,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let has_matrix_gates = config.gates.iter().any(|gate| {
        gate.surfaces.contains_key(&GateSurface::Ci)
            && gate.wiring.as_ref() != Some(&GateWiring::HandWired)
    });
    if !has_matrix_gates {
        return Ok(());
    }
    let has_enumeration = workflow.jobs.get("enumerate").is_some_and(|job| {
        job.steps
            .iter()
            .filter_map(|step| step.run.as_deref())
            .any(|run| run.contains("gate list --surface=ci"))
    });
    let has_matrix_dispatcher = workflow.jobs.get("gate").is_some_and(|job| {
        let derives_gate_matrix = job.needs.contains("enumerate")
            && job
                .strategy
                .matrix
                .get("gate")
                .is_some_and(|entry| entry.contains("fromJson(needs.enumerate.outputs.gates)"));
        let dispatches_selected_gate = job
            .steps
            .iter()
            .filter_map(|step| step.run.as_deref())
            .any(|run| run.contains("gate run --surface=ci --only=${{ matrix.gate.id }}"));
        derives_gate_matrix && dispatches_selected_gate
    });
    let aggregate_requires_matrix_prerequisites = workflow
        .jobs
        .get("quality-gate")
        .is_some_and(|job| job.needs.contains("enumerate") && job.needs.contains("gate"));
    if has_enumeration && has_matrix_dispatcher && aggregate_requires_matrix_prerequisites {
        return Ok(());
    }
    let message = "CI workflow must derive its gate matrix from the enumerate job's gate list, dispatch it through the gate job, and make quality-gate depend on enumerate and gate";
    writeln!(writer, "{message}")?;
    Err(anyhow!(message))
}

/// Validates that Doctor setup is selected from registry metadata rather than
/// performing a full bootstrap in every CI job.
fn validate_ci_doctor_bootstrap(
    config: &repo_config::RepoConfig,
    workflow: &Workflow,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    if !config
        .gates
        .iter()
        .any(|gate| !gate.doctor_tools.is_empty())
    {
        return Ok(());
    }

    let has_full_bootstrap = workflow.jobs.values().any(|job| {
        job.steps
            .iter()
            .filter_map(|step| step.run.as_deref())
            .any(|run| run.contains("npm run doctor -- --fix") && !run.contains("--tools"))
    });
    if has_full_bootstrap {
        let message = "CI workflow must not run an unconditional full Doctor bootstrap";
        writeln!(writer, "{message}")?;
        return Err(anyhow!(message));
    }

    let format_derives_tool_union = workflow.jobs.get("format").is_some_and(|job| {
        job.steps
            .iter()
            .filter_map(|step| step.run.as_deref())
            .any(|run| {
                run.contains("gate list --surface=pre-commit --format=json")
                    && run.contains("[.[] | .doctor_tools[]]")
                    && run.contains("unique")
                    && run.contains("npm run doctor -- --fix --tools")
                    && run.contains("if [ -n \"$tools\" ]")
            })
    });
    let matrix_uses_declared_tools = workflow.jobs.get("gate").is_some_and(|job| {
        job.steps
            .iter()
            .filter_map(|step| step.run.as_deref())
            .any(|run| {
                run.contains("matrix.gate.doctor_tools")
                    && run.contains("npm run doctor -- --fix --tools")
                    && run.contains("if [ -n \"$tools\" ]")
            })
    });
    if format_derives_tool_union && matrix_uses_declared_tools {
        return Ok(());
    }

    let message = "CI workflow must derive format and matrix Doctor selections from registry doctor_tools and skip empty selections";
    writeln!(writer, "{message}")?;
    Err(anyhow!(message))
}

/// Checks only explicit CI gate-driver invocations, leaving setup/control shell alone.
fn validate_ci_gate_invocations(
    config: &repo_config::RepoConfig,
    workflow: &Workflow,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for command in workflow
        .jobs
        .values()
        .flat_map(|job| job.steps.iter())
        .filter_map(|step| step.run.as_deref())
        .flat_map(str::lines)
        .map(str::trim)
        .filter(|line| !line.starts_with('#'))
    {
        if !command.contains("gate run --surface=ci") {
            continue;
        }
        let Some(selector) = command.split("--only=").nth(1) else {
            let message = format!(
                "CI workflow gate run invocation {command:?} must select exactly one matrix gate"
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        };
        let selector = selector.trim().trim_matches('"').trim_matches('\'');
        if selector.contains("${{") || selector.starts_with('$') {
            continue;
        }
        if config
            .gates
            .iter()
            .any(|gate| gate.id == selector && gate.surfaces.contains_key(&GateSurface::Ci))
        {
            continue;
        }
        let message =
            format!("CI workflow invokes undeclared CI gate selector {selector:?} via {command:?}");
        writeln!(writer, "{message}")?;
        return Err(anyhow!(message));
    }
    Ok(())
}

/// The small subset of GitHub Actions workflow YAML needed for CI derivation checks.
#[derive(Default, Deserialize)]
struct Workflow {
    /// All named workflow jobs.
    #[serde(default)]
    jobs: BTreeMap<String, WorkflowJob>,
}

/// A workflow job and the steps that can execute a command.
#[derive(Deserialize)]
struct WorkflowJob {
    /// Shell or action steps configured for this job.
    #[serde(default)]
    steps: Vec<WorkflowStep>,
    /// Jobs this job waits for before running.
    #[serde(default)]
    needs: WorkflowNeeds,
    /// Matrix strategy declarations for registry-derived jobs.
    #[serde(default)]
    strategy: WorkflowStrategy,
    /// Optional job execution condition.
    #[serde(rename = "if")]
    condition: Option<WorkflowCondition>,
}

/// The matrix portion of a GitHub Actions job strategy.
#[derive(Default, Deserialize)]
struct WorkflowStrategy {
    /// Named matrix dimensions and their expressions.
    #[serde(default)]
    matrix: BTreeMap<String, String>,
}

/// GitHub Actions accepts a single `needs` job or an array of job ids.
#[derive(Deserialize)]
#[serde(untagged)]
enum WorkflowNeeds {
    /// A single prerequisite job.
    One(String),
    /// Multiple prerequisite jobs.
    Many(Vec<String>),
}

impl Default for WorkflowNeeds {
    fn default() -> Self {
        Self::Many(Vec::new())
    }
}

impl WorkflowNeeds {
    /// Whether the dependency list includes one job id.
    fn contains(&self, expected: &str) -> bool {
        match self {
            Self::One(actual) => actual == expected,
            Self::Many(actual) => actual.iter().any(|job| job == expected),
        }
    }
}

/// A workflow step's optional shell command.
#[derive(Deserialize)]
struct WorkflowStep {
    /// Optional shell command, including YAML block scalars.
    #[serde(default)]
    run: Option<String>,
    /// Optional step execution condition.
    #[serde(rename = "if")]
    condition: Option<WorkflowCondition>,
}

/// A GitHub Actions execution condition expressed as a YAML boolean or string.
#[derive(Deserialize)]
#[serde(untagged)]
enum WorkflowCondition {
    /// A native YAML boolean condition.
    Boolean(bool),
    /// A GitHub Actions expression or string condition.
    String(String),
}

impl WorkflowCondition {
    /// Whether this condition is one of GitHub Actions' literal-falsy forms.
    fn is_literal_false(&self) -> bool {
        match self {
            Self::Boolean(value) => !value,
            Self::String(value) => {
                let trimmed = value.trim();
                let expression = trimmed
                    .strip_prefix("${{")
                    .and_then(|value| value.strip_suffix("}}"))
                    .unwrap_or(trimmed)
                    .trim();
                matches!(expression, "false" | "0" | "-0" | "''" | "\"\"" | "null")
            }
        }
    }
}

/// Validates that every hand-wired CI command has an aggregated workflow job.
///
/// # Errors
///
/// Returns an error when a hand-wired CI command is missing, its workflow job
/// is not a direct `quality-gate` dependency, or its diagnostic cannot be
/// written.
fn validate_hand_wired_ci_jobs(
    config: &repo_config::RepoConfig,
    workflow: &Workflow,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let hand_wired_ci_gates = config
        .gates
        .iter()
        .filter(|gate| {
            gate.wiring.as_ref() == Some(&GateWiring::HandWired)
                && gate.surfaces.contains_key(&GateSurface::Ci)
        })
        .collect::<Vec<_>>();
    if hand_wired_ci_gates.is_empty() {
        return Ok(());
    }

    let Some(quality_gate) = workflow.jobs.get("quality-gate") else {
        let message = "CI workflow pr-quality-gate.yml must declare a quality-gate job for hand-wired CI gates";
        writeln!(writer, "{message}")?;
        return Err(anyhow!(message));
    };

    for hand_wired_gate in hand_wired_ci_gates {
        let matching_jobs = workflow
            .jobs
            .iter()
            .filter_map(|(job_id, job)| {
                (!job
                    .condition
                    .as_ref()
                    .is_some_and(WorkflowCondition::is_literal_false)
                    && job.steps.iter().any(|step| {
                        !step
                            .condition
                            .as_ref()
                            .is_some_and(WorkflowCondition::is_literal_false)
                            && step.run.as_deref().is_some_and(|run| {
                                run_declares_command(run, &hand_wired_gate.command)
                            })
                    }))
                .then_some(job_id.as_str())
            })
            .collect::<Vec<_>>();
        if matching_jobs.is_empty() {
            let message = format!(
                "Hand-wired CI gate {:?} command {:?} is missing from pr-quality-gate.yml",
                hand_wired_gate.id, hand_wired_gate.command
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }

        let unaggregated_jobs = matching_jobs
            .iter()
            .copied()
            .filter(|job_id| !quality_gate.needs.contains(job_id))
            .collect::<Vec<_>>();
        if !unaggregated_jobs.is_empty() {
            let message = format!(
                "Hand-wired CI gate {:?} command {:?} maps to job(s) {} that must be direct quality-gate dependencies in pr-quality-gate.yml",
                hand_wired_gate.id,
                hand_wired_gate.command,
                unaggregated_jobs.join(", "),
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
}

/// Returns whether a shell command invokes the declared gate as an Nx target.
fn run_declares_command(run: &str, command: &str) -> bool {
    run.lines().any(|line| {
        let tokens = shell_tokens(line);
        !tokens
            .iter()
            .any(|token| matches!(token.as_str(), "&&" | "||" | ";" | "|"))
            && nx_targets(&tokens)
                .into_iter()
                .any(|target| target == command)
    })
}

/// Splits one shell command line, stopping at unquoted comments.
fn shell_tokens(line: &str) -> Vec<String> {
    let mut tokens = Vec::new();
    let mut token = String::new();
    let mut quote = None;
    let mut escaped = false;

    for character in line.chars() {
        if escaped {
            token.push(character);
            escaped = false;
            continue;
        }
        match quote {
            Some('\'') if character == '\'' => quote = None,
            Some('"') if character == '"' => quote = None,
            None if character == '#' => break,
            None if matches!(character, '\'' | '"') => quote = Some(character),
            Some('"') | None if character == '\\' => escaped = true,
            None if character.is_whitespace() => {
                if !token.is_empty() {
                    tokens.push(std::mem::take(&mut token));
                }
            }
            Some(_) | None => token.push(character),
        }
    }
    if !token.is_empty() {
        tokens.push(token);
    }
    tokens
}

/// Returns the declared targets of an executable `npx nx affected -t` command.
fn nx_targets(tokens: &[String]) -> Vec<&str> {
    let Some((executable, rest)) = tokens.split_first() else {
        return Vec::new();
    };
    if executable != "npx" {
        return Vec::new();
    }
    let Some((runner, arguments)) = rest.split_first() else {
        return Vec::new();
    };
    if runner != "nx" {
        return Vec::new();
    }
    if arguments
        .first()
        .is_none_or(|subcommand| subcommand != "affected")
    {
        return Vec::new();
    }
    let Some(target_index) = arguments
        .iter()
        .position(|argument| argument == "-t" || argument == "--targets")
    else {
        return Vec::new();
    };

    arguments[target_index + 1..]
        .iter()
        .take_while(|argument| {
            !argument.starts_with('-') && !matches!(argument.as_str(), "&&" | ";" | "|")
        })
        .flat_map(|argument| argument.split(','))
        .collect()
}

/// Validates that `package.json` contains the generated lint-staged block.
///
/// # Errors
///
/// Returns an error when `package.json` cannot be parsed, the generated block
/// differs, or the diagnostic cannot be written.
fn validate_lint_staged(
    repo_root: &Path,
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let package_path = repo_root.join("package.json");
    if let Ok(package_data) = std::fs::read(&package_path) {
        let package: serde_json::Value = serde_json::from_slice(&package_data)?;
        let committed = package.get("lint-staged").cloned().unwrap_or_default();
        let expected = serde_json::Value::Object(emit::lint_staged_from_config(config));
        if committed != expected {
            let message = "package.json lint-staged differs from the gate registry; run gate emit --surface=pre-commit";
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn composition_rule_violation() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: missing-ci\n",
            "    type: check\n",
            "    command: repo-config validate\n",
            "    kind: rhino-cli\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains("Gate Composition Rule")
            && rendered.contains("missing-ci")
            && rendered.contains("ci"),
        "a pre-commit check without ci and no carve-out must violate the Gate Composition Rule; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn pre_push_composition_rule_violation() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: missing-ci\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains("Gate Composition Rule")
            && rendered.contains("missing-ci")
            && rendered.contains("ci"),
        "a pre-push check without ci and no carve-out must violate the Gate Composition Rule; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn mutation_pre_commit_only_passes() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: format\n",
            "    type: mutation\n",
            "    command: prettier --write\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        ),
    )
    .unwrap();
    std::fs::create_dir(repo.path().join(".husky")).unwrap();
    std::fs::write(
        repo.path().join(".husky/pre-commit"),
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    )
    .unwrap();
    std::fs::set_permissions(
        repo.path().join(".husky/pre-commit"),
        std::fs::Permissions::from_mode(0o755),
    )
    .unwrap();

    assert!(
        run_at_root(repo.path(), &mut Vec::new()).is_ok(),
        "a pre-commit-only mutation is outside the check composition rule"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn staged_only_carve_out_exempts_pre_commit_check() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: index-guard\n",
            "    type: check\n",
            "    command: index validate\n",
            "    kind: rhino-cli\n",
            "    carve-out: staged-only\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
        ),
    )
    .unwrap();
    std::fs::create_dir(repo.path().join(".husky")).unwrap();
    std::fs::write(
        repo.path().join(".husky/pre-commit"),
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    )
    .unwrap();
    std::fs::set_permissions(
        repo.path().join(".husky/pre-commit"),
        std::fs::Permissions::from_mode(0o755),
    )
    .unwrap();

    assert!(
        run_at_root(repo.path(), &mut Vec::new()).is_ok(),
        "the staged-only carve-out exempts this pre-commit-only check"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn missing_surface_shim() {
    let repo = tempfile::TempDir::new().unwrap();
    let husky = repo.path().join(".husky");
    std::fs::create_dir(&husky).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: pre-push-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      pre-push: { scope: affected-projects }\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(husky.join("pre-push"), "#!/bin/sh\necho stale hook\n").unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err() && rendered.contains(".husky/pre-push") && rendered.contains("pre-push"),
        "a declared pre-push surface without its registry shim must name the surface file; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn missing_pre_commit_surface_shim() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: pre-commit-check\n",
            "    type: check\n",
            "    command: md naming validate\n",
            "    kind: rhino-cli\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
            "      ci: { scope: all-file-type }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains(".husky/pre-commit")
            && rendered.contains("pre-commit"),
        "a declared pre-commit surface without its registry shim must name the surface file; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn commented_surface_shim_is_not_a_registry_delegation() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::create_dir(repo.path().join(".husky")).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: pre-commit-check\n",
            "    type: check\n",
            "    command: md naming validate\n",
            "    kind: rhino-cli\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
            "      ci: { scope: all-file-type }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        repo.path().join(".husky/pre-commit"),
        "#!/bin/sh\n# rhino-cli gate run --surface=pre-commit\n",
    )
    .unwrap();

    let result = run_at_root(repo.path(), &mut Vec::new());

    assert!(
        result.is_err(),
        "a commented-out registry invocation must not validate a hook shim"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn legacy_non_executable_commit_msg_shim_is_rejected() {
    use std::os::unix::fs::PermissionsExt;

    let repo = tempfile::TempDir::new().unwrap();
    let husky = repo.path().join(".husky");
    std::fs::create_dir(&husky).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: commitlint\n",
            "    type: check\n",
            "    command: commitlint --edit\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      commit-msg: { scope: other }\n",
            "  - id: pre-commit-mutation\n",
            "    type: mutation\n",
            "    command: prettier --write\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-commit: { scope: other }\n",
            "  - id: pre-push-mutation\n",
            "    type: mutation\n",
            "    command: verify\n",
            "    kind: external\n",
            "    surfaces:\n",
            "      pre-push: { scope: other }\n",
        ),
    )
    .unwrap();
    for (hook, invocation) in [("pre-commit", "pre-commit"), ("pre-push", "pre-push")] {
        let hook_path = husky.join(hook);
        std::fs::write(
            &hook_path,
            format!("#!/bin/sh\nrhino-cli gate run --surface={invocation}\n"),
        )
        .unwrap();
        std::fs::set_permissions(&hook_path, std::fs::Permissions::from_mode(0o755)).unwrap();
    }
    let commit_msg = husky.join("commit-msg");
    std::fs::write(
        &commit_msg,
        "#!/bin/sh\nnpx --no -- commitlint --edit \"$1\"\n",
    )
    .unwrap();
    std::fs::set_permissions(&commit_msg, std::fs::Permissions::from_mode(0o644)).unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains(".husky/commit-msg")
            && rendered.contains("gate run --surface=commit-msg"),
        "a legacy, non-executable commit-msg hook must not validate when pre-commit and pre-push delegate correctly; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn every_declared_hook_shim_must_be_executable() {
    use std::os::unix::fs::PermissionsExt;

    for hook_without_executable_mode in ["commit-msg", "pre-commit", "pre-push"] {
        let repo = tempfile::TempDir::new().unwrap();
        let husky = repo.path().join(".husky");
        std::fs::create_dir(&husky).unwrap();
        std::fs::write(
            repo.path().join("repo-config.yml"),
            concat!(
                "gates:\n",
                "  - id: commitlint\n",
                "    type: check\n",
                "    command: commitlint --edit\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      commit-msg: { scope: other }\n",
                "  - id: pre-commit-mutation\n",
                "    type: mutation\n",
                "    command: prettier --write\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      pre-commit: { scope: other }\n",
                "  - id: pre-push-mutation\n",
                "    type: mutation\n",
                "    command: verify\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      pre-push: { scope: other }\n",
            ),
        )
        .unwrap();
        for hook in ["commit-msg", "pre-commit", "pre-push"] {
            let hook_path = husky.join(hook);
            std::fs::write(
                &hook_path,
                format!("#!/bin/sh\nrhino-cli gate run --surface={hook}\n"),
            )
            .unwrap();
            let mode = if hook == hook_without_executable_mode {
                0o644
            } else {
                0o755
            };
            std::fs::set_permissions(&hook_path, std::fs::Permissions::from_mode(mode)).unwrap();
        }

        let mut output = Vec::new();
        let result = run_at_root(repo.path(), &mut output);
        let rendered = String::from_utf8_lossy(&output);
        assert!(
            result.is_err() && rendered.contains(&format!(".husky/{hook_without_executable_mode}")),
            "a non-executable {hook_without_executable_mode} hook must fail validation; \
             result_ok={}, output={rendered:?}",
            result.is_ok()
        );
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn formatter_requires_exactly_one_verifying_check() {
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
            "    surfaces:\n",
            "      ci: { scope: all-file-type }\n",
            "  - id: verify-format-one\n",
            "    type: check\n",
            "    command: prettier --check\n",
            "    kind: external\n",
            "    verifies: format-markdown\n",
            "    surfaces:\n",
            "      ci: { scope: all-file-type }\n",
            "  - id: verify-format-two\n",
            "    type: check\n",
            "    command: prettier --check\n",
            "    kind: external\n",
            "    verifies: format-markdown\n",
            "    surfaces:\n",
            "      ci: { scope: all-file-type }\n",
        ),
    )
    .unwrap();

    let result = run_at_root(repo.path(), &mut Vec::new());

    assert!(
        result.is_err(),
        "a formatter must not accept multiple verifying checks"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn matrix_ci_dispatcher_is_accepted_when_derived_from_gate_list() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: declared-ci-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "jobs:\n",
            "  enumerate:\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json\n",
            "  gate:\n",
            "    needs: enumerate\n",
            "    strategy:\n",
            "      matrix:\n",
            "        gate: ${{ fromJson(needs.enumerate.outputs.gates) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --only=${{ matrix.gate.id }}\n",
            "  quality-gate:\n",
            "    needs: [enumerate, gate]\n",
        ),
    )
    .unwrap();

    assert!(
        run_at_root(repo.path(), &mut Vec::new()).is_ok(),
        "the registry-derived CI matrix dispatcher must validate"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn quality_gate_requires_enumerate_as_well_as_gate() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: declared-ci-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "jobs:\n",
            "  enumerate:\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json\n",
            "  gate:\n",
            "    needs: enumerate\n",
            "    strategy:\n",
            "      matrix:\n",
            "        gate: ${{ fromJson(needs.enumerate.outputs.gates) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --only=${{ matrix.gate.id }}\n",
            "  quality-gate:\n",
            "    needs: gate\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);

    assert!(
        result.is_err() && rendered.contains("enumerate") && rendered.contains("quality-gate"),
        "quality-gate must directly depend on enumerate and gate; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn cargo_prefixed_matrix_dispatcher_ignores_ci_setup_shell() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: declared-ci-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "jobs:\n",
            "  enumerate:\n",
            "    steps:\n",
            "      - run: echo setup complete\n",
            "      - run: cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate list --surface=ci --format=json\n",
            "  gate:\n",
            "    needs: enumerate\n",
            "    strategy:\n",
            "      matrix:\n",
            "        gate: ${{ fromJson(needs.enumerate.outputs.gates) }}\n",
            "    steps:\n",
            "      - run: cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate run --surface=ci --only=${{ matrix.gate.id }}\n",
            "  quality-gate:\n",
            "    needs: [enumerate, gate]\n",
        ),
    )
    .unwrap();

    assert!(
        run_at_root(repo.path(), &mut Vec::new()).is_ok(),
        "ordinary setup shell plus a Cargo-prefixed registry matrix must validate"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn missing_named_ci_matrix_job_is_rejected() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: declared-ci-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "jobs:\n",
            "  enumerate:\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json\n",
            "      - run: echo '${{ fromJson(needs.enumerate.outputs.gates) }}'\n",
            "  quality-gate:\n",
            "    needs: [enumerate, gate]\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err() && rendered.contains("matrix"),
        "a CI registry gate requires the named matrix dispatcher; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn undeclared_ci_command() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: declared-ci-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "name: PR quality gate\n",
            "jobs:\n",
            "  enumerate:\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json\n",
            "  gate:\n",
            "    needs: enumerate\n",
            "    strategy:\n",
            "      matrix:\n",
            "        gate: ${{ fromJson(needs.enumerate.outputs.gates) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --only=${{ matrix.gate.id }}\n",
            "  quality-gate:\n",
            "    needs: [enumerate, gate]\n",
            "  unexpected:\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --only=unregistered-check\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err() && rendered.contains("unregistered-check"),
        "an explicit CI gate invocation absent from the registry must name the undeclared selector; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn named_block_ci_step_is_checked_against_the_registry() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: declared-ci-check\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "jobs:\n",
            "  enumerate:\n",
            "    steps:\n",
            "      - run: rhino-cli gate list --surface=ci --format=json\n",
            "  gate:\n",
            "    needs: enumerate\n",
            "    strategy:\n",
            "      matrix:\n",
            "        gate: ${{ fromJson(needs.enumerate.outputs.gates) }}\n",
            "    steps:\n",
            "      - run: rhino-cli gate run --surface=ci --only=${{ matrix.gate.id }}\n",
            "  quality-gate:\n",
            "    needs: [enumerate, gate]\n",
            "  unexpected:\n",
            "    steps:\n",
            "      - name: undeclared block gate invocation\n",
            "        run: |\n",
            "          cargo run --release --quiet --manifest-path apps/rhino-cli/Cargo.toml -- gate run --surface=ci --only=unregistered-check\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err() && rendered.contains("unregistered-check"),
        "a named block CI step must not bypass explicit registry gate validation; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn orphan_verifies_reference() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: verify-format\n",
            "    type: check\n",
            "    command: prettier --check\n",
            "    kind: external\n",
            "    verifies: missing-format\n",
            "    surfaces:\n",
            "      ci: { scope: affected-file-type, glob: '*.md' }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains("verify-format")
            && rendered.contains("missing-format"),
        "an orphan verifies reference must name the referring gate and missing gate; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn stale_lint_staged_block() {
    use std::os::unix::fs::PermissionsExt;

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
        r#"{"lint-staged":{"*.md":"prettier --check"}}"#,
    )
    .unwrap();
    std::fs::create_dir(repo.path().join(".husky")).unwrap();
    std::fs::write(
        repo.path().join(".husky/pre-commit"),
        "#!/bin/sh\nrhino-cli gate run --surface=pre-commit\n",
    )
    .unwrap();
    std::fs::set_permissions(
        repo.path().join(".husky/pre-commit"),
        std::fs::Permissions::from_mode(0o755),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains("package.json")
            && rendered.contains("gate emit --surface=pre-commit"),
        "a stale lint-staged block must name package.json and its registry regeneration command; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn unverified_formatter() {
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
            "    surfaces:\n",
            "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err() && rendered.contains("format-markdown") && rendered.contains("verifies"),
        "a formatter mutation without a verifies-linked check must name the formatter; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn hand_wired_present() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: test-quick\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    wiring: hand-wired\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(
        workflows.join("pr-quality-gate.yml"),
        concat!(
            "jobs:\n",
            "  test-quick:\n",
            "    steps:\n",
            "      - run: npx nx affected -t test:quick\n",
            "  quality-gate:\n",
            "    needs: [test-quick]\n",
        ),
    )
    .unwrap();

    assert!(
        run_at_root(repo.path(), &mut Vec::new()).is_ok(),
        "a hand-wired CI gate with its matching workflow job must validate"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn hand_wired_gate_requires_a_quality_gate_dependency() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();
    let workflow: Workflow = serde_norway::from_str(concat!(
        "jobs:\n",
        "  detached:\n",
        "    steps:\n",
        "      - run: npx nx affected -t test:quick\n",
        "  quality-gate:\n",
        "    needs: []\n",
    ))
    .unwrap();

    let mut output = Vec::new();
    let result = validate_hand_wired_ci_jobs(&config, &workflow, &mut output);
    let rendered = String::from_utf8_lossy(&output);

    assert!(
        result.is_err()
            && rendered.contains("test-quick")
            && rendered.contains("detached")
            && rendered.contains("quality-gate"),
        "a hand-wired command in an unaggregated job must fail; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn commented_hand_wired_command_is_rejected() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();
    let workflow: Workflow = serde_norway::from_str(concat!(
        "jobs:\n",
        "  test-quick:\n",
        "    steps:\n",
        "      - run: '# npx nx affected -t test:quick'\n",
        "  quality-gate:\n",
        "    needs: [test-quick]\n",
    ))
    .unwrap();

    assert!(
        validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err(),
        "a commented hand-wired command must not satisfy the CI workflow contract"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn disabled_hand_wired_command_is_rejected() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();

    for workflow_source in [
        concat!(
            "jobs:\n",
            "  test-quick:\n",
            "    if: false\n",
            "    steps:\n",
            "      - run: npx nx affected -t test:quick\n",
            "  quality-gate:\n",
            "    needs: [test-quick]\n",
        ),
        concat!(
            "jobs:\n",
            "  test-quick:\n",
            "    steps:\n",
            "      - if: false\n",
            "        run: npx nx affected -t test:quick\n",
            "  quality-gate:\n",
            "    needs: [test-quick]\n",
        ),
    ] {
        let workflow: Workflow = serde_norway::from_str(workflow_source).unwrap();
        assert!(
            validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err(),
            "a literal false job or step guard must not satisfy the hand-wired CI contract"
        );
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn inline_comment_or_quoted_hand_wired_command_is_rejected() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();

    let results = [
        ": # npx nx affected -t test:quick",
        "echo 'npx nx affected -t test:quick'",
    ]
    .into_iter()
    .map(|run| {
        let workflow_source = format!(
            "jobs:\n  test-quick:\n    steps:\n      - run: \"{run}\"\n  quality-gate:\n    needs: [test-quick]\n"
        );
        let workflow: Workflow = serde_norway::from_str(&workflow_source).unwrap();
        validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err()
    })
    .collect::<Vec<_>>();
    assert!(
        results.iter().all(|result| *result),
        "inline comments and quoted commands must not satisfy the hand-wired CI contract: {results:?}"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn unspaced_false_expression_hand_wired_guards_are_rejected() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();

    let mut results = Vec::new();
    for condition in ["${{ false }}", "${{false}}"] {
        for workflow_source in [
            format!(
                "jobs:\n  test-quick:\n    if: '{condition}'\n    steps:\n      - run: npx nx affected -t test:quick\n  quality-gate:\n    needs: [test-quick]\n"
            ),
            format!(
                "jobs:\n  test-quick:\n    steps:\n      - if: '{condition}'\n        run: npx nx affected -t test:quick\n  quality-gate:\n    needs: [test-quick]\n"
            ),
        ] {
            let workflow: Workflow = serde_norway::from_str(&workflow_source).unwrap();
            results.push(validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err());
        }
    }
    assert!(
        results.iter().all(|result| *result),
        "literal false job and step expressions must not satisfy the hand-wired CI contract: {results:?}"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn falsey_expression_hand_wired_guards_are_rejected() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();

    let mut results = Vec::new();
    for condition in [
        "${{ 0 }}",
        "${{ -0 }}",
        "${{ '' }}",
        "${{ \"\" }}",
        "${{ null }}",
    ] {
        for workflow_source in [
            format!(
                "jobs:\n  test-quick:\n    if: |-\n      {condition}\n    steps:\n      - run: npx nx affected -t test:quick\n  quality-gate:\n    needs: [test-quick]\n"
            ),
            format!(
                "jobs:\n  test-quick:\n    steps:\n      - if: |-\n          {condition}\n        run: npx nx affected -t test:quick\n  quality-gate:\n    needs: [test-quick]\n"
            ),
        ] {
            let workflow: Workflow = serde_norway::from_str(&workflow_source).unwrap();
            results.push(validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err());
        }
    }
    assert!(
        results.iter().all(|result| *result),
        "literal falsey job and step expressions must not satisfy the hand-wired CI contract: {results:?}"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn non_executing_nx_subcommands_do_not_satisfy_hand_wired_gates() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();

    let results = [
        "npx nx report -t test:quick",
        "npx nx show projects -t test:quick",
    ]
    .into_iter()
    .map(|run| {
        let workflow_source = format!(
            "jobs:\n  test-quick:\n    steps:\n      - run: \"{run}\"\n  quality-gate:\n    needs: [test-quick]\n"
        );
        let workflow: Workflow = serde_norway::from_str(&workflow_source).unwrap();
        validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err()
    })
    .collect::<Vec<_>>();
    assert!(
        results.iter().all(|result| *result),
        "non-executing Nx subcommands must not satisfy the hand-wired CI contract: {results:?}"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn error_masked_hand_wired_command_is_rejected() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: test-quick\n",
        "    type: check\n",
        "    command: test:quick\n",
        "    kind: nx\n",
        "    wiring: hand-wired\n",
        "    surfaces:\n",
        "      ci: { scope: affected-projects }\n",
    ))
    .unwrap();
    let results = ["||", "&&", ";", "|"]
        .into_iter()
        .map(|operator| {
            let workflow_source = format!(
                "jobs:\n  test-quick:\n    steps:\n      - run: npx nx affected -t test:quick {operator} true\n  quality-gate:\n    needs: [test-quick]\n"
            );
            let workflow: Workflow = serde_norway::from_str(&workflow_source).unwrap();
            validate_hand_wired_ci_jobs(&config, &workflow, &mut Vec::new()).is_err()
        })
        .collect::<Vec<_>>();
    assert!(
        results.iter().all(|result| *result),
        "compound Nx commands must not satisfy the hand-wired CI contract: {results:?}"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn hand_wired_job_deleted() {
    let repo = tempfile::TempDir::new().unwrap();
    let workflows = repo.path().join(".github/workflows");
    std::fs::create_dir_all(&workflows).unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: test-quick\n",
            "    type: check\n",
            "    command: test:quick\n",
            "    kind: nx\n",
            "    wiring: hand-wired\n",
            "    surfaces:\n",
            "      ci: { scope: affected-projects }\n",
        ),
    )
    .unwrap();
    std::fs::write(workflows.join("pr-quality-gate.yml"), "jobs: {}\n").unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err()
            && rendered.contains("test-quick")
            && rendered.contains("pr-quality-gate.yml"),
        "a deleted hand-wired job must name its gate id and CI workflow file; \
         result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn doctor_tool_metadata_rejects_an_unconditional_ci_bootstrap() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: shellcheck\n",
        "    type: check\n",
        "    command: shellcheck\n",
        "    kind: external\n",
        "    doctor-tools: [shellcheck]\n",
        "    surfaces:\n",
        "      ci: { scope: all-file-type }\n",
    ))
    .unwrap();
    let workflow: Workflow = serde_norway::from_str(concat!(
        "jobs:\n",
        "  format:\n",
        "    steps:\n",
        "      - run: npm run doctor -- --fix\n",
    ))
    .unwrap();

    let mut output = Vec::new();
    let result = validate_ci_doctor_bootstrap(&config, &workflow, &mut output);
    let rendered = String::from_utf8_lossy(&output);

    assert!(
        result.is_err() && rendered.contains("unconditional full Doctor bootstrap"),
        "unscoped Doctor setup must fail; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn doctor_tool_metadata_requires_registry_derived_format_and_matrix_selection() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: shellcheck\n",
        "    type: check\n",
        "    command: shellcheck\n",
        "    kind: external\n",
        "    doctor-tools: [shellcheck]\n",
        "    surfaces:\n",
        "      ci: { scope: all-file-type }\n",
    ))
    .unwrap();
    let workflow: Workflow = serde_norway::from_str(concat!(
        "jobs:\n",
        "  format:\n",
        "    steps:\n",
        "      - run: |\n",
        "          tools=$(rhino-cli gate list --surface=pre-commit --format=json | jq -r '[.[] | .doctor_tools[]] | unique | join(\",\")')\n",
        "          if [ -n \"$tools\" ]; then\n",
        "            npm run doctor -- --fix --tools \"$tools\"\n",
        "          fi\n",
        "  gate:\n",
        "    steps:\n",
        "      - run: |\n",
        "          tools=\"${{ join(matrix.gate.doctor_tools, ',') }}\"\n",
        "          if [ -n \"$tools\" ]; then\n",
        "            npm run doctor -- --fix --tools \"$tools\"\n",
        "          fi\n",
    ))
    .unwrap();

    assert!(
        validate_ci_doctor_bootstrap(&config, &workflow, &mut Vec::new()).is_ok(),
        "registry-derived Doctor selections must validate"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn doctor_tool_metadata_rejects_formatter_only_format_selection() {
    let config: repo_config::RepoConfig = serde_norway::from_str(concat!(
        "gates:\n",
        "  - id: format-shfmt\n",
        "    type: mutation\n",
        "    command: shfmt\n",
        "    kind: external\n",
        "    category: formatter\n",
        "    doctor-tools: [shfmt]\n",
        "    surfaces:\n",
        "      pre-commit: { scope: all-file-type }\n",
        "  - id: shellcheck\n",
        "    type: check\n",
        "    command: shellcheck\n",
        "    kind: external\n",
        "    doctor-tools: [shellcheck]\n",
        "    surfaces:\n",
        "      pre-commit: { scope: all-file-type }\n",
        "      ci: { scope: all-file-type }\n",
    ))
    .unwrap();
    let workflow: Workflow = serde_norway::from_str(concat!(
        "jobs:\n",
        "  format:\n",
        "    steps:\n",
        "      - run: |\n",
        "          tools=$(rhino-cli gate list --surface=pre-commit --format=json | jq -r '[.[] | select(.type == \"mutation\" and .category == \"formatter\") | .doctor_tools[]] | unique | join(\",\")')\n",
        "          if [ -n \"$tools\" ]; then\n",
        "            npm run doctor -- --fix --tools \"$tools\"\n",
        "          fi\n",
        "  gate:\n",
        "    steps:\n",
        "      - run: |\n",
        "          tools=\"${{ join(matrix.gate.doctor_tools, ',') }}\"\n",
        "          if [ -n \"$tools\" ]; then\n",
        "            npm run doctor -- --fix --tools \"$tools\"\n",
        "          fi\n",
    ))
    .unwrap();

    let mut output = Vec::new();
    let result = validate_ci_doctor_bootstrap(&config, &workflow, &mut output);
    let rendered = String::from_utf8_lossy(&output);

    assert!(
        result.is_err() && rendered.contains("format and matrix Doctor selections"),
        "formatter-only format setup must fail; result_ok={}, output={rendered:?}",
        result.is_ok()
    );
}
