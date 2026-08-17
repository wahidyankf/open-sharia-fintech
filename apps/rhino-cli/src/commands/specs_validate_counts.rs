//! `specs counts validate` — checks that spec folders have the minimum required file counts.
//!
//! Kept as a standalone leaf (mirroring ose-private) because `specs structure validate`
//! hardcodes the `specs/apps/<name>` prefix and cannot reach spec trees that live outside
//! `specs/apps/` — e.g. `specs/libs/web-ui`, `specs/libs/web-ui-token`, `specs/libs/rust-commons`,
//! `specs/libs/fsharp-crane-core`, whose `specs:structure-validation` Nx targets pass an explicit
//! `specs/libs/...` folder here.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::repo_config;
use crate::application::specs::validate_spec_counts;
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// CLI arguments for `specs validate-counts`.
#[derive(Args, Debug)]
pub struct ValidateCountsArgs {
    /// Single positional folder.
    #[arg(value_name = "folder")]
    pub folder: Option<String>,
    /// Comma-separated app names.
    #[arg(long = "apps", value_delimiter = ',')]
    pub apps: Vec<String>,
}

/// Resolve the list of folders to validate from positional and flag inputs.
///
/// When neither a positional folder nor `--apps` is given, the default app list
/// is `default_apps` — read from `repo-config.yml`'s `specs.ddd-areas` by the
/// caller, so the scan targets are repo data, not a source-hard-coded per-repo
/// allowlist.
fn resolve_folders(
    positional: Option<&String>,
    flag: &[String],
    default_apps: &[String],
) -> Vec<String> {
    if let Some(p) = positional {
        return vec![p.clone()];
    }
    let apps: Vec<String> = if flag.is_empty() {
        default_apps.to_vec()
    } else {
        flag.to_vec()
    };
    apps.into_iter()
        .map(|a| format!("specs/apps/{a}"))
        .collect()
}

/// Run the `specs validate-counts` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found or findings are detected.
pub fn run(args: &ValidateCountsArgs, _output: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    run_at_root(&repo_root, args, &mut std::io::stdout())
}

/// Run `specs validate-counts` from a known `repo_root` (testable entry point).
///
/// # Errors
///
/// Returns an error if output cannot be written or findings are detected.
pub fn run_at_root(
    repo_root: &std::path::Path,
    args: &ValidateCountsArgs,
    w: &mut dyn std::io::Write,
) -> std::result::Result<(), Error> {
    let default_apps = repo_config::load_or_default(repo_root).specs.ddd_areas;
    let folders = resolve_folders(args.folder.as_ref(), &args.apps, &default_apps);
    let mut total = 0usize;
    for folder in &folders {
        let findings = validate_spec_counts(repo_root, folder);
        total += findings.len();
        if findings.is_empty() {
            writeln!(w, "specs validate-counts: 0 finding(s) for \"{folder}\"")?;
            continue;
        }
        for f in &findings {
            writeln!(w, "{}: {}: {}", f.file, f.criticality, f.evidence)?;
        }
    }
    if total > 0 {
        return Err(anyhow!("{total} finding(s) found by specs validate-counts"));
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn resolve_folders_positional() {
        let v = resolve_folders(Some(&"x".to_string()), &[], &[]);
        assert_eq!(v, vec!["x".to_string()]);
    }

    #[test]
    fn resolve_folders_default_reads_config_areas() {
        // The default app list is the config-supplied `specs.ddd-areas`, not a
        // source-hard-coded allowlist.
        let default_apps = vec!["fixture-ledger".to_string(), "fixture-catalog".to_string()];
        let v = resolve_folders(None, &[], &default_apps);
        assert_eq!(
            v,
            vec![
                "specs/apps/fixture-ledger".to_string(),
                "specs/apps/fixture-catalog".to_string()
            ]
        );
    }

    #[test]
    fn resolve_folders_flag() {
        let v = resolve_folders(None, &["a".to_string()], &[]);
        assert_eq!(v, vec!["specs/apps/a".to_string()]);
    }

    #[test]
    fn run_at_root_missing_folder_errors() {
        let dir = tempfile::tempdir().unwrap();
        let mut buf: Vec<u8> = Vec::new();
        let args = ValidateCountsArgs {
            folder: Some("specs/apps/missing".to_string()),
            apps: vec![],
        };
        assert!(run_at_root(dir.path(), &args, &mut buf).is_err());
    }

    #[test]
    fn run_at_root_clean_folder_passes() {
        let dir = tempfile::tempdir().unwrap();
        for sub in crate::application::specs::required_spec_folders() {
            let p = dir.path().join("specs/apps/x").join(sub);
            std::fs::create_dir_all(&p).unwrap();
            std::fs::write(p.join("a.md"), "x").unwrap();
        }
        let mut buf: Vec<u8> = Vec::new();
        let args = ValidateCountsArgs {
            folder: Some("specs/apps/x".to_string()),
            apps: vec![],
        };
        assert!(run_at_root(dir.path(), &args, &mut buf).is_ok());
        assert!(String::from_utf8_lossy(&buf).contains("0 finding(s)"));
    }
}
