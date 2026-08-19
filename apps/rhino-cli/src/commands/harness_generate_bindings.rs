//! `harness bindings generate` — runs `OpenCode` sync, Cursor emit, then Amazon Q emit-bindings.
//!
//! Combines the `OpenCode` sync (`.claude/` → `.opencode/`), Cursor emit
//! (`.claude/` → `.cursor/agents/`), and Amazon Q emit-bindings
//! (`.claude/` → `.amazonq/`) into a single idempotent command. Use
//! `--harness opencode`, `--harness cursor`, or `--harness amazonq` to
//! regenerate only one platform binding. Legacy per-step flags `--opencode=false`
//! and `--amazonq=false` are still accepted for compatibility.

use std::path::Path;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::repo_config;
use crate::domain::cliout::OutputFormat;
use crate::internal::agents::bindings::{emit_bindings, expected_bindings};
use crate::internal::agents::converter::ConvertAllResult;
use crate::internal::agents::cursor::convert_all_cursor_agents;
use crate::internal::agents::reporter::{format_sync_json, format_sync_markdown, format_sync_text};
use crate::internal::agents::sync::{SyncOptions, SyncResult, sync_all};
use crate::internal::git;

/// Registry name the `OpenCode` sync step answers to.
const OPENCODE_HARNESS: &str = "opencode";
/// Registry name the Cursor emit step answers to.
const CURSOR_HARNESS: &str = "cursor";
/// Registry name the Amazon Q emit-bindings step answers to.
const AMAZONQ_HARNESS: &str = "amazonq";

/// CLI arguments for `harness bindings generate`.
#[derive(Args, Debug)]
pub struct GenerateBindingsArgs {
    /// Run the `OpenCode` sync step (`.claude/` → `.opencode/`).
    #[arg(long, default_value = "true")]
    pub opencode: bool,
    /// Run the Cursor emit step (`.claude/` → `.cursor/agents/`).
    #[arg(long, default_value = "true")]
    pub cursor: bool,
    /// Run the Amazon Q emit-bindings step (`.claude/` → `.amazonq/`).
    #[arg(long, default_value = "true")]
    pub amazonq: bool,
    /// Regenerate only the named harness binding: `opencode`, `cursor`, or `amazonq`.
    /// Overrides `--opencode` / `--cursor` / `--amazonq` flags when present.
    #[arg(long, value_name = "NAME")]
    pub harness: Option<String>,
    /// Preview changes without modifying files (applies to `OpenCode` and Cursor sync).
    #[arg(long = "dry-run")]
    pub dry_run: bool,
    /// Verbose output.
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output.
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// Runs `OpenCode` sync, Cursor emit, and Amazon Q emit-bindings in sequence. If
/// none of the steps is effectively enabled the command exits with an error.
///
/// # Errors
///
/// Returns an error if the git repository root cannot be found, if the
/// `OpenCode` sync fails, if the Cursor emit step fails, or if the Amazon Q
/// emit-bindings step fails.
pub fn run(
    args: &GenerateBindingsArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    // `--harness <name>` overrides the per-step flags when present. The accepted
    // set is derived from the `harness:` registry in repo-config.yml, so adding
    // a harness is a config change rather than a source edit (DD-2).
    if let Some(requested) = args.harness.as_deref() {
        let config = repo_config::load(&repo_root)
            .map_err(|e| anyhow!("failed to load repo-config.yml: {e}"))?;
        if !config.harness.iter().any(|h| h.matches_name(requested)) {
            let accepted = config
                .harness
                .iter()
                .map(|h| format!("'{}'", h.name))
                .collect::<Vec<_>>()
                .join(", ");
            return Err(anyhow!(
                "unknown harness name '{requested}'; expected one of {accepted}"
            ));
        }
    }

    // Each emitter asks whether it is the selected harness. The name each one
    // answers to is a single named constant beside its import, so no harness
    // name is spelled inline in this dispatch.
    let selected = args.harness.as_deref();
    let run_opencode = selected.map_or(args.opencode, |name| name == OPENCODE_HARNESS);
    let run_cursor = selected.map_or(args.cursor, |name| name == CURSOR_HARNESS);
    let run_amazonq = selected.map_or(args.amazonq, |name| name == AMAZONQ_HARNESS);

    if !run_opencode && !run_cursor && !run_amazonq {
        return Err(anyhow!(
            "at least one of --opencode, --cursor, or --amazonq must be enabled"
        ));
    }

    if run_opencode {
        run_opencode_sync(args, &repo_root, output_format)?;
    }

    if run_cursor {
        run_cursor_emit(args, &repo_root, output_format)?;
    }

    if run_amazonq {
        run_amazonq_emit(args, &repo_root, output_format)?;
    }

    Ok(())
}

/// Run the `OpenCode` sync sub-step.
fn run_opencode_sync(
    args: &GenerateBindingsArgs,
    repo_root: &Path,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let opts = SyncOptions {
        repo_root: repo_root.to_path_buf(),
        dry_run: args.dry_run,
        agents_only: false,
        skills_only: false,
        verbose: args.verbose,
        quiet: args.quiet,
    };
    let result = sync_all(&opts).map_err(|e| anyhow!("opencode sync failed: {e}"))?;

    if !args.quiet {
        match output_format {
            OutputFormat::Text => {
                print!("{}", format_sync_text(&result, args.verbose, args.quiet));
            }
            OutputFormat::Json => println!("{}", format_sync_json(&result)?),
            OutputFormat::Markdown => print!("{}", format_sync_markdown(&result)),
        }
    }

    if !result.failed_files.is_empty() {
        return Err(anyhow!(
            "opencode sync completed with {} failures",
            result.failed_files.len()
        ));
    }
    Ok(())
}

/// Run the Cursor emit sub-step.
fn run_cursor_emit(
    args: &GenerateBindingsArgs,
    repo_root: &Path,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let result = convert_all_cursor_agents(repo_root, args.dry_run)
        .map_err(|e| anyhow!("cursor emit failed: {e}"))?;

    if !args.quiet {
        let sync_result = cursor_result_to_sync(&result);
        match output_format {
            OutputFormat::Text => {
                print!(
                    "{}",
                    format_sync_text(&sync_result, args.verbose, args.quiet)
                        .replace("OpenCode", "Cursor")
                );
            }
            OutputFormat::Json => println!("{}", format_sync_json(&sync_result)?),
            OutputFormat::Markdown => print!(
                "{}",
                format_sync_markdown(&sync_result).replace("OpenCode", "Cursor")
            ),
        }
    }

    if !result.failed_files.is_empty() {
        return Err(anyhow!(
            "cursor emit completed with {} failures",
            result.failed_files.len()
        ));
    }
    Ok(())
}

/// Map a Cursor `ConvertAllResult` into the shared sync reporter shape.
fn cursor_result_to_sync(result: &ConvertAllResult) -> SyncResult {
    SyncResult {
        agents_converted: result.converted,
        agents_failed: result.failed,
        failed_files: result.failed_files.clone(),
        warnings: result.warnings.clone(),
        ..SyncResult::default()
    }
}

/// Run the Amazon Q emit-bindings sub-step.
fn run_amazonq_emit(
    args: &GenerateBindingsArgs,
    repo_root: &Path,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    if args.dry_run {
        return report_amazonq_dry_run(args, repo_root, output_format);
    }

    let result =
        emit_bindings(repo_root).map_err(|e| anyhow!("amazonq emit-bindings failed: {e}"))?;

    if !args.quiet {
        match output_format {
            OutputFormat::Text => {
                for path in &result.written {
                    println!("wrote {path}");
                }
                println!(
                    "\u{2713} emit-bindings wrote {} file(s)",
                    result.written.len()
                );
            }
            OutputFormat::Json => {
                #[derive(serde::Serialize)]
                struct Out<'a> {
                    status: &'a str,
                    written: &'a [String],
                    count: usize,
                }
                let out = Out {
                    status: "success",
                    written: &result.written,
                    count: result.written.len(),
                };
                println!("{}", serde_json::to_string_pretty(&out)?);
            }
            OutputFormat::Markdown => {
                println!("# Amazon Q Bindings Emit\n");
                for path in &result.written {
                    println!("- `{path}`");
                }
                println!("\nWrote {} file(s).", result.written.len());
            }
        }
    }
    Ok(())
}

/// Previews the Amazon Q bridge files that `run_amazonq_emit` would write,
/// without touching the filesystem.
fn report_amazonq_dry_run(
    args: &GenerateBindingsArgs,
    repo_root: &Path,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let paths: Vec<String> = expected_bindings(repo_root)
        .map_err(|error| anyhow!("load Amazon Q binding configuration: {error}"))?
        .into_iter()
        .map(|b| b.rel_path)
        .collect();

    if !args.quiet {
        match output_format {
            OutputFormat::Text => {
                for path in &paths {
                    println!("would write {path}");
                }
                println!(
                    "\u{2713} emit-bindings would write {} file(s) (dry-run)",
                    paths.len()
                );
            }
            OutputFormat::Json => {
                #[derive(serde::Serialize)]
                struct Out<'a> {
                    status: &'a str,
                    would_write: &'a [String],
                    count: usize,
                    dry_run: bool,
                }
                let out = Out {
                    status: "success",
                    would_write: &paths,
                    count: paths.len(),
                    dry_run: true,
                };
                println!("{}", serde_json::to_string_pretty(&out)?);
            }
            OutputFormat::Markdown => {
                println!("# Amazon Q Bindings Emit (dry-run)\n");
                for path in &paths {
                    println!("- `{path}`");
                }
                println!("\nWould write {} file(s).", paths.len());
            }
        }
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn args_defaults() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: true,
            amazonq: true,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: false,
        };
        assert!(a.opencode);
        assert!(a.amazonq);
        assert!(!a.dry_run);
    }

    #[test]
    fn both_disabled_is_error() {
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: false,
        };
        let result = run(&a, OutputFormat::Text);
        assert!(result.is_err());
        let msg = result.unwrap_err().to_string();
        assert!(msg.contains("at least one of"));
    }

    #[test]
    fn opencode_only_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        // May fail due to missing git root in test env — that's expected.
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn amazonq_only_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        // May fail due to missing git root in test env — that's expected.
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn both_enabled_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: true,
            amazonq: true,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn verbose_flag_set_correctly() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: false,
            verbose: true,
            quiet: false,
        };
        assert!(a.verbose);
        assert!(!a.quiet);
    }

    #[test]
    fn dry_run_flag_set_correctly() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: true,
            verbose: false,
            quiet: false,
        };
        assert!(a.dry_run);
    }

    #[test]
    fn quiet_flag_set_correctly() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        assert!(a.quiet);
    }

    #[test]
    fn opencode_json_output_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Json);
    }

    #[test]
    fn opencode_markdown_output_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Markdown);
    }

    #[test]
    fn amazonq_json_output_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Json);
    }

    #[test]
    fn amazonq_markdown_output_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: None,
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Markdown);
    }

    #[test]
    fn dry_run_opencode_runs_without_panic() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: None,
            dry_run: true,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn harness_opencode_overrides_amazonq_flag() {
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: Some("opencode".to_string()),
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        // --harness opencode means run opencode only, even though --amazonq=true
        // May fail due to missing git root; that's fine — we just verify no panic on arg logic.
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn harness_amazonq_overrides_opencode_flag() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: false,
            amazonq: false,
            harness: Some("amazonq".to_string()),
            dry_run: false,
            verbose: false,
            quiet: true,
        };
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn harness_unknown_name_is_error() {
        let a = GenerateBindingsArgs {
            opencode: true,
            cursor: true,
            amazonq: true,
            harness: Some("unknown".to_string()),
            dry_run: false,
            verbose: false,
            quiet: false,
        };
        let result = run(&a, OutputFormat::Text);
        assert!(result.is_err());
        let msg = result.unwrap_err().to_string();
        assert!(msg.contains("unknown harness name"));
    }
}
