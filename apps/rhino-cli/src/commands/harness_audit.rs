//! `harness audit` — runs all harness validators in sequence.
//!
//! Runs detect-duplication, validate-claude, validate-sync, and
//! validate-bindings with default arguments.  Generator commands (sync,
//! emit-bindings, generate-bindings) are intentionally excluded.
//! Use `--skip <name>` to exclude individual validators.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::commands::{
    governance_validate_word_budget, harness_catalog, harness_validate_bindings,
    harness_validate_claude, harness_validate_duplication, harness_validate_sync,
};
use crate::domain::cliout::OutputFormat;

/// Member validators run by `harness audit` in order.
///
/// Generator commands (`sync`, `emit-bindings`, `generate-bindings`) are
/// excluded because they modify files rather than validate them.
const MEMBERS: &[&str] = &[
    "detect-duplication",
    "validate-claude",
    "validate-sync",
    "validate-bindings",
    "validate-catalog",
    "validate-word-budget",
];

/// CLI arguments for `harness audit`.
#[derive(Args, Debug)]
pub struct AuditArgs {
    /// Validator name to skip (repeatable).
    #[arg(long = "skip")]
    pub skip: Vec<String>,
}

/// Run the `harness audit` command.
///
/// Runs every harness validator with default arguments.  Collects all
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
        // Name the member before running it. The per-validator reporters print
        // only failures at this verbosity, so without this line a passing audit
        // never says which validators it actually ran.
        println!("harness audit: {name}");
        let result = run_member(name, output_format);
        if let Err(e) = result {
            failures.push(format!("{name}: {e}"));
        }
    }

    if failures.is_empty() {
        println!(
            "HARNESS AUDIT PASSED: all {} validators passed",
            MEMBERS.len() - args.skip.len()
        );
        Ok(())
    } else {
        eprintln!(
            "HARNESS AUDIT FAILED: {} validator(s) reported failures",
            failures.len()
        );
        for f in &failures {
            eprintln!("  {f}");
        }
        Err(anyhow!("harness audit found {} failure(s)", failures.len()))
    }
}

/// Dispatch a single validator by name with default arguments.
fn run_member(name: &str, output_format: OutputFormat) -> std::result::Result<(), Error> {
    match name {
        "detect-duplication" => harness_validate_duplication::run(
            &harness_validate_duplication::DetectDuplicationArgs {},
            output_format,
        ),
        "validate-claude" => harness_validate_claude::run(
            &harness_validate_claude::ValidateClaudeArgs {
                agents_only: false,
                skills_only: false,
                verbose: false,
                quiet: false,
            },
            output_format,
        ),
        "validate-sync" => harness_validate_sync::run(
            &harness_validate_sync::ValidateSyncArgs {
                verbose: false,
                quiet: false,
            },
            output_format,
        ),
        "validate-bindings" => harness_validate_bindings::run(
            &harness_validate_bindings::ValidateBindingsArgs {
                verbose: false,
                quiet: false,
            },
            output_format,
        ),
        "validate-catalog" => harness_catalog::run_validate(
            &harness_catalog::CatalogValidateArgs {
                verbose: false,
                quiet: false,
            },
            output_format,
        ),
        "validate-word-budget" => governance_validate_word_budget::run(
            &governance_validate_word_budget::ValidateWordBudgetArgs {
                exclude: Vec::new(),
            },
            output_format,
        ),
        _ => Err(anyhow!("unknown harness validator: {name}")),
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn members_list_has_expected_count() {
        assert_eq!(MEMBERS.len(), 6);
    }

    #[test]
    fn members_list_contains_expected_validators() {
        assert!(MEMBERS.contains(&"detect-duplication"));
        assert!(MEMBERS.contains(&"validate-claude"));
        assert!(MEMBERS.contains(&"validate-sync"));
        assert!(MEMBERS.contains(&"validate-bindings"));
        assert!(MEMBERS.contains(&"validate-catalog"));
        assert!(MEMBERS.contains(&"validate-word-budget"));
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
        assert!(msg.contains("unknown harness validator"));
    }

    #[test]
    fn run_member_covers_all_known_names_without_panic() {
        for &name in MEMBERS {
            let _ = run_member(name, OutputFormat::Text);
        }
    }

    #[test]
    fn run_with_partial_skip_does_not_panic() {
        // Skip all but one to trigger failure path.
        let args = AuditArgs {
            skip: vec![
                "detect-duplication".to_string(),
                "validate-claude".to_string(),
                "validate-sync".to_string(),
            ],
        };
        // validate-bindings may error (no git root), triggering failure path.
        let _ = run(&args, OutputFormat::Text);
    }

    #[test]
    fn audit_args_skip_is_vec() {
        let a = AuditArgs {
            skip: vec!["detect-duplication".to_string()],
        };
        assert_eq!(a.skip.len(), 1);
    }
}
