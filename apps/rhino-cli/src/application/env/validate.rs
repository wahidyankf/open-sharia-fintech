//! `env validate` — code↔config drift detection for `env-contract:` surfaces.
//!
//! Three validator surfaces ship active, dispatched by [`SurfaceKind`]: `app`
//! (`.env.example` vs Rust/TypeScript/F# code reads), `terraform`
//! (`terraform.tfvars.example` vs `variable` blocks), and `ansible` (playbook
//! env lookups vs `.env.example`). The terraform/ansible validators were ported
//! from `ose-private` so the canonical source is byte-identical across repos; a
//! repo that declares no `terraform`/`ansible` surfaces simply never runs them —
//! the no-op is data-driven (declared surfaces), not a source stub.
//!
//! # ENV-VALIDATE CONFIG: the `env-contract:` section of `repo-config.yml` at the
//! repo root, parsed with `serde_norway`. Each surface entry carries `root`,
//! `kind`, `lang` (app only), and `allowlist`.

use std::collections::HashSet;
use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Context, Error};
use regex::Regex;
use serde::Deserialize;
use walkdir::WalkDir;

/// Surface kind that selects which drift validator runs for an entry.
///
/// Deserialized case-insensitively from the lowercase `kind:` value in
/// `repo-config.yml` (`app`, `terraform`, or `ansible`). Which variants a
/// repo exercises is pure data: a repo declaring only `app` surfaces never
/// runs the `IaC` validators, and a repo declaring `terraform`/`ansible`
/// surfaces runs the real validators against them — no per-repo source
/// carve-out.
#[derive(Debug, Deserialize, Clone, Copy, PartialEq, Eq)]
#[serde(rename_all = "lowercase")]
pub enum SurfaceKind {
    /// Application surface (Rust / TypeScript / F#): `.env.example` vs code reads.
    App,
    /// Terraform surface: `terraform.tfvars.example` vs `variable` blocks.
    Terraform,
    /// Ansible surface: playbook env lookups vs `.env.example`.
    Ansible,
}

/// A single env-validate surface entry from the `env-contract:` section.
#[derive(Debug, Deserialize, Clone)]
pub struct SurfaceConfig {
    /// Path relative to repo root (e.g. `apps/organiclever-be`).
    pub root: String,
    /// Surface kind selecting the validator (`app` / `terraform` / `ansible`).
    pub kind: SurfaceKind,
    /// Source language for the app validator: `"rust"`, `"typescript"`, or `"fsharp"`.
    /// Unused for `terraform` / `ansible` surfaces.
    #[serde(default)]
    pub lang: String,
    /// Keys intentionally exempt from drift detection (framework-injected, test-only, etc.).
    #[serde(default)]
    pub allowlist: Vec<String>,
}

/// Top-level `env-contract:` structure.
#[derive(Debug, Deserialize, Clone)]
pub struct Contract {
    /// Ordered list of surfaces to validate.
    pub surfaces: Vec<SurfaceConfig>,
}

/// A single drift finding produced by the validator.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Finding {
    /// Repo-relative surface root.
    pub root: PathBuf,
    /// Drift direction.
    pub drift: DriftKind,
    /// The divergent env-var key name.
    pub key: String,
}

/// Drift direction for a finding.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DriftKind {
    /// App: key present in `.env.example` but not consumed by any code in the surface.
    DeclaredButUnread,
    /// App: key consumed by code but absent from `.env.example`.
    ReadButUndeclared,
    /// Terraform: key in `terraform.tfvars.example` with no matching `variable` block.
    ExampleNotDeclared,
    /// Terraform: required variable (no `default`) missing from `terraform.tfvars.example`.
    RequiredMissingFromExample,
    /// Ansible: env lookup in a playbook not declared in `.env.example`.
    ConsumedNotDeclared,
}

impl DriftKind {
    /// Human-readable label for display.
    pub fn label(self) -> &'static str {
        match self {
            Self::DeclaredButUnread => "declared-but-unread",
            Self::ReadButUndeclared => "read-but-undeclared",
            Self::ExampleNotDeclared => "example-not-declared",
            Self::RequiredMissingFromExample => "required-missing-from-example",
            Self::ConsumedNotDeclared => "consumed-not-declared",
        }
    }
}

/// Load and parse the `env-contract:` section from `repo-config.yml` at `repo_root`.
///
/// # Errors
///
/// Returns an error when `repo-config.yml` cannot be read, is not valid YAML,
/// or the `env-contract:` section is absent.
pub fn load_contract(repo_root: &Path) -> Result<Contract, Error> {
    #[derive(Deserialize)]
    struct Wrapper {
        #[serde(rename = "env-contract")]
        env_contract: Option<Contract>,
    }

    let path = repo_root.join("repo-config.yml");
    let data = fs::read_to_string(&path)
        .with_context(|| format!("cannot read repo-config.yml at {}", path.display()))?;
    let wrapper: Wrapper = serde_norway::from_str(&data)
        .with_context(|| format!("failed to parse repo-config.yml at {}", path.display()))?;
    wrapper.env_contract.ok_or_else(|| {
        anyhow::anyhow!(
            "env-contract: section missing from repo-config.yml at {}",
            path.display()
        )
    })
}

/// Parse declared keys from a `.env.example` file.
///
/// Both active lines (`KEY=…`) and commented-out var lines (`# KEY=`) count as declared.
/// Pure annotation comments (no `KEY=` pattern) and blank lines are ignored.
///
/// # Errors
///
/// Returns an error when the file cannot be read.
pub fn parse_declared_keys(env_example: &Path) -> Result<Vec<String>, Error> {
    let content = fs::read_to_string(env_example)
        .with_context(|| format!("cannot read {}", env_example.display()))?;
    let mut keys = Vec::new();
    for line in content.lines() {
        let trimmed = line.trim();
        let effective = if let Some(rest) = trimmed.strip_prefix('#') {
            rest.trim()
        } else {
            trimmed
        };
        if effective.is_empty() {
            continue;
        }
        if let Some(eq_pos) = effective.find('=') {
            let key = effective[..eq_pos].trim();
            if is_env_var_name(key) {
                keys.push(key.to_string());
            }
        }
    }
    Ok(keys)
}

/// Returns `true` if `s` is a valid env var name (uppercase letters, digits, underscores only).
fn is_env_var_name(s: &str) -> bool {
    !s.is_empty()
        && s.chars()
            .all(|c| c.is_ascii_uppercase() || c.is_ascii_digit() || c == '_')
}

/// Scan Rust source for environment variable keys consumed by the code.
///
/// Detects:
/// - `envy`-derived struct field names in `#[derive(Deserialize)]` structs
///   (`field_name` → `FIELD_NAME`).
/// - `std::env::var("KEY")` / `env::var("KEY")` string literals.
///
/// # Panics
///
/// Panics if the internal static regexes fail to compile (compile-time invariant).
///
/// # Errors
///
/// Returns an error when a source file cannot be read.
pub fn scan_rust_reads(root: &Path) -> Result<Vec<String>, Error> {
    let mut keys: HashSet<String> = HashSet::new();

    let env_var_re =
        Regex::new(r#"(?:std::)?env::var\s*\(\s*"([A-Z][A-Z0-9_]*)"\s*\)"#).expect("static regex");
    // Only scan the envy-mapped `Config` struct — not every Deserialize struct.
    let config_struct_re = Regex::new(r"^\s*pub\s+struct\s+Config\b").expect("static regex");
    let pub_field_re = Regex::new(r"^\s+pub\s+([a-z][a-z0-9_]*)\s*:").expect("static regex");

    let src_dir = root.join("src");
    for entry in WalkDir::new(&src_dir).into_iter().flatten() {
        if entry.file_type().is_dir() {
            continue;
        }
        let path = entry.path();
        if !path
            .file_name()
            .is_some_and(|n| n.to_string_lossy().ends_with(".rs"))
        {
            continue;
        }
        let content =
            fs::read_to_string(path).with_context(|| format!("cannot read {}", path.display()))?;

        for cap in env_var_re.captures_iter(&content) {
            keys.insert(cap[1].to_string());
        }

        let mut in_config_struct = false;
        let mut brace_depth: i32 = 0;
        for line in content.lines() {
            if !in_config_struct && config_struct_re.is_match(line) {
                in_config_struct = true;
                brace_depth = 0;
            }
            if in_config_struct {
                for ch in line.chars() {
                    match ch {
                        '{' => brace_depth += 1,
                        '}' => {
                            brace_depth -= 1;
                            if brace_depth <= 0 {
                                in_config_struct = false;
                            }
                        }
                        _ => {}
                    }
                }
                if in_config_struct
                    && brace_depth > 0
                    && let Some(cap) = pub_field_re.captures(line)
                {
                    keys.insert(cap[1].to_ascii_uppercase());
                }
            }
        }
    }

    Ok(keys.into_iter().collect())
}

/// Scan TypeScript source for environment variable keys consumed by the code.
///
/// Detects:
/// - Keys declared in `createEnv` schema blocks in `env.ts` (`UPPER_CASE_KEY:` lines).
/// - `env.KEY` property accesses in any `.ts` / `.tsx` file.
///
/// # Panics
///
/// Panics if the internal static regexes fail to compile (compile-time invariant).
///
/// # Errors
///
/// Returns an error when a source file cannot be read.
pub fn scan_ts_reads(root: &Path) -> Result<Vec<String>, Error> {
    let mut keys: HashSet<String> = HashSet::new();

    let env_prop_re = Regex::new(r"\benv\.([A-Z][A-Z0-9_]+)\b").expect("static regex");
    let schema_key_re = Regex::new(r"^\s+([A-Z][A-Z0-9_]+)\s*:").expect("static regex");

    let src_dir = root.join("src");
    for entry in WalkDir::new(&src_dir).into_iter().flatten() {
        if entry.file_type().is_dir() {
            continue;
        }
        let path = entry.path();
        let name = path
            .file_name()
            .map(|n| n.to_string_lossy().into_owned())
            .unwrap_or_default();
        if !name.ends_with(".ts") && !name.ends_with(".tsx") {
            continue;
        }
        // Skip test files — they set process.env for mocking, not for production reads.
        if name.contains(".test.") || name.contains(".spec.") {
            continue;
        }
        let content =
            fs::read_to_string(path).with_context(|| format!("cannot read {}", path.display()))?;

        for cap in env_prop_re.captures_iter(&content) {
            keys.insert(cap[1].to_string());
        }

        if name == "env.ts" {
            for line in content.lines() {
                if let Some(cap) = schema_key_re.captures(line) {
                    keys.insert(cap[1].to_string());
                }
            }
        }
    }

    Ok(keys.into_iter().collect())
}

/// Scan F# source for environment variable keys consumed by the code.
///
/// Detects:
/// - `Environment.GetEnvironmentVariable("VAR_NAME")` calls
/// - `System.Environment.GetEnvironmentVariable("VAR_NAME")` calls
///
/// # Panics
///
/// Panics if the internal static regexes fail to compile (compile-time invariant).
///
/// # Errors
///
/// Returns an error when a source file cannot be read.
pub fn scan_fsharp_reads(root: &Path) -> Result<Vec<String>, Error> {
    let mut keys: HashSet<String> = HashSet::new();

    let env_var_re = Regex::new(
        r#"(?:System\.)?Environment\.GetEnvironmentVariable\s*\(\s*"([A-Z][A-Z0-9_]*)"\s*\)"#,
    )
    .expect("static regex");

    let src_dir = root.join("src");
    for entry in WalkDir::new(&src_dir).into_iter().flatten() {
        if entry.file_type().is_dir() {
            continue;
        }
        let path = entry.path();
        if !path
            .file_name()
            .is_some_and(|n| n.to_string_lossy().ends_with(".fs"))
        {
            continue;
        }
        let content =
            fs::read_to_string(path).with_context(|| format!("cannot read {}", path.display()))?;
        for cap in env_var_re.captures_iter(&content) {
            keys.insert(cap[1].to_string());
        }
    }

    Ok(keys.into_iter().collect())
}

/// Validate a single `app`-kind surface against its `.env.example`.
///
/// Returns zero or more drift findings.
///
/// # Errors
///
/// Returns an error when source files cannot be read or the lang is unsupported.
pub fn validate_app_surface(
    repo_root: &Path,
    surface: &SurfaceConfig,
) -> Result<Vec<Finding>, Error> {
    let root = repo_root.join(&surface.root);
    let env_example = root.join(".env.example");

    let declared: HashSet<String> = parse_declared_keys(&env_example)?.into_iter().collect();

    let read: HashSet<String> = match surface.lang.as_str() {
        "rust" => scan_rust_reads(&root)?.into_iter().collect(),
        "typescript" => scan_ts_reads(&root)?.into_iter().collect(),
        "fsharp" => scan_fsharp_reads(&root)?.into_iter().collect(),
        other => return Err(anyhow::anyhow!("unsupported lang: {other}")),
    };

    let allowlist: HashSet<&str> = surface.allowlist.iter().map(String::as_str).collect();

    let mut findings = Vec::new();

    for key in &declared {
        if !read.contains(key) && !allowlist.contains(key.as_str()) {
            findings.push(Finding {
                root: PathBuf::from(&surface.root),
                drift: DriftKind::DeclaredButUnread,
                key: key.clone(),
            });
        }
    }

    for key in &read {
        if !declared.contains(key) && !allowlist.contains(key.as_str()) {
            findings.push(Finding {
                root: PathBuf::from(&surface.root),
                drift: DriftKind::ReadButUndeclared,
                key: key.clone(),
            });
        }
    }

    findings.sort_by(|a, b| a.key.cmp(&b.key));
    Ok(findings)
}

/// Validate all surfaces declared in `contract`.
///
/// Dispatches on each surface's [`SurfaceKind`]: `app` surfaces run the
/// code↔`.env.example` drift scan, `terraform` and `ansible` surfaces run the
/// real `IaC` drift validators. A repo that declares no `terraform`/`ansible`
/// surfaces simply never invokes those validators — the no-op is driven by
/// data (which surfaces are declared), not by a source stub.
///
/// # Errors
///
/// Returns an error when any surface validation fails.
pub fn validate_all(repo_root: &Path, contract: &Contract) -> Result<Vec<Finding>, Error> {
    let mut all = Vec::new();
    for surface in &contract.surfaces {
        match surface.kind {
            SurfaceKind::App => all.extend(validate_app_surface(repo_root, surface)?),
            SurfaceKind::Terraform => {
                let root = repo_root.join(&surface.root);
                let result = validate_terraform(&root, &surface.allowlist)?;
                all.extend(result_to_findings(&surface.root, &result));
            }
            SurfaceKind::Ansible => {
                let root = repo_root.join(&surface.root);
                let result = validate_ansible(&root, &surface.allowlist)?;
                all.extend(result_to_findings(&surface.root, &result));
            }
        }
    }
    Ok(all)
}

/// Aggregated drift for a Terraform or Ansible surface.
///
/// Ported (with its unit-test modules) from `ose-private`'s
/// `application/env/validate.rs`. App-surface drift is reported through
/// [`Finding`]/[`DriftKind`]; this struct backs the `IaC` validators and is
/// converted into [`Finding`]s by [`result_to_findings`] for uniform reporting.
#[derive(Debug, Default)]
pub struct ValidationResult {
    /// Repo-relative or absolute surface root (for diagnostics).
    pub surface_root: String,
    /// App: keys in `.env.example` not read by code.
    pub declared_not_read: Vec<String>,
    /// App: keys read by code not in `.env.example`.
    pub read_not_declared: Vec<String>,
    /// Terraform: keys in `terraform.tfvars.example` not declared in `*.tf` variables.
    pub example_not_declared: Vec<String>,
    /// Terraform: required variables (no default) missing from `terraform.tfvars.example`.
    pub required_missing_from_example: Vec<String>,
    /// Ansible: env lookups in playbooks not declared in `.env.example`.
    pub consumed_not_declared: Vec<String>,
}

impl ValidationResult {
    /// Returns `true` when the surface has no drift of any kind.
    pub fn is_clean(&self) -> bool {
        self.declared_not_read.is_empty()
            && self.read_not_declared.is_empty()
            && self.example_not_declared.is_empty()
            && self.required_missing_from_example.is_empty()
            && self.consumed_not_declared.is_empty()
    }
}

/// Convert a Terraform/Ansible [`ValidationResult`] into [`Finding`]s rooted at
/// the repo-relative `surface_root`.
fn result_to_findings(surface_root: &str, result: &ValidationResult) -> Vec<Finding> {
    let mut findings = Vec::new();
    for key in &result.example_not_declared {
        findings.push(Finding {
            root: PathBuf::from(surface_root),
            drift: DriftKind::ExampleNotDeclared,
            key: key.clone(),
        });
    }
    for key in &result.required_missing_from_example {
        findings.push(Finding {
            root: PathBuf::from(surface_root),
            drift: DriftKind::RequiredMissingFromExample,
            key: key.clone(),
        });
    }
    for key in &result.consumed_not_declared {
        findings.push(Finding {
            root: PathBuf::from(surface_root),
            drift: DriftKind::ConsumedNotDeclared,
            key: key.clone(),
        });
    }
    findings.sort_by(|a, b| a.key.cmp(&b.key));
    findings
}

// ---------------------------------------------------------------------------
// Terraform validator (ported from ose-private)
// ---------------------------------------------------------------------------

/// Validate a Terraform surface.
///
/// Scans `*.tf` for `variable "KEY" { }` blocks (detecting `default` lines
/// inside = optional). Scans `terraform.tfvars.example` for `KEY =` lines.
///
/// # Errors
///
/// Returns an error when a `*.tf` or `terraform.tfvars.example` file cannot be read.
pub fn validate_terraform(root: &Path, allowlist: &[String]) -> Result<ValidationResult, Error> {
    let allow: HashSet<String> = allowlist.iter().cloned().collect();

    let (declared_keys, required_keys) = scan_terraform_variables(root)?;
    let example_keys = parse_tfvars_example(root)?;

    let mut example_not_declared: Vec<String> = example_keys
        .difference(&declared_keys)
        .filter(|k| !allow.contains(*k))
        .cloned()
        .collect();
    example_not_declared.sort();

    let mut required_missing_from_example: Vec<String> = required_keys
        .difference(&example_keys)
        .filter(|k| !allow.contains(*k))
        .cloned()
        .collect();
    required_missing_from_example.sort();

    Ok(ValidationResult {
        surface_root: root.to_string_lossy().into_owned(),
        example_not_declared,
        required_missing_from_example,
        ..Default::default()
    })
}

/// Returns `(all_declared, required_only)` variable names from `*.tf` files.
fn scan_terraform_variables(root: &Path) -> Result<(HashSet<String>, HashSet<String>), Error> {
    let var_re = Regex::new(r#"^\s*variable\s+"([A-Za-z_][A-Za-z0-9_]*)"\s*\{"#)
        .expect("static regex is valid");
    let default_re = Regex::new(r"^\s*default\s*=").expect("static regex is valid");

    let mut all_declared = HashSet::new();
    let mut required = HashSet::new();

    for entry in WalkDir::new(root)
        .follow_links(false)
        .into_iter()
        .filter_map(std::result::Result::ok)
        .filter(|e| e.file_type().is_file())
    {
        let path = entry.path();
        if path.extension().and_then(|e| e.to_str()) != Some("tf") {
            continue;
        }
        let text =
            fs::read_to_string(path).with_context(|| format!("reading {}", path.display()))?;
        let lines: Vec<&str> = text.lines().collect();
        let mut i = 0;
        while i < lines.len() {
            let line = lines[i];
            if let Some(cap) = var_re.captures(line) {
                let key = cap[1].to_string();
                all_declared.insert(key.clone());
                // State machine: scan inside the block for a `default =` line.
                let open = line.chars().filter(|&c| c == '{').count();
                let close = line.chars().filter(|&c| c == '}').count();
                let mut brace_depth: usize = open.saturating_sub(close);
                let mut has_default = false;
                i += 1;
                while i < lines.len() && brace_depth > 0 {
                    let inner = lines[i];
                    brace_depth = brace_depth
                        .saturating_add(inner.chars().filter(|&c| c == '{').count())
                        .saturating_sub(inner.chars().filter(|&c| c == '}').count());
                    if default_re.is_match(inner) {
                        has_default = true;
                    }
                    i += 1;
                }
                if !has_default {
                    required.insert(key);
                }
            } else {
                i += 1;
            }
        }
    }
    Ok((all_declared, required))
}

/// Parse `KEY =` names from `terraform.tfvars.example`.
fn parse_tfvars_example(root: &Path) -> Result<HashSet<String>, Error> {
    let path = root.join("terraform.tfvars.example");
    if !path.exists() {
        return Ok(HashSet::new());
    }
    let text = fs::read_to_string(&path).with_context(|| format!("reading {}", path.display()))?;
    let key_re = Regex::new(r"^([A-Za-z_][A-Za-z0-9_]*)\s*=").expect("static regex is valid");
    let keys = text
        .lines()
        .filter(|l| !l.trim().is_empty() && !l.trim().starts_with('#'))
        .filter_map(|l| key_re.captures(l).map(|c| c[1].to_string()))
        .collect();
    Ok(keys)
}

// ---------------------------------------------------------------------------
// Ansible validator (ported from ose-private)
// ---------------------------------------------------------------------------

/// Validate an Ansible surface.
///
/// Scans `playbook-*.yml` for `lookup('ansible.builtin.env', 'KEY')` and
/// `lookup('env', 'KEY')`. Parses `.env.example` allowing commented-out lines
/// (commented `# KEY=` lines count as declared).
///
/// # Errors
///
/// Returns an error when a playbook or `.env.example` file cannot be read.
pub fn validate_ansible(root: &Path, allowlist: &[String]) -> Result<ValidationResult, Error> {
    let allow: HashSet<String> = allowlist.iter().cloned().collect();

    let consumed = scan_ansible_playbooks(root)?;
    let declared = parse_env_example_with_comments(root)?;

    let mut consumed_not_declared: Vec<String> = consumed
        .difference(&declared)
        .filter(|k| !allow.contains(*k))
        .cloned()
        .collect();
    consumed_not_declared.sort();

    Ok(ValidationResult {
        surface_root: root.to_string_lossy().into_owned(),
        consumed_not_declared,
        ..Default::default()
    })
}

/// Scan `playbook-*.yml` files for env lookups.
fn scan_ansible_playbooks(root: &Path) -> Result<HashSet<String>, Error> {
    let builtin_re =
        Regex::new(r"lookup\(\s*'ansible\.builtin\.env'\s*,\s*'([A-Z_][A-Z0-9_]*)'\s*\)")
            .expect("static regex is valid");
    let short_re = Regex::new(r"lookup\(\s*'env'\s*,\s*'([A-Z_][A-Z0-9_]*)'\s*\)")
        .expect("static regex is valid");

    let mut keys = HashSet::new();

    for entry in WalkDir::new(root)
        .follow_links(false)
        .into_iter()
        .filter_map(std::result::Result::ok)
        .filter(|e| e.file_type().is_file())
    {
        let path = entry.path();
        let name = path
            .file_name()
            .and_then(|n| n.to_str())
            .unwrap_or_default();
        if !name.starts_with("playbook-") || !name.ends_with(".yml") {
            continue;
        }
        let text =
            fs::read_to_string(path).with_context(|| format!("reading {}", path.display()))?;
        for cap in builtin_re.captures_iter(&text) {
            keys.insert(cap[1].to_string());
        }
        for cap in short_re.captures_iter(&text) {
            keys.insert(cap[1].to_string());
        }
    }
    Ok(keys)
}

/// Parse `.env.example` including commented-out lines (strip a leading `#`
/// and whitespace, then apply the same `KEY=` extraction).
fn parse_env_example_with_comments(root: &Path) -> Result<HashSet<String>, Error> {
    let path = root.join(".env.example");
    if !path.exists() {
        return Ok(HashSet::new());
    }
    let text = fs::read_to_string(&path).with_context(|| format!("reading {}", path.display()))?;
    let keys = text
        .lines()
        .filter(|l| !l.trim().is_empty())
        .map(|l| {
            let stripped = l.trim();
            if stripped.starts_with('#') {
                stripped.trim_start_matches('#').trim()
            } else {
                stripped
            }
        })
        .filter(|l| l.contains('='))
        .filter_map(|l| l.split('=').next().map(str::trim).map(String::from))
        .filter(|k| !k.is_empty())
        .collect();
    Ok(keys)
}

#[cfg(test)]
#[allow(clippy::unwrap_used)]
mod tests {
    use super::*;
    use std::fs;
    use tempfile::TempDir;

    fn write(dir: &TempDir, rel: &str, content: &str) {
        let p = dir.path().join(rel);
        fs::create_dir_all(p.parent().unwrap()).unwrap();
        fs::write(p, content).unwrap();
    }

    // ── parse_declared_keys ──────────────────────────────────────────────────

    #[test]
    fn parse_active_key() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            ".env.example",
            "DATABASE_URL=postgres://localhost/db\n",
        );
        let keys = parse_declared_keys(&tmp.path().join(".env.example")).unwrap();
        assert_eq!(keys, vec!["DATABASE_URL"]);
    }

    #[test]
    fn parse_commented_optional_key() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            ".env.example",
            "# OPTIONAL | string | desc\n# MY_KEY=\n",
        );
        let keys = parse_declared_keys(&tmp.path().join(".env.example")).unwrap();
        assert_eq!(keys, vec!["MY_KEY"]);
    }

    #[test]
    fn parse_skips_pure_comment() {
        let tmp = TempDir::new().unwrap();
        write(&tmp, ".env.example", "# This is a pure comment\n");
        let keys = parse_declared_keys(&tmp.path().join(".env.example")).unwrap();
        assert!(keys.is_empty());
    }

    #[test]
    fn parse_skips_lowercase_key() {
        let tmp = TempDir::new().unwrap();
        write(&tmp, ".env.example", "not_env_var=value\n");
        let keys = parse_declared_keys(&tmp.path().join(".env.example")).unwrap();
        assert!(keys.is_empty());
    }

    // ── scan_rust_reads ──────────────────────────────────────────────────────

    #[test]
    fn scan_rust_finds_envy_struct_fields() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            "src/config.rs",
            r"use serde::Deserialize;
#[derive(Deserialize)]
pub struct Config {
    pub database_url: String,
    pub app_port: u16,
}
",
        );
        let mut keys = scan_rust_reads(tmp.path()).unwrap();
        keys.sort();
        assert_eq!(keys, vec!["APP_PORT", "DATABASE_URL"]);
    }

    #[test]
    fn scan_rust_finds_env_var_literals() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            "src/main.rs",
            r#"fn main() { let v = std::env::var("SOME_KEY").unwrap(); }
"#,
        );
        let keys = scan_rust_reads(tmp.path()).unwrap();
        assert!(
            keys.contains(&"SOME_KEY".to_string()),
            "expected SOME_KEY; got {keys:?}"
        );
    }

    // ── scan_ts_reads ────────────────────────────────────────────────────────

    #[test]
    fn scan_ts_finds_create_env_schema_keys() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            "src/env.ts",
            r#"import { createEnv } from "@t3-oss/env-nextjs";
import { z } from "zod";
export const env = createEnv({
  server: {
    MY_SERVER_KEY: z.string().optional(),
    ANOTHER_KEY: z.string(),
  },
  experimental__runtimeEnv: {},
});
"#,
        );
        let mut keys = scan_ts_reads(tmp.path()).unwrap();
        keys.sort();
        assert!(keys.contains(&"MY_SERVER_KEY".to_string()), "got {keys:?}");
        assert!(keys.contains(&"ANOTHER_KEY".to_string()), "got {keys:?}");
    }

    #[test]
    fn scan_ts_finds_env_property_accesses() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            "src/app/page.tsx",
            r#"import { env } from "@/env";
const url = env.ORGANICLEVER_BE_URL ?? "default";
"#,
        );
        let keys = scan_ts_reads(tmp.path()).unwrap();
        assert!(
            keys.contains(&"ORGANICLEVER_BE_URL".to_string()),
            "got {keys:?}"
        );
    }

    // ── scan_fsharp_reads ────────────────────────────────────────────────────

    #[test]
    fn scan_fsharp_finds_env_var_literals() {
        let dir = tempfile::tempdir().unwrap();
        let src_dir = dir.path().join("src");
        fs::create_dir_all(&src_dir).unwrap();
        fs::write(
            src_dir.join("Config.fs"),
            r#"module Config
let load () =
    let port = Environment.GetEnvironmentVariable("CRANE_BE_PORT")
    let url = System.Environment.GetEnvironmentVariable("CRANE_BE_NATS_URL")
    (port, url)
"#,
        )
        .unwrap();
        let keys = scan_fsharp_reads(dir.path()).unwrap();
        assert!(
            keys.contains(&"CRANE_BE_PORT".to_string()),
            "expected CRANE_BE_PORT; got {keys:?}"
        );
        assert!(
            keys.contains(&"CRANE_BE_NATS_URL".to_string()),
            "expected CRANE_BE_NATS_URL; got {keys:?}"
        );
    }

    // ── validate_app_surface ────────────────────────────────────────────────

    #[test]
    fn validate_matching_app_returns_no_findings() {
        let tmp = TempDir::new().unwrap();
        write(&tmp, "apps/myapp/.env.example", "MY_KEY=value\n");
        write(
            &tmp,
            "apps/myapp/src/env.ts",
            "export const env = createEnv({\n  server: {\n    MY_KEY: z.string(),\n  },\n  experimental__runtimeEnv: {},\n});\n",
        );
        let surface = SurfaceConfig {
            root: "apps/myapp".to_string(),
            kind: SurfaceKind::App,
            lang: "typescript".to_string(),
            allowlist: vec![],
        };
        let findings = validate_app_surface(tmp.path(), &surface).unwrap();
        assert!(
            findings.is_empty(),
            "expected no findings; got {findings:?}"
        );
    }

    #[test]
    fn validate_declared_but_unread_key_is_reported() {
        let tmp = TempDir::new().unwrap();
        write(&tmp, "apps/myapp/.env.example", "STALE_KEY=value\n");
        write(
            &tmp,
            "apps/myapp/src/env.ts",
            r"export const env = createEnv({ server: {}, experimental__runtimeEnv: {} });
",
        );
        let surface = SurfaceConfig {
            root: "apps/myapp".to_string(),
            kind: SurfaceKind::App,
            lang: "typescript".to_string(),
            allowlist: vec![],
        };
        let findings = validate_app_surface(tmp.path(), &surface).unwrap();
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].drift, DriftKind::DeclaredButUnread);
        assert_eq!(findings[0].key, "STALE_KEY");
    }

    #[test]
    fn validate_read_but_undeclared_key_is_reported() {
        let tmp = TempDir::new().unwrap();
        write(&tmp, "apps/myapp/.env.example", "");
        write(
            &tmp,
            "apps/myapp/src/env.ts",
            "export const env = createEnv({\n  server: {\n    NEW_KEY: z.string(),\n  },\n  experimental__runtimeEnv: {},\n});\n",
        );
        let surface = SurfaceConfig {
            root: "apps/myapp".to_string(),
            kind: SurfaceKind::App,
            lang: "typescript".to_string(),
            allowlist: vec![],
        };
        let findings = validate_app_surface(tmp.path(), &surface).unwrap();
        assert_eq!(findings.len(), 1);
        assert_eq!(findings[0].drift, DriftKind::ReadButUndeclared);
        assert_eq!(findings[0].key, "NEW_KEY");
    }

    #[test]
    fn validate_allowlisted_key_is_not_reported() {
        let tmp = TempDir::new().unwrap();
        write(&tmp, "apps/myapp/.env.example", "# PORT=3100\n");
        write(
            &tmp,
            "apps/myapp/src/env.ts",
            r"export const env = createEnv({ server: {}, experimental__runtimeEnv: {} });
",
        );
        let surface = SurfaceConfig {
            root: "apps/myapp".to_string(),
            kind: SurfaceKind::App,
            lang: "typescript".to_string(),
            allowlist: vec!["PORT".to_string()],
        };
        let findings = validate_app_surface(tmp.path(), &surface).unwrap();
        assert!(
            findings.is_empty(),
            "expected no findings; got {findings:?}"
        );
    }

    #[test]
    fn validate_rust_matching_config_returns_no_findings() {
        let tmp = TempDir::new().unwrap();
        write(
            &tmp,
            "apps/myapp/.env.example",
            "DATABASE_URL=postgres://localhost/db\nAPP_PORT=8080\n",
        );
        write(
            &tmp,
            "apps/myapp/src/config.rs",
            r"use serde::Deserialize;
#[derive(Deserialize)]
pub struct Config {
    pub database_url: String,
    pub app_port: u16,
}
",
        );
        let surface = SurfaceConfig {
            root: "apps/myapp".to_string(),
            kind: SurfaceKind::App,
            lang: "rust".to_string(),
            allowlist: vec![],
        };
        let findings = validate_app_surface(tmp.path(), &surface).unwrap();
        assert!(
            findings.is_empty(),
            "expected no findings; got {findings:?}"
        );
    }

    // ── load_contract from repo-config.yml (RED → GREEN) ─────────────────────

    #[test]
    fn load_contract_reads_env_contract_section_from_repo_config_yml() {
        let tmp = TempDir::new().unwrap();
        let yaml = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
            "env-contract:\n",
            "  surfaces:\n",
            "    - root: apps/myapp\n",
            "      kind: app\n",
            "      lang: typescript\n",
            "      allowlist: []\n",
        );
        fs::write(tmp.path().join("repo-config.yml"), yaml).unwrap();
        // NO standalone env-contract.yaml — loader must read from repo-config.yml
        let result = load_contract(tmp.path());
        assert!(
            result.is_ok(),
            "should read env-contract: from repo-config.yml without standalone file: {result:?}"
        );
        let contract = result.unwrap();
        assert_eq!(contract.surfaces.len(), 1);
        assert_eq!(contract.surfaces[0].root, "apps/myapp");
    }

    #[test]
    fn load_contract_errors_when_env_contract_section_missing_from_repo_config_yml() {
        let tmp = TempDir::new().unwrap();
        let yaml = concat!(
            "harness: []\n",
            "coverage:\n  projects: []\n",
            "specs:\n  ddd-areas: []\n  domain-areas: []\n",
        );
        fs::write(tmp.path().join("repo-config.yml"), yaml).unwrap();
        // NO standalone env-contract.yaml, NO env-contract: section in repo-config.yml
        let result = load_contract(tmp.path());
        assert!(
            result.is_err(),
            "should error when env-contract: section is absent from repo-config.yml"
        );
    }

    // ── terraform_validator (ported from ose-private) ──────────────────────────

    #[allow(clippy::unwrap_used, clippy::panic)]
    mod terraform_validator {
        use super::*;
        use tempfile::tempdir;

        #[test]
        fn terraform_validator_flags_example_not_declared() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            // tfvars.example has BOGUS but no variable "BOGUS" in *.tf
            fs::write(root.join("terraform.tfvars.example"), "BOGUS = \"x\"\n").unwrap();
            fs::write(root.join("main.tf"), "# no variables\n").unwrap();

            let result = validate_terraform(root, &[]).unwrap();
            assert!(
                result.example_not_declared.contains(&"BOGUS".to_string()),
                "expected BOGUS in example_not_declared, got {:?}",
                result.example_not_declared
            );
        }

        #[test]
        fn terraform_validator_flags_required_missing_from_example() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            fs::write(
                root.join("main.tf"),
                "variable \"REQUIRED_KEY\" {\n  description = \"required\"\n}\n",
            )
            .unwrap();
            // tfvars.example missing REQUIRED_KEY
            fs::write(root.join("terraform.tfvars.example"), "# empty\n").unwrap();

            let result = validate_terraform(root, &[]).unwrap();
            assert!(
                result
                    .required_missing_from_example
                    .contains(&"REQUIRED_KEY".to_string()),
                "expected REQUIRED_KEY in required_missing_from_example, got {:?}",
                result.required_missing_from_example
            );
        }

        #[test]
        fn terraform_validator_optional_var_not_required() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            fs::write(
                root.join("main.tf"),
                "variable \"OPTIONAL_KEY\" {\n  default = \"fallback\"\n}\n",
            )
            .unwrap();
            // tfvars.example doesn't include optional key — should be clean
            fs::write(root.join("terraform.tfvars.example"), "# empty\n").unwrap();

            let result = validate_terraform(root, &[]).unwrap();
            assert!(
                result.required_missing_from_example.is_empty(),
                "optional vars should not appear in required_missing_from_example: {:?}",
                result.required_missing_from_example
            );
        }

        #[test]
        fn terraform_validator_clean_when_matched() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            fs::write(
                root.join("main.tf"),
                "variable \"DB_URL\" {\n  description = \"db\"\n}\n",
            )
            .unwrap();
            fs::write(root.join("terraform.tfvars.example"), "DB_URL = \"x\"\n").unwrap();

            let result = validate_terraform(root, &[]).unwrap();
            assert!(result.is_clean(), "expected clean result: {result:?}");
        }
    }

    // ── ansible_validator (ported from ose-private) ────────────────────────────

    #[allow(clippy::unwrap_used, clippy::panic)]
    mod ansible_validator {
        use super::*;
        use tempfile::tempdir;

        #[test]
        fn ansible_validator_flags_consumed_not_declared() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            // playbook consumes UNDECLARED but .env.example is empty
            fs::write(
                root.join("playbook-site.yml"),
                "- name: test\n  tasks:\n    - debug: msg={{ lookup('ansible.builtin.env', 'UNDECLARED') }}\n",
            )
            .unwrap();
            fs::write(root.join(".env.example"), "# no vars\n").unwrap();

            let result = validate_ansible(root, &[]).unwrap();
            assert!(
                result
                    .consumed_not_declared
                    .contains(&"UNDECLARED".to_string()),
                "expected UNDECLARED in consumed_not_declared, got {:?}",
                result.consumed_not_declared
            );
        }

        #[test]
        fn ansible_validator_counts_commented_lines_as_declared() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            // .env.example has # OPTIONAL_KEY=xxx (commented out)
            fs::write(root.join(".env.example"), "# OPTIONAL_KEY=xxx\n").unwrap();
            fs::write(
                root.join("playbook-site.yml"),
                "- name: test\n  tasks:\n    - debug: msg={{ lookup('env', 'OPTIONAL_KEY') }}\n",
            )
            .unwrap();

            let result = validate_ansible(root, &[]).unwrap();
            assert!(
                result.consumed_not_declared.is_empty(),
                "commented-out env key should be considered declared: {:?}",
                result.consumed_not_declared
            );
        }

        #[test]
        fn ansible_validator_short_lookup_syntax() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            fs::write(root.join(".env.example"), "SHORT_KEY=val\n").unwrap();
            fs::write(
                root.join("playbook-deploy.yml"),
                "tasks:\n  - set_fact: val={{ lookup('env', 'SHORT_KEY') }}\n",
            )
            .unwrap();

            let result = validate_ansible(root, &[]).unwrap();
            assert!(
                result.is_clean(),
                "short lookup syntax should be detected: {result:?}",
            );
        }

        #[test]
        fn ansible_validator_non_playbook_files_skipped() {
            let dir = tempdir().unwrap();
            let root = dir.path();
            // vars file (not playbook-*.yml) with env lookup should not trigger
            fs::write(
                root.join("vars.yml"),
                "tasks:\n  - debug: msg={{ lookup('env', 'SKIPPED_KEY') }}\n",
            )
            .unwrap();
            fs::write(root.join(".env.example"), "# nothing\n").unwrap();

            let result = validate_ansible(root, &[]).unwrap();
            assert!(
                result.consumed_not_declared.is_empty(),
                "non-playbook files should not be scanned: {:?}",
                result.consumed_not_declared
            );
        }
    }
}
