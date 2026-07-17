# Product Requirements — rhino-cli Source-Drift Reconciliation

## Overview

Make the four drifted in-boundary `apps/rhino-cli/src/` files identical across `ose-public`,
`ose-primer`, and `ose-infra` by adopting the **union command/tool surface** as canonical, then
verify full rhino-cli byte-identity across all three repos. The reconciliation runs across all three
working trees via the
[Plan Multi-Repo Parity Planning workflow](../../../repo-governance/workflows/plan/plan-multi-repo-parity-planning.md)
`[Repo-grounded]`.

## Personas

Solo-maintainer repo; the maintainer wears hats and agents consume outputs:

- **Toolchain maintainer** — owns `apps/rhino-cli` and its cross-repo byte-identity obligation;
  verifies the reconciliation restores it `[Repo-grounded: docs/reference/sdlc-gate-standard.md]`.
- **Downstream plan author** (`e2e-scenario-coverage-gap-detector`) — consumes a clean,
  already-identical rhino-cli base as an explicit precondition before adding a new subcommand
  `[Repo-grounded: sibling plan's README §Prerequisite]`.
- **Reviewer / `pr-review-maker` / `pr-review-fixer`** — review each repo's reconciliation diff via
  the PR-Review Maker→Fixer Cycle before merge `[Repo-grounded]`.

## User Stories

- **As the toolchain maintainer**, I want the four drifted rhino-cli `src/` files reconciled to a
  single canonical union form, **so that** the byte-identity guarantee documented in the SDLC Gate
  Standard is actually true rather than silently false.
- **As the downstream `e2e-scenario-coverage-gap-detector` plan author**, I want a verified-identical
  rhino-cli base before adding the new subcommand, **so that** identical bytes across all three repos
  is a checked precondition rather than an assumption.
- **As a reviewer**, I want the reconciliation to preserve every repo's applicable behavior as
  dormant-not-deleted, **so that** no repo silently loses functionality it relies on.
- **As the toolchain maintainer**, I want any hardcoded per-repo value difference moved into
  `repo-config.yml`, **so that** the `.rs` source itself stays byte-identical rather than carrying
  per-repo branches.

## Requirements

1. **Per-file canonical determination**: for each drifted file, determine the canonical form as the
   **union** of all three repos' content — every tool parser, naming rule, and command branch present
   in any repo is present in the canonical form; behavior inapplicable to a given repo is dormant
   (gated by `repo-config.yml` data), not deleted. Where a difference is genuinely a hardcoded
   per-repo **value** (e.g. an instruction-size budget), it must move to `repo-config.yml` data so the
   source stays identical — or be documented as an accepted equal value if already data-driven.
2. **Byte-identity after reconciliation**: after applying the canonical form, a tri-repo `diff` over
   the full boundary (`src/`, `Cargo.toml`, `Cargo.lock`, `project.json`, `LICENSE`, and
   `specs/apps/rhino/behavior/rhino-cli/gherkin/**`) returns **zero** differences between every pair
   of repos.
3. **No behavioral regression**: rhino-cli's full test suite (unit + integration + the `tests/`
   binaries) passes in **each** repo after reconciliation; dormant verbs remain dormant where their
   projects are absent.
4. **`tests/doctor.rs` reconciled or justified**: the adjacent `tests/doctor.rs` drift is either
   reconciled to identical or explicitly documented as a sanctioned divergence with rationale.
5. **Applied to all three repos**: the change lands in `ose-public`, `ose-primer`, AND `ose-infra`
   (one delivery leg per repo), not just one.

## Acceptance Criteria (Gherkin)

```gherkin
Feature: rhino-cli source byte-identity across sibling repos

  Background:
    Given the three sibling repos ose-public, ose-primer, and ose-infra are checked out on main
    And each repo's rhino-cli source is reconciled to the canonical union form

  Scenario: Boundary src files are byte-identical across all repo pairs
    When a recursive diff runs over apps/rhino-cli/src between ose-public and ose-primer
    And a recursive diff runs over apps/rhino-cli/src between ose-public and ose-infra
    Then both diffs report zero differing files

  Scenario: The previously drifted files are identical
    When apps/rhino-cli/src/application/doctor/tools.rs is compared across all three repos
    And apps/rhino-cli/src/application/doctor/checker.rs is compared across all three repos
    And apps/rhino-cli/src/application/docs/naming.rs is compared across all three repos
    And apps/rhino-cli/src/application/repo_governance/instruction_size.rs is compared across all three repos
    Then every file is byte-identical in all three repos

  Scenario: Union surface preserves each repo's applicable behavior
    Given ose-public's tools.rs carried tool parsers absent from ose-primer before reconciliation
    When the canonical union form is applied to all three repos
    Then every repo's rhino-cli exposes the full tool-parser surface
    And a parser whose tool is absent in a given repo is dormant, not removed

  Scenario: No behavioral regression after reconciliation
    When rhino-cli's unit, integration, and tests/ binaries run in each repo
    Then all suites pass in ose-public, ose-primer, and ose-infra

  Scenario: Manifest and gherkin boundary stays identical
    When Cargo.toml, Cargo.lock, project.json, LICENSE, and the gherkin behavior tree are diffed across repos
    Then they remain byte-identical (this plan introduces no drift there)
```

## Success Criteria

- Tri-repo `diff` over the full rhino-cli byte-identity boundary returns zero differences.
- rhino-cli test suites green in all three repos.
- The e2e-scenario-coverage-gap-detector plan can proceed on a verified-identical base.

## Product Scope

**In scope (product):**

- Reconciling the four drifted `src/` files + `tests/doctor.rs` to a canonical union form.
- Moving any hardcoded per-repo value differences into `repo-config.yml` data.
- Verifying byte-identity via the tri-repo `diff` across the full boundary (`src/`, manifest files,
  gherkin tree).
- Landing the change in all three repos with rhino-cli's test suite green.

**Out of scope (product):**

- Adding new rhino-cli commands or behavior.
- Building a standing automated tri-repo src-diff gate (candidate follow-up, tracked in Knowledge
  Capture).
- Touching `speccoverage/checker.rs` (already identical; owned by the multiline-scan plan).
- Reconciling any files outside the rhino-cli byte-identity boundary.

## Product-Level Risks

| Risk                                                                                                       | Mitigation                                                                                                                                                                             |
| ---------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Union reconstruction accidentally drops applicable behavior for a repo                                     | Canonical form is derived by reading all three variants side-by-side (Phase 1); Phase 2's RED step asserts the union surface is reachable before GREEN `[Repo-grounded: delivery.md]`. |
| A previously-dormant tool parser or check activates a false positive in a repo that never exercised it     | Phase 2's REFACTOR step runs the full local suite (`cargo test`, `nx run rhino-cli:test:unit`) in every repo, not just the repo where the drift originated.                            |
| Partial tri-repo application leaves the invariant broken in a different way (two repos identical, one not) | Phase 3's tri-repo `diff` gate blocks progression until all pairs report zero differences; Phase 4 requires all three PRs green before Phase 5.                                        |

## Open Questions (resolved during execution, not before)

- For each drifted file, is the difference a **union-surface gap** (adopt superset) or a hardcoded
  **per-repo value** (move to `repo-config.yml`)? Determined per file in Phase 1 by reading all three
  variants.
- Does `instruction_size.rs`'s primer-only drift reflect a real budget-value difference that must
  become data, or stale source? Determined in Phase 1.

## Related

- [brd.md](./brd.md) — business rationale and success metrics these scenarios operationalize.
- [tech-docs.md](./tech-docs.md) — reconciliation approach and where each per-file decision is recorded.
