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

## Learning: isolated single-shot benchmarks overstated a batched-execution saving by ~4x

- **Context**: `tech-docs.md` §A.2 benchmarked prettier/markdownlint-cli2's pre-DD-2 "current form"
  as standalone `npx --no -- <tool>` invocations (622 ms / 441 ms) to derive DD-2's claimed ~250 ms
  per-tool saving and the plan's "3,047 ms → 683 ms" M1 projection, which Phase 3's own gate then
  encoded as a hard `≤900 ms` acceptance clause.
- **Observation**: the real pre-commit path never paid `npx` per tool. `repo-config.yml`'s actual
  commands were always bare (`prettier --write`, no `npx` prefix); only the outer
  `apps/rhino-cli/src/commands/gate/run.rs` batch runner spawns `npx --no -- lint-staged` **once**
  for the whole batch, and prettier/markdownlint-cli2 ran as its children via lint-staged's own
  `node_modules/.bin`-inclusive `PATH` — the isolated per-tool `npx` tax the benchmark measured was
  never actually being paid twice in the integrated path. Real measured Phase 3 M1 saving: −138 ms
  (−5.4 % vs Phase 2), not the ~500+ ms the isolated benchmark implied. Phase 3 Gate's `≤900 ms`
  acceptance clause was corrected in place (see `delivery.md` Phase 3 Gate) rather than forced to a
  false PASS.
- **Why it might generalize**: a **candidate follow-up** worth triaging (a `DD-10`-class idea, not
  authored or scoped by this plan): the one remaining process-spawn cost neither DD-1 nor DD-2
  touches is that single outer `npx --no -- lint-staged` spawn in `run.rs` — replacing it with a
  direct `node_modules/.bin/lint-staged` call is outside `GateKind` command-rendering (DD-1/DD-2's
  actual mechanism) and was never an authored step here. More generally: a per-invocation isolated
  benchmark does not necessarily predict its saving inside a batched/child-process execution model —
  measure the actual integrated path before hard-gating a phase on the isolated number.

## Learning: a new gate-emission.feature scenario needs step bindings in TWO places, every time

- **Context**: both Phase 2 (resolver-shim scenario) and Phase 3 (node_modules/.bin scenario) added
  a scenario to `gate-emission.feature` and bound it at the `emit.rs` unit-test level, per the
  phase's own authored RED step. Both times, `apps/rhino-cli/tests/gate_specs.rs`'s cucumber harness
  — which scans the whole `gate/` feature directory regardless of which scenario a given phase is
  "working on" — hit an undefined-step failure on the very next `test:quick`/pre-push run, requiring
  a same-day follow-up fix commit each time.
- **Observation**: this is now a confirmed repeat, not a one-off. The pre-push `test-quick` gate did
  catch it correctly both times (nothing shipped broken), but only after a full commit+push cycle,
  costing a wasted push attempt and a follow-up commit each time.
- **Why it might generalize**: any future phase in this plan (or any future rhino-cli change) that
  adds a `gate-emission.feature`/`gate-execution.feature`/etc. scenario must budget for TWO binding
  sites, not one — the unit-test module AND `gate_specs.rs` — and should verify
  `cargo test --test gate_specs` locally (not just the narrower `--lib gate::emit`) before ever
  committing, not rely on the pre-push gate to catch it after the fact. Worth flagging for Phase 12
  triage as a documentation gap: the RED-step convention in this plan's own delivery.md items only
  ever names the unit-test command, never the integration-test command, for scenarios of this kind.
