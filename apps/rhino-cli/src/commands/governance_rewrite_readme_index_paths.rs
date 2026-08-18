//! `rhino-cli governance readme-index rewrite-paths` — repoints markdown link
//! targets across the tracked corpus according to a TSV rename map.
//!
//! Companion to `governance readme-index generate`: `generate` owns an index's
//! entry list, this command owns the link targets inside it after a rename
//! sweep. It rewrites **only** the target inside a `](...)` link, leaving entry
//! order, annotation text, and prose byte-identical.

use std::path::Path;

use anyhow::{Context, Error, anyhow};
use clap::Args;
use serde::Serialize;

use crate::application::governance::readme_index::rewrite_index_paths;
use crate::domain::cliout::OutputFormat;
use crate::infrastructure::fs::real::RealFs;
use crate::internal::git;

use super::governance_validate_readme_index::DEFAULT_PATHS;

/// Output schema identifier for the JSON envelope.
const SCHEMA: &str = "rhino-cli/readme-index-rewrite-paths/v1";

/// CLI arguments for `governance readme-index rewrite-paths`.
#[derive(Args, Debug)]
pub struct ReadmeIndexRewritePathsArgs {
    /// Path to a TSV rename map: one `old<TAB>new` pair per line. Lines that
    /// are blank or start with `#` are ignored.
    #[arg(long = "map")]
    pub map: String,
    /// Path to scan (repeatable). Overrides `DEFAULT_PATHS` when given.
    #[arg(long = "paths")]
    pub paths: Vec<String>,
}

/// JSON envelope wrapping the list of rewritten files.
#[derive(Serialize)]
struct Envelope<'a> {
    /// Output schema identifier.
    schema: &'a str,
    /// Always `"passed"` — rewriting link targets has no finding-based exit
    /// criterion.
    status: &'a str,
    /// Every file whose content actually changed.
    rewritten: Vec<String>,
}

/// Parses a TSV rename map into `(old, new)` pairs.
///
/// # Errors
///
/// Returns an error if a non-comment, non-blank line does not carry exactly
/// two tab-separated fields — a silently-skipped malformed row would drop a
/// rename from the sweep and leave a dangling link.
fn parse_map(content: &str) -> std::result::Result<Vec<(String, String)>, Error> {
    let mut out = Vec::new();
    for (i, line) in content.lines().enumerate() {
        let line = line.trim_end_matches(['\r', '\n']);
        if line.trim().is_empty() || line.trim_start().starts_with('#') {
            continue;
        }
        let cols: Vec<&str> = line.split('\t').collect();
        if cols.len() != 2 || cols[0].trim().is_empty() || cols[1].trim().is_empty() {
            return Err(anyhow!(
                "rename map line {} is malformed (expected `old<TAB>new`): {line:?}",
                i + 1
            ));
        }
        out.push((cols[0].trim().to_string(), cols[1].trim().to_string()));
    }
    Ok(out)
}

/// Run the `governance readme-index rewrite-paths` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, the map cannot be read or
/// parsed, or a file cannot be written.
pub fn run(
    args: &ReadmeIndexRewritePathsArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    let map_raw = std::fs::read_to_string(&args.map)
        .with_context(|| format!("read rename map {}", args.map))?;
    let map = parse_map(&map_raw)?;

    let rel_paths: Vec<String> = if args.paths.is_empty() {
        DEFAULT_PATHS
            .iter()
            .map(std::string::ToString::to_string)
            .collect()
    } else {
        args.paths.clone()
    };
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

    let rewritten = rewrite_index_paths(&RealFs, &full_paths, &map)
        .context("readme-index rewrite-paths failed")?;
    let rewritten: Vec<String> = rewritten
        .iter()
        .map(|p| p.to_string_lossy().to_string())
        .collect();

    match output_format {
        OutputFormat::Json => {
            let env = Envelope {
                schema: SCHEMA,
                status: "passed",
                rewritten,
            };
            println!("{}", serde_json::to_string_pretty(&env)?);
        }
        OutputFormat::Text | OutputFormat::Markdown => {
            println!(
                "readme-index rewrite-paths: {} file(s) updated",
                rewritten.len()
            );
            for p in &rewritten {
                println!("  {p}");
            }
        }
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn parse_map_reads_tab_separated_pairs() {
        let map = parse_map("01-a.md\ta.md\n02-b.md\tb.md\n").unwrap();
        assert_eq!(
            map,
            vec![
                ("01-a.md".to_string(), "a.md".to_string()),
                ("02-b.md".to_string(), "b.md".to_string()),
            ]
        );
    }

    #[test]
    fn parse_map_skips_blank_and_comment_lines() {
        let map = parse_map("# comment\n\n01-a.md\ta.md\n").unwrap();
        assert_eq!(map.len(), 1);
    }

    #[test]
    fn parse_map_rejects_a_malformed_row_rather_than_dropping_it() {
        // A silently-skipped row would leave a dangling link after the sweep.
        let err = parse_map("01-a.md a.md\n").unwrap_err();
        assert!(err.to_string().contains("malformed"), "{err}");
    }
}
