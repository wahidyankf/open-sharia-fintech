---
title: "Comprehensive Decision Records"
description: Defines the audience, end-to-end purpose, alternatives, and prior-art record required in formal plans.
category: explanation
subcategory: conventions
tags: [conventions, plans, decisions, readability]
created: 2026-08-30
when_to_use: Use when authoring or reviewing the reasoning and context in a formal plan.
---

# Comprehensive Decision Records

## Purpose

A formal plan preserves the complete route from evidence to delivery. Its reader is a junior
engineer fresh from bootcamp with no professional work experience and no repository or stack
context, including no product, framework, or conversational context.

The primary teaching and execution surfaces are the selected technical form (`tech-docs.md` or the
mapped `tech-docs/`) and `delivery.md`. Summary files may orient the reader, but they cannot carry
missing technical context or compensate for an under-specified delivery checklist.

## Standards

- Treat a **material decision** as a substantive choice that changes the proposed product,
  architecture, implementation contract, delivery boundary, rollout, operation, testing strategy,
  or recovery behavior. Record why that solution choice was selected.
- Do not turn the plan into a changelog of its own authoring process. Wording changes, section
  moves, checker/fixer findings, drafting order, rejected phrasing, and other editorial iterations
  are not decision-record alternatives unless they change the delivered contract. Git history and
  review threads carry that editorial history.
- Make the journey traceable: evidence and current state; goal and non-goals; viable options and
  prior art; decision and consequences; requirements and design; delivery and proof; rollout,
  rollback, and learnings.
- Define relevant repository and product terms. Explain affected stack concepts or link their
  canonical documentation at the point of use. Show current and target flows when prose would make
  the reader reconstruct them.
- In the selected technical form, teach enough current state, stack concepts, alternatives,
  contracts, architecture, dependencies, migration/rollback mechanics, and verification design for
  that junior engineer to understand why the delivery is shaped this way.
- In `delivery.md`, translate that design into ordered, granular actions with prerequisites, exact
  paths or bounded discovery, copyable commands, expected observations, failure handling, evidence,
  and separate RED/GREEN/REFACTOR tasks where code changes. The same junior engineer must be able to
  execute it without author or chat assistance.
- Leave no product, security, data, migration, UI, testing, rollout, or rollback behavior for the
  reader to invent. Use exact paths, commands, and contracts where they materially remove ambiguity.
- For every material decision, record the selected option and at least two viable alternatives,
  including the status quo when it is genuinely viable. Record evidence, constraints, trade-offs,
  rejection reasons, consequences, and revisit triggers.
- Search repository documentation and history first, then cite applicable external prior art. When
  fewer than three viable options exist, record the search and the constraints that disqualify the
  missing options; never fabricate alternatives to satisfy a count.

## Examples

A storage decision compares the existing store, an extension of it, and a new store. It explains
why each can meet the goal, why one is selected, the operational consequence, and the condition
that would reopen the choice. A claim that “the new store is best” without this record fails.

## Validation

Plan quality review asks whether the stated audience can trace the decision-to-delivery journey
without asking the author or relying on chat history. It rejects plan-authoring changelogs presented
as solution alternatives. Deterministic gates do not judge readability or the viability of
alternatives.
