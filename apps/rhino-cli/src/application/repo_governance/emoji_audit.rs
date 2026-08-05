//! Emoji audit for source and configuration files.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/repo-governance/emoji_audit.go`.

use std::path::{Path, PathBuf};

use anyhow::{Context, Error, anyhow};

use crate::application::fs::port::Fs;

/// A single emoji violation found in a source or configuration file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EmojiFinding {
    /// Path of the file containing the emoji.
    pub file: String,
    /// 1-based line number.
    pub line: usize,
    /// 1-based column (character offset within the line).
    pub column: usize,
    /// Unicode codepoint formatted as `U+XXXX`.
    pub codepoint: String,
    /// Severity; currently always `"high"`.
    pub severity: String,
}

/// File extensions for which emoji are forbidden.
const EMOJI_FORBIDDEN_EXTENSIONS: &[&str] = &[
    ".json", ".yaml", ".yml", ".toml", ".go", ".ts", ".tsx", ".js", ".jsx", ".py", ".java", ".kt",
    ".rs", ".fs", ".cs", ".dart", ".exs", ".ex", ".clj",
];

/// Directory names to skip during the walk.
const EMOJI_SKIP_DIRS: &[&str] = &[
    "node_modules",
    ".agents",
    ".git",
    ".next",
    "dist",
    "build",
    "target",
    "generated",
    "generated-contracts",
    "generated-sources",
    "generated-test-sources",
    "generated-reports",
    "archived",
    "test-results",
    "playwright-report",
    "coverage",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".dart_tool",
    "out",
    ".cache",
    "storybook-static",
    ".playwright-mcp",
    "raw",
];

/// Walks each directory in `paths` and reports any emoji codepoints found in
/// files with a forbidden extension.
///
/// Findings are sorted by `file`, then `line`, then `column`.
///
/// # Errors
///
/// Returns an error when `paths` is empty or when a file cannot be read during
/// the scan.
pub fn audit_emoji(fs: &dyn Fs, paths: &[String]) -> std::result::Result<Vec<EmojiFinding>, Error> {
    if paths.is_empty() {
        return Err(anyhow!("at least one path is required"));
    }
    let mut findings = Vec::new();
    for root in paths {
        let files = walk_emoji_paths(fs, Path::new(root));
        for f in &files {
            let mut more =
                scan_emoji_file(fs, f).with_context(|| format!("scan {}", f.display()))?;
            findings.append(&mut more);
        }
    }
    findings.sort_by(|a, b| {
        a.file
            .cmp(&b.file)
            .then(a.line.cmp(&b.line))
            .then(a.column.cmp(&b.column))
    });
    Ok(findings)
}

/// Recursively walks `root` and returns paths of files that have a forbidden
/// emoji extension, skipping hidden directories and those listed in
/// [`EMOJI_SKIP_DIRS`].
fn walk_emoji_paths(fs: &dyn Fs, root: &Path) -> Vec<PathBuf> {
    let mut files: Vec<PathBuf> = fs
        .walk_files(root, EMOJI_SKIP_DIRS)
        .into_iter()
        .filter(|p| {
            p.file_name()
                .is_some_and(|n| has_forbidden_emoji_extension(&n.to_string_lossy()))
        })
        .collect();
    files.sort();
    files
}

/// Returns `true` when `name` ends with one of [`EMOJI_FORBIDDEN_EXTENSIONS`]
/// (case-insensitive).
fn has_forbidden_emoji_extension(name: &str) -> bool {
    let lower = name.to_lowercase();
    EMOJI_FORBIDDEN_EXTENSIONS
        .iter()
        .any(|ext| lower.ends_with(ext))
}

/// Scans a single file for emoji codepoints line by line.
///
/// # Errors
///
/// Returns an error when the file cannot be opened.
fn scan_emoji_file(fs: &dyn Fs, path: &Path) -> std::result::Result<Vec<EmojiFinding>, Error> {
    let lines = fs.read_lines(path)?;
    let path_s = path.to_string_lossy().to_string();
    let mut findings = Vec::new();
    for (line_idx, raw) in lines.into_iter().enumerate() {
        let line_num = line_idx + 1;
        let Ok(line) = raw else { continue };
        for (col_idx, r) in line.chars().enumerate() {
            let col = col_idx + 1;
            if is_emoji_rune(r) {
                findings.push(EmojiFinding {
                    file: path_s.clone(),
                    line: line_num,
                    column: col,
                    codepoint: format_codepoint(r),
                    severity: "high".to_string(),
                });
            }
        }
    }
    Ok(findings)
}

/// Returns `true` when `r` falls within one of the emoji Unicode blocks
/// checked by this audit.
fn is_emoji_rune(r: char) -> bool {
    let n = r as u32;
    matches!(n,
        0x2300..=0x23FF
        | 0x2600..=0x27BF
        | 0x200D
        | 0xFE0F
        | 0x1F000..=0x1FFFF
    )
}

/// Formats `r` as a Unicode codepoint string (e.g., `U+1F680`).
///
/// Codepoints up to `U+FFFF` are zero-padded to four hex digits; higher
/// codepoints use the minimal number of digits.
fn format_codepoint(r: char) -> String {
    let n = r as u32;
    if n <= 0xFFFF {
        format!("U+{n:04X}")
    } else {
        format!("U+{n:X}")
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use std::fs;
    use tempfile::TempDir;

    // Test fixtures below use \u{...} escapes rather than literal emoji
    // characters so this detector's own source file doesn't trip the
    // emoji-in-source-code convention it implements.

    #[test]
    fn is_emoji_rune_classifies_known_blocks() {
        assert!(is_emoji_rune('\u{2713}')); // U+2713 Misc Symbols
        assert!(is_emoji_rune('\u{26A0}')); // U+26A0 Warning
        assert!(is_emoji_rune('\u{274C}')); // U+274C Cross
        assert!(is_emoji_rune('\u{1F680}')); // U+1F680
        assert!(!is_emoji_rune('a'));
        assert!(!is_emoji_rune('\u{65E5}')); // CJK is not emoji
    }

    #[test]
    fn format_codepoint_pads_under_ffff() {
        assert_eq!(format_codepoint('a'), "U+0061");
        assert_eq!(format_codepoint('\u{2713}'), "U+2713");
        assert_eq!(format_codepoint('\u{1F680}'), "U+1F680");
    }

    #[test]
    fn audit_emoji_finds_codepoint_in_json_file() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("conf.json");
        fs::write(&p, "{\n  \"label\": \"hi \u{2713} there\"\n}\n").unwrap();
        let findings = audit_emoji(&RealFs, &[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].line, 2);
        assert_eq!(findings[0].codepoint, "U+2713");
        assert_eq!(findings[0].severity, "high");
    }

    #[test]
    fn audit_emoji_skips_non_forbidden_extensions() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("readme.md"), "# \u{1F680} Hello\n").unwrap();
        let findings = audit_emoji(&RealFs, &[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn audit_emoji_skips_node_modules() {
        let tmp = TempDir::new().unwrap();
        let nm = tmp.path().join("node_modules");
        fs::create_dir(&nm).unwrap();
        fs::write(nm.join("x.json"), "\u{2713}\n").unwrap();
        let findings = audit_emoji(&RealFs, &[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn audit_emoji_empty_paths_errors() {
        let err = audit_emoji(&RealFs, &[]).unwrap_err();
        assert!(err.to_string().contains("at least one path"));
    }

    #[test]
    fn audit_emoji_sorts_findings_by_file_line_column() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("b.json"), "\u{2713}\n").unwrap();
        fs::write(tmp.path().join("a.json"), "x\n\u{2713}\n").unwrap();
        let findings = audit_emoji(&RealFs, &[tmp.path().to_string_lossy().to_string()]).unwrap();
        assert_eq!(findings.len(), 2);
        assert!(findings[0].file.ends_with("a.json"));
        assert!(findings[1].file.ends_with("b.json"));
    }
}
