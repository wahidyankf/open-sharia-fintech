---
title: "Rule 5 and Rule 6 — One Decision Per Question; the Native-Tool Mechanism"
description: The rule that each question resolves exactly one decision (batching only tightly-coupled ones), and the opening statement of the native-tool-first mechanism.
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
when_to_use: Use when deciding whether two decisions may be batched into one grilling prompt, or when starting to render a grill through a native interactive tool.
---

# Rule 5 and Rule 6 — One Decision Per Question; the Native-Tool Mechanism

## Rule 5 — One Decision Per Question; Batch Only Tightly Coupled Decisions

Each grilling question MUST resolve exactly one decision branch. Tightly coupled decisions
(where the answer to one necessarily constrains the other) MAY be batched in a single
multi-question prompt. Unrelated decisions MUST NOT be bundled — present them as separate
questions, in the same grill session if needed.

**What counts as tightly coupled**: "Which layer should the convention live in?" and "What
filename should it use?" are tightly coupled (the filename depends on the layer choice).
These may appear together.

**What counts as unrelated**: "Which layer?" and "Should we update the README?" are
independent. Present them separately.

## Rule 6 — Mechanism: Native Interactive Tool First, Markdown Fallback

When the interactive root thread provides a native multiple-choice question tool, grilling MUST
use it. The native tool renders options as selectable UI elements and returns the user's choice as
structured data, eliminating parse ambiguity.
