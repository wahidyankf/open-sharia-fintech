//! `specs scaffold dart` — generates Dart package scaffolding (`pubspec.yaml`,
//! `lib/` barrel library) around generated Dart contract types.
//!
//! Post-processes `openapi-generator-cli`'s Dart output for the
//! `crud-fe-dart-flutterweb` codegen pipeline: `flutter pub get` requires a
//! valid `pubspec.yaml`, and the `OpenAPI` generator does not emit one for the
//! Dart model-only target. See `crate::internal::contracts::dart_scaffold`
//! for the scaffolding algorithm.

use std::fmt::Write as _;

use anyhow::Error;
use clap::Args;
use serde::Serialize;

use crate::domain::cliout::OutputFormat;
use crate::internal::contracts::dart_scaffold::scaffold_dart;
use crate::internal::contracts::types::{DartScaffoldOptions, DartScaffoldResult};

/// CLI arguments for `specs scaffold dart`.
#[derive(Args, Debug)]
pub struct ScaffoldDartArgs {
    /// Root directory for the generated Dart package.
    #[arg(long, value_name = "dir")]
    pub dir: Option<String>,
}

/// JSON output envelope for `specs scaffold dart`.
#[derive(Serialize)]
struct DartScaffoldJson<'a> {
    /// Always `"success"` — the command errors out rather than reporting failure.
    status: &'a str,
    /// Whether `pubspec.yaml` was written.
    pubspec_created: bool,
    /// Whether the barrel library was written.
    barrel_created: bool,
    /// Basenames of the model files that were scaffolded.
    model_files: &'a [String],
}

/// Run the `specs scaffold dart` command.
///
/// # Errors
///
/// Returns an error when the target directory cannot be resolved, the model
/// glob cannot be evaluated, or `pubspec.yaml`/the barrel library cannot be
/// written.
pub fn run(args: &ScaffoldDartArgs, output: OutputFormat) -> std::result::Result<(), Error> {
    let dir = args.dir.as_deref().unwrap_or(".");
    let abs_dir = std::path::absolute(dir)?;

    let opts = DartScaffoldOptions {
        dir: abs_dir.to_string_lossy().into_owned(),
    };
    let result = scaffold_dart(&opts)?;

    match output {
        OutputFormat::Text => print!("{}", format_text(&result)),
        OutputFormat::Json => print!("{}", format_json(&result)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&result)),
    }
    Ok(())
}

/// Formats the scaffold result as human-readable text.
fn format_text(result: &DartScaffoldResult) -> String {
    let mut out = String::new();
    let _ = writeln!(
        out,
        "Dart scaffold created: pubspec.yaml + barrel library ({} model files).",
        result.model_files.len()
    );
    for f in &result.model_files {
        let _ = writeln!(out, "  {f}");
    }
    out
}

/// Formats the scaffold result as a JSON envelope.
///
/// # Errors
///
/// Returns an error if JSON serialization fails.
fn format_json(result: &DartScaffoldResult) -> std::result::Result<String, Error> {
    let env = DartScaffoldJson {
        status: "success",
        pubspec_created: result.pubspec_created,
        barrel_created: result.barrel_created,
        model_files: &result.model_files,
    };
    let mut s = serde_json::to_string_pretty(&env)?;
    s.push('\n');
    Ok(s)
}

/// Formats the scaffold result as Markdown.
fn format_markdown(result: &DartScaffoldResult) -> String {
    let mut out = String::new();
    out.push_str("# Dart Contract Scaffold Report\n\n");

    let pubspec_status = if result.pubspec_created {
        "created"
    } else {
        "not created"
    };
    let barrel_status = if result.barrel_created {
        "created"
    } else {
        "not created"
    };
    let _ = writeln!(out, "- **pubspec.yaml**: {pubspec_status}");
    let _ = writeln!(out, "- **Barrel library**: {barrel_status}");
    let _ = writeln!(out, "- **Model files**: {}", result.model_files.len());

    if result.model_files.is_empty() {
        return out;
    }

    out.push_str("\n## Model Files\n\n");
    for f in &result.model_files {
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
        let a = ScaffoldDartArgs { dir: None };
        assert!(a.dir.is_none());
    }

    // --- Regression: `specs scaffold dart` must actually write `pubspec.yaml`
    // and the barrel library. The phase 9a/b/c command-surface rationalization
    // replaced the real scaffolder with a permanent no-op stub ("dormant in
    // ose-public") while `internal::contracts::dart_scaffold` (the working
    // algorithm, with its own passing unit tests) sat unwired and unreachable.
    // A polyglot consumer's `crud-fe-dart-flutterweb` Nx target pipes real
    // OpenAPI-generated Dart models through this exact command before running
    // `flutter pub get`, so a no-op regressed that pipeline silently. ---

    #[test]
    fn run_actually_writes_pubspec_and_barrel() {
        let tmp = TempDir::new().unwrap();
        let model_dir = tmp.path().join("lib/model");
        fs::create_dir_all(&model_dir).unwrap();
        fs::write(model_dir.join("user.dart"), "// user model\n").unwrap();

        let args = ScaffoldDartArgs {
            dir: Some(tmp.path().to_string_lossy().into_owned()),
        };
        run(&args, OutputFormat::Text).unwrap();

        let pubspec = fs::read_to_string(tmp.path().join("pubspec.yaml")).unwrap();
        assert!(pubspec.contains("name: crud_contracts"), "{pubspec}");

        let barrel = fs::read_to_string(tmp.path().join("lib/crud_contracts.dart")).unwrap();
        assert!(barrel.contains("part 'model/user.dart';"), "{barrel}");
    }

    #[test]
    fn format_text_lists_model_files() {
        let r = DartScaffoldResult {
            pubspec_created: true,
            barrel_created: true,
            model_files: vec!["a.dart".to_string(), "b.dart".to_string()],
        };
        let s = format_text(&r);
        assert!(s.starts_with(
            "Dart scaffold created: pubspec.yaml + barrel library (2 model files).\n"
        ));
        assert!(s.contains("  a.dart\n"));
    }

    #[test]
    fn format_json_shape() {
        let r = DartScaffoldResult {
            pubspec_created: true,
            barrel_created: true,
            model_files: vec!["m.dart".to_string()],
        };
        let s = format_json(&r).unwrap();
        let v: serde_json::Value = serde_json::from_str(&s).unwrap();
        assert_eq!(v["status"], "success");
        assert_eq!(v["pubspec_created"], true);
        assert_eq!(v["barrel_created"], true);
        assert_eq!(v["model_files"][0], "m.dart");
    }

    #[test]
    fn format_markdown_shapes() {
        let empty = format_markdown(&DartScaffoldResult {
            pubspec_created: false,
            barrel_created: false,
            model_files: vec![],
        });
        assert!(empty.contains("- **pubspec.yaml**: not created\n"));
        assert!(empty.contains("- **Model files**: 0\n"));
        assert!(!empty.contains("## Model Files"));

        let some = format_markdown(&DartScaffoldResult {
            pubspec_created: true,
            barrel_created: true,
            model_files: vec!["x.dart".to_string()],
        });
        assert!(some.contains("- **pubspec.yaml**: created\n"));
        assert!(some.contains("## Model Files\n\n"));
        assert!(some.contains("- `x.dart`\n"));
    }
}
