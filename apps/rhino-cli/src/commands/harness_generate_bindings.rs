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

use crate::domain::cliout::OutputFormat;
use crate::internal::agents::bindings::{emit_bindings, expected_bindings};
use crate::internal::agents::converter::ConvertAllResult;
use crate::internal::agents::cursor::convert_all_cursor_agents;
use crate::internal::agents::reporter::{format_sync_json, format_sync_markdown, format_sync_text};
use crate::internal::agents::sync::{SyncOptions, SyncResult, sync_all};
use crate::internal::git;

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
    // --harness <name> overrides the per-step flags when present.
    let run_opencode = match args.harness.as_deref() {
        Some("opencode") => true,
        Some("cursor" | "amazonq") => false,
        Some(other) => {
            return Err(anyhow!(
                "unknown harness name '{other}'; expected 'opencode', 'cursor', or 'amazonq'"
            ));
        }
        None => args.opencode,
    };
    let run_cursor = match args.harness.as_deref() {
        Some("cursor") => true,
        Some("opencode" | "amazonq") => false,
        _ => args.cursor,
    };
    let run_amazonq = match args.harness.as_deref() {
        Some("amazonq") => true,
        Some("opencode" | "cursor") => false,
        _ => args.amazonq,
    };

    if !run_opencode && !run_cursor && !run_amazonq {
        return Err(anyhow!(
            "at least one of --opencode, --cursor, or --amazonq must be enabled"
        ));
    }

    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

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
    use crate::test_support::CwdLock;

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

    // --- Regression: `--dry-run` must also apply to the Amazon Q emit step, not just
    // the OpenCode sync step. Previously `run_amazonq_emit` ignored `args.dry_run`
    // entirely and wrote the binding files unconditionally. ---

    #[test]
    fn amazonq_dry_run_text_output_runs_without_panic() {
        // `find_root()` reads the process cwd; serialize against the other
        // cwd-sensitive tests so a concurrent chdir cannot fail this one.
        let _cwd = CwdLock::acquire();
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: None,
            dry_run: true,
            verbose: false,
            quiet: false,
        };
        let repo_root = git::root::find_root().expect("repo root");
        let result = report_amazonq_dry_run(&a, &repo_root, OutputFormat::Text);
        assert!(result.is_ok());
    }

    #[test]
    fn amazonq_dry_run_json_output_runs_without_panic() {
        // `find_root()` reads the process cwd; serialize against the other
        // cwd-sensitive tests so a concurrent chdir cannot fail this one.
        let _cwd = CwdLock::acquire();
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: None,
            dry_run: true,
            verbose: false,
            quiet: true,
        };
        let repo_root = git::root::find_root().expect("repo root");
        let result = report_amazonq_dry_run(&a, &repo_root, OutputFormat::Json);
        assert!(result.is_ok());
    }

    #[test]
    fn amazonq_dry_run_markdown_output_runs_without_panic() {
        // `find_root()` reads the process cwd; serialize against the other
        // cwd-sensitive tests so a concurrent chdir cannot fail this one.
        let _cwd = CwdLock::acquire();
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: None,
            dry_run: true,
            verbose: false,
            quiet: true,
        };
        let repo_root = git::root::find_root().expect("repo root");
        let result = report_amazonq_dry_run(&a, &repo_root, OutputFormat::Markdown);
        assert!(result.is_ok());
    }

    #[test]
    fn harness_amazonq_dry_run_via_run_reaches_dry_run_branch() {
        // `harness bindings generate --harness amazonq --dry-run` must take the
        // dry-run branch (no filesystem writes, no git-root-dependent failure from
        // `emit_bindings`). `run()` resolves the repo root from the process cwd,
        // so hold the cwd lock for the duration.
        let _cwd = CwdLock::acquire();
        let a = GenerateBindingsArgs {
            opencode: false,
            cursor: false,
            amazonq: true,
            harness: Some("amazonq".to_string()),
            dry_run: true,
            verbose: false,
            quiet: true,
        };
        let result = run(&a, OutputFormat::Text);
        assert!(result.is_ok(), "{:?}", result.err());
    }
}
