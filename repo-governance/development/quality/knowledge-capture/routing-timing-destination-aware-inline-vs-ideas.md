---
title: "Routing Timing: Destination-Aware (Inline vs. Ideas)"
description: "Inline routing versus explicitly authorized plans/ideas filing."
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
when_to_use: "Use when deciding inline fix vs. an explicitly authorized plans/ideas two-pager."
---

# Routing Timing: Destination-Aware (Inline vs. Ideas)

Timing has a hard boundary determined by **destination**, not by convenience:

**Hard boundary:** Knowledge Capture MUST NOT create `plans/backlog/` directly. Its only permitted
new future-work artifact is an explicitly authorized `plans/ideas/` two-pager after the overlap
scan. Without literal authorization, use `Reported without plan authorization`. Promotion from an
idea to backlog belongs exclusively to the idea-promotion workflow.

- **Non-code homes** (`docs/`, `repo-governance/`, `.claude/agents/`, `.claude/skills/`,
  `post-mortems/`, and any other non-code home): a **small** edit MAY land **inline** in the current
  plan's own commit/PR. A learning implying **large new work** becomes a tracked
  `plans/ideas/<slug>.md` two-pager only when the user literally authorizes that plan artifact.
  Otherwise report it to the user and record `Reported without plan authorization` with the report
  location or conversation handoff.
- **`plans/ideas/` two-pager** (a non-code home): future work becomes a two-pager only when the user
  literally authorizes that artifact. Fold into an existing two-pager rather than duplicating. Do
  not create a backlog folder directly; the idea-promotion workflow owns the evidence-backed
  transition to a formal backlog plan and carries the code-routing gates forward.
- **Code homes** (`apps/`, `libs/`, tests): per the code-routing downstream rule above, never inline.
  File a separate `plans/ideas/` two-pager only with literal authorization; otherwise use the
  reported terminal state. Never create its backlog folder directly. The Iron Rule 3
  current-plan-blocker carve-out remains unchanged.
- **Discard**: logged with a one-line reason; no further action.

Archival is **BLOCKED** until every `learnings.md` entry reaches one of four terminal states:

1. **Routed inline** (non-code homes only) — the edit has landed in this plan's own commits.
2. **Filed** as an explicitly authorized `plans/ideas/` two-pager — the entry records its path.
3. **Reported without plan authorization** — the entry records the handoff evidence and no plan is created.
4. **Discarded** with a one-line reason.

Nothing is silently dropped, and nothing sits in an open, undecided state at archival time.
