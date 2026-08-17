//! `convention audit` — runs all convention validators in sequence.
//!
//! Runs the emoji and license validators with default arguments.
//! Use `--skip <name>` to exclude individual validators.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::commands::{convention_validate_emoji, convention_validate_license};
use crate::domain::cliout::OutputFormat;

/// Member validators run by `convention audit` in order.
const MEMBERS: &[&str] = &["emoji", "license"];

/// CLI arguments for `convention audit`.
#[derive(Args, Debug)]
pub struct AuditArgs {
    /// Validator name to skip (repeatable).
    #[arg(long = "skip")]
    pub skip: Vec<String>,
}

/// Run the `convention audit` command.
///
/// Runs every convention validator with default arguments.  Collects all
/// failures and returns an aggregated error when any validator fails.
///
/// # Errors
///
/// Returns an aggregated error listing each failing validator.
pub fn run(args: &AuditArgs, output_format: OutputFormat) -> std::result::Result<(), Error> {
    let mut failures: Vec<String> = Vec::new();

    for &name in MEMBERS {
        if args.skip.iter().any(|s| s == name) {
            continue;
        }
        let result = run_member(name, output_format);
        if let Err(e) = result {
            failures.push(format!("{name}: {e}"));
        }
    }

    if failures.is_empty() {
        println!(
            "CONVENTION AUDIT PASSED: all {} validators passed",
            MEMBERS.len() - args.skip.len()
        );
        Ok(())
    } else {
        eprintln!(
            "CONVENTION AUDIT FAILED: {} validator(s) reported failures",
            failures.len()
        );
        for f in &failures {
            eprintln!("  {f}");
        }
        Err(anyhow!(
            "convention audit found {} failure(s)",
            failures.len()
        ))
    }
}

/// Dispatch a single validator by name with default arguments.
fn run_member(name: &str, output_format: OutputFormat) -> std::result::Result<(), Error> {
    match name {
        "emoji" => convention_validate_emoji::run(
            &convention_validate_emoji::EmojiAuditArgs {
                path: vec![],
                positional: vec![],
            },
            output_format,
        ),
        "license" => convention_validate_license::run(
            &convention_validate_license::LicenseAuditArgs {},
            output_format,
        ),
        _ => Err(anyhow!("unknown convention validator: {name}")),
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn members_list_has_expected_count() {
        assert_eq!(MEMBERS.len(), 2);
    }

    #[test]
    fn members_list_contains_expected_validators() {
        assert!(MEMBERS.contains(&"emoji"));
        assert!(MEMBERS.contains(&"license"));
    }

    #[test]
    fn run_with_all_skipped_succeeds() {
        let args = AuditArgs {
            skip: MEMBERS.iter().map(|&s| s.to_string()).collect(),
        };
        let result = run(&args, OutputFormat::Text);
        assert!(result.is_ok());
    }

    #[test]
    fn run_member_unknown_returns_error() {
        let r = run_member("not-a-thing", OutputFormat::Text);
        assert!(r.is_err());
        let msg = r.unwrap_err().to_string();
        assert!(msg.contains("unknown convention validator"));
    }

    #[test]
    fn run_member_covers_all_known_names_without_panic() {
        for &name in MEMBERS {
            let _ = run_member(name, OutputFormat::Text);
        }
    }

    #[test]
    fn run_with_partial_skip_does_not_panic() {
        let args = AuditArgs {
            skip: vec!["emoji".to_string()],
        };
        // `license` still runs; a failure there exercises the failure path.
        let _ = run(&args, OutputFormat::Text);
    }

    #[test]
    fn audit_args_skip_is_vec() {
        let a = AuditArgs {
            skip: vec!["emoji".to_string()],
        };
        assert_eq!(a.skip.len(), 1);
    }
}
