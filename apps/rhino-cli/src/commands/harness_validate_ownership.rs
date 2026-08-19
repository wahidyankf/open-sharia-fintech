//! `harness ownership validate` — enforces that every tracked file under every
//! binding directory carries exactly one declared ownership class.
//!
//! Reports through the same reporter as every other harness validator, so the
//! output shape a reader already knows does not change per command. See
//! `crate::application::agents::ownership`.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::agents::ownership::validate_ownership;
use crate::application::agents::reporter::{
    format_validation_json, format_validation_markdown, format_validation_text,
};
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// CLI arguments for `harness ownership validate`.
#[derive(Args, Debug)]
pub struct ValidateOwnershipArgs {
    /// Verbose output (show all checks).
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output (summary only).
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// Run the `harness ownership validate` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found or any ownership check fails.
pub fn run(
    args: &ValidateOwnershipArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let result = validate_ownership(&repo_root);

    match output_format {
        OutputFormat::Text => print!(
            "{}",
            format_validation_text(&result, args.verbose, args.quiet)
        ),
        OutputFormat::Json => println!("{}", format_validation_json(&result)?),
        OutputFormat::Markdown => print!("{}", format_validation_markdown(&result, args.verbose)),
    }

    if result.failed_checks > 0 {
        return Err(anyhow!(
            "ownership validation failed: {} checks failed",
            result.failed_checks
        ));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn args_default() {
        let a = ValidateOwnershipArgs {
            verbose: false,
            quiet: false,
        };
        assert!(!a.verbose);
        assert!(!a.quiet);
    }
}
