<!-- Knowledge Capture running log — append entries during execution. -->
<!-- Triage every entry (or record the explicit "none" escape) before archival. -->

# Learnings: E2E Scenario Coverage Gap Detector

Append one entry per generalizable learning as it surfaces during execution, using the shape below.
Sanitize per the secret/sensitivity gate before writing. Triage all entries in Phase 7's Knowledge
Capture section (before archival-in-PR) before archival.

<!--
## Learning: <one-line summary>

- **Context**: what was being done when this surfaced
- **Observation**: what was noticed (sanitized)
- **Why it might generalize**: the litmus reasoning
- **Terminal state**: routed inline to <path> / filed as plans/backlog/<slug> / discarded — <reason>
-->

## Learning: ayokoding-www-fe-e2e's stale "~104" unbound-scenario estimate

- **Context**: Phase 5, generating `apps/ayokoding-www-fe-e2e/e2e-coverage-baseline.json` via
  `--update-baseline`. `playwright.config.ts` carries a long-standing comment estimating ~104
  preexisting scenarios lack e2e step definitions.
- **Observation**: The generated baseline holds exactly **3** entries, all in
  `code-block-copy.feature`: "A non-mermaid code block renders a copy button", "A mermaid block
  renders no copy button", "The copy button is labelled in Indonesian on the Indonesian site".
  Cross-checked three ways: (1) `grep -c "test.fixme("` across `.features-gen` = 43 total, of which
  only 3 carry the `@e2e` tag (40 are `@unit`-only); (2) repo-wide count of `@e2e`-tagged scenarios
  under the ayokoding gherkin tree = 156, of which 153 already have bound e2e step definitions; (3)
  a synthetic new-gap injection (see below) proves the detector reacts to real deltas, not a
  miscounted baseline. The "~104" figure is stale documentation from an earlier point in
  ayokoding-www's content buildout — not a bug in the new detector.
- **Why it might generalize**: Anyone reading `playwright.config.ts`'s comment before this plan
  would over-estimate remaining e2e-coverage debt for ayokoding-www-fe-e2e by ~34x. The comment
  itself is out of scope for this plan (already has a designated follow-up reference in
  `plans/ideas.md`) but the accurate count belongs on record so the next person doesn't re-derive it.
- **Terminal state**: recorded here as the authoritative count; the stale `playwright.config.ts`
  comment is left untouched per Root Cause Orientation (out-of-proportion for this plan, has its own
  follow-up plan reference) — no further routing needed.

## Execution evidence

### Baseline generation (Phase 5, ayokoding-www-fe-e2e)

```
$ cargo run --release --quiet --manifest-path ../../apps/rhino-cli/Cargo.toml -- specs e2e-coverage validate \
    --project ayokoding-www-fe-e2e \
    --features "../../specs/apps/ayokoding/behavior/ayokoding-www/gherkin/**/*.feature" \
    --features "../../specs/libs/web-ui/behavior/gherkin/resizable-panel/resizable-panel.feature" \
    --features-gen .features-gen --baseline e2e-coverage-baseline.json --update-baseline
Wrote baseline manifest to e2e-coverage-baseline.json
```

Baseline written with 3 `allowedUnbound` entries (see discrepancy learning above).

### Synthetic-gap verification (Task P5 #186)

A temporary `@unit @e2e` scenario ("SCRATCH synthetic gap fixture for e2e coverage gate
verification") with a step no `.steps.ts` file implements was appended to the end of
`specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/code-block-copy.feature`, then reverted
after verification (`git status --short` on the file confirmed a clean working tree post-revert).

FAIL run (`npx nx run ayokoding-www-fe-e2e:specs:e2e:coverage --skip-nx-cache`), scratch scenario present:

```
E2E COVERAGE GAP DETECTOR FAILED: 1 new unbound scenario(s) found (increase of 1 over baseline)
  ../../specs/apps/ayokoding/behavior/ayokoding-www/gherkin/content/code-block-copy.feature
    -> Scenario: "SCRATCH synthetic gap fixture for e2e coverage gate verification"
Error: 1 new unbound scenario(s) found beyond baseline
```

PASS run, same command, after reverting the scratch scenario:

```
E2E COVERAGE GAP DETECTOR PASSED: 0 new unbound scenario(s) beyond baseline
```

This is also the manual CLI verification for pass-case and fail-case output of `specs:e2e:coverage`.

### Rollout to the remaining 10 playwright-bdd projects

`ayokoding-www-be-e2e`, `organiclever-app-web-e2e`, `organiclever-be-e2e`, `organiclever-www-be-e2e`,
`organiclever-www-fe-e2e`, `ose-app-web-e2e`, `ose-be-e2e`, `ose-www-be-e2e`, `ose-www-fe-e2e`,
`wahidyankf-www-fe-e2e` all use playwright-bdd's default `missingSteps` mode (`fail-on-gen`), not
`ayokoding-www-fe-e2e`'s `skip-scenario` override — confirmed by reading each project's
`playwright.config.ts` (no `missingSteps` key present). Under `fail-on-gen`, `bddgen` only succeeds
when every consumed scenario already has a bound step, so `test.fixme(...)` never appears; each of
the 10 baselines generated as `{"project": "<name>", "allowedUnbound": []}`, matching delivery.md's
prediction ("each `fail-on-gen` project is expected to produce an empty `allowedUnbound: []` baseline
and a trivially-passing gate"). `npx nx run-many -t specs:e2e:coverage --skip-nx-cache` confirmed all
11 projects (the 10 plus `ayokoding-www-fe-e2e`) exit 0 in one workspace-wide pass.
