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

Use a same-document, uniquely named runbook packet only when literal repetition would duplicate
one maintained procedure or disclose private detail. Its finite binding to the checkbox ID or phase
MUST state record sources, copyable commands, its admitted public path or private-safe target, and
the pass/fail record. It cannot refer generically elsewhere, invent records at execution, change a
merge gate, or evade file-touch, scope, or acceptance requirements.

**Enforcement disposition — unenforced by decision:** contextual `plan-checker` review records the
binding and violations; no scanner or exception list is introduced. This limits drift and preserves
human readability without adding maintenance burden.

- **One scenario per behavior cycle + inline Gherkin**: each behavior RED→GREEN→REFACTOR cycle
  binds exactly one verbatim scenario. See [Gherkin-Tagged Delivery Steps](../../../development/workflow/test-driven-development/gherkin-tagged-delivery-steps.md#gherkin-tagged-delivery-steps).

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

**Acceptance Criteria**: User stories in `prd.md` (or a single-file plan’s condensed PRD) use testable Gherkin. See [Acceptance Criteria Convention](../../../development/infra/acceptance-criteria.md).
