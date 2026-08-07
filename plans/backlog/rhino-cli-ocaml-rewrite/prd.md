# PRD — rhino-cli OCaml Rewrite

## Product overview

`rhino-cli` is the repository's governance binary. This plan replaces its implementation language —
Rust to OCaml — while holding its **observable contract absolutely fixed**: the same commands, the
same flags, the same exit codes, and byte-identical stdout and stderr.

The product deliverable is therefore unusual: from the outside, **nothing changes**. Every
acceptance criterion below is a statement about something staying the same, or about a developer-
experience or governance-coverage property improving. There is no new user-facing feature.

Two genuinely new artefacts ship alongside:

1. `libs/ocaml-rhino-gherkin` — a Gherkin parser and test harness, because no maintained OCaml
   Cucumber implementation exists.
2. Replacements for the four other OCaml tooling gaps (linter configuration, dependency audit,
   coverage threshold, reproducible lockfile) so no governance gate is silently lost.

## Personas

The maintainer wears several hats; several agents consume the output. Neither list contains external
stakeholders.

| Persona                                  | Needs from this plan                                                               |
| ---------------------------------------- | ---------------------------------------------------------------------------------- |
| **Maintainer as tool author**            | A fast edit-compile-check loop on the binary every gate runs through               |
| **Maintainer as governance owner**       | Absolute confidence no gate weakened during the swap                               |
| **Maintainer as machine owner**          | A smaller resident toolchain footprint                                             |
| **Plan-executing AI agent**              | A binary that builds fast enough that a plan step does not stall on a 68 s rebuild |
| **`repo-setup-manager`**                 | `npm run doctor -- --fix` provisions the OCaml toolchain in a fresh worktree       |
| **`swe-code-checker`**                   | An OCaml ruleset to validate against — it has none today                           |
| **`ci-checker`**                         | An Nx target set that still satisfies the mandatory-target convention              |
| **`repo-harness-compatibility-checker`** | A regenerated three-repo parity manifest that still verifies                       |

## User stories

### Epic A — Decide on evidence, not expectation

**A1.** As the **maintainer as machine owner**, I want the reclaimable Rust footprint reclaimed and
re-measured **before** the rewrite is committed to, so that I know how much of the 16 GB was ever
about the language.

**A2.** As the **maintainer as tool author**, I want the release-profile settings removed from the
inner dev loop and the incremental rebuild re-measured, so that I know how much of the 68.4 s was
ever about the compiler.

**A3.** As the **maintainer as governance owner**, I want each of the five OCaml tooling gaps to have
a demonstrated working replacement before any porting begins, so that the rewrite cannot quietly
trade correctness enforcement for build speed.

**A4.** As the **maintainer**, I want a single explicit go/no-go decision point holding the Phase 1
control numbers next to the Phase 2 spike numbers, so that ~59,000 lines of reimplementation across
three repositories is a choice I make against data rather than a commitment I inherit.

### Epic B — Preserve the contract exactly

**B1.** As the **maintainer as governance owner**, I want every one of the 441 Gherkin scenarios to
pass against the OCaml binary, so that behaviour parity is proven by the existing spec corpus rather
than asserted.

**B2.** As the **maintainer as governance owner**, I want `shadow-diff.sh` to report zero byte
differences between the frozen Rust binary and the OCaml binary, so that stdout, stderr, and exit
codes are provably unchanged for every consumer that parses them.

**B3.** As a **plan-executing AI agent**, I want all 21 hook gates to run and fail on exactly the
same inputs as before, so that a commit that was blocked yesterday is still blocked today.

**B4.** As the **`repo-harness-compatibility-checker`**, I want `rhino-cli` to remain byte-identical
across `ose-public`, `ose-primer`, and `ose-private`, so that the parity gate does not break
unrelated work in the sibling repos.

### Epic C — Build the missing Gherkin harness

**C1.** As the **maintainer as tool author**, I want an OCaml Gherkin harness that executes the
existing `.feature` corpus **without editing a single feature file**, so that the specs remain the
system of record and the harness is the thing that adapts.

**C2.** As the **maintainer as tool author**, I want the harness to accept the same step-matching
semantics `cucumber-rs` uses — regex patterns and cucumber expressions — so that the 1,124 existing
step bindings port mechanically rather than being redesigned.

**C3.** As the **maintainer as governance owner**, I want the harness to carry its own Gherkin spec
corpus and coverage gate, so that the tool every other gate depends on is itself gated.

### Epic D — Do not lose governance coverage

**D1.** As the **`swe-code-checker`**, I want a documented OCaml warning-and-lint set enforced as
errors, so that the
[cross-language lint strictness convention](../../../repo-governance/development/quality/cross-language-lint-strictness.md)
gains an OCaml row instead of an exemption.

**D2.** As the **maintainer as governance owner**, I want line coverage still gated at 90%, so that
the coverage floor survives a coverage tool that emits no lcov and has no threshold flag.

**D3.** As the **maintainer as governance owner**, I want a committed lock artefact and a clean-machine
resolution check, so that the
[reproducible environments convention](../../../repo-governance/development/workflow/reproducible-environments.md)
still holds without `Cargo.lock`.

## Acceptance criteria

Every scenario uses exactly one primary `Given`, one `When`, and one `Then`, chaining with
`And` / `But`, per the
[Acceptance Criteria Convention](../../../repo-governance/development/infra/acceptance-criteria.md).

### AC-1 — The control experiment is run and recorded (story A1, A2)

```gherkin
Feature: Pre-rewrite cost baseline

  Scenario: Toolchain reclamation and profile tuning are measured before the rewrite
    Given the superseded rustup toolchains are uninstalled and a fast dev profile is wired into the validator Nx targets
    When the incremental rebuild and the total resident footprint are re-measured with the same commands used for the 68.4 s and 16 GB baseline
    Then both post-tuning figures are recorded in "evidence/phase-1-retuned-baseline.txt"
    And the file states each figure beside its pre-tuning counterpart
```

### AC-2 — Dead dependencies are removed (story A2)

```gherkin
Feature: Dependency hygiene

  Scenario: The three unused crates are dropped without breaking the build
    Given "tree-sitter", "pulldown-cmark", and "ignore" are declared in "apps/rhino-cli/Cargo.toml" with zero references in the source tree
    When the three declarations are deleted and "npx nx run rhino-cli:test:quick" is run
    Then the target exits 0
    And "apps/rhino-cli/Cargo.lock" contains fewer than 183 package entries
```

### AC-3 — The five tooling gaps are closed, not waived (story A3, D1, D2, D3)

```gherkin
Feature: Governance-gap closure

  Scenario: Each identified OCaml tooling gap has a working replacement
    Given the five gaps G1 through G5 are recorded in "tech-docs.md"
    When the Phase 2 gate is evaluated
    Then each gap has a named artefact that executes successfully against the spike project
    And no gap is closed by an unargued waiver
    But a waiver explicitly accepted by the maintainer at the go/no-go gate is permitted and recorded with its reason
```

### AC-4 — The go/no-go gate is decided against measured numbers (story A4)

```gherkin
Feature: Rewrite decision gate

  Scenario: The maintainer decides with the control and spike numbers side by side
    Given "evidence/phase-1-retuned-baseline.txt" and "evidence/phase-2-ocaml-spike.txt" both exist
    When the maintainer is presented with both files at the Phase 2 gate
    Then the decision to proceed or stop is recorded in "delivery.md" with its rationale
    And no porting phase begins before that decision is recorded
```

### AC-5 — Every Gherkin scenario passes unchanged (story B1, C1)

```gherkin
Feature: Behaviour parity via the existing spec corpus

  Scenario: The full rhino Gherkin corpus executes green against the OCaml binary
    Given the 67 feature files under "specs/apps/rhino/behavior/rhino-cli/gherkin/" are unmodified since the rewrite began
    When "npx nx run rhino-cli:test:unit" and "npx nx run rhino-cli:test:integration" are run against the OCaml build
    Then all 441 scenarios report as passing
    And "git diff --stat specs/apps/rhino/" reports no changes
```

### AC-6 — Byte-identical output against the frozen Rust binary (story B2)

```gherkin
Feature: Shadow-diff parity

  Scenario: A command group's OCaml implementation matches the frozen Rust binary byte for byte
    Given "local-temp/rhino-rust-frozen" holds the release binary built from the pre-rewrite commit
    When "apps/rhino-cli/scripts/shadow-diff.sh" runs both binaries over the golden-master corpus
    Then the script exits 0
    And it reports zero differing bytes on stdout, stderr, and exit code for every fixture
```

### AC-7 — All hook gates still run and still block (story B3)

```gherkin
Feature: Gate-surface preservation

  Scenario: Every registered gate survives the cutover
    Given "rhino-cli gate list" reported 28 pre-commit and 14 pre-push gates before the cutover
    When "rhino-cli gate list --surface=pre-commit" and "--surface=pre-push" are run against the OCaml binary
    Then the two outputs are byte-identical to the pre-cutover captures in "evidence/phase-0-gate-list.txt"
    And "rhino-cli gate validate" exits 0
```

### AC-8 — Three-repo byte-identity is restored in the same delivery unit (story B4)

```gherkin
Feature: Cross-repo parity

  Scenario: The parity manifest verifies across all three bound repositories
    Given the cutover has landed in "ose-public", "ose-primer", and "ose-private"
    When "rhino-cli parity verify" is run in each of the three repositories
    Then all three exit 0
    And the "rhino-cli-parity-audit.yml" workflow passes in each repository
```

### AC-9 — The harness runs the corpus without editing it (story C1, C2)

```gherkin
Feature: Home-grown Gherkin harness compatibility

  Scenario: The harness binds an existing step definition by cucumber-expression pattern
    Given a feature file containing the step "Given a repository with a valid repo-config.yml"
    When the harness resolves that step against a registry populated with the ported cucumber-expression patterns
    Then exactly one handler matches
    And the captured arguments equal those "cucumber-rs" produced for the same step
```

### AC-10 — The harness supports the constructs the wider specs tree uses (story C1)

```gherkin
Feature: Gherkin construct coverage

  Scenario Outline: The parser accepts every construct present in the repository's spec corpus
    Given a feature file using the "<construct>" construct
    When the harness parses it
    Then parsing succeeds
    And the resulting AST exposes the construct

    Examples:
      | construct         |
      | Rule              |
      | Background        |
      | Scenario Outline  |
      | Examples table    |
      | data table        |
      | tag               |
```

### AC-11 — The harness is itself gated (story C3)

```gherkin
Feature: Harness self-gating

  Scenario: The harness's own behaviour coverage is validated
    Given "specs/libs/ocaml-rhino-gherkin/behavior/" contains the harness's feature corpus
    When "rhino-cli specs behavior-coverage validate specs/libs/ocaml-rhino-gherkin/behavior libs/ocaml-rhino-gherkin" is run
    Then it exits 0
    And every scenario in the corpus is reported as bound to a step definition
```

### AC-12 — Coverage stays gated at 90% (story D2)

```gherkin
Feature: Coverage floor preservation

  Scenario: A drop below the line-coverage floor fails the quality gate
    Given the OCaml coverage pipeline is wired into "rhino-cli:test:coverage"
    When a build whose line coverage is below 90 percent runs that target
    Then the target exits non-zero
    And the emitted report is readable by "rhino-cli test-coverage validate"
```

### AC-13 — Reproducible resolution from a clean machine (story D3)

```gherkin
Feature: Reproducible dependency resolution

  Scenario: A clean environment resolves to the committed lock artefact
    Given "apps/rhino-cli/opam.locked" is committed
    When a fresh opam switch installs dependencies from that lock artefact in CI
    Then the resolved package set matches the lock artefact exactly
    And the build produces a binary that passes the shadow-diff corpus
```

### AC-14 — Startup cost does not regress (story A2, B3)

```gherkin
Feature: Invocation overhead

  Scenario: Per-invocation startup stays in the single-digit-millisecond class
    Given the hook surfaces launch "rhino-cli" 21 times per commit-and-push cycle
    When the OCaml binary is invoked 10 times with "--help" and timed
    Then the mean per-invocation time is within 3 times the measured Rust baseline of 4.4 milliseconds
    And the figure is recorded in "evidence/phase-2-ocaml-spike.txt"
```

## Product scope

### In scope

- Reimplementing all 14 command groups and 49 subcommands in OCaml with an identical observable
  contract.
- `libs/ocaml-rhino-gherkin` — parser, step registry, runner, reporter, cucumber-expression matcher.
- Replacements for gaps G2-G5 (lint set, dependency audit, coverage threshold, lockfile).
- Retargeting `apps/rhino-cli/project.json` and the ~30 consuming `project.json` files.
- Retargeting `repo-config.yml`, the three Husky shims, and the six GitHub Actions workflows.
- Toolchain provisioning: `npm run doctor`, `Brewfile`, worktree setup docs.
- Propagating the identical change to `ose-primer` and `ose-private`; re-basing `beaver-nest`'s fork.
- Governance-doc updates for the language change.

### Out of scope

- Any behaviour change to `rhino-cli`. Feature work is a separate plan.
- Authoring or editing any `.feature` file under `specs/apps/rhino/`.
- Migrating `libs/rust-commons`, `apps/ayokoding-cli`, `apps/ose-cli`, or `ose-primer`'s Rust demo
  apps. Rust stays in the monorepo.
- A full Cucumber-specification implementation. The harness targets the corpus's measured subset;
  doc strings (`"""`) are excluded because the corpus contains zero.
- Adopting OCaml anywhere else on the platform.
- Publishing `ocaml-rhino-gherkin` to opam.

## Product-level risks

| #   | Risk                                                                                                   | Severity | Handling                                                                                      |
| --- | ------------------------------------------------------------------------------------------------------ | -------- | --------------------------------------------------------------------------------------------- |
| P1  | `cmdliner`'s generated `--help` text cannot match clap's byte-for-byte, so AC-6 fails on help fixtures | HIGH     | The `specs` group (14 subcommands) is spiked first in Phase 2 precisely to surface this early |
| P2  | The harness's step-matching diverges subtly, so a scenario passes for the wrong reason                 | HIGH     | Port `cucumber_expr.rs` directly; AC-9 compares captured arguments, not just match success    |
| P3  | Coverage instrumentation perturbs output bytes and breaks the shadow diff                              | MEDIUM   | Separate dune profiles for coverage runs and shadow-diff runs                                 |
| P4  | Consuming projects are re-pointed inconsistently, so a gate silently stops running                     | HIGH     | AC-7 compares full `gate list` output against a Phase 0 capture, not a spot check             |
| P5  | The 90-tag corpus's tag-filtering semantics differ, so a tagged subset silently under-runs             | MEDIUM   | Scenario counts are asserted, not just exit codes                                             |
| P6  | The rewrite lands and the dev loop is not meaningfully faster                                          | HIGH     | AC-4's go/no-go gate is the designed exit; stopping there is a valid, cheap outcome           |
