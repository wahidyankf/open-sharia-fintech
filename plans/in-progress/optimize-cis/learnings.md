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

## Learning: cross-phase forward-references in a checklist item's own text can hard-error

- **Context**: Phase 2 item 5 (`rhino-bin.sh` creation) specified `cargo build --profile gate` and
  `target/gate/rhino-cli`, but `[profile.gate]` is not added to `Cargo.toml` until Phase 4 — which
  even carries its own dedicated step to repoint `rhino-bin.sh` at `--profile gate`, proving the
  sequencing was always meant to be later.
- **Observation**: had the item been executed literally, the first test exercising the shim's
  build-fallback path would have hard-errored with `error: profile`gate`is not defined`. Caught
  only because the executing agent proactively flagged the missing profile section before writing
  the script, not by any earlier plan-quality-gate pass — 5 `plan-checker`/`plan-fixer` iterations
  had already run clean over this exact text.
- **Why it might generalize**: `plan-checker` currently validates structure/completeness, not
  whether a step's own command text is satisfiable given what prior phases have actually built by
  that point. A phase-ordering / forward-reference check (does this step's command reference an
  artifact — profile, flag, file — that a later phase's step is the one that creates it?) would
  catch this class before execution, not during it.

## Learning: a byte-identity-governed file trips its local parity-manifest gate on the very next push

- **Context**: Phase 2's `emit.rs` edit (DD-1 resolver-shim rendering) is inside the zero-carve-out
  `apps/rhino-cli` byte-identity boundary (`src/`, `Cargo.toml`, `Cargo.lock`, `project.json`,
  `LICENSE`, the shared Gherkin tree) spanning `ose-public`/`ose-primer`/`ose-private`.
- **Observation**: the first `git push` after committing the edit was blocked by the local
  `parity-manifest` pre-push gate — not a cross-repo diff, just this repo's own recorded checksum of
  `emit.rs` going stale the moment the file changed. Fix was `rhino-cli parity manifest generate`
  (regenerates the local checksum), committed as its own follow-up commit, then the push succeeded.
  The gate's own error text states the real obligation plainly: the identical change must still
  propagate to the other repos — regenerating the local manifest does not satisfy that, it only
  unblocks this repo's own push.
- **Why it might generalize**: any future phase (this plan's own Phase 10, or any unrelated future
  edit) touching a byte-identity-governed `apps/rhino-cli` file should expect this same local gate to
  fire on the very next push, immediately, before any cross-repo work has happened — it is a
  same-repo self-consistency check, not a signal that propagation is already done or overdue.
