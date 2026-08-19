//! `harness catalog generate` and `harness catalog validate` — render the
//! platform-binding catalog table from the harness registry, and guard the
//! generated region against hand edits.
//!
//! Reports through the same reporter as every other harness validator, so the
//! output shape a reader already knows does not change per command. See
//! `crate::application::agents::catalog`.

use std::fs;
use std::path::{Path, PathBuf};

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::agents::catalog::{CATALOG_REMEDIATION, render_region, rewrite_region};
use crate::application::agents::reporter::{
    format_validation_json, format_validation_markdown, format_validation_text,
};
use crate::application::agents::types::{ValidationCheck, ValidationResult};
use crate::application::repo_config;
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Check name shared by both subcommands, so a reader sees one label whichever
/// command reported the drift.
const CHECK_NAME: &str = "Harness catalog: generated region";

/// CLI arguments for `harness catalog generate`.
#[derive(Args, Debug)]
pub struct CatalogGenerateArgs {
    /// Verbose output (show all checks).
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output (summary only).
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// CLI arguments for `harness catalog validate`.
#[derive(Args, Debug)]
pub struct CatalogValidateArgs {
    /// Verbose output (show all checks).
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output (summary only).
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// The catalog document's path, its current text, and the text a fresh render
/// would produce.
struct Rendered {
    /// Repository-relative document path, as declared in the registry.
    relative: String,
    /// Absolute path on disk.
    absolute: PathBuf,
    /// The document as it currently stands.
    current: String,
    /// The document with a freshly rendered region substituted in.
    expected: String,
}

/// Loads the registry, renders the region, and returns both document states.
fn render(repo_root: &Path) -> Result<Rendered, Error> {
    let config = repo_config::load(repo_root)?;
    let settings = config.harness_catalog.as_ref().ok_or_else(|| {
        anyhow!(
            "repo-config.yml declares no `harness-catalog:` block; \
             the catalog document path and verification date must be declared, not inferred"
        )
    })?;

    let region = render_region(&config.harness, &settings.verified)?;
    let absolute = repo_root.join(&settings.document);
    let current = fs::read_to_string(&absolute)
        .map_err(|e| anyhow!("cannot read {}: {e}", settings.document))?;
    let expected = rewrite_region(&current, &region, &settings.document)?;

    Ok(Rendered {
        relative: settings.document.clone(),
        absolute,
        current,
        expected,
    })
}

/// Emits the result through the reporter the caller selected.
fn report(result: &ValidationResult, format: OutputFormat, verbose: bool, quiet: bool) {
    match format {
        OutputFormat::Text => print!("{}", format_validation_text(result, verbose, quiet)),
        OutputFormat::Json => match format_validation_json(result) {
            Ok(json) => println!("{json}"),
            Err(error) => eprintln!("failed to render JSON: {error}"),
        },
        OutputFormat::Markdown => print!("{}", format_validation_markdown(result, verbose)),
    }
}

/// Run the `harness catalog generate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, the registry or document
/// cannot be read, or the rewritten document cannot be written back.
pub fn run_generate(
    args: &CatalogGenerateArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let rendered = render(&repo_root)?;

    let mut result = ValidationResult::default();
    if rendered.current == rendered.expected {
        result.tally(ValidationCheck::passed(
            CHECK_NAME,
            format!("{} already matches the registry", rendered.relative),
        ));
    } else {
        fs::write(&rendered.absolute, &rendered.expected)
            .map_err(|e| anyhow!("cannot write {}: {e}", rendered.relative))?;
        result.tally(ValidationCheck::passed(
            CHECK_NAME,
            format!("{} regenerated from the registry", rendered.relative),
        ));
    }

    report(&result, output_format, args.verbose, args.quiet);
    Ok(())
}

/// Run the `harness catalog validate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, the registry or document
/// cannot be read, or the generated region diverges from the registry.
pub fn run_validate(
    args: &CatalogValidateArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let rendered = render(&repo_root)?;

    let mut result = ValidationResult::default();
    if rendered.current == rendered.expected {
        result.tally(ValidationCheck::passed(
            CHECK_NAME,
            format!("{} matches the registry", rendered.relative),
        ));
    } else {
        result.tally(ValidationCheck::failed(
            CHECK_NAME,
            "generated region rendered from repo-config.yml",
            format!("{} diverges from the registry", rendered.relative),
            format!(
                "the generated region of {} was hand-edited or the registry changed; \
                 {CATALOG_REMEDIATION}",
                rendered.relative
            ),
        ));
    }

    report(&result, output_format, args.verbose, args.quiet);

    if result.failed_checks > 0 {
        return Err(anyhow!(
            "catalog validation failed: {} diverges from the harness registry; \
             {CATALOG_REMEDIATION}",
            rendered.relative
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn both_subcommands_report_under_one_check_name() {
        // The two commands are separate entry points onto the same claim. A
        // reader who saw one label from `validate` must see the same label from
        // `generate`, or the two read as unrelated checks.
        assert!(CHECK_NAME.starts_with("Harness catalog:"));
    }

    #[test]
    fn args_default() {
        let generate = CatalogGenerateArgs {
            verbose: false,
            quiet: false,
        };
        let validate = CatalogValidateArgs {
            verbose: false,
            quiet: false,
        };
        assert!(!generate.verbose);
        assert!(!validate.quiet);
    }
}
