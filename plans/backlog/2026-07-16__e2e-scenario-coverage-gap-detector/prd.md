# Product Requirements: E2E Scenario Coverage Gap Detector

## Overview

A validator (likely a `rhino-cli` command, e.g. `rhino-cli specs e2e-coverage`, or a `ci-checker`
enhancement — exact home is a technical decision for this plan's tech-docs phase) that, for every
project with a `playwright-bdd` e2e suite, compares:

- **Declared**: `@e2e`-tagged `Scenario:`/`Scenario Outline:` entries across that project's
  consumed `specs/**/*.feature` files.
- **Bound**: scenarios actually receiving a real step definition after `bddgen` runs (i.e., NOT
  falling back to `test.fixme` under `missingSteps: skip-scenario`).

## Requirements

1. **Baseline-aware, not baseline-breaking**: on first run, the validator MUST snapshot the
   current gap count per project (expected: the ~104 scenarios already tracked in
   `plans/ideas.md`) as an allowed baseline — it must not immediately fail CI repo-wide.
2. **New-gap detection**: the validator MUST fail (or clearly flag) when a project's unbound-gap
   count **increases** beyond its recorded baseline — i.e., a newly added scenario that ships
   without a step definition is caught, even though pre-existing debt is not immediately blocking.
3. **Baseline shrinkage is always allowed**: reducing the gap count (fixing a previously-unbound
   scenario) must never fail the check.
4. **Clear reporting**: output must name the specific `.feature` file and scenario title(s) newly
   unbound, not just a raw count delta — so a reviewer can act on it directly.
5. **Runs where reviewers already look**: wire into the same gate `pr-review-maker` and/or
   `ci-checker` already consult, so this doesn't require a new standalone tool someone has to
   remember to run.

## Open Questions (for this plan's own grilling pass when promoted to in-progress)

- Exact home: new `rhino-cli` subcommand vs. an addition to an existing `ci-checker`/CI job step?
- Where does the baseline snapshot live — a checked-in manifest file, or computed against
  `plans/ideas.md`'s existing backlog list?
- Should this run at `test:e2e` time (post-`bddgen`) or as a separate lint-style pass?

## Success Criteria

- A newly-added `@e2e` scenario without a step definition is caught by CI (or an equivalent
  reviewer-visible signal) before merge, without requiring a human to manually run `bddgen` and
  count scenarios.
- The existing ~104-scenario backlog does not need to be resolved before this validator can ship.
