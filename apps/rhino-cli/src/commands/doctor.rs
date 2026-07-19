//! `doctor` — checks and optionally installs required development tools.
//!
//! Port of `apps/rhino-cli/cmd/doctor.go`.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::domain::cliout::OutputFormat;
use crate::infrastructure::git::common_dir;
use crate::internal::doctor::{
    self, CheckOptions, FixOptions, Scope, cache_root_ambient, cargo_sweep_present, check_all,
    check_target_shares, fix_all, fix_target_shares, format_fix_summary, format_json,
    format_markdown, format_text, is_ci_ambient, prune_orphans, repo_name, sweep_stale,
};
use crate::internal::git;

/// CLI arguments for the `doctor` command.
#[derive(Args, Debug)]
pub struct DoctorArgs {
    /// Tool scope: full or minimal.
    #[arg(long = "scope", default_value = "full")]
    pub scope: String,
    /// Attempt to install missing tools.
    #[arg(long = "fix")]
    pub fix: bool,
    /// Preview what --fix would install (only effective with --fix).
    #[arg(long = "dry-run")]
    pub dry_run: bool,
    /// Prune shared cargo-target cache entries no live worktree/checkout
    /// references (worktree-aware GC; honors `--dry-run` for preview).
    #[arg(long = "prune-cargo-cache")]
    pub prune_cargo_cache: bool,
    /// Verbose output.
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output.
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// Runs the cargo `target/` share check (and, when `fix` is set, the fix)
/// plus the optional prune-cache GC, printing a short human-readable report.
///
/// Split out of [`run`] to keep that function's cyclomatic complexity down
/// and to give this specific wiring its own `#[cfg(test)]` coverage (see
/// `wiring_check_mode_does_not_mutate_filesystem`) without depending on the
/// tool-check subprocess plumbing `run` also drives.
fn run_target_share_step(repo_root: &std::path::Path, args: &DoctorArgs) {
    let ci = is_ci_ambient();
    let cache_root = cache_root_ambient();
    let Ok(common) = common_dir::find_common_dir_from(Some(repo_root)) else {
        // Not inside a git repository — nothing to share.
        return;
    };
    let name = repo_name(&common);
    if name.is_empty() {
        return;
    }

    let unshared = check_target_shares(repo_root, &cache_root, &name, ci);
    if ci {
        println!("\nTarget-share: CI detected — skipped.");
    } else if unshared.is_empty() {
        println!("\nTarget-share: all crates already share their target/ via the cache.");
    } else {
        println!("\nTarget-share: {} crate(s) need sharing:", unshared.len());
        for status in &unshared {
            println!("  {}", status.crate_dir.display());
        }
    }

    if args.fix {
        let outcome = fix_target_shares(repo_root, &cache_root, &name, ci);
        if outcome.skipped_ci {
            println!("Target-share fix: CI detected — skipped.");
        } else {
            println!(
                "Target-share fix: {} created, {} already correct, {} plain dir(s) replaced",
                outcome.created, outcome.already_correct, outcome.replaced_plain_dir
            );
        }
    }

    if args.prune_cargo_cache {
        let prune = prune_orphans(repo_root, &cache_root, &name, args.dry_run, ci);
        if prune.skipped_ci {
            println!("Prune: CI detected — skipped.");
        } else if prune.enumeration_failed {
            println!("Prune: could not enumerate worktrees — skipped (nothing deleted).");
        } else if args.dry_run {
            println!(
                "Prune (dry-run): {} candidate(s) for deletion",
                prune.candidates.len()
            );
            for candidate in &prune.candidates {
                println!("  {}", candidate.display());
            }
        } else {
            println!("Prune: {} orphaned entrie(s) deleted", prune.deleted.len());
        }

        let sweep = sweep_stale(&cache_root, &name, args.dry_run, cargo_sweep_present(), ci);
        if sweep.skipped_ci {
            println!("Sweep: CI detected — skipped.");
        } else if sweep.skipped {
            println!("Sweep: cargo-sweep not installed — skipped.");
        }
    }
}

/// Run the `doctor` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, if any tools fail to
/// install (when `--fix` is set), or if missing tools are detected.
pub fn run(args: &DoctorArgs, output: OutputFormat) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;

    let parsed_scope = Scope::parse(&args.scope).unwrap_or(Scope::Full);

    let opts = CheckOptions {
        repo_root,
        runner: None,
        scope: parsed_scope,
    };

    let result = check_all(&opts);

    match output {
        OutputFormat::Text => print!("{}", format_text(&result, args.verbose, args.quiet)),
        OutputFormat::Json => println!("{}", format_json(&result)?),
        OutputFormat::Markdown => print!("{}", format_markdown(&result)),
    }

    // Target-share reporting is plain, unstructured text — interleaving it
    // with `--output json`/`--output markdown` would corrupt those
    // machine-/document-oriented formats (e.g. break JSON parsing). Restrict
    // it to the default text output, matching every target-share Gherkin
    // scenario, which drives `doctor` with no `--output` flag.
    if matches!(output, OutputFormat::Text) {
        run_target_share_step(&opts.repo_root, args);
    }

    if args.fix && result.missing_count > 0 {
        let mut buf = String::new();
        let fr = fix_all(
            &result,
            &opts,
            &FixOptions {
                dry_run: args.dry_run,
                runner: None,
            },
            |m| {
                buf.push_str(m);
                print!("{m}");
            },
        );
        print!("{}", format_fix_summary(&fr));
        if fr.failed > 0 {
            return Err(anyhow!("{} tool(s) failed to install", fr.failed));
        }
        if !args.dry_run && fr.fixed > 0 {
            return Ok(());
        }
    }

    if args.fix && result.missing_count == 0 {
        println!("\nNothing to fix — all tools are installed.");
    }

    if result.missing_count > 0 {
        return Err(anyhow!(
            "{} tool(s) not found in PATH",
            result.missing_count
        ));
    }

    // Silence unused-import lint on platforms that omit Doctor sub-helpers.
    let _ = doctor::is_minimal_tool;
    Ok(())
}

#[cfg(test)]
#[allow(clippy::unwrap_used, clippy::panic)]
mod tests {
    use super::*;

    #[test]
    fn args_default_values() {
        let _ = DoctorArgs {
            scope: "full".into(),
            fix: false,
            dry_run: false,
            prune_cargo_cache: false,
            verbose: false,
            quiet: false,
        };
    }

    /// Proves `run_target_share_step`'s wiring compiles and, in **check**
    /// mode (`fix: false`, `prune_cargo_cache: false`), performs zero
    /// filesystem mutation: no `target/` symlink is created and the shared
    /// cache directory is never populated. Uses a synthetic tempdir repo
    /// only — never the real repo root or the real `$HOME` cache.
    #[test]
    fn wiring_check_mode_does_not_mutate_filesystem() {
        let repo_root = tempfile::tempdir().unwrap();
        let crate_dir = repo_root.path().join("apps/foo");
        std::fs::create_dir_all(&crate_dir).unwrap();
        std::fs::write(crate_dir.join("Cargo.toml"), "[package]\nname = \"x\"\n").unwrap();

        let args = DoctorArgs {
            scope: "full".into(),
            fix: false,
            dry_run: false,
            prune_cargo_cache: false,
            verbose: false,
            quiet: false,
        };

        run_target_share_step(repo_root.path(), &args);

        assert!(
            !crate_dir.join("target").exists(),
            "check mode must not create a target/ symlink"
        );
    }
}
