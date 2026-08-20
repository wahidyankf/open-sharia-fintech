//! Total ownership of binding files (US-8).
//!
//! Every tracked file under a binding directory falls into exactly one declared
//! class — `generated`, `vendored`, or `source`. There is no fourth class and no
//! unclassified residue.
//!
//! The defect this module exists to make impossible: `.opencode/skills/` sat in
//! a binding directory for months owned by nobody. It was not generated from
//! anything, not declared vendored, and excluded from the word budget by a
//! comment — so no check could tell it apart from a file someone meant to keep.
//! Enumerating from the git index and demanding a declared class for every entry
//! turns that silence into a named failure.
//!
//! Classification is DECLARED, never inferred. An inference such as "a file with
//! no source counterpart must be stale" would have deleted the committed plugin
//! payload under `.agents/skills/` (DD-7).

use std::path::Path;
use std::process::Command;
use std::time::Instant;

use crate::application::agents::bindings::validate_bindings;
use crate::application::agents::types::{ValidationCheck, ValidationResult};
use crate::application::repo_config::{self, OwnershipClass, RepoConfig, Tier};

/// Name of the classification check, so the gate output is greppable.
const CLASSIFICATION_CHECK: &str = "Ownership: every tracked binding file is classified";

/// Name of the emitter-target guard check.
const SOURCE_GUARD_CHECK: &str = "Ownership: no emitter target is declared source";

/// One tracked binding file and the class that owns it.
#[derive(Debug, Clone)]
pub struct ClassifiedFile {
    /// Repository-relative path, exactly as `git ls-files` reports it.
    pub path: String,
    /// The declaration that claimed it, and the class that declaration carries.
    pub class: OwnershipClass,
}

/// Result of classifying every tracked file under every binding directory.
#[derive(Debug, Default)]
pub struct OwnershipReport {
    /// Files carrying a declared class.
    pub classified: Vec<ClassifiedFile>,
    /// Files under a binding directory that no declaration claims.
    pub unclassified: Vec<String>,
}

impl OwnershipReport {
    /// Total tracked binding files seen, classified or not.
    #[must_use]
    pub fn total(&self) -> usize {
        self.classified.len() + self.unclassified.len()
    }

    /// How many files carry `class`.
    #[must_use]
    pub fn count(&self, class: OwnershipClass) -> usize {
        self.classified.iter().filter(|f| f.class == class).count()
    }
}

/// Directories and files the registry treats as binding surfaces.
///
/// Derived from the registry rather than hard-coded, so adding a fourth harness
/// is still one `repo-config.yml` entry (DD-2). A declaration's root is its
/// first path component for a directory-shaped path, and the path itself for a
/// root-level file such as `AGENTS.md`.
fn binding_roots(config: &RepoConfig) -> Vec<String> {
    let mut roots: Vec<String> = Vec::new();
    let mut push = |value: &str| {
        let trimmed = value.trim_end_matches('/');
        if trimmed.is_empty() {
            return;
        }
        let root = trimmed
            .split_once('/')
            .map_or(trimmed, |(head, _)| head)
            .to_owned();
        if !roots.contains(&root) {
            roots.push(root);
        }
    };
    for entry in &config.harness {
        for opt in [
            entry.agent_dir.as_ref(),
            entry.skills_dir.as_ref(),
            entry.rules_dir.as_ref(),
            entry.config.as_ref(),
        ]
        .into_iter()
        .flatten()
        {
            push(opt);
        }
        for path in &entry.instruction {
            push(path);
        }
        for owned in &entry.ownership {
            push(&owned.path);
        }
    }
    roots.sort();
    roots
}

/// True when `declaration` claims `file`.
///
/// A declaration claims a path when it names it exactly or is a directory
/// prefix of it. Routes through [`repo_config::path_is_under`] — the crate's
/// one shared component-wise containment predicate — rather than a
/// string-prefix test, which used to be a third, independent implementation
/// of the same check and could disagree with it on a doubled separator
/// (`.claude//skills` claiming `.claude/skills/x.md`).
fn claims(declaration: &str, file: &str) -> bool {
    let decl = declaration.trim_end_matches('/');
    file == decl || repo_config::path_is_under(file, decl)
}

/// Every ownership declaration in the registry, flattened across harnesses.
///
/// The same path may be declared by more than one harness — `AGENTS.md` is read
/// by both `OpenCode` and Codex — which is why the declarations are flattened and
/// the longest match wins rather than the first.
fn declarations(config: &RepoConfig) -> Vec<(String, OwnershipClass)> {
    config
        .harness
        .iter()
        .flat_map(|entry| {
            entry
                .ownership
                .iter()
                .map(|owned| (owned.path.trim_end_matches('/').to_owned(), owned.class))
        })
        .collect()
}

/// Tracked files under `roots`, straight from the git index.
///
/// Reading the index rather than walking the filesystem means a local scratch
/// file is not a failure, and a deleted-but-still-present file is not counted.
fn tracked_files(repo_root: &Path, roots: &[String]) -> Result<Vec<String>, String> {
    if roots.is_empty() {
        return Ok(Vec::new());
    }
    let mut args: Vec<&str> = vec!["ls-files", "-z", "--"];
    args.extend(roots.iter().map(String::as_str));
    let out = Command::new("git")
        .args(&args)
        .current_dir(repo_root)
        .output()
        .map_err(|e| format!("failed to run git ls-files: {e}"))?;
    if !out.status.success() {
        return Err(format!(
            "git ls-files failed: {}",
            String::from_utf8_lossy(&out.stderr).trim()
        ));
    }
    Ok(String::from_utf8_lossy(&out.stdout)
        .split('\0')
        .filter(|s| !s.is_empty())
        .map(ToOwned::to_owned)
        .collect())
}

/// Classify every tracked file under every binding directory.
///
/// # Errors
///
/// Returns an error when `repo-config.yml` cannot be read or `git ls-files`
/// fails.
pub fn classify(repo_root: &Path) -> Result<OwnershipReport, String> {
    let config = repo_config::load(repo_root).map_err(|e| format!("{e:#}"))?;
    let roots = binding_roots(&config);
    let decls = declarations(&config);
    let mut report = OwnershipReport::default();
    for file in tracked_files(repo_root, &roots)? {
        // Longest declaration wins, so `.claude/skills` beats `.claude/` for a
        // file under it and a broad root declaration cannot mask a narrower one.
        let best = decls
            .iter()
            .filter(|(decl, _)| claims(decl, &file))
            .max_by_key(|(decl, _)| decl.len());
        match best {
            Some((_, class)) => report.classified.push(ClassifiedFile {
                path: file,
                class: *class,
            }),
            None => report.unclassified.push(file),
        }
    }
    report.unclassified.sort();
    Ok(report)
}

/// Refuse to run the emitters when any emitter output path is declared `source`.
///
/// A generator that writes into hand-authored canonical source destroys the very
/// thing every mirror is generated from, so this refuses before the first write
/// rather than reporting the damage afterwards.
///
/// # Errors
///
/// Returns an error naming the offending path when a generated-tier entry's
/// output directory is declared `source`, or when `repo-config.yml` itself
/// fails to parse.
///
/// Deliberately `load`, not `load_or_default`: a registry that fails to parse
/// must stop generation rather than fall back to an empty config whose empty
/// `harness` list would make every entry's guard vacuously pass (C3 — a
/// malformed `tier` used to do exactly this).
///
/// This guard is not independently sound against a malformed *value* the way
/// it is against a malformed *shape*: `claims()` routes through
/// [`repo_config::path_is_under`], which trusts `decl` to already be a valid
/// repository-relative path. Soundness against a `path`/`vendored` entry that
/// trims to the empty string rests on the sibling `repo-config-schema` gate
/// (`repo_config_validate::validate_repo_relative_path`) rejecting that value
/// before it ever reaches this function, not on anything checked here.
pub fn guard_emitter_targets(repo_root: &Path) -> Result<(), String> {
    let config = repo_config::load(repo_root).map_err(|e| format!("{e:#}"))?;
    let decls = declarations(&config);
    for entry in &config.harness {
        if entry.tier != Tier::Generated {
            continue;
        }
        for target in [entry.agent_dir.as_ref(), entry.skills_dir.as_ref()]
            .into_iter()
            .flatten()
        {
            let claimed = decls
                .iter()
                .filter(|(decl, _)| claims(decl, target) || claims(target, decl))
                .max_by_key(|(decl, _)| decl.len());
            if let Some((decl, OwnershipClass::Source)) = claimed {
                return Err(format!(
                    "refusing to generate: harness {:?} would write to {target:?}, \
                     which {decl:?} declares source; the emitter never writes to \
                     hand-authored canonical input",
                    entry.name
                ));
            }
        }
    }
    Ok(())
}

/// Validate total ownership of every binding file.
///
/// Two obligations, reported through the shared check reporter:
/// 1. classification — no tracked binding file is unowned;
/// 2. class enforcement — a `generated` path reproduces byte-for-byte, which is
///    exactly what `harness bindings validate` already proves, so its checks are
///    folded in here rather than reimplemented. A `vendored` path carries no
///    byte guard by design, and a `source` path is guarded by refusing the write.
#[must_use]
pub fn validate_ownership(repo_root: &Path) -> ValidationResult {
    let start = Instant::now();
    let mut result = ValidationResult::default();

    match classify(repo_root) {
        Ok(report) if report.unclassified.is_empty() => {
            result.tally(ValidationCheck::passed(
                CLASSIFICATION_CHECK,
                format!(
                    "{} tracked binding file(s): {} generated, {} vendored, {} source",
                    report.total(),
                    report.count(OwnershipClass::Generated),
                    report.count(OwnershipClass::Vendored),
                    report.count(OwnershipClass::Source),
                ),
            ));
        }
        Ok(report) => {
            result.tally(ValidationCheck::failed_msg(
                CLASSIFICATION_CHECK,
                format!(
                    "{} tracked binding file(s) carry no declared ownership class: {}",
                    report.unclassified.len(),
                    report.unclassified.join(", ")
                ),
            ));
        }
        Err(error) => result.tally(ValidationCheck::failed_msg(CLASSIFICATION_CHECK, error)),
    }

    match guard_emitter_targets(repo_root) {
        Ok(()) => result.tally(ValidationCheck::passed(
            SOURCE_GUARD_CHECK,
            "no generated-tier output directory is declared source",
        )),
        Err(error) => result.tally(ValidationCheck::failed_msg(SOURCE_GUARD_CHECK, error)),
    }

    for check in validate_bindings(repo_root).checks {
        result.tally(check);
    }

    result.duration = start.elapsed();
    result
}

#[cfg(test)]
mod tests {
    use super::*;

    fn config_from(yaml: &str) -> RepoConfig {
        serde_norway::from_str(yaml).expect("fixture config parses")
    }

    #[test]
    fn a_declaration_claims_itself_and_its_children_only() {
        assert!(claims(".claude/skills", ".claude/skills"));
        assert!(claims(".claude/skills", ".claude/skills/a/SKILL.md"));
        assert!(claims(".claude/", ".claude/settings.json"));
        // Component-wise, so a sibling with a shared textual prefix is not claimed.
        assert!(!claims(".claude/skills", ".claude/skills-archive/a.md"));
        assert!(!claims(".claude/skills", ".claude"));
    }

    // Regression for the thread-12 fix: `claims()` used to be a third,
    // independent string-prefix implementation of the same containment check
    // `path_is_under` provides, and could disagree with it on a doubled
    // separator — `.claude//skills` would fail to claim `.claude/skills/x.md`
    // even though `path_is_under` (used elsewhere for the identical question)
    // matched correctly. Now unified onto `repo_config::path_is_under`.
    #[test]
    fn a_doubled_separator_declaration_still_claims_its_children() {
        assert!(claims(".claude//skills", ".claude/skills/x.md"));
    }

    // Cycle-4 F1 regression: an `ownership[].path` declaration that trims to
    // the empty string (e.g. `/`) must not claim every tracked file. Blocked
    // in production by `repo-config-schema` rejecting the value outright, but
    // `claims()` itself must not depend on that sibling gate to stay sound.
    #[test]
    fn an_empty_declaration_claims_nothing() {
        assert!(!claims("", "any/tracked/file.md"));
        assert!(!claims("/", "any/tracked/file.md"));
    }

    #[test]
    fn binding_roots_come_from_the_registry_not_a_hard_coded_list() {
        let config = config_from(concat!(
            "harness:\n",
            "  - name: made-up\n",
            "    tier: generated\n",
            "    agent-dir: .madeup/agents\n",
            "    mirrors: .claude/agents\n",
            "    instruction: [MADEUP.md]\n",
        ));
        let roots = binding_roots(&config);
        assert!(roots.contains(&".madeup".to_owned()), "roots: {roots:?}");
        assert!(roots.contains(&"MADEUP.md".to_owned()), "roots: {roots:?}");
    }

    #[test]
    fn the_longest_declaration_wins_so_a_root_cannot_mask_a_narrower_one() {
        let config = config_from(concat!(
            "harness:\n",
            "  - name: h\n",
            "    tier: source\n",
            "    agent-dir: .x/agents\n",
            "    ownership:\n",
            "      - { path: .x/, class: source }\n",
            "      - { path: .x/agents, class: generated }\n",
        ));
        let decls = declarations(&config);
        let best = decls
            .iter()
            .filter(|(d, _)| claims(d, ".x/agents/a.md"))
            .max_by_key(|(d, _)| d.len())
            .expect("a declaration claims the file");
        assert_eq!(best.1, OwnershipClass::Generated);
    }

    #[test]
    fn the_guard_refuses_an_emitter_target_declared_source() {
        let dir = tempfile::TempDir::new().expect("temp");
        std::fs::write(
            dir.path().join("repo-config.yml"),
            concat!(
                "harness:\n",
                "  - name: h\n",
                "    tier: generated\n",
                "    agent-dir: .out/agents\n",
                "    mirrors: .claude/agents\n",
                "    ownership:\n",
                "      - { path: .out/agents, class: source, reason: deliberately wrong }\n",
            ),
        )
        .expect("write");
        let error = guard_emitter_targets(dir.path()).expect_err("must refuse");
        assert!(error.contains(".out/agents"), "error was: {error}");
    }

    #[test]
    fn the_guard_permits_a_generated_target() {
        let dir = tempfile::TempDir::new().expect("temp");
        std::fs::write(
            dir.path().join("repo-config.yml"),
            concat!(
                "harness:\n",
                "  - name: h\n",
                "    tier: generated\n",
                "    agent-dir: .out/agents\n",
                "    mirrors: .claude/agents\n",
                "    ownership:\n",
                "      - { path: .out/agents, class: generated }\n",
            ),
        )
        .expect("write");
        guard_emitter_targets(dir.path()).expect("a generated target is permitted");
    }

    // Regression for C3: a one-character `tier:` typo used to deserialize as a
    // plain `String` that simply failed the `!= "generated"` comparison,
    // silently skipping the guard instead of failing to parse. `Tier` is now
    // an enum, so this fixture — identical to `the_guard_refuses_an_emitter_
    // target_declared_source` except for the typo — must fail generation
    // rather than let it through unguarded.
    #[test]
    fn a_mistyped_tier_fails_generation_instead_of_silently_bypassing_the_guard() {
        let dir = tempfile::TempDir::new().expect("temp");
        std::fs::write(
            dir.path().join("repo-config.yml"),
            concat!(
                "harness:\n",
                "  - name: h\n",
                "    tier: generatd\n", // one character short of "generated"
                "    agent-dir: .out/agents\n",
                "    mirrors: .claude/agents\n",
                "    ownership:\n",
                "      - { path: .out/agents, class: source, reason: deliberately wrong }\n",
            ),
        )
        .expect("write");
        let error =
            guard_emitter_targets(dir.path()).expect_err("a mistyped tier must fail, not pass");
        assert!(error.contains("tier"), "error was: {error}");
    }
}
