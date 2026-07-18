# Product Requirements: E2E Scenario Coverage Gap Detector

## Overview

`rhino-cli specs e2e-coverage validate` `[Repo-grounded: verb-last CLI grammar, cli.rs §specs]` is a
mechanical validator that, for a project with a `playwright-bdd` e2e suite, compares:

- **Declared**: `@e2e`-tagged `Scenario:` / `Scenario Outline:` entries across the project's consumed
  `specs/**/*.feature` files.
- **Bound**: scenarios that receive a real step definition after `bddgen` runs — i.e., those NOT
  emitted as `test.fixme` into `.features-gen/**/*.spec.js` under `missingSteps: "skip-scenario"`
  `[Repo-grounded: playwright.config.ts, .features-gen gitignore]`.

The **unbound-gap set** = declared `@e2e` scenarios that appear as `test.fixme` in the generated
output. The validator diffs this set against a checked-in per-project **baseline manifest**
(`apps/<project>-e2e/e2e-coverage-baseline.json`). It fails when a scenario appears in the current
unbound-gap set but not in the baseline (a **new** gap); shrinkage never fails.

## Personas

Solo-maintainer repo; the maintainer wears hats and agents consume outputs:

- **Contributor** — adds `@e2e` scenarios; wants a fast pre-push signal when one ships unbound.
- **Reviewer / `pr-review-maker` / `ci-checker`** — read the `specs:e2e:coverage` gate result in the
  PR CI run as a mechanical, actionable signal.
- **Toolchain maintainer** — owns `rhino-cli` and its cross-repo byte-identity obligation.

## User Stories

- **As a contributor**, I want a new unbound `@e2e` scenario to fail a gate that names the feature
  file and scenario title, **so that** I catch the gap before merge instead of shipping a silently
  skipped test.
- **As a reviewer/agent**, I want the gap signal in the gate I already read (`test:quick` →
  `test:specs`), **so that** I do not need to remember a separate command or hand-count scenarios.
- **As the toolchain maintainer**, I want the ~104 pre-existing gaps captured as an explicit,
  reviewable baseline, **so that** shipping the validator does not require fixing debt first and any
  future growth of the baseline is a visible PR diff.

## Acceptance Criteria (Gherkin)

Each scenario below is bound to exactly one delivery RED→GREEN→REFACTOR cycle in `delivery.md`. Every
scenario uses one primary `Given` / `When` / `Then`, with extras chained via `And` per the
step-keyword cardinality HARD rule.

### AC-1 — Baseline-aware first run does not fail on pre-existing gaps

```gherkin
Scenario: A project's current unbound gaps exactly match its checked-in baseline
  Given a playwright-bdd project whose generated output marks scenarios "A" and "B" as test.fixme
  And a baseline manifest that lists exactly scenarios "A" and "B" as allowed unbound
  When rhino-cli specs e2e-coverage validate runs for that project
  Then it passes with exit code 0
  And it reports 2 declared-but-unbound scenarios all covered by the baseline
```

### AC-2 — A new unbound scenario beyond baseline fails

```gherkin
Scenario: A newly added @e2e scenario ships without a step definition
  Given a baseline manifest that lists exactly scenario "A" as allowed unbound
  And generated output that marks scenarios "A" and "C" as test.fixme
  When rhino-cli specs e2e-coverage validate runs for that project
  Then it fails with a non-zero exit code
  And it names scenario "C" and its containing .feature file as a new unbound gap
  And it does not report scenario "A" as a new gap
```

### AC-3 — Baseline shrinkage always passes

```gherkin
Scenario: A previously-unbound scenario is now bound
  Given a baseline manifest that lists scenarios "A" and "B" as allowed unbound
  And generated output that marks only scenario "A" as test.fixme
  When rhino-cli specs e2e-coverage validate runs for that project
  Then it passes with exit code 0
  And it reports scenario "B" as newly bound relative to the baseline
```

### AC-4 — Reporting names the specific feature file and scenario title

```gherkin
Scenario: Output identifies each new gap by feature path and scenario title
  Given a new unbound scenario "Resize the sidebar by keyboard" in "resizable-panel.feature"
  When rhino-cli specs e2e-coverage validate runs and detects it as a new gap
  Then the failure output contains the scenario title "Resize the sidebar by keyboard"
  And the failure output contains the feature file path ending in "resizable-panel.feature"
  And the failure output states the delta is an increase of 1 over baseline
```

### AC-5 — Only @e2e-tagged scenarios count as declared

```gherkin
Scenario: A test.fixme scenario that is not @e2e-tagged is ignored
  Given a scenario tagged @unit only that appears as test.fixme in the generated output
  And a baseline manifest that lists no allowed unbound scenarios
  When rhino-cli specs e2e-coverage validate runs for that project
  Then it passes with exit code 0
  And it does not report the @unit-only scenario as an unbound gap
```

### AC-6 — Baseline snapshot mode records the current gap set

```gherkin
Scenario: First-time baseline generation snapshots current unbound scenarios
  Given a project with no baseline manifest yet
  And generated output that marks scenarios "A" and "B" as test.fixme
  When rhino-cli specs e2e-coverage validate runs with the --update-baseline flag
  Then it writes a baseline manifest listing scenarios "A" and "B" as allowed unbound
  And a subsequent validate run for that project passes with exit code 0
```

### AC-7 — Missing generated output is a clear operational error, not a silent pass

```gherkin
Scenario: The generated output directory is absent
  Given a project whose .features-gen directory does not exist
  When rhino-cli specs e2e-coverage validate runs for that project
  Then it fails with a non-zero exit code
  And it reports that bddgen output was not found and must be generated first
```

### AC-8 — A stale baseline entry (no longer unbound) is reported for pruning

```gherkin
Scenario: The baseline lists a scenario that is no longer unbound
  Given a baseline manifest that lists scenarios "A" and "B" as allowed unbound
  And generated output that marks only scenario "A" as test.fixme
  When rhino-cli specs e2e-coverage validate runs for that project
  Then it passes with exit code 0
  And it reports scenario "B" as a stale baseline entry that can be pruned
```

## Product Scope

**In scope (features):**

- Diff-against-baseline validation for a single project (positional/flag-driven project path).
- `--update-baseline` snapshot mode (AC-6).
- Text, JSON, and Markdown output via the existing `--output` global flag `[Repo-grounded: cli.rs
OutputFormat]`.
- Per-project baseline manifests colocated in each playwright-bdd e2e project.
- `specs:e2e:coverage` Nx target per playwright-bdd e2e project, aggregated into `test:specs`.

**Out of scope (features):**

- Switching any suite to `"fail-on-gen"`.
- Auto-generating step definitions.
- Cross-project aggregation into a single repo-wide report (each project validates independently, as
  the other `specs:*` targets do `[Repo-grounded: nx-targets.md]`).
- Unbound detection at the `@unit`/`@integration` levels (this validator is e2e-specific; the
  `specs:behavior:coverage` gate already governs per-level `@covers` coverage `[Repo-grounded]`).

## Product-Level Risks

| Risk                                                                        | Mitigation                                                                                                                                                                                                                                           |
| --------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Scenario titles are not unique across feature files, causing diff ambiguity | Baseline entries key on `{feature-path, scenario-title}` pairs, not title alone (AC-4)                                                                                                                                                               |
| `Scenario Outline` expands to multiple generated tests                      | Declared set counts the outline once by title; the generated scan matches the outline's wrapping `test.describe(...)` block title, treating the outline as unbound if any Examples-row test inside it is `test.fixme` (documented in `tech-docs.md`) |
| A project on `fail-on-gen` never emits `test.fixme`, so the gate is a no-op | Documented as belt-and-suspenders; empty baseline + zero fixme = trivial pass (AC-1 with empty sets)                                                                                                                                                 |

## Related

- [brd.md](./brd.md) — business rationale and success metrics these scenarios operationalize.
- [tech-docs.md](./tech-docs.md) — how declared/bound sets are computed and where the baseline lives.
