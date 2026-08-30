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
  `plans/ideas/<slug>.md` two-pager instead. The `learnings.md` entry records which path was taken
  (and the two-pager path, if filed).
- **`plans/ideas/` two-pager** (a non-code home): a **future-work idea** becomes a two-pager filed
  **inline** in the current plan's own commit/PR (creating one `plans/ideas/<slug>.md` is a small doc
  edit). Fold into an existing two-pager rather than duplicating. This routes the **pre-plan brief
  only** — any eventual code work still flows through a full backlog plan when the two-pager is
  promoted, carrying the code-routing gates above in full.

  **`plans/ideas/` is the only destination an executing agent may file new future work to.** A run
  MUST NOT create a `plans/backlog/<slug>/` folder for a finding it raised itself, however
  plan-ready it judges that finding to be. `backlog/` is reached only through
  [plan-idea-promotion-planning](../../../workflows/plan/plan-idea-promotion-planning.md), whose
  ripeness gate is the mechanism that decides an idea is plan-ready — an executing agent's own
  judgment is not a substitute for it, and self-assessed readiness is exactly the reasoning that
  bypasses the gate. A human MAY direct a specific finding straight to `backlog/`; that instruction
  is scoped to the findings it names and never generalizes to later ones raised by the same run.

- **Code homes** (`apps/`, `libs/`, tests): per the code-routing downstream rule above, **always** a
  separate follow-up — **never** inline, no exceptions besides the Iron Rule 3 current-plan-blocker
  carve-out. The run files the `plans/ideas/<slug>.md` two-pager; promotion turns it into the
  `plans/backlog/<slug>/` plan that carries the specs/Gherkin, regression-test, and TDD obligations.
- **Discard**: logged with a one-line reason; no further action.

Archival is **BLOCKED** until every `learnings.md` entry reaches one of three terminal states:

1. **Routed inline** (non-code homes only) — the edit has landed in this plan's own commits.
2. **Filed** as a `plans/ideas/<slug>.md` two-pager (any home; **mandatory** for code) — the entry
   records the two-pager path.
3. **Discarded** with a one-line reason.

Nothing is silently dropped, and nothing sits in an open, undecided state at archival time.
