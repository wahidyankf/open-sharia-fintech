//! `gate list` command adapter.

use std::collections::HashSet;
use std::io::Write;
use std::path::Path;

use anyhow::{Error, anyhow};
use clap::Args;
use serde::Serialize;

use crate::application::repo_config::{
    self, GateCarveOut, GateEntry, GateSurface, GateType, GateWiring, ScopeKind,
};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Arguments for `gate list`.
#[derive(Args, Debug)]
pub struct ListArgs {
    /// Surface whose declared gates to list.
    #[arg(long)]
    pub surface: String,
    /// Output format for the listed gates.
    #[arg(long, default_value = "text")]
    pub format: String,
}

/// JSON-friendly projection of one gate on one surface.
#[derive(Serialize)]
struct GateListEntry {
    /// Stable identifier of the declared gate.
    id: String,
    /// Declared gate type, serialized as the `type` field.
    #[serde(rename = "type")]
    gate_type: String,
    /// Command declared for the gate.
    command: String,
    /// Ordered Doctor tool identifiers declared for the gate.
    doctor_tools: Vec<String>,
    /// Scope declared for this surface.
    scope: String,
    /// Optional composition carve-out declared for the gate.
    #[serde(rename = "carve-out", skip_serializing_if = "Option::is_none")]
    carve_out: Option<String>,
    /// Formatter classification when the entry is a mutation formatter.
    #[serde(skip_serializing_if = "Option::is_none")]
    category: Option<String>,
    /// Mutation id checked by this verifier entry.
    #[serde(skip_serializing_if = "Option::is_none")]
    verifies: Option<String>,
    /// Explicit execution-wiring override for this gate.
    #[serde(skip_serializing_if = "Option::is_none")]
    wiring: Option<String>,
    /// Every surface where the registry declares this gate.
    surfaces: Vec<String>,
    /// Whether the gate is implemented directly by its workflow job.
    #[serde(skip_serializing)]
    hand_wired: bool,
}

/// List gates declared on one surface from `repo-config.yml`.
///
/// # Errors
///
/// Returns an error when the repository root cannot be found, the configured
/// output format is invalid, or `repo-config.yml` cannot be read or rendered.
pub fn run(args: &ListArgs, _output_format: OutputFormat) -> Result<(), Error> {
    let repo_root = git::root::find_root()?;
    let output_format = OutputFormat::parse(&args.format)?;
    run_at_root(
        &repo_root,
        &args.surface,
        output_format,
        &mut std::io::stdout(),
    )
}

/// List gates at a known repository root (testable entry point).
///
/// # Errors
///
/// Returns an error when `repo-config.yml` cannot be read or rendered.
pub fn run_at_root(
    repo_root: &Path,
    surface: &str,
    output_format: OutputFormat,
    writer: &mut dyn Write,
) -> Result<(), Error> {
    let surface = parse_surface(surface)?;
    let config = repo_config::load(repo_root)?;
    let surface_gates = config
        .gates
        .iter()
        .filter(|gate| gate.surfaces.contains_key(&surface))
        .collect::<Vec<_>>();
    validate_gate_ids(&surface_gates, None)?;
    let entries: Vec<GateListEntry> = surface_gates
        .iter()
        .filter(|gate| {
            output_format != OutputFormat::Json
                || gate.wiring.as_ref() != Some(&GateWiring::HandWired)
        })
        .map(|gate| {
            let scope = &gate.surfaces[&surface];
            GateListEntry {
                id: gate.id.clone(),
                gate_type: gate_type_name(&gate.gate_type).to_string(),
                command: gate.command.clone(),
                doctor_tools: gate.doctor_tools.clone(),
                scope: scope_name(&scope.scope).to_string(),
                carve_out: carve_out_name(gate.carve_out.as_ref()).map(str::to_owned),
                category: gate.category.clone(),
                verifies: gate.verifies.clone(),
                wiring: wiring_name(gate.wiring.as_ref()).map(str::to_owned),
                surfaces: gate
                    .surfaces
                    .keys()
                    .map(|surface| surface_name(surface).to_string())
                    .collect(),
                hand_wired: gate.wiring.as_ref() == Some(&GateWiring::HandWired),
            }
        })
        .collect();

    match output_format {
        OutputFormat::Json => {
            serde_json::to_writer_pretty(&mut *writer, &entries)?;
            writeln!(writer)?;
        }
        OutputFormat::Text | OutputFormat::Markdown => {
            for entry in entries {
                let marker = if entry.hand_wired { "\thand-wired" } else { "" };
                let carve_out = entry
                    .carve_out
                    .as_deref()
                    .map_or(String::new(), |value| format!("\tcarve-out={value}"));
                writeln!(
                    writer,
                    "{}\t{}\t{}\t{}{marker}{carve_out}",
                    entry.id, entry.gate_type, entry.command, entry.scope,
                )?;
            }
        }
    }
    Ok(())
}

/// Validates duplicate gate ids or an exact `--only` selector against one surface.
pub(crate) fn validate_gate_ids(gates: &[&GateEntry], only: Option<&str>) -> Result<(), Error> {
    if let Some(id) = only {
        let count = gates.iter().filter(|gate| gate.id == id).count();
        if count != 1 {
            return Err(anyhow!(
                "--only gate id {id:?} must select exactly one gate, found {count}"
            ));
        }
        return Ok(());
    }

    let mut ids = HashSet::new();
    for gate in gates {
        if !ids.insert(&gate.id) {
            return Err(anyhow!("duplicate gate id {:?}", gate.id));
        }
    }
    Ok(())
}

/// Parses a command-line surface name into its registry variant.
///
/// # Errors
///
/// Returns an error when the surface name is not supported by the registry.
fn parse_surface(surface: &str) -> Result<GateSurface, Error> {
    match surface {
        "commit-msg" => Ok(GateSurface::CommitMsg),
        "pre-commit" => Ok(GateSurface::PreCommit),
        "pre-push" => Ok(GateSurface::PrePush),
        "ci" => Ok(GateSurface::Ci),
        _ => Err(anyhow!(
            "unknown gate surface {surface:?}: expected one of commit-msg, pre-commit, pre-push, ci"
        )),
    }
}

/// Returns the registry spelling for a gate type.
fn gate_type_name(gate_type: &GateType) -> &'static str {
    match gate_type {
        GateType::Check => "check",
        GateType::Mutation => "mutation",
    }
}

/// Returns the registry spelling for an optional composition carve-out.
fn carve_out_name(carve_out: Option<&GateCarveOut>) -> Option<&'static str> {
    match carve_out {
        Some(GateCarveOut::StagedOnly) => Some("staged-only"),
        None => None,
    }
}

/// Returns the registry spelling for an optional execution-wiring override.
fn wiring_name(wiring: Option<&GateWiring>) -> Option<&'static str> {
    match wiring {
        Some(GateWiring::Matrix) => Some("matrix"),
        Some(GateWiring::HandWired) => Some("hand-wired"),
        None => None,
    }
}

/// Returns the registry spelling for a gate surface.
fn surface_name(surface: &GateSurface) -> &'static str {
    match surface {
        GateSurface::CommitMsg => "commit-msg",
        GateSurface::PreCommit => "pre-commit",
        GateSurface::PrePush => "pre-push",
        GateSurface::Ci => "ci",
    }
}

/// Returns the registry spelling for a surface scope.
fn scope_name(scope: &ScopeKind) -> &'static str {
    match scope {
        ScopeKind::AffectedFileType => "affected-file-type",
        ScopeKind::AllFileType => "all-file-type",
        ScopeKind::AffectedProjects => "affected-projects",
        ScopeKind::AllProjects => "all-projects",
        ScopeKind::Other => "other",
        ScopeKind::PathGated => "path-gated",
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn ci_json_lists_only_ci_gates_with_required_fields() {
        let repo = TempDir::new().unwrap();
        std::fs::write(
            repo.path().join("repo-config.yml"),
            concat!(
                "gates:\n",
                "  - id: ci-check\n",
                "    type: check\n",
                "    command: test:quick\n",
                "    kind: nx\n",
                "    doctor-tools: [git, node]\n",
                "    surfaces:\n",
                "      ci: { scope: affected-projects }\n",
                "  - id: pre-commit-format\n",
                "    type: mutation\n",
                "    command: prettier --write\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
                "  - id: ci-links\n",
                "    type: check\n",
                "    command: md links validate\n",
                "    kind: rhino-cli\n",
                "    surfaces:\n",
                "      ci: { scope: all-file-type }\n",
            ),
        )
        .unwrap();

        let mut output = Vec::new();
        run_at_root(repo.path(), "ci", OutputFormat::Json, &mut output)
            .expect("gate list command path must enumerate CI gates as JSON");

        let entries: Vec<serde_json::Value> = serde_json::from_slice(&output).unwrap();
        assert_eq!(entries.len(), 2);
        assert_eq!(entries[0]["id"], "ci-check");
        assert_eq!(entries[1]["id"], "ci-links");
        assert_eq!(
            entries[0]["doctor_tools"],
            serde_json::json!(["git", "node"])
        );
        assert_eq!(entries[1]["doctor_tools"], serde_json::json!([]));
        for entry in entries {
            assert!(entry.get("id").is_some());
            assert!(entry.get("type").is_some());
            assert!(entry.get("command").is_some());
            assert!(entry.get("scope").is_some());
            assert!(entry["doctor_tools"].is_array());
        }
    }

    #[test]
    fn json_preserves_formatter_verifier_wiring_and_declared_surface_metadata() {
        let repo = TempDir::new().unwrap();
        std::fs::write(
            repo.path().join("repo-config.yml"),
            concat!(
                "gates:\n",
                "  - id: format-prettier\n",
                "    type: mutation\n",
                "    category: formatter\n",
                "    command: prettier --write\n",
                "    kind: external\n",
                "    surfaces:\n",
                "      pre-commit: { scope: affected-file-type, glob: '*.md' }\n",
                "  - id: format-verify-prettier\n",
                "    type: check\n",
                "    command: prettier --check\n",
                "    kind: external\n",
                "    verifies: format-prettier\n",
                "    surfaces:\n",
                "      ci: { scope: all-file-type }\n",
                "  - id: ci-matrix\n",
                "    type: check\n",
                "    command: test:quick\n",
                "    kind: nx\n",
                "    wiring: matrix\n",
                "    surfaces:\n",
                "      pre-push: { scope: affected-projects }\n",
                "      ci: { scope: affected-projects }\n",
            ),
        )
        .unwrap();

        let mut pre_commit = Vec::new();
        run_at_root(
            repo.path(),
            "pre-commit",
            OutputFormat::Json,
            &mut pre_commit,
        )
        .unwrap();
        let formatter: serde_json::Value = serde_json::from_slice(&pre_commit).unwrap();
        let formatter = &formatter[0];
        assert_eq!(formatter["category"], "formatter");
        assert_eq!(formatter["surfaces"], serde_json::json!(["pre-commit"]));

        let mut ci = Vec::new();
        run_at_root(repo.path(), "ci", OutputFormat::Json, &mut ci).unwrap();
        let entries: Vec<serde_json::Value> = serde_json::from_slice(&ci).unwrap();
        let verifier = entries
            .iter()
            .find(|entry| entry["id"] == "format-verify-prettier")
            .expect("verifier emitted in CI matrix JSON");
        assert_eq!(verifier["verifies"], "format-prettier");
        let matrix = entries
            .iter()
            .find(|entry| entry["id"] == "ci-matrix")
            .expect("matrix gate emitted in CI matrix JSON");
        assert_eq!(matrix["wiring"], "matrix");
        assert_eq!(matrix["surfaces"], serde_json::json!(["pre-push", "ci"]));
    }

    #[test]
    fn valid_surfaces_without_gates_return_empty_json_arrays() {
        let repo = TempDir::new().unwrap();
        std::fs::write(repo.path().join("repo-config.yml"), "gates: []\n").unwrap();

        for surface in ["commit-msg", "pre-commit", "pre-push", "ci"] {
            let mut output = Vec::new();
            run_at_root(repo.path(), surface, OutputFormat::Json, &mut output).unwrap();
            assert_eq!(output, b"[]\n", "{surface} must return an empty array");
        }
    }

    #[test]
    fn unknown_surface_names_all_allowed_surfaces() {
        let repo = TempDir::new().unwrap();
        std::fs::write(repo.path().join("repo-config.yml"), "gates: []\n").unwrap();

        let error = run_at_root(repo.path(), "cron", OutputFormat::Json, &mut Vec::new())
            .unwrap_err()
            .to_string();
        assert!(error.contains("cron"));
        assert!(error.contains("commit-msg"));
        assert!(error.contains("pre-commit"));
        assert!(error.contains("pre-push"));
        assert!(error.contains("ci"));
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn format_json_omits_hand_wired() {
    let repo = tempfile::TempDir::new().unwrap();
    std::fs::write(
        repo.path().join("repo-config.yml"),
        concat!(
            "gates:\n",
            "  - id: matrix-check\n",
            "    type: check\n",
            "    command: md links validate\n",
            "    kind: rhino-cli\n",
            "    surfaces:\n",
            "      ci: { scope: all-file-type }\n",
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

    let mut output = Vec::new();
    run_at_root(repo.path(), "ci", OutputFormat::Json, &mut output).unwrap();
    let entries: Vec<serde_json::Value> = serde_json::from_slice(&output).unwrap();
    assert!(entries.iter().all(|entry| entry["id"] != "test-quick"));
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn format_text_includes_hand_wired() {
    let repo = tempfile::TempDir::new().unwrap();
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

    let mut output = Vec::new();
    run_at_root(repo.path(), "ci", OutputFormat::Text, &mut output).unwrap();
    let output = String::from_utf8(output).unwrap();
    assert!(output.contains("test-quick"));
    assert!(output.contains("hand-wired"));
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
#[test]
fn format_text_reports_staged_only_carve_out() {
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

    let mut output = Vec::new();
    run_at_root(repo.path(), "pre-commit", OutputFormat::Text, &mut output).unwrap();
    let output = String::from_utf8(output).unwrap();
    assert!(output.contains("index-guard"));
    assert!(output.contains("carve-out=staged-only"));
}
