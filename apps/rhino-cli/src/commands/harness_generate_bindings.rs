//! `harness bindings generate` — regenerates every generated-tier harness binding.
//!
//! Walks the `harness:` registry in `repo-config.yml` and runs each
//! generated-tier harness's emitter: the `OpenCode` sync (`.claude/agents/` →
//! `.opencode/agents/`) and the Codex emitter (`.claude/agents/` →
//! `.codex/agents/`).
//! Pass `--harness <NAME>` to regenerate a single binding; the accepted names
//! are exactly the registry entries, so adding a harness is a config change
//! rather than a source edit (DD-2).

use std::path::Path;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::agents::codex::emit_codex_bindings;
use crate::application::agents::skills_mirror::emit_skills_mirrors;
use crate::application::repo_config;
use crate::domain::cliout::OutputFormat;
use crate::internal::agents::reporter::{format_sync_json, format_sync_markdown, format_sync_text};
use crate::internal::agents::sync::{SyncOptions, sync_all};
use crate::internal::git;

/// Registry name the `OpenCode` sync step answers to.
const OPENCODE_HARNESS: &str = "opencode";

/// Registry name the Codex emitter answers to.
const CODEX_HARNESS: &str = "codex";

/// CLI arguments for `harness bindings generate`.
#[derive(Args, Debug)]
pub struct GenerateBindingsArgs {
    /// Regenerate only the named harness binding. Accepted values are the
    /// `harness:` registry entries in `repo-config.yml`. Omit to regenerate all.
    #[arg(long, value_name = "NAME")]
    pub harness: Option<String>,
    /// Preview changes without modifying files.
    #[arg(long = "dry-run")]
    pub dry_run: bool,
    /// Verbose output.
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output.
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// Regenerates every generated-tier harness binding, or just the one named by
/// `--harness`.
///
/// # Errors
///
/// Returns an error if the git repository root cannot be found, if
/// `repo-config.yml` cannot be loaded, if `--harness` names a harness absent
/// from the registry, or if an emitter fails.
pub fn run(
    args: &GenerateBindingsArgs,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    // The accepted `--harness` set is derived from the registry, never from a
    // hard-coded list, so a registry contraction rejects the dropped name
    // automatically (DD-2).
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

    // Each emitter asks whether it is the selected harness. The name it answers
    // to is a single named constant beside its import, so no harness name is
    // spelled inline in this dispatch.
    let selected = args.harness.as_deref();
    if selected.is_none_or(|name| name == OPENCODE_HARNESS) {
        run_opencode_sync(args, &repo_root, output_format)?;
    }
    if selected.is_none_or(|name| name == CODEX_HARNESS) {
        run_codex_emit(args, &repo_root)?;
    }

    Ok(())
}

/// Run the Codex emit sub-step: one `.codex/agents/<name>.toml` per Claude
/// agent, plus the generated region of `.codex/config.toml`.
fn run_codex_emit(args: &GenerateBindingsArgs, repo_root: &Path) -> std::result::Result<(), Error> {
    let emitted = emit_codex_bindings(repo_root, args.dry_run)
        .map_err(|e| anyhow!("codex emit failed: {e}"))?;

    if !args.quiet {
        println!("codex: {} agent(s) emitted", emitted.result.converted);
    }
    if !emitted.result.failed_files.is_empty() {
        return Err(anyhow!(
            "codex emit completed with {} failures: {}",
            emitted.result.failed_files.len(),
            emitted.result.failed_files.join(", ")
        ));
    }

    // The skills mirror is registry-driven: it runs for whichever harness
    // entries declare both `skills-dir` and `skills-mirrors`, so it needs no
    // flag of its own and no harness name spelled here.
    let mirror = emit_skills_mirrors(repo_root, args.dry_run)
        .map_err(|e| anyhow!("skills mirror failed: {e}"))?;
    if !args.quiet {
        println!(
            "codex: {} skill file(s) mirrored, {} stale removed",
            mirror.copied, mirror.removed
        );
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

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    /// Build args with every flag at its default.
    fn args(harness: Option<&str>) -> GenerateBindingsArgs {
        GenerateBindingsArgs {
            harness: harness.map(str::to_string),
            dry_run: false,
            verbose: false,
            quiet: true,
        }
    }

    #[test]
    fn args_defaults() {
        let a = args(None);
        assert!(a.harness.is_none());
        assert!(!a.dry_run);
        assert!(!a.verbose);
    }

    #[test]
    fn no_harness_selector_runs_without_panic() {
        // May fail due to missing git root in test env — that's expected.
        let _ = run(&args(None), OutputFormat::Text);
    }

    #[test]
    fn harness_opencode_runs_without_panic() {
        let _ = run(&args(Some(OPENCODE_HARNESS)), OutputFormat::Text);
    }

    // No `run(Some(CODEX_HARNESS))` smoke test here: the existing `run()`-calling
    // tests resolve the git root from the process CWD, so they are only as
    // isolated as the whole test binary's CWD. The Codex emit path is covered by
    // `application::agents::codex`'s unit tests and by `tests/codex_binding.rs`,
    // neither of which depends on process-global state.

    #[test]
    fn verbose_flag_set_correctly() {
        let mut a = args(None);
        a.verbose = true;
        a.quiet = false;
        assert!(a.verbose);
        assert!(!a.quiet);
    }

    #[test]
    fn dry_run_flag_set_correctly() {
        let mut a = args(None);
        a.dry_run = true;
        assert!(a.dry_run);
    }

    #[test]
    fn quiet_flag_set_correctly() {
        assert!(args(None).quiet);
    }

    #[test]
    fn opencode_json_output_runs_without_panic() {
        let _ = run(&args(Some(OPENCODE_HARNESS)), OutputFormat::Json);
    }

    #[test]
    fn opencode_markdown_output_runs_without_panic() {
        let _ = run(&args(Some(OPENCODE_HARNESS)), OutputFormat::Markdown);
    }

    #[test]
    fn dry_run_opencode_runs_without_panic() {
        let mut a = args(Some(OPENCODE_HARNESS));
        a.dry_run = true;
        let _ = run(&a, OutputFormat::Text);
    }

    #[test]
    fn harness_amazonq_is_rejected_after_registry_contraction() {
        let result = run(&args(Some("amazonq")), OutputFormat::Text);
        assert!(result.is_err());
        let msg = result.unwrap_err().to_string();
        assert!(msg.contains("unknown harness name"), "got: {msg}");
    }

    #[test]
    fn harness_amazonq_dry_run_is_rejected_before_reaching_any_emitter() {
        let mut a = args(Some("amazonq"));
        a.dry_run = true;
        let result = run(&a, OutputFormat::Text);
        assert!(result.is_err());
        let msg = result.unwrap_err().to_string();
        assert!(msg.contains("unknown harness name"), "got: {msg}");
    }

    #[test]
    fn harness_unknown_name_is_error() {
        let result = run(&args(Some("unknown")), OutputFormat::Text);
        assert!(result.is_err());
        let msg = result.unwrap_err().to_string();
        assert!(msg.contains("unknown harness name"));
    }
}
