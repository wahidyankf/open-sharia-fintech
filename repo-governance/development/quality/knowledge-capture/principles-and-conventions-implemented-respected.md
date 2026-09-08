---
description: "Principles/conventions this convention implements."
when_to_use: "Use when tracing this convention's rationale."
---

# Principles and Conventions Implemented/Respected

## Principles Implemented/Respected

This convention implements the following core principles:

- **[Root Cause Orientation](../../../principles/general/root-cause-orientation.md)**: A learning that
  is noticed but never routed to a durable home is a symptom recurring in waiting. Routing a learning
  to the surface that owns its kind of knowledge (a convention, an agent, a test, a skill) is what
  actually prevents recurrence — not the act of writing it down.
- **[Documentation First](../../../principles/content/documentation-first.md)**: Knowledge Capture
  treats the learnings a plan produces as a first-class deliverable of the plan, not an informal
  byproduct that lives only in the executor's working memory.
- **[Simplicity Over Complexity](../../../principles/general/simplicity-over-complexity.md)**: The
  routing matrix is deliberately a single pass over a running log, not a dashboard, a database, or a
  standing review board. The anti-theater guardrails exist specifically to keep the mechanism this
  simple.
- **[Explicit Over Implicit](../../../principles/software-engineering/explicit-over-implicit.md)**: The
  mandatory + explicit "none" escape means an empty `learnings.md` is never ambiguous — either it
  carries a routed/discarded record for every learning, or it carries an explicit
  `No generalizable learnings — <reason>` statement. Silence is never an accepted state.
- **[Deliberate Problem-Solving](../../../principles/general/deliberate-problem-solving.md)**: The litmus
  test ("would the system catch this next time?") forces a deliberate judgment before a learning is
  kept, rather than reflexively logging everything an executor happened to notice.

## Conventions Implemented/Respected

This convention implements/respects the following conventions:

- **[Plans Organization Convention](../../../conventions/structure/plans.md)**: `learnings.md` is a plan
  folder artifact that follows the same lifecycle as the rest of the plan (backlog is not
  applicable; it accrues in `in-progress/` and moves with the plan on archival to `done/`).
- **[Feature Change Completeness Convention](.././feature-change-completeness.md)**: When a learning
  routes to code (`apps/`, `libs/`, tests), the resulting follow-up plan is bound by this convention's
  specs/Gherkin two-path rule in full — Knowledge Capture does not create a side channel that bypasses
  it.
- **[Regression Test Mandate](.././regression-test-mandate.md)**: When a learning identifies a bug, its
  code-routed follow-up plan carries the regression-test mandate exactly as any other bug fix would.
- **[Post-Mortem Convention](../../../conventions/structure/post-mortems.md)**: Failure/incident learnings
  route through this convention's matrix to a post-mortem; that convention remains the single source
  of truth for post-mortem structure and content.
- **[No Secrets in Git Convention](../../../conventions/security/no-secrets-in-committed-files.md)**: The
  secret/sensitivity safety gate below inherits this hard iron rule in full — `learnings.md` is
  committed and, in the public repos, world-readable.
