//! `gate validate` command adapter.

use std::io::Write;
use std::path::Path;

use anyhow::{Error, anyhow};
use clap::Args;

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
/// declared for pre-commit is missing its CI declaration.
pub fn run_at_root(repo_root: &Path, writer: &mut dyn Write) -> Result<(), Error> {
    let config = repo_config::load(repo_root)?;

    validate_pre_commit_composition(&config, writer)?;
    validate_verifies_references(&config, writer)?;
    validate_formatter_verification(&config, writer)?;
    validate_pre_push_shim(repo_root, &config, writer)?;
    validate_ci_workflow(repo_root, &config, writer)?;
    validate_lint_staged(repo_root, &config, writer)
}

/// Validates the pre-commit check-to-CI composition rule.
///
/// # Errors
///
/// Returns an error when a check gate declares pre-commit without CI and lacks
/// the `staged-only` carve-out, or when the diagnostic cannot be written.
fn validate_pre_commit_composition(
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for gate in &config.gates {
        let is_pre_commit_check_without_ci = gate.gate_type == GateType::Check
            && gate.surfaces.contains_key(&GateSurface::PreCommit)
            && !gate.surfaces.contains_key(&GateSurface::Ci)
            && gate.carve_out.as_ref() != Some(&GateCarveOut::StagedOnly);
        if is_pre_commit_check_without_ci {
            let message = format!(
                "Gate Composition Rule violation: gate {:?} declares pre-commit but is missing ci",
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
        if let Some(verified_gate) = &gate.verifies
            && !config
                .gates
                .iter()
                .any(|candidate| candidate.id == *verified_gate)
        {
            let message = format!(
                "Gate {:?} verifies orphan gate {:?}",
                gate.id, verified_gate
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
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
        let has_verifying_check = config.gates.iter().any(|gate| {
            gate.gate_type == GateType::Check
                && gate.verifies.as_deref() == Some(formatter.id.as_str())
        });
        if !has_verifying_check {
            let message = format!(
                "Formatter mutation {:?} requires a check gate whose verifies field names it",
                formatter.id
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
}

/// Validates the generated Husky shim required by pre-push gates.
///
/// # Errors
///
/// Returns an error when the required registry invocation is absent or the
/// diagnostic cannot be written.
fn validate_pre_push_shim(
    repo_root: &Path,
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    if config
        .gates
        .iter()
        .any(|gate| gate.surfaces.contains_key(&GateSurface::PrePush))
    {
        let shim = repo_root.join(".husky/pre-push");
        let has_registry_invocation = std::fs::read_to_string(&shim)
            .is_ok_and(|contents| contents.contains("gate run --surface=pre-push"));
        if !has_registry_invocation {
            let message =
                "Gate surface shim .husky/pre-push must invoke gate run --surface=pre-push";
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
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
    let workflow_jobs = workflow_jobs(repo_root, config, writer)?;
    validate_hand_wired_ci_jobs(config, &workflow_jobs, writer)
}

/// Collects CI workflow job names after checking registry-backed commands.
///
/// # Errors
///
/// Returns an error when the workflow declares a command absent from the gate
/// registry or its diagnostic cannot be written.
fn workflow_jobs(
    repo_root: &Path,
    config: &repo_config::RepoConfig,
    writer: &mut dyn Write,
) -> Result<Vec<String>, Error> {
    let pr_workflow = repo_root.join(".github/workflows/pr-quality-gate.yml");
    let mut workflow_jobs = Vec::new();
    if let Ok(workflow) = std::fs::read_to_string(&pr_workflow) {
        let mut current_job = None;
        for line in workflow.lines() {
            if let Some(job) = line
                .strip_prefix("  ")
                .and_then(|candidate| candidate.strip_suffix(':'))
                .filter(|candidate| !candidate.starts_with(' '))
            {
                current_job = Some(job);
                workflow_jobs.push(job.to_owned());
                continue;
            }
            let Some(command) = line.trim().strip_prefix("- run: ") else {
                continue;
            };
            let is_declared_command = config.gates.iter().any(|gate| gate.command == command);
            let is_hand_wired_job = current_job.is_some_and(|job| {
                config.gates.iter().any(|gate| {
                    gate.id == job
                        && gate.wiring.as_ref() == Some(&GateWiring::HandWired)
                        && gate.surfaces.contains_key(&GateSurface::Ci)
                })
            });
            if !is_declared_command && !is_hand_wired_job {
                let message = format!(
                    "CI workflow pr-quality-gate.yml declares command {command:?} absent from the gate registry"
                );
                writeln!(writer, "{message}")?;
                return Err(anyhow!(message));
            }
        }
    }
    Ok(workflow_jobs)
}

/// Validates that every hand-wired CI gate has a workflow job of the same id.
///
/// # Errors
///
/// Returns an error when a hand-wired CI gate is missing or its diagnostic
/// cannot be written.
fn validate_hand_wired_ci_jobs(
    config: &repo_config::RepoConfig,
    workflow_jobs: &[String],
    writer: &mut dyn Write,
) -> Result<(), Error> {
    for hand_wired_gate in config.gates.iter().filter(|gate| {
        gate.wiring.as_ref() == Some(&GateWiring::HandWired)
            && gate.surfaces.contains_key(&GateSurface::Ci)
    }) {
        if !workflow_jobs.iter().any(|job| job == &hand_wired_gate.id) {
            let message = format!(
                "Hand-wired CI gate {:?} is missing from pr-quality-gate.yml",
                hand_wired_gate.id
            );
            writeln!(writer, "{message}")?;
            return Err(anyhow!(message));
        }
    }
    Ok(())
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
fn mutation_pre_commit_only_passes() {
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

    assert!(
        run_at_root(repo.path(), &mut Vec::new()).is_ok(),
        "a pre-commit-only mutation is outside the check composition rule"
    );
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn staged_only_carve_out_exempts_pre_commit_check() {
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
            "  quality:\n",
            "    steps:\n",
            "      - run: npm run unregistered-check\n",
        ),
    )
    .unwrap();

    let mut output = Vec::new();
    let result = run_at_root(repo.path(), &mut output);
    let rendered = String::from_utf8_lossy(&output);
    assert!(
        result.is_err() && rendered.contains("npm run unregistered-check"),
        "a hard-coded CI check absent from the registry must name the undeclared command; \
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
