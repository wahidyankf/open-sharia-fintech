# Product Requirements — Rhino speccoverage multi-line scenario scan

## Product overview

The `speccoverage` engine in `apps/rhino-cli` maps Gherkin scenarios to their test bindings by
extracting scenario titles from source files. For TypeScript/JavaScript files it recognizes
`Scenario("title", …)` and `Scenario('title', …)` calls. This change makes that extraction
**line-layout-independent**: a title split from its `Scenario(` token across physical lines is
extracted correctly, so coverage results stop depending on how a formatter wraps the call. As a
consequence, the two `// prettier-ignore` workarounds in `libs/web-ui` are removed.

## Personas

Solo-maintainer repo. The maintainer consumes this feature wearing two hats; agents consume it as a
gate.

- **Tooling maintainer** — runs `rhino-cli specs behavior-coverage validate` locally and in CI.
- **Frontend maintainer** — writes vitest-cucumber step files in `libs/web-ui`; wants Prettier to
  format them without breaking coverage.
- **CI gate (agent consumer)** — `specs:behavior:coverage` job that must not false-fail.

## User stories

- **US-1** — As a tooling maintainer, I want scenario-title extraction to read the whole file rather
  than one line at a time, so that a wrapped `Scenario(` title is still recognized and coverage
  reflects the real bindings.
- **US-2** — As a frontend maintainer, I want to write step files and let Prettier format them
  freely, so that I never need a `// prettier-ignore` hack to keep spec coverage green.
- **US-3** — As a release/parity maintainer, I want the scanner fix to land byte-identical in all
  three repos, so that the shared `apps/rhino-cli` never drifts.

## Acceptance criteria (Gherkin)

All scenarios obey the step-keyword cardinality rule (one primary `Given`/`When`/`Then`; extras
chained with `And`).

### AC-1 — Cross-line double-quoted title is extracted (unit)

```gherkin
Scenario: A double-quoted scenario title on the line after Scenario( is extracted
  Given a TypeScript test file whose Scenario( token and its double-quoted title are on separate physical lines
  When extract_ts_scenario_titles reads the file
  Then the returned title set contains the wrapped title
  And the same-line double-quoted title in the same file is also present
```

### AC-2 — Cross-line single-quoted title is extracted (unit)

```gherkin
Scenario: A single-quoted scenario title on the line after Scenario( is extracted
  Given a TypeScript test file whose Scenario( token and its single-quoted title are on separate physical lines
  When extract_ts_scenario_titles reads the file
  Then the returned title set contains the wrapped title
```

### AC-3 — Same-line extraction is preserved (regression guard)

```gherkin
Scenario: Same-line scenario titles remain extracted after the change
  Given a TypeScript test file with double-quoted and single-quoted Scenario( titles on the same line as their token
  When extract_ts_scenario_titles reads the file
  Then the returned title set contains both titles
```

### AC-4 — Coverage reports no false gap for a wrapped binding (feature / cucumber-rs)

```gherkin
Scenario: A scenario whose title wraps onto a following physical line is still recognized as covered
  Given a feature file whose scenario is bound by a test whose Scenario(...) title wraps onto the next physical line
  When the developer runs behavior-coverage validate on the specs and app directories
  Then the command exits successfully
  And the output does not report the wrapped-title scenario as an unimplemented scenario
```

### AC-5 — Hack removal leaves web-ui coverage green (ose-public only)

```gherkin
Scenario: Removing the prettier-ignore hacks keeps web-ui spec coverage green
  Given the scanner fix has landed and the prettier-ignore single-line hacks are removed from the code-block step files
  When Prettier re-wraps the Scenario( calls and the developer runs the web-ui spec-coverage gate
  Then no prettier-ignore comment remains in libs/web-ui/src/primitives/code-block
  And the web-ui spec-coverage gate reports zero scenario gaps
```

### AC-6 — Byte-identity preserved across repos

```gherkin
Scenario: The rhino-cli change is byte-identical across the three sibling repos
  Given the scanner fix and its behavior-tree scenario have landed in ose-public
  When the change is propagated to ose-primer and ose-infra
  Then checker.rs is byte-identical across ose-public, ose-primer, and ose-infra
  And the spec-coverage behavior feature file is byte-identical across all three repos
```

## Product scope

**In scope**

- `extract_ts_scenario_titles` whole-content scan (behavior of the TS/JS extractor only).
- Unit regression fixtures for cross-line double- and single-quoted titles, plus a same-line guard.
- One new behavior-tree Gherkin scenario + its cucumber-rs binder.
- Removal of the two `// prettier-ignore` hacks in `libs/web-ui` code-block step files.
- Byte-identical propagation of the rhino-cli change to `ose-primer` and `ose-infra`.

**Out of scope**

- The `scenario_def_re()` regex pattern text (unchanged; already newline-tolerant via `\s`).
- Non-TS extractors and other coverage-matching logic.
- Any runtime/user-facing `libs/web-ui` component behavior — this plan touches only test files there.

## Product-level risks

- **False negatives from over-matching**: scanning whole-content could, in theory, match a
  `Scenario(` inside a comment or string literal. Mitigation: the same `scenario_def_re()` pattern is
  used (only the iteration unit changes), and `step_def_re()` already scans whole-content with the
  same class of pattern without incident [Repo-grounded — `checker.rs:37-41`].
- **Coverage-count table drift** in the gherkin README after adding a scenario. Mitigation: a
  delivery step recounts and updates the table.

## UI-design-funnel exemption

This plan is **not UI-bearing**. It touches `libs/web-ui` solely by removing `// prettier-ignore`
comments from `*.steps.tsx` **test files** — no user-facing screen or component is added or changed.
The UI-design-funnel requirement therefore does not apply. See [`tech-docs.md §6`](./tech-docs.md)
for the full exemption record (UI funnel, Rule-15/16 retest, manual UI/API verification).
