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

Plans are executed by execution-grade (sonnet-tier) agents, not planning-grade agents. Authoring-grade clarity is not sufficient — every checkbox MUST be unambiguous at execution time without consulting additional context.

**Each checkbox MUST contain all of the following that apply:**

- **Explicit file path(s)**: Name the exact file path(s) when known (e.g., `apps/ose-www/src/server/trpc.ts`). When the path cannot be determined at authoring time (e.g., a new file whose location is implementation-dependent), provide the maximum-possible-detail target: parent directory + naming pattern + sibling reference (e.g., "new file under `apps/organiclever-www/src/lib/` following the pattern of sibling `auth.ts`").
- **Explicit shell command(s)**: State the verbatim invocation when a command is involved (e.g., `npx nx run ose-www:test:quick`), not a vague instruction like "run the lint".
- **Concrete acceptance criterion**: State the observable change that proves done (e.g., "all assertions in `trpc.test.ts` pass" or "`nx run ose-www:typecheck` exits 0"). No bare "implement X", "set up Y", or "configure Z" without a concrete verifiable outcome.
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

**Bad** (missing path, missing command, missing criterion):

```markdown
- [ ] Add caching
```

**Good** (explicit path, explicit command, explicit criterion):

```markdown
- [ ] Edit `apps/ose-www/src/server/trpc.ts`: wrap the public router with
      `unstable_cache(..., { revalidate: 300 })`. Verify by running
      `npx nx run ose-www:test:quick` — all tests pass.
```

**Acceptance Criteria**: All user stories in `prd.md` (or the condensed PRD section of a single-file plan's `README.md`) must include testable acceptance criteria using Gherkin format. See [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md) for complete details, including the **step-keyword cardinality HARD rule**: every `Scenario` uses exactly one primary `Given`, one `When`, and one `Then`; additional steps chain with `And`/`But`. `Background` blocks and `Scenario Outline` `Examples` tables are exempt. `plan-checker` and `repo-rules-checker` enforce this rule on Gherkin fences in `plans/in-progress/` and `plans/backlog/`; `plans/done/` is exempt as an immutable archive.
