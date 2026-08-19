//! The single generation path every binding emitter runs behind.
//!
//! `harness bindings generate` writes into the repository; divergence triage
//! writes the same output into a scratch tree and compares. Both call [`emit`],
//! so "what the generator produces" has exactly one definition and the two
//! cannot drift into disagreeing about it.

use std::path::Path;

use super::codex::{CodexEmitResult, emit_codex_bindings};
use super::skills_mirror::{MirrorResult, emit_skills_mirrors};
use super::sync::{SyncOptions, SyncResult, sync_all};

/// Registry name the `OpenCode` sync step answers to.
pub const OPENCODE_HARNESS: &str = "opencode";

/// Registry name the Codex emitter answers to.
pub const CODEX_HARNESS: &str = "codex";

/// What one generation run produced, one field per emitter.
///
/// Each field is `None` when a `--harness` selector excluded that emitter,
/// which is why the selector cannot silently be reported as a zero-count run.
#[derive(Debug, Default)]
pub struct EmitOutcome {
    /// `.claude/agents/` → `.opencode/agents/` sync.
    pub sync: Option<SyncResult>,
    /// `.claude/agents/` → `.codex/agents/` plus the `.codex/config.toml` region.
    pub codex: Option<CodexEmitResult>,
    /// `.claude/skills/` → `.agents/skills/` mirror.
    pub mirror: Option<MirrorResult>,
}

impl EmitOutcome {
    /// Every path an emitter reported as failed, across every emitter that ran.
    #[must_use]
    pub fn failed_files(&self) -> Vec<String> {
        let mut all: Vec<String> = self
            .sync
            .as_ref()
            .map(|s| s.failed_files.clone())
            .unwrap_or_default();
        if let Some(codex) = self.codex.as_ref() {
            all.extend(codex.result.failed_files.iter().cloned());
        }
        all
    }
}

/// Run the generated-tier emitters `selected` names, or all of them when it is
/// `None`.
///
/// The skills mirror rides with the Codex selection rather than answering to a
/// flag of its own: it is registry-driven, running for whichever entries
/// declare both `skills-dir` and `skills-mirrors`.
///
/// # Errors
///
/// Returns an error if any emitter fails.
pub fn emit(
    repo_root: &Path,
    selected: Option<&str>,
    dry_run: bool,
    verbose: bool,
    quiet: bool,
) -> Result<EmitOutcome, String> {
    let mut outcome = EmitOutcome::default();

    if selected.is_none_or(|name| name == OPENCODE_HARNESS) {
        outcome.sync = Some(
            sync_all(&SyncOptions {
                repo_root: repo_root.to_path_buf(),
                dry_run,
                agents_only: false,
                skills_only: false,
                verbose,
                quiet,
            })
            .map_err(|e| format!("opencode sync failed: {e}"))?,
        );
    }

    if selected.is_none_or(|name| name == CODEX_HARNESS) {
        outcome.codex = Some(
            emit_codex_bindings(repo_root, dry_run)
                .map_err(|e| format!("codex emit failed: {e}"))?,
        );
        outcome.mirror = Some(
            emit_skills_mirrors(repo_root, dry_run)
                .map_err(|e| format!("skills mirror failed: {e}"))?,
        );
    }

    Ok(outcome)
}
