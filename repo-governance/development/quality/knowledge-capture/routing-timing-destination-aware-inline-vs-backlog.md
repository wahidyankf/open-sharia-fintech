---
title: "Routing Timing: Destination-Aware (Inline vs. Backlog)"
description: "Inline routing versus backlog filing."
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
when_to_use: "Use when deciding inline fix vs. backlog plan."
---

# Routing Timing: Destination-Aware (Inline vs. Backlog)

Timing has a hard boundary determined by **destination**, not by convenience:

- **Non-code homes** (`docs/`, `repo-governance/`, `.claude/agents/`, `.claude/skills/`,
  `post-mortems/`, and any other non-code home): a **small** edit MAY land **inline** in the current
  plan's own commit/PR. A learning implying **large new work** becomes a tracked
  `plans/backlog/<slug>/` follow-up plan instead. The `learnings.md` entry records which
  path was taken (and the backlog path, if filed).
- **`plans/ideas/` two-pager** (a non-code home): a **future-work idea that is not yet plan-ready**
  becomes a two-pager filed **inline** in the current plan's own commit/PR (creating one
  `plans/ideas/<slug>.md` is a small doc edit). Distinguish from `backlog/`: a learning that is
  **already plan-ready** goes straight to a `plans/backlog/<slug>/` follow-up plan; a
  promising-but-unripe idea that still needs its own pitch/triage goes to `plans/ideas/`. Fold into an
  existing two-pager rather than duplicating. This routes the **pre-plan brief only** — any eventual
  code work still flows through a full backlog plan when the two-pager is promoted, carrying the
  code-routing gates above in full.
- **Code homes** (`apps/`, `libs/`, tests): per the code-routing downstream rule above, **always** a
  separate `plans/backlog/` plan — **never** inline, no exceptions besides the Iron Rule 3
  current-plan-blocker carve-out.
- **Discard**: logged with a one-line reason; no further action.

Archival is **BLOCKED** until every `learnings.md` entry reaches one of three terminal states:

1. **Routed inline** (non-code homes only) — the edit has landed in this plan's own commits.
2. **Filed** as a `plans/backlog/` plan (any home; **mandatory** for code) — the entry records the
   backlog folder path.
3. **Discarded** with a one-line reason.

Nothing is silently dropped, and nothing sits in an open, undecided state at archival time.
