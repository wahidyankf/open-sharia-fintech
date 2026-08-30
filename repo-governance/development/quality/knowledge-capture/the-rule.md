---
title: "The Rule"
description: "The core knowledge-capture rule."
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
when_to_use: "Use for the exact wording of the rule."
---

# The Rule

**Every substantive plan MUST accrue a transient `learnings.md` running log during execution and
MUST triage every surviving entry through this convention's open-ended routing matrix, applying both
safety gates, before the plan is archived to `plans/done/`.** Archival is blocked until every entry
reaches a terminal state: routed inline, filed as a `plans/ideas/` two-pager follow-up, or discarded
with a one-line reason. A plan MAY record the explicit `No generalizable learnings — <reason>` escape
instead of individual entries, but it may never leave `learnings.md` silently empty.
