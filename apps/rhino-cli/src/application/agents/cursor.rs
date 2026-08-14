//! Cursor platform binding converter — `.claude/agents/` → `.cursor/agents/`.
//!
//! Emits `name`, `description`, and `model` in fixed order. Deliberately omits
//! `readonly` and `is_background` per the adopt-cursor-platform-binding design.

use std::collections::HashMap;
use std::fmt::Write as FmtWrite;
use std::fs;
use std::path::Path;
use std::sync::OnceLock;

use serde_norway::Value;

use super::converter::ConversionWarning;
use super::field_policy::{FieldAction, FieldPolicy};
use super::frontmatter::extract_frontmatter;

/// Relative path of the Cursor agent directory.
pub const CURSOR_AGENT_DIR: &str = ".cursor/agents";

/// Remediation sentence shared by Cursor mirror drift checks.
pub const CURSOR_MIRROR_REMEDIATION: &str =
    "run `rhino-cli harness bindings generate` to regenerate the Cursor mirror";

/// Non-fast Composer 2.5 model ID. Full tier collapse: every Claude alias
/// (`opus`, `sonnet`, `haiku`, and omitted) maps here — never `composer-2.5-fast`.
pub const CURSOR_MODEL_ID: &str = "composer-2.5";

/// Fixed frontmatter field order emitted by `encode_cursor_agent`.
const CURSOR_EMITTED_FIELDS: &[&str] = &["name", "description", "model"];

/// Frontmatter delimiter line written by `encode_cursor_agent`.
const FRONTMATTER_DELIMITER: &str = "---";

/// Static (field, action, reason) table powering `cursor_field_policy()`.
pub const CURSOR_FIELD_POLICY_TABLE: &[(&str, FieldAction, &str)] = &[
    ("name", FieldAction::Preserve, ""),
    ("description", FieldAction::Preserve, ""),
    ("model", FieldAction::Translate, ""),
    ("color", FieldAction::DropWarn, "no cursor equivalent"),
    ("tools", FieldAction::DropWarn, "no cursor equivalent"),
    ("skills", FieldAction::DropWarn, "no cursor equivalent"),
    ("maxTurns", FieldAction::DropWarn, "no cursor equivalent"),
    (
        "disallowedTools",
        FieldAction::DropWarn,
        "no cursor equivalent",
    ),
    (
        "permissionMode",
        FieldAction::DropWarn,
        "no cursor equivalent",
    ),
    ("effort", FieldAction::DropWarn, "claude-only"),
    ("memory", FieldAction::DropWarn, "claude-only"),
    ("isolation", FieldAction::DropWarn, "claude-only"),
    ("background", FieldAction::DropWarn, "claude-only"),
    ("initialPrompt", FieldAction::DropWarn, "claude-only"),
    ("mcpServers", FieldAction::DropWarn, "no cursor equivalent"),
    ("hooks", FieldAction::DropWarn, "no cursor equivalent"),
];

/// Cursor agent emit shape: `name`, `description`, `model` only.
#[derive(Debug, Clone, Default)]
pub struct CursorAgent {
    /// Agent name (always emitted).
    pub name: String,
    /// Agent description (always emitted).
    pub description: String,
    /// Cursor model ID (always emitted).
    pub model: String,
}

/// Return the lazily-initialized Cursor field policy map.
fn cursor_field_policy() -> &'static HashMap<&'static str, FieldPolicy> {
    static M: OnceLock<HashMap<&'static str, FieldPolicy>> = OnceLock::new();
    M.get_or_init(|| {
        CURSOR_FIELD_POLICY_TABLE
            .iter()
            .map(|(k, action, reason)| {
                (
                    *k,
                    FieldPolicy {
                        action: *action,
                        reason,
                    },
                )
            })
            .collect()
    })
}

/// Converts a Claude model alias to the Cursor model ID.
///
/// Full tier collapse: `haiku`, `opus`, `sonnet`, empty, and every other alias
/// resolve to the same non-fast Composer 2.5 identifier.
// `opus`, `haiku`, and the default branch are intentionally identical — full tier collapse.
#[allow(clippy::if_same_then_else)]
pub fn convert_cursor_model(claude_model: &str) -> String {
    let _ = claude_model.trim();
    CURSOR_MODEL_ID.to_string()
}

/// Return true when `name` is a Claude agent markdown file that should be mirrored.
pub fn is_mirrorable_agent_filename(name: &str, is_dir: bool) -> bool {
    !is_dir && name.ends_with(".md") && name != "README.md"
}

/// Extract the agent name (filename stem without `.md`) from a path.
fn agent_name_from_path(p: &Path) -> String {
    let base = p
        .file_name()
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default();
    base.strip_suffix(".md").unwrap_or(&base).to_string()
}

/// Render a Claude agent file as Cursor-format bytes without writing to disk.
/// `claude_dir`/`mirror_dir` are used to rebase relative links in the body
/// exactly as `convert_cursor_agent` would (see `rebase_agent_links`).
///
/// # Errors
///
/// Returns an error string if the file cannot be read or parsed.
pub fn render_cursor_agent_bytes(
    input_path: &Path,
    claude_dir: &Path,
    mirror_dir: &Path,
) -> Result<Vec<u8>, String> {
    let (output, _warnings) =
        convert_cursor_agent_inner(input_path, None, claude_dir, mirror_dir, true)?;
    Ok(output)
}

/// Convert a single Claude agent file to Cursor format. `claude_dir` is
/// `.claude/agents/`'s path, used to rebase relative links in the body when
/// `input_path` sits under a group subdirectory that the mirror flattens away.
///
/// # Errors
///
/// Returns an error string if the file cannot be read, parsed, or written.
pub fn convert_cursor_agent(
    input_path: &Path,
    output_path: &Path,
    claude_dir: &Path,
    dry_run: bool,
) -> Result<Vec<ConversionWarning>, String> {
    let mirror_dir = output_path.parent().unwrap_or(output_path);
    let (_output, warnings) = convert_cursor_agent_inner(
        input_path,
        Some(output_path),
        claude_dir,
        mirror_dir,
        dry_run,
    )?;
    Ok(warnings)
}

/// Internal conversion entry point shared by `convert_cursor_agent` and
/// `render_cursor_agent_bytes`.
#[allow(clippy::collapsible_if)]
fn convert_cursor_agent_inner(
    input_path: &Path,
    output_path: Option<&Path>,
    claude_dir: &Path,
    mirror_dir: &Path,
    dry_run: bool,
) -> Result<(Vec<u8>, Vec<ConversionWarning>), String> {
    let content = fs::read(input_path).map_err(|e| format!("failed to read file: {e}"))?;
    let (frontmatter, body) =
        extract_frontmatter(&content).map_err(|e| format!("failed to extract frontmatter: {e}"))?;

    let frontmatter_str = String::from_utf8_lossy(&frontmatter).into_owned();
    let value: Value = serde_norway::from_str(&frontmatter_str)
        .map_err(|e| format!("failed to parse YAML: {e}"))?;

    let Value::Mapping(mapping) = value else {
        return Err("frontmatter is not a mapping".to_string());
    };

    let stem_name = agent_name_from_path(input_path);
    let mut warnings: Vec<ConversionWarning> = Vec::new();
    let mut out = CursorAgent {
        name: stem_name.clone(),
        model: convert_cursor_model(""),
        ..CursorAgent::default()
    };

    let policy_map = cursor_field_policy();

    for (k, v) in mapping {
        let Some(s) = k.as_str() else { continue };
        let key = s.to_string();
        let Some(policy) = policy_map.get(key.as_str()) else {
            warnings.push(ConversionWarning {
                agent_name: stem_name.clone(),
                field: key.clone(),
                reason: "unknown claude code field".to_string(),
            });
            continue;
        };
        match policy.action {
            FieldAction::Drop => {}
            FieldAction::DropWarn => {
                warnings.push(ConversionWarning {
                    agent_name: stem_name.clone(),
                    field: key.clone(),
                    reason: policy.reason.to_string(),
                });
            }
            FieldAction::Preserve => apply_cursor_preserve(&mut out, &key, &v),
            FieldAction::Translate => apply_cursor_translate(&mut out, &key, &v),
        }
    }

    let rebased_body =
        super::converter::rebase_agent_links(&body, input_path, claude_dir, mirror_dir);
    let output = encode_cursor_agent(&out, &rebased_body);

    if let Some(path) = output_path {
        if !dry_run {
            if let Some(parent) = path.parent() {
                fs::create_dir_all(parent)
                    .map_err(|e| format!("failed to create output directory: {e}"))?;
            }
            fs::write(path, &output).map_err(|e| format!("failed to write file: {e}"))?;
        }
    }

    Ok((output, warnings))
}

/// Apply a preserve-policy frontmatter field to the Cursor emit shape.
fn apply_cursor_preserve(out: &mut CursorAgent, key: &str, value: &Value) {
    match key {
        "name" => {
            if let Some(s) = value.as_str() {
                out.name = s.to_string();
            }
        }
        "description" => {
            if let Some(s) = value.as_str() {
                out.description = s.to_string();
            }
        }
        _ => {}
    }
}

/// Apply a translate-policy frontmatter field to the Cursor emit shape.
fn apply_cursor_translate(out: &mut CursorAgent, key: &str, value: &Value) {
    if key == "model" {
        let s = value.as_str().unwrap_or("");
        out.model = convert_cursor_model(s);
    }
}

/// Emit `CursorAgent` frontmatter plus the unchanged body.
///
/// Writes exactly three frontmatter keys in order (`name`, `description`, `model`)
/// and deliberately omits `readonly` and `is_background`.
pub fn encode_cursor_agent(agent: &CursorAgent, body: &[u8]) -> Vec<u8> {
    let mut frontmatter = String::new();
    let _ = writeln!(frontmatter, "name: {}", yaml_string(&agent.name));
    let _ = writeln!(
        frontmatter,
        "description: {}",
        yaml_string(&agent.description)
    );
    let _ = writeln!(frontmatter, "model: {}", yaml_string(&agent.model));

    debug_assert_eq!(CURSOR_EMITTED_FIELDS, &["name", "description", "model"]);

    let mut output = Vec::new();
    output.extend_from_slice(format!("{FRONTMATTER_DELIMITER}\n").as_bytes());
    output.extend_from_slice(frontmatter.as_bytes());
    output.extend_from_slice(format!("{FRONTMATTER_DELIMITER}\n").as_bytes());
    output.extend_from_slice(body);
    output
}

/// Quote a YAML scalar when special characters require it.
fn yaml_string(s: &str) -> String {
    if needs_quoting(s) {
        let escaped = s.replace('\\', "\\\\").replace('"', "\\\"");
        format!("\"{escaped}\"")
    } else {
        s.to_string()
    }
}

/// Return true when a YAML scalar must be double-quoted.
#[allow(clippy::collapsible_if, clippy::collapsible_match)]
fn needs_quoting(s: &str) -> bool {
    if s.is_empty() {
        return true;
    }
    if let Some(c) = s.chars().next() {
        if matches!(
            c,
            '-' | '?'
                | ':'
                | ','
                | '['
                | ']'
                | '{'
                | '}'
                | '#'
                | '&'
                | '*'
                | '!'
                | '|'
                | '>'
                | '\''
                | '"'
                | '%'
                | '@'
                | '`'
        ) {
            return true;
        }
    }
    if s.ends_with(' ') || s.ends_with('\t') {
        return true;
    }
    if s.contains(": ") || s.ends_with(':') {
        return true;
    }
    if s.contains(" #") {
        return true;
    }
    if s.contains('\n') {
        return true;
    }
    false
}

/// Aggregate result of converting all agents in `.claude/agents/`.
pub use super::converter::ConvertAllResult;

/// Convert every mirrorable `.md` agent in `.claude/agents/` to `.cursor/agents/`.
///
/// Sources may be ungrouped (`.claude/agents/<file>.md`) or grouped one level
/// deep (`.claude/agents/<group>/<file>.md`); either way the mirror is always
/// emitted flat at `.cursor/agents/<name>.md`, where `<name>` is the source's
/// `name` frontmatter field (FR-3.18) — Cursor's subdirectory support is
/// unconfirmed, so flattening is required just as it is for `OpenCode`.
///
/// # Errors
///
/// Returns an error if the `.claude/agents/` directory cannot be read, if a
/// discovered file's `name` frontmatter cannot be read, or if two sources
/// collide on the same `name`.
pub fn convert_all_cursor_agents(
    repo_root: &Path,
    dry_run: bool,
) -> Result<ConvertAllResult, String> {
    let claude_dir = repo_root.join(".claude").join("agents");
    let cursor_dir = repo_root.join(CURSOR_AGENT_DIR);

    let sources = super::converter::discover_agent_sources(&claude_dir)?;

    let mut result = ConvertAllResult::default();
    for (input, name) in sources {
        let filename = format!("{name}.md");
        let output = cursor_dir.join(&filename);
        if let Ok(w) = convert_cursor_agent(&input, &output, &claude_dir, dry_run) {
            result.converted += 1;
            result.warnings.extend(w);
        } else {
            result.failed += 1;
            result.failed_files.push(filename);
        }
    }

    Ok(result)
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

    #[test]
    fn cursor_model_maps_opus() {
        assert_eq!(convert_cursor_model("opus"), CURSOR_MODEL_ID);
    }

    #[test]
    fn cursor_model_maps_sonnet() {
        assert_eq!(convert_cursor_model("sonnet"), CURSOR_MODEL_ID);
    }

    #[test]
    fn cursor_model_maps_omitted() {
        assert_eq!(convert_cursor_model(""), CURSOR_MODEL_ID);
    }

    #[test]
    fn cursor_model_maps_haiku() {
        assert_eq!(convert_cursor_model("haiku"), CURSOR_MODEL_ID);
    }

    #[test]
    fn cursor_policy_preserves_name() {
        let policy = cursor_field_policy();
        assert_eq!(
            policy.get("name").map(|p| p.action),
            Some(FieldAction::Preserve)
        );
    }

    #[test]
    fn cursor_policy_drops_color_with_warning() {
        let policy = cursor_field_policy();
        assert_eq!(
            policy.get("color").map(|p| p.action),
            Some(FieldAction::DropWarn)
        );
    }

    #[test]
    fn cursor_policy_drops_tools_with_warning() {
        let policy = cursor_field_policy();
        assert_eq!(
            policy.get("tools").map(|p| p.action),
            Some(FieldAction::DropWarn)
        );
    }

    #[test]
    fn cursor_encoder_emits_single_delimiter_and_verbatim_body() {
        let agent = CursorAgent {
            name: "fixture".to_string(),
            description: "desc".to_string(),
            model: CURSOR_MODEL_ID.to_string(),
        };
        let body = b"# Heading\n\n```rust\nfn main() {}\n```\n";
        let output = encode_cursor_agent(&agent, body);
        let text = String::from_utf8(output).unwrap();
        assert!(text.starts_with("---\n"));
        assert_eq!(text.matches("\n---\n").count(), 1);
        assert!(text.ends_with(std::str::from_utf8(body).unwrap()));
        assert!(text.contains("name: fixture"));
        assert!(text.contains(&format!("model: {CURSOR_MODEL_ID}")));
    }

    #[test]
    fn convert_all_cursor_agents_ungrouped_source_unchanged() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("a.md"),
            "---\nname: a\ndescription: a\ntools: Read\nmodel: sonnet\n---\nBody A\n",
        );
        write(
            &claude.join("b.md"),
            "---\nname: b\ndescription: b\ntools: Write\nmodel: sonnet\n---\nBody B\n",
        );
        write(&claude.join("README.md"), "skip me\n");
        let r = convert_all_cursor_agents(dir.path(), false).unwrap();
        assert_eq!(r.converted, 2);
        assert_eq!(r.failed, 0);
        assert!(dir.path().join(".cursor/agents/a.md").exists());
        assert!(dir.path().join(".cursor/agents/b.md").exists());
        assert!(!dir.path().join(".cursor/agents/README.md").exists());
    }

    #[test]
    fn convert_all_cursor_agents_flattens_grouped_source() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("checkers/docs-checker.md"),
            "---\nname: docs-checker\ndescription: checks docs\ntools: Read\nmodel: sonnet\n---\nBody\n",
        );
        let r = convert_all_cursor_agents(dir.path(), false).unwrap();
        assert_eq!(r.converted, 1);
        assert_eq!(r.failed, 0);
        assert!(
            dir.path().join(".cursor/agents/docs-checker.md").exists(),
            "grouped source must mirror to a flat .cursor/agents/<name>.md path"
        );
        assert!(
            !dir.path().join(".cursor/agents/checkers").exists(),
            "the mirror must not reproduce the source's group subdirectory"
        );
        let content =
            std::fs::read_to_string(dir.path().join(".cursor/agents/docs-checker.md")).unwrap();
        assert!(content.contains("name: docs-checker"));
    }

    #[test]
    fn convert_all_cursor_agents_rebases_cross_group_agent_link_to_bare_filename() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("checkers/docs-checker.md"),
            "---\nname: docs-checker\ndescription: checks docs\ntools: Read\nmodel: sonnet\n---\nSee [docs-fixer](../fixers/docs-fixer.md).\n",
        );
        write(
            &claude.join("fixers/docs-fixer.md"),
            "---\nname: docs-fixer\ndescription: fixes docs\ntools: Read\nmodel: sonnet\n---\nBody\n",
        );
        convert_all_cursor_agents(dir.path(), false).unwrap();
        let content =
            std::fs::read_to_string(dir.path().join(".cursor/agents/docs-checker.md")).unwrap();
        assert!(
            content.contains("(docs-fixer.md)"),
            "a cross-group agent-to-agent link must become a bare same-directory link in the flat mirror: {content}"
        );
    }

    #[test]
    fn convert_all_cursor_agents_name_collision_across_groups_is_hard_error() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("group-a/dup.md"),
            "---\nname: dup\ndescription: a\ntools: Read\nmodel: sonnet\n---\nBody A\n",
        );
        write(
            &claude.join("group-b/other.md"),
            "---\nname: dup\ndescription: b\ntools: Read\nmodel: sonnet\n---\nBody B\n",
        );
        let r = convert_all_cursor_agents(dir.path(), false);
        let err =
            r.expect_err("two sources sharing a name must be a hard error, not a silent overwrite");
        assert!(
            err.contains("dup"),
            "collision error should name the colliding 'name' value: {err}"
        );
    }

    #[test]
    fn convert_all_cursor_agents_name_collision_grouped_and_ungrouped_is_hard_error() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("dup.md"),
            "---\nname: dup\ndescription: ungrouped\ntools: Read\nmodel: sonnet\n---\nBody A\n",
        );
        write(
            &claude.join("group/other.md"),
            "---\nname: dup\ndescription: grouped\ntools: Read\nmodel: sonnet\n---\nBody B\n",
        );
        let r = convert_all_cursor_agents(dir.path(), false);
        assert!(
            r.is_err(),
            "an ungrouped source colliding with a grouped source's name must also be a hard error"
        );
    }
}
