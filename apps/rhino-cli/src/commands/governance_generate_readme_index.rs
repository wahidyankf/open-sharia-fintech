//! `rhino-cli governance readme-index generate` — writes conforming README
//! indexes instead of reporting their absence (FR-3.12).
//!
//! Shares the file-discovery and annotation-derivation core with
//! `governance readme-index validate`
//! (`application::governance::readme_index::generate_readme_index`); this
//! command file only adds CLI plumbing and output formatting, mirroring
//! `commands::governance_validate_readme_index`'s own shape.

use std::fmt::Write as _;
use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;
use serde::Serialize;

use crate::application::governance::readme_index::generate_readme_index;
use crate::commands::governance_validate_readme_index::DEFAULT_PATHS;
use crate::domain::cliout::OutputFormat;
use crate::infrastructure::fs::real::RealFs;
use crate::internal::git;

/// JSON output schema identifier for this command.
const SCHEMA: &str = "rhino-cli/readme-index-generate/v1";

/// CLI arguments for `governance readme-index generate`.
#[derive(Args, Debug)]
pub struct ReadmeIndexGenerateArgs {
    /// Glob to exclude from generation (repeatable).
    #[arg(long = "exclude")]
    pub exclude: Vec<String>,
    /// Path to scan (repeatable). Overrides `DEFAULT_PATHS` when given —
    /// the same `--paths` semantics `governance readme-index validate` uses
    /// (FR-3.12), so `generate` and `validate` always cover the same scope.
    #[arg(long = "paths")]
    pub paths: Vec<String>,
    /// Positional paths (legacy override, same effect as `--paths`).
    pub positional: Vec<String>,
}

/// JSON envelope wrapping the list of generated files.
#[derive(Serialize)]
struct Envelope<'a> {
    /// Output schema identifier.
    schema: &'a str,
    /// Always `"passed"` — writing conforming indexes cannot itself fail the
    /// gate (there is no finding-based exit criterion for `generate`).
    status: &'a str,
    /// Every index file written, repo-relative-ish string form.
    written: Vec<String>,
}

/// Resolves the scan-path list for this invocation — `--paths` wins when
/// given, then the legacy `positional` argument, then
/// [`DEFAULT_PATHS`][crate::commands::governance_validate_readme_index::DEFAULT_PATHS],
/// unchanged, mirroring
/// `governance_validate_readme_index::resolve_scan_paths` exactly (FR-3.12).
#[must_use]
pub fn resolve_scan_paths(args: &ReadmeIndexGenerateArgs) -> Vec<String> {
    if !args.paths.is_empty() {
        return args.paths.clone();
    }
    if !args.positional.is_empty() {
        return args.positional.clone();
    }
    DEFAULT_PATHS
        .iter()
        .map(std::string::ToString::to_string)
        .collect()
}

/// Run the `governance readme-index generate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found or the generation itself
/// fails (a directory cannot be read, or a file cannot be written).
pub fn run(
    args: &ReadmeIndexGenerateArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let rel_paths = resolve_scan_paths(args);
    let full_paths: Vec<String> = rel_paths
        .iter()
        .map(|p| {
            if Path::new(p).is_absolute() {
                p.clone()
            } else {
                repo_root.join(p).to_string_lossy().to_string()
            }
        })
        .collect();

    let written = generate_readme_index(&RealFs, &full_paths, &args.exclude)
        .context("readme-index generate failed")?;
    let written: Vec<String> = written
        .iter()
        .map(|p| p.to_string_lossy().to_string())
        .collect();

    match output_format {
        OutputFormat::Text => print!("{}", format_text(&written)),
        OutputFormat::Json => print!("{}", format_json(&written)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&written)),
    }

    Ok(())
}

/// Format the generated-file list as human-readable text.
fn format_text(written: &[String]) -> String {
    if written.is_empty() {
        return "README INDEX GENERATE: no directory needed a new or updated index\n".to_string();
    }
    let mut sb = String::new();
    let _ = writeln!(
        sb,
        "README INDEX GENERATE: wrote {} index(es)",
        written.len()
    );
    for f in written {
        let _ = writeln!(sb, "  {f}");
    }
    sb
}

/// Serialize the generated-file list as a JSON envelope string.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
fn format_json(written: &[String]) -> std::result::Result<String, Error> {
    let env = Envelope {
        schema: SCHEMA,
        status: "passed",
        written: written.to_vec(),
    };
    let mut s = serde_json::to_string_pretty(&env)?;
    s.push('\n');
    Ok(s)
}

/// Format the generated-file list as a Markdown list.
fn format_markdown(written: &[String]) -> String {
    if written.is_empty() {
        return "## README Index Generate\n\nNo directory needed a new or updated index.\n"
            .to_string();
    }
    let mut sb = String::new();
    let _ = writeln!(
        sb,
        "## README Index Generate\n\nWrote {} index(es):\n",
        written.len()
    );
    for f in written {
        let _ = writeln!(sb, "- {f}");
    }
    sb
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn format_text_empty() {
        assert!(format_text(&[]).starts_with("README INDEX GENERATE: no directory"));
    }

    #[test]
    fn format_text_lists_written_files() {
        let s = format_text(&["repo-governance/formatting/README.md".to_string()]);
        assert!(s.contains("wrote 1 index(es)"));
        assert!(s.contains("repo-governance/formatting/README.md"));
    }

    #[test]
    fn format_json_lists_written_files() {
        let s = format_json(&["a/README.md".to_string()]).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "passed");
        assert_eq!(v["schema"], SCHEMA);
        assert_eq!(v["written"][0], "a/README.md");
    }

    #[test]
    fn format_markdown_lists_written_files() {
        let s = format_markdown(&["a/README.md".to_string()]);
        assert!(s.contains("Wrote 1 index(es)"));
        assert!(s.contains("- a/README.md"));
    }

    #[test]
    fn paths_flag_overrides_default_paths_when_given() {
        let args = ReadmeIndexGenerateArgs {
            exclude: vec![],
            paths: vec!["repo-governance/".to_string()],
            positional: vec![],
        };
        let resolved = resolve_scan_paths(&args);
        assert_eq!(resolved, vec!["repo-governance/".to_string()]);
    }

    #[test]
    fn paths_flag_falls_back_to_default_paths_when_absent() {
        let args = ReadmeIndexGenerateArgs {
            exclude: vec![],
            paths: vec![],
            positional: vec![],
        };
        let resolved = resolve_scan_paths(&args);
        let expected: Vec<String> = DEFAULT_PATHS
            .iter()
            .map(std::string::ToString::to_string)
            .collect();
        assert_eq!(
            resolved, expected,
            "FR-3.12: generate must default to the same DEFAULT_PATHS scope as validate"
        );
    }

    #[test]
    fn positional_paths_override_default_when_given_and_no_paths_flag() {
        let args = ReadmeIndexGenerateArgs {
            exclude: vec![],
            paths: vec![],
            positional: vec!["docs/".to_string()],
        };
        assert_eq!(resolve_scan_paths(&args), vec!["docs/".to_string()]);
    }
}
