---
title: "The Transient-Log Caveat"
description: "Why learnings.md is never a durable home."
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
when_to_use: "Use when deciding if content still needs routing."
---

# The Transient-Log Caveat

**`learnings.md` is transient scaffolding. It is NEVER the system of record.**

`plans/done/*/learnings.md` MAY be deleted at any future date — `plans/done/` is a historical
record of plan execution, not a permanent knowledge archive. Consequently:

- Everything worth keeping from a learning MUST be routed to a durable home (a convention, a doc, an
  agent, a skill, code, a test, or a post-mortem) **before** archival. Routing-out is mandatory
  pre-archival, not optional cleanup.
- **No process, agent, or future plan may depend on querying `learnings.md` later.** If something in
  a `learnings.md` entry matters, it must already live somewhere durable by the time the plan is
  archived. Treat `learnings.md` as safe to delete the moment its entries are all terminal.
- This caveat is why the routing matrix's timing rule (inline vs. backlog) and the mandatory-terminal
  rule at archival both exist: they are what actually makes `learnings.md`'s transience safe.
