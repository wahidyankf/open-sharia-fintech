//! Audit that every covered directory has a `README.md` index (or is exempt
//! as a split directory), that every index links all its siblings, that
//! every link resolves, and that every entry carries a derived annotation —
//! plus a `generate` mode (FR-3.12) that writes conforming indexes instead
//! of reporting their absence.
//!
//! Rename-and-extend of `application/repo_governance/readme_index_audit.rs`
//! (`tech-docs.md` §1.1/§4): the `orphan`/`ghost` detection below is carried
//! forward unchanged; `missing` and `unannotated` are new finding kinds.

use std::collections::{BTreeSet, HashMap, HashSet};
use std::path::{Path, PathBuf};
use std::sync::OnceLock;

use anyhow::{Context, Error, anyhow};
use glob::Pattern;
use regex::Regex;

use crate::application::docs::frontmatter::extract_frontmatter;
use crate::application::fs::port::Fs;

/// A single finding from the README index audit.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ReadmeIndexFinding {
    /// Absolute or relative path of the file (or directory, for `"missing"`)
    /// implicated in the finding.
    pub file: String,
    /// Severity; currently always `"high"`.
    pub severity: String,
    /// Machine-readable violation category: `"orphan"`, `"ghost"`,
    /// `"missing"`, or `"unannotated"`.
    pub kind: String,
    /// Human-readable description of the finding.
    pub message: String,
}

/// Returns a compiled `Regex` that captures the target of a Markdown link
/// whose href ends with `.md` (optionally with a fragment or query string).
fn readme_link_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        // The link-text group tolerates ONE level of nested square brackets
        // (`[Executor Tagging — [AI] vs [HUMAN]](./17-….md)`), which real
        // governance titles use. A flat `[^\]]+` silently fails to match those
        // links, so a correctly-linked sibling was reported as an orphan.
        Regex::new(r"\[(?:[^\[\]]|\[[^\[\]]*\])+\]\(([^)]*\.md(?:[#?][^)]*)?)\)")
            .expect("valid hardcoded regex")
    })
}

/// Returns a compiled `Regex` that matches a `.md` link immediately followed
/// (same line) by an em-dash or double-hyphen annotation separator and
/// non-whitespace text — the `- [<title>](<path>) — <description>
/// <when_to_use>` shape §4.1 requires.
fn annotated_link_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| {
        // Same one-level nested-bracket tolerance as `readme_link_re`.
        Regex::new(r"\[(?:[^\[\]]|\[[^\[\]]*\])+\]\([^)]*\.md(?:[#?][^)]*)?\)\s*(?:—|--)\s*\S")
            .expect("valid hardcoded regex")
    })
}

/// Directory names skipped during the recursive walk.
const SKIP_DIRS: &[&str] = &["node_modules", "target", "dist", "build", ".next", ".git"];

/// Audits every covered directory found under each root in `paths`.
///
/// For each directory that needs an index (has a sibling `.md` file other
/// than `README.md`, or a subdirectory with its own `README.md`), a
/// `README.md` is required — unless a sibling `<dir-name>.md` file exists,
/// making the directory a split-directory whose parent indexes it instead
/// (`tech-docs.md` §4.3).
///
/// For every index file found (a directory's own `README.md`, or a split
/// directory's sibling `<name>.md`), sibling `.md` files and subdirectories
/// containing their own `README.md` must be linked. Unlinked siblings are
/// reported as `"orphan"` findings; links to non-existent targets are
/// reported as `"ghost"` findings; a bare link lacking the derived-annotation
/// format is reported as `"unannotated"`. A directory that needs an index but
/// has none is reported as `"missing"`.
///
/// Paths and globs in `excludes` are skipped.  Findings are sorted by `file`,
/// then by `kind`.
///
/// # Errors
///
/// Returns an error when `paths` is empty or when any file cannot be read.
pub fn audit_readme_index(
    fs: &dyn Fs,
    paths: &[String],
    excludes: &[String],
) -> std::result::Result<Vec<ReadmeIndexFinding>, Error> {
    if paths.is_empty() {
        return Err(anyhow!("at least one path is required"));
    }
    let mut findings = Vec::new();
    for root in paths {
        findings.extend(audit_root(fs, root, excludes)?);
    }
    findings.sort_by(|a, b| a.file.cmp(&b.file).then(a.kind.cmp(&b.kind)));
    Ok(findings)
}

/// Audits every directory reachable from `root`.
fn audit_root(
    fs: &dyn Fs,
    root: &str,
    excludes: &[String],
) -> std::result::Result<Vec<ReadmeIndexFinding>, Error> {
    let root_p = Path::new(root);
    let dirs = list_all_dirs(fs, root_p, excludes)?;
    let mut findings = Vec::new();
    for dir in &dirs {
        findings.extend(audit_one_dir(fs, dir, root_p, excludes)?);
    }
    Ok(findings)
}

/// Audits a single directory: mandatory-README detection, additive
/// sibling-index auditing, and orphan/ghost/unannotated detection.
fn audit_one_dir(
    fs: &dyn Fs,
    dir: &Path,
    root: &Path,
    excludes: &[String],
) -> std::result::Result<Vec<ReadmeIndexFinding>, Error> {
    let mut findings = Vec::new();

    // A sibling "<dir-name>.md" progressive-disclosure parent is still audited
    // as an index over `dir`'s contents whenever it exists, so its own
    // orphan/ghost/unannotated coverage is unchanged. What it no longer does
    // is EXEMPT `dir` from carrying its own README.md: the former FR-3.5
    // split-directory exemption is removed, and every directory now carries a
    // literal README.md with no exception. Both indexes are audited when both
    // exist — each is independently required to list the directory's contents.
    if dir != root
        && let Some(parent) = dir.parent()
        && let Some(name) = dir.file_name()
    {
        let split_index = parent.join(format!("{}.md", name.to_string_lossy()));
        if fs.exists(&split_index) {
            findings.extend(audit_index_file(fs, &split_index, dir, root, excludes)?);
        }
    }

    let readme_path = dir.join("README.md");
    if fs.exists(&readme_path) {
        findings.extend(audit_index_file(fs, &readme_path, dir, root, excludes)?);
        return Ok(findings);
    }

    // No README.md — report "missing" whenever the directory actually holds
    // indexable content (FR-3.1's Applicability rule). The scan root stays
    // exempt for one narrow reason only: a caller passes a covered-tree root
    // deliberately, and every real covered-tree root already carries a
    // top-level README.md. A descendant directory is never exempt.
    if dir == root {
        return Ok(findings);
    }
    let targets = list_sibling_targets(fs, dir, root, excludes)?;
    if !targets.files.is_empty() || !targets.sub_dirs.is_empty() {
        let dir_display = dir.to_string_lossy().to_string();
        findings.push(ReadmeIndexFinding {
            file: dir_display.clone(),
            severity: "high".to_string(),
            kind: "missing".to_string(),
            message: format!(
                "missing: {dir_display} contains indexable content but has no README.md"
            ),
        });
    }
    Ok(findings)
}

/// Audits a single index file (`README.md`, or a split directory's sibling
/// `<name>.md`) against the sibling targets present under `target_dir`.
///
/// # Errors
///
/// Returns an error when the index file or the target directory cannot be
/// read.
fn audit_index_file(
    fs: &dyn Fs,
    index_path: &Path,
    target_dir: &Path,
    root: &Path,
    excludes: &[String],
) -> std::result::Result<Vec<ReadmeIndexFinding>, Error> {
    let index_display = index_path.to_string_lossy().to_string();
    let data = fs
        .read_to_string(index_path)
        .with_context(|| format!("read {index_display}"))?;

    // A split-directory index file (`tech-docs.md` §4.3's exemption) lives in
    // `target_dir`'s *parent*, not in `target_dir` itself — so its link
    // targets are written relative to the parent, carrying an explicit
    // "<target_dir-name>/" prefix (e.g. "ai-agents/01-catalog.md"). Strip
    // that prefix before comparing against `target_dir`'s own sibling names,
    // which are computed relative to `target_dir`.
    let index_dir = index_path.parent().unwrap_or_else(|| Path::new("."));
    let strip_prefix: Option<String> = if index_dir == target_dir {
        None
    } else {
        target_dir
            .file_name()
            .map(|n| format!("{}/", n.to_string_lossy()))
    };
    // Returns the normalized link plus whether `raw` actually carried the
    // `strip_prefix` (i.e. was genuinely written relative to `target_dir`'s
    // parent). This provenance matters below: only a link that never carried
    // the prefix may fall back to resolving against `index_dir` — a
    // prefixed link that fails to resolve under `target_dir` is a genuine
    // ghost, not a same-dir sibling reference, even if a same-named file
    // happens to sit beside `index_dir`.
    let normalize = |raw: &str| -> (String, bool) {
        match strip_prefix.as_deref().and_then(|p| raw.strip_prefix(p)) {
            Some(stripped) => (stripped.to_string(), true),
            None => (raw.to_string(), false),
        }
    };

    // Map from normalized link -> "was this link ever seen prefixed with
    // target_dir's name?". Defaults to `false` (unprefixed); flips to `true`
    // if any raw occurrence of this normalized link carried the prefix, so
    // that the ghost guard below always errs toward reporting rather than
    // silently swallowing a genuine ghost.
    let mut linked_provenance: HashMap<String, bool> = HashMap::new();
    for l in &extract_readme_links(&data) {
        let (normalized, was_prefixed) = normalize(l);
        let entry = linked_provenance.entry(normalized).or_insert(false);
        *entry = *entry || was_prefixed;
    }
    let linked: HashSet<String> = linked_provenance.keys().cloned().collect();
    let unannotated: HashSet<String> = extract_unannotated_link_targets(&data)
        .iter()
        .map(|l| normalize(l).0)
        .collect();
    let actual = list_sibling_targets(fs, target_dir, root, excludes)?;

    let mut findings = Vec::new();

    // Orphans: file on disk but not in the index.
    for name in actual.sorted_names() {
        if linked.contains(&name) {
            continue;
        }
        // A subdirectory target `<name>/README.md` is equally satisfied by a
        // link to its progressive-disclosure parent `<name>.md`: that sibling
        // file is itself an index over the same directory, so the directory is
        // reachable from here either way. Without this, every governance index
        // would have to carry two links to the same content — one to
        // `<name>.md` and one to `<name>/README.md` — now that a split
        // directory also carries its own README.md.
        if let Some(dir_name) = name.strip_suffix("/README.md")
            && linked.contains(&format!("{dir_name}.md"))
        {
            continue;
        }
        let full = target_dir.join(&name);
        findings.push(ReadmeIndexFinding {
            file: full.to_string_lossy().to_string(),
            severity: "high".to_string(),
            kind: "orphan".to_string(),
            message: format!("orphan: {name} exists but is not linked from {index_display}"),
        });
    }

    // Ghosts and unannotated: index links a target.
    let mut sorted_links: Vec<String> = linked.into_iter().collect();
    sorted_links.sort();
    for link in sorted_links {
        if !actual.present(&link) {
            let full = target_dir.join(&link);
            // Cross-dir links (e.g. "agents/foo.md") point to files inside a
            // subdirectory.  If the path exists on disk the link is valid — don't
            // ghost it.  Only report ghost when the target is genuinely missing.
            if fs.exists(&full) {
                continue;
            }
            // A split-index file (index_dir != target_dir) physically lives in
            // index_dir, not target_dir — it may legitimately link a sibling of
            // itself (e.g. "general.md") rather than a child under target_dir.
            // Such a link resolves against index_dir, the file's real location,
            // not target_dir. Check that base too before declaring ghost — but
            // ONLY when this link never carried the target_dir prefix. A link
            // that WAS written with the prefix (e.g. "ai-agents/foo.md") is
            // unambiguously a target_dir-relative reference; if it fails to
            // resolve there it is a genuine ghost, even when an unrelated file
            // with a matching basename happens to sit beside index_dir.
            let was_prefixed = linked_provenance.get(&link).copied().unwrap_or(false);
            if !was_prefixed && index_dir != target_dir && fs.exists(&index_dir.join(&link)) {
                continue;
            }
            findings.push(ReadmeIndexFinding {
                file: full.to_string_lossy().to_string(),
                severity: "high".to_string(),
                kind: "ghost".to_string(),
                message: format!(
                    "ghost: {index_display} references {link} but the target does not exist"
                ),
            });
            continue;
        }
        if unannotated.contains(&link) {
            let full = target_dir.join(&link);
            findings.push(ReadmeIndexFinding {
                file: full.to_string_lossy().to_string(),
                severity: "high".to_string(),
                kind: "unannotated".to_string(),
                message: format!(
                    "unannotated: {index_display} links {link} without a derived annotation \
                     (`- [<title>](<path>) — <description> <when_to_use>`)"
                ),
            });
        }
    }

    Ok(findings)
}

/// Extracts all relative `.md` link targets from `content`, stripping fragment
/// and query suffixes, leading `./`, and ignoring absolute paths, parent paths,
/// and URL-like hrefs.
/// Splits a raw markdown link target into its path part and any trailing
/// `#fragment` / `?query` suffix. The suffix is preserved verbatim by callers
/// that rewrite the path, so an anchor survives a rename.
fn split_link_suffix(target: &str) -> (&str, &str) {
    match target.find(['#', '?']) {
        Some(i) => (&target[..i], &target[i..]),
        None => (target, ""),
    }
}

/// Normalises a raw markdown link target into the canonical sibling-target
/// form the index logic compares on: `./` stripped, any `#fragment`/`?query`
/// dropped, backslashes normalised to `/`.
///
/// Returns `None` for anything that is not a sibling target — an empty target,
/// an absolute path, a parent-relative path, or a URL — so every caller applies
/// one definition of "the same target" instead of re-deriving it.
fn normalize_link_target(raw: &str) -> Option<String> {
    let raw = raw.trim();
    if raw.is_empty() {
        return None;
    }
    let raw = raw.strip_prefix("./").unwrap_or(raw);
    let (raw, _) = split_link_suffix(raw);
    if raw.is_empty() || raw.starts_with('/') || raw.starts_with("..") {
        return None;
    }
    // Skip URLs: leading scheme followed by ":" before the first "/".
    let url_like = match raw.find(':') {
        Some(colon) if colon > 0 => raw.find('/').is_none_or(|s| colon < s),
        _ => false,
    };
    if url_like {
        return None;
    }
    Some(raw.replace('\\', "/"))
}

/// Extracts every sibling `.md` link target found anywhere in `content`,
/// normalised by [`normalize_link_target`].
fn extract_readme_links(content: &str) -> HashSet<String> {
    let mut out = HashSet::new();
    for cap in readme_link_re().captures_iter(content) {
        if let Some(target) = normalize_link_target(&cap[1]) {
            out.insert(target);
        }
    }
    out
}

/// Extracts the link targets of every `.md` link that appears on a line with
/// no derived-annotation suffix (§4.1) — the `"unannotated"` finding kind
/// (dark-launched at Phase 1, not yet armed — `tech-docs.md` §4.3).
fn extract_unannotated_link_targets(content: &str) -> HashSet<String> {
    let mut out = HashSet::new();
    for line in content.lines() {
        if !readme_link_re().is_match(line) || annotated_link_re().is_match(line) {
            continue;
        }
        for cap in readme_link_re().captures_iter(line) {
            let raw = cap[1].trim();
            let raw = raw.strip_prefix("./").unwrap_or(raw);
            let raw = match raw.find(['#', '?']) {
                Some(i) => &raw[..i],
                None => raw,
            };
            if raw.is_empty() || raw.starts_with('/') || raw.starts_with("..") {
                continue;
            }
            out.insert(raw.replace('\\', "/"));
        }
    }
    out
}

/// The set of linkable targets adjacent to an index file.
struct SiblingTargets {
    /// Sibling `.md` files (excluding `README.md` itself).
    files: HashSet<String>,
    /// Subdirectory `README.md` paths relative to the parent directory.
    sub_dirs: HashSet<String>,
}

impl SiblingTargets {
    /// Creates an empty `SiblingTargets`.
    fn new() -> Self {
        Self {
            files: HashSet::new(),
            sub_dirs: HashSet::new(),
        }
    }

    /// Returns a sorted `Vec` of all linkable target names.
    fn sorted_names(&self) -> Vec<String> {
        let mut all: BTreeSet<String> = BTreeSet::new();
        all.extend(self.files.iter().cloned());
        all.extend(self.sub_dirs.iter().cloned());
        all.into_iter().collect()
    }

    /// Returns `true` when `link` refers to a file or subdirectory that exists
    /// on disk, including bare-directory links (e.g., `"structure"` resolves to
    /// `"structure/README.md"`).
    fn present(&self, link: &str) -> bool {
        let normalized = link.replace('\\', "/");
        let normalized = normalized.trim_end_matches('/').to_string();
        if self.files.contains(&normalized) {
            return true;
        }
        if self.sub_dirs.contains(&normalized) {
            return true;
        }
        // Allow bare-directory: "structure" → "structure/README.md".
        let bare = format!("{normalized}/README.md");
        if self.sub_dirs.contains(&bare) {
            return true;
        }
        false
    }
}

/// Lists the sibling `.md` files and subdirectories that contain a `README.md`
/// adjacent to an index file at `dir`, relative to `root`.
///
/// Hidden entries and those in [`SKIP_DIRS`] are excluded.  Paths matching
/// `excludes` globs are also excluded.
///
/// # Errors
///
/// Returns an error when `dir` cannot be read.
fn list_sibling_targets(
    fs: &dyn Fs,
    dir: &Path,
    root: &Path,
    excludes: &[String],
) -> std::result::Result<SiblingTargets, Error> {
    let mut out = SiblingTargets::new();
    let entries = fs
        .read_dir(dir)
        .with_context(|| format!("read dir {}", dir.display()))?;
    for entry in entries {
        let name = entry.name;
        let full = dir.join(&name);
        let rel = match full.strip_prefix(root) {
            Ok(r) => r.to_string_lossy().to_string(),
            Err(_) => name.clone(),
        };
        if matches_any_glob(&rel, excludes) {
            continue;
        }
        if entry.is_dir {
            if name.starts_with('.') || SKIP_DIRS.contains(&name.as_str()) {
                continue;
            }
            let sub_readme = full.join("README.md");
            if fs.exists(&sub_readme) {
                out.sub_dirs
                    .insert(format!("{name}/README.md").replace('\\', "/"));
            }
            continue;
        }
        if name.starts_with('.') {
            continue;
        }
        if name == "README.md" {
            continue;
        }
        if !name.ends_with(".md") {
            continue;
        }
        out.files.insert(name);
    }
    Ok(out)
}

/// Recursively lists every directory reachable from `root` (including `root`
/// itself), skipping [`SKIP_DIRS`] and `excludes`-matched entries.
///
/// Unlike [`list_sibling_targets`]'s per-child dot-name skip (which excludes
/// a hidden directory from needing its own index entry), this walker does
/// **not** apply a blanket dot-prefix exclusion: `tech-docs.md` §4's covered
/// tree explicitly includes dot-directories (`.claude/`, `.codex/`, `.pi/`,
/// `.amazonq/`) as first-class governance content, not build junk — only
/// [`SKIP_DIRS`] (`.git`, `.next`, ...) and `excludes` prune here.
///
/// Returns an empty list when `root` is not a directory.
///
/// # Errors
///
/// Returns an error when a reachable directory cannot be read.
fn list_all_dirs(
    fs: &dyn Fs,
    root: &Path,
    excludes: &[String],
) -> std::result::Result<Vec<PathBuf>, Error> {
    let mut dirs = Vec::new();
    if !fs.is_dir(root) {
        return Ok(dirs);
    }
    dirs.push(root.to_path_buf());
    walk_dirs_recursive(fs, root, root, excludes, &mut dirs)?;
    Ok(dirs)
}

/// Recursive helper for [`list_all_dirs`].
fn walk_dirs_recursive(
    fs: &dyn Fs,
    dir: &Path,
    root: &Path,
    excludes: &[String],
    out: &mut Vec<PathBuf>,
) -> std::result::Result<(), Error> {
    let entries = fs
        .read_dir(dir)
        .with_context(|| format!("read dir {}", dir.display()))?;
    for entry in entries {
        if !entry.is_dir {
            continue;
        }
        if SKIP_DIRS.contains(&entry.name.as_str()) {
            continue;
        }
        let full = dir.join(&entry.name);
        let rel = full.strip_prefix(root).map_or_else(
            |_| full.to_string_lossy().to_string(),
            |p| p.to_string_lossy().to_string(),
        );
        if matches_any_glob(&rel, excludes) {
            continue;
        }
        out.push(full.clone());
        walk_dirs_recursive(fs, &full, root, excludes, out)?;
    }
    Ok(())
}

/// Returns `true` when `rel` matches at least one of the `patterns` using
/// `glob::Pattern`.
///
/// Matching is attempted against the full path, the basename, and each path
/// component.
fn matches_any_glob(rel: &str, patterns: &[String]) -> bool {
    if rel.is_empty() || rel == "." {
        return false;
    }
    let slashed = rel.replace('\\', "/");
    let components: Vec<&str> = slashed.split('/').collect();
    let basename = PathBuf::from(&slashed)
        .file_name()
        .map(|s| s.to_string_lossy().to_string())
        .unwrap_or_default();
    for p in patterns {
        if p.is_empty() {
            continue;
        }
        let Ok(pat) = Pattern::new(p) else {
            continue;
        };
        if pat.matches(&slashed) {
            return true;
        }
        if pat.matches(&basename) {
            return true;
        }
        for c in &components {
            if pat.matches(c) {
                return true;
            }
        }
    }
    false
}

// ===========================================================================
// FR-3.12 — `governance readme-index generate`
// ===========================================================================

/// Frontmatter fields read from a link target to derive its README-index
/// annotation (FR-3.10/FR-3.11). `None` when the field is absent, empty, or
/// the target has no parsable frontmatter at all — `generate` never invents
/// annotation text, it only derives it from what is already on disk.
struct TargetMeta {
    /// The target's `title` frontmatter field.
    title: Option<String>,
    /// The target's `description` frontmatter field.
    description: Option<String>,
    /// The target's `when_to_use` frontmatter field (only meaningful for
    /// `repo-governance/` targets — FR-4.6).
    when_to_use: Option<String>,
}

/// Writes conforming `README.md` (or, for a split directory, sibling
/// `<name>.md`) indexes for every covered directory reachable from `paths`
/// that needs one, per the same applicability rule [`audit_readme_index`]'s
/// `"missing"` finding kind already implements (FR-3.1/FR-3.12) — reusing
/// this module's own [`list_all_dirs`] and [`list_sibling_targets`]
/// file-discovery helpers rather than re-walking the tree a second way.
///
/// Each generated index's Markdown *body* (the H1 heading and the annotated
/// link list) is fully regenerated from what is on disk; an *existing*
/// index's own YAML frontmatter block is preserved verbatim. Frontmatter
/// (`title`/`description`/`when_to_use`) is a distinct, separately gated
/// concern (`md-frontmatter`/FR-4) — not something this generator invents or
/// overwrites. A brand-new index gets a minimal synthesized `title:`
/// frontmatter field only, derived from its directory or file name.
///
/// Idempotent: running this function twice against the same tree produces
/// byte-identical output the second time, because both the entry set (via
/// [`list_sibling_targets`]) and the annotation text (derived from each
/// target's own, untouched frontmatter) are deterministic functions of the
/// files already on disk, and re-running never mutates a target's
/// frontmatter.
///
/// Returns the sorted, de-duplicated list of index files written.
///
/// # Errors
///
/// Returns an error when `paths` is empty, when a directory cannot be read,
/// when an existing index file cannot be read (never silently rebuilt), or
/// when a generated index file cannot be written.
pub fn generate_readme_index(
    fs: &dyn Fs,
    paths: &[String],
    excludes: &[String],
) -> std::result::Result<Vec<PathBuf>, Error> {
    if paths.is_empty() {
        return Err(anyhow!("at least one path is required"));
    }
    let mut written = Vec::new();
    for root in paths {
        written.extend(generate_root(fs, root, excludes)?);
    }
    written.sort();
    written.dedup();
    Ok(written)
}

/// Rewrites markdown **link targets** across every `.md` file reachable from
/// `paths`, according to a rename map of `(old_basename, new_basename)` pairs.
///
/// Only the target inside a `](...)` link is touched. Entry order, annotation
/// text, prose, and every other byte are left exactly as they were — a rename
/// sweep must not become an unreviewable reformat. A bare mention of an old
/// filename in prose is deliberately NOT rewritten, because it is not a link
/// and rewriting it would silently edit narrative text.
///
/// Returns the paths whose content actually changed.
///
/// # Errors
///
/// Returns an error if `paths` is empty or a file cannot be written.
pub fn rewrite_index_paths(
    fs: &dyn Fs,
    paths: &[String],
    map: &[(String, String)],
) -> std::result::Result<Vec<PathBuf>, Error> {
    if paths.is_empty() {
        return Err(anyhow!("at least one path is required"));
    }
    let renames: std::collections::HashMap<&str, &str> =
        map.iter().map(|(o, n)| (o.as_str(), n.as_str())).collect();
    if renames.is_empty() {
        return Ok(Vec::new());
    }

    let mut changed = Vec::new();
    for root in paths {
        for file in fs.walk_files(Path::new(root), &[".git", "node_modules", "target"]) {
            if file.extension().and_then(|e| e.to_str()) != Some("md") {
                continue;
            }
            let Ok(content) = fs.read_to_string(&file) else {
                continue;
            };
            let updated = rewrite_link_targets(&content, &renames);
            if updated != content {
                fs.write_string(&file, &updated)
                    .with_context(|| format!("write {}", file.display()))?;
                changed.push(file);
            }
        }
    }
    changed.sort();
    changed.dedup();
    Ok(changed)
}

/// Rewrites every markdown link target in `content` whose final path segment
/// matches a key in `renames`, preserving the target's directory prefix and any
/// `#fragment`/`?query` suffix.
fn rewrite_link_targets(content: &str, renames: &std::collections::HashMap<&str, &str>) -> String {
    let mut out = String::with_capacity(content.len());
    let mut rest = content;
    while let Some(open) = rest.find("](") {
        let (head, tail) = rest.split_at(open + 2);
        out.push_str(head);
        let Some(close) = tail.find(')') else {
            rest = tail;
            break;
        };
        let (target, after) = tail.split_at(close);
        out.push_str(&rewrite_one_target(target, renames));
        rest = after;
    }
    out.push_str(rest);
    out
}

/// Rewrites a single link target, or returns it unchanged.
fn rewrite_one_target(target: &str, renames: &std::collections::HashMap<&str, &str>) -> String {
    // Split off a trailing #fragment / ?query so it survives the rename.
    let (path_part, suffix) = split_link_suffix(target);
    let Some(slash) = path_part.rfind('/') else {
        return match renames.get(path_part) {
            Some(new) => format!("{new}{suffix}"),
            None => target.to_string(),
        };
    };
    let (dir, base) = path_part.split_at(slash + 1);
    match renames.get(base) {
        Some(new) => format!("{dir}{new}{suffix}"),
        None => target.to_string(),
    }
}

/// Generates every index reachable from `root` that needs one.
fn generate_root(
    fs: &dyn Fs,
    root: &str,
    excludes: &[String],
) -> std::result::Result<Vec<PathBuf>, Error> {
    let root_p = Path::new(root);
    let dirs = list_all_dirs(fs, root_p, excludes)?;
    let mut written = Vec::new();
    for dir in &dirs {
        written.extend(generate_one_dir(fs, dir, root_p, excludes)?);
    }
    Ok(written)
}

/// Mirrors [`audit_one_dir`]'s sibling-index / existing-index /
/// root-exemption / applicability decision tree exactly, so `generate` and
/// `validate` never disagree about which directories need an index — but
/// writes conforming files instead of reporting `"missing"` findings.
///
/// Returns every index written for this directory: the progressive-disclosure
/// sibling index when one exists, and `dir/README.md`, which is now mandatory
/// rather than substitutable (the former FR-3.5 exemption is removed).
fn generate_one_dir(
    fs: &dyn Fs,
    dir: &Path,
    root: &Path,
    excludes: &[String],
) -> std::result::Result<Vec<PathBuf>, Error> {
    let mut written = Vec::new();

    // A sibling "<dir-name>.md" progressive-disclosure parent is still
    // regenerated as an index over `dir`, carrying the FR-3.6 link prefix. It
    // no longer substitutes for `dir/README.md`.
    if dir != root
        && let Some(parent) = dir.parent()
        && let Some(name) = dir.file_name()
    {
        let split_index = parent.join(format!("{}.md", name.to_string_lossy()));
        if fs.exists(&split_index) {
            let link_prefix = format!("{}/", name.to_string_lossy());
            written.push(generate_index_file(
                fs,
                &split_index,
                dir,
                root,
                excludes,
                &link_prefix,
            )?);
        }
    }

    let readme_path = dir.join("README.md");
    if fs.exists(&readme_path) {
        written.push(generate_index_file(
            fs,
            &readme_path,
            dir,
            root,
            excludes,
            "",
        )?);
        return Ok(written);
    }

    // No README.md on disk yet. Mirror `audit_one_dir`'s root exemption: the
    // scan root itself is never auto-created (a caller passes a covered-tree
    // root deliberately — see `audit_one_dir`'s doc comment for the full
    // rationale); only a genuine descendant directory gets a brand-new index.
    if dir == root {
        return Ok(written);
    }
    let targets = list_sibling_targets(fs, dir, root, excludes)?;
    if targets.files.is_empty() && targets.sub_dirs.is_empty() {
        return Ok(written);
    }
    written.push(generate_index_file(
        fs,
        &readme_path,
        dir,
        root,
        excludes,
        "",
    )?);
    Ok(written)
}

/// Writes a single conforming index file at `index_path`, listing every
/// sibling target in `target_dir` (reusing [`list_sibling_targets`], the
/// same file-discovery helper [`audit_index_file`] uses). `link_prefix` is
/// `""` when `index_path` lives inside `target_dir` itself (the common
/// case), or `"<target_dir-name>/"` for a split directory's sibling index,
/// whose link targets carry an explicit directory prefix (FR-3.6).
///
/// # Errors
///
/// Returns an error when `target_dir` cannot be read or `index_path` cannot
/// be written.
/// Returns the zero-based line numbers of an existing index's entry lines —
/// every list item that links a sibling `.md` target — in document order.
///
/// Only the positions are needed: whether a target is already indexed is
/// decided by [`extract_readme_links`] over the whole document (a link in a
/// table cell or a sentence counts, exactly as it does for `audit_one_dir`),
/// while these positions decide only *where* a genuinely missing entry is
/// spliced in.
///
/// Returns an empty vector when the index contains no such entries — precisely
/// the scaffold case, where the caller derives the whole list from disk.
fn existing_entry_lines(content: &str) -> Vec<usize> {
    let mut out = Vec::new();
    for (line_no, line) in content.lines().enumerate() {
        let trimmed = line.trim_start();
        if !(trimmed.starts_with("- ") || trimmed.starts_with("* ")) {
            continue;
        }
        let Some(cap) = readme_link_re().captures(line) else {
            continue;
        };
        if normalize_link_target(&cap[1]).is_some() {
            out.push(line_no);
        }
    }
    out
}

/// Writes `index_path`, preserving any existing entry order and annotations
/// and appending only the sibling targets absent from it.
///
/// # Errors
///
/// Returns an error if the directory cannot be listed or the index cannot be
/// written.
fn generate_index_file(
    fs: &dyn Fs,
    index_path: &Path,
    target_dir: &Path,
    root: &Path,
    excludes: &[String],
    link_prefix: &str,
) -> std::result::Result<PathBuf, Error> {
    let targets = list_sibling_targets(fs, target_dir, root, excludes)?;

    // Builds the entry line for one sibling target.
    let entry_for = |name: &str| {
        let link = format!("./{link_prefix}{name}");
        let target_path = target_dir.join(name);
        let meta = read_target_meta(fs, &target_path);
        let title = meta
            .title
            .clone()
            .unwrap_or_else(|| fallback_entry_title(name));
        let is_governance = path_is_repo_governance(&target_path);
        format_entry(&title, &link, is_governance, &meta)
    };

    // An index that already exists is EDITED, never rebuilt. Reading order is
    // authored, and so is everything around the list — section headings,
    // grouping prose, trailing notes. Rebuilding the body would silently
    // delete all of it, so missing entries are spliced in beside the existing
    // list and every other byte is left alone. A directory with no index takes
    // the scaffold path below.
    if fs.exists(index_path) {
        // The index is known to exist: a read failure here (invalid UTF-8, a
        // transient permission error, a TOCTOU race) must propagate as an
        // error, never fall through to the scaffold path below. Conflating
        // "no index on disk" with "index exists but could not be read" would
        // silently overwrite an existing, authored document.
        let content = fs
            .read_to_string(index_path)
            .with_context(|| format!("read {}", index_path.display()))?;
        let entry_lines = existing_entry_lines(&content);
        // Membership is decided by the WHOLE document's link set, exactly as
        // `audit_one_dir` decides it. A target linked from a table cell or a
        // prose sentence is already indexed; re-appending it as a list entry
        // would add a duplicate link `validate` never asked for. The
        // line-scanned `entry_lines` are used only to pick the splice point.
        let already: HashSet<String> = extract_readme_links(&content);
        // Compare on the SAME key the emitted link uses. For a split index
        // (`<name>.md` indexing `<name>/`), `link_prefix` is `<name>/`, so an
        // already-present link normalises to `<name>/01-foo.md` while
        // `sorted_names()` yields the bare `01-foo.md`. Comparing the bare
        // form against prefixed keys marks every existing entry "missing" and
        // duplicates the whole index.
        let missing: Vec<String> = targets
            .sorted_names()
            .into_iter()
            .filter(|n| !already.contains(&format!("{link_prefix}{n}")))
            // Same split-pattern exemption `audit_one_dir` applies: when the
            // index already links `<dir>.md`, the sibling `<dir>/README.md` is
            // an index over the same content and is NOT a second missing
            // entry. Without this, `generate` would append a duplicate link
            // that `validate` never asked for, and the two would disagree
            // about what a complete index is.
            .filter(|n| {
                n.strip_suffix("/README.md")
                    .is_none_or(|dir| !already.contains(&format!("{link_prefix}{dir}.md")))
            })
            .map(|n| entry_for(&n))
            .collect();

        if missing.is_empty() {
            // Already complete: writing nothing is what keeps `generate` safe
            // to run over a conforming tree.
            return Ok(index_path.to_path_buf());
        }

        let mut lines: Vec<String> = content.lines().map(String::from).collect();
        let insert_at = entry_lines
            .iter()
            .map(|n| n + 1)
            .max()
            .unwrap_or(lines.len());
        for (offset, entry) in missing.into_iter().enumerate() {
            lines.insert(insert_at + offset, entry);
        }
        let mut updated = lines.join("\n");
        if content.ends_with('\n') {
            updated.push('\n');
        }
        fs.write_string(index_path, &updated)
            .with_context(|| format!("write {}", index_path.display()))?;
        return Ok(index_path.to_path_buf());
    }

    // Scaffold path: no index on disk, so derive the whole document.
    let lines: Vec<String> = targets
        .sorted_names()
        .iter()
        .map(|n| entry_for(n))
        .collect();
    let dir_title_fallback = fallback_index_title(index_path);
    let (frontmatter, h1_title) =
        resolve_frontmatter_and_title(fs, index_path, &dir_title_fallback);
    let body = if lines.is_empty() {
        format!("# {h1_title}\n")
    } else {
        format!("# {h1_title}\n\n{}\n", lines.join("\n"))
    };
    let content = format!("---\n{frontmatter}\n---\n\n{body}");

    fs.write_string(index_path, &content)
        .with_context(|| format!("write {}", index_path.display()))?;
    Ok(index_path.to_path_buf())
}

/// Reads and returns `index_path`'s existing YAML frontmatter block verbatim
/// (never regenerated — a separate, `md-frontmatter`-gated concern) plus the
/// title text to use for the generated H1 heading. Falls back to
/// `dir_title_fallback` — for both the frontmatter's `title:` field and the
/// H1 — when `index_path` does not yet exist or has no frontmatter of its
/// own.
fn resolve_frontmatter_and_title(
    fs: &dyn Fs,
    index_path: &Path,
    dir_title_fallback: &str,
) -> (String, String) {
    if fs.exists(index_path)
        && let Ok(existing) = fs.read_to_string(index_path)
        && let Some(fm_block) = extract_frontmatter(&existing)
    {
        let title = serde_norway::from_str::<serde_norway::Value>(&fm_block)
            .ok()
            .and_then(|v| non_empty_frontmatter_string(&v, "title"))
            .unwrap_or_else(|| dir_title_fallback.to_string());
        return (fm_block, title);
    }
    (
        format!("title: \"{dir_title_fallback}\""),
        dir_title_fallback.to_string(),
    )
}

/// Reads `path`'s frontmatter `title`/`description`/`when_to_use` fields
/// (FR-3.11's derivation source), tolerating a target with no frontmatter at
/// all (every field is then `None` — the entry is generated bare rather than
/// with an invented annotation).
fn read_target_meta(fs: &dyn Fs, path: &Path) -> TargetMeta {
    let empty = || TargetMeta {
        title: None,
        description: None,
        when_to_use: None,
    };
    let Ok(content) = fs.read_to_string(path) else {
        return empty();
    };
    let Some(fm_block) = extract_frontmatter(&content) else {
        return empty();
    };
    let Ok(value) = serde_norway::from_str::<serde_norway::Value>(&fm_block) else {
        return empty();
    };
    TargetMeta {
        title: non_empty_frontmatter_string(&value, "title"),
        description: non_empty_frontmatter_string(&value, "description"),
        when_to_use: non_empty_frontmatter_string(&value, "when_to_use"),
    }
}

/// Returns `value[key]` as a trimmed, non-empty `String`, or `None` when the
/// key is absent, not a string, or empty/whitespace-only.
fn non_empty_frontmatter_string(value: &serde_norway::Value, key: &str) -> Option<String> {
    value
        .get(key)
        .and_then(serde_norway::Value::as_str)
        .map(str::trim)
        .filter(|s| !s.is_empty())
        .map(std::string::ToString::to_string)
}

/// Formats one annotated index entry (FR-3.10/FR-3.13):
/// `- [<title>](<link>) — <description> <when_to_use>` for a
/// `repo-governance/` target with both fields present, `- [<title>](<link>)
/// — <description>` for every other target (or a governance target missing
/// `when_to_use`), and a bare `- [<title>](<link>)` when the target has no
/// `description` to derive one from at all — never a fabricated annotation.
fn format_entry(title: &str, link: &str, is_governance: bool, meta: &TargetMeta) -> String {
    match &meta.description {
        Some(description) => {
            if is_governance && let Some(when_to_use) = &meta.when_to_use {
                format!("- [{title}]({link}) — {description} {when_to_use}")
            } else {
                format!("- [{title}]({link}) — {description}")
            }
        }
        None => format!("- [{title}]({link})"),
    }
}

/// Returns `true` when `path` lies under a `repo-governance/` tree — FR-3.13's
/// `when_to_use` requirement applies only there (FR-4.6).
fn path_is_repo_governance(path: &Path) -> bool {
    path.to_string_lossy()
        .replace('\\', "/")
        .contains("repo-governance/")
}

/// Derives a human-readable fallback title from a sibling-target `name`
/// (e.g. `"linking.md"` → `"Linking"`, `"structure/README.md"` →
/// `"Structure"`) — used only when the target itself carries no `title`
/// frontmatter to derive one from.
fn fallback_entry_title(name: &str) -> String {
    let base = name
        .strip_suffix("/README.md")
        .unwrap_or_else(|| name.strip_suffix(".md").unwrap_or(name));
    let base = base.rsplit('/').next().unwrap_or(base);
    title_case_from_stem(base)
}

/// Derives a human-readable fallback title for an index file itself, used
/// only to synthesize a brand-new file's `title:` frontmatter field and H1
/// heading. A `README.md` index takes its title from its parent directory's
/// name; a split-directory sibling `<name>.md` index takes its title from
/// its own file stem.
fn fallback_index_title(index_path: &Path) -> String {
    let stem = index_path
        .file_stem()
        .map(|s| s.to_string_lossy().to_string())
        .unwrap_or_default();
    if stem.eq_ignore_ascii_case("README") {
        index_path.parent().and_then(Path::file_name).map_or_else(
            || "Index".to_string(),
            |n| title_case_from_stem(&n.to_string_lossy()),
        )
    } else {
        title_case_from_stem(&stem)
    }
}

/// Converts a kebab/snake-case stem (e.g. `"formatting"`, `"ai-agents"`,
/// `"01-catalog"`) into Title Case words joined by spaces.
fn title_case_from_stem(stem: &str) -> String {
    stem.split(['-', '_'])
        .filter(|w| !w.is_empty())
        .map(|w| {
            let mut chars = w.chars();
            chars.next().map_or_else(String::new, |first| {
                first.to_uppercase().collect::<String>() + chars.as_str()
            })
        })
        .collect::<Vec<_>>()
        .join(" ")
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::infrastructure::fs::real::RealFs;
    use std::fs;
    use tempfile::TempDir;

    #[test]
    fn errors_on_empty_paths() {
        let err = audit_readme_index(&RealFs, &[], &[]).unwrap_err();
        assert!(err.to_string().contains("at least one path"));
    }

    #[test]
    fn detects_orphan_md_file() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "# Title\n").unwrap();
        fs::write(tmp.path().join("other.md"), "x\n").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(findings.iter().any(|f| f.kind == "orphan"));
    }

    #[test]
    fn detects_ghost_link() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "[ghost](nonexistent.md)\n").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(findings.iter().any(|f| f.kind == "ghost"));
    }

    /// Returns `true` when `findings` contains no `orphan`, `ghost`, or
    /// `missing` finding — the completeness guarantee these pre-existing
    /// tests exist to prove. `unannotated` is a separate, additive,
    /// dark-launched dimension (FR-3.20) introduced alongside these tests'
    /// bare-link fixtures, which were never written with annotations, so it
    /// is deliberately excluded from this helper — see
    /// `scenario_unannotated_finding_kind_is_discoverable` below for the
    /// dedicated coverage of that kind.
    fn has_no_completeness_finding(findings: &[ReadmeIndexFinding]) -> bool {
        findings
            .iter()
            .all(|f| f.kind != "orphan" && f.kind != "ghost" && f.kind != "missing")
    }

    #[test]
    fn clean_when_all_linked() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "[other](other.md)\n").unwrap();
        fs::write(tmp.path().join("other.md"), "x\n").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(has_no_completeness_finding(&findings), "{findings:?}");
    }

    #[test]
    fn subdir_readme_treated_as_target() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "[sub](structure/README.md)\n").unwrap();
        fs::create_dir(tmp.path().join("structure")).unwrap();
        fs::write(tmp.path().join("structure/README.md"), "# Sub\n").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(has_no_completeness_finding(&findings), "{findings:?}");
    }

    #[test]
    fn bare_dir_link_recognized() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "[sub](structure)\n").unwrap();
        fs::create_dir(tmp.path().join("structure")).unwrap();
        fs::write(tmp.path().join("structure/README.md"), "x\n").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        // No orphan/ghost because README links subdir as bare dir.
        assert!(findings.iter().all(|f| f.kind != "ghost"));
    }

    #[test]
    fn extract_links_strips_fragments() {
        let links = extract_readme_links("[a](foo.md#anchor) [b](bar.md?x=y)");
        assert!(links.contains("foo.md"));
        assert!(links.contains("bar.md"));
    }

    #[test]
    fn extract_links_skips_urls() {
        let links = extract_readme_links("[a](https://example.com/foo.md) [b](mailto:x.md)");
        assert!(links.is_empty());
    }

    #[test]
    fn extract_links_skips_parent_paths() {
        let links = extract_readme_links("[a](../foo.md) [b](/abs/foo.md)");
        assert!(links.is_empty());
    }

    #[test]
    fn matches_glob_basename_full_and_component() {
        assert!(matches_any_glob("foo/bar.md", &["*.md".to_string()]));
        assert!(matches_any_glob(
            "node_modules/foo",
            &["node_modules".to_string()]
        ));
        assert!(matches_any_glob("a/scratch/b.md", &["scratch".to_string()]));
        assert!(!matches_any_glob("foo/bar.md", &["*.txt".to_string()]));
    }

    #[test]
    fn cross_dir_link_to_existing_file_not_ghost() {
        let tmp = TempDir::new().unwrap();
        let sub = tmp.path().join("sub");
        fs::create_dir(&sub).unwrap();
        fs::write(sub.join("README.md"), "# Sub\n").unwrap();
        fs::write(sub.join("detail.md"), "# Detail\n").unwrap();
        // Parent README links to a file inside a subdir: "sub/detail.md"
        fs::write(
            tmp.path().join("README.md"),
            "[sub readme](sub/README.md)\n[sub detail](sub/detail.md)\n",
        )
        .unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings.iter().all(|f| f.kind != "ghost"),
            "cross-dir link to existing file must not be reported as ghost: {findings:?}"
        );
    }

    #[test]
    fn excludes_filter_out_files() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "# x\n").unwrap();
        fs::write(tmp.path().join("scratch.tmp.md"), "x\n").unwrap();
        let findings = audit_readme_index(
            &RealFs,
            &[tmp.path().to_string_lossy().to_string()],
            &["*.tmp.md".to_string()],
        )
        .unwrap();
        assert!(findings.is_empty());
    }

    // -----------------------------------------------------------------------
    // Phase 1a (TDD RED) — plans/done/2026-08-15__optimize-governance-md
    //
    // Tests below cover every FR-3 Gherkin scenario in `prd.md` that is
    // testable at this module's boundary. Two scenarios are deliberately
    // *not* duplicated here even though `prd.md` lists them alongside FR-3:
    // "A generated mirror is still subject to the word budget" is an FR-1
    // concern and lives in `word_budget.rs`
    // (`scenario_generated_mirror_file_is_still_subject_to_the_word_budget`);
    // "The unannotated finding kind fails once armed and in scope" is a
    // `--fail-kinds` exit-code concern and lives in
    // `governance_validate_readme_index.rs`.
    // -----------------------------------------------------------------------

    #[test]
    fn scenario_a_complete_index_passes() {
        let tmp = TempDir::new().unwrap();
        fs::write(
            tmp.path().join("README.md"),
            "[linking](./linking.md)\n[emoji](./emoji.md)\n",
        )
        .unwrap();
        fs::write(tmp.path().join("linking.md"), "x").unwrap();
        fs::write(tmp.path().join("emoji.md"), "x").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            has_no_completeness_finding(&findings),
            "FR-3.2: a README linking every sibling must pass cleanly (orphan/ghost/missing): \
             {findings:?}"
        );
    }

    #[test]
    fn scenario_a_missing_sibling_link_fails() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "[linking](./linking.md)\n").unwrap();
        fs::write(tmp.path().join("linking.md"), "x").unwrap();
        fs::write(tmp.path().join("emoji.md"), "x").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == "orphan" && f.file.contains("emoji.md")),
            "FR-3.2: an unlinked sibling must be reported as an orphan finding: {findings:?}"
        );
    }

    #[test]
    fn scenario_a_missing_subdirectory_readme_link_fails() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "# Conventions\n").unwrap();
        let sub = tmp.path().join("structure");
        fs::create_dir_all(&sub).unwrap();
        fs::write(sub.join("README.md"), "# Structure\n").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == "orphan" && f.file.contains("structure/README.md")),
            "FR-3.3: an unlinked subdirectory README must be reported as an orphan finding: \
             {findings:?}"
        );
    }

    #[test]
    fn scenario_a_missing_readme_fails_when_siblings_exist() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join(".claude/skills/grill-me/reference");
        fs::create_dir_all(&dir).unwrap();
        fs::write(dir.join("01-options.md"), "content").unwrap();
        // No README.md written — FR-3.1 requires one because a sibling *.md
        // exists. The current implementation only audits READMEs that already
        // exist, so this directory is never visited at all today.
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings.iter().any(|f| f.kind == "missing"),
            "FR-3.1: a directory with sibling *.md files but no README.md must report a \
             'missing' finding, not silently pass: {findings:?}"
        );
    }

    #[test]
    fn scenario_the_rule_does_not_reach_grandchildren() {
        let tmp = TempDir::new().unwrap();
        fs::write(
            tmp.path().join("README.md"),
            "[conventions](./conventions/README.md)\n",
        )
        .unwrap();
        let conv = tmp.path().join("conventions");
        fs::create_dir_all(&conv).unwrap();
        fs::write(
            conv.join("README.md"),
            "[structure](./structure/README.md)\n",
        )
        .unwrap();
        let structure = conv.join("structure");
        fs::create_dir_all(&structure).unwrap();
        fs::write(structure.join("README.md"), "[plans](./plans.md)\n").unwrap();
        fs::write(structure.join("plans.md"), "x").unwrap();
        // The top-level README links its immediate child (conventions/README.md)
        // but is never required to reach the grandchild plans.md directly.
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            has_no_completeness_finding(&findings),
            "FR-3.4: a README must never be required to index a grandchild: {findings:?}"
        );
    }

    #[test]
    fn scenario_a_split_directory_still_requires_its_own_readme() {
        let tmp = TempDir::new().unwrap();
        fs::write(
            tmp.path().join("ai-agents.md"),
            "[catalog](./ai-agents/01-catalog.md)\n[naming](./ai-agents/02-naming.md)\n",
        )
        .unwrap();
        let sub = tmp.path().join("ai-agents");
        fs::create_dir_all(&sub).unwrap();
        fs::write(sub.join("01-catalog.md"), "x").unwrap();
        fs::write(sub.join("02-naming.md"), "x").unwrap();
        // The former FR-3.5 exemption is removed: a sibling "ai-agents.md"
        // fully linking every child no longer excuses ai-agents/ from carrying
        // its own README.md. Every directory carries one, with no exception.
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == "missing" && f.file.ends_with("ai-agents")),
            "a split directory with no README.md must report a missing finding: {findings:?}"
        );
    }

    #[test]
    fn scenario_a_split_directory_with_a_readme_passes_and_both_indexes_are_audited() {
        let tmp = TempDir::new().unwrap();
        fs::write(
            tmp.path().join("ai-agents.md"),
            "[catalog](./ai-agents/01-catalog.md)\n[naming](./ai-agents/02-naming.md)\n",
        )
        .unwrap();
        let sub = tmp.path().join("ai-agents");
        fs::create_dir_all(&sub).unwrap();
        fs::write(sub.join("01-catalog.md"), "x").unwrap();
        fs::write(sub.join("02-naming.md"), "x").unwrap();
        fs::write(
            sub.join("README.md"),
            "[catalog](./01-catalog.md)\n[naming](./02-naming.md)\n",
        )
        .unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            has_no_completeness_finding(&findings),
            "a split directory carrying its own fully-linked README.md must pass cleanly: \
             {findings:?}"
        );
        // The sibling index keeps its own coverage: dropping a child from it
        // is still an orphan finding even though README.md lists everything.
        fs::write(
            tmp.path().join("ai-agents.md"),
            "[catalog](./ai-agents/01-catalog.md)\n",
        )
        .unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == "orphan" && f.file.ends_with("02-naming.md")),
            "the sibling index must still be audited alongside README.md: {findings:?}"
        );
    }

    #[test]
    fn scenario_a_split_index_link_to_its_own_sibling_is_not_a_ghost() {
        let tmp = TempDir::new().unwrap();
        // ai-agents.md (the split-index file) lives beside general.md, its own
        // sibling — NOT under ai-agents/. This link is written unprefixed
        // (no "ai-agents/" prefix) because it targets index_dir itself, not
        // target_dir. It must resolve against index_dir, the file's real
        // location, and never be reported as a ghost.
        fs::write(
            tmp.path().join("ai-agents.md"),
            "[catalog](./ai-agents/01-catalog.md)\n[general](./general.md)\n",
        )
        .unwrap();
        fs::write(tmp.path().join("general.md"), "x").unwrap();
        let sub = tmp.path().join("ai-agents");
        fs::create_dir_all(&sub).unwrap();
        fs::write(sub.join("01-catalog.md"), "x").unwrap();
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings.iter().all(|f| f.kind != "ghost"),
            "a split-index link to its own unprefixed sibling must resolve against index_dir, \
             not be reported as ghost: {findings:?}"
        );
    }

    #[test]
    fn scenario_a_split_index_prefixed_link_to_a_genuinely_missing_target_is_still_ghost() {
        let tmp = TempDir::new().unwrap();
        // The link IS prefixed ("ai-agents/missing.md") — it unambiguously
        // targets target_dir, not index_dir. An unrelated file that happens
        // to share the same basename ("missing.md") sitting beside the index
        // file must NOT suppress the ghost finding: only unprefixed links may
        // fall back to resolving against index_dir.
        fs::write(
            tmp.path().join("ai-agents.md"),
            "[catalog](./ai-agents/01-catalog.md)\n[missing](./ai-agents/missing.md)\n",
        )
        .unwrap();
        // Decoy: a same-basename file beside index_dir, NOT under target_dir.
        fs::write(tmp.path().join("missing.md"), "x").unwrap();
        let sub = tmp.path().join("ai-agents");
        fs::create_dir_all(&sub).unwrap();
        fs::write(sub.join("01-catalog.md"), "x").unwrap();
        // Deliberately do not create ai-agents/missing.md — the link is a
        // genuine ghost.
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == "ghost" && f.message.contains("missing.md")),
            "a target_dir-prefixed link to a genuinely missing target must still be reported as \
             ghost, even when an unrelated same-basename file sits beside index_dir: {findings:?}"
        );
    }

    #[test]
    fn scenario_a_split_directory_whose_parent_omits_a_child_fails() {
        let tmp = TempDir::new().unwrap();
        fs::write(
            tmp.path().join("ai-agents.md"),
            "[catalog](./ai-agents/01-catalog.md)\n",
        )
        .unwrap();
        let sub = tmp.path().join("ai-agents");
        fs::create_dir_all(&sub).unwrap();
        fs::write(sub.join("01-catalog.md"), "x").unwrap();
        fs::write(sub.join("02-naming.md"), "x").unwrap();
        // ai-agents.md omits 02-naming.md — the current implementation never
        // audits a non-"README.md"-named parent at all, so this always passes
        // silently today regardless of what ai-agents.md links.
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings
                .iter()
                .any(|f| f.kind == "orphan" && f.file.contains("02-naming.md")),
            "FR-3.6: a split-directory parent that omits a child must report that child as \
             unindexed (orphan): {findings:?}"
        );
    }

    #[test]
    fn scenario_an_uncovered_tree_is_not_scanned() {
        let tmp = TempDir::new().unwrap();
        // FR-3.8: apps/ and plans/ are explicitly uncovered trees — a caller
        // that only ever passes the FR-3.7 covered-tree list never visits them.
        for dir in [
            "apps/ayokoding-www/content/en/",
            "plans/backlog/some-plan/",
            "plans/done/2026-01-01__a-plan/",
        ] {
            fs::create_dir_all(tmp.path().join(dir)).unwrap();
            fs::write(tmp.path().join(dir).join("file.md"), "x").unwrap();
        }
        fs::create_dir_all(tmp.path().join("repo-governance")).unwrap();
        fs::write(
            tmp.path().join("repo-governance/README.md"),
            "# Governance\n",
        )
        .unwrap();
        let findings = audit_readme_index(
            &RealFs,
            &[tmp
                .path()
                .join("repo-governance")
                .to_string_lossy()
                .to_string()],
            &[],
        )
        .unwrap();
        assert!(
            findings.is_empty(),
            "FR-3.8: scanning only the covered tree must never touch apps/ or plans/: \
             {findings:?}"
        );
    }

    #[test]
    fn scenario_a_generated_mirror_directory_is_not_scanned() {
        let tmp = TempDir::new().unwrap();
        let mirror = tmp.path().join(".opencode/agents");
        fs::create_dir_all(&mirror).unwrap();
        for i in 0..95 {
            fs::write(mirror.join(format!("agent-{i}.md")), "x").unwrap();
        }
        // No README.md under .opencode/agents/ — FR-3.17 excludes generated
        // mirrors from the README-index gate entirely; a caller that only ever
        // passes FR-3.7's covered trees never visits it.
        fs::create_dir_all(tmp.path().join("repo-governance")).unwrap();
        fs::write(
            tmp.path().join("repo-governance/README.md"),
            "# Governance\n",
        )
        .unwrap();
        let findings = audit_readme_index(
            &RealFs,
            &[tmp
                .path()
                .join("repo-governance")
                .to_string_lossy()
                .to_string()],
            &[],
        )
        .unwrap();
        assert!(
            findings.is_empty(),
            "FR-3.17: a mirror tree outside the scanned paths must produce no findings: \
             {findings:?}"
        );
    }

    #[test]
    fn scenario_phase1_rename_introduces_no_enforcement_gap_for_orphan_or_ghost() {
        let repo_root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let cfg = fs::read_to_string(repo_root.join("repo-config.yml"))
            .expect("repo-config.yml must exist at the repo root");
        assert!(
            !cfg.contains("id: md-readme-index"),
            "FR-3: the legacy md-readme-index gate id must be renamed away in the same commit \
             as the git mv"
        );
        assert!(
            cfg.contains("id: governance-readme-index"),
            "FR-3.19: governance-readme-index must be registered, continuously armed, with no \
             enforcement gap"
        );
    }

    #[test]
    fn scenario_unannotated_finding_kind_is_discoverable() {
        let tmp = TempDir::new().unwrap();
        fs::write(tmp.path().join("README.md"), "[linking](./linking.md)\n").unwrap();
        fs::write(tmp.path().join("linking.md"), "x").unwrap();
        // FR-3.10/FR-3.11: an index entry must be annotated
        // (`- [<title>](<path>) — <description> <when_to_use>`), derived from
        // the target's frontmatter. This link has no annotation text at all —
        // Phase 1 dark-launches discovery of the "unannotated" kind (FR-3.20);
        // enforcement (failing the build on it) is armed later at Phase 9.
        let findings =
            audit_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();
        assert!(
            findings.iter().any(|f| f.kind == "unannotated"),
            "FR-3.10: a bare, unannotated link must be discoverable as an 'unannotated' \
             finding: {findings:?}"
        );
    }

    // -----------------------------------------------------------------------
    // Phase 1b — `generate_readme_index` (FR-3.12)
    // -----------------------------------------------------------------------

    /// Writes a minimal governance-doc frontmatter block (`title`,
    /// `description`, `when_to_use`) plus a one-line body at `path`.
    fn write_governance_target(path: &std::path::Path, title: &str, description: &str, when: &str) {
        fs::write(
            path,
            format!(
                "---\ntitle: \"{title}\"\ndescription: {description}\nwhen_to_use: {when}\n---\n\n# {title}\n"
            ),
        )
        .unwrap();
    }

    /// Writes a minimal non-governance-doc frontmatter block (`title`,
    /// `description`, `when_to_use` — the `when_to_use` field is present in
    /// the fixture so `generate_omits_when_to_use_outside_repo_governance`
    /// can prove it is *never emitted* for a non-`repo-governance/` target,
    /// not merely absent from the fixture) plus a one-line body at `path`.
    fn write_doc_target(path: &std::path::Path, title: &str, description: &str, when: &str) {
        write_governance_target(path, title, description, when);
    }

    #[test]
    fn generate_writes_annotated_readme_for_a_directory_needing_one() {
        let tmp = TempDir::new().unwrap();
        let gov_root = tmp.path().join("repo-governance");
        let leaf = gov_root.join("formatting");
        fs::create_dir_all(&leaf).unwrap();
        write_governance_target(
            &leaf.join("linking.md"),
            "Linking Convention",
            "shared standards for links",
            "Use when adding or reviewing a hyperlink",
        );
        write_governance_target(
            &leaf.join("emoji.md"),
            "Emoji Convention",
            "semantic emoji usage",
            "Use when choosing an emoji",
        );

        let written =
            generate_readme_index(&RealFs, &[gov_root.to_string_lossy().to_string()], &[]).unwrap();

        let readme_path = leaf.join("README.md");
        assert!(
            written.contains(&readme_path),
            "FR-3.12: generate must write the leaf directory's README.md: {written:?}"
        );
        let content = fs::read_to_string(&readme_path).unwrap();
        assert!(
            content.contains(
                "- [Linking Convention](./linking.md) — shared standards for links Use when \
                 adding or reviewing a hyperlink"
            ),
            "FR-3.10/FR-3.11: annotation must be derived verbatim from the target's frontmatter, \
             including when_to_use for a repo-governance/ target: {content}"
        );
        assert!(
            content.contains(
                "- [Emoji Convention](./emoji.md) — semantic emoji usage Use when choosing an \
                 emoji"
            ),
            "{content}"
        );
        assert!(
            content.starts_with("---\n"),
            "index must carry frontmatter: {content}"
        );
    }

    #[test]
    fn generate_omits_when_to_use_outside_repo_governance() {
        let tmp = TempDir::new().unwrap();
        let leaf = tmp.path().join("docs/formatting");
        fs::create_dir_all(&leaf).unwrap();
        write_doc_target(
            &leaf.join("linking.md"),
            "Linking",
            "how to link pages",
            "Use when adding a page link",
        );

        let written = generate_readme_index(
            &RealFs,
            &[tmp.path().join("docs").to_string_lossy().to_string()],
            &[],
        )
        .unwrap();
        let readme_path = leaf.join("README.md");
        assert!(written.contains(&readme_path), "{written:?}");
        let content = fs::read_to_string(&readme_path).unwrap();
        assert!(
            content.contains("- [Linking](./linking.md) — how to link pages"),
            "FR-3.13: a non-repo-governance target must still get its description: {content}"
        );
        assert!(
            !content.contains("Use when adding a page link"),
            "FR-3.13: when_to_use must never be emitted for a target outside repo-governance/, \
             even when the frontmatter carries one: {content}"
        );
    }

    #[test]
    fn generate_writes_sibling_md_for_split_directory() {
        let tmp = TempDir::new().unwrap();
        // The split sibling file must already exist (possibly as a bare
        // placeholder) for `dir` to be recognized as split — generate then
        // (re)writes its body, exactly mirroring `audit_one_dir`'s own
        // split-detection precondition.
        fs::write(tmp.path().join("ai-agents.md"), "# Placeholder\n").unwrap();
        let sub = tmp.path().join("ai-agents");
        fs::create_dir_all(&sub).unwrap();
        write_governance_target(
            &sub.join("01-catalog.md"),
            "Agent Catalog",
            "the full agent list",
            "Use when locating an agent",
        );
        write_governance_target(
            &sub.join("02-naming.md"),
            "Agent Naming",
            "naming rules for agents",
            "Use when naming a new agent",
        );

        let written =
            generate_readme_index(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[])
                .unwrap();

        let split_index = tmp.path().join("ai-agents.md");
        assert!(
            written.contains(&split_index),
            "FR-3.6/FR-3.12: generate must (re)write the split directory's sibling <name>.md: \
             {written:?}"
        );
        assert!(
            written.contains(&sub.join("README.md")),
            "a split directory must ALSO get its own README.md — the FR-3.5 exemption is \
             removed: {written:?}"
        );
        assert!(
            sub.join("README.md").exists(),
            "every directory carries a literal README.md, with no exception"
        );
        let content = fs::read_to_string(&split_index).unwrap();
        assert!(content.contains("./ai-agents/01-catalog.md"), "{content}");
        assert!(content.contains("./ai-agents/02-naming.md"), "{content}");
    }

    #[test]
    fn generate_is_idempotent() {
        let tmp = TempDir::new().unwrap();
        let gov_root = tmp.path().join("repo-governance");
        let leaf = gov_root.join("formatting");
        fs::create_dir_all(&leaf).unwrap();
        write_governance_target(
            &leaf.join("linking.md"),
            "Linking Convention",
            "shared standards for links",
            "Use when adding or reviewing a hyperlink",
        );

        let paths = vec![gov_root.to_string_lossy().to_string()];
        generate_readme_index(&RealFs, &paths, &[]).unwrap();
        let first_pass = fs::read_to_string(leaf.join("README.md")).unwrap();

        generate_readme_index(&RealFs, &paths, &[]).unwrap();
        let second_pass = fs::read_to_string(leaf.join("README.md")).unwrap();

        assert_eq!(
            first_pass, second_pass,
            "FR-3.12: generate must be idempotent — a second run must produce byte-identical \
             output"
        );

        let findings = audit_readme_index(&RealFs, &paths, &[]).unwrap();
        assert!(
            findings
                .iter()
                .all(|f| f.kind != "missing" && f.kind != "unannotated"),
            "FR-3.12: validate must report zero missing/unannotated findings after generate: \
             {findings:?}"
        );
    }

    /// Binds Gherkin scenario "Generate no longer rewrites an existing index's
    /// order": a directory whose `README.md` already carries hand-authored
    /// entry order must keep that order and those annotations verbatim, with
    /// only genuinely missing targets appended.
    #[test]
    fn generate_preserves_existing_index_order_and_annotations() {
        let tmp = TempDir::new().unwrap();
        let gov_root = tmp.path().join("repo-governance");
        let leaf = gov_root.join("formatting");
        fs::create_dir_all(&leaf).unwrap();
        write_governance_target(
            &leaf.join("linking.md"),
            "Linking Convention",
            "shared standards for links",
            "Use when adding or reviewing a hyperlink",
        );
        write_governance_target(
            &leaf.join("emoji.md"),
            "Emoji Convention",
            "semantic emoji usage",
            "Use when choosing an emoji",
        );
        write_governance_target(
            &leaf.join("appended.md"),
            "Appended Convention",
            "a target absent from the hand-authored index",
            "Use when checking append behaviour",
        );

        // Hand-authored index: linking BEFORE emoji. Sorted order would be
        // appended, emoji, linking — so "linking first" is reachable ONLY by
        // preserving the hand-authored order, never by re-deriving it.
        let hand_authored = concat!(
            "---\n",
            "title: \"Formatting\"\n",
            "---\n",
            "\n",
            "# Formatting\n",
            "\n",
            "- [Linking Convention](./linking.md) — HAND-AUTHORED annotation that must survive.\n",
            "- [Emoji Convention](./emoji.md) — semantic emoji usage Use when choosing an emoji\n",
        );
        fs::write(leaf.join("README.md"), hand_authored).unwrap();

        generate_readme_index(&RealFs, &[gov_root.to_string_lossy().to_string()], &[]).unwrap();
        let after = fs::read_to_string(leaf.join("README.md")).unwrap();

        let emoji_at = after.find("./emoji.md").expect("emoji entry must survive");
        let linking_at = after
            .find("./linking.md")
            .expect("linking entry must survive");
        assert!(
            linking_at < emoji_at,
            "generate must preserve hand-authored entry order (linking before emoji, which \
             alphabetical re-derivation would reverse):\n{after}"
        );
        assert!(
            after.contains("HAND-AUTHORED annotation that must survive"),
            "generate must preserve each existing entry's annotation verbatim:\n{after}"
        );
        assert!(
            after.contains("./appended.md"),
            "generate must append genuinely missing targets:\n{after}"
        );
    }

    /// Binds Gherkin scenario "Generate still scaffolds a directory with no
    /// index": the no-index path must be unchanged by order preservation — a
    /// complete annotated index is written and every sibling appears exactly
    /// once (never duplicated by the append pass).
    #[test]
    fn generate_still_scaffolds_a_directory_with_no_index() {
        let tmp = TempDir::new().unwrap();
        let gov_root = tmp.path().join("repo-governance");
        let leaf = gov_root.join("formatting");
        fs::create_dir_all(&leaf).unwrap();
        for (name, title) in [
            ("linking.md", "Linking Convention"),
            ("emoji.md", "Emoji Convention"),
            ("zebra.md", "Zebra Convention"),
        ] {
            write_governance_target(&leaf.join(name), title, "a description", "Use when testing");
        }
        assert!(
            !leaf.join("README.md").exists(),
            "fixture must start with no index"
        );

        generate_readme_index(&RealFs, &[gov_root.to_string_lossy().to_string()], &[]).unwrap();
        let after = fs::read_to_string(leaf.join("README.md")).unwrap();

        for name in ["linking.md", "emoji.md", "zebra.md"] {
            let needle = format!("./{name}");
            assert_eq!(
                after.matches(&needle).count(),
                1,
                "scaffold must emit {name} exactly once:\n{after}"
            );
        }
        // Scaffold order remains sorted, since there is no authored order to keep.
        let e = after.find("./emoji.md").unwrap();
        let l = after.find("./linking.md").unwrap();
        let z = after.find("./zebra.md").unwrap();
        assert!(
            e < l && l < z,
            "scaffold must stay in sorted order:\n{after}"
        );
    }

    /// Regression test for the CRITICAL finding on this PR: a read failure
    /// on an EXISTING index must propagate as an error, never fall through
    /// to the scaffold path and overwrite the file. Uses invalid UTF-8 bytes
    /// (`std::fs::read_to_string`'s documented failure mode) rather than a
    /// permission error, since the latter is not portably reproducible in a
    /// test sandbox. Written directly via `std::fs::write` (raw bytes, not
    /// the `String`-typed fixture helpers used elsewhere in this module,
    /// which cannot hold invalid UTF-8 at all).
    #[test]
    fn generate_errors_instead_of_overwriting_an_unreadable_existing_index() {
        let tmp = TempDir::new().unwrap();
        let gov_root = tmp.path().join("repo-governance");
        let leaf = gov_root.join("formatting");
        fs::create_dir_all(&leaf).unwrap();
        write_governance_target(
            &leaf.join("linking.md"),
            "Linking Convention",
            "shared standards for links",
            "Use when adding or reviewing a hyperlink",
        );

        let invalid_utf8: &[u8] = &[0xFF, 0xFE, b'h', b'i'];
        let index_path = leaf.join("README.md");
        fs::write(&index_path, invalid_utf8).unwrap();

        let result = generate_readme_index(&RealFs, &[gov_root.to_string_lossy().to_string()], &[]);

        assert!(
            result.is_err(),
            "an existing-but-unreadable index must return Err, not Ok"
        );
        let after = fs::read(&index_path).unwrap();
        assert_eq!(
            after, invalid_utf8,
            "the unreadable index's original bytes must survive untouched — a fallthrough to \
             the scaffold path would silently overwrite them"
        );
    }

    /// Binds Gherkin scenario "Rewrite-paths updates link targets without
    /// touching order": every index link target is repointed to its new path
    /// while entry order, annotation text, and surrounding prose stay byte-
    /// identical apart from the target itself.
    #[test]
    fn rewrite_paths_updates_targets_without_touching_order_or_prose() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join("repo-governance").join("formatting");
        fs::create_dir_all(&dir).unwrap();

        let before = concat!(
            "---\n",
            "title: \"Formatting\"\n",
            "---\n",
            "\n",
            "# Formatting\n",
            "\n",
            "Intro prose mentioning 01-linking.md inline, which must NOT be rewritten.\n",
            "\n",
            "- [Linking](./01-linking.md) — annotation one.\n",
            "- [Emoji](./02-emoji.md) — annotation two.\n",
            "\n",
            "Trailing prose.\n",
        );
        fs::write(dir.join("README.md"), before).unwrap();

        let map = vec![
            ("01-linking.md".to_string(), "linking.md".to_string()),
            ("02-emoji.md".to_string(), "emoji.md".to_string()),
        ];
        let changed =
            rewrite_index_paths(&RealFs, &[tmp.path().to_string_lossy().to_string()], &map)
                .unwrap();
        assert!(
            !changed.is_empty(),
            "rewrite-paths must report the file it changed"
        );

        let after = fs::read_to_string(dir.join("README.md")).unwrap();
        assert!(
            after.contains("(./linking.md)"),
            "link target must be rewritten:\n{after}"
        );
        assert!(
            after.contains("(./emoji.md)"),
            "link target must be rewritten:\n{after}"
        );
        assert!(
            !after.contains("(./01-linking.md)"),
            "old target must be gone:\n{after}"
        );

        // Order preserved: linking still before emoji.
        assert!(
            after.find("./linking.md").unwrap() < after.find("./emoji.md").unwrap(),
            "entry order must be unchanged:\n{after}"
        );
        // Annotations and prose preserved verbatim.
        assert!(
            after.contains("— annotation one."),
            "annotation must survive:\n{after}"
        );
        assert!(
            after.contains("— annotation two."),
            "annotation must survive:\n{after}"
        );
        assert!(
            after.contains("Trailing prose."),
            "prose must survive:\n{after}"
        );
        assert!(
            after.contains("Intro prose mentioning 01-linking.md inline"),
            "a bare non-link mention must NOT be rewritten:\n{after}"
        );
    }

    /// `rewrite_index_paths(&[], ..)` must reject an empty `paths` list, the
    /// same way every other multi-path entry point in this module does.
    #[test]
    fn rewrite_paths_errors_on_empty_paths() {
        let err = rewrite_index_paths(&RealFs, &[], &[]).unwrap_err();
        assert!(
            err.to_string().contains("at least one path is required"),
            "{err}"
        );
    }

    /// An empty rename map is a legitimate no-op (nothing was asked to be
    /// renamed) and must return `Ok(Vec::new())` without touching the
    /// filesystem — this is the early-return branch, distinct from "a
    /// non-empty map that matches nothing" below, which walks the tree.
    #[test]
    fn rewrite_paths_empty_map_is_a_no_touch_no_op() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join("repo-governance").join("formatting");
        fs::create_dir_all(&dir).unwrap();
        let before = "- [Linking](./01-linking.md) — annotation.\n";
        fs::write(dir.join("README.md"), before).unwrap();

        let changed =
            rewrite_index_paths(&RealFs, &[tmp.path().to_string_lossy().to_string()], &[]).unwrap();

        assert!(changed.is_empty(), "empty map must report no changed files");
        assert_eq!(
            fs::read_to_string(dir.join("README.md")).unwrap(),
            before,
            "empty map must not touch the file on disk"
        );
    }

    /// Pins today's silent-no-op behaviour (Finding 5 / WS-3 in
    /// `plans/backlog/rhino-cli-governance-tooling-defects/`): a non-empty
    /// rename map that matches no basename anywhere in the tree returns
    /// `Ok(Vec::new())` — the CLI reports "0 file(s) updated" and exits 0,
    /// byte-indistinguishable from "nothing needed changing". This is the
    /// compensating control for deferring the basename→path keying redesign
    /// to WS-3: the moment that redesign introduces a dead-row exit code,
    /// this test fails loudly, which is exactly the signal WS-3 wants.
    #[test]
    fn rewrite_paths_map_matching_nothing_is_a_silent_ok_no_op() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join("repo-governance").join("formatting");
        fs::create_dir_all(&dir).unwrap();
        let before = "- [Linking](./01-linking.md) — annotation.\n";
        fs::write(dir.join("README.md"), before).unwrap();

        let map = vec![(
            "no-such-basename.md".to_string(),
            "irrelevant.md".to_string(),
        )];
        let changed =
            rewrite_index_paths(&RealFs, &[tmp.path().to_string_lossy().to_string()], &map)
                .unwrap();

        assert!(
            changed.is_empty(),
            "a map matching nothing must report zero changed files, not an error"
        );
        assert_eq!(
            fs::read_to_string(dir.join("README.md")).unwrap(),
            before,
            "a map matching nothing must not touch any file on disk"
        );
    }

    /// Non-`.md` files reachable from `paths` must be skipped entirely — a
    /// filename match against a `.png`/`.rs`/etc. sibling of a renamed
    /// basename is never rewritten, even when its extension-free stem
    /// happens to collide.
    #[test]
    fn rewrite_paths_skips_non_markdown_files() {
        let tmp = TempDir::new().unwrap();
        let dir = tmp.path().join("repo-governance").join("formatting");
        fs::create_dir_all(&dir).unwrap();
        let before = "[asset](./old-name.png)\n";
        fs::write(dir.join("README.md"), before).unwrap();
        // A non-markdown file whose own name also happens to match a map key
        // — must be left alone; only `.md` link TARGETS are ever rewritten,
        // and only inside `.md` SOURCE files.
        fs::write(dir.join("old-name.png"), b"not a markdown file").unwrap();

        let map = vec![("old-name.png".to_string(), "new-name.png".to_string())];
        let changed =
            rewrite_index_paths(&RealFs, &[tmp.path().to_string_lossy().to_string()], &map)
                .unwrap();

        // The link TARGET inside the .md file is still rewritten (targets
        // are matched by basename regardless of extension); what must be
        // skipped is walking/rewriting non-`.md` SOURCE files themselves.
        assert_eq!(
            changed,
            vec![dir.join("README.md")],
            "only the .md source file may be reported as changed"
        );
        assert_eq!(
            fs::read(dir.join("old-name.png")).unwrap(),
            b"not a markdown file",
            "a non-markdown file must never be rewritten, even if its name matches a map key"
        );
    }
}
