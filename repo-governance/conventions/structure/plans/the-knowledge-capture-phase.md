---
title: "The Knowledge Capture Phase (Final Phase Before Archival)"
description: Requires every substantive plan's delivery.md to end with a Knowledge Capture phase that routes every learnings.md entry to a terminal state before archival.
category: explanation
subcategory: conventions
tags:
  - conventions
  - plans
  - project-planning
  - organization
created: 2025-12-05
when_to_use: Use when authoring or executing a plan's final Knowledge Capture phase before moving it to done/.
---

# The Knowledge Capture Phase (Final Phase Before Archival)

Every substantive plan's `delivery.md` MUST end with a **Knowledge Capture** phase, immediately
before the Plan Archival phase. This phase triages every entry in `learnings.md` through the
[Knowledge Capture Convention](../../../development/quality/knowledge-capture.md)'s open-ended,
principle-based routing matrix: each surviving learning is routed to exactly one durable home (a
convention, a doc, an agent, a skill, code, a test, or a post-mortem) — small non-code routings land
inline in the current plan's commits. Large non-code routings and ALL code routings become a
user-authorized `plans/ideas/` two-pager; never create a `plans/backlog/` folder directly because
the promotion ripeness gate owns that transition. Without literal plan-artifact authorization they
are reported to the user and recorded as `Reported without plan authorization`. Non-generalizable
entries are discarded with a one-line reason.
Two safety gates (secret/sensitivity and repo-relevance) run on every surviving entry before routing.

Archival is **BLOCKED** until every `learnings.md` entry reaches a terminal state — routed inline,
filed as a two-pager, reported without plan authorization, or discarded — or the plan carries the explicit
`No generalizable learnings — <reason>` escape. `learnings.md` is transient: nothing durable may
depend on it surviving past archival. Pure-docs and trivial plans are exempt from elaborate capture,
mirroring the specs/Gherkin exemption. See the
[Knowledge Capture Convention](../../../development/quality/knowledge-capture.md) for the complete
rubric, both safety gates, and the anti-theater guardrails.
