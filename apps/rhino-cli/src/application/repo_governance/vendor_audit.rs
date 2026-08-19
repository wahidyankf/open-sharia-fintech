//! Vendor-independence audit for governance Markdown documents.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/repo-governance/governance_vendor_audit.go`.

use std::path::Path;
use std::sync::OnceLock;

use anyhow::{Context, Error};
use regex::Regex;

use crate::application::fs::port::Fs;

/// A single vendor-term finding in a governance Markdown document.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Finding {
    /// Path of the file containing the forbidden term.
    pub path: String,
    /// 1-based line number of the match.
    pub line: usize,
    /// The display name of the matched term (e.g., `"Claude Code"`).
    pub r#match: String,
    /// Suggested vendor-neutral replacement text.
    pub replacement: String,
}

/// The convention-definition file that is always exempt from this audit.
const FORBIDDEN_CONVENTION_SUFFIX: &str =
    "repo-governance/conventions/structure/governance-vendor-independence.md";

/// The convention-definition file's split-directory children (per the Split
/// Pattern, `governance-vendor-independence.md`'s own child files) are exempt
/// for the same reason as the parent: they document forbidden vendor terms by
/// naming them as examples.
const FORBIDDEN_CONVENTION_DIR_SUFFIX: &str =
    "repo-governance/conventions/structure/governance-vendor-independence/";

/// A compiled forbidden-term entry.
struct ForbiddenTerm {
    /// Compiled regex that matches the term in prose.
    re: Regex,
    /// Human-readable name used in the `Finding::match` field.
    display_term: &'static str,
    /// Suggested vendor-neutral replacement text.
    replacement: &'static str,
}

/// Source data for [`forbidden_terms`]: `(pattern, display_term, replacement)`.
///
/// Kept as a module-level `const` slice (not a function body) so the table can
/// grow without tripping Clippy's `too_many_lines` ceiling.
///
/// This table detects vendor leakage into vendor-neutral prose. It is NOT a
/// supported-harness declaration — `repo-config.yml` `harness:` is the sole
/// authority on which harnesses this repository supports. Names of harnesses
/// the repository has dropped therefore STAY here on purpose: prose must not
/// name them either, and a dropped name is exactly the leakage this audit
/// exists to catch. Do not tidy an entry away because its harness is no longer
/// supported (`plans/.../update-harness-support/tech-docs.md` DD-3).
const FORBIDDEN: &[(&str, &str, &str)] = &[
    (r"Claude Code", "Claude Code", "\"the coding agent\""),
    (
        r"OpenCode",
        "OpenCode",
        "\"the coding agent\" or drop where redundant",
    ),
    (
        r"\bCursor\b",
        "Cursor",
        "\"the coding agent\" or \"AI coding editor\"",
    ),
    (
        r"\bWindsurf\b",
        "Windsurf",
        "\"the coding agent\" or \"AI coding editor\"",
    ),
    (
        r"\bCodeium\b",
        "Codeium",
        "\"the coding agent\" (legacy Windsurf brand)",
    ),
    (
        r"\bCopilot\b",
        "Copilot",
        "\"the coding agent\" or \"AI coding assistant\"",
    ),
    (
        r"\bAider\b",
        "Aider",
        "\"the coding agent\" or \"AI coding assistant\"",
    ),
    (
        r"\bCline\b",
        "Cline",
        "\"the coding agent\" or \"AI coding assistant\"",
    ),
    (
        r"\bDevin\b",
        "Devin",
        "\"the coding agent\" (false-positive risk: personal name; review context)",
    ),
    (
        r"\bJunie\b",
        "Junie",
        "\"the coding agent\" or \"AI coding assistant\"",
    ),
    (
        r"\bJetBrains\b",
        "JetBrains",
        "\"the model vendor\" or drop",
    ),
    (r"\bAmazon Q\b", "Amazon Q", "\"the coding agent\""),
    (
        r"\bAntigravity\b",
        "Antigravity",
        "\"the coding agent\" or \"AI coding editor\"",
    ),
    (
        r"Pi Coding Agent",
        "Pi Coding Agent",
        "\"the coding agent\"",
    ),
    (r"pi\.dev", "pi.dev", "\"the coding agent\""),
    (r"\bEarendil\b", "Earendil", "\"the model vendor\" or drop"),
    (r"\.claude/", ".claude/", "\"primary binding directory\""),
    (
        r"\.opencode/",
        ".opencode/",
        "\"secondary binding directory\"",
    ),
    (
        r"\.cursor/",
        ".cursor/",
        "\"the platform binding directory\"",
    ),
    (
        r"\.windsurf/",
        ".windsurf/",
        "\"the platform binding directory\"",
    ),
    (
        r"\.continue/",
        ".continue/",
        "\"the platform binding directory\"",
    ),
    (
        r"\.clinerules/",
        ".clinerules/",
        "\"the platform binding directory\"",
    ),
    (r"\.junie/", ".junie/", "\"the platform binding directory\""),
    (
        r"\.amazonq/",
        ".amazonq/",
        "\"the platform binding directory\"",
    ),
    (r"\.pi/", ".pi/", "\"the platform binding directory\""),
    (
        r"\.gemini/",
        ".gemini/",
        "\"the platform binding directory\"",
    ),
    (r"\.agent/", ".agent/", "\"the platform binding directory\""),
    (
        r"\.agents/",
        ".agents/",
        "\"the platform binding directory\"",
    ),
    (r"Anthropic", "Anthropic", "\"the model vendor\" or drop"),
    (r"\bOpenAI\b", "OpenAI", "\"the model vendor\" or drop"),
    (r"\bxAI\b", "xAI", "\"the model vendor\" or drop"),
    (r"\bSonnet\b", "Sonnet", "\"execution-grade\""),
    (r"\bOpus\b", "Opus", "\"planning-grade\""),
    (r"\bHaiku\b", "Haiku", "\"fast\""),
    (r"\bGPT\b", "GPT", "\"AI model\" or capability tier"),
    (r"\bGemini\b", "Gemini", "\"AI model\" or capability tier"),
    (
        r"\bDeepSeek\b",
        "DeepSeek",
        "\"AI model\" or capability tier",
    ),
    (r"\bQwen\b", "Qwen", "\"AI model\" or capability tier"),
    (r"\bLlama\b", "Llama", "\"AI model\" or capability tier"),
    (r"\bMistral\b", "Mistral", "\"AI model\" or capability tier"),
    (
        r"\bGrok\b",
        "Grok",
        "\"AI model\" (false-positive risk: verb \"to grok\"; review context)",
    ),
    (r"\bSkills\b", "Skills", "\"agent skills\" (lowercase)"),
];

/// Returns the lazily-compiled slice of all [`ForbiddenTerm`]s built from
/// [`FORBIDDEN`].
fn forbidden_terms() -> &'static Vec<ForbiddenTerm> {
    static TERMS: OnceLock<Vec<ForbiddenTerm>> = OnceLock::new();
    TERMS.get_or_init(|| FORBIDDEN.iter().map(|&(p, t, r)| mk(p, t, r)).collect())
}

/// Constructs a [`ForbiddenTerm`] from a raw regex `pattern`.
///
/// # Panics
///
/// Panics when `pattern` is not a valid regex — all patterns in [`FORBIDDEN`]
/// are validated at compile time so this should never occur in practice.
fn mk(pattern: &str, term: &'static str, replacement: &'static str) -> ForbiddenTerm {
    ForbiddenTerm {
        re: Regex::new(pattern).expect("valid hardcoded regex"),
        display_term: term,
        replacement,
    }
}

/// Returns a compiled `Regex` matching inline HTML comments (`<!-- … -->`).
fn html_comment_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"<!--.*?-->").expect("valid hardcoded regex"))
}

/// Returns a compiled `Regex` matching inline code spans (`` `…` ``).
fn inline_code_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"`[^`]*`").expect("valid hardcoded regex"))
}

/// Returns a compiled `Regex` matching Markdown links `[text](url)`.
fn link_url_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\[([^\]]*)\]\([^)]*\)").expect("valid hardcoded regex"))
}

/// Reads the file at `path` and scans it for forbidden vendor terms.
///
/// # Errors
///
/// Returns an error when the file cannot be read.
pub fn scan_file(fs: &dyn Fs, path: &Path) -> std::result::Result<Vec<Finding>, Error> {
    let data = fs
        .read_to_string(path)
        .with_context(|| format!("read {}", path.display()))?;
    Ok(scan_lines(&path.to_string_lossy(), &data))
}

/// Recursively walks `root` and scans every `.md` file for forbidden vendor
/// terms, skipping the convention-definition file.
///
/// Returns an empty `Vec` when `root` does not exist.
///
/// # Errors
///
/// Returns an error when any file cannot be read.
pub fn walk(fs: &dyn Fs, root: &Path) -> std::result::Result<Vec<Finding>, Error> {
    let mut findings = Vec::new();
    for p in fs.walk_files(root, &[]) {
        let name = p.file_name().map(|n| n.to_string_lossy().to_string());
        if !name.is_some_and(|n| n.ends_with(".md")) {
            continue;
        }
        let p_slash = p.to_string_lossy().replace('\\', "/");
        if p_slash.ends_with(FORBIDDEN_CONVENTION_SUFFIX)
            || p_slash.contains(FORBIDDEN_CONVENTION_DIR_SUFFIX)
        {
            continue;
        }
        findings.extend(scan_file(fs, &p)?);
    }
    Ok(findings)
}

/// Root-level instruction files that are in scope for the vendor audit in
/// addition to the `repo-governance/` subtree, per the
/// [Governance Vendor-Independence Convention] "Scope" section.
///
/// [Governance Vendor-Independence Convention]: repo-governance/conventions/structure/governance-vendor-independence.md
const ROOT_INSTRUCTION_SURFACES: &[&str] = &["AGENTS.md", "CLAUDE.md"];

/// Walks the canonical governance audit scope rooted at `repo_root`:
/// every `.md` file under `repo_root/repo-governance/` plus the root
/// instruction surfaces in [`ROOT_INSTRUCTION_SURFACES`].
///
/// This is the scope the `repo-governance audit` orchestrator uses — narrower
/// than a whole-repo walk so build caches, app content, worktrees, and
/// third-party vendored skills are never scanned. Mirrors the default scope of
/// the standalone `repo-governance vendor validate` command (which defaults to
/// `repo-governance/`), extended with the two root instruction surfaces the
/// convention also governs.
///
/// # Errors
///
/// Returns an error when any in-scope file cannot be read.
pub fn walk_governance_scope(
    fs: &dyn Fs,
    repo_root: &Path,
) -> std::result::Result<Vec<Finding>, Error> {
    let mut findings = walk(fs, &repo_root.join("repo-governance"))?;
    for name in ROOT_INSTRUCTION_SURFACES {
        let p = repo_root.join(name);
        if fs.exists(&p) && !fs.is_dir(&p) {
            findings.extend(scan_file(fs, &p)?);
        }
    }
    Ok(findings)
}

/// Scans `content` line-by-line for forbidden vendor terms, respecting YAML
/// frontmatter, code fences, HTML comments, inline code, link URLs, and the
/// "Platform Binding Examples" heading scope.
fn scan_lines(path: &str, content: &str) -> Vec<Finding> {
    let lines: Vec<&str> = content.split('\n').collect();
    let mut findings = Vec::new();

    let mut in_code_fence_len: usize = 0;
    let mut in_frontmatter = false;
    let mut in_html_comment = false;
    let mut in_platform_binding_section = false;
    let mut platform_binding_heading_level: usize = 0;

    for (i, line) in lines.iter().enumerate() {
        let line_num = i + 1;

        // YAML frontmatter.
        if line_num == 1 && line.trim() == "---" {
            in_frontmatter = true;
            continue;
        }
        if in_frontmatter {
            if line.trim() == "---" {
                in_frontmatter = false;
            }
            continue;
        }

        // Multi-line HTML comment.
        if in_html_comment {
            if line.contains("-->") {
                in_html_comment = false;
            }
            continue;
        }
        if line.contains("<!--") && !line.contains("-->") {
            in_html_comment = true;
            if let Some(idx) = line.find("<!--") {
                let before = &line[..idx];
                let stripped = strip_non_prose(before);
                if !stripped.is_empty() {
                    for ft in forbidden_terms() {
                        if ft.re.is_match(&stripped) {
                            findings.push(Finding {
                                path: path.to_string(),
                                line: line_num,
                                r#match: ft.display_term.to_string(),
                                replacement: ft.replacement.to_string(),
                            });
                        }
                    }
                }
            }
            continue;
        }

        // Code fences (length-aware per `CommonMark`).
        let fl = fence_line_len(line);
        if fl > 0 {
            if in_code_fence_len == 0 {
                in_code_fence_len = fl;
                continue;
            } else if fl >= in_code_fence_len {
                in_code_fence_len = 0;
                continue;
            }
            // Inner fence line (shorter than opener) — falls through.
        }

        if in_code_fence_len > 0 {
            continue;
        }

        // Platform Binding Examples heading scope.
        if let Some(level) = parse_heading(line) {
            if is_platform_binding_heading(line) {
                in_platform_binding_section = true;
                platform_binding_heading_level = level;
                continue;
            }
            if in_platform_binding_section && level <= platform_binding_heading_level {
                in_platform_binding_section = false;
                platform_binding_heading_level = 0;
            }
        }

        if in_platform_binding_section {
            continue;
        }

        // Scan for forbidden terms.
        let stripped = strip_non_prose(line);
        for ft in forbidden_terms() {
            if ft.re.is_match(&stripped) {
                findings.push(Finding {
                    path: path.to_string(),
                    line: line_num,
                    r#match: ft.display_term.to_string(),
                    replacement: ft.replacement.to_string(),
                });
            }
        }
    }
    findings
}

/// Returns the number of leading backtick characters on `line` when it is a
/// valid `CommonMark` code fence (3 or more backticks), or `0` otherwise.
fn fence_line_len(line: &str) -> usize {
    let trimmed = line.trim();
    let mut n = 0;
    for ch in trimmed.chars() {
        if ch == '`' {
            n += 1;
        } else {
            break;
        }
    }
    if n >= 3 { n } else { 0 }
}

/// Removes inline HTML comments, inline code spans, and link URLs from `line`
/// so that only prose text remains for vendor-term matching.
fn strip_non_prose(line: &str) -> String {
    let s = html_comment_re().replace_all(line, "");
    let s = inline_code_re().replace_all(&s, "``");
    let s = link_url_re().replace_all(&s, "[$1]");
    s.into_owned()
}

/// Parses `line` as an ATX heading and returns its level (1–6), or `None` when
/// the line is not a valid heading.
fn parse_heading(line: &str) -> Option<usize> {
    let trimmed = line.trim();
    if !trimmed.starts_with('#') {
        return None;
    }
    let mut level = 0;
    for ch in trimmed.chars() {
        if ch == '#' {
            level += 1;
        } else {
            break;
        }
    }
    if level > 6 {
        return None;
    }
    let bytes = trimmed.as_bytes();
    if bytes.len() <= level || bytes[level] != b' ' {
        return None;
    }
    Some(level)
}

/// Returns `true` when `line` is a "Platform Binding Examples" heading that
/// opens a vendor-exempt section.
fn is_platform_binding_heading(line: &str) -> bool {
    line.to_lowercase().contains("platform binding examples")
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use std::fs;
    use tempfile::TempDir;

    #[test]
    fn detects_forbidden_brand_in_prose() {
        let findings = scan_lines("x.md", "I use Claude Code.\n");
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].r#match, "Claude Code");
    }

    #[test]
    fn skips_code_fences() {
        let findings = scan_lines("x.md", "```\nClaude Code\n```\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_nested_quad_fences() {
        let findings = scan_lines("x.md", "````md\n```\nClaude Code\n```\n````\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_frontmatter() {
        let findings = scan_lines("x.md", "---\ntitle: Claude Code\n---\n\nBody.\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_html_comments() {
        let findings = scan_lines("x.md", "<!-- Claude Code -->\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_multiline_html_comments() {
        let findings = scan_lines("x.md", "<!--\nClaude Code\n-->\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_inline_code_spans() {
        let findings = scan_lines("x.md", "Use `Claude Code` here.\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_link_urls() {
        let findings = scan_lines("x.md", "[link](https://example.com/Claude-Code/foo)\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_platform_binding_section() {
        let content = "# X\n\n## Platform Binding Examples\n\nClaude Code\n\n## Next\n";
        let findings = scan_lines("x.md", content);
        assert!(findings.is_empty());
    }

    #[test]
    fn platform_binding_scope_ends_at_same_level_heading() {
        // line 1: ## Platform Binding Examples
        // line 2: (blank)
        // line 3: Claude Code (in scope)
        // line 4: ## Other
        // line 5: (blank)
        // line 6: Claude Code (out of scope)
        let content = "## Platform Binding Examples\n\nClaude Code\n## Other\n\nClaude Code\n";
        let findings = scan_lines("x.md", content);
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].line, 6);
    }

    #[test]
    fn detects_binding_dir_path() {
        let findings = scan_lines(
            "x.md",
            "Edit `.claude/agents/` is wrong, edit .claude/agents/ instead.\n",
        );
        // The `.claude/` regex matches in stripped prose (inline code already removed).
        assert!(findings.iter().any(|f| f.r#match == ".claude/"));
    }

    #[test]
    fn skip_convention_definition_file() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join(FORBIDDEN_CONVENTION_SUFFIX);
        fs::create_dir_all(p.parent().unwrap()).unwrap();
        fs::write(&p, "Claude Code\n").unwrap();
        let findings = walk(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn skip_convention_definition_split_children() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join(FORBIDDEN_CONVENTION_DIR_SUFFIX);
        fs::create_dir_all(&dir).unwrap();
        fs::write(dir.join("01-purpose-and-scope.md"), "Claude Code\n").unwrap();
        let findings = walk(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }

    #[test]
    fn detects_junie_in_prose() {
        let findings = scan_lines("x.md", "I use Junie for coding.\n");
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].r#match, "Junie");
    }

    #[test]
    fn detects_amazon_q_in_prose() {
        let findings = scan_lines("x.md", "I use Amazon Q for coding.\n");
        assert!(findings.iter().any(|f| f.r#match == "Amazon Q"));
    }

    #[test]
    fn detects_antigravity_in_prose() {
        let findings = scan_lines("x.md", "I use Antigravity for coding.\n");
        assert!(findings.iter().any(|f| f.r#match == "Antigravity"));
    }

    #[test]
    fn does_not_flag_math_constant_pi() {
        let findings = scan_lines("x.md", "The value of pi is 3.14159.\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn does_not_flag_bare_capital_q() {
        let findings = scan_lines("x.md", "Press Q to quit.\n");
        assert!(findings.is_empty());
    }

    #[test]
    fn skips_new_vendor_in_platform_binding_section() {
        let content = "# X\n\n## Platform Binding Examples\n\nJunie\n\n## Next\n";
        let findings = scan_lines("x.md", content);
        assert!(findings.is_empty());
    }

    #[test]
    fn parse_heading_recognises_atx_levels() {
        assert_eq!(parse_heading("## Foo"), Some(2));
        assert_eq!(parse_heading("### Bar"), Some(3));
        assert_eq!(parse_heading("####### Too deep"), None);
        assert_eq!(parse_heading("##NoSpace"), None);
        assert_eq!(parse_heading("Foo"), None);
    }

    #[test]
    fn fence_line_len_counts_backticks() {
        assert_eq!(fence_line_len("```"), 3);
        assert_eq!(fence_line_len("```js"), 3);
        assert_eq!(fence_line_len("````"), 4);
        assert_eq!(fence_line_len("``"), 0);
        assert_eq!(fence_line_len("text"), 0);
    }

    #[test]
    fn governance_scope_walks_in_scope_and_skips_out_of_scope() {
        // The vendor-independence convention scopes the audit to `repo-governance/`
        // prose plus the canonical root instruction surfaces `AGENTS.md` and
        // `CLAUDE.md`. Everything else in the repo (build caches, app content,
        // worktrees) is out of scope and must NOT be scanned.
        let tmp = TempDir::new().unwrap();
        let root = tmp.path();

        // In scope: repo-governance/ subtree.
        let gov = root.join("repo-governance/conventions");
        fs::create_dir_all(&gov).unwrap();
        fs::write(gov.join("foo.md"), "We use Claude Code internally.\n").unwrap();

        // In scope: root instruction surfaces.
        fs::write(root.join("AGENTS.md"), "Edited with Cursor today.\n").unwrap();
        fs::write(root.join("CLAUDE.md"), "Powered by Anthropic models.\n").unwrap();

        // Out of scope: build cache, app source, worktree — each with a vendor term.
        for rel in [".nx/cache/x.md", "apps/web/y.md", "worktrees/wt/z.md"] {
            let p = root.join(rel);
            fs::create_dir_all(p.parent().unwrap()).unwrap();
            fs::write(&p, "Built on OpenCode.\n").unwrap();
        }

        let findings = walk_governance_scope(&RealFs, root).unwrap();

        // Exactly the three in-scope files contribute findings.
        let files: std::collections::BTreeSet<String> =
            findings.iter().map(|f| f.path.replace('\\', "/")).collect();
        assert_eq!(findings.len(), 3, "expected one finding per in-scope file");
        assert!(
            files
                .iter()
                .any(|p| p.ends_with("repo-governance/conventions/foo.md"))
        );
        assert!(files.iter().any(|p| p.ends_with("/AGENTS.md")));
        assert!(files.iter().any(|p| p.ends_with("/CLAUDE.md")));
        // No out-of-scope path leaks in.
        assert!(!files.iter().any(|p| p.contains("/.nx/")));
        assert!(!files.iter().any(|p| p.contains("/apps/")));
        assert!(!files.iter().any(|p| p.contains("/worktrees/")));
    }

    #[test]
    fn governance_scope_tolerates_missing_root_files() {
        // When AGENTS.md / CLAUDE.md are absent, the scoped walk still succeeds
        // and returns only the repo-governance/ findings (here: none).
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("repo-governance")).unwrap();
        let findings = walk_governance_scope(&RealFs, tmp.path()).unwrap();
        assert!(findings.is_empty());
    }
}
