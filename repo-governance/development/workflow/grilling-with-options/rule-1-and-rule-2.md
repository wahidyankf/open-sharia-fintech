---
title: "Rule 1 and Rule 2 — Explore Before Asking; Structured Options"
description: The requirement to read repo artifacts before grilling, and the 2-4 mutually-exclusive substantive-option cap.
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
when_to_use: Use before composing a grilling question, to confirm the answer isn't already discoverable and that the option count is within bounds.
---

# Rule 1 and Rule 2 — Explore Before Asking; Structured Options

## Rule 1 — Explore Before Asking

Before composing any grilling question, the agent MUST read the relevant repo artifacts. If
the answer to a potential question already exists in a convention file, a plan, or the
codebase, the agent MUST use that information directly and MUST NOT ask the user a question
that a file read could answer.

**Rationale**: Every unnecessary question erodes trust and wastes context. The repo is the
ground truth; the user is the tiebreaker for genuinely ambiguous decisions.

## Rule 2 — Structured Options (2-4, Mutually Exclusive)

Every grilling question MUST present between 2 and 4 concrete, mutually exclusive substantive
options. The options MUST collectively cover the realistic decision space. Beyond those
substantive options, every question ALSO carries two standing options — a free-form blank-state
write-in and a "chat about this" path (see
[Rule 8](./rule-7-and-rule-8.md#rule-8--two-standing-options-always-present-type-blank-state-and-chat)).
The two standing options do NOT count
against the 2-4 substantive cap, and the blank-state write-in MUST be surfaced explicitly,
never left merely implicit.

**Rationale**: Fewer than 2 options is a binary yes/no (use a confirmation prompt instead,
not a grill). More than 4 options overwhelms the user and signals the agent has not pruned
the decision space sufficiently.
