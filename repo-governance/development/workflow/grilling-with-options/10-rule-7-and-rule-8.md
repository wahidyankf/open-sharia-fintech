---
title: "Rule 7 and Rule 8 — Unlisted Answers; Standing Options"
description: The rule that a user's write-in answer always counts, and the two standing options every grilling question must carry.
category: explanation
subcategory: development
tags:
  - planning
  - grill-me
  - user-interaction
  - plan-maker
  - design-decisions
  - interaction
  - agents
created: 2026-05-26
when_to_use: Use when a user supplies an unlisted answer, or when checking whether a question surfaces both the blank-state type option and the chat option.
---

# Rule 7 and Rule 8 — Unlisted Answers; Standing Options

## Rule 7 — User Can Always Supply an Unlisted Answer

Options are a structured starting point, not a closed cage. The agent MUST treat a user's
write-in answer with the same weight as a listed option. If the write-in answer opens a new
decision branch, the agent grills on that branch before proceeding.

## Rule 8 — Two Standing Options Always Present: Type (Blank State) and Chat

Beyond its 2-4 substantive options, every grilling question MUST ALWAYS surface two standing
options, on every question, regardless of rendering mechanism:

1. **Type (blank state)** — an explicit free-form write-in path whose answer depends entirely
   on what the user types. This is NOT optional and NOT merely implicit: it MUST be visible on
   every question. When a native tool auto-provides a free-text "Other" entry, that entry
   satisfies this requirement; with the markdown fallback, an explicit
   `**Other — type your own answer**` bullet MUST be listed.
2. **Chat about this** — an explicit option signalling the user wants to discuss the decision
   conversationally before committing, rather than pick a listed option or write a final
   answer. When the user selects it, the agent drops the structured options, talks the branch
   through in prose, then returns to a structured question once the user is ready to decide.

These two standing options do NOT count against the 2-4 substantive cap; they are universal
escape hatches present on every question, not decision branches.

**Rationale**: Structured options accelerate the common path, but a user must never be boxed
in. The blank-state type guarantees the user can always answer in their own words; the chat
option guarantees they can always reopen the decision for discussion. Dropping either —
especially the blank-state type, the single most common omission — turns a grill into a forced
choice.
