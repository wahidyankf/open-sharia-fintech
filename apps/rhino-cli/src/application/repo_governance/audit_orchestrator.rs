//! Audit orchestrator for repository governance.
//!
//! Ported from `apps/rhino-cli/internal/repo-governance/audit_orchestrator.go`.
//!
//! Runs the deterministic governance audits in fixed order, normalises
//! per-category findings to [`AuditFinding`], and aggregates them into an
//! [`AuditEnvelope`].

use std::collections::BTreeMap;
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

use anyhow::Error;
use chrono::Utc;
use regex::Regex;
use serde::Serialize;
use sha2::{Digest, Sha256};

use super::instruction_size::{self, Severity as InstructionSeverity};
use super::layer_coherence::audit_layer_coherence;
use super::traceability_audit::audit_traceability;
use super::vendor_audit::walk_governance_scope as audit_vendor_walk;
use crate::application::fs::port::Fs;
use crate::infrastructure::fs::real::RealFs;

/// JSON schema identifier embedded in every [`AuditEnvelope`].
pub const AUDIT_ENVELOPE_SCHEMA: &str = "rhino-cli/repo-governance-audit/v1";
/// Severity label applied to all findings emitted by this orchestrator.
const AUDIT_SEVERITY_HIGH: &str = "high";
/// Criticality label applied to all findings emitted by this orchestrator.
const AUDIT_CRITICALITY_HIGH: &str = "HIGH";

/// Returns the fixed ordered slice of audit category names.
///
/// Categories are executed in this order by [`run_audit`].
pub fn audit_category_order() -> &'static [&'static str] {
    &[
        "layer-coherence",
        "traceability-audit",
        "vendor-audit",
        "instruction-size",
    ]
}

/// Maps an audit category `name` to the CLI sub-command that runs it.
///
/// Returns an empty string for unrecognised names.
fn audit_category_command(name: &str) -> &'static str {
    match name {
        "layer-coherence" => "repo-governance validate layer-coherence",
        "traceability-audit" => "repo-governance validate traceability",
        "vendor-audit" => "repo-governance validate vendor",
        "instruction-size" => "harness instruction-size validate",
        _ => "",
    }
}

/// Configuration options for a single [`run_audit`] invocation.
#[derive(Debug, Clone, Default)]
pub struct AuditOptions {
    /// Absolute path to the repository root used to resolve relative search paths.
    pub repo_root: PathBuf,
    /// Category names to skip entirely.
    pub skip: Vec<String>,
    /// When non-empty only these category names are executed (allowlist).
    pub include_only: Vec<String>,
    /// Override for the `ran_at` timestamp (RFC 3339). `None` defaults to `Utc::now()`.
    pub now: Option<String>,
    /// Path to a known-false-positives Markdown file. Defaults to
    /// `generated-reports/.known-false-positives.md` under `repo_root`.
    pub known_false_positives_path: Option<PathBuf>,
    /// Glob patterns; findings whose `file` field matches are excluded.
    pub exclude_globs: Vec<String>,
}

/// Top-level JSON envelope returned by [`run_audit`].
#[derive(Debug, Clone, Serialize)]
pub struct AuditEnvelope {
    /// Schema identifier; always `AUDIT_ENVELOPE_SCHEMA`.
    pub schema: String,
    /// Overall outcome: `"ok"` (zero findings) or `"failed"`.
    pub status: String,
    /// Detailed audit results.
    pub result: AuditResult,
}

/// Detailed outcome of a [`run_audit`] call.
#[derive(Debug, Clone, Serialize)]
pub struct AuditResult {
    /// Short git SHA of `HEAD` at audit time, or `"unknown"`.
    pub git_sha: String,
    /// RFC 3339 timestamp at which the audit ran.
    pub ran_at: String,
    /// Total number of findings across all categories.
    pub total_findings: usize,
    /// Finding counts keyed by severity string.
    pub by_severity: BTreeMap<String, usize>,
    /// Finding counts keyed by category name.
    pub by_category: BTreeMap<String, usize>,
    /// Per-category results in execution order.
    pub categories: Vec<AuditCategoryResult>,
    /// Findings that were suppressed via the known-false-positives list.
    pub skipped_false_positives: Vec<AuditFinding>,
}

/// Result for a single audit category.
#[derive(Debug, Clone, Serialize)]
pub struct AuditCategoryResult {
    /// Category name (matches an entry in [`audit_category_order`]).
    pub name: String,
    /// CLI sub-command that runs this category.
    pub command: String,
    /// `true` when `findings` is empty after false-positive filtering.
    pub passed: bool,
    /// All findings for this category.
    pub findings: Vec<AuditFinding>,
}

/// A single governance finding produced by any audit category.
#[derive(Debug, Clone, Serialize)]
pub struct AuditFinding {
    /// Stable key used for false-positive suppression (format:
    /// `<category>|<file>|<hash8>`).
    pub key: String,
    /// Severity label (currently always `"high"`).
    pub severity: String,
    /// Criticality label (currently always `"HIGH"`).
    pub criticality: String,
    /// Path of the file that triggered the finding; omitted when empty.
    #[serde(skip_serializing_if = "str::is_empty")]
    pub file: String,
    /// 1-based line number within `file`; omitted when zero.
    #[serde(skip_serializing_if = "skip_zero")]
    pub line: usize,
    /// Human-readable description of the finding.
    pub message: String,
}

/// Returns `true` when `n` is zero; used as a `serde` skip predicate.
#[allow(clippy::trivially_copy_pass_by_ref)]
fn skip_zero(n: &usize) -> bool {
    *n == 0
}

/// Runs all governance audits described by `opts` and returns a consolidated
/// [`AuditEnvelope`].
///
/// Categories listed in `opts.skip` are not executed.  When `opts.include_only`
/// is non-empty only those categories are executed.  Known false positives
/// loaded from the file referenced by `opts.known_false_positives_path` are
/// moved from `categories` findings into `skipped_false_positives`.
///
/// # Errors
///
/// Returns an error if any category fails to execute (e.g., an IO error while
/// walking the filesystem or deserialising YAML).
pub fn run_audit(fs: &dyn Fs, opts: &AuditOptions) -> std::result::Result<AuditEnvelope, Error> {
    let ran_at = opts
        .now
        .clone()
        .unwrap_or_else(|| Utc::now().format("%Y-%m-%dT%H:%M:%SZ").to_string());

    let mut categories: Vec<AuditCategoryResult> = Vec::new();
    for &name in audit_category_order() {
        if opts.skip.iter().any(|s| s == name) {
            continue;
        }
        if !opts.include_only.is_empty() && !opts.include_only.iter().any(|s| s == name) {
            continue;
        }
        let mut findings = run_category(fs, name, opts)?;
        findings = filter_excluded(findings, &opts.exclude_globs);
        sort_audit_findings(&mut findings);
        categories.push(AuditCategoryResult {
            name: name.to_string(),
            command: audit_category_command(name).to_string(),
            passed: findings.is_empty(),
            findings,
        });
    }

    let skip_set = load_known_false_positives(fs, opts)?;
    let (categories, skipped) = partition_false_positives(categories, &skip_set);

    let mut total = 0usize;
    let mut by_sev: BTreeMap<String, usize> = BTreeMap::new();
    let mut by_cat: BTreeMap<String, usize> = BTreeMap::new();
    for c in &categories {
        total += c.findings.len();
        by_cat.insert(c.name.clone(), c.findings.len());
        for f in &c.findings {
            *by_sev.entry(f.severity.clone()).or_insert(0) += 1;
        }
    }

    let status = if total > 0 { "failed" } else { "ok" }.to_string();
    let git_sha = read_git_sha(&opts.repo_root);

    Ok(AuditEnvelope {
        schema: AUDIT_ENVELOPE_SCHEMA.to_string(),
        status,
        result: AuditResult {
            git_sha,
            ran_at,
            total_findings: total,
            by_severity: by_sev,
            by_category: by_cat,
            categories,
            skipped_false_positives: skipped,
        },
    })
}

/// Dispatches a single audit `name` to the appropriate runner.
///
/// # Errors
///
/// Returns an error for unrecognised category names or when the delegated
/// runner propagates an IO or parse error.
fn run_category(
    fs: &dyn Fs,
    name: &str,
    opts: &AuditOptions,
) -> std::result::Result<Vec<AuditFinding>, Error> {
    match name {
        "layer-coherence" => {
            let findings = audit_layer_coherence(fs, &opts.repo_root)?;
            Ok(findings
                .into_iter()
                .map(|f| new_audit_finding(name, &f.file, 0, &f.message))
                .collect())
        }
        "traceability-audit" => {
            let findings = audit_traceability(fs, &opts.repo_root)?;
            Ok(findings
                .into_iter()
                .map(|f| new_audit_finding(name, &f.path, f.line, &f.message))
                .collect())
        }
        "vendor-audit" => {
            let findings = audit_vendor_walk(fs, &opts.repo_root)?;
            Ok(findings
                .into_iter()
                .map(|f| {
                    let msg = format!("forbidden term '{}' → use '{}'", f.r#match, f.replacement);
                    new_audit_finding(name, &f.path, f.line, &msg)
                })
                .collect())
        }
        "instruction-size" => Ok(audit_instruction_size(&opts.repo_root)),
        _ => Err(anyhow::anyhow!("unknown category {name}")),
    }
}

/// Checks all instruction-file size surfaces (per `repo-config.yml`'s
/// `instruction-size:` section and harness registry) and returns only the
/// hard-`Fail` findings as [`AuditFinding`]s. `Warn`-severity findings are
/// advisory (matching `harness instruction-size validate`'s own exit-code
/// gating) and never block this preflight category.
///
/// Returns an empty vector when neither an `instruction-size:` section nor
/// any harness registry `instruction:` surfaces are configured.
fn audit_instruction_size(repo_root: &Path) -> Vec<AuditFinding> {
    let Some(config) = instruction_size::merged_budget_config(repo_root) else {
        return Vec::new();
    };
    let mut findings = instruction_size::check_instruction_sizes(&RealFs, repo_root, &config);
    if let Some(tree_finding) = instruction_size::check_resolved_tree(&RealFs, repo_root, &config) {
        findings.push(tree_finding);
    }
    findings
        .into_iter()
        .filter(|f| f.severity == InstructionSeverity::Fail)
        .map(|f| new_audit_finding("instruction-size", &f.path, 0, &f.message))
        .collect()
}

/// Resolves a search-path list against `repo_root`.
///
/// When `override_paths` is non-empty those paths are used; otherwise
/// `defaults` are used.  Relative paths are joined to `repo_root`; absolute
/// paths are kept as-is.
#[cfg(test)]
fn resolve_paths(repo_root: &Path, override_paths: &[String], defaults: &[&str]) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    let push_resolved = |out: &mut Vec<String>, p: &str| {
        if Path::new(p).is_absolute() {
            out.push(p.to_string());
        } else {
            out.push(go_filepath_join(&repo_root.to_string_lossy(), p));
        }
    };
    if override_paths.is_empty() {
        for p in defaults {
            push_resolved(&mut out, p);
        }
    } else {
        for p in override_paths {
            push_resolved(&mut out, p);
        }
    }
    out
}

/// Mirror Go's `filepath.Join`: lexical join + `path.Clean` (drops `.` and
/// trailing slashes).
#[cfg(test)]
fn go_filepath_join(base: &str, rel: &str) -> String {
    let joined = if base.ends_with('/') {
        format!("{base}{rel}")
    } else {
        format!("{base}/{rel}")
    };
    clean_path(&joined)
}

/// Lexically cleans `p` by resolving `.` and `..` segments and collapsing
/// duplicate slashes — mirrors Go's `path.Clean`.
#[cfg(test)]
#[allow(clippy::collapsible_if, clippy::collapsible_match)]
fn clean_path(p: &str) -> String {
    if p.is_empty() {
        return ".".to_string();
    }
    let absolute = p.starts_with('/');
    let mut stack: Vec<&str> = Vec::new();
    for seg in p.split('/') {
        match seg {
            "" | "." => {}
            ".." => {
                if let Some(last) = stack.last() {
                    if *last != ".." {
                        stack.pop();
                        continue;
                    }
                }
                if !absolute {
                    stack.push("..");
                }
            }
            _ => stack.push(seg),
        }
    }
    let body = stack.join("/");
    if absolute {
        format!("/{body}")
    } else if body.is_empty() {
        ".".to_string()
    } else {
        body
    }
}

/// Returns `true` when `path` matches at least one of the `globs`.
///
/// Supports `/**` suffix (directory subtree) and simple `*` wildcards.
/// Path separators are normalised to `/` before matching.
fn path_matches_any_glob(path: &str, globs: &[String]) -> bool {
    let slashed_path = path.replace('\\', "/");
    for g in globs {
        let slashed_glob = g.replace('\\', "/");
        if let Some(prefix) = slashed_glob.strip_suffix("/**") {
            if slashed_path.contains(&format!("/{prefix}/"))
                || slashed_path.starts_with(&format!("{prefix}/"))
                || slashed_path.ends_with(&format!("/{prefix}"))
            {
                return true;
            }
            for part in slashed_path.split('/') {
                if part == prefix {
                    return true;
                }
            }
            continue;
        }
        // simple wildcard match
        if simple_match(g, path) {
            return true;
        }
        if simple_match(&slashed_glob, &slashed_path) {
            return true;
        }
    }
    false
}

/// Minimal `*`-wildcard glob matcher.
///
/// Splits `pattern` on `*` and verifies that the resulting segments appear in
/// `s` in order, anchoring the first segment to the start and the last to the
/// end.
fn simple_match(pattern: &str, s: &str) -> bool {
    // Minimal `*` glob matcher.
    let parts: Vec<&str> = pattern.split('*').collect();
    if parts.len() == 1 {
        return pattern == s;
    }
    let mut pos = 0;
    for (i, part) in parts.iter().enumerate() {
        if i == 0 {
            if !s[pos..].starts_with(part) {
                return false;
            }
            pos += part.len();
        } else if i == parts.len() - 1 {
            return s[pos..].ends_with(part);
        } else if let Some(idx) = s[pos..].find(part) {
            pos += idx + part.len();
        } else {
            return false;
        }
    }
    true
}

/// Removes findings whose `file` field matches any of `exclude_globs`.
fn filter_excluded(findings: Vec<AuditFinding>, exclude_globs: &[String]) -> Vec<AuditFinding> {
    if exclude_globs.is_empty() {
        return findings;
    }
    findings
        .into_iter()
        .filter(|f| !path_matches_any_glob(&f.file, exclude_globs))
        .collect()
}

/// Constructs a new [`AuditFinding`] with a deterministic `key` derived from
/// `category`, `file`, and `message`.
fn new_audit_finding(category: &str, file: &str, line: usize, message: &str) -> AuditFinding {
    AuditFinding {
        key: build_audit_key(category, file, message),
        severity: AUDIT_SEVERITY_HIGH.to_string(),
        criticality: AUDIT_CRITICALITY_HIGH.to_string(),
        file: file.to_string(),
        line,
        message: message.to_string(),
    }
}

/// Builds a stable, human-readable key for a finding.
///
/// Format: `<category>|<file>|<sha256_prefix_8>` where the hash covers only
/// `message`.
fn build_audit_key(category: &str, file: &str, message: &str) -> String {
    let mut hasher = Sha256::new();
    hasher.update(message.as_bytes());
    let digest = hex::encode(hasher.finalize());
    format!("{category}|{file}|{}", &digest[..8])
}

/// Sorts `findings` by `file`, then by `line`, then by `key` for a stable,
/// deterministic output order.
fn sort_audit_findings(findings: &mut [AuditFinding]) {
    findings.sort_by(|a, b| {
        a.file
            .cmp(&b.file)
            .then(a.line.cmp(&b.line))
            .then(a.key.cmp(&b.key))
    });
}

/// Returns a compiled `Regex` that matches backtick-quoted keys in a
/// known-false-positives Markdown bullet list.
fn known_false_positive_pattern() -> &'static Regex {
    static R: OnceLock<Regex> = OnceLock::new();
    R.get_or_init(|| Regex::new(r"(?m)^\s*-\s+`([^`]+)`").expect("valid hardcoded regex"))
}

/// Loads the set of known-false-positive keys from the Markdown file referenced
/// by `opts`.
///
/// Returns an empty set when the file does not exist (not an error).
///
/// # Errors
///
/// Returns an error when the file exists but cannot be read.
fn load_known_false_positives(
    fs: &dyn Fs,
    opts: &AuditOptions,
) -> std::result::Result<std::collections::HashSet<String>, Error> {
    let path = opts.known_false_positives_path.clone().unwrap_or_else(|| {
        opts.repo_root
            .join("generated-reports")
            .join(".known-false-positives.md")
    });
    let mut set = std::collections::HashSet::new();
    match fs.read_to_string(&path) {
        Ok(content) => {
            for cap in known_false_positive_pattern().captures_iter(&content) {
                set.insert(cap[1].to_string());
            }
            Ok(set)
        }
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Ok(set),
        Err(e) => Err(e.into()),
    }
}

/// Splits each category's findings into kept and skipped sets.
///
/// Any finding whose `key` is present in `skip_set` is moved into the returned
/// `skipped` vector; the rest remain in the category.  The skipped vector is
/// sorted by `key` for deterministic output.
fn partition_false_positives(
    mut categories: Vec<AuditCategoryResult>,
    skip_set: &std::collections::HashSet<String>,
) -> (Vec<AuditCategoryResult>, Vec<AuditFinding>) {
    let mut skipped: Vec<AuditFinding> = Vec::new();
    for c in &mut categories {
        let mut kept: Vec<AuditFinding> = Vec::new();
        for f in c.findings.drain(..) {
            if skip_set.contains(&f.key) {
                skipped.push(f);
            } else {
                kept.push(f);
            }
        }
        c.findings = kept;
        c.passed = c.findings.is_empty();
    }
    skipped.sort_by(|a, b| a.key.cmp(&b.key));
    (categories, skipped)
}

/// Reads the short `HEAD` SHA from the git repository at `repo_root`.
///
/// Returns `"unknown"` when the `git` command fails or produces non-UTF-8
/// output.
fn read_git_sha(repo_root: &Path) -> String {
    let out = std::process::Command::new("git")
        .arg("-C")
        .arg(repo_root)
        .arg("rev-parse")
        .arg("--short")
        .arg("HEAD")
        .output();
    match out {
        Ok(o) if o.status.success() => String::from_utf8_lossy(&o.stdout).trim().to_string(),
        _ => "unknown".to_string(),
    }
}

/// Minimal hex encoding without a `hex` crate dependency.
mod hex {
    use std::fmt::Write as FmtWrite;

    /// Encodes `bytes` as a lowercase hexadecimal string.
    pub fn encode<T: AsRef<[u8]>>(bytes: T) -> String {
        let b = bytes.as_ref();
        let mut s = String::with_capacity(b.len() * 2);
        for byte in b {
            let _ = write!(s, "{byte:02x}");
        }
        s
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use crate::test_support::CwdLock;

    #[test]
    fn build_audit_key_deterministic() {
        let k = build_audit_key("cat", "file.md", "msg");
        assert!(k.starts_with("cat|file.md|"));
        assert_eq!(k.len(), "cat|file.md|".len() + 8);
        // Same inputs → same hash.
        let k2 = build_audit_key("cat", "file.md", "msg");
        assert_eq!(k, k2);
    }

    #[test]
    fn sort_audit_findings_sorts_by_file_then_line() {
        let mut v = vec![
            new_audit_finding("c", "b.md", 5, "m"),
            new_audit_finding("c", "a.md", 10, "m"),
            new_audit_finding("c", "a.md", 5, "m"),
        ];
        sort_audit_findings(&mut v);
        assert_eq!(v[0].file, "a.md");
        assert_eq!(v[0].line, 5);
        assert_eq!(v[1].file, "a.md");
        assert_eq!(v[1].line, 10);
        assert_eq!(v[2].file, "b.md");
    }

    #[test]
    fn resolve_paths_joins_relative() {
        let r = resolve_paths(Path::new("/repo"), &[], &["docs/", "/abs/"]);
        assert!(r[0].contains("/repo/docs"));
        assert!(r[1].starts_with("/abs"));
    }

    #[test]
    fn resolve_paths_override_wins() {
        let r = resolve_paths(Path::new("/repo"), &["custom/".to_string()], &["default/"]);
        assert!(r[0].contains("/repo/custom"));
        assert!(!r.iter().any(|p| p.contains("default")));
    }

    #[test]
    fn path_matches_glob_dir_star() {
        assert!(path_matches_any_glob(
            "archived/foo/bar.md",
            &["archived/**".to_string()]
        ));
        assert!(!path_matches_any_glob(
            "docs/foo.md",
            &["archived/**".to_string()]
        ));
    }

    #[test]
    fn path_matches_glob_simple() {
        // simple_match handles basic wildcard cases.
        assert!(simple_match("*.md", "foo.md"));
        assert!(simple_match("a*b", "axb"));
        assert!(!simple_match("a*b", "ax"));
    }

    #[test]
    fn filter_excluded_drops_matches() {
        let v = vec![
            new_audit_finding("c", "archived/x.md", 0, "m"),
            new_audit_finding("c", "docs/y.md", 0, "m"),
        ];
        let out = filter_excluded(v, &["archived/**".to_string()]);
        assert_eq!(out.len(), 1);
        assert_eq!(out[0].file, "docs/y.md");
    }

    #[test]
    fn partition_false_positives_moves_keys() {
        let f1 = new_audit_finding("c", "a.md", 0, "msg1");
        let f2 = new_audit_finding("c", "b.md", 0, "msg2");
        let cats = vec![AuditCategoryResult {
            name: "c".to_string(),
            command: "x".to_string(),
            passed: false,
            findings: vec![f1.clone(), f2.clone()],
        }];
        let mut skip = std::collections::HashSet::new();
        skip.insert(f1.key.clone());
        let (kept, skipped) = partition_false_positives(cats, &skip);
        assert_eq!(kept[0].findings.len(), 1);
        assert_eq!(skipped.len(), 1);
    }

    #[test]
    fn known_false_positive_pattern_parses_bullets() {
        let content = "- `cat|file.md|abcd1234`\n- `other`\nfoo bar\n";
        let re = known_false_positive_pattern();
        let m: Vec<String> = re
            .captures_iter(content)
            .map(|c| c[1].to_string())
            .collect();
        assert_eq!(m.len(), 2);
        assert_eq!(m[0], "cat|file.md|abcd1234");
    }

    #[test]
    fn skip_zero_helper() {
        assert!(skip_zero(&0));
        assert!(!skip_zero(&5));
    }

    #[test]
    fn clean_path_handles_dot_segments() {
        assert_eq!(clean_path("/a/./b"), "/a/b");
        assert_eq!(clean_path("/a/b/.."), "/a");
        assert_eq!(clean_path("a/./b/"), "a/b");
        assert_eq!(clean_path(""), ".");
        assert_eq!(clean_path("/"), "/");
        assert_eq!(clean_path("./foo/../bar"), "bar");
    }

    #[test]
    fn go_filepath_join_drops_dot() {
        let r = go_filepath_join("/repo", "./.agents");
        assert_eq!(r, "/repo/.agents");
        let r = go_filepath_join("/repo/", "docs/");
        assert_eq!(r, "/repo/docs");
        let r = go_filepath_join("/repo", ".");
        assert_eq!(r, "/repo");
    }

    #[test]
    fn audit_category_command_returns_expected() {
        assert_eq!(
            audit_category_command("layer-coherence"),
            "repo-governance validate layer-coherence"
        );
        assert_eq!(
            audit_category_command("traceability-audit"),
            "repo-governance validate traceability"
        );
        assert_eq!(
            audit_category_command("vendor-audit"),
            "repo-governance validate vendor"
        );
        assert_eq!(
            audit_category_command("instruction-size"),
            "harness instruction-size validate"
        );
        assert_eq!(audit_category_command("unknown"), "");
    }

    #[test]
    fn audit_category_order_is_fixed() {
        let o = audit_category_order();
        assert_eq!(o.len(), 4);
        assert_eq!(o[0], "layer-coherence");
        assert_eq!(o[1], "traceability-audit");
        assert_eq!(o[2], "vendor-audit");
        assert_eq!(o[3], "instruction-size");
    }

    #[test]
    fn run_audit_empty_repo_skip_all_categories() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            skip: audit_category_order()
                .iter()
                .map(std::string::ToString::to_string)
                .collect(),
            now: Some("2026-05-23T00:00:00Z".to_string()),
            ..Default::default()
        };
        let env = run_audit(&RealFs, &opts).unwrap();
        assert_eq!(env.status, "ok");
        assert_eq!(env.result.total_findings, 0);
        assert!(env.result.categories.is_empty());
    }

    #[test]
    fn run_audit_include_only_filter() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            include_only: vec!["layer-coherence".to_string()],
            now: Some("2026-05-23T00:00:00Z".to_string()),
            ..Default::default()
        };
        let env = run_audit(&RealFs, &opts).unwrap();
        assert_eq!(env.result.categories.len(), 1);
        assert_eq!(env.result.categories[0].name, "layer-coherence");
    }

    #[test]
    fn run_audit_unknown_category_returns_error() {
        // Construct an opts with a fake skip name that does not exist —
        // since our include_only uses it but it's not in order, run_audit
        // will pass through with no categories.
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            include_only: vec!["never-real".to_string()],
            now: Some("2026-05-23T00:00:00Z".to_string()),
            ..Default::default()
        };
        let env = run_audit(&RealFs, &opts).unwrap();
        assert!(env.result.categories.is_empty());
    }

    #[test]
    fn run_category_unknown_returns_error() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            ..Default::default()
        };
        let r = run_category(&RealFs, "nope-not-real", &opts);
        assert!(r.is_err());
    }

    #[test]
    fn audit_envelope_json_includes_schema() {
        let env = AuditEnvelope {
            schema: AUDIT_ENVELOPE_SCHEMA.to_string(),
            status: "ok".to_string(),
            result: AuditResult {
                git_sha: "x".into(),
                ran_at: "2026".into(),
                total_findings: 0,
                by_severity: BTreeMap::new(),
                by_category: BTreeMap::new(),
                categories: vec![],
                skipped_false_positives: vec![],
            },
        };
        let s = serde_json::to_string(&env).unwrap();
        assert!(s.contains("\"schema\":\"rhino-cli/repo-governance-audit/v1\""));
    }

    #[test]
    fn read_git_sha_returns_unknown_in_nongit_dir() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let s = read_git_sha(dir.path());
        assert_eq!(s, "unknown");
    }

    // ---- instruction-size category ----

    #[test]
    fn run_audit_includes_instruction_size_category_with_no_findings_by_default() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            include_only: vec!["instruction-size".to_string()],
            now: Some("2026-05-23T00:00:00Z".to_string()),
            ..Default::default()
        };
        let env = run_audit(&RealFs, &opts).unwrap();
        assert_eq!(env.result.categories.len(), 1, "got: {env:?}");
        assert_eq!(env.result.categories[0].name, "instruction-size");
        assert!(
            env.result.categories[0].passed,
            "no repo-config.yml instruction-size: section — must not fail: {env:?}"
        );
    }

    #[test]
    fn run_audit_instruction_size_reports_fail_finding_for_oversized_surface() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let repo_cfg = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            "instruction-size:\n",
            "  surfaces:\n",
            "    - glob: \"AGENTS.md\"\n",
            "      target: 24000\n",
            "      warn: 27000\n",
            "      fail: 30000\n",
            "  resolved_tree:\n",
            "    root: \"CLAUDE.md\"\n",
            "    target: 30000\n",
            "    warn: 34000\n",
            "    fail: 38000\n",
        );
        std::fs::write(dir.path().join("repo-config.yml"), repo_cfg).unwrap();
        std::fs::write(dir.path().join("AGENTS.md"), "x".repeat(31_000)).unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            include_only: vec!["instruction-size".to_string()],
            now: Some("2026-05-23T00:00:00Z".to_string()),
            ..Default::default()
        };
        let env = run_audit(&RealFs, &opts).unwrap();
        let category = &env.result.categories[0];
        assert_eq!(category.name, "instruction-size");
        assert!(!category.passed, "got: {env:?}");
        assert!(
            category.findings.iter().any(|f| f.file == "AGENTS.md"),
            "got: {env:?}"
        );
    }

    #[test]
    fn run_audit_instruction_size_ignores_warn_only_findings() {
        let _cwd = CwdLock::acquire();
        let dir = tempfile::tempdir().unwrap();
        let repo_cfg = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            "instruction-size:\n",
            "  surfaces:\n",
            "    - glob: \"AGENTS.md\"\n",
            "      target: 24000\n",
            "      warn: 27000\n",
            "      fail: 30000\n",
            "  resolved_tree:\n",
            "    root: \"CLAUDE.md\"\n",
            "    target: 30000\n",
            "    warn: 34000\n",
            "    fail: 38000\n",
        );
        std::fs::write(dir.path().join("repo-config.yml"), repo_cfg).unwrap();
        // 28000 is over target (24000) but under fail (30000) — Warn only.
        std::fs::write(dir.path().join("AGENTS.md"), "x".repeat(28_000)).unwrap();
        let opts = AuditOptions {
            repo_root: dir.path().to_path_buf(),
            include_only: vec!["instruction-size".to_string()],
            now: Some("2026-05-23T00:00:00Z".to_string()),
            ..Default::default()
        };
        let env = run_audit(&RealFs, &opts).unwrap();
        let category = &env.result.categories[0];
        assert!(
            category.passed,
            "Warn-severity findings must not fail the instruction-size preflight category: {env:?}"
        );
    }

    use std::collections::BTreeMap;
}
