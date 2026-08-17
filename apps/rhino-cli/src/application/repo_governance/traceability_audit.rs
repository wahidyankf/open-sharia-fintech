//! Traceability audit for governance Markdown documents.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/repo-governance/traceability_audit.go`.

use std::path::Path;
use std::sync::OnceLock;

use anyhow::{Context, Error};
use regex::Regex;

use crate::application::fs::port::Fs;

/// A single finding from the traceability audit.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TraceabilityFinding {
    /// Path of the governance document that is missing a required heading or
    /// reference.
    pub path: String,
    /// 1-based line number where the issue was detected (typically `1` when
    /// the heading is entirely absent).
    pub line: usize,
    /// Machine-readable violation category (one of the `KIND_*` constants).
    pub kind: String,
    /// Human-readable description of the finding.
    pub message: String,
}

/// Finding kind: a principle document is missing the required
/// `## Vision Supported` heading.
pub const KIND_MISSING_VISION_SUPPORTED: &str = "missing-vision-supported";
/// Finding kind: a convention or development document is missing the required
/// `## Principles Implemented/Respected` heading.
pub const KIND_MISSING_PRINCIPLES_IMPLEMENTED: &str = "missing-principles-implemented";
/// Finding kind: a development document is missing the required
/// `## Conventions Implemented/Respected` heading.
pub const KIND_MISSING_CONVENTIONS_IMPLEMENTED: &str = "missing-conventions-implemented";
/// Finding kind: a workflow document does not reference any
/// `.claude/agents/<name>.md` file.
pub const KIND_MISSING_AGENT_REFERENCE: &str = "missing-agent-reference";

/// Returns a compiled `Regex` that matches the `## Vision Supported` ATX
/// heading.
fn vision_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"(?m)^##\s+Vision Supported\s*$").expect("valid hardcoded regex"))
}

/// Returns a compiled `Regex` that matches the
/// `## Principles Implemented/Respected` ATX heading.
fn principles_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"(?m)^##\s+Principles Implemented/Respected\s*$")
            .expect("valid hardcoded regex")
    })
}

/// Returns a compiled `Regex` that matches the
/// `## Conventions Implemented/Respected` ATX heading.
fn conventions_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"(?m)^##\s+Conventions Implemented/Respected\s*$")
            .expect("valid hardcoded regex")
    })
}

/// Returns a compiled `Regex` that matches any `.claude/agents/<name>.md`
/// reference in a workflow document.
///
/// Agent definitions live one directory deep (`.claude/agents/<domain>/<name>.md`),
/// so the optional `<domain>/` segment is part of the pattern; a flat
/// `.claude/agents/<name>.md` still matches for forward compatibility.
fn agent_ref_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        Regex::new(r"\.claude/agents/(?:[a-z0-9-]+/)?[a-z0-9-]+\.md")
            .expect("valid hardcoded regex")
    })
}

/// Relative paths (within the workflows directory) that are exempt from the
/// agent-reference requirement.
const META_EXEMPT: &[&str] = &["meta/execution-modes.md", "meta/workflow-identifier.md"];

/// Audits traceability across four governance document families.
///
/// - `repo-governance/principles/` — each file must have `## Vision Supported`.
/// - `repo-governance/conventions/` — each file must have
///   `## Principles Implemented/Respected`.
/// - `repo-governance/development/` — each file must have both
///   `## Principles Implemented/Respected` and
///   `## Conventions Implemented/Respected`.
/// - `repo-governance/workflows/` — each non-exempt file must reference at
///   least one `.claude/agents/<name>.md` path.
///
/// `README.md` files are exempt from all checks.  Findings are sorted by
/// `path`, then by `line`.
///
/// # Errors
///
/// Returns an error when any governance document cannot be read.
pub fn audit_traceability(
    fs: &dyn Fs,
    repo_root: &Path,
) -> std::result::Result<Vec<TraceabilityFinding>, Error> {
    let mut findings = Vec::new();
    findings.extend(audit_principles(
        fs,
        &repo_root.join("repo-governance/principles"),
    )?);
    findings.extend(audit_conventions(
        fs,
        &repo_root.join("repo-governance/conventions"),
    )?);
    findings.extend(audit_development(
        fs,
        &repo_root.join("repo-governance/development"),
    )?);
    findings.extend(audit_workflows(
        fs,
        &repo_root.join("repo-governance/workflows"),
    )?);

    findings.sort_by(|a, b| a.path.cmp(&b.path).then(a.line.cmp(&b.line)));
    Ok(findings)
}

/// Checks that every Markdown file under `root` contains a
/// `## Vision Supported` heading.
///
/// # Errors
///
/// Returns an error when a file cannot be read.
fn audit_principles(
    fs: &dyn Fs,
    root: &Path,
) -> std::result::Result<Vec<TraceabilityFinding>, Error> {
    let files = list_governance_markdown(fs, root)?;
    let mut findings = Vec::new();
    for path in files {
        let data = fs
            .read_to_string(Path::new(&path))
            .with_context(|| format!("read {path}"))?;
        if !vision_re().is_match(&data) {
            findings.push(TraceabilityFinding {
                path: path.clone(),
                line: 1,
                kind: KIND_MISSING_VISION_SUPPORTED.to_string(),
                message: "principle is missing required \"## Vision Supported\" heading"
                    .to_string(),
            });
        }
    }
    Ok(findings)
}

/// Checks that every Markdown file under `root` contains a
/// `## Principles Implemented/Respected` heading.
///
/// # Errors
///
/// Returns an error when a file cannot be read.
fn audit_conventions(
    fs: &dyn Fs,
    root: &Path,
) -> std::result::Result<Vec<TraceabilityFinding>, Error> {
    let files = list_governance_markdown(fs, root)?;
    let mut findings = Vec::new();
    for path in files {
        let data = fs
            .read_to_string(Path::new(&path))
            .with_context(|| format!("read {path}"))?;
        if !principles_re().is_match(&data) {
            findings.push(TraceabilityFinding {
                path: path.clone(),
                line: 1,
                kind: KIND_MISSING_PRINCIPLES_IMPLEMENTED.to_string(),
                message:
                    "convention is missing required \"## Principles Implemented/Respected\" heading"
                        .to_string(),
            });
        }
    }
    Ok(findings)
}

/// Checks that every Markdown file under `root` contains both
/// `## Principles Implemented/Respected` and
/// `## Conventions Implemented/Respected` headings.
///
/// # Errors
///
/// Returns an error when a file cannot be read.
fn audit_development(
    fs: &dyn Fs,
    root: &Path,
) -> std::result::Result<Vec<TraceabilityFinding>, Error> {
    let files = list_governance_markdown(fs, root)?;
    let mut findings = Vec::new();
    for path in files {
        let data = fs
            .read_to_string(Path::new(&path))
            .with_context(|| format!("read {path}"))?;
        if !principles_re().is_match(&data) {
            findings.push(TraceabilityFinding {
                path: path.clone(),
                line: 1,
                kind: KIND_MISSING_PRINCIPLES_IMPLEMENTED.to_string(),
                message: "development doc is missing required \"## Principles Implemented/Respected\" heading"
                    .to_string(),
            });
        }
        if !conventions_re().is_match(&data) {
            findings.push(TraceabilityFinding {
                path: path.clone(),
                line: 1,
                kind: KIND_MISSING_CONVENTIONS_IMPLEMENTED.to_string(),
                message: "development doc is missing required \"## Conventions Implemented/Respected\" heading"
                    .to_string(),
            });
        }
    }
    Ok(findings)
}

/// Checks that every non-exempt Markdown file under `root` contains at least
/// one `.claude/agents/<name>.md` reference.
///
/// Files listed in [`META_EXEMPT`] are skipped.
///
/// # Errors
///
/// Returns an error when a file cannot be read.
fn audit_workflows(
    fs: &dyn Fs,
    root: &Path,
) -> std::result::Result<Vec<TraceabilityFinding>, Error> {
    let files = list_governance_markdown(fs, root)?;
    let mut findings = Vec::new();
    for path in files {
        let rel = Path::new(&path)
            .strip_prefix(root)
            .map(|p| p.to_string_lossy().replace('\\', "/"))
            .unwrap_or_default();
        if META_EXEMPT.contains(&rel.as_str()) {
            continue;
        }
        let data = fs
            .read_to_string(Path::new(&path))
            .with_context(|| format!("read {path}"))?;
        if !agent_ref_re().is_match(&data) {
            let line = first_non_empty_line(&data);
            findings.push(TraceabilityFinding {
                path: path.clone(),
                line,
                kind: KIND_MISSING_AGENT_REFERENCE.to_string(),
                message: "workflow does not reference any .claude/agents/<name>.md file"
                    .to_string(),
            });
        }
    }
    Ok(findings)
}

/// Returns the 1-based line number of the first non-empty line in `data`.
///
/// Returns `1` when `data` is empty or consists entirely of blank lines.
fn first_non_empty_line(data: &str) -> usize {
    for (idx, line) in data.split('\n').enumerate() {
        if !line.trim().is_empty() {
            return idx + 1;
        }
    }
    1
}

/// Returns a sorted list of paths to all `.md` files under `root`, excluding
/// `README.md` files.
///
/// Returns an empty `Vec` when `root` does not exist.
///
/// # Errors
///
/// Returns an error when the directory walk fails.
fn list_governance_markdown(fs: &dyn Fs, root: &Path) -> std::result::Result<Vec<String>, Error> {
    let mut files: Vec<String> = fs
        .walk_files(root, &[])
        .into_iter()
        .filter(|p| {
            p.file_name().is_some_and(|n| {
                let n = n.to_string_lossy();
                n.ends_with(".md") && n != "README.md"
            })
        })
        .filter(|p| !is_split_child(p))
        .map(|p| p.to_string_lossy().to_string())
        .collect();
    files.sort();
    Ok(files)
}

/// Reports whether `path` is a progressive-disclosure split child.
///
/// Splitting a governance document produces `<name>.md` (the parent, which
/// keeps the traceability headings) plus a `<name>/` directory of `NN-<slug>.md`
/// children indexed by a sibling `README.md`. A child carries one section of
/// the parent and structurally cannot repeat the parent's
/// `## Principles Implemented/Respected` / `## Conventions Implemented/Respected`
/// / `## Vision Supported` headings, so requiring them of every child would
/// make the audit report thousands of unfixable findings. The parent is still
/// checked — the requirement is enforced exactly once per document.
fn is_split_child(path: &Path) -> bool {
    let Some(name) = path.file_name().map(|n| n.to_string_lossy().to_string()) else {
        return false;
    };
    let numbered = name.len() > 3
        && name.as_bytes()[0].is_ascii_digit()
        && name.as_bytes()[1].is_ascii_digit()
        && name.as_bytes()[2] == b'-';
    if !numbered {
        return false;
    }
    path.parent()
        .is_some_and(|dir| dir.join("README.md").is_file())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use std::fs;
    use tempfile::TempDir;

    fn write(p: &Path, content: &str) {
        fs::create_dir_all(p.parent().unwrap()).unwrap();
        fs::write(p, content).unwrap();
    }

    #[test]
    fn split_children_are_exempt_but_their_parent_is_not() {
        let tmp = TempDir::new().unwrap();
        // Parent keeps the heading requirement...
        write(
            &tmp.path().join("repo-governance/principles/p.md"),
            "# P\n\nno heading here\n",
        );
        // ...its split children are indexed by a README and are exempt.
        write(
            &tmp.path().join("repo-governance/principles/p/README.md"),
            "# P\n\n- [One](./01-one.md) — x\n",
        );
        write(
            &tmp.path().join("repo-governance/principles/p/01-one.md"),
            "# One\n\nno heading here either\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert_eq!(
            findings.len(),
            1,
            "only the parent may be flagged, got {findings:?}"
        );
        assert!(findings[0].path.ends_with("principles/p.md"));
    }

    #[test]
    fn numbered_file_without_a_sibling_readme_is_still_checked() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("repo-governance/principles/01-standalone.md"),
            "# S\n\nno heading\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert_eq!(findings.len(), 1, "got {findings:?}");
    }

    #[test]
    fn principle_passes_when_vision_section_present() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/principles/p.md"),
            "# P\n\n## Vision Supported\n\nx\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn principle_missing_vision_emits_finding() {
        let tmp = TempDir::new().unwrap();
        write(&tmp.path().join("repo-governance/principles/p.md"), "# P\n");
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == KIND_MISSING_VISION_SUPPORTED)
        );
    }

    #[test]
    fn convention_missing_principles_emits_finding() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/conventions/c.md"),
            "# C\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == KIND_MISSING_PRINCIPLES_IMPLEMENTED)
        );
    }

    #[test]
    fn development_requires_both_sections() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/development/d.md"),
            "# D\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        let kinds: Vec<&str> = findings.iter().map(|f| f.kind.as_str()).collect();
        assert!(kinds.contains(&KIND_MISSING_PRINCIPLES_IMPLEMENTED));
        assert!(kinds.contains(&KIND_MISSING_CONVENTIONS_IMPLEMENTED));
    }

    #[test]
    fn development_passes_with_both_sections() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/development/d.md"),
            "# D\n\n## Principles Implemented/Respected\n\n## Conventions Implemented/Respected\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn workflow_missing_agent_ref_emits_finding() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/workflows/w.md"),
            "# W\n\nno agent here\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == KIND_MISSING_AGENT_REFERENCE)
        );
    }

    #[test]
    fn workflow_passes_when_agent_referenced() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/workflows/w.md"),
            "# W\n\nSee `.claude/agents/foo-bar.md`\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn workflow_passes_when_agent_referenced_in_a_subdirectory() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/workflows/w.md"),
            "# W\n\nSee `.claude/agents/pr-review/pr-review-fixer.md`\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(
            findings.is_empty(),
            "nested agent paths are the real on-disk layout and must satisfy the reference check"
        );
    }

    #[test]
    fn meta_exempt_paths_skip_agent_check() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("repo-governance/workflows/meta/execution-modes.md"),
            "# meta\n\nno agent ref needed\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn readme_files_are_exempt() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/principles/README.md"),
            "# Index\n",
        );
        let findings = audit_traceability(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn first_non_empty_line_skips_blanks() {
        assert_eq!(first_non_empty_line("\n\nhello\n"), 3);
        assert_eq!(first_non_empty_line("hello\n"), 1);
        assert_eq!(first_non_empty_line(""), 1);
    }
}
