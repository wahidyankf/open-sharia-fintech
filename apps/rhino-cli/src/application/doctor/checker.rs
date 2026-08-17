//! Port of `apps/rhino-cli/internal/doctor/checker.go`.
//!
//! Provides version readers (parse a config file to get the required version),
//! output parsers (extract the installed version from a tool's `--version`
//! output), comparators (decide `Ok` vs `Warning`), and the top-level
//! [`check_all`] orchestrator.

#![allow(
    clippy::collapsible_if,
    clippy::collapsible_match,
    clippy::manual_split_once,
    clippy::needless_splitn,
    clippy::trim_split_whitespace
)]

use std::path::Path;
use std::process::Command;
use std::time::Instant;

#[cfg(test)]
use super::Scope;
use super::tools::ToolDef;
use super::{
    CheckOptions, CommandOutput, CommandRunner, DoctorResult, ToolCheck, ToolStatus,
    selected_tool_defs,
};

/// Strip a leading "v" from a version string.
pub(super) fn normalize_simple_version(s: &str) -> String {
    s.strip_prefix('v').unwrap_or(s).to_string()
}

/// Trim whitespace then strip leading "v".
pub(super) fn parse_trim_version(s: &str) -> String {
    normalize_simple_version(s.trim())
}

/// Return the `word_idx`-th space-separated token from the first line that
/// starts with `line_prefix` (after trimming whitespace). If `token_prefix`
/// is non-empty, it is stripped from the matched token.
pub(super) fn parse_line_word(
    output: &str,
    line_prefix: &str,
    word_idx: usize,
    token_prefix: &str,
) -> String {
    for line in output.split('\n') {
        let trimmed = line.trim();
        if trimmed.starts_with(line_prefix) {
            let parts: Vec<&str> = trimmed.split_whitespace().collect();
            if word_idx < parts.len() {
                let p = parts[word_idx];
                return p.strip_prefix(token_prefix).unwrap_or(p).to_string();
            }
        }
    }
    String::new()
}

// --- Version readers ---

/// Reads the `volta.node` version from a `package.json` file.
///
/// Returns `None` when the file is missing, malformed, or lacks a `volta.node` key.
pub(super) fn read_node_version(path: &Path) -> Option<String> {
    let data = std::fs::read(path).ok()?;
    let v: serde_json::Value = serde_json::from_slice(&data).ok()?;
    v.get("volta")?
        .get("node")?
        .as_str()
        .map(std::string::ToString::to_string)
}

/// Reads the `volta.npm` version from a `package.json` file.
///
/// Returns `None` when the file is missing, malformed, or lacks a `volta.npm` key.
pub(super) fn read_npm_version(path: &Path) -> Option<String> {
    let data = std::fs::read(path).ok()?;
    let v: serde_json::Value = serde_json::from_slice(&data).ok()?;
    v.get("volta")?
        .get("npm")?
        .as_str()
        .map(std::string::ToString::to_string)
}

/// Reads the .NET SDK version from a `global.json` file (`sdk.version`).
///
/// Returns `None` when the file is missing, malformed, or lacks `sdk.version`.
pub(super) fn read_dotnet_version(path: &Path) -> Option<String> {
    let data = std::fs::read(path).ok()?;
    let v: serde_json::Value = serde_json::from_slice(&data).ok()?;
    v.get("sdk")?
        .get("version")?
        .as_str()
        .map(std::string::ToString::to_string)
}

/// Reads the pinned `channel` from a `rust-toolchain.toml` file.
///
/// This is the exact toolchain version `cargo` builds with — distinct from a
/// `Cargo.toml` `rust-version` MSRV floor, which the installed compiler may
/// legitimately exceed. A pinned channel is not a floor: `doctor` compares
/// against it with exact equality, not `>=`.
///
/// Returns `None` when the file is missing or does not contain a `channel`
/// key in the `[toolchain]` table.
pub(super) fn read_rust_toolchain_channel(path: &Path) -> Option<String> {
    let data = std::fs::read_to_string(path).ok()?;
    for line in data.lines() {
        let t = line.trim();
        if t.starts_with("channel") {
            if let Some((_, rhs)) = t.split_once('=') {
                let mut v = rhs.trim().to_string();
                v = v.trim_matches('"').to_string();
                return Some(v);
            }
        }
    }
    None
}

/// Components every pinned Rust toolchain must declare so lint gates can run.
///
/// `cargo fmt` ships as the `rustfmt` component and `cargo clippy` as `clippy`;
/// neither is part of rustup's `minimal` profile.
pub(super) const REQUIRED_RUST_TOOLCHAIN_COMPONENTS: [&str; 2] = ["rustfmt", "clippy"];

/// Enumerates repo-relative `rust-toolchain.toml` paths, workspace root first.
///
/// Only the workspace root and the immediate `apps/*` and `libs/*` project
/// directories are scanned; `rust-toolchain.toml` files nested any deeper
/// (vendored copies under `target/`, `node_modules/`, or a local cargo home)
/// are deliberately out of scope.
pub(super) fn rust_toolchain_manifests(repo_root: &Path) -> Vec<String> {
    const FILE_NAME: &str = "rust-toolchain.toml";
    let mut found = Vec::new();
    if repo_root.join(FILE_NAME).is_file() {
        found.push(FILE_NAME.to_string());
    }
    for parent in ["apps", "libs"] {
        let Ok(entries) = std::fs::read_dir(repo_root.join(parent)) else {
            continue;
        };
        let mut in_parent: Vec<String> = entries
            .flatten()
            .filter(|entry| entry.path().join(FILE_NAME).is_file())
            .filter_map(|entry| entry.file_name().into_string().ok())
            .map(|project| format!("{parent}/{project}/{FILE_NAME}"))
            .collect();
        in_parent.sort();
        found.extend(in_parent);
    }
    found
}

/// Strips a trailing `#` comment from one line, if the line is not entirely
/// a comment.
///
/// This file class never puts `#` inside a component name, so an unquoted,
/// position-based strip is sufficient — no TOML string-literal awareness is
/// needed. A line that is a comment in its entirety (e.g. a commented-out
/// decoy key) collapses to an empty string, which never satisfies the
/// key-equality check in [`read_rust_toolchain_components`].
fn strip_trailing_comment(line: &str) -> &str {
    match line.find('#') {
        Some(index) => &line[..index],
        None => line,
    }
}

/// Splits a comma-separated array segment into trimmed, unquoted entries.
///
/// Recognizes both TOML basic strings (`"clippy"`) and literal strings
/// (`'clippy'`), and drops empty segments produced by a trailing comma.
fn parse_component_entries(segment: &str) -> Vec<String> {
    segment
        .split(',')
        .map(str::trim)
        .filter(|entry| !entry.is_empty())
        .map(|entry| entry.trim_matches('"').trim_matches('\'').to_string())
        .filter(|entry| !entry.is_empty())
        .collect()
}

/// Extracts the `components` array declared under `[toolchain]` in a
/// `rust-toolchain.toml` body.
///
/// Line-anchored, unlike a raw substring search: a line opens the array only
/// when its non-comment key (the text before an unquoted `=`) is exactly
/// `components` — a commented-out decoy (`# components = [...]`) or an
/// unrelated key that merely contains the substring (`excluded_components =
/// [...]`) is never accepted, because neither line's key trims to exactly
/// `components`. Once opened, the array may continue across multiple lines;
/// each line has its trailing `# comment` stripped before entries are split,
/// and each entry is trimmed of both `"..."` (basic) and `'...'` (literal)
/// TOML string quoting.
///
/// Returns an empty vector when the file declares no `components` key.
pub(super) fn read_rust_toolchain_components(contents: &str) -> Vec<String> {
    let mut in_array = false;
    let mut components = Vec::new();
    for raw_line in contents.lines() {
        let line = strip_trailing_comment(raw_line);
        if !in_array {
            let trimmed = line.trim();
            let Some((key, rhs)) = trimmed.split_once('=') else {
                continue;
            };
            if key.trim() != "components" {
                continue;
            }
            let Some(after_open) = rhs.trim().strip_prefix('[') else {
                continue;
            };
            in_array = true;
            if let Some((body, _rest)) = after_open.split_once(']') {
                components.extend(parse_component_entries(body));
                break;
            }
            components.extend(parse_component_entries(after_open));
            continue;
        }
        if let Some((body, _rest)) = line.split_once(']') {
            components.extend(parse_component_entries(body));
            break;
        }
        components.extend(parse_component_entries(line));
    }
    components
}

/// Builds one [`ToolCheck`] per scanned `rust-toolchain.toml` that omits a
/// required lint component.
///
/// Reported as [`ToolStatus::Warning`], matching Doctor's existing severity
/// convention for a version mismatch (e.g. a stale `rustc`): a missing
/// component does not fail `rustc`/`cargo`'s own presence check, so it does
/// not fail Doctor's exit code either — see `needs_remediation`, which never
/// treats a `Warning` on this check name as actionable. A crate that pins a
/// `channel` without listing `components` relies on that exact toolchain
/// having been installed with a non-minimal profile, or on a sibling crate's
/// toolchain file having added the components first; CI pre-installs each
/// declared MSRV with `--profile minimal`, so an omission here is a latent,
/// intermittent `'cargo-fmt' is not installed for the toolchain '<channel>'`
/// failure waiting to race a parallel lint job.
pub(super) fn rust_toolchain_lint_component_checks(repo_root: &Path) -> Vec<ToolCheck> {
    let mut checks = Vec::new();
    for relative in rust_toolchain_manifests(repo_root) {
        let Ok(contents) = std::fs::read_to_string(repo_root.join(&relative)) else {
            continue;
        };
        let declared = read_rust_toolchain_components(&contents);
        let missing: Vec<&str> = REQUIRED_RUST_TOOLCHAIN_COMPONENTS
            .into_iter()
            .filter(|required| !declared.iter().any(|found| found == required))
            .collect();
        if missing.is_empty() {
            continue;
        }
        let note = format!(
            "{relative} pins a Rust toolchain but does not declare the {} component(s); \
             a lint gate running cargo fmt/clippy under that channel fails whenever rustup \
             installed it with --profile minimal",
            missing.join(", ")
        );
        checks.push(ToolCheck {
            name: "rust-toolchain-components".to_string(),
            binary: String::new(),
            status: ToolStatus::Warning,
            installed_version: declared.join(", "),
            required_version: REQUIRED_RUST_TOOLCHAIN_COMPONENTS.join(", "),
            source: relative,
            note,
        });
    }
    checks
}

// --- Parsers for tool output ---

/// Extracts the Rust version from `rustc --version` output (e.g. `"rustc 1.88.0 ..."`).
pub(super) fn parse_rust_version(out: &str) -> String {
    parse_line_word(out, "rustc ", 1, "")
}

/// Extracts the `cargo-llvm-cov` version from `cargo llvm-cov --version` output.
pub(super) fn parse_cargo_llvm_cov(out: &str) -> String {
    parse_line_word(out, "cargo-llvm-cov ", 1, "")
}

/// Extracts the .NET SDK version from `dotnet --version` output (trimmed).
pub(super) fn parse_dotnet_version(out: &str) -> String {
    out.trim().to_string()
}

/// Extracts the Docker version from `docker --version` output
/// (e.g. `"Docker version 29.2.1, build abc"` → `"29.2.1"`).
pub(super) fn parse_docker_version(out: &str) -> String {
    for line in out.split('\n') {
        let t = line.trim();
        if t.starts_with("Docker version") {
            let fields: Vec<&str> = t.split_whitespace().collect();
            if fields.len() >= 3 {
                return fields[2].trim_end_matches(',').to_string();
            }
        }
    }
    String::new()
}

/// Extracts the `shellcheck` version from `shellcheck --version` output
/// (the `version: 0.11.0` line).
pub(super) fn parse_shellcheck_version(out: &str) -> String {
    out.lines()
        .find_map(|l| l.trim().strip_prefix("version:"))
        .map(|v| v.trim().to_string())
        .unwrap_or_default()
}

/// Extracts the `hadolint` version from `hadolint --version` output
/// (e.g. `"Haskell Dockerfile Linter 2.14.0"`).
pub(super) fn parse_hadolint_version(out: &str) -> String {
    parse_line_word(out, "Haskell Dockerfile Linter", 3, "")
}

/// Extracts the `actionlint` version from `actionlint --version` output
/// (the version is the first line, e.g. `"1.7.12"`).
pub(super) fn parse_actionlint_version(out: &str) -> String {
    out.lines().next().unwrap_or("").trim().to_string()
}

/// Extracts the `jq` version from `jq --version` output
/// (e.g. `"jq-1.8.1"` → `"1.8.1"`).
pub(super) fn parse_jq_version(out: &str) -> String {
    out.trim()
        .strip_prefix("jq-")
        .unwrap_or(out.trim())
        .to_string()
}

/// Extracts the Playwright version from `npx playwright --version` output
/// (e.g. `"Version 1.58.2"`).
pub(super) fn parse_playwright_version(out: &str) -> String {
    parse_line_word(out, "Version ", 1, "")
}

/// Extracts the `clang-format` version from `clang-format --version` output.
///
/// Handles both the Xcode-bundled variant (e.g.
/// `"Apple clang-format version 17.0.0 (clang-1700.0.13.3)"`) and the
/// LLVM.org standalone variant (e.g. `"clang-format version 18.1.0"`) by
/// locating the `"version"` token on the first matching line and returning
/// the token that follows it. [`parse_line_word`] cannot be reused here
/// because it requires the line to *start with* a fixed prefix, but the
/// Xcode variant prepends `"Apple "` before `"clang-format version"`.
pub(super) fn parse_clang_format_version(out: &str) -> String {
    for line in out.split('\n') {
        let words: Vec<&str> = line.split_whitespace().collect();
        if let Some(v) = words
            .iter()
            .position(|w| *w == "version")
            .and_then(|idx| words.get(idx + 1))
        {
            return (*v).to_string();
        }
    }
    String::new()
}

// --- Comparators ---

/// Compares two version strings for exact equality (after stripping a leading `v`).
///
/// Returns `(`[`ToolStatus::Ok`]`, note)` when they match, or
/// `(`[`ToolStatus::Warning`]`, note)` on mismatch.
/// Returns `Ok` immediately when `required` is empty.
pub(super) fn compare_exact(installed: &str, required: &str) -> (ToolStatus, String) {
    if required.is_empty() {
        return (ToolStatus::Ok, "no version requirement".into());
    }
    let inst = normalize_simple_version(installed);
    let req = normalize_simple_version(required);
    if inst == req {
        (ToolStatus::Ok, format!("required: {required}"))
    } else {
        (
            ToolStatus::Warning,
            format!("required: {required}, version mismatch"),
        )
    }
}

/// Parses a semver-style string into `(major, minor, patch)` integers.
///
/// Strips a leading `v`, then splits on `.`.  Returns `None` when any
/// component fails to parse as an integer.
pub(super) fn parse_version_parts(s: &str) -> Option<(i64, i64, i64)> {
    let s = normalize_simple_version(s);
    let parts: Vec<&str> = s.splitn(3, '.').collect();
    let mut nums = [0i64; 3];
    for (i, p) in parts.iter().enumerate() {
        let n: i64 = p.parse().ok()?;
        nums[i] = n;
    }
    Some((nums[0], nums[1], nums[2]))
}

/// Checks that the installed major version is greater than or equal to the required major version.
///
/// Falls back to [`compare_exact`] when either major component cannot be
/// parsed as an integer.  Returns `Ok` immediately when `required` is empty.
pub(super) fn compare_major_gte(installed: &str, required: &str) -> (ToolStatus, String) {
    if required.is_empty() {
        return (ToolStatus::Ok, "no version requirement".into());
    }
    let inst = normalize_simple_version(installed);
    let req = normalize_simple_version(required);
    let i_major = inst.splitn(2, '.').next().unwrap_or("");
    let r_major = req.splitn(2, '.').next().unwrap_or("");
    let (i_maj, r_maj): (i64, i64) = match (i_major.parse(), r_major.parse()) {
        (Ok(a), Ok(b)) => (a, b),
        _ => return compare_exact(installed, required),
    };
    if i_maj >= r_maj {
        (
            ToolStatus::Ok,
            format!("required: \u{2265}{required} (major)"),
        )
    } else {
        (
            ToolStatus::Warning,
            format!("required: \u{2265}{required} (major), version too old"),
        )
    }
}

/// Checks that the installed version is greater than or equal to the required version
/// using full semver comparison (`major.minor.patch`).
///
/// Falls back to [`compare_exact`] when either version cannot be parsed.
/// Returns `Ok` immediately when `required` is empty.
pub(super) fn compare_gte(installed: &str, required: &str) -> (ToolStatus, String) {
    if required.is_empty() {
        return (ToolStatus::Ok, "no version requirement".into());
    }
    let i = parse_version_parts(installed);
    let r = parse_version_parts(required);
    let (Some(a), Some(b)) = (i, r) else {
        return compare_exact(installed, required);
    };
    let (i_maj, i_min, i_pat) = a;
    let (r_maj, r_min, r_pat) = b;
    if i_maj > r_maj
        || (i_maj == r_maj && i_min > r_min)
        || (i_maj == r_maj && i_min == r_min && i_pat >= r_pat)
    {
        (ToolStatus::Ok, format!("required: \u{2265}{required}"))
    } else {
        (
            ToolStatus::Warning,
            format!("required: \u{2265}{required}, version too old"),
        )
    }
}

// --- Playwright browser detection ---

/// Returns `true` when at least one Chromium Playwright browser bundle is
/// found in the platform-specific Playwright cache directory.
///
/// On macOS the cache is `~/Library/Caches/ms-playwright`; on other systems it
/// is `~/.cache/ms-playwright`.  Returns `false` when the home directory
/// cannot be determined or the cache directory does not exist.
pub(super) fn check_playwright_browsers() -> bool {
    let Some(home) = dirs_home() else {
        return false;
    };
    let cache_dir = if cfg!(target_os = "macos") {
        home.join("Library").join("Caches").join("ms-playwright")
    } else {
        home.join(".cache").join("ms-playwright")
    };
    let Ok(entries) = std::fs::read_dir(&cache_dir) else {
        return false;
    };
    for e in entries.flatten() {
        if let Some(name) = e.file_name().to_str() {
            if name.starts_with("chromium-") {
                return true;
            }
        }
    }
    false
}

/// Returns the current user's home directory from the `HOME` environment variable.
///
/// Returns `None` when `HOME` is unset or empty.
fn dirs_home() -> Option<std::path::PathBuf> {
    std::env::var_os("HOME")
        .map(std::path::PathBuf::from)
        .filter(|p| !p.as_os_str().is_empty())
}

/// Checks whether Playwright browsers are installed; ignores the version strings.
///
/// Returns `Warning` with an install hint when no Chromium bundle is found in
/// the Playwright cache.  Returns `Ok` otherwise.
pub(super) fn compare_playwright(_installed: &str, _required: &str) -> (ToolStatus, String) {
    if !check_playwright_browsers() {
        return (
            ToolStatus::Warning,
            "browsers not installed \u{2014} run: npx playwright install".into(),
        );
    }
    (ToolStatus::Ok, "no version requirement".into())
}

// --- Runner ---

/// Executes `name` with `args` and returns `(stdout, stderr, exit_code)`.
///
/// Returns `Err` when `name` is not found in `PATH` (no process is started).
///
/// # Errors
///
/// Returns `Err(String)` when the binary is absent from `PATH` or the OS
/// fails to spawn the process.
pub fn real_runner(name: &str, args: &[&str]) -> CommandOutput {
    if !binary_in_path(name) {
        return Err(format!("binary not found in PATH: {name}"));
    }
    let out = Command::new(name)
        .args(args)
        .output()
        .map_err(|e| e.to_string())?;
    let stdout = String::from_utf8_lossy(&out.stdout).into_owned();
    let stderr = String::from_utf8_lossy(&out.stderr).into_owned();
    let code = out.status.code().unwrap_or(-1);
    Ok((stdout, stderr, code))
}

/// Mirror of Go's `exec.LookPath`. Walks `$PATH` for an executable file named `name`.
///
/// When `name` contains a `/`, checks the path directly instead of walking `PATH`.
fn binary_in_path(name: &str) -> bool {
    if name.contains('/') {
        return std::fs::metadata(name).is_ok_and(|m| m.is_file());
    }
    let Some(path_var) = std::env::var_os("PATH") else {
        return false;
    };
    for dir in std::env::split_paths(&path_var) {
        let candidate = dir.join(name);
        if candidate.is_file() {
            return true;
        }
    }
    false
}

/// Executes a single [`ToolDef`] check using `runner` and returns a [`ToolCheck`].
///
/// When the runner returns `Err` (binary not found), the check is immediately
/// recorded as [`ToolStatus::Missing`] without calling any parser or comparator.
pub(super) fn run_one_def(runner: CommandRunner<'_>, def: &ToolDef) -> ToolCheck {
    let required_version = (def.read_req)();
    let args_strs: Vec<&str> = def.args.iter().map(std::string::String::as_str).collect();
    match runner(&def.binary, &args_strs) {
        Err(_) => ToolCheck {
            name: def.name.clone(),
            binary: def.binary.clone(),
            status: ToolStatus::Missing,
            installed_version: String::new(),
            required_version,
            source: def.source.clone(),
            note: "not found in PATH".into(),
        },
        Ok((stdout, stderr, _code)) => {
            let output = if def.use_stderr { &stderr } else { &stdout };
            let installed = (def.parse_ver)(output);
            let (status, note) = (def.compare)(&installed, &required_version);
            ToolCheck {
                name: def.name.clone(),
                binary: def.binary.clone(),
                status,
                installed_version: installed,
                required_version,
                source: def.source.clone(),
                note,
            }
        }
    }
}

/// Runs all tool checks described in [`CheckOptions`] and returns aggregated results.
///
/// When `opts.scope` is [`Scope::Minimal`], only the core tool set is checked.
/// An explicit selection further narrows that set; an explicit empty selection
/// checks no tools. Tools named under `repo-config.yml`'s `doctor.skip-tools`
/// are always excluded. A missing or unparsable `repo-config.yml` is treated as
/// an empty skip list, not an error.
/// The `opts.runner` field overrides the default [`real_runner`] for testing.
pub fn check_all(opts: &CheckOptions<'_>) -> DoctorResult {
    let start = Instant::now();

    let runner: CommandRunner<'_> = opts.runner.unwrap_or(&real_runner);

    let defs = selected_tool_defs(opts);

    let mut checks = Vec::with_capacity(defs.len());
    for def in &defs {
        checks.push(run_one_def(runner, def));
    }

    // Tied to the same selection/scope/skip-tools filtering as the `rust`
    // tool itself (Minimal scope and `doctor.skip-tools: [rust]` both
    // exclude it, `--tools rust` includes it alone) rather than running
    // unconditionally — this is Rust toolchain hygiene, not an independent
    // probe. Appended after every `ToolDef`-backed check, never spliced in
    // among them: `fix()` (fixer.rs) looks up `defs[i]` by the same index as
    // `checks[i]` to find install steps, so any check without a same-index
    // `ToolDef` counterpart must sit past `defs.len() - 1`. It always does:
    // `needs_remediation` returns `false` for a `Warning` whose name isn't
    // `"tofu"`, so `fix()` short-circuits to `already_ok` before ever
    // indexing into `defs` for these entries.
    if defs.iter().any(|definition| definition.name == "rust") {
        checks.extend(rust_toolchain_lint_component_checks(&opts.repo_root));
    }

    let mut ok = 0usize;
    let mut warn = 0usize;
    let mut missing = 0usize;
    for c in &checks {
        match c.status {
            ToolStatus::Ok => ok += 1,
            ToolStatus::Warning => warn += 1,
            ToolStatus::Missing => missing += 1,
        }
    }

    DoctorResult {
        checks,
        ok_count: ok,
        warn_count: warn,
        missing_count: missing,
        duration: start.elapsed(),
        scope: opts.scope,
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn compare_exact_no_req() {
        assert_eq!(compare_exact("1.0", "").0, ToolStatus::Ok);
    }

    #[test]
    fn compare_exact_match() {
        let (s, n) = compare_exact("1.2.3", "1.2.3");
        assert_eq!(s, ToolStatus::Ok);
        assert!(n.contains("required: 1.2.3"));
    }

    #[test]
    fn compare_exact_mismatch() {
        let (s, _) = compare_exact("1.2.3", "1.2.4");
        assert_eq!(s, ToolStatus::Warning);
    }

    #[test]
    fn compare_exact_strips_v() {
        let (s, _) = compare_exact("v1.2.3", "1.2.3");
        assert_eq!(s, ToolStatus::Ok);
    }

    #[test]
    fn compare_gte_higher_ok() {
        let (s, _) = compare_gte("1.25.0", "1.24.0");
        assert_eq!(s, ToolStatus::Ok);
    }

    #[test]
    fn compare_gte_equal_ok() {
        let (s, _) = compare_gte("1.24.0", "1.24.0");
        assert_eq!(s, ToolStatus::Ok);
    }

    #[test]
    fn compare_gte_lower_warn() {
        let (s, _) = compare_gte("1.22.0", "1.24.0");
        assert_eq!(s, ToolStatus::Warning);
    }

    #[test]
    fn compare_gte_falls_back_on_parse_fail() {
        let (s, _) = compare_gte("abc", "1.24.0");
        // Non-numeric installed: falls back to exact comparison → mismatch.
        assert_eq!(s, ToolStatus::Warning);
    }

    #[test]
    fn compare_major_gte_higher_ok() {
        let (s, _) = compare_major_gte("28", "27");
        assert_eq!(s, ToolStatus::Ok);
    }

    #[test]
    fn compare_major_gte_lower_warn() {
        let (s, _) = compare_major_gte("26", "27");
        assert_eq!(s, ToolStatus::Warning);
    }

    #[test]
    fn parse_line_word_match() {
        let s = parse_line_word("git version 2.42.0", "git version ", 2, "");
        assert_eq!(s, "2.42.0");
    }

    #[test]
    fn parse_line_word_strips_prefix() {
        let s = parse_line_word("OpenTofu v1.9.0", "OpenTofu ", 1, "v");
        assert_eq!(s, "1.9.0");
    }

    #[test]
    fn parse_trim_strips_v() {
        assert_eq!(parse_trim_version("  v24.11.1\n"), "24.11.1");
    }

    #[test]
    fn parse_docker_strips_comma() {
        assert_eq!(
            parse_docker_version("Docker version 29.2.1, build abc"),
            "29.2.1"
        );
    }

    #[test]
    fn parse_jq_strips_prefix() {
        assert_eq!(parse_jq_version("jq-1.8.1"), "1.8.1");
    }

    #[test]
    fn parse_playwright_word() {
        assert_eq!(parse_playwright_version("Version 1.58.2"), "1.58.2");
    }

    #[test]
    fn parse_clang_format_xcode_variant() {
        assert_eq!(
            parse_clang_format_version("Apple clang-format version 17.0.0 (clang-1700.0.13.3)"),
            "17.0.0"
        );
    }

    #[test]
    fn parse_clang_format_llvm_variant() {
        assert_eq!(
            parse_clang_format_version("clang-format version 18.1.0"),
            "18.1.0"
        );
    }

    #[test]
    fn read_node_version_reads_volta_node() {
        let dir = tempfile::tempdir().unwrap();
        let p = dir.path().join("package.json");
        std::fs::write(&p, r#"{"volta":{"node":"24.11.1","npm":"10.9.0"}}"#).unwrap();
        assert_eq!(read_node_version(&p).as_deref(), Some("24.11.1"));
        assert_eq!(read_npm_version(&p).as_deref(), Some("10.9.0"));
    }

    #[test]
    fn read_rust_toolchain_channel_from_rust_toolchain_toml() {
        let dir = tempfile::tempdir().unwrap();
        let p = dir.path().join("rust-toolchain.toml");
        std::fs::write(
            &p,
            "[toolchain]\nchannel = \"1.75.0\"\ncomponents = [\"clippy\"]\n",
        )
        .unwrap();
        assert_eq!(read_rust_toolchain_channel(&p).as_deref(), Some("1.75.0"));
    }

    #[test]
    fn read_dotnet_version_from_global_json() {
        let dir = tempfile::tempdir().unwrap();
        let p = dir.path().join("global.json");
        std::fs::write(&p, r#"{"sdk":{"version":"8.0.401"}}"#).unwrap();
        assert_eq!(read_dotnet_version(&p).as_deref(), Some("8.0.401"));
    }

    #[test]
    fn run_one_def_missing() {
        let def = ToolDef {
            name: "ghosttool".into(),
            binary: "ghosttool-binary-that-does-not-exist".into(),
            source: String::new(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: |s| s.trim().to_string(),
            compare: compare_exact,
            read_req: || String::new(),
            install_cmd: None,
        };
        let runner: CommandRunner = &|_, _| Err("not found".into());
        let c = run_one_def(runner, &def);
        assert_eq!(c.status, ToolStatus::Missing);
        assert_eq!(c.note, "not found in PATH");
    }

    #[test]
    fn run_one_def_ok_with_fake_runner() {
        let def = ToolDef {
            name: "fake".into(),
            binary: "fake".into(),
            source: String::new(),
            args: vec!["--version".into()],
            use_stderr: false,
            parse_ver: |s| s.trim().to_string(),
            compare: compare_exact,
            read_req: || "1.0.0".into(),
            install_cmd: None,
        };
        let runner: CommandRunner = &|_, _| Ok(("1.0.0\n".into(), String::new(), 0));
        let c = run_one_def(runner, &def);
        assert_eq!(c.status, ToolStatus::Ok);
        assert_eq!(c.installed_version, "1.0.0");
    }

    #[test]
    fn check_all_runs_and_aggregates() {
        let dir = tempfile::tempdir().unwrap();
        std::fs::write(dir.path().join("package.json"), "{}").unwrap();
        let runner: CommandRunner = &|name, _args| match name {
            "git" => Ok(("git version 2.42.0\n".into(), String::new(), 0)),
            "volta" => Ok(("2.0.2\n".into(), String::new(), 0)),
            _ => Err("not found".into()),
        };
        let opts = CheckOptions {
            repo_root: dir.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Minimal,
            selected_tools: None,
        };
        let r = check_all(&opts);
        assert_eq!(r.checks.len(), 6);
        assert!(r.ok_count >= 2);
        assert!(r.missing_count >= 1);
    }

    #[test]
    fn check_all_full_scope_respects_repo_config_skip_tools() {
        let dir = tempfile::tempdir().unwrap();
        std::fs::write(dir.path().join("package.json"), "{}").unwrap();
        std::fs::write(
            dir.path().join("repo-config.yml"),
            "doctor:\n  skip-tools: [shfmt, tofu, clang-format]\n",
        )
        .unwrap();
        let runner: CommandRunner = &|name, _args| match name {
            "shfmt" | "tofu" | "clang-format" => {
                panic!("skip-tools entry {name} must never be probed")
            }
            _ => Ok(("1.0.0\n".into(), String::new(), 0)),
        };
        let opts = CheckOptions {
            repo_root: dir.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Full,
            selected_tools: None,
        };
        let r = check_all(&opts);
        assert!(
            !r.checks
                .iter()
                .any(|c| ["shfmt", "tofu", "clang-format"].contains(&c.name.as_str())),
            "skip-tools entries must be excluded from checks, got: {:?}",
            r.checks.iter().map(|c| &c.name).collect::<Vec<_>>()
        );
        assert_eq!(r.checks.len(), 13, "16 known tools minus 3 skipped");
    }

    #[test]
    fn check_all_full_scope_without_repo_config_checks_every_tool() {
        // No repo-config.yml written — load_or_default() must fall back to an
        // empty skip list rather than erroring, so a repo with no `doctor:`
        // section keeps checking the full roster (today's ose-public behavior).
        let dir = tempfile::tempdir().unwrap();
        std::fs::write(dir.path().join("package.json"), "{}").unwrap();
        let runner: CommandRunner = &|_, _| Ok(("1.0.0\n".into(), String::new(), 0));
        let opts = CheckOptions {
            repo_root: dir.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Full,
            selected_tools: None,
        };
        let r = check_all(&opts);
        assert_eq!(r.checks.len(), 16, "no skip-tools configured — full roster");
    }

    #[test]
    fn explicit_empty_tool_selection_runs_zero_probes() {
        let dir = tempfile::tempdir().unwrap();
        std::fs::write(dir.path().join("package.json"), "{}").unwrap();
        let runner: CommandRunner = &|name, _| panic!("must not probe {name}");
        let opts = CheckOptions {
            repo_root: dir.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Full,
            selected_tools: Some(Vec::new()),
        };

        let result = check_all(&opts);

        assert!(result.checks.is_empty());
        assert_eq!(
            result.ok_count + result.warn_count + result.missing_count,
            0
        );
    }

    #[test]
    fn explicit_tool_selection_probes_only_the_requested_tool() {
        let dir = tempfile::tempdir().unwrap();
        std::fs::write(dir.path().join("package.json"), "{}").unwrap();
        let runner: CommandRunner = &|name, _| match name {
            "tofu" => Ok(("OpenTofu v1.12.3\n".into(), String::new(), 0)),
            _ => panic!("selection must not probe {name}"),
        };
        let opts = CheckOptions {
            repo_root: dir.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Full,
            selected_tools: Some(vec!["tofu".into()]),
        };

        let result = check_all(&opts);

        assert_eq!(result.checks.len(), 1);
        assert_eq!(result.checks[0].name, "tofu");
    }

    // --- rust-toolchain.toml lint-component checks ---
    //
    // Six inputs, matching the cases verified in the PR #31 review: A/B are
    // baseline-pass forms, C-F each reproduce a distinct parser defect a
    // substring-based extractor gets wrong (false rejection for C/D, false
    // acceptance — the more dangerous direction — for E/F).

    #[test]
    fn components_case_a_baseline_single_line() {
        let contents = "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\", \"rustfmt\", \"llvm-tools\"]\n";
        assert_eq!(
            read_rust_toolchain_components(contents),
            vec![
                "clippy".to_string(),
                "rustfmt".to_string(),
                "llvm-tools".to_string()
            ]
        );
    }

    #[test]
    fn components_case_b_multi_line_no_comments() {
        let contents = concat!(
            "[toolchain]\n",
            "channel = \"1.95.0\"\n",
            "components = [\n",
            "  \"clippy\",\n",
            "  \"rustfmt\",\n",
            "]\n",
        );
        assert_eq!(
            read_rust_toolchain_components(contents),
            vec!["clippy".to_string(), "rustfmt".to_string()],
            "the multi-line components array form must parse into its component names"
        );
    }

    #[test]
    fn components_case_c_multi_line_with_per_entry_comments() {
        let contents = concat!(
            "[toolchain]\n",
            "channel = \"1.95.0\"\n",
            "components = [\n",
            "  \"clippy\",  # linter\n",
            "  \"rustfmt\", # formatter\n",
            "]\n",
        );
        assert_eq!(
            read_rust_toolchain_components(contents),
            vec!["clippy".to_string(), "rustfmt".to_string()],
            "a per-entry trailing # comment must not corrupt the following entry"
        );
    }

    #[test]
    fn components_case_d_single_quoted_literal_strings() {
        let contents = "[toolchain]\nchannel = \"1.95.0\"\ncomponents = ['clippy', 'rustfmt']\n";
        assert_eq!(
            read_rust_toolchain_components(contents),
            vec!["clippy".to_string(), "rustfmt".to_string()],
            "TOML literal strings ('clippy') must parse the same as basic strings (\"clippy\")"
        );
    }

    #[test]
    fn components_case_e_commented_out_decoy_is_ignored() {
        let contents = concat!(
            "# components = [\"clippy\", \"rustfmt\"]\n",
            "[toolchain]\n",
            "channel = \"1.95.0\"\n",
        );
        assert_eq!(
            read_rust_toolchain_components(contents),
            Vec::<String>::new(),
            "a commented-out components line must never satisfy the check — false \
             acceptance is the more dangerous direction than false rejection here"
        );
    }

    #[test]
    fn components_case_f_unrelated_key_is_ignored() {
        let contents =
            "[toolchain]\nchannel = \"1.95.0\"\nexcluded_components = [\"clippy\", \"rustfmt\"]\n";
        assert_eq!(
            read_rust_toolchain_components(contents),
            Vec::<String>::new(),
            "a key that merely contains the substring \"components\" must not satisfy the check"
        );
    }

    #[test]
    fn rust_toolchain_manifests_covers_root_and_project_dirs() {
        let repo = tempfile::TempDir::new().unwrap();
        let body = "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\", \"rustfmt\"]\n";
        std::fs::write(repo.path().join("rust-toolchain.toml"), body).unwrap();
        for project in ["apps/rhino-cli", "libs/rust-commons"] {
            let dir = repo.path().join(project);
            std::fs::create_dir_all(&dir).unwrap();
            std::fs::write(dir.join("rust-toolchain.toml"), body).unwrap();
        }
        // A vendored copy below the scanned depth must stay out of scope.
        let vendored = repo.path().join("apps/rhino-cli/target/pkg");
        std::fs::create_dir_all(&vendored).unwrap();
        std::fs::write(vendored.join("rust-toolchain.toml"), "[toolchain]\n").unwrap();

        assert_eq!(
            rust_toolchain_manifests(repo.path()),
            vec![
                "rust-toolchain.toml".to_string(),
                "apps/rhino-cli/rust-toolchain.toml".to_string(),
                "libs/rust-commons/rust-toolchain.toml".to_string(),
            ],
            "only the workspace root and immediate apps/libs project dirs are scanned"
        );
    }

    #[test]
    fn rust_toolchain_lint_component_checks_flags_missing_components() {
        let repo = tempfile::TempDir::new().unwrap();
        let project = repo.path().join("apps").join("coralpolyp-be");
        std::fs::create_dir_all(&project).unwrap();
        std::fs::write(
            project.join("rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.95.0\"\n",
        )
        .unwrap();

        let checks = rust_toolchain_lint_component_checks(repo.path());

        assert_eq!(checks.len(), 1);
        assert_eq!(checks[0].name, "rust-toolchain-components");
        assert_eq!(checks[0].status, ToolStatus::Warning);
        assert_eq!(checks[0].source, "apps/coralpolyp-be/rust-toolchain.toml");
        assert!(checks[0].note.contains("rustfmt") && checks[0].note.contains("clippy"));
    }

    #[test]
    fn rust_toolchain_lint_component_checks_passes_when_declared() {
        let repo = tempfile::TempDir::new().unwrap();
        for project in ["apps/rhino-cli", "libs/rust-commons"] {
            let dir = repo.path().join(project);
            std::fs::create_dir_all(&dir).unwrap();
            std::fs::write(
                dir.join("rust-toolchain.toml"),
                "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\", \"rustfmt\", \"llvm-tools\"]\nprofile = \"minimal\"\n",
            )
            .unwrap();
        }

        assert!(
            rust_toolchain_lint_component_checks(repo.path()).is_empty(),
            "rust-toolchain.toml files declaring rustfmt and clippy must produce no warning"
        );
    }

    /// A `rust-toolchain.toml` declaring exactly one required component must
    /// name only the genuinely missing one — proves `missing.join(", ")`
    /// does not regress to printing the full required list regardless of
    /// what is actually declared.
    #[test]
    fn rust_toolchain_lint_component_checks_names_only_the_missing_component() {
        let repo = tempfile::TempDir::new().unwrap();
        let project = repo.path().join("apps").join("coralpolyp-be");
        std::fs::create_dir_all(&project).unwrap();
        std::fs::write(
            project.join("rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.95.0\"\ncomponents = [\"clippy\"]\n",
        )
        .unwrap();

        let checks = rust_toolchain_lint_component_checks(repo.path());

        assert_eq!(checks.len(), 1);
        assert!(
            checks[0].note.contains("rustfmt") && !checks[0].note.contains("clippy component"),
            "note must name only the missing rustfmt component, not the already-declared \
             clippy one: {}",
            checks[0].note
        );
        assert!(
            !checks[0].note.contains("the clippy, rustfmt component"),
            "must not regress to printing the full required list: {}",
            checks[0].note
        );
    }

    /// Binds the Gherkin scenario "A pinned Rust toolchain without lint
    /// components is reported as a warning, not a failure"
    /// (specs/apps/rhino/behavior/rhino-cli/gherkin/system/doctor.feature).
    #[test]
    fn check_all_reports_missing_lint_components_as_warning_not_missing() {
        let repo = tempfile::TempDir::new().unwrap();
        std::fs::write(repo.path().join("package.json"), "{}").unwrap();
        let project = repo.path().join("apps").join("rhino-cli");
        std::fs::create_dir_all(&project).unwrap();
        std::fs::write(
            project.join("rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.95.0\"\n",
        )
        .unwrap();
        let runner: CommandRunner = &|_name, _args| Ok(("1.95.0\n".into(), String::new(), 0));
        let opts = CheckOptions {
            repo_root: repo.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Full,
            selected_tools: Some(vec!["rust".into()]),
        };

        let result = check_all(&opts);

        let component_check = result
            .checks
            .iter()
            .find(|check| check.name == "rust-toolchain-components")
            .expect("component check must be present when the rust tool is selected");
        assert_eq!(component_check.status, ToolStatus::Warning);
        assert_eq!(
            result.missing_count, 0,
            "a component warning must never count as missing"
        );
    }

    #[test]
    fn check_all_omits_lint_component_checks_in_minimal_scope() {
        let repo = tempfile::TempDir::new().unwrap();
        std::fs::write(repo.path().join("package.json"), "{}").unwrap();
        let project = repo.path().join("apps").join("rhino-cli");
        std::fs::create_dir_all(&project).unwrap();
        std::fs::write(
            project.join("rust-toolchain.toml"),
            "[toolchain]\nchannel = \"1.95.0\"\n",
        )
        .unwrap();
        let runner: CommandRunner = &|_name, _args| Ok(("1.0.0\n".into(), String::new(), 0));
        let opts = CheckOptions {
            repo_root: repo.path().to_path_buf(),
            runner: Some(runner),
            scope: Scope::Minimal,
            selected_tools: None,
        };

        let result = check_all(&opts);

        assert!(
            !result
                .checks
                .iter()
                .any(|check| check.name == "rust-toolchain-components"),
            "Minimal scope excludes the rust tool, and the component check with it"
        );
    }
}
