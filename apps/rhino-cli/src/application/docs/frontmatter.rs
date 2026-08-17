//! YAML frontmatter validator for repository markdown files.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/docs/frontmatter.go`.
//!
//! Files in `docs/explanation/software-engineering/` are checked against the
//! full software schema (title, description, category, subcategory, tags).
//! Files under `repo-governance/` subdirectories are checked against the
//! lighter governance schema (title required, description recommended).

use std::fs;
use std::path::Path;

use anyhow::{Error, anyhow};
use walkdir::WalkDir;

/// A single frontmatter validation finding for a markdown file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DocsFrontmatterFinding {
    /// Path to the file that contains the finding.
    pub file: String,
    /// Severity string: `"fail"` or `"warn"`.
    pub severity: String,
    /// Machine-readable kind identifier (e.g. `"missing-title"`).
    pub kind: String,
    /// Human-readable description of the issue.
    pub message: String,
}

/// Severity string for findings that must block the pipeline.
const SEVERITY_FAIL: &str = "fail";
/// Severity string for findings that are advisory warnings only.
const SEVERITY_WARN: &str = "warn";

/// Finding kind for files whose frontmatter block is not valid YAML.
const KIND_INVALID_YAML: &str = "invalid-yaml";
/// Finding kind for files that have no `---`-delimited frontmatter block at all.
const KIND_MISSING_FRONTMATTER: &str = "missing-frontmatter";
/// Finding kind for frontmatter blocks that are missing the `title` field.
const KIND_MISSING_TITLE: &str = "missing-title";
/// Finding kind for frontmatter blocks that are missing the `description` field.
const KIND_MISSING_DESCRIPTION: &str = "missing-description";
/// Finding kind for governance-doc frontmatter blocks missing `when_to_use`.
///
/// FR-4.1: dark-launched at WARN severity in Phase 1 (this check exists and
/// reports, but does not fail the gate); armed to FAIL at Phase 9/16 — see
/// `tech-docs.md` §5 "Dark-launch sequencing".
const KIND_MISSING_WHEN_TO_USE: &str = "missing-when-to-use";
/// Finding kind for frontmatter blocks that are missing the `category` field.
const KIND_MISSING_CATEGORY: &str = "missing-category";
/// Finding kind for frontmatter blocks that are missing the `subcategory` field.
const KIND_MISSING_SUBCATEGORY: &str = "missing-subcategory";
/// Finding kind for frontmatter blocks that are missing the `tags` field.
const KIND_MISSING_TAGS: &str = "missing-tags";
/// Finding kind for frontmatter blocks whose `category` value is not in the allowed set.
const KIND_WRONG_CATEGORY_VALUE: &str = "wrong-category-value";
/// Finding kind for frontmatter blocks whose `category` is `"software"` (deprecated).
const KIND_CATEGORY_DEPRECATED: &str = "category-deprecated";

/// The allowed values for the `category` frontmatter field (Diátaxis framework).
const VALID_CATEGORIES: &[&str] = &["tutorial", "how-to", "reference", "explanation"];

/// Path fragment that identifies software-engineering explanation documents.
const SOFTWARE_DOC_PREFIX: &str = "docs/explanation/software-engineering/";

/// Path fragments that identify governance documents.
const GOVERNANCE_DOC_PREFIXES: &[&str] = &[
    "repo-governance/conventions/",
    "repo-governance/principles/",
    "repo-governance/development/",
    "repo-governance/workflows/",
];

/// Directory names that are skipped during recursive walks.
const SKIP_DIRS: &[&str] = &["node_modules", ".git", ".next", "dist", "build", "target"];

/// Classifies a markdown file as belonging to a known documentation area.
#[derive(Clone, Copy)]
enum DocArea {
    /// The file is not in any recognised documentation area.
    Unknown,
    /// The file is in `docs/explanation/software-engineering/`.
    Software,
    /// The file is under one of the `repo-governance/` sub-trees.
    Governance,
}

/// Validates the YAML frontmatter of every markdown file reachable from `paths`.
///
/// Files outside the recognised documentation areas (`SOFTWARE_DOC_PREFIX`,
/// `GOVERNANCE_DOC_PREFIXES`) are silently skipped.  The returned list is
/// sorted by file path, then by finding kind.
///
/// # Errors
///
/// Returns an error when `paths` is empty, or when a file cannot be read.
pub fn validate_docs_frontmatter(
    paths: &[String],
) -> std::result::Result<Vec<DocsFrontmatterFinding>, Error> {
    if paths.is_empty() {
        return Err(anyhow!("at least one path is required"));
    }
    let mut findings = Vec::new();
    for root in paths {
        findings.extend(walk_frontmatter_path(root)?);
    }
    findings.sort_by(|a, b| a.file.cmp(&b.file).then(a.kind.cmp(&b.kind)));
    Ok(findings)
}

/// Walks `root` recursively and collects frontmatter findings from every
/// markdown file in a recognised documentation area.
///
/// Returns an empty list if `root` does not exist on the filesystem.
///
/// # Errors
///
/// Returns an error when a markdown file cannot be read.
fn walk_frontmatter_path(root: &str) -> std::result::Result<Vec<DocsFrontmatterFinding>, Error> {
    let root_p = Path::new(root);
    if !root_p.exists() {
        return Ok(Vec::new());
    }
    let mut findings = Vec::new();
    let walker = WalkDir::new(root_p).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy().to_string();
            !SKIP_DIRS.contains(&name.as_str())
        } else {
            true
        }
    });
    for entry in walker.flatten() {
        if !entry.file_type().is_file() {
            continue;
        }
        let name = entry.file_name().to_string_lossy().to_string();
        if !name.ends_with(".md") {
            continue;
        }
        let path = entry.path();
        let area = classify_doc_area(&path.to_string_lossy());
        if matches!(area, DocArea::Unknown) {
            continue;
        }
        findings.extend(scan_frontmatter_file(&path.to_string_lossy(), area)?);
    }
    Ok(findings)
}

/// Determines which documentation area `path` belongs to.
///
/// Returns [`DocArea::Unknown`] when the path does not match any known prefix.
fn classify_doc_area(path: &str) -> DocArea {
    let slashed = path.replace('\\', "/");
    if slashed.contains(SOFTWARE_DOC_PREFIX) {
        return DocArea::Software;
    }
    for prefix in GOVERNANCE_DOC_PREFIXES {
        if slashed.contains(prefix) {
            return DocArea::Governance;
        }
    }
    DocArea::Unknown
}

/// Reads `path`, extracts the frontmatter block, parses it as YAML, and
/// delegates to the area-specific schema validator.
///
/// Returns a single `missing-frontmatter` finding when no `---` fence is found,
/// or a single `invalid-yaml` finding when the block is not valid YAML.
///
/// # Errors
///
/// Returns an error when the file cannot be read from disk.
fn scan_frontmatter_file(
    path: &str,
    area: DocArea,
) -> std::result::Result<Vec<DocsFrontmatterFinding>, Error> {
    let data = fs::read_to_string(path)?;
    let Some(frontmatter) = extract_frontmatter(&data) else {
        return Ok(vec![DocsFrontmatterFinding {
            file: path.to_string(),
            severity: SEVERITY_FAIL.to_string(),
            kind: KIND_MISSING_FRONTMATTER.to_string(),
            message: "file has no YAML frontmatter (delimited by `---` fences)".to_string(),
        }]);
    };
    let parsed: serde_norway::Value = match serde_norway::from_str(&frontmatter) {
        Ok(v) => v,
        Err(e) => {
            return Ok(vec![DocsFrontmatterFinding {
                file: path.to_string(),
                severity: SEVERITY_FAIL.to_string(),
                kind: KIND_INVALID_YAML.to_string(),
                message: format!("frontmatter is not valid YAML: {e}"),
            }]);
        }
    };
    Ok(match area {
        DocArea::Software => validate_software_schema(path, &parsed),
        DocArea::Governance => validate_governance_schema(path, &parsed),
        DocArea::Unknown => Vec::new(),
    })
}

/// Extracts the YAML content between the first pair of `---` fences.
///
/// Returns `None` when the file does not begin with `---` or has no closing fence.
///
/// `pub(crate)` — reused by
/// `application::governance::readme_index::generate_readme_index` (FR-3.12)
/// to read/preserve a README index file's own frontmatter block when
/// regenerating its body, rather than re-implementing frontmatter-fence
/// extraction a second time.
pub(crate) fn extract_frontmatter(content: &str) -> Option<String> {
    let lines: Vec<&str> = content.split('\n').collect();
    if lines.is_empty() || lines[0].trim() != "---" {
        return None;
    }
    for i in 1..lines.len() {
        if lines[i].trim() == "---" {
            return Some(lines[1..i].join("\n"));
        }
    }
    None
}

/// Validates the full software-engineering frontmatter schema.
///
/// Required fields: `title`, `description`, `category` (one of
/// [`VALID_CATEGORIES`]), `subcategory`, `tags` (non-empty list).
fn validate_software_schema(path: &str, fm: &serde_norway::Value) -> Vec<DocsFrontmatterFinding> {
    let mut findings = Vec::new();
    if !has_non_empty_string(fm, "title") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_TITLE,
            "required field \"title\" is missing or empty",
        ));
    }
    if !has_non_empty_string(fm, "description") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_DESCRIPTION,
            "required field \"description\" is missing or empty",
        ));
    }
    if has_non_empty_string(fm, "category") {
        let v = string_value(fm.get("category"));
        if VALID_CATEGORIES.contains(&v.as_str()) {
            // ok
        } else if v == "software" {
            findings.push(DocsFrontmatterFinding {
                file: path.to_string(),
                severity: SEVERITY_WARN.to_string(),
                kind: KIND_CATEGORY_DEPRECATED.to_string(),
                message: "field \"category\" value \"software\" is deprecated; use one of: tutorial, how-to, reference, explanation".to_string(),
            });
        } else {
            findings.push(DocsFrontmatterFinding {
                file: path.to_string(),
                severity: SEVERITY_FAIL.to_string(),
                kind: KIND_WRONG_CATEGORY_VALUE.to_string(),
                message: format!(
                    "field \"category\" must be one of: tutorial, how-to, reference, explanation; found \"{v}\""
                ),
            });
        }
    } else {
        findings.push(mk_fail(
            path,
            KIND_MISSING_CATEGORY,
            "required field \"category\" is missing or empty",
        ));
    }
    if !has_non_empty_string(fm, "subcategory") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_SUBCATEGORY,
            "required field \"subcategory\" is missing or empty",
        ));
    }
    if !has_non_empty_list(fm, "tags") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_TAGS,
            "required field \"tags\" must be a non-empty list",
        ));
    }
    findings
}

/// Validates the lighter governance-document frontmatter schema.
///
/// `title` is required (fail); `description` is recommended (warn).
fn validate_governance_schema(path: &str, fm: &serde_norway::Value) -> Vec<DocsFrontmatterFinding> {
    let mut findings = Vec::new();
    if !has_non_empty_string(fm, "title") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_TITLE,
            "required field \"title\" is missing or empty",
        ));
    }
    if !has_non_empty_string(fm, "description") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_DESCRIPTION,
            "recommended field \"description\" is missing or empty",
        ));
    }
    // FR-4 armed at Phase 9 (ose-public) / Phase 16 (ose-private): `when_to_use` is
    // now FAIL-severity, per plans/done/2026-08-15__optimize-governance-md `tech-docs.md`
    // §5 "Dark-launch sequencing" — was WARN-severity from Phase 1 through Phase 8.
    if !has_non_empty_string(fm, "when_to_use") {
        findings.push(mk_fail(
            path,
            KIND_MISSING_WHEN_TO_USE,
            "recommended field \"when_to_use\" is missing or empty",
        ));
    }
    findings
}

/// Constructs a `fail`-severity [`DocsFrontmatterFinding`].
fn mk_fail(path: &str, kind: &str, message: &str) -> DocsFrontmatterFinding {
    DocsFrontmatterFinding {
        file: path.to_string(),
        severity: SEVERITY_FAIL.to_string(),
        kind: kind.to_string(),
        message: message.to_string(),
    }
}

/// Returns `true` when `fm[key]` is a non-empty, non-whitespace-only string.
fn has_non_empty_string(fm: &serde_norway::Value, key: &str) -> bool {
    let v = fm.get(key);
    let s = string_value(v);
    !s.trim().is_empty()
}

/// Coerces a YAML value to a `String` for display and comparison purposes.
///
/// `None` and `Null` map to an empty string.
fn string_value(v: Option<&serde_norway::Value>) -> String {
    match v {
        None | Some(serde_norway::Value::Null) => String::new(),
        Some(serde_norway::Value::String(s)) => s.clone(),
        Some(serde_norway::Value::Bool(b)) => b.to_string(),
        Some(serde_norway::Value::Number(n)) => n.to_string(),
        Some(other) => serde_norway::to_string(other)
            .unwrap_or_default()
            .trim()
            .to_string(),
    }
}

/// Returns `true` when `fm[key]` is a YAML sequence with at least one element.
fn has_non_empty_list(fm: &serde_norway::Value, key: &str) -> bool {
    match fm.get(key) {
        Some(serde_norway::Value::Sequence(list)) => !list.is_empty(),
        _ => false,
    }
}

/// Returns `true` when any finding in the slice has severity `"fail"`.
pub fn has_fail_findings(findings: &[DocsFrontmatterFinding]) -> bool {
    findings.iter().any(|f| f.severity == SEVERITY_FAIL)
}

/// Counts the number of findings in `findings` that match the given severity string.
pub fn count_severity(findings: &[DocsFrontmatterFinding], sev: &str) -> usize {
    findings.iter().filter(|f| f.severity == sev).count()
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// Creates a file at `p`, making parent directories as needed.
    fn write(p: &Path, content: &str) {
        fs::create_dir_all(p.parent().unwrap()).unwrap();
        fs::write(p, content).unwrap();
    }

    /// Verifies that an empty paths slice returns an error.
    #[test]
    fn errors_on_empty_paths() {
        let err = validate_docs_frontmatter(&[]).unwrap_err();
        assert!(err.to_string().contains("at least one path"));
    }

    /// Verifies that a file with no frontmatter emits a `missing-frontmatter` fail finding.
    #[test]
    fn missing_frontmatter_emits_fail() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("docs/explanation/software-engineering/foo.md"),
            "# No frontmatter\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.iter().any(|f| f.kind == KIND_MISSING_FRONTMATTER));
    }

    /// Verifies that a file with all required software fields passes without findings.
    #[test]
    fn software_full_schema_passes() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("docs/explanation/software-engineering/foo.md"),
            "---\ntitle: T\ndescription: D\ncategory: explanation\nsubcategory: S\ntags: [a]\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.is_empty());
    }

    /// Verifies that missing required software fields each produce a fail finding.
    #[test]
    fn software_missing_required_fields_emit_fails() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("docs/explanation/software-engineering/foo.md"),
            "---\ntitle: T\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        let kinds: Vec<&str> = findings.iter().map(|f| f.kind.as_str()).collect();
        assert!(kinds.contains(&KIND_MISSING_DESCRIPTION));
        assert!(kinds.contains(&KIND_MISSING_CATEGORY));
        assert!(kinds.contains(&KIND_MISSING_SUBCATEGORY));
        assert!(kinds.contains(&KIND_MISSING_TAGS));
    }

    /// Verifies that the deprecated `"software"` category value emits a warn finding.
    #[test]
    fn software_deprecated_category_emits_warn() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("docs/explanation/software-engineering/foo.md"),
            "---\ntitle: T\ndescription: D\ncategory: software\nsubcategory: S\ntags: [a]\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        let f = findings
            .iter()
            .find(|f| f.kind == KIND_CATEGORY_DEPRECATED)
            .unwrap();
        assert_eq!(f.severity, SEVERITY_WARN);
    }

    /// Verifies that an unrecognised category value emits a fail finding.
    #[test]
    fn software_wrong_category_emits_fail() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("docs/explanation/software-engineering/foo.md"),
            "---\ntitle: T\ndescription: D\ncategory: random\nsubcategory: S\ntags: [a]\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.iter().any(|f| f.kind == KIND_WRONG_CATEGORY_VALUE));
    }

    /// Verifies that a governance file with no `title` or `description` gets a fail
    /// for each — FR-4 armed at Phase 9/16.
    #[test]
    fn governance_title_and_description_both_fail() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/conventions/foo.md"),
            "---\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        let kinds: Vec<&str> = findings.iter().map(|f| f.kind.as_str()).collect();
        assert!(kinds.contains(&KIND_MISSING_TITLE));
        let desc = findings
            .iter()
            .find(|f| f.kind == KIND_MISSING_DESCRIPTION)
            .unwrap();
        assert_eq!(desc.severity, SEVERITY_FAIL);
    }

    /// Verifies that a governance file with all recommended fields passes.
    #[test]
    fn governance_full_schema_passes() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/principles/foo.md"),
            "---\ntitle: T\ndescription: D\nwhen_to_use: Use when W.\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.is_empty());
    }

    /// Verifies that files outside recognised areas are silently skipped.
    #[test]
    fn unknown_area_passes() {
        let tmp = TempDir::new().unwrap();
        write(&tmp.path().join("random/foo.md"), "no frontmatter\n");
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.is_empty());
    }

    /// Verifies that invalid YAML in the frontmatter block emits an `invalid-yaml` fail.
    #[test]
    fn invalid_yaml_emits_fail() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path()
                .join("docs/explanation/software-engineering/foo.md"),
            "---\ntitle: T\n  invalid: : :\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.iter().any(|f| f.kind == KIND_INVALID_YAML));
    }

    /// Verifies that [`has_fail_findings`] correctly identifies the presence or absence
    /// of fail-severity findings.
    #[test]
    fn has_fail_findings_detects_severity() {
        let f1 = DocsFrontmatterFinding {
            file: "a.md".to_string(),
            severity: SEVERITY_WARN.to_string(),
            kind: "x".to_string(),
            message: "m".to_string(),
        };
        let f2 = DocsFrontmatterFinding {
            file: "b.md".to_string(),
            severity: SEVERITY_FAIL.to_string(),
            kind: "y".to_string(),
            message: "m".to_string(),
        };
        assert!(!has_fail_findings(std::slice::from_ref(&f1)));
        assert!(has_fail_findings(&[f1, f2]));
    }

    // -----------------------------------------------------------------------
    // Phase 9 (armed) — plans/done/2026-08-15__optimize-governance-md
    //
    // FR-4: `KIND_MISSING_WHEN_TO_USE` was WARN-severity (dark-launched) from
    // Phase 1 through Phase 8; Phase 9 (ose-public) / Phase 16 (ose-private)
    // arms it to FAIL-severity, matching `description`'s existing severity.
    // -----------------------------------------------------------------------

    /// Verifies that a governance file with no `when_to_use` frontmatter
    /// produces a FAIL-severity `KIND_MISSING_WHEN_TO_USE` finding — FR-4
    /// armed (see prd.md FR-4 "Dark-launch sequencing").
    #[test]
    fn governance_missing_when_to_use_fails() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp.path().join("repo-governance/conventions/foo.md"),
            "---\ntitle: T\ndescription: D\n---\nbody\n",
        );
        let findings =
            validate_docs_frontmatter(&[tmp.path().to_string_lossy().to_string()]).unwrap();
        let finding = findings
            .iter()
            .find(|f| f.kind == KIND_MISSING_WHEN_TO_USE)
            .expect(
                "FR-4 armed: a governance file with no when_to_use must produce a \
                 KIND_MISSING_WHEN_TO_USE finding",
            );
        assert_eq!(
            finding.severity, SEVERITY_FAIL,
            "FR-4 armed at Phase 9/16: missing when_to_use is FAIL-severity"
        );
    }
}
