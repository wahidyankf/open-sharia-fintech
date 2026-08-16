//! `specs clean java-imports` — strips unused, same-package, and duplicate
//! imports from generated Java contract files.
//!
//! Post-processes `openapi-generator-cli`'s Java output for the
//! `crud-be-java-springboot` and `crud-be-java-vertx` codegen pipelines,
//! which otherwise emit unused/duplicate imports that trip IDE and compiler
//! warnings. See `crate::internal::contracts::java_clean_imports` for the
//! cleaning algorithm.

use std::fmt::Write as _;

use anyhow::Error;
use clap::Args;
use serde::Serialize;

use crate::domain::cliout::OutputFormat;
use crate::internal::contracts::java_clean_imports::clean_java_imports;
use crate::internal::contracts::types::{JavaCleanImportsOptions, JavaCleanImportsResult};

/// CLI arguments for `specs clean java-imports`.
#[derive(Args, Debug)]
pub struct CleanJavaImportsArgs {
    /// Root directory to scan for generated Java files.
    #[arg(long, value_name = "dir")]
    pub dir: Option<String>,
}

/// JSON output envelope for `specs clean java-imports`.
#[derive(Serialize)]
struct CleanImportsJson<'a> {
    /// `"clean"` when nothing needed cleaning, `"modified"` otherwise.
    status: &'a str,
    /// Number of `.java` files scanned.
    total_files: usize,
    /// Number of files rewritten.
    modified_files: usize,
    /// Relative paths of the rewritten files.
    modified: &'a [String],
}

/// Run the `specs clean java-imports` command.
///
/// # Errors
///
/// Returns an error when the target directory cannot be resolved or walked,
/// or when a Java file cannot be read or rewritten.
pub fn run(args: &CleanJavaImportsArgs, output: OutputFormat) -> std::result::Result<(), Error> {
    let dir = args.dir.as_deref().unwrap_or(".");
    let abs_dir = std::path::absolute(dir)?;

    let opts = JavaCleanImportsOptions {
        dir: abs_dir.to_string_lossy().into_owned(),
    };
    let result = clean_java_imports(&opts)?;

    match output {
        OutputFormat::Text => print!("{}", format_text(&result)),
        OutputFormat::Json => print!("{}", format_json(&result)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&result)),
    }
    Ok(())
}

/// Formats the cleaning result as human-readable text.
fn format_text(result: &JavaCleanImportsResult) -> String {
    if result.modified_files == 0 {
        return "No imports needed cleaning.\n".to_string();
    }

    let mut out = String::new();
    let _ = writeln!(
        out,
        "Cleaned imports in {} of {} Java files.",
        result.modified_files, result.total_files
    );
    for f in &result.modified {
        let _ = writeln!(out, "  {f}");
    }
    out
}

/// Formats the cleaning result as a JSON envelope.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
fn format_json(result: &JavaCleanImportsResult) -> std::result::Result<String, Error> {
    let status = if result.modified_files == 0 {
        "clean"
    } else {
        "modified"
    };
    let env = CleanImportsJson {
        status,
        total_files: result.total_files,
        modified_files: result.modified_files,
        modified: &result.modified,
    };
    let mut s = serde_json::to_string_pretty(&env)?;
    s.push('\n');
    Ok(s)
}

/// Formats the cleaning result as Markdown.
fn format_markdown(result: &JavaCleanImportsResult) -> String {
    let mut out = String::new();
    out.push_str("# Java Import Cleaning Report\n\n");
    let _ = writeln!(out, "- **Total files**: {}", result.total_files);
    let _ = writeln!(out, "- **Modified files**: {}", result.modified_files);

    if result.modified_files == 0 {
        out.push_str("\nNo files needed cleaning.\n");
        return out;
    }

    out.push_str("\n## Modified Files\n\n");
    for f in &result.modified {
        let _ = writeln!(out, "- `{f}`");
    }
    out
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use std::fs;

    use tempfile::TempDir;

    use super::*;

    #[test]
    fn args_constructible() {
        let a = CleanJavaImportsArgs { dir: None };
        assert!(a.dir.is_none());
    }

    // --- Regression: `specs clean java-imports` must actually clean the
    // generated Java files it is pointed at. The phase 9a/b/c command-surface
    // rationalization replaced the real cleaner with a permanent no-op stub
    // ("dormant in ose-public") while `internal::contracts::java_clean_imports`
    // (the working algorithm, with its own passing unit tests) sat unwired and
    // unreachable. A polyglot consumer's Java `crud-be-*` Nx targets pipe real
    // OpenAPI-generated Java through this exact command, so a no-op regressed
    // those pipelines silently. ---

    #[test]
    fn run_actually_removes_unused_imports() {
        let tmp = TempDir::new().unwrap();
        let f = tmp.path().join("Foo.java");
        fs::write(
            &f,
            "package com.foo;\nimport java.util.List;\nimport java.util.Map;\n\nclass Foo { List x; }\n",
        )
        .unwrap();

        let args = CleanJavaImportsArgs {
            dir: Some(tmp.path().to_string_lossy().into_owned()),
        };
        run(&args, OutputFormat::Text).unwrap();

        let after = fs::read_to_string(&f).unwrap();
        assert!(after.contains("import java.util.List;"), "kept: {after}");
        assert!(!after.contains("import java.util.Map;"), "removed: {after}");
    }

    #[test]
    fn run_defaults_dir_to_cwd_without_error() {
        // No generated Java files under the crate manifest dir → walks an
        // empty result set, not an error.
        let args = CleanJavaImportsArgs { dir: None };
        assert!(run(&args, OutputFormat::Text).is_ok());
    }

    #[test]
    fn format_text_no_modifications() {
        let r = JavaCleanImportsResult {
            total_files: 5,
            modified_files: 0,
            modified: vec![],
        };
        assert_eq!(format_text(&r), "No imports needed cleaning.\n");
    }

    #[test]
    fn format_text_with_modifications_lists_files() {
        let r = JavaCleanImportsResult {
            total_files: 5,
            modified_files: 2,
            modified: vec!["A.java".to_string(), "B.java".to_string()],
        };
        let s = format_text(&r);
        assert!(s.starts_with("Cleaned imports in 2 of 5 Java files.\n"));
        assert!(s.contains("  A.java\n"));
        assert!(s.contains("  B.java\n"));
    }

    #[test]
    fn format_json_status_reflects_modifications() {
        let clean = JavaCleanImportsResult {
            total_files: 3,
            modified_files: 0,
            modified: vec![],
        };
        let s = format_json(&clean).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "clean");
        assert_eq!(v["total_files"], 3);

        let modified = JavaCleanImportsResult {
            total_files: 3,
            modified_files: 1,
            modified: vec!["X.java".to_string()],
        };
        let s = format_json(&modified).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "modified");
        assert_eq!(v["modified"][0], "X.java");
    }

    #[test]
    fn format_markdown_with_and_without_modifications() {
        let none = format_markdown(&JavaCleanImportsResult {
            total_files: 2,
            modified_files: 0,
            modified: vec![],
        });
        assert!(none.contains("- **Total files**: 2\n"));
        assert!(none.ends_with("\nNo files needed cleaning.\n"));

        let some = format_markdown(&JavaCleanImportsResult {
            total_files: 2,
            modified_files: 1,
            modified: vec!["X.java".to_string()],
        });
        assert!(some.contains("## Modified Files\n\n"));
        assert!(some.contains("- `X.java`\n"));
    }
}
