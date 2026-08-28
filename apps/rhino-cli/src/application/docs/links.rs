//! Relative markdown link validator.
//!
//! Byte-for-byte port of `apps/rhino-cli/internal/docs/links_*.go`.
//!
//! Scans markdown files for relative links and verifies that each target
//! exists on the filesystem.  External URLs, anchor-only links, and a
//! curated set of known placeholder patterns are silently skipped.

use std::collections::{BTreeMap, HashMap, HashSet};
use std::fmt::Write as _;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use std::sync::OnceLock;
use std::time::Instant;

use anyhow::{Context, Error};
use chrono::Local;
use regex::Regex;
use walkdir::WalkDir;

/// Directories skipped by the full-repo walker.
///
/// This is the standardized cross-repo noise-skip set shared by the markdown
/// gate validators (mermaid, links, heading-hierarchy).
const FULL_REPO_SKIP_DIRS: &[&str] = &[
    "node_modules",
    "dist",
    "build",
    "target",
    ".next",
    "coverage",
    "generated-reports",
    "local-tmp",
    "archived",
    "apps-labs",
    "worktrees",
    ".terraform",
    "generated-contracts",
    ".nx",
    ".fvm-cache",
    ".git",
    "deps",
    "_build",
    "cover",
];

/// A relative markdown link that could not be resolved to an existing file.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BrokenLink {
    /// One-based line number where the link appears in the source file.
    pub line_number: usize,
    /// Repository-relative path of the file that contains the link.
    pub source_file: String,
    /// The raw link target string (after stripping angle-bracket wrappers).
    pub link_text: String,
    /// Absolute path that the link resolved to (does not exist).
    pub target_path: String,
    /// Human-readable category for grouping in reports.
    pub category: String,
}

/// Aggregated result returned by [`validate_all_links`].
pub struct LinkValidationResult {
    /// Total number of markdown files scanned.
    pub total_files: usize,
    /// Total number of relative links examined.
    pub total_links: usize,
    /// All broken links found during the scan.
    pub broken_links: Vec<BrokenLink>,
    /// Broken links grouped by their [`categorize_broken_link`] category string.
    /// A `BTreeMap`, not a `HashMap` — deterministic key order matters here:
    /// this field feeds `format_link_json`'s `categories` object directly,
    /// and `std::collections::HashMap`'s randomized per-process iteration
    /// order would make that JSON output nondeterministic across runs of
    /// the same binary, which broke shadow-diff byte-identity even between
    /// two Rust invocations (Wave D integration, rewrite-rhino-cli-to-fsharp).
    pub broken_by_category: BTreeMap<String, Vec<BrokenLink>>,
    /// Wall-clock time for the full scan, in milliseconds.
    pub scan_duration_ms: i64,
}

/// Options that control the behaviour of [`validate_all_links`].
pub struct ScanOptions {
    /// Absolute path to the repository root.
    pub repo_root: PathBuf,
    /// When `true`, only files staged in the Git index are scanned.
    pub staged_only: bool,
    /// Repository-relative path prefixes that are excluded from scanning.
    pub skip_paths: Vec<String>,
}

/// Internal representation of a parsed markdown link before validation.
#[derive(Debug, Clone)]
struct LinkInfo {
    /// One-based source line number.
    line_number: usize,
    /// Raw URL string extracted from the markdown link syntax.
    url: String,
}

/// Returns the compiled regex for matching `[text](url)` markdown links.
fn link_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\[([^\]]+)\]\(([^)]+)\)").expect("valid hardcoded regex"))
}

/// Returns the compiled regex for matching bracket-style placeholder tokens
/// such as `[placeholder-name]`.
fn bracket_placeholder_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\[[\w-]+\]").expect("valid hardcoded regex"))
}

/// Scans all markdown files according to `opts` and returns a [`LinkValidationResult`].
///
/// # Errors
///
/// Returns an error when the list of files to scan cannot be determined (e.g. the
/// `git diff --cached` command fails when `staged_only` is `true`).
///
/// # Panics
///
/// Panics if the elapsed scan duration in milliseconds does not fit in `i64`,
/// which cannot happen for any realistic scan duration.
pub fn validate_all_links(opts: &ScanOptions) -> std::result::Result<LinkValidationResult, Error> {
    let start = Instant::now();
    let files = get_markdown_files(opts)?;
    let mut result = LinkValidationResult {
        total_files: files.len(),
        total_links: 0,
        broken_links: Vec::new(),
        broken_by_category: BTreeMap::new(),
        scan_duration_ms: 0,
    };

    for path in &files {
        let Ok(links) = extract_links(path) else {
            continue;
        };
        result.total_links += links.len();

        let Ok(broken) = validate_file(path, opts, &links) else {
            continue;
        };
        for b in broken {
            result
                .broken_by_category
                .entry(b.category.clone())
                .or_default()
                .push(b.clone());
            result.broken_links.push(b);
        }
    }
    result.scan_duration_ms =
        i64::try_from(start.elapsed().as_millis()).expect("duration fits in i64");
    Ok(result)
}

/// Selects the markdown files to scan based on `opts.staged_only` and applies
/// the skip-path filter.
///
/// # Errors
///
/// Returns an error when the staged-file list cannot be retrieved from Git.
fn get_markdown_files(opts: &ScanOptions) -> std::result::Result<Vec<PathBuf>, Error> {
    let files = if opts.staged_only {
        get_staged_markdown_files(&opts.repo_root)?
    } else {
        get_all_markdown_files(&opts.repo_root)?
    };
    Ok(filter_skip_paths(files, &opts.repo_root, &opts.skip_paths))
}

/// Returns the list of staged `.md` files reported by `git diff --cached`.
///
/// # Errors
///
/// Returns an error when the `git` command cannot be executed.
fn get_staged_markdown_files(repo_root: &Path) -> std::result::Result<Vec<PathBuf>, Error> {
    let output = Command::new("git")
        .args(["diff", "--cached", "--name-only", "--diff-filter=ACM"])
        .current_dir(repo_root)
        .output()
        .context("git diff --cached")?;
    let text = String::from_utf8_lossy(&output.stdout);
    Ok(text
        .lines()
        .filter(|l| !l.is_empty() && l.ends_with(".md"))
        .map(|l| repo_root.join(l))
        .collect())
}

/// Returns all `.md` files in the repository via a full recursive walk, skipping
/// known noise directories (`node_modules`, `dist`, `target`, `.next`, `coverage`,
/// `generated-reports`, `local-tmp`, `archived`, `apps-labs`, `.fvm-cache`, `.git`).
///
/// # Errors
///
/// This function currently never returns an error (filesystem errors are silently
/// swallowed), but the signature is kept for future extensibility.
fn get_all_markdown_files(repo_root: &Path) -> std::result::Result<Vec<PathBuf>, Error> {
    let mut files = Vec::new();
    let walker = WalkDir::new(repo_root).into_iter().filter_entry(|e| {
        if e.file_type().is_dir() {
            let name = e.file_name().to_string_lossy().to_string();
            !FULL_REPO_SKIP_DIRS.contains(&name.as_str())
        } else {
            true
        }
    });
    for entry in walker.flatten() {
        if entry.file_type().is_file() && entry.path().extension().is_some_and(|e| e == "md") {
            files.push(entry.path().to_path_buf());
        }
    }
    Ok(files)
}

/// Removes paths from `files` that start with any of the `skip_paths` prefixes
/// (relative to `repo_root`).
fn filter_skip_paths(files: Vec<PathBuf>, repo_root: &Path, skip_paths: &[String]) -> Vec<PathBuf> {
    if skip_paths.is_empty() {
        return files;
    }
    files
        .into_iter()
        .filter(|f| {
            let rel = match f.strip_prefix(repo_root) {
                Ok(r) => r.to_string_lossy().to_string(),
                Err(_) => return true,
            };
            for skip in skip_paths {
                if rel.starts_with(skip) {
                    return false;
                }
            }
            true
        })
        .collect()
}

/// Replaces inline code spans (`` `...` `` and ` ``...`` `) with spaces,
/// preserving byte positions so regex match offsets remain valid.
fn strip_inline_code_spans(line: &str) -> String {
    let bytes = line.as_bytes();
    let len = bytes.len();
    let mut out: Vec<u8> = bytes.to_vec();
    let mut i = 0;
    while i < len {
        if bytes[i] == b'`' {
            let tick_count = if i + 1 < len && bytes[i + 1] == b'`' {
                2
            } else {
                1
            };
            let start = i;
            i += tick_count;
            let mut found = false;
            while i < len {
                if tick_count == 2 && i + 1 < len && bytes[i] == b'`' && bytes[i + 1] == b'`' {
                    i += 2;
                    found = true;
                    break;
                } else if tick_count == 1 && bytes[i] == b'`' {
                    i += 1;
                    found = true;
                    break;
                }
                i += 1;
            }
            if found {
                for b in &mut out[start..i] {
                    *b = b' ';
                }
            }
        } else {
            i += 1;
        }
    }
    String::from_utf8(out).unwrap_or_else(|_| line.to_string())
}

/// Extracts all relative links from `path`, skipping lines inside fenced code blocks
/// and inline code spans, discarding external URLs and placeholder patterns.
///
/// # Errors
///
/// Returns an error when the file cannot be read.
fn extract_links(path: &Path) -> std::result::Result<Vec<LinkInfo>, Error> {
    let data = fs::read_to_string(path)?;
    let mut links = Vec::new();
    let mut in_code_block = false;
    for (i, line) in data.split('\n').enumerate() {
        let line_num = i + 1;
        if line.trim_start().starts_with("```") {
            in_code_block = !in_code_block;
            continue;
        }
        if in_code_block {
            continue;
        }
        let stripped = strip_inline_code_spans(line);
        for cap in link_re().captures_iter(&stripped) {
            let mut url = cap[2].to_string();
            url = url
                .trim_start_matches('<')
                .trim_end_matches('>')
                .to_string();
            if url.starts_with("http://")
                || url.starts_with("https://")
                || url.starts_with("mailto:")
            {
                continue;
            }
            if should_skip_link(&url) {
                continue;
            }
            links.push(LinkInfo {
                line_number: line_num,
                url,
            });
        }
    }
    Ok(links)
}

/// Converts a heading title string to a GitHub-flavoured markdown anchor slug.
///
/// Rules: lowercase, remove all chars that are not alphanumeric, underscore,
/// space, or hyphen, then replace spaces with hyphens (no collapsing).
/// Verified against the `github-slugger` v2 reference implementation —
/// underscores (`U+005F`) and Unicode letters/digits are KEPT.
pub fn github_slug(title: &str) -> String {
    title
        .to_lowercase()
        .chars()
        .map(|c| {
            if c.is_alphanumeric() || c == '-' || c == '_' {
                c
            } else if c == ' ' {
                '-'
            } else {
                '\0'
            }
        })
        .filter(|&c| c != '\0')
        .collect()
}

/// Collects all ATX heading titles from `content` (fence-aware) as
/// `(line, level, title)` tuples.  Shares the same fence-aware logic as
/// `heading_hierarchy::collect_headings`.
pub(crate) fn collect_atx_headings(content: &str) -> Vec<(usize, usize, String)> {
    use super::heading_hierarchy::{parse_fence_open_pub, parse_heading_level_pub};
    let mut out = Vec::new();
    let mut in_fence = false;
    let mut fence_char: char = ' ';
    let mut fence_len: usize = 0;
    for (i, line) in content.split('\n').enumerate() {
        let line_num = i + 1;
        let trimmed = line.trim_start_matches([' ', '\t']);
        if let Some((ch, length)) = parse_fence_open_pub(trimmed) {
            if !in_fence {
                in_fence = true;
                fence_char = ch;
                fence_len = length;
            } else if ch == fence_char && length >= fence_len {
                in_fence = false;
                fence_char = ' ';
                fence_len = 0;
            }
            continue;
        }
        if in_fence {
            continue;
        }
        if let Some(level) = parse_heading_level_pub(trimmed) {
            // Extract the title text (after `#`s and the mandatory space/tab)
            let bytes = trimmed.as_bytes();
            let title = trimmed[level + 1..].trim().to_string();
            if !title.is_empty() {
                let _ = bytes; // suppress unused-variable warning
                out.push((line_num, level, title));
            }
        }
    }
    out
}

/// Builds a [`HashSet`] of all GitHub-slugified anchor names (with duplicate
/// collision suffixes applied) for `content`.
pub(crate) fn slugs_from_content(content: &str) -> HashSet<String> {
    let headings = collect_atx_headings(content);
    let mut slug_counts: HashMap<String, usize> = HashMap::new();
    let mut result = HashSet::new();
    for (_, _, title) in &headings {
        let base = github_slug(title);
        let count = slug_counts.entry(base.clone()).or_insert(0);
        let slug = if *count == 0 {
            base.clone()
        } else {
            format!("{base}-{count}")
        };
        *count += 1;
        result.insert(slug);
    }
    result
}

/// Returns `true` when `link` matches a known placeholder or example pattern that
/// should not be validated against the filesystem.
pub fn should_skip_link(link: &str) -> bool {
    if link.starts_with('/') {
        return true;
    }
    if link.contains("{{<") || link.contains("{{%") {
        return true;
    }
    let placeholders = [
        "path.md",
        "target",
        "link",
        "./path/to/",
        "../path/to/",
        "path/to/convention.md",
        "path/to/practice.md",
        "path/to/rule.md",
        "./relative/path/to/",
    ];
    for p in &placeholders {
        if link.contains(p) {
            return true;
        }
    }
    if bracket_placeholder_re().is_match(link) {
        return true;
    }
    if link == "path" || link == "target" || link == "link" {
        return true;
    }
    if link.contains("/images/") && !link.starts_with("../") {
        return true;
    }
    let example_patterns = [
        "./overview",
        "./guide.md",
        "./examples.md",
        "./reference.md",
        "./diagram.png",
        "./image.png",
        "./screenshots/",
        "./auth-guide.md",
        "by-concept/beginner",
        "./by-example/beginner",
        "swe/prog-lang/",
        "../parent",
        "./ai/",
        "../swe/",
        "../../advanced/",
        "url",
        "./LICENSE",
        "../../features.md",
        "../../.opencode/",
    ];
    for p in &example_patterns {
        if link.contains(p) {
            return true;
        }
    }
    false
}

/// Path fragments identifying a skill tree, whose files are exempt from link
/// validation.
///
/// The exemption is a property of skill files as a class, not of one directory:
/// `.agents/skills/` holds a byte-for-byte mirror of `.claude/skills/`, so a rule
/// keyed on the canonical path alone would validate the copy while exempting the
/// original and report the same bytes as both broken and fine.
const SKILL_TREE_MARKERS: &[&str] = &[".claude/skills/", ".agents/skills/"];

/// Validates each link in `links` against the filesystem, relative to `file_path`.
///
/// Skill files (see [`SKILL_TREE_MARKERS`]) are unconditionally skipped.
/// After checking file existence, anchor fragments are validated against the
/// headings of the target file (or the source file for pure `#fragment` links).
///
/// # Errors
///
/// This function currently never returns an error but retains the `Result` return
/// type for future extensibility.
fn validate_file(
    file_path: &Path,
    opts: &ScanOptions,
    links: &[LinkInfo],
) -> std::result::Result<Vec<BrokenLink>, Error> {
    // Skill files: skip validation, in whichever skill tree they live.
    let p_str = file_path.to_string_lossy();
    if SKILL_TREE_MARKERS
        .iter()
        .any(|marker| p_str.contains(marker))
    {
        return Ok(Vec::new());
    }
    let mut broken = Vec::new();
    for link in links {
        let rel = file_path.strip_prefix(&opts.repo_root).map_or_else(
            |_| file_path.to_string_lossy().to_string(),
            |p| p.to_string_lossy().to_string(),
        );

        // Split URL into path-part and optional anchor fragment.
        let (path_part, fragment) = if let Some(hash_pos) = link.url.find('#') {
            (&link.url[..hash_pos], Some(&link.url[hash_pos + 1..]))
        } else {
            (link.url.as_str(), None)
        };

        if path_part.is_empty() {
            // Pure same-file anchor: `[text](#fragment)` — validate against source file.
            if let (Some(frag), Ok(content)) = (
                fragment.filter(|f| !f.is_empty()),
                fs::read_to_string(file_path),
            ) {
                let slugs = slugs_from_content(&content);
                if !slugs.contains(frag) {
                    broken.push(BrokenLink {
                        line_number: link.line_number,
                        source_file: rel,
                        link_text: link.url.clone(),
                        target_path: format!("{}#{frag}", file_path.to_string_lossy()),
                        category: "broken-anchor".to_string(),
                    });
                }
            }
            continue;
        }

        let target = resolve_link(file_path, path_part);
        if !target.exists() {
            let category = categorize_broken_link(&link.url);
            broken.push(BrokenLink {
                line_number: link.line_number,
                source_file: rel,
                link_text: link.url.clone(),
                target_path: target.to_string_lossy().to_string(),
                category,
            });
        } else if let Some(frag) = fragment.filter(|f| !f.is_empty()) {
            // File exists — validate the anchor against the target's headings.
            if let Ok(content) = fs::read_to_string(&target) {
                let slugs = slugs_from_content(&content);
                if !slugs.contains(frag) {
                    broken.push(BrokenLink {
                        line_number: link.line_number,
                        source_file: rel,
                        link_text: link.url.clone(),
                        target_path: format!("{}#{frag}", target.to_string_lossy()),
                        category: "broken-anchor".to_string(),
                    });
                }
            }
        }
    }
    Ok(broken)
}

/// Resolves a relative `link` against the directory containing `source_file`.
///
/// Anchor fragments (everything after `#`) are stripped before resolution.
/// An empty link (pure anchor) returns `source_file` unchanged.
///
/// # Panics
///
/// Panics if `source_file` has no parent component (i.e. it is a bare filename
/// with no directory component and no parent at the filesystem root), which
/// cannot happen for any real repository file path.
fn resolve_link(source_file: &Path, link: &str) -> PathBuf {
    let without_anchor = link.split('#').next().unwrap_or("");
    if without_anchor.is_empty() {
        return source_file.to_path_buf();
    }
    let parent = source_file.parent().unwrap_or(Path::new(""));
    let joined = parent.join(without_anchor);
    // filepath.Clean equivalent: normalize . and ..
    clean_path(&joined)
}

/// Normalises a path by resolving `.` and `..` components, equivalent to Go's
/// `filepath.Clean`.
fn clean_path(p: &Path) -> PathBuf {
    let mut out = Vec::new();
    let mut is_abs = false;
    for comp in p.components() {
        use std::path::Component;
        match comp {
            Component::CurDir | Component::Prefix(_) => {}
            Component::ParentDir => {
                if matches!(out.last(), Some(s) if s != ".." && s != "/") {
                    out.pop();
                } else {
                    out.push("..".to_string());
                }
            }
            Component::Normal(s) => out.push(s.to_string_lossy().to_string()),
            Component::RootDir => {
                is_abs = true;
                out.clear();
            }
        }
    }
    let mut result = PathBuf::new();
    if is_abs {
        result.push("/");
    }
    for c in out {
        result.push(c);
    }
    if result.as_os_str().is_empty() {
        result.push(".");
    }
    result
}

/// Assigns a human-readable category string to a broken link for report grouping.
pub fn categorize_broken_link(link: &str) -> String {
    if link.contains("workflows/") && !link.contains("repo-governance/workflows/") {
        return "workflows/ paths".to_string();
    }
    if link.contains("vision/") && !link.contains("repo-governance/vision/") {
        return "vision/ paths".to_string();
    }
    if link.contains("conventions/README.md") {
        return "conventions README".to_string();
    }
    if link == "CODE_OF_CONDUCT.md" || link == "CHANGELOG.md" {
        return "Missing files".to_string();
    }
    "General/other paths".to_string()
}

/// Formats `result` as a human-readable plain-text report.
///
/// When `quiet` is `true` and there are no broken links, returns an empty string.
/// The `_verbose` flag is reserved for future use.
pub fn format_link_text(result: &LinkValidationResult, _verbose: bool, quiet: bool) -> String {
    let mut output = String::new();
    if result.broken_links.is_empty() {
        if !quiet {
            output.push_str("All links valid! No broken links found.\n");
        }
        return output;
    }
    output.push_str("# Broken Links Report\n\n");
    let _ = writeln!(
        output,
        "**Total broken links**: {}",
        result.broken_links.len()
    );

    let category_order = [
        "Legacy prefixed paths",
        "Missing files",
        "General/other paths",
        "workflows/ paths",
        "vision/ paths",
        "conventions README",
        "broken-anchor",
    ];

    for category in &category_order {
        let links = match result.broken_by_category.get(*category) {
            Some(l) if !l.is_empty() => l,
            _ => continue,
        };
        let _ = write!(output, "\n## {category} ({} links)\n", links.len());

        let mut by_file: HashMap<String, Vec<BrokenLink>> = HashMap::new();
        for link in links {
            by_file
                .entry(link.source_file.clone())
                .or_default()
                .push(link.clone());
        }
        let mut files: Vec<String> = by_file.keys().cloned().collect();
        files.sort();
        for file in files {
            let _ = write!(output, "\n### {file}\n\n");
            let mut file_links = by_file.remove(&file).unwrap_or_default();
            file_links.sort_by_key(|l| l.line_number);
            for link in file_links {
                let _ = writeln!(output, "- Line {}: `{}`", link.line_number, link.link_text);
            }
        }
    }
    output
}

/// Formats `result` as a pretty-printed JSON string.
///
/// # Errors
///
/// Returns an error when JSON serialisation fails (extremely unlikely with
/// the simple data types involved).
pub fn format_link_json(result: &LinkValidationResult) -> std::result::Result<String, Error> {
    use serde::Serialize;

    /// JSON shape for a single broken link entry.
    #[derive(Serialize)]
    struct JsonBrokenLink<'a> {
        /// Repository-relative path of the source file.
        source_file: &'a str,
        /// One-based line number.
        line_number: usize,
        /// Raw link target string.
        link_text: &'a str,
        /// Absolute path the link resolved to.
        target_path: &'a str,
    }

    /// Top-level JSON output object.
    #[derive(Serialize)]
    struct JsonOutput<'a> {
        /// `"success"` or `"failure"`.
        status: &'a str,
        /// ISO-8601 timestamp of the scan.
        timestamp: String,
        /// Total files scanned.
        total_files: usize,
        /// Total relative links examined.
        total_links: usize,
        /// Number of broken links found.
        broken_count: usize,
        /// Wall-clock duration of the scan in milliseconds.
        duration_ms: i64,
        /// Broken links grouped by category. A `BTreeMap` for the same
        /// determinism reason as `LinkValidationResult::broken_by_category`.
        categories: BTreeMap<&'a str, Vec<JsonBrokenLink<'a>>>,
    }

    let status = if result.broken_links.is_empty() {
        "success"
    } else {
        "failure"
    };
    let timestamp = Local::now().format("%Y-%m-%dT%H:%M:%S%:z").to_string();
    let mut categories: BTreeMap<&str, Vec<JsonBrokenLink>> = BTreeMap::new();
    for (cat, links) in &result.broken_by_category {
        let jl: Vec<JsonBrokenLink> = links
            .iter()
            .map(|l| JsonBrokenLink {
                source_file: &l.source_file,
                line_number: l.line_number,
                link_text: &l.link_text,
                target_path: &l.target_path,
            })
            .collect();
        categories.insert(cat.as_str(), jl);
    }
    let out = JsonOutput {
        status,
        timestamp,
        total_files: result.total_files,
        total_links: result.total_links,
        broken_count: result.broken_links.len(),
        duration_ms: result.scan_duration_ms,
        categories,
    };
    Ok(serde_json::to_string_pretty(&out)?)
}

/// Formats `result` as a Markdown report (delegates to [`format_link_text`]).
pub fn format_link_markdown(result: &LinkValidationResult) -> String {
    format_link_text(result, false, false)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    /// Both skill trees are exempt from link validation, and a non-skill path is
    /// not. `.agents/skills/` holds a byte-for-byte mirror of `.claude/skills/`,
    /// so exempting one but not the other would report identical bytes as both
    /// broken and fine.
    #[test]
    fn every_skill_tree_is_exempt_and_nothing_else_is() {
        let dir = TempDir::new().unwrap();
        let root = dir.path();
        let opts = ScanOptions {
            repo_root: root.to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let dangling = vec![LinkInfo {
            line_number: 1,
            url: "./definitely-not-here.md".to_string(),
        }];

        for marker in SKILL_TREE_MARKERS {
            let file = root.join(marker).join("some-skill/reference/page.md");
            fs::create_dir_all(file.parent().unwrap()).unwrap();
            fs::write(&file, "body\n").unwrap();
            assert!(
                validate_file(&file, &opts, &dangling).unwrap().is_empty(),
                "{marker} must be exempt from link validation"
            );
        }

        // Falsifiable the other way: the SAME dangling link outside a skill tree
        // is still reported, so the exemption did not disable the check itself.
        let ordinary = root.join("docs/reference/page.md");
        fs::create_dir_all(ordinary.parent().unwrap()).unwrap();
        fs::write(&ordinary, "body\n").unwrap();
        assert_eq!(
            validate_file(&ordinary, &opts, &dangling).unwrap().len(),
            1,
            "a dangling link outside a skill tree must still be reported"
        );
    }

    /// Verifies that [`should_skip_link`] correctly identifies placeholder and
    /// example links that should not be validated.
    #[test]
    fn skip_link_recognises_placeholders() {
        assert!(should_skip_link("/absolute"));
        assert!(should_skip_link("path"));
        assert!(should_skip_link("target"));
        assert!(should_skip_link("link"));
        assert!(should_skip_link("./relative/path/to/foo"));
        assert!(should_skip_link("[placeholder]-link"));
        assert!(should_skip_link("./images/foo.png"));
        assert!(!should_skip_link("real.md"));
    }

    /// Verifies that [`categorize_broken_link`] assigns the correct category for
    /// each recognised pattern.
    #[test]
    fn categorize_returns_categories() {
        assert_eq!(
            categorize_broken_link("docs/workflows/foo.md"),
            "workflows/ paths"
        );
        assert_eq!(
            categorize_broken_link("docs/vision/foo.md"),
            "vision/ paths"
        );
        assert_eq!(
            categorize_broken_link("conventions/README.md"),
            "conventions README"
        );
        assert_eq!(
            categorize_broken_link("CODE_OF_CONDUCT.md"),
            "Missing files"
        );
        assert_eq!(categorize_broken_link("foo.md"), "General/other paths");
    }

    /// Verifies that [`extract_links`] finds all relative links in a file.
    #[test]
    fn extract_links_finds_valid_links() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("a.md");
        fs::write(&p, "See [link](foo.md) and [code](`bar.md`)\n").unwrap();
        let links = extract_links(&p).unwrap();
        assert_eq!(links.len(), 2);
    }

    /// Verifies that links inside fenced code blocks are ignored.
    #[test]
    fn extract_links_skips_inside_fence() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("a.md");
        fs::write(&p, "```\n[in fence](x.md)\n```\n[outside](y.md)\n").unwrap();
        let links = extract_links(&p).unwrap();
        assert_eq!(links.len(), 1);
        assert_eq!(links[0].url, "y.md");
    }

    /// Verifies that external URLs and mailto links are skipped; same-file anchor
    /// links (`#fragment`) are now extracted for anchor validation.
    #[test]
    fn extract_links_skips_external_urls() {
        let tmp = TempDir::new().unwrap();
        let p = tmp.path().join("a.md");
        fs::write(
            &p,
            "[a](https://example.com) [b](http://x.io) [c](#anchor) [d](mailto:x@y) [e](real.md)\n",
        )
        .unwrap();
        let links = extract_links(&p).unwrap();
        // https, http, mailto are skipped; #anchor and real.md are extracted
        assert_eq!(links.len(), 2);
        assert!(links.iter().any(|l| l.url == "#anchor"));
        assert!(links.iter().any(|l| l.url == "real.md"));
    }

    /// Verifies that [`validate_all_links`] detects broken links in the `docs/` directory.
    #[test]
    fn validate_all_links_returns_broken() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir(tmp.path().join("docs")).unwrap();
        fs::write(tmp.path().join("docs/a.md"), "[bad](nonexistent.md)\n").unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();
        assert_eq!(result.total_files, 1);
        assert!(!result.broken_links.is_empty());
    }

    /// Verifies that a clean scan (no broken links) produces the expected success message.
    #[test]
    fn format_link_text_succeeds_with_no_broken() {
        let result = LinkValidationResult {
            total_files: 5,
            total_links: 20,
            broken_links: Vec::new(),
            broken_by_category: BTreeMap::new(),
            scan_duration_ms: 100,
        };
        let s = format_link_text(&result, false, false);
        assert!(s.contains("All links valid"));
    }

    /// Verifies that `quiet` mode returns an empty string when there are no broken links.
    #[test]
    fn format_link_text_quiet_is_empty_when_clean() {
        let result = LinkValidationResult {
            total_files: 5,
            total_links: 20,
            broken_links: Vec::new(),
            broken_by_category: BTreeMap::new(),
            scan_duration_ms: 100,
        };
        let s = format_link_text(&result, false, true);
        assert!(s.is_empty());
    }

    /// Constructs a [`BrokenLink`] fixture for use in multiple tests.
    fn broken_link() -> BrokenLink {
        BrokenLink {
            line_number: 5,
            source_file: "docs/foo.md".to_string(),
            link_text: "nonexistent.md".to_string(),
            target_path: "docs/nonexistent.md".to_string(),
            category: "General/other paths".to_string(),
        }
    }

    /// Constructs a [`LinkValidationResult`] that contains one broken link.
    fn result_with_broken() -> LinkValidationResult {
        let mut by_cat = BTreeMap::new();
        by_cat.insert("General/other paths".to_string(), vec![broken_link()]);
        LinkValidationResult {
            total_files: 1,
            total_links: 1,
            broken_links: vec![broken_link()],
            broken_by_category: by_cat,
            scan_duration_ms: 50,
        }
    }

    /// Verifies that a text report with broken links includes all expected sections.
    #[test]
    fn format_link_text_with_broken_renders_report() {
        let s = format_link_text(&result_with_broken(), false, false);
        assert!(s.contains("# Broken Links Report"));
        assert!(s.contains("**Total broken links**: 1"));
        assert!(s.contains("General/other paths"));
        assert!(s.contains("docs/foo.md"));
        assert!(s.contains("nonexistent.md"));
    }

    /// Regression test: `category_order` in [`format_link_text`] omitted
    /// `"broken-anchor"`, so broken-anchor findings silently vanished from
    /// text/markdown reports — the summary count still reflected them (and
    /// the command still failed with a non-zero exit code), but the
    /// file/link responsible was never named. Proves the finding's source
    /// file and link text now surface.
    #[test]
    fn format_link_text_includes_broken_anchor_category() {
        let anchor_link = BrokenLink {
            line_number: 3,
            source_file: "docs/index.md".to_string(),
            link_text: "./chapter.md#missing-section".to_string(),
            target_path: "docs/chapter.md#missing-section".to_string(),
            category: "broken-anchor".to_string(),
        };
        let mut by_cat = BTreeMap::new();
        by_cat.insert("broken-anchor".to_string(), vec![anchor_link]);
        let result = LinkValidationResult {
            total_files: 1,
            total_links: 1,
            broken_links: vec![BrokenLink {
                line_number: 3,
                source_file: "docs/index.md".to_string(),
                link_text: "./chapter.md#missing-section".to_string(),
                target_path: "docs/chapter.md#missing-section".to_string(),
                category: "broken-anchor".to_string(),
            }],
            broken_by_category: by_cat,
            scan_duration_ms: 10,
        };
        let s = format_link_text(&result, false, false);
        assert!(s.contains("broken-anchor"), "got: {s}");
        assert!(s.contains("docs/index.md"), "got: {s}");
        assert!(s.contains("./chapter.md#missing-section"), "got: {s}");
    }

    /// Verifies that [`format_link_markdown`] delegates to [`format_link_text`].
    #[test]
    fn format_link_markdown_delegates_to_text() {
        let s = format_link_markdown(&result_with_broken());
        assert!(s.contains("Broken Links Report"));
    }

    /// Verifies that the JSON output for a result with broken links has `"failure"` status.
    #[test]
    fn format_link_json_with_broken_status_failure() {
        let s = format_link_json(&result_with_broken()).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "failure");
        assert_eq!(v["broken_count"], 1);
        assert!(v["categories"]["General/other paths"].is_array());
    }

    /// Verifies that skill files (`.claude/skills/`) are unconditionally skipped.
    #[test]
    fn validate_file_skips_skill_files() {
        let tmp = TempDir::new().unwrap();
        let skill_dir = tmp.path().join(".claude/skills/foo");
        fs::create_dir_all(&skill_dir).unwrap();
        let p = skill_dir.join("SKILL.md");
        fs::write(&p, "[bad](nonexistent.md)\n").unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let links = extract_links(&p).unwrap();
        let broken = validate_file(&p, &opts, &links).unwrap();
        assert!(broken.is_empty());
    }

    /// Verifies that listed `skip_paths` prefixes are removed from the file list.
    #[test]
    fn filter_skip_paths_excludes_listed() {
        let tmp = TempDir::new().unwrap();
        let f1 = tmp.path().join("docs/keep.md");
        let f2 = tmp.path().join("skip/me.md");
        let files = vec![f1.clone(), f2.clone()];
        let filtered = filter_skip_paths(files, tmp.path(), &["skip".to_string()]);
        assert_eq!(filtered.len(), 1);
        assert_eq!(filtered[0], f1);
    }

    /// Verifies that [`resolve_link`] strips anchor fragments before resolving.
    #[test]
    fn resolve_link_handles_anchors() {
        let source = PathBuf::from("/repo/docs/a.md");
        let resolved = resolve_link(&source, "b.md#section");
        assert_eq!(resolved, PathBuf::from("/repo/docs/b.md"));
    }

    /// Verifies that a pure anchor link resolves to the source file itself.
    #[test]
    fn resolve_link_pure_anchor_returns_source() {
        let source = PathBuf::from("/repo/docs/a.md");
        let resolved = resolve_link(&source, "");
        assert_eq!(resolved, source);
    }

    /// Verifies that [`clean_path`] resolves `..` components correctly.
    #[test]
    fn clean_path_resolves_dotdot() {
        let p = PathBuf::from("/a/b/../c");
        let cleaned = clean_path(&p);
        assert_eq!(cleaned, PathBuf::from("/a/c"));
    }

    /// Verifies that [`format_link_json`] produces a `"success"` JSON payload for a clean scan.
    #[test]
    fn format_link_json_has_status() {
        let result = LinkValidationResult {
            total_files: 5,
            total_links: 20,
            broken_links: Vec::new(),
            broken_by_category: BTreeMap::new(),
            scan_duration_ms: 100,
        };
        let s = format_link_json(&result).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "success");
        assert_eq!(v["total_files"], 5);
    }

    // ── Phase 1 RED tests ─────────────────────────────────────────────────────

    /// (a) `--exclude plans/done` removes a broken link under `plans/done` from
    /// results while a broken link elsewhere is still reported.
    #[test]
    fn exclude_suppresses_subtree_but_not_others() {
        let tmp = TempDir::new().unwrap();
        // plans/done/ subtree — should be excluded
        fs::create_dir_all(tmp.path().join("plans/done")).unwrap();
        fs::write(
            tmp.path().join("plans/done/a.md"),
            "[bad](nonexistent.md)\n",
        )
        .unwrap();
        // docs/ subtree — should NOT be excluded
        fs::create_dir_all(tmp.path().join("docs")).unwrap();
        fs::write(tmp.path().join("docs/b.md"), "[bad](also_nonexistent.md)\n").unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: vec!["plans/done".to_string()],
        };
        let result = validate_all_links(&opts).unwrap();
        // plans/done/a.md must not appear in broken links
        assert!(
            result
                .broken_links
                .iter()
                .all(|b| !b.source_file.contains("plans/done")),
            "plans/done broken link should be excluded"
        );
        // docs/b.md must appear
        assert!(
            result
                .broken_links
                .iter()
                .any(|b| b.source_file.contains("docs/b.md")),
            "docs/b.md broken link should still be reported"
        );
    }

    /// (b) A repo-wide scan finds a broken link under `libs/` (outside the
    /// original 3-dir set) and automatically skips files under `node_modules/`.
    #[test]
    fn repo_wide_scan_finds_libs_and_skips_node_modules() {
        let tmp = TempDir::new().unwrap();
        // libs/ — should be scanned in full-repo mode
        fs::create_dir_all(tmp.path().join("libs/rust-commons")).unwrap();
        fs::write(
            tmp.path().join("libs/rust-commons/README.md"),
            "[bad](nonexistent_lib.md)\n",
        )
        .unwrap();
        // node_modules/ — should always be skipped by the full-repo walker
        fs::create_dir_all(tmp.path().join("node_modules/some-pkg")).unwrap();
        fs::write(
            tmp.path().join("node_modules/some-pkg/README.md"),
            "[bad](nm_nonexistent.md)\n",
        )
        .unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();
        // libs/rust-commons/README.md broken link must be found
        assert!(
            result
                .broken_links
                .iter()
                .any(|b| b.source_file.contains("libs/rust-commons")),
            "libs/ broken link should be found by full-repo walk"
        );
        // node_modules must not appear
        assert!(
            result
                .broken_links
                .iter()
                .all(|b| !b.source_file.contains("node_modules")),
            "node_modules/ should be skipped by full-repo walk"
        );
    }

    /// Regression: FVM's local cache is ignored by Git and must not be treated
    /// as repository documentation by the full-repository link validator.
    #[test]
    fn repo_wide_scan_skips_ignored_fvm_cache() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("docs")).unwrap();
        fs::write(tmp.path().join("docs/valid.md"), "# Valid\n").unwrap();
        fs::create_dir_all(tmp.path().join(".fvm-cache/flutter-sdk")).unwrap();
        fs::write(
            tmp.path().join(".fvm-cache/flutter-sdk/README.md"),
            "[bad](missing-cache-file.md)\n",
        )
        .unwrap();

        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();

        assert_eq!(result.total_files, 1);
        assert!(result.broken_links.is_empty());
    }

    /// (c) A cross-file anchor link `[X](./concepts.md#missing-section)` where
    /// `concepts.md` exists but has no heading that slugifies to `missing-section`
    /// yields a `broken-anchor` finding.
    #[test]
    fn broken_cross_file_anchor_yields_finding() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("docs")).unwrap();
        // source file linking to a specific anchor
        fs::write(
            tmp.path().join("docs/source.md"),
            "[link](./concepts.md#missing-section)\n",
        )
        .unwrap();
        // concepts.md exists but does NOT have `## Missing Section`
        fs::write(
            tmp.path().join("docs/concepts.md"),
            "# Concepts\n\n## Other\n",
        )
        .unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();
        assert!(
            result
                .broken_links
                .iter()
                .any(|b| b.category == "broken-anchor"),
            "expected a broken-anchor finding but got: {:?}",
            result.broken_links
        );
    }

    /// (d) A cross-file anchor link `[X](./concepts.md#real-section)` where
    /// `concepts.md` has `## Real Section` yields NO anchor finding.
    #[test]
    fn valid_cross_file_anchor_yields_no_finding() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("docs")).unwrap();
        fs::write(
            tmp.path().join("docs/source.md"),
            "[link](./concepts.md#real-section)\n",
        )
        .unwrap();
        fs::write(
            tmp.path().join("docs/concepts.md"),
            "# Concepts\n\n## Real Section\n",
        )
        .unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();
        assert!(
            result
                .broken_links
                .iter()
                .all(|b| b.category != "broken-anchor"),
            "should not report broken-anchor for a valid anchor"
        );
    }

    /// (d2) Emoji heading: slug preserves leading hyphen that results from emoji stripping,
    /// matching GitHub's actual behavior (e.g. a heading starting with a leading pictograph
    /// becomes a leading hyphen in the slug).
    #[test]
    fn github_slug_emoji_heading_preserves_leading_hyphen() {
        // GitHub strips the emoji (non-alphanumeric/space/hyphen) leaving a leading space,
        // which becomes a leading hyphen. GitHub keeps it; our slug must match.
        // Unicode escapes (not literal glyphs) per the source-code no-emoji convention.
        assert_eq!(github_slug("\u{1F4DC} WCAG Standards"), "-wcag-standards");
        assert_eq!(github_slug("\u{1F512} Security"), "-security");
        // Non-emoji headings must not regress.
        assert_eq!(github_slug("WCAG Standards"), "wcag-standards");
        assert_eq!(github_slug("Setup"), "setup");
    }

    /// (d3) Underscores are KEPT by GitHub's slugger (`U+005F` is not in the
    /// removal set — verified against `github-slugger` v2: `foo_bar baz` →
    /// `foo_bar-baz`). Our slug must match.
    #[test]
    fn github_slug_keeps_underscores() {
        assert_eq!(github_slug("foo_bar baz"), "foo_bar-baz");
        assert_eq!(github_slug("snake_case"), "snake_case");
        // Multi-space: each space becomes a hyphen, no collapsing (github-slugger: `a  b` → `a--b`).
        assert_eq!(github_slug("a  b"), "a--b");
    }

    /// (e) The slug helper maps duplicate `Setup` headings to `setup` and `setup-1`.
    #[test]
    fn github_slug_handles_duplicate_headings() {
        let content = "# Setup\n\n## Setup\n";
        let headings = collect_atx_headings(content);
        let slugs: Vec<String> = headings.iter().map(|(_, _, t)| github_slug(t)).collect();
        // The raw slugs from both will be "setup"; collision handling is done
        // at the call site. Here we just verify the slug helper itself is correct.
        assert_eq!(slugs[0], "setup");
        assert_eq!(slugs[1], "setup");
        // Verify the dedup logic via the anchor-finding helper
        let slugset = slugs_from_content(content);
        assert!(slugset.contains("setup"), "first Setup → 'setup'");
        assert!(slugset.contains("setup-1"), "second Setup → 'setup-1'");
    }

    /// (f) A same-file anchor `[Y](#own-section)` with no matching heading in the
    /// source file yields a `broken-anchor` finding.
    #[test]
    fn broken_same_file_anchor_yields_finding() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("docs")).unwrap();
        fs::write(
            tmp.path().join("docs/a.md"),
            "# Title\n\n[broken](#no-such-section)\n",
        )
        .unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();
        assert!(
            result
                .broken_links
                .iter()
                .any(|b| b.category == "broken-anchor"),
            "expected broken-anchor for same-file link with no matching heading"
        );
    }

    /// (g) Links inside inline code spans must NOT be reported as broken anchors.
    /// Covers false positives like `[text](#fragment)` appearing in prose descriptions
    /// of link syntax (e.g., plan documentation, technical specs).
    #[test]
    fn inline_code_span_links_not_reported_as_broken() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("docs")).unwrap();
        // File contains backtick-enclosed examples that look like broken anchors
        // but are NOT real links — they are inline code spans.
        fs::write(
            tmp.path().join("docs/spec.md"),
            "# Spec\n\nUse `[text](#fragment)` syntax and `[X](#frag)` form.\n\nAlso `[Y](#own-section)` for same-file.\n",
        )
        .unwrap();
        let opts = ScanOptions {
            repo_root: tmp.path().to_path_buf(),
            staged_only: false,
            skip_paths: Vec::new(),
        };
        let result = validate_all_links(&opts).unwrap();
        assert!(
            result
                .broken_links
                .iter()
                .all(|b| b.category != "broken-anchor"),
            "links inside inline code spans must not produce broken-anchor findings"
        );
    }
}
