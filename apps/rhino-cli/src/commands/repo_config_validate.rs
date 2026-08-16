//! `repo-config validate` — schema-parity gate for `repo-config.yml`.
//!
//! Strict-deserializes `repo-config.yml` against the canonical
//! [`RepoConfig`](crate::application::repo_config::RepoConfig) schema
//! (`#[serde(deny_unknown_fields)]`), then applies semantic checks:
//! required-non-empty on `harness` and `coverage.projects`, and enum checks on
//! `harness[].tier` and `coverage.projects[].levels`. Every failure names the
//! offending key and its path.
//!
//! Because the parsing struct is byte-identical source across ose-public and
//! ose-private, each repo validating its own `repo-config.yml` against its own
//! copy of that struct is equivalent to both files carrying an identical key set
//! (values may differ).

use std::collections::HashSet;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::repo_config::{
    self, DOCTOR_TOOL_INVENTORY, GateEntry, GateKind, GateSurface, GateType, RepoConfig, ScopeKind,
    SurfaceScope, validate_repo_relative_path,
};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Accepted values for `harness[].tier`.
const VALID_TIERS: &[&str] = &["source", "generated", "source-config", "native"];

/// Accepted values for `coverage.projects[].levels[]`.
const VALID_LEVELS: &[&str] = &["unit", "integration", "e2e"];

/// CLI arguments for `repo-config validate` (none required).
#[derive(Args, Debug)]
pub struct ValidateArgs {}

/// Run the `repo-config validate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, `repo-config.yml` cannot be
/// strict-deserialized, or any semantic check fails.
pub fn run(_args: &ValidateArgs, _output: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    run_at_root(&repo_root, &mut std::io::stdout())
}

/// Run `repo-config validate` from a known `repo_root` (testable entry point).
///
/// # Errors
///
/// Returns an error when `repo-config.yml` fails strict deserialization or any
/// semantic check produces a finding.
pub fn run_at_root(
    repo_root: &std::path::Path,
    w: &mut dyn std::io::Write,
) -> std::result::Result<(), Error> {
    // Strict deserialize (deny_unknown_fields): an unknown or misspelled key here
    // is reported by serde with the offending key named.
    let config = repo_config::load(repo_root).map_err(|e| {
        anyhow!("repo-config validate: repo-config.yml failed strict schema deserialization: {e:#}")
    })?;

    let mut findings = semantic_findings(&config);
    if let Some(path) = &config.doctor.dotnet_global_json
        && let Err(error) = repo_config::confined_repo_path(repo_root, path)
    {
        findings.push(format!(
            "doctor.dotnet-global-json: invalid value {path:?} ({error:#})"
        ));
    }

    if findings.is_empty() {
        writeln!(
            w,
            "repo-config validate: repo-config.yml matches the canonical schema (key set + enums OK)"
        )?;
        return Ok(());
    }

    for f in &findings {
        writeln!(w, "{f}")?;
    }
    Err(anyhow!(
        "repo-config validate: {} schema finding(s); fix the key(s) listed above",
        findings.len()
    ))
}

/// Collect semantic findings (required-non-empty + enum checks) for `config`.
///
/// Each finding names the offending key and its path.
pub(crate) fn semantic_findings(config: &RepoConfig) -> Vec<String> {
    let mut findings = Vec::new();

    if config.harness.is_empty() {
        findings.push(
            "harness: required key is missing or empty (expected at least one harness entry)"
                .to_string(),
        );
    }
    if config.coverage.projects.is_empty() {
        findings.push(
            "coverage.projects: required key is missing or empty \
             (expected at least one project entry)"
                .to_string(),
        );
    }

    for (i, entry) in config.harness.iter().enumerate() {
        if !VALID_TIERS.contains(&entry.tier.as_str()) {
            findings.push(format!(
                "harness[{i}].tier: invalid value {:?} (expected one of {})",
                entry.tier,
                VALID_TIERS.join(" | ")
            ));
        }
    }

    for (i, project) in config.coverage.projects.iter().enumerate() {
        for level in &project.levels {
            if !VALID_LEVELS.contains(&level.as_str()) {
                findings.push(format!(
                    "coverage.projects[{i}].levels: invalid value {:?} (expected one of {})",
                    level,
                    VALID_LEVELS.join(" | ")
                ));
            }
        }
    }

    if let Some(path) = &config.doctor.dotnet_global_json
        && let Err(error) = validate_repo_relative_path(path)
    {
        findings.push(format!(
            "doctor.dotnet-global-json: invalid value {path:?} ({error})"
        ));
    }

    findings.extend(gate_semantic_findings(config));

    findings
}

/// Collect semantic findings that apply specifically to the gate registry.
///
/// This is shared by `repo-config validate` and `gate run`, so dispatch rejects
/// malformed registry entries before it selects or invokes a leaf.
pub(crate) fn gate_semantic_findings(config: &RepoConfig) -> Vec<String> {
    let mut findings = Vec::new();
    let mut gate_ids = HashSet::new();
    for (i, gate) in config.gates.iter().enumerate() {
        if !gate_ids.insert(gate.id.as_str()) {
            findings.push(format!("gates[{i}].id: duplicate gate id {:?}", gate.id));
        }
        if gate.id.is_empty()
            || !gate
                .id
                .bytes()
                .all(|b| b.is_ascii_lowercase() || b.is_ascii_digit() || b == b'-')
        {
            findings.push(format!(
                "gates[{i}].id: {:?} must be non-empty lowercase kebab-case (`[a-z0-9-]+`) — \
                 this value reaches shell contexts (CI matrix dispatch, hook generation) \
                 unescaped, so any other character is a defense-in-depth risk, not merely a \
                 style violation",
                gate.id
            ));
        }
        if gate.surfaces.is_empty() {
            findings.push(format!(
                "gates[{i}] (gate id {:?}).surfaces: at least one surface is required",
                gate.id
            ));
        }
        if gate.wiring.is_some() && gate.gate_type != GateType::Check {
            findings.push(format!(
                "gates[{i}] (gate id {:?}).wiring: only valid for type \"check\" (found type \"mutation\")",
                gate.id
            ));
        }
        if gate.restages && gate.gate_type != GateType::Mutation {
            findings.push(format!(
                "gates[{i}] (gate id {:?}).restages: only valid for type \"mutation\" (found type \"check\")",
                gate.id
            ));
        }
        if gate.carve_out.is_some() && gate.gate_type != GateType::Check {
            findings.push(format!(
                "gates[{i}] (gate id {:?}).carve-out: only valid for type \"check\" (found type \"mutation\")",
                gate.id
            ));
        }
        findings.extend(doctor_tools_semantic_findings(i, gate));
        for (surface, scope) in &gate.surfaces {
            findings.extend(gate_surface_semantic_findings(i, gate, surface, scope));
        }
    }

    findings
}

/// Collect semantic findings for a gate's optional ordered Doctor-tool list.
fn doctor_tools_semantic_findings(index: usize, gate: &GateEntry) -> Vec<String> {
    let mut findings = Vec::new();
    let mut declared = HashSet::new();

    for tool in &gate.doctor_tools {
        if !DOCTOR_TOOL_INVENTORY.contains(&tool.as_str()) {
            findings.push(format!(
                "gates[{index}] (gate id {:?}).doctor-tools: unknown Doctor tool {:?}",
                gate.id, tool
            ));
        }
        if !declared.insert(tool.as_str()) {
            findings.push(format!(
                "gates[{index}] (gate id {:?}).doctor-tools: duplicate Doctor tool {:?}",
                gate.id, tool
            ));
        }
    }

    findings
}

/// Collect semantic findings for one gate on one declared surface.
fn gate_surface_semantic_findings(
    index: usize,
    gate: &GateEntry,
    surface: &GateSurface,
    scope: &SurfaceScope,
) -> Vec<String> {
    let mut findings = Vec::new();
    let is_file_scope = matches!(
        scope.scope,
        ScopeKind::AffectedFileType | ScopeKind::AllFileType
    );
    let has_globs = scope.glob.is_some() || !scope.globs.is_empty();
    if has_globs && !is_file_scope {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}: glob and globs require a file scope",
            gate.id
        ));
    }
    lint_staged_shell_findings(&mut findings, index, gate, surface, scope);
    if !scope.trigger.is_empty() && scope.scope != ScopeKind::PathGated {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}.trigger: only valid for path-gated scope",
            gate.id
        ));
    }
    if scope.scope == ScopeKind::PathGated && scope.trigger.is_empty() {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}.trigger: path-gated scope requires at least one trigger",
            gate.id
        ));
    }
    for glob in scope.glob.iter().chain(&scope.globs) {
        if let Err(error) = glob::Pattern::new(glob) {
            findings.push(format!(
                "gates[{index}] (gate id {:?}).surfaces.{surface:?}: invalid glob {glob:?}: {error}",
                gate.id
            ));
        }
    }
    let is_project_scope = matches!(
        scope.scope,
        ScopeKind::AffectedProjects | ScopeKind::AllProjects
    );
    if gate.kind == GateKind::Nx && !is_project_scope {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}: nx kind requires an affected-projects or all-projects scope",
            gate.id
        ));
    }
    if gate.kind != GateKind::Nx && is_project_scope {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}: project scopes require kind nx",
            gate.id
        ));
    }
    findings
}

/// Add findings for the pre-commit-only lint-staged shell override.
fn lint_staged_shell_findings(
    findings: &mut Vec<String>,
    index: usize,
    gate: &GateEntry,
    surface: &GateSurface,
    scope: &SurfaceScope,
) {
    let Some(shell) = &scope.lint_staged_shell else {
        return;
    };
    if *surface != GateSurface::PreCommit || scope.scope != ScopeKind::AffectedFileType {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}.lint-staged-shell: only valid for pre-commit affected-file-type",
            gate.id
        ));
    }
    if shell.trim().is_empty() {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}.lint-staged-shell: must not be blank",
            gate.id
        ));
    }
    if shell.matches("{{command}}").count() > 1 {
        findings.push(format!(
            "gates[{index}] (gate id {:?}).surfaces.{surface:?}.lint-staged-shell: {{command}} may appear at most once",
            gate.id
        ));
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// A minimal but schema-complete, valid `repo-config.yml`.
    const VALID: &str = concat!(
        "harness:\n",
        "  - { name: claude-code, tier: source, agent-dir: .claude/agents }\n",
        "coverage:\n",
        "  projects:\n",
        "    - name: rhino-cli\n",
        "      levels: [unit, integration]\n",
        "      specs: \"specs/apps/rhino/behavior/rhino-cli/**\"\n",
        "specs:\n  ddd-areas: []\n  domain-areas: []\n",
    );

    fn write_and_run(content: &str) -> (bool, String) {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), content).unwrap();
        let mut buf: Vec<u8> = Vec::new();
        let result = run_at_root(tmp.path(), &mut buf);
        (result.is_ok(), String::from_utf8_lossy(&buf).into_owned())
    }

    #[test]
    fn valid_config_passes() {
        let (ok, out) = write_and_run(VALID);
        assert!(ok, "valid config must pass; got: {out}");
    }

    #[test]
    fn value_only_difference_still_passes() {
        let mutated = VALID.replace("rhino-cli", "some-other-project");
        let (ok, _) = write_and_run(&mutated);
        assert!(ok, "a value-only change (same key set) must still pass");
    }

    #[test]
    fn unknown_key_is_rejected() {
        let with_unknown = format!("{VALID}bogus-unknown-section: true\n");
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("repo-config.yml"), &with_unknown).unwrap();
        let mut buf: Vec<u8> = Vec::new();
        let result = run_at_root(tmp.path(), &mut buf);
        assert!(result.is_err(), "unknown top-level key must be rejected");
        let msg = format!("{:#}", result.unwrap_err());
        assert!(
            msg.contains("bogus-unknown-section"),
            "error must name the offending key; got: {msg}"
        );
    }

    #[test]
    fn empty_coverage_projects_is_rejected() {
        let empty = "harness:\n  - { name: claude-code, tier: source, agent-dir: .claude/agents }\ncoverage:\n  projects: []\nspecs:\n  ddd-areas: []\n  domain-areas: []\n";
        let (ok, out) = write_and_run(empty);
        assert!(!ok, "empty coverage.projects must be rejected");
        assert!(
            out.contains("coverage.projects"),
            "finding must name coverage.projects; got: {out}"
        );
    }

    #[test]
    fn empty_harness_is_rejected() {
        let empty = "harness: []\ncoverage:\n  projects:\n    - name: p\n      levels: [unit]\n      specs: \"x\"\nspecs:\n  ddd-areas: []\n  domain-areas: []\n";
        let (ok, out) = write_and_run(empty);
        assert!(!ok, "empty harness must be rejected");
        assert!(
            out.contains("harness"),
            "finding must name harness; got: {out}"
        );
    }

    #[test]
    fn invalid_tier_enum_is_rejected() {
        let bad = VALID.replace("tier: source", "tier: bogus-tier");
        let (ok, out) = write_and_run(&bad);
        assert!(!ok, "invalid harness tier must be rejected");
        assert!(
            out.contains("tier") && out.contains("bogus-tier"),
            "finding must name the offending tier value; got: {out}"
        );
    }

    #[test]
    fn invalid_level_enum_is_rejected() {
        let bad = VALID.replace("[unit, integration]", "[unit, bogus-level]");
        let (ok, out) = write_and_run(&bad);
        assert!(!ok, "invalid coverage level must be rejected");
        assert!(
            out.contains("levels") && out.contains("bogus-level"),
            "finding must name the offending level value; got: {out}"
        );
    }

    #[test]
    fn unsafe_dotnet_global_json_paths_are_rejected() {
        for path in [
            "/tmp/global.json",
            "../global.json",
            "tooling/../../global.json",
        ] {
            let config = format!(
                "harness:\n  - {{ name: claude-code, tier: source, agent-dir: .claude/agents }}\ncoverage:\n  projects:\n    - name: p\n      levels: [unit]\n      specs: x\ndoctor:\n  dotnet-global-json: {path}\n"
            );
            let (ok, output) = write_and_run(&config);
            assert!(!ok, "unsafe path {path:?} must fail");
            assert!(
                output.contains("doctor.dotnet-global-json"),
                "finding must name the unsafe path key; got: {output}"
            );
        }
    }

    #[cfg(unix)]
    #[test]
    fn dotnet_global_json_symlink_escape_is_rejected() {
        use std::os::unix::fs::symlink;

        let tmp = TempDir::new().unwrap();
        let outside = TempDir::new().unwrap();
        symlink(outside.path(), tmp.path().join("tooling")).unwrap();
        fs::write(
            tmp.path().join("repo-config.yml"),
            format!("{VALID}doctor:\n  dotnet-global-json: tooling/sdk/global.json\n"),
        )
        .unwrap();
        let mut output = Vec::new();
        let result = run_at_root(tmp.path(), &mut output);
        let text = String::from_utf8_lossy(&output);

        assert!(result.is_err(), "a symlink escape must fail validation");
        assert!(text.contains("doctor.dotnet-global-json"));
        assert!(text.contains("escapes the repository root"));
    }

    #[test]
    fn args_constructible() {
        let _ = ValidateArgs {};
    }

    #[test]
    fn malformed_gate_glob_is_a_semantic_finding() {
        let tmp = TempDir::new().expect("create registry fixture");
        fs::write(
            tmp.path().join("repo-config.yml"),
            concat!(
                "gates:\n",
                "  - id: malformed-glob\n",
                "    type: check\n",
                "    command: true\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      ci: { scope: affected-file-type, glob: '[' }\n",
            ),
        )
        .expect("write registry fixture");
        let config = repo_config::load(tmp.path()).expect("fixture config must deserialize");

        assert!(
            semantic_findings(&config)
                .iter()
                .any(|finding| finding.contains("malformed-glob") && finding.contains("glob")),
            "a malformed gate glob must be reported before dispatch"
        );
    }

    #[test]
    fn gate_id_charset_accepts_valid_kebab_case() {
        let config = format!(
            "{VALID}{}",
            concat!(
                "gates:\n",
                "  - id: gate-1\n",
                "    type: check\n",
                "    command: true\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      ci: { scope: all-file-type }\n",
            )
        );
        let (ok, output) = write_and_run(&config);

        assert!(ok, "a valid kebab-case gate id must pass; got: {output}");
    }

    #[test]
    fn gate_id_charset_rejects_invalid_characters() {
        for bad_id in ["Gate_ID", "gate id", "gate/../x", ""] {
            let config = format!(
                "{VALID}gates:\n  - id: {bad_id:?}\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      ci: {{ scope: all-file-type }}\n"
            );
            let (ok, output) = write_and_run(&config);

            assert!(
                !ok,
                "gate id {bad_id:?} must be rejected; got ok output: {output}"
            );
            assert!(
                output.contains("kebab-case"),
                "finding for {bad_id:?} must cite the kebab-case rule; got: {output}"
            );
        }
    }

    #[test]
    fn lint_staged_shell_is_valid_for_pre_commit_affected_file_type() {
        let config = format!(
            "{VALID}{}",
            concat!(
                "gates:\n",
                "  - id: compose\n",
                "    type: check\n",
                "    command: docker compose config\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      pre-commit:\n",
                "        scope: affected-file-type\n",
                "        glob: 'docker-compose*.{yml,yaml}'\n",
                "        lint-staged-shell: \"bash -c 'for f; do {{command}} -f \\\"$f\\\"; done' --\"\n",
            )
        );
        let (ok, output) = write_and_run(&config);

        assert!(
            ok,
            "a pre-commit affected-file override must pass validation; got: {output}"
        );
    }

    #[test]
    fn lint_staged_shell_requires_pre_commit_affected_file_type() {
        let config = format!(
            "{VALID}{}",
            concat!(
                "gates:\n",
                "  - id: compose\n",
                "    type: check\n",
                "    command: docker compose config\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      ci:\n",
                "        scope: all-file-type\n",
                "        lint-staged-shell: bash -c '{{command}}'\n",
            )
        );
        let (ok, output) = write_and_run(&config);

        assert!(!ok, "a CI shell override must be rejected");
        assert!(
            output.contains("lint-staged-shell") && output.contains("pre-commit"),
            "finding must name the override and its only permitted surface; got: {output}"
        );
    }

    #[test]
    fn lint_staged_shell_preserves_existing_glob_and_globs_support() {
        let config = format!(
            "{VALID}{}",
            concat!(
                "gates:\n",
                "  - id: multiple-inputs\n",
                "    type: check\n",
                "    command: formatter verify\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      pre-commit:\n",
                "        scope: affected-file-type\n",
                "        glob: '*.md'\n",
                "        globs: ['*.json', '*.{yml,yaml}']\n",
                "        lint-staged-shell: \"sh -c 'formatter --staged' --\"\n",
            )
        );
        let (ok, output) = write_and_run(&config);

        assert!(
            ok,
            "the optional override must leave existing glob and globs forms valid; got: {output}"
        );
    }

    #[test]
    fn lint_staged_shell_rejects_blank_and_repeated_command_placeholders() {
        for shell in ["   ", "sh -c '{{command}} && {{command}}' --"] {
            let content = format!(
                "{VALID}gates:\n  - id: override\n    type: check\n    command: true\n    kind: external\n    surfaces:\n      pre-commit:\n        scope: affected-file-type\n        glob: '*.txt'\n        lint-staged-shell: {shell:?}\n"
            );
            let (ok, output) = write_and_run(&content);

            assert!(!ok, "invalid lint-staged-shell {shell:?} must fail");
            assert!(
                output.contains("lint-staged-shell"),
                "finding must name the invalid override; got: {output}"
            );
        }
    }
}
