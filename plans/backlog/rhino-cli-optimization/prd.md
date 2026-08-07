# Product Requirements — rhino-cli Optimization

## Personas

| Persona                     | Who                                                              | What they need from this plan                                                             |
| --------------------------- | ---------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| **Maintainer**              | The repository owner, running commits and pushes all day         | Gates that finish in seconds, and a machine that does not lose 16 GB to a build toolchain |
| **Executing agent**         | An AI agent working a plan through the Husky and Nx gate surface | Fast, deterministic gate turnaround; no silent skips that let a broken change through     |
| **rhino-cli contributor**   | Whoever next edits the 195 source files                          | A compiler that rejects an indexing panic before it reaches a gate at runtime             |
| **Sibling-repo maintainer** | Whoever works in `ose-private` under the byte-identity gate      | Changes that land as one unit, so parity never breaks mid-flight                          |
| **Next-plan executor**      | Whoever runs `beaver-nest-repo-consolidation` after this plan    | Steps that still resolve — no citation of a file or command form this plan removed        |

## Epics

| Epic | Name                         | Delivers                                                                                     |
| ---- | ---------------------------- | -------------------------------------------------------------------------------------------- |
| A    | Build speed                  | The gate binary rebuilds in under 10 s after a one-line edit                                 |
| B    | Disk footprint               | ~10 GB reclaimed, and hygiene encoded so it does not regrow                                  |
| C    | Type safety                  | `indexing_slicing` and `arithmetic_side_effects` denied crate-wide, plus the cheap adjacents |
| D    | Gated language re-evaluation | A measured, human-decided answer to "should this be a different language" — only if needed   |
| E    | Documentation propagation    | Every document restating a fact this plan invalidates is corrected, in both repos            |

## User stories

**A1** — As the maintainer, I want the gate binary to rebuild in seconds after an edit, so that a
one-line change does not cost more than a minute of waiting before the gate even starts.

**A2** — As the maintainer, I want every gate invocation site to resolve the binary through one
mechanism, so that changing how the binary is built is one edit rather than 53.

**A3** — As a contributor, I want the integration-test suite to link the library once rather than
22 times, so that `cargo check --all-targets` stops paying a fixed cost that buys nothing.

**A4** — As an executing agent, I want `nx affected` to detect changes confined to
`apps/rhino-cli/src/**/*.rs`, so that a rhino-cli-only commit is actually tested before it lands.

**A5** — As the next-plan executor, I want every downstream step that cites a file or command form
this plan removes to be updated in the same delivery, so that the following plan does not fail on a
path that no longer exists.

**B1** — As the maintainer, I want rustup toolchains that no repository pins to be reclaimed, so
that the largest single term in the disk footprint stops being owned by nobody.

**B2** — As the maintainer, I want the footprint to stay reclaimed after a `rustup update`, so that
the cleanup is a permanent change rather than a one-time event.

**B3** — As the maintainer, I want the dev profile to stop emitting 255 MB of debug info I do not
use, so that the target directory a working day produces is proportional to the work done.

**C1** — As a contributor, I want the compiler to reject an unchecked index, so that a malformed
Markdown file in the working tree cannot abort a quality gate with a bare panic.

**C2** — As a contributor, I want every lint suppression to carry a written reason, so that a
considered exception is distinguishable from a silenced warning.

**C3** — As the maintainer, I want the observable CLI contract to be provably unchanged by all of
the above, so that a safety improvement cannot silently become a behaviour change.

**D1** — As the maintainer, I want the language question answered against post-optimization numbers
and closed by an explicit human decision, so that it stops resurfacing.

**E1** — As a contributor, I want every governance rule this plan changes to be swept across its
register, its checker, and every index that names it, so that a rule is not documented in one place
and enforced in none.

**E2** — As a contributor, I want the documents outside `repo-governance/` — `AGENTS.md`,
`CLAUDE.md`, the `docs/reference/` set, app READMEs, agent and skill files — corrected too, so that
no instruction file teaches an invocation form that no longer exists.

**E3** — As the maintainer, I want the plan to touch exactly `ose-public` and `ose-private`, so that
a delayed-sync repo never blocks a delivery unit and no work lands in a repository about to be
archived.

## Acceptance criteria

Each scenario carries exactly one `Given`, one `When`, and one `Then`; additional steps chain with
`And` or `But`, per the Gherkin step-keyword cardinality rule.

### Epic A — Build speed

```gherkin
Feature: rhino-cli build speed

  Scenario: A one-line edit rebuilds the gate binary in under ten seconds
    Given the repository is checked out with a warm build cache
    And a single line of "apps/rhino-cli/src/lib.rs" has been modified
    When the gate binary is rebuilt through the profile the gates invoke
    Then the rebuild completes in under 10 seconds
    And the resulting binary produces byte-identical output to the frozen baseline binary

  Scenario: No invocation site shells out to a release-profile build
    Given the repository is checked out at the head of the delivery branch
    When every "project.json", Husky shim, and workflow file is scanned for "cargo run --release"
    Then zero occurrences remain that target "apps/rhino-cli/Cargo.toml"
    And every gate invocation resolves the binary through the single shared indirection

  Scenario: The integration-test suite links the library once
    Given "apps/rhino-cli/Cargo.toml" previously declared 22 "harness = false" test binaries
    When the consolidated test suite is built and run
    Then exactly one integration-test binary is produced
    And the set of executed test names is identical to the pre-consolidation set

  Scenario: nx affected detects a rhino-cli-only Rust change
    Given a commit whose only changed file is under "apps/rhino-cli/src/"
    When "nx show projects --affected" is run against that commit
    Then "rhino-cli" appears in the output
    And the pre-push gate runs "rhino-cli:test:quick" for that commit without a manual override

  Scenario: Downstream plan citations survive this plan
    Given the downstream consolidation plan cites rhino-cli test paths and command forms
    When this plan's delivery removes any cited path or command form
    Then the downstream plan is updated in the same delivery unit
    And no downstream step references a path that no longer resolves
```

### Epic B — Disk footprint

```gherkin
Feature: Rust toolchain and build-cache footprint

  Scenario: Superseded toolchains are reclaimed
    Given six rustup toolchains are installed and exactly one is pinned by a sibling repository
    When the toolchain reclamation step runs
    Then only toolchains pinned by at least one sibling "rust-toolchain.toml" remain installed
    And every sibling repository still builds without a manual toolchain reinstall

  Scenario: The footprint does not regrow undetected
    Given the toolchain reclamation has already run
    And a new unpinned toolchain has since been installed
    When "npm run doctor" is run
    Then it reports the unpinned toolchain as reclaimable
    But it does not remove the toolchain without an explicit fix invocation

  Scenario: The dev profile stops emitting unused debug info
    Given the dev profile previously produced a 615 MB target directory
    When a clean dev build runs under the tuned profile
    Then the target directory is under 400 MB
    And backtraces from a deliberately failing test still identify the failing source line
```

### Epic C — Type safety

```gherkin
Feature: rhino-cli compile-time guarantees

  Scenario: Unchecked indexing is rejected crate-wide
    Given "clippy::indexing_slicing" is set to deny in "apps/rhino-cli/Cargo.toml"
    When clippy runs across every target in the crate
    Then it reports zero "indexing_slicing" diagnostics
    And every remaining index site is either a checked access or carries an allow with a reason

  Scenario: Unchecked arithmetic is rejected crate-wide
    Given "clippy::arithmetic_side_effects" is set to deny in "apps/rhino-cli/Cargo.toml"
    When clippy runs across every target in the crate
    Then it reports zero "arithmetic_side_effects" diagnostics
    And no allow-listed type pair is introduced that suppresses a genuinely unbounded computation

  Scenario: Every suppression carries a written reason
    Given "clippy::allow_attributes_without_reason" is set to deny
    When clippy runs across every target in the crate
    Then it reports zero diagnostics
    And each of the 190 pre-existing allow attributes states why the lint does not apply

  Scenario: A malformed input file fails cleanly instead of panicking
    Given a deliberately truncated Markdown fixture is placed in a scratch working tree
    When the corresponding rhino-cli validator is run against it
    Then the command exits with its documented non-zero error code
    But it does not abort with a panic message

  Scenario: The observable contract survives the sweep
    Given the frozen pre-sweep binary is retained as the baseline
    When every rhino-cli subcommand is run against the same working tree under both binaries
    Then stdout, stderr, and the exit code match byte for byte for every subcommand
```

### Epic D — Gated language re-evaluation

```gherkin
Feature: Language re-evaluation gate

  Scenario: The language question is entered only on measured failure
    Given Axes A, B, and C have all been delivered and measured
    When the post-optimization figures are compared against the plan's targets
    Then Axis D is entered only if at least one target remains unmet
    And the specific unmet target is recorded as the question the spike must answer

  Scenario: The language decision is closed by a human
    Given an Axis D spike has produced measured build, disk, and tooling figures
    When the go/no-go gate is reached
    Then a human records an explicit decision with its rationale
    And the decision is written into the plan's learnings regardless of which way it goes
```

### Epic E — Documentation propagation

```gherkin
Feature: Documentation reflects the optimized rhino-cli

  Scenario: A changed governance rule is swept across every surface
    Given this plan established a rule that gate targets use a fast build profile
    When "repo-rules-maker" propagates that rule
    Then the convention doc, its register entry, the checker rule list, and every naming index agree
    And "repo-rules-checker" reports no unresolved findings

  Scenario: Instruction files stop teaching a removed invocation form
    Given "AGENTS.md" and the agent and skill files previously cited "cargo run --release"
    When the documentation sweep completes
    Then a grep for that invocation form against rhino-cli returns zero matches outside plan history
    But the same grep returned a non-zero count before the sweep

  Scenario: Generated harness mirrors stay generated
    Given the sweep edited files under ".claude/"
    When "npm run generate:bindings" and "npm run validate:sync" are run
    Then validate:sync passes
    And no mirror under ".opencode/", ".cursor/", or ".amazonq/" was hand-edited

  Scenario: Both bound repositories carry the same documentation
    Given the documentation sweep landed in "ose-public"
    When the same delivery unit is applied to "ose-private"
    Then both repos state the same invocation form, test layout, lint contract, and boundary
    But no change is made to "ose-primer" or "beaver-nest"
```

## Product scope

### In scope

- Behaviour-preserving changes to how `apps/rhino-cli` is built, invoked, and lint-gated.
- The gate invocation surface: 27 `project.json` files, 3 Husky shims, one GitHub Actions workflow.
- Machine-level Rust toolchain and build-cache hygiene, plus the automation that maintains it.
- Propagation of every code change to `ose-private` under the byte-identity gate.
- Updating the downstream `beaver-nest-repo-consolidation` plan wherever this plan invalidates one
  of its steps.

### Out of scope

- Any change to what `rhino-cli` does. No new validators, no changed output, no changed exit codes.
- Splitting the crate into a Cargo workspace — a disqualified lever, reasoned in `tech-docs.md`.
- Adopting `sccache`, a replacement linker, Cranelift, or the nightly parallel frontend, each of
  which research disqualified for this platform or this workload.
- `beaver-nest`'s `rhino-cli` fork, which the downstream plan discards rather than reconciles.

## Product risks

| ID  | Risk                                                                                                 | Mitigation                                                                                |
| --- | ---------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------- |
| P1  | A faster build profile produces a binary slow enough that 21 gate invocations per push erase the win | The gate measures **end-to-end wall clock**, not compile time alone                       |
| P2  | The Axis C sweep silently changes error messages, which some gate output depends on                  | Shadow-diff covers stderr as well as stdout, byte for byte                                |
| P3  | Consolidating test binaries changes which tests run without changing how many                        | The executed test-name set is asserted equal, not just the count                          |
| P4  | Reclaiming toolchains breaks a sibling repo that pins one this repo does not                         | Every sibling's `rust-toolchain.toml` is read before any uninstall                        |
| P5  | Deferring the language question makes it resurface indefinitely                                      | Axis D closes it either way with a recorded human decision, entered on a measured trigger |
| P6  | The downstream plan silently breaks because a cited path or command form disappeared                 | The hand-off obligation is enumerated per artefact and verified at the Phase 12 gate      |
