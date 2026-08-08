<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: optimize-cis

## Learning: zsh does not word-split unquoted variables, silently voiding timing harnesses

- **Context**: benchmarking `rhino-cli` gate commands during plan authoring, using a
  `for c in "md links validate" ...; do $BIN $c; done` loop under `zsh`.
- **Observation**: `zsh` passed `"md links validate"` as a single argument, so every invocation
  exited with `unrecognized subcommand` in ~3 ms. The measurements looked like a spectacular result
  and were entirely fabricated by the harness. A second harness variant used `python3` subprocesses
  for timestamps, whose ~700 ms startup swamped the thing being measured. Both were caught only by
  checking exit codes and output, not by looking at the timings.
- **Why it might generalize**: this repo's default shell is `zsh`, and agents write ad-hoc timing
  loops routinely. A benchmarking-method rule — measure under `bash`, loop N times and divide, and
  always verify non-error execution before trusting a number — would catch this class every time.
  Same family as the recorded `grep -L`, `ls`-is-eza, and RTK-output-transform traps: a builtin
  quietly transforms the thing being measured and a false zero reads as a pass.

## Learning: cross-worktree cargo build-lock contention costs more than the disk it saves

- **Context**: first `cargo run` invocation of the session in a fresh worktree.
- **Observation**: blocked **65.05 s wall at 0.31 s user / 0.50 s sys** — pure lock wait, no
  compilation. Cause: `doctor --fix` symlinks every worktree's per-crate `target/` into one shared
  `~/.cache/ose-cargo-target/<repo>/<crate>`, so concurrent cargo processes across worktrees
  serialize on a single build-directory lock.
- **Why it might generalize**: the repo mandates `worktree-to-pr` and assumes concurrent agents on
  one disk, so shared-mutable-build-state is a standing design tension, not a one-off. Whether the
  disk saving is worth the serialization is a real design question — possibly answered by per-profile
  sharing or a content-addressed cache instead of a shared target dir.
