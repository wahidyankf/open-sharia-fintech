//! `lang java null-safety-annotations validate` — checks Java packages carry
//! required null-safety annotations on generated/contract code.
//!
//! Scans a Java source tree and verifies every package (any directory
//! containing at least one `.java` file) has a `package-info.java` carrying
//! the required null-safety annotation. Backs the `typecheck` Nx target for
//! `crud-be-java-springboot` and `crud-be-java-vertx`. See
//! `crate::internal::java::validator` for the scanning algorithm.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::domain::cliout::OutputFormat;
use crate::internal::java::reporter;
use crate::internal::java::types::ValidationOptions;
use crate::internal::java::validator::validate_all;

/// CLI arguments for `lang java null-safety-annotations validate`.
#[derive(Args, Debug)]
pub struct ValidateNullSafetyArgs {
    /// Root directory to scan (defaults to repo root).
    #[arg(long, value_name = "dir")]
    pub dir: Option<String>,
    /// Annotation name to require in `package-info.java` files.
    #[arg(long, default_value = "NullMarked")]
    pub annotation: String,
}

/// Run the `lang java null-safety-annotations validate` command.
///
/// # Errors
///
/// Returns an error when the target directory cannot be resolved or walked,
/// or when one or more Java packages fail annotation validation.
pub fn run(args: &ValidateNullSafetyArgs, output: OutputFormat) -> std::result::Result<(), Error> {
    let dir = args.dir.as_deref().unwrap_or(".");
    let abs_dir = std::path::absolute(dir)?;

    let opts = ValidationOptions {
        source_root: abs_dir.to_string_lossy().into_owned(),
        annotation: args.annotation.clone(),
    };
    let result = validate_all(&opts)?;

    let out = match output {
        OutputFormat::Text => reporter::format_text(&result, false, false),
        OutputFormat::Json => reporter::format_json(&result)?,
        OutputFormat::Markdown => reporter::format_markdown(&result),
    };
    print!("{out}");

    let num_violations = result.total_packages - result.valid_packages;
    if num_violations > 0 {
        return Err(anyhow!("found {num_violations} violation(s)"));
    }

    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use std::fs;

    use tempfile::TempDir;

    use super::*;

    #[test]
    fn args_constructible() {
        let a = ValidateNullSafetyArgs {
            dir: None,
            annotation: "NullMarked".to_string(),
        };
        assert!(a.dir.is_none());
        assert_eq!(a.annotation, "NullMarked");
    }

    // --- Regression: `lang java null-safety-annotations validate` must
    // actually scan Java packages for the required annotation. The phase
    // 9a/b/c command-surface rationalization replaced the real validator
    // (formerly `commands::java::run_validate_annotations`) with a permanent
    // no-op stub ("dormant in ose-public") while `internal::java::validator`
    // (the working algorithm, with its own passing unit tests) sat unwired
    // and unreachable in `internal.rs`. A polyglot consumer's Java `crud-be-*`
    // `typecheck` Nx targets invoke this exact command before
    // `mvn compile -Pnullcheck`, so a no-op silently regressed that quality
    // gate. ---

    #[test]
    fn run_detects_missing_package_info() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("com/a")).unwrap();
        fs::write(tmp.path().join("com/a/A.java"), "package com.a;\n").unwrap();

        let args = ValidateNullSafetyArgs {
            dir: Some(tmp.path().to_string_lossy().into_owned()),
            annotation: "NullMarked".to_string(),
        };
        let err = run(&args, OutputFormat::Text).unwrap_err();
        assert!(err.to_string().contains("violation"), "got: {err}");
    }

    #[test]
    fn run_passes_when_all_packages_annotated() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("com/a")).unwrap();
        fs::write(tmp.path().join("com/a/A.java"), "package com.a;\n").unwrap();
        fs::write(
            tmp.path().join("com/a/package-info.java"),
            "@NullMarked\npackage com.a;\n",
        )
        .unwrap();

        let args = ValidateNullSafetyArgs {
            dir: Some(tmp.path().to_string_lossy().into_owned()),
            annotation: "NullMarked".to_string(),
        };
        assert!(run(&args, OutputFormat::Text).is_ok());
    }

    #[test]
    fn run_honors_custom_annotation() {
        let tmp = TempDir::new().unwrap();
        fs::create_dir_all(tmp.path().join("com/a")).unwrap();
        fs::write(tmp.path().join("com/a/A.java"), "package com.a;\n").unwrap();
        fs::write(
            tmp.path().join("com/a/package-info.java"),
            "@NonNull\npackage com.a;\n",
        )
        .unwrap();

        let args = ValidateNullSafetyArgs {
            dir: Some(tmp.path().to_string_lossy().into_owned()),
            annotation: "NonNull".to_string(),
        };
        assert!(run(&args, OutputFormat::Text).is_ok());
    }

    #[test]
    fn run_with_dir_none_defaults_to_cwd_without_error() {
        // The crate manifest dir has no Java sources at its root → an empty
        // scan, not an error.
        let args = ValidateNullSafetyArgs {
            dir: None,
            annotation: "NullMarked".to_string(),
        };
        assert!(run(&args, OutputFormat::Text).is_ok());
    }
}
