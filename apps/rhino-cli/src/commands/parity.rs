//! `parity manifest` command adapters.

use anyhow::{Context, Error};
use clap::Args;

use crate::application::parity;
use crate::domain::cliout::OutputFormat;
use crate::internal::git;

/// Arguments for `parity manifest generate` (none required).
#[derive(Args, Debug)]
pub struct GenerateArgs {}

/// Arguments for `parity manifest validate` (none required).
#[derive(Args, Debug)]
pub struct ValidateArgs {}

/// Generate the deliberate parity manifest at the current repository root.
///
/// # Errors
/// Returns an error if the root cannot be located or the manifest cannot be
/// generated from its tracked boundary files.
pub fn generate(_args: &GenerateArgs, _output: OutputFormat) -> Result<(), Error> {
    let root = git::root::find_root().context("find repository root")?;
    parity::generate_at_root(&root)?;
    println!("generated {}", parity::MANIFEST_PATH);
    Ok(())
}

/// Validate the deliberate parity manifest at the current repository root.
///
/// # Errors
/// Returns a drift error when a tracked boundary file differs from the
/// committed manifest.
pub fn validate(_args: &ValidateArgs, _output: OutputFormat) -> Result<(), Error> {
    let root = git::root::find_root().context("find repository root")?;
    parity::validate_at_root(&root)?;
    println!("{} is current", parity::MANIFEST_PATH);
    Ok(())
}
