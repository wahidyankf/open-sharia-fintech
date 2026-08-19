//! `harness bindings generate` — regenerates every generated-tier harness binding.
//!
//! Walks the `harness:` registry in `repo-config.yml` and runs each
//! generated-tier harness's emitter: the `OpenCode` sync (`.claude/agents/` →
//! `.opencode/agents/`) and the Codex emitter (`.claude/agents/` →
//! `.codex/agents/`).
//! Pass `--harness <NAME>` to regenerate a single binding; the accepted names
//! are exactly the registry entries, so adding a harness is a config change
//! rather than a source edit (DD-2).

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::agents::emit::{EmitOutcome, emit};
use crate::application::agents::ownership::guard_emitter_targets;
use crate::application::repo_config;
use crate::domain::cliout::OutputFormat;
use crate::internal::agents::reporter::{format_sync_json, format_sync_markdown, format_sync_text};
use crate::internal::git;

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

    // Refuse before the first write when any emitter's output directory is
    // declared `source`. A generator that overwrites hand-authored canonical
    // input destroys the thing every mirror is generated from, so this fails
    // up front rather than reporting the damage afterwards (US-8).
    guard_emitter_targets(&repo_root).map_err(|e| anyhow!("{e}"))?;

    // Generation itself lives in `application::agents::emit`, which divergence
    // triage also calls. Selecting the emitters here instead would give the two
    // callers two definitions of "what the generator produces", and drift
    // between them is exactly the failure this command exists to prevent.
    let outcome = emit(
        &repo_root,
        args.harness.as_deref(),
        args.dry_run,
        args.verbose,
        args.quiet,
    )
    .map_err(|e| anyhow!("{e}"))?;

    report(args, &outcome, output_format)?;

    let failed = outcome.failed_files();
    if !failed.is_empty() {
        return Err(anyhow!(
            "generation completed with {} failure(s): {}",
            failed.len(),
            failed.join(", ")
        ));
    }
    Ok(())
}

/// Print whatever ran. Each emitter reports only when it was selected, so a
/// `--harness` run never prints a zero that reads like "nothing to do".
fn report(
    args: &GenerateBindingsArgs,
    outcome: &EmitOutcome,
    output_format: OutputFormat,
) -> std::result::Result<(), Error> {
    if args.quiet {
        return Ok(());
    }
    if let Some(sync) = outcome.sync.as_ref() {
        match output_format {
            OutputFormat::Text => {
                print!("{}", format_sync_text(sync, args.verbose, args.quiet));
            }
            OutputFormat::Json => println!("{}", format_sync_json(sync)?),
            OutputFormat::Markdown => print!("{}", format_sync_markdown(sync)),
        }
    }
    if let Some(codex) = outcome.codex.as_ref() {
        println!("codex: {} agent(s) emitted", codex.result.converted);
    }
    if let Some(mirror) = outcome.mirror.as_ref() {
        println!(
            "codex: {} skill file(s) mirrored, {} stale removed",
            mirror.copied, mirror.removed
        );
    }
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;
    use crate::application::agents::emit::OPENCODE_HARNESS;

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
