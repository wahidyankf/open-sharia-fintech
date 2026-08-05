//! `md audit` — runs all md validators in sequence and aggregates findings.
//!
//! Equivalent to running each md subcommand individually.  Any validator
//! failure is recorded and reported at the end.  Use `--skip <name>` to
//! exclude individual validators.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::commands::{
    md_validate_frontmatter, md_validate_frontmatter_dates, md_validate_heading_hierarchy,
    md_validate_links, md_validate_mermaid, md_validate_naming, md_validate_readme_index,
};
use crate::domain::cliout::OutputFormat;

/// Member validators run by `md audit` in order.
const MEMBERS: &[&str] = &[
    "validate-naming",
    "validate-frontmatter",
    "validate-heading-hierarchy",
    "validate-links",
    "validate-mermaid",
    "frontmatter-dates",
    "readme-index",
];

/// CLI arguments for `md audit`.
#[derive(Args, Debug)]
pub struct AuditArgs {
    /// Validator name to skip (repeatable).
    #[arg(long = "skip")]
    pub skip: Vec<String>,
}

/// Run the `md audit` command.
///
/// Runs every md validator with default arguments.  Collects all failures
/// and returns an aggregated error at the end when any validator fails.
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
            "MD AUDIT PASSED: all {} validators passed",
            MEMBERS.len() - args.skip.len()
        );
        Ok(())
    } else {
        eprintln!(
            "MD AUDIT FAILED: {} validator(s) reported failures",
            failures.len()
        );
        for f in &failures {
            eprintln!("  {f}");
        }
        Err(anyhow!("md audit found {} failure(s)", failures.len()))
    }
}

/// Dispatch a single validator by name with default arguments.
fn run_member(name: &str, output_format: OutputFormat) -> std::result::Result<(), Error> {
    match name {
        "validate-naming" => md_validate_naming::run(
            &md_validate_naming::ValidateNamingArgs {
                exempt: vec![],
                positional: vec![],
            },
            output_format,
        ),
        "validate-frontmatter" => md_validate_frontmatter::run(
            &md_validate_frontmatter::ValidateFrontmatterArgs { positional: vec![] },
            output_format,
        ),
        "validate-heading-hierarchy" => md_validate_heading_hierarchy::run(
            &md_validate_heading_hierarchy::ValidateHeadingHierarchyArgs {
                positional: vec![],
                exclude: vec![],
            },
            output_format,
        ),
        "validate-links" => md_validate_links::run(
            &md_validate_links::ValidateLinksArgs {
                staged_only: false,
                exclude: vec![],
            },
            output_format,
        ),
        "validate-mermaid" => md_validate_mermaid::run(
            &md_validate_mermaid::ValidateMermaidArgs {
                staged_only: false,
                changed_only: false,
                max_label_len: 30,
                max_width: 4,
                max_depth: 0,
                max_subgraph_nodes: 6,
                positional: vec![],
                exclude: vec![],
            },
            output_format,
            false,
            false,
        ),
        "frontmatter-dates" => md_validate_frontmatter_dates::run(
            &md_validate_frontmatter_dates::FrontmatterAuditArgs {
                path: vec![],
                exclude: vec![],
                positional: vec![],
            },
            output_format,
        ),
        "readme-index" => md_validate_readme_index::run(
            &md_validate_readme_index::ReadmeIndexAuditArgs {
                exclude: vec![],
                positional: vec![],
            },
            output_format,
        ),
        _ => Err(anyhow!("unknown md validator: {name}")),
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn members_list_has_expected_count() {
        assert_eq!(MEMBERS.len(), 7);
    }

    #[test]
    fn members_list_contains_expected_validators() {
        assert!(MEMBERS.contains(&"validate-naming"));
        assert!(MEMBERS.contains(&"validate-frontmatter"));
        assert!(MEMBERS.contains(&"validate-heading-hierarchy"));
        assert!(MEMBERS.contains(&"validate-links"));
        assert!(MEMBERS.contains(&"validate-mermaid"));
        assert!(MEMBERS.contains(&"frontmatter-dates"));
        assert!(MEMBERS.contains(&"readme-index"));
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
    fn run_with_partial_skip_skips_named_validators() {
        // Skip all but one (validate-naming which will fail outside a git repo).
        // The important thing is the skip logic works.
        let args = AuditArgs {
            skip: MEMBERS
                .iter()
                .filter(|&&s| s != "validate-naming")
                .map(|&s| s.to_string())
                .collect(),
        };
        // validate-naming will error (no git root), which goes into failures.
        let result = run(&args, OutputFormat::Text);
        // Either ok (if git root found and no naming issues) or err (expected in test env).
        let _ = result; // Just test it doesn't panic.
    }

    #[test]
    fn run_member_unknown_returns_error() {
        let r = run_member("not-a-thing", OutputFormat::Text);
        assert!(r.is_err());
        let msg = r.unwrap_err().to_string();
        assert!(msg.contains("unknown md validator"));
    }

    #[test]
    fn run_member_covers_all_known_names_without_panic() {
        // All known names should dispatch without panic (may error due to missing git root).
        for &name in MEMBERS {
            let _ = run_member(name, OutputFormat::Text);
        }
    }

    #[test]
    fn audit_args_skip_is_vec() {
        let a = AuditArgs {
            skip: vec!["validate-naming".to_string()],
        };
        assert_eq!(a.skip.len(), 1);
    }
}
