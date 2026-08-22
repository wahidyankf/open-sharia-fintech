---
title: "Review as Teaching — Every Finding Is Legible to a Junior Engineer"
description: "Binds review findings and replies to be understandable by someone still learning the codebase, and separates critique of code from judgement of people."
category: explanation
subcategory: development
tags:
  - pr-review
  - governance
  - agents
  - quality-gates
created: 2026-08-22
when_to_use: "Use when writing a review finding or a fixer reply."
---

# Review as Teaching — Every Finding Is Legible to a Junior Engineer

A PR review is the most-read technical writing this repo produces, and its thread is permanent.
Someone new to the codebase learns more from reading past reviews than from any document written
to be read. That makes legibility a requirement of the finding, not a courtesy — a finding only a
specialist can decode teaches nobody, and the review culture it builds is one where people stop
reading.

## What Every Finding Carries

- **The consequence, in plain terms.** What actually breaks, and for whom. `file:line` and a rule
  citation say _where_ and _which rule_; neither says _why it matters_. One sentence.
- **The rule paraphrased, not merely linked.** A bare path is a lookup task. State what the rule
  requires in the finding itself and link for the detail.
- **Terms of art defined on first use**, or replaced with plain words. Precision survives
  translation; jargon is not precision.
- **Enough context to act without prior knowledge of the discussion.** Never "as discussed."

## What Every Reply Carries

A fixer reply is half the conversation. `Fixed: <what changed>` states the change; the reply also
states **why that change resolves the finding**. A rejection explains the reasoning so a reader
learns the boundary, not just the outcome — a rejection nobody can follow reads as a dismissal
even when it is correct.

## Critique the Change, Never the Author

Anti-sycophantic framing means stating plainly what is wrong. It does not license contempt.
Address the code and the consequence; never the competence, care, or motive of whoever wrote it.
These are compatible: the clearest findings are blunt about the defect and neutral about the
person.

## Not a Licence to Pad

Teaching is a sentence of consequence, not an essay, and the
[governance word budget](../../../conventions/structure/governance-word-budget.md) still applies.
A finding that lectures fails this rule as surely as one that explains nothing.

## Enforcement

None automated. `pr-review-synthesis-maker`'s reasonableness filter already drops a finding
stating a defect no reader could act on, and a finding failing this rule is exactly that: an
unactionable finding. The filter is where it dies.
