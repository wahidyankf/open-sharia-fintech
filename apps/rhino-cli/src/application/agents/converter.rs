//! Converter ported from `apps/rhino-cli/internal/agents/converter.go`.
//
// Implements:
// - OpenCodeAgent struct (emit shape with omitempty parity)
// - ConversionWarning struct
// - ConvertModel, ConvertPermission, ConvertColor
// - ConvertAgent: reads a Claude .md, writes the OpenCode equivalent
// - ConvertAllAgents: iterates .claude/agents/ and writes .opencode/agents/

use std::collections::{BTreeMap, HashMap};
use std::fmt::Write as FmtWrite;
use std::fs;
use std::path::{Component, Path, PathBuf};
use std::sync::OnceLock;

use regex::Regex;
use serde_norway::Value;

use super::field_policy::{FieldAction, FieldPolicy};
use super::frontmatter::{extract_frontmatter, parse_claude_tools};

/// Relative path of the `OpenCode` agent directory (plural `agents/`).
pub const OPENCODE_AGENT_DIR: &str = ".opencode/agents";

/// Return true when `name` is a Claude agent markdown file that should be mirrored.
///
/// Shared by every mirror emitter and by the sync validators, so one rule
/// decides what counts as a mirrorable agent file.
pub fn is_mirrorable_agent_filename(name: &str, is_dir: bool) -> bool {
    !is_dir && name.ends_with(".md") && name != "README.md"
}

/// A field that was dropped or translated during agent conversion.
#[derive(Debug, Clone)]
pub struct ConversionWarning {
    /// Name of the agent (stem of the `.md` filename).
    pub agent_name: String,
    /// YAML field key that triggered the warning.
    pub field: String,
    /// Human-readable explanation of why the field was dropped or translated.
    pub reason: String,
}

/// `OpenCode` agent emit shape matching Go's struct.
/// Field order: description, model, permission, color, steps, skills.
/// `omitempty` fields: color (empty string), steps (0), skills (empty vec).
#[derive(Debug, Clone, Default)]
pub struct OpenCodeAgent {
    /// Agent description (always emitted).
    pub description: String,
    /// `OpenCode` model ID (always emitted).
    pub model: String,
    /// Permission map: lowercase tool name → "allow" (always emitted, `{}` when empty).
    pub permission: BTreeMap<String, String>,
    /// `OpenCode` color token (omitted when empty).
    pub color: String,
    /// Max agent turns (`steps` in `OpenCode`, omitted when 0).
    pub steps: i64,
    /// Skill names (omitted when empty).
    pub skills: Vec<String>,
}

/// Static (field, action, reason) table powering `claude_agent_field_policy()`.
const FIELD_POLICY_TABLE: &[(&str, FieldAction, &str)] = &[
    ("name", FieldAction::Drop, "filename carries name"),
    ("description", FieldAction::Preserve, ""),
    ("tools", FieldAction::Translate, ""),
    ("model", FieldAction::Translate, ""),
    ("color", FieldAction::Translate, ""),
    ("skills", FieldAction::Preserve, ""),
    ("maxTurns", FieldAction::Translate, ""),
    (
        "disallowedTools",
        FieldAction::DropWarn,
        "no opencode equivalent",
    ),
    (
        "permissionMode",
        FieldAction::DropWarn,
        "use opencode permission block",
    ),
    ("effort", FieldAction::DropWarn, "claude-only"),
    ("memory", FieldAction::DropWarn, "claude-only"),
    ("isolation", FieldAction::DropWarn, "claude-only"),
    ("background", FieldAction::DropWarn, "claude-only"),
    ("initialPrompt", FieldAction::DropWarn, "claude-only"),
    (
        "mcpServers",
        FieldAction::DropWarn,
        "opencode declares mcp at config level",
    ),
    ("hooks", FieldAction::DropWarn, "no opencode equivalent"),
];

/// Return the lazily-initialized field policy map built from `FIELD_POLICY_TABLE`.
fn claude_agent_field_policy() -> &'static HashMap<&'static str, FieldPolicy> {
    static M: OnceLock<HashMap<&'static str, FieldPolicy>> = OnceLock::new();
    M.get_or_init(|| {
        FIELD_POLICY_TABLE
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

/// Return the lazily-initialized Claude-to-OpenCode color token translation map.
fn claude_to_opencode_color() -> &'static HashMap<&'static str, &'static str> {
    static M: OnceLock<HashMap<&'static str, &'static str>> = OnceLock::new();
    M.get_or_init(|| {
        let mut m = HashMap::new();
        m.insert("blue", "primary");
        m.insert("green", "success");
        m.insert("yellow", "warning");
        m.insert("purple", "secondary");
        m.insert("red", "error");
        m.insert("orange", "warning");
        m.insert("pink", "accent");
        m.insert("cyan", "info");
        m
    })
}

/// Translate a Claude named color to the corresponding `OpenCode` theme token.
/// Returns the input unchanged if it is already an `OpenCode` token or unknown.
pub fn convert_color(c: &str) -> String {
    if c.is_empty() {
        return String::new();
    }
    if let Some(mapped) = claude_to_opencode_color().get(c) {
        return (*mapped).to_string();
    }
    c.to_string()
}

/// Extract the agent name (filename stem without `.md`) from a path.
fn agent_name_from_path(p: &Path) -> String {
    let base = p
        .file_name()
        .map(|s| s.to_string_lossy().into_owned())
        .unwrap_or_default();
    base.strip_suffix(".md").unwrap_or(&base).to_string()
}

/// Lazily-compiled regex matching Markdown link targets `](...)`.
fn agent_link_re() -> &'static Regex {
    static RE: OnceLock<Regex> = OnceLock::new();
    RE.get_or_init(|| Regex::new(r"\]\(([^)]*)\)").expect("valid hardcoded regex"))
}

/// Lexically normalize `..`/`.` components without touching the filesystem.
fn normalize_lexical(path: &Path) -> PathBuf {
    let mut out = PathBuf::new();
    for component in path.components() {
        match component {
            Component::ParentDir => {
                out.pop();
            }
            Component::CurDir => {}
            other => out.push(other.as_os_str()),
        }
    }
    out
}

/// Compute `target`'s path relative to `base_dir`, given both are already
/// lexically normalized and share a common root.
fn relative_from(target: &Path, base_dir: &Path) -> PathBuf {
    let target_components: Vec<_> = target.components().collect();
    let base_components: Vec<_> = base_dir.components().collect();
    let mut common = 0;
    while common < target_components.len()
        && common < base_components.len()
        && target_components[common] == base_components[common]
    {
        common += 1;
    }
    let mut result = PathBuf::new();
    for _ in common..base_components.len() {
        result.push("..");
    }
    for component in &target_components[common..] {
        result.push(component.as_os_str());
    }
    result
}

/// Rebase every relative Markdown link in `body` so it still resolves once a
/// source file at `input_path` (which may sit one `<group>/` level under
/// `claude_dir`, per FR-3.18 grouping) is emitted flat under `mirror_dir`.
///
/// A link that resolves to another file inside `claude_dir` becomes a bare
/// same-directory link, matching the mirror's own flattening (every mirrored
/// agent lands as a sibling regardless of its source group). Every other
/// relative link is re-relativized from `mirror_dir`, since the source
/// file's effective depth may have changed. Absolute paths (`/...`), URLs,
/// and anchor-only links pass through unchanged.
pub(crate) fn rebase_agent_links(
    body: &[u8],
    input_path: &Path,
    claude_dir: &Path,
    mirror_dir: &Path,
) -> Vec<u8> {
    let Ok(text) = std::str::from_utf8(body) else {
        return body.to_vec();
    };
    let input_dir = input_path.parent().unwrap_or(input_path);

    let rebased = agent_link_re().replace_all(text, |caps: &regex::Captures<'_>| {
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
        let resolved = normalize_lexical(&input_dir.join(path_part));
        let new_path = match resolved.strip_prefix(claude_dir) {
            Ok(rel) if rel.file_name().is_some() => {
                PathBuf::from(rel.file_name().expect("checked by guard above"))
            }
            _ => relative_from(&resolved, mirror_dir),
        };
        let mut out = new_path.to_string_lossy().replace('\\', "/");
        if let Some(a) = anchor {
            out.push('#');
            out.push_str(a);
        }
        format!("]({out})")
    });

    rebased.into_owned().into_bytes()
}

/// Convert a single Claude agent file to `OpenCode` format. Returns conversion
/// warnings; writes to `output_path` unless `dry_run` is true. `claude_dir` is
/// `.claude/agents/`'s path, used to rebase relative links in the body when
/// `input_path` sits under a group subdirectory that the mirror flattens away.
///
/// # Errors
///
/// Returns an error string if the file cannot be read, if the frontmatter
/// cannot be extracted or parsed as YAML, or if writing the output file fails.
pub fn convert_agent(
    input_path: &Path,
    output_path: &Path,
    claude_dir: &Path,
    dry_run: bool,
) -> Result<Vec<ConversionWarning>, String> {
    let content = fs::read(input_path).map_err(|e| format!("failed to read file: {e}"))?;
    let (frontmatter, body) =
        extract_frontmatter(&content).map_err(|e| format!("failed to extract frontmatter: {e}"))?;

    let frontmatter_str = String::from_utf8_lossy(&frontmatter).into_owned();
    let value: Value = serde_norway::from_str(&frontmatter_str)
        .map_err(|e| format!("failed to parse YAML: {e}"))?;

    let Value::Mapping(mapping) = value else {
        return Err("frontmatter is not a mapping".to_string());
    };

    let agent_name = agent_name_from_path(input_path);
    let mut warnings: Vec<ConversionWarning> = Vec::new();
    let mut out = OpenCodeAgent::default();

    let policy_map = claude_agent_field_policy();

    for (k, v) in mapping {
        let Some(s) = k.as_str() else { continue };
        let key = s.to_string();
        let Some(policy) = policy_map.get(key.as_str()) else {
            warnings.push(ConversionWarning {
                agent_name: agent_name.clone(),
                field: key.clone(),
                reason: "unknown claude code field".to_string(),
            });
            continue;
        };
        match policy.action {
            FieldAction::Drop => {}
            FieldAction::DropWarn => {
                warnings.push(ConversionWarning {
                    agent_name: agent_name.clone(),
                    field: key.clone(),
                    reason: policy.reason.to_string(),
                });
            }
            FieldAction::Preserve => apply_preserve(&mut out, &key, &v),
            FieldAction::Translate => apply_translate(&mut out, &key, &v),
        }
    }

    let new_frontmatter = encode_opencode_agent(&out);
    let mirror_dir = output_path.parent().unwrap_or(output_path);
    let rebased_body = rebase_agent_links(&body, input_path, claude_dir, mirror_dir);

    let mut output = Vec::new();
    output.extend_from_slice(b"---\n");
    output.extend_from_slice(new_frontmatter.as_bytes());
    output.extend_from_slice(b"---\n");
    output.extend_from_slice(&rebased_body);

    if !dry_run {
        if let Some(parent) = output_path.parent() {
            fs::create_dir_all(parent)
                .map_err(|e| format!("failed to create output directory: {e}"))?;
        }
        fs::write(output_path, &output).map_err(|e| format!("failed to write file: {e}"))?;
    }

    Ok(warnings)
}

/// Copy a `Preserve`-tagged field value directly into the `OpenCode` output.
fn apply_preserve(out: &mut OpenCodeAgent, key: &str, value: &Value) {
    match key {
        "description" => {
            if let Some(s) = value.as_str() {
                out.description = s.to_string();
            }
        }
        "skills" => {
            if let Value::Sequence(seq) = value {
                out.skills = seq
                    .iter()
                    .filter_map(|v| v.as_str().map(std::string::ToString::to_string))
                    .collect();
            }
        }
        _ => {}
    }
}

/// Translate a `Translate`-tagged field and write the converted value to the `OpenCode` output.
// maxTurns may arrive as f64 from YAML; cast to i64 is safe for small whole-number turn counts.
#[allow(clippy::cast_possible_truncation)]
fn apply_translate(out: &mut OpenCodeAgent, key: &str, value: &Value) {
    match key {
        "tools" => {
            let tools = parse_claude_tools(value);
            out.permission = convert_permission(&tools);
        }
        "model" => {
            let s = value.as_str().unwrap_or("");
            out.model = convert_model(s);
        }
        "maxTurns" => {
            if let Some(n) = value.as_i64() {
                out.steps = n;
            } else if let Some(f) = value.as_f64() {
                out.steps = f as i64;
            }
        }
        "color" => {
            if let Some(s) = value.as_str() {
                out.color = convert_color(s);
            }
        }
        _ => {}
    }
}

/// Emit `OpenCodeAgent` as YAML matching Go's gopkg.in/yaml.v3 output:
/// - 2-space indent
/// - description, model, permission always emit
/// - color, steps, skills are omitempty (skip when empty/0/empty-vec)
/// - permission is a map (each entry on own line, value is the action string)
/// - skills is a sequence (each entry on own line, "- skill-name")
fn encode_opencode_agent(a: &OpenCodeAgent) -> String {
    let mut s = String::new();
    let _ = writeln!(s, "description: {}", yaml_string(&a.description));
    let _ = writeln!(s, "model: {}", yaml_string(&a.model));
    if a.permission.is_empty() {
        s.push_str("permission: {}\n");
    } else {
        s.push_str("permission:\n");
        for (k, v) in &a.permission {
            let _ = writeln!(s, "  {k}: {v}");
        }
    }
    if !a.color.is_empty() {
        let _ = writeln!(s, "color: {}", yaml_string(&a.color));
    }
    if a.steps != 0 {
        let _ = writeln!(s, "steps: {}", a.steps);
    }
    if !a.skills.is_empty() {
        s.push_str("skills:\n");
        for sk in &a.skills {
            let _ = writeln!(s, "  - {}", yaml_string(sk));
        }
    }
    s
}

/// Render a Go yaml.v3 plain scalar — bare if no special chars, otherwise
/// double-quoted. Matches Go's default behaviour for most agent string values.
fn yaml_string(s: &str) -> String {
    if needs_quoting(s) {
        let escaped = s.replace('\\', "\\\\").replace('"', "\\\"");
        format!("\"{escaped}\"")
    } else {
        s.to_string()
    }
}

/// Return true if `s` requires YAML double-quoting as a plain scalar.
#[allow(clippy::collapsible_if, clippy::collapsible_match)]
fn needs_quoting(s: &str) -> bool {
    if s.is_empty() {
        return true;
    }
    // Reserved leading indicator chars per YAML 1.2 plain-scalar rules.
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
    // Trailing whitespace forces quotation.
    if s.ends_with(' ') || s.ends_with('\t') {
        return true;
    }
    // ": " inside a value is ambiguous (mapping marker).
    if s.contains(": ") || s.ends_with(':') {
        return true;
    }
    // " #" inside a value would start a comment.
    if s.contains(" #") {
        return true;
    }
    if s.contains('\n') {
        return true;
    }
    false
}

/// Converts a Claude tools array to an `OpenCode` permission map.
/// Lower-cases each entry and maps it to `"allow"`; empty entries are dropped.
/// Tools not listed in the Claude array are omitted from the map.
pub fn convert_permission(claude_tools: &[String]) -> BTreeMap<String, String> {
    claude_tools
        .iter()
        .map(|t| t.trim().to_lowercase())
        .filter(|t| !t.is_empty())
        .map(|t| (t, "allow".to_string()))
        .collect()
}

/// Converts a Claude model alias to the corresponding `OpenCode` model ID.
///
/// All tiers (`opus`, `sonnet`/omitted, `haiku`) resolve to `zai-coding-plan/glm-5.2` via the
/// GLM Coding Plan primary provider. The `opencode-go` provider remains configured for `/models`
/// access but is not used in agent tier mapping.
#[allow(clippy::if_same_then_else)]
pub fn convert_model(claude_model: &str) -> String {
    let m = claude_model.trim();
    if m == "haiku" {
        "zai-coding-plan/glm-5.2".to_string()
    } else if m == "opus" {
        "zai-coding-plan/glm-5.2".to_string()
    } else {
        "zai-coding-plan/glm-5.2".to_string()
    }
}

/// Aggregate result of converting all agents in `.claude/agents/`.
#[derive(Debug, Clone, Default)]
pub struct ConvertAllResult {
    /// Number of agents successfully converted.
    pub converted: usize,
    /// Number of agents that failed to convert.
    pub failed: usize,
    /// Filenames of agents that failed to convert.
    pub failed_files: Vec<String>,
    /// Collected conversion warnings across all agents.
    pub warnings: Vec<ConversionWarning>,
}

/// Read only the `name` frontmatter field from an agent file, without
/// performing a full field-policy conversion.
///
/// # Errors
///
/// Returns an error if the file cannot be read, if its frontmatter cannot be
/// extracted or parsed as YAML, or if the frontmatter has no scalar `name` key.
pub fn read_agent_name(path: &Path) -> Result<String, String> {
    let content =
        fs::read(path).map_err(|e| format!("failed to read file {}: {e}", path.display()))?;
    let (frontmatter, _body) = extract_frontmatter(&content)
        .map_err(|e| format!("failed to extract frontmatter from {}: {e}", path.display()))?;

    let frontmatter_str = String::from_utf8_lossy(&frontmatter).into_owned();
    let value: Value = serde_norway::from_str(&frontmatter_str).map_err(|e| {
        format!(
            "failed to parse YAML frontmatter in {}: {e}",
            path.display()
        )
    })?;

    let Value::Mapping(mapping) = value else {
        return Err(format!(
            "frontmatter is not a mapping in {}",
            path.display()
        ));
    };

    for (k, v) in mapping {
        if k.as_str() == Some("name")
            && let Some(s) = v.as_str()
        {
            return Ok(s.to_string());
        }
    }

    Err(format!(
        "agent file {} has no scalar 'name' frontmatter field",
        path.display()
    ))
}

/// Discover mirrorable `.md` agent files under `.claude/agents/`, walking
/// files directly in the directory (ungrouped) plus one level of subdirectory
/// ("group") nesting — `.claude/agents/<group>/<file>.md`. Groups are not
/// expected to nest further, so only one level of recursion is performed.
///
/// Returns `(source_path, name)` pairs sorted by `name`, where `name` is read
/// from each file's `name` frontmatter field — never derived from the source
/// filename or path, because a grouped source must still flatten to a single
/// mirror filename (FR-3.18).
///
/// # Errors
///
/// Returns an error if `.claude/agents/` cannot be read, if any discovered
/// file's `name` frontmatter cannot be read, or if two distinct source files
/// resolve to the same `name` — a mirror-path collision that would make the
/// generated `.opencode/`/`.cursor/` mirror non-deterministic.
pub fn discover_agent_sources(claude_dir: &Path) -> Result<Vec<(PathBuf, String)>, String> {
    let mut files: Vec<PathBuf> = Vec::new();

    let entries = fs::read_dir(claude_dir)
        .map_err(|e| format!("failed to read {} directory: {e}", claude_dir.display()))?;
    for entry in entries.flatten() {
        let path = entry.path();
        let name = entry.file_name().to_string_lossy().into_owned();
        let is_dir = entry.file_type().is_ok_and(|t| t.is_dir());
        if is_dir {
            // One level of group nesting only: `.claude/agents/<group>/<file>.md`.
            // Groups are not expected to nest further, so a group's own
            // subdirectories (if any) are not walked.
            let Ok(group_entries) = fs::read_dir(&path) else {
                continue;
            };
            for group_entry in group_entries.flatten() {
                let group_name = group_entry.file_name().to_string_lossy().into_owned();
                let group_is_dir = group_entry.file_type().is_ok_and(|t| t.is_dir());
                if is_mirrorable_agent_filename(&group_name, group_is_dir) {
                    files.push(group_entry.path());
                }
            }
            continue;
        }
        if is_mirrorable_agent_filename(&name, is_dir) {
            files.push(path);
        }
    }

    let mut seen: HashMap<String, PathBuf> = HashMap::new();
    let mut named: Vec<(PathBuf, String)> = Vec::with_capacity(files.len());
    for path in files {
        let name = read_agent_name(&path)?;
        if let Some(existing) = seen.get(&name) {
            return Err(format!(
                "agent name collision: '{name}' is used by both {} and {} — flat mirror filenames must be unique",
                existing.display(),
                path.display()
            ));
        }
        seen.insert(name.clone(), path.clone());
        named.push((path, name));
    }
    named.sort_by(|a, b| a.1.cmp(&b.1));

    Ok(named)
}

/// Convert every `.md` agent in `.claude/agents/` to `OpenCode` format under `.opencode/agents/`.
///
/// Sources may be ungrouped (`.claude/agents/<file>.md`) or grouped one level
/// deep (`.claude/agents/<group>/<file>.md`); either way the mirror is always
/// emitted flat at `.opencode/agents/<name>.md`, where `<name>` is the
/// source's `name` frontmatter field (FR-3.18).
///
/// # Errors
///
/// Returns an error if the `.claude/agents/` directory cannot be read, if a
/// discovered file's `name` frontmatter cannot be read, or if two sources
/// collide on the same `name`.
pub fn convert_all_agents(repo_root: &Path, dry_run: bool) -> Result<ConvertAllResult, String> {
    let claude_dir = repo_root.join(".claude").join("agents");
    let opencode_dir = repo_root.join(OPENCODE_AGENT_DIR);

    let sources = discover_agent_sources(&claude_dir)?;

    let mut result = ConvertAllResult::default();
    for (input, name) in sources {
        let filename = format!("{name}.md");
        let output = opencode_dir.join(&filename);
        if let Ok(w) = convert_agent(&input, &output, &claude_dir, dry_run) {
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
    fn convert_color_translates_known() {
        assert_eq!(convert_color("blue"), "primary");
        assert_eq!(convert_color("green"), "success");
        assert_eq!(convert_color("yellow"), "warning");
        assert_eq!(convert_color("purple"), "secondary");
        assert_eq!(convert_color("red"), "error");
        assert_eq!(convert_color("orange"), "warning");
        assert_eq!(convert_color("pink"), "accent");
        assert_eq!(convert_color("cyan"), "info");
    }

    #[test]
    fn convert_color_passes_through_unknown() {
        assert_eq!(convert_color("primary"), "primary");
        assert_eq!(convert_color("#ff00aa"), "#ff00aa");
        assert_eq!(convert_color(""), "");
    }

    #[test]
    fn agent_name_from_path_strips_extension() {
        assert_eq!(agent_name_from_path(Path::new("/x/foo.md")), "foo");
        assert_eq!(agent_name_from_path(Path::new("/x/bar.md")), "bar");
    }

    #[test]
    fn convert_agent_writes_opencode_file() {
        let dir = tempdir().unwrap();
        let input = dir.path().join("foo.md");
        let output = dir.path().join(".opencode/agents/foo.md");
        write(
            &input,
            "---\nname: foo\ndescription: desc\ntools: Read, Write\nmodel: sonnet\ncolor: blue\nskills:\n  - my-skill\n---\nBody text\n",
        );
        let warnings = convert_agent(&input, &output, dir.path(), false).unwrap();
        assert!(warnings.is_empty());
        let content = std::fs::read_to_string(&output).unwrap();
        assert!(content.starts_with("---\n"));
        assert!(content.contains("description: desc"));
        assert!(content.contains("model: zai-coding-plan/glm-5.2"));
        assert!(content.contains("permission:"));
        assert!(content.contains("read: allow"));
        assert!(content.contains("write: allow"));
        assert!(content.contains("color: primary"));
        assert!(content.contains("- my-skill"));
        assert!(content.ends_with("Body text\n"));
    }

    #[test]
    fn convert_agent_dry_run_does_not_write() {
        let dir = tempdir().unwrap();
        let input = dir.path().join("foo.md");
        let output = dir.path().join(".opencode/agents/foo.md");
        write(
            &input,
            "---\nname: foo\ndescription: desc\ntools: Read\nmodel: sonnet\n---\nBody\n",
        );
        convert_agent(&input, &output, dir.path(), true).unwrap();
        assert!(!output.exists());
    }

    #[test]
    fn convert_agent_drops_warn_known_field() {
        let dir = tempdir().unwrap();
        let input = dir.path().join("foo.md");
        let output = dir.path().join("out.md");
        write(
            &input,
            "---\nname: foo\ndescription: d\ntools: Read\nmodel: sonnet\nmcpServers:\n  one: two\n---\nBody\n",
        );
        let warnings = convert_agent(&input, &output, dir.path(), true).unwrap();
        assert!(warnings.iter().any(|w| w.field == "mcpServers"));
    }

    #[test]
    fn convert_agent_warns_unknown_field() {
        let dir = tempdir().unwrap();
        let input = dir.path().join("foo.md");
        let output = dir.path().join("out.md");
        write(
            &input,
            "---\nname: foo\ndescription: d\ntools: Read\nmodel: sonnet\nbogus: yes\n---\nBody\n",
        );
        let warnings = convert_agent(&input, &output, dir.path(), true).unwrap();
        assert!(
            warnings
                .iter()
                .any(|w| w.field == "bogus" && w.reason == "unknown claude code field")
        );
    }

    #[test]
    fn convert_all_agents_iterates() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        std::fs::create_dir_all(&claude).unwrap();
        write(
            &claude.join("a.md"),
            "---\nname: a\ndescription: a\ntools: Read\nmodel: sonnet\n---\nBody A\n",
        );
        write(
            &claude.join("b.md"),
            "---\nname: b\ndescription: b\ntools: Write\nmodel: sonnet\n---\nBody B\n",
        );
        write(&claude.join("README.md"), "skip me\n");
        let r = convert_all_agents(dir.path(), false).unwrap();
        assert_eq!(r.converted, 2);
        assert_eq!(r.failed, 0);
        assert!(dir.path().join(".opencode/agents/a.md").exists());
        assert!(dir.path().join(".opencode/agents/b.md").exists());
        assert!(!dir.path().join(".opencode/agents/README.md").exists());
    }

    #[test]
    fn convert_all_agents_flattens_grouped_source() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("checkers/docs-checker.md"),
            "---\nname: docs-checker\ndescription: checks docs\ntools: Read\nmodel: sonnet\n---\nBody\n",
        );
        let r = convert_all_agents(dir.path(), false).unwrap();
        assert_eq!(r.converted, 1);
        assert_eq!(r.failed, 0);
        assert!(
            dir.path().join(".opencode/agents/docs-checker.md").exists(),
            "grouped source must mirror to a flat .opencode/agents/<name>.md path"
        );
        assert!(
            !dir.path().join(".opencode/agents/checkers").exists(),
            "the mirror must not reproduce the source's group subdirectory"
        );
    }

    #[test]
    fn convert_all_agents_rebases_external_link_for_grouped_source() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("checkers/docs-checker.md"),
            "---\nname: docs-checker\ndescription: checks docs\ntools: Read\nmodel: sonnet\n---\nSee [conventions](../../../repo-governance/conventions/README.md).\n",
        );
        convert_all_agents(dir.path(), false).unwrap();
        let content =
            std::fs::read_to_string(dir.path().join(".opencode/agents/docs-checker.md")).unwrap();
        assert!(
            content.contains("(../../repo-governance/conventions/README.md)"),
            "an external link from a grouped source must lose exactly one '../' level to match the flat mirror's shallower depth: {content}"
        );
    }

    #[test]
    fn convert_all_agents_rebases_cross_group_agent_link_to_bare_filename() {
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
        convert_all_agents(dir.path(), false).unwrap();
        let content =
            std::fs::read_to_string(dir.path().join(".opencode/agents/docs-checker.md")).unwrap();
        assert!(
            content.contains("(docs-fixer.md)"),
            "a cross-group agent-to-agent link must become a bare same-directory link in the flat mirror: {content}"
        );
    }

    #[test]
    fn convert_all_agents_ungrouped_source_link_is_unchanged() {
        let dir = tempdir().unwrap();
        let claude = dir.path().join(".claude/agents");
        write(
            &claude.join("docs-checker.md"),
            "---\nname: docs-checker\ndescription: checks docs\ntools: Read\nmodel: sonnet\n---\nSee [conventions](../../repo-governance/conventions/README.md).\n",
        );
        convert_all_agents(dir.path(), false).unwrap();
        let content =
            std::fs::read_to_string(dir.path().join(".opencode/agents/docs-checker.md")).unwrap();
        assert!(
            content.contains("(../../repo-governance/conventions/README.md)"),
            "an ungrouped source's links must be unaffected (mirror depth unchanged): {content}"
        );
    }

    #[test]
    fn convert_all_agents_name_collision_across_groups_is_hard_error() {
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
        let r = convert_all_agents(dir.path(), false);
        let err =
            r.expect_err("two sources sharing a name must be a hard error, not a silent overwrite");
        assert!(
            err.contains("dup"),
            "collision error should name the colliding 'name' value: {err}"
        );
    }

    #[test]
    fn convert_all_agents_name_collision_grouped_and_ungrouped_is_hard_error() {
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
        let r = convert_all_agents(dir.path(), false);
        assert!(
            r.is_err(),
            "an ungrouped source colliding with a grouped source's name must also be a hard error"
        );
    }

    #[test]
    fn convert_permission_lowercases() {
        let in_tools = vec!["Read".to_string(), "Write".to_string(), "BASH".to_string()];
        let out = convert_permission(&in_tools);
        assert_eq!(out.get("read").map(String::as_str), Some("allow"));
        assert_eq!(out.get("write").map(String::as_str), Some("allow"));
        assert_eq!(out.get("bash").map(String::as_str), Some("allow"));
    }

    #[test]
    fn convert_permission_skips_empty() {
        let in_tools = vec![String::new(), "  ".to_string(), "Read".to_string()];
        let out = convert_permission(&in_tools);
        assert_eq!(out.len(), 1);
    }

    #[test]
    fn convert_model_haiku() {
        assert_eq!(convert_model("haiku"), "zai-coding-plan/glm-5.2");
    }

    #[test]
    fn convert_model_opus() {
        assert_eq!(convert_model("opus"), "zai-coding-plan/glm-5.2");
    }

    #[test]
    fn convert_model_sonnet_and_default() {
        assert_eq!(convert_model("sonnet"), "zai-coding-plan/glm-5.2");
        assert_eq!(convert_model(""), "zai-coding-plan/glm-5.2");
        assert_eq!(convert_model("inherit"), "zai-coding-plan/glm-5.2");
    }

    #[test]
    fn convert_permission_maps_tools_to_allow() {
        let in_tools = vec!["Read".to_string(), "Write".to_string()];
        let out: BTreeMap<String, String> = convert_permission(&in_tools);
        let expected: BTreeMap<String, String> = BTreeMap::from([
            ("read".to_string(), "allow".to_string()),
            ("write".to_string(), "allow".to_string()),
        ]);
        assert_eq!(out, expected);
    }

    #[test]
    fn encode_emits_permission_block_not_tools() {
        let agent = OpenCodeAgent {
            description: "desc".to_string(),
            model: "zai-coding-plan/glm-5.2".to_string(),
            permission: convert_permission(&["Read".to_string()]),
            ..Default::default()
        };
        let yaml = encode_opencode_agent(&agent);
        assert!(
            yaml.contains("permission:\n"),
            "expected a permission: block, got:\n{yaml}"
        );
        assert!(
            yaml.contains("  read: allow\n"),
            "expected read: allow under permission, got:\n{yaml}"
        );
        assert!(
            !yaml.contains("tools:"),
            "boolean tools: map must not be emitted, got:\n{yaml}"
        );
        assert!(
            !yaml.contains("read: true"),
            "boolean tool flags must not be emitted, got:\n{yaml}"
        );
    }
}
