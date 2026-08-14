//! `harness validate-naming` — checks that agent file names carry a valid role suffix.
//!
//! Port of `apps/rhino-cli/cmd/agents_validate_naming.go`.

use std::fs;
use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;

use crate::application::repo_config;
use crate::domain::cliout::OutputFormat;
use crate::internal::git;
use crate::internal::naming::{self, Violation};

use crate::internal::naming::reporter::{format_json, format_markdown, format_text};

/// Accepted role suffixes for agent file names.
const AGENT_ROLES: &[&str] = &[
    "maker",
    "checker",
    "fixer",
    "dev",
    "deployer",
    "manager",
    "tester",
    "researcher",
];

/// CLI arguments for `agents validate-naming` (none required).
#[derive(Args, Debug)]
pub struct ValidateNamingArgs {}

/// Run the `agents validate-naming` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, if agent files cannot be
/// read, or if any naming violations are found.
pub fn run(
    _args: &ValidateNamingArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let violations = agents_validate_naming(&repo_root.to_string_lossy())?;

    match output_format {
        OutputFormat::Text => print!("{}", format_text("Agents", &violations, false, false)),
        OutputFormat::Json => print!("{}", format_json("agents", &violations)?),
        OutputFormat::Markdown => print!("{}", format_markdown("Agents", &violations)),
    }

    if !violations.is_empty() {
        return Err(anyhow!("{} naming violation(s) found", violations.len()));
    }
    Ok(())
}

/// Collect naming violations for agent files under `repo_root`.
///
/// Reads source and generated tier dirs from `repo-config.yml` when available; falls back to
/// `.claude/agents` + `.opencode/agents` when the registry is absent or empty.
///
/// # Errors
///
/// Returns an error if any agent file cannot be read.
fn agents_validate_naming(repo_root: &str) -> std::result::Result<Vec<Violation>, Error> {
    let root = Path::new(repo_root);
    let config = repo_config::load_or_default(root);

    // Source tier: the single dir that all generated tiers must mirror.
    let source_dir = config
        .harness
        .iter()
        .find(|e| e.is_source_with_agents())
        .and_then(|e| e.agent_dir.as_deref())
        .map_or_else(|| root.join(".claude").join("agents"), |d| root.join(d));

    let source_files = list_agent_files(&source_dir);
    let source_dir_label = source_dir
        .strip_prefix(root)
        .unwrap_or(&source_dir)
        .to_string_lossy()
        .to_string();

    let mut violations: Vec<Violation> = Vec::new();

    // Suffix + frontmatter for source tier agents.
    for path in &source_files {
        if let Some(v) = naming::validate_suffix(path, AGENT_ROLES, "role-suffix") {
            violations.push(v);
        }
        let content = fs::read(path).with_context(|| format!("read {path}"))?;
        if let Some(v) = naming::validate_frontmatter_name(path, &content) {
            violations.push(v);
        }
    }

    // Generated tiers: suffix check + N-way mirror parity.
    let generated_entries: Vec<_> = config
        .harness
        .iter()
        .filter(|e| e.is_generated_with_agents())
        .collect();

    if generated_entries.is_empty() {
        // Fallback: OpenCode only (pre-registry behavior).
        let opencode_dir = root.join(".opencode").join("agents");
        let opencode_files = list_agent_files(&opencode_dir);
        for path in &opencode_files {
            if let Some(v) = naming::validate_suffix(path, AGENT_ROLES, "role-suffix") {
                violations.push(v);
            }
        }
        violations.extend(naming::validate_mirror(&source_files, &opencode_files));
    } else {
        for entry in generated_entries {
            let dir = root.join(entry.agent_dir.as_deref().unwrap_or(""));
            let target_files = list_agent_files(&dir);
            let target_dir_label = dir
                .strip_prefix(root)
                .unwrap_or(&dir)
                .to_string_lossy()
                .to_string();
            // Suffix check for this generated tier.
            for path in &target_files {
                if let Some(v) = naming::validate_suffix(path, AGENT_ROLES, "role-suffix") {
                    violations.push(v);
                }
            }
            // N-way mirror parity: source ↔ this generated tier.
            violations.extend(naming::validate_mirror_with_dirs(
                &source_files,
                &target_files,
                &source_dir_label,
                &target_dir_label,
            ));
        }
    }

    violations.sort_by(|a, b| a.path.cmp(&b.path).then(a.kind.cmp(&b.kind)));
    Ok(violations)
}

/// Return sorted paths of agent `.md` files in `dir`, excluding special files.
///
/// Walks one level of group subdirectory nesting the same way
/// `discover_agent_sources` does, so a grouped source tier
/// (`.claude/agents/<group>/<file>.md`) is not silently read as empty.
fn list_agent_files(dir: &Path) -> Vec<String> {
    let Ok(entries) = fs::read_dir(dir) else {
        return Vec::new();
    };
    let mut files = Vec::new();
    for entry in entries.flatten() {
        let is_dir = entry.file_type().is_ok_and(|t| t.is_dir());
        if is_dir {
            let Ok(group_entries) = fs::read_dir(entry.path()) else {
                continue;
            };
            for group_entry in group_entries.flatten() {
                if group_entry.file_type().is_ok_and(|t| t.is_dir()) {
                    continue;
                }
                push_agent_file(
                    &mut files,
                    &group_entry.file_name().to_string_lossy(),
                    &group_entry.path(),
                );
            }
            continue;
        }
        push_agent_file(
            &mut files,
            &entry.file_name().to_string_lossy(),
            &entry.path(),
        );
    }
    files.sort();
    files
}

/// Push `path` onto `files` unless `name` is a special/non-agent filename.
fn push_agent_file(files: &mut Vec<String>, name: &str, path: &Path) {
    if name == "README.md" || name == "ci-monitor-subagent.md" {
        return;
    }
    if !name.ends_with(".md") {
        return;
    }
    files.push(path.to_string_lossy().to_string());
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::TempDir;

    #[test]
    fn list_agent_files_skips_readme_and_subagent() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join(".claude/agents");
        std::fs::create_dir_all(&dir).unwrap();
        std::fs::write(dir.join("README.md"), "x").unwrap();
        std::fs::write(dir.join("ci-monitor-subagent.md"), "x").unwrap();
        std::fs::write(dir.join("foo-maker.md"), "x").unwrap();
        let files = list_agent_files(&dir);
        assert_eq!(files.len(), 1);
        assert!(files[0].ends_with("foo-maker.md"));
    }

    #[test]
    fn list_agent_files_missing_dir_is_empty() {
        let tmp = TempDir::new().unwrap();
        let files = list_agent_files(&tmp.path().join("nonexistent"));
        assert!(files.is_empty());
    }

    #[test]
    fn agents_validate_naming_clean_repo_is_empty() {
        let tmp = TempDir::new().unwrap();
        let cd = tmp.path().join(".claude/agents");
        let od = tmp.path().join(".opencode/agents");
        std::fs::create_dir_all(&cd).unwrap();
        std::fs::create_dir_all(&od).unwrap();
        std::fs::write(cd.join("foo-maker.md"), "---\nname: foo-maker\n---\n").unwrap();
        std::fs::write(od.join("foo-maker.md"), "---\n---\n").unwrap();
        let result = agents_validate_naming(&tmp.path().to_string_lossy()).unwrap();
        assert!(result.is_empty());
    }

    #[test]
    fn agents_validate_naming_accepts_tester_role() {
        let tmp = TempDir::new().unwrap();
        let cd = tmp.path().join(".claude/agents");
        let od = tmp.path().join(".opencode/agents");
        std::fs::create_dir_all(&cd).unwrap();
        std::fs::create_dir_all(&od).unwrap();
        std::fs::write(
            cd.join("exploratory-web-tester.md"),
            "---\nname: exploratory-web-tester\n---\n",
        )
        .unwrap();
        std::fs::write(od.join("exploratory-web-tester.md"), "---\n---\n").unwrap();
        let result = agents_validate_naming(&tmp.path().to_string_lossy()).unwrap();
        assert!(result.is_empty());
    }

    #[test]
    fn agents_validate_naming_accepts_researcher_role() {
        let tmp = TempDir::new().unwrap();
        let cd = tmp.path().join(".claude/agents");
        let od = tmp.path().join(".opencode/agents");
        std::fs::create_dir_all(&cd).unwrap();
        std::fs::create_dir_all(&od).unwrap();
        std::fs::write(
            cd.join("web-researcher.md"),
            "---\nname: web-researcher\n---\n",
        )
        .unwrap();
        std::fs::write(od.join("web-researcher.md"), "---\n---\n").unwrap();
        let result = agents_validate_naming(&tmp.path().to_string_lossy()).unwrap();
        assert!(result.is_empty());
    }

    #[test]
    fn agents_validate_naming_detects_suffix_and_mirror() {
        let tmp = TempDir::new().unwrap();
        let cd = tmp.path().join(".claude/agents");
        let od = tmp.path().join(".opencode/agents");
        std::fs::create_dir_all(&cd).unwrap();
        std::fs::create_dir_all(&od).unwrap();
        // Bad suffix + missing mirror in .opencode
        std::fs::write(cd.join("foo-bar.md"), "---\nname: foo-bar\n---\n").unwrap();
        let result = agents_validate_naming(&tmp.path().to_string_lossy()).unwrap();
        let kinds: Vec<&str> = result.iter().map(|v| v.kind.as_str()).collect();
        assert!(kinds.contains(&"role-suffix"));
        assert!(kinds.contains(&"mirror-drift"));
    }

    fn write_full_harness_config(dir: &std::path::Path) {
        let config = concat!(
            "harness:\n",
            "  - { name: claude-code, tier: source, agent-dir: .claude/agents,",
            " skills-dir: .claude/skills }\n",
            "  - { name: opencode, tier: generated, agent-dir: .opencode/agents,",
            " mirrors: .claude/agents }\n",
            "  - name: amazonq\n",
            "    tier: generated\n",
            "    agent-dir: .amazonq/cli-agents\n",
            "    mirrors: .claude/agents\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
        );
        std::fs::write(dir.join("repo-config.yml"), config).unwrap();
    }

    #[test]
    fn harness_naming_validate_checks_amazonq_agent_dir() {
        // Registry-driven: naming validate checks .amazonq/cli-agents/ per repo-config.yml harness:.
        let tmp = TempDir::new().unwrap();
        write_full_harness_config(tmp.path());
        std::fs::create_dir_all(tmp.path().join(".claude/agents")).unwrap();
        std::fs::create_dir_all(tmp.path().join(".opencode/agents")).unwrap();
        let amazonq_dir = tmp.path().join(".amazonq/cli-agents");
        std::fs::create_dir_all(&amazonq_dir).unwrap();
        // File with bad role suffix in the Amazon Q agent dir
        std::fs::write(
            amazonq_dir.join("bad-suffix.md"),
            "---\nname: bad-suffix\n---\n",
        )
        .unwrap();
        let violations = agents_validate_naming(&tmp.path().to_string_lossy()).unwrap();
        let has_amazonq = violations
            .iter()
            .any(|v| v.path.contains(".amazonq") || v.path.contains("amazonq"));
        assert!(
            has_amazonq,
            "naming validate must check .amazonq/cli-agents/ per harness registry"
        );
    }

    #[test]
    fn harness_naming_validate_mirrors_include_amazonq_n_way() {
        // Registry-driven: missing mirror in .amazonq/cli-agents/ must flag mirror-drift.
        let tmp = TempDir::new().unwrap();
        write_full_harness_config(tmp.path());
        let claude_dir = tmp.path().join(".claude/agents");
        let opencode_dir = tmp.path().join(".opencode/agents");
        let amazonq_dir = tmp.path().join(".amazonq/cli-agents");
        std::fs::create_dir_all(&claude_dir).unwrap();
        std::fs::create_dir_all(&opencode_dir).unwrap();
        std::fs::create_dir_all(&amazonq_dir).unwrap();
        // Agent present in .claude and .opencode but absent from .amazonq
        std::fs::write(
            claude_dir.join("foo-maker.md"),
            "---\nname: foo-maker\n---\n",
        )
        .unwrap();
        std::fs::write(opencode_dir.join("foo-maker.md"), "---\n---\n").unwrap();
        // .amazonq/cli-agents/ intentionally left empty — should flag mirror-drift
        let violations = agents_validate_naming(&tmp.path().to_string_lossy()).unwrap();
        let has_amazonq_drift = violations.iter().any(|v| {
            v.kind == "mirror-drift"
                && (v.path.contains(".amazonq") || v.message.contains(".amazonq"))
        });
        assert!(
            has_amazonq_drift,
            "naming validate must flag mirror-drift when .amazonq/cli-agents/ lacks an agent \
             present in .claude/agents/"
        );
    }
}
