//! Sync validator ported from
//! `apps/rhino-cli/internal/agents/sync_validator.go`.

use std::collections::BTreeMap;
use std::fs;
use std::path::Path;
use std::time::Instant;

use serde_norway::Value;

use super::bindings::drift_remediation;
use super::converter::{
    OPENCODE_AGENT_DIR, convert_model, convert_permission, is_mirrorable_agent_filename,
};
use super::frontmatter::{extract_frontmatter, parse_claude_tools};
use super::skills_mirror::{MirrorDrift, audit_skills_mirrors};
use super::types::{ValidationCheck, ValidationResult};

/// Run all sync-parity checks between `.claude/agents/` and `.opencode/agents/`.
pub fn validate_sync(repo_root: &Path) -> ValidationResult {
    let start = Instant::now();
    let mut result = ValidationResult::default();

    result.tally(validate_no_stale_agent_dir(repo_root));
    result.tally(validate_agent_count(repo_root));

    let equivalence = validate_agent_equivalence(repo_root);
    for c in equivalence {
        result.tally(c);
    }

    result.tally(validate_no_synced_skills(repo_root));
    result.tally(validate_skills_mirror(repo_root));

    result.duration = start.elapsed();
    result
}

/// Validates that every registry-declared skills mirror agrees with its
/// canonical source tree.
///
/// Deliberately reuses the emitter's own diff rather than re-deriving what the
/// mirror should hold: a second reader would drift from the emitter the moment
/// either side changed, and the drift would surface as a false pass.
fn validate_skills_mirror(repo_root: &Path) -> ValidationCheck {
    let check_name = "Skills Mirror: .agents/skills".to_string();
    match audit_skills_mirrors(repo_root) {
        Err(e) => ValidationCheck::failed_msg(check_name, e),
        Ok(drifts) if drifts.is_empty() => {
            ValidationCheck::passed(check_name, "skills mirror matches its source tree")
        }
        Ok(drifts) => {
            let detail = drifts
                .iter()
                .map(ToString::to_string)
                .collect::<Vec<_>>()
                .join("; ");
            // A skills mirror is `generated`-class exactly like an agent
            // mirror, so a hand-edited one is exactly as promotable — the
            // remedy must name `harness sync promote` too, not only the
            // regenerate command that discards the edit (H1). Only
            // `Missing` drifts (a hand-edited or stale mirror file with a
            // real canonical source) route through `drift_remediation`; an
            // `Undeclared` drift (an orphan with no source counterpart and
            // no vendored declaration) has nothing to promote into.
            let remediation = drifts
                .iter()
                .map(|drift| match drift {
                    MirrorDrift::Missing(mirror_rel) => drift_remediation(repo_root, mirror_rel),
                    MirrorDrift::Undeclared(mirror_rel) => format!(
                        "{mirror_rel} has no source counterpart and is not declared vendored; \
                         run `rhino-cli harness bindings generate` to remove it."
                    ),
                })
                .collect::<Vec<_>>()
                .join(" ");
            ValidationCheck::failed(
                check_name,
                "mirror byte-equal to its canonical source tree",
                detail,
                remediation,
            )
        }
    }
}

/// Check that the legacy singular `.opencode/agent` path does not exist.
fn validate_no_stale_agent_dir(repo_root: &Path) -> ValidationCheck {
    let stale = repo_root.join(".opencode").join("agent");
    match fs::metadata(&stale) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => ValidationCheck::passed(
            "No Stale Agent Directory",
            "Legacy singular .opencode/agent does not exist",
        ),
        Err(e) => ValidationCheck::failed_msg(
            "No Stale Agent Directory",
            format!("Failed to stat .opencode/agent: {e}"),
        ),
        Ok(info) if info.is_dir() => ValidationCheck::failed(
            "No Stale Agent Directory",
            ".opencode/agent does not exist",
            ".opencode/agent exists as a directory",
            "Stale singular .opencode/agent reappeared; canonical OpenCode path is .opencode/agents/ (plural). Remove the stale directory.",
        ),
        Ok(_) => ValidationCheck::failed(
            "No Stale Agent Directory",
            ".opencode/agent does not exist",
            ".opencode/agent exists",
            "Stale .opencode/agent entry reappeared; canonical OpenCode path is .opencode/agents/ (plural). Remove the stale entry.",
        ),
    }
}

/// Check that `.opencode/agents/` contains at least as many `.md` files as `.claude/agents/`.
fn validate_agent_count(repo_root: &Path) -> ValidationCheck {
    let claude_dir = repo_root.join(".claude").join("agents");
    let opencode_dir = repo_root.join(OPENCODE_AGENT_DIR);

    let claude_count = count_claude_agent_sources(&claude_dir);
    let opencode_count = count_markdown_files(&opencode_dir);

    if opencode_count >= claude_count {
        ValidationCheck::passed(
            "Agent Count",
            "OpenCode agents directory contains every Claude agent",
        )
        .with_expected(format!(">= {claude_count} agents"))
        .with_actual(format!("{opencode_count} agents"))
    } else {
        ValidationCheck::failed(
            "Agent Count",
            format!(">= {claude_count} agents"),
            format!("{opencode_count} agents"),
            "OpenCode agents directory missing one or more Claude agents",
        )
    }
}

/// Builder extension for setting `expected`/`actual` fields after construction.
trait WithExpectedActual {
    /// Set the `expected` field and return `self`.
    fn with_expected(self, e: String) -> Self;
    /// Set the `actual` field and return `self`.
    fn with_actual(self, a: String) -> Self;
}

impl WithExpectedActual for ValidationCheck {
    fn with_expected(mut self, e: String) -> Self {
        self.expected = e;
        self
    }
    fn with_actual(mut self, a: String) -> Self {
        self.actual = a;
        self
    }
}

/// Compare each Claude agent to its `OpenCode` counterpart for semantic equivalence.
fn validate_agent_equivalence(repo_root: &Path) -> Vec<ValidationCheck> {
    let mut checks = Vec::new();
    let claude_dir = repo_root.join(".claude").join("agents");
    let opencode_dir = repo_root.join(OPENCODE_AGENT_DIR);

    // Walks one level of group subdirectory nesting (FR-3.18) — a plain
    // `fs::read_dir` would silently see zero grouped agents.
    let files = match super::converter::discover_agent_sources(&claude_dir) {
        Ok(v) => v,
        Err(e) => {
            checks.push(ValidationCheck::failed_msg(
                "Agent Equivalence",
                format!("Failed to read Claude agents directory: {e}"),
            ));
            return checks;
        }
    };

    for (claude_path, name) in files {
        let opencode_path = opencode_dir.join(format!("{name}.md"));
        checks.push(validate_agent_file(
            &name,
            &claude_path,
            &opencode_path,
            &claude_dir,
            &opencode_dir,
        ));
    }

    checks
}

/// Read and parse both copies of `name` then delegate to `validate_agent_yaml`.
/// `claude_dir`/`mirror_dir` rebase the Claude body's relative links before
/// comparison, matching what the generator itself would emit for a grouped
/// source (see `rebase_agent_links`).
fn validate_agent_file(
    name: &str,
    claude_path: &Path,
    opencode_path: &Path,
    claude_dir: &Path,
    mirror_dir: &Path,
) -> ValidationCheck {
    let check_name = format!("Agent: {name}");

    let claude_content = match fs::read(claude_path) {
        Ok(v) => v,
        Err(e) => {
            return ValidationCheck::failed_msg(
                &check_name,
                format!("Failed to read Claude agent: {e}"),
            );
        }
    };
    let opencode_content = match fs::read(opencode_path) {
        Ok(v) => v,
        Err(e) => {
            return ValidationCheck::failed_msg(
                &check_name,
                format!("Failed to read OpenCode agent: {e}"),
            );
        }
    };

    let (claude_front, claude_body) = match extract_frontmatter(&claude_content) {
        Ok(v) => v,
        Err(e) => {
            return ValidationCheck::failed_msg(
                &check_name,
                format!("Failed to parse Claude frontmatter: {e}"),
            );
        }
    };
    let (opencode_front, opencode_body) = match extract_frontmatter(&opencode_content) {
        Ok(v) => v,
        Err(e) => {
            return ValidationCheck::failed_msg(
                &check_name,
                format!("Failed to parse OpenCode frontmatter: {e}"),
            );
        }
    };

    let claude_str = String::from_utf8_lossy(&claude_front).into_owned();
    let opencode_str = String::from_utf8_lossy(&opencode_front).into_owned();

    let claude_yaml: Value = match serde_norway::from_str(&claude_str) {
        Ok(v) => v,
        Err(e) => {
            return ValidationCheck::failed_msg(
                &check_name,
                format!("Failed to parse Claude YAML: {e}"),
            );
        }
    };
    let opencode_yaml: Value = match serde_norway::from_str(&opencode_str) {
        Ok(v) => v,
        Err(e) => {
            return ValidationCheck::failed_msg(
                &check_name,
                format!("Failed to parse OpenCode YAML: {e}"),
            );
        }
    };

    let expected_body =
        super::converter::rebase_agent_links(&claude_body, claude_path, claude_dir, mirror_dir);

    validate_agent_yaml(
        &check_name,
        &claude_yaml,
        &opencode_yaml,
        &expected_body,
        &opencode_body,
    )
}

/// Check description, model, permission, skills, and body parity between the two YAML trees.
fn validate_agent_yaml(
    check_name: &str,
    claude_yaml: &Value,
    opencode_yaml: &Value,
    claude_body: &[u8],
    opencode_body: &[u8],
) -> ValidationCheck {
    let claude_desc = claude_yaml
        .get("description")
        .and_then(|v| v.as_str())
        .unwrap_or("");
    let opencode_desc = opencode_yaml
        .get("description")
        .and_then(|v| v.as_str())
        .unwrap_or("");
    if claude_desc != opencode_desc {
        return ValidationCheck::failed(
            check_name,
            "Matching descriptions",
            "Descriptions differ",
            "Description mismatch",
        );
    }

    let claude_model = claude_yaml
        .get("model")
        .and_then(|v| v.as_str())
        .unwrap_or("");
    let expected_model = convert_model(claude_model);
    let opencode_model = opencode_yaml
        .get("model")
        .and_then(|v| v.as_str())
        .unwrap_or("");
    if expected_model != opencode_model {
        return ValidationCheck::failed(
            check_name,
            format!("Model: {expected_model}"),
            format!("Model: {opencode_model}"),
            "Model mismatch",
        );
    }

    let claude_tools = match claude_yaml.get("tools") {
        Some(v) => parse_claude_tools(v),
        None => Vec::new(),
    };
    let expected_permission = convert_permission(&claude_tools);
    let opencode_permission = parse_opencode_permission(opencode_yaml.get("permission"));
    if !permission_match(&expected_permission, &opencode_permission) {
        return ValidationCheck::failed(
            check_name,
            format!(
                "Permission: {}",
                format_string_slice_owned(&sorted_keys(&expected_permission))
            ),
            format!(
                "Permission: {}",
                format_string_slice_owned(&sorted_keys(&opencode_permission))
            ),
            "Permission mismatch",
        );
    }

    let claude_skills = parse_string_seq(claude_yaml.get("skills"));
    let opencode_skills = parse_string_seq(opencode_yaml.get("skills"));
    if !skills_match(&claude_skills, &opencode_skills) {
        return ValidationCheck::failed(
            check_name,
            format!("Skills: {}", format_string_slice_owned(&claude_skills)),
            format!("Skills: {}", format_string_slice_owned(&opencode_skills)),
            "Skills mismatch",
        );
    }

    if claude_body != opencode_body {
        return ValidationCheck::failed(
            check_name,
            "Matching body content",
            "Body content differs",
            "Body mismatch",
        );
    }

    ValidationCheck::passed(check_name, "Agent is semantically equivalent")
}

/// Parse an `OpenCode` permission YAML mapping into a `BTreeMap<tool, action>`.
fn parse_opencode_permission(v: Option<&Value>) -> BTreeMap<String, String> {
    let mut out = BTreeMap::new();
    if let Some(Value::Mapping(m)) = v {
        for (k, val) in m {
            if let (Some(key), Some(action)) = (k.as_str(), val.as_str()) {
                out.insert(key.to_string(), action.to_string());
            }
        }
    }
    out
}

/// Parse a YAML sequence of strings into a `Vec<String>`.
fn parse_string_seq(v: Option<&Value>) -> Vec<String> {
    let mut out = Vec::new();
    if let Some(Value::Sequence(seq)) = v {
        for item in seq {
            if let Some(s) = item.as_str() {
                out.push(s.to_string());
            }
        }
    }
    out
}

/// Check that no `.claude/skills/<name>/SKILL.md` mirror exists under `.opencode/skill[s]/`.
fn validate_no_synced_skills(repo_root: &Path) -> ValidationCheck {
    let claude_dir = repo_root.join(".claude").join("skills");
    let mut claude_names: std::collections::HashSet<String> = std::collections::HashSet::new();
    if let Ok(entries) = fs::read_dir(&claude_dir) {
        for entry in entries.flatten() {
            if entry.file_type().is_ok_and(|t| t.is_dir()) {
                let skill_file = entry.path().join("SKILL.md");
                if skill_file.exists() {
                    claude_names.insert(entry.file_name().to_string_lossy().into_owned());
                }
            }
        }
    }

    let mirror_dirs = [
        repo_root.join(".opencode").join("skill"),
        repo_root.join(".opencode").join("skills"),
    ];

    let mut offenders: Vec<String> = Vec::new();
    for dir in &mirror_dirs {
        if let Ok(entries) = fs::read_dir(dir) {
            for entry in entries.flatten() {
                let name = entry.file_name().to_string_lossy().into_owned();
                if entry.file_type().is_ok_and(|t| t.is_dir()) && claude_names.contains(&name) {
                    let skill_file = entry.path().join("SKILL.md");
                    if skill_file.exists() {
                        offenders.push(entry.path().to_string_lossy().into_owned());
                    }
                }
            }
        }
    }

    if offenders.is_empty() {
        ValidationCheck::passed(
            "No Synced Skill Mirror",
            "No rhino-cli-managed skill copies under .opencode/skill or .opencode/skills",
        )
    } else {
        ValidationCheck::failed(
            "No Synced Skill Mirror",
            "No skill copy mirroring .claude/skills/<name>",
            format!(
                "Found {} mirrored skill dir(s): {}",
                offenders.len(),
                format_string_slice_owned(&offenders)
            ),
            "OpenCode reads .claude/skills/ natively; remove the mirror copies",
        )
    }
}

/// Count non-README `.md` files directly inside `dir` (returns 0 if dir doesn't exist).
fn count_markdown_files(dir: &Path) -> usize {
    let Ok(entries) = fs::read_dir(dir) else {
        return 0;
    };
    let mut count = 0;
    for entry in entries.flatten() {
        let name = entry.file_name().to_string_lossy().into_owned();
        if entry.file_type().is_ok_and(|t| !t.is_dir())
            && is_mirrorable_agent_filename(&name, false)
        {
            count += 1;
        }
    }
    count
}

/// Count agent sources under `.claude/agents/`, walking one level of group
/// subdirectory nesting the same way `discover_agent_sources` does — a plain
/// `fs::read_dir` would undercount to zero once agents are grouped (FR-3.18).
fn count_claude_agent_sources(claude_dir: &Path) -> usize {
    super::converter::discover_agent_sources(claude_dir).map_or(0, |sources| sources.len())
}

/// Return true if two permission maps are identical (same keys and values).
fn permission_match(a: &BTreeMap<String, String>, b: &BTreeMap<String, String>) -> bool {
    a == b
}

/// Return true if both skill sequences are identical (order-sensitive).
fn skills_match(a: &[String], b: &[String]) -> bool {
    a == b
}

/// Return the keys of `m` in sorted order for deterministic display.
fn sorted_keys(m: &BTreeMap<String, String>) -> Vec<String> {
    m.keys().cloned().collect()
}

/// Format an owned string slice as `[a b c]` — Go `%v` style.
fn format_string_slice_owned(s: &[String]) -> String {
    format!("[{}]", s.join(" "))
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    fn write(path: &Path, content: &str) {
        if let Some(p) = path.parent() {
            std::fs::create_dir_all(p).unwrap();
        }
        std::fs::write(path, content).unwrap();
    }

    fn setup() -> tempfile::TempDir {
        let dir = tempdir().unwrap();
        let root = dir.path();
        let claude = root.join(".claude/agents");
        let opencode = root.join(".opencode/agents");
        std::fs::create_dir_all(&claude).unwrap();
        std::fs::create_dir_all(&opencode).unwrap();
        write(
            &claude.join("foo.md"),
            "---\nname: foo\ndescription: desc\ntools: Read, Write\nmodel: sonnet\nskills:\n  - my-skill\n---\nBody\n",
        );
        write(
            &opencode.join("foo.md"),
            "---\ndescription: desc\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n  write: allow\nskills:\n  - my-skill\n---\nBody\n",
        );
        dir
    }

    // Regression for H1: a hand-edited skills mirror's remediation must name
    // `harness sync promote` alongside the destructive `bindings generate`,
    // exactly as an agent mirror's does — not only the remedy that discards
    // the edit.
    #[test]
    fn validate_skills_mirror_names_promote_for_a_drifted_mirror_with_a_canonical_source() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write(
            &root.join("repo-config.yml"),
            concat!(
                "harness:\n",
                "  - name: codex\n",
                "    tier: generated\n",
                "    agent-dir: .codex/agents\n",
                "    mirrors: .claude/agents\n",
                "    skills-dir: .agents/skills\n",
                "    skills-mirrors: .claude/skills\n",
            ),
        );
        write(&root.join(".claude/skills/demo/SKILL.md"), "canonical\n");
        write(&root.join(".agents/skills/demo/SKILL.md"), "hand-edited\n");

        let check = validate_skills_mirror(root);

        assert_eq!(check.status, "failed");
        assert!(
            check.message.contains("harness sync promote"),
            "message must name the preserving remedy too; got: {}",
            check.message
        );
        assert!(
            check.message.contains(".claude/skills/demo/SKILL.md"),
            "message must resolve the canonical source path; got: {}",
            check.message
        );
    }

    #[test]
    fn validate_no_stale_agent_dir_passes_when_absent() {
        let dir = tempdir().unwrap();
        let c = validate_no_stale_agent_dir(dir.path());
        assert_eq!(c.status, "passed");
    }

    #[test]
    fn validate_no_stale_agent_dir_fails_when_present_as_dir() {
        let dir = tempdir().unwrap();
        std::fs::create_dir_all(dir.path().join(".opencode/agent")).unwrap();
        let c = validate_no_stale_agent_dir(dir.path());
        assert_eq!(c.status, "failed");
        assert!(c.actual.contains("exists as a directory"));
    }

    #[test]
    fn validate_no_stale_agent_dir_fails_when_present_as_file() {
        let dir = tempdir().unwrap();
        std::fs::create_dir_all(dir.path().join(".opencode")).unwrap();
        std::fs::write(dir.path().join(".opencode/agent"), b"x").unwrap();
        let c = validate_no_stale_agent_dir(dir.path());
        assert_eq!(c.status, "failed");
    }

    #[test]
    fn validate_agent_count_passes() {
        let dir = setup();
        let c = validate_agent_count(dir.path());
        assert_eq!(c.status, "passed");
    }

    #[test]
    fn validate_agent_count_fails_with_missing() {
        let dir = setup();
        std::fs::remove_file(dir.path().join(".opencode/agents/foo.md")).unwrap();
        let c = validate_agent_count(dir.path());
        assert_eq!(c.status, "failed");
    }

    #[test]
    fn validate_agent_equivalence_pass() {
        let dir = setup();
        let checks = validate_agent_equivalence(dir.path());
        assert!(!checks.is_empty());
        assert!(checks.iter().all(|c| c.status == "passed"), "{checks:#?}");
    }

    #[test]
    fn validate_agent_equivalence_passes_for_grouped_source_with_rebased_link() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write(
            &root.join(".claude/agents/checkers/docs-checker.md"),
            "---\nname: docs-checker\ndescription: desc\ntools: Read\nmodel: sonnet\n---\nSee [conventions](../../../repo-governance/conventions/README.md).\n",
        );
        write(
            &root.join(".opencode/agents/docs-checker.md"),
            "---\ndescription: desc\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n---\nSee [conventions](../../repo-governance/conventions/README.md).\n",
        );
        let checks = validate_agent_equivalence(root);
        assert!(!checks.is_empty());
        assert!(
            checks.iter().all(|c| c.status == "passed"),
            "the expected body must be rebased exactly like the generator's own output before comparison: {checks:#?}"
        );
    }

    #[test]
    fn validate_agent_equivalence_fails_on_desc_mismatch() {
        let dir = setup();
        write(
            &dir.path().join(".opencode/agents/foo.md"),
            "---\ndescription: NOPE\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n  write: allow\nskills:\n  - my-skill\n---\nBody\n",
        );
        let checks = validate_agent_equivalence(dir.path());
        assert!(
            checks
                .iter()
                .any(|c| c.status == "failed" && c.message == "Description mismatch")
        );
    }

    #[test]
    fn validate_agent_equivalence_fails_on_model_mismatch() {
        let dir = setup();
        write(
            &dir.path().join(".opencode/agents/foo.md"),
            "---\ndescription: desc\nmodel: zai-coding-plan/wrong\npermission:\n  read: allow\n  write: allow\nskills:\n  - my-skill\n---\nBody\n",
        );
        let checks = validate_agent_equivalence(dir.path());
        assert!(
            checks
                .iter()
                .any(|c| c.status == "failed" && c.message == "Model mismatch")
        );
    }

    #[test]
    fn validate_agent_equivalence_fails_on_permission_mismatch() {
        let dir = setup();
        write(
            &dir.path().join(".opencode/agents/foo.md"),
            "---\ndescription: desc\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\nskills:\n  - my-skill\n---\nBody\n",
        );
        let checks = validate_agent_equivalence(dir.path());
        assert!(
            checks
                .iter()
                .any(|c| c.status == "failed" && c.message == "Permission mismatch")
        );
    }

    #[test]
    fn validate_agent_equivalence_fails_on_skills_mismatch() {
        let dir = setup();
        write(
            &dir.path().join(".opencode/agents/foo.md"),
            "---\ndescription: desc\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n  write: allow\nskills:\n  - other-skill\n---\nBody\n",
        );
        let checks = validate_agent_equivalence(dir.path());
        assert!(
            checks
                .iter()
                .any(|c| c.status == "failed" && c.message == "Skills mismatch")
        );
    }

    #[test]
    fn validate_agent_equivalence_fails_on_body_mismatch() {
        let dir = setup();
        write(
            &dir.path().join(".opencode/agents/foo.md"),
            "---\ndescription: desc\nmodel: zai-coding-plan/glm-5.2\npermission:\n  read: allow\n  write: allow\nskills:\n  - my-skill\n---\nDifferent Body\n",
        );
        let checks = validate_agent_equivalence(dir.path());
        assert!(
            checks
                .iter()
                .any(|c| c.status == "failed" && c.message == "Body mismatch")
        );
    }

    #[test]
    fn validate_no_synced_skills_passes() {
        let dir = setup();
        // Create .claude/skills/my-skill/SKILL.md but no mirror
        write(
            &dir.path().join(".claude/skills/my-skill/SKILL.md"),
            "---\nname: my-skill\ndescription: ok\n---\n",
        );
        let c = validate_no_synced_skills(dir.path());
        assert_eq!(c.status, "passed");
    }

    #[test]
    fn validate_no_synced_skills_fails_with_mirror() {
        let dir = setup();
        write(
            &dir.path().join(".claude/skills/my-skill/SKILL.md"),
            "---\nname: my-skill\ndescription: ok\n---\n",
        );
        write(
            &dir.path().join(".opencode/skills/my-skill/SKILL.md"),
            "---\nname: my-skill\ndescription: ok\n---\n",
        );
        let c = validate_no_synced_skills(dir.path());
        assert_eq!(c.status, "failed");
    }

    #[test]
    fn validate_no_synced_skills_tolerates_extra_skill() {
        let dir = setup();
        write(
            &dir.path().join(".claude/skills/my-skill/SKILL.md"),
            "---\nname: my-skill\ndescription: ok\n---\n",
        );
        write(
            &dir.path().join(".opencode/skills/other-skill/SKILL.md"),
            "---\nname: other-skill\ndescription: ok\n---\n",
        );
        let c = validate_no_synced_skills(dir.path());
        assert_eq!(c.status, "passed");
    }

    #[test]
    fn count_markdown_files_excludes_readme() {
        let dir = tempdir().unwrap();
        std::fs::create_dir_all(dir.path()).unwrap();
        write(&dir.path().join("a.md"), "x");
        write(&dir.path().join("README.md"), "x");
        assert_eq!(count_markdown_files(dir.path()), 1);
    }

    #[test]
    fn permission_match_basic() {
        let mut a = BTreeMap::new();
        a.insert("read".to_string(), "allow".to_string());
        let mut b = BTreeMap::new();
        b.insert("read".to_string(), "allow".to_string());
        assert!(permission_match(&a, &b));
        b.insert("write".to_string(), "allow".to_string());
        assert!(!permission_match(&a, &b));
    }

    #[test]
    fn full_validate_sync_pass() {
        let dir = setup();
        let r = validate_sync(dir.path());
        assert_eq!(r.failed_checks, 0, "result: {r:#?}");
    }
}
