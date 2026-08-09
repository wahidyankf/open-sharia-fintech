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

## Learning: `cargo hack check --rust-version` installs a major.minor toolchain distinct from the pinned patch

- **Context**: Phase 4's MSRV bump set `rust-version = "1.95.0"` in all four `ose-public` manifests,
  matching the already-installed `1.95.0-aarch64-apple-darwin` `rustup` toolchain exactly. The
  `compat:min-version` Nx target (`cargo hack --manifest-path apps/rhino-cli/Cargo.toml check
--rust-version`) was expected to need no new toolchain as a result.
- **Observation**: it installed one anyway — a **new**, separate `1.95-aarch64-apple-darwin`
  toolchain (1.3 GB), distinct from the already-present `1.95.0-aarch64-apple-darwin`. `cargo-hack`
  appears to resolve/invoke the major.minor form of the pinned `rust-version` rather than the exact
  patch, and `rustup` treats `1.95` and `1.95.0` as separate installed toolchains even though they
  currently resolve to the same release.
- **Why it might generalize**: Phase 9 (disk hygiene, this plan's own rustup-toolchain-pruning phase)
  should expect and account for this extra toolchain when auditing what's installed and why — it is
  a legitimate, reproducible side effect of running `compat:min-version` at all, not drift or a
  concurrent-agent artifact. Any future MSRV bump anywhere in this repo should expect the same
  `X.Y`-vs-`X.Y.Z` toolchain duplication from this exact Nx target.

## Learning: a plan step can add a Gherkin scenario that no phase can yet bind — 2nd instance of the cross-phase forward-reference class

- **Context**: Phase 5's own delivery.md text instructed adding the AC-9 and AC-10 CI-topology
  scenarios (prebuilt-binary consumption, conditional `npm ci` skip) to `gate-execution.feature`
  during Phase 5 — but AC-9 describes the `build-rhino` job Phase 6 creates and AC-10 describes the
  conditional node-setup input Phase 7 creates. Neither exists in `.github/workflows/pr-quality-gate.yml`
  yet at Phase 5.
- **Observation**: `specs gherkin-cardinality validate` passed immediately (it only checks keyword
  structure), so nothing caught this at authoring time. The real failure surfaced one layer deeper:
  `apps/rhino-cli/tests/gate_specs.rs`'s cucumber suite requires a literal, **passing** step binding
  for every scenario in the entire `gherkin/gate/` tree regardless of which phase "owns" it, and there
  was no truthful way to bind either scenario — the behavior they assert doesn't exist yet. Forcing a
  binding would have meant fabricating a fixture that asserts against nothing real.
- **Why it might generalize**: this is the same forward-reference class already logged above
  ("cross-phase forward-references in a checklist item's own text can hard-error"), but at the
  Gherkin-coverage layer instead of a Cargo-profile layer — proof it's a general planning-time gap,
  not a one-off. Fixed here by moving the scenario authoring out of Phase 5 and into Phase 6/Phase 7
  themselves, right where each behavior actually lands. The general rule this suggests for
  `plan-checker`: a step that adds a Gherkin scenario should be checked not just for keyword structure
  but for whether the behavior it describes is created by an **earlier or same** phase — never a
  later one — since this repo's coverage tools require whole-tree, always-live bindings.

## Learning: "does this job run git diff/nx affected" must be checked one layer deeper than the workflow YAML

- **Context**: Phase 6's fetch-depth reduction item reasoned that `build-rhino`, `enumerate`, and
  `gate` could all safely drop `fetch-depth: 0` because none of their `run:` steps invoke `nx
affected` or `git diff` directly in the workflow YAML.
- **Observation**: that reasoning was correct for `build-rhino` and `enumerate`, but wrong for `gate`
  — its single `run:` step dispatches `rhino-cli gate run --surface=ci --group=<id>`, which internally
  fans out to several affected-file-type and Nx-scoped gates (`format-verify-*`,
  `shell-docker-actions`, `specs-structure`) that themselves run `git diff`/`nx affected` against
  `origin/main` one process down. A shallow clone has no `origin/main` ref, so 3 of 6 matrix groups
  failed live in CI (`31281760676`) with "unknown revision" / "git diff ... failed" — not a flake,
  a real gap in the analysis, caught only once the real workflow ran end-to-end.
- **Why it might generalize**: "does this job need full history" can't be answered by grepping the
  job's own YAML for `git diff`/`nx affected` — it has to be answered by asking what the job's
  dispatched CLI/script does _underneath_, including any commands that further dispatch to other
  tools. Any future fetch-depth or similar shallow-clone optimization in this repo's CI should trace
  the full call chain of what a job actually invokes, not just its literal `run:` lines.

## Learning: `gate list --by-group`'s hand-wired exclusion and `gate run --group`'s membership must be the same filter, not two independent implementations of "which gates belong to this group"

- **Context**: Phase 7's `run-npm-ci` wiring derives per-group node-need from `matrix.group.doctor_tools`,
  which comes from `gate list --format=json --by-group` — a code path that already excludes hand-wired
  gates (`gate/list.rs`'s `visible_gates` filter, JSON format only) from the emitted group membership.
- **Observation**: `gate/run.rs`'s `resolve_group_gates` (the code path `gate run --surface=ci --group=<id>`
  actually executes) shared the group-_bucketing_ predicate with `list.rs` (`gates_in_ci_group`) but not
  its hand-wired _exclusion_. So the `specs` CI group's emitted membership (used to compute
  `run-npm-ci`) was `[specs-gherkin-cardinality]`, while the group actually **executed** was
  `[specs-gherkin-cardinality, specs-structure]` — `specs-structure` is `kind: nx`/`wiring: hand-wired`
  and needs `node_modules`, which `run-npm-ci=false` (correctly computed from the visible membership)
  then stopped installing. Live CI (`31284082843`) failed with "Could not find Nx modules" the moment
  this stopped being masked by `npm ci` always running unconditionally beforehand — a pre-existing,
  silently-redundant double-execution of a hand-wired gate that Phase 7's optimization exposed rather
  than caused.
- **Why it might generalize**: whenever two code paths both claim to answer "which gates are in this
  group" (one for _reporting/enumeration_, one for _execution_), a filter applied to one but not the
  other is invisible until something downstream depends on the two agreeing — here, until execution
  behavior (`npm ci` or not) started depending on enumeration output (`doctor_tools`). The fix folds
  the same hand-wired exclusion into `resolve_group_gates` so both paths compute identical membership
  from one predicate, closing the class rather than the single instance.

## Learning: A "pre-install the pinned toolchain" race fix only works if it installs the toolchain _name_ the racing tool actually asks rustup for

- **Context**: The `setup-rust` composite action already carried a pre-install step whose stated
  purpose was to defeat the rustup download race that parallel `cargo hack check --rust-version`
  tasks trigger. Its loop read each crate's declared `rust-version` and ran
  `rustup toolchain install "$v"`, with `$v` being the full `1.95.0` string.
- **Observation**: `cargo hack --rust-version` does not request `1.95.0` — it resolves the floor to
  its **major-minor** form and shells out to `rustup toolchain add 1.95 --no-self-update`. rustup
  stores `1.95` and `1.95.0` as **distinct toolchains in distinct directories**, so pre-installing
  `1.95.0` satisfied nothing: all four Rust crates still raced rustup for `1.95` in parallel, and
  three of four failed live in CI (`31285020618`) with a bare
  `error: process didn't exit successfully: rustup toolchain add 1.95 --no-self-update (exit status: 1)`.
  The mitigation had been in place and passing review for several phases while providing zero
  protection — its failure mode looked exactly like the original flake it was written to fix, which
  is why four prior occurrences were all classified as accepted infra flake rather than a live bug.
- **Second defect, same step**: the extraction used `grep -rhoP`. BSD grep (macOS) has no `-P`, so on
  a non-GNU-grep host the loop iterates over an empty list, installs nothing, and still exits 0 —
  a silent no-op that a local run cannot distinguish from success. Rewritten with portable `sed`.
- **Why it might generalize**: a mitigation that names a resource must name it in the **same
  vocabulary the consumer uses**, and the way to verify that is to observe the consumer's actual
  invocation, not to re-read the mitigation's own intent. The regression test added here does exactly
  that — it executes the real checked-in script with a stub `rustup` on `PATH` and asserts on the
  toolchain names the script genuinely requests, so any future drift between "what we pre-install"
  and "what the tool asks for" fails locally instead of after ~50 minutes of CI.

## Learning: A wall-clock target can only be moved by the critical path, so check which job actually holds it before applying the remedy the plan prescribes

- **Context**: Phase 7 Gate treats an M4 (CI wall-clock p50) regression as a hard stop and prescribes
  a specific remedy — "re-balance group composition before proceeding." Measured p50 came in at
  1,219 s against a 974.5 s baseline: nominally +25.1 %, squarely in hard-stop territory.
- **Observation**: the per-job timeline showed the run's critical path was the **TypeScript quality
  gate at 1,033 s**, and that same job took 1,030 s and 1,018 s on this branch _before_ the topology
  change — it was untouched. All six gate groups finished by 01:03:45 in a run that ended 01:16:41,
  putting them ~13 minutes clear of the critical path. Re-balancing group composition could not have
  moved wall-clock by a single second. The real gap was diff scope: this branch edits
  `repo-config.yml`, `.github/`, and governance docs, so every TypeScript project is affected,
  whereas the Phase 0 baseline sampled 18 much narrower PRs.
- **Why it might generalize**: a plan can correctly identify a metric, correctly set a threshold, and
  still hard-code a remedy aimed at the wrong component — because the remedy is written before anyone
  has seen a real timeline. Wall-clock in a fan-out DAG is a **max**, not a sum: it is insensitive to
  everything off the critical path, so any wall-clock remedy must first prove the thing it changes is
  _on_ it. The same asymmetry explains why M3 (runner-seconds, a sum) fell 47.6 % in the same runs
  where M4 rose — the two metrics were never going to move together, and a plan that treats both as
  symptoms of one cause will mis-diagnose whichever one it reads second.
