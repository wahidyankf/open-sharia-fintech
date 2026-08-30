---
title: "Execution-Grade Clarity (HARD RULE)"
description: Defines the outcome-section and granular-checkbox detail required for execution without extra context or duplicated Gherkin.
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

Plans are executed by execution-grade agents. Every outcome section and action checkbox MUST be
unambiguous to a junior engineer fresh from bootcamp with no professional work experience and no
repository or stack context, chat, or tribal knowledge.

**Each checkbox MUST contain all of the following that apply:**

- **Exact path(s)**, or the maximum-detail target: parent, naming pattern, and sibling reference.
- **Verbatim command(s)** when a command is involved.
- Section-level **Input, Outcome, and Proof**, plus the applicable acceptance-criterion reference.
- Exactly one independently verifiable action per checkbox, including its prerequisites, expected
  observation, failure handling, and evidence destination. Never write only “implement”, “set up”,
  or “configure”.
- Separate RED, GREEN, and REFACTOR checkboxes for every code behavior slice, each with its exact
  test/source path, symbol, copyable command, and expected failure/pass state.

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

- **Canonical Gherkin references**: Name the acceptance-criterion/scenario ID or exact title and
  link its canonical PRD or `specs/**` home. Do not copy the full Gherkin into `delivery.md`.
  A cohesive outcome section may cover multiple scenarios only when they share one observable outcome and
  proof boundary; list each reference. See
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

**Acceptance Criteria**: All user stories in `prd.md` must include testable acceptance criteria using
Gherkin format. See [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md)
for complete details. Deterministic gates own Gherkin mechanics; semantic plan review checks that
the referenced behavior, outcome, and proof are complete and consistent.
