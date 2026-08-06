# Wire the behavior-coverage JSON-report cross-check

One-line summary: actually thread rhino-cli's `specs behavior-coverage validate` JSON-run-report flags
into project targets and CI, closing the gap between what an archived plan claimed and what is wired.

> Surfaced 2026-07-05 during post-archival hollow-spec re-verification.

## Problem / context

`rhino-cli specs behavior-coverage validate`'s `--unit-report` / `--integration-report` /
`--e2e-report` JSON-ingestion flags exist and work, but **zero** `project.json` or CI workflow in any
of the three repos passes them (confirmed by repo-wide grep, 2026-07-05). The archived plan's Final
Gate claims this mechanism is "wired to pre-push + CI", which is not accurate as literally described.
The anti-hollow-spec guarantee today instead rests on two other mechanisms that **are** wired and
verified: static step-text matching (`@covers` must resolve to a registered step) and per-language
fail-on-skip grep-bans in each project's `test:unit` / `test:quick`.

## Why now

The discrepancy between the overclaimed Final Gate and the actual wiring is documented but unresolved;
wiring the mechanism for real would make the claim true and add a genuine third cross-check.

## Prior art / precedents

- **Cucumber JSON run reports** — established prior art for emitting machine-readable test-run
  reports that downstream tooling ingests, the exact mechanism this idea wires.
  [cucumber reporting](https://cucumber.io/docs/cucumber/reporting/)
- **Specs & feature-change-completeness gate** — the repo's existing anti-hollow-spec guarantee this
  cross-check would add a third mechanism to.
  [feature-change-completeness](../../../repo-governance/development/quality/feature-change-completeness.md)
- **Nx targets & specs coverage** — the canonical target model the `--*-report` flags must thread
  through across the ~59 projects. [nx-targets](../../../repo-governance/development/infra/nx-targets.md)

## Proposed direction (sketch)

- Decide which test tier emits which report format, per language/tool.
- Thread `specs:behavior:coverage --*-report` through the ~59 projects' targets and CI.

## Rough scope & non-goals

In scope: wiring the JSON-run-report cross-check for the tiers that can emit it.

Out of scope (for now): replacing the static step-text and grep-ban mechanisms — they stay; this is
additive.

## Risks & open questions

- Which report format does each language/tool emit, and which tier owns it? (open — the core design
  question)
- Is the JSON mechanism worth wiring across 59 projects given two redundant mechanisms **already**
  prevent hollow specs? (open — this is a cost/benefit call, and "not worth it, correct the overclaim
  instead" is a legitimate outcome)

## What success looks like + promotion signal

Success: the JSON-report cross-check runs in CI for the tiers that emit it, and the archived plan's
claim becomes literally true. Ready to promote once the per-language format mapping is decided — or
discard in favour of simply correcting the overclaim, if the cost/benefit says so.
