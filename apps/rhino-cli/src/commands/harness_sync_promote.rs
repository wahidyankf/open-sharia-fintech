//! `harness sync promote` — proposes a mirror edit as a patch against canonical
//! source, and never writes canonical source itself.
//!
//! Cross-harness translation is lossy: an `OpenCode` or Codex mirror cannot
//! carry every canonical field. Promotion therefore emits a diff for a human to
//! apply, plus the list of canonical fields the editing harness never showed
//! them (DD-4, DD-13).

use std::fmt::Write as _;

use anyhow::{Error, anyhow};
use clap::Args;

use crate::application::agents::triage::{PromoteProposal, promote};
use crate::internal::git;

/// CLI arguments for `harness sync promote`.
#[derive(Args, Debug)]
pub struct SyncPromoteArgs {
    /// Repository-relative path of the generated mirror carrying the edit.
    #[arg(long = "from", value_name = "MIRROR")]
    pub from: String,
}

/// Run the `harness sync promote` command.
///
/// # Errors
///
/// Returns an error if the git root cannot be found, if `--from` does not name
/// a generated binding file, or if no canonical source is declared for it.
pub fn run(args: &SyncPromoteArgs) -> std::result::Result<(), Error> {
    let repo_root =
        git::root::find_root().map_err(|e| anyhow!("failed to find git repository root: {e}"))?;
    let proposal = promote(&repo_root, &args.from).map_err(|e| anyhow!("{e}"))?;
    print!("{}", format_proposal(&proposal));
    Ok(())
}

/// Render the proposal. Nothing here writes; the closing line says so, because
/// a diff on stdout otherwise reads like a report of something already done.
fn format_proposal(proposal: &PromoteProposal) -> String {
    let mut out = format!(
        "proposed change to {} (from {})\n\n",
        proposal.canonical, proposal.mirror
    );
    if proposal.both_diverged {
        out.push_str(
            "HARD STOP: both the mirror and its canonical source were hand-edited since HEAD. \
             This diff's removed lines include the canonical-side edit — review it carefully \
             before applying, or reconcile the two sides by hand instead.\n\n",
        );
    }
    if proposal.diff.is_empty() {
        out.push_str("no change: the mirror carries nothing the canonical source lacks\n\n");
    } else {
        out.push_str(&proposal.diff);
        out.push('\n');
    }

    out.push_str("At risk of loss — canonical fields this harness cannot carry:\n");
    if proposal.at_risk.is_empty() {
        out.push_str("  (none)\n");
    } else {
        for (field, reason) in &proposal.at_risk {
            let _ = writeln!(out, "  - {field} ({reason})");
        }
    }
    let _ = writeln!(
        out,
        "\nNothing was written. Apply the diff to {} yourself to accept it.",
        proposal.canonical
    );
    out
}

#[cfg(test)]
mod tests {
    use super::*;

    fn proposal(at_risk: Vec<(String, String)>, diff: &str) -> PromoteProposal {
        PromoteProposal {
            mirror: ".opencode/agents/alpha.md".to_string(),
            canonical: ".claude/agents/alpha.md".to_string(),
            diff: diff.to_string(),
            at_risk,
            both_diverged: false,
        }
    }

    #[test]
    fn lists_every_at_risk_field_with_its_reason() {
        let out = format_proposal(&proposal(
            vec![
                (
                    "permissionMode".to_string(),
                    "use opencode permission block".to_string(),
                ),
                ("isolation".to_string(), "claude-only".to_string()),
            ],
            "--- a/x\n+++ b/x\n",
        ));
        assert!(out.contains("- permissionMode (use opencode permission block)"));
        assert!(out.contains("- isolation (claude-only)"));
    }

    #[test]
    fn an_agent_with_no_unrepresentable_field_lists_none() {
        let out = format_proposal(&proposal(Vec::new(), "--- a/x\n+++ b/x\n"));
        assert!(out.contains("(none)"));
        assert!(!out.contains("permissionMode"));
    }

    #[test]
    fn always_states_that_nothing_was_written() {
        let out = format_proposal(&proposal(Vec::new(), ""));
        assert!(out.contains("Nothing was written"));
        assert!(out.contains("no change"));
    }

    // Regression for M1: `promote` carries no hard-stop signal when it is
    // called directly (without `triage` having run first) against a pair
    // where both sides were hand-edited.
    #[test]
    fn a_both_diverged_proposal_prints_a_hard_stop_warning() {
        let mut p = proposal(Vec::new(), "--- a/x\n+++ b/x\n");
        p.both_diverged = true;
        let out = format_proposal(&p);
        assert!(out.contains("HARD STOP"));
        assert!(out.contains("both the mirror and its canonical source"));
    }

    #[test]
    fn an_in_sync_proposal_prints_no_hard_stop_warning() {
        let out = format_proposal(&proposal(Vec::new(), "--- a/x\n+++ b/x\n"));
        assert!(!out.contains("HARD STOP"));
    }
}
