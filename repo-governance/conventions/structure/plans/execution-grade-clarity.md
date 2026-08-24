---
title: "Execution-Grade Clarity (HARD RULE)"
description: Lists what every delivery.md checkbox must contain — explicit file paths, commands, acceptance criteria, and inline Gherkin — so an execution-grade agent can act without extra context.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when writing or reviewing a delivery.md checkbox for execution-grade clarity.
---

# Execution-Grade Clarity (HARD RULE)

Plans are executed by execution-grade agents. Every checkbox MUST be unambiguous without extra context.

**Each checkbox MUST contain all of the following that apply:**

- **Exact path(s)**, or the maximum-detail target: parent, naming pattern, and sibling reference.
- **Verbatim command(s)** when a command is involved.
- **Observable acceptance criterion**; never only “implement”, “set up”, or “configure”.

## Controlled Runbook-Reference Exception

Use a same-document, uniquely named runbook packet only for a finite cross-repository lifecycle
procedure where literal row repetition would duplicate one maintained procedure or disclose private
detail. Its finite binding to the checkbox ID or phase MUST state why the packet is needed, record
sources, copyable commands, its admitted public path or private-safe target, and the pass/fail
record. It cannot refer generically elsewhere, invent records at execution, change an existing merge
gate, or evade file-touch, scope, or acceptance requirements.

**Enforcement disposition — unenforced by decision:** contextual `plan-checker` review records the
binding and violations; no scanner or exception list is introduced. This limits drift and preserves
human readability without adding maintenance burden.

- **One scenario per behavior cycle + inline Gherkin**: Every behavior-implementing
  RED→GREEN→REFACTOR cycle targets **exactly one** Gherkin scenario. Its RED step carries a
  single-scenario `**Gherkin (binds) →** "<title>"` tag line followed immediately by that
  scenario's full `Given/When/Then` as a fenced ` ```gherkin ` block copied verbatim from the
  companion `.feature`; never bundle multiple scenarios into one cycle (long checklists are
  expected). Pure-core (`**Gherkin (underpins) →**`) data/calc tests and the aggregate
  feature-consuming / `playwright-bdd` binders are the only steps that keep a multi-scenario
  title list. `plan-checker` flags a multi-scenario behavior RED, or absent/non-verbatim inline
  Gherkin, as a **HIGH** finding. See
  [Gherkin-Tagged Delivery Steps](../../../development/workflow/test-driven-development/gherkin-tagged-delivery-steps.md#gherkin-tagged-delivery-steps).

**HARD RULE**: `plan-checker` flags violations of this rule as HIGH severity. `plan-fixer` rewrites offending items with maximum detail.

**Bad**:

```markdown
- [ ] Add caching
```

**Good**:

```markdown
- [ ] Edit `apps/ose-www/src/server/trpc.ts`: wrap the public router with
      `unstable_cache(..., { revalidate: 300 })`. Verify by running
      `npx nx run ose-www:test:quick` — all tests pass.
```

**Acceptance Criteria**: All user stories in `prd.md` (or the condensed PRD section of a single-file plan's `README.md`) must include testable acceptance criteria using Gherkin format. See [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md) for complete details, including the **step-keyword cardinality HARD rule**: every `Scenario` uses exactly one primary `Given`, one `When`, and one `Then`; additional steps chain with `And`/`But`. `Background` blocks and `Scenario Outline` `Examples` tables are exempt. `plan-checker` and `repo-rules-checker` enforce this rule on Gherkin fences in `plans/in-progress/` and `plans/backlog/`; `plans/done/` is exempt as an immutable archive.
