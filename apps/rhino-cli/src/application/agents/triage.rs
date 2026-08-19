//! Divergence triage between canonical `.claude/` source and its generated
//! mirrors, and the reviewed promotion of a mirror edit back into canonical
//! source.
//!
//! # Detection is by content, never by a clock
//!
//! Divergence is decided by regenerating every `generated`-class mirror into a
//! scratch tree and comparing bytes. Nothing on this path reads a file's
//! modification time, and nothing may: git stores no such stamp, so in a fresh
//! clone every file's stamp is checkout time. A clock-based design would
//! report the whole tree as simultaneously changed there, and report nothing at
//! all in a tree where an editor preserved stamps. Content is the only signal
//! that survives both.
//!
//! # Generation stays one-way
//!
//! A hand-edited mirror still fails `harness bindings validate` exactly as it
//! did before this module existed. Triage explains the failure; promotion
//! proposes a patch. Neither ever writes to canonical source (DD-13).

use std::collections::{BTreeMap, BTreeSet};
use std::fmt::Write as _;
use std::path::{Path, PathBuf};
use std::process::Command;

use super::codex::CODEX_FIELD_POLICY_TABLE;
use super::converter::{
    OPENCODE_FIELD_POLICY_TABLE, agent_link_re, discover_agent_sources, normalize_lexical,
    relative_from,
};
use super::emit::emit;
use super::field_policy::FieldAction;
use super::ownership::classify;
use crate::application::repo_config::{self, HarnessEntry, OwnershipClass, RepoConfig};

/// Which side of a canonical/mirror pair the report holds responsible.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Side {
    /// The generated mirror was hand-edited. Promotion is the reviewed way to
    /// keep the edit; regeneration is the way to discard it.
    Mirror,
    /// The canonical source is ahead of its mirror — either it was edited and
    /// the generator has not run since, or the emitter itself changed.
    /// Regeneration is the only correct answer; there is nothing to promote.
    Canonical,
}

/// The three — and only three — states a canonical/mirror pair can be in.
///
/// Exhaustive by construction: a fourth state would have to be added here and
/// every `match` would stop compiling, rather than falling through to a default
/// that quietly guesses.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Outcome {
    /// The mirror is exactly what the generator produces right now.
    InSync,
    /// Exactly one side moved. The [`Side`] says which.
    OneSided(Side),
    /// Both sides were hand-edited. There is no correct automatic answer, so
    /// this is a hard stop: no promotion is offered and nothing is resolved.
    BothDiverged,
}

/// One mirror file that is not what the generator would produce.
#[derive(Debug, Clone)]
pub struct Divergence {
    /// Repository-relative path of the generated mirror.
    pub mirror: String,
    /// Repository-relative path of the canonical source it is generated from,
    /// when one can be resolved from the registry.
    pub canonical: Option<String>,
    /// Which side moved.
    pub outcome: Outcome,
}

/// What one triage run found.
#[derive(Debug, Default)]
pub struct TriageReport {
    /// How many `generated`-class files were compared.
    pub compared: usize,
    /// Every compared file whose bytes differ from the regenerated output.
    pub divergences: Vec<Divergence>,
}

impl TriageReport {
    /// The report's single verdict: the most severe per-file outcome.
    #[must_use]
    pub fn verdict(&self) -> Outcome {
        if self
            .divergences
            .iter()
            .any(|d| d.outcome == Outcome::BothDiverged)
        {
            return Outcome::BothDiverged;
        }
        self.divergences
            .first()
            .map_or(Outcome::InSync, |d| d.outcome)
    }
}

/// The `.claude/` path a promoted edit would land in, plus what promoting it
/// would put at risk.
#[derive(Debug)]
pub struct PromoteProposal {
    /// Repository-relative path of the mirror the edit was made in.
    pub mirror: String,
    /// Repository-relative path of the canonical file the diff applies to.
    pub canonical: String,
    /// Unified diff from the current canonical file to the proposed one. Empty
    /// when the mirror carries no change the canonical file does not already
    /// have.
    pub diff: String,
    /// Canonical frontmatter fields the editing harness's schema cannot carry,
    /// paired with why. Whoever edited the mirror never saw these.
    pub at_risk: Vec<(String, String)>,
    /// `true` when [`attribute`] independently confirms both the mirror and
    /// its canonical source were hand-edited since `HEAD` (M1). `promote`
    /// itself still produces a proposal in this case — refusing outright
    /// would remove the opt-in escape hatch — but the canonical-side edit
    /// this diff's `-` lines silently absorb is otherwise indistinguishable
    /// from ordinary diff churn, and nothing tells a caller who never ran
    /// `harness sync triage` first that the tool's own design calls this
    /// state unreconcilable.
    pub both_diverged: bool,
}

// ---------------------------------------------------------------------------
// Detection
// ---------------------------------------------------------------------------

/// Regenerate every binding into a scratch copy of `repo_root` and report every
/// `generated`-class file whose committed bytes differ from the regenerated
/// output.
///
/// # Errors
///
/// Returns an error if the registry cannot be read, the scratch tree cannot be
/// built, or an emitter fails.
pub fn triage(repo_root: &Path) -> Result<TriageReport, String> {
    let config = repo_config::load_or_default(repo_root);
    let generated = generated_files(repo_root)?;
    let scratch = ScratchTree::build(repo_root, &config)?;
    emit(scratch.root(), None, false, false, true)?;

    let mut report = TriageReport {
        compared: generated.len(),
        divergences: Vec::new(),
    };

    for rel in &generated {
        let actual = std::fs::read(repo_root.join(rel)).ok();
        let expected = std::fs::read(scratch.root().join(rel)).ok();
        if actual == expected {
            continue;
        }
        let canonical = resolve_canonical(repo_root, &config, rel);
        let outcome = attribute(repo_root, rel, canonical.as_deref());
        report.divergences.push(Divergence {
            mirror: rel.clone(),
            canonical,
            outcome,
        });
    }

    Ok(report)
}

/// Decide which side moved, by comparing each side's working-tree bytes against
/// the same file at `HEAD`.
///
/// `HEAD` is the shared reference both sides are measured from, so "was this
/// hand-edited" is answered by content rather than by any stamp the filesystem
/// happens to carry.
fn attribute(repo_root: &Path, mirror: &str, canonical: Option<&str>) -> Outcome {
    let mirror_edited = differs_from_head(repo_root, mirror);
    let canonical_edited = canonical.is_some_and(|c| differs_from_head(repo_root, c));

    match (mirror_edited, canonical_edited) {
        (true, true) => Outcome::BothDiverged,
        (true, false) => Outcome::OneSided(Side::Mirror),
        // Neither side moved in the working tree yet the mirror still disagrees
        // with the generator: the committed mirror is stale, or the emitter
        // itself changed. Regeneration is the fix in both cases, which is
        // exactly what the canonical side reports.
        (false, _) => Outcome::OneSided(Side::Canonical),
    }
}

/// `true` when `rel`'s working-tree bytes differ from its bytes at `HEAD`.
///
/// A path absent from `HEAD` counts as differing: a file that did not exist in
/// the last commit is, unambiguously, a working-tree change.
fn differs_from_head(repo_root: &Path, rel: &str) -> bool {
    let head = Command::new("git")
        .args(["show", &format!("HEAD:{rel}")])
        .current_dir(repo_root)
        .output();
    let Ok(head) = head else { return true };
    if !head.status.success() {
        return true;
    }
    std::fs::read(repo_root.join(rel)).is_ok_and(|working| working != head.stdout)
}

/// Every tracked binding file the registry classifies `generated`.
///
/// Scoped to that one class on purpose (DD-12): a `vendored` file has no
/// in-repo source to regenerate from, so comparing it would report every
/// third-party payload as permanently diverged, and a `source` file is the
/// promotion target rather than a triage subject.
fn generated_files(repo_root: &Path) -> Result<Vec<String>, String> {
    Ok(classify(repo_root)?
        .classified
        .into_iter()
        .filter(|f| f.class == OwnershipClass::Generated)
        .map(|f| f.path)
        .collect())
}

// ---------------------------------------------------------------------------
// Scratch regeneration
// ---------------------------------------------------------------------------

/// A throwaway copy of the repository's binding surface, deleted on drop.
///
/// Only the registry and the declared binding roots are copied: the emitters
/// read nothing else, and copying the whole repository to regenerate a few
/// hundred small files would be waste rather than caution.
struct ScratchTree {
    /// The temporary directory; removed when this value drops.
    dir: tempfile::TempDir,
}

/// The one non-directory input the emitters read: the registry itself.
const SCRATCH_REGISTRY: &str = "repo-config.yml";

impl ScratchTree {
    /// Copy the registry and every declared binding root into a fresh
    /// temporary directory.
    fn build(repo_root: &Path, config: &RepoConfig) -> Result<Self, String> {
        let dir = tempfile::TempDir::new().map_err(|e| format!("scratch tree: {e}"))?;

        let registry = repo_root.join(SCRATCH_REGISTRY);
        if registry.is_file() {
            copy_file(&registry, &dir.path().join(SCRATCH_REGISTRY))?;
        }
        for root in scratch_roots(config) {
            copy_tree(&repo_root.join(&root), &dir.path().join(&root))?;
        }
        Ok(Self { dir })
    }

    /// Absolute path of the scratch tree's root.
    fn root(&self) -> &Path {
        self.dir.path()
    }
}

/// Every directory the emitters read from or write to, derived from the
/// registry rather than listed here, so a fourth harness needs no edit.
fn scratch_roots(config: &RepoConfig) -> BTreeSet<String> {
    let mut roots = BTreeSet::new();
    for entry in &config.harness {
        for candidate in [
            entry.agent_dir.as_ref(),
            entry.skills_dir.as_ref(),
            entry.mirrors.as_ref(),
            entry.skills_mirrors.as_ref(),
            entry.config.as_ref(),
        ]
        .into_iter()
        .flatten()
        {
            roots.insert(top_component(candidate));
        }
    }
    roots
}

/// The first path component of `rel` — the binding root a declared path sits
/// under, e.g. `.codex` for `.codex/config.toml`.
fn top_component(rel: &str) -> String {
    Path::new(rel).components().next().map_or_else(
        || rel.to_string(),
        |c| c.as_os_str().to_string_lossy().into(),
    )
}

/// Copy one file, creating the destination's parent directories.
fn copy_file(src: &Path, dst: &Path) -> Result<(), String> {
    if let Some(parent) = dst.parent() {
        std::fs::create_dir_all(parent).map_err(|e| format!("mkdir {}: {e}", parent.display()))?;
    }
    std::fs::copy(src, dst).map_err(|e| format!("copy {}: {e}", src.display()))?;
    Ok(())
}

/// Copy every regular file under `src` into `dst`.
///
/// Uses `symlink_metadata` so a symlinked directory is never followed: the
/// scratch tree must reproduce what the emitters would see, not what a link
/// points at.
fn copy_tree(src: &Path, dst: &Path) -> Result<(), String> {
    if !src.is_dir() {
        return Ok(());
    }
    let entries = std::fs::read_dir(src).map_err(|e| format!("read dir {}: {e}", src.display()))?;
    for entry in entries.flatten() {
        let from = entry.path();
        let to = dst.join(entry.file_name());
        let Ok(meta) = std::fs::symlink_metadata(&from) else {
            continue;
        };
        if meta.file_type().is_dir() {
            copy_tree(&from, &to)?;
        } else if meta.file_type().is_file() {
            copy_file(&from, &to)?;
        }
    }
    Ok(())
}

// ---------------------------------------------------------------------------
// Canonical-source resolution
// ---------------------------------------------------------------------------

/// The canonical source path a mirror file is generated from, resolved through
/// the registry's `mirrors` / `skills-mirrors` declarations.
///
/// Returns `None` when no harness entry claims the path, which is the honest
/// answer for a generated file whose provenance the registry does not state.
#[must_use]
pub fn resolve_canonical(
    repo_root: &Path,
    config: &RepoConfig,
    mirror_rel: &str,
) -> Option<String> {
    for entry in &config.harness {
        if let Some(found) = canonical_for_entry(repo_root, entry, mirror_rel) {
            return Some(found);
        }
    }
    None
}

/// [`resolve_canonical`] for one registry entry: the skills mirror maps path
/// for path, and an agent mirror maps through the agent's unique `name`.
fn canonical_for_entry(repo_root: &Path, entry: &HarnessEntry, mirror_rel: &str) -> Option<String> {
    // A skills mirror is a byte copy, so the path maps one-to-one.
    if let (Some(skills_dir), Some(source_dir)) = (&entry.skills_dir, &entry.skills_mirrors)
        && let Some(suffix) = strip_dir(mirror_rel, skills_dir)
    {
        return Some(format!("{source_dir}/{suffix}"));
    }

    // An agent mirror is keyed on the agent's `name`, which the emitter also
    // uses as the emitted filename, so the stem identifies the source.
    if let (Some(agent_dir), Some(source_dir)) = (&entry.agent_dir, &entry.mirrors)
        && let Some(suffix) = strip_dir(mirror_rel, agent_dir)
    {
        let stem = Path::new(&suffix)
            .file_stem()?
            .to_string_lossy()
            .to_string();
        let sources = discover_agent_sources(&repo_root.join(source_dir)).ok()?;
        let (path, _) = sources.into_iter().find(|(_, name)| *name == stem)?;
        return path
            .strip_prefix(repo_root)
            .ok()
            .map(|p| p.to_string_lossy().replace('\\', "/"));
    }

    None
}

/// The remainder of `rel` below `dir`, comparing path components so `.agents/skills`
/// never claims `.agents/skills-archive/x.md`.
fn strip_dir(rel: &str, dir: &str) -> Option<String> {
    Path::new(rel)
        .strip_prefix(Path::new(dir))
        .ok()
        .map(|p| p.to_string_lossy().replace('\\', "/"))
}

// ---------------------------------------------------------------------------
// Promotion
// ---------------------------------------------------------------------------

/// Build the proposed canonical content for one mirror edit, and the list of
/// canonical fields the editing harness could not have carried.
///
/// Writes nothing. The caller prints the proposal; a human applies it.
///
/// # Errors
///
/// Returns an error if the mirror is not a tracked `generated` file, if no
/// canonical source can be resolved for it, or if either file cannot be read.
pub fn promote(repo_root: &Path, mirror_rel: &str) -> Result<PromoteProposal, String> {
    let mirror_rel = mirror_rel.trim_start_matches("./").to_string();
    let config = repo_config::load_or_default(repo_root);

    if !generated_files(repo_root)?.contains(&mirror_rel) {
        return Err(format!(
            "{mirror_rel} is not a generated binding file; only a file the registry classifies \
             `generated` has a canonical source to promote into"
        ));
    }
    let canonical_rel = resolve_canonical(repo_root, &config, &mirror_rel).ok_or_else(|| {
        format!("no canonical source is declared for {mirror_rel}; nothing to promote into")
    })?;

    let canonical = std::fs::read_to_string(repo_root.join(&canonical_rel))
        .map_err(|e| format!("failed to read {canonical_rel}: {e}"))?;
    let mirror = std::fs::read_to_string(repo_root.join(&mirror_rel))
        .map_err(|e| format!("failed to read {mirror_rel}: {e}"))?;

    let entry = owning_entry(&config, &mirror_rel);
    let skills_mirror = is_skills_mirror(&config, &mirror_rel);
    let proposed = if skills_mirror {
        // A byte copy translates nothing, so the mirror IS the proposal.
        mirror.clone()
    } else {
        let claude_dir = entry
            .and_then(|e| e.mirrors.clone())
            .map_or_else(|| repo_root.join(".claude/agents"), |m| repo_root.join(m));
        let sources = discover_agent_sources(&claude_dir).unwrap_or_default();
        let ctx = AgentPaths {
            mirror_dir: parent_of(repo_root, &mirror_rel),
            canonical_dir: parent_of(repo_root, &canonical_rel),
            claude_dir,
            sources: &sources,
        };
        propose_agent(&ctx, &canonical, &mirror)
    };

    // M2: a skills mirror is a byte copy (checked above), so promoting one
    // translates nothing and puts no field at risk — exactly what
    // `is_skills_mirror`'s own doc comment already claimed. Computing
    // `at_risk_fields` unconditionally applied the Codex *agent*
    // field-policy table to skill frontmatter, which happens to produce no
    // false positive today only because no `DropWarn`-class agent field name
    // collides with `name:`/`description:`.
    let at_risk = if skills_mirror {
        Vec::new()
    } else {
        at_risk_fields(&canonical, entry.map(|e| e.name.as_str()))
    };

    // M1: `attribute()` is what `harness sync triage` uses to compute
    // `Outcome::BothDiverged` and print its hard-stop wording; `promote` is
    // directly callable on its own with no dependency on triage having run,
    // so the same check runs here too rather than existing only in triage's
    // output formatter.
    let both_diverged =
        attribute(repo_root, &mirror_rel, Some(&canonical_rel)) == Outcome::BothDiverged;

    Ok(PromoteProposal {
        diff: unified_diff(&canonical_rel, &canonical, &proposed),
        at_risk,
        mirror: mirror_rel,
        canonical: canonical_rel,
        both_diverged,
    })
}

/// Absolute directory `rel` sits in, under `repo_root`.
fn parent_of(repo_root: &Path, rel: &str) -> PathBuf {
    let joined = repo_root.join(rel);
    joined.parent().map_or(joined.clone(), Path::to_path_buf)
}

/// The harness entry whose mirror trees contain `rel`.
fn owning_entry<'a>(config: &'a RepoConfig, rel: &str) -> Option<&'a HarnessEntry> {
    config.harness.iter().find(|e| {
        e.skills_dir
            .as_ref()
            .is_some_and(|d| e.skills_mirrors.is_some() && strip_dir(rel, d).is_some())
            || e.agent_dir
                .as_ref()
                .is_some_and(|d| e.mirrors.is_some() && strip_dir(rel, d).is_some())
    })
}

/// `true` when `rel` sits in a byte-copy skills mirror rather than a
/// translated agent mirror. A byte copy loses nothing, so promotion from one
/// needs no field translation and puts no field at risk.
fn is_skills_mirror(config: &RepoConfig, rel: &str) -> bool {
    config.harness.iter().any(|e| {
        e.skills_mirrors.is_some()
            && e.skills_dir
                .as_ref()
                .is_some_and(|d| strip_dir(rel, d).is_some())
    })
}

/// Substitute the mirror's description and body into the canonical file,
/// leaving every other canonical frontmatter field exactly as it was.
///
/// This is what makes promotion non-destructive by construction: a field the
/// editing harness never carried is never in a position to be dropped, because
/// the canonical file's own frontmatter is the base being edited rather than
/// something reconstructed from the mirror.
fn propose_agent(ctx: &AgentPaths<'_>, canonical: &str, mirror: &str) -> String {
    let (mut front, _) = split_frontmatter(canonical);
    let (_, body) = mirror_content(mirror);
    let body = rebase_links_to_canonical(&body, ctx);

    if let Some(description) = mirror_description(mirror) {
        front = replace_scalar_field(&front, "description", &description);
    }
    if front.is_empty() {
        return body;
    }
    format!("---\n{front}---\n{body}")
}

/// The three directories a reverse link rebase needs, gathered so the rebase
/// signature stays readable.
struct AgentPaths<'a> {
    /// Absolute `.claude/agents/` path — the canonical agent tree.
    claude_dir: PathBuf,
    /// Absolute directory the mirror file sits in.
    mirror_dir: PathBuf,
    /// Absolute directory the canonical file sits in, which may be one
    /// `<group>/` level deeper than `claude_dir`.
    canonical_dir: PathBuf,
    /// Canonical agent sources, `(absolute path, name)`, for resolving the
    /// bare-filename links the emitter flattens agent-to-agent links into.
    sources: &'a [(PathBuf, String)],
}

/// Invert [`super::converter::rebase_agent_links`]: rewrite every relative link
/// in a mirror body so it resolves from the canonical file's own depth.
///
/// The forward rewrite is invertible in both of the shapes it produces. A link
/// to another agent was flattened to a bare filename, and agent names are
/// unique by construction, so the canonical path is a lookup. Every other link
/// was re-relativized from the mirror directory, which is a pure depth change.
///
/// Without this, promoting a body verbatim would write the mirror's shallower
/// `../` depth into a canonical file one level deeper, silently breaking every
/// relative link in it — a data-loss event of exactly the kind promotion exists
/// to prevent.
fn rebase_links_to_canonical(body: &str, ctx: &AgentPaths<'_>) -> String {
    agent_link_re()
        .replace_all(body, |caps: &regex::Captures<'_>| {
            let link = &caps[1];
            if link.is_empty()
                || link.starts_with("http://")
                || link.starts_with("https://")
                || link.starts_with('#')
                || link.starts_with('/')
            {
                return format!("]({link})");
            }
            let (path_part, anchor) = link
                .split_once('#')
                .map_or((link, None), |(p, a)| (p, Some(a)));
            if path_part.is_empty() {
                return format!("]({link})");
            }

            let target = agent_target(path_part, ctx)
                .unwrap_or_else(|| normalize_lexical(&ctx.mirror_dir.join(path_part)));
            let mut out = relative_from(&target, &ctx.canonical_dir)
                .to_string_lossy()
                .replace('\\', "/");
            if let Some(a) = anchor {
                out.push('#');
                out.push_str(a);
            }
            format!("]({out})")
        })
        .into_owned()
}

/// The canonical path a flattened agent-to-agent link points at, or `None` when
/// the link is not one.
fn agent_target(path_part: &str, ctx: &AgentPaths<'_>) -> Option<PathBuf> {
    if path_part.contains('/') {
        return None;
    }
    let stem = Path::new(path_part)
        .file_stem()?
        .to_string_lossy()
        .to_string();
    // Only a link that would otherwise resolve inside the canonical agent tree
    // is an agent link; anything else is an ordinary relative path.
    ctx.sources
        .iter()
        .find(|(path, name)| *name == stem && path.starts_with(&ctx.claude_dir))
        .map(|(path, _)| path.clone())
}

/// `(frontmatter, body)` for a markdown file with a leading `---` block.
/// A file without one yields an empty frontmatter and its whole content as body.
fn split_frontmatter(text: &str) -> (String, String) {
    let Some(rest) = text.strip_prefix("---\n") else {
        return (String::new(), text.to_string());
    };
    match rest.split_once("\n---\n") {
        Some((front, body)) => (format!("{front}\n"), body.to_string()),
        None => (String::new(), text.to_string()),
    }
}

/// `(frontmatter, body)` for a mirror in either shape the emitters produce:
/// markdown with YAML frontmatter, or the Codex TOML agent table.
fn mirror_content(mirror: &str) -> (String, String) {
    if mirror.starts_with("---\n") {
        return split_frontmatter(mirror);
    }
    (
        String::new(),
        toml_string_value(mirror, "developer_instructions").unwrap_or_default(),
    )
}

/// The mirror's `description`, read from whichever shape it carries.
fn mirror_description(mirror: &str) -> Option<String> {
    if mirror.starts_with("---\n") {
        let (front, _) = split_frontmatter(mirror);
        return yaml_scalar(&front, "description");
    }
    toml_string_value(mirror, "description")
}

/// The value of a top-level `key: value` scalar in a YAML frontmatter block.
fn yaml_scalar(front: &str, key: &str) -> Option<String> {
    let prefix = format!("{key}:");
    front
        .lines()
        .find(|l| l.starts_with(&prefix))
        .map(|l| l[prefix.len()..].trim().to_string())
}

/// The value of a TOML `key = "..."` or `key = """..."""` assignment.
///
/// Deliberately narrow: the Codex emitter writes exactly these two shapes, and
/// a full TOML parse would accept shapes the emitter never produces.
fn toml_string_value(text: &str, key: &str) -> Option<String> {
    let needle = format!("{key} = ");
    let start = text.find(&needle)? + needle.len();
    let rest = &text[start..];
    if let Some(body) = rest.strip_prefix("\"\"\"\n") {
        return body.split("\"\"\"").next().map(str::to_string);
    }
    let body = rest.strip_prefix('"')?;
    body.split('"').next().map(|s| s.replace("\\\"", "\""))
}

/// Replace a top-level scalar field's value, preserving key order. Appends the
/// field when it is absent.
fn replace_scalar_field(front: &str, key: &str, value: &str) -> String {
    let prefix = format!("{key}:");
    let mut replaced = false;
    let mut out = String::new();
    for line in front.lines() {
        if line.starts_with(&prefix) {
            let _ = writeln!(out, "{key}: {value}");
            replaced = true;
        } else {
            out.push_str(line);
            out.push('\n');
        }
    }
    if !replaced {
        let _ = writeln!(out, "{key}: {value}");
    }
    out
}

/// The canonical frontmatter keys the named harness's field policy drops with a
/// warning — the fields whoever edited the mirror never saw.
///
/// Computed by intersecting the canonical file's actual keys with the harness's
/// own policy table, so adding a field to a policy updates this automatically
/// and no second list of field names exists anywhere.
fn at_risk_fields(canonical: &str, harness: Option<&str>) -> Vec<(String, String)> {
    let Some(table) = harness.and_then(policy_table) else {
        return Vec::new();
    };
    let drop_warn: BTreeMap<&str, &str> = table
        .iter()
        .filter(|(_, action, _)| *action == FieldAction::DropWarn)
        .map(|(field, _, reason)| (*field, *reason))
        .collect();

    let (front, _) = split_frontmatter(canonical);
    front
        .lines()
        .filter_map(|line| line.split_once(':').map(|(k, _)| k))
        .filter(|key| !key.starts_with(char::is_whitespace))
        .filter_map(|key| {
            drop_warn
                .get(key)
                .map(|reason| (key.to_string(), (*reason).to_string()))
        })
        .collect()
}

/// The field-policy table a harness name answers to.
///
/// The one place a harness name is matched to its policy. A harness with no
/// translation step — a byte-copy mirror — has no table and therefore no
/// at-risk fields, which is correct rather than missing.
fn policy_table(harness: &str) -> Option<&'static [(&'static str, FieldAction, &'static str)]> {
    match harness {
        "opencode" => Some(OPENCODE_FIELD_POLICY_TABLE),
        "codex" => Some(CODEX_FIELD_POLICY_TABLE),
        _ => None,
    }
}

// ---------------------------------------------------------------------------
// Unified diff
// ---------------------------------------------------------------------------

/// Number of unchanged lines shown around each hunk.
const DIFF_CONTEXT: usize = 3;

/// A unified diff from `old` to `new`, labelled with `path`.
///
/// Returns an empty string when the two are identical, so a caller can treat
/// "no proposal" as an empty diff rather than a special case.
#[must_use]
pub fn unified_diff(path: &str, old: &str, new: &str) -> String {
    if old == new {
        return String::new();
    }
    let a: Vec<&str> = old.lines().collect();
    let b: Vec<&str> = new.lines().collect();
    let common = lcs_table(&a, &b);

    let mut ops: Vec<(char, &str)> = Vec::new();
    let (mut i, mut j) = (0_usize, 0_usize);
    while i < a.len() && j < b.len() {
        if a[i] == b[j] {
            ops.push((' ', a[i]));
            i += 1;
            j += 1;
        } else if common[i + 1][j] >= common[i][j + 1] {
            ops.push(('-', a[i]));
            i += 1;
        } else {
            ops.push(('+', b[j]));
            j += 1;
        }
    }
    for line in a.iter().skip(i) {
        ops.push(('-', line));
    }
    for line in b.iter().skip(j) {
        ops.push(('+', line));
    }

    render_hunks(path, &ops)
}

/// `common[i][j]` is the longest common subsequence length of `a[i..]`/`b[j..]`.
fn lcs_table(a: &[&str], b: &[&str]) -> Vec<Vec<usize>> {
    let mut table = vec![vec![0_usize; b.len() + 1]; a.len() + 1];
    for i in (0..a.len()).rev() {
        for j in (0..b.len()).rev() {
            table[i][j] = if a[i] == b[j] {
                table[i + 1][j + 1] + 1
            } else {
                table[i + 1][j].max(table[i][j + 1])
            };
        }
    }
    table
}

/// Render the edit script as unified-diff hunks with [`DIFF_CONTEXT`] lines of
/// context on each side.
fn render_hunks(path: &str, ops: &[(char, &str)]) -> String {
    let changed: Vec<usize> = ops
        .iter()
        .enumerate()
        .filter(|(_, (tag, _))| *tag != ' ')
        .map(|(idx, _)| idx)
        .collect();
    if changed.is_empty() {
        return String::new();
    }

    let mut out = format!("--- a/{path}\n+++ b/{path}\n");
    let mut cursor = 0_usize;
    while cursor < changed.len() {
        let start = changed[cursor].saturating_sub(DIFF_CONTEXT);
        let mut end = changed[cursor] + DIFF_CONTEXT;
        let mut next = cursor + 1;
        while next < changed.len() && changed[next] <= end + DIFF_CONTEXT {
            end = changed[next] + DIFF_CONTEXT;
            next += 1;
        }
        let end = end.min(ops.len() - 1);

        let (mut old_len, mut new_len) = (0_usize, 0_usize);
        for (tag, _) in &ops[start..=end] {
            match tag {
                '-' => old_len += 1,
                '+' => new_len += 1,
                _ => {
                    old_len += 1;
                    new_len += 1;
                }
            }
        }
        let old_start = ops[..start].iter().filter(|(t, _)| *t != '+').count() + 1;
        let new_start = ops[..start].iter().filter(|(t, _)| *t != '-').count() + 1;
        let _ = writeln!(out, "@@ -{old_start},{old_len} +{new_start},{new_len} @@");
        for (tag, line) in &ops[start..=end] {
            out.push(*tag);
            out.push_str(line);
            out.push('\n');
        }
        cursor = next;
    }
    out
}
