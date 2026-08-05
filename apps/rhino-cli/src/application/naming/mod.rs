//! Pure validators for agent and workflow naming conventions.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/naming/naming.go`.
//!
//! Filesystem-agnostic: callers collect file lists (and content bytes for
//! frontmatter checks) and pass them in.

pub mod reporter;

use std::path::Path;

/// A single naming-convention violation detected by a validator.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Violation {
    /// Relative (or absolute) path of the offending file.
    pub path: String,
    /// Short machine-readable category for the violation (e.g., `"role-suffix"`).
    pub kind: String,
    /// Human-readable description of what is wrong.
    pub message: String,
}

/// Returns the file stem (basename without extension) of `path`.
///
/// Falls back to the full filename when there is no extension, and to an empty
/// string when the path has no filename component at all.
pub fn basename_sans_ext(path: &str) -> String {
    let p = Path::new(path);
    let stem = p.file_stem().map(|s| s.to_string_lossy().to_string());
    stem.unwrap_or_else(|| {
        Path::new(path)
            .file_name()
            .map(|s| s.to_string_lossy().to_string())
            .unwrap_or_default()
    })
}

/// Validates that the file at `path` ends with one of the `allowed_suffixes`.
///
/// A bare suffix filename (e.g., `maker.md` where `"maker"` is an allowed
/// suffix) is considered invalid because it carries no scope prefix.
///
/// Returns `None` when the name is valid, or `Some(Violation)` when it is not.
/// The returned violation has its `kind` field set to the `kind` argument.
pub fn validate_suffix(path: &str, allowed_suffixes: &[&str], kind: &str) -> Option<Violation> {
    let name = basename_sans_ext(path);
    for suffix in allowed_suffixes {
        if name == *suffix {
            // Bare suffix (e.g. "maker.md") has no scope and is invalid.
            continue;
        }
        if name.ends_with(&format!("-{suffix}")) {
            return None;
        }
    }
    Some(Violation {
        path: path.to_string(),
        kind: kind.to_string(),
        message: format!(
            "filename \"{name}\" does not end with any allowed suffix ({})",
            allowed_suffixes.join(", ")
        ),
    })
}

/// Extracts the `name:` value from a YAML frontmatter block.
///
/// Returns the value of the first `name:` key found inside the leading `---`
/// fences, with surrounding quotes stripped.  Returns an empty string when
/// there is no valid frontmatter block or no `name:` key.
pub fn extract_frontmatter_name(content: &[u8]) -> String {
    let text = String::from_utf8_lossy(content);
    if !text.starts_with("---\n") && !text.starts_with("---\r\n") {
        return String::new();
    }
    let rest = &text[4..];
    let Some(end) = rest.find("\n---") else {
        return String::new();
    };
    let frontmatter = &rest[..end];
    for line in frontmatter.split('\n') {
        let trimmed = line.trim();
        if let Some(rest) = trimmed.strip_prefix("name:") {
            let value = rest.trim();
            let value = value.trim_matches(|c| c == '"' || c == '\'');
            return value.to_string();
        }
    }
    String::new()
}

/// Validates that the frontmatter `name:` field matches the file's basename.
///
/// Returns `None` when the frontmatter contains no `name:` field (treated as
/// conforming) or when the name matches the basename.  Returns
/// `Some(Violation)` with `kind = "frontmatter-mismatch"` when the values
/// differ.
pub fn validate_frontmatter_name(path: &str, content: &[u8]) -> Option<Violation> {
    let name = extract_frontmatter_name(content);
    if name.is_empty() {
        return None;
    }
    let expected = basename_sans_ext(path);
    if name == expected {
        return None;
    }
    Some(Violation {
        path: path.to_string(),
        kind: "frontmatter-mismatch".to_string(),
        message: format!("frontmatter name \"{name}\" does not match filename \"{expected}\""),
    })
}

/// Validates that every agent definition file has a counterpart in both binding
/// directories.
///
/// `claude_files` are paths under `.claude/agents/` and `opencode_files` are
/// paths under `.opencode/agents/`.  For each stem that exists in only one set
/// a `"mirror-drift"` `Violation` is emitted.  The returned slice is sorted by
/// `path`.
pub fn validate_mirror(claude_files: &[String], opencode_files: &[String]) -> Vec<Violation> {
    validate_mirror_with_dirs(
        claude_files,
        opencode_files,
        ".claude/agents",
        ".opencode/agents",
    )
}

/// Like [`validate_mirror`] but uses explicit `source_dir` / `target_dir` labels in messages.
///
/// Use this for N-way mirror checks (e.g. source → Amazon Q) where the target directory
/// is not `.opencode/agents/`.
pub fn validate_mirror_with_dirs(
    source_files: &[String],
    target_files: &[String],
    source_dir: &str,
    target_dir: &str,
) -> Vec<Violation> {
    use std::collections::HashMap;
    let mut source_set: HashMap<String, String> = HashMap::new();
    for p in source_files {
        source_set.insert(basename_sans_ext(p), p.clone());
    }
    let mut target_set: HashMap<String, String> = HashMap::new();
    for p in target_files {
        target_set.insert(basename_sans_ext(p), p.clone());
    }
    let mut violations = Vec::new();
    for (name, path) in &source_set {
        if !target_set.contains_key(name) {
            violations.push(Violation {
                path: path.clone(),
                kind: "mirror-drift".to_string(),
                message: format!("{name}.md exists in {source_dir}/ but not in {target_dir}/"),
            });
        }
    }
    for (name, path) in &target_set {
        if !source_set.contains_key(name) {
            violations.push(Violation {
                path: path.clone(),
                kind: "mirror-drift".to_string(),
                message: format!("{name}.md exists in {target_dir}/ but not in {source_dir}/"),
            });
        }
    }
    violations.sort_by(|a, b| a.path.cmp(&b.path));
    violations
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn basename_strips_md_extension() {
        assert_eq!(basename_sans_ext("a/b/foo.md"), "foo");
        assert_eq!(basename_sans_ext("foo.md"), "foo");
        assert_eq!(basename_sans_ext("foo"), "foo");
    }

    #[test]
    fn validate_suffix_accepts_matching_role() {
        assert!(
            validate_suffix("apps-foo-maker.md", &["maker", "checker"], "role-suffix").is_none()
        );
        assert!(validate_suffix("foo-checker.md", &["maker", "checker"], "role-suffix").is_none());
    }

    #[test]
    fn validate_suffix_rejects_mismatch() {
        let v = validate_suffix("foo-bar.md", &["maker", "checker"], "role-suffix").unwrap();
        assert_eq!(v.kind, "role-suffix");
        assert!(v.message.contains("does not end with"));
    }

    #[test]
    fn validate_suffix_rejects_bare_suffix() {
        let v = validate_suffix("maker.md", &["maker"], "role-suffix");
        assert!(v.is_some());
    }

    #[test]
    fn validate_suffix_matches_multi_word() {
        assert!(
            validate_suffix("plan-quality-gate.md", &["quality-gate"], "type-suffix").is_none()
        );
    }

    #[test]
    fn validate_suffix_accepts_grooming_type() {
        assert!(validate_suffix("plan-ideas-grooming.md", &["grooming"], "type-suffix").is_none());
    }

    #[test]
    fn extract_frontmatter_returns_name() {
        let content = b"---\nname: foo-bar\ndescription: D\n---\n# Body";
        assert_eq!(extract_frontmatter_name(content), "foo-bar");
    }

    #[test]
    fn extract_frontmatter_strips_quotes() {
        let content = b"---\nname: \"foo-bar\"\n---\n";
        assert_eq!(extract_frontmatter_name(content), "foo-bar");
    }

    #[test]
    fn extract_frontmatter_no_block_returns_empty() {
        assert_eq!(extract_frontmatter_name(b"# Title\n"), "");
    }

    #[test]
    fn validate_frontmatter_name_matches() {
        assert!(validate_frontmatter_name("foo.md", b"---\nname: foo\n---\n").is_none());
    }

    #[test]
    fn validate_frontmatter_name_mismatch() {
        let v = validate_frontmatter_name("foo.md", b"---\nname: bar\n---\n").unwrap();
        assert_eq!(v.kind, "frontmatter-mismatch");
    }

    #[test]
    fn validate_mirror_finds_missing_pairs() {
        let claude = vec![".claude/agents/foo.md".to_string()];
        let opencode = vec![".opencode/agents/bar.md".to_string()];
        let vs = validate_mirror(&claude, &opencode);
        assert_eq!(vs.len(), 2);
    }

    #[test]
    fn validate_mirror_clean_when_pairs_match() {
        let claude = vec![".claude/agents/foo.md".to_string()];
        let opencode = vec![".opencode/agents/foo.md".to_string()];
        let vs = validate_mirror(&claude, &opencode);
        assert!(vs.is_empty());
    }

    #[test]
    fn validate_mirror_empty_inputs_is_clean() {
        let vs = validate_mirror(&[], &[]);
        assert!(vs.is_empty());
    }

    #[test]
    fn validate_mirror_returns_sorted_by_path() {
        let claude = vec![
            ".claude/agents/z.md".to_string(),
            ".claude/agents/a.md".to_string(),
        ];
        let vs = validate_mirror(&claude, &[]);
        assert_eq!(vs.len(), 2);
        assert!(vs[0].path.contains("a.md"));
        assert!(vs[1].path.contains("z.md"));
    }

    #[test]
    fn extract_frontmatter_handles_crlf() {
        let content = b"---\r\nname: foo\r\n---\r\n";
        assert_eq!(extract_frontmatter_name(content), "foo");
    }

    #[test]
    fn extract_frontmatter_missing_closing_returns_empty() {
        assert_eq!(extract_frontmatter_name(b"---\nname: foo\n"), "");
    }

    #[test]
    fn validate_frontmatter_name_no_name_is_none() {
        assert!(validate_frontmatter_name("foo.md", b"---\ndescription: D\n---\n").is_none());
    }

    #[test]
    fn validate_suffix_message_includes_all_allowed() {
        let v = validate_suffix("foo.md", &["maker", "checker", "fixer"], "role-suffix").unwrap();
        assert!(v.message.contains("maker"));
        assert!(v.message.contains("checker"));
        assert!(v.message.contains("fixer"));
    }
}
