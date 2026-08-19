//! Binding generator and all-harness parity guard for rhino-cli.
//
// Covers all 3 supported coding-agent harnesses:
//   Source tier (hand-authored, the origin every mirror derives from):
//     - Claude Code (.claude/agents/ + .claude/skills/)
//
//   Generated tier (byte-parity enforced):
//     - OpenCode (.opencode/agents/ mirrors .claude/agents/)
//     - Codex (.codex/agents/ mirrors .claude/agents/; .agents/skills/ mirrors .claude/skills/)
//
//   Catalog coverage is enforced for every surface above plus .github/, which
//   carries repository-level agent configuration rather than a harness binding.
//
// Also validates the color/tier translation maps from validate-cross-vendor-parity.sh
// (invariants 5a/5b), replacing that shell script.

use std::fs;
use std::path::{Path, PathBuf};
use std::time::Instant;

use super::sync_validator::validate_sync;
use super::types::{ValidationCheck, ValidationResult};

/// Known binding directories / files checked for catalog coverage. If a path
/// in this list exists on disk, the platform-bindings catalog must reference it.
/// Covers all 3 supported harnesses plus the repository-level `.github` surface:
///   - Claude Code (.claude) — source of truth
///   - `OpenCode` (.opencode) — generated mirror of `.claude/agents/`
///   - Codex (.codex) — generated mirror of `.claude/agents/`, plus its own config
///   - Agent Skills (.agents) — the vendor-neutral skills surface Codex reads
///   - `.github` — repository-level configuration, not a harness binding
pub const KNOWN_BINDING_DIRS: &[&str] = &[".claude", ".opencode", ".codex", ".agents", ".github"];

/// Relative path (from repo root) of the platform-bindings catalog document.
pub const PLATFORM_BINDINGS_CATALOG: &str = "docs/reference/platform-bindings.md";

/// One canonical (relative path, expected content) pair for a generated file.
#[derive(Debug, Clone)]
pub struct BindingFile {
    /// POSIX-style path relative to the repository root (e.g. `.codex/agents/foo-maker.toml`).
    pub rel_path: String,
    /// Exact byte content the file must contain.
    pub content: String,
}

/// The canonical (path, content) pairs the parity guard compares the working
/// tree against.
///
/// Currently empty: the Amazon Q bridge this used to describe was deleted with
/// its harness, and the Codex emitter that replaces it lands in Phase 5 of the
/// `update-harness-support` plan, which is what fills this vector. Until then
/// the byte-parity guard has nothing static to compare, and the mirror trees are
/// covered by the sync validators instead.
///
/// # Errors
///
/// Returns an error when the repository configuration cannot be read. Reserved
/// for the Phase 5 implementation; the present body cannot fail.
pub fn expected_bindings(_repo_root: &Path) -> Result<Vec<BindingFile>, String> {
    Ok(Vec::new())
}

/// Validates all 3 supported harnesses:
/// - Static binding files: byte-for-byte parity with `expected_bindings(repo_root)`
/// - `OpenCode` mirror: `.opencode/agents/` mirrors `.claude/agents/` (via `validate_sync`)
/// - Catalog coverage: every present binding dir referenced in the platform-bindings doc
/// - No-Codex-agents-dir: `.codex/agents/` must not exist (Codex reads AGENTS.md natively)
/// - Color/tier translation maps: every `color:` and `model:` value in `.claude/agents/*.md`
///   resolves in the governance docs (ported from `validate-cross-vendor-parity.sh` §5a/5b)
#[must_use]
pub fn validate_bindings(repo_root: &Path) -> ValidationResult {
    let start = Instant::now();
    let mut result = ValidationResult::default();

    // Static binding files (byte-parity against their canonical content).
    match expected_bindings(repo_root) {
        Ok(bindings) => {
            for binding in &bindings {
                result.tally(validate_binding_file(repo_root, binding));
            }
        }
        Err(error) => result.tally(ValidationCheck::failed_msg(
            "Static binding configuration",
            error,
        )),
    }

    // OpenCode agent mirror parity (.claude/ ↔ .opencode/)
    let sync_result = validate_sync(repo_root);
    for check in sync_result.checks {
        result.tally(check);
    }

    // Catalog coverage for every present known binding dir / file
    for dir in KNOWN_BINDING_DIRS {
        result.tally(validate_catalog_coverage(repo_root, dir));
    }

    result.tally(validate_no_codex_agents_dir(repo_root));

    // Color/tier translation-map coverage (absorbed from validate-cross-vendor-parity.sh §5a/5b)
    for check in validate_color_tier_maps(repo_root) {
        result.tally(check);
    }

    result.duration = start.elapsed();
    result
}

/// Reads `path`'s content, plus (per the Split Pattern) the content of every
/// `.md` child in its sibling split directory (`<parent>/<stem>/*.md`), when
/// one exists. Governance docs relocate table content into split children
/// while the parent keeps only a trimmed index, so a lookup scoped to the
/// parent file alone would miss relocated tables.
fn read_with_split_children(path: &Path) -> String {
    let mut content = fs::read_to_string(path).unwrap_or_default();
    if let Some(stem) = path.file_stem().and_then(|s| s.to_str())
        && let Some(parent) = path.parent()
    {
        let split_dir = parent.join(stem);
        if let Ok(entries) = fs::read_dir(&split_dir) {
            let mut children: Vec<_> = entries
                .flatten()
                .map(|e| e.path())
                .filter(|p| p.extension().and_then(|e| e.to_str()) == Some("md"))
                .collect();
            children.sort();
            for child in children {
                if let Ok(child_content) = fs::read_to_string(&child) {
                    content.push('\n');
                    content.push_str(&child_content);
                }
            }
        }
    }
    content
}

/// Validates that every `color:` and `model:` value used in `.claude/agents/*.md`
/// resolves in the governance translation-map documents (§5a/5b of the
/// cross-vendor parity invariant).
///
/// Returns an empty vec when the agents directory does not exist (nothing to check).
#[allow(clippy::too_many_lines)]
fn validate_color_tier_maps(repo_root: &Path) -> Vec<ValidationCheck> {
    let agents_dir = repo_root.join(".claude").join("agents");
    if !agents_dir.is_dir() {
        return vec![];
    }

    let color_map_path = repo_root.join("repo-governance/development/agents/ai-agents.md");
    let tier_map_path = repo_root.join("repo-governance/development/agents/model-selection.md");

    let color_map = read_with_split_children(&color_map_path);
    let tier_map = read_with_split_children(&tier_map_path);

    let mut checks = Vec::new();
    let mut seen_colors = std::collections::BTreeSet::new();
    let mut seen_tiers = std::collections::BTreeSet::new();

    let Ok(entries) = fs::read_dir(&agents_dir) else {
        return vec![];
    };
    for entry in entries.flatten() {
        let path = entry.path();
        if path.extension().and_then(|e| e.to_str()) != Some("md") {
            continue;
        }
        let Ok(content) = fs::read_to_string(&path) else {
            continue;
        };
        for line in content.lines() {
            if let Some(color) = line.strip_prefix("color:").map(str::trim)
                && !color.is_empty()
            {
                seen_colors.insert(color.to_string());
            }
            if let Some(model) = line.strip_prefix("model:").map(str::trim)
                && !model.is_empty()
            {
                seen_tiers.insert(model.to_string());
            }
        }
    }

    // §5a: color translation map
    let opencode_direct = [
        "primary",
        "success",
        "warning",
        "secondary",
        "error",
        "info",
        "accent",
        "muted",
    ];
    for color in &seen_colors {
        if opencode_direct.contains(&color.as_str()) {
            checks.push(ValidationCheck::passed(
                format!("Color translation: {color}"),
                format!("'{color}' is a valid OpenCode theme token (no mapping needed)"),
            ));
            continue;
        }
        if color_map.contains(&format!("`{color}`")) {
            checks.push(ValidationCheck::passed(
                format!("Color translation: {color}"),
                format!("'{color}' is mapped in ai-agents.md"),
            ));
        } else {
            checks.push(ValidationCheck::failed(
                format!("Color translation: {color}"),
                "color mapped in repo-governance/development/agents/ai-agents.md",
                format!("'{color}' is NOT in the color translation table"),
                format!(
                    "Add a row for '{color}' in the Platform Binding Color Translation table in ai-agents.md"
                ),
            ));
        }
    }
    if seen_colors.is_empty() {
        checks.push(ValidationCheck::passed(
            "Color translation map",
            "No agent color values to verify (no agents or all use theme tokens)",
        ));
    }

    // §5b: capability-tier map
    for tier in &seen_tiers {
        let needle = format!("`{tier}`");
        if tier_map.contains(&needle) || tier_map.contains(&format!("model: {tier}")) {
            checks.push(ValidationCheck::passed(
                format!("Tier mapping: {tier}"),
                format!("'{tier}' is mapped in model-selection.md"),
            ));
        } else {
            checks.push(ValidationCheck::failed(
                format!("Tier mapping: {tier}"),
                "model value mapped in repo-governance/development/agents/model-selection.md",
                format!("'{tier}' is NOT in the capability-tier map"),
                format!(
                    "Add a row for '{tier}' in the capability-tier table in model-selection.md"
                ),
            ));
        }
    }
    if seen_tiers.is_empty() {
        checks.push(ValidationCheck::passed(
            "Capability-tier map",
            "No agent model values to verify (all agents use planning-grade inherit)",
        ));
    }

    checks
}

/// Check that the committed file at `binding.rel_path` has the exact expected bytes.
fn validate_binding_file(repo_root: &Path, binding: &BindingFile) -> ValidationCheck {
    let check_name = format!("Binding: {}", binding.rel_path);
    let abs = join_rel(repo_root, &binding.rel_path);

    match fs::read(&abs) {
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => ValidationCheck::failed(
            check_name,
            "file present and byte-equal to generated content",
            "file missing",
            format!(
                "{} is missing; run `rhino-cli agents emit-bindings`",
                binding.rel_path
            ),
        ),
        Err(e) => ValidationCheck::failed_msg(
            check_name,
            format!("failed to read {}: {e}", binding.rel_path),
        ),
        Ok(actual) => {
            if actual == binding.content.as_bytes() {
                ValidationCheck::passed(
                    check_name,
                    format!("{} matches generated content", binding.rel_path),
                )
            } else {
                ValidationCheck::failed(
                    check_name,
                    "byte-equal to generated content",
                    "content differs from generated bytes",
                    format!(
                        "{} drifted from canonical content; run `rhino-cli agents emit-bindings`",
                        binding.rel_path
                    ),
                )
            }
        }
    }
}

/// Check that `dir` is referenced in the platform-bindings catalog when it exists on disk.
fn validate_catalog_coverage(repo_root: &Path, dir: &str) -> ValidationCheck {
    let check_name = format!("Catalog Coverage: {dir}");
    let dir_path = repo_root.join(strip_leading_slash(dir));

    if !dir_path.exists() {
        return ValidationCheck::passed(
            check_name,
            format!("{dir} absent on disk; no catalog row required"),
        );
    }

    let catalog_path = join_rel(repo_root, PLATFORM_BINDINGS_CATALOG);
    let catalog = match fs::read_to_string(&catalog_path) {
        Ok(c) => c,
        Err(e) => {
            return ValidationCheck::failed_msg(
                check_name,
                format!("failed to read {PLATFORM_BINDINGS_CATALOG}: {e}"),
            );
        }
    };

    if catalog.contains(dir) {
        ValidationCheck::passed(
            check_name,
            format!("{dir} referenced in {PLATFORM_BINDINGS_CATALOG}"),
        )
    } else {
        ValidationCheck::failed(
            check_name,
            format!("{dir} referenced in {PLATFORM_BINDINGS_CATALOG}"),
            format!("{dir} present on disk but absent from catalog"),
            format!(
                "binding dir {dir} exists but is not referenced in {PLATFORM_BINDINGS_CATALOG}; add a catalog row"
            ),
        )
    }
}

/// Check that the non-standard `.codex/agents/` directory does not exist.
/// Codex CLI configures agents via `agents.<name>` sub-tables in
/// `.codex/config.toml`, not via a directory of agent files.
fn validate_no_codex_agents_dir(repo_root: &Path) -> ValidationCheck {
    let check_name = "No Codex Agents Dir: .codex/agents".to_string();
    let dir_path = join_rel(repo_root, ".codex/agents");

    if dir_path.exists() {
        ValidationCheck::failed(
            check_name,
            ".codex/agents absent",
            ".codex/agents present on disk",
            ".codex/agents/ is not an official Codex CLI convention; define agents as \
             `agents.<name>` sub-tables in .codex/config.toml and delete the directory"
                .to_string(),
        )
    } else {
        ValidationCheck::passed(
            check_name,
            ".codex/agents absent; Codex CLI agents configured via config.toml sub-tables"
                .to_string(),
        )
    }
}

/// Joins a POSIX-style relative path onto the repo root for the host FS.
fn join_rel(repo_root: &Path, rel: &str) -> PathBuf {
    let mut path = repo_root.to_path_buf();
    for segment in rel.split('/') {
        if !segment.is_empty() {
            path.push(segment);
        }
    }
    path
}

/// Strip a leading `/` from `s` if present, to allow safe `Path::join`.
fn strip_leading_slash(s: &str) -> &str {
    s.strip_prefix('/').unwrap_or(s)
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use tempfile::tempdir;

    fn write(path: &Path, content: &str) {
        if let Some(p) = path.parent() {
            std::fs::create_dir_all(p).unwrap();
        }
        std::fs::write(path, content).unwrap();
    }

    /// The smallest registry a fixture repo needs: a source tier plus the two
    /// generated mirrors, matching the shape production carries.
    fn write_three_harness_config(root: &Path) {
        write(
            &root.join("repo-config.yml"),
            concat!(
                "harness:\n",
                "  - { name: claude-code, tier: source, agent-dir: .claude/agents }\n",
                "  - name: opencode\n",
                "    tier: generated\n",
                "    agent-dir: .opencode/agents\n",
                "    mirrors: .claude/agents\n",
                "  - name: codex\n",
                "    tier: generated\n",
                "    agent-dir: .codex/agents\n",
                "    mirrors: .claude/agents\n",
                "coverage:\n  projects: []\n",
            ),
        );
    }

    /// Materializes the mirror pair every sync check expects to find.
    fn write_empty_mirror_pair(root: &Path) {
        std::fs::create_dir_all(root.join(".claude/agents")).unwrap();
        std::fs::create_dir_all(root.join(".opencode/agents")).unwrap();
    }

    /// A catalog body that references every known binding dir, so coverage
    /// passes for whichever dirs the test materializes.
    fn full_catalog() -> String {
        use std::fmt::Write as _;
        let mut s = String::from("# Platform Bindings\n\n");
        for dir in KNOWN_BINDING_DIRS {
            let _ = writeln!(s, "- `{dir}` row");
        }
        s
    }

    #[test]
    fn expected_bindings_is_empty_until_codex_lands() {
        // The Amazon Q bridge was deleted with its harness; Phase 5 refills this.
        let dir = tempdir().unwrap();
        let files = expected_bindings(dir.path()).expect("expected_bindings resolves");
        assert!(
            files.is_empty(),
            "no static binding file is expected yet; got: {files:#?}"
        );
    }

    #[test]
    fn validate_passes_when_catalog_covers_every_present_dir() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write_three_harness_config(root);
        write_empty_mirror_pair(root);
        std::fs::create_dir_all(root.join(".github")).unwrap();
        std::fs::create_dir_all(root.join(".codex")).unwrap();
        write(&root.join(PLATFORM_BINDINGS_CATALOG), &full_catalog());

        let result = validate_bindings(root);
        assert_eq!(result.failed_checks, 0, "result: {result:#?}");
    }

    #[test]
    fn validate_fails_when_present_dir_absent_from_catalog() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write_three_harness_config(root);
        write_empty_mirror_pair(root);
        // Materialize a known binding dir the catalog will not reference.
        std::fs::create_dir_all(root.join(".github")).unwrap();
        write(
            &root.join(PLATFORM_BINDINGS_CATALOG),
            "# Platform Bindings\n\n- `.claude` row\n- `.opencode` row\n",
        );

        let result = validate_bindings(root);
        assert!(
            result
                .checks
                .iter()
                .any(|c| c.status == "failed" && c.name == "Catalog Coverage: .github"),
            "result: {result:#?}"
        );
    }

    #[test]
    fn validate_fails_when_codex_agents_dir_exists() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write_three_harness_config(root);
        write_empty_mirror_pair(root);
        std::fs::create_dir_all(root.join(".github")).unwrap();
        std::fs::create_dir_all(root.join(".codex")).unwrap();
        write(&root.join(PLATFORM_BINDINGS_CATALOG), &full_catalog());

        // `.codex/agents/` is NOT an official Codex CLI convention (the
        // official mechanism is `agents.<name>` sub-tables in config.toml);
        // its presence must fail validation as a regression guard.
        std::fs::create_dir_all(root.join(".codex/agents")).unwrap();

        let result = validate_bindings(root);
        let failed_codex_agents_check = result.checks.iter().find(|c| {
            c.status == "failed"
                && c.message.contains("config.toml")
                && (c.message.contains("sub-table") || c.message.contains("agents.<name>"))
        });
        assert!(
            failed_codex_agents_check.is_some(),
            "expected a failed check whose advice points to config.toml \
             `agents.<name>` sub-tables when .codex/agents exists; result: {result:#?}"
        );
    }

    #[test]
    fn validate_skips_catalog_check_for_absent_dirs() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write_three_harness_config(root);
        write_empty_mirror_pair(root);
        // Catalog references .claude + .opencode (present); the rest are absent.
        write(
            &root.join(PLATFORM_BINDINGS_CATALOG),
            "# Platform Bindings\n\n- `.claude` row\n- `.opencode` row\n",
        );

        let result = validate_bindings(root);
        // .codex / .agents / .github absent → no catalog row required.
        assert_eq!(result.failed_checks, 0, "result: {result:#?}");
    }

    // ---- harness bindings validate covers every supported harness ----

    /// Asserts all 3 supported harnesses are covered by `harness bindings validate`:
    /// every surviving surface is in `KNOWN_BINDING_DIRS`, and the mirror parity
    /// checks appear in the `validate_bindings()` result via `validate_sync`.
    #[test]
    fn harness_bindings_validate_covers_all_three_harnesses() {
        // Check 1: every supported harness surface is a known binding dir.
        for surface in [".claude", ".opencode", ".codex", ".agents"] {
            assert!(
                KNOWN_BINDING_DIRS.contains(&surface),
                "supported surface {surface:?} not in KNOWN_BINDING_DIRS"
            );
        }

        // Check 2: no dropped harness surface survives.
        for dropped in [
            ".amazonq",
            ".cursor",
            ".pi",
            ".windsurf",
            ".junie",
            "GEMINI.md",
            "CONVENTIONS.md",
        ] {
            assert!(
                !KNOWN_BINDING_DIRS.contains(&dropped),
                "dropped surface {dropped:?} survives in KNOWN_BINDING_DIRS"
            );
        }

        // Check 3: validate_bindings() produces mirror-parity checks.
        let dir = tempdir().unwrap();
        let root = dir.path();
        write_three_harness_config(root);
        write_empty_mirror_pair(root);
        write(
            &root.join(PLATFORM_BINDINGS_CATALOG),
            "# Platform Bindings\n\n- `.claude` row\n- `.opencode` row\n",
        );
        let result = validate_bindings(root);
        let has_opencode_check = result.checks.iter().any(|c| {
            let n = c.name.to_lowercase();
            n.contains("opencode") || n.contains("sync") || n.contains("agent")
        });
        assert!(
            has_opencode_check,
            "validate_bindings must produce an OpenCode/sync/agent check; got: {:?}",
            result.checks.iter().map(|c| &c.name).collect::<Vec<_>>()
        );
    }

    #[test]
    fn read_with_split_children_finds_table_relocated_to_a_child_file() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write(
            &root.join("docs/ai-agents.md"),
            "# AI Agents\n\nindex only\n",
        );
        write(
            &root.join("docs/ai-agents/17-agent-color-categorization.md"),
            "| Claude Code | OpenCode |\n|---|---|\n| `purple` | secondary |\n",
        );

        let content = read_with_split_children(&root.join("docs/ai-agents.md"));

        assert!(content.contains("index only"));
        assert!(content.contains("`purple`"));
    }

    #[test]
    fn read_with_split_children_handles_missing_split_dir() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write(&root.join("docs/model-selection.md"), "no split children\n");

        let content = read_with_split_children(&root.join("docs/model-selection.md"));

        assert_eq!(content, "no split children\n");
    }

    #[test]
    fn validate_color_tier_maps_resolves_tables_relocated_to_split_children() {
        let dir = tempdir().unwrap();
        let root = dir.path();
        write(
            &root.join(".claude/agents/fixture.md"),
            "---\ncolor: purple\nmodel: opus\n---\n",
        );
        write(
            &root.join("repo-governance/development/agents/ai-agents.md"),
            "# AI Agents\n\nindex only\n",
        );
        write(
            &root.join("repo-governance/development/agents/ai-agents/17-colors.md"),
            "| Claude Code | OpenCode |\n|---|---|\n| `purple` | secondary |\n",
        );
        write(
            &root.join("repo-governance/development/agents/model-selection.md"),
            "# Model Selection\n\nindex only\n",
        );
        write(
            &root.join("repo-governance/development/agents/model-selection/13-bindings.md"),
            "Planning-grade: `opus`\n",
        );

        let checks = validate_color_tier_maps(root);

        assert!(
            checks.iter().all(|c| c.status == "passed"),
            "expected all checks to pass once split-child tables are searched; got: {checks:?}"
        );
    }
}
