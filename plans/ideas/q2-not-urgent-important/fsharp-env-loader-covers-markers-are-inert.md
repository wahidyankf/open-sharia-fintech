# `libs/fsharp-env-loader`'s `@covers` markers are inert

One-line summary: the library carries 11 `@covers` traceability markers but has no step-definition
harness and no `specs:behavior:coverage` target, so nothing checks them — and adding the target alone
does not work, because the validator matches step text rather than scenario markers.

> Surfaced 2026-08-19 during the runtime-port-override delivery (PR #230), where the target was added,
> observed to fail, reverted, and the gap written into the spec README instead.

## Problem / context

`libs/fsharp-env-loader` is the only F# project in the repo carrying `@covers` markers that nothing
enforces. Of the six F# projects with real source — `apps/beavernest-be`, `apps/crane-cli`,
`apps/organiclever-be`, `apps/ose-be`, `libs/fsharp-crane-core`, `libs/fsharp-env-loader` — the first
five each have both a `[<Given>]`-attributed step harness and a `specs:behavior:coverage` target in
their `project.json`. `libs/fsharp-env-loader` has neither, while `PortResolverTests.fs` carries 8
`@covers` markers and `EnvTierTests.fs` carries 3. Its whole test tree is two files, with no `Steps/`
directory at all.

The obvious fix does not work, and that is the point of this brief. Wiring
`specs:behavior:coverage` for the library was attempted during PR #230 and reverted: the validator
reported 0 scenario gaps but 33 step gaps, because
`rhino-cli specs behavior-coverage validate --shared-steps` matches Gherkin **step text** against
registered step definitions, not scenario-level `@covers` comments. `libs/fsharp-crane-core` passes
the same target only because it has a real harness in
`tests/unit/Tests/PdfToMarkdownRoutingSteps.fs`. So the 11 markers are hand-verified prose: they look
like a traceability guarantee and are not one.

## Why now

Not urgent — no plan is blocked and no defect is running. It matters because the failure mode is
silent in the worst direction: a reader who greps for `@covers` finds markers and reasonably concludes
the coverage is gated, when the enforcement is a human having checked once. The library was just
extended with the whole port-resolution contract, which is exactly when its traceability claim starts
carrying weight it cannot hold.

## Prior art / precedents

- **`libs/fsharp-crane-core`** — the in-repo working precedent: the same validator, the same language,
  passing because it has an actual `[<Given>]` step harness.
- **Cucumber step definitions** — defines the step-text-to-implementation matching model the
  validator implements. [step-definitions](https://cucumber.io/docs/cucumber/step-definitions/)
- **Reqnroll (formerly SpecFlow)** — the established .NET Gherkin binding library, and the obvious
  alternative to hand-rolling another attributed harness.
  [reqnroll](https://reqnroll.net/)
- **Feature-change-completeness gate** — the repo rule that obliges specs and Gherkin for code
  changes, which these markers are meant to satisfy.
  [feature-change-completeness](../../../repo-governance/development/quality/feature-change-completeness.md)

## Proposed direction (sketch)

- Give the library a step harness in the shape the other five F# projects already use, then wire the
  `specs:behavior:coverage` target that the harness makes passable.
- Alternatively, decide the library does not warrant a harness and remove the 11 markers, so the
  absence of enforcement is visible rather than implied. Both outcomes are honest; the current state
  is the only dishonest one.
- Either way, add something that catches the general case — a project carrying `@covers` markers with
  no coverage target — since this brief exists because nothing did.

## Rough scope & non-goals

In scope: `libs/fsharp-env-loader`'s test tree, its `project.json`, and the shared Gherkin feature its
markers point at.

Out of scope (for now): the JSON-run-report cross-check, which is a separate mechanism with its own
brief; the `--exclude-dir` asymmetry in the whole-app step scan, likewise; changing the validator's
step-text matching model; retrofitting harnesses to projects that carry no markers.

## Risks & open questions

- Is a step harness proportionate for a two-file test tree, or is deleting the markers the better
  outcome? (open — decides the whole shape, and "delete" is a legitimate answer)
- The library's Gherkin lives under `specs/libs/ts-env-loader/`, shared with the TypeScript twin. Does
  a second harness against one shared feature file create a double-counting problem for the validator?
  (open — needs checking before promotion)
- Would a general "markers without a target" check produce false positives on projects that
  deliberately carry neither? (open)

## What success looks like + promotion signal

Success: every `@covers` marker in the repo is either mechanically enforced or absent — no third
category of marker that reads as a guarantee and is not one. Ready to promote once the
harness-versus-delete question is decided, since the two answers share almost no work.
