<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: rust-cargo-target-dir-sharing

## Baseline measurements (filled in during Phase 0 / Phase 3)

- **Disk "before"** (Phase 0): _record the `du -sh` table across worktrees here._
- **Crate `build.outputs` snapshot** (Phase 0): _record the `jq` output for ayokoding-cli, ose-cli,
  rust-commons, rhino-cli here._
- **Disk "after"** (Phase 3): _record the shared-cache `du -sh` and the dedup comparison here._
- **Three-way byte-identity `diff`** (Phase 6): _record the `diff -rq` result (expect 0) here._

<!--
Entry shape:

## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized — real $HOME paths reduced to $HOME)
- **Why it might generalize**: the litmus reasoning
-->
