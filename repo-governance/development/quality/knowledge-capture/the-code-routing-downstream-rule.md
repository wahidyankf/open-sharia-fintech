---
title: "The Code-Routing Downstream Rule"
description: "Routing for a learning implying a code change."
category: explanation
subcategory: development
tags:
  - knowledge-capture
  - learnings
  - plans
  - triage
  - safety-gates
  - post-mortems
created: 2026-07-05
when_to_use: "Use when a learning implies a code change."
---

# The Code-Routing Downstream Rule

When a learning's home is `apps/`, `libs/`, or tests — i.e., the codebase itself must change — that
follow-up work is **never landed inline** in the current plan's commits or PR. Create a separate
`plans/ideas/` two-pager only when the user literally authorizes that plan artifact. Without that
authorization, record `Reported without plan authorization` plus the report location or
conversation handoff evidence.

**Why**: a code change is bound by the repository's normal engineering gates, and a captured learning
does not get to bypass them:

- **[Feature Change Completeness](.././feature-change-completeness.md)**: an observable behaviour change
  in `apps/`/`libs/` ships with companion `specs/` Gherkin, carried by the follow-up plan.
- **[Regression Test Mandate](.././regression-test-mandate.md)**: if the learning names a bug, its fix
  lands with a reproducing test (failing before, passing after) in the same commit/PR as the fix.
- **[Test-Driven Development](../../workflow/test-driven-development.md)**: Red → Green → Refactor
  governs the code change itself.

Because these gates apply, an authorized code-routed learning is filed as its own
`plans/ideas/<slug>.md` two-pager and reaches backlog only through the promotion ripeness gate. An
unauthorized one is reported, never silently filed or smuggled into
the current governance/docs plan's PR.

**Carve-out (Iron Rule 3 — Root Cause Orientation still applies in full)**: this downstream rule
governs learnings captured for **future** evolution. A bug, failing test, or lint failure the
executor must fix to finish the **current** plan's own deliverables is a **blocker** — ordinary
inline execution under Root Cause Orientation ("fix all issues, including preexisting"), not a
deferred learning. The separate-follow-up rule applies only to code changes a learning _suggests_
as a future improvement that are **not required** to complete the current plan. Do not
misuse this carve-out to smuggle unrelated code changes into a docs/governance plan — it covers
only what is genuinely required to finish the plan's own scope.
