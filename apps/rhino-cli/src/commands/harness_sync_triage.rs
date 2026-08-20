//! `harness sync triage` — reports every generated mirror that is not what the
//! generator produces right now, and says which side moved.
//!
//! One formatter per outcome, so the hard-stop message cannot drift into
//! sounding recoverable by sharing wording with the case that is.

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::agents::triage::{Divergence, Outcome, Side, TriageReport, triage};
use crate::internal::git;

/// CLI arguments for `harness sync triage`.
#[derive(Args, Debug)]
pub struct SyncTriageArgs {
    /// Verbose output (name every compared file, not only the diverged ones).
    #[arg(long, short = 'v')]
    pub verbose: bool,
    /// Quiet output (summary line only).
    #[arg(long, short = 'q')]
    pub quiet: bool,
}

/// Run the `harness sync triage` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, if regeneration fails, or
/// if any generated file diverged.
pub fn run(args: &SyncTriageArgs) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let report = triage(&repo_root).map_err(|e| anyhow!("{e}"))?;

    println!(
        "harness sync triage: {} generated file(s) compared, {} divergence(s)",
        report.compared,
        report.divergences.len()
    );
    if !args.quiet {
        for divergence in &report.divergences {
            print!("{}", format_divergence(divergence));
        }
    }

    if report.divergences.is_empty() {
        return Ok(());
    }
    Err(anyhow!("{}", verdict_summary(&report)))
}

/// The single sentence the non-zero exit carries.
fn verdict_summary(report: &TriageReport) -> String {
    match report.verdict() {
        // Unreachable while a caller only asks for a summary after finding a
        // divergence, but stated rather than defaulted so a fourth outcome
        // would not silently land here.
        Outcome::InSync => "no divergence".to_string(),
        Outcome::BothDiverged => format!(
            "{} divergence(s), at least one with edits on BOTH sides — reconcile by hand",
            report.divergences.len()
        ),
        Outcome::OneSided(_) => format!("{} divergence(s)", report.divergences.len()),
    }
}

/// One block per diverged file. Each outcome has its own formatter: the
/// both-diverged case must never be rendered by code that also knows how to
/// offer a resolution.
fn format_divergence(divergence: &Divergence) -> String {
    let canonical = divergence.canonical.as_deref().unwrap_or("<undeclared>");
    match divergence.outcome {
        Outcome::InSync => String::new(),
        Outcome::OneSided(Side::Mirror) => format!(
            "\u{2718} {mirror} — the mirror was hand-edited\n    \
             canonical source: {canonical}\n    \
             keep the edit:    rhino-cli harness sync promote --from {mirror}\n    \
             discard the edit: rhino-cli harness bindings generate\n",
            mirror = divergence.mirror,
        ),
        Outcome::OneSided(Side::Canonical) => format!(
            "\u{2718} {mirror} — the canonical source is ahead of this mirror\n    \
             canonical source: {canonical}\n    \
             regenerate:       rhino-cli harness bindings generate\n",
            mirror = divergence.mirror,
        ),
        Outcome::BothDiverged => format!(
            "\u{2718} {mirror} — HARD STOP: both sides were hand-edited\n    \
             canonical source: {canonical}\n    \
             Both files carry edits this tool cannot reconcile. No automatic\n    \
             resolution exists and none is offered. Reconcile them by hand,\n    \
             then re-run.\n",
            mirror = divergence.mirror,
        ),
    }
}

#[cfg(test)]
#[allow(clippy::unwrap_used)]
mod tests {
    use super::*;

    fn divergence(outcome: Outcome) -> Divergence {
        Divergence {
            mirror: ".opencode/agents/alpha.md".to_string(),
            canonical: Some(".claude/agents/alpha.md".to_string()),
            outcome,
        }
    }

    #[test]
    fn mirror_side_offers_promotion() {
        let out = format_divergence(&divergence(Outcome::OneSided(Side::Mirror)));
        assert!(out.contains("harness sync promote --from .opencode/agents/alpha.md"));
        assert!(out.contains(".claude/agents/alpha.md"));
    }

    #[test]
    fn canonical_side_offers_regeneration_and_never_promotion() {
        let out = format_divergence(&divergence(Outcome::OneSided(Side::Canonical)));
        assert!(out.contains("harness bindings generate"));
        assert!(!out.contains("promote"), "got: {out}");
    }

    #[test]
    fn hard_stop_offers_no_resolution_at_all() {
        let out = format_divergence(&divergence(Outcome::BothDiverged));
        assert!(out.contains("HARD STOP"));
        assert!(!out.contains("promote"), "got: {out}");
        assert!(!out.contains("bindings generate"), "got: {out}");
    }

    #[test]
    fn in_sync_renders_nothing() {
        assert!(format_divergence(&divergence(Outcome::InSync)).is_empty());
    }

    #[test]
    fn summary_names_the_hard_stop() {
        let report = TriageReport {
            compared: 2,
            divergences: vec![divergence(Outcome::BothDiverged)],
        };
        assert!(verdict_summary(&report).contains("BOTH sides"));
    }

    #[test]
    fn undeclared_canonical_is_stated_rather_than_omitted() {
        let mut d = divergence(Outcome::OneSided(Side::Mirror));
        d.canonical = None;
        assert!(format_divergence(&d).contains("<undeclared>"));
    }
}
