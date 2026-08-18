# 🧹 oxlint Upgrade and Lint-Toolchain Reproducibility

## Context

`repo-rules-sweep` was blocked mid-execution when ose-public PR #227's TypeScript quality gate turned
red on a branch that had passed it two hours earlier, without touching the tree the failure named.

Root cause: every lint target invoked `npx oxlint@latest`, and `oxlint` was not a declared dependency
anywhere. oxlint 1.79.0 published `2026-08-18T15:10:39Z` and added `react(set-state-in-effect)`; the
next CI run resolved it and failed on pre-existing code.

That plan pinned oxlint to **1.78.0** across all 22 call sites (21 in `ose-public`, 1 in `ose-private`)
under the [Code-Routing Downstream Rule](../../../repo-governance/development/quality/knowledge-capture/the-code-routing-downstream-rule.md)'s
blocker carve-out — a lint failure blocking the current plan is fixed inline.

**The pin defers the finding; it does not resolve it.** This plan resolves it.

## Workstreams

| ID    | Workstream                                                 | Status    |
| ----- | ---------------------------------------------------------- | --------- |
| WS-O1 | Fix the `set-state-in-effect` violation in `ose-www`       | Specified |
| WS-O2 | Upgrade the pin to current oxlint and absorb the new rules | Specified |
| WS-O3 | Prevent the class: no unpinned tool may gate CI            | Specified |

### WS-O1 — the real finding

`apps/ose-www/src/features/search/shell/search-dialog.tsx:36` calls `setState` synchronously inside an
effect. oxlint's message is specific about the remedy: _"Derive the value during render, initialize
state directly, or update it from the event that caused the change."_

The line was last touched by the unrelated commit `5f7f8fdbe`, so this is a genuine pre-existing
defect that a stricter linter surfaced — not damage from the sweep.

### WS-O2 — take the upgrade deliberately

Move the pin from 1.78.0 to current. Expect further findings: 1.79.0 alone added a rule that fires on
this repository. Every new finding is triaged on its merits — fixed, or the rule disabled in
`oxlint.json` **with a stated reason**. Silently pinning backwards is not an outcome this plan allows.

### WS-O3 — the class, not the instance

21 sites in `ose-public` and 1 in `ose-private` each fetched a fresh linter at run time, so **any**
upstream release could turn CI red at any moment, in any of them. Pinning fixed today's instance.
This workstream asks the broader question: what else does the toolchain resolve unpinned, and what
gate would have caught it?

## Scope

**Repositories**: `ose-public` and `ose-private`. Both were pinned; both must be upgraded together or
they diverge, violating the same-maintainer-experience constraint.

**Trees in scope**: `apps/ose-www/src/`, root `package.json` in both repos, `oxlint.json` configs,
and — for WS-O3 — the gate registry in `repo-config.yml`.

**Out of scope**: replacing oxlint; changing the eslint pairing; the twenty orphaned `rhino-cli` test
files (separate follow-up).

## Approach Summary

WS-O1 is a TDD code change under the ordinary gates: it alters observable behaviour in an app, so it
carries companion `specs/` Gherkin per
[Feature Change Completeness](../../../repo-governance/development/quality/feature-change-completeness.md).

WS-O2 must not be attempted before WS-O1 lands, or the upgrade and the fix confound each other.

WS-O3 begins with an enumeration, not a fix — the same method that produced this plan.

## Documents

- [brd.md](./brd.md) — why an unpinned linter is a delivery risk.
- [prd.md](./prd.md) — user stories and Gherkin acceptance criteria.
- [tech-docs.md](./tech-docs.md) — the defect, the evidence, and the fix design.
- [delivery.md](./delivery.md) — the phase-by-phase execution checklist.
