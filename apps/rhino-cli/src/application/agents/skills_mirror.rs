//! Real-file mirror of the canonical skills tree into a generated harness's
//! skills directory.
//!
//! `Claude Code` and `OpenCode` both read `.claude/skills/<name>/SKILL.md`
//! natively, so neither needs a copy. Codex does not: it discovers skills only
//! under `.agents/skills/`. This module materialises that tree as **real
//! files** — never symlinks — because the mirror is committed and a symlink
//! would not survive a `git archive`, a Windows checkout, or a container COPY.
//!
//! Both the source tree and the mirror target come from the `harness:` registry
//! in `repo-config.yml` (`skills-mirrors` and `skills-dir`), so adding a fourth
//! harness that wants a skills mirror is a config change, not a source edit
//! (DD-2).

use std::collections::BTreeSet;
use std::path::{Path, PathBuf};

use crate::application::repo_config;

/// Outcome of one `emit_skills_mirrors` run.
#[derive(Debug, Default, Clone, PartialEq, Eq)]
pub struct MirrorResult {
    /// Files written (or that would be written under `dry_run`).
    pub copied: usize,
    /// Files removed because their source counterpart no longer exists.
    pub removed: usize,
    /// Mirror directories left untouched because the registry declares them vendored.
    pub vendored_skipped: usize,
}

/// One harness entry's mirror job, resolved from the registry.
#[derive(Debug, Clone)]
struct MirrorJob {
    /// Absolute path of the canonical source tree.
    source: PathBuf,
    /// Absolute path of the generated mirror tree.
    target: PathBuf,
    /// Repository-relative path of the mirror tree, used to test a mirrored file
    /// against the registry's vendored declarations, which are repo-relative.
    target_rel: PathBuf,
    /// Repository-relative vendored directories the emitter must not touch.
    vendored: Vec<String>,
}

/// Every mirror job the registry declares.
///
/// A harness participates only when it declares BOTH `skills-dir` (where the
/// mirror goes) and `skills-mirrors` (what it mirrors). Declaring one without
/// the other is not an implicit mirror — that would resurrect the inference this
/// design exists to remove.
fn mirror_jobs(repo_root: &Path) -> Result<Vec<MirrorJob>, String> {
    // `load_optional`, not `load_or_default` and not a `Path::exists()` guard.
    // A tree with no `repo-config.yml` declares no mirrors, which means there
    // is nothing to do; but a *present, schema-invalid* registry — or one that
    // exists but cannot be read, e.g. a dangling symlink or a permission-denied
    // ancestor — must fail loudly rather than collapse into
    // `RepoConfig::default()`'s empty `harness` list, which would make every
    // downstream reader (the drift audit, and the pre-push validate gate that
    // calls it) report zero mirrors and exit success over a registry that
    // never actually parsed. `load_optional` discriminates on the read's own
    // `io::ErrorKind::NotFound`, so only a genuinely-absent file takes the
    // default branch — unlike `ownership.rs::guard_emitter_targets`, which
    // uses an unconditional strict `load` with no absent-file branch at all
    // (deliberately: the write path has no legitimate "no registry" case).
    let config = repo_config::load_optional(repo_root)
        .map_err(|error| format!("{error:#}"))?
        .unwrap_or_default();
    config
        .harness
        .iter()
        .filter_map(|entry| {
            let target_rel = entry.skills_dir.as_ref()?;
            let source_rel = entry.skills_mirrors.as_ref()?;
            Some((entry, target_rel, source_rel))
        })
        .map(|(entry, target_rel, source_rel)| {
            // `Path::join` silently discards `repo_root` when the joined value
            // is itself absolute, so an absolute or `../`-escaping `skills-dir`
            // / `skills-mirrors` would otherwise make this job read from and
            // write/delete outside the repository entirely, with
            // `repo-config validate` exiting 0 (C4). `confined_repo_path` goes
            // further than a lexical check: it canonicalizes the nearest
            // existing ancestor, so a path that is lexically repo-relative but
            // resolves outside `repo_root` through a committed symlink is also
            // refused here, before the job is built (cycle-2 Finding 2).
            let source =
                repo_config::confined_repo_path(repo_root, source_rel).map_err(|error| {
                    format!(
                        "harness {:?} skills-mirrors {source_rel:?}: {error:#}",
                        entry.name
                    )
                })?;
            let target =
                repo_config::confined_repo_path(repo_root, target_rel).map_err(|error| {
                    format!(
                        "harness {:?} skills-dir {target_rel:?}: {error:#}",
                        entry.name
                    )
                })?;
            // A `vendored[]` entry that trims to empty or root (`""`, `/`) must
            // fail the whole job rather than silently mean "nothing is
            // vendored": `is_vendored` routes every declaration through
            // `path_is_under`, whose empty-dir guard makes a malformed
            // declaration match no file, which flips every currently-vendored
            // file into `job_diff`'s `to_remove` set and deletes it on the next
            // `emit_skills_mirrors` (cycle-5 CRITICAL). `repo-config validate`
            // already rejects this shape, but nothing forces that command to
            // run before `harness bindings generate` does — this defensive
            // check makes the removal path itself fail-safe rather than
            // depending on a separate command having been run first, the same
            // pattern `confined_repo_path` above already applies to
            // `skills-dir`/`skills-mirrors`.
            for v in &entry.vendored {
                repo_config::validate_repo_relative_path(v).map_err(|error| {
                    format!(
                        "harness {:?} vendored {v:?}: {error} (a malformed vendored declaration \
                         must not be treated as \"nothing is vendored\" — that would delete \
                         every mirrored file this entry was supposed to protect)",
                        entry.name
                    )
                })?;
            }
            Ok(MirrorJob {
                source,
                target,
                target_rel: PathBuf::from(target_rel),
                vendored: entry.vendored.clone(),
            })
        })
        .collect()
}

/// Relative paths of every regular file under `root`, sorted.
///
/// Uses `symlink_metadata` so a symlinked directory is never traversed: the
/// mirror must be able to observe one rather than silently follow it.
fn relative_files(root: &Path) -> Vec<String> {
    fn walk(dir: &Path, base: &Path, out: &mut Vec<String>) {
        let Ok(entries) = std::fs::read_dir(dir) else {
            return;
        };
        for entry in entries.flatten() {
            let path = entry.path();
            let Ok(meta) = std::fs::symlink_metadata(&path) else {
                continue;
            };
            if meta.file_type().is_dir() {
                walk(&path, base, out);
            } else if let Ok(rel) = path.strip_prefix(base) {
                out.push(rel.to_string_lossy().into_owned());
            }
        }
    }
    let mut out = Vec::new();
    walk(root, root, &mut out);
    out.sort();
    out
}

/// `true` when `rel` (a path relative to the repository root) lies inside any
/// declared vendored directory.
///
/// Compares path components rather than string prefixes, so a vendored
/// `.agents/skills/compress` never also claims `.agents/skills/compress-extra`.
fn is_vendored(rel: &Path, vendored: &[String]) -> bool {
    vendored.iter().any(|v| repo_config::path_is_under(rel, v))
}

/// What one mirror job would change, computed without touching the filesystem.
#[derive(Debug, Default, Clone, PartialEq, Eq)]
pub struct JobDiff {
    /// Source-relative paths whose mirrored copy is missing or byte-different.
    pub to_write: Vec<String>,
    /// Mirror-relative paths with no source counterpart and no vendored declaration.
    pub to_remove: Vec<String>,
    /// Mirrored files left alone because the registry declares them vendored.
    pub vendored_skipped: usize,
}

/// Computes one job's pending changes.
///
/// Both the emitter and the validator call this, so "what the mirror should
/// contain" is decided exactly once. A validator with its own reader would
/// drift from the emitter the moment either changed.
fn job_diff(job: &MirrorJob) -> Result<JobDiff, String> {
    let mut diff = JobDiff::default();
    let wanted: BTreeSet<String> = relative_files(&job.source).into_iter().collect();

    for rel in &wanted {
        let src = job.source.join(rel);
        let dst = job.target.join(rel);
        let bytes =
            std::fs::read(&src).map_err(|e| format!("failed to read {}: {e}", src.display()))?;
        if !std::fs::read(&dst).is_ok_and(|existing| existing == bytes) {
            diff.to_write.push(rel.clone());
        }
    }

    for rel in relative_files(&job.target) {
        // Ownership is READ FROM THE REGISTRY, never inferred from "this file has
        // no source counterpart": by that inference every vendored file is stale,
        // and one regeneration would delete the whole committed plugin payload
        // (DD-7).
        if is_vendored(&job.target_rel.join(&rel), &job.vendored) {
            diff.vendored_skipped += 1;
        } else if !wanted.contains(&rel) {
            diff.to_remove.push(rel);
        }
    }

    Ok(diff)
}

/// A mirror file that disagrees with the canonical tree.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum MirrorDrift {
    /// A source skill file with a missing or byte-different mirrored copy.
    Missing(String),
    /// A mirrored file with neither a source counterpart nor a vendored declaration.
    Undeclared(String),
}

impl std::fmt::Display for MirrorDrift {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Missing(p) => write!(f, "missing or stale mirror for {p}"),
            Self::Undeclared(p) => write!(f, "undeclared directory in the mirror: {p}"),
        }
    }
}

/// Reports every mirror file that disagrees with the canonical tree, without
/// modifying anything.
///
/// # Errors
///
/// Returns an error if `repo-config.yml` cannot be loaded or a source file
/// cannot be read.
pub fn audit_skills_mirrors(repo_root: &Path) -> Result<Vec<MirrorDrift>, String> {
    let mut drifts = Vec::new();
    for job in mirror_jobs(repo_root)? {
        if !job.source.is_dir() {
            continue;
        }
        let diff = job_diff(&job)?;
        let rel = |p: &str| job.target_rel.join(p).to_string_lossy().into_owned();
        drifts.extend(diff.to_write.iter().map(|p| MirrorDrift::Missing(rel(p))));
        drifts.extend(
            diff.to_remove
                .iter()
                .map(|p| MirrorDrift::Undeclared(rel(p))),
        );
    }
    Ok(drifts)
}

/// Mirrors every registry-declared skills tree into its harness's skills
/// directory as real files, deleting mirrored files whose source counterpart is
/// gone and leaving every declared vendored directory alone.
///
/// # Errors
///
/// Returns an error if `repo-config.yml` cannot be loaded, or if a directory or
/// file cannot be created, read, written, or removed.
pub fn emit_skills_mirrors(repo_root: &Path, dry_run: bool) -> Result<MirrorResult, String> {
    let mut result = MirrorResult::default();
    // `job.target` is `confined_repo_path`'s **canonicalized** return value, so
    // this defense-in-depth re-check must compare against a canonicalized
    // `repo_root` too — comparing against the raw, possibly-symlinked
    // `repo_root` parameter would make the check spuriously fail (or, before
    // this fix, spuriously always pass: the un-canonicalized lexical join
    // used to make `job.target.starts_with(repo_root)` a tautology that could
    // never be false, documented as a live safety net it did not provide).
    let canonical_repo_root = repo_root
        .canonicalize()
        .map_err(|e| format!("canonicalize repository root {}: {e}", repo_root.display()))?;
    for job in mirror_jobs(repo_root)? {
        // Defense in depth alongside `mirror_jobs`' `confined_repo_path`
        // proof: every write and delete below stays inside `repo_root`, full
        // stop. Real protection now, not a tautology: `confined_repo_path`
        // returns the canonicalized destination, so a future maintainer who
        // weakens it or adds a `MirrorJob` construction path that bypasses it
        // is still caught here.
        if !job.target.starts_with(&canonical_repo_root) {
            return Err(format!(
                "refusing to write outside the repository: {}",
                job.target.display()
            ));
        }
        if !job.source.is_dir() {
            continue;
        }
        let diff = job_diff(&job)?;
        result.copied += diff.to_write.len();
        result.removed += diff.to_remove.len();
        result.vendored_skipped += diff.vendored_skipped;
        if dry_run {
            continue;
        }

        for rel in &diff.to_write {
            let src = job.source.join(rel);
            let dst = job.target.join(rel);
            let bytes = std::fs::read(&src)
                .map_err(|e| format!("failed to read {}: {e}", src.display()))?;
            if let Some(parent) = dst.parent() {
                std::fs::create_dir_all(parent)
                    .map_err(|e| format!("failed to create {}: {e}", parent.display()))?;
            }
            std::fs::write(&dst, &bytes)
                .map_err(|e| format!("failed to write {}: {e}", dst.display()))?;
        }

        for rel in &diff.to_remove {
            let path = job.target.join(rel);
            std::fs::remove_file(&path)
                .map_err(|e| format!("failed to remove {}: {e}", path.display()))?;
            prune_empty_dirs(path.parent(), &job.target);
        }
    }
    Ok(result)
}

/// Walks upward from `dir` removing directories left empty by a deletion,
/// stopping at (and never removing) `stop`.
///
/// A failed removal is deliberately ignored: the only expected cause is a
/// non-empty directory, which is exactly the case where stopping is correct.
fn prune_empty_dirs(dir: Option<&Path>, stop: &Path) {
    let mut cursor = dir;
    while let Some(path) = cursor {
        if path == stop || !path.starts_with(stop) || std::fs::remove_dir(path).is_err() {
            return;
        }
        cursor = path.parent();
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    fn write(root: &Path, rel: &str, body: &str) {
        let p = root.join(rel);
        std::fs::create_dir_all(p.parent().unwrap()).unwrap();
        std::fs::write(p, body).unwrap();
    }

    fn fixture(vendored: &str) -> tempfile::TempDir {
        let dir = tempfile::TempDir::new().unwrap();
        write(
            dir.path(),
            "repo-config.yml",
            &format!(
                "harness:\n  - {{ name: claude-code, tier: source, agent-dir: .claude/agents }}\n  \
                 - name: codex\n    tier: generated\n    agent-dir: .codex/agents\n    \
                 skills-dir: .agents/skills\n    skills-mirrors: .claude/skills\n{vendored}\
                 coverage:\n  projects: []\n"
            ),
        );
        dir
    }

    #[test]
    fn mirrors_nested_payload_as_real_files() {
        let dir = fixture("");
        write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
        write(dir.path(), ".claude/skills/a/reference/r.md", "ref\n");
        let out = emit_skills_mirrors(dir.path(), false).unwrap();
        assert_eq!(out.copied, 2);
        assert_eq!(
            std::fs::read_to_string(dir.path().join(".agents/skills/a/reference/r.md")).unwrap(),
            "ref\n"
        );
        assert!(
            std::fs::symlink_metadata(dir.path().join(".agents/skills/a/SKILL.md"))
                .unwrap()
                .file_type()
                .is_file()
        );
    }

    #[test]
    fn a_second_run_copies_nothing() {
        let dir = fixture("");
        write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
        assert_eq!(emit_skills_mirrors(dir.path(), false).unwrap().copied, 1);
        assert_eq!(emit_skills_mirrors(dir.path(), false).unwrap().copied, 0);
    }

    #[test]
    fn dry_run_writes_nothing() {
        let dir = fixture("");
        write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
        assert_eq!(emit_skills_mirrors(dir.path(), true).unwrap().copied, 1);
        assert!(!dir.path().join(".agents/skills/a/SKILL.md").exists());
    }

    #[test]
    fn a_harness_declaring_no_source_is_not_mirrored() {
        let dir = tempfile::TempDir::new().unwrap();
        write(
            dir.path(),
            "repo-config.yml",
            "harness:\n  - { name: claude-code, tier: source, agent-dir: .claude/agents, \
             skills-dir: .claude/skills }\ncoverage:\n  projects: []\n",
        );
        write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
        // claude-code declares skills-dir but no skills-mirrors, so it is a
        // source tree, not a mirror target: nothing may be written into it.
        assert_eq!(emit_skills_mirrors(dir.path(), false).unwrap().copied, 0);
    }

    #[test]
    fn a_renamed_source_directory_moves_its_mirror() {
        let dir = fixture("");
        write(dir.path(), ".claude/skills/old-name/SKILL.md", "skill\n");
        emit_skills_mirrors(dir.path(), false).unwrap();
        assert!(dir.path().join(".agents/skills/old-name/SKILL.md").exists());

        std::fs::remove_dir_all(dir.path().join(".claude/skills/old-name")).unwrap();
        write(dir.path(), ".claude/skills/new-name/SKILL.md", "skill\n");
        let out = emit_skills_mirrors(dir.path(), false).unwrap();

        assert_eq!(out.removed, 1);
        assert!(!dir.path().join(".agents/skills/old-name").exists());
        assert!(dir.path().join(".agents/skills/new-name/SKILL.md").exists());
    }

    #[test]
    fn a_vendored_directory_survives_regeneration() {
        let dir = fixture("    vendored:\n      - .agents/skills/vendor-plugin\n");
        write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
        write(
            dir.path(),
            ".agents/skills/vendor-plugin/SKILL.md",
            "vendored payload\n",
        );
        let out = emit_skills_mirrors(dir.path(), false).unwrap();

        assert_eq!(out.vendored_skipped, 1);
        assert_eq!(out.removed, 0, "a vendored file is never stale");
        assert_eq!(
            std::fs::read_to_string(dir.path().join(".agents/skills/vendor-plugin/SKILL.md"))
                .unwrap(),
            "vendored payload\n",
            "vendored payload must be byte-identical after regeneration"
        );
    }

    #[test]
    fn an_undeclared_orphan_is_removed_but_a_declared_one_is_not() {
        // Falsifiable both ways from one fixture pair: the SAME orphan file is
        // deleted when undeclared and preserved when declared.
        for (vendored, expect_removed) in [
            ("", 1_usize),
            ("    vendored:\n      - .agents/skills/orphan\n", 0),
        ] {
            let dir = fixture(vendored);
            write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
            write(dir.path(), ".agents/skills/orphan/SKILL.md", "orphan\n");
            let out = emit_skills_mirrors(dir.path(), false).unwrap();
            assert_eq!(
                out.removed, expect_removed,
                "vendored block was: {vendored:?}"
            );
            assert_eq!(
                dir.path().join(".agents/skills/orphan/SKILL.md").exists(),
                expect_removed == 0
            );
        }
    }

    // Cycle-5 CRITICAL regression: a `vendored[]` entry that trims to empty or
    // root must fail the whole job rather than silently delete the file it
    // was declared to protect. Falsifiable both ways from the same fixture
    // shape the doubled-orphan test above uses: an already-vendored, already-
    // present file must still exist on disk after the refusal, not just after
    // a passing run.
    #[test]
    fn a_malformed_vendored_declaration_is_refused_rather_than_deleting_the_file_it_protects() {
        for bad_vendored in [
            "    vendored:\n      - \"\"\n",
            "    vendored:\n      - /\n",
        ] {
            let dir = fixture(bad_vendored);
            write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
            write(
                dir.path(),
                ".agents/skills/vendor-plugin/SKILL.md",
                "vendored payload\n",
            );

            let error = emit_skills_mirrors(dir.path(), false)
                .expect_err("an empty or root vendored declaration must be refused");
            assert!(
                error.contains("vendored"),
                "error must name the offending field; got: {error}"
            );
            assert!(
                dir.path()
                    .join(".agents/skills/vendor-plugin/SKILL.md")
                    .exists(),
                "a malformed vendored declaration must not delete an unrelated file \
                 (bad_vendored was: {bad_vendored:?})"
            );
        }
    }

    // Cycle-5 CRITICAL regression, direct at `is_vendored` itself (the fourth
    // and previously-uncovered `path_is_under` call site): an empty
    // declaration must not claim every mirrored file — `path_is_under`'s
    // empty-dir guard is what makes this `false`, and `mirror_jobs`'
    // validation above is what stops the malformed declaration from reaching
    // `is_vendored` in production, but this function must stay sound on its
    // own rather than depend on that caller.
    #[test]
    fn is_vendored_rejects_an_empty_or_root_declaration_against_any_path() {
        assert!(!is_vendored(
            Path::new("any/mirrored/file.md"),
            &[String::new()]
        ));
        assert!(!is_vendored(
            Path::new("any/mirrored/file.md"),
            &["/".to_string()]
        ));
    }

    #[test]
    fn an_absolute_skills_dir_is_refused_rather_than_written_outside_the_repository() {
        let dir = tempfile::TempDir::new().unwrap();
        let outside = tempfile::TempDir::new().unwrap();
        write(dir.path(), ".claude/skills/a/SKILL.md", "skill\n");
        write(outside.path(), "victim.md", "must survive regeneration\n");
        write(
            dir.path(),
            "repo-config.yml",
            &format!(
                "harness:\n  - {{ name: claude-code, tier: source, agent-dir: .claude/agents }}\n  \
                 - name: codex\n    tier: generated\n    agent-dir: .codex/agents\n    \
                 skills-dir: {}\n    skills-mirrors: .claude/skills\ncoverage:\n  projects: []\n",
                outside.path().display()
            ),
        );

        let error = emit_skills_mirrors(dir.path(), false)
            .expect_err("an absolute skills-dir must be refused");
        assert!(error.contains("skills-dir"), "error was: {error}");
        assert!(
            outside.path().join("victim.md").exists(),
            "the file outside the repository must survive"
        );
    }

    #[test]
    fn vendored_prefix_matching_is_component_wise() {
        assert!(is_vendored(
            Path::new(".agents/skills/compress/SKILL.md"),
            &[".agents/skills/compress".to_string()]
        ));
        assert!(!is_vendored(
            Path::new(".agents/skills/compress-extra/SKILL.md"),
            &[".agents/skills/compress".to_string()]
        ));
    }

    // Regression for the thread-1 fix: a `repo-config.yml` that is present but
    // unreadable (here, a dangling symlink) must NOT be treated as "no
    // registry declared". `Path::exists()` returns `false` for both a
    // genuinely-absent file and a dangling symlink, which is exactly the
    // ambiguity `load_optional` was introduced to remove.
    #[cfg(unix)]
    #[test]
    fn a_dangling_repo_config_symlink_fails_loudly_instead_of_defaulting() {
        use std::os::unix::fs::symlink;

        let dir = tempfile::TempDir::new().unwrap();
        symlink(
            dir.path().join("nonexistent-target"),
            dir.path().join("repo-config.yml"),
        )
        .unwrap();

        let error = emit_skills_mirrors(dir.path(), false)
            .expect_err("a dangling symlink must not silently default to zero mirrors");
        assert!(
            !error.is_empty(),
            "the error must name the underlying read failure"
        );
    }

    #[test]
    fn a_genuinely_absent_repo_config_yields_zero_mirrors_not_an_error() {
        let dir = tempfile::TempDir::new().unwrap();
        let out = emit_skills_mirrors(dir.path(), false)
            .expect("a tree with no repo-config.yml at all declares no mirrors");
        assert_eq!(out.copied, 0);
        assert_eq!(out.removed, 0);
    }
}
